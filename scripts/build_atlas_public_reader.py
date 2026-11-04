"""Publish a complete static HTML/text projection of the existing Atlas graph.

python scripts/build_atlas_public_reader.py [--check]
Only derived reader pages, discovery files and the root sitemap are written.
The graph, source records, dialogues and all existing editorial pages stay intact.
"""
from pathlib import Path
from collections import defaultdict
from hashlib import sha256
from html import escape
from urllib.parse import quote,urlsplit,unquote
from html.parser import HTMLParser
import json,math,re,sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
STAGE=REPO
SOURCE=REPO/'docs/atlas/mapa/grafo.json'
SOURCE_BYTES=SOURCE.read_bytes()
g=json.loads(SOURCE_BYTES);N={n['id']:n for n in g['nodes']};E=g['edges'];NAV=g.get('navigation',[]);D={d['id']:d for d in g['documents']}
BASE='https://dakleyer.github.io/perspective-beyond';PREFIX='/perspective-beyond/atlas/lectura';URL=BASE+'/atlas/lectura';OUT=STAGE/'docs/atlas/lectura'
GRAPH=BASE+'/atlas/mapa/grafo.json';DIGEST=sha256(SOURCE_BYTES).hexdigest();files={};html=[];adj=defaultdict(list);where={}
def H(v):return escape(str(v),quote=True)
def slug(s):return re.sub('[^a-zA-Z0-9_-]','_',s)
assert len({slug(k)for k in N})==len(N)
def put(path,text):files['docs/atlas/lectura/'+path.lstrip('/')]=text.encode('utf8')if isinstance(text,str)else text
def url(path='/'):return URL+path
def A(path,title):return '<a href="'+H(PREFIX+path if path.startswith('/')else path)+'">'+H(title)+'</a>'
def nodepath(n):return '/'+('conceptos'if n['type']=='concepto'else'fichas')+'/'+slug(n['id'])+'/'
def p(text):return ''.join('<p>'+H(x).replace('\n','<br>')+'</p>'for x in re.split(r'\n\s*\n',str(text or''))if x.strip())
CSS='''*{box-sizing:border-box}html{color-scheme:light}body{margin:0;background:#f7f4ec;color:#182f39;font:17px/1.75 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:clamp(24px,6vw,72px)}h1,h2,h3{font-family:Georgia,serif;line-height:1.17;font-weight:600;text-wrap:balance}h1{font-size:clamp(34px,5vw,62px);margin:20px 0 28px}h2{font-size:28px}h3{font-size:23px}a{color:#214f5e;text-underline-offset:4px;overflow-wrap:anywhere}nav,.tags,.actions{display:flex;flex-wrap:wrap;gap:10px 20px}.kicker{font-size:12px;text-transform:uppercase;letter-spacing:.16em;color:#89652e;font-weight:700}.body{max-width:860px;margin:44px auto}.card,.reading{background:#fffdf8;border:1px solid #d8cfbe;padding:clamp(20px,4vw,34px);min-width:0;overflow-wrap:anywhere}.reading p:first-child{margin-top:0}.reading p:last-child{margin-bottom:0}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.cards h2{font-size:25px;margin:0 0 12px}.entries{padding:0;list-style:none;display:grid;gap:18px}.entries h2,.entries h3{margin-top:0}.meta,footer{font-size:13px;color:#53666d}.tags a,.pager a{border:1px solid #d8cfbe;padding:4px 10px}.pager{margin:24px 0}.quote{border-left:3px solid #ad843f;padding-left:22px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.7 ui-monospace,monospace;background:#fffdf8;border:1px solid #d8cfbe;padding:20px}details{margin:20px 0}summary{cursor:pointer;font-weight:650}footer{border-top:1px solid #d8cfbe;padding-top:24px;margin-top:56px}@media(max-width:650px){.cards{grid-template-columns:minmax(0,1fr)}nav{gap:8px 14px}h2{font-size:25px}}'''
put('style.css',CSS)
def page(path,title,body,lead=''):
 path=path.rstrip('/')+'/'if path!='/'else path
 canonical=url(path);plain=canonical+'lectura.txt'
 doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow,max-snippet:-1"><meta name="description" content="'+H(lead or'Complete Atlas: navigable thought, concepts, sources and relationships.')+'"><title>'+H(title)+' · Mind Atlas</title><link rel="canonical" href="'+H(canonical)+'"><link rel="stylesheet" href="'+PREFIX+'/style.css"><link rel="sitemap" type="application/xml" href="'+URL+'/sitemap.xml"></head><body><main><header><p class="kicker">Perspective Beyond · Mind Atlas</p><h1>'+H(title)+'</h1><nav aria-label="Atlas reading paths">'+''.join(A(x,t)for x,t in[('/','Home'),('/entrada/','With your assistant'),('/clusters/','Clusters'),('/etiquetas/','Tags'),('/fichas/','Cards'),('/conceptos/','Concepts'),('/relaciones/','Relationships'),('/documentos/','Sources')])+'</nav></header><section class="body">'+('<p class="lead">'+H(lead)+'</p>'if lead else'')+body+'</section><footer><p>'+A('/entrada.txt','Text instructions')+' · '+A(GRAPH,'Complete graph')+' · '+A('/inventario.json','Reading inventory')+' · '+A('/sitemap.xml','URL map')+'</p><p>Edition '+H(g['edition'])+' · source '+H(DIGEST[:12])+'. Cards and relationships retain their identifiers and content. Each source publication retains its context and authorship.</p></footer></main></body></html>\n'
 put(path.lstrip('/')+'index.html',doc);html.append(path)
