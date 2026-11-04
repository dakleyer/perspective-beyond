# Perspective Beyond · Pruebas con asistentes

## Nuevas conversaciones sin contexto previo · 4 de noviembre de 2026

Cinco agentes nuevos recibieron únicamente una URL pública, una pregunta de visitante y la petición de registrar sus lecturas. Se crearon sin historial del hilo. En un caso hubo una segunda intervención para elegir la configuración. Las respuestas se contrastaron con las fuentes citadas y con la selección que debía conservar cada entrada.

| Visita | Configuración y pregunta | Lectura observada |
| --- | --- | --- |
| A | Embajador, Diálogos cerrado; dos etiquetas 70:30; cuatro frases, ejemplo cotidiano y pregunta final. Equipos que compran herramientas y definen problemas distintos. | Encontró «Dices cloud y acabas comprando cloud», «Una empresa vive en varias ideas de negocio» y «Diez minutos mirando desde el lugar de otro». Explicó cómo la definición del problema orienta la solución; propuso observar juntos un pedido. Respetó las cuatro frases. Detectó que una clave llevaba una mayúscula y aplicó solo el peso restante según las instrucciones entonces publicadas. |
| B | Investigador Federado; matemáticas 0,5 y empresa 0,3; filtro exclusivo; partir del rechazo de una entrada y explicar control de acceso. | Recuperó el reparto 62,5 % / 37,5 %. Distinguió pertenencia al dominio, decisión y rechazo; leyó un estudio OAuth/OIDC fijado a commit y conservó la separación entre documentación de 2025–2026 y el antecedente de 2016. |
| C | Consultor Poroso, Diálogos → JubAp.Net; pesos 150:20; dos opciones y una observación semanal sobre transmisión de soluciones entre áreas. El visitante pidió añadir movilidad. | Recuperó el puente de la solución inaudible al saber práctico de Tiger Teams y el reparto 88,2 % / 11,8 %. Propuso recuperar una solución atascada y practicarla entre áreas. Mantuvo la selección del puente al responder a la petición de movilidad. |
| D | Rol personalizado de tutor; espiritualidad 100 %, filtro exclusivo, tres párrafos, imagen cotidiana y enlaces titulados. Comprometerse con un papel sin quedar encerrado en él. | Localizó siete fichas elegibles y desarrolló su respuesta desde atención, convivencia y razones compartidas. Usó la imagen de un delantal y una observación semanal, señaladas como elaboración propia. Conservó el formato de tres párrafos. |
| E | Entrada general; después Consultor Federado, Diálogos 60 % e Integral Management 40 %, dos observaciones y experimento semanal. Un grupo que reproduce las rutinas del fundador. | Primero pidió la selección en un solo mensaje. Después distinguió operar una estructura de reconstruir sus supuestos y conectó esa idea con el manifiesto y los aprendizajes de Nueva Perspectiva. Propuso una variación de la rutina que otra persona pudiera resolver. |

### Ajustes derivados de estas lecturas

- Las diferencias de mayúsculas en claves conocidas se resuelven contra su escritura canónica. Una etiqueta desconocida, duplicada o fuera del alcance pide corrección; el selector conserva pendiente el reparto en lugar de sustituirlo por otro.
- La entrada cerrada de Diálogos pasa de aproximadamente 505 KB a 8 KB. Enlaza el catálogo íntegro por separado y un índice breve con 93 entradas conceptuales. El contenido de las 298 reflexiones y de las fuentes del corpus se conserva.
- Las instrucciones comunes piden explicar primero la idea y su mecanismo, usar títulos legibles en los enlaces e integrar las fechas donde aclaren una afirmación. El registro técnico se presenta aparte cuando el lector lo pide.
- Veinte comprobaciones de funciones verifican normalización, números, duplicados, claves desconocidas, alcance y conservación de selecciones anteriores del mapa. [Resultados de las funciones](pruebas-funciones.json).

El lector web empleado en estas conversaciones devolvió errores para algunas URLs de Pages. Los agentes recuperaron los textos públicos por HTTP y registraron ese recorrido. La entrada conserva la ruta equivalente de GitHub para lectores de texto.

### Ronda posterior a la publicación de los ajustes

