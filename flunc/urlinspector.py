from twill.commands import get_browser
from twill.errors import TwillAssertionError

import urllib

def url_qs(what):
    browser = get_browser()
    qs = urllib.splitquery(browser.get_url())[-1]
    qs = qs.split('&')
    qsdict = {}
    for q in qs:
        q = q.split('=')
        qsdict[q[0]] = q[1]
        
    if what not in qsdict:
        raise TwillAssertionError("no match to '%s' in %s" % (what, qs))
    
