import optparse 
import sys
import os 
import urllib
import twill 
from twill.namespaces import get_twill_glocals

from parser import parse_test_call, make_dict_from_call, make_twill_local_defs

CONFIGURATION      = '.conf'
SUITE              = '.tsuite'
TEST               = '.twill' 
CLEANUP            = '_cleanup'
CONFIG_OVERRIDES   = None

options = {}
name_lookup = {}

def define_twill_vars(**kwargs): 
    tglobals, tlocals = get_twill_glocals()
    tglobals.update(kwargs)

def read_file_type(name, ext): 
    try: 
        filename = name_lookup[name + ext]
        return open(filename).read()
    except KeyError:
        raise IOError('Unable to locate %s in the search path' % (name + ext))

def file_exists(name,ext):
    return name_lookup.has_key(name + ext)

def scan_for_tests(root): 
    """
    recursively scans for relevant files in the directory given
    """
    log_info("scanning for tests in '%s'" % root)
    found = {} 

    def check_files(files):
        for filename in files: 
            base, ext = os.path.splitext(filename)
            if ext in (TEST, SUITE, CONFIGURATION):
                if filename in found: 
                    log_warn("ignoring %s in %s (already found: %s)" % \
                         (filename, root, found[filename]))
                else: 
                    found[filename] = os.path.join(root, filename)
                    

    if options.recursive:
        # XXX this is DFS, it probably should do BFS ? 
        for root, dirs, files in os.walk(root): 
            check_files(files)
    else: 
        check_files(os.listdir(root))
        
                
    return found 

    
def list_suites():
    names = name_lookup.keys()
    names.sort()
    
    found_suite = False 
    for name in names:
        base, ext = os.path.splitext(name)
        full = name_lookup[name]

        if ext != SUITE or base.endswith(CLEANUP):
            continue
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
    if not found_suite:
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
    return read_file_type(name, CONFIGURATION)

def read_suite(name): 
    return read_file_type(name, SUITE)

def read_test(name): 
    return read_file_type(name, TEST)

def has_cleanup_handler(name):
    return file_exists(name + CLEANUP, SUITE)

def read_cleanup_for(name):
    return read_file_type(name + CLEANUP, SUITE)

def parse_suite(suite_data): 
    valid_line = lambda line: line.strip() and\
                              not line.lstrip().startswith('#')
    return map(parse_test_call,filter(valid_line, suite_data.splitlines()))

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
    
    if options.dump_file:
        html = twill.get_browser().get_html()
        if options.dump_file == '-':
            print html
        else:
            try:
                open(options.dump_file, 'w').write(html)
                log_info("saved html to: %s" % options.dump_file)
            except IOError, e:
                log_warn("Unable to save to: %s" % options.dump_file)

    if e.args:
        log_error("%s (%s)" % (msg,e.args[0]))
    else:
        log_error(msg)

    if options.show_error_in_browser:
        try:
            log_info("Launching web browser...")
            import webbrowser
            path = os.path.abspath(options.dump_file)
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
    if has_cleanup_handler(name): 
        log_info("running cleanup handler for %s" % name)
        try:
            suite_data = read_cleanup_for(name)
            calls = parse_suite(suite_data)
            for script,args in calls:
                try:
                    if file_exists(script,SUITE):
                        log_warn("Cannot call sub-suite %s during cleanup." % name)
                    else:
                        run_test(script,args)
                except Exception, e:
                    maybe_print_stack() 
                    log_warn("Cleanup call to %s failed." 
                         % (script + args))
        except IOError,e:
            maybe_print_stack()
            log_warn("Unable to read cleanup handler for %s" % name)
        except Exception,e:
            maybe_print_stack()
            log_warn("Exception during cleanup handler for %s" % name)


def load_overrides(): 
    if CONFIG_OVERRIDES: 
        try:
            twill.execute_string(CONFIG_OVERRIDES, no_reset=1)
        except Exception, e:
            handle_exception('Error in global configuration', e)

def load_configuration(name): 
    if file_exists(name,CONFIGURATION):
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
        try:
            log_info("running suite: %s" % name)
            suite_data = read_suite(name)
            calls = parse_suite(suite_data)
        
            load_configuration(name)
            return run_tests(calls)
        except IOError,e: 
            handle_exception("Unable to read suite %s" % name,e)
            return 1
    finally: 
        do_cleanup_for(name)

