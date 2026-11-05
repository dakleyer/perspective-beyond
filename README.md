# Perspective Beyond

[Mind Atlas · complete web reader](https://integralmanagement.ch/atlas-reader/) · [Autonomous entry for assistants](https://integralmanagement.ch/atlas-reader/entrada.txt)

[Connect your assistant to the Atlas · direct reading](https://tegrity.ai/atlas-reader/)

[Open the interactive atlas](https://dakleyer.github.io/perspective-beyond/) · [Read the guide](https://dakleyer.github.io/perspective-beyond/guide/) · [Browse the sources](https://dakleyer.github.io/perspective-beyond/sources/)

Perspective Beyond connects the concepts, research, interventions and field cases that inform an architectural approach to action under incomplete evidence. Start with the guide or enter through a concept, case or source. Each relationship has a type, and its source or operating conditions appear where recorded.

## Generate a relationship-radius map

[Open the radius viewer](https://dakleyer.github.io/perspective-beyond/atlas/mapa/) | [See an embedded example](https://dakleyer.github.io/perspective-beyond/atlas/mapa/ejemplo.html) | [Read the URL protocol and CLI](docs/atlas/mapa/README.md)

Start from an Atlas card, a concept, or a source URL. Choose how many relationship hops to follow and weight the topics that matter to the reading. The same calculation produces the interactive map and machine-readable JSON.

## Connect an assistant through a versioned entry

[Browse entry points and QR codes](https://dakleyer.github.io/perspective-beyond/atlas/i/) | [Read the instance and integration protocol](docs/atlas/i/README.md)

Each entry carries a configuration for the same Atlas. Published configurations have a versioned URL and a plain-text entry for assistants.

## Positioning and mini maps

A positioning is an entry document, such as a website landing page. The document has cards; the cards have percentage compositions of tags and relationships with other cards and concepts. The visitor's combination and a token budget open a mini map whose reading expands as that budget increases.

[Open a positioning](https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/) · [Protocol and model](docs/atlas/posicionamiento/README.md) · [Prepared packages](https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/preparados/) · [Data and percentages](docs/atlas/posicionamiento/etiquetas-fichas.json).

The public calculation is in `docs/atlas/positioning.mjs`. The CLI accepts `posicionamiento`, `tokens` and tag weights. The graph retains the source document of each card and the reading costs calculated with `o200k_base`.

## Edit the atlas

- `narrative/guide.md` holds the long-form reading guide. Link concept and source IDs using double brackets.
- `data/concepts.json` and `data/sources.json` hold definitions and original source references.
- `data/relations.json` records conceptual edges. `data/document-relations.json` records comparative readings and `data/reading-links.json` records recommendations published on source sites.
- `data/article-maps.json` records the concepts and close readings in each article map.
- `site/assets/` holds the atlas interface and Cytoscape.js, bundled with its license.
- Run `python build.py` with Python 3.10 or later, then commit the regenerated `docs/` files. GitHub Pages publishes from `main:/docs`.

GitHub research links preserve the commit referenced by the edition or source record. The edition metadata is in `data/edition.json`.

## Check preservation and links

[Historical and navigation review · 4 November 2026](docs/atlas/mapa/REVISION-20261104-2.md)

From a repository clone, `node tools/check-atlas-history.mjs` checks the cards, relationships and associations of all previous editions. `node tools/check-atlas-history.mjs --self-test` runs its seven checks. `python tools/check-atlas-links.py` checks the files and anchors of published internal links. Both read Git objects without writing copies of their content.

## Self-contained sources for assistants

[Open the product](https://dakleyer.github.io/perspective-beyond/atlas/asistentes/) · [Product README](docs/atlas/asistentes/README.md) · [Try a text source](https://dakleyer.github.io/perspective-beyond/atlas/asistentes/ejemplos/arquitectura-y-lenguajes.txt)

A compact file brings together texts, relationships, references and the configuration of an Atlas selection. The reader's assistant can discuss that thinking or give it the form of a website, audio, video or document. Each mini map allows its own self-contained source to be downloaded.

## Complete web edition

[Entry for assistants](https://perspective-beyond-atlas.carvedgem.chatgpt.site/entrada/) · [Complete Atlas in HTML](https://perspective-beyond-atlas.carvedgem.chatgpt.site/) · [Reproduction and provenance](web-edition/README.md)

The web edition reproduces every public Atlas file and adds linked HTML pages for reading cards, concepts, documents and relationships. GitHub retains the canonical source.

## Understand the Atlas before choosing where to enter

[Atlas Orientation](https://tegrity.ai/atlas-orientation/) brings together the corpus's major questions and proposes concrete entry points. [Model and protocol](web-edition/README.md#orientación-antes-del-posicionamiento).

## Current phase: a companion to web navigation and understanding

In this phase, the Atlas complements website navigation and understanding. Each page is an entry point to its cards, concepts, cases and sources; it retains the source URL and allows readers to go deeper, connect ideas and return to the original text. The test compares these guided journeys with conventional web navigation through tokens consumed, source relevance and understanding of the corpus.

[Contract, integration and test protocol](docs/atlas/web-navigation.md).

## Iterative source review and node discovery

[Read the source-review method](methodology/iterative-source-review.md) · [Run the implementation example](methodology/examples/source-review-cycle.json)

Return to identified source revisions, compare their arguments with existing cards, enrich incomplete explanations and develop missing nodes and specific relationships. The method records covered ideas, new facets, source decisions and preservation checks for each incremental cycle.
