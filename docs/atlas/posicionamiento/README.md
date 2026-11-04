# Positioning · Atlas of thinking

A **positioning** is an entry point into the Atlas. It can be a website landing page, another source document or a specific card. From there, a combination of tags and a token budget is chosen to open a mini map.

The chosen document is the positioning. Weights, scope and tokens form its reading configuration.

**Source document → its cards → other related cards and concepts.** Each relationship retains its meaning and provenance. A document can bring together several cards: the Instituto del Totonacapan's published biography, for example, has passages and readings sharing that origin.

## Two tag combinations

1. **The card's composition.** Expresses its editorial reading profile. It can contain, for example, Business 35%, Transformation 25%, Representation 20%, Mathematics 10%, Learning 5% and Evidence 5%. It totals 100% and is editable.
2. **The positioning's combination.** Chosen by the person entering: for example, Business 50% and Mathematics 50%. This combination guides affinity with each card's proportions. A card is included only once.

Profiles are in [etiquetas-fichas.json](etiquetas-fichas.json), in the catalogue's `source_tag_weights` and in nodes' `tagWeights`. `tag_weight_overrides` retains explicit editorial compositions for the next generation. The rest is calculated through documented signals in the title, summary and linked concepts.

Cards whose catalogue contained only metadata incorporate, when available, a literal extract from the Abstract or opening paragraphs of their public source. The extract supplies the mechanism explaining the article and contributes to its thematic composition. [lecturas-fuentes.json](lecturas-fuentes.json) identifies each source's origin, section, reading time and hash. Dialogues retain their full text and explicit editorial profiles are maintained.

## Tokens and distance

The **token budget** determines the reading content entering the mini map: document header, cards and arrival relationships. **Distance** counts connections traversed from that document. Increasing tokens with the same positioning, tags and scope retains the previous selection and allows the reading to continue growing.

Blocks are counted independently with `tiktoken 0.12.0`, encoding `o200k_base`. The `budget` field records the limit, consumption, remainder and cost of the next addition. The count applies to `reading`, the downloadable reading text. The JSON also contains map data. [Tokenizer reference](https://github.com/openai/tiktoken).

`max` sets how many pieces are drawn. The downloadable reading retains every piece that entered the budget, even when some are outside the visible diagram. The map records separately what is excluded by budget and by visualisation.

## How it is calculated

- Resolve the source document and its cards. If a specific card is specified, that card is the entry to the document.
- Apply the Closed, Porous or Federated scope and the chosen tag filter.
- Thematic affinity is the sum of each positioning weight multiplied by that tag's proportion in the card. Cluster, documented perspective and concept weights are also accepted.
- Traverse existing relationships. For landing pages, incorporate reading links verified in their content, identified as navigation.
- For cards with an article extract, first retain a foundation of up to four concepts directly supported by that article. They are ordered by affinity with the document's own composition. This explains its mechanism before expanding towards the visitor's preferences.
- If an outgoing relationship of documented use exists, that foundation also includes a reading directly linked to the originating mechanism. The relationship type already recorded in the Atlas is retained.
- Order the pieces by affinity and proximity, retaining the connections needed to reach each one. Priority is `(0.25 + 0.75 × affinity) / (1 + distance)`.
- Take the prefix of that traversal that fits within the budget. The sequence is calculated independently of the budget. The next addition is stopped in full when it requires more tokens.

Conceptual relationships explain ideas. Navigation relationships open readings from a page. Both retain their type in the map.

## URL and protocol

```text
https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/?posicionamiento=D-285&tokens=2000&peso=empresa:50&peso=matematicas:50
```

Parameters: `posicionamiento`, `tokens`, repeated `peso`, `modo`, `site`, `puente`, `solo`, `red`, `sentido`, `max`, `rol`, `lectura` and `instruccion`. `centro` and `desde` continue to serve as earlier entry points. Known keys are recognised without regard to case.

[Entry for assistants](entrada.txt) · [Prepared positionings](preparados/index.html) · [Documents and their cards](documentos.json) · [Complete graph](../mapa/grafo.json).

For web readers, each document and card has a small JSON record under `documentos/` and `fichas/`. A card record contains its reading text, cost, composition and relationships to neighbouring cards. Prepared packages offer calculated readings for initial entries. The viewer calculates custom configurations and allows their reading text and map to be downloaded.

Relationships in those records also include the neighbouring card's composition, cluster and cost, allowing the next reading to be chosen without opening every candidate. Results in the [journey comparison](comparacion/README.md) document the questions, packages and responses of the blind tests.

Readers using only the web can consult [calculated configurations](configurados/index.json). Their JSON delivers `reading`, `selection` and the complete `budget` count. Positioning, budget, scope, cluster, network, direction and normalised proportions are compared; the URL's role, purpose and instruction continue to personalise the response. In Closed scope, all clusters of each node must match the selected cluster. Shared concepts are explored through a scope that permits them.

The same calculation works in Node.js:

```sh
node docs/atlas/mapa/cli.mjs "posicionamiento=D-285&tokens=2000&peso=empresa:50&peso=matematicas:50"
```

The public function is `positionMap(graph, readPosition(params, graph))` in `positioning.mjs`. The graph publishes documents, card references, compositions and token costs. To regenerate costs, install `tiktoken==0.12.0` and run `docs/atlas/mapa/build_graph.py` with the catalogue and canonical file of the edition.
