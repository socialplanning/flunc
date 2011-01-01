import optparse 
import sys
import os 
import urllib
import re
import time

import twill 
from twill.namespaces import get_twill_glocals

from parser import parse_test_call, make_dict_from_call, make_twill_local_defs
from logging import log_info, log_warn, log_error, output_stream

CONFIGURATION      = '.conf'
SUITE              = '.tsuite'
TEST               = '.twill' 
CLEANUP            = '_cleanup'
CONFIG_OVERRIDE_SCRIPT   = None
CONFIG_OVERRIDE_DICT = {}
PATH_SEP  = '.'

options = {}
name_lookup = {}

class Namespace(object):


    def __init__(self, directory, base_namespace=None):

        # tests, suites, and associated data
        self.tests = {}
        self.suites = {}
        self.conf = {}
        self.cleanup = {}
        self.data = ( 'tests', 'suites', 'conf', 'cleanup' )

        self.directory = directory

        # if the base namespace is not specified, 
        # then this namespace is top-level
        if base_namespace is None: 
            base_namespace = self

        if not os.path.isdir(directory):
            die("Test directory not found (%s). Use -p to specify test search path" % directory)

        self.base = base_namespace
        self.scan_for_tests()
        files = [ os.path.join(self.directory, i)
                  for i in os.listdir(self.directory) 
                  if not i.startswith('.') ] # don't include dotfiles
        self.namespaces = [ Namespace(i, base_namespace) 
                            for i in files
                            if os.path.isdir(i) ]
        self.namespaces = [ i for i in self.namespaces
                            if i.tests ]
        self.namespaces = dict([(i.name(), i) 
                                for i in self.namespaces])

    def get(self, path, _type):
        path = path.split(PATH_SEP)
        if len(path) == 1:
            item = getattr(self, _type).get(path[0])
            if item:
                return item
        else:
            ns = self.namespaces.get(path[0])
            if ns:
                return ns.get(PATH_SEP.join(path[1:]), _type=_type)

        # if not found in the current namespace, try the global
        if self.base is not self:
            return self.base.get(PATH_SEP.join(path), _type)

    def lookup(self, path, set_current=True, types=('suites', 'tests')):
        """
        return a test and set the current namespace for that test
        returns None if the test is not found
        """

        global current_namespace
        path = path.split(PATH_SEP)
        if len(path) == 1:
            for _type in types:
                item = getattr(self, _type).get(path[0])
                if item:
                    if set_current:
                        current_namespace.append(self)
                    return path[0]
                elif _type == 'suites': # XXX hack
                    ns = self.namespaces.get(path[0])
                    if ns:
                        suite = ns.suites.get(path[0])
                        if suite:
                            if set_current:  # XXX this should be true here
                                current_namespace.append(ns)
                            return path[0]
        else:
            ns = self.namespaces.get(path[0])
            if ns:
                return ns.lookup(PATH_SEP.join(path[1:]))

        # if not found in the current namespace, try the global
        if self.base is not self:
            return self.base.lookup(PATH_SEP.join(path), set_current=set_current, types=types)


    def flatten(self):
        """flattens the namespace"""
        for namespace in self.namespaces.values():
            namespace.flatten()

            # updat the data
            for item in self.data:
                getattr(self, item).update(getattr(namespace, item))

        # delete the namespaces
        self.namespaces = {} 

    def scan_for_tests(self): 
        """
        scans for relevant files in the directory given.
        """
        log_info("scanning for tests in '%s'" % self.directory)
        for filename in os.listdir(self.directory):
            base, ext = os.path.splitext(filename)
            fullname = os.path.join(self.directory, filename)
            if ext == SUITE:
                if base.endswith(CLEANUP):
                    base = base.rsplit(CLEANUP, 1)[0]
                    self.cleanup[base] = fullname
                else:
                    self.suites[base] = fullname
            if ext == CONFIGURATION:
                self.conf[base] = fullname
            if ext == TEST:
                self.tests[base] = fullname

    def name(self):
        return os.path.split(self.directory)[-1]
        

