"""Glossa Filter: a deterministic linguistic mediation layer.

Aziel Eliab, 2026. Apache-2.0.

Same functional or ethical intent is rendered into multiple languages
and dialects as **peers** (no primary/canonical phrasing). Language is
treated as a routing surface ("linguistic static IP"): a stable,
repeatable mapping that preserves semantic intent while varying surface
expression. Transform rules are inspectable. Meaning stays verifiable.
Authorship is not stamped onto the renders.

This product is NOT concealment, steganography, identity masking, or a
tool for hiding wrongdoing. It is NOT a live translator (no Google /
DeepL / LLM API, no network calls at runtime). It is NOT a philosophy
engine. It is NOT ForgeReceipts, ZionPattern Solver, DecisionGATE,
AZ-OS, or any *Lock product.

Ethical boundaries (whitepaper §7) — must remain accurate in code:
- No deception: content remains accurate.
- No incitement: outputs are non-mobilizing.
- No identity masking for wrongdoing.
- Clear separation between civic speech and tooling.

Motto: Human opinion remains human, and tools remain tools.

Forks are welcome and always allowed.
"""

from __future__ import annotations

from glossafilter.engine import GlossaFilter, Result
from glossafilter.intent import (
    CanonicalPeerError,
    EmptyIntentError,
    GlossaError,
    IdentityFieldError,
    Intent,
    Proposition,
    ToolingPhilosophyError,
    UnknownChannelError,
    UnknownPeerError,
)

__version__ = "0.1.0"
__author__ = "Aziel Eliab"
__all__ = [
    "CanonicalPeerError",
    "EmptyIntentError",
    "GlossaError",
    "GlossaFilter",
    "IdentityFieldError",
    "Intent",
    "Proposition",
    "Result",
    "ToolingPhilosophyError",
    "UnknownChannelError",
    "UnknownPeerError",
    "__version__",
]
