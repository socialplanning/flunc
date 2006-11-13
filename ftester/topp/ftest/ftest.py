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

def find_file_type(name, ext): 
    filename = os.path.join(options.search_path, name + ext)
    if not os.path.isfile(filename):
        raise IOError("unable to locate '%s'" % filename)
    return filename 

def find_configuration(name): 
    return find_file_type(name, CONFIGURATION)

def find_suite(name): 
    return find_file_type(name, SUITE)

def find_test(name): 
    return find_file_type(name, TEST)


def parse_suite(filename): 
    all_lines = open(filename).readlines()
    
    test_lines = []
    for line in all_lines: 
        line = line.strip()
        if line and not line.startswith('#'):
            test_lines.append(line)
    return test_lines

def do_overrides(): 
    if CONFIG_OVERRIDES: 
        twill.execute_file(CONFIG_OVERRIDES, no_reset=1)


def run_script(filename): 
    print "run_script(%s)" % filename
    twill.execute_file(filename, no_reset=1)

def run_tests(names): 
    for name in names: 
        run_test(name)

def run_test(name): 
    try:
        suite_file = find_suite(name)
        print "Running suite %s"  % suite_file
        names = parse_suite(suite_file)
        scripts = map(find_test, names)
        
        try: 
            configuration = find_configuration(name)
            run_script(configuration)
        except IOError: 
            print "Warning: unable to locate configuration for suite %s" % suite_file 
            pass 

        do_overrides() 

        for script in scripts: 
            run_script(script)
        
        return 

    except IOError: 
        pass 

    try:
        test_file = find_test(name)
        do_overrides()
        run_script(test_file)
    except IOError: 
        raise IOError("unable to locate '%s' or '%s' in %s" % (name + SUITE, 
                                                               name + TEST, 
                                                               options.search_path)) 

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = optparse.OptionParser()
    parser.add_option('-t', '--host',
                      help='specifies the base url of the portal to test',
                      dest='baseURL',
                      default='http://localhost:8080/portal')
    parser.add_option('-c', '--config',
                      help='specifies file with configuration overrides',
                      dest='config_file')
    parser.add_option('-p', '--path',
                      dest='search_path',
                      default='ftests', 
                      help='specifies location to search for tests')
    
    global options 
    options, args = parser.parse_args(argv)

    if len(args) < 2: 
        die("No tests specified", parser)

    define_twill_vars(baseURL=options.baseURL)

    if options.config_file: 
        try: 
            global CONFIG_OVERRIDES 
            CONFIG_OVERRIDES = find_configuration(options.config_file)
        except IOError, msg: 
            die(msg)

    run_tests(args[1:]) 
 

if __name__ == '__main__':
    main(sys.argv)

