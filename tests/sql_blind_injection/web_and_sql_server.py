import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import time
import sqlite3
from sqlite3 import Error
 
 
def create_in_memory_connection():
    try:
        conn = sqlite3.connect(':memory:')
    except Error as e:
        print(e)
    return conn


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
        if path.startswith("sleep("):
            try:
                self.cursor.execute("SELECT " + path)
            except:
                pass
    
    def _try_to_execute_command(self, path):
        os.system(path)

    def send_error(self, code, message=None, explain=None):
        pass


def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    conn = create_in_memory_connection()

    # Define custom sleep function
    # On different DB engines it can be predefined
    conn.create_function("sleep", 1, time.sleep)

    RequestHandler.cursor = conn.cursor()

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
