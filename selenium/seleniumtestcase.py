import unittest 

from Products.OpenPlans.tests.openplanstestcase import OpenPlansTestCase
from Testing.ZopeTestCase.utils import startZServer
import selenium 
import seleniumutils
import traceback

class SeleniumSuiteTestCase(OpenPlansTestCase): 
    """ 
    runs a selenium HTML suite against a fixture
    instance of OpenPlans

    XXX this runs the whole suite as a single testcase 
    """ 

    def __init__(self,suiteHTMLFilename): 
        """ 
        suiteHTMLFilename - the name of the file containing the selenium suite
        """ 
        unittest.TestCase.__init__(self,"runTest")
        self.suiteFile = suiteHTMLFilename

    def afterSetUp(self): 
        OpenPlansTestCase.afterSetUp(self)
        # make the fixture accessible via http
        serverAddr = startZServer()

        # record where it is 
        self.openPlansURL = "http://%s:%s/%s" % (serverAddr[0],serverAddr[1],self.portal.getId())
    
    def runTest(self):
        serverPort = 4444
        server = seleniumutils.startSeleniumServer(serverPort)
        tester = None

        try:
            tester = selenium.selenium('localhost',serverPort,
                              '*firefox /usr/lib/firefox/firefox-bin',
                              self.openPlansURL)
            tester.start()
            print "Running with baseURL = ", self.openPlansURL
            passed = seleniumutils.runSeleniumSuite(tester,self.suiteFile,
                                                    baseURL=self.openPlansURL)
            if not passed:
                self.fail("Selenium suite " + self.suiteFile + " did not execute successfully.")
                         
        finally:
            if tester != None:
                try:
                    tester.stop()
                except Exception,reason:
                    print "Error stopping selenium tester:",reason

            seleniumutils.stopSeleniumServer(server)
            





def SeleniumSuite(suiteHTMLFilename): 
  """create a unittest.TestSuite which runs the 
     selenium HTML suite in the filename given
  """
  suite = unittest.TestSuite()
  suite.addTest(SeleniumSuiteTestCase(suiteHTMLFilename))
  return suite
