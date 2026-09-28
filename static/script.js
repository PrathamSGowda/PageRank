// PageRank Simulator - frontend only handles the UI. All maths happens in Python (/calculate).

// ---------- Graph state ----------
// graph[source][destination] = 1 means "source links to destination"
let labels = [];
let graph = [];
let nextId = 0;          // used to generate new page names
let result = null;       // last response from Flask (null when graph changed since)
let activeTab = "adjacency";
let selected = null;     // index of the node chosen as link source (null = none)

const $ = (id) => document.getElementById(id);
const SVG_NS = "http://www.w3.org/2000/svg";

function makeLabel(i) {
  // A..Z, then P27, P28, ...
  return i < 26 ? String.fromCharCode(65 + i) : "P" + (i + 1);
}

function resetGraph() {
  labels = []; graph = []; nextId = 0; result = null;
  selected = null;
  for (let i = 0; i < 4; i++) addPage(true);
  // small starting example: A->B, A->C, B->C, C->A, D->C
  [[0, 1], [0, 2], [1, 2], [2, 0], [3, 2]].forEach(([s, d]) => (graph[s][d] = 1));
  $("results").hidden = true;
  refresh();
  showMessage("");
}

function addPage(silent) {
  labels.push(makeLabel(nextId++));
  graph.forEach((row) => row.push(0));
  graph.push(new Array(labels.length).fill(0));
  if (!silent) { result = null; refresh(); showMessage(""); }
}

function removePage() {
  const i = Number($("removePageSelect").value);
  if (Number.isNaN(i) || labels.length === 0) return showMessage("There are no pages to remove.", true);
  labels.splice(i, 1);
  graph.splice(i, 1);
  graph.forEach((row) => row.splice(i, 1));
  result = null;
  refresh();
  showMessage("");
}

// Node click: first click = source, second click = destination (order sets direction)
function selectNode(i) {
  if (selected === null) {
    selected = i;
    updateSelection();
    return showMessage(`Source ${labels[i]} selected. Now click the destination page.`);
  }
  const from = selected;
  selected = null;
  changeLink(1, from, i);
  updateSelection();   // clears the highlight (also needed when changeLink only shows an error)
}

// Clicking an edge in the graph removes that link
function removeEdge(from, to) {
  graph[from][to] = 0;
  result = null;
  refresh();
  showMessage(`Removed link ${labels[from]} \u2192 ${labels[to]}.`);
}

function updateSelection() {
  [...$("nodes").children].forEach((g, i) => g.classList.toggle("selected", i === selected));
}

function changeLink(value, from, to) {
  if (labels.length === 0 || Number.isNaN(from) || Number.isNaN(to)) return showMessage("Add pages first.", true);
  if (from === to) return showMessage("A page cannot link to itself here. Pick two different pages.", true);
  if (graph[from][to] === value) {
    return showMessage(value ? `${labels[from]} already links to ${labels[to]}.` : `There is no link from ${labels[from]} to ${labels[to]}.`, true);
  }
  graph[from][to] = value;
  result = null;
  refresh();
  showMessage(value ? `Added link ${labels[from]} \u2192 ${labels[to]}.` : `Removed link ${labels[from]} \u2192 ${labels[to]}.`);
}

function showMessage(text, isError) {
  const el = $("message");
  el.textContent = text;
  el.classList.toggle("error", Boolean(isError));
}

// ---------- Controls ----------
function fillSelect(select, keepIndex) {
  const old = select.value;
  select.innerHTML = labels.map((l, i) => `<option value="${i}">${l}</option>`).join("");
  if (old !== "" && Number(old) < labels.length) select.value = old;
  else if (keepIndex !== undefined && keepIndex < labels.length) select.value = keepIndex;
}

function refresh() {
  selected = null;
  fillSelect($("removePageSelect"), 0);
  drawGraph();
  if (!result) $("results").hidden = true;
}

// ---------- SVG graph ----------
function nodePositions() {
  const n = labels.length, cx = 300, cy = 210, R = 145;
  if (n === 1) return [{ x: cx, y: cy }];
  return labels.map((_, i) => {
    const angle = -Math.PI / 2 + (2 * Math.PI * i) / n;
    return { x: cx + R * Math.cos(angle), y: cy + R * Math.sin(angle) };
  });
}

// Node radius: fixed, or slightly larger for higher PageRank after calculation
function radiusOf(i) {
  return result ? 20 + 22 * result.pagerank[i] : 24;
}

