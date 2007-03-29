import twill 
from twill.namespaces import get_twill_glocals

from flunc import hostname_redirect_mapping
from parser import _substitute_vars

__all__ = ['host_alias']

def host_alias(old_host, new_host):
    twill_globals, _locals = get_twill_glocals()
    old_host_subst = _substitute_vars(old_host, twill_globals)
    new_host_subst = _substitute_vars(new_host, twill_globals)

    hostname_redirect_mapping[old_host_subst] = new_host_subst
