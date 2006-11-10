import Products


def gettestbrowser(Fivetb=False):
    global _browserSingleton

    try:
        type(_browserSingleton)
    except NameError:
        if Fivetb:
            from Products.Five.testbrowser import Browser
        else:
            from zope.testbrowser.browser import Browser
        _browserSingleton = Browser()
        
    return _browserSingleton
