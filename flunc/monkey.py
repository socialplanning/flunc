import socket
from urllib2 import URLError

import twill
try:
    from twill.other_packages._mechanize_dist._response import closeable_response
except ImportError:
    from twill.other_packages.mechanize._response import closeable_response

def patched_do_open(self, http_class, req):
    """XXX This is copied from the mechanize AbstractHTTPHandler
       The difference is that we modify the host to request to
       if we have a mapping specified for it, while leaving the
       host header intact

    http_class must implement the HTTPConnection API from httplib.
    The addinfourl return value is a file-like object.  It also
    has methods and attributes including:
    - info(): return a mimetools.Message object for the headers
    - geturl(): return the original request URL
    - code: HTTP status code
    """

    host = req.get_host()
    if not host:
        raise URLError('no host given')

    headers = dict(req.headers)
    headers.update(req.unredirected_hdrs)
    # We want to make an HTTP/1.1 request, but the addinfourl
    # class isn't prepared to deal with a persistent connection.
    # It will try to read all remaining data from the socket,
    # which will block while the server waits for the next request.
    # So make sure the connection gets closed after the (only)
    # request.
    headers["Connection"] = "close"
    headers = dict(
        [(name.title(), val) for name, val in headers.items()])

    # here is the difference with the mechanize implementation
    # we modify the host to request to if we have a mapping for it
    # the old host will still get placed in the header though

    old_host = host 
    host, init_selector = map_host_name(host)
    if old_host != host: 
        print "[!] host_alias mapped %s -> %s" % (old_host, host)


    selector = init_selector + req.get_selector()

    h = http_class(host) # will parse host:port
    h.set_debuglevel(self._debuglevel)

    try:
        h.request(req.get_method(), selector, req.data, headers)
        r = h.getresponse()
    except socket.error, err: # XXX what error?
        raise URLError(err)

    # Pick apart the HTTPResponse object to get the addinfourl
    # object initialized properly.

    # Wrap the HTTPResponse object in socket's file object adapter
    # for Windows.  That adapter calls recv(), so delegate recv()
    # to read().  This weird wrapping allows the returned object to
    # have readline() and readlines() methods.

    # XXX It might be better to extract the read buffering code
    # out of socket._fileobject() and into a base class.

    r.recv = r.read
    fp = socket._fileobject(r)

    resp = closeable_response(fp, r.msg, req.get_full_url(),
                              r.status, r.reason)
    return resp


def map_host_name(old_host):
    # get the mapping from the flunc module
    from flunc import hostname_redirect_mapping
    host = hostname_redirect_mapping.get(old_host, old_host)
    slash_pos = host.find('/')
    if slash_pos == -1:
        return host, ''
    else:
        host, selector = host[:slash_pos], host[slash_pos:]
        return host, selector
        

def patch_browser():
    # patch the do_open method of the http handler class
    # to our do_open function above
    browser = twill.get_browser()
    http_handler = browser._browser.handler_classes['http']
    http_handler.do_open = patched_do_open
