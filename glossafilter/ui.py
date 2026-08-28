"""Local Glossa Filter UI. Bind 127.0.0.1 only.

Form: channel select, proposition fields, optional extra propositions,
peer checkboxes (all selected by default, none labeled primary).
Vertical equal stack of peer outputs. JSON export of digest + audit + peers.
No CDN. No phone-home.

Motto: Human opinion remains human, and tools remain tools.

Ethical boundaries: no deception, no incitement, no identity masking
for wrongdoing, clear separation between civic speech and tooling.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from urllib.parse import urlparse

from glossafilter import __version__
from glossafilter.engine import GlossaFilter
from glossafilter.intent import GlossaError, Intent
from glossafilter.packs import load_packs

LOOPBACK = frozenset({"127.0.0.1", "localhost", "::1"})
WEB = files("glossafilter") / "web"
MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
}


def _web_bytes(name: str) -> bytes:
    return (WEB / name).read_bytes()


class Handler(BaseHTTPRequestHandler):
    server_version = f"GlossaFilter/{__version__}"

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, obj: object) -> None:
        body = json.dumps(obj, indent=2, ensure_ascii=False).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            self._send(200, _web_bytes("index.html"), MIME[".html"])
            return
        if path == "/style.css":
            self._send(200, _web_bytes("style.css"), MIME[".css"])
            return
        if path == "/app.js":
            self._send(200, _web_bytes("app.js"), MIME[".js"])
            return
        if path == "/api/peers":
            packs = load_packs()
            payload = {
                "peers": [packs[k].to_public() for k in sorted(packs)],
                "note": "All peers are equal. None is primary or canonical.",
            }
            self._json(200, payload)
            return
        if path == "/api/version":
            self._json(200, {"name": "glossafilter", "version": __version__})
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/api/render":
            self._json(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._json(400, {"error": "JSON body required"})
            return
        if not isinstance(payload, dict):
            self._json(400, {"error": "JSON object required"})
            return
        peers = payload.get("peers")
        if peers is not None and not isinstance(peers, list):
            self._json(400, {"error": "peers must be a list of peer ids"})
            return
        try:
            intent = Intent.from_dict(payload.get("intent") if isinstance(payload.get("intent"), dict) else payload)
            result = GlossaFilter().render(intent, peers=peers)
        except GlossaError as exc:
            self._json(400, {"error": str(exc), "type": type(exc).__name__})
            return
        self._json(200, result.to_dict())


def make_server(host: str = "127.0.0.1", port: int = 8792) -> ThreadingHTTPServer:
    if host not in LOOPBACK:
        raise ValueError("Glossa Filter UI binds loopback only (127.0.0.1)")
    return ThreadingHTTPServer((host, port), Handler)


def serve(host: str = "127.0.0.1", port: int = 8792) -> None:
    httpd = make_server(host, port)
    bound_host, bound_port = httpd.server_address[:2]
    print(
        f"Glossa Filter UI http://{bound_host}:{bound_port} "
        "(loopback only; mediation, not a translator)"
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
