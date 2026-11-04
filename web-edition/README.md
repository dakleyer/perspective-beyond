# Atlas completo en la web

[Entrada para asistentes](https://perspective-beyond-atlas.carvedgem.chatgpt.site/entrada/) · [Explorar la edición web](https://perspective-beyond-atlas.carvedgem.chatgpt.site/) · [Guía en texto](https://perspective-beyond-atlas.carvedgem.chatgpt.site/entrada.txt)

La edición web permite recorrer el Atlas mediante páginas HTML públicas, sin cuenta ni JavaScript. GitHub conserva el repositorio canónico y la historia de cambios.

La edición publicada reproduce los **5,155 archivos** de la revisión **7cfd1665348e7a34a6d233133f32969d8011561d**, con **76,706,211 bytes** idénticos a sus originales. Añade vistas de lectura HTML de las 1.294 fichas, 272 conceptos, 1.212 documentos y 11.832 relaciones, junto con los 46 enlaces de navegación del mapa.

## Recorridos

- [Fichas y fuentes](https://perspective-beyond-atlas.carvedgem.chatgpt.site/fichas/)
- [Conceptos](https://perspective-beyond-atlas.carvedgem.chatgpt.site/conceptos/)
- [Relaciones](https://perspective-beyond-atlas.carvedgem.chatgpt.site/relaciones/)
- [Clústeres](https://perspective-beyond-atlas.carvedgem.chatgpt.site/clusters/)
- [Etiquetas](https://perspective-beyond-atlas.carvedgem.chatgpt.site/etiquetas/)
- [Documentos](https://perspective-beyond-atlas.carvedgem.chatgpt.site/documentos/)
- [Todos los archivos](https://perspective-beyond-atlas.carvedgem.chatgpt.site/archivos/)
- [Edición y procedencia](https://perspective-beyond-atlas.carvedgem.chatgpt.site/edicion/)

Cada ficha tiene su contenido de lectura, composición, procedencia y conexiones. Las relaciones se pueden seguir en ambos sentidos. Los archivos JSON, textos, scripts y recursos de la edición original siguen disponibles bajo /perspective-beyond/ en el mismo servidor. Los originales externos conservan sus referencias.

## Regenerar una edición

Los generadores leen los objetos del repositorio y producen la publicación web. Desde esta carpeta:

~~~text
python build_web.py RUTA_REPOSITORIO REVISION_COMPLETA ORIGEN_PUBLICO
python check_web.py
~~~

dist/edicion/archivos.json conserva el tamaño y SHA-256 de cada archivo canónico. La verificación comprueba las páginas de todas las fichas, los enlaces y anclas internos y las huellas de los archivos reproducidos. El proceso genera una publicación web; no crea respaldos del proyecto.

[Metadatos de la publicación](publication.json).

El archivo vacio de control de GitHub Pages conserva su contenido y se sirve mediante la ruta de texto indicada en el inventario de archivos.

## Orientación antes del posicionamiento

[Comprender el Atlas](https://tegrity.ai/atlas-orientation/) · [Mapa superior](https://perspective-beyond-atlas.carvedgem.chatgpt.site/orientacion/) · [Resumen para asistentes](https://perspective-beyond-atlas.carvedgem.chatgpt.site/orientacion/lectura.txt)

Siete áreas agrupan los temas existentes; 36 puentes dirigidos resumen sus relaciones registradas. Las 1.566 fichas y conceptos mantienen su identidad y pueden participar en varias áreas. Once rutas por pregunta proponen dos o tres entradas concretas antes de pedir clúster, pesos y alcance a un visitante nuevo. Las configuraciones ya fijadas por el lector o su URL se conservan.

`orientation.py` genera esta capa al terminar `build_web.py`. `check_orientation.py` comprueba cobertura, correspondencias, relaciones, diversidad de entradas y continuidad de la configuración. El modelo completo conserva la pertenencia de cada pieza y los identificadores de las relaciones agrupadas. El grafo original permanece intacto.
