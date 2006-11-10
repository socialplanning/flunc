import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite, FunctionalTestCase, Functional
from Products.OpenPlans.tests.openplanstestcase import OpenPlansTestCase
from Testing.ZopeTestCase.utils import startZServer

from metadata import *


# testfiles should be ordered
testfiles = ['create_user.txt',
             'list_users.txt',
             'login.txt',
             'create_project.txt',
             'edit_project.txt']

def SuiteWrapper(suite):
    wrapperSuite = unittest.TestSuite()
    wrapperSuite.addTest(SuiteTestCase(suite))
    return wrapperSuite



class SuiteTestCase(OpenPlansTestCase):
    def __init__(self,suite):
        OpenPlansTestCase.__init__(self)
        #unittest.TestCase.__init__(self,methodName='runTest')
        self.suite = suite
    
    def __call__(self,*args,**kwds):
        print "****** yoink *****"
        print args
        self.results = args[0]
        return OpenPlansTestCase.__call__(self,*args,**kwds)

    def runTest(self):
        print "***** running *****"
        get_baseURL(set=self.portal.absolute_url())
        #serverAddr = startZServer()

        # record where it is 
        #get_baseURL(set="http://%s:%s/%s" % (serverAddr[0],serverAddr[1],self.portal.getId()))

        self.suite(self.results)

class SingleFixtureSuiteTest(unittest.TestSuite):
    def __init__(self,suite):
        unittest.TestSuite.__init__(self)
        self.suite = suite

    def countTestCases(self):
        return self.suite.countTestCases()

    def __iter__(self):
        print "**** ITER ****"
        return iter([])

    def __call__(self,*args,**kw):
        print "*************** RUNNING ****************"
        fixtureMaker = OpenPlansTestCase()
        fixtureMaker.setUp()
   #     suite(*args,**kw)
        fixtureMaker.tearDown()
 

def test_suite():

    kw = {'optionflags':doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS,
          'package':'Products.testbrowser_doctest'}

    docSuite = FunctionalDocFileSuite(*testfiles,**kw)


    if useFiveTB:
        return SuiteWrapper(docSuite)
    else:
        return docSuite
    
    

if __name__ == '__main__':
    suite = test_suite()
    TestRunner = unittest.TextTestRunner
    TestRunner(verbosity=1).run(suite)
