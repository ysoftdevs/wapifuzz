from encodings_helper import Encoder, EncodingTypes


def generate_json_dict_from_schema(json_schema):
    json_dict = _iterate_over_properties(json_schema)
    return json_dict


def _iterate_over_properties(properties):
    json_dict = {}

    # 1] Just single key-value tuple of JSON structure, recursively decomposing JSON value
    if isinstance(properties, tuple):
        json_key = properties[0]
        json_value = properties[1]
        nested = _iterate_over_properties(json_value)
        json_dict[json_key] = nested
    # 2] Value is an JSON array, need to find out type and generate few array items
    elif "Type" in properties and "ArrayItemSchema" in properties and properties["Type"] == "array":
        return [_parse_array_schema(properties)]
    # 3] Properties contains description of single JSON primitive
    elif "Type" in properties and "Format" in properties:
        property_type = properties["Type"]
        property_format = properties["Format"]
        if properties["Example"]:
            return _convert_example_to_right_data_type(property_type, properties["Example"])
        return _get_example_by_type(property_type, property_format)
    # 4] Properties contains JSON dictionary and need to be recursively parsed further
    else:
        json_values = properties.items()
        for value in json_values:
            nested = _iterate_over_properties(value)
            json_dict = {**json_dict, **nested}
    return json_dict


def _parse_array_schema(array_schema):
    single_item_schema = array_schema["ArrayItemSchema"]
    property_type = single_item_schema["Type"] if "Type" in single_item_schema else None
    property_format = single_item_schema["Format"] if "Format" in single_item_schema else None
    if property_type and property_format:
        return _get_example_by_type(single_item_schema["Type"], single_item_schema["Format"])
    else:
        return _iterate_over_properties(single_item_schema)


# If there is no example, we have to generate one
# Based on following documentations:
# https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md
# https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md
def _get_example_by_type(property_type, property_format):
    if property_type == "boolean":
        return True
    elif property_type == "integer":
        return 0
    elif property_type == "number":
        return 0.0
    elif property_type == "string":
        if property_format == "byte":
            return Encoder.encode_string("example", encoding_type=EncodingTypes.base64)
        elif property_format == "binary":
            return "01234567"
        elif property_format == "date":
            return "2002-10-02"
        elif property_format == "date-time":
            return "2002-10-02T10:00:00-05:00"
        elif property_format == "password":
            return "string"
        else:
            return "string"


# Examples from documentation comes as JSON strings, we need to cast them to proper data type
# Should never fail, because parser will throw an error if data type in documentation is not matching
def _convert_example_to_right_data_type(property_type, example_value):
    if property_type == "integer":
        return int(example_value)
    elif property_type == "number":
        return float(example_value)
    elif property_type == "boolean":
        return str(example_value).lower() == "true"
    else:
        return example_value
