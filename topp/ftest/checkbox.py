import twill
from twill import commands
import ClientForm

__all__ = ['edit_checkbox']

def edit_checkbox(formname, name, value):

    if has_multiple_values(formname, name):
        commands.fv(formname, name, value)
    else:
        if value.startswith('-'):
            commands.fv(formname, name, 'False')
        else:
            commands.fv(formname, name, 'True')

def has_multiple_values(formname, name):
    browser = twill.get_browser()
    form = browser.get_form(formname)
    if not form:
        raise TwillAssertionError("no matching forms!")
    control = browser.get_form_field(form, name)
    return hasattr(control, 'items') and len(control.items) > 1
