import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite

def test_suite():
    print "OpenPlans test:  edit project"
    return unittest.TestSuite(
        FunctionalDocFileSuite('edit_project.txt')
        )
