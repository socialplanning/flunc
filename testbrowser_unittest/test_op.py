import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest


from metadata import *
    
def test_suite():
    suite = unittest.TestSuite()
    tests = ['op_login',
             'op_edit_project']


    if inzopectl:
        modstring = "Testing.ZopeTestCase."
    else:
        modstring = ""

    for test in tests:
        Testing = __import__(modstring + test)

        if inzopectl:
            testmodule = getattr(Testing.ZopeTestCase, test[:-3])
        else:
            testmodule = Testing
            
        if hasattr(testmodule, 'test_suite'):
            suite.addTest(testmodule.test_suite())
    return suite

if __name__ == '__main__':
    suite = test_suite()
    TestRunner(verbosity=1).run(suite)
