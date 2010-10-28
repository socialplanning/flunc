from twill.commands import get_browser
from twill.errors import TwillAssertionError

import urllib

def url_qs(what, val=None):
    browser = get_browser()
    qs = urllib.splitquery(browser.get_url())[-1]
    qs = qs.split('&')
    qsdict = {}
    for q in qs:
        q = q.split('=')
        qsdict[q[0]] = q[1]
        
    if what not in qsdict:
        raise TwillAssertionError("no match to '%s' in %s" % (what, qs))
    
    if val is None:
        return

    if qsdict[what] != val:
        raise TwillAssertionError("Expected query_string argument %s to be %s, but it's %s instead" 
                                  % (what, val, qsdict[what]))
