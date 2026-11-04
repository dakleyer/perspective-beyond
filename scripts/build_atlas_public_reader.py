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
 doc='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow,max-snippet:-1"><meta name="description" content="'+H(lead or'Atlas completo: pensamiento, conceptos, fuentes y relaciones navegables.')+'"><title>'+H(title)+' · Mind Atlas</title><link rel="canonical" href="'+H(canonical)+'"><link rel="stylesheet" href="'+PREFIX+'/style.css"><link rel="sitemap" type="application/xml" href="'+URL+'/sitemap.xml"></head><body><main><header><p class="kicker">Perspective Beyond · Mind Atlas</p><h1>'+H(title)+'</h1><nav aria-label="Recorridos del Atlas">'+''.join(A(x,t)for x,t in[('/','Inicio'),('/entrada/','Con tu asistente'),('/clusters/','Clústeres'),('/etiquetas/','Etiquetas'),('/fichas/','Fichas'),('/conceptos/','Conceptos'),('/relaciones/','Relaciones'),('/documentos/','Fuentes')])+'</nav></header><section class="body">'+('<p class="lead">'+H(lead)+'</p>'if lead else'')+body+'</section><footer><p>'+A('/entrada.txt','Instrucciones en texto')+' · '+A(GRAPH,'Grafo completo')+' · '+A('/inventario.json','Inventario de lectura')+' · '+A('/sitemap.xml','Mapa de URLs')+'</p><p>Edición '+H(g['edition'])+' · fuente '+H(DIGEST[:12])+'. Las fichas y relaciones conservan sus identificadores y contenido. Cada publicación de origen mantiene su contexto y autoría.</p></footer></main></body></html>\n'
 put(path.lstrip('/')+'index.html',doc);html.append(path)
def listing(path,title,items,render,lead='',size=45):
 total=max(1,math.ceil(len(items)/size))
 def dest(i):return path if not i else path+'pagina-'+str(i+1)+'/'
 for i in range(total):
  pager='<nav class="pager" aria-label="Páginas">'+''.join(A(dest(j),str(j+1))for j in range(total))+'</nav>'if total>1 else''
  body='<p class="meta">'+str(len(items))+' elementos · página '+str(i+1)+' de '+str(total)+'</p>'+pager+'<ul class="entries">'+''.join('<li class="card">'+render(x)+'</li>'for x in items[i*size:(i+1)*size])+'</ul>'+pager
  page(dest(i),title,body,lead)
