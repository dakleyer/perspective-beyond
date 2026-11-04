# Posicionamiento · pruebas de lectura

4 de noviembre de 2026.

## Comparación de recorridos y cierre

La [comparación ciega de seis preguntas](comparacion/README.md) dio tres preferencias al posicionamiento y tres empates en la última evaluación independiente. Se incorporaron extractos literales de las fuentes públicas en 154 fichas y una base de conceptos directamente sostenidos por el documento antes de ampliar por las etiquetas del visitante. El cierre conserva también una lectura de uso documentado cuando existe. Otro lector nuevo repitió las dos preguntas afectadas y mantuvo el empate y la preferencia del posicionamiento.

La versión de cierre pasa 36 pruebas funcionales y 48 comprobaciones exactas de tokens. El protocolo y los registros de fichas permiten elegir la siguiente lectura con los porcentajes y costes de las vecinas. Siete configuraciones calculadas entregan también el contexto y la cuenta completa a lectores que usan solo la web. La selección de cada paquete coincide con la del motor y los paquetes cerrados conservan exclusivamente su clúster. Los textos originales de los artículos y las relaciones conceptuales conservan su contenido.

Una prueba pública desde una URL configurada, sin ejecutar código, recuperó la selección cerrada de cinco piezas de Tegrity.AI y la cuenta completa de 1.755/2.400 tokens. Conservó los pesos 70:30, el rol de consultor y la instrucción de respuesta. La conversación posterior distinguió trabajo compensatorio evitable y supervisión necesaria. El [registro de comparación](comparacion/README.md) describe esa prueba.

## Qué se comprobó

El posicionamiento abre un documento de origen. Sus fichas tienen una composición porcentual de etiquetas; el visitante aporta otra combinación que orienta el recorrido. El presupuesto de tokens incorpora piezas completas y sus relaciones de llegada. Al ampliarlo se conserva el prefijo anterior de la lectura.

Se comprobaron 1.209 documentos, 1.291 fichas y 272 conceptos. Cada ficha conserva un documento de origen y todas las composiciones suman 100 %. El documento biográfico contiene varias fichas, que también pueden elegirse como entradas concretas. Las landings enlazan sus lecturas mediante navegación observada en el cuerpo de las webs.

Las 30 pruebas funcionales cubren resolución del documento, porcentajes, afinidad, crecimiento del presupuesto, continuidad de las conexiones, filtros, alcances Cerrado y Poroso, pesos normalizados, ausencia de duplicados, compatibilidad con las entradas anteriores y conservación del rol e instrucciones en la URL. Las 48 lecturas de prueba se volvieron a codificar con `tiktoken 0.12.0`, `o200k_base`: el número obtenido coincidió con el declarado y quedó dentro de cada presupuesto.

[Resultados funcionales](pruebas-funciones.json) · [Comprobación de tokens](pruebas-tokens.json) · [Pruebas reproducibles](pruebas.mjs).

Para repetir las pruebas, desde la raíz del repositorio:

```sh
node docs/atlas/posicionamiento/pruebas.mjs
```

## Dos lectores sin historial del proyecto

Un lector recibió únicamente las URLs públicas, el protocolo y los módulos publicados. Ejecutó por su cuenta el mismo posicionamiento, D-285, con pesos 50:50 de empresa y matemáticas. Con 2.000 tokens obtuvo 1.721 tokens de lectura y cuatro piezas seleccionadas. Con 4.000 obtuvo 3.790 y diez piezas. Las primeras cuatro conservaron su orden; el máximo de conexiones recorridas siguió siendo tres. El aumento amplió también la lectura lateral. El documento de entrada se muestra como un nodo adicional.

El lector recuperó la composición 35 % empresa, 25 % transformación, 20 % representación, 10 % matemáticas, 5 % aprendizaje y 5 % evidencia. Calculó la afinidad con la combinación elegida: `0,5 × 0,35 + 0,5 × 0,10 = 0,225`. Explicó la relación entre traducción de contexto, límites de observación y representación utilizando los textos públicos de D-285, D-216 y D-265.

El segundo lector utilizó solo herramientas web y el paquete público de JubAp.eu de 2.000 tokens. Reconoció la landing como documento de entrada, su ficha y las lecturas conectadas de Field Notes, el framework y Reframing Value Creation. El paquete incluyó 1.969 tokens, dejó 31 y detuvo la lectura ante un siguiente bloque de 124. Interpretó el 45 % de empresa como composición temática de la ficha. Explicó el mecanismo con un ejemplo de excepciones entre áreas y consultó las fuentes públicas citadas.

## Publicación

El modelo, el cálculo, los porcentajes y los documentos de entrada están en este repositorio. Hay 33 lecturas preparadas: once posicionamientos iniciales con presupuestos de 1.000, 2.000 y 4.000 tokens. El navegador permite combinar otros documentos, etiquetas y presupuestos y descargar el resultado.

Los registros de fuentes, textos de artículos y relaciones conceptuales anteriores conservaron su contenido. La navegación de las landings se registra por separado. El catálogo canónico `docs/data/atlas.json` conserva SHA-256 `5e37a308dc5d57011d4884dc95dcc7b26223f1c383ad9c3a8bf2367e15a7fb49`.
