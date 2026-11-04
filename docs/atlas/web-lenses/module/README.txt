MIND ATLAS / ATLAS MENTAL — NUEVA PERSPECTIVA

Un grafo compartido. Una ventana de lectura para cada página.

ABRIR EL PROYECTO
https://integralmanagement.ch/nueva-perspectiva/atlas-mental/
https://perspective-beyond-atlas.carvedgem.chatgpt.site/mind-atlas/
Fuente canónica: https://github.com/dakleyer/perspective-beyond/tree/main/docs/atlas/web-lenses

ESTRUCTURA
Documento de origen → fichas → composiciones de etiquetas → relaciones explicadas con otras cards and concepts.
Una página web conserva su texto y su mapa visual. El diseñador selecciona el punto de entrada, unos pesos de etiquetas y un presupuesto pequeño de lectura. La vista ampliada reproduce esa misma configuración sobre el grafo compartido.

CRITERIOS PUBLICADOS
profiles.json contiene, para cada página, su URL, fichas de inicio, pesos, presupuesto, alcance y URL reproducible. selections/ contiene el resultado JSON y la lectura de texto preparada para asistentes. Todos los nodos y relaciones seleccionados conservan sus identificadores del grafo canónico.
Las páginas con fichas propias parten de ellas. Las otras entradas publican una selección de inicio del diseñador que conecta esa lectura con fichas existentes. Esta configuración es una capa de navegación; el sustrato del grafo se conserva.

CÁLCULO
Se utiliza docs/atlas/positioning.mjs: readPosition, positionMap y positionParams.
La composición porcentual de cada ficha permite calcular afinidad con los pesos elegidos. El recorrido sigue relaciones existentes y conserva los caminos hacia cada incorporación. El presupuesto cuenta el texto de las fichas y las relaciones seleccionadas con o200k_base. Una ficha no se divide al alcanzar el límite. El mini mapa muestra un prefijo conectado; la lectura descargable conserva la selección completa.
Un peso no concede acceso ni modifica una fuente. El alcance cerrado, poroso o federado determina qué clusters pueden participar.

EJEMPLO DE URL CONFIGURADA
https://perspective-beyond-atlas.carvedgem.chatgpt.site/perspective-beyond/atlas/posicionamiento/?posicionamiento=E1628&tokens=2200&max=11&modo=federated&site=eu&peso=tema%3Aperspectiva%3A45&peso=tema%3Atransformacion%3A30&peso=tema%3Aaprendizaje%3A15&peso=tema%3Adecision%3A10

EJEMPLO COMPLETO PARA COMPRENDER
Abre la entrada de texto de la página The JUBAP Framework: selections/eu-1628.txt. Parte de su documento de origen. Explícame el movimiento UP y cómo se relaciona con JUMP. Elige dos conexiones de la lectura que permitan comprender el mecanismo. Explica qué aporta cada una y conserva los enlaces a las fuentes. Pregúntame qué situación quiero examinar.

EJEMPLO COMPLETO PARA COMPARAR
Lee selections/net-1287.txt. Quiero comparar la transmisión de conocimiento tácito en los Tiger Teams con otra experiencia de aprendizaje del mismo Atlas. Distingue el conocimiento que viaja, quién puede ejercerlo y qué condiciones permiten continuarlo. Explica una semejanza útil y una diferencia que cambie su aplicación. Conserva las fechas y los contextos de los textos y enlaza sus originales.

CONFIGURAR UNA PREGUNTA
1. Identifica el documento o ficha de entrada.
2. Elige el propósito: comprender, comparar, resolver, enseñar o elaborar.
3. Conserva la configuración que ya venga en la URL. Pregunta solo por lo que falte.
4. Elige pesos de etiquetas: por ejemplo aprendizaje 50, perspectiva 30, encuentros 20.
5. Elige alcance y presupuesto. Amplía el presupuesto cuando la pregunta necesite más lectura.
6. Lee las relaciones, explica los mecanismos y vuelve a las fuentes originales.

PROTOCOL COMPARTIDO PARA ASISTENTES
https://tegrity.ai/wp-content/uploads/2026/11/atlas-web-entry-2884295fa843.txt
ORIENTACIÓN SUPERIOR
https://perspective-beyond-atlas.carvedgem.chatgpt.site/orientacion/
CLÚSTERES
https://perspective-beyond-atlas.carvedgem.chatgpt.site/clusters/
FICHAS
https://perspective-beyond-atlas.carvedgem.chatgpt.site/fichas/

MANTENIMIENTO
Actualizar el inventario público y los perfiles de diseñador. Ejecutar build_selections.mjs con el mismo grafo y módulo de posicionamiento. Verificar identificadores, relaciones, presupuestos y enlaces. Publicar los perfiles, las selecciones y su integración. La regeneración no reescribe artículos, notas metodológicas, notas de campo ni Related; conserva el diseño de los mapas existentes.
