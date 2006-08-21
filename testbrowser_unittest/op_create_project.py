import unittest

from metadata import *
import login, logout

class TestCreateProject(unittest.TestCase):

    def test_create_project(self):
        """ test creating a project """
        
        browser = login.login(user, password)
        home()
        browser.getLink('Start a Project').click()
        browser.getControl(name='title').value = projname
        browser.getControl(name='full_name').value = projfullname
        browser.getControl(name='workflow_policy').value = ['open_policy']
        browser.getControl(name='form_submit').click()
                
        assert 'This is the home page for your project' in browser.contents
        assert "tester's test project" in browser.contents
        assert projname in browser.url

        logout.logout(browser)

def test_suite():
    print "OpenPlans test:  create project"
    suite = unittest.makeSuite(TestCreateProject, 'test')
    return suite
