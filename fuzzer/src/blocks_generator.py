import json
from typing import Union
from boofuzz import s_initialize, s_delim, s_static, s_block_start, s_block_end
from request_build_helper import RequestBuildHelper
from configuration_manager import ConfigurationManager
from fuzz_payloads import s_http_string
from fuzzing_json_decoder import FuzzingJsonDecoder
from encodings_helper import EncodingTypes


# 1] General HTTP fuzzing
def generate_http_fuzzed_blocks() -> str:
    request_name = "General HTTP fuzzing:"
    s_initialize(name=request_name)

    s_http_string("GET", name="HTTP method")
    s_delim(" ", name="Delimiter between method and path")
    s_http_string("/path", encoding=EncodingTypes.ascii, name="HTTP path")
    s_delim(" ", name="Delimiter between path and version")
    s_http_string("HTTP/1.1\r\n", name="HTTP version")

    s_static("Host: " + ConfigurationManager.config["target"]["hostname"] + "\r\n")

    s_static("Content-Length: 0" + "\r\n")

    s_static("User-Agent: ")
    s_http_string("WFuzz", name="User-agent")

    s_delim("\r\n\r\n", name="HTTP headers and body delimiter")

    return request_name


# 2] URI attributes fuzzing
def generate_url_attributes_fuzzed_blocks(endpoint, request) -> str:
    body_str = request["BodyExample"]
    body_schema = request["BodySchema"]
    is_body_json, json_decoder = _prepare_content_body(body_str, body_schema, True)

    request_name = "URI attributes fuzzing: " + \
                   RequestBuildHelper.get_request_name(endpoint["Uri"], request["Method"])
    s_initialize(name=request_name)

    _generate_http_header(request, endpoint, fuzzable=True)

    _generate_content_body(is_body_json, json_decoder, body_str, fuzzable=False)

    return request_name


# 3] Request body fuzzing
def generate_body_fuzzed_blocks(endpoint, request, add_quotation_marks_into_non_string_primitives=False) -> str:
    body_str = request["BodyExample"]
    body_schema = request["BodySchema"]
    is_body_json, json_decoder = _prepare_content_body(body_str, body_schema, add_quotation_marks_into_non_string_primitives)

    subcategory_name = " (adding quotation marks)" if add_quotation_marks_into_non_string_primitives else ''
    request_name = "Request body fuzzing" + subcategory_name + ": " + RequestBuildHelper.get_request_name(endpoint["Uri"], request["Method"])
    s_initialize(name=request_name)

    _generate_http_header(request, endpoint, False)

    _generate_content_body(is_body_json, json_decoder, body_str, True)

    return request_name


def _prepare_content_body(documentation_body_example, documentation_body_schema, add_quotation_marks_into_non_string_primitives):
    is_body_json = True if documentation_body_example and RequestBuildHelper.is_string_valid_json(documentation_body_example) else False

    json_decoder: Union[FuzzingJsonDecoder, None] = FuzzingJsonDecoder(add_quotation_marks_into_non_string_primitives)
    if is_body_json:
        json_decoder.decode_dict(json.loads(documentation_body_example))
    elif documentation_body_schema:
        is_body_json = True
        json_decoder.generate_from_schema(documentation_body_schema)

    return is_body_json, json_decoder


def _generate_content_body(is_body_json, json_decoder, body_string_example, fuzzable):
    if s_block_start("body"):
        if is_body_json:
            json_decoder.generate_mutations(fuzzable=fuzzable)
        elif body_string_example:
            s_http_string(body_string_example, name="Whole HTTP body", fuzzable=fuzzable)
    s_block_end()


def _generate_http_header(request, endpoint, fuzzable):
    s_static(request["Method"].upper() + " ")
    RequestBuildHelper.generate_uri(endpoint["Uri"], request["UriAttributes"], ConfigurationManager.config, fuzzable)
    s_static(" HTTP/1.1\r\n")
    RequestBuildHelper.generate_headers(ConfigurationManager.config)
    s_static("\r\n\r\n")

