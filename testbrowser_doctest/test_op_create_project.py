import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite

def test_suite():
    print "OpenPlans test:  create project"
    return unittest.TestSuite(
        FunctionalDocFileSuite('create_project.txt')
        )
