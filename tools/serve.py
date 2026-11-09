"""Local web server for SHRAM STAMBH.

    python3 tools/serve.py          then open http://localhost:8123

Better than "python3 -m http.server" for this site because it:
  - tells the browser to re-check pages, scripts and styles every time, so you
    never see an old cached copy after a change;
  - lets the voice clips in audio/ be cached for good (their names change
    whenever their words change);
  - fixes addresses pasted with punctuation stuck on the end, such as
    "login.html," or "index.html."
Only listens on this computer (127.0.0.1)."""
import os
import socket
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, urlunsplit

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8123


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        parts = urlsplit(self.path)
        if parts.path == "/favicon.ico":
            self.send_response(301)
            self.send_header("Location", "/favicon.svg")
            self.end_headers()
            return
        clean = parts.path.rstrip(",.;:)!'\"")
        if clean != parts.path and clean:
            self.send_response(301)
            self.send_header("Location", urlunsplit(("", "", clean, parts.query, parts.fragment)))
            self.end_headers()
            return
        super().do_GET()

    def send_error(self, code, message=None, explain=None):
        page = os.path.join(ROOT, "404.html")
        if code == 404 and os.path.exists(page):
            body = open(page, "rb").read()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def end_headers(self):
        path = urlsplit(self.path).path
        if path.startswith("/audio/"):
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        else:
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))


class Server6(ThreadingHTTPServer):
    address_family = socket.AF_INET6


if __name__ == "__main__":
    # "localhost" can mean 127.0.0.1 or ::1 depending on the browser, so answer on both
    servers = [ThreadingHTTPServer(("127.0.0.1", PORT), Handler)]
    try:
        servers.append(Server6(("::1", PORT), Handler))
    except OSError:
        pass
    for srv in servers[1:]:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"SHRAM STAMBH is running at http://localhost:{PORT}  (press Ctrl-C to stop)")
    try:
        servers[0].serve_forever()
    except KeyboardInterrupt:
        print("stopped")
