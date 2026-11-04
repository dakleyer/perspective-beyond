# Relationship-radius maps · Perspective Beyond

[Open the viewer](https://dakleyer.github.io/perspective-beyond/atlas/mapa/) · [View an embedded map](https://dakleyer.github.io/perspective-beyond/atlas/mapa/ejemplo.html) · [Read the complete graph](https://dakleyer.github.io/perspective-beyond/atlas/mapa/grafo.json)

A radius map selects a neighbourhood around a card, concept or source URL. The browser and bot tool run the same calculation. Every node in the complete graph carries its thematic tags and clusters. Documents use the catalogue's tags. A concept inherits the tags present in at least half of its supporting cards. If none reaches that threshold, it falls under Research and technical documentation.

## URL parameters

| Parameter | Meaning | Default value |
| --- | --- | --- |
| `centro` | ID, card URL or original URL. Published edition aliases are also valid. | `T1499` |
| `radio` | Maximum number of relationships traversed from the centre. Accepts 0 to 4. | `2` |
| `max` | Nodes that may appear, including the centre. Accepts 1 to 60. | `16` |
| `red` | `documentos` traverses documentary relationships. `ideas` also includes concepts, conceptual relationships and supporting links between documents and concepts. | `documentos` |
| `sentido` | `ambas`, `salientes` or `entrantes`. Controls traversal. Arrows retain the recorded direction of the relationship. | `ambas` |
| `peso` | Repeatable. Use `tag:weight`, for example `matematicas:0.5` and `empresa:0.3`. Also accepts the `tema:` prefix and a decimal comma. | No weighting |
| `solo` | With `1`, traversal passes only through nodes sharing a selected tag. The centre remains visible. | Disabled |
| `embed` | With `1`, displays the map and its reading panel in an embeddable format. | Disabled |

Tag keys are in `topics` in `grafo.json` and in the [tag index](https://dakleyer.github.io/perspective-beyond/atlas/enfoques.txt). If a URL identifies several cards, the viewer indicates their IDs so the correct one can be selected. It retains the fragments and parameters of the original URL that identify content.

## Reproducible calculation

1. Resolve the central node and select the layers and traversal direction. A breadth-first search measures minimum distance, one hop per relationship. The centre has distance zero.
2. Divide each weight by the sum. A node's affinity is the sum of the normalised weights of the tags it carries. For example, 0.5 and 0.3 become 62.5% and 37.5%.
3. Sort candidates by `(0.25 + 0.75 × affinity) / (1 + distance)`. Without weights, use `1 / (1 + distance)`. Break ties by distance and ID. When choosing a card, retain its path to the centre if it fits within the limit. For paths of equal length, traversal visits neighbours with greater affinity first and breaks ties by node and relationship ID.
4. Return the nodes, their distance and path, the relationships between visible nodes, and counts of reachable, visible and omitted nodes by ring. `route: true` distinguishes links supporting the path to the centre from additional crossings. Priority expresses proximity and affinity within the corpus. Its interpretation depends on each relationship's type, text and provenance.

## Generate a map from a bot

Run with Node.js from the repository root.

```sh
node docs/atlas/mapa/cli.mjs "centro=GH049&radio=2&max=16&red=ideas&peso=matematicas:0.5&peso=empresa:0.3" > mapa.json
```

You can also pass the full URL as the first argument. To calculate with another edition, add the path to its `grafo.json` as the second argument. The `perspective-beyond/radius-v1` output includes `request`, `dataset`, `center`, `layers`, `nodes` and `edges`. Nodes include the card URL, the original when available, tags, distance, affinity and traversal relationship. Links retain type, direction, explanation and evidence when recorded. `dataset` contains the hashes of the two source catalogues. To repeat a result after an update, use `grafo.json` from that edition's GitHub commit.

The `perspective-beyond/graph-v1` format contains `nodes` and `edges`. `edgeFields` declares the field order of each relationship. A relationship ID retains its original ID with a layer prefix, such as `documento:D001` or `concepto:D001`. The generator checks that every relationship points to existing nodes and every tag is in the register.

## Embed in a website

In the viewer, calculate the map and click **Copy embed code**, or use the URL directly with `embed=1`.

```html
<iframe
  src="https://dakleyer.github.io/perspective-beyond/atlas/mapa/?centro=GH049&amp;radio=2&amp;red=ideas&amp;peso=matematicas%3A0.5&amp;peso=empresa%3A0.3&amp;embed=1"
  title="Relationship map for card A23"
  loading="lazy"
  style="width:100%;height:720px;border:0"></iframe>
```

The host page can share the URL, embed HTML or resulting JSON. The map is recalculated with the published graph when opened. Rings show the hops, and the reading panel allows each card and its source to be opened.

The [calculated JSON example](https://raw.githubusercontent.com/dakleyer/perspective-beyond/main/docs/atlas/mapa/ejemplos/structural-awareness.json) allows the same selection to be checked with a text reader. For another map, download its JSON from the viewer or use the CLI.

## Update the graph

After updating `docs/data/atlas.json` and `docs/atlas/global-catalog.json`, run:

```sh
python docs/atlas/mapa/build_graph.py
```

The generator validates that both inputs belong to the same edition. Publish the new `grafo.json` in the same commit as the Atlas sources so shared URLs continue to resolve against a coherent edition.
