"""Render the same article map in the atlas and on its original site."""
from html import escape

BASE = "https://dakleyer.github.io/perspective-beyond/"

def focus_url(source):
    return f"{BASE}?focus={source}#atlas"

def field_diagram():
    return """<svg class="pbx-diagram" viewBox="0 0 280 156" aria-hidden="true" focusable="false">
<g fill="none" stroke="#6f9688"><ellipse cx="140" cy="78" rx="118" ry="65"/><ellipse cx="140" cy="78" rx="77" ry="45"/><path d="M25 78h230M140 14v128" opacity=".35"/></g>
<g fill="none" stroke="#d2ac74"><path d="M140 78 80 48 40 32M80 48 23 63M140 78 80 108 23 93M80 108 40 125M140 78 200 48 240 32M200 48 257 63M140 78 200 108 257 93M200 108 240 125"/></g>
<g fill="#efd09c"><circle cx="140" cy="78" r="9"/><circle cx="80" cy="48" r="4"/><circle cx="80" cy="108" r="4"/><circle cx="200" cy="48" r="4"/><circle cx="200" cy="108" r="4"/></g>
<g fill="#a9c5b3"><circle cx="40" cy="32" r="4"/><circle cx="23" cy="63" r="4"/><circle cx="23" cy="93" r="4"/><circle cx="40" cy="125" r="4"/><circle cx="240" cy="32" r="4"/><circle cx="257" cy="63" r="4"/><circle cx="257" cy="93" r="4"/><circle cx="240" cy="125" r="4"/></g>
</svg>"""

def article_map(source, title, concepts, neighbors, *, key, opened=False, conceptual=False):
    def list_items(rows, label):
        cards = []
        for i, row in enumerate(rows, 1):
            relation = f'<span class="pbx-type">{escape(row["relationship"])}</span>' if row.get("relationship") else ""
            cards.append(f'<li><a href="{escape(row["url"], quote=True)}"><span class="pbx-number" aria-hidden="true">{i:02}</span><span class="pbx-card">{relation}<strong>{escape(row["title"])}</strong><span class="pbx-reading">{escape(row["reading"])}</span></span><span aria-hidden="true" class="pbx-arrow">↗</span></a></li>')
        return f'<section class="pbx-branch" aria-label="{label}"><h3>{label}</h3><ul>{"".join(cards)}</ul></section>'

    opened_attr = " open" if opened else ""
    branch_label = "Conceptual connections" if conceptual else "Closest readings"
    summary_label = "Map of ideas and connections" if conceptual else "Map of ideas and readings"
    count_label = "4 ideas · 4 connections" if conceptual else "4 concepts · 4 readings"
    return f'''<aside class="pbx" id="{key}" data-pbx-source="{source}" aria-labelledby="{key}-title">
<div class="pbx-cover">
<div class="pbx-copy">
<p class="pbx-kicker"><span aria-hidden="true">◇</span> Perspective Beyond <span class="pbx-separator">/</span> Article concept map</p>
<h2 id="{key}-title">{escape(title)}</h2>
<p class="pbx-lens"><span>Reading lens</span> {escape(concepts[0]["title"])}</p>
<a class="pbx-atlas" href="{focus_url(source)}">Explore this article in the central atlas <span aria-hidden="true">↗</span></a>
</div><div class="pbx-art">{field_diagram()}</div>
</div>
<details class="pbx-details"{opened_attr}>
<summary><span>{summary_label}</span><span class="pbx-count">{count_label}</span><span class="pbx-toggle" aria-hidden="true"></span></summary>
<div class="pbx-branches">{list_items(concepts, "Concepts and methods")}{list_items(neighbors, branch_label)}</div>
</details></aside>'''
