"""Generate versioned Atlas launch pages, plain-text entries and QR codes."""

import argparse
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlencode, urljoin, urlsplit


ATLAS = "https://dakleyer.github.io/perspective-beyond/atlas/"
RAW = "https://raw.githubusercontent.com/dakleyer/perspective-beyond/main/docs/atlas/"
SCHEMA = "perspective-beyond/instances-v1"
MODES = {"closed": "Closed", "porous": "Porous", "federated": "Federated"}
CONFIG_KEYS = ("cluster", "mode", "centro", "rol", "lectura", "pesos", "solo", "puente")


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def make_qr(url, path):
    import qrcode

    parsed = urlsplit(url)
    if (parsed.scheme, parsed.netloc) != ("https", "dakleyer.github.io") or not parsed.path.startswith("/perspective-beyond/atlas/"):
        raise ValueError("The QR code must open a public Perspective Beyond URL.")
    path.parent.mkdir(parents=True, exist_ok=True)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(path)


def link(url, label, attrs=""):
    return f'<a href="{escape(url, quote=True)}"{attrs}>{escape(label)}</a>'


def page(title, css, body):
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{escape(title)} · Perspective Beyond</title><link rel="stylesheet" href="{css}">'
        '<style>.launch{display:grid;grid-template-columns:minmax(0,1fr) minmax(10rem,15rem);gap:1.5rem}'
        '.qr{display:block;width:100%;height:auto;max-width:14rem;background:white;border:1px solid #d6cbb8;border-radius:.3rem}'
        '.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,16rem),1fr));gap:.75rem}'
        '.cards .panel{margin:0}.cards h2{font-size:1.45rem}'
        '@media(max-width:38rem){.launch{grid-template-columns:minmax(0,1fr)}}</style></head>'
        f'<body><main>{body}</main></body></html>'
    )


def weight_labels(weights, topics):
    total = sum(weights.values())
    shares = {tag: divmod(value * 1000, total) for tag, value in weights.items()}
    spare = 1000 - sum(tenths for tenths, _ in shares.values())
    extra = set(sorted(weights, key=lambda tag: -shares[tag][1])[:spare])
    labels = []
    for tag, (tenths, _) in shares.items():
        whole, fraction = divmod(tenths + (tag in extra), 10)
        percent = f"{whole},{fraction}" if fraction else str(whole)
        labels.append(f"{topics[tag]['label']} {percent} %")
    return " · ".join(labels)


def guard_versions(previous, current):
    index = {(row["id"], row["version"]): row for row in current}
    for before in previous:
        key = before["id"], before["version"]
        after = index.get(key)
        if after is None or any(before.get(field) != after.get(field) for field in CONFIG_KEYS):
            raise ValueError(f"Conserva {key[0]}/{key[1]} y añade otra versión para cambiar su configuración.")


