# Instancias de Perspective Beyond

[Ver las entradas y sus QR](https://dakleyer.github.io/perspective-beyond/atlas/i/) · [Registro de instancias](https://dakleyer.github.io/perspective-beyond/atlas/i/instancias.json) · [Atlas central](https://dakleyer.github.io/perspective-beyond/atlas/)

Una instancia es una configuración inicial del Atlas. Define la versión, el clúster, el alcance, el rol, el propósito, las etiquetas y sus pesos. Puede señalar una ficha de partida. El catálogo, las fuentes y las relaciones se consultan en el Atlas central.

## Qué enlace colocar en cada web

- Usa la URL de una instancia versionada si quieres ofrecer una selección lista para abrir. La página incluye un QR, el texto para el asistente y el enlace para ajustar la sesión en el Atlas.
- Usa el enlace de texto de la instancia cuando quieras compartir una sola URL directamente con un asistente. La selección está escrita en el archivo. Para lectores web se ofrece el mismo texto en GitHub Raw.
- Usa un enlace con `desde=ID` si una página propone su propia ficha de partida. El ID tiene que pertenecer al alcance y cumplir el filtro temático de la sesión. La ficha orienta la lectura cuando es pertinente a la pregunta.

Ejemplo de un enlace y un QR para una página de Integral Management.

```html
<a href="https://dakleyer.github.io/perspective-beyond/atlas/i/imsv/v1/">
  Conecta tu asistente a Nueva Perspectiva
</a>
<a href="https://dakleyer.github.io/perspective-beyond/atlas/i/imsv/v1/">
  <img src="https://dakleyer.github.io/perspective-beyond/atlas/i/imsv/v1/qr.png"
       width="144" height="144" loading="lazy"
       alt="Código QR para conectar tu asistente a Nueva Perspectiva">
</a>
```

Ejemplo de una selección para una página concreta. `E1628` corresponde a *The JUBAP Framework*.

[Abrir la configuración de esa ficha](https://dakleyer.github.io/perspective-beyond/atlas/?site=eu&modo=closed&config=1&rol=consultor&lectura=ideas&enfoque=personalizado&peso=tema%3Aperspectiva%3A60&peso=tema%3Adecision%3A40&desde=E1628#asistente)

## Versionar y generar

Edita [definiciones.json](definiciones.json) para dar de alta otra instancia o versión. Un cambio de configuración de una instancia publicada se añade como una versión nueva. Las webs pueden adoptar la nueva URL a su ritmo. Un QR anterior sigue apuntando a su versión.

Desde la raíz del repositorio, con Python 3.10 o posterior.

```sh
python -m pip install "qrcode[pil]==8.2"
python docs/atlas/i/build_instances.py
```

El generador usa los catálogos públicos de la misma edición. Comprueba que la ficha y las etiquetas elegidas correspondan al alcance y que un puente poroso salga del clúster indicado. Produce `instancias.json`, una página por versión, su `entrada.txt` y su `qr.png`.

Para crear un QR de una configuración particular, copia el enlace del selector del Atlas. Conserva el texto alternativo y un enlace normal junto al QR.

```sh
python docs/atlas/i/build_instances.py --qr "https://dakleyer.github.io/perspective-beyond/atlas/?site=eu&modo=closed&desde=E1628#asistente" --output-qr jubap-framework.png
```

## Comprobaciones al publicar

1. Decodifica el QR y comprueba que la URL incluya la versión esperada.
2. Abre el texto en GitHub Raw. Comprueba clúster, alcance, rol, etiquetas y ficha de partida.
3. Abre la configuración en el Atlas y copia la URL para el asistente. Comprueba que incluya los pesos y la ficha mientras esta sea elegible.
4. Cambia a un clúster que deje fuera la ficha. La interfaz debe señalarlo y la URL copiada debe quedar sin `desde`.

[Pruebas de conversación con asistentes](../perfiles/VALIDACION.md)
