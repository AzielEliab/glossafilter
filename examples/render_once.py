#!/usr/bin/env python3
"""Render one tooling Intent across all bundled peers.

Behavior and interface only. Not a translator. Not concealment.
"""

from __future__ import annotations

from glossafilter import GlossaFilter, Intent


def main() -> None:
    intent = Intent.from_dict(
        {
            "channel": "tooling",
            "propositions": [
                {"subject": "package", "rel": "release", "object": "filter"},
            ],
            "slots": {"action": "binds", "interface": "loopback"},
        }
    )
    result = GlossaFilter().render(intent)
    print(f"digest: {result.digest}")
    for peer_id in sorted(result.peers):
        print(f"--- {peer_id} ---")
        print(result.peers[peer_id])
    print("--- audit ---")
    for row in result.audit:
        print(row["id"])


if __name__ == "__main__":
    main()
