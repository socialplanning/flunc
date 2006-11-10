inzopectl = True  # boolean flag:  is being run from `zopectl test`?
useFiveTB = True  # boolean flag:  use Five.testbrowser?

# this is the address of the instance of zope you are testing if
# you are not connecting to a fixture 
_server='http://localhost:8080'

# this is the path to the open plans object you are testing
_portalURL = '/foo'

# this should be accessed via get_baseURL()
_baseURL= _server + _portalURL

# user with rights to perform test cleanup (an admin)
cleanup_user = 'ltucker'
cleanup_password = 'joop'

# info about for user that is created by the tests
user='tester'
fullname='John Q. Tester'
password='tester1'
email='test@test.test'

# info for the project that is created by the tests
projname='testhaven'
projfullname="tester's test project"
projtitle='testing home'
projdesc='a test project to document the test procedure of testing'
projbody='page body text'
projver='the first version'