def listing(path,title,items,render,lead='',size=45):
 total=max(1,math.ceil(len(items)/size))
 def dest(i):return path if not i else path+'pagina-'+str(i+1)+'/'
 for i in range(total):
  pager='<nav class="pager" aria-label="Pages">'+''.join(A(dest(j),str(j+1))for j in range(total))+'</nav>'if total>1 else''
  body='<p class="meta">'+str(len(items))+' items · page '+str(i+1)+' of '+str(total)+'</p>'+pager+'<ul class="entries">'+''.join('<li class="card">'+render(x)+'</li>'for x in items[i*size:(i+1)*size])+'</ul>'+pager
  page(dest(i),title,body,lead)
def card(n):return '<h2>'+A(nodepath(n),n['title'])+'</h2>'+p((n.get('readingSummary')or n.get('summary')or n.get('reading')or'')[:460])+'<p class="meta">'+H(' · '.join(g['clusters'][x]for x in n['clusters']))+'</p>'
ALL=E+NAV
for i,e in enumerate(ALL):
 assert e[1]in N and e[2]in N
 path='/relaciones/'+('pagina-'+str(i//60+1)+'/'if i//60 else'');where[e[0]]=path+'#r-'+sha256(e[0].encode()).hexdigest()[:16];adj[e[1]].append(e);adj[e[2]].append(e)
def relation(e):
 body='<div id="'+where[e[0]].split('#')[1]+'"><h2>'+A(nodepath(N[e[1]]),N[e[1]]['title'])+' → '+A(nodepath(N[e[2]]),N[e[2]]['title'])+'</h2><p><strong>'+H(e[3])+'</strong></p>'+p(e[4])
 if e[5]and str(e[5]).startswith(('https://','http://')):body+='<p class="meta">'+A(e[5],'Relationship source')+'</p>'
 if len(e)>7 and e[7]:body+=p(e[7])
 return body+'<p class="meta">'+H(e[0])+'</p></div>'
listing('/relaciones/','Atlas relationships',ALL,relation,'Each connection links to both endpoints and retains its direction, meaning and provenance.',60)
ordered=sorted(N.values(),key=lambda n:n['title'].casefold());fichas=[n for n in ordered if n['type']=='ficha'];concepts=[n for n in ordered if n['type']=='concepto']
listing('/fichas/','Cards and sources',fichas,card);listing('/conceptos/','Concepts',concepts,card)
for n in ordered:
 path=nodepath(n);reading=n.get('reading')or n.get('summary')or'';related=list({e[0]:e for e in adj[n['id']]}.values())
 body='<p class="meta">'+H(n['id'])+'</p><div class="tags">'+''.join(A('/clusters/'+c+'/',g['clusters'][c])for c in n['clusters'])+'</div><section class="reading">'+p(reading)+'</section>'
 body+='<p class="actions">'+A(path+'lectura.txt','Complete text of this card')+' '+A(path+'registro.json','Card and relationship data')+'</p>'
 if n.get('original'):body+='<p>'+A(n['original'],'Read the source publication')+'</p>'
 if n.get('commitUrl'):body+='<p>'+A(n['commitUrl'],'Research source revision')+'</p>'
 if n.get('documentId')in D:body+='<p>'+A('/documentos/'+n['documentId']+'/','Source document and its cards')+'</p>'
 body+='<details><summary>Reading perspectives</summary><div class="tags">'+''.join(A('/etiquetas/'+t+'/',g['topics'][t]+' · '+format(w*100,'.2f')+' %')for t,w in sorted(n['tagWeights'].items(),key=lambda x:-x[1]))+'</div></details>'
 total=max(1,math.ceil(len(related)/45))
 def dest(j):return path if not j else path+'relaciones-'+str(j+1)+'/'
 for i in range(total):
  pager='<nav class="pager">'+''.join(A(dest(j),'Relationships '+str(j+1))for j in range(total))+'</nav>'if total>1 else''
  content=(body if not i else'<p>'+A(path,'Return to the card and its sources')+'</p>')+'<h2>Relationships of this piece</h2><p>'+str(len(related))+' connections.</p>'+pager+'<ul class="entries">'
  for e in related[i*45:(i+1)*45]:
   other=N[e[2]if e[1]==n['id']else e[1]];content+='<li class="card"><h3>'+('→ 'if e[1]==n['id']else'← ')+A(nodepath(other),other['title'])+'</h3><p><strong>'+H(e[3])+'</strong></p>'+p(e[4])+'<p>'+A(where[e[0]],'View the relationship and its sources')+'</p></li>'
  page(dest(i),n['title'],content+'</ul>'+pager)
 text='# '+n['title']+'\n\n'+reading+'\n\nCard: '+url(path)+'\n'+('Source publication: '+n['original']+'\n'if n.get('original')else'')+'\nRELATIONSHIPS\n'
 for e in related:
  other=N[e[2]if e[1]==n['id']else e[1]];text+=N[e[1]]['title']+' → '+N[e[2]]['title']+'\n'+e[3]+'. '+e[4]+'\nRelationship: '+url(where[e[0]])+'\nOther card: '+url(nodepath(other))+'\n\n'
 put(path.lstrip('/')+'lectura.txt',text);put(path.lstrip('/')+'registro.json',json.dumps({'graphSha256':DIGEST,'node':n,'relations':related},ensure_ascii=False,separators=(',',':'))+'\n')
for c,label in g['clusters'].items():listing('/clusters/'+c+'/',label,[n for n in ordered if c in n['clusters']],card,'A perspective within the same constellation, connected to the others through specific relationships.')
page('/clusters/','Constellation clusters','<div class="cards">'+''.join('<section class="card"><h2>'+A('/clusters/'+c+'/',label)+'</h2><p>'+str(sum(c in n['clusters']for n in ordered))+' cards and concepts.</p></section>'for c,label in g['clusters'].items())+'</div>')
for t,label in g['topics'].items():listing('/etiquetas/'+t+'/',label,sorted([n for n in ordered if n['tagWeights'].get(t,0)>0],key=lambda n:-n['tagWeights'][t]),card)
page('/etiquetas/','Tags and perspectives','<div class="tags">'+''.join(A('/etiquetas/'+t+'/',label)for t,label in g['topics'].items())+'</div>')
for d in D.values():page('/documentos/'+d['id']+'/',d['title'],'<p>'+A(d['url'],'Source publication')+'</p><ul class="entries">'+''.join('<li class="card">'+card(N[sid])+'</li>'for sid in d['fichas'])+'</ul>')
listing('/documentos/','Source documents',sorted(D.values(),key=lambda d:d['title'].casefold()),lambda d:'<h2>'+A('/documentos/'+d['id']+'/',d['title'])+'</h2><p>'+str(len(d['fichas']))+' cards from this document.</p>')
RULE='''ANSWER THE QUESTION FIRST. Explain identity, activity, mechanism, usefulness or application according to what the visitor asks. Tags, weights and codes organise your reading; use understandable names in the answer.
COMPLETE THE READING. If a card is insufficient or empty, open its source publication and the main pages needed to answer within the chosen scope. A series expresses one part of an institution: to explain the organisation, first cover governance, activities and related entities.
RETAIN THE CONFIGURATION. Read the parameters of the visitor's URL: cluster, alcance/modo, posicionamiento/desde/page, rol, lectura, enfoque, repeatable peso, tokens and instruccion. Apply the choices already made; ask only for what is missing. Without a configuration, start with the visitor's question and offer two or three relevant reading paths.
SCOPE. Closed: one cluster. Porous: the agreed thematic bridge and its direction. Federated: recorded relationships between several clusters. Weights are reading priorities and a card's tags are its composition. The tokens budget limits the selected reading; original cards and relationships remain in the graph.
NAVIGATION. Indexes link to each card; cards link to neighbours, complete relationships and sources. All these pages contain readable HTML and public text without running JavaScript, signing in, downloading an application or adding special headers. Use the published links to continue and retain chronology and provenance.
'''
entry='MIND ATLAS · PERSPECTIVE BEYOND · SELF-CONTAINED ENTRY\n\n'+RULE+'\n'+str(len(fichas))+' cards · '+str(len(concepts))+' concepts · '+str(len(E))+' relationships · edition '+g['edition']+'\n\nREADING PATHS\n'+''.join(label+': '+url('/clusters/'+c+'/')+'\n'for c,label in g['clusters'].items())+'\nTags: '+url('/etiquetas/')+'\nCards: '+url('/fichas/')+'\nConcepts: '+url('/conceptos/')+'\nRelationships: '+url('/relaciones/')+'\nDocuments: '+url('/documentos/')+'\nInventory: '+url('/inventario.json')+'\nComplete graph: '+GRAPH+'\nPositioning and budgets: '+BASE+'/atlas/posicionamiento/entrada.txt\n'
put('entrada.txt',entry);put('llms.txt',entry)
page('/entrada/','Connect your assistant to the Atlas',p(RULE)+'<h2>Available reading paths</h2><ul>'+''.join('<li>'+A('/clusters/'+c+'/',label)+'</li>'for c,label in g['clusters'].items())+'</ul><p>'+A('/entrada.txt','Read these instructions as UTF-8 text')+'</p><h2>Usage example</h2><pre>Read this Atlas entry and explain what The Integral Management Society is, what it does and how it relates to the other entities. Start with the institution and continue through the relationships relevant to my question.</pre>')
page('/','A complete, open and navigable Atlas','<p class="quote">An idea is better understood when we can explore its relationships.</p><p>'+str(len(fichas))+' cards · '+str(len(concepts))+' concepts · '+str(len(E))+' relationships.</p><p>Enter through a question, a publication, a concept or a perspective. Each piece leads to its sources and the connections that allow deeper exploration.</p><p class="actions">'+A('/entrada/','Connect your assistant')+A('/clusters/','Explore the perspectives')+A('/fichas/','Read the cards')+'</p><h2>Choose a reading context</h2><div class="cards">'+''.join('<section class="card"><h2>'+A('/clusters/'+c+'/',label)+'</h2><p>'+str(sum(c in n['clusters']for n in ordered))+' connected pieces.</p></section>'for c,label in g['clusters'].items())+'</div>')
inventory={'schema':'atlas/public-reader-v1','graphSha256':DIGEST,'edition':g['edition'],'entry':url('/entrada.txt'),'graph':GRAPH,'counts':{'fichas':len(fichas),'concepts':len(concepts),'relations':len(E),'navigation':len(NAV),'documents':len(D)},'nodes':{n['id']:{'title':n['title'],'html':url(nodepath(n)),'text':url(nodepath(n)+'lectura.txt'),'data':url(nodepath(n)+'registro.json')}for n in ordered},'clusters':{c:url('/clusters/'+c+'/')for c in g['clusters']}}
put('inventario.json',json.dumps(inventory,ensure_ascii=False,separators=(',',':'))+'\n')
sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+H(url(path))+'</loc></url>'for path in html)+'</urlset>\n';put('sitemap.xml',sitemap)
put('README.txt','Mind Atlas: complete public reading\n\n'+entry+'\nGeneration: python scripts/build_atlas_public_reader.py\nVerification: python scripts/build_atlas_public_reader.py --check\nThe generator reads the canonical graph without modifying cards, relationships or source documents.\n')
issues=[]
for path,data in files.items():
 target=STAGE/path
 if '--check'in sys.argv:
  if not target.is_file()or target.read_bytes()!=data:issues.append(path)
 else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
report={'graphSha256':DIGEST,'nodes':len(N),'relations':len(E),'htmlPages':len(html),'files':len(files),'bytes':sum(len(d)for d in files.values()),'sourceUntouched':True,'check':('--check'in sys.argv),'issues':issues,'pass':not issues}
print(json.dumps(report));sys.exit(bool(issues))
