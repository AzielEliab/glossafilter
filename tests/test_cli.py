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
    assert "Next:" in err
    assert "glossafilter render --subject" in err


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


def test_help_lists_ui_and_version() -> None:
    from glossafilter.cli import _build_parser

    text = _build_parser().format_help()
    assert "ui" in text
    assert "version" in text
    assert "127.0.0.1:8792" in text or "glossafilter ui" in text
    assert "examples:" in text
    assert "advanced:" in text
    assert "changelog" not in text.lower()
    assert "the following arguments are required" not in text


def test_bare_command_welcomes(capsys) -> None:
    assert main([]) == 0
    out = capsys.readouterr().out
    err = capsys.readouterr().err
    assert "glossafilter ui" in out
    assert "http://127.0.0.1:8792/" in out
    assert "Aziel Eliab" in out
    assert "glossafilter --help" in out
    assert err == ""
    assert "required: cmd" not in out


def test_unknown_command_has_next_step(capsys) -> None:
    code = main(["bogus"])
    err = capsys.readouterr().err
    assert code == 2
    assert 'Unknown command "bogus"' in err
    assert "glossafilter --help" in err
    assert "Traceback" not in err


def test_import_human_and_json(capsys, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "in.json"
    src.write_text(json.dumps({"hello": 1}), encoding="utf-8")
    assert main(["import", str(src)]) == 0
    out = capsys.readouterr().out
    assert "Imported" in out
    assert not out.lstrip().startswith("{")
    assert main(["import", "--json", str(src)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert "hello" in payload["keys"]
    dest = tmp_path / "out.json"
    assert main(["export", str(dest)]) == 0
    human = capsys.readouterr().out
    assert "Exported" in human
    assert dest.is_file()
    assert main(["export", "--json", str(dest)]) == 0
    exported = json.loads(capsys.readouterr().out)
    assert exported["ok"] is True
    assert exported["author"] == "Aziel Eliab"
