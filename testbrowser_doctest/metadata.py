""" metadata for OpenCore tests """

import configuration
from configuration import *
from gettestbrowser import gettestbrowser

browser = gettestbrowser(configuration.useFiveTB)

def get_baseURL(set=''):
    global local_baseURL
    if not set == '':
        local_baseURL = set

    # make sure 'local_baseURL' is set
    try:
        type(local_baseURL)
    except NameError:
        local_baseURL = configuration._baseURL
    
    return local_baseURL

def home():
    browser.open(get_baseURL())

def login(name, password):
    home()
    browser.getLink('Log in').click()
    browser.getControl(name='__ac_name').value = name
    browser.getControl(name='__ac_password').value = password
    browser.getControl(name='submit').click()
    return browser

def logout(browser):
    home()
    browser.getLink('Log out').click()

