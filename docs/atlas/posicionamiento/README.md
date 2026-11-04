# Posicionamiento · Atlas de pensamiento

Un **posicionamiento** es un punto de entrada al Atlas. Puede ser la landing de una web, otro documento de origen o una ficha concreta. Desde ahí se elige una combinación de etiquetas y un presupuesto de tokens para abrir un mini mapa.

El documento elegido es el posicionamiento. Los pesos, el alcance y los tokens forman su configuración de lectura.

**Documento de origen → sus fichas → otras fichas y conceptos relacionados.** Cada relación conserva su significado y su procedencia. El documento puede reunir varias fichas: la biografía publicada del Instituto del Totonacapan, por ejemplo, tiene pasajes y lecturas que comparten ese origen.

## Dos combinaciones de etiquetas

1. **La composición de la ficha.** Expresa su perfil editorial de lectura. Puede contener, por ejemplo, Empresa 35 %, Transformación 25 %, Representación 20 %, Matemáticas 10 %, Aprendizaje 5 % y Evidencia 5 %. Suma 100 % y es editable.
2. **La combinación del posicionamiento.** La elige quien entra: por ejemplo, Empresa 50 % y Matemáticas 50 %. Esa combinación orienta la afinidad con las proporciones de cada ficha. Una ficha se incorpora una sola vez.

Los perfiles están en [etiquetas-fichas.json](etiquetas-fichas.json), en `source_tag_weights` del catálogo y en `tagWeights` de los nodos. `tag_weight_overrides` conserva las composiciones editoriales explícitas para la siguiente generación. El resto se calcula mediante señales documentadas en título, resumen y conceptos vinculados.

Las fichas cuyo catálogo contenía solo metadatos incorporan, cuando está disponible, un extracto literal del Abstract o de los párrafos iniciales de su fuente pública. El extracto aporta el mecanismo que explica el artículo y participa en su composición temática. [lecturas-fuentes.json](lecturas-fuentes.json) identifica el origen, la sección, el momento de lectura y la huella de cada fuente. Los diálogos conservan su texto completo y los perfiles editoriales explícitos se mantienen.

## Tokens y distancia

El **presupuesto de tokens** determina el contenido de lectura que entra en el mini mapa: cabecera del documento, fichas y relaciones de llegada. La **distancia** cuenta conexiones recorridas desde ese documento. Al aumentar los tokens con el mismo posicionamiento, etiquetas y alcance, la selección anterior se conserva y la lectura puede seguir creciendo.

Los bloques se cuentan de forma independiente con `tiktoken 0.12.0`, codificación `o200k_base`. El campo `budget` registra límite, consumo, resto y coste de la siguiente incorporación. La cuenta se aplica al texto `reading`, que es la lectura descargable. El JSON contiene además los datos del mapa. [Referencia del tokenizador](https://github.com/openai/tiktoken).

`max` establece cuántas piezas se dibujan. La lectura descargable conserva todas las piezas que entraron en el presupuesto, aunque algunas queden fuera del diagrama visible. El mapa registra por separado lo que queda fuera por presupuesto y por visualización.

## Cómo se calcula

- Se resuelve el documento de origen y sus fichas. Si se indica una ficha concreta, esa ficha es la entrada al documento.
- Se aplica el alcance Cerrado, Poroso o Federado y el filtro de etiquetas elegido.
- La afinidad temática es la suma de cada peso del posicionamiento multiplicado por la proporción de esa etiqueta en la ficha. También se admiten pesos de clúster, perspectiva documentada y concepto.
- Se recorren relaciones existentes. Para las landings se incorporan enlaces de lectura comprobados en su contenido, identificados como navegación.
- En las fichas con extracto de un artículo se conserva primero una base de hasta cuatro conceptos que ese artículo sostiene directamente. Se ordenan por afinidad con la composición del propio documento. Así se explica su mecanismo antes de ampliar hacia las preferencias del visitante.
- Si existe una relación saliente de uso documentado, esa base incluye también una lectura vinculada directamente con el mecanismo de origen. Se conserva el tipo de relación ya registrado en el Atlas.
- Se ordenan las piezas por afinidad y cercanía, conservando las conexiones necesarias para llegar a cada una. La prioridad es `(0.25 + 0.75 × afinidad) / (1 + distancia)`.
- Se toma el prefijo de ese recorrido que cabe en el presupuesto. La secuencia se calcula independientemente del presupuesto. La siguiente incorporación se detiene completa cuando necesita más tokens.

Las relaciones conceptuales explican ideas. Las relaciones de navegación abren lecturas desde una página. Ambas conservan su tipo en el mapa.

## URL y protocolo

```text
https://dakleyer.github.io/perspective-beyond/atlas/posicionamiento/?posicionamiento=D-285&tokens=2000&peso=empresa:50&peso=matematicas:50
```

Parámetros: `posicionamiento`, `tokens`, `peso` repetido, `modo`, `site`, `puente`, `solo`, `red`, `sentido`, `max`, `rol`, `lectura` e `instruccion`. `centro` y `desde` siguen sirviendo como puntos de entrada anteriores. Las claves conocidas se reconocen al ignorar mayúsculas.

[Entrada para asistentes](entrada.txt) · [Posicionamientos preparados](preparados/index.html) · [Documentos y sus fichas](documentos.json) · [Grafo completo](../mapa/grafo.json).

Para lectores web, cada documento y cada ficha dispone de un registro JSON pequeño bajo `documentos/` y `fichas/`. El registro de una ficha contiene su texto de lectura, coste, composición y relaciones hacia las fichas vecinas. Los paquetes preparados ofrecen lecturas calculadas para las entradas iniciales. El visualizador calcula configuraciones personalizadas y permite descargar su lectura y su mapa.

Las relaciones de esos registros incluyen también la composición, el clúster y el coste de la ficha vecina, para elegir la próxima lectura sin abrir todas las candidatas. Los resultados de la [comparación de recorridos](comparacion/README.md) documentan las preguntas, paquetes y respuestas de las pruebas ciegas.

El mismo cálculo funciona en Node.js:

```sh
node docs/atlas/mapa/cli.mjs "posicionamiento=D-285&tokens=2000&peso=empresa:50&peso=matematicas:50"
```

La función pública es `positionMap(graph, readPosition(params, graph))` de `positioning.mjs`. El grafo publica documentos, referencias de fichas, composiciones y costes de tokens. Para regenerar los costes, instalar `tiktoken==0.12.0` y ejecutar `docs/atlas/mapa/build_graph.py` con el catálogo y el archivo canónico de la edición.
