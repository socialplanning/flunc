#
# Runs all tests in the current directory
#
# Execute like:
#   python runalltests.py
#
# Alternatively use the testrunner:
#   python /path/to/Zope/utilities/testrunner.py -qa
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))


import unittest
TestRunner = unittest.TextTestRunner
suite = unittest.TestSuite()

# these are ordered for 'live' sites
tests = ['test_op_create_user', 'test_op_login',
         'test_op_create_project', 'test_op_edit_project']

for test in tests:
    print test
    m = __import__(test)
    if hasattr(m, 'test_suite'):
        suite.addTest(m.test_suite())

if __name__ == '__main__':
    TestRunner(verbosity=1).run(suite)
