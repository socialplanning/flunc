from flunc import options
from logging import log_error
from logging import log_warn
from twill.commands import go
from twill.commands import get_browser

def destroy_posts(projurl):
    """delete all blog posts in a project"""

    log_warn("(wordpress) Deleting posts")
    
    url = '%s/blog/wp-admin/edit.php' % projurl

    def delete_links():
        go(url)
        return [link.url for link in get_browser()._browser.links()
                if link.text == 'Delete']

    try:
        for link in delete_links():
            go('%s/blog/wp-admin/%s' % (projurl, link))
    except:
        if options.verbose:
            raise
        log_error("Error removing posts from '%s'" % projurl)

    assert not delete_links()
