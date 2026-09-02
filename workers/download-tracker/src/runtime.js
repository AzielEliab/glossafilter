/**
 * Glossa Filter hosted runtime (port of intent.py + engine.py).
 * Mediation, not concealment. No live translator APIs. /v1 never touches DOWNLOADS KV.
 */
const PRODUCT = "glossafilter";
const EXAMPLE_PAYLOAD = {
  "subject": "package",
  "rel": "release",
  "object": "filter",
  "channel": "tooling"
};

const VERSION = "0.1.0";
const MOTTO = "Human opinion remains human, and tools remain tools.";
const HOST = "https://glossafilter-download-tracker.vibelock.workers.dev";
const SKILL = "---\nname: Glossa Filter\ndescription: Use when rendering the same intent into multiple language/dialect peers. Mediation, not concealment. No live translator APIs. Hosted /v1 via this Worker or aziel-runtime. Author Aziel Eliab.\n---\n\n# Glossa Filter\n\nHuman opinion remains human, and tools remain tools.\n\nAuthor: **Aziel Eliab**.\n\nUse when rendering the same intent into multiple language/dialect peers. Mediation, not concealment. No live translator APIs.\n\nAlways send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.\n\n## Endpoints (this Worker)\n\nHost: `https://glossafilter-download-tracker.vibelock.workers.dev`\n\n| Method | Path | What |\n|--------|------|------|\n| GET | `/v1/health` | Liveness. Does not increment downloads. |\n| GET | `/v1/skill` | This markdown. Does not increment downloads. |\n| GET | `/v1/peers` | List peer language packs. |\n| POST | `/v1/render` | Render intent into peer phrasings. No live translator APIs. |\n\nOpenAPI: `https://glossafilter-download-tracker.vibelock.workers.dev/openapi.json`\n\nCatalog OpenAPI: `https://aziel-runtime.vibelock.workers.dev/openapi.json`\n\nMCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`\n\nCatalog aliases under `/p/glossafilter/\u2026`.\n\n## How to call (Mozilla/5.0)\n\n```bash\ncurl -s -A 'Mozilla/5.0' https://glossafilter-download-tracker.vibelock.workers.dev/v1/health\ncurl -s -A 'Mozilla/5.0' -X POST https://glossafilter-download-tracker.vibelock.workers.dev/v1/render \\\n  -H 'content-type: application/json' \\\n  -d '{\"channel\":\"tooling\",\"intent\":{\"what\":\"release\",\"action\":\"publish\"}}'\ncurl -s -A 'Mozilla/5.0' https://glossafilter-download-tracker.vibelock.workers.dev/v1/skill\n```\n\nGrok: import the catalog OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.\n\n## Local (after one-click install)\n\n```bash\ncurl -fsSL https://glossafilter-download-tracker.vibelock.workers.dev/install.sh | bash\nglossafilter ui\n```\n\nThen open http://127.0.0.1:8792 (this computer only).\n\n## Honest banner\n\nTHIS IS: deterministic linguistic mediation into peer renders. THIS IS NOT: concealment, a live translator API, authorship stamping, or a canonical phrasing. Author Aziel Eliab.\n\nApache-2.0 (or the repo LICENSE). Forks are welcome and always allowed.\n\n## Catalog + local UI\n\nAuthor: **Aziel Eliab**. Honest scope: Render an intent across bundled peer ids. Human opinion remains human.\n\n- Catalog product: https://aziel-runtime.vibelock.workers.dev/p/glossafilter/\n- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json\n- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`\n- This Worker skill: `GET https://glossafilter-download-tracker.vibelock.workers.dev/v1/skill`\n- This Worker OpenAPI: https://glossafilter-download-tracker.vibelock.workers.dev/openapi.json\n- Sample payload: `GET https://glossafilter-download-tracker.vibelock.workers.dev/v1/example`\n\nLocal UI: **Import JSON file** (`type=file`) and **Export JSON**. Then `glossafilter doctor`.\n\nGrok: import catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.\n";

const CHANNELS = new Set(["tooling", "civic"]);
const SLOT_KEYS = ["who", "what", "when", "action", "constraint", "interface"];
const IDENTITY_FIELDS = new Set(["author","github","real_name","realname","real-name","identity","full_name","fullname","twitter","email"]);
const PHILOSOPHY_FIELDS = new Set(["philosophy","ideology","belief","doctrine","creed","worldview","partisan"]);
const CANONICAL_FIELDS = new Set(["canonical","primary","authoritative"]);
const PUNCT = `!"#$%&'()*+,-./:;<=>?@[\\]^_\`{|}~`;

