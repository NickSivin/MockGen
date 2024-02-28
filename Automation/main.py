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
    def __init__(self, function, custom_name):
        self.function = function
        self.name = parser.function_name(function)
        self.custom_name = custom_name
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
    file.seek(0)
    protocol_lines = __make_protocol_body_lines(file, protocol_definition)
    functions = __make_protocol_functions(protocol_lines)
    properties = __make_protocol_properties(protocol_lines)

    mock_file_name = protocol_name.replace(config.PROTOCOL_IDENTIFICATION, '', 1) + 'Mock'
    mock_file_path = os.path.join(root_path, config.OUTPUT_PATH, f'{mock_file_name}.swift')
    with open(mock_file_path, 'w') as mock_file:
        file.seek(0)
        file_helper.write_header(mock_file, mock_file_name)
        file_helper.write_imports(mock_file, file)
        file_helper.write_class_start_line(mock_file, mock_file_name, protocol_name)
        for property_info in properties:
            file_helper.write_property(mock_file, property_info)
        for function_info in functions:
            file_helper.write_function(mock_file, function_info)
        file_helper.write_class_end_line(mock_file)


def __make_protocol_body_lines(file, protocol_definition):
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
    prev_line = ''
    custom_name_candidate = ''
    for line in lines:
        if line.startswith('//'):
            prev_line = line
            continue
        if line.startswith('func'):
            __append_function(function, functions, custom_name_candidate)
            function = line
            custom_name_candidate = prev_line
        elif line.startswith('var'):
            __append_function(function, functions, custom_name_candidate)
            function = ''
            custom_name_candidate = ''
            continue
        else:
            if function.endswith(','):
                function += ' '
            function += line
        prev_line = line
    __append_function(function, functions, custom_name_candidate)
    return functions


def __append_function(function, functions, custom_name_candidate):
    if not function:
        return

    custom_name = parser.function_custom_name(custom_name_candidate)
    functions.append(FunctionInfo(function.strip(), custom_name.strip()))


if __name__ == '__main__':
    generate()
