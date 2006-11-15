import optparse 
import sys
import os 

import twill 
from twill.namespaces import get_twill_glocals
from twill.errors import TwillAssertionError

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

def list_suites():
    names = os.listdir(options.search_path)
    names.sort()
    for name in names:
        base, ext = os.path.splitext(name)
        full = os.path.join(options.search_path, name)
        if ext != SUITE:
            continue
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
    return filter(valid_line, suite_data.splitlines())

def do_overrides(): 
    if CONFIG_OVERRIDES: 
        try:
            twill.execute_string(CONFIG_OVERRIDES, no_reset=1)
        except TwillAssertionError, e:
            if options.verbose: raise e
            print 'ERROR in global configuration'
            sys.exit(1)

def run_script(script_data): 
    twill.execute_string(script_data, no_reset=1)

def run_tests(names): 
    for name in names: 
        run_test(name)

def run_test(name): 
    try:
        suite_data = read_suite(name)
        print "* running suite: %s" % name 

        names = parse_suite(suite_data)
        
        try: 
            configuration = read_configuration(name)
            run_script(configuration)
            print "* loaded configuration: %s" % name + CONFIGURATION
        except IOError: 
            print "Warning: unable to locate configuration for suite %s" % suite_file 
        except TwillAssertionError:
            print "Invalid configuration: '%s'" % name + CONFIGURATION
            return
        
        run_tests(names)
        return

    except IOError: 
        # not a suite, try a test
        pass

    do_overrides()
        
    try:
        print "* running test: %s" % name
        script = read_test(name)
        run_script(script)
    except IOError: 
        raise IOError("unable to locate '%s' or '%s' in %s" % (name + SUITE, 
                                                               name + TEST, 
                                                               options.search_path))
    except TwillAssertionError, e:
        if options.verbose: raise e
        print "ERROR: %s" % name
        sys.exit(1)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    ftest_dir = rel_filename(os.path.join(base_dir, 'ftests'))
    if not ftest_dir.startswith(os.path.sep):
        # Suppress optparse's word wrapping:
        ftest_dir = '.'+os.path.sep+ftest_dir
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
    parser.add_option('-l', '--list',
                      dest='list_suites',
                      action='store_true',
                      help="List the available suites (don't test anything)")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      help="Display stack traces from twill")

    global options 
    options, args = parser.parse_args(argv)

    if options.list_suites:
        list_suites()
        return

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

