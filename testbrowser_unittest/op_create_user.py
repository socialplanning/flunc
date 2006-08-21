import unittest

from metadata import *

class TestCreateUser(unittest.TestCase):

    def test_create_user(self):
        """ test creating a user """
        
        home()
        assert 'OpenPlans Home' in browser.contents

        browser.getLink('Join').click()
        assert browser.url == baseURL + '/createMember'

        browser.getControl(name='id').value = user
        browser.getControl(name='fullname').value = fullname
        browser.getControl(name='email').value = email
        browser.getControl(name='password').value = password
        browser.getControl(name='confirm_password').value = password
        browser.getControl(name='form.button.register').click()

        assert 'You have been registered' in browser.contents

def test_suite():
    print "OpenPlans test:  create user"
    suite = unittest.makeSuite(TestCreateUser, 'test')
    return suite
