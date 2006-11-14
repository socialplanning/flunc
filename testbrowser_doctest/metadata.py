""" metadata for OpenCore tests """

from configuration import *

from gettestbrowser import gettestbrowser
browser = gettestbrowser(useFiveTB)

def get_baseURL(set=''):
    global local_baseURL
    if not set == '':
        local_baseURL = set

    # make sure 'local_baseURL' is set
    try:
        type(local_baseURL)
    except NameError:
        local_baseURL = baseURL
    
    return local_baseURL

def home():
    global inzopectl, server, portalURL, baseURL
    if useFiveTB:
        from Products.OpenPlans.tests.openplanstestcase import *
        print OpenPlansTestCase.portal.absolute_url()
        browser.open(OpenPlansTestCase.portal.absolute_url())
    else:
        # print 'home:', get_baseURL()
        browser.open(get_baseURL())

import login, logout
