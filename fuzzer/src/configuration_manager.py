import sys
import json
from typing import Union, List


class ConfigurationManager:
    config = None
    
    def __init__(self, config_file_pointer):
        ConfigurationManager.config = json.load(config_file_pointer)
        self._config_validation()

    @staticmethod
    def get_startup_command():
        return ConfigurationManager.config["startup_command"] if "startup_command" in ConfigurationManager.config else None

    @staticmethod
    def get_payloads_folders_for_boolean_json_primitive() -> Union[List, None]:
        return ConfigurationManager._get_payloads_folders_for_specific_json_primitive("boolean")

    @staticmethod
    def get_payloads_folders_for_number_json_primitive() -> Union[List, None]:
        return ConfigurationManager._get_payloads_folders_for_specific_json_primitive("number")

    @staticmethod
    def get_payloads_folders_for_string_json_primitive() -> Union[List, None]:
        return ConfigurationManager._get_payloads_folders_for_specific_json_primitive("string")

    @staticmethod
    def _get_payloads_folders_for_specific_json_primitive(json_type: str) -> Union[List, None]:
        mapping = ConfigurationManager._get_payloads_to_json_primitives_mapping()
        if mapping:
            return mapping[json_type] if json_type in mapping else None
        else:
            return None

    @staticmethod
    def _get_payloads_to_json_primitives_mapping():
        return ConfigurationManager.config["payloads_to_json_primitives_mapping"] if "payloads_to_json_primitives_mapping" in ConfigurationManager.config else None

    @staticmethod
    def get_receive_timeout():
        return ConfigurationManager.config["receive_timeout"]

    @staticmethod
    def get_reporting_interval():
        return ConfigurationManager.config["reporting_interval"]

    @staticmethod
    def get_keywords_for_endpoints_skipping() -> List:
        return ConfigurationManager.config["skipping_endpoints_keywords"]

    @staticmethod
    def get_target():
        return ConfigurationManager.config["target"]

    @staticmethod
    def is_http_fuzzing_allowed():
        return ConfigurationManager.config["http_fuzzing"]

    def _config_validation(self):
        reporting_interval: Union[int, float] = self.config["reporting_interval"]
        receive_timeout: Union[int, float] = self.config["receive_timeout"]
        http_fuzzing: bool = self.config["http_fuzzing"]

        if reporting_interval <= 0 or reporting_interval < receive_timeout:
            print("Wrong reporting interval. Should be smaller than response_timeout.")
            sys.exit(-1)

        if "target" not in ConfigurationManager.config:
            print("Missing configuration of target.")
            sys.exit(-1)

        if http_fuzzing is None:
            print("Missing flag for enabling / disabling HTTP fuzzing.")
            sys.exit(-1)
