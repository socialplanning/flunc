import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite, FunctionalTestCase

from metadata import *

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS

# testfiles should be ordered
testfiles = ('create_user.txt',
             'login.txt',
             'create_project.txt',
             'edit_project.txt')

def test_suite():
    tests = []

    for name in testfiles:
        tests.append(FunctionalDocFileSuite(name,
                                            optionflags=optionflags,
                                            package='Products.testbrowser_doctest',
                                            test_class = FunctionalTestCase
                                            ))
    
    return unittest.TestSuite(tests)

if __name__ == '__main__':
    suite = test_suite()
    TestRunner = unittest.TextTestRunner
    TestRunner(verbosity=1).run(suite)
