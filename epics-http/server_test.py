#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Shared class-level user storage
    users = {
        1: {"id": 1, "name": "Alice"},
        2: {"id": 2, "name": "Bob"}
    }

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == "/users":
            self._set_headers()
            # Return list of users (values of the dict)
            response = {"users": list(SimpleHTTPRequestHandler.users.values())}
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/users":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                user_id = data.get("id")
                name = data.get("name")
                if not user_id or not name:
                    raise ValueError("Missing 'id' or 'name'")

                # Add the new user to the class-level dictionary
                SimpleHTTPRequestHandler.users[user_id] = {"id": user_id, "name": name}

                self._set_headers(201)
                response = {
                    "message": "User added",
                    "users": list(SimpleHTTPRequestHandler.users.values())
                }
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except (json.JSONDecodeError, ValueError) as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting test HTTP server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
