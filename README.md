# Perspective Beyond

[Open the interactive atlas](https://dakleyer.github.io/perspective-beyond/) · [Read the guide](https://dakleyer.github.io/perspective-beyond/guide/) · [Browse the sources](https://dakleyer.github.io/perspective-beyond/sources/)

Perspective Beyond connects the concepts, research, interventions and field cases that inform an architectural approach to action under incomplete evidence. Start with the guide or enter through a concept, case or source. Each relationship has a type, and its source or operating conditions appear where recorded.

## Generate a relationship-radius map

[Open the radius viewer](https://dakleyer.github.io/perspective-beyond/atlas/mapa/) | [See an embedded example](https://dakleyer.github.io/perspective-beyond/atlas/mapa/ejemplo.html) | [Read the URL protocol and CLI](docs/atlas/mapa/README.md)

Start from an Atlas card, a concept, or a source URL. Choose how many relationship hops to follow and weight the topics that matter to the reading. The same calculation produces the interactive map and machine-readable JSON.

## Edit the atlas

- `narrative/guide.md` holds the long-form reading guide. Link concept and source IDs using double brackets.
- `data/concepts.json` and `data/sources.json` hold definitions and original source references.
- `data/relations.json` records conceptual edges. `data/document-relations.json` records comparative readings and `data/reading-links.json` records recommendations published on source sites.
- `data/article-maps.json` records the concepts and close readings in each article map.
- `site/assets/` holds the atlas interface and Cytoscape.js, bundled with its license.
- Run `python build.py` with Python 3.10 or later, then commit the regenerated `docs/` files. GitHub Pages publishes from `main:/docs`.

GitHub research links preserve the commit referenced by the edition or source record. The edition metadata is in `data/edition.json`.
