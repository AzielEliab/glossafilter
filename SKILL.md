---
name: Glossa Filter
description: Use when calling Glossa Filter hosted /v1 or installing the local package. Author Aziel Eliab.
---

# Glossa Filter

A deterministic linguistic mediation layer. Peer renders, not a translator. Author: **Aziel Eliab**.

**THIS IS:** a deterministic linguistic mediation layer.

**THIS IS NOT:** a translator, a censorship filter, or a truth verdict. Hosted `/v1` does not increment downloads or views.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Call these URLs

- Worker OpenAPI: https://glossafilter-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Live skill (this markdown): `GET https://glossafilter-download-tracker.vibelock.workers.dev/v1/skill`

Ops (do **not** increment downloads or views):

- `GET /v1/health` — liveness
- `GET /v1/skill` — this file
- Product POSTs listed in OpenAPI

Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://glossafilter-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://glossafilter-download-tracker.vibelock.workers.dev/v1/skill
```

## Local (after one-click install)

```bash
curl -fsSL https://glossafilter-download-tracker.vibelock.workers.dev/install.sh | bash
glossafilter ui
glossafilter doctor
```

Then open http://127.0.0.1:8792 (loopback only).

Counted download (gzip HTTP 200, no 302): https://glossafilter-download-tracker.vibelock.workers.dev/download?asset=glossafilter-0.1.0.tar.gz
GitHub: https://github.com/AzielEliab/glossafilter

## Catalog + local UI

Author: **Aziel Eliab**. Honest scope: Render an intent across bundled peer ids. Human opinion remains human.

- Catalog product: https://aziel-runtime.vibelock.workers.dev/p/glossafilter/
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- This Worker skill: `GET https://glossafilter-download-tracker.vibelock.workers.dev/v1/skill`
- This Worker OpenAPI: https://glossafilter-download-tracker.vibelock.workers.dev/openapi.json
- Sample payload: `GET https://glossafilter-download-tracker.vibelock.workers.dev/v1/example`

Local UI: **Import JSON file** (`type=file`) and **Export JSON**. Then `glossafilter doctor`.

Grok: import catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.
