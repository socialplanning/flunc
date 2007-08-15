import os
from tempfile import NamedTemporaryFile
import flunc
import twill
from twill.namespaces import get_twill_glocals
from logging import log_info
from parser import substitute_vars

__all__ = ['fake_form']


def fake_form(filename):
    """
    Subsitite variables in the file
    given and make the current location
    the result. 

    eg this can be used to generate a form
    submitting "someinput" to an arbitrary url
    using a local file like 

    <html>
      <head>
      </head>
      <body>
        <form action="${form_action}">
          <input name="someinput" />
        </form>
      </body>
    </html>

    """

    search_path = flunc.options.search_path

    form_template_fn = os.path.join(search_path,
                                    filename)

    fake_form_template = open(form_template_fn).read()
    lookup = get_twill_glocals()[0]
    fake_form_data = substitute_vars(fake_form_template, lookup)

    fake_form = NamedTemporaryFile(mode="w", prefix="flunc-", suffix=".html")
    fake_form.write(fake_form_data)
    fake_form.flush()

    fake_form_url = "file://%s" % fake_form.name   
    twill.commands.go(fake_form_url)
