import os
from seleniumtestcase import SeleniumSuite   
import sys
from Globals import package_home

if __name__ == '__main__': 
  execfile(os.path.join(sys.path[0],'framework.py'))


def test_suite():

  # find where we are
  basePath = package_home(globals())

  return SeleniumSuite(os.path.join(basePath,"TestSuite.html"))


if __name__ == '__main__':
    framework()
