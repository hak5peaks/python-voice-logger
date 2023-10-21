from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys

sys.stderr = open(os.devnull, 'w')

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        recognized_text = data.get('text', 'Unknown')

        print(f"Recognized text: {recognized_text}")
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 8000
    server = HTTPServer((host, port), RequestHandler)
    print(f"Server listening on {host}:{port}")
    server.serve_forever()
