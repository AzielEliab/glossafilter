"""GlossaFilter engine: deterministic peer renders.

Identical Intent + identical peer set + identical packs → byte-identical
outputs. Sort keys. No random unless seeded from a SHA-256 of the
canonical intent JSON. That hash is used only to pick among
register_variants so the same intent always picks the same synonym;
different intents can differ.

This is **anti-fingerprint variance that is content-derived, never
author-derived**. Authorship is not stamped onto the renders.

Audit: every render returns the list of rule/template/glossary ids applied.
Inspectable. Meaning stays verifiable.

API returns a map of peer_id → text, never a single "the" translation.

Ethical boundaries (whitepaper §7):
- No deception: content remains accurate.
- No incitement: outputs are non-mobilizing.
- No identity masking for wrongdoing.
- Clear separation between civic speech and tooling.

Not concealment. Not a live translator. No network calls at runtime.
Not ForgeReceipts / ZionPattern Solver / DecisionGATE / AZ-OS.
"""

from __future__ import annotations

import hashlib
import string
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from glossafilter.intent import (
    CanonicalPeerError,
    Intent,
    UnknownPeerError,
)
from glossafilter.packs import Pack, load_packs


class _SafeMap(dict):
    def __missing__(self, key: str) -> str:
        return ""


def pick_variant_index(digest: str, peer_id: str, lemma: str, n: int) -> int:
    """Content-derived pick. Never author-derived.

    Mixes the intent digest with peer_id and lemma so the same intent
    always yields the same synonym per peer, while different intents
    can differ. Not a fingerprint of the author.
    """
    if n <= 0:
        return 0
    material = f"{digest}|{peer_id}|{lemma}".encode("utf-8")
    hashed = hashlib.sha256(material).digest()
    return int.from_bytes(hashed[:8], "big") % n


def _split_punct(token: str) -> tuple[str, str, str]:
    """Return (leading_punct, core, trailing_punct)."""
    start = 0
    end = len(token)
    while start < end and token[start] in string.punctuation:
        start += 1
    while end > start and token[end - 1] in string.punctuation:
        end -= 1
    return token[:start], token[start:end], token[end:]


def _match_case(original: str, surface: str) -> str:
    if not original or not surface:
        return surface
    if original.isupper() and len(original) > 1:
        return surface.upper()
    if original[0].isupper():
        return surface[0].upper() + surface[1:]
    return surface


@dataclass
class Result:
    """Parallel expression. peers is a map, never a single translation."""

    peers: dict[str, str]
    audit: list[dict[str, Any]]
    digest: str

    def to_dict(self) -> dict[str, Any]:
        ordered = {k: self.peers[k] for k in sorted(self.peers)}
        return {
            "audit": list(self.audit),
            "digest": self.digest,
            "peers": ordered,
            "texts": ordered,
        }


def _audit(
    audit_id: str,
    kind: str,
    peer: str,
    **extra: Any,
) -> dict[str, Any]:
    row: dict[str, Any] = {"id": audit_id, "kind": kind, "peer": peer}
    for key in sorted(extra):
        row[key] = extra[key]
    return row


