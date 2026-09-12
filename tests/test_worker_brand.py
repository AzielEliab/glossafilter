"""Worker homepage rose-star brand mark (Aziel Eliab only).

Public HTML uses /sigil.png with empty alt and no words on the mark.
Do not put “everblooming sigil” on the mark. FragGate / Remain-OFF untouched.
Verify contracts that require Everblooming header/skill strings stay unchanged.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "workers" / "download-tracker" / "src" / "index.js").read_text(
    encoding="utf-8"
)
RUNTIME = (ROOT / "workers" / "download-tracker" / "src" / "runtime.js").read_text(
    encoding="utf-8"
)
MESH = (ROOT / "workers" / "download-tracker" / "src" / "mesh.js").read_text(
    encoding="utf-8"
)
WRANGLER = (ROOT / "workers" / "download-tracker" / "wrangler.toml").read_text(
    encoding="utf-8"
)
PUBLIC_SIGIL = ROOT / "workers" / "download-tracker" / "public" / "sigil.png"

# Official Aziel rose-star (196×139, ~75KB). Not the 40×40 placeholder.
ROSE_STAR_SHA256 = "af095e8b0916a7262860a53619c7110f25539988806775b1c7bff8df7b0ee848"
BRAND_ROW = (
    '<div class="brandrow"><img class="brandmark" src="/sigil.png" '
    'width="40" height="40" alt="" decoding="async"></div>'
)


def _home_html() -> str:
    start = INDEX.index("<!doctype html>")
    end = INDEX.rindex("</html>") + 7
    return INDEX[start:end]


def _ai_html() -> str:
    start = RUNTIME.index("<!doctype html>")
    end = RUNTIME.rindex("</html>") + 7
    return RUNTIME[start:end]


def test_homepage_has_rose_star_brandrow() -> None:
    home = _home_html()
    assert BRAND_ROW in home
    assert 'class="brandrow"' in home
    assert 'class="brandmark"' in home
    assert 'src="/sigil.png"' in home
    assert 'alt=""' in home
    assert ".brandrow" in home
    assert ".brandmark" in home
    assert "Aziel Eliab" in home


def test_ai_page_has_rose_star_brandrow() -> None:
    ai = _ai_html()
    assert BRAND_ROW in ai
    assert 'alt=""' in ai
    assert "Aziel Eliab" in ai


def test_public_html_does_not_name_everblooming_on_the_mark() -> None:
    home = _home_html()
    ai = _ai_html()
    brand_start = INDEX.find('<div class="brandrow">')
    brand = INDEX[brand_start : brand_start + 180]
    assert "everblooming" not in brand.lower()
    assert "everblooming sigil" not in home.lower()
    assert "everblooming sigil" not in ai.lower()
    assert "Everblooming sigil" not in INDEX
    assert "Everblooming sigil" not in RUNTIME
    assert 'alt="everblooming sigil"' not in INDEX.lower()
    assert 'alt="Everblooming' not in INDEX
    assert 'alt="Everblooming' not in RUNTIME
    assert 'title="Home — everblooming sigil"' not in INDEX
    assert "Everblooming sigil ·" not in INDEX
    assert "Everblooming sigil ·" not in RUNTIME


def test_hosted_sigil_is_official_rose_star_png() -> None:
    assert PUBLIC_SIGIL.is_file()
    data = PUBLIC_SIGIL.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(data) > 70_000
    assert hashlib.sha256(data).hexdigest() == ROSE_STAR_SHA256
    assert "/sigil.png" not in WRANGLER  # assets serve the file; worker-first list stays unchanged


def test_fraggate_remain_off_and_mesh_proxy_untouched() -> None:
    assert "FragGate slug=mesh" in INDEX
    assert "handleMeshApi(request, url, env)" in INDEX
    assert "MESH_DEFAULT_OFF = true" in MESH
    assert "Remain-OFF" not in INDEX
    assert "Remain-OFF" not in MESH
    assert "Remain-OFF" not in RUNTIME
