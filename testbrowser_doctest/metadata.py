""" metadata for OpenCore tests """

from configuration import *

from gettestbrowser import gettestbrowser
browser = gettestbrowser(useFiveTB)

def home():
    browser.open(baseURL)

import login, logout
