import twill 
from twill.namespaces import get_twill_glocals 
from xmlrpclib import Server as XMLRPCServer 
import urllib 
from twill.commands import go

from logging import log_warn

__all__ = ['get_uid']


def get_twill_var(varname): 
    twill_globals, twill_locals = get_twill_glocals()
    return twill_globals.get(varname)

def get_uid(username, admin_user, admin_pw): 
    globals, locals = get_twill_glocals()

    base_url = globals.get('base_url')
    prepath = globals.get('prepath')

    log_warn("(zope) Getting uid for user %s on %s" % (username, base_url))

    scheme, uri = urllib.splittype(base_url) 
    host, path = urllib.splithost(uri)
    if prepath is not None:
        path = prepath + path
    auth_url = "%s://%s:%s@%s%s/" % (scheme, admin_user, admin_pw, host, path)
    portal = XMLRPCServer(auth_url)

    confirmation_code = getattr(portal.portal_memberdata, username).getUserConfirmationCode()

    locals['__uid__'] = confirmation_code
