# Perspective Beyond

[Mind Atlas · lectura web completa](https://integralmanagement.ch/atlas-reader/) · [Entrada autónoma para asistentes](https://integralmanagement.ch/atlas-reader/entrada.txt)


[Conecta tu asistente al Atlas · lectura directa](https://tegrity.ai/atlas-reader/)

[Open the interactive atlas](https://dakleyer.github.io/perspective-beyond/) · [Read the guide](https://dakleyer.github.io/perspective-beyond/guide/) · [Browse the sources](https://dakleyer.github.io/perspective-beyond/sources/)

Perspective Beyond connects the concepts, research, interventions and field cases that inform an architectural approach to action under incomplete evidence. Start with the guide or enter through a concept, case or source. Each relationship has a type, and its source or operating conditions appear where recorded.

## Generate a relationship-radius map

[Open the radius viewer](https://dakleyer.github.io/perspective-beyond/atlas/mapa/) | [See an embedded example](https://dakleyer.github.io/perspective-beyond/atlas/mapa/ejemplo.html) | [Read the URL protocol and CLI](docs/atlas/mapa/README.md)

Start from an Atlas card, a concept, or a source URL. Choose how many relationship hops to follow and weight the topics that matter to the reading. The same calculation produces the interactive map and machine-readable JSON.

## Connect an assistant through a versioned entry

[Browse entry points and QR codes](https://dakleyer.github.io/perspective-beyond/atlas/i/) | [Read the instance and integration protocol](docs/atlas/i/README.md)

Each entry carries a configuration for the same Atlas. Published configurations have a versioned URL and a plain-text entry for assistants.

## Posicionamiento y mini mapas

Un posicionamiento es un documento de entrada, como la landing de una web. El documento tiene fichas; las fichas tienen composiciones porcentuales de etiquetas y relaciones con otras fichas y conceptos. La combinación del visitante y un presupuesto de tokens abren un mini mapa cuya lectura crece al ampliar ese presupuesto.

[Abrir un posicionamiento](https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/) · [Protocolo y modelo](docs/atlas/posicionamiento/README.md) · [Paquetes preparados](https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/preparados/) · [Datos y porcentajes](docs/atlas/posicionamiento/etiquetas-fichas.json).

El cálculo público está en `docs/atlas/positioning.mjs`. La CLI admite `posicionamiento`, `tokens` y pesos de etiquetas. El grafo conserva el documento de origen de cada ficha y los costes de lectura calculados con `o200k_base`.

## Edit the atlas

- `narrative/guide.md` holds the long-form reading guide. Link concept and source IDs using double brackets.
- `data/concepts.json` and `data/sources.json` hold definitions and original source references.
- `data/relations.json` records conceptual edges. `data/document-relations.json` records comparative readings and `data/reading-links.json` records recommendations published on source sites.
- `data/article-maps.json` records the concepts and close readings in each article map.
- `site/assets/` holds the atlas interface and Cytoscape.js, bundled with its license.
- Run `python build.py` with Python 3.10 or later, then commit the regenerated `docs/` files. GitHub Pages publishes from `main:/docs`.

GitHub research links preserve the commit referenced by the edition or source record. The edition metadata is in `data/edition.json`.

## Revisar la conservación y los enlaces

[Revisión histórica y de navegación · 4 de noviembre de 2026](docs/atlas/mapa/REVISION-20261104-2.md)

Desde un clon del repositorio, `node tools/check-atlas-history.mjs` comprueba las fichas, relaciones y asociaciones de todas las ediciones anteriores. `node tools/check-atlas-history.mjs --self-test` ejecuta sus siete controles. `python tools/check-atlas-links.py` revisa los archivos y anclas de los enlaces internos publicados. Ambos leen los objetos de Git sin escribir copias del contenido.

## Fuentes autocontenidas para asistentes

[Abrir el producto](https://dakleyer.github.io/perspective-beyond/atlas/asistentes/) · [README del producto](docs/atlas/asistentes/README.md) · [Probar una fuente de texto](https://dakleyer.github.io/perspective-beyond/atlas/asistentes/ejemplos/arquitectura-y-lenguajes.txt)

Un archivo compacto reúne textos, relaciones, referencias y configuración de una selección del Atlas. El asistente del lector puede conversar sobre ese pensamiento o darle forma de web, audio, vídeo o documento. Cada mini mapa permite descargar su propia fuente autocontenida.

## Edición web completa

[Entrada para asistentes](https://perspective-beyond-atlas.carvedgem.chatgpt.site/entrada/) · [Atlas completo en HTML](https://perspective-beyond-atlas.carvedgem.chatgpt.site/) · [Reproducción y procedencia](web-edition/README.md)

La edición web reproduce todos los archivos públicos del Atlas y añade páginas HTML enlazadas para leer fichas, conceptos, documentos y relaciones. GitHub conserva la fuente canónica.

## Comprender el Atlas antes de elegir dónde entrar

[Atlas Orientation](https://tegrity.ai/atlas-orientation/) reúne las grandes preguntas del corpus y propone puntos de entrada concretos. [Modelo y protocolo](web-edition/README.md#orientación-antes-del-posicionamiento).

## Fase actual: complemento de navegación y comprensión web

En esta fase, el Atlas complementa la navegación y la comprensión de las webs. Cada página es un punto de entrada a sus fichas, conceptos, casos y fuentes; conserva la URL de origen y permite profundizar, relacionar ideas y volver al texto original. La prueba compara estos recorridos dirigidos con la navegación web convencional mediante tokens consumidos, pertinencia de las fuentes y comprensión del corpus.

[Contrato, integración y protocolo de prueba](docs/atlas/web-navigation.md).