def run_tests(calls): 
    return sum(run_test(name, args) for name, args in calls)

def run_test(name,args): 
    if file_exists(name, SUITE):
        if args:
            log_warn("Arguments provided to suites are ignored! [%s%s]" 
                 % (name,args))
        return run_suite(name)
    elif file_exists(name, TEST): 
        load_overrides()
        
        try:
            log_info("running test: %s" % name)
            script = read_test(name)
            script = make_twill_local_defs(make_dict_from_call(args,get_twill_glocals()[0])) + script 
            twill.execute_string(script, no_reset=1)
            return 0
        except IOError, e: 
            handle_exception("Unable to read test '%s'" % (name + TEST), e)
            return 1
        except Exception, e: 
            handle_exception("Error running %s" % name, e)
            return 1
    else:
        raise NameError("Unable to locate %s or %s in search path",
                        (name + TEST, name + SUITE))

def log_error(msg):
    print "[X] Error:", msg 

def log_warn(msg):
    print "[!] Warning:", msg 

def log_info(msg):
    print "[*]", msg 

def die(message, parser=None): 
    print message 
    if parser is not None:
        parser.print_usage()
    sys.exit(0)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    base_dir = os.path.dirname(os.path.dirname(__file__))
    ftest_dir = rel_filename(os.path.join(base_dir, 'ftests'))
    if not ftest_dir.startswith(os.path.sep):
        # Suppress optparse's word wrapping:
        ftest_dir = '.'+os.path.sep+ftest_dir
    usage = "usage: %prog [options] <test name> [test name...]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-t', '--host',
                      help='specifies the base url of the portal to test [default: %default]',
                      dest='base_url',
                      default='http://localhost:8080/portal')
    parser.add_option('-c', '--config',
                      help='specifies file with configuration overrides',
                      dest='config_file')
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
                      help="search recursively for tests in the search path")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      help="Display stack traces from twill")
    parser.add_option('-i', '--interactive-debug',
                      dest='interactive',
                      action='store_true',
                      help="Fall into twill shell on error")
    parser.add_option('-F', '--ignore-failures',
                      dest='ignore_failures',
                      action='store_true',
                      help="continue running tests after failures")
    parser.add_option('-d', '--dump-html',
                      dest='dump_file',
                      help="dump current HTML to file specified on error. specify - for stdout.")
    parser.add_option('-w', '--show-error-in-browser', 
                      dest='show_error_in_browser', 
                      action='store_true',
                      help="show dumped HTML in a web browser on error, forces interactive mode")
    parser.add_option('-b','--browser',
                      dest='browser',
                      default='firefox', 
                      help="specifies web browser to use when viewing error pages [default: %default]")



    global options 
    options, args = parser.parse_args(argv)

    global name_lookup 
    name_lookup = scan_for_tests(options.search_path)

    if options.list_suites:
        list_suites()
        return

    if len(args) < 2: 
        die("No tests specified", parser)

    if options.show_error_in_browser:
        if not options.dump_file:
            die("Must specify dump file when requesting browser launch",parser)
        options.interactive = True

    if options.browser: 
        os.environ['BROWSER'] = options.browser

    scheme, uri = urllib.splittype(options.base_url)
    if scheme is None: 
        warn("no scheme specified in test url, assuming http")
        options.base_url = "http://" + options.base_url 
    elif not scheme == 'http' and not scheme == 'https':
        die("unsupported scheme '%s' in '%s'" % (scheme,options.base_url))
    
    host, path = urllib.splithost(uri)

    print "* Running against %s, host: %s path=%s" % \
        (options.base_url,host,path)
    # define utility variables to help point scripts at desired location
    define_twill_vars(base_url=options.base_url)
    define_twill_vars(base_host=host)
    define_twill_vars(base_path=path)
    
    if options.config_file: 
        try: 
            global CONFIG_OVERRIDES 
            CONFIG_OVERRIDES = read_configuration(options.config_file)
        except IOError, msg: 
            die(msg)

    try:
        nerrors = run_tests(map(parse_test_call,args[1:]))
    except Exception, e:
        handle_exception("ERROR",e)
    else:
        if nerrors == 0:
            log_info('All Tests Passed!')
        else:
            log_info('%d Errors Found' % nerrors)


if __name__ == '__main__':
    main(sys.argv)
