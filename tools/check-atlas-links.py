#!/usr/bin/env python3
"""Check published Atlas links and anchors directly from a Git revision.

Usage: python tools/check-atlas-links.py [revision] [repository]
Only reads Git objects. No website copy or backup is written.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import json
import re
import subprocess
import sys

REPO = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent
REF = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
HOST = "https://dakleyer.github.io/perspective-beyond/"

def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args])

tree = {line.split("\t", 1)[1]: line.split()[2]
        for line in git("ls-tree", "-r", REF, "--", "docs").decode().splitlines()}
paths = [p for p in tree if p.startswith("docs/atlas/") and p.endswith((".html", ".json", ".txt", ".md"))]
pipe = subprocess.Popen(["git", "-C", str(REPO), "cat-file", "--batch"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
cache = {}

def read(path):
    if path not in cache:
        pipe.stdin.write((tree[path] + "\n").encode())
        pipe.stdin.flush()
        header = pipe.stdout.readline().decode().split()
        size = int(header[2])
        cache[path] = pipe.stdout.read(size).decode("utf8")
        pipe.stdout.read(1)
    return cache[path]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links = set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])

pages, targets, issues = {}, {}, []
checks = 0

def page(path):
    if path not in pages:
        pages[path] = Page(read(path))
    return pages[path]

def check(source, href):
    global checks
    if href.startswith(("mailto:", "tel:", "data:", "javascript:", "blob:")):
        return
    url = urlsplit(urljoin(HOST + source.removeprefix("docs/"), href))
    if url.netloc != "dakleyer.github.io" or not url.path.startswith("/perspective-beyond/"):
        return
    target = "docs/" + unquote(url.path.removeprefix("/perspective-beyond/"))
    if target.endswith("/"):
        target += "index.html"
    if any(x in target for x in ("<", ">", "/ID.json", "/DOCUMENT_ID")):
        return
    checks += 1
    key = (target, unquote(url.fragment))
    if key in targets:
        return
    targets[key] = source
    if target not in tree:
        issues.append({"source": source, "href": href, "target": target, "kind": "missing_file"})
    elif url.fragment and target.endswith(".html") and unquote(url.fragment) not in page(target).ids:
        issues.append({"source": source, "href": href, "target": target, "kind": "missing_anchor"})

try:
    for path in paths:
        if path.endswith(".html"):
            for href in page(path).links:
                check(path, href)
        elif path.endswith(".json"):
            for href in re.findall(r'https://dakleyer\.github\.io/perspective-beyond/[^\s"<>\\]*', read(path)):
                check(path, href.rstrip(").,;:"))
finally:
    pipe.stdin.close()
    pipe.stdout.close()
    pipe.wait()

report = {"head": git("rev-parse", REF).decode().strip(), "published_files": len(paths),
          "pages": len(pages), "link_occurrences": checks, "unique_internal_targets": len(targets),
          "issues": issues, "pass": not issues}
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(0 if report["pass"] else 1)

