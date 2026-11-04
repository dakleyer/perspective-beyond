"""Build the versioned public graph used by the radius viewer and CLI."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit


ATLAS = "https://dakleyer.github.io/perspective-beyond/atlas/"


def build(canonical_bytes, catalog_bytes):
    canonical = json.loads(canonical_bytes)
    catalog = json.loads(catalog_bytes)
    assert sha256(canonical_bytes).hexdigest() == catalog["canonical_sha256"], "Atlas editions do not match"
    topics = catalog["topics"]
    notes = catalog["editorial_cards"]
    source_tags = catalog["source_tags"]
    membership = catalog["source_cluster"]
    nodes, edges = [], []
    for source in canonical["sources"] + catalog["sources"]:
        sid = source["id"]
        note = notes.get(sid, {})
        provenance = note.get("provenance", {})
        page = note.get("url") or "../sources/" + source["slug"] + "/"
        aliases = [provenance.get("url")] + [variant["url"] for variant in note.get("variants", [])]
        github = re.fullmatch(r"https://github\.com/([^/]+/[^/]+)/blob/([0-9a-f]{40})/([^?#]+)(?:[?#].*)?",
                              provenance.get("url") or source["url"])
        commit = github[2] if github else None
        nodes.append({
            "id": sid, "type": "ficha", "title": note.get("title", source["title"]),
            "url": urljoin(ATLAS, page), "original": source["url"],
            "aliases": sorted(set(url for url in aliases if url and url != source["url"])),
            "clusters": [membership[sid]], "tags": source_tags[sid],
            "summary": note.get("summary", ""),
            "commit": commit, "sourcePath": provenance.get("path") or (github[3] if github else None),
            "commitUrl": f"https://github.com/{github[1]}/commit/{commit}" if github else None,
        })
    for concept in canonical["concepts"] + catalog["concepts"]:
        sid = concept["id"]
        refs = list(dict.fromkeys(concept["sources"]))
        assert all(ref in membership for ref in refs), sid
        # A concept inherits tags supported by at least half of its sources.
        supported = [tag for tag in topics if refs and
                     sum(tag in source_tags[ref] for ref in refs) * 2 >= len(refs)]
        nodes.append({
            "id": sid, "type": "concepto", "title": concept.get("original_label") or concept["label"],
            "url": urljoin(ATLAS, concept.get("url") or "../concepts/" + concept["slug"] + "/"),
            "original": None, "aliases": [], "clusters": sorted({membership[ref] for ref in refs}),
            "tags": supported or ["documentacion"],
            "summary": concept["definition"], "commit": None, "sourcePath": None, "commitUrl": None,
        })
        for ref in refs:
            edges.append([f"apoyo:{ref}:{sid}", ref, sid, "documenta el concepto",
                          "", None, "apoyo", ""])
    for layer, records in (
        ("documento", canonical["documentRelations"] + catalog["relations"]),
        ("concepto", canonical["relations"] + catalog["concept_relations"]),
    ):
        for edge in records:
            condition = edge.get("condition_es") or edge.get("boundary_es") or ""
            edges.append([f"{layer}:{edge['id']}", edge["from"], edge["to"], edge["kind"],
                          edge.get("reading") or edge.get("relation_es") or "",
                          edge.get("evidence"), layer, condition])
    ids = {node["id"] for node in nodes}
    assert len(ids) == len(nodes) and len({edge[0] for edge in edges}) == len(edges)
    assert all(edge[1] in ids and edge[2] in ids for edge in edges)
    assert all(node["tags"] and set(node["tags"]) <= topics.keys() for node in nodes)
    assert all(urlsplit(node["url"]).scheme == "https" for node in nodes)
    return {
        "schema": "perspective-beyond/graph-v1",
        "edition": catalog["edition"],
        "canonicalSha256": sha256(canonical_bytes).hexdigest(),
        "catalogSha256": sha256(catalog_bytes).hexdigest(),
        "topics": {key: entry["label"] for key, entry in topics.items()},
        "clusters": {key: value[0] for key, value in catalog["clusters"].items()},
        "nodes": nodes,
        "edgeFields": ["id", "from", "to", "kind", "reading", "evidence", "layer", "condition"],
        "edges": edges,
    }


def write_graph(output, canonical_bytes, catalog_bytes):
    graph = build(canonical_bytes, catalog_bytes)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8", newline="\n")
    return graph


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical", type=Path, default=here.parent.parent / "data/atlas.json")
    parser.add_argument("--catalog", type=Path, default=here.parent / "global-catalog.json")
    parser.add_argument("--output", type=Path, default=here / "grafo.json")
    args = parser.parse_args()
    graph = write_graph(args.output, args.canonical.read_bytes(), args.catalog.read_bytes())
    print(f"{len(graph['nodes'])} nodes, {len(graph['edges'])} edges, {len(graph['topics'])} topics")
