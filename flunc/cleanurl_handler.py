from mechanize._http import HTTPRedirectHandler
from mechanize._html import clean_url
from logging import log_warn

class CleanURLRedirectHandler(HTTPRedirectHandler):
    """
    Override the redirect request method to pass in a url encoded url
    """

    def redirect_request(self, url, req, fp, code, msg, headers):
        newurl = clean_url(url, 'utf-8')

        if newurl != url: 
            log_warn("Recieved possible unescaped url in redirect: %s using %s" % (url,newurl))

        return HTTPRedirectHandler.redirect_request(self,
                                                    newurl,
                                                    req,
                                                    fp,
                                                    code,
                                                    msg,
                                                    headers)
