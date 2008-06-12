import twill
from twill import commands
from twill.errors import TwillAssertionError
try:
    from twill.other_packages import ClientForm
except ImportError:
    from twill.other_packages._mechanize_dist import ClientForm

__all__ = ['edit_checkbox', 'check_group_values', 'has_multiple_values', 'is_disabled', 'is_selected']

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

def is_disabled(formname, name, value=None):
    """Raise an exception if the named control is not disabled.  If
    the value argument is passed, the test applies only to options
    with that value.
    """
    browser = twill.get_browser()
    form = browser.get_form(formname)
    if not form:
        raise TwillAssertionError("no matching forms!")
    control = browser.get_form_field(form, name)
    if value:
        if not (control.disabled or control.get_item_disabled(value)):
            raise TwillAssertionError("%r value %r not disabled!" % (name, value))
        return
    if not control.disabled:
        raise TwillAssertionError("input %r not disabled!" % name)

def is_selected(formname, name, value):
    """Raise an exception if the control option with the given value
    is not selected.
    (Useful eg. for making assertions about form defaults.)
    """
    browser = twill.get_browser()
    form = browser.get_form(formname)
    if not form:
        raise TwillAssertionError("no matching forms!")
    control = browser.get_form_field(form, name)
    if not control.get(value)._selected:
        raise TwillAssertionError("%r option %r not selected!" % (name, value))

