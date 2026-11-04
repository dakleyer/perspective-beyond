# Lectura pública completa del Atlas

La entrada web es https://integralmanagement.ch/atlas-reader/ . Incluye la guía del asistente, los índices, el texto de cada ficha y concepto, sus relaciones en ambos sentidos, las fuentes y las perspectivas por etiquetas. El visitante puede dar esa única URL a su asistente. La configuración de la URL se conserva en la propia guía.

El HTML se sirve completo: el lector recibe contenido y enlaces antes de ejecutar JavaScript. Cada ficha también publica lectura.txt y registro.json. El inventario relaciona cada identificador con sus URLs de HTML, texto y datos. sitemap.xml permite descubrir las páginas; el llms.txt de la raíz publica la entrada de lectura. La proyección utiliza los registros del grafo sin crear o eliminar fichas ni relaciones.

Generar: `python scripts/build_atlas_public_reader.py`. Comprobar vigencia: `python scripts/build_atlas_public_reader.py --check`. Comprobar enlaces: `python scripts/check_atlas_public_reader.py`.

El repositorio conserva el grafo y las versiones. La entrega HTML es una proyección del mismo contenido para personas y asistentes. Las interfaces visuales existentes mantienen su función y diseño; esta ruta añade lectura pública y descubrimiento del corpus completo.

El lector del dominio institucional sirve las páginas en su propio dominio y conserva una copia de cada recurso público con verificación SHA-256. La fuente corresponde a un commit concreto del repositorio. El visitante y su asistente recorren las fichas y relaciones sin acceder al repositorio. Cada respuesta pública enlaza la guía mediante Link: describedby. Los registros de fichas y el grafo conservan sus campos originales.
