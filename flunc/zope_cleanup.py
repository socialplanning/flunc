import twill 
from twill.namespaces import get_twill_glocals 
from xmlrpclib import Server as XMLRPCServer 
import urllib 


__all__ = ['zope_delobject']


def get_twill_var(varname): 
    twill_globals, twill_locals = get_twill_glocals()
    return twill_globals.get(varname)

def zope_delobject(container, obj, admin_user, admin_pw): 
    base_url = get_twill_var('base_url')
    prepath = get_twill_var('prepath')

    print "(zope) Deleting %s from %s on %s" % (obj, container, base_url)

    scheme, uri = urllib.splittype(base_url) 
    host, path = urllib.splithost(uri)
    if prepath is not None:
        path = prepath + path
    auth_url = "%s://%s:%s@%s%s" % (scheme, admin_user, admin_pw, host, path)
    portal = XMLRPCServer(auth_url)
    getattr(portal, container).manage_delObjects([obj])
