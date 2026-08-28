# Glossa Filter

A deterministic **linguistic mediation layer**. Same functional or ethical
intent is rendered into multiple languages and dialects as **peers** (no
primary or canonical phrasing). Language is treated as a routing surface
("linguistic static IP"): a stable, repeatable mapping that preserves
semantic intent while varying surface expression. Transform rules are
inspectable. Meaning stays verifiable. Authorship is not stamped onto the
renders.

**Author:** Aziel Eliab
**Date:** 2026
**License:** [Apache-2.0](LICENSE)

> Human opinion remains human, and tools remain tools.

See the spec: [docs/whitepaper.md](docs/whitepaper.md).
How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

**Forks are welcome and always allowed.**

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
glossafilter ui
```

Open http://127.0.0.1:8792 (loopback only). No CDN, no telemetry.

Counted download: [https://glossafilter-download-tracker.vibelock.workers.dev/](https://glossafilter-download-tracker.vibelock.workers.dev/)



This tree is a standalone product; not ForgeReceipts / ZionPattern /
DecisionGATE / AZ-OS.

Counted downloads (number on the button, no user reporting):
[https://glossafilter-download-tracker.vibelock.workers.dev/](https://glossafilter-download-tracker.vibelock.workers.dev/)

GitHub: [https://github.com/AzielEliab/glossafilter](https://github.com/AzielEliab/glossafilter)

---

## What it is

- Structured **Intent** (propositions + slots + channel), not English as source.
- Bundled **peer packs** (`en-plain`, `en-formal`, `es`, `fr`, `pt`, `ht`). All equal.
- Deterministic renders: identical Intent + identical peer set + identical packs → byte-identical outputs.
- Anti-fingerprint variance that is **content-derived** (SHA-256 of canonical intent JSON), never author-derived.
- Inspectable **audit** of every template / glossary / register-variant id applied.
- Parallel expression: a map of `peer_id → text`, never a single "the" translation.

## What it is not

- Not concealment, steganography, identity masking, or a tool for hiding wrongdoing.
- Not a live translator (no Google / DeepL / LLM API, no network calls at runtime).
- Not a philosophy engine and not software that declares ideology.
- Not ForgeReceipts, ZionPattern Solver, DecisionGATE, AZ-OS, or any *Lock product.
- Do not market it as hiding identity. It is mediation, not secrecy.

## Ethical boundaries

- No deception: content remains accurate.
- No incitement: outputs are non-mobilizing.
- No identity masking for wrongdoing.
- Clear separation between civic speech and tooling.

`channel=tooling` renders may only talk about behavior and interface.
Mixing philosophy into tooling is a **failure**, not a render.
`channel=civic` may carry ethical or philosophical intent. Notes are civic-only.

## Install

Python 3.10+. Stdlib only at runtime.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI

```bash
glossafilter version          # glossafilter 0.1.0
glossafilter peers            # list bundled peer ids
glossafilter render --subject package --rel release --object filter --channel tooling
glossafilter render --json intent.json
glossafilter ui               # 127.0.0.1:8792 loopback only
```

`--json` on render dumps lineage: intent digest, peers, audit, texts.

## Library

```python
from glossafilter import GlossaFilter, Intent

intent = Intent.from_dict({
    "channel": "tooling",
    "propositions": [
        {"subject": "package", "rel": "release", "object": "filter"},
    ],
    "slots": {"action": "binds", "interface": "loopback"},
})
result = GlossaFilter().render(intent)
for peer_id, text in result.peers.items():
    print(peer_id, text)
print(result.digest)
for row in result.audit:
    print(row["id"])
```

## UI

`glossafilter ui` binds **127.0.0.1:8792** only. Form for channel,
proposition fields, optional extra propositions, peer checkboxes (all
selected by default, none labeled primary). Vertical equal stack of peer
outputs. JSON export of digest + audit + peers. Self-contained CSS, no
CDN, no phone-home. Motto on the page.


## iPhone & Android

Flutter sources: [`mobile/`](mobile/). Application id `com.azieeliab.glossafilter`. Offline. No analytics. Dark matte / gold.

Structured intent → peer renders (en-plain, en-formal, es). No canonical language. Mediation, not concealment.

```bash
cd mobile
flutter create --org com.azieeliab --project-name glossafilter .
flutter pub get
flutter run
```

The `android/` and `ios/` folders in this tree are skeleton READMEs until you run `flutter create .` (this machine has no Flutter SDK on PATH). Then open `android/` in Android Studio or `ios/Runner.xcworkspace` in Xcode. Not a store listing.

## Tests

```bash
pip install -e ".[dev]"
python -m pytest -q
```

Offline. No network. Stdlib runtime. pytest is the dev extra.

## Worker

Isolated download counter for this project only.
See [workers/download-tracker/README.md](workers/download-tracker/README.md).
Do not deploy wrangler from this tree; parent ships.

## Layout

```
glossafilter/       library (intent, packs, engine, cli, ui)
glossafilter/packs/ bundled peer packs (all equal)
tests/              pytest
docs/whitepaper.md  spec
mobile/             Flutter iPhone + Android (`flutter create .`)
workers/download-tracker/   Cloudflare Worker
```

## License

Apache-2.0. See [LICENSE](LICENSE).

Forks are welcome and always allowed.
