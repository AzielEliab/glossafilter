/* Glossa Filter local page. Loopback. Local packs only. */
(function () {
  const form = document.getElementById("intent-form");
  const stack = document.getElementById("peer-stack");
  const boxes = document.getElementById("peer-boxes");
  const exportBtn = document.getElementById("export");
  const channelEl = document.getElementById("channel");
  const notesEl = document.getElementById("notes");
  const statusEl = document.getElementById("status");
  const digestEl = document.getElementById("digest-line");
  const SLOT_KEYS = ["who", "what", "when", "action", "constraint", "interface"];
  let lastResult = null;
  let peerMeta = [];

  function syncNotes() {
    const civic = channelEl.value === "civic";
    notesEl.disabled = !civic;
    if (!civic) notesEl.value = "";
  }
  channelEl.addEventListener("change", syncNotes);
  syncNotes();

  function renderBoxes(peers) {
    boxes.innerHTML = "";
    peers.forEach(function (p) {
      const lab = document.createElement("label");
      const input = document.createElement("input");
      input.type = "checkbox";
      input.checked = true;
      input.value = p.peer_id;
      input.setAttribute("data-peer", p.peer_id);
      lab.appendChild(input);
      lab.appendChild(document.createTextNode(" " + p.label + " (" + p.peer_id + ")"));
      boxes.appendChild(lab);
    });
  }

  fetch("/api/peers")
    .then(function (r) { return r.json(); })
    .then(function (data) {
      peerMeta = data.peers || [];
      renderBoxes(peerMeta);
    })
    .catch(function () {
      peerMeta = [
        {peer_id: "en-plain", label: "English (plain)"},
        {peer_id: "en-formal", label: "English (formal)"},
        {peer_id: "es", label: "Español"},
        {peer_id: "fr", label: "Français"},
        {peer_id: "pt", label: "Português"},
        {peer_id: "ht", label: "Kreyòl Ayisyen"}
      ];
      renderBoxes(peerMeta);
    });

  function selectedPeers() {
    const inputs = boxes.querySelectorAll("input[data-peer]");
    if (!inputs.length) return null;
    const out = [];
    inputs.forEach(function (el) {
      if (el.checked) out.push(el.value);
    });
    return out;
  }

  function extraProps() {
    const raw = document.getElementById("extra").value || "";
    return raw.split(/\n/).map(function (line) {
      const parts = line.split("|").map(function (s) { return s.trim(); });
      if (!parts[0] && !parts[1] && !parts[2]) return null;
      return { subject: parts[0] || "", rel: parts[1] || "", object: parts[2] || "" };
    }).filter(Boolean);
  }

  function slotValues() {
    const slots = {};
    SLOT_KEYS.forEach(function (key) {
      const el = document.getElementById(key);
      if (el && el.value.trim()) slots[key] = el.value.trim();
    });
    return slots;
  }

  function setField(id, value) {
    const el = document.getElementById(id);
    if (el && value) el.value = value;
  }

  function nextStep(type) {
    if (type === "EmptyIntentError") {
      return "Fill in subject, relation, and object, then render again.";
    }
    if (type === "IdentityFieldError") {
      return "Remove identity fields from the intent, then render again.";
    }
    if (type === "ToolingPhilosophyError") {
      return "Clear notes, or switch the channel to civic.";
    }
    if (type === "UnknownPeerError") {
      return "Open Advanced and choose peers from the list.";
    }
    if (type === "UnknownChannelError") {
      return "Choose tooling or civic.";
    }
    if (type === "RequestError") {
      return "If this keeps happening, stop the page and run glossafilter ui again.";
    }
    return "Check the fields and render again.";
  }

  function clearStack() {
    stack.innerHTML = "";
    digestEl.hidden = true;
    digestEl.textContent = "";
  }

  function paint(result) {
    lastResult = result && result.peers ? result : null;
    exportBtn.disabled = !lastResult;
    clearStack();
    if (!result || result.error) {
      const reason = (result && result.error) || "The render did not complete.";
      const step = nextStep(result && result.type);
      statusEl.textContent = reason + " " + step;
      return;
    }
    statusEl.textContent = "Each card is one peer. They are equal.";
    const labels = {};
    peerMeta.forEach(function (p) { labels[p.peer_id] = p.label; });
    Object.keys(result.peers || {}).sort().forEach(function (pid) {
      const card = document.createElement("article");
      card.className = "peer-card";
      const title = document.createElement("div");
      title.className = "title";
      title.textContent = pid;
      const label = document.createElement("div");
      label.className = "label";
      label.textContent = labels[pid] || "peer";
      const text = document.createElement("p");
      text.className = "text";
      text.textContent = result.peers[pid];
      card.appendChild(title);
      card.appendChild(label);
      card.appendChild(text);
      stack.appendChild(card);
    });
    if (result.digest) {
      digestEl.hidden = false;
      digestEl.textContent = "digest: " + result.digest;
    }
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    const subject = document.getElementById("subject").value.trim();
    const rel = document.getElementById("rel").value.trim();
    const object = document.getElementById("object").value.trim();
    const propositions = [{ subject: subject, rel: rel, object: object }].concat(extraProps());
    const blank = propositions.every(function (p) {
      return !p.subject && !p.rel && !p.object;
    });
    if (blank) {
      paint({
        error: "Nothing to render yet.",
        type: "EmptyIntentError"
      });
      return;
    }
    const peers = selectedPeers();
    if (peers && peers.length === 0) {
      paint({
        error: "Select at least one peer.",
        type: "UnknownPeerError"
      });
      return;
    }
    const body = {
      channel: channelEl.value,
      propositions: propositions,
      slots: slotValues(),
      notes: channelEl.value === "civic" ? notesEl.value : ""
    };
    if (peers) body.peers = peers;
    statusEl.textContent = "Rendering…";
    fetch("/api/render", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    })
      .then(function (r) { return r.json(); })
      .then(paint)
      .catch(function () {
        paint({
          error: "The page could not reach the local render service.",
          type: "RequestError"
        });
      });
  });

  exportBtn.addEventListener("click", function () {
    if (!lastResult) return;
    const blob = new Blob([JSON.stringify(lastResult, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "glossafilter-result.json";
    a.click();
    URL.revokeObjectURL(a.href);
  });

  const importEl = document.getElementById("import-json");
  if (importEl) importEl.addEventListener("change", function () {
    const f = importEl.files && importEl.files[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = function () {
      let obj;
      try {
        obj = JSON.parse(String(reader.result || "{}"));
      } catch (e) {
        paint({
          error: "That file is not JSON.",
          type: "RequestError"
        });
        return;
      }
      const intent = obj.intent || obj;
      if (intent.channel) channelEl.value = intent.channel;
      const props = intent.propositions || [];
      if (props[0]) {
        document.getElementById("subject").value = props[0].subject || "";
        document.getElementById("rel").value = props[0].rel || "";
        document.getElementById("object").value = props[0].object || "";
      }
      if (props.length > 1) {
        document.getElementById("extra").value = props.slice(1).map(function (p) {
          return [p.subject || "", p.rel || "", p.object || ""].join(" | ");
        }).join("\n");
      }
      const slots = intent.slots || {};
      SLOT_KEYS.forEach(function (key) {
        const el = document.getElementById(key);
        if (!el) return;
        el.value = slots[key] || intent[key] || "";
      });
      if (intent.notes) notesEl.value = intent.notes;
      syncNotes();
      document.getElementById("advanced").open = true;
      if (obj.peers && !Array.isArray(obj.peers)) paint(obj);
      else statusEl.textContent = "Imported. Render when you are ready.";
    };
    reader.readAsText(f);
  });
})();
