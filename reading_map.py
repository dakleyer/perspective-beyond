"""Render the same directional concept connections on the article and atlas."""
from html import escape

def edge_markup(edges, core, language):
    titles = {n["id"]: n["title"] for n in core}
    cards = []
    for edge in edges:
        incoming = edge["from"] not in titles
        base = edge["to"] if incoming else edge["from"]
        name = escape(titles[base])
        direction = "←" if incoming else "→"
        label = ("Conexión entrante" if incoming else "Conexión saliente") if language == "es" else (
            "Incoming connection" if incoming else "Outgoing connection")
        title = escape(edge["title"])
        cards.append(
            f'<li><a class="pb2-edge" href="{escape(edge["url"], quote=True)}">'
            f'<span class="pb2-trace">{name}<span class="pb2-direction" role="img" aria-label="{label}">{direction}</span></span>'
            f'<strong>{title}</strong><span class="pbx-type">{escape(edge["relationship"])}</span>'
            f'<span class="pbx-reading">{escape(edge["reading"])}</span></a></li>'
        )
    return "".join(cards)
