import unittest 
import twill
from twill.namespaces import get_twill_glocals

from Products.OpenPlans.tests.openplanstestcase import OpenPlansTestCase
from Testing.ZopeTestCase.utils import startZServer


class FunctionalMultiTwillTest(OpenPlansTestCase): 
    """ 
    runs a series of twill script tests against a Fixture instance 
    of Open Plans.  
    """ 

    def __init__(self,twillFiles): 
        unittest.TestCase.__init__(self,"runTest")
        self.twillFiles = twillFiles

    def afterSetUp(self): 
        OpenPlansTestCase.afterSetUp(self)
        # make the fixture accessible via http
        serverAddr = startZServer()

        # record where it is 
        self.openPlansURL = "http://%s:%s/%s" % (serverAddr[0],serverAddr[1],self.portal.getId())
    
    def runTest(self):
        
        # let twill scripts know where the instance is 
	twill_globals,twill_locals = get_twill_glocals()
        twill_globals['baseURL'] = self.openPlansURL

        for twillFile in self.twillFiles: 
            print "Executing twill script: ", twillFile
            twill.execute_file(twillFile,no_reset=1)


def makeTwillSuite(twillScripts): 
  """create a unittest.TestSuite which runs the 
     twill scripts contained in the files given 
     by file name in the list twillScripts in 
     the order given by the list 
  """   
  twillSuite = unittest.TestSuite()
  twillSuite.addTest(FunctionalMultiTwillTest(twillScripts))
  return twillSuite
