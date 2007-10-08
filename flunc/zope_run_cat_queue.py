from twill.namespaces import get_twill_glocals 
from xmlrpclib import Server as XMLRPCServer 
import urllib 

from logging import log_warn

__all__ = ['run_cat_queue']


def run_cat_queue(admin_user, admin_pw): 
    globals, locals = get_twill_glocals()

    base_url = globals.get('base_url')
    prepath = globals.get('prepath')

    log_warn("(zope) Running catalog queue for %s" % (base_url))

    scheme, uri = urllib.splittype(base_url) 
    host, path = urllib.splithost(uri)
    if prepath is not None:
        path = prepath + path
    auth_url = "%s://%s:%s@%s%s/" % (scheme, admin_user, admin_pw, host, path)
    portal = XMLRPCServer(auth_url)

    portal.portal_catalog_queue.manage_process()
