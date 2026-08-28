"""Shared fixtures for Glossa Filter tests."""

from __future__ import annotations

from glossafilter.intent import Intent, Proposition

TOOLING_TRIPLE = ("package", "release", "filter")

TOOLING_DICT = {
    "channel": "tooling",
    "propositions": [
        {"subject": "package", "rel": "release", "object": "filter"},
    ],
    "slots": {
        "action": "binds",
        "interface": "loopback",
    },
}

CIVIC_DICT = {
    "channel": "civic",
    "propositions": [
        {"subject": "speech", "rel": "remains", "object": "human"},
    ],
    "notes": "Human opinion remains human, and tools remain tools.",
}


def tooling_intent() -> Intent:
    return Intent.from_dict(TOOLING_DICT)


def civic_intent() -> Intent:
    return Intent.from_dict(CIVIC_DICT)


def triple_intent(subject: str, rel: str, obj: str, channel: str = "tooling") -> Intent:
    return Intent(
        propositions=(Proposition(subject=subject, rel=rel, object=obj),),
        channel=channel,
    )
