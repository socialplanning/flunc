inzopectl = False  # boolean flag:  is being run from `zopectl test`?
useFiveTB = False  # boolean flag:  use Five.testbrowser?

# this is the address of the instance of zope you are testing
server='http://localhost:8080'

# this is the path to the open plans object you are testing
portalURL = '/openplans'

baseURL=server + portalURL

# user with rights to perform test cleanup (an admin)
cleanup_user = 'admin_username'
cleanup_password = 'admin_password'

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
