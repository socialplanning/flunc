import os, sys
import unittest
suite = unittest.TestSuite()

def test_suite():
    print __file__
    dirname = os.path.dirname(__file__)
    prodstring = "Products.OpenPlans_twill_tests."
    if not len(dirname):
        dirname = '.'
        prodstring = ''
    print "'%s'" % dirname
    names = os.listdir(dirname)

    tests = [x for x in names \
             if x.startswith('test') and x.endswith('.py') and not x == 'tests.py']

    for test in tests:
        Products = __import__(prodstring + test[:-3])
        testmodule = getattr(Products.OpenPlans_twill_tests, test[:-3])
        if hasattr(testmodule, 'test_suite'):
            suite.addTest(testmodule.test_suite())
    return suite

# currently, running using 'python tests.py' does not work
if __name__ == '__main__':
    suite = test_suite()
    TestRunner = unittest.TextTestRunner
    TestRunner(verbosity=1).run(suite)
