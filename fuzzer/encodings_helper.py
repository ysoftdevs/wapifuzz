import json
import urllib.parse
import base64
from enum import Enum
from typing import Dict, List, Union


class EncodingTypes(Enum):
    ascii = 1,
    utf8 = 2,
    urlencoded = 3,
    base64 = 4,
    json_string_escaping = 5


class Encoder:
    @staticmethod
    def encode_string(value: Union[str, bytes], encoding_type: EncodingTypes) -> bytes:

        # If value is already in bytes, I assume that is properly encoded
        if isinstance(value, bytes):
            return value

        if encoding_type == EncodingTypes.ascii:
            return value.encode('ascii', 'ignore')
        elif encoding_type == EncodingTypes.utf8:
            return value.encode('utf8', 'ignore')
        elif encoding_type == EncodingTypes.urlencoded:
            return urllib.parse.quote(value)
        elif encoding_type == EncodingTypes.base64:
            return base64.b64encode(bytes(value))
        elif encoding_type == EncodingTypes.json_string_escaping:
            return json.dumps(value)[1:][:-1].encode('utf8', 'ignore')
        else:
            raise NotImplementedError

    @staticmethod
    def encode_dict(dictionary, encoding_type: EncodingTypes) -> Union[Dict, List[Dict], bytes]:
        if isinstance(dictionary, dict):
            return {Encoder.encode_dict(key, encoding_type): Encoder.encode_dict(value, encoding_type)
                    for key, value in dictionary.items()}
        elif isinstance(dictionary, list):
            return [Encoder.encode_dict(element, encoding_type) for element in dictionary]
        elif isinstance(dictionary, str):
            return Encoder.encode_string(dictionary, encoding_type)
        else:
            return dictionary

    @staticmethod
    def get_ascii_encoded_quotation_mark():
        return Encoder.encode_string("\"", EncodingTypes.ascii)
