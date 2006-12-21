from mechanize._http import HTTPRedirectHandler
from mechanize._html import clean_url

class CleanURLRedirectHandler(HTTPRedirectHandler):
    """
    Override the redirect request method to pass in a url encoded url
    """

    def redirect_request(self, newurl, req, fp, code, msg, headers):
        url = clean_url(newurl, 'utf-8')
        return HTTPRedirectHandler.redirect_request(self,
                                                    url,
                                                    req,
                                                    fp,
                                                    code,
                                                    msg,
                                                    headers)
