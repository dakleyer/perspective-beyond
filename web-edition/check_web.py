"""Validate full publication payload, static navigation and source preservation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote
from hashlib import sha256
import json,sys
R=Path(__file__).resolve().parent
D=R/'dist'
edition=json.loads((D/'edicion/edicion.json').read_bytes())
manifest=json.loads((D/'edicion/archivos.json').read_bytes())
origin=edition['publicOrigin']
issues=[]
for m in manifest:
    p=D/m['webPath'].lstrip('/')
    if not p.is_file():issues.append({'missingCanonical':m['canonicalPath']});continue
    if sha256(p.read_bytes()).hexdigest()!=m['sha256']:issues.append({'changedCanonical':m['canonicalPath']})
graph=json.loads((D/'perspective-beyond/atlas/mapa/grafo.json').read_bytes())
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        for k in ['href','src']:
            if a.get(k):self.links.append(a[k])
files={p.relative_to(D).as_posix():p for p in D.rglob('*')if p.is_file()}
pages={path:Page(p.read_text(encoding='utf8'))for path,p in files.items()if path.endswith('.html')}
checks=0;targets=set()
for path,page in pages.items():
    base=origin+'/'+path
    for href in page.links:
        if href.startswith(('mailto:','tel:','data:','javascript:','blob:')):continue
        url=urlsplit(urljoin(base,href))
        if url.netloc!=urlsplit(origin).netloc:continue
        target=unquote(url.path).lstrip('/')
        if not target or target.endswith('/'):target+='index.html'
        checks+=1;key=(target,unquote(url.fragment))
        if key in targets:continue
        targets.add(key)
        if target not in files:issues.append({'page':path,'href':href,'kind':'missingFile'})
        elif url.fragment and target in pages and unquote(url.fragment)not in pages[target].ids:issues.append({'page':path,'href':href,'kind':'missingAnchor'})
for n in graph['nodes']:
    slug=''.join(c if c.isascii()and(c.isalnum()or c in '_-')else'_'for c in n['id'])
    path=('conceptos'if n['type']=='concepto'else'fichas')+'/'+slug+'/index.html'
    if path not in pages:issues.append({'missingFicha':n['id']})
    elif '<script'in files[path].read_text(encoding='utf8'):issues.append({'scriptInReader':n['id']})
result={'canonicalRevision':edition['canonicalRevision'],'canonicalFiles':len(manifest),'canonicalBytes':sum(m['bytes']for m in manifest),
'canonicalFilesIdentical':not any('Canonical'in str(e)for e in issues),'htmlPages':len(pages),'linkOccurrences':checks,
'internalTargets':len(targets),'fichasAndConcepts':len(graph['nodes']),'relations':len(graph['edges']),
'totalFiles':len(files),'totalBytes':sum(p.stat().st_size for p in files.values()),'issues':issues,'pass':not issues}
(R/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if result['pass']else 1)