function drawGraph() {
  const pos = nodePositions();
  const edges = $("edges"), nodes = $("nodes");
  edges.innerHTML = ""; nodes.innerHTML = "";

  for (let s = 0; s < labels.length; s++) {
    for (let d = 0; d < labels.length; d++) {
      if (!graph[s][d]) continue;
      const a = pos[s], b = pos[d];
      // Bend the line a little if the reverse link also exists, so both arrows are visible
      const bend = graph[d][s] ? 28 : 0;
      const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy) || 1;
      const mx = (a.x + b.x) / 2 + (-dy / len) * bend;
      const my = (a.y + b.y) / 2 + (dx / len) * bend;
      // Start/end on the circle borders (aim toward the control point)
      const start = edgePoint(a, { x: mx, y: my }, radiusOf(s));
      const end = edgePoint(b, { x: mx, y: my }, radiusOf(d) + 2);
      const d_attr = `M${start.x},${start.y} Q${mx},${my} ${end.x},${end.y}`;
      const wrap = document.createElementNS(SVG_NS, "g");
      wrap.setAttribute("class", "edge-wrap");
      const path = document.createElementNS(SVG_NS, "path");
      path.setAttribute("class", "edge");
      path.setAttribute("d", d_attr);
      // wider invisible path so the thin line is easy to click
      const hit = document.createElementNS(SVG_NS, "path");
      hit.setAttribute("class", "edge-hit");
      hit.setAttribute("d", d_attr);
      hit.innerHTML = `<title>Click to remove ${labels[s]} \u2192 ${labels[d]}</title>`;
      hit.addEventListener("click", () => removeEdge(s, d));
      wrap.appendChild(path);
      wrap.appendChild(hit);
      edges.appendChild(wrap);
    }
  }

  labels.forEach((label, i) => {
    const g = document.createElementNS(SVG_NS, "g");
    g.setAttribute("class", "node");
    g.innerHTML = `<circle cx="${pos[i].x}" cy="${pos[i].y}" r="${radiusOf(i)}"></circle>
                   <text x="${pos[i].x}" y="${pos[i].y}">${label}</text>`;
    g.addEventListener("click", () => selectNode(i));
    nodes.appendChild(g);
  });
  updateSelection();
}

// Point on the circle around `center` in the direction of `toward`
function edgePoint(center, toward, r) {
  const dx = toward.x - center.x, dy = toward.y - center.y, len = Math.hypot(dx, dy) || 1;
  return { x: center.x + (dx / len) * r, y: center.y + (dy / len) * r };
}

// ---------- Calculate (talks to Flask) ----------
async function calculate() {
  if (labels.length === 0) return showMessage("Add at least one page before calculating.", true);
  try {
    const response = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ labels, graph }),
    });
    const data = await response.json();
    if (!response.ok) return showMessage(data.error || "Calculation failed.", true);
    result = data;
    showMessage(labels.length === 1 ? "Only one page: it holds all of the PageRank." : "PageRank calculated.");
    $("results").hidden = false;
    drawGraph();          // redraw with sizes based on PageRank
    renderMatrix();
    renderResults();
    $("results").scrollIntoView({ behavior: "smooth", block: "nearest" });
  } catch (err) {
    showMessage("Could not reach the Flask server. Is app.py running?", true);
  }
}

// ---------- Matrices ----------
const NOTES = {
  adjacency: "Rows are source pages, columns are destination pages. A 1 in row A, column B means A links to B.",
  transition: "Columns are source pages, rows are destination pages. Each column sums to 1. A page with no outgoing links (dangling) has 1/n in every row of its column.",
  google: "G = dM + ((1\u2212d)/n)J with d = 0.85. Same orientation as M: columns are source pages, rows are destination pages.",
};

function renderMatrix() {
  if (!result) return;
  const digits = activeTab === "adjacency" ? 0 : 4;
  const m = result[activeTab];
  const sourceIsRow = activeTab === "adjacency";
  $("matrixNote").textContent = NOTES[activeTab];

  // Headers make the orientation explicit
  const colHead = labels.map((l) => `<th>${sourceIsRow ? "to " : "from "}${l}</th>`).join("");
  let html = `<table><thead><tr><th></th>${colHead}`;
  if (sourceIsRow) html += `<th>links out</th>`;
  html += `</tr></thead><tbody>`;
  m.forEach((row, r) => {
    const rowHead = `${sourceIsRow ? "from " : "to "}${labels[r]}`;
    html += `<tr><th>${rowHead}</th>${row.map((v) => `<td>${v.toFixed(digits)}</td>`).join("")}`;
    if (sourceIsRow) html += `<td>${result.outgoing[r]}</td>`;
    html += `</tr>`;
  });
  if (!sourceIsRow) {
    // column sums, to show that each column is a probability distribution
    const sums = labels.map((_, c) => m.reduce((acc, row) => acc + row[c], 0));
    html += `<tr><th>column sum</th>${sums.map((s) => `<td>${s.toFixed(4)}</td>`).join("")}</tr>`;
  }
  $("matrixWrap").innerHTML = html + `</tbody></table>`;
}

// ---------- PageRank table ----------
function renderResults() {
  const max = Math.max(...result.pagerank);
  $("resultsBody").innerHTML = result.order.map((idx, position) => {
    const value = result.pagerank[idx];
    const width = max > 0 ? (value / max) * 100 : 0;
    return `<tr>
      <td>${position + 1}</td>
      <td>${labels[idx]}</td>
      <td>${value.toFixed(4)}</td>
      <td>${(value * 100).toFixed(2)}%</td>
      <td class="bar-cell"><div class="bar" style="width:${width}%"></div></td>
    </tr>`;
  }).join("");
}

// ---------- Events ----------
document.querySelectorAll(".tab").forEach((btn) =>
  btn.addEventListener("click", () => {
    activeTab = btn.dataset.tab;
    document.querySelectorAll(".tab").forEach((b) => b.classList.toggle("active", b === btn));
    renderMatrix();
  })
);
$("addPage").addEventListener("click", () => addPage(false));
$("removePage").addEventListener("click", removePage);
$("calculate").addEventListener("click", calculate);
$("reset").addEventListener("click", resetGraph);

resetGraph();
