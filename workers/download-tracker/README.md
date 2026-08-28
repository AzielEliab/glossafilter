# Glossa Filter download tracker (Cloudflare Worker)

Counts GitHub-release downloads for Glossa Filter across the canonical
repository, other branches, and forks. Forks are identified by GitHub
`owner/repo`.

Homepage is an **isolated counter**: the number is on the download
button. Nobody reports a download. The click is the count.

GET `/download` **serves** the tarball via `env.ASSETS.fetch`. It does
not 302 to GitHub.

**Do not deploy wrangler from this tree.** Parent ships.

Until deploy,
`https://glossafilter-download-tracker.vibelock.workers.dev` will not
resolve. Send people to
[GitHub Releases](https://github.com/AzielEliab/glossafilter/releases).

No secrets belong in this directory.

Human opinion remains human, and tools remain tools. Forks are welcome
and always allowed.

This worker is Glossa Filter only. It is not mixed with ForgeReceipts,
ZionPattern Solver, DecisionGATE, AZ-OS, or any other product.

Isolated counter: Worker `glossafilter-download-tracker`, project
`glossafilter`.

## Bindings

| Binding     | Type | Purpose |
|-------------|------|---------|
| `DOWNLOADS` | KV   | Counters keyed `project|owner|repo|branch|fork` |

KV id in `wrangler.toml`: `4dca63572f354a3c9c60b354d1acc330`.
Binding name MUST stay `DOWNLOADS` (not `GLOSSA_DOWNLOADS`).

## Deploy (later — not from this tree)

Parent ships. Do not run `wrangler deploy` here. Do not create
`.wrangler`. Leave `public/` without the tarball until deploy; keep
`.gitkeep`.

The intended public URL is
`https://glossafilter-download-tracker.vibelock.workers.dev`.

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/` | Isolated homepage: live count on the download button |
| GET | `/download?repo=&tag=&asset=` | Increment KV, serve the asset from `ASSETS` |
| GET | `/stats` | JSON totals plus per-repo and per-branch breakdown |
| POST | `/event` | A fork reports a download |

Query params on `/download`: `owner`, `repo` (`AzielEliab/glossafilter` is
accepted), `branch`, `fork` (`1` or `owner/repo`), `tag`, `asset`.

Tracked asset URL (after deploy):

```
https://glossafilter-download-tracker.vibelock.workers.dev/download?repo=AzielEliab/glossafilter&tag=latest&asset=glossafilter-0.1.0.tar.gz
```

A fork reports its own download:

```bash
curl -X POST https://glossafilter-download-tracker.vibelock.workers.dev/event \
  -H "content-type: application/json" \
  -d '{
    "owner": "YourFork",
    "repo": "glossafilter",
    "branch": "main",
    "fork": "1",
    "asset": "glossafilter-0.1.0.tar.gz"
  }'
```

`fork=1` or `fork=YourFork/glossafilter`. If `owner/repo` is not
`AzielEliab/glossafilter`, the worker records `fork=1` automatically.

## Stats

`GET /stats` returns `total`, `by_repo`, `by_branch`, `by_fork`, and a
`breakdown` array so forks can read aggregates.

## CORS

All responses include `Access-Control-Allow-Origin: *`.
