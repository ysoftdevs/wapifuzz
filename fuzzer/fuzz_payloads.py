from typing import List, Dict
from boofuzz import s_group, s_static
from encodings_helper import Encoder, EncodingTypes
from configuration_manager import ConfigurationManager


class FuzzPayloads:
    payloads: Dict[str, List[str]] = {}
    CUSTOM_PAYLOADS_KEY = "custom"

    @staticmethod
    def add_payload_to_list(line, directory_name):
        if directory_name not in FuzzPayloads.payloads:
            FuzzPayloads.payloads[directory_name] = []

        if line not in FuzzPayloads.payloads[directory_name]:
            FuzzPayloads.payloads[directory_name].append(line)

    @staticmethod
    def _get_payloads_using_directory_names(directory_names: List[str]) -> List[str]:
        directory_names.append(FuzzPayloads.CUSTOM_PAYLOADS_KEY)    # Always add custom payloads into any payloads set
        payloads: List[str] = []
        for directory_name in directory_names:
            if directory_name in FuzzPayloads.payloads:
                for line in FuzzPayloads.payloads[directory_name]:
                    payloads.append(line)
        return list(set(payloads))          # Remove duplicities

    @staticmethod
    def get_all_payloads():
        return FuzzPayloads._get_payloads_using_directory_names(list(FuzzPayloads.payloads.keys()))

    @staticmethod
    def _get_specific_type_payloads(payload_folders):
        return FuzzPayloads._get_payloads_using_directory_names(payload_folders) if payload_folders else FuzzPayloads.get_all_payloads()

    @staticmethod
    def get_string_payloads():
        payload_folders = ConfigurationManager.get_payloads_folders_for_string_json_primitive()
        return FuzzPayloads._get_specific_type_payloads(payload_folders)

    @staticmethod
    def get_number_payloads():
        payload_folders = ConfigurationManager.get_payloads_folders_for_number_json_primitive()
        return FuzzPayloads._get_specific_type_payloads(payload_folders)

    @staticmethod
    def get_boolean_payloads():
        payload_folders = ConfigurationManager.get_payloads_folders_for_boolean_json_primitive()
        return FuzzPayloads._get_specific_type_payloads(payload_folders)


def s_http_general(value, payloads, fuzzable=True, encoding: EncodingTypes = EncodingTypes.ascii, name=None, add_quotation_marks=False):
    # Encode all payloads
    encoded_payloads: List[bytes] = []
    for payload in payloads:
        encoded = Encoder.encode_string(payload, encoding)
        if add_quotation_marks:
            encoded = Encoder.get_ascii_encoded_quotation_mark() + encoded + Encoder.get_ascii_encoded_quotation_mark()
        encoded_payloads.append(encoded)

    # Encode default value
    default_value = Encoder.encode_string(value, encoding)
    if fuzzable:
        # noinspection PyTypeChecker
        s_group(name, encoded_payloads, default_value)
    else:
        s_static(default_value)


def s_http_string(value, fuzzable=True, encoding: EncodingTypes = EncodingTypes.ascii, name=None):
    s_http_general(value, FuzzPayloads.get_string_payloads(), fuzzable, encoding, name)


def s_http_number(value, fuzzable=True, encoding: EncodingTypes = EncodingTypes.ascii, name=None, add_quotation_marks=False):
    s_http_general(value, FuzzPayloads.get_number_payloads(), fuzzable, encoding, name, add_quotation_marks)


def s_http_boolean(value, fuzzable=True, encoding: EncodingTypes = EncodingTypes.ascii, name=None, add_quotation_marks=False):
    s_http_general(value, FuzzPayloads.get_boolean_payloads(), fuzzable, encoding, name, add_quotation_marks)