def configure(config, catalog, routes, sources):
    slug, version, cluster, mode = (config[key] for key in ("id", "version", "cluster", "mode"))
    if not re.fullmatch(r"[a-z][a-z0-9-]*", slug) or not re.fullmatch(r"v[1-9][0-9]*", version):
        raise ValueError(f"Invalid ID or version: {slug}/{version}")
    if mode not in MODES or (cluster != "all" and cluster not in catalog["clusters"]):
        raise ValueError(f"Invalid cluster or scope: {slug}")
    role, purpose = config["rol"], config["lectura"]
    role_label, role_rule = catalog["session_profiles"]["roles"][role]
    purpose_label, purpose_rule = catalog["session_profiles"]["purposes"][purpose]
    weights = config.get("pesos", {})
    strict = config.get("solo", False)
    if not isinstance(strict, bool) or (strict and not weights):
        raise ValueError(f"Invalid thematic filter: {slug}")
    if cluster == "all" and mode != "federated":
        raise ValueError(f"The complete constellation requires federated scope: {slug}")
    clusters = catalog["clusters"]
    membership = catalog["source_cluster"]
    center = config.get("centro")
    route_group = routes["text_entries"]["clusters"].get(cluster)
    active = list(clusters) if mode == "federated" else [cluster]
    bridge_id = config.get("puente")
    if mode == "porous" and bridge_id not in routes["bridges"]:
        raise ValueError(f"Porous mode requires a recorded bridge: {slug}")
    bridge = routes["bridges"][bridge_id] if mode == "porous" else None
    if bridge:
        if bridge["from"] != cluster:
            raise ValueError(f"The bridge does not leave the selected cluster: {slug}")
        active.append(bridge["to"])
        route = route_group["porous"][bridge_id]
    else:
        route = routes["text_entries"]["global"] if cluster == "all" else route_group[mode]
    if center and membership[center] not in active:
        raise ValueError(f"The central card falls outside scope: {slug}")
    topics = catalog["topics"]
    for tag, value in weights.items():
        if type(value) is not int or not 1 <= value <= 10000:
            raise ValueError(f"Invalid weight: {slug}/{tag}")
        if not any(membership[sid] in active for sid in topics[tag]["sources"]):
            raise ValueError(f"Tag outside scope: {slug}/{tag}")
    if strict and center and not set(weights).intersection(catalog["source_tags"][center]):
        raise ValueError(f"The central card falls outside the thematic filter: {slug}")

    name = "The whole constellation" if cluster == "all" else clusters[cluster][0]
    focus = "personalizado" if weights else "parejo"
    params = [("config", "1"), ("rol", role), ("lectura", purpose), ("enfoque", focus)]
    params.extend(("peso", f"tema:{tag}:{value}") for tag, value in weights.items())
    if strict:
        params.append(("solo", "1"))
    if center:
        params.append(("desde", center))
    if bridge:
        params.append(("puente", bridge_id))
    web = [("site", cluster), ("modo", mode), *params]
    url = f"{ATLAS}i/{slug}/{version}/"
    source = sources[center] if center else None
    note = catalog["editorial_cards"].get(center, {})
    focus_label = weight_labels(weights, topics) if weights else "Balanced focus"
    if strict:
        focus_label += " · exclusive thematic selection"
    return {
        **config, "nombre": name, "alcance": [clusters[key][0] for key in active],
        "url": url, "qr": url + "qr.png", "texto": url + "entrada.txt",
        "textoGithub": f"{RAW}i/{slug}/{version}/entrada.txt",
        "selector": ATLAS + "?" + urlencode(web) + "#asistente",
        "ruta": ATLAS + route + "?" + urlencode(params),
        "rutaGithub": RAW + route + "?" + urlencode(params),
        "indice": RAW + route,
        "indicesTematicos": [RAW + f"temas/{tag}.txt" for tag in weights],
        "mapa": ATLAS + "mapa/?" + urlencode({"centro": center, "red": "ideas"}) if center else None,
        "rolNombre": role_label, "rolRegla": role_rule, "proposito": purpose_label, "propositoRegla": purpose_rule,
        "modoNombre": MODES[mode], "enfoqueNombre": focus_label, "puenteNombre": bridge["title"] if bridge else None,
        "fuente": {"id": center, "titulo": source["title"], "original": note.get("provenance", {}).get("url") or source["url"],
                   "ficha": urljoin(ATLAS, note.get("url") or "../sources/" + source["slug"] + "/")} if source else None,
    }


