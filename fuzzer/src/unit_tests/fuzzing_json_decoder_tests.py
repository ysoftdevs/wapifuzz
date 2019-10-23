import unittest
import json
from boofuzz import *
from fuzzing_json_decoder import FuzzingJsonDecoder
from fuzz_payloads import FuzzPayloads
from configuration_manager import ConfigurationManager


class FuzzingJsonDecoderTests(unittest.TestCase):
    def setUp(self):
        # Just init block for boofuzz
        s_initialize(self.id())

        # Generate at least few payloads for at least minimum number of mutations
        FuzzPayloads.add_payload_to_list("payload 1", FuzzPayloads.CUSTOM_PAYLOADS_KEY)
        FuzzPayloads.add_payload_to_list("payload 2", FuzzPayloads.CUSTOM_PAYLOADS_KEY)

        # Generate fake configuration
        ConfigurationManager.config = []

    def __json_equality_assertion(self, original_json, generated_json):
        self.assertDictEqual(json.loads(original_json), json.loads(generated_json))

    def test_empty_dict(self):
        # Prepare
        original_json = '{}'

        # Action
        decoder = FuzzingJsonDecoder(False)
        decoder.decode_dict(json.loads(original_json))
        decoder.generate_mutations()
        generated_json = s_render()

        # Assert
        self.__json_equality_assertion(original_json, generated_json)

    def test_empty_list(self):
        # Prepare
        original_json = '{"array": []}'

        # Action
        decoder = FuzzingJsonDecoder(False)
        decoder.decode_dict(json.loads(original_json))
        decoder.generate_mutations()
        generated_json = s_render()

        # Assert
        self.__json_equality_assertion(original_json, generated_json)

    def test_dict_primitives(self):
        # Prepare
        original_json = '{"array": [{"primitives": {"1": 1, "2": 1e1, "3": false, "4": null}}]}'

        # Action
        decoder = FuzzingJsonDecoder(False)
        decoder.decode_dict(json.loads(original_json))
        decoder.generate_mutations()
        generated_json = s_render()

        # Assert
        self.__json_equality_assertion(original_json, generated_json)

    def test_nested_dict(self):
        # Prepare
        original_json = '{ "problems": [{ "Diabetes":[{ "medications":[{ "medicationsClasses":[{ "className":[{ "associatedDrug":[{ "name":"asprin", "dose":"", "strength":"500 mg" }], "associatedDrug#2":[{ "name":"somethingElse", "dose":"", "strength":"500 mg" }] }], "className2":[{ "associatedDrug":[{ "name":"asprin", "dose":"", "strength":"500 mg" }], "associatedDrug#2":[{ "name":"somethingElse", "dose":"", "strength":"500 mg" }] }] }] }], "labs":[{ "missing_field": "missing_value" }] }], "Asthma":[{}] }]}'

        # Action
        decoder = FuzzingJsonDecoder(False)
        decoder.decode_dict(json.loads(original_json))
        decoder.generate_mutations()
        generated_json = s_render()

        # Assert
        self.__json_equality_assertion(original_json, generated_json)

    def test_huge_dict(self):
        # Prepare
        original_json = ' { "medications":[{ "aceInhibitors":[{ "name":"lisinopril", "strength":"10 mg Tab", "dose":"1 tab", "route":"PO", "sig":"daily", "pillCount":"#90", "refills":"Refill 3" }], "antianginal":[{ "name":"nitroglycerin", "strength":"0.4 mg Sublingual Tab", "dose":"1 tab", "route":"SL", "sig":"q15min PRN", "pillCount":"#30", "refills":"Refill 1" }], "anticoagulants":[{ "name":"warfarin sodium", "strength":"3 mg Tab", "dose":"1 tab", "route":"PO", "sig":"daily", "pillCount":"#90", "refills":"Refill 3" }], "betaBlocker":[{ "name":"metoprolol tartrate", "strength":"25 mg Tab", "dose":"1 tab", "route":"PO", "sig":"daily", "pillCount":"#90", "refills":"Refill 3" }], "diuretic":[{ "name":"furosemide", "strength":"40 mg Tab", "dose":"1 tab", "route":"PO", "sig":"daily", "pillCount":"#90", "refills":"Refill 3" }], "mineral":[{ "name":"potassium chloride ER", "strength":"10 mEq Tab", "dose":"1 tab", "route":"PO", "sig":"daily", "pillCount":"#90", "refills":"Refill 3" }] } ], "labs":[{ "name":"Arterial Blood Gas", "time":"Today", "location":"Main Hospital Lab" }, { "name":"BMP", "time":"Today", "location":"Primary Care Clinic" }, { "name":"BNP", "time":"3 Weeks", "location":"Primary Care Clinic" }, { "name":"BUN", "time":"1 Year", "location":"Primary Care Clinic" }, { "name":"Cardiac Enzymes", "time":"Today", "location":"Primary Care Clinic" }, { "name":"CBC", "time":"1 Year", "location":"Primary Care Clinic" }, { "name":"Creatinine", "time":"1 Year", "location":"Main Hospital Lab" }, { "name":"Electrolyte Panel", "time":"1 Year", "location":"Primary Care Clinic" }, { "name":"Glucose", "time":"1 Year", "location":"Main Hospital Lab" }, { "name":"PT/INR", "time":"3 Weeks", "location":"Primary Care Clinic" }, { "name":"PTT", "time":"3 Weeks", "location":"Coumadin Clinic" }, { "name":"TSH", "time":"1 Year", "location":"Primary Care Clinic" } ], "imaging":[{ "name":"Chest X-Ray", "time":"Today", "location":"Main Hospital Radiology" }, { "name":"Chest X-Ray", "time":"Today", "location":"Main Hospital Radiology" }, { "name":"Chest X-Ray", "time":"Today", "location":"Main Hospital Radiology" } ] }'

        # Action
        decoder = FuzzingJsonDecoder(False)
        decoder.decode_dict(json.loads(original_json))
        decoder.generate_mutations()
        generated_json = s_render()

        # Assert
        self.__json_equality_assertion(original_json, generated_json)

    def test_dicts_in_array(self):
        # Prepare
        original_json = '{ "one": { "two": [{ "four": { "name": "four1_name" } }, { "four": { "name": "four2_name" } }] } }'

        # Action
        decoder = FuzzingJsonDecoder(False)
        decoder.decode_dict(json.loads(original_json))
        decoder.generate_mutations()
        generated_json = s_render()

        # Assert
        self.__json_equality_assertion(original_json, generated_json)

    def test_that_quotation_marks_are_not_added_into_default_values(self):
        # Prepare
        original_json = '{ "one": false, "two": 0  }'

        # Action
        decoder = FuzzingJsonDecoder(True)
        decoder.decode_dict(json.loads(original_json))
        decoder.generate_mutations()
        generated_json = s_render()

        # Assert
        self.__json_equality_assertion(original_json, generated_json)


if __name__ == '__main__':
    unittest.main()
