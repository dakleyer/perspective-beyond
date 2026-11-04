# Posicionamiento y recorrido: comparación de lectura

4 de noviembre de 2026.

El posicionamiento combina un documento de entrada, sus fichas, la composición porcentual de cada ficha, los pesos elegidos por el visitante y un presupuesto de tokens. Esta prueba comparó la explicación que producen sus lecturas con la del recorrido anterior por saltos.

## Resultado

En la última evaluación independiente de seis preguntas, el posicionamiento obtuvo preferencia en tres y empató en tres. El recorrido combina una base próxima al documento con una expansión por afinidad temática. Las conexiones conservan su significado y las piezas seleccionadas se mantienen al ampliar el presupuesto.

| Pregunta de lectura | Recorrido anterior /20 | Posicionamiento /20 | Preferencia del evaluador |
| --- | ---: | ---: | --- |
| Qué aporta el arquitecto entre oficios y planteamiento matemático | 18 | 20 | Posicionamiento |
| Contribución humana, trabajo compensatorio y decisión de mejora | 20 | 20 | Empate |
| Señal, autorización y liquidez compartida en Phylons | 20 | 20 | Empate |
| De la landing de JubAp.eu a una intervención y sus lecturas | 14 | 20 | Posicionamiento |
| Capacidad empresarial distribuida entre territorios | 19 | 20 | Posicionamiento |
| Una solución expresada que sigue sin ser escuchada | 20 | 20 | Empate |

## Cómo se compararon

Las dos variantes recibieron la misma pregunta, presupuesto y bloques de texto de la misma edición de fuentes. Se cambió el recorrido que selecciona las piezas. El algoritmo anterior se tomó del commit `f269656e8e6ce937f833bb7946430d654d6e0356`, con radio cuatro y hasta sesenta piezas; su lectura se empaquetó en bloques completos hasta el presupuesto común. El posicionamiento aplicó los porcentajes y el presupuesto directamente. El orden de presentación A/B se alternó entre preguntas.

Los lectores comenzaron sin historial del autor y trabajaron exclusivamente con sus paquetes. Produjeron una respuesta independiente por variante. Otro lector juzgó las respuestas y los textos recibidos, sin conocer qué método correspondía a A/B y sin usar las puntuaciones propuestas por sus autores. Cada respuesta recibió cinco notas de cero a cuatro: mecanismo, cobertura de la pregunta, apoyo documental, fluidez para un tercero y precisión temporal y de atribución.

## Qué cambiaron las pruebas

La primera evaluación independiente dio tres preferencias al posicionamiento, dos al recorrido anterior y un empate. Mostró dos mejoras concretas:

1. Algunas fichas de las webs tenían título y referencias, pero poco texto de lectura. Se incorporaron extractos literales de Abstract o de los párrafos iniciales en 154 fichas. Cada extracto identifica la fuente y su huella; también mejora su composición temática.
2. Una afinidad temática alta podía adelantar índices generales y desplazar conceptos necesarios para explicar el documento de entrada. El recorrido conserva ahora hasta cuatro conceptos directamente sostenidos por el artículo, ordenados por afinidad con su propia composición. Después sigue la expansión ponderada del visitante. Una relación de uso documentado incorpora también la lectura que desarrolla ese mecanismo.

Dos pruebas ciegas específicas de los extractos prefirieron la lectura corregida de Human Intelligence Debt y Phylons. Se repitieron las seis preguntas con los mismos extractos disponibles para ambas variantes; después se repitió la comparación con la base conceptual cercana al documento. La tabla recoge el juicio independiente de esta última ronda.

El cierre incorporó una lectura de uso documentado antes de la expansión temática. Otro lector nuevo repitió las dos preguntas afectadas: mantuvo el empate en Human Intelligence Debt (19/19) y prefirió el posicionamiento en capacidad empresarial distribuida (19/17). Esta prueba conservó los mismos presupuestos y fuentes.

Los registros pequeños de las fichas incluyen los porcentajes, clústeres y costes de sus vecinas. Un lector puede elegir la siguiente lectura con esos datos. Los 83 pasajes de la biografía comparten su documento de origen y conservan entradas concretas por ficha; la URL del documento abre el conjunto.

## Materiales de la prueba

- [Paquetes de la comparación final: grupo 1](paquetes-1.json) y [grupo 2](paquetes-2.json).
- [Respuestas del grupo 1](respuestas-1.json) y [grupo 2](respuestas-2.json).
- [Juicio independiente](evaluacion-independiente.json) y [clave de variantes](clave.json).
- [Resultados de la primera comparación](evaluacion-inicial.json).
- [Prueba del extracto de Human Intelligence Debt](extracto-hid.json) y [Phylons](extracto-phylons.json).
- [Paquetes del cierre](paquetes-cierre.json), [respuestas del cierre](respuestas-cierre.json) y [clave del cierre](clave-cierre.json).
- [Protocolo del posicionamiento](../README.md), [pruebas funcionales](../pruebas-funciones.json) y [comprobación de tokens](../pruebas-tokens.json).

El código y los materiales de la prueba están versionados en este repositorio. Los textos originales de artículos, registros de fuentes y relaciones conceptuales conservaron su contenido.
