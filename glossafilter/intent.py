"""Intent: structured record, not English-as-source.

Ethical boundaries (whitepaper §7):
- No deception: content remains accurate.
- No incitement: outputs are non-mobilizing.
- No identity masking for wrongdoing.
- Clear separation between civic speech and tooling.

channel=tooling renders may only talk about behavior and interface,
never philosophy/identity/ideology. Mixing philosophy into tooling is a
failure, not a render. channel=civic may carry ethical/philosophical
intent. notes are civic-only.

Identity fields (author, github, real name) on an Intent are rejected.
Authorship is not stamped onto renders. This is mediation, not secrecy.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

CHANNELS = frozenset({"tooling", "civic"})
SLOT_KEYS = ("who", "what", "when", "action", "constraint", "interface")

IDENTITY_FIELDS = frozenset(
    {
        "author",
        "github",
        "real_name",
        "realname",
        "real-name",
        "identity",
        "full_name",
        "fullname",
        "twitter",
        "email",
    }
)
PHILOSOPHY_FIELDS = frozenset(
    {
        "philosophy",
        "ideology",
        "belief",
        "doctrine",
        "creed",
        "worldview",
        "partisan",
    }
)
CANONICAL_FIELDS = frozenset({"canonical", "primary", "authoritative"})


class GlossaError(ValueError):
    """Base error. Failures are explicit; they are not renders."""


class EmptyIntentError(GlossaError):
    """Empty intent is a failure, not a render."""


class IdentityFieldError(GlossaError):
    """Identity fields on Intent are rejected. Authorship is not stamped onto renders."""


class ToolingPhilosophyError(GlossaError):
    """Philosophy/ideology on channel=tooling is a failure, not a render."""


class CanonicalPeerError(GlossaError):
    """Treating one peer as authoritative is a failure. All outputs are peers."""


class UnknownPeerError(GlossaError):
    """Requested peer id is not a bundled pack."""


class UnknownChannelError(GlossaError):
    """channel must be tooling or civic."""


def _norm_key(key: object) -> str:
    return str(key).strip().lower().replace("-", "_")


def reject_forbidden_keys(data: Mapping[str, Any], *, channel: str) -> None:
    """Reject identity always; reject philosophy on tooling; reject canonical flags."""
    for key, value in data.items():
        nk = _norm_key(key)
        if nk in IDENTITY_FIELDS:
            raise IdentityFieldError(
                f"identity field {key!r} is not allowed on Intent; "
                "authorship is not stamped onto renders"
            )
        if nk in CANONICAL_FIELDS and value:
            raise CanonicalPeerError(
                "one language treated as authoritative; all outputs are peers"
            )
        if nk in PHILOSOPHY_FIELDS and channel == "tooling":
            raise ToolingPhilosophyError(
                "philosophy/ideology fields on channel=tooling are a failure, not a render"
            )


@dataclass(frozen=True)
class Proposition:
    """One {subject, rel, object} triple. Plain strings. No canonical phrasing."""

    subject: str
    rel: str
    object: str

    def to_dict(self) -> dict[str, str]:
        return {
            "object": self.object.strip(),
            "rel": self.rel.strip(),
            "subject": self.subject.strip(),
        }

    def is_blank(self) -> bool:
        return not (self.subject.strip() or self.rel.strip() or self.object.strip())

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Proposition":
        return cls(
            subject=str(data.get("subject") or ""),
            rel=str(data.get("rel") or ""),
            object=str(data.get("object") or ""),
        )


@dataclass(frozen=True)
class Intent:
    """Structured intent. English is not the source language; this record is."""

    propositions: tuple[Proposition, ...]
    slots: dict[str, str] = field(default_factory=dict)
    channel: str = "tooling"
    notes: str = ""

    def __post_init__(self) -> None:
        channel = (self.channel or "tooling").strip().lower()
        object.__setattr__(self, "channel", channel)
        object.__setattr__(self, "notes", (self.notes or "").strip())
        props: tuple[Proposition, ...]
        if isinstance(self.propositions, Proposition):
            props = (self.propositions,)
        else:
            props = tuple(self.propositions)
        object.__setattr__(self, "propositions", props)
        cleaned: dict[str, str] = {}
        for key, value in dict(self.slots or {}).items():
            nk = _norm_key(key)
            text = str(value).strip()
            if not text:
                continue
            cleaned[nk] = text
        object.__setattr__(self, "slots", cleaned)
        self.validate()

    def validate(self) -> None:
        if self.channel not in CHANNELS:
            raise UnknownChannelError(
                f"channel must be 'tooling' or 'civic', not {self.channel!r}"
            )
        if not self.propositions or all(p.is_blank() for p in self.propositions):
            raise EmptyIntentError("empty intent is a failure, not a render")
        if self.channel == "tooling" and self.notes:
            raise ToolingPhilosophyError(
                "notes are civic-only; mixing philosophy into tooling is a failure, not a render"
            )
        reject_forbidden_keys(self.slots, channel=self.channel)

    def canonical_dict(self) -> dict[str, Any]:
        """Stable dict. Keys sorted at dump time. No author fields."""
        return {
            "channel": self.channel,
            "notes": self.notes if self.channel == "civic" else "",
            "propositions": [p.to_dict() for p in self.propositions],
            "slots": {k: self.slots[k] for k in sorted(self.slots)},
        }

    def canonical_json(self) -> str:
        """Byte-stable JSON of this Intent. Sort keys. Separators compact."""
        return json.dumps(
            self.canonical_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    def digest(self) -> str:
        """SHA-256 of canonical intent JSON. Content-derived, never author-derived."""
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> "Intent":
        if not data or not isinstance(data, Mapping):
            raise EmptyIntentError("empty intent is a failure, not a render")
        channel = str(data.get("channel") or "tooling").strip().lower()
        reject_forbidden_keys(data, channel=channel)
        slots_raw = data.get("slots") or {}
        if slots_raw and not isinstance(slots_raw, Mapping):
            raise EmptyIntentError("slots must be a mapping")
        if isinstance(slots_raw, Mapping):
            reject_forbidden_keys(slots_raw, channel=channel)
        raw_props = data.get("propositions")
        propositions: list[Proposition] = []
        if isinstance(raw_props, Sequence) and not isinstance(raw_props, (str, bytes)):
            for item in raw_props:
                if isinstance(item, Mapping):
                    propositions.append(Proposition.from_mapping(item))
                elif isinstance(item, Proposition):
                    propositions.append(item)
        if not propositions and (
            data.get("subject") or data.get("rel") or data.get("object")
        ):
            propositions.append(
                Proposition(
                    subject=str(data.get("subject") or ""),
                    rel=str(data.get("rel") or ""),
                    object=str(data.get("object") or ""),
                )
            )
        notes = str(data.get("notes") or "")
        slots = dict(slots_raw) if isinstance(slots_raw, Mapping) else {}
        for key in SLOT_KEYS:
            if key in data and data[key] not in (None, ""):
                slots.setdefault(key, str(data[key]))
        return cls(
            propositions=tuple(propositions),
            slots=slots,
            channel=channel,
            notes=notes,
        )

    @classmethod
    def from_triples(
        cls,
        triples: Iterable[tuple[str, str, str]],
        *,
        channel: str = "tooling",
        slots: Mapping[str, str] | None = None,
        notes: str = "",
    ) -> "Intent":
        props = tuple(Proposition(subject=s, rel=r, object=o) for s, r, o in triples)
        return cls(propositions=props, slots=dict(slots or {}), channel=channel, notes=notes)