class GlossaFilter:
    """Deterministic linguistic mediation layer."""

    def __init__(self, packs: Mapping[str, Pack] | None = None) -> None:
        self.packs: dict[str, Pack] = dict(packs) if packs is not None else load_packs()
        for pack in self.packs.values():
            # Belt-and-braces: a pack object should never carry a canonical flag.
            if getattr(pack, "canonical", False) or getattr(pack, "primary", False):
                raise CanonicalPeerError(
                    "one language treated as authoritative; all outputs are peers"
                )

    def render(
        self,
        intent: Intent,
        peers: Sequence[str] | None = None,
        *,
        canonical: Any = None,
        primary: Any = None,
        authoritative: Any = None,
        canonical_peer: Any = None,
    ) -> Result:
        """Render intent across peers. Returns a map, never one translation.

        Rejects any attempt to treat one peer as authoritative.
        """
        if canonical or primary or authoritative or canonical_peer:
            raise CanonicalPeerError(
                "one language treated as authoritative; all outputs are peers"
            )
        intent.validate()
        digest = intent.digest()
        if peers is None:
            selected = sorted(self.packs.keys())
        else:
            selected = list(peers)
            unknown = [p for p in selected if p not in self.packs]
            if unknown:
                raise UnknownPeerError(
                    f"unknown peer(s) {unknown!r}; bundled: {sorted(self.packs)}"
                )
            # Stable output order even if the caller passed an unsorted list.
            selected = sorted(dict.fromkeys(selected))
        texts: dict[str, str] = {}
        audit: list[dict[str, Any]] = []
        for peer_id in selected:
            pack = self.packs[peer_id]
            text, entries = self._render_peer(intent, pack, digest)
            texts[peer_id] = text
            audit.extend(entries)
        return Result(peers=texts, audit=audit, digest=digest)

    def _surface(
        self,
        text: str,
        pack: Pack,
        digest: str,
        audit: list[dict[str, Any]],
    ) -> str:
        if not text:
            return ""
        out: list[str] = []
        for token in text.split():
            lead, core, trail = _split_punct(token)
            lemma = core.lower()
            if not lemma:
                out.append(token)
                continue
            if lemma in pack.register_variants:
                variants = pack.register_variants[lemma]
                idx = pick_variant_index(digest, pack.peer_id, lemma, len(variants))
                surface = _match_case(core, variants[idx])
                audit.append(
                    _audit(
                        f"register:{pack.peer_id}:{lemma}",
                        "register_variant",
                        pack.peer_id,
                        lemma=lemma,
                        surface=surface,
                    )
                )
                out.append(f"{lead}{surface}{trail}")
            elif lemma in pack.glossary:
                surface = _match_case(core, pack.glossary[lemma])
                audit.append(
                    _audit(
                        f"glossary:{pack.peer_id}:{lemma}",
                        "glossary",
                        pack.peer_id,
                        lemma=lemma,
                        surface=surface,
                    )
                )
                out.append(f"{lead}{surface}{trail}")
            else:
                out.append(token)
        return " ".join(out)

    def _render_peer(
        self,
        intent: Intent,
        pack: Pack,
        digest: str,
    ) -> tuple[str, list[dict[str, Any]]]:
        audit: list[dict[str, Any]] = [
            _audit(f"pack:{pack.peer_id}", "pack", pack.peer_id, label=pack.label)
        ]
        lines: list[str] = []
        prop_tmpl = pack.templates.get("proposition", "{subject} {rel} {object}.")
        for prop in intent.propositions:
            subject = self._surface(prop.subject, pack, digest, audit)
            rel = self._surface(prop.rel, pack, digest, audit)
            obj = self._surface(prop.object, pack, digest, audit)
            audit.append(
                _audit(
                    f"template:{pack.peer_id}:proposition",
                    "template",
                    pack.peer_id,
                    template="proposition",
                )
            )
            mapping = _SafeMap(subject=subject, rel=rel, object=obj, **{
                k: self._surface(v, pack, digest, audit) for k, v in intent.slots.items()
            })
            lines.append(prop_tmpl.format_map(mapping).strip())
        if intent.slots:
            blurb_tmpl = pack.templates.get("blurb", "")
            if blurb_tmpl:
                surfaced_slots = {
                    k: self._surface(v, pack, digest, audit) for k, v in intent.slots.items()
                }
                audit.append(
                    _audit(
                        f"template:{pack.peer_id}:blurb",
                        "template",
                        pack.peer_id,
                        template="blurb",
                    )
                )
                mapping = _SafeMap(**surfaced_slots)
                blurb = blurb_tmpl.format_map(mapping).strip()
                if blurb:
                    lines.append(blurb)
        if intent.channel == "civic" and intent.notes:
            # Civic-only. Notes are mapped through the same glossary; never an author stamp.
            note_line = self._surface(intent.notes, pack, digest, audit)
            if note_line:
                lines.append(note_line)
        text = "\n".join(line for line in lines if line)
        return text, audit
