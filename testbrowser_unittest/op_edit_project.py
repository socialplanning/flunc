import unittest

from metadata import *
import login, logout

class TestEditProject(unittest.TestCase):

    def test_edit_project(self):
        """ test editing a project """
        
        # first, login
        browser = login.login(user, password)

        # do the edits -- this could be split into two sections
        browser.getLink('Projects').click()
        browser.getLink(projname).click()
        browser.getLink('Edit').click()
        browser.getControl(name="title").value = projtitle
        browser.getControl(name="description").value = projdesc
        browser.getControl(name="text").value = 'the quick brown fox'
        browser.getControl(name="cmfeditions_version_comment").value = projver
        browser.getControl(name="form_submit").click()

        # check the edits
        assert 'Changes saved.' in browser.contents
        assert projtitle in browser.contents
        
        # logout
        logout.logout(browser)

def test_suite():
    print "OpenPlans test:  edit project"
    suite = unittest.makeSuite(TestEditProject, 'test')
    return suite
