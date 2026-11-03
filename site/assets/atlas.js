"use strict";

const element = id => document.getElementById(id);
const overview = "G53 G02 G54 G01 G04 G05 G06 G07 C26 G21 G23 C32 G24 G25 C90".split(" ");
const start = "G01";

function make(tag, text, className) {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (className) node.className = className;
  return node;
}

async function launch() {
  const response = await fetch("data/atlas.json");
  if (!response.ok) return;
  const atlas = await response.json();
  const concepts = new Map(atlas.concepts.map(row => [row.id, row]));
  const records = new Map([...atlas.concepts, ...atlas.sources].map(row => [row.id, row]));
  const groupLabels = new Map(atlas.groups.map(row => [row.id, row.label]));
  const labels = id => records.get(id).label || records.get(id).title;
  const href = id => (concepts.has(id) ? "concepts/" : "sources/") + records.get(id).slug + "/";
  const docEdges = [...atlas.documentRelations, ...atlas.readingLinks];
  const citations = atlas.concepts.flatMap(row => row.sources.map(source => ({
    from: row.id, to: source, kind: "source reference", reading: "Read the original source cited by this concept."
  })));
  const neighbors = new Map();
  for (const edge of [...atlas.relations, ...docEdges, ...citations]) {
    for (const id of new Set([edge.from, edge.to])) {
      if (!neighbors.has(id)) neighbors.set(id, []);
      neighbors.get(id).push(edge);
    }
  }

  function link(id, text) {
    const node = make("a", text || labels(id));
    node.href = href(id);
    return node;
  }

  function inspect(id) {
    const record = records.get(id);
    const side = element("inspector");
    const related = neighbors.get(id) || [];
    const entries = [...related.filter(edge => edge.kind === "source reference").slice(0, 3),
      ...related.filter(edge => edge.kind !== "source reference").slice(0, 6)];
    side.replaceChildren(
      make("p", groupLabels.get(record.group) || record.site, "tag"),
      make("h3", labels(id)),
      make("p", record.definition || record.kind),
      ...(record.boundary ? [make("p", record.boundary)] : []),
      link(id, concepts.has(id) ? "Open concept page →" : "Open source page →")
    );
    if (entries.length) {
      const list = make("ul");
      entries.forEach(edge => {
        const other = edge.from === id ? edge.to : edge.from;
        const row = make("li");
        const action = make("button", labels(other));
        action.type = "button";
        action.addEventListener("click", () => render(other));
        row.append(action, " · " + edge.kind);
        list.append(row);
      });
      side.append(list);
    }
  }

  element("explorer").hidden = false;
  const graph = cytoscape({
    container: element("graph"),
    layout: {name:"preset"},
    minZoom: .25,
    maxZoom: 2,
    style: [
      {selector:"node", style:{"label":"data(label)", "color":"#f9f5e8", "font-size":12, "font-weight":600, "text-wrap":"wrap", "text-max-width":120, "text-margin-y":7, "text-valign":"bottom", "text-outline-color":"#142925", "text-outline-width":3, "background-color":"#a8beae", "width":18, "height":18}},
      {selector:"node.focus", style:{"background-color":"#edbf7c","width":27,"height":27}},
      {selector:"node.document", style:{"shape":"round-rectangle"}},
      {selector:"edge", style:{"width":1.25,"line-color":"#a2b5a7","target-arrow-color":"#a2b5a7","target-arrow-shape":"triangle","curve-style":"bezier","opacity":.66}},
      {selector:"edge.conditional", style:{"line-style":"dashed","line-color":"#deb178","target-arrow-color":"#deb178"}}
    ]
  });
  graph.on("tap", "node", event => render(event.target.id()));
  graph.on("tap", "edge", event => {
    const edge = event.target.data("relationship");
    const title = make("h3");
    title.append(link(edge.from), " → ", link(edge.to));
    const side = element("inspector");
    side.replaceChildren(make("p", edge.predicate || edge.kind, "tag"), title);
    const reading = edge.reading || edge.relation_es;
    const condition = edge.condition || edge.condition_es || edge.boundary_es;
    if (reading) side.append(make("p", reading));
    if (condition) side.append(make("p", condition));
    for (const source of edge.sources || []) {
      const row = make("p");
      row.append(link(source));
      side.append(row);
    }
  });

  function render(focus) {
    const documents = focus ? !concepts.has(focus) : element("view").value === "documents";
    element("view").value = documents ? "documents" : "concepts";
    element("group").disabled = documents;
    const group = element("group").value;
    const primary = documents ? docEdges : atlas.relations;
    const pool = focus ? [...primary, ...citations] : primary;
    let ids;
    if (focus) {
      const adjacent = neighbors.get(focus) || [];
      const other = edge => edge.from === focus ? edge.to : edge.from;
      const references = [...new Set(adjacent.filter(edge => edge.kind === "source reference").map(other))].slice(0, 3);
      const peers = [...new Set(adjacent.filter(edge => edge.kind !== "source reference").map(other))].filter(id => id !== focus).slice(0, 11 - references.length);
      ids = [focus, ...peers, ...references];
    } else if (documents) {
      ids = [...new Set(docEdges.filter(edge => edge.from[0] !== edge.to[0]).slice(0, 12).flatMap(edge => [edge.from, edge.to]))].slice(0, 12);
    } else if (group) {
      ids = atlas.concepts.filter(row => row.group === group).sort((a, b) => (neighbors.get(b.id)?.length || 0) - (neighbors.get(a.id)?.length || 0)).slice(0, 14).map(row => row.id);
    } else {
      ids = overview;
    }

    const selected = new Set(ids);
    const active = focus || (selected.has(start) ? start : ids[0]);
    const edges = pool.filter(edge => selected.has(edge.from) && selected.has(edge.to));
    const wide = element("graph").clientWidth > 520;
    const columns = wide ? 4 : 3;
    const arrange = ids.map((id, i) => {
      const label = labels(id);
      return {data:{id,label:label.length > 51 ? label.slice(0, 48).replace(/\s+\S*$/, "") + "…" : label},
        position:{x:(i % columns) * 157,y:Math.floor(i / columns) * 101},
        classes:[id === active && "focus", !concepts.has(id) && "document"].filter(Boolean).join(" ")};
    });
    graph.elements().remove();
    graph.add(arrange.concat(edges.map((edge, i) => ({
      data:{id:"e" + i,source:edge.from,target:edge.to,relationship:edge},
      classes:/analog|comparison|transfer|hypoth/i.test(edge.kind) ? "conditional" : ""
    }))));
    graph.fit(undefined, 32);
    inspect(active);
  }

  for (const id of ["view", "group"]) element(id).addEventListener("change", () => render());
  element("fit").addEventListener("click", () => graph.fit(undefined, 32));
  element("query").addEventListener("input", event => {
    const query = event.target.value.trim().toLowerCase();
    const results = element("results");
    results.replaceChildren();
    results.hidden = query.length < 2;
    if (results.hidden) return;
    const all = [...records.values()];
    const hits = all.filter(row => labels(row.id).toLowerCase().includes(query))
      .sort((a, b) => Number(labels(b.id).toLowerCase() === query) - Number(labels(a.id).toLowerCase() === query));
    if (!hits.length) {
      results.append(make("span", "No titles match that search."));
      return;
    }
    for (const row of hits.slice(0, 9)) {
      const type = concepts.has(row.id) ? "Concept" : row.site;
      const button = make("button", labels(row.id) + " · " + type);
      button.type = "button";
      button.addEventListener("click", () => {
        render(row.id);
        results.hidden = true;
        element("inspector").querySelector("a").focus({preventScroll:true});
      });
      results.append(button);
    }
  });
  render();
}

if (typeof cytoscape === "function") {
  launch().catch(() => { element("explorer").hidden = true; });
}
