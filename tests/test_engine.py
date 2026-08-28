"""Engine: determinism, peer equality, audit, glossary, variants."""

from __future__ import annotations

import json

import pytest

from glossafilter.engine import GlossaFilter, pick_variant_index
from glossafilter.intent import CanonicalPeerError, Intent, UnknownPeerError
from tests.helpers import civic_intent, tooling_intent, triple_intent


def test_determinism_byte_identical() -> None:
    intent = tooling_intent()
    engine = GlossaFilter()
    a = engine.render(intent)
    b = engine.render(intent)
    assert a.digest == b.digest
    assert a.peers == b.peers
    assert json.dumps(a.to_dict(), sort_keys=True) == json.dumps(b.to_dict(), sort_keys=True)


def test_second_engine_same_bytes() -> None:
    intent = tooling_intent()
    a = GlossaFilter().render(intent)
    b = GlossaFilter().render(intent)
    for peer_id in a.peers:
        assert a.peers[peer_id].encode("utf-8") == b.peers[peer_id].encode("utf-8")


def test_peer_equality_no_primary_key() -> None:
    result = GlossaFilter().render(tooling_intent())
    assert "primary" not in result.peers
    assert "canonical" not in result.peers
    assert "original" not in result.peers
    payload = result.to_dict()
    assert "primary" not in payload
    assert set(payload["peers"]) == set(result.peers)


def test_all_peers_returned_by_default() -> None:
    result = GlossaFilter().render(tooling_intent())
    for pid in ("en-plain", "en-formal", "es", "fr", "pt", "ht"):
        assert pid in result.peers
        assert result.peers[pid].strip()


def test_audit_non_empty() -> None:
    result = GlossaFilter().render(tooling_intent())
    assert result.audit
    ids = [row["id"] for row in result.audit]
    assert any(i.startswith("pack:") for i in ids)
    assert any(i.startswith("template:") for i in ids)
    assert any("glossary:" in i or "register:" in i for i in ids)


def test_glossary_changes_surface() -> None:
    intent = triple_intent("package", "uses", "filter")
    result = GlossaFilter().render(intent, peers=["en-plain", "fr", "ht"])
    assert "filtre" in result.peers["fr"]
    assert "filtè" in result.peers["ht"]
    assert result.peers["fr"] != result.peers["en-plain"]
    lemmas = [row.get("lemma") for row in result.audit if row["kind"] == "glossary"]
    assert "filter" in lemmas


def test_register_variants_content_derived() -> None:
    intent = tooling_intent()
    a = GlossaFilter().render(intent, peers=["en-plain"])
    b = GlossaFilter().render(intent, peers=["en-plain"])
    assert a.peers["en-plain"] == b.peers["en-plain"]
    digest = intent.digest()
    n = 3
    assert pick_variant_index(digest, "en-plain", "release", n) == pick_variant_index(
        digest, "en-plain", "release", n
    )


def test_different_intents_may_pick_different_indices() -> None:
    d1 = triple_intent("package", "release", "filter").digest()
    d2 = triple_intent("package", "release", "tool").digest()
    assert d1 != d2
    # Indices *may* collide; the requirement is they are content-derived.
    # At least the digests differ so the pick input differs.
    i1 = pick_variant_index(d1, "en-plain", "release", 3)
    i2 = pick_variant_index(d2, "en-plain", "release", 3)
    assert i1 in (0, 1, 2)
    assert i2 in (0, 1, 2)


def test_subset_peers() -> None:
    result = GlossaFilter().render(tooling_intent(), peers=["es", "ht"])
    assert set(result.peers) == {"es", "ht"}
    assert list(result.to_dict()["peers"]) == ["es", "ht"]


def test_unknown_peer_rejected() -> None:
    with pytest.raises(UnknownPeerError):
        GlossaFilter().render(tooling_intent(), peers=["xx-nope"])


def test_canonical_peer_kwarg_rejected() -> None:
    with pytest.raises(CanonicalPeerError):
        GlossaFilter().render(tooling_intent(), canonical=True)


def test_primary_kwarg_rejected() -> None:
    with pytest.raises(CanonicalPeerError):
        GlossaFilter().render(tooling_intent(), primary=True)


def test_result_to_dict_sorted() -> None:
    payload = GlossaFilter().render(tooling_intent()).to_dict()
    assert list(payload.keys()) == sorted(payload.keys())
    assert list(payload["peers"].keys()) == sorted(payload["peers"].keys())
    assert payload["texts"] == payload["peers"]
    assert payload["digest"]


def test_civic_includes_notes_tooling_does_not() -> None:
    civic = GlossaFilter().render(civic_intent(), peers=["en-plain"])
    tooling = GlossaFilter().render(tooling_intent(), peers=["en-plain"])
    assert "Human opinion remains human" in civic.peers["en-plain"] or "stays" in civic.peers["en-plain"]
    assert "opinion" not in tooling.peers["en-plain"].lower() or "Human opinion" not in tooling.peers["en-plain"]


def test_tooling_render_mentions_behavior_surface() -> None:
    result = GlossaFilter().render(tooling_intent(), peers=["en-plain", "es"])
    assert "package" in result.peers["en-plain"] or "ships" in result.peers["en-plain"] or "puts out" in result.peers["en-plain"] or "sends out" in result.peers["en-plain"]
    assert "paquete" in result.peers["es"]


def test_en_plain_glossary_maps_release() -> None:
    intent = triple_intent("package", "release", "filter")
    # Force glossary path by using a lemma not only in variants? release is in variants.
    # Glossary for "filter" is the stable surface change; "package" maps to itself in en-plain.
    result = GlossaFilter().render(intent, peers=["en-plain", "en-formal"])
    assert result.peers["en-plain"] != result.peers["en-formal"]
