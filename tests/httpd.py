import sys
import importlib
from http.server import HTTPServer
from pprint import pprint

handler_class = importlib.import_module(sys.argv[1][2:] + ".handler").RequestHandler

def run(server_class=HTTPServer, handler_class=handler_class, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
