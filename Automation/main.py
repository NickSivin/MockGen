import fnmatch
import os
import config
import file_helper
import parser


class PropertyInfo:
    def __init__(self, property_line):
        self.property = parser.property_definition(property_line)
        self.name = parser.property_name(property_line)
        self.type = parser.property_type(property_line)
        self.read_only = 'set' not in property_line


class FunctionInfo:
    def __init__(self, function):
        self.function = function
        self.name = parser.function_name(function)
        self.custom_name = ''
        self.params = parser.function_params(function)
        self.generic_types = parser.function_generic_types(function)
        self.result_type = parser.function_result_type(function)
        self.actual_result_type = parser.replace_generic_type_if_needed(self.result_type, self.generic_types)


def generate():
    root_path = os.getcwd().replace(config.FILE_PATH, '')
    sources_path = root_path + config.SOURCES_PATH
    for root, dirs, files in os.walk(sources_path):
        for name in fnmatch.filter(files, '*.swift'):
            for protocol_name in config.PROTOCOL_LIST:
                file_path = os.path.join(root, name)
                with open(file_path) as file:
                    __check_protocol_in_file_and_generate_mock_file_if_needed(file, root_path, protocol_name)


def __check_protocol_in_file_and_generate_mock_file_if_needed(file, root_path, protocol_name):
    protocol_definition = f'protocol {protocol_name} {{'
    if protocol_definition in file.read():
        __generate_mock_file(file, root_path, protocol_definition, protocol_name)


def __generate_mock_file(file, root_path, protocol_definition, protocol_name):
    imports = parser.file_imports(file)
    protocol_lines = __make_protocol_body_lines(file, protocol_definition)
    functions = __make_protocol_functions(protocol_lines)
    properties = __make_protocol_properties(protocol_lines)
    __find_and_rename_all_duplicates(functions)

    mock_file_name = protocol_name.replace(config.PROTOCOL_IDENTIFICATION, '', 1) + 'Mock'
    mock_file_path = os.path.join(root_path, config.OUTPUT_PATH, f'{mock_file_name}.swift')
    with open(mock_file_path, 'w') as mock_file:
        file_helper.write_header(mock_file, mock_file_name)
        file_helper.write_imports(mock_file, imports)
        file_helper.write_class_start_line(mock_file, mock_file_name, protocol_name)
        for property_info in properties:
            file_helper.write_property(mock_file, property_info)
        for function_info in functions:
            file_helper.write_function(mock_file, function_info)
        file_helper.write_class_end_line(mock_file)


def __make_protocol_body_lines(file, protocol_definition):
    file.seek(0)
    lines = []
    is_inside_protocol = False
    for line in file:
        line = line.strip()
        if not line:
            continue
        if protocol_definition in line:
            is_inside_protocol = True
            continue
        if is_inside_protocol and line.startswith('}'):
            break
        if is_inside_protocol:
            lines.append(line)
    return lines


def __make_protocol_properties(lines):
    properties = []
    for line in lines:
        if line.startswith('//'):
            continue
        if line.startswith('var'):
            properties.append(PropertyInfo(line))
    return properties


def __make_protocol_functions(lines):
    functions = []
    function = ''
    for line in lines:
        if line.startswith('//'):
            continue
        if line.startswith('func'):
            __append_function(function, functions)
            function = line
        elif line.startswith('var'):
            __append_function(function, functions)
            function = ''
            continue
        else:
            if function.endswith(','):
                function += ' '
            function += line
    __append_function(function, functions)
    return functions


def __append_function(function, functions):
    if not function:
        return
    functions.append(FunctionInfo(function.strip()))


def __find_and_rename_all_duplicates(functions):
    functions = list(filter(lambda func: not func.custom_name, functions))
    # Find and rename duplicates with same name
    # by adding params name to end
    renamed_functions = __find_and_rename_duplicates(
        functions,
        lambda func: func.name,
        lambda param: __upper_param_part(param, 0)
    )
    # Find and rename duplicates with same custom name (e.g. functions has same parameters count)
    # by adding types of params to end
    __find_and_rename_duplicates(
        renamed_functions,
        lambda func: func.custom_name,
        lambda param: __upper_param_part(param, 1)
    )


def __upper_param_part(param, index):
    return __upper_first(param.split(':')[index].strip())


def __find_and_rename_duplicates(functions, func_name_lambda, param_part_lambda):
    duplicates = __find_duplicates(functions, func_name_lambda)
    grouped_functions = list(map(lambda items: __rename_duplicates(items[1], param_part_lambda), duplicates.items()))
    return __flattening_list(grouped_functions)


def __find_duplicates(functions, func_name_lambda):
    grouped_functions = {}
    for function in functions:
        function_name = func_name_lambda(function)
        if function_name in grouped_functions:
            grouped_functions[function_name].append(function)
        else:
            grouped_functions[function_name] = [function]
    return {k: v for k, v in grouped_functions.items() if len(v) > 1}


def __rename_duplicates(functions, param_part_lambda):
    for function in functions:
        params_string = ''.join(list(map(lambda param: param_part_lambda(param), function.params)))
        function.custom_name = function.name + params_string
    return functions


def __flattening_list(nested_sublists):
    return [item for sublist in nested_sublists for item in sublist]


def __upper_first(string):
    return string[:1].upper() + string[1:]


if __name__ == '__main__':
    generate()
