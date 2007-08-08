import twill 
from twill.namespaces import get_twill_glocals 
from xmlrpclib import Server as XMLRPCServer 
import urllib 
from logging import log_warn

__all__ = ['create_doc']


def get_twill_var(varname): 
    twill_globals, twill_locals = get_twill_glocals()
    return twill_globals.get(varname)

def create_doc(container, admin_user, admin_pw, id, title, body, revision=None): 
    base_url = get_twill_var('base_url')
    prepath = get_twill_var('prepath')

    log_warn("(zope) Creating document %s in %s" % (id, container))
    scheme, uri = urllib.splittype(base_url) 
    host, path = urllib.splithost(uri)
    if prepath is not None:
        path = prepath + path
    auth_url = "%s://%s:%s@%s%s/" % (scheme, admin_user, admin_pw, host, path)
    portal = XMLRPCServer(auth_url)
    getattr(portal, container).invokeFactory('Document', id)
    item = getattr(getattr(portal, container), id)
    item.setTitle(title)
    item.setText(body)

    # XXX getting error:
    # TypeError: cannot marshal <type 'instancemethod'> objects
#    if revision:
#        getattr(portal, 'portal_repository').save(item, revision)

    item.reindexObject()
