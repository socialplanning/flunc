import os, sys
import unittest
suite = unittest.TestSuite()

def test_suite():
    names = os.listdir(os.path.dirname(__file__))
    tests = [x for x in names \
             if x.startswith('test') and x.endswith('.py') and not x == 'tests.py']

    for test in tests:
        Products = __import__("Products.testbrowser_doctest." + test[:-3])
        testmodule = getattr(Products.testbrowser_doctest, test[:-3])
        if hasattr(testmodule, 'test_suite'):
            suite.addTest(testmodule.test_suite())
    return suite

if __name__ == '__main__':
    suite = test_suite()
    TestRunner = unittest.TextTestRunner
    TestRunner(verbosity=1).run(suite)