Se crearon otros tres agentes sin historial y se les entregaron nuevas URLs de la versión [4d19db3](https://github.com/dakleyer/perspective-beyond/commit/4d19db3219ad3827667142afe8baf3a376f0e058). En conjunto, esta revisión comprende ocho agentes y nueve respuestas de visitante, incluida la selección en dos intervenciones de la visita E.

| Visita | Función comprobada | Resultado observado |
| --- | --- | --- |
| F | Lectura exclusivamente web, sin terminal ni HTTP desde código; repetir la selección 70:30 que contenía una mayúscula. | Leyó la entrada y los textos mediante el espejo de GitHub indicado por el Atlas. Conservó Perspectiva 70 % y Empresa 30 %. Desarrolló la definición del problema, las expectativas de cada equipo y el cambio observable, con cuatro frases, ejemplo y pregunta final. |
| G | Una etiqueta desconocida con peso 70 junto a Empresa con peso 30. | Pidió corregir solo la etiqueta desconocida; conservó Empresa y la configuración pendiente. Esperó la corrección antes de abrir fuentes o recalcular el reparto. |
| H | Mapa desde el diálogo sobre vocabularios de los oficios; radio 2, máximo 12, empresa 0,5 y matemáticas 0,3, con mayúsculas. | Leyó y ejecutó los módulos públicos: 176 nodos alcanzables, 12 mostrados, pesos 62,5 % / 37,5 %. Reconstruyó un recorrido real y el sentido inverso de una de sus aristas. Identificó que el concepto matemático era alcanzable pero quedaba fuera de los doce mostrados. |

Las lecturas recuperaron mecanismos diferentes del corpus: revisar cómo se formula el problema; distinguir admisión, decisión y resultado; transmitir juicio práctico mediante trabajo compartido; mantener apertura al asumir un papel; y aprender a reconstruir una rutina en vez de reproducirla solamente. Los ejemplos y ejercicios nuevos se presentaron como aplicaciones de los agentes.

También se realizaron cinco comprobaciones en el selector publicado: recuperación 70:30, conservación de una instrucción especial en la URL, copia efectiva de esa URL, bloqueo de una selección con etiqueta desconocida y corrección explícita conservando rol y modo. [Resultados del selector](pruebas-selector.json). El registro de funciones contiene veinte comprobaciones, incluidas ocho comparaciones del recorrido de mapas con la versión anterior.

Para repetir las visitas, usa la [entrada breve](https://dakleyer.github.io/perspective-beyond/atlas/entrada/dialogos/cerrado.txt), el [espejo de texto](https://raw.githubusercontent.com/dakleyer/perspective-beyond/main/docs/atlas/entrada/dialogos/cerrado.txt), el [índice conceptual](https://dakleyer.github.io/perspective-beyond/atlas/dialogos/indice.txt) o el [mapa de oficios con pesos](https://dakleyer.github.io/perspective-beyond/atlas/mapa/?centro=D-285&radio=2&max=12&red=ideas&peso=Empresa%3A0.5&peso=Matematicas%3A0.3). La conversación nueva debe recibir solo la URL configurada y su pregunta.

El 4 de noviembre de 2026 se probaron cinco agentes en contextos separados. Los agentes recibieron una URL pública y una pregunta de visitante. Las comprobaciones observaron si podían abrir el material, conservar la configuración, escoger fuentes dentro del alcance y distinguir la aportación original de una lectura editorial o de una aplicación propuesta durante la conversación.

[Selector del Atlas](https://dakleyer.github.io/perspective-beyond/atlas/#asistente) · [Guía y perfiles](https://dakleyer.github.io/perspective-beyond/atlas/guide.html) · [Protocolo del mapa](https://github.com/dakleyer/perspective-beyond/tree/main/docs/atlas/mapa#readme)

## Primera ronda

| Ensayo | Pregunta o decisión del visitante | Resultado observado |
| --- | --- | --- |
| Embajador, Integral Management cerrado, 100 % | Cómo pasa Nueva Perspectiva de observar a actuar. La URL pedía tres viñetas y dos fuentes. El visitante sugirió añadir Phylons. | El agente usó tres viñetas, citó los originales de JUMP UP y la encajonadora, separó el ejemplo propuesto del caso histórico y dejó Phylons fuera del alcance. |
| Investigador, Matemáticas al 100 %, alcance cerrado | Qué establece A23 y si acredita una aplicación en xSeil en 2016. | El agente cruzó los índices, leyó A23 y su revisión semántica en el commit registrado, distinguió P1/P2/P4 de P3/P5/P6 y separó el resultado formal de 2026 de la afirmación histórica. |
| Entrada general → Consultor poroso | Abrir una sesión sin parámetros y, en el siguiente mensaje, elegir Integral Management → JubAp.eu, 150:20, con dos opciones y un primer paso. El visitante sugirió usar Tiger Teams de JubAp.Net. | El primer mensaje pidió las elecciones en una sola respuesta. El segundo verificó el puente np-r25, aplicó 88,2 % y 11,8 %, citó los originales pertinentes y dejó las fuentes de JubAp.Net fuera del recorrido. |
| Mapa de Structural Awareness | Calcular radio 2, máximo 16, Matemáticas 0,5 y Empresa 0,3. Explicar un camino y el sentido de sus flechas. | El agente ejecutó el módulo público con el grafo publicado. Obtuvo 294 nodos alcanzables, 16 visibles y los pesos 62,5 % y 37,5 %. Comprobó en el README fuente un camino de dos referencias documentales. |

El lector web utilizado devolvió errores de acceso para las entradas de GitHub Pages. Las mismas URLs devolvieron HTTP 200 en una consulta directa con todos sus parámetros. Para que el lector de texto pudiera recibir una configuración completa sin depender de esos parámetros ni de JavaScript, se publicaron los perfiles escritos y el JSON precalculado en el [commit bb36688](https://github.com/dakleyer/perspective-beyond/commit/bb36688521236a901d292885ed3865c9cec49cd1).

## Segunda ronda

| Entrada que recibió el agente | Comprobación y resultado |
| --- | --- |
| [Perfil Investigador sin parámetros](https://raw.githubusercontent.com/dakleyer/perspective-beyond/bb36688521236a901d292885ed3865c9cec49cd1/docs/atlas/perfiles/investigador-matematicas.txt) | El lector web abrió el perfil, los dos índices, ambas fichas por el espejo y los originales de A23. El agente distinguió el acto de registrar un cambio del control que impide ejecutar con una autorización obsoleta. Atribuyó su ejemplo de un puente cerrado a su propia aplicación y dejó la hipótesis histórica de xSeil sin verificar. |
| [Perfil Consultor sin parámetros](https://raw.githubusercontent.com/dakleyer/perspective-beyond/bb36688521236a901d292885ed3865c9cec49cd1/docs/atlas/perfiles/consultor-accion-integral.txt) | El lector web recuperó rol, pesos, destino y puente del archivo. El agente propuso separar la espera en el traspaso de una avería repetida mediante el parte de turno y el registro de averías. Consultó directamente los dos originales cuando el lector web devolvió error. |
| [JSON del mapa](https://raw.githubusercontent.com/dakleyer/perspective-beyond/bb36688521236a901d292885ed3865c9cec49cd1/docs/atlas/mapa/ejemplos/structural-awareness.json) | Con el lector web y sin JavaScript, el agente recuperó centro, pesos y conteos por anillo. Buscó los dos IDs de relación en el mismo archivo y comprobó que la primera flecha se recorre en sentido inverso y la segunda en su sentido registrado. |
| [URL federada con dos pesos](https://raw.githubusercontent.com/dakleyer/perspective-beyond/bb36688521236a901d292885ed3865c9cec49cd1/docs/atlas/entrada/dialogos/federado.txt?config=1&rol=investigador&lectura=explore&enfoque=personalizado&peso=cluster%3Adialogos%3A60&peso=cluster%3Aimsv%3A40) | El lector web recuperó ambos pesos, Diálogos 60 % e Integral Management 40 %. El agente encontró el puente dg-181 y comprobó los originales por HTTP directo. Distinguió lo que Iván formula en el manifiesto, la lectura editorial del diálogo y su propia aplicación a una red de bibliotecas. |

## Cómo repetir la prueba

1. Abre una conversación nueva. Pega solo una URL de la tabla y una pregunta. Puedes pedir al asistente que explique de dónde tomó su respuesta y que indique qué fuentes abrió.
2. Incluye una petición que requiera otro ámbito. Comprueba que el asistente identifique el límite antes de usar la fuente y proponga una selección nueva si hace falta.
3. Pide una aplicación a un caso nuevo. Revisa que queden separadas la idea atribuida, la conexión editorial y la aplicación propuesta.
4. Repite con una URL del selector y con un perfil de texto. Para un mapa, compara el JSON descargado con la selección visible y verifica la dirección de cada flecha en `edges`.

La validación describe el comportamiento observado en estas conversaciones. El perfil indica cómo leer el Atlas. El acceso a cada original depende de las capacidades de lectura del asistente.
