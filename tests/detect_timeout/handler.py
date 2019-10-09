from http.server import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pass

    def send_error(self, code, message=None, explain=None):
        pass
