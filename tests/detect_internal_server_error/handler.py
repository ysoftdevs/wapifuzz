from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(b'Internal server error')

    def send_error(self, code, message=None, explain=None):
        pass
