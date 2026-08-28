"""Command-line interface for Glossa Filter.

    glossafilter version
    glossafilter peers
    glossafilter render --subject ... --rel ... --object ... [--channel tooling|civic]
                        [--peer en-plain --peer es ...]
    glossafilter render --json intent.json
    glossafilter ui     # 127.0.0.1:8792 loopback only

Mediation, not secrecy. Parallel expression. No primary language.
Ethical boundaries: no deception, no incitement, no identity masking
for wrongdoing, clear separation between civic speech and tooling.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from glossafilter import __version__
from glossafilter.engine import GlossaFilter
from glossafilter.intent import GlossaError, Intent, Proposition, SLOT_KEYS
from glossafilter.packs import load_packs


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="glossafilter",
        description=(
            "Glossa Filter — deterministic linguistic mediation layer "
            "(Aziel Eliab, 2026). Peer renders, not a translator. "
            "Human opinion remains human, and tools remain tools. "
            "Local UI: `glossafilter ui` at http://127.0.0.1:8792."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("version", help="Print package version.")
    sub.add_parser("peers", help="List bundled peer ids. All equal; none primary.")

    p_render = sub.add_parser(
        "render",
        help="Render one Intent across selected peers (default: all bundled).",
    )
    p_render.add_argument(
        "intent_json",
        nargs="?",
        default=None,
        help="Path to an Intent JSON file.",
    )
    p_render.add_argument("--subject", default="", help="Proposition subject.")
    p_render.add_argument("--rel", default="", help="Proposition relation.")
    p_render.add_argument("--object", default="", dest="object_", help="Proposition object.")
    p_render.add_argument(
        "--channel",
        default="tooling",
        choices=["tooling", "civic"],
        help="tooling = behavior/interface only; civic may carry ethical intent.",
    )
    p_render.add_argument(
        "--peer",
        action="append",
        dest="peers",
        default=None,
        help="Peer id to include. Repeatable. Default: all bundled, equally.",
    )
    p_render.add_argument(
        "--note",
        default="",
        help="Civic-only notes. Rejected on channel=tooling.",
    )
    p_render.add_argument("--who", default="", help="Optional slot: who.")
    p_render.add_argument("--what", default="", help="Optional slot: what.")
    p_render.add_argument("--when", default="", help="Optional slot: when.")
    p_render.add_argument("--action", default="", help="Optional slot: action.")
    p_render.add_argument("--constraint", default="", help="Optional slot: constraint.")
    p_render.add_argument("--interface", default="", help="Optional slot: interface.")
    p_render.add_argument(
        "--proposition",
        action="append",
        dest="extra_props",
        default=[],
        help="Extra proposition as subject|rel|object. Repeatable.",
    )
    p_render.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Dump lineage JSON: digest, peers, audit, texts.",
    )

    p_ui = sub.add_parser(
        "ui",
        help="Serve the local mediation UI on 127.0.0.1:8792.",
    )
    p_ui.add_argument("--host", default="127.0.0.1", help="Loopback host (default 127.0.0.1).")
    p_ui.add_argument("--port", type=int, default=8792, help="Port (default 8792).")

    return parser


def _intent_from_args(args: argparse.Namespace) -> Intent:
    if args.intent_json:
        path = Path(args.intent_json)
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise GlossaError("intent JSON must be an object")
        return Intent.from_dict(data)
    propositions = []
    if args.subject or args.rel or args.object_:
        propositions.append(
            Proposition(subject=args.subject, rel=args.rel, object=args.object_)
        )
    for raw in args.extra_props or []:
        parts = [p.strip() for p in str(raw).split("|")]
        while len(parts) < 3:
            parts.append("")
        propositions.append(Proposition(subject=parts[0], rel=parts[1], object=parts[2]))
    slots = {}
    for key in SLOT_KEYS:
        value = getattr(args, key, "") or ""
        if str(value).strip():
            slots[key] = str(value).strip()
    return Intent(
        propositions=tuple(propositions),
        slots=slots,
        channel=args.channel,
        notes=args.note,
    )


def _print_human(result) -> None:
    for peer_id in sorted(result.peers):
        print(f"{peer_id}:")
        for line in result.peers[peer_id].splitlines() or [""]:
            print(f"  {line}")
        print()
    print(f"digest: {result.digest}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.cmd == "version":
        print(f"glossafilter {__version__}")
        return 0

    if args.cmd == "peers":
        packs = load_packs()
        for peer_id in sorted(packs):
            print(f"{peer_id}\t{packs[peer_id].label}")
        return 0

    if args.cmd == "render":
        try:
            intent = _intent_from_args(args)
            result = GlossaFilter().render(intent, peers=args.peers)
        except GlossaError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        except json.JSONDecodeError as exc:
            print(f"error: invalid JSON ({exc})", file=sys.stderr)
            return 1
        if args.as_json:
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            _print_human(result)
        return 0

    if args.cmd == "ui":
        from glossafilter.ui import serve

        try:
            serve(host=args.host, port=args.port)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        return 0

    parser.error(f"unknown command {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
