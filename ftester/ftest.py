import twill 
from twill.namespaces import get_twill_glocals
import optparse 
import sys
import os 

# this one's for ian 
TEST_HOST_VARIABLE = 'test-host'
CONFIGURATION      = '.conf'
SUITE              = '.tsuite'
TEST               = '.twill' 
GLOBAL_CONFIG      = None


def define_twill_vars(**kwargs): 
    tglobals, tlocals = get_twill_glocals()
    tglobals.update(kwargs)


def die(message, parser=None): 
    print message 
    if parser is not None:
        parser.print_usage()
    sys.exit(0)

def find_file_type(name, ext): 
    filename = name + ext
    if not os.path.isfile(filename):
        raise IOError("unable to locate '%s'" % name + ext)
    return filename 

def find_configuration(name): 
    return find_file_type(name, CONFIGURATION)

def find_suite(name): 
    return find_file_type(name, SUITE)

def find_test(name): 
    return find_file_type(name, TEST)

def find_scripts(name): 
    """
    returns a list of test filenames referred to by the name given. 
    if name refers to a suite, the list of filenames of tests 
    in the suite is returned. 

    if name refers to a test, a list containing the filename 
    of the test is returned. 
    """
    try:
        suite_file = find_suite(name)
        names = parse_suite(suite_file)
        scripts = []
        for name in names: 
            test_file = find_test(name)
            scripts.append(test_file)
        return scripts 
    except IOError: 
        pass 

    try:
        test_file = find_test(name)
        return [test_file]
    except IOError: 
        raise IOError("unable to locate '%s' or '%s'" % (name + SUITE, 
                                                         name + TEST)) 


def parse_suite(filename): 
    all_lines = open(filename).readlines()
    
    test_lines = []
    for line in lines: 
        line.strip()
        if len(line) and not line.startwith('#'):
            test_lines.append(line)
    return test_lines

def run_file(filename): 
    twill.execute_file(filename, no_reset=1)


def main(argv):
    parser = optparse.OptionParser()
    parser.add_option('-t','--host',
                      help='specifies the host and port to test',
                      dest='host', 
                      default='http://localhost:8080')
    parser.add_option('-c','--config',
                      help='specifies file with configuration overrides',
                      dest='config_file')
    parser.add_option('-F','--fail-on-first',
                      help='specifies file with configuration overrides',
                      dest='config_file')
    
    options, args = parser.parse_args(argv)

    if len(args) < 2: 
        die("No tests specified", parser)

    scripts = []
    for name in args[2:]: 
        scripts += find_scripts(name)

    define_twill_vars(host=options.host)

    if options.config_file: 
        try: 
            GLOBAL_CONFIG = find_configuration(options.config_file)
        except IOError, msg: 
            die(msg)

    print "SCRIPTS: " , scripts
 
    
    

    

    
if __name__ == '__main__':
    main(sys.argv)

