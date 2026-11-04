# The complete Atlas on the web

[Assistant entry](https://perspective-beyond-atlas.carvedgem.chatgpt.site/entrada/) · [Explore the web edition](https://perspective-beyond-atlas.carvedgem.chatgpt.site/) · [Text guide](https://perspective-beyond-atlas.carvedgem.chatgpt.site/entrada.txt)

The web edition lets readers explore the Atlas through public HTML pages, without an account or JavaScript. GitHub retains the canonical repository and change history.

The published edition reproduces the **5,155 files** of revision **7cfd1665348e7a34a6d233133f32969d8011561d**, with **76,706,211 bytes** identical to their originals. It adds HTML reading views of the 1,294 cards, 272 concepts, 1,212 documents and 11,832 relationships, together with the map's 46 navigation links.

## Reading paths

- [Cards and sources](https://perspective-beyond-atlas.carvedgem.chatgpt.site/fichas/)
- [Concepts](https://perspective-beyond-atlas.carvedgem.chatgpt.site/conceptos/)
- [Relationships](https://perspective-beyond-atlas.carvedgem.chatgpt.site/relaciones/)
- [Clusters](https://perspective-beyond-atlas.carvedgem.chatgpt.site/clusters/)
- [Tags](https://perspective-beyond-atlas.carvedgem.chatgpt.site/etiquetas/)
- [Documents](https://perspective-beyond-atlas.carvedgem.chatgpt.site/documentos/)
- [All files](https://perspective-beyond-atlas.carvedgem.chatgpt.site/archivos/)
- [Edition and provenance](https://perspective-beyond-atlas.carvedgem.chatgpt.site/edicion/)

Every card has its reading content, composition, provenance and connections. Relationships can be followed in both directions. The original edition's JSON files, texts, scripts and resources remain available under /perspective-beyond/ on the same server. External originals retain their references.

## Regenerating an edition

The generators read repository objects and produce the web publication. From this folder:

~~~text
python build_web.py REPOSITORY_PATH FULL_REVISION PUBLIC_ORIGIN
python check_web.py
~~~

dist/edicion/archivos.json retains the size and SHA-256 of every canonical file. Verification checks every card's pages, internal links and anchors, and the reproduced files' hashes. The process generates a web publication; it does not create project backups.

[Publication metadata](publication.json).

The empty GitHub Pages control file retains its content and is served through the text path indicated in the file inventory.

<a id="orientación-antes-del-posicionamiento"></a>

## Orientation before positioning

[Understand the Atlas](https://tegrity.ai/atlas-orientation/) · [Upper-level map](https://perspective-beyond-atlas.carvedgem.chatgpt.site/orientacion/) · [Assistant summary](https://perspective-beyond-atlas.carvedgem.chatgpt.site/orientacion/lectura.txt)

Seven areas group the existing topics; 36 directed bridges summarise their recorded relationships. The 1,566 cards and concepts retain their identity and may participate in several areas. Eleven question-based routes suggest two or three specific entry points before asking a new visitor for a cluster, weights and scope. Configurations already set by the reader or their URL are retained.

`orientation.py` generates this layer when `build_web.py` finishes. `check_orientation.py` checks coverage, correspondences, relationships, entry diversity and configuration continuity. The complete model retains each piece's membership and the identifiers of the grouped relationships. The original graph remains intact.

## Direct reading on Tegrity.AI

[Stable entry](https://tegrity.ai/atlas-reader/) · [Text source](https://tegrity.ai/wp-content/uploads/2026/11/atlas-8733a98c-entrada.txt)

This edition lets readers explore the 1,566 original pieces and 11,832 relationships independently of delivery from the chatgpt.site domain. Ten cluster indexes, pagination, a locator and card and relationship files are served as public text on the organisation's own domain. It retains the 46 navigation links, 1,212 documents and every record's fields. The inventory publishes the URLs and SHA-256 hashes of the 127 files.

After generating the web edition, run `python build_direct_reader.py` and `python build_direct_reader_page.py`. The resulting reading files are published at the origin declared by the generator; check the URLs and hashes after publication. Do not change cards or relationships to adapt transport.
