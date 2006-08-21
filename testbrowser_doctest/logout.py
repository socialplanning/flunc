from metadata import *

def logout(browser):
     home()
     browser.getLink('Log out').click()
