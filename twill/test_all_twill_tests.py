import os,sys
import twilltestcase
from twill_openplans_suite import twillFiles as openPlansTwillSuite
from Globals import package_home
from Products.OpenPlans.config import GLOBALS 

if __name__ == '__main__': 
  execfile(os.path.join(sys.path[0],'framework.py'))


def test_suite():

  basePath = package_home(GLOBALS)

  allTwillTests = [ os.path.sep.join([basePath,'tests',filename]) \
                      for filename in openPlansTwillSuite ]

  return twilltestcase.makeTwillSuite(allTwillTests)


if __name__ == '__main__':
    framework()
