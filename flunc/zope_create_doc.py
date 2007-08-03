import twill 
from twill.namespaces import get_twill_glocals 
from xmlrpclib import Server as XMLRPCServer 
import urllib 


__all__ = ['create_doc']


def get_twill_var(varname): 
    twill_globals, twill_locals = get_twill_glocals()
    return twill_globals.get(varname)

def create_doc(container, admin_user, admin_pw, id, title, body, revision=None): 
    base_url = get_twill_var('base_url')
    prepath = get_twill_var('prepath')

    print "(zope) Creating document %s in %s" % (id, container)
    scheme, uri = urllib.splittype(base_url) 
    host, path = urllib.splithost(uri)
    if prepath is not None:
        path = prepath + path
    auth_url = "%s://%s:%s@%s%s/" % (scheme, admin_user, admin_pw, host, path)
    portal = XMLRPCServer(auth_url)
    getattr(portal, container).invokeFactory('Document', id, title)
    item = getattr(getattr(portal, container), id)
    item.setText('body')

    # set the revision text
#    if revision:
#        getattr(portal, 'portal_repository').save(revision)
