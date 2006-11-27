import re


variable_expression = re.compile("\${(.*?)}")

def _substitute_vars(raw_str, globals_dict):
    result = ''
    pos = 0
    for m in variable_expression.finditer(raw_str):
        result = result+raw_str[pos:m.start()]
        try:
            result += "'%s'" % eval(m.group(1), globals_dict, {})
        except NameError:
            raise NameError("Unbound variable '%s' in: '%s'" % \
                            (m.group(1), raw_str))
        pos = m.end()
    result += raw_str[pos:]
    return result

def make_dict_from_call(raw_str, globals_dict): 
    if raw_str: 
        str = 'dict' + _substitute_vars(raw_str, globals_dict)
        return eval(str)
    else: 
        return {}

def make_twill_local_defs(vars): 
    return '\n'.join("setlocal %s '%s'" % (k,v) for k,v in vars.items()) + '\n'


# valid regular expressions include name of test or suite
# or the name of a test as a function call with local overrides
# foo
# foo(user=${new_user})
# foo # optionally with comments
test_call_sep = re.compile("^\s*([^(\s]+)(\([^)]*?\))\s*(?:#.*)?$")
test_non_call = re.compile("^\s*([A-Za-z_.-]+)\s*(?:#.*)?$")

def parse_test_call(callstr): 
    match = test_call_sep.search(callstr)
    if not match: 
        match = test_non_call.search(callstr)
        if not match:
            raise ValueError("Invalid test name: '%s'" % callstr)
        else:
            return (match.group(1), '')
    
    return match.groups()
