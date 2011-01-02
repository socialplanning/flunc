from logging import log_warn
import simplejson
import time
import urllib 
from twill.commands import get_browser, go, find
from twill.errors import TwillAssertionError
from twill.namespaces import get_twill_glocals 
from xmlrpclib import Server as XMLRPCServer 


__all__ = ['run_cat_queue',
           'run_export_queue', 'ensure_project_export']

def ensure_project_export(admin_user, admin_pw, project):
    """
    Looks for a project export zipfile in the page.
    (Expects to be already on the project's export view.)
    If no export zipfile is found, trigger the export queue
    processing on the remote server, and then check again.
    """
    globals, locals = get_twill_glocals()

    base_url = globals.get('base_url')
    url = "%s/projects/%s/export/current_status_json" % (
        base_url, project)
    go(url)
    html = get_browser().get_html()
    if "state" not in html:
        run_export_queue(admin_user, admin_pw, project)
    else:
        json = simplejson.loads(html)
        if json['state'] == "failed":
            raise TwillAssertionError(
                "Export failed: %s" % html)
        if json['state'] != 'finished':
            time.sleep(5)

def run_export_queue(admin_user, admin_pw, expected=None):
    globals, locals = get_twill_glocals()

    base_url = globals.get('base_url')
    prepath = globals.get('prepath')

    log_warn("(zope) Running export queue for %s" % (base_url))

    scheme, uri = urllib.splittype(base_url) 
    host, path = urllib.splithost(uri)
    if prepath is not None:
        path = prepath + path
    auth_url = "%s://%s:%s@%s%s/" % (scheme, admin_user, admin_pw, host, path)
    portal = XMLRPCServer(auth_url)

    # pass in a maxwait of 1 second to speed things up
    exports = portal.manage_project_export_queue(1)
    if expected is not None and expected not in exports:
        raise TwillAssertionError("project id %s not found in exported projects: %r" % (expected, exports))

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
