"""This tree is Glossa Filter only. Not merged into sibling products."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "glossafilter"

FORBIDDEN_ROOTS = frozenset(
    {
        "forgereceipts",
        "zionpattern",
        "zion_pattern",
        "zion_pattern_solver",
        "decisiongate",
        "azos",
        "az_os",
        "veillock",
        "vibelock",
        "godlock",
        "codelock",
        "shadowlock",
        "temporallock",
        "staticclock",
        "miragegrid",
    }
)


def _root_of(name: str) -> str:
    return name.split(".")[0].lower().replace("-", "_")


def test_package_never_imports_siblings() -> None:
    import glossafilter  # noqa: F401
    import glossafilter.cli  # noqa: F401
    import glossafilter.engine  # noqa: F401
    import glossafilter.intent  # noqa: F401
    import glossafilter.packs  # noqa: F401
    import glossafilter.ui  # noqa: F401

    for name in list(sys.modules):
        assert _root_of(name) not in FORBIDDEN_ROOTS


def test_source_imports_isolated() -> None:
    for py in PKG.rglob("*.py"):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert _root_of(alias.name) not in FORBIDDEN_ROOTS
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert _root_of(node.module) not in FORBIDDEN_ROOTS


def test_not_inside_sibling_products() -> None:
    text = str(ROOT)
    assert text.endswith("glossafilter") or "/glossafilter" in text
    assert "forgereceipts" not in text
    assert "zion-pattern" not in text
    assert "decisiongate" not in text
    assert (PKG / "engine.py").is_file()
    assert not (ROOT / "forgereceipts").exists()
    assert not (ROOT / "decisiongate").exists()
    assert not (ROOT / "azos").exists()


def test_worker_kv_real_and_isolated() -> None:
    toml = (ROOT / "workers" / "download-tracker" / "wrangler.toml").read_text(encoding="utf-8")
    assert 'name = "glossafilter-download-tracker"' in toml
    assert "account_id = \"ac575a9b822bea2bed97d0ab73aed238\"" in toml
    assert 'binding = "DOWNLOADS"' in toml
    assert "GLOSSA_DOWNLOADS" not in toml
    assert "4dca63572f354a3c9c60b354d1acc330" in toml
    assert "REPLACE_ME" not in toml
    src = (ROOT / "workers" / "download-tracker" / "src" / "index.js").read_text(encoding="utf-8")
    assert 'const PROJECT = "glossafilter"' in src
    assert "glossafilter-0.1.0.tar.gz" in src
    assert "Human opinion remains human, and tools remain tools." in src
    assert "Isolated counter" in src
    assert "glossafilter-download-tracker" in src
    assert "env.ASSETS.fetch" in src
    lowered = src.lower().replace("-", "").replace("_", "").replace(" ", "")
    assert "forgereceipts" not in lowered
    assert "zionpattern" not in lowered
    assert "decisiongate" not in lowered
    assert "azos" not in lowered


def test_runtime_has_no_network_translator_imports() -> None:
    src = (PKG / "engine.py").read_text(encoding="utf-8")
    assert "urllib" not in src
    assert "requests" not in src
    assert "http.client" not in src
    assert "deepl" not in src.lower()
    assert "openai" not in src.lower()
