import re


def file_imports(file):
    file.seek(0)
    return list(filter(lambda line: line.startswith('import '), file))


def property_definition(property_line):
    return __first_match_or_empty(r'.*(?=\s{)', property_line)


def property_name(property_line):
    return __first_match_or_empty(r'(?<=var\s).*(?=:)', property_line)


def property_type(property_line):
    return __first_match_or_empty(r'(?<=:\s).[\w\.]+(?=\s{)', property_line)


def function_name(function):
    return __first_match_or_empty(r'(?<=func\s)[^(<|\()]*', function)


def function_params(function):
    params_string = __cut_string_between_symbols(function, '(', ')')
    if params_string:
        params = params_string.split(',')
        generic_types = function_generic_types(function)
        return list(map(lambda parameter: __sanitized_parameter(parameter.strip(), generic_types), params))
    else:
        return []


def function_result_type(function):
    if 'where' in function:
        return __first_match_or_empty(r'(?!.*>)(?!.*\))(?![async|throws])[^\s][\w\:\s\[\]]*(?=\swhere)', function)
    else:
        return __first_match_or_empty(r'(?!.*>)(?!.*\))(?![async|throws])[^\s][\w\:\s\[\]]+', function)


def function_generic_types(function):
    regex = r'(?<=<).+?(?=>)'
    match = re.search(regex, function)
    if match:
        list_of_types = match.group().split(',')
        return list(map(lambda generic_type: generic_type.strip().split(':')[0].strip(), list_of_types))
    else:
        return []


def replace_generic_type_if_needed(parameter_type, generic_types):
    parameter_type = parameter_type.split('.')[0] if '.' in parameter_type else parameter_type
    return 'Any' if parameter_type in generic_types else parameter_type


def __sanitized_parameter(parameter, generic_types):
    parts = parameter.split(':')

    parameter_name = parts[0].strip()
    if ' ' in parameter_name:
        parameter_name = parameter_name.split(' ')[-1]
    if parameter_name.startswith('_'):
        parameter_name = parameter_name[1:].strip()

    parameter_type = parts[1].strip()
    if '@escaping' in parameter_type:
        parameter_type = parameter_type.replace('@escaping', '').strip()
    parameter_type = replace_generic_type_if_needed(parameter_type, generic_types)

    return ': '.join([parameter_name, parameter_type])


def __first_match_or_empty(regex, string):
    match = re.search(regex, string)
    return match.group() if match else ''


def __cut_string_between_symbols(string, start_symbol, end_symbol):
    trimmed_string = __first_match_or_empty(fr'(?<=\{start_symbol}).*', string)
    count = 1
    result = ''
    for char in trimmed_string:
        if char == start_symbol:
            count += 1
        if char == end_symbol:
            count -= 1
        if count == 0:
            break
        result += char
    return result
