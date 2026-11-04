# Sources for assistants · Perspective Beyond

**One source of thinking. Many ways to create.**

[Open the product](https://dakleyer.github.io/perspective-beyond/atlas/asistentes/) · [Read an example source](https://dakleyer.github.io/perspective-beyond/atlas/asistentes/ejemplos/arquitectura-y-lenguajes.txt) · [Prepare another selection](https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/)

The Atlas has a website for people to explore and reading sources prepared for assistants. Each source is a small, self-contained file: it brings together an entry point, its texts, a selection of explained relationships, references and the working configuration.

The assistant can receive a single URL or the downloaded file. From that content, it can explain the thinking, hold a conversation, create a website, develop a document, or prepare and produce audio and video with the tools available to it. The format changes; the original thinking and its provenance are retained.

## Try it

1. Open one of the text sources listed below.
2. Copy its URL and give it to your assistant.
3. Request the result: for example, “Explain this thinking through a concrete case”, “Create a website from this source” or “Prepare a three-minute audio”.

You can also download the file and open it in a text editor. Its content is in UTF-8 and can be transported, reviewed and adapted like a normal document.

| Source | Text entry for the assistant | Readable page |
| --- | --- | --- |
| Thinking across languages and crafts | [Source](ejemplos/arquitectura-y-lenguajes.txt) | [Read](ejemplos/arquitectura-y-lenguajes.html) |
| Preserving the capability that makes things work | [Source](ejemplos/conocimiento-tacito.txt) | [Read](ejemplos/conocimiento-tacito.html) |
| Observing the structure that supports a decision | [Source](ejemplos/integridad-estructural.txt) | [Read](ejemplos/integridad-estructural.html) |
| From a business intention to an operational capability | [Source](ejemplos/valor-y-ejecucion.txt) | [Read](ejemplos/valor-y-ejecucion.html) |

The output format can be changed during the conversation while retaining the same source. To change the cards, weights or scope, export a new selection.

## What the file contains

- **Instructions for use:** role, purpose, initial format and custom instruction.
- **Positioning:** entry document or card, scope and combination of tags.
- **Thinking and texts:** content of the selected cards and concepts, with their thematic compositions.
- **Relationships:** the mechanism connecting the pieces, its direction and provenance. Cross-connections in the mini map are also included, up to eight in addition to its arrival paths.
- **Sources and edition:** links to originals, recorded passages and the map revision used.
- **Continuation:** a link to reopen the configuration and create another reading.

The included selection can be read and used without downloading the graph or opening additional files. The originals remain linked for going deeper, checking a passage or extending the research.

## Prepare your own source

In [Positioning](https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/):

1. Choose the entry document, card or URL.
2. Adjust the tags, scope and reading tokens.
3. Open the mini map.
4. Select Conversation, Web page, Audio, Video or Document.
5. Click **Download source for my assistant**.

The role, purpose and custom instruction of a configured URL are retained in the source. Percentages are those of the positioning and its cards. The Closed, Porous or Federated scope is applied before preparing the file.

The source is specific: it carries the calculated selection, with the context needed to work on it. The original reading retains its token count; instructions, references and additional relationships also take space in the final file. The [example index](ejemplos/index.json) records size, hash and selection; the [tests](pruebas.json) record the total count of the examples with the reference tokenizer.

## Working formats

- **Conversation:** understand, explain and relate ideas.
- **Web:** a complete HTML page adaptable to mobile, with explanation and references.
- **Audio:** spoken text and production through the assistant's voice tool.
- **Video:** script, scenes, narration and production through its audiovisual tools.
- **Document:** exposition, proposal or application to a new case.

For a voice guided by a person or institution, the source retains the documented vocabulary and ways of reasoning and attributes ideas by name. Each new application is presented as a development of that thinking.

## Integration and regeneration

The format is implemented in [source.mjs](source.mjs). It uses the result of the positioning calculation:

~~~javascript
import {readPosition, positionMap} from '../positioning.mjs';
import {assistantSource, sourceHTML} from './source.mjs';

const result = positionMap(graph, readPosition(params, graph));
const source = assistantSource(result, graph, {format: 'web'});
// source.text is the self-contained Markdown / UTF-8 text file.
const html = sourceHTML(source);
~~~

The HTML also carries the texts, relationships and instructions inside the document itself. Example pages include their styling in the file and can be read without JavaScript.

To regenerate the examples from the same map:

~~~text
node docs/atlas/asistentes/build.mjs SOURCE_GIT_REVISION
node docs/atlas/asistentes/pruebas.mjs
~~~

The revision must be the public commit containing the graph used. The generator writes derivatives under this folder. The Atlas cards, concepts, relationships and compositions are read and remain intact.
