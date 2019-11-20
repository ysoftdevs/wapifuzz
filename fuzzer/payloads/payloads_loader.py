import os
from fuzz_payloads import FuzzPayloads


class PayloadsLoader:
    def __init__(self, hostname):
        self.replacements = {"<<target_hostname>>": hostname}

    def load_payloads(self, file_path: str, directory_name: str, keep_newlines: bool = False):
        if file_path:
            try:
                with open(file_path, 'r', encoding="utf8") as custom_payloads_file_pointer:
                    for line in custom_payloads_file_pointer:

                        # Skip empty lines
                        if self._is_empty_or_comment(line):
                            continue

                        line = self._replace_target_hostname(line)
                        if not keep_newlines:
                            line = line.rstrip('\n').rstrip('\r\n')

                        FuzzPayloads.add_payload_to_list(line, directory_name)

            # If there is some problem with file, just continue with the rest of payloads
            except FileNotFoundError or IOError:
                print("WARNING: Error when opening file: " + file_path)

    def _replace_target_hostname(self, line: str):
        for pattern, replacement_value in self.replacements.items():
            line = line.replace(pattern, replacement_value)
        return line

    @staticmethod
    def _is_empty_or_comment(line):
        # Comment is every line which starts (without white spaces) with '#'
        if len(line.strip()) == 0 or line.startswith("#"):
            return True


def load_default_payloads(hostname: str):
    loader = PayloadsLoader(hostname)
    base_path = './fuzzer/payloads/lists/'
    for root, directories, files in os.walk(base_path):
        for file in files:
            if file.endswith('.txt'):
                directory_name = os.path.basename(os.path.normpath(root))
                loader.load_payloads(os.path.join(root, file), directory_name)
