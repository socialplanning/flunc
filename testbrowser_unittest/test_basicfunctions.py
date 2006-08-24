import unittest

def test_suite():
    tests = unittest.TestSuite()

    # testfiles should be ordered
    testfiles = ('op_create_user',
                 'op_login',
                 'op_create_project',
                 'op_edit_project')

    for name in testfiles:        
        Products = __import__("Products.testbrowser_unittest." + name)
        testmodule = getattr(Products.testbrowser_unittest, name)
        tests.addTest(testmodule.test_suite())
              
    return tests

if __name__ == '__main__':
    suite = test_suite()
    TestRunner = unittest.TextTestRunner
    TestRunner(verbosity=1).run(suite)
