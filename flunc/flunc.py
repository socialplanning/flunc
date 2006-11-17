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
CONFIG_OVERRIDES   = None
# these are for ian 
options = {}
name_lookup = {}

def define_twill_vars(**kwargs): 
    tglobals, tlocals = get_twill_glocals()
    tglobals.update(kwargs)

def die(message, parser=None): 
    print message 
    if parser is not None:
        parser.print_usage()
    sys.exit(0)

def read_file_type(name, ext): 
    try: 
        filename = name_lookup[name + ext]
        return open(filename).read()
    except KeyError:
        raise IOError('Unable to locate %s in the search path' % (name + ext))
    

def scan_for_tests(root): 
    """
    recursively scans for relevant files in the directory given
    """
    print "* scanning for tests in '%s'" % root
    found = {} 

    def check_files(files):
        for filename in files: 
            base, ext = os.path.splitext(filename)
            if ext in (TEST, SUITE, CONFIGURATION):
                if filename in found: 
                    print "! Warning: ignoring %s in %s (already found: %s)" % \
                        (filename, root, found[filename])
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

        if ext != SUITE:
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

def parse_suite(suite_data): 
    valid_line = lambda line: line.strip() and\
                              not line.lstrip().startswith('#')
    return map(parse_test_call,filter(valid_line, suite_data.splitlines()))

def handle_exception(msg, e):
    if options.verbose:
        import traceback
        traceback.print_exception(*sys.exc_info())

    if options.dump_file:
        html = twill.get_browser().get_html()
        if options.dump_file == '-':
            print html
        else:
            try:
                open(options.dump_file, 'w').write(html)
                print "* saved html to: %s" % options.dump_file
            except IOError, e:
                print "Unable to save to: %s" % options.dump_file
                print e.args[0]

    if e.args:
        print "X ", msg, ":", e.args[0]
    else:
        print "X ", msg
    if options.interactive:
        sys.argv[1:] = []
        # twill shell takes arguments from sys.argv
        twill.shell.main()
    sys.exit(1)

def do_overrides(): 
    if CONFIG_OVERRIDES: 
        try:
            twill.execute_string(CONFIG_OVERRIDES, no_reset=1)
        except Exception, e:
            handle_exception('ERROR in global configuration', e)

def run_script(script_data): 
    twill.execute_string(script_data, no_reset=1)

def run_tests(calls): 
    for name,args in calls: 
        run_test(name,args)

def run_test(name,args): 
    try:
        suite_data = read_suite(name)
        print "* running suite: %s" % name 

        calls = parse_suite(suite_data)
        
        try: 
            configuration = read_configuration(name)
            run_script(configuration)
            print "* loaded configuration: %s" % (name + CONFIGURATION)
        except IOError: 
            print "! Warning: unable to locate configuration for suite %s" % (name + SUITE)
        except Exception,e:
            handle_exception("Invalid configuration: '%s'" % (name + CONFIGURATION), e)
        
        run_tests(calls)
        return

    except IOError: 
        # not a suite, try a test
        pass

    do_overrides()
        
    try:
        print "* running test: %s" % name
        script = read_test(name)
        script = make_twill_local_defs(make_dict_from_call(args,get_twill_glocals()[0])) + script 
        run_script(script)
    except IOError, e: 
        # reraise with more specific message
        try: 
            raise IOError("Unable to locate '%s' or '%s' in search path" % (name + SUITE, 
                                                                            name + TEST))
        except IOError, e: 
            handle_exception("ERROR", e)
                          

    except Exception, e:
        handle_exception("ERROR : %s" % name, e)

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
    parser.add_option('-d', '--dump-html',
                      dest='dump_file',
                      help="dump current HTML to file specified on error. specify - for stdout.")

    global options 
    options, args = parser.parse_args(argv)

    global name_lookup 
    name_lookup = scan_for_tests(options.search_path)

    if options.list_suites:
        list_suites()
        return

    if len(args) < 2: 
        die("No tests specified", parser)

    scheme, uri = urllib.splittype(options.base_url)
    if scheme is None: 
        print "! Warning: no scheme specified in test url, assuming http"
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

    run_tests(map(parse_test_call,args[1:])) 

    print 'All Tests Passed!'
 

if __name__ == '__main__':
    main(sys.argv)