def card(n):return '<h2>'+A(nodepath(n),n['title'])+'</h2>'+p((n.get('readingSummary')or n.get('summary')or n.get('reading')or'')[:460])+'<p class="meta">'+H(' · '.join(g['clusters'][x]for x in n['clusters']))+'</p>'
ALL=E+NAV
for i,e in enumerate(ALL):
 assert e[1]in N and e[2]in N
 path='/relaciones/'+('pagina-'+str(i//60+1)+'/'if i//60 else'');where[e[0]]=path+'#r-'+sha256(e[0].encode()).hexdigest()[:16];adj[e[1]].append(e);adj[e[2]].append(e)
def relation(e):
 body='<div id="'+where[e[0]].split('#')[1]+'"><h2>'+A(nodepath(N[e[1]]),N[e[1]]['title'])+' → '+A(nodepath(N[e[2]]),N[e[2]]['title'])+'</h2><p><strong>'+H(e[3])+'</strong></p>'+p(e[4])
 if e[5]and str(e[5]).startswith(('https://','http://')):body+='<p class="meta">'+A(e[5],'Fuente de la relación')+'</p>'
 if len(e)>7 and e[7]:body+=p(e[7])
 return body+'<p class="meta">'+H(e[0])+'</p></div>'
listing('/relaciones/','Relaciones del Atlas',ALL,relation,'Cada conexión enlaza con sus dos extremos y conserva dirección, significado y procedencia.',60)
ordered=sorted(N.values(),key=lambda n:n['title'].casefold());fichas=[n for n in ordered if n['type']=='ficha'];concepts=[n for n in ordered if n['type']=='concepto']
listing('/fichas/','Fichas y fuentes',fichas,card);listing('/conceptos/','Conceptos',concepts,card)
for n in ordered:
 path=nodepath(n);reading=n.get('reading')or n.get('summary')or'';related=list({e[0]:e for e in adj[n['id']]}.values())
 body='<p class="meta">'+H(n['id'])+'</p><div class="tags">'+''.join(A('/clusters/'+c+'/',g['clusters'][c])for c in n['clusters'])+'</div><section class="reading">'+p(reading)+'</section>'
 body+='<p class="actions">'+A(path+'lectura.txt','Texto completo de esta ficha')+' '+A(path+'registro.json','Ficha y relaciones en datos')+'</p>'
 if n.get('original'):body+='<p>'+A(n['original'],'Leer la publicación de origen')+'</p>'
 if n.get('commitUrl'):body+='<p>'+A(n['commitUrl'],'Revisión de la fuente de investigación')+'</p>'
 if n.get('documentId')in D:body+='<p>'+A('/documentos/'+n['documentId']+'/','Documento de origen y sus fichas')+'</p>'
 body+='<details><summary>Perspectivas de lectura</summary><div class="tags">'+''.join(A('/etiquetas/'+t+'/',g['topics'][t]+' · '+format(w*100,'.2f')+' %')for t,w in sorted(n['tagWeights'].items(),key=lambda x:-x[1]))+'</div></details>'
 total=max(1,math.ceil(len(related)/45))
 def dest(j):return path if not j else path+'relaciones-'+str(j+1)+'/'
 for i in range(total):
  pager='<nav class="pager">'+''.join(A(dest(j),'Relaciones '+str(j+1))for j in range(total))+'</nav>'if total>1 else''
  content=(body if not i else'<p>'+A(path,'Volver a la ficha y sus fuentes')+'</p>')+'<h2>Relaciones de esta pieza</h2><p>'+str(len(related))+' conexiones.</p>'+pager+'<ul class="entries">'
  for e in related[i*45:(i+1)*45]:
   other=N[e[2]if e[1]==n['id']else e[1]];content+='<li class="card"><h3>'+('→ 'if e[1]==n['id']else'← ')+A(nodepath(other),other['title'])+'</h3><p><strong>'+H(e[3])+'</strong></p>'+p(e[4])+'<p>'+A(where[e[0]],'Ver la relación y sus fuentes')+'</p></li>'
  page(dest(i),n['title'],content+'</ul>'+pager)
 text='# '+n['title']+'\n\n'+reading+'\n\nFicha: '+url(path)+'\n'+('Publicación de origen: '+n['original']+'\n'if n.get('original')else'')+'\nRELACIONES\n'
 for e in related:
  other=N[e[2]if e[1]==n['id']else e[1]];text+=N[e[1]]['title']+' → '+N[e[2]]['title']+'\n'+e[3]+'. '+e[4]+'\nRelación: '+url(where[e[0]])+'\nOtra ficha: '+url(nodepath(other))+'\n\n'
 put(path.lstrip('/')+'lectura.txt',text);put(path.lstrip('/')+'registro.json',json.dumps({'graphSha256':DIGEST,'node':n,'relations':related},ensure_ascii=False,separators=(',',':'))+'\n')
for c,label in g['clusters'].items():listing('/clusters/'+c+'/',label,[n for n in ordered if c in n['clusters']],card,'Una perspectiva de la misma constelación, conectada con las demás mediante relaciones concretas.')
page('/clusters/','Clústeres de la constelación','<div class="cards">'+''.join('<section class="card"><h2>'+A('/clusters/'+c+'/',label)+'</h2><p>'+str(sum(c in n['clusters']for n in ordered))+' fichas y conceptos.</p></section>'for c,label in g['clusters'].items())+'</div>')
for t,label in g['topics'].items():listing('/etiquetas/'+t+'/',label,sorted([n for n in ordered if n['tagWeights'].get(t,0)>0],key=lambda n:-n['tagWeights'][t]),card)
page('/etiquetas/','Etiquetas y perspectivas','<div class="tags">'+''.join(A('/etiquetas/'+t+'/',label)for t,label in g['topics'].items())+'</div>')
for d in D.values():page('/documentos/'+d['id']+'/',d['title'],'<p>'+A(d['url'],'Publicación de origen')+'</p><ul class="entries">'+''.join('<li class="card">'+card(N[sid])+'</li>'for sid in d['fichas'])+'</ul>')
listing('/documentos/','Documentos de origen',sorted(D.values(),key=lambda d:d['title'].casefold()),lambda d:'<h2>'+A('/documentos/'+d['id']+'/',d['title'])+'</h2><p>'+str(len(d['fichas']))+' fichas de este documento.</p>')
RULE='''RESPONDE PRIMERO A LA PREGUNTA. Explica identidad, actividad, mecanismo, utilidad o aplicación según lo que el visitante pregunte. Las etiquetas, pesos y códigos organizan tu lectura; usa nombres comprensibles en la respuesta.
COMPLETA LA LECTURA. Si una ficha es insuficiente o está vacía, abre su publicación de origen y las páginas principales que permitan responder dentro del alcance elegido. Una serie expresa una parte de una institución: para explicar la organización cubre primero gobierno, actividades y entidades relacionadas.
CONSERVA LA CONFIGURACIÓN. Lee los parámetros de la URL que te dio el visitante: cluster, alcance/modo, posicionamiento/desde/page, rol, lectura, enfoque, peso repetible, tokens e instruccion. Aplica las selecciones ya elegidas; pregunta solo por lo que falte. Sin configuración, parte de su pregunta y ofrece dos o tres recorridos pertinentes.
ALCANCE. Cerrado: un clúster. Poroso: el puente temático acordado y su dirección. Federado: relaciones registradas entre varios clústeres. Los pesos son prioridades de lectura y las etiquetas de una ficha son su composición. El presupuesto tokens limita la lectura seleccionada; las fichas y relaciones originales permanecen en el grafo.
NAVEGACIÓN. Los índices enlazan con cada ficha; las fichas enlazan con vecinos, relaciones completas y fuentes. Todas estas páginas contienen HTML legible y texto público sin ejecutar JavaScript, iniciar sesión, descargar una aplicación o añadir cabeceras especiales. Usa los enlaces publicados para continuar y conserva la cronología y procedencia.
'''
entry='MIND ATLAS · PERSPECTIVE BEYOND · ENTRADA AUTÓNOMA\n\n'+RULE+'\n'+str(len(fichas))+' fichas · '+str(len(concepts))+' conceptos · '+str(len(E))+' relaciones · edición '+g['edition']+'\n\nRECORRIDOS\n'+''.join(label+': '+url('/clusters/'+c+'/')+'\n'for c,label in g['clusters'].items())+'\nEtiquetas: '+url('/etiquetas/')+'\nFichas: '+url('/fichas/')+'\nConceptos: '+url('/conceptos/')+'\nRelaciones: '+url('/relaciones/')+'\nDocumentos: '+url('/documentos/')+'\nInventario: '+url('/inventario.json')+'\nGrafo completo: '+GRAPH+'\nPosicionamiento y presupuestos: '+BASE+'/atlas/posicionamiento/entrada.txt\n'
put('entrada.txt',entry);put('llms.txt',entry)
page('/entrada/','Conecta tu asistente al Atlas',p(RULE)+'<h2>Recorridos disponibles</h2><ul>'+''.join('<li>'+A('/clusters/'+c+'/',label)+'</li>'for c,label in g['clusters'].items())+'</ul><p>'+A('/entrada.txt','Leer estas instrucciones como texto UTF-8')+'</p><h2>Ejemplo de uso</h2><pre>Lee esta entrada del Atlas y explícame qué es The Integral Management Society, qué hace y cómo se relaciona con las demás entidades. Empieza por la institución y continúa por las relaciones pertinentes a mi pregunta.</pre>')
page('/','Un Atlas completo, abierto y navegable','<p class="quote">Una idea se comprende mejor cuando podemos recorrer sus relaciones.</p><p>'+str(len(fichas))+' fichas · '+str(len(concepts))+' conceptos · '+str(len(E))+' relaciones.</p><p>Entra desde una pregunta, una publicación, un concepto o una perspectiva. Cada pieza conduce a sus fuentes y a las conexiones que permiten profundizar.</p><p class="actions">'+A('/entrada/','Conecta tu asistente')+A('/clusters/','Explora las perspectivas')+A('/fichas/','Lee las fichas')+'</p><h2>Elige un contexto de lectura</h2><div class="cards">'+''.join('<section class="card"><h2>'+A('/clusters/'+c+'/',label)+'</h2><p>'+str(sum(c in n['clusters']for n in ordered))+' piezas conectadas.</p></section>'for c,label in g['clusters'].items())+'</div>')
inventory={'schema':'atlas/public-reader-v1','graphSha256':DIGEST,'edition':g['edition'],'entry':url('/entrada.txt'),'graph':GRAPH,'counts':{'fichas':len(fichas),'concepts':len(concepts),'relations':len(E),'navigation':len(NAV),'documents':len(D)},'nodes':{n['id']:{'title':n['title'],'html':url(nodepath(n)),'text':url(nodepath(n)+'lectura.txt'),'data':url(nodepath(n)+'registro.json')}for n in ordered},'clusters':{c:url('/clusters/'+c+'/')for c in g['clusters']}}
put('inventario.json',json.dumps(inventory,ensure_ascii=False,separators=(',',':'))+'\n')
sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+H(url(path))+'</loc></url>'for path in html)+'</urlset>\n';put('sitemap.xml',sitemap)
put('README.txt','Mind Atlas: lectura pública completa\n\n'+entry+'\nGeneración: python scripts/build_atlas_public_reader.py\nVerificación: python scripts/build_atlas_public_reader.py --check\nEl generador lee el grafo canónico sin modificar fichas, relaciones ni documentos de origen.\n')
issues=[]
for path,data in files.items():
 target=STAGE/path
 if '--check'in sys.argv:
  if not target.is_file()or target.read_bytes()!=data:issues.append(path)
 else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
report={'graphSha256':DIGEST,'nodes':len(N),'relations':len(E),'htmlPages':len(html),'files':len(files),'bytes':sum(len(d)for d in files.values()),'sourceUntouched':True,'check':('--check'in sys.argv),'issues':issues,'pass':not issues}
print(json.dumps(report));sys.exit(bool(issues))
