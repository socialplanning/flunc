import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite

def test_suite():
    print "OpenPlans test:  create user"
    return unittest.TestSuite(
        FunctionalDocFileSuite('create_user.txt')
        )
