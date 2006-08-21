import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite

def test_suite():
    print "OpenPlans test:  login"
    return unittest.TestSuite(
        FunctionalDocFileSuite('login.txt')
        )
