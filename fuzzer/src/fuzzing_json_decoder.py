import json
from typing import Union
from json_schema_parser import generate_json_dict_from_schema
from fuzz_payloads import s_http_string, s_http_number, s_http_boolean
from encodings_helper import EncodingTypes


class FuzzingJsonDecoder:
    def __init__(self, add_quotation_marks_into_non_string_primitives: bool):
        self.parts: [JsonStrPart] = []
        self.add_quotation_marks_into_non_string_primitives = add_quotation_marks_into_non_string_primitives

    def generate_from_schema(self, json_schema):
        json_dict = generate_json_dict_from_schema(json_schema)
        self.decode_dict(json_dict)

    def decode_dict(self, json_dict):
        if json_dict is not None:
            self._decode_dict(json_dict)

    def _decode_dict(self, json_dict, indent='', is_last=True):
        self.parts.append(JsonStrPart('{\n', fuzzable=False))
        i = 0
        for key, val in json_dict.items():
            i += 1
            is_sub_item_last = True if i == len(json_dict.items()) else False
            self.parts.append(JsonStrPart('{}  "{}": '.format(indent, key), fuzzable=False))
            if isinstance(val, dict):
                self._decode_dict(val, indent + '  ', is_sub_item_last)
            elif isinstance(val, list) or isinstance(val, tuple):
                self.__decode_list(val, indent, is_sub_item_last)
            else:
                self.__parse_primitive(val, is_sub_item_last)

        self.parts.append(JsonStrPart(indent + '}\n' if is_last else indent + '},\n', fuzzable=False))

    def __decode_list(self, lst, indent, is_last):
        self.parts.append(JsonStrPart('[', fuzzable=False))
        i = 0
        for item in lst:
            i += 1
            is_sub_item_last = True if i == len(lst) else False
            if isinstance(item, list) or isinstance(item, tuple):
                self.__decode_list(item, indent, is_sub_item_last)
            elif isinstance(item, dict):
                self._decode_dict(item, indent, is_sub_item_last)
            else:
                self.__parse_primitive(item, is_sub_item_last, True)

        self.parts.append(JsonStrPart(']\n' if is_last else '],\n', fuzzable=False))

    def __parse_primitive(self, value, is_last, is_in_list=False):
        # We need to convert Python data types into JSON primitives variants (e.g. False -> false, sanitization, etc.)
        # A little "hack", convert value using built-in JSON parser into dictionary with single value and then parse value
        json_value = json.dumps({"value": value})[10:-1]

        if type(value) == str:
            json_value = json_value[1:-1]       # Remove auto-generated quotation marks
            self._add_quotation_mark()
            self.parts.append(JsonStrPart(json_value, fuzzable=True, json_primitive_type=str, encoding=EncodingTypes.json_string_escaping))
            self._add_quotation_mark()
        else:
            self.parts.append(JsonStrPart(json_value, fuzzable=True, json_primitive_type=type(value), add_quotation_marks_into_payloads=self.add_quotation_marks_into_non_string_primitives))

        if not is_last:
            self.parts.append(JsonStrPart(', ', fuzzable=False))
        if not is_in_list:
            self.parts.append(JsonStrPart('\n', fuzzable=False))

    def _add_quotation_mark(self):
        self.parts.append(JsonStrPart("\"", fuzzable=False))

    def generate_mutations(self, fuzzable=True):
        sequence_generator = _unique_json_primitive_id()
        for part in self.parts:
            name = "JSON Primitive, default value: " + part.value + ", id: " + next(sequence_generator)

            if part.json_primitive_type == int or part.json_primitive_type == float:
                s_http_number(part.value, fuzzable=fuzzable and part.fuzzable, encoding=part.encoding, name=name, add_quotation_marks=part.add_quotation_marks_into_payloads)
            elif part.json_primitive_type == bool:
                s_http_boolean(part.value, fuzzable=fuzzable and part.fuzzable, encoding=part.encoding, name=name, add_quotation_marks=part.add_quotation_marks_into_payloads)
            else:
                s_http_string(part.value, fuzzable=fuzzable and part.fuzzable, encoding=part.encoding, name=name)


class JsonStrPart:
    def __init__(self, value, fuzzable=True, encoding=EncodingTypes.utf8, json_primitive_type=None, add_quotation_marks_into_payloads=False):
        self.value: str = value
        self.fuzzable: bool = fuzzable
        self.encoding: EncodingTypes = encoding
        self.json_primitive_type: Union[type, None] = json_primitive_type
        self.add_quotation_marks_into_payloads: bool = add_quotation_marks_into_payloads


def _unique_json_primitive_id():
    sequence = 0
    while True:
        yield str(sequence)
        sequence += 1
