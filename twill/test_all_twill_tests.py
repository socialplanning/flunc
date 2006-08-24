import os,sys
import twilltestcase
from twill_openplans_suite import twillFiles as openPlansTwillSuite
from Globals import package_home

if __name__ == '__main__': 
  execfile(os.path.join(sys.path[0],'framework.py'))


def test_suite():

  # find where we are
  basePath = package_home(globals())

  allTwillTests = [ os.path.sep.join([basePath,filename]) \
                      for filename in openPlansTwillSuite ]

  return twilltestcase.makeTwillSuite(allTwillTests)


if __name__ == '__main__':
    framework()
