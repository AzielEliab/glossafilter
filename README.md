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


## One-click install

```bash
curl -fsSL https://glossafilter-download-tracker.vibelock.workers.dev/install.sh | bash
```

The script curls the **counted** tarball from this project's Worker
(`/download`, User-Agent `Mozilla/5.0`), extracts, makes a venv, and
`pip install -e .`. Then run `glossafilter ui`.

Or tap **Download** / **One-click install** on the Worker homepage:
https://glossafilter-download-tracker.vibelock.workers.dev/

## Counted download (Cloudflare Worker)

**This is the counted download.** GitHub releases exist as a mirror.
The Worker serves the gzip itself (HTTP 200, no 302 to GitHub).

- Homepage: [https://glossafilter-download-tracker.vibelock.workers.dev/](https://glossafilter-download-tracker.vibelock.workers.dev/)
- Direct tarball: [glossafilter-0.1.0.tar.gz](https://glossafilter-download-tracker.vibelock.workers.dev/download?asset=glossafilter-0.1.0.tar.gz)
- One-click install: [https://glossafilter-download-tracker.vibelock.workers.dev/install.sh](https://glossafilter-download-tracker.vibelock.workers.dev/install.sh)
- Skill: [https://glossafilter-download-tracker.vibelock.workers.dev/v1/skill](https://glossafilter-download-tracker.vibelock.workers.dev/v1/skill)
- OpenAPI: [https://glossafilter-download-tracker.vibelock.workers.dev/openapi.json](https://glossafilter-download-tracker.vibelock.workers.dev/openapi.json)
- GitHub: [https://github.com/AzielEliab/glossafilter](https://github.com/AzielEliab/glossafilter)

Isolated counter: Worker `glossafilter-download-tracker`, KV `GLOSSAFILTER_DOWNLOADS`. `/v1` does not increment downloads.

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

## Use with Grok, ChatGPT, Venice

- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json

Live HTTPS runtime on the existing download-tracker Worker. Mediation, not concealment. No live translator APIs.

OpenAPI (ChatGPT GPT Actions / Venice custom HTTP / Grok custom tool):

```
https://glossafilter-download-tracker.vibelock.workers.dev/openapi.json
```

Setup notes: [https://glossafilter-download-tracker.vibelock.workers.dev/ai](https://glossafilter-download-tracker.vibelock.workers.dev/ai)

MCP catalog (ships separately): `https://aziel-runtime.vibelock.workers.dev/mcp`

```bash
curl -sS -X POST https://glossafilter-download-tracker.vibelock.workers.dev/v1/render \
  -H "content-type: application/json" \
  -d '{
    "channel": "tooling",
    "subject": "package",
    "rel": "release",
    "object": "filter",
    "action": "binds",
    "interface": "loopback"
  }'
```

## Cite this

Aziel Eliab. Glossa Filter. https://github.com/AzielEliab/glossafilter. https://glossafilter-download-tracker.vibelock.workers.dev.

- Catalog: https://aziel-runtime.vibelock.workers.dev/
- Worker homepage: https://glossafilter-download-tracker.vibelock.workers.dev/
- Counted download (gzip HTTP 200, no 302): https://glossafilter-download-tracker.vibelock.workers.dev/download
- GitHub: https://github.com/AzielEliab/glossafilter
- Citation JSON: https://glossafilter-download-tracker.vibelock.workers.dev/cite.json

## License

Apache-2.0. See [LICENSE](LICENSE).

Forks are welcome and always allowed.
