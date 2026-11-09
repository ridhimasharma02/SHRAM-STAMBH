"""Tiny local helper for recording audio.
Receives the list of spoken sentences from tools/collect.html and saves it to
tools/collected.json. Only listens on localhost. Run: python3 tools/collect_server.py"""
import json, os
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))

class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "http://localhost:8123")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        self.send_response(200); self._cors(); self.send_header("Content-Type", "text/plain"); self.end_headers()
        self.wfile.write(b"collector ready")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(n).decode("utf-8"))
        with open(os.path.join(HERE, "collected.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=0)
        self.send_response(200); self._cors(); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps({"saved": len(data)}).encode())

HTTPServer(("127.0.0.1", 8124), H).serve_forever()
