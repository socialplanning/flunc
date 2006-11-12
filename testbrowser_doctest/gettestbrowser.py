import Products

def gettestbrowser(Fivetb=False):
    if Fivetb:
        from Products.Five.testbrowser import Browser
    else:
        from zope.testbrowser.browser import Browser
    browser = Browser()
    return browser
