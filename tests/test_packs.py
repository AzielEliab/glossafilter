"""Bundled peer packs: equality, required keys, Haitian Creole honesty."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from glossafilter.intent import CanonicalPeerError
from glossafilter.packs import BUNDLED_PEER_IDS, list_peer_ids, load_packs, pack_from_dict

ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "glossafilter" / "packs"


def test_bundled_peer_ids() -> None:
    ids = list_peer_ids()
    for expected in ("en-plain", "en-formal", "es", "fr", "pt", "ht"):
        assert expected in ids
    assert ids == sorted(ids)
    assert set(BUNDLED_PEER_IDS) <= set(ids)


def test_no_canonical_flag_on_packs() -> None:
    for path in PACK_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert not data.get("canonical")
        assert not data.get("primary")
        assert not data.get("authoritative")
        assert "canonical" not in data
        assert "primary" not in data


def test_packs_have_required_keys() -> None:
    packs = load_packs()
    for peer_id, pack in packs.items():
        assert pack.peer_id == peer_id
        assert pack.label
        assert "proposition" in pack.templates
        assert "blurb" in pack.templates
        assert pack.glossary
        assert isinstance(pack.register_variants, dict)


def test_ht_pack_is_small_glossary() -> None:
    packs = load_packs()
    ht = packs["ht"]
    assert ht.peer_id == "ht"
    assert "Kreyòl" in ht.label or "Creole" in ht.label or "Ayisyen" in ht.label
    assert len(ht.glossary) <= 24
    assert "filter" in ht.glossary
    assert ht.glossary["filter"] == "filtè"


def test_load_rejects_canonical_pack() -> None:
    with pytest.raises(CanonicalPeerError):
        pack_from_dict(
            {
                "peer_id": "xx",
                "label": "Nope",
                "canonical": True,
                "templates": {"proposition": "{subject}."},
                "glossary": {},
                "register_variants": {},
            }
        )


def test_load_rejects_primary_pack() -> None:
    with pytest.raises(CanonicalPeerError):
        pack_from_dict(
            {
                "peer_id": "xx",
                "label": "Nope",
                "primary": True,
                "templates": {},
                "glossary": {},
                "register_variants": {},
            }
        )


def test_peer_labels_are_not_ranked() -> None:
    packs = load_packs()
    joined = " ".join(p.label.lower() for p in packs.values())
    assert "primary" not in joined
    assert "canonical" not in joined
    assert "original" not in joined
