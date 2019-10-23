import sys
import json
from fuzz_payloads import FuzzPayloads
from text_logger import TextLogger
from junit_logger import JUnitLogger
from payloads.payloads_loader import PayloadsLoader, load_default_payloads
from configuration_manager import ConfigurationManager
from fuzzer import Fuzzer


def main():
    config_file_path = sys.argv[1]
    endpoints_description = sys.argv[2]
    junit_output = sys.argv[3]
    custom_payloads_path = sys.argv[4] if len(sys.argv) == 5 else None

    with open(config_file_path, 'r') as config_file_pointer:
        ConfigurationManager(config_file_pointer)

    target = ConfigurationManager.config["target"]

    # Load and generate default payloads
    load_default_payloads(target["hostname"])

    # If user specified file with custom payloads, we add them to our mutations
    payloads_loader = PayloadsLoader(target["hostname"])
    payloads_loader.load_payloads(custom_payloads_path, FuzzPayloads.CUSTOM_PAYLOADS_KEY)

    with open(junit_output, 'w', encoding='utf8') as junit_output_file_pointer:
        text_logger = TextLogger()
        junit_logger = JUnitLogger(junit_output_file_pointer, test_suite_name_delimiter=":", hostname=target["hostname"])
        protocol = 'ssl' if target["ssl"] is True else 'tcp'

        with open(endpoints_description, 'r') as endpoints_description_file_pointer:
            endpoints = json.loads(endpoints_description_file_pointer.read())

        fuzzer = Fuzzer(endpoints, text_logger, junit_logger, protocol)
        fuzzer.fuzz()


if __name__ == '__main__':
    main()
