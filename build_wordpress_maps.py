"""Build integrity-pinned maps for the four WordPress sites and their small loaders."""
import json
from base64 import b64encode
from hashlib import sha256, sha384
from pathlib import Path
from urllib.parse import urlsplit

from article_design import article_map, BASE

ROOT = Path(__file__).resolve().parent
SITES = {"jubap.eu": 35, "jubap.net": 41, "jubap.us": 11, "tegrity.ai": 57}
MOUNT = r'''
  const site = location.hostname.replace(/^www\./, "");
  const path = location.pathname.replace(/\/$/, "") || "/";
  const marker = document.querySelectorAll("section.corpus-related[id^='corpus-related-']");
  if (site !== host || marker.length !== 1) return;
  const key = marker[0].id.slice("corpus-related-".length);
  const entry = maps[key];
  if (!entry || entry.path !== path) return;
  const id = "concept-map-" + key;
  const old = document.getElementById(id);
  if (old && !old.matches("details.pbm")) return;
  const template = document.createElement("template");
  template.innerHTML = entry.html;
  const map = template.content.firstElementChild;
  if (!map || map.id !== id) return;
  const disclosure = map.querySelector("details");
  disclosure.open = Boolean(old?.open) || location.hash === "#" + id;
  const sheet = document.createElement("style");
  sheet.id = "pbx-design";
  sheet.textContent = css;
  document.head.append(sheet);
  if (old) old.replaceWith(map);
  else marker[0].before(map);
  if (location.hash === "#" + id) requestAnimationFrame(() => map.scrollIntoView({block: "start"}));
'''

LOADER = r'''
  if (location.hostname.replace(/^www\./, "") !== host) return;
  const mount = () => {
    const marker = document.querySelectorAll("section.corpus-related[id^='corpus-related-']");
    if (marker.length !== 1) return;
    const key = marker[0].id.slice("corpus-related-".length);
    const path = location.pathname.replace(/\/$/, "") || "/";
    if (!Object.hasOwn(paths, key) || paths[key] !== path || document.getElementById("pbx-map-bundle")) return;
    const script = document.createElement("script");
    script.id = "pbx-map-bundle";
    script.crossOrigin = "anonymous";
    script.integrity = integrity;
    script.src = asset;
    document.head.append(script);
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount, {once:true});
  else mount();
'''

def encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</script", "<\\/script")

def path(url):
    return urlsplit(url).path.rstrip("/") or "/"

def build(rows, output):
    output.mkdir(parents=True, exist_ok=True)
    css = (ROOT / "site/assets/article-design.css").read_text(encoding="utf8")
    result = {}
    for site, count in SITES.items():
        selected = {row["source"].lower(): row for row in rows if row["site"] == site}
        assert len(selected) == count
        assert len({path(r["source_url"]) for r in selected.values()}) == count
        maps = {}
        for key, row in selected.items():
            assert urlsplit(row["source_url"]).hostname == site
            assert len(row["concepts"]) == len(row["neighbors"]) == 4
            maps[key] = {"path": path(row["source_url"]),
                         "html": article_map(row["source"], row["title"], row["concepts"], row["neighbors"],
                                             key="concept-map-" + key)}
        script = f'(() => {{\n  "use strict";\n  const host = {encoded(site)}, maps = {encoded(maps)}, css = {encoded(css)};\n' + MOUNT + "})();\n"
        payload = script.encode()
        filename = f'premium-maps-{site.replace(".", "-")}-{sha256(payload).hexdigest()[:12]}.js'
        (ROOT / "site" / "assets" / filename).write_bytes(payload)
        integrity = "sha384-" + b64encode(sha384(payload).digest()).decode()
        url = BASE + "assets/" + filename
        paths = {key: entry["path"] for key, entry in maps.items()}
        launch = f'(() => {{\n  "use strict";\n  const host = {encoded(site)}, paths = {encoded(paths)}, integrity = {encoded(integrity)}, asset = {encoded(url)};\n' + LOADER + "})();"
        (output / f"{site}-loader.html").write_text(
            '\n<!-- Perspective Beyond premium article maps -->\n<script id="pbx-premium-map-loader">\n'
            + launch + '\n</script>\n<!-- End Perspective Beyond premium article maps -->\n', encoding="utf8")
        result[site] = {"url": url, "integrity": integrity, "keys": paths, "file": filename}
    (output / "release.json").write_text(json.dumps(result, indent=2), encoding="utf8")
    print({site: len(r["keys"]) for site, r in result.items()})

if __name__ == "__main__":
    from argparse import ArgumentParser
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("maps", type=Path)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    build(json.loads(args.maps.read_text(encoding="utf8")), args.output)
