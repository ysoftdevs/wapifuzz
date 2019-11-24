from boofuzz import FuzzLoggerText, helpers
from fake_socket import get_response_object


class TextLogger(FuzzLoggerText):
    def __init__(self, full_log_file_pointer):
        super().__init__()
        self._log_file = full_log_file_pointer

    def open_test_step(self, description):
        self._print_log_msg(msg=description, msg_type='step')

    def log_check(self, description):
        self._print_log_msg(msg=description, msg_type='check')

    def log_error(self, description):
        self._print_log_msg(msg=description, msg_type='error')

    # Log full response just when it is needed
    def log_recv(self, data):
        response = get_response_object(data)
        if response is None or response.status >= 300:
            self._print_log_msg(data=data, msg_type='receive')
        else:
            message = "Returned status code " + str(response.status) + ", received message omitted."
            self._print_log_msg(msg=message, msg_type='info')

    def log_send(self, data):
        self._print_log_msg(data=data, msg_type='send')

    def log_info(self, description):
        pass

    def open_test_case(self, test_case_id, name, index, *args, **kwargs):
        self._print_log_msg(msg=test_case_id, msg_type='test_case')

    def log_fail(self, description=""):
        self._print_log_msg(msg=description, msg_type='fail')

    def log_pass(self, description=""):
        self._print_log_msg(msg=description, msg_type='pass')

    def close_test_case(self):
        print(file=self._log_file)

    def close_test(self):
        pass

    def _print_log_msg(self, msg_type, msg=None, data=None):
        print(
            helpers.format_log_msg(
                msg_type=msg_type, description=msg, data=data, indent_size=self.INDENT_SIZE, format_type="html"
            ), file=self._log_file
        )
