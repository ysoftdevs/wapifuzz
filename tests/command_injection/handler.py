import os
import urllib.parse
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'plain/text')
        self.end_headers()

    def do_GET(self):
        self._get_path_parameters()
        self._set_headers()
        self.wfile.write(b'OK')
    
    def _get_path_parameters(self):
        path = urllib.parse.unquote(self.path)[len("/pets?attributeName="):]
        if path.startswith("sleep "):
            self._try_to_execute_command(path)
    
    def _try_to_execute_command(self, path):
        os.system(path)

    def send_error(self, code, message=None, explain=None):
        pass
