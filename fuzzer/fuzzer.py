import sys
import ssl
from typing import List
from boofuzz import Session, Target, SocketConnection, s_get, pedrpc
from progress_reporter import report_progress
from configuration_manager import ConfigurationManager
from post_test_case_callback import PostTestCaseCallback
from blocks_generator import generate_http_fuzzed_blocks, generate_url_attributes_fuzzed_blocks, \
    generate_body_fuzzed_blocks


class Fuzzer:
    def __init__(self, endpoints, text_logger, junit_logger, protocol: str):
        self._endpoints = endpoints
        self._text_logger = text_logger
        self._junit_logger = junit_logger
        self._protocol = protocol
        self._session = None

        self._configure_session()

        self._remove_endpoints_by_keywords(ConfigurationManager.get_keywords_for_endpoints_skipping())

        if ConfigurationManager.is_http_fuzzing_allowed():
            self._generate_http_fuzzing()
        self._generate_uri_attributes_fuzzing()
        self._generate_request_body_fuzzing()
        self._generate_request_body_fuzzing(add_quotation_marks_into_non_string_primitives=True)

    def _configure_session(self):
        target_config = ConfigurationManager.get_target()
        startup_command = ConfigurationManager.get_startup_command()

        ssl_context = None
        if self._protocol == 'ssl':
            ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        recv_timeout = ConfigurationManager.get_receive_timeout()

        remote_connection = SocketConnection(
            target_config["hostname"],
            target_config["port"],
            proto=self._protocol,
            sslcontext=ssl_context,
            recv_timeout=recv_timeout
        )
        if startup_command:
            process_monitor = pedrpc.Client(target_config["hostname"], 26002)
            process_monitor_options = {"start_commands": [startup_command]}
            target = Target(connection=remote_connection, procmon=process_monitor, procmon_options=process_monitor_options)
        else:
            target = Target(connection=remote_connection)

        self._session = Session(
            target=target,
            fuzz_loggers=[self._text_logger, self._junit_logger],
            post_test_case_callbacks=[PostTestCaseCallback.post_test_callback],
            restart_sleep_time=0,
            keep_web_open=False,
            fuzz_db_keep_only_n_pass_cases=sys.maxsize,
            crash_threshold_element=10,
            crash_threshold_request=30)

    def _generate_http_fuzzing(self):
        self._session.connect(s_get(generate_http_fuzzed_blocks()))

    def _generate_uri_attributes_fuzzing(self):
        for endpoint in self._endpoints:
            for request in endpoint["Requests"]:
                request_name = generate_url_attributes_fuzzed_blocks(endpoint, request)
                self._session.connect(s_get(request_name))

    def _generate_request_body_fuzzing(self, add_quotation_marks_into_non_string_primitives=False):
        for endpoint in self._endpoints:
            for request in endpoint["Requests"]:
                request_name = generate_body_fuzzed_blocks(endpoint, request, add_quotation_marks_into_non_string_primitives)
                self._session.connect(s_get(request_name))

    def _remove_endpoints_by_keywords(self, keywords: List[str]):
        for keyword in keywords:
            self._endpoints[:] = [endpoint for endpoint in self._endpoints if keyword not in endpoint.get('Uri')]

    def fuzz(self):
        report_progress(self._session, self._junit_logger)
        self._session.fuzz()

    def was_there_any_failure(self):
        return self._junit_logger.was_there_any_failure
