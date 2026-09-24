"""Command-line interface for Glossa Filter.

People get a short welcome, plain text, and a next step.
Machines pass --json and receive the same records as before.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Sequence

from glossafilter import __version__
from glossafilter.engine import GlossaFilter
from glossafilter.intent import GlossaError, Intent, Proposition, SLOT_KEYS
from glossafilter.packs import load_packs

HELP = """\
glossafilter — write one intent into every peer language

usage:
  glossafilter
  glossafilter ui
  glossafilter render --subject <subject> --rel <rel> --object <object>
  glossafilter <command> --help

commands:
  ui        Open http://127.0.0.1:8792/
  render    Render an intent into peer texts
  peers     List bundled peers
  doctor    Check this install
  version   Print the version

advanced:
  import <file>    Store a JSON document on this computer
  export <file>    Write the stored document to a file
  render --json    Print the machine record (digest, peers, audit, texts)
  render --peer    Include one peer (repeatable; default is every peer)
  render --note    Civic notes (refused on the tooling channel)
  render --who --what --when --action --constraint --interface

examples:
  glossafilter ui
  glossafilter render --subject package --rel release --object filter
  glossafilter render --json --subject package --rel release --object filter
  glossafilter doctor

Author: Aziel Eliab
"""

WELCOME = """\
Glossa Filter writes one intent into every bundled peer language.

Next, open the local page:
  glossafilter ui
  Open http://127.0.0.1:8792/

Or render from the terminal:
  glossafilter render --subject package --rel release --object filter

Check this install with glossafilter doctor.
Full command list: glossafilter --help

