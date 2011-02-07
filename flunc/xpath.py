from twill.namespaces import get_twill_glocals 
from twill.commands import get_browser
from twill.errors import TwillAssertionError
from twill.errors import TwillException
from flunc import options
from logging import log_error, log_warn
from lxml.etree import XPathEvalError
import lxml.html
import re
from lxml.cssselect import CSSSelector

__all__ = ['find_in_xpath', 'notfind_in_xpath', 'find_in_css', 'notfind_in_css', 'css_len']

def css_len(css, num):
    num = int(num)

    _, twill_locals = get_twill_glocals()
    browser = get_browser()
    html = browser.get_html()
    tree = lxml.html.document_fromstring(html)
    sel = CSSSelector(css)
    results = sel(tree)
    
    actual_num = len(results)
    if actual_num != num:
        raise TwillAssertionError("Expected %s matches to \"%s\"; found %s" % (
                num, css, actual_num))

def find_in_css(what, css):
    _, twill_locals = get_twill_glocals()
    browser = get_browser()
    html = browser.get_html()
    tree = lxml.html.document_fromstring(html)
    sel = CSSSelector(css)
    results = sel(tree)
    results = '\n'.join(lxml.html.tostring(r)
                        for r in results)

    regexp = re.compile(what, re.IGNORECASE)
    m = regexp.search(results)
    if not m:
        raise TwillAssertionError("no match to '%s' in '%s'" %
                                  (what, results))

    if m.groups():
        match_str = m.group(1)
    else:
        match_str = m.group(0)
    twill_locals['__match__'] = match_str

def notfind_in_css(what, css):
    try:
        find_in_css(what, css)
    except TwillAssertionError:
        return
    raise TwillAssertionError("match to '%s' in %s" % (what, repr(css)))

def _run_xpath(xpath):
    _, twill_locals = get_twill_glocals()
    browser = get_browser()
    html = browser.get_html()
    tree = lxml.html.document_fromstring(html)

    try:
        results = tree.xpath(xpath)
    except XPathEvalError:
        err_msg = "Invalid xpath expression: '%s'" % xpath
        log_error(err_msg)
        raise TwillException(err_msg)

    #XXX we aggregate all the values together and warn when there is more than
    #one result
    if results:
        if len(results) > 1:
            log_warn("xpath '%s' found multiple results: using all of them" % xpath)
        result = '\n'.join(lxml.html.tostring(r) for r in results)
    else:
        log_error("xpath '%s' found no results")
        result = ''
    # in case we want to cache it at some point
    twill_locals['__xpath_result__'] = result
    twill_locals['__xpath_expr__'] = xpath
    return result

#XXX add in argument to pass in flags?
def find_in_xpath(what, xpath):
    _, twill_locals = get_twill_glocals()
    xpath_result = _run_xpath(xpath)
    #XXX we just ignore case for now
    #if we need to differentiate then we can pass in a flag
    regexp = re.compile(what, re.IGNORECASE)
    m = regexp.search(xpath_result)
    if not m:
        raise TwillAssertionError("no match to '%s' in '%s'" %
                                  (what, xpath_result))
    if m.groups():
        match_str = m.group(1)
    else:
        match_str = m.group(0)
    twill_locals['__match__'] = match_str

def notfind_in_xpath(what, xpath):
    try:
        find_in_xpath(what, xpath)
    except TwillAssertionError:
        return
    raise TwillAssertionError("match to '%s' in %s" % (what, repr(xpath)))

#XXX add a find_last_xpath to make re-running finds on xpaths easier
