"""Intent validation: empty, identity, tooling-vs-civic, canonical JSON."""

from __future__ import annotations

import json

import pytest

from glossafilter.intent import (
    CanonicalPeerError,
    EmptyIntentError,
    IdentityFieldError,
    Intent,
    Proposition,
    ToolingPhilosophyError,
    UnknownChannelError,
)
from tests.helpers import CIVIC_DICT, TOOLING_DICT, tooling_intent


def test_empty_intent_rejected() -> None:
    with pytest.raises(EmptyIntentError):
        Intent.from_dict({})


def test_empty_mapping_none_rejected() -> None:
    with pytest.raises(EmptyIntentError):
        Intent.from_dict(None)


def test_blank_propositions_rejected() -> None:
    with pytest.raises(EmptyIntentError):
        Intent(
            propositions=(Proposition(subject="  ", rel="", object=""),),
            channel="tooling",
        )


def test_identity_author_rejected() -> None:
    with pytest.raises(IdentityFieldError):
        Intent.from_dict({**TOOLING_DICT, "author": "Aziel Eliab"})


def test_identity_github_rejected() -> None:
    with pytest.raises(IdentityFieldError):
        Intent.from_dict({**TOOLING_DICT, "github": "AzielEliab"})


def test_identity_real_name_rejected() -> None:
    with pytest.raises(IdentityFieldError):
        Intent.from_dict({**TOOLING_DICT, "real_name": "Aziel Eliab"})


def test_identity_in_slots_rejected() -> None:
    with pytest.raises(IdentityFieldError):
        Intent.from_dict(
            {
                **TOOLING_DICT,
                "slots": {"author": "someone", "action": "binds"},
            }
        )


def test_philosophy_on_tooling_rejected() -> None:
    with pytest.raises(ToolingPhilosophyError):
        Intent.from_dict({**TOOLING_DICT, "philosophy": "a stance"})


def test_ideology_on_tooling_rejected() -> None:
    with pytest.raises(ToolingPhilosophyError):
        Intent.from_dict({**TOOLING_DICT, "ideology": "a frame"})


def test_notes_on_tooling_rejected() -> None:
    with pytest.raises(ToolingPhilosophyError):
        Intent.from_dict({**TOOLING_DICT, "notes": "a civic aside"})


def test_civic_notes_allowed() -> None:
    intent = Intent.from_dict(CIVIC_DICT)
    assert intent.channel == "civic"
    assert "human" in intent.notes.lower()


def test_civic_philosophy_field_does_not_fail() -> None:
    intent = Intent.from_dict({**CIVIC_DICT, "philosophy": "ethical dual-channel"})
    assert intent.channel == "civic"
    assert intent.notes


def test_unknown_channel_rejected() -> None:
    with pytest.raises(UnknownChannelError):
        Intent(
            propositions=(Proposition("a", "b", "c"),),
            channel="secret",
        )


def test_canonical_flag_on_intent_rejected() -> None:
    with pytest.raises(CanonicalPeerError):
        Intent.from_dict({**TOOLING_DICT, "canonical": True})


def test_canonical_json_sorts_keys() -> None:
    intent = tooling_intent()
    dumped = intent.canonical_json()
    parsed = json.loads(dumped)
    assert list(parsed.keys()) == sorted(parsed.keys())
    assert list(parsed["propositions"][0].keys()) == sorted(
        parsed["propositions"][0].keys()
    )
    assert dumped == json.dumps(parsed, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def test_digest_stable() -> None:
    a = tooling_intent()
    b = tooling_intent()
    assert a.digest() == b.digest()
    assert len(a.digest()) == 64


def test_from_dict_top_level_triple() -> None:
    intent = Intent.from_dict(
        {"subject": "package", "rel": "release", "object": "filter", "channel": "tooling"}
    )
    assert len(intent.propositions) == 1
    assert intent.propositions[0].rel == "release"


def test_tooling_and_civic_digests_differ() -> None:
    t = Intent.from_dict(
        {"channel": "tooling", "propositions": [{"subject": "a", "rel": "b", "object": "c"}]}
    )
    c = Intent.from_dict(
        {"channel": "civic", "propositions": [{"subject": "a", "rel": "b", "object": "c"}]}
    )
    assert t.digest() != c.digest()
