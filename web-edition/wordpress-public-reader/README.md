# Mind Atlas: lectura pública en el dominio institucional

Entrada: https://integralmanagement.ch/atlas-reader/

Una única URL descubre la guía, los clústeres, etiquetas, fichas, conceptos, documentos, relaciones, textos UTF-8 y registros JSON. Cada respuesta enlaza la guía con la cabecera HTTP Link describedby. El HTML ya contiene el texto y sus enlaces; el lector no requiere JavaScript, cookies, credenciales o cabeceras especiales.

El componente solo atiende GET y HEAD bajo /atlas-reader/. Su manifiesto enumera los archivos públicos de una revisión inmutable del repositorio y sus SHA-256. La primera lectura recupera el recurso público desde esa revisión, verifica su huella y lo conserva como activo de publicación local en uploads/mind-atlas-reader. Las lecturas posteriores se sirven desde esa copia. El visitante navega únicamente por el dominio institucional.

Los campos de las fichas, las relaciones y el grafo permanecen idénticos; el transporte adapta las URLs de navegación de HTML y texto al dominio de lectura. Cada registro JSON de ficha conserva el nodo y sus relaciones completos. El grafo JSON conserva la misma huella que la fuente.

El paquete se construye con package.py a partir de una revisión ya publicada. No necesita ni contiene material privado, credenciales o copias del espacio de trabajo. No modifica artículos, usuarios, capacidades, contenido editorial, temas ni configuraciones de seguridad. El recurso se publica como un componente propio del proyecto.
