import config

def write_header(file, file_name):
    file.write('//\n')
    file.write(f'//  {file_name}.swift \n')
    file.write(f'//  {config.TEST_MODULE} \n')
    file.write('//\n')
    file.write('//  GENERATED FILE\n')
    file.write('//\n')


def write_imports(file, imports):
    file.write('\n')
    [file.write(f'{line.strip()}\n') for line in imports]
    file.write(f'@testable import {config.TESTABLE_MODULE}\n')
    file.write('\n')


def write_class_start_line(file, class_name, protocol_name):
    file.write(f'final class {class_name}: {protocol_name} {{')


def write_class_end_line(file):
    file.write('\n}')


def write_property(file, propertyInfo):
    file.write(f'\n\n\tvar {propertyInfo.name}Called: Bool {{ {propertyInfo.name}CalledCount > 0 }}')
    file.write(f'\n\tvar {propertyInfo.name}CalledCount = 0')
    file.write(f'\n\tvar {propertyInfo.name}ResultStub: {propertyInfo.type}!')
    file.write(f'\n\n\t{propertyInfo.property} {{')
    file.write('\n\t\tget {')
    file.write(f'\n\t\t\t{propertyInfo.name}CalledCount += 1')
    file.write(f'\n\t\t\treturn {propertyInfo.name}ResultStub')
    file.write('\n\t\t}')
    if not propertyInfo.read_only:
        file.write(f'\n\t\tset {{ {propertyInfo.name}ResultStub = newValue }}')
    file.write('\n\t}')


def write_function(file, functionInfo):
    function_name = functionInfo.name
    if functionInfo.custom_name:
        function_name = functionInfo.custom_name

    called_count_name = f'{function_name}CalledCount'
    called_parameters_list_name = f'{function_name}CalledParametersList'
    result_stub_name = f'{function_name}ResultStub'

    file.write(f'\n\n\tvar {function_name}Called: Bool {{ {function_name}CalledCount > 0 }}')
    file.write(f'\n\tvar {called_count_name} = 0')
    if functionInfo.params:
        string_params = ', '.join(functionInfo.params)
        if len(functionInfo.params) > 1:
            file.write(f'\n\tvar {called_parameters_list_name}: [({string_params})] = []')
        else:
            param_type = functionInfo.params[0].split(':')[1].strip()
            file.write(f'\n\tvar {called_parameters_list_name}: [{param_type}] = []')
    if functionInfo.result_type:
        file.write(f'\n\tvar {result_stub_name}: {functionInfo.actual_result_type}!')

    file.write(f'\n\n\t{functionInfo.function} {{')
    file.write(f'\n\t\t{called_count_name} += 1')
    if functionInfo.params:
        string_params = ', '.join(list(map(lambda param: param.split(':')[0].strip(), functionInfo.params)))
        if len(functionInfo.params) > 1:
            file.write(f'\n\t\t{called_parameters_list_name}.append(({string_params}))')
        else:
            file.write(f'\n\t\t{called_parameters_list_name}.append({string_params})')
    if functionInfo.result_type:
        if functionInfo.actual_result_type == functionInfo.result_type:
            file.write(f'\n\t\treturn {result_stub_name}')
        else:
            file.write(f'\n\t\treturn {result_stub_name} as! {functionInfo.result_type}')
    file.write('\n\t}')
