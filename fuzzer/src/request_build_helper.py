import json
from boofuzz import s_static, s_size
from fuzz_payloads import s_http_string, s_http_number, s_http_boolean
from encodings_helper import EncodingTypes
from parameter import Parameter


class RequestBuildHelper(object):

    # Content-length and Host are mandatory
    @staticmethod
    def generate_headers(config):
        # Append headers from config
        headers = config["headers"]
        if headers is not None:
            for key, value in headers.items():
                s_static(key + ": " + value)
                s_static("\r\n")

        # Append host, if it is not provided in config
        if not RequestBuildHelper._is_header_in_config(headers, "Host"):
            s_static("Host: " + config["target"]["hostname"])
            s_static("\r\n")

        # Append content-length, if it is not provided in config
        if not RequestBuildHelper._is_header_in_config(headers, "Content-Length"):
            s_static('Content-Length: ')
            # s_size calculates the byte length of Boofuzz block with name "body",
            # which contains whole HTTP request content part. with actual mutation.
            s_size("body", output_format="ascii", fuzzable=False)

    @staticmethod
    def _is_header_in_config(headers, header_name):
        return headers is not None and header_name in headers

    @staticmethod
    def generate_uri(uri, uri_parameters, config, fuzzable=False):
        fixed_attributes = config["fixed_url_attributes"] if "fixed_url_attributes" in config else None
        id_generator = _unique_uri_attribute_id()

        while True:
            try:
                # Find first not yet found parameter, if there is one
                index = uri.index("{")
                prefix = uri[0:index]
                s_http_string(prefix, fuzzable=False, encoding=EncodingTypes.ascii)
                uri = uri[index + 1:]
                index = uri.index("}")
                parameter_name = uri[0:index]

                parameter: Parameter = RequestBuildHelper._get_parameter(parameter_name, fixed_attributes, uri_parameters)
                name = "URI attribute, default value: " + parameter.value + ", id: " + next(id_generator)
                is_part_fuzzable = fuzzable and not parameter.is_from_config

                if parameter.data_type and (parameter.data_type == 'integer' or parameter.data_type == 'number'):
                    s_http_number(parameter.value, fuzzable=is_part_fuzzable, encoding=EncodingTypes.urlencoded, name=name)
                elif parameter.data_type and parameter.data_type == 'string':
                    s_http_boolean(parameter.value, fuzzable=is_part_fuzzable, encoding=EncodingTypes.urlencoded, name=name)
                else:
                    s_http_string(parameter.value, fuzzable=is_part_fuzzable, encoding=EncodingTypes.urlencoded, name=name)

                uri = uri[index + 1:]
            except ValueError:
                if len(uri) > 0:
                    name = "URI attribute, default value: " + uri + ", id: " + next(id_generator)
                    s_http_string(uri, fuzzable=False, encoding=EncodingTypes.ascii, name=name)
                break

    # Getting parameter value from these sources (ordered):
    # 1] Fixed attributes from config
    # 2] Example value from documentation
    # 3] Placeholder 'attribute'
    @staticmethod
    def _get_parameter(parameter_name, fixed_attributes, uri_parameters) -> Parameter:
        if fixed_attributes is not None and parameter_name in fixed_attributes:
            return Parameter(parameter_name, fixed_attributes[parameter_name], None, None, True)
        elif any(parameter["Name"] == parameter_name for parameter in uri_parameters):
            for parameter in uri_parameters:
                if parameter["Name"] == parameter_name:
                    return Parameter(parameter_name, parameter["ExampleValue"], parameter["Type"], parameter["Format"], False)
        else:
            return Parameter(parameter_name, 'attribute', None, None, False)

    @staticmethod
    def is_string_valid_json(input_string: str) -> bool:
        try:
            json.loads(input_string)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_request_name(uri, method_type) -> str:
        return uri + ", " + method_type


def _unique_uri_attribute_id():
    sequence = 0
    while True:
        yield str(sequence)
        sequence += 1
