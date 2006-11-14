import twill 
from twill.namespaces import get_twill_glocals
import optparse 
import sys
import os 

# this one's for ian 
CONFIGURATION      = '.conf'
SUITE              = '.tsuite'
TEST               = '.twill' 
CONFIG_OVERRIDES   = None
options = {}

def define_twill_vars(**kwargs): 
    tglobals, tlocals = get_twill_glocals()
    tglobals.update(kwargs)

def die(message, parser=None): 
    print message 
    if parser is not None:
        parser.print_usage()
    sys.exit(0)

def read_file_type(name, ext): 
    filename = os.path.join(options.search_path, name + ext)
    return open(filename).read()

def read_configuration(name): 
    return read_file_type(name, CONFIGURATION)

def read_suite(name): 
    return read_file_type(name, SUITE)

def read_test(name): 
    return read_file_type(name, TEST)

def parse_suite(suite_data): 
    valid_line = lambda line: line.strip() and\
                              not line.lstrip().startswith('#')
    file_names = filter(valid_line, suite_data.splitlines())
    return '\n'.join(map(read_test, file_names))

def do_overrides(): 
    if CONFIG_OVERRIDES: 
        twill.execute_string(CONFIG_OVERRIDES, no_reset=1)

def run_script(script_data): 
    twill.execute_string(script_data, no_reset=1)

def run_tests(names): 
    for name in names: 
        run_test(name)

def run_test(name): 
    try:
        suite_data = read_suite(name)
        script_data = parse_suite(suite_data)
        
        try: 
            configuration = read_configuration(name)
            run_script(configuration)
        except IOError: 
            print "Warning: unable to locate configuration for suite %s" % suite_file 
            pass 

    except IOError: 
        try:
            script_data = read_test(name)
        except IOError: 
            raise IOError("unable to locate '%s' or '%s' in %s" % (name + SUITE, 
                                                               name + TEST, 
                                                               options.search_path)) 

    do_overrides()
    run_script(script_data)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    ftest_dir = os.path.join(base_dir, 'ftests')
    usage = "usage: %prog [options] <test name> [test name...]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-t', '--host',
                      help='specifies the base url of the portal to test [default: %default]',
                      dest='baseURL',
                      default='http://localhost:8080/portal')
    parser.add_option('-c', '--config',
                      help='specifies file with configuration overrides',
                      dest='config_file')
    parser.add_option('-p', '--path',
                      dest='search_path',
                      default=ftest_dir, 
                      help='specifies location to search for tests [default: %default]')
    
    global options 
    options, args = parser.parse_args(argv)

    if len(args) < 2: 
        die("No tests specified", parser)

    define_twill_vars(baseURL=options.baseURL)

    if options.config_file: 
        try: 
            global CONFIG_OVERRIDES 
            CONFIG_OVERRIDES = read_configuration(options.config_file)
        except IOError, msg: 
            die(msg)

    run_tests(args[1:]) 

    print 'All Tests Passed!'
 

if __name__ == '__main__':
    main(sys.argv)

