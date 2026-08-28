# Contributing to Glossa Filter

**Forks are first-class.** This project is Apache-2.0; you do not need
permission to fork, patch, or redistribute.

**Forks are welcome and always allowed.**

## How to run tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q
```

Python 3.10+. Core is stdlib only (`dataclasses`, `json`, `http.server`,
`argparse`, `hashlib`). pytest is the dev extra. No network. No ML. No
live translator.

## Ground rules

1. **This is mediation, not concealment.** Do not add steganography,
   identity masking, or "hide this" features. Do not market the product
   as secrecy.
2. **No primary language.** All peer packs are equal. Reject
   `canonical=true` / `primary=true`.
3. **Determinism stays byte-identical.** Identical Intent + identical
   peer set + identical packs → identical outputs. Sort keys. Register
   variants are picked from a SHA-256 of the canonical intent JSON
   (content-derived, never author-derived).
4. **Keep the dependency list tiny.** Stdlib only in the core. No
   Google / DeepL / LLM API. No network at runtime.
5. **UI binds loopback only** (`127.0.0.1`). Do not listen on `0.0.0.0`.
6. **Do not merge this product into ForgeReceipts, ZionPattern Solver,
   DecisionGATE, AZ-OS, or any *Lock tree.** Glossa Filter is standalone.
7. **Do not deploy the download tracker** from this tree. Parent ships.
8. New behavior needs a test that fails without the change.
9. **Separation of Roles:** `channel=tooling` may only talk about
   behavior and interface. Mixing philosophy into tooling is a failure,
   not a render.
10. Ethical boundaries stay in README and code comments:
    - No deception: content remains accurate.
    - No incitement: outputs are non-mobilizing.
    - No identity masking for wrongdoing.
    - Clear separation between civic speech and tooling.

## Where to change things

- Intent / validation: `glossafilter/intent.py`
- Peer packs: `glossafilter/packs/` and `glossafilter/packs.py`
- Render engine / audit: `glossafilter/engine.py`
- CLI: `glossafilter/cli.py`
- Local UI: `glossafilter/ui.py`, `glossafilter/web/`
- Spec: `docs/whitepaper.md`
- Isolated counter: `workers/download-tracker/`

## License of contributions

By submitting a change you agree it is licensed under Apache-2.0, the
same license as the rest of the tree. Keep the copyright lines honest.
