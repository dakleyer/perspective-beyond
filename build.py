"""Build the public Perspective Beyond atlas from its versioned records."""
from collections import defaultdict
from csv import writer
from hashlib import sha256
from html import escape
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"
BASE = "https://dakleyer.github.io/perspective-beyond/"

def data(name):
    return json.loads((ROOT / "data" / (name + ".json")).read_text(encoding="utf-8"))

concepts = data("concepts")
sources = data("sources")
relations = data("relations")
document_relations = data("document-relations")
reading_links = data("reading-links")
edition = data("edition")
article_maps = {row["source"]: row for row in data("article-maps")}
journeys = data("journeys")
groups = edition["groups"]
records = {r["id"]: r for r in concepts + sources}
concept_ids = {r["id"] for r in concepts}
group_labels = {g["id"]: g["label"] for g in groups}
source_by_url = {r["url"].rstrip("/"): r["id"] for r in sources}
atlas_version = sha256((ROOT / "site" / "assets" / "atlas.js").read_bytes()).hexdigest()[:12]
style_version = sha256((ROOT / "site" / "assets" / "atlas.css").read_bytes()).hexdigest()[:12]

MAPS = {
    "foundations": ("What the record can tell us", "Start with the distinction between what happens in an operation and what a model preserves. Follow the conditions under which evidence can support a decision, be reconstructed, or travel into a new setting.", "G53 G02 G54 G01 C60 C120"),
    "architecture": ("Evidence, authority and control", "Trace how participants qualify a decision, notice a change of regime and configure a response. The architecture connects provenance and local context to a feasible action, handoff or escalation.", "G04 G05 G06 G07 C25 C26 C47"),
    "human-intelligence": ("Human judgment inside the system", "Follow attribution, invisible work, informational friction and accumulated intelligence debt. A record that preserves the outcome and loses the judgment behind it leaves the next decision owner with less to work with.", "G21 G23 G22 C32 C83"),
    "interventions": ("How an intervention travels", "Read the work as a sequence of observation, design, field execution and transfer. The JUBAP framework, rationalization and Tiger Teams connect architectural intent to a bounded decision in a live operation.", "G24 G25 G47 C61 C64 C85 C90"),
    "cases": ("What field cases make visible", "Compare field mechanisms in logistics, mobility, industrial coordination and transformation. Follow each case into later methods through the stated relationship, source and operating conditions.", "G41 G27 G30 G49 C01 C02 C06"),
    "institutions": ("How capabilities move across institutions", "Follow the transfer of knowledge, operating responsibility and stewardship across companies, research groups and regional units. Locate the actor, the mandate and the evidence for each relationship.", "G51 C51 C57 C99 C103 C105 C109"),
}

def route(record):
    collection = "concepts" if record["id"] in concept_ids else "sources"
    return f'{collection}/{record["slug"]}/'

def ref(record_id, prefix):
    record = records[record_id]
    return f'<a href="{prefix}{route(record)}">{escape(record.get("label") or record["title"])}</a>'

def refs(ids, prefix):
    return '<ul class="chips">' + "".join(f"<li>{ref(i, prefix)}</li>" for i in dict.fromkeys(ids)) + "</ul>"

def inline(value, prefix):
    chunks = re.split(r"\[([^\]\n]+)\]\((https://[^\s)]+)\)", value)
    result = [escape(chunks[0])]
    for label, url, tail in zip(chunks[1::3], chunks[2::3], chunks[3::3]):
        record_id = source_by_url.get(url.rstrip("/"))
        if record_id:
            result.append(f'<a href="{prefix}{route(records[record_id])}">{escape(label)}</a>')
        else:
            result.append(escape(label))
        result.append(escape(tail))
    return "".join(result)

def card(record, prefix, line):
    return f'<li><a href="{prefix}{route(record)}"><strong>{escape(record.get("label") or record["title"])}</strong><span>{escape(line)}</span></a></li>'

