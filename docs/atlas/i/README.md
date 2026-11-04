# Perspective Beyond instances

[View entries and their QR codes](https://dakleyer.github.io/perspective-beyond/atlas/i/) · [Instance register](https://dakleyer.github.io/perspective-beyond/atlas/i/instancias.json) · [Central Atlas](https://dakleyer.github.io/perspective-beyond/atlas/)

An instance is an initial Atlas configuration. It defines the version, cluster, scope, role, purpose, tags and their weights. It may specify a starting card. The catalogue, sources and relationships are consulted in the central Atlas.

## Which link to place on each website

- Use the URL of a versioned instance to offer a selection ready to open. The page includes a QR code, the text for the assistant and a link to adjust the session in the Atlas.
- Use the instance's text link to share a single URL directly with an assistant. The selection is written into the file. The same text is offered on GitHub Raw for web readers.
- Use a link with `desde=ID` when a page proposes its own starting card. The ID must belong to the scope and meet the session's thematic filter. The card guides the reading when it is relevant to the question.

Example of a link and QR code for an Integral Management page.

```html
<a href="https://dakleyer.github.io/perspective-beyond/atlas/i/imsv/v1/">
  Connect your assistant to Nueva Perspectiva
</a>
<a href="https://dakleyer.github.io/perspective-beyond/atlas/i/imsv/v1/">
  <img src="https://dakleyer.github.io/perspective-beyond/atlas/i/imsv/v1/qr.png"
       width="144" height="144" loading="lazy"
       alt="QR code to connect your assistant to Nueva Perspectiva">
</a>
```

Example of a selection for a specific page. `E1628` corresponds to *The JUBAP Framework*.

[Open that card's configuration](https://dakleyer.github.io/perspective-beyond/atlas/?site=eu&modo=closed&config=1&rol=consultor&lectura=ideas&enfoque=personalizado&peso=tema%3Aperspectiva%3A60&peso=tema%3Adecision%3A40&desde=E1628#asistente)

## Version and generate

Edit [definiciones.json](definiciones.json) to register another instance or version. A configuration change to a published instance is added as a new version. Websites can adopt the new URL at their own pace. An earlier QR code continues to point to its version.

From the repository root, with Python 3.10 or later.

```sh
python -m pip install "qrcode[pil]==8.2"
python docs/atlas/i/build_instances.py
```

The generator uses the public catalogues from the same edition. It checks that the selected card and tags match the scope and that a porous bridge leaves the specified cluster. It produces `instancias.json`, one page per version, its `entrada.txt` and its `qr.png`.

To create a QR code for a particular configuration, copy the link from the Atlas selector. Retain the alternative text and a normal link next to the QR code.

```sh
python docs/atlas/i/build_instances.py --qr "https://dakleyer.github.io/perspective-beyond/atlas/?site=eu&modo=closed&desde=E1628#asistente" --output-qr jubap-framework.png
```

## Publication checks

1. Decode the QR code and check that the URL includes the expected version.
2. Open the text on GitHub Raw. Check the cluster, scope, role, tags and starting card.
3. Open the configuration in the Atlas and copy the URL for the assistant. Check that it includes the weights and the card while that card remains eligible.
4. Switch to a cluster that excludes the card. The interface must indicate this, and the copied URL must no longer contain `desde`.

[Instance checks](VALIDACION.md) · [Conversation tests with assistants](../perfiles/VALIDACION.md)