# add ability to redirect requests to different hosts
import monkey
monkey.patch_browser()
hostname_redirect_mapping = {}

def define_twill_vars(**kwargs): 
    tglobals, tlocals = get_twill_glocals()
    tglobals.update(kwargs)

def read_file_type(name, ext): # XXX still needed?
    try:
        filename = name_lookup[name + ext]
    except KeyError:
        if name.startswith('/'):
            filename = name
        else:
            raise IOError('Unable to locate %s in the search path' % (name + ext))
    return open(filename).read()
    
def list_suites():
    names = name_lookup.suites.keys()
    names.sort()
    
    for name in names:
        base, ext = os.path.splitext(name)
        full = name_lookup.suites[name]
        found_suite = True 
        print '%s' % base
        print '  from %s' % rel_filename(full)
        f = open(full)
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if not line.startswith('#'):
                # End of comment header
                break
            line = line.lstrip('# ')
            print '    %s' % line
            
    if not names:
        print "No suites found"

def rel_filename(filename, relative_to=None):
    """
    returns the filename, shortened by seeing if it is relative
    to the given path (CWD by default)
    """
    if relative_to is None:
        relative_to = os.getcwd()
    if not relative_to.endswith(os.path.sep):
        relative_to += os.path.sep
    filename = os.path.normpath(os.path.abspath(filename))
    if filename.startswith(relative_to):
        return filename[len(relative_to):]
    else:
        return filename

def read_configuration(name):
    filename = current_namespace[-1].conf.get(name)
    if filename is None:
        filename = name
    conftext = file(filename).read()
    lines = conftext.split('\n')
    output = []
    for line in lines:
        tokens = line.strip().split()
        if tokens and tokens[0] == 'include':
            for includename in tokens[1:]:
                _includename = current_namespace[-1].get(includename, _type='conf')
                if _includename is None:
                    raise NameError('including configuration file %s from %s not found' % ( includename, name ))
                else:
                    log_info('including config %s' % includename)
                    output.append(read_configuration(_includename))
        else:
            output.append(line)
    return '\n'.join(output)

def read_test(name):
    filename = current_namespace[-1].get(name, _type='tests')
    if filename is None:
        raise NameError('test %s not found' % name)
    return file(filename).read()

def has_cleanup_handler(name):
    return current_namespace[-1].cleanup.has_key(name)

def parse_suite(suite_data): 
    lineno = 0 
    calls = [] 
    for line in suite_data.splitlines(): 
        lineno = lineno + 1
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        calls.append(parse_test_call(line) + (lineno,))

    return calls 

def maybe_print_stack(): 
    if options.verbose:
        import traceback
        traceback.print_exception(*sys.exc_info())

def do_twill_repl():
    welcome_msg = "\n interactive twill debugger. type 'help' for options\n"
    
    repl = twill.shell.TwillCommandLoop()

    while 1:
        try:
            repl.cmdloop(welcome_msg)
        except KeyboardInterrupt:
            sys.stdout.write('\n')
        except SystemExit:
            raise