def page(path, title, description, body, graph=False, term=None):
    prefix = "../" * path.count("/")
    canonical = BASE + path
    nav = "".join(f'<a href="{prefix}{p}">{label}</a>' for p, label in [("guide/", "Reading guide"), ("concepts/", "Concepts"), ("sources/", "Sources"), ("article-maps/", "Article maps"), ("heatmap/", "Heat map")])
    schema = {"@context": "https://schema.org", "@type": "DefinedTerm" if term else ("WebSite" if not path else "WebPage"), "name": title, "url": canonical, "description": description}
    if term:
        schema["inDefinedTermSet"] = BASE + "concepts/"
    scripts = (f'<script defer src="{prefix}assets/cytoscape-3.33.1.min.js"></script><script defer src="{prefix}assets/atlas.js?v={atlas_version}"></script>') if graph else ""
    full_title = title if not path else title + " · Perspective Beyond"
    target = OUT / path / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{canonical}"><meta property="og:title" content="{escape(full_title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{canonical}">
<link rel="stylesheet" href="{prefix}assets/atlas.css?v={style_version}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace("<", chr(92) + "u003c")}</script>{scripts}
</head><body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="shell"><a class="brand" href="{prefix or './'}"><span aria-hidden="true">◈</span> Perspective Beyond</a><nav aria-label="Main navigation">{nav}</nav></div></header>
<main id="main" class="shell">{body}</main>
<footer class="foot"><div class="shell"><span>Perspective Beyond · Edition {edition["edition"]}</span><a href="https://github.com/dakleyer/perspective-beyond">Edit or cite on GitHub ↗</a></div></footer></body></html>
''', encoding="utf-8")

def heading(kicker, title, lead):
    return f'<header class="intro"><p class="kicker">{escape(kicker)}</p><h1>{escape(title)}</h1><p class="lead">{escape(lead)}</p></header>'

def group_cards(group, prefix):
    return '<ul class="tiles">' + "".join(card(c, prefix, c["definition"]) for c in sorted(concepts, key=lambda c: c["label"].lower()) if c["group"] == group) + "</ul>"

def index_by_endpoint(rows):
    index = defaultdict(list)
    for row in rows:
        index[row["from"]].append(row)
        if row["from"] != row["to"]:
            index[row["to"]].append(row)
    return index

def connections(rows, record_id, prefix):
    if not rows:
        return ""
    content = []
    for row in rows:
        outward = row["from"] == record_id
        other = row["to"] if outward else row["from"]
        statement = row.get("reading") or row.get("relation_es") or row["kind"]
        condition = row.get("condition") or row.get("condition_es") or row.get("boundary_es")
        details = f'<p class="condition">{escape(condition)}</p>' if condition else ""
        evidence = refs(row["sources"], prefix) if row.get("sources") else ""
        direction = "To" if outward else "From"
        label = row.get("predicate", row["kind"]).replace("_", " ")
        content.append(f'<li><span class="tag">{escape(label)} · {direction}</span><h3>{ref(other, prefix)}</h3><p>{inline(statement, prefix)}</p>{details}{evidence}</li>')
    return '<ul class="edges">' + "".join(content) + "</ul>"

def guide():
    source = (ROOT / "narrative" / "guide.md").read_text(encoding="utf-8")
    parts = source.strip().split("\n\n")
    body = heading("Reading guide", parts[0].removeprefix("# "), parts[1])
    body += '<div class="prose">'
    for block in parts[2:]:
        if block.startswith("## "):
            body += "<h2>" + escape(block[3:]) + "</h2>"
        elif block.startswith("[["):
            body += refs(re.findall(r"\[\[([A-Z0-9]+)\]\]", block), "../")
        elif re.match(r"1\. ", block):
            body += "<ol>" + "".join("<li>" + escape(re.sub(r"^\d+\. ", "", line)) + "</li>" for line in block.splitlines()) + "</ol>"
        else:
            body += "<p>" + escape(block) + "</p>"
    body += '<p><a class="button" href="../journeys/">Explore the twelve reading journeys →</a></p>'
    page("guide/", "A guide to Perspective Beyond", parts[1], body + "</div>")

def reading_journeys():
    lead = "Trace a case or a question through its mechanism, practical use and conditions."
    items = "".join(f'<li><a href="#{j["id"]}"><span class="tag">{index:02}</span><strong>{escape(j["title"])}</strong></a></li>'
                    for index, j in enumerate(journeys, 1))
    body = heading("Case to mechanism", "Twelve reading journeys", lead)
    body += f'<nav aria-label="Reading journeys"><ol class="tiles">{items}</ol></nav>'
    for index, journey in enumerate(journeys, 1):
        steps = "".join("<li>" + " · ".join(ref(key, "../") for key in step) + "</li>" for step in journey["steps"])
        body += f'''<section class="section journey" id="{journey["id"]}">
<p class="kicker">Journey {index:02}</p><h2>{escape(journey["title"])}</h2>
<ol class="journey-steps">{steps}</ol>
<p><strong>In practice.</strong> {escape(journey["application"])}</p>
<p class="condition"><strong>Conditions.</strong> {escape(journey["boundary"])}</p>
</section>'''
    page("journeys/", "Twelve reading journeys", lead, body)

def heat_table(labels, counts, caption):
    maximum = max(counts.values())
    headings = "".join(f'<th scope="col">{escape(label)}</th>' for _, label, _ in labels)
    rows = []
    for origin, label, href in labels:
        cells = []
        for target, _, _ in labels:
            count = counts[(origin, target)]
            strength = round((count / maximum) ** .55 * 72)
            cells.append(f'<td style="background:color-mix(in srgb,#af7e43 {strength}%,#fffdf8)">{count}</td>')
        name = f'<a href="{href}">{escape(label)}</a>' if href else escape(label)
        rows.append(f'<tr><th scope="row">{name}</th>{"".join(cells)}</tr>')
    return f'<div class="table-wrap" tabindex="0" role="region" aria-label="{escape(caption, quote=True)}"><table><caption>{escape(caption)}</caption><thead><tr><th scope="col">From ↓ / To →</th>{headings}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'

def save_matrix(name, origins, targets, counts):
    def label(row):
        return f'{row["id"]} {row.get("label") or row["title"]}'

    with (OUT / "data" / name).open("w", encoding="utf-8-sig", newline="") as handle:
        out = writer(handle, lineterminator="\n")
        out.writerow(["Origin / destination", *(label(t) for t in targets)])
        for origin in origins:
            out.writerow([label(origin), *(counts.get((origin["id"], t["id"]), 0) for t in targets)])

def heatmap():
    paths = defaultdict(int)
    all_concepts = defaultdict(int)
    original_concepts = defaultdict(int)
    families = defaultdict(int)
    for row in relations:
        a, b = records[row["from"]], records[row["to"]]
        paths[(a["group"], b["group"])] += 1
        all_concepts[(a["id"], b["id"])] += 1
        if "relation_es" in row:
            original_concepts[(a["id"], b["id"])] += 1
            families[(a["family"], b["family"])] += 1
    base = [c for c in concepts if c["layer"] == "concept inventory"]
    family_names = list(dict.fromkeys(c["family"] for c in base))
    citation_counts = {(c["id"], source): 1 for c in concepts for source in c["sources"]}
    save_matrix("concept-matrix.csv", concepts, concepts, all_concepts)
    save_matrix("original-concept-matrix.csv", base, base, original_concepts)
    save_matrix("concept-source-matrix.csv", concepts, sources, citation_counts)
    lead = "Read across each row to see where its relationships lead. The diagonal counts relationships within a reading path."
    body = heading("Corpus structure", "Relationship heat map", lead)
    body += heat_table([(g["id"], g["label"], f'../maps/{g["id"]}/') for g in groups],
                       paths, f"{len(relations)} directed concept relationships by reading path")
    body += '<p class="map-key">Darker cells indicate more recorded relationships. The counts describe coverage in this edition. Use the individual relationship and source pages to judge the strength of each connection.</p>'
    body += '<section class="section"><h2>Ten families of the original corpus</h2>'
    body += heat_table([(name, name, None) for name in family_names], families,
                       f"{sum(families.values())} directed relationships in the original corpus")
    body += '''<h2>Download the full matrices</h2>
<ul class="chips">
<li><a href="../data/concept-matrix.csv" download>Combined concepts · 179 × 179</a></li>
<li><a href="../data/original-concept-matrix.csv" download>Original concepts · 125 × 125</a></li>
<li><a href="../data/concept-source-matrix.csv" download>Concepts and sources · 179 × 278</a></li>
</ul><p class="map-key">Concept cells count directed relationships. A 1 in the source matrix marks a citation.</p></section>'''
    page("heatmap/", "Relationship heat map", lead, body)

def article_map(entry):
    def nodes(items):
        result = []
        for item in items:
            record = records[item["id"]]
            label = record.get("label") or record["title"]
            target = "../../" + route(record) if item["id"] in concept_ids else record["url"]
            tag = f'<span class="pbm-type">{escape(item["relationship"])}</span>' if "relationship" in item else ""
            result.append(f'<li><a href="{escape(target, quote=True)}">{tag}<strong>{escape(label)}</strong><span class="pbm-meaning">{escape(item["reading"])}</span></a></li>')
        return "<ul>" + "".join(result) + "</ul>"
    title = escape(records[entry["source"]]["title"])
    concepts, neighbors = entry["concepts"], entry["neighbors"]
    return f'''<details class="pbm" id="article-map" open>
<summary><span class="pbm-mark" aria-hidden="true">◇</span><span class="pbm-label">Concept map</span><span class="pbm-count">{len(concepts) + len(neighbors)} connections</span><span class="pbm-toggle" aria-hidden="true"></span></summary>
<div class="pbm-body"><p class="pbm-hub"><span>THIS ARTICLE</span><strong>{title}</strong></p>
<div class="pbm-branches"><section aria-label="Concepts and methods"><p class="pbm-branch">Concepts and methods</p>{nodes(concepts)}</section>
<section aria-label="Closest readings"><p class="pbm-branch">Closest readings</p>{nodes(neighbors)}</section></div></div></details>'''

def map_index():
    lead = "Open a compact map for an article or case to find its main ideas and the closest readings across the corpus."
    body = heading("Four sites · one corpus", "Article concept maps", lead)
    by_site = defaultdict(list)
    for record_id in article_maps:
        by_site[records[record_id]["site"]].append(records[record_id])
    for site, entries in sorted(by_site.items()):
        items = "".join(
            f'<li><a href="../{route(r)}#article-map"><strong>{escape(r["title"])}</strong><span>Open concept map →</span></a></li>'
            for r in sorted(entries, key=lambda r: r["title"].lower())
        )
        body += f'<section class="section"><h2>{escape(site)} <small>{len(entries)}</small></h2><ul class="tiles">{items}</ul></section>'
    page("article-maps/", "Article concept maps", lead, body)

def build():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "site" / "assets", OUT / "assets", dirs_exist_ok=True)
    (OUT / ".nojekyll").touch()
    (OUT / "data").mkdir(exist_ok=True)
    graph = {"concepts": concepts, "sources": sources, "relations": relations, "documentRelations": document_relations, "readingLinks": reading_links, "groups": groups}
    (OUT / "data" / "atlas.json").write_text(json.dumps(graph, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    maps = "".join(f'<li><a href="maps/{g["id"]}/"><span class="tag">{g["label"]}</span><strong>{escape(MAPS[g["id"]][0])}</strong><span>{escape(MAPS[g["id"]][1])}</span></a></li>' for g in groups)
    lead = "An atlas of how evidence, judgment and authority shape action across research, operating systems and field interventions."
    home = f'''<section class="hero"><div><p class="kicker">An atlas of architectural thought</p>
<h1>Perspective<br>Beyond<span>.</span></h1><p class="lead">{lead}</p>
<div class="actions"><a class="button" href="#atlas">Explore the map ↓</a><a href="guide/">Read the guide →</a></div></div>
<div class="plate"><svg viewBox="0 0 420 320" aria-hidden="true"><defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M 24 0 L 0 0 0 24" fill="none" stroke="#acb6b2" stroke-opacity=".22"/></pattern></defs>
<rect width="420" height="320" fill="url(#grid)"/><g fill="none" stroke="#9cb4ad"><ellipse cx="210" cy="160" rx="146" ry="80" transform="rotate(-26 210 160)"/><ellipse cx="210" cy="160" rx="146" ry="80" transform="rotate(25 210 160)"/><ellipse cx="210" cy="160" rx="91" ry="111"/><path d="M46 160H374M210 30V290" opacity=".55"/></g>
<g fill="#e2b46a"><circle cx="210" cy="160" r="8"/><circle cx="123" cy="115" r="5"/><circle cx="283" cy="224" r="5"/><circle cx="298" cy="131" r="5"/><circle cx="210" cy="49" r="4"/><circle cx="210" cy="271" r="4"/></g></svg><span>Evidence · judgment · action</span></div></section>
<div class="metrics"><div><b>{len(concepts)}</b><span>Concepts</span></div><div><b>{len(sources)}</b><span>Sources</span></div><div><b>{len(relations)}</b><span>Concept relationships</span></div><div><b>{len(groups)}</b><span>Reading paths</span></div></div>
<section class="section" id="atlas"><p class="kicker">Interactive atlas</p><h2>Follow a question across the corpus</h2>
<p class="lead">Select a node to trace a relationship. Switch to documents to compare source material and follow further reading.</p>
<div class="explorer" id="explorer" hidden><div class="controls"><label>View<select id="view"><option value="concepts">Concepts</option><option value="documents">Documents</option></select></label><label>Reading path<select id="group"><option value="">Overview</option>{"".join(f'<option value="{g["id"]}">{g["label"]}</option>' for g in groups)}</select></label><label class="search">Find a concept or source<input id="query" type="search" placeholder="e.g. Regime Awareness"></label><button id="fit" type="button">Fit map</button></div><div id="results" class="results" hidden></div>
<div class="map-layout"><div id="graph" aria-label="Visual relationship map"></div><aside id="inspector" aria-live="polite"></aside></div></div>
<p class="map-key">Circles are concepts and squares are sources. Select a node to open its neighborhood or an arrow to read the relationship. Dashed lines mark comparisons, possible transfers and hypotheses.</p>
<p class="alternatives"><a href="concepts/">Browse all concepts →</a> <a href="sources/">Browse the sources →</a> <a href="heatmap/">See the relationship heat map →</a></p></section>
<section class="section"><p class="kicker">Six reading paths</p><h2>Start where your question begins</h2><ul class="tiles">{maps}</ul></section>
<section class="section closing"><p class="kicker">The reading guide</p><h2>From a representation to an accountable decision</h2><p>Follow the argument from Logic Fields and Structural Awareness to the JUBAP framework, Tiger Teams, operational cases and institutional stewardship.</p><p class="alternatives"><a href="guide/">Read the full guide →</a> <a href="journeys/">Explore the twelve reading journeys →</a></p></section>'''
    page("", "Perspective Beyond", lead, home, graph=True)

    body = heading("Concept index", "Concepts", "Definitions, operating conditions and relationships across the Perspective Beyond corpus.")
    for group in groups:
        body += f'<section class="section"><h2><a href="../maps/{group["id"]}/">{group["label"]}</a></h2>{group_cards(group["id"], "../")}</section>'
        slug = group["id"]
        title, lead, anchors = MAPS[slug]
        page(f"maps/{slug}/", title, lead, heading(group["label"], title, lead) + '<section class="section"><h2>Start here</h2>' + refs(anchors.split(), "../../") + '</section><section class="section"><h2>Concepts on this path</h2>' + group_cards(slug, "../../") + '</section>')
    page("concepts/", "Concepts", "Definitions and links across 179 concepts in six reading paths.", body)

    by_concept = index_by_endpoint(relations)
    cited_by = defaultdict(list)
    for concept in concepts:
        for source_id in concept["sources"]:
            cited_by[source_id].append(concept["id"])
        body = heading(group_labels[concept["group"]], concept["label"], concept["definition"])
        body += f'<p class="back"><a href="../../maps/{concept["group"]}/">← {group_labels[concept["group"]]}</a></p>'
        body += '<section class="callout"><h2>When it applies</h2><p>' + escape(concept["boundary"]) + '</p></section>'
        if concept["sources"]:
            body += '<section class="section"><h2>Sources</h2>' + refs(concept["sources"], "../../") + '</section>'
        if by_concept[concept["id"]]:
            body += '<section class="section"><h2>Relationships</h2>' + connections(by_concept[concept["id"]], concept["id"], "../../") + '</section>'
        page(route(concept), concept["label"], concept["definition"], body, term=concept)

    by_document = index_by_endpoint(document_relations)
    published = defaultdict(list)
    for row in reading_links:
        published[row["from"]].append(row)
    by_site = defaultdict(list)
    for source in sources:
        by_site[source["site"]].append(source)
        body = heading(source["site"], source["title"], source["kind"].capitalize())
        body += f'<p class="source-meta"><a class="button" href="{escape(source["url"], quote=True)}">Read the original ↗</a>'
        if source.get("date"):
            body += f'<span>{escape(source["date"])}</span>'
        if source.get("version"):
            body += f'<span>Version <code>{escape(source["version"])}</code></span>'
        body += '</p>'
        source_id = source["id"]
        if source_id in article_maps:
            body += article_map(article_maps[source_id])
        if cited_by[source_id]:
            body += '<section class="section"><h2>Concepts that cite this source</h2>' + refs(cited_by[source_id], "../../") + '</section>'
        if by_document[source_id]:
            body += '<section class="section"><h2>Document comparisons</h2>' + connections(by_document[source_id], source_id, "../../") + '</section>'
        if published[source_id]:
            body += '<section class="section"><h2>Further reading on the original website</h2>' + connections(published[source_id], source_id, "../../") + '</section>'
        page(route(source), source["title"], f'{source["kind"].capitalize()} from {source["site"]} in the Perspective Beyond atlas.', body)
    body = heading("Source index", "Sources", "Read the original material. Each source page gathers the concepts, comparisons and published reading links that point to it.")
    for site, entries in sorted(by_site.items()):
        body += f'<section class="section"><h2>{escape(site)} <small>{len(entries)}</small></h2><ul class="tiles">'
        body += "".join(card(r, "../", r["kind"].capitalize() + (" · " + r["date"] if r.get("date") else "")) for r in sorted(entries, key=lambda r: r["title"].lower()))
        body += "</ul></section>"
    page("sources/", "Sources", "A source index spanning research, articles, cases and operational material.", body)
    guide()
    reading_journeys()
    heatmap()
    map_index()
    urls = sorted(p.parent.relative_to(OUT).as_posix().strip(".") for p in OUT.rglob("index.html"))
    sitemap = "\n".join("<url><loc>" + BASE + escape(path + "/" if path else "") + "</loc></url>" for path in urls)
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sitemap + "\n</urlset>\n", encoding="utf-8")
    print(f"{len(urls)} HTML pages built")

if __name__ == "__main__":
    build()