const PACKS_RAW = {
  "en-formal": {
    "peer_id": "en-formal",
    "label": "English (formal)",
    "templates": {
      "proposition": "{subject} {rel} {object}.",
      "blurb": "{action} {interface}."
    },
    "glossary": {
      "package": "package",
      "release": "issues",
      "filter": "filter",
      "tool": "instrument",
      "interface": "interface",
      "behavior": "specified behavior",
      "binds": "attaches",
      "bind": "attaches",
      "channel": "channel",
      "loopback": "loopback interface",
      "speech": "speech",
      "remains": "remains",
      "human": "human",
      "tools": "instruments"
    },
    "register_variants": {
      "release": [
        "issues",
        "disseminates",
        "promulgates"
      ],
      "binds": [
        "attaches",
        "associates",
        "connects"
      ]
    }
  },
  "en-plain": {
    "peer_id": "en-plain",
    "label": "English (plain)",
    "templates": {
      "proposition": "{subject} {rel} {object}.",
      "blurb": "{action} {interface}."
    },
    "glossary": {
      "package": "package",
      "release": "ships",
      "filter": "filter",
      "tool": "tool",
      "interface": "interface",
      "behavior": "behavior",
      "binds": "binds",
      "bind": "binds",
      "channel": "channel",
      "loopback": "loopback",
      "speech": "speech",
      "remains": "stays",
      "human": "human",
      "tools": "tools"
    },
    "register_variants": {
      "release": [
        "ships",
        "puts out",
        "sends out"
      ],
      "binds": [
        "binds",
        "hooks to",
        "listens on"
      ]
    }
  },
  "es": {
    "peer_id": "es",
    "label": "Español",
    "templates": {
      "proposition": "{subject} {rel} {object}.",
      "blurb": "{action} {interface}."
    },
    "glossary": {
      "package": "paquete",
      "release": "publica",
      "filter": "filtro",
      "tool": "herramienta",
      "interface": "interfaz",
      "behavior": "comportamiento",
      "binds": "enlaza",
      "bind": "enlaza",
      "channel": "canal",
      "loopback": "bucle local",
      "speech": "habla",
      "remains": "permanece",
      "human": "humana",
      "tools": "herramientas"
    },
    "register_variants": {
      "release": [
        "publica",
        "emite",
        "expide"
      ],
      "binds": [
        "enlaza",
        "vincula",
        "asocia"
      ]
    }
  },
  "fr": {
    "peer_id": "fr",
    "label": "Français",
    "templates": {
      "proposition": "{subject} {rel} {object}.",
      "blurb": "{action} {interface}."
    },
    "glossary": {
      "package": "paquet",
      "release": "publie",
      "filter": "filtre",
      "tool": "outil",
      "interface": "interface",
      "behavior": "comportement",
      "binds": "lie",
      "bind": "lie",
      "channel": "canal",
      "loopback": "boucle locale",
      "speech": "parole",
      "remains": "demeure",
      "human": "humaine",
      "tools": "outils"
    },
    "register_variants": {
      "release": [
        "publie",
        "émet",
        "diffuse"
      ],
      "binds": [
        "lie",
        "associe",
        "relie"
      ]
    }
  },
  "ht": {
    "peer_id": "ht",
    "label": "Kreyòl Ayisyen",
    "templates": {
      "proposition": "{subject} {rel} {object}.",
      "blurb": "{action} {interface}."
    },
    "glossary": {
      "package": "pake",
      "release": "lage",
      "filter": "filtè",
      "tool": "zouti",
      "interface": "entèfas",
      "behavior": "konpòtman",
      "binds": "mare",
      "bind": "mare",
      "channel": "kanal",
      "loopback": "loopback",
      "speech": "pawòl",
      "remains": "rete",
      "human": "moun",
      "tools": "zouti"
    },
    "register_variants": {
      "release": [
        "lage",
        "voye",
        "pibliye"
      ]
    }
  },
  "pt": {
    "peer_id": "pt",
    "label": "Português",
    "templates": {
      "proposition": "{subject} {rel} {object}.",
      "blurb": "{action} {interface}."
    },
    "glossary": {
      "package": "pacote",
      "release": "publica",
      "filter": "filtro",
      "tool": "ferramenta",
      "interface": "interface",
      "behavior": "comportamento",
      "binds": "vincula",
      "bind": "vincula",
      "channel": "canal",
      "loopback": "loopback",
      "speech": "fala",
      "remains": "permanece",
      "human": "humana",
      "tools": "ferramentas"
    },
    "register_variants": {
      "release": [
        "publica",
        "emite",
        "divulga"
      ],
      "binds": [
        "vincula",
        "liga",
        "associa"
      ]
    }
  }
};

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...corsHeaders() },
  });
}

