# Perspective Beyond · Pruebas con asistentes

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
