# Fuentes para asistentes · Perspective Beyond

**Una fuente de pensamiento. Muchas formas de crear.**

[Abrir el producto](https://dakleyer.github.io/perspective-beyond/atlas/asistentes/) · [Leer una fuente de ejemplo](https://dakleyer.github.io/perspective-beyond/atlas/asistentes/ejemplos/arquitectura-y-lenguajes.txt) · [Preparar otra selección](https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/)

El Atlas tiene una web para explorar como persona y fuentes de lectura preparadas para asistentes. Cada fuente es un archivo pequeño y autocontenido: reúne un punto de entrada, sus textos, una selección de relaciones explicadas, las referencias y la configuración de trabajo.

El asistente puede recibir una sola URL o el archivo descargado. Desde ese contenido puede explicar el pensamiento, mantener una conversación, crear una web, desarrollar un documento o preparar y producir audio y vídeo con las herramientas que tenga disponibles. El formato cambia; el pensamiento de origen y su procedencia se conservan.

## Probarlo

1. Abre una de las fuentes de texto que aparecen abajo.
2. Copia su URL y entrégasela a tu asistente.
3. Pide el resultado: por ejemplo, «Explícame este pensamiento con un caso concreto», «Crea una web con esta fuente» o «Prepara un audio de tres minutos».

También puedes descargar el archivo y abrirlo en un editor de texto. Su contenido está en UTF-8 y se puede transportar, revisar y adaptar como un documento normal.

| Fuente | Entrada de texto para el asistente | Página legible |
| --- | --- | --- |
| Pensar entre lenguajes y oficios | [Fuente](ejemplos/arquitectura-y-lenguajes.txt) | [Leer](ejemplos/arquitectura-y-lenguajes.html) |
| Conservar la capacidad que hace funcionar las cosas | [Fuente](ejemplos/conocimiento-tacito.txt) | [Leer](ejemplos/conocimiento-tacito.html) |
| Observar la estructura que sostiene una decisión | [Fuente](ejemplos/integridad-estructural.txt) | [Leer](ejemplos/integridad-estructural.html) |
| De una intención empresarial a una capacidad operativa | [Fuente](ejemplos/valor-y-ejecucion.txt) | [Leer](ejemplos/valor-y-ejecucion.html) |

En la conversación se puede cambiar el formato de salida conservando la misma fuente. Para cambiar las fichas, los pesos o el alcance, se exporta una nueva selección.

## Qué contiene el archivo

- **Indicaciones de uso:** rol, propósito, formato inicial e instrucción personalizada.
- **Posicionamiento:** documento o ficha de entrada, alcance y combinación de etiquetas.
- **Pensamiento y textos:** contenido de las fichas y conceptos seleccionados, con sus composiciones temáticas.
- **Relaciones:** el mecanismo que conecta las piezas, su dirección y su procedencia. Se incluyen también conexiones cruzadas del mini mapa, hasta ocho adicionales a sus recorridos de llegada.
- **Fuentes y edición:** enlaces a los originales, pasajes registrados y revisión del mapa utilizada.
- **Continuación:** enlace para reabrir la configuración y crear otra lectura.

La selección incluida se puede leer y utilizar sin descargar el grafo ni abrir archivos adicionales. Los originales quedan enlazados para profundizar, comprobar un pasaje o ampliar la investigación.

## Preparar una fuente propia

En [Posicionamiento](https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/):

1. Elige el documento, la ficha o la URL de entrada.
2. Ajusta las etiquetas, el alcance y los tokens de lectura.
3. Abre el mini mapa.
4. Selecciona Conversación, Página web, Audio, Vídeo o Documento.
5. Pulsa **Descargar fuente para mi asistente**.

El rol, propósito e instrucción personalizada de una URL configurada se conservan en la fuente. Los porcentajes son los del posicionamiento y de sus fichas. El alcance Cerrado, Poroso o Federado se aplica antes de preparar el archivo.

La fuente es concreta: lleva la selección que se ha calculado, con el contexto necesario para trabajar sobre ella. La lectura de origen mantiene su cuenta de tokens; las instrucciones, referencias y relaciones adicionales ocupan también espacio en el archivo final. El [índice de ejemplos](ejemplos/index.json) registra tamaño, huella y selección; las [pruebas](pruebas.json) recogen la cuenta total de los ejemplos con el tokenizador de referencia.

## Formatos de trabajo

- **Conversación:** comprender, explicar y relacionar las ideas.
- **Web:** una página HTML completa y adaptable a móvil, con explicación y referencias.
- **Audio:** texto hablado y producción mediante la herramienta de voz del asistente.
- **Vídeo:** guion, escenas, narración y producción mediante sus herramientas audiovisuales.
- **Documento:** exposición, propuesta o aplicación a un caso nuevo.

Para una voz guiada por una persona o institución, la fuente conserva el vocabulario y las formas de razonar que están documentados y atribuye las ideas por su nombre. Cada aplicación nueva se presenta como una elaboración sobre ese pensamiento.

## Integración y regeneración

El formato está implementado en [source.mjs](source.mjs). Utiliza el resultado del cálculo de posicionamiento:

~~~javascript
import {readPosition, positionMap} from '../positioning.mjs';
import {assistantSource, sourceHTML} from './source.mjs';

const result = positionMap(graph, readPosition(params, graph));
const source = assistantSource(result, graph, {format: 'web'});
// source.text es el archivo autocontenido en Markdown / texto UTF-8.
const html = sourceHTML(source);
~~~

El HTML también lleva los textos, relaciones e indicaciones dentro del propio documento. Las páginas de ejemplo incluyen su estilo en el archivo y se pueden leer sin JavaScript.

Para regenerar los ejemplos desde el mismo mapa:

~~~text
node docs/atlas/asistentes/build.mjs REVISION_GIT_DE_ORIGEN
node docs/atlas/asistentes/pruebas.mjs
~~~

La revisión debe ser el commit público que contiene el grafo utilizado. El generador escribe derivados bajo esta carpeta. Las fichas, conceptos, relaciones y composiciones del Atlas se leen y permanecen intactos.

