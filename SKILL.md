---
name: Glossa Filter
description: Use when calling Glossa Filter hosted /v1 or installing the local package. Dual surface: Worker /v1 + catalog MCP. This Worker /v1/mesh/* PROXY to aziel-runtime via AZIEL_RUNTIME. Suite mesh default OFF. QNM-BUILD-1.0 live|locked|isolated. No Node Gate. No auto-heal. Not anonymity. Author Aziel Eliab.
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
- `GET /v1/mesh` — PROXY suite mesh status. Default OFF. QNM live|locked|isolated. Never enables.
- `GET /v1/mesh/nodes` — PROXY Live Nodes roster (5-minute presence).
- `POST /v1/mesh/{enable,disable,join,heartbeat,leave,broadcast}` — PROXY. Bearer required to enable. No auto-heal. Anon-broadcast is not a publish path.
- Product POSTs listed in OpenAPI

Works with MCP/OpenAPI-capable assistants, including ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants. Import OpenAPI as a custom tool, GPT Action, HTTP tool, or MCP catalog entry.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://glossafilter-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://glossafilter-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' https://glossafilter-download-tracker.vibelock.workers.dev/v1/mesh
```

## Local (after one-click install)

```bash
curl -fsSL https://glossafilter-download-tracker.vibelock.workers.dev/install.sh | bash
glossafilter ui
glossafilter doctor
```

Then open http://127.0.0.1:8792 (loopback only). Worker homepage Live Nodes strip polls `GET /v1/mesh` (default OFF).

Counted download (gzip HTTP 200, no 302): https://glossafilter-download-tracker.vibelock.workers.dev/download?asset=glossafilter-0.1.0.tar.gz
GitHub: https://github.com/AzielEliab/glossafilter
