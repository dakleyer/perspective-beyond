"""Validate complete public reader coverage, all internal targets and source identity."""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit,urljoin,unquote
import json,sys
REPO=Path(__file__).resolve().parent.parent;OUT=REPO/'docs/atlas/lectura';PREFIX='/perspective-beyond/atlas/lectura/';ORIGIN='https://dakleyer.github.io'
raw=(REPO/'docs/atlas/mapa/grafo.json').read_bytes();g=json.loads(raw);inventory=json.loads((OUT/'inventario.json').read_bytes());issues=[]
assert inventory['graphSha256']==sha256(raw).hexdigest()
nodes={n['id']:n for n in g['nodes']};assert set(inventory['nodes'])==set(nodes)
class Doc(HTMLParser):
 def __init__(self,text):super().__init__();self.links=[];self.ids=set();self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  for key in ['href','src']:
   if a.get(key):self.links.append(a[key])
  if tag=='script' and a.get('type')not in {'application/ld+json','application/json'}:issues.append('Executable script in static reader')
files={p.relative_to(OUT).as_posix():p for p in OUT.rglob('*')if p.is_file()};pages={k:Doc(v.read_text(encoding='utf8'))for k,v in files.items()if k.endswith('.html')};targets=set();checked=0
for path,doc in pages.items():
 for href in doc.links:
  dest=urlsplit(urljoin(ORIGIN+PREFIX+path,href))
  if dest.netloc!='dakleyer.github.io' or not dest.path.startswith(PREFIX):continue
  target=unquote(dest.path[len(PREFIX):]);target=target+'index.html'if not target or target.endswith('/')else target;fragment=unquote(dest.fragment);checked+=1
  if (target,fragment)in targets:continue
  targets.add((target,fragment))
  if target not in files:issues.append('Missing internal URL: '+href)
  elif fragment and target in pages and fragment not in pages[target].ids:issues.append('Missing anchor: '+href)
seen={}
for sid,row in inventory['nodes'].items():
 path=unquote(urlsplit(row['data']).path[len(PREFIX):]);record=json.loads(files[path].read_bytes());assert record['node']==nodes[sid],sid
 for edge in record['relations']:
  if edge[0]in seen:assert seen[edge[0]]==edge,edge[0]
  seen[edge[0]]=edge
 html=files[unquote(urlsplit(row['html']).path[len(PREFIX):])+'index.html'].read_text(encoding='utf8');body=nodes[sid].get('reading')or nodes[sid].get('summary')or''
 assert all(escape(line,quote=True)in html for line in body.splitlines()if line.strip()),sid
 for key in ['html','text','data']:
  rel=unquote(urlsplit(row[key]).path[len(PREFIX):]);rel+='index.html'if rel.endswith('/')else'';assert rel in files,(sid,key)
assert seen=={e[0]:e for e in g['edges']+g.get('navigation',[])}
report={'pass':not issues,'graphSha256':inventory['graphSha256'],'nodesPreserved':len(nodes),'relationsPreserved':len(g['edges']),'navigationPreserved':len(g.get('navigation',[])),'htmlPages':len(pages),'files':len(files),'checkedLinks':checked,'uniqueTargets':len(targets),'issues':issues}
print(json.dumps(report,ensure_ascii=False));sys.exit(bool(issues))