class GlossaError extends Error {
  constructor(message, code = 400) {
    super(message);
    this.code = code;
    this.name = "GlossaError";
  }
}

function normKey(key) {
  return String(key).trim().toLowerCase().replace(/-/g, "_");
}

function rejectForbiddenKeys(data, channel) {
  for (const [key, value] of Object.entries(data || {})) {
    const nk = normKey(key);
    if (IDENTITY_FIELDS.has(nk) || IDENTITY_FIELDS.has(key)) {
      throw new GlossaError(`identity field '${key}' is not allowed on Intent; authorship is not stamped onto renders`);
    }
    if (CANONICAL_FIELDS.has(nk) && value) {
      throw new GlossaError("one language treated as authoritative; all outputs are peers");
    }
    if (PHILOSOPHY_FIELDS.has(nk) && channel === "tooling") {
      throw new GlossaError("philosophy/ideology fields on channel=tooling are a failure, not a render");
    }
  }
}

function sortedJson(value) {
  if (value === null || value === undefined) return "null";
  if (typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return "[" + value.map(sortedJson).join(",") + "]";
  const keys = Object.keys(value).sort();
  return "{" + keys.map((k) => JSON.stringify(k) + ":" + sortedJson(value[k])).join(",") + "}";
}

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function loadPacks() {
  const packs = {};
  for (const raw of Object.values(PACKS_RAW)) {
    for (const flag of ["canonical", "primary", "authoritative"]) {
      if (raw[flag]) throw new GlossaError("one language treated as authoritative; all outputs are peers");
    }
    const peer_id = String(raw.peer_id || "").trim();
    const templates = {};
    for (const [k, v] of Object.entries(raw.templates || {})) {
      if (String(v).trim()) templates[String(k)] = String(v);
    }
    if (!templates.proposition) templates.proposition = "{subject} {rel} {object}.";
    if (!templates.blurb) templates.blurb = "{action} {interface}.";
    const glossary = {};
    for (const [k, v] of Object.entries(raw.glossary || {})) {
      if (String(k).trim() && String(v).trim()) glossary[String(k).trim().toLowerCase()] = String(v);
    }
    const variants = {};
    for (const [k, values] of Object.entries(raw.register_variants || {})) {
      const lemma = String(k).trim().toLowerCase();
      if (!lemma) continue;
      const items = Array.isArray(values) ? values.map(String).filter((x) => x.trim()) : [String(values)];
      if (items.length) variants[lemma] = items;
    }
    packs[peer_id] = {
      peer_id,
      label: String(raw.label || peer_id).trim(),
      templates,
      glossary,
      register_variants: variants,
    };
  }
  return packs;
}

const PACKS = loadPacks();

function parseIntent(data) {
  if (!data || typeof data !== "object") {
    throw new GlossaError("empty intent is a failure, not a render");
  }
  const channel = String(data.channel || "tooling").trim().toLowerCase();
  rejectForbiddenKeys(data, channel);
  if (!CHANNELS.has(channel)) {
    throw new GlossaError(`channel must be 'tooling' or 'civic', not '${channel}'`);
  }
  let slotsRaw = data.slots || {};
  if (slotsRaw && typeof slotsRaw !== "object") throw new GlossaError("slots must be a mapping");
  if (slotsRaw && typeof slotsRaw === "object") rejectForbiddenKeys(slotsRaw, channel);
  const propositions = [];
  const rawProps = data.propositions;
  if (Array.isArray(rawProps)) {
    for (const item of rawProps) {
      if (item && typeof item === "object") {
        propositions.push({
          subject: String(item.subject || ""),
          rel: String(item.rel || ""),
          object: String(item.object || ""),
        });
      }
    }
  }
  if (!propositions.length && (data.subject || data.rel || data.object)) {
    propositions.push({
      subject: String(data.subject || ""),
      rel: String(data.rel || ""),
      object: String(data.object || ""),
    });
  }
  const extra = data.extra_props || data.proposition;
  if (Array.isArray(extra)) {
    for (const raw of extra) {
      const parts = String(raw).split("|").map((p) => p.trim());
      while (parts.length < 3) parts.push("");
      propositions.push({ subject: parts[0], rel: parts[1], object: parts[2] });
    }
  }
  const notes = String(data.notes || data.note || "").trim();
  const slots = {};
  for (const [key, value] of Object.entries(slotsRaw || {})) {
    const nk = normKey(key);
    const text = String(value).trim();
    if (text) slots[nk] = text;
  }
  for (const key of SLOT_KEYS) {
    if (data[key] != null && data[key] !== "") slots[key] = String(data[key]);
  }
  if (channel !== "tooling" && channel !== "civic") {
    throw new GlossaError(`channel must be 'tooling' or 'civic', not '${channel}'`);
  }
  if (!propositions.length || propositions.every((p) => !(p.subject.trim() || p.rel.trim() || p.object.trim()))) {
    throw new GlossaError("empty intent is a failure, not a render");
  }
  if (channel === "tooling" && notes) {
    throw new GlossaError("notes are civic-only; mixing philosophy into tooling is a failure, not a render");
  }
  rejectForbiddenKeys(slots, channel);
  return {
    propositions: propositions.map((p) => ({
      subject: p.subject.trim(),
      rel: p.rel.trim(),
      object: p.object.trim(),
    })),
    slots,
    channel,
    notes: channel === "civic" ? notes : "",
  };
}

function canonicalDict(intent) {
  return {
    channel: intent.channel,
    notes: intent.channel === "civic" ? intent.notes : "",
    propositions: intent.propositions.map((p) => ({
      object: p.object,
      rel: p.rel,
      subject: p.subject,
    })),
    slots: Object.fromEntries(Object.keys(intent.slots).sort().map((k) => [k, intent.slots[k]])),
  };
}

function splitPunct(token) {
  let start = 0;
  let end = token.length;
  while (start < end && PUNCT.includes(token[start])) start += 1;
  while (end > start && PUNCT.includes(token[end - 1])) end -= 1;
  return [token.slice(0, start), token.slice(start, end), token.slice(end)];
}

function matchCase(original, surface) {
  if (!original || !surface) return surface;
  if (original === original.toUpperCase() && original.length > 1) return surface.toUpperCase();
  if (original[0] === original[0].toUpperCase()) return surface[0].toUpperCase() + surface.slice(1);
  return surface;
}

function pickVariantIndex(digestHex, peerId, lemma, n) {
  if (n <= 0) return 0;
  // sync fallback not used; this is called after we have digest bytes via hex
  return 0;
}

async function pickVariantIndexAsync(digest, peerId, lemma, n) {
  if (n <= 0) return 0;
  const material = new TextEncoder().encode(`${digest}|${peerId}|${lemma}`);
  const hashed = new Uint8Array(await crypto.subtle.digest("SHA-256", material));
  let n64 = 0n;
  for (let i = 0; i < 8; i++) n64 = (n64 << 8n) + BigInt(hashed[i]);
  return Number(n64 % BigInt(n));
}

function formatMap(tmpl, map) {
  return tmpl.replace(/\{([A-Za-z_][A-Za-z0-9_]*)\}/g, (_, k) => (map[k] != null ? map[k] : ""));
}

function auditRow(id, kind, peer, extra = {}) {
  const row = { id, kind, peer };
  for (const key of Object.keys(extra).sort()) row[key] = extra[key];
  return row;
}

async function surface(text, pack, digest, audit) {
  if (!text) return "";
  const out = [];
  for (const token of text.split(/\s+/)) {
    const [lead, core, trail] = splitPunct(token);
    const lemma = core.toLowerCase();
    if (!lemma) {
      out.push(token);
      continue;
    }
    if (pack.register_variants[lemma]) {
      const variants = pack.register_variants[lemma];
      const idx = await pickVariantIndexAsync(digest, pack.peer_id, lemma, variants.length);
      const s = matchCase(core, variants[idx]);
      audit.push(auditRow(`register:${pack.peer_id}:${lemma}`, "register_variant", pack.peer_id, { lemma, surface: s }));
      out.push(`${lead}${s}${trail}`);
    } else if (pack.glossary[lemma]) {
      const s = matchCase(core, pack.glossary[lemma]);
      audit.push(auditRow(`glossary:${pack.peer_id}:${lemma}`, "glossary", pack.peer_id, { lemma, surface: s }));
      out.push(`${lead}${s}${trail}`);
    } else {
      out.push(token);
    }
  }
  return out.join(" ");
}

async function renderPeer(intent, pack, digest) {
  const audit = [auditRow(`pack:${pack.peer_id}`, "pack", pack.peer_id, { label: pack.label })];
  const lines = [];
  const propTmpl = pack.templates.proposition || "{subject} {rel} {object}.";
  for (const prop of intent.propositions) {
    const subject = await surface(prop.subject, pack, digest, audit);
    const rel = await surface(prop.rel, pack, digest, audit);
    const obj = await surface(prop.object, pack, digest, audit);
    audit.push(auditRow(`template:${pack.peer_id}:proposition`, "template", pack.peer_id, { template: "proposition" }));
    const mapping = { subject, rel, object: obj };
    for (const [k, v] of Object.entries(intent.slots)) {
      mapping[k] = await surface(v, pack, digest, audit);
    }
    lines.push(formatMap(propTmpl, mapping).trim());
  }
  if (Object.keys(intent.slots).length) {
    const blurbTmpl = pack.templates.blurb || "";
    if (blurbTmpl) {
      const surfacedSlots = {};
      for (const [k, v] of Object.entries(intent.slots)) {
        surfacedSlots[k] = await surface(v, pack, digest, audit);
      }
      audit.push(auditRow(`template:${pack.peer_id}:blurb`, "template", pack.peer_id, { template: "blurb" }));
      const blurb = formatMap(blurbTmpl, surfacedSlots).trim();
      if (blurb) lines.push(blurb);
    }
  }
  if (intent.channel === "civic" && intent.notes) {
    const noteLine = await surface(intent.notes, pack, digest, audit);
    if (noteLine) lines.push(noteLine);
  }
  return { text: lines.filter(Boolean).join("\n"), audit };
}

async function render(intent, peers) {
  if (intent.canonical || intent.primary || intent.authoritative || intent.canonical_peer) {
    throw new GlossaError("one language treated as authoritative; all outputs are peers");
  }
  const digest = await sha256Hex(sortedJson(canonicalDict(intent)));
  let selected;
  if (peers == null) selected = Object.keys(PACKS).sort();
  else {
    selected = Array.isArray(peers) ? peers : [peers];
    const unknown = selected.filter((p) => !PACKS[p]);
    if (unknown.length) {
      throw new GlossaError(`unknown peer(s) ${JSON.stringify(unknown)}; bundled: ${JSON.stringify(Object.keys(PACKS).sort())}`);
    }
    selected = [...new Set(selected)].sort();
  }
  const texts = {};
  const audit = [];
  for (const peerId of selected) {
    const { text, audit: entries } = await renderPeer(intent, PACKS[peerId], digest);
    texts[peerId] = text;
    audit.push(...entries);
  }
  const ordered = Object.fromEntries(Object.keys(texts).sort().map((k) => [k, texts[k]]));
  return { audit, digest, peers: ordered, texts: ordered, motto: MOTTO, product: PRODUCT, version: VERSION };
}

function listPeers() {
  return {
    product: PRODUCT,
    version: VERSION,
    motto: MOTTO,
    note: "All peers are equal. None is primary. Mediation, not concealment. No live translator APIs.",
    peers: Object.keys(PACKS).sort().map((id) => ({ peer_id: id, label: PACKS[id].label })),
  };
}

function openapiSpec() {
  const intentSchema = {
    type: "object",
    properties: {
      channel: { type: "string", enum: ["tooling", "civic"] },
      subject: { type: "string" },
      rel: { type: "string" },
      object: { type: "string" },
      notes: { type: "string" },
      propositions: {
        type: "array",
        items: {
          type: "object",
          properties: { subject: { type: "string" }, rel: { type: "string" }, object: { type: "string" } },
        },
      },
      slots: { type: "object", additionalProperties: { type: "string" } },
      peers: { type: "array", items: { type: "string" } },
      who: { type: "string" },
      what: { type: "string" },
      when: { type: "string" },
      action: { type: "string" },
      constraint: { type: "string" },
      interface: { type: "string" },
    },
  };
  return {
    openapi: "3.1.0",
    info: {
      title: "Glossa Filter runtime",
      version: VERSION,
      description: "Deterministic linguistic mediation. Peer renders, not a translator. " + MOTTO,
    },
    servers: [{ url: HOST }],
    paths: {
      
            "/v1/example": { get: { operationId: "glossafilterExample", summary: "Sample JSON payload. Does not increment downloads.", responses: { "200": { description: "OK" } } } },
      "/v1/skill": {
        get: {
          operationId: "glossafilter_skill",
          summary: "Return skill markdown. Does not increment download KV.",
          responses: { "200": { description: "markdown" } },
        },
      },
"/v1/health": {
        get: { operationId: "health", summary: "Liveness", responses: { "200": { description: "ok", content: { "application/json": { schema: { type: "object" } } } } } },
      },
      "/v1/peers": {
        get: { operationId: "peers", summary: "List bundled peer ids (all equal).", responses: { "200": { description: "peers", content: { "application/json": { schema: { type: "object" } } } } } },
      },
      "/v1/render": {
        post: {
          operationId: "render",
          summary: "Render structured Intent across peers. Not a live translator.",
          requestBody: { required: true, content: { "application/json": { schema: intentSchema } } },
          responses: { "200": { description: "peer map", content: { "application/json": { schema: { type: "object" } } } } },
        },
      },
    },
  };
}

function aiHtml() {
  return `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Glossa Filter — use with Grok, ChatGPT, Venice</title>
<style>
  :root { color-scheme: dark; }
  body { font: 16px/1.45 system-ui, sans-serif; max-width: 42rem; margin: 3rem auto; padding: 0 1.25rem; background: #0e1014; color: #e8eaef; }
  code { background: #151922; padding: .15rem .4rem; border-radius: 4px; }
  a { color: #c9d4ff; }
  .motto { color: #9aa3b2; font-style: italic; }
</style>
<body>
  <h1>Glossa Filter live API</h1>
  <p class="motto">${MOTTO}</p>
  <p>Mediation, not concealment. Parallel peer renders. No live translator APIs (no Google / DeepL / LLM).</p>
  <h2>ChatGPT (GPT Actions)</h2>
  <p>Paste this OpenAPI URL into GPT Actions:</p>
  <p><code>${HOST}/openapi.json</code></p>
  <h2>Grok / xAI</h2>
  <p>Custom tool pointing at <code>POST ${HOST}/v1/render</code> and <code>GET ${HOST}/v1/peers</code>.</p>
  <h2>Venice</h2>
  <p>Custom HTTP tool from the same OpenAPI URL.</p>
  <h2>MCP catalog</h2>
  <p>The shared catalog (ships separately) is <code>https://aziel-runtime.vibelock.workers.dev/mcp</code>.</p>
  <p><a href="/openapi.json">openapi.json</a> · <a href="/v1/health">health</a> · <a href="/">downloads</a></p>
</body>
</html>`;
}

export async function handleRuntimeApi(request, url) {
  const path = url.pathname;
  const isApi = path === "/v1" || path.startsWith("/v1/") || path === "/openapi.json" || path === "/ai";
  if (!isApi) return null;
  try {
    if (path === "/v1/health" && request.method === "GET") {
      return json({ ok: true, author: "Aziel Eliab", product: PRODUCT, version: VERSION });
    }
  if ((path === "/v1/example" || path === "/v1/example/") && (request.method === "GET" || request.method === "HEAD")) {
    return json({
      ok: true,
      product: PRODUCT,
      author: "Aziel Eliab",
      example: EXAMPLE_PAYLOAD,
      note: "Sample payload only. Does not increment downloads.",
    });
  }

    if (path === "/v1/skill" && request.method === "GET") {
      return new Response(SKILL, {
      status: 200,
      headers: { "Content-Type": "text/markdown; charset=utf-8", "Cache-Control": "private, no-store", ...corsHeaders() },
      });
  }
    if (path === "/openapi.json" && request.method === "GET") return json(openapiSpec());
    if (path === "/ai" && request.method === "GET") {
      return new Response(aiHtml(), { headers: { "Content-Type": "text/html; charset=utf-8", ...corsHeaders() } });
    }
    if (path === "/v1/peers" && request.method === "GET") return json(listPeers());
    if (path === "/v1/render" && request.method === "POST") {
      let body;
      try { body = await request.json(); } catch { return json({ error: "JSON body required" }, 400); }
      if (body && (body.canonical || body.primary || body.authoritative || body.canonical_peer)) {
        throw new GlossaError("one language treated as authoritative; all outputs are peers");
      }
      const intent = parseIntent(body);
      const result = await render(intent, body.peers || body.peer || null);
      return json(result);
    }
    return json({ error: "not found" }, 404);
  } catch (err) {
    if (err instanceof GlossaError) return json({ error: err.message }, err.code || 400);
    return json({ error: String(err.message || err) }, 400);
  }
}
