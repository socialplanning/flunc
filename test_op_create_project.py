import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite, FunctionalTestCase

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS
def test_suite():
    tests = []
    testfiles = ('login.txt',
                 'create_project.txt',
                 'edit_project.txt',
                 'login.txt',
                 'create_user.txt')
    
    for name in testfiles:
        #doctest.DocFileSuite
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
