"""Load bundled peer packs. All peers are equal. None is primary.

Each pack is JSON under glossafilter/packs/:
  peer_id, label, templates (proposition + blurb), glossary (lemma → surface),
  register_variants (synonym lists).

canonical=true / primary=true / authoritative=true is a failure, not a load.

This is glossary+templates, not a live translator. The Haitian Creole pack
is small and honest. No network. No LLM.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import files
from typing import Any, Mapping

from glossafilter.intent import CanonicalPeerError, UnknownPeerError

PACK_ROOT = files("glossafilter") / "packs"

# Bundled peer ids, all equal. Sort order is the only order.
BUNDLED_PEER_IDS = ("en-formal", "en-plain", "es", "fr", "ht", "pt")


@dataclass(frozen=True)
class Pack:
    """One linguistic peer. Not a canonical phrasing."""

    peer_id: str
    label: str
    templates: dict[str, str]
    glossary: dict[str, str]
    register_variants: dict[str, tuple[str, ...]]

    def to_public(self) -> dict[str, str]:
        return {"peer_id": self.peer_id, "label": self.label}


def pack_from_dict(data: Mapping[str, Any]) -> Pack:
    """Build a Pack. Reject any attempt to mark one peer authoritative."""
    if not isinstance(data, Mapping):
        raise CanonicalPeerError("pack must be a mapping")
    for flag in ("canonical", "primary", "authoritative"):
        if data.get(flag):
            raise CanonicalPeerError(
                "one language treated as authoritative; all outputs are peers"
            )
    peer_id = str(data.get("peer_id") or "").strip()
    if not peer_id:
        raise CanonicalPeerError("pack missing peer_id")
    label = str(data.get("label") or peer_id).strip()
    templates_raw = data.get("templates") or {}
    glossary_raw = data.get("glossary") or {}
    variants_raw = data.get("register_variants") or {}
    templates = {
        str(k): str(v)
        for k, v in dict(templates_raw).items()
        if str(v).strip()
    }
    glossary = {
        str(k).strip().lower(): str(v)
        for k, v in dict(glossary_raw).items()
        if str(k).strip() and str(v).strip()
    }
    variants: dict[str, tuple[str, ...]] = {}
    for key, values in dict(variants_raw).items():
        lemma = str(key).strip().lower()
        if not lemma:
            continue
        if isinstance(values, (list, tuple)):
            items = tuple(str(x) for x in values if str(x).strip())
        else:
            items = (str(values),) if str(values).strip() else ()
        if items:
            variants[lemma] = items
    if "proposition" not in templates:
        templates["proposition"] = "{subject} {rel} {object}."
    if "blurb" not in templates:
        templates["blurb"] = "{action} {interface}."
    return Pack(
        peer_id=peer_id,
        label=label,
        templates=templates,
        glossary=glossary,
        register_variants=variants,
    )


def load_packs() -> dict[str, Pack]:
    """Load every bundled JSON pack. Sorted keys. None marked primary."""
    packs: dict[str, Pack] = {}
    json_files = []
    for item in PACK_ROOT.iterdir():
        name = getattr(item, "name", str(item))
        if name.endswith(".json"):
            json_files.append(item)
    json_files.sort(key=lambda t: getattr(t, "name", str(t)))
    for item in json_files:
        raw = json.loads(item.read_text(encoding="utf-8"))
        pack = pack_from_dict(raw)
        packs[pack.peer_id] = pack
    if not packs:
        raise UnknownPeerError("no bundled peer packs found")
    return packs


def list_peer_ids(packs: Mapping[str, Pack] | None = None) -> list[str]:
    """Sorted peer ids. Equal peers, no primary."""
    source = packs if packs is not None else load_packs()
    return sorted(source.keys())


def get_pack(peer_id: str, packs: Mapping[str, Pack] | None = None) -> Pack:
    source = packs if packs is not None else load_packs()
    if peer_id not in source:
        raise UnknownPeerError(f"unknown peer {peer_id!r}; bundled: {sorted(source)}")
    return source[peer_id]
