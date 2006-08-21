""" metadata for OpenCore tests """

inzopectl = False  # boolean flag:  is being run from zopectl test?

# user data
user='tester'
fullname='John Q. Tester'
password='tester1'
email='test@test.test'

# project data
projname='testhaven'
projfullname="tester's test project"
projtitle='testing home'
projdesc='a test project to document the test procedure of testing'
projbody='page body text'
projver='the first version'

# url data
server='http://localhost:8082/'
baseURL='openplans_copy'

# testbrowser setup

useFiveTB = False # boolean flag: use Five.testbrowser?

from gettestbrowser import gettestbrowser
browser = gettestbrowser(useFiveTB)
baseURL=server + baseURL

def home():
    browser.open(baseURL)
