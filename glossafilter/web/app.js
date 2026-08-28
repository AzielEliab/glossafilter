/* Glossa Filter UI. No CDN. Mediation, not a translator. No phone-home. */
(function () {
  const form = document.getElementById("intent-form");
  const stack = document.getElementById("peer-stack");
  const boxes = document.getElementById("peer-boxes");
  const exportBtn = document.getElementById("export");
  const channelEl = document.getElementById("channel");
  const notesEl = document.getElementById("notes");
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
      lab.appendChild(document.createTextNode(" " + p.peer_id + " — " + p.label));
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
    const out = [];
    boxes.querySelectorAll("input[data-peer]").forEach(function (el) {
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

  function paint(result) {
    lastResult = result;
    exportBtn.disabled = !result || !result.peers;
    stack.innerHTML = "";
    if (result.error) {
      const card = document.createElement("article");
      card.className = "peer-card error";
      card.innerHTML = '<div class="lamp" aria-hidden="true"></div><div><div class="title">' +
        (result.type || "error") + '</div><p class="text">' + result.error + "</p></div>";
      stack.appendChild(card);
      return;
    }
    const labels = {};
    peerMeta.forEach(function (p) { labels[p.peer_id] = p.label; });
    Object.keys(result.peers || {}).sort().forEach(function (pid) {
      const card = document.createElement("article");
      card.className = "peer-card PASS";
      const body = document.createElement("div");
      const title = document.createElement("div");
      title.className = "title";
      title.textContent = pid;
      const label = document.createElement("div");
      label.className = "label";
      label.textContent = labels[pid] || "peer";
      const text = document.createElement("p");
      text.className = "text";
      text.textContent = result.peers[pid];
      body.appendChild(title);
      body.appendChild(label);
      body.appendChild(text);
      const lamp = document.createElement("div");
      lamp.className = "lamp";
      lamp.setAttribute("aria-hidden", "true");
      card.appendChild(lamp);
      card.appendChild(body);
      stack.appendChild(card);
    });
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    const propositions = [
      {
        subject: document.getElementById("subject").value,
        rel: document.getElementById("rel").value,
        object: document.getElementById("object").value
      }
    ].concat(extraProps());
    const body = {
      channel: channelEl.value,
      propositions: propositions,
      slots: {
        action: document.getElementById("action").value,
        interface: document.getElementById("interface").value
      },
      notes: channelEl.value === "civic" ? notesEl.value : "",
      peers: selectedPeers()
    };
    fetch("/api/render", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    })
      .then(function (r) { return r.json(); })
      .then(paint)
      .catch(function (err) {
        paint({ error: String(err), type: "RequestError" });
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
})();
