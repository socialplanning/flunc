import unittest

from metadata import *

# testfiles should be ordered
testfiles = ('op_create_user',
             'op_login',
             'op_create_project',
             'op_edit_project')

if inzopectl:  ### if running in zopectl...
    from Products.OpenPlans.tests.openplanstestcase import OpenPlansTestCase
    from Testing.ZopeTestCase.utils import startZServer
    
    class TestBasicFunctions(OpenPlansTestCase):
        'example class for basic tests'

        def afterSetUp(self):
            OpenPlansTestCase.afterSetUp(self)

            # make the fixture accessible via http
            serverAddr = startZServer()

            # record where it is 
            server = "http://%s:%s" % (serverAddr[0],serverAddr[1])
            portalURL = "/%s" % (self.portal.getId())
            get_baseURL(server + portalURL)
            

        def test_run(self):
            ' run the tests '
            for name in testfiles:
                Products = __import__("Products.testbrowser_unittest." + name)
                testmodule = getattr(Products.testbrowser_unittest, name)
                theresult = unittest.TestResult()
                testmodule.test_suite().run(theresult)

                # check for errors/failures
                if len(theresult.errors):
                    print theresult.errors
                if len(theresult.failures):
                    print theresult.failures
                assert theresult.wasSuccessful()                

    def test_suite():
        print "OpenPlans test:  fivetb"
        suite = unittest.TestSuite(unittest.makeSuite(TestBasicFunctions))

        return suite
else: ### if not running w/in zopectl

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
