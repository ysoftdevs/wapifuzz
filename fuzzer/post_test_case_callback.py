import json
from http.client import HTTPResponse
from boofuzz import exception
from fake_socket import get_response_object


class PostTestCaseCallback(object):
    timeout_message = "Timeout or closed connection"

    @staticmethod
    def post_test_callback(target, fuzz_data_logger, session, sock, *args, **kwargs):
        fuzz_data_logger.log_info("Mutation: " + session.fuzz_node.mutant._rendered.decode('utf-8', errors='ignore'))
        fuzz_data_logger.log_info("Original value: " + session.fuzz_node.mutant.original_value.decode('utf-8', errors='ignore'))

        try:
            response_string = target.recv()
        except exception.BoofuzzTargetConnectionReset:
            fuzz_data_logger.log_fail(PostTestCaseCallback.timeout_message)
            return

        if not response_string:
            fuzz_data_logger.log_fail(PostTestCaseCallback.timeout_message)
            return

        response = get_response_object(response_string)

        if get_response_object(response_string) is None:
            fuzz_data_logger.log_fail("Bad HTTP header")
            return

        PostTestCaseCallback._http_response_asserts(response, fuzz_data_logger)

    @staticmethod
    def _http_response_asserts(response: HTTPResponse, fuzz_data_logger):
        if response.status >= 500:
            fuzz_data_logger.log_fail("Status code higher or equal than 500!")

        if response.getheader("Content-Type") == "application/json":
            try:
                json.loads(response.read())
            except ValueError:
                fuzz_data_logger.log_fail("application/json body is not valid JSON structure")