def handle_exception(msg, e):
    maybe_print_stack()
    log_error("Caught exception at %s" %
              time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    html = twill.get_browser().get_html()
    if options.dump_file == '-':
        print html
    else:
        dump_file_name = os.path.expanduser(options.dump_file)
            
        try:
            if html is not None:
                if options.show_error_in_browser:
                    # If we are showing it in the browser, lets get the
                    # paths right (even if if means changing the HTML a
                    # little)
                    base_href = '\n<!-- added by flunc: --><base href="%s">' % twill.get_browser().get_url()
                    match = re.search('<head.*?>', html, re.I|re.S)
                    if match:
                        html = html[:match.end()] + base_href + html[match.end():]
                    else:
                        html = base_href + html
                f = open(dump_file_name, 'wb')
                f.write(html)
                f.close()
                log_info("saved error html to: %s" % dump_file_name)
        except IOError, e:
            log_warn("Unable to save error HTML to: %s" % dump_file_name)

    if e.args:
        log_error("%s (%s)" % (msg,e.args[0]))
    else:
        log_error(msg)

    if options.show_error_in_browser:
        if options.dump_file == '-': 
            log_warn("Web browser view is not supported when dumping error html to standard out.")
        else:
            try:
                log_info("Launching web browser...")
                import webbrowser
                path = os.path.abspath(os.path.expanduser(options.dump_file))
                webbrowser.open('file://' + path)            
            except: 
                maybe_print_stack()
                log_error("Unable to open current HTML in webbrowser")
        

    if options.interactive:
        try: 
            do_twill_repl()
        except Exception:
            pass 
                
    if not options.ignore_failures: 
        sys.exit(1)


def do_cleanup_for(name):
    if has_cleanup_handler(name) and not options.no_cleanup_mode: 
        log_info("running cleanup handler for %s" % name)
        try:
            suite_data = file(current_namespace[-1].cleanup[name]).read()
            calls = parse_suite(suite_data)
            for script,args,line in calls:
                try:
                    if current_namespace[-1].suites.get(script):
                        log_warn("Cannot call sub-suite %s during cleanup at %s(%d)" % (script,name,line))
                    else:
                        log_info("running cleanup: %s" % name)
                        script_data = read_test(script)
                        try:
                            parameters = make_dict_from_call(args,get_twill_glocals()[0])
                        except (ValueError, TypeError, SyntaxError), e:
                            e.args = ("\"%s%s\": Only positional argument passing is supported in suites." % \
                                          (name, args), ) + e.args[1:]
                            raise e
                        script_data = make_twill_local_defs(parameters) + script_data 
                        twill.execute_string(script_data, no_reset=1)
                except Exception, e:
                    maybe_print_stack() 
                    log_warn("Cleanup call to %s failed at %s(%d)" 
                         % (script + args, name + CLEANUP, line))
        except IOError,e:
            maybe_print_stack()
            log_warn("Unable to read cleanup handler for %s" % name)
        except Exception,e:
            maybe_print_stack()
            log_warn("Exception during cleanup handler for %s" % name)


def load_overrides(): 
    if CONFIG_OVERRIDE_SCRIPT: 
        try:
            twill.execute_string(CONFIG_OVERRIDE_SCRIPT, no_reset=1)
        except Exception, e:
            handle_exception('Error in global configuration overrides', e)
    if CONFIG_OVERRIDE_DICT:
        define_twill_vars(**CONFIG_OVERRIDE_DICT)

def load_configuration(name):
    filename = current_namespace[-1].conf.get(name)
    if filename:
        try: 
            configuration = read_configuration(name)
            twill.execute_string(configuration, no_reset=1)
            log_info("loaded configuration: %s" % (name + CONFIGURATION))
        except IOError,e: 
            handle_exception("Unable to read configuration for suite %s" \
                             % (name + SUITE), e)
        except Exception,e:
            handle_exception("Invalid configuration: '%s'" \
                             % (name + CONFIGURATION), e)
    else:
        log_warn("Unable to locate configuration for suite %s" 
             % (name + SUITE))

def run_suite(name):
    try: 
        if not options.cleanup_mode:
            log_info("running suite: %s" % name)
            output_stream.indent()
        try:
        
            suite_data = file(current_namespace[-1].suites[name]).read()
            calls = parse_suite(suite_data)
        
            load_configuration(name)
            load_overrides() 

            error_list = [] 
            # skip running suites if cleanup-only mode is set 
            if not options.cleanup_mode:
                for script,args,line in calls: 
                    errors = run_test(script,args)
                    if len(errors):                     
                        error_list += [name + "(%d)::%s" % (line,x) for x in errors if x]
            return error_list
        except IOError,e: 
            handle_exception("Unable to read suite %s" % name,e)
            return [name]
    finally: 
        do_cleanup_for(name)
        output_stream.outdent()

def run_test(name,args):

    # this pushes the correct namespace on the stack
    # should be popped
    test = current_namespace[-1].lookup(name)
    if test is None:
        raise NameError("Unable to locate %s or %s in search path" %
                        (name + TEST, name + SUITE))
    name = test

    current = current_namespace[-1]
    try:
        if current.suites.get(name):
            if args:
                log_warn("Arguments provided to suites are ignored! [%s%s]" 
                         % (name,args))
            return run_suite(name)
        elif current.tests.get(name):

            # don't do anything in cleanup only mode 
            if options.cleanup_mode:
                return []

            try:
                log_info("running test: %s" % name)
                output_stream.indent()
                try:            
                    script = file(current.tests[name]).read()
                    try:
                        parameters = make_dict_from_call(args,get_twill_glocals()[0])
                    except (ValueError, TypeError, SyntaxError), e:
                        e.args = ("\"%s%s\": Only positional argument passing is supported in suites." % \
                                      (name, args), ) + e.args[1:]
                        raise e
                    script = make_twill_local_defs(parameters) + script
                    twill.execute_string(script, no_reset=1)
                    return []
                except IOError, e: 
                    handle_exception("Unable to read test '%s'" % (name + TEST), e)
                    return [name]
                except Exception, e: 
                    handle_exception("Error running %s" % name, e)
                    return [name]
            finally:
                output_stream.outdent()
    finally:
        current_namespace.pop()

def die(message, parser=None):
    message = str(message)
    log_error(message)
    if parser is not None:
        parser.print_usage()
    sys.exit(0)

def set_use_tidy(value):
    setting = int(bool(value))
    twill.execute_string("config use_tidy %d" % value, no_reset=1)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser, usage = get_optparser()

    global options 
    options, args = parser.parse_args(argv)

    global name_lookup
    directory = os.path.expanduser(options.search_path)
    name_lookup = Namespace(directory)
    global current_namespace
    current_namespace = [name_lookup]

    if options.recursive:
        name_lookup.flatten()

    if options.list_suites:
        list_suites()
        return

    if len(args) < 2: 
        die("No tests specified", parser)

    if options.cleanup_mode and options.no_cleanup_mode:
        die("Conflicting options specified, only one of cleanup-mode, no-cleanup-mode may be specified.",parser)

    # showing an error in the browser implies interactive mode
    if options.show_error_in_browser:
        options.interactive = True

    if options.browser: 
        os.environ['BROWSER'] = options.browser

    scheme, uri = urllib.splittype(options.base_url)
    if scheme is None: 
        log_warn("no scheme specified in test url, assuming http")
        options.base_url = "http://" + options.base_url 
    elif not scheme == 'http' and not scheme == 'https':
        die("unsupported scheme '%s' in '%s'" % (scheme,options.base_url))
    
    host, path = urllib.splithost(uri)

    log_info("Running against %s, host: %s path=%s" % \
        (options.base_url,host,path))
    # define utility variables to help point scripts at desired location
    define_twill_vars(base_url=options.base_url)
    define_twill_vars(base_host=host)
    define_twill_vars(base_path=path)
    define_twill_vars(test_path=os.path.realpath(options.search_path))

    # use the base_url if the cleanup_base_url was not specified
    if options.cleanup_base_url is None:
        options.cleanup_base_url = options.base_url
    define_twill_vars(cleanup_base_url=options.cleanup_base_url)
    
    if options.config_file: 
        try: 
            global CONFIG_OVERRIDE_SCRIPT 
            CONFIG_OVERRIDE_SCRIPT = read_configuration(options.config_file)
            log_info("Loaded global config overrides: %s" % options.config_file)
        except IOError, msg:
            die(msg)

    if options.global_defines:
        try:
            CONFIG_OVERRIDE_DICT.update(
                dict([x.split('=') for x in options.global_defines.split(',')])
                )
        except Exception, msg:
            die('Error parsing global definitions (%s): %s' % (options.global_defines, msg))

    if options.cleanup_mode:
        log_info("Running in Cleanup-Only mode")

    if options.host_file is not None:
        try:
            map_file = open(options.host_file)
            lines = [x.strip() for x in map_file]
            lines = [x for x in lines if x and not x.startswith('#')]
            mapping = [x.split() for x in lines]
            mapping = [x for x in mapping if len(x) == 2]
            hostname_redirect_mapping.update(dict(mapping))
            if options.verbose:
                log_info('[*] mapping\n%s' % (
                    '\n'.join(['%s -> %s' % (a, b) for a, b in mapping])))
        except IOError:
            pass

    set_use_tidy(options.use_tidy)

    twill.execute_string("add_extra_header 'Accept-Language' '%s'" % options.language)   

    try:
        error_tests = [] 
        calls = map(parse_test_call,args[1:])
        for name,args in calls: 
            load_overrides()
            error_tests += run_test(name,args)
    except SystemExit:
        raise
    except Exception, e:
        handle_exception("ERROR",e)
    else:
        nerrors = len(error_tests)
        if options.cleanup_mode:
            log_info('Cleanup Complete.')
        elif nerrors == 0:
            log_info('All Tests Passed!')
        else:
            log_info('%d Errors Found' % nerrors)
            log_info('Failing Tests:\n%s' % '\n'.join(error_tests))

def get_optparser():
    base_dir = os.path.dirname(os.path.dirname(__file__))
#    ftest_dir = rel_filename(os.path.join(base_dir, 'ftests')) # does not exist
#    if not ftest_dir.startswith(os.path.sep):
        # Suppress optparse's word wrapping:
#        ftest_dir = '.'+os.path.sep+ftest_dir
    ftest_dir = '.'
    usage = "usage: %prog [options] <test name> [test name...]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-t', '--host',
                      help='specifies the base url of the portal to test [default: %default]',
                      dest='base_url',
                      default='http://localhost/')
    parser.add_option('-T', '--cleanup-host',
                      help='specifies the base url of the portal to run the cleanup scripts against [default: base_url]',
                      dest='cleanup_base_url',
                      default=None)
    parser.add_option('-c', '--config',
                      help='specifies file with configuration overrides',
                      dest='config_file')
    parser.add_option('-D', '--define',
                      help="specifies configuration overrides as a comma separated list of name='value' pairs",
                      dest='global_defines')
    parser.add_option('-l', '--list',
                      dest='list_suites',
                      action='store_true',
                      help="List the available suites (don't test anything)")
    parser.add_option('-p', '--path',
                      dest='search_path',
                      default=ftest_dir, 
                      help='specifies location to search for tests [default: %default]')
    parser.add_option('-r', '--recursive',
                      dest='recursive',
                      action='store_true',
                      help="search recursively for tests in the search path and puts them in a flat namespace")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      help="Display stack traces from twill")
    parser.add_option('-i', '--interactive-debug',
                      dest='interactive',
                      action='store_true',
                      help="Fall into twill shell on error")
    parser.add_option('-C', '--cleanup-only',
                      dest='cleanup_mode',
                      action='store_true',
                      help="Only run cleanup handlers for suites given.")
    parser.add_option('-X', '--no-cleanup',
                      dest='no_cleanup_mode',
                      action='store_true',
                      help="Do not run cleanup handlers.")
    parser.add_option('-F', '--ignore-failures',
                      dest='ignore_failures',
                      action='store_true',
                      help="continue running tests after failures")
    parser.add_option('-d', '--dump-html',
                      dest='dump_file',
                      default='err.html',
                      help="set file to dump HTML to when an error is encountered.  specify - for stdout. [default: %default]")
    parser.add_option('-w', '--show-error-in-browser', 
                      dest='show_error_in_browser', 
                      action='store_true',
                      help="show dumped HTML in a web browser on error, forces interactive mode")
    parser.add_option('-b','--browser',
                      dest='browser',
                      default='firefox', 
                      help="specifies web browser to use when viewing error pages [default: %default]")
    parser.add_option('-m','--host-mapping',
                      dest='host_file',
                      default=None, 
                      help="Specifies host mapping file to use. Syntax in file is old-host new-host")
    parser.add_option('-y','--use-tidy',
                      dest='use_tidy',
                      default=False,
                      action="store_true",
                      help="Specifies whether to use tidy or not")
    parser.add_option('-L', '--language',
                      dest='language',
                      default='az, en', 
                      help='Specifies what language to request in the http headers [default: %default]')
    return parser, usage

if __name__ == '__main__':
    main(sys.argv)
