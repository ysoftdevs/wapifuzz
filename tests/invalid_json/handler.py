from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(b'invalid json')
    
    def send_error(self, code, message=None, explain=None):
        pass
