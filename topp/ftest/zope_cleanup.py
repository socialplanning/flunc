import twill 
from twill.namespaces import get_twill_glocals 
from xmlrpclib import Server as XMLRPCServer 
import urllib 


__all__ = ['zope_delobject']


def get_twill_var(varname): 
    twill_globals, twill_locals = get_twill_glocals()
    return twill_globals[varname]

def zope_delobject(container, object): 
    print "(zope) Deleting %s from %s" % (object,container)
    base_url = get_twill_var('baseURL') 
    admin_user = get_twill_var('admin')
    admin_pw = get_twill_var('adminpw')
    
    scheme, uri = urllib.splittype(base_url) 
    host, path = urllib.splithost(uri)
    authURL = "%s://%s:%s@%s%s" % (scheme, admin_user, admin_pw, host, path)
    portal = XMLRPCServer(authURL)
    getattr(portal,container).manage_delObjects([object])
