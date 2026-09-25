# Glossa Filter

Write one intent and read it in every peer language. The same record is rendered on this computer into equal peers: `en-plain`, `en-formal`, `es`, `fr`, `pt`, and `ht`.

**Author:** Aziel Eliab
**License:** [Apache-2.0](LICENSE)

> Human opinion remains human, and tools remain tools.

## Start

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e .
glossafilter
glossafilter ui
```

Open http://127.0.0.1:8792/ (this computer only).

A counted archive and install script are published at
https://glossafilter-download-tracker.vibelock.workers.dev/ .
See [RUN.txt](RUN.txt).

## Everyday commands

```bash
glossafilter ui
glossafilter render --subject package --rel release --object filter
glossafilter peers
glossafilter doctor
glossafilter --help
```

People see labeled peer texts. `glossafilter render --json` prints the machine record: digest, peers, audit, and texts. The same split is on the local page: HTML for people, JSON when the request asks for `application/json`.

`import`, `export`, extra slots, civic notes, and peer selection stay under **Advanced** in `--help` and on the local page.

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

Identical intent, peer set, and packs produce byte-identical text. The synonym pick is a SHA-256 of the canonical intent JSON (content-derived). The audit lists every template, glossary, and register id that was applied.

## Notes

Tooling renders stay on behavior and interface. Civic renders may carry ethical intent. Notes are civic-only.

Content stays accurate. Outputs stay non-mobilizing. Civic speech and tooling stay separate. Authorship is not written into the peer texts.

Packs are local glossaries and templates. A render does not call out to the network. Spec: [docs/whitepaper.md](docs/whitepaper.md). Contributions: [CONTRIBUTING.md](CONTRIBUTING.md). Forks are welcome and always allowed.

## Phone

Flutter sources live in [`mobile/`](mobile/). Application id `com.azieeliab.glossafilter`. Offline.

```bash
cd mobile
flutter create --org com.azieeliab --project-name glossafilter .
flutter pub get && flutter run
```

## Tests

```bash
pip install -e ".[dev]"
python -m pytest -q
```

Python 3.10+. The runtime is the standard library. pytest is the dev extra.

## For assistants

Hosted render (separate from the local command):

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

OpenAPI: https://glossafilter-download-tracker.vibelock.workers.dev/openapi.json

Suite mesh `/v1/mesh` proxies to aziel-runtime via `AZIEL_RUNTIME` (default off; QNM-BUILD-1.0 live|locked|isolated). QNS-CD-1.0 (photon QNS1 packet transfer) is a hub cite / Worker mesh cross-map only — local qnsd in [qnm-node](https://github.com/AzielEliab/qnm-node), runtime cites in [aziel-runtime](https://github.com/AzielEliab/aziel-runtime). No public qnsd proxy.

GitHub: https://github.com/AzielEliab/glossafilter

## Layout

```
glossafilter/       library, CLI, and local page
glossafilter/packs/ bundled peer packs
tests/              pytest
docs/whitepaper.md  spec
mobile/             Flutter
workers/download-tracker/   isolated download counter (do not deploy from this tree)
```
