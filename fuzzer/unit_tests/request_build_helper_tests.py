import unittest
from request_build_helper import RequestBuildHelper
from boofuzz import *
from configuration_manager import ConfigurationManager


class RequestBuilderHelperTests(unittest.TestCase):
    def setUp(self):
        # Just init block for boofuzz
        s_initialize(self.id())

        ConfigurationManager.config = []

    def test_generate_simple_uri_without_parameters(self):
        uri_parameters = []
        base_uri = '/api/endpoint'

        RequestBuildHelper.generate_uri(base_uri, uri_parameters)

        uri = s_render().decode('utf8', 'ignore')
        self.assertEqual(base_uri, uri)

    def test_generate_uri_path_parameter_without_documentation(self):
        uri_parameters = []

        RequestBuildHelper.generate_uri('/api/endpoint/{id}', uri_parameters)

        uri = s_render().decode('utf8', 'ignore')
        self.assertEqual('/api/endpoint/attribute', uri)

    def test_generate_uri_path_parameter_with_fixed_config_value(self):
        uri_parameters = []
        ConfigurationManager.config = {
            "fixed_url_attributes": {
                "id": "20"
            }
        }

        RequestBuildHelper.generate_uri('/api/endpoint/{id}', uri_parameters)

        uri = s_render().decode('utf8', 'ignore')
        self.assertEqual('/api/endpoint/20', uri)

    def test_generate_uri_path_parameter_with_documented_example(self):
        uri_parameters = [{'Name': 'id', 'Required': True, 'ExampleValue': '1', 'Type': 'string', 'Format': None, 'Location': 'Path'}]

        RequestBuildHelper.generate_uri('/api/endpoint/{id}', uri_parameters)

        uri = s_render().decode('utf8', 'ignore')
        self.assertEqual('/api/endpoint/1', uri)

    def test_generate_uri_single_query_parameter_with_documented_example(self):
        uri_parameters = [{'Name': 'id', 'Required': True, 'ExampleValue': '1', 'Type': 'string', 'Format': None, 'Location': 'Query'}]

        RequestBuildHelper.generate_uri('/api/endpoint', uri_parameters)

        uri = s_render().decode('utf8', 'ignore')
        self.assertEqual('/api/endpoint?id=1', uri)

    def test_generate_uri_single_query_parameter_with_multiple_documented_examples(self):
        uri_parameters = [
            {'Name': 'id', 'Required': True, 'ExampleValue': '1', 'Type': 'string', 'Format': None, 'Location': 'Query'},
            {'Name': 'attr', 'Required': True, 'ExampleValue': '2', 'Type': 'string', 'Format': None, 'Location': 'Query'}
        ]

        RequestBuildHelper.generate_uri('/api/endpoint', uri_parameters)

        uri = s_render().decode('utf8', 'ignore')
        self.assertEqual('/api/endpoint?id=1&attr=2', uri)

    def test_generate_uri_single_non_required_query_parameter_is_not_in_uri(self):
        ConfigurationManager.config = {
            "are_non_required_attributes_in_requests": False
        }

        uri_parameters = [
            {'Name': 'id', 'Required': False, 'ExampleValue': '1', 'Type': 'string', 'Format': None, 'Location': 'Query'},
        ]

        RequestBuildHelper.generate_uri('/api/endpoint', uri_parameters)

        uri = s_render().decode('utf8', 'ignore')
        self.assertEqual('/api/endpoint', uri)

    def test_generate_uri_combined_parameters(self):
        ConfigurationManager.config = {
            "fixed_url_attributes": {
                "attr2": "20"
            }
        }
        uri_parameters = [
            {'Name': 'id', 'Required': True, 'ExampleValue': '1', 'Type': 'string', 'Format': None, 'Location': 'Path'},
            {'Name': 'attr1', 'Required': True, 'ExampleValue': '2', 'Type': 'string', 'Format': None, 'Location': 'Query'},
            {'Name': 'attr2', 'Required': True, 'ExampleValue': '3', 'Type': 'integer', 'Format': 'int32', 'Location': 'Query'}
        ]

        RequestBuildHelper.generate_uri('/api/endpoint/{id}', uri_parameters)

        uri = s_render().decode('utf8', 'ignore')
        self.assertEqual('/api/endpoint/1?attr1=2&attr2=20', uri)
