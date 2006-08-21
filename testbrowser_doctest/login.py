from metadata import *

def login(name, password):
     home()
     browser.getLink('Log in').click()
     browser.getControl(name='__ac_name').value = name
     browser.getControl(name='__ac_password').value = password
     browser.getControl(name='submit').click()
     return browser
