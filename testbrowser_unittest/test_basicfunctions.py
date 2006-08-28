import unittest

from metadata import *

# testfiles should be ordered
testfiles = ('op_create_user',
             'op_login',
             'op_create_project',
             'op_edit_project')

if useFiveTB:
    class TestBasicFunctions(OpenPlansTestCase):
        'example class for basic tests'
        
        def test_dummy(self):
            print 'hi'
            print self.portal.absolute_url()
            browser.open('http://localhost')
#            browser.open(self.portal.absolute_url())

#            print browser.contents

    def test_suite():
        print "OpenPlans test:  fivetb"
        suite = unittest.makeSuite(TestBasicFunctions, 'test')
        return suite
else:

    def test_suite():
        tests = unittest.TestSuite()

        for name in testfiles:
            Products = __import__("Products.testbrowser_unittest." + name)
            testmodule = getattr(Products.testbrowser_unittest, name)
            tests.addTest(testmodule.test_suite())

        return tests

if __name__ == '__main__':
    suite = test_suite()
    TestRunner = unittest.TextTestRunner
    TestRunner(verbosity=1).run(suite)
