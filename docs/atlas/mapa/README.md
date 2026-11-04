# Mapas de radio de relaciones · Perspective Beyond

[Abrir el visualizador](https://dakleyer.github.io/perspective-beyond/atlas/mapa/) · [Ver un mapa insertado](https://dakleyer.github.io/perspective-beyond/atlas/mapa/ejemplo.html) · [Leer el grafo completo](https://dakleyer.github.io/perspective-beyond/atlas/mapa/grafo.json)

Un mapa de radio selecciona un vecindario alrededor de una ficha, un concepto o una URL de origen. El navegador y la herramienta para bots ejecutan el mismo cálculo. Cada nodo del grafo completo lleva sus etiquetas temáticas y sus clústeres. Los documentos usan las etiquetas del catálogo. Un concepto hereda las etiquetas presentes en al menos la mitad de sus fichas de apoyo. Si ninguna alcanza ese umbral, queda bajo Investigación y documentación técnica.

## Parámetros de la URL

| Parámetro | Significado | Valor por defecto |
| --- | --- | --- |
| `centro` | ID, URL de la ficha o URL original. Los alias de edición publicados también son válidos. | `T1499` |
| `radio` | Número máximo de relaciones recorridas desde el centro. Admite 0 a 4. | `2` |
| `max` | Nodos que pueden aparecer, incluido el centro. Admite 1 a 60. | `16` |
| `red` | `documentos` recorre las relaciones documentales. `ideas` incluye además conceptos, relaciones conceptuales y vínculos de apoyo entre documentos y conceptos. | `documentos` |
| `sentido` | `ambas`, `salientes` o `entrantes`. Controla el recorrido. Las flechas conservan el sentido registrado de la relación. | `ambas` |
| `peso` | Repetible. Usa `etiqueta:peso`, por ejemplo `matematicas:0.5` y `empresa:0.3`. También admite prefijo `tema:` y coma decimal. | Sin ponderación |
| `solo` | Con `1`, el recorrido pasa únicamente por nodos que comparten alguna etiqueta elegida. El centro permanece visible. | Desactivado |
| `embed` | Con `1`, muestra el mapa y su panel de lectura en formato insertable. | Desactivado |

Las claves de las etiquetas están en `topics` de `grafo.json` y en el [índice de etiquetas](https://dakleyer.github.io/perspective-beyond/atlas/enfoques.txt). Si una URL identifica varias fichas, el visualizador indica sus IDs para que se pueda elegir la correcta. Conserva los fragmentos y los parámetros de la URL original que identifican contenido.

## Cálculo reproducible

1. Resuelve el nodo central y selecciona las capas y el sentido del recorrido. Una búsqueda por amplitud mide la distancia mínima, un salto por relación. El centro tiene distancia cero.
2. Divide cada peso por la suma. La afinidad de un nodo es la suma de los pesos normalizados de las etiquetas que lleva. Por ejemplo, 0,5 y 0,3 se convierten en 62,5 % y 37,5 %.
3. Ordena candidatos por `(0.25 + 0.75 × afinidad) / (1 + distancia)`. Sin pesos, usa `1 / (1 + distancia)`. Desempata por distancia e ID. Al elegir una ficha, conserva su camino al centro si cabe en el límite. En caminos de igual longitud, el recorrido visita primero vecinos de mayor afinidad y desempata por ID de nodo y relación.
4. Devuelve los nodos, su distancia y camino, las relaciones entre los nodos visibles, y los conteos de alcanzables, visibles y omitidos por anillo. `route: true` distingue los enlaces que sostienen el camino al centro de los cruces adicionales. La prioridad expresa cercanía y afinidad dentro del corpus. Su interpretación depende del tipo, el texto y la procedencia de cada relación.

## Generar un mapa desde un bot

Ejecuta con Node.js, desde la raíz del repositorio.

```sh
node docs/atlas/mapa/cli.mjs "centro=GH049&radio=2&max=16&red=ideas&peso=matematicas:0.5&peso=empresa:0.3" > mapa.json
```

También puedes pasar la URL completa como primer argumento. Para calcular con otra edición, añade como segundo argumento la ruta de su `grafo.json`. La salida `perspective-beyond/radius-v1` incluye `request`, `dataset`, `center`, `layers`, `nodes` y `edges`. Los nodos incluyen URL de ficha, original cuando existe, etiquetas, distancia, afinidad y relación de recorrido. Los enlaces conservan tipo, sentido, explicación y evidencia cuando está registrada. `dataset` contiene las huellas de los dos catálogos fuente. Para repetir un resultado después de una actualización, usa `grafo.json` del commit de GitHub de esa edición.

El formato `perspective-beyond/graph-v1` contiene `nodes` y `edges`. `edgeFields` declara el orden de los campos de cada relación. El ID de una relación conserva su ID original con el prefijo de capa, como `documento:D001` o `concepto:D001`. El generador verifica que cada relación apunte a nodos existentes y que todas las etiquetas estén en el registro.

## Insertar en una web

En el visualizador, calcula el mapa y pulsa **Copiar código para insertar**, o usa directamente la URL con `embed=1`.

```html
<iframe
  src="https://dakleyer.github.io/perspective-beyond/atlas/mapa/?centro=GH049&amp;radio=2&amp;red=ideas&amp;peso=matematicas%3A0.5&amp;peso=empresa%3A0.3&amp;embed=1"
  title="Mapa de relaciones de la ficha A23"
  loading="lazy"
  style="width:100%;height:720px;border:0"></iframe>
```

La página anfitriona puede compartir la URL, el HTML de inserción o el JSON resultante. El mapa se vuelve a calcular con el grafo publicado cuando se abre. Los anillos muestran los saltos, y el panel de lectura permite abrir cada ficha y su fuente.

## Actualizar el grafo

Después de actualizar `docs/data/atlas.json` y `docs/atlas/global-catalog.json`, ejecuta:

```sh
python docs/atlas/mapa/build_graph.py
```

El generador valida que ambas entradas sean de la misma edición. Publica el nuevo `grafo.json` en el mismo commit que las fuentes del Atlas para que las URLs compartidas sigan resolviendo sobre una edición coherente.
