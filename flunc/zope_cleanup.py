import twill 
from twill.namespaces import get_twill_glocals 
from xmlrpclib import Server as XMLRPCServer
from xmlrpclib import Fault
import urllib 
from logging import log_error, log_warn
from flunc import options


__all__ = ['zope_delobject']


def get_twill_var(varname): 
    twill_globals, twill_locals = get_twill_glocals()
    return twill_globals.get(varname)

def zope_delobject(container, obj, admin_user, admin_pw):
    # use a the 'cleanup_base_url', which may be different than the base_url
    base_url = get_twill_var('cleanup_base_url')
    prepath = get_twill_var('prepath')

    log_warn("(zope) Deleting %s from %s on %s" % (obj, container, base_url))

    scheme, uri = urllib.splittype(base_url) 
    host, path = urllib.splithost(uri)
    if prepath is not None:
        path = prepath + path
    auth_url = "%s://%s:%s@%s%s/" % (scheme, admin_user, admin_pw, host, path)
    portal = XMLRPCServer(auth_url)
    try:
        getattr(portal, container).manage_delObjects([obj])
    except Fault, e:
        ignorable = '%s does not exist' % obj
        if str(e).count(ignorable):
            log_warn("(zope) can't delete %s/%s/%s, it didn't exist" % (uri, container, obj))
        elif options.verbose:
            raise
        else:
            log_error("Error removing '%s' from '%s': %s" % (obj, container, str(e)))

