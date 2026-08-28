"""Local UI: loopback only, motto, peer stack, render API."""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request

import pytest

from glossafilter.ui import LOOPBACK, make_server
from tests.helpers import TOOLING_DICT


def test_ui_rejects_non_loopback() -> None:
    with pytest.raises(ValueError, match="loopback"):
        make_server("0.0.0.0", 9)
    assert "127.0.0.1" in LOOPBACK


def test_ui_get_root_200_contains_motto() -> None:
    httpd = make_server("127.0.0.1", 0)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=3) as resp:
            assert resp.status == 200
            html = resp.read().decode("utf-8")
        assert "Glossa Filter" in html
        assert "Human opinion remains human, and tools remain tools." in html
        assert "cdn" not in html.lower()
        assert "googleapis" not in html.lower()
        assert "None is primary" in html or "none is primary" in html.lower() or "none is canonical" in html.lower() or "No primary language" in html
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/style.css", timeout=3) as resp:
            css = resp.read().decode("utf-8")
        assert "PASS" in css or "--pass" in css or "peer-card" in css
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/peers", timeout=3) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        ids = [p["peer_id"] for p in payload["peers"]]
        assert "en-plain" in ids
        assert "ht" in ids
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/render",
            data=json.dumps(TOOLING_DICT).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        assert result["digest"]
        assert result["peers"]["es"]
        assert result["audit"]
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_ui_api_empty_intent_400() -> None:
    httpd = make_server("127.0.0.1", 0)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/render",
            data=json.dumps({"channel": "tooling", "propositions": []}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=3)
            raise AssertionError("expected HTTPError")
        except urllib.error.HTTPError as exc:
            assert exc.code == 400
            payload = json.loads(exc.read().decode("utf-8"))
            assert payload["type"] == "EmptyIntentError"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_ui_binds_loopback_address() -> None:
    httpd = make_server("127.0.0.1", 0)
    try:
        host, port = httpd.server_address[:2]
        assert host == "127.0.0.1"
        assert port > 0
    finally:
        httpd.server_close()
