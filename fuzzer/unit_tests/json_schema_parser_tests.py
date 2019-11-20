import unittest
import json
from json_schema_parser import generate_json_dict_from_schema


class FuzzingJsonDecoderTests(unittest.TestCase):

    def test_single_bool_primitive(self):
        # Prepare
        original_json_schema = '{"test": {"Title": null,"Type": "boolean","Format": null,"Example": null}}'
        loaded_json_schema = json.loads(original_json_schema)

        # Action
        generated_json = generate_json_dict_from_schema(loaded_json_schema)

        # Assert
        self.assertTrue("test" in generated_json)
        self.assertTrue(isinstance(generated_json["test"], bool))
        self.assertEqual(generated_json["test"], True)

    def test_nested_string_primitive_with_example(self):
        # Prepare
        original_json_schema = '{"test": {"nested": {"Title": null,"Type": "string","Format": null,"Example": "example"}}}'
        loaded_json_schema = json.loads(original_json_schema)

        # Action
        generated_json = generate_json_dict_from_schema(loaded_json_schema)

        # Assert
        self.assertTrue("test" in generated_json)
        self.assertTrue("nested" in generated_json["test"])
        self.assertTrue(isinstance(generated_json["test"]["nested"], str))
        self.assertEqual(generated_json["test"]["nested"], "example")

    def test_array_with_primitive(self):
        # Prepare
        original_json_schema = '{"test": {"Type": "array","ArrayItemSchema": {"Title": null,"Type": "number","Format": "double","Example": null}}}'
        loaded_json_schema = json.loads(original_json_schema)

        # Action
        generated_json = generate_json_dict_from_schema(loaded_json_schema)

        # Assert
        self.assertTrue("test" in generated_json)
        self.assertTrue(isinstance(generated_json["test"], list))
        self.assertTrue(isinstance(generated_json["test"][0], float))
        self.assertEqual(generated_json["test"][0], 0.0)

    def test_array_with_complex_object(self):
        # Prepare
        original_json_schema = '{"test": {"Type": "array","ArrayItemSchema": {"nested1": {"Title": null,"Type": "string","Format": null,"Example": "example"},"nested2": {"Title": null,"Type": "integer","Format": null,"Example": null}}}}'
        loaded_json_schema = json.loads(original_json_schema)

        # Action
        generated_json = generate_json_dict_from_schema(loaded_json_schema)

        # Assert
        self.assertTrue("test" in generated_json)
        self.assertTrue(isinstance(generated_json["test"], list))
        self.assertTrue(isinstance(generated_json["test"][0], dict))
        self.assertTrue("nested1" in generated_json["test"][0])
        self.assertTrue("nested2" in generated_json["test"][0])
        self.assertEqual(generated_json["test"][0]["nested1"], "example")
        self.assertEqual(generated_json["test"][0]["nested2"], 0)


if __name__ == '__main__':
    unittest.main()