Author: Aziel Eliab
"""

_NEXT = {
    "EmptyIntentError": (
        "Give a subject, relation, and object. "
        "Example: glossafilter render --subject package --rel release --object filter"
    ),
    "IdentityFieldError": "Remove identity fields from the intent, then render again.",
    "ToolingPhilosophyError": "Drop --note, or switch to --channel civic.",
    "UnknownPeerError": "List peers with: glossafilter peers",
    "UnknownChannelError": "Use --channel tooling or --channel civic.",
    "CanonicalPeerError": "Leave every peer equal, then render again.",
}


class HumanParser(argparse.ArgumentParser):
    """Argparse with git-style top-level help and plain misuse messages."""

    human_help: str | None = None

    def format_help(self) -> str:
        if self.human_help:
            text = self.human_help
            return text if text.endswith("\n") else text + "\n"
        return super().format_help()

    def error(self, message: str) -> None:
        self.exit(2, _plain_arg_error(message))


def _plain_arg_error(message: str) -> str:
    low = message.lower()
    choice = re.search(r"invalid choice: '([^']*)'", message)
    if choice and "argument cmd" in low:
        name = choice.group(1)
        return (
            f'Unknown command "{name}". '
            "Try: glossafilter ui   or   glossafilter --help\n"
        )
    if "invalid choice" in low and "channel" in low:
        return (
            "Channel must be tooling or civic.\n"
            "Try: glossafilter render --channel tooling "
            "--subject package --rel release --object filter\n"
        )
    if "unrecognized arguments" in low:
        extra = message.split(":", 1)[-1].strip()
        return f"Unknown option {extra}. Try: glossafilter --help\n"
    if "required: path" in low:
        return (
            "A file path is required. "
            "Try: glossafilter import <file>   or   glossafilter export <file>\n"
        )
    if "the following arguments are required" in low:
        return "That command needs more detail. Try: glossafilter --help\n"
    if "invalid int" in low and "port" in low:
        return "Port must be a number. Try: glossafilter ui --port 8792\n"
    return f"{message}\nTry: glossafilter --help\n"


def _build_parser() -> HumanParser:
    parser = HumanParser(prog="glossafilter")
    parser.human_help = HELP
    sub = parser.add_subparsers(dest="cmd", required=False, parser_class=HumanParser)

    sub.add_parser("version", help="Print the version.")
    sub.add_parser("peers", help="List bundled peers.")

    p_render = sub.add_parser(
        "render",
        help="Render an intent into peer texts.",
        description="Render an intent into peer texts. Add --json for the machine record.",
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
        help="tooling stays on behavior and interface; civic may carry ethical intent.",
    )
    p_render.add_argument(
        "--peer",
        action="append",
        dest="peers",
        default=None,
        help="Peer id to include. Repeatable. Default: every bundled peer.",
    )
    p_render.add_argument(
        "--note",
        default="",
        help="Civic notes. Refused when --channel tooling.",
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
        help="Print the machine record: digest, peers, audit, texts.",
    )

    p_ui = sub.add_parser("ui", help="Open the local page on this computer.")
    p_ui.add_argument("--host", default="127.0.0.1", help="Loopback host (default 127.0.0.1).")
    p_ui.add_argument("--port", type=int, default=8792, help="Port (default 8792).")

    p_doc = sub.add_parser("doctor", help="Check this install. No network.")
    p_doc.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Print doctor results as JSON.",
    )

    p_imp = sub.add_parser("import", help="Store a JSON document on this computer.")
    p_imp.add_argument("path")
    p_imp.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Print the machine record.",
    )

    p_exp = sub.add_parser("export", help="Write the stored document to a file.")
    p_exp.add_argument("path")
    p_exp.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Print the machine record.",
    )

    return parser


def _intent_from_args(args: argparse.Namespace) -> Intent:
    if args.intent_json:
        path = Path(args.intent_json)
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
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


def _fail(reason: str, nxt: str) -> int:
    print(f"error: {reason}", file=sys.stderr)
    print(f"Next: {nxt}", file=sys.stderr)
    return 1


def _next_for(exc: BaseException) -> str:
    return _NEXT.get(type(exc).__name__, "Try: glossafilter render --help")


def _print_welcome() -> None:
    print(WELCOME, end="" if WELCOME.endswith("\n") else "\n")


def _print_human(result) -> None:
    labels = {}
    try:
        labels = {peer_id: pack.label for peer_id, pack in load_packs().items()}
    except GlossaError:
        labels = {}
    for peer_id in sorted(result.peers):
        label = labels.get(peer_id, "")
        title = f"{peer_id}: {label}" if label else f"{peer_id}:"
        print(title)
        for line in result.peers[peer_id].splitlines() or [""]:
            print(f"  {line}")
        print()
    print(f"digest: {result.digest}")


def _print_record(rec: dict, *, as_json: bool, human_lines: list[str]) -> None:
    if as_json:
        sys.stdout.write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
        return
    for line in human_lines:
        print(line)


def main(argv: Sequence[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    if not raw:
        _print_welcome()
        return 0

    parser = _build_parser()
    try:
        args = parser.parse_args(raw)
    except SystemExit as exc:
        code = exc.code
        if code is None or code == 0:
            return 0
        if isinstance(code, int):
            return code
        return 2

    if args.cmd is None:
        _print_welcome()
        return 0

    if args.cmd == "version":
        print(f"glossafilter {__version__}")
        return 0

    if args.cmd == "peers":
        packs = load_packs()
        width = max(len(peer_id) for peer_id in packs)
        for peer_id in sorted(packs):
            print(f"{peer_id.ljust(width)}  {packs[peer_id].label}")
        return 0

    if args.cmd == "render":
        try:
            intent = _intent_from_args(args)
            result = GlossaFilter().render(intent, peers=args.peers)
        except GlossaError as exc:
            nxt = _next_for(exc)
            if type(exc) is GlossaError and "object" in str(exc):
                nxt = "Pass a JSON object, or use --subject, --rel, and --object."
            return _fail(str(exc), nxt)
        except FileNotFoundError:
            return _fail(
                f"Couldn't read {args.intent_json}.",
                "Check the path, or pass --subject, --rel, and --object.",
            )
        except json.JSONDecodeError as exc:
            return _fail(
                f"invalid JSON ({exc.msg})",
                "Fix the file, or pass --subject, --rel, and --object.",
            )
        except OSError as exc:
            return _fail(str(exc), "Check the file path and try again.")
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
            print(f"error: {exc}", file=sys.stderr)
            print("Next: glossafilter ui --host 127.0.0.1 --port 8792", file=sys.stderr)
            return 2
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            print("Next: choose another port. Example: glossafilter ui --port 8793", file=sys.stderr)
            return 2
        return 0

    if args.cmd == "doctor":
        from glossafilter.doctor import run_doctor

        return run_doctor(as_json=getattr(args, "as_json", False))

    if args.cmd == "import":
        from glossafilter.jsonio import import_json

        try:
            rec = import_json(args.path)
        except json.JSONDecodeError as exc:
            return _fail(
                f"invalid JSON ({exc.msg})",
                f"Fix the file, then: glossafilter import {args.path}",
            )
        except ValueError as exc:
            return _fail(str(exc), "Pass a JSON object. Example: glossafilter import notes.json")
        except OSError as exc:
            return _fail(str(exc), "Check the path. Example: glossafilter import notes.json")
        keys = ", ".join(rec.get("keys") or []) or "(none)"
        _print_record(
            rec,
            as_json=args.as_json,
            human_lines=[
                f"Imported {rec.get('imported', args.path)}",
                f"Stored {rec.get('stored', '')}",
                f"Keys: {keys}",
            ],
        )
        return 0

    if args.cmd == "export":
        from glossafilter.jsonio import export_json

        try:
            rec = export_json(args.path)
        except OSError as exc:
            return _fail(str(exc), "Check the destination path and try again.")
        _print_record(
            rec,
            as_json=args.as_json,
            human_lines=[f"Exported {rec.get('exported', args.path)}"],
        )
        return 0

    parser.error(f"unknown command {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
