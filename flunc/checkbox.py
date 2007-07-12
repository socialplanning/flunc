import twill
from twill import commands
from twill.errors import TwillAssertionError
from twill.other_packages._mechanize_dist import ClientForm

__all__ = ['edit_checkbox', 'check_group_values']

def check_group_values(formname, name, values_str):
    """
    checks the values in the comma seperated list 'values'
    eg:
    check_radio_values('some_form', 'favorites', 'apples, bannanas, onions')
    """
    values = [x.strip() for x in values_str.split(',') if x.strip()]
    for value in values:
        edit_checkbox(formname, name, value)
        
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