def build_instances(out, canonical_bytes, definitions_path):
    catalog = json.loads((out / "global-catalog.json").read_bytes())
    assert catalog["canonical_sha256"] == sha256(canonical_bytes).hexdigest()
    canonical = json.loads(canonical_bytes)
    routes = json.loads((out / "rutas.json").read_bytes())
    sources = {row["id"]: row for row in canonical["sources"] + catalog["sources"]}
    definitions = json.loads(definitions_path.read_bytes())
    assert definitions["schema"] == SCHEMA
    instances = [configure(row, catalog, routes, sources) for row in definitions["instances"]]
    if len({(row["id"], row["version"]) for row in instances}) != len(instances):
        raise ValueError("An instance is repeated in the same version.")
    folder = out / "i"
    registry = folder / "instancias.json"
    if registry.exists():
        guard_versions(json.loads(registry.read_bytes())["instances"], instances)
    cards = []
    for row in instances:
        target = folder / row["id"] / row["version"]
        title = f'{row["nombre"]} · {row["version"]}'
        source = row["fuente"]
        lead = f'{row["modoNombre"]} · {row["rolNombre"]} · {row["enfoqueNombre"]}'
        actions = [
            link(row["textoGithub"], "Open text for my assistant"),
            link(row["selector"], "Open configuration in the Atlas"),
        ]
        if source:
            actions.append(link(row["mapa"], "Explore this card's map"))
        write(target / "index.html", page(title, "../../../mapa/mapa.css",
            '<p class="kicker">Perspective Beyond · Entry point</p>'
            f'<h1>{escape(title)}</h1><p class="lead">{escape(lead)}</p>'
            f'<p>{link("../../", "View all entry points")}</p>'
            '<section class="panel launch"><div><h2>Connect your assistant</h2>'
            '<p>Copy the text address and paste it into your assistant along with your question. '
            'You can also open the configuration to explore or adjust your selection.</p>'
            f'<div class="actions">{"".join(actions)}</div>'
            + (f'<p>Starting point · {link(source["original"], source["titulo"])}</p>' if source else '')
            + '</div><div><h2>QR code</h2>'
            '<img src="qr.png" class="qr" width="320" height="320" alt="QR code to open this entry point">'
            f'<p>{link("qr.png", "Download the QR code", " download")}</p></div></section>'))
        lines = [
            "PERSPECTIVE BEYOND · CONNECT YOUR ASSISTANT",
            f'Instance: {row["id"]}/{row["version"]} · {row["nombre"]}',
            f'Scope: {row["modoNombre"]} · {", ".join(row["alcance"])}',
            f'Role: {row["rolNombre"]}. {row["rolRegla"]}',
            f'Purpose: {row["proposito"]}. {row["propositoRegla"]}',
            "Focus: " + row["enfoqueNombre"] + ".",
            "",
            "Apply the selection written in this file. If there is already a question, answer it. "
            "Otherwise, ask what the visitor wants to explore.",
            "Use eligible cards and open the relevant originals. Distinguish the original text, "
            "the editorial relationship and your own application. Weights indicate reading priorities.",
        ]
        if row.get("solo"):
            lines.append("Consult only the intersection of the scope and chosen tags. Link relationships between eligible cards.")
        if row["puenteNombre"]:
            lines.append("Only authorised bridge: " + row["puenteNombre"])
        if source:
            lines += ["", f'Starting point: [{source["id"]}] {source["titulo"]}',
                      "Card: " + source["ficha"], "Original: " + source["original"],
                      "Consider this source when it is relevant to the question."]
        lines += ["", "Scope index: " + row["indice"]]
        lines.extend("Tag index: " + value for value in row["indicesTematicos"])
        lines += ["Central Atlas: " + ATLAS, "Open the configuration: " + row["selector"]]
        write(target / "entrada.txt", "\n".join(lines))
        make_qr(row["url"], target / "qr.png")
        cards.append(f'<article class="panel"><h2>{link(row["url"], title)}</h2><p>{escape(lead)}</p>'
                     f'<div class="actions">{link(row["textoGithub"], "Text for the assistant")}'
                     f'{link(row["qr"], "QR code")}</div></article>')
    write(registry, json.dumps({"schema": SCHEMA, "atlas": ATLAS, "instances": instances},
                               ensure_ascii=False, indent=2))
    write(folder / "index.html", page("Entry points", "../mapa/mapa.css",
        '<p class="kicker">Perspective Beyond · One Atlas, several entries</p><h1>Connect your assistant</h1>'
        '<p class="lead">Each entry opens the same constellation with an initial selection. '
        'Choose an instance and share its link or QR code.</p>'
        f'<nav>{link(ATLAS, "Global Atlas")}{link("instancias.json", "Instance registry")}'
        f'{link("https://github.com/dakleyer/perspective-beyond/tree/main/docs/atlas/i#readme", "Integration protocol")}</nav>'
        f'<div class="cards">{"".join(cards)}</div>'))
    return instances


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas", type=Path, default=here.parent)
    parser.add_argument("--canonical", type=Path, default=here.parent.parent / "data/atlas.json")
    parser.add_argument("--definitions", type=Path, default=here / "definiciones.json")
    parser.add_argument("--qr")
    parser.add_argument("--output-qr", type=Path, default=Path("atlas-qr.png"))
    args = parser.parse_args()
    if args.qr:
        make_qr(args.qr, args.output_qr)
    else:
        instances = build_instances(args.atlas, args.canonical.read_bytes(), args.definitions)
        print(f"{len(instances)} Atlas instances generated")
