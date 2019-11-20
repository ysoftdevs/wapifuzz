import copy
import sys
import re
from datetime import datetime
from typing import TextIO
from typing import List, Dict
from boofuzz import helpers, ifuzz_logger_backend
from junit_xml import TestSuite, TestCase
from fake_socket import get_response_object


class JUnitLogger(ifuzz_logger_backend.IFuzzLoggerBackend):
    DEFAULT_TEST_SUITE_NAME = "Default test suite"
    SKIPPED_TEST_CASE_MESSAGES_REGEX = ["Crash threshold reached for this element, exhausting (\d+) mutants.",
                                        "Crash threshold reached for this request, exhausting (\d+) mutants."]

    def __init__(self, file_handle: TextIO = sys.stdout, test_suite_name_delimiter: str = None, hostname: str = None):
        self._file_handle = file_handle
        self._test_suite_name_delimiter = test_suite_name_delimiter
        self._hostname = hostname

        self._test_cases = []
        self._actual_test_case = None
        self._error = None
        self._failure = None
        self._starting_time = None
        self._sent_string = None
        self._sent_bytes = None
        self._received_string = None
        self._received_bytes = None
        self._default_value = None
        self._mutant_value = None

        self.was_there_any_failure: bool = False

    def open_test_step(self, description):
        skipped_count = 0
        for skipped_test_case_message_regex in self.SKIPPED_TEST_CASE_MESSAGES_REGEX:
            match = re.match(skipped_test_case_message_regex, description)
            if match is not None:
                skipped_count += int(match.group(1))

        if skipped_count > 0:
            for i in range(skipped_count):
                skipped_test_case = self._create_skipped_test_case(self._actual_test_case.name, i)
                self._test_cases.append(skipped_test_case)

    def log_check(self, description):
        pass

    def log_error(self, description):
        self._error = description
        self.was_there_any_failure = True

    def log_recv(self, data):
        self._received_bytes = helpers.hex_str(data)
        self._received_string = data.decode('utf-8')

    def log_send(self, data):
        self._sent_bytes = helpers.hex_str(data)
        self._sent_string = data.decode('utf-8')

    def log_info(self, description):
        default_value_prefix = "Original value: "
        mutation_value_prefix = "Mutation: "
        if description.startswith(default_value_prefix):
            self._default_value = description[len(default_value_prefix):]
        elif description.startswith(mutation_value_prefix):
            self._mutant_value = description[len(mutation_value_prefix):]

    def open_test_case(self, test_case_id, name, index, *args, **kwargs):
        self._actual_test_case = TestCase(name)
        self._starting_time = datetime.now()

    def log_fail(self, description=""):
        self._failure = description
        self.was_there_any_failure = True

    def log_pass(self, description=""):
        pass

    def close_test_case(self):
        elapsed_time = datetime.now() - self._starting_time
        self._actual_test_case.elapsed_sec = elapsed_time.total_seconds()

        if self._error is not None:
            self._actual_test_case.add_error_info(message=self._error, output=self._generate_output_message())
            self._actual_test_case.classname = "Error"
        elif self._failure is not None:
            self._actual_test_case.add_failure_info(message=self._failure, output=self._generate_output_message())
            self._actual_test_case.classname = "Failure: " + self._failure
        else:
            self._actual_test_case.classname = "Success"
            response = get_response_object(self._received_string.encode()) if self._received_string else None
            if response:
                self._actual_test_case.classname += ": " + str(response.status)

        self._test_cases.append(copy.deepcopy(self._actual_test_case))

        self._actual_test_case = None
        self._error = None
        self._failure = None
        self._starting_time = None
        self._sent_string = None
        self._sent_bytes = None
        self._received_string = None
        self._received_bytes = None
        self._default_value = None
        self._mutant_value = None

    def close_test(self):
        test_suites = self._generate_test_suites()
        TestSuite.to_file(self._file_handle, test_suites, prettyprint=True)

    @staticmethod
    def _format_log_msg(msg_type, msg=None, data=None) -> str:
        # Encode the response data to default encoding
        if data and isinstance(data, str):
            data = data.encode()
        return helpers.format_log_msg(msg_type=msg_type, description=msg, data=data, indent_size=2, format_type='html')

    def _separate_test_suite_name(self, test_case_name) -> (str, str):
        split = test_case_name.split(self._test_suite_name_delimiter, 1)
        if len(split) == 2:
            return split[0], split[1]
        else:
            return None, split[0]

    def _generate_test_suites(self) -> List[TestSuite]:
        test_suites = {}
        for test_case in self._test_cases:
            if self._test_suite_name_delimiter is not None:
                group_name, test_name = self._separate_test_suite_name(test_case.name)
                if group_name is None:
                    test_suites = self._create_or_append_test(test_suites, test_case, self.DEFAULT_TEST_SUITE_NAME)
                else:
                    test_suites = self._create_or_append_test(test_suites, test_case, group_name)
            else:
                test_suites = self._create_or_append_test(test_suites, test_case, self.DEFAULT_TEST_SUITE_NAME)
        return list(test_suites.values())

    def _create_or_append_test(self, test_suites: Dict[str, TestSuite], test_case: TestCase, group_name: str)\
            -> Dict[str, TestSuite]:
        if group_name not in test_suites:
            test_suites[group_name] = TestSuite(group_name, test_cases=[test_case], hostname=self._hostname)
        else:
            test_suites[group_name].test_cases.append(test_case)
        return test_suites

    def _generate_output_message(self):
        message = ""

        if self._default_value is not None:
            message += "Default value: " + self._default_value + "\n"
        if self._mutant_value is not None:
            message += "Mutant value: " + self._mutant_value + "\n"
        message += "\n\n"

        message += "Sent string:\n"
        message += self._sent_string + "\n\n"
        message += "Sent bytes: \n"
        message += self._sent_bytes + "\n\n\n"

        if self._received_string:
            message += "Received string:\n"
            message += self._received_string + "\n\n"
            message += "Received bytes: \n"
            message += self._received_bytes
        else:
            message += "Nothing was received!"

        return message

    @staticmethod
    def _create_skipped_test_case(name, index):
        skipped_test_case = TestCase(name + "; Skip index" + str(index))
        skipped_test_case.classname = "Skipped"
        skipped_test_case.skipped_output = "Skipped test case"
        skipped_test_case.elapsed_sec = 0
        return skipped_test_case
