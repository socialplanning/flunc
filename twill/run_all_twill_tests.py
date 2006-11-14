import sys
import twill_utils
from twill_openplans_suite import twillFiles as openPlansTwillSuite

if len(sys.argv) < 2: 
    print "usage",sys.argv[0],"<url to test>"
    sys.exit(0)

baseURL = sys.argv[1]
twill_utils.executeTwillScriptsInSession(openPlansTwillSuite,{'baseURL':baseURL})
