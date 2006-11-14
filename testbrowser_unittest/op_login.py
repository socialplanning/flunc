import unittest

from metadata import *
import login, logout

class TestLogin(unittest.TestCase):

    def test_login(self):
        browser = login.login(user, password)
        assert 'You are now logged in' in browser.contents

    def test_logout(self):
        logout.logout(browser)
        assert 'You are now logged out' in browser.contents

def test_suite():
    print "OpenPlans test:  login"
    suite = unittest.makeSuite(TestLogin, 'test')
    return suite

