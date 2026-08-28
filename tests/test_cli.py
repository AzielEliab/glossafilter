"""CLI: version, peers, render, JSON lineage."""

from __future__ import annotations

import json
from pathlib import Path

from glossafilter import __version__
from glossafilter.cli import main
from tests.helpers import TOOLING_DICT


def test_cli_version(capsys) -> None:
    assert main(["version"]) == 0
    assert capsys.readouterr().out.strip() == f"glossafilter {__version__}"
    assert __version__ == "0.1.0"


def test_cli_peers(capsys) -> None:
    assert main(["peers"]) == 0
    out = capsys.readouterr().out
    for pid in ("en-plain", "en-formal", "es", "fr", "pt", "ht"):
        assert pid in out
    assert "primary" not in out.lower()
    assert "canonical" not in out.lower()


def test_cli_render(capsys) -> None:
    code = main(
        [
            "render",
            "--subject",
            "package",
            "--rel",
            "release",
            "--object",
            "filter",
            "--channel",
            "tooling",
            "--peer",
            "en-plain",
            "--peer",
            "es",
        ]
    )
    out = capsys.readouterr().out
    assert code == 0
    assert "en-plain:" in out
    assert "es:" in out
    assert "digest:" in out
    assert "original" not in out.lower()


def test_cli_render_json(capsys) -> None:
    code = main(
        [
            "render",
            "--json",
            "--subject",
            "package",
            "--rel",
            "release",
            "--object",
            "filter",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    assert code == 0
    assert payload["digest"]
    assert payload["peers"]
    assert payload["audit"]
    assert "en-plain" in payload["peers"]
    assert "texts" in payload


def test_cli_render_json_file(capsys, tmp_path: Path) -> None:
    path = tmp_path / "intent.json"
    path.write_text(json.dumps(TOOLING_DICT), encoding="utf-8")
    code = main(["render", "--json", str(path)])
    payload = json.loads(capsys.readouterr().out)
    assert code == 0
    assert payload["digest"]
    assert "ht" in payload["peers"]


def test_cli_empty_nonzero(capsys) -> None:
    code = main(["render", "--subject", "", "--rel", "", "--object", ""])
    err = capsys.readouterr().err
    assert code == 1
    assert "empty" in err.lower() or "error" in err.lower()


def test_cli_identity_rejected(capsys, tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text(
        json.dumps(
            {
                "channel": "tooling",
                "propositions": [{"subject": "a", "rel": "b", "object": "c"}],
                "author": "nope",
            }
        ),
        encoding="utf-8",
    )
    code = main(["render", str(path)])
    err = capsys.readouterr().err
    assert code == 1
    assert "identity" in err.lower() or "author" in err.lower()


def test_cli_tooling_notes_rejected(capsys) -> None:
    code = main(
        [
            "render",
            "--subject",
            "package",
            "--rel",
            "release",
            "--object",
            "filter",
            "--channel",
            "tooling",
            "--note",
            "a civic aside",
        ]
    )
    err = capsys.readouterr().err
    assert code == 1
    assert "civic" in err.lower() or "tooling" in err.lower() or "notes" in err.lower()
