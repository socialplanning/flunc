import ClientCookie
from zope.testbrowser.browser import Browser as ZopeTestBrowser
from mechanize import Browser as MechanizeBrowser 

class RedirectableMechBrowser(MechanizeBrowser): 
  def __init__(self, *args, **kwargs): 
    self.handler_classes['_redirect'] = ClientCookie.HTTPRedirectHandler
    MechanizeBrowser.__init__(self,*args,**kwargs)


def getTestBrowser(): 
  return ZopeTestBrowser(mech_browser=RedirectableMechBrowser())
