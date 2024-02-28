# Path to script files
FILE_PATH = 'Automation'
# Path to project sources files
SOURCES_PATH = 'Sources'
# Path to folder for generated mock files
OUTPUT_PATH = 'Mocks'
# Identification word or symbol for each protocol
# !!! REQUIRED for correctly compose mock file name (e.g. NetworkServiceProtocol -> NetworkServiceMock)
PROTOCOL_IDENTIFICATION = 'Protocol'
# Name of main module
TESTABLE_MODULE = 'Project'
# Name of test module
TEST_MODULE = 'ProjectTests'
# List of protocols to generate mock files
PROTOCOL_LIST = [
    # Protocol names (e.g. NetworkServiceProtocol, etc.)
    'ServiceProtocol', 'StorageProtocol'
]
