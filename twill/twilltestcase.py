import unittest 
import twill

class TwillTestCase(unittest.TestCase): 
  """Test case which runs an individual 
     twill script. 
  """ 

  def __init__(self,fileName,resetTwill): 
    """init a TwillTestCase. fileName is the 
       name of the file containing the twill 
       script. if resetTwill is set to True the 
       test will be run in a new browser session
    """ 
    unittest.TestCase.__init__(self,"runTest")
    self.twillScript = fileName
    self.resetTwill = resetTwill

  def runTest(self): 
    try: 
      print "Executing", self.twillScript 
      if self.resetTwill: 
        twill.execute_file(self.twillScript)
      else: 
        twill.execute_file(self.twillScript,no_reset=1)
    except Exception: 
      self.fail("Twill test " + self.twillScript + " failed")


def makeTwillSuite(twillScripts): 
  """create a unittest.TestSuite which runs the 
     twill scripts contained in the files given 
     by file name in the list twillScripts in 
     the order given by the list 
  """ 
  twillSuite = unittest.TestSuite()
  for fileName in twillScripts: 
    twillSuite.addTest(TwillTestCase(fileName,resetTwill=False))
  return twillSuite
