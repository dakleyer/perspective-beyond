# Comprobación de las instancias del Atlas

La primera publicación registró once entradas `v1`. Se cotejaron 45 URLs públicas con los archivos publicados. Los once QR devolvieron su URL versionada al decodificarlos a tamaño original y a 144 píxeles. También se comprobó un QR generado para una ficha concreta con `desde=E1731`. [Primera publicación](https://github.com/dakleyer/perspective-beyond/commit/d8765f6dfd8286b8efb6ce490aec2304060dd3b0)

| Recorrido | Comprobación |
| --- | --- |
| QR de JubAp.eu → selector | El navegador abrió `eu/v1` y recuperó el rol Consultor, la ficha E1628 y los pesos Perspectiva 60 % y Decisiones 40 %. Al cambiar el origen a Diálogos, retiró E1628 de las URLs compartidas y del texto copiado. |
| URL de una página con `desde` | Un agente abrió en GitHub Raw la sesión cerrada de E1628 con ambos pesos. Verificó el marco JUBAP y distinguió la propuesta de la fuente de su propia prueba para dos áreas. El original abrió por HTTP directo después de fallar en el lector web. |
| Texto versionado de Investigación | Otro agente recuperó `research/v1`, el rol Investigador, Matemáticas al 100 % en modo exclusivo y la ficha GH049 desde el archivo sin parámetros. Explicó la diferencia entre detectar un cambio y bloquear una ejecución obsoleta. Dejó fuera la encajonadora porque pertenece a otro clúster. |

La revisión detectó dos referencias de GitHub para GH049. El archivo era idéntico en ambos commits. La instancia y las instrucciones del selector usan ahora el commit de la edición examinada que aparece en la ficha. Una configuración inválida de clúster, alcance o puente pide corregir la selección. Si se solicita una etiqueta exclusiva y el filtro queda vacío, el selector detiene la exportación hasta resolverlo.

[Registro de instancias](https://dakleyer.github.io/perspective-beyond/atlas/i/instancias.json) · [JubAp.eu v1](https://dakleyer.github.io/perspective-beyond/atlas/i/eu/v1/) · [Investigación v1, texto para el asistente](https://raw.githubusercontent.com/dakleyer/perspective-beyond/main/docs/atlas/i/research/v1/entrada.txt)
