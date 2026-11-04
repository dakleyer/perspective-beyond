"""Build the complete public web edition from a canonical Git revision.

Usage: python build_web.py REPOSITORY REVISION PUBLIC_ORIGIN
The output is the requested published web edition, never a project backup.
"""
from pathlib import Path
from collections import Counter,defaultdict
from hashlib import sha256
from html import escape
from urllib.parse import quote
import json,math,re,subprocess,sys

ROOT=Path(__file__).resolve().parent
REPO=Path(sys.argv[1]).resolve()
REVISION=sys.argv[2]
ORIGIN=sys.argv[3].rstrip('/')
OUT=ROOT/'dist'
CANON='https://dakleyer.github.io/perspective-beyond/'
def git(*args):
    return subprocess.check_output(['git','-C',str(REPO),*args])
assert re.fullmatch(r'[0-9a-f]{40}',REVISION)
assert ORIGIN.startswith('https://')
tree={}
for line in git('ls-tree','-r','-l',REVISION,'--','docs').decode().splitlines():
    meta,path=line.split('\t',1)
    mode,kind,oid,size=meta.split()
    assert kind=='blob' and mode=='100644'
    tree[path]={'oid':oid,'size':int(size)}
pipe=subprocess.Popen(['git','-C',str(REPO),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
def blob(path):
    pipe.stdin.write((tree[path]['oid']+'\n').encode());pipe.stdin.flush()
    header=pipe.stdout.readline().decode().split()
    data=pipe.stdout.read(int(header[2]));assert pipe.stdout.read(1)==b'\n'
    return data
def write(path,data):
    path=OUT/path
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data.encode('utf8')if isinstance(data,str)else data)
manifest=[]
for path,meta in tree.items():
    data=blob(path)
    destination='perspective-beyond/'+path.removeprefix('docs/')
    write(destination,data)
    manifest.append({'canonicalPath':path,'webPath':'/'+destination,'bytes':len(data),'sha256':sha256(data).hexdigest()})
pipe.stdin.close();pipe.stdout.close();pipe.wait()
graph=json.loads((OUT/'perspective-beyond/atlas/mapa/grafo.json').read_bytes())
nodes={n['id']:n for n in graph['nodes']}
docs={d['id']:d for d in graph['documents']}
edges=graph['edges']
navigation=graph.get('navigation',[])
assert len(nodes)>=1566 and len(edges)>=11832 and len(graph['nodes'])==len(nodes)
assert all(e[1]in nodes and e[2]in nodes for e in edges+navigation)
slugs={k:re.sub(r'[^a-zA-Z0-9_-]','_',k)for k in nodes}
assert len(set(slugs.values()))==len(slugs)
def node_path(n):
    return '/'+('conceptos'if n['type']=='concepto'else'fichas')+'/'+slugs[n['id']]+'/'
def doc_path(d):
    return '/documentos/'+d['id']+'/'
def h(text):
    return escape(str(text),quote=True)
def a(url,label):
    assert url.startswith(('https://','http://','/','#'))
    return '<a href="'+h(url)+'">'+h(label)+'</a>'
def original_url(url):
    return url.replace(CANON,ORIGIN+'/perspective-beyond/',1) if url.startswith(CANON)else url
def paras(text):
    return ''.join('<p>'+h(p).replace('\n','<br>')+'</p>'for p in re.split(r'\n\s*\n',str(text or ''))if p.strip())
css=(OUT/'perspective-beyond/atlas/asistentes/asistentes.css').read_text(encoding='utf8')+"""
main{max-width:76rem}h1{max-width:27ch;font-size:clamp(2rem,5vw,3.9rem)}.body{max-width:88ch;margin:2rem auto}
.entries{list-style:none;padding:0;display:grid;gap:.8rem}.entries>li{background:#fffdf8;border:1px solid var(--line);padding:1.1rem 1.3rem;min-width:0;overflow-wrap:anywhere}.entries h2{font-size:1.5rem;margin:.2rem 0 .7rem}.entries h3{margin:.2rem 0 .5rem}
.facts{display:flex;gap:.5rem 1.3rem;flex-wrap:wrap}.facts strong{font:1.5rem Georgia,serif}.pager{display:flex;flex-wrap:wrap;gap:.5rem;margin:1.5rem 0}.pager a{padding:.35rem .65rem;border:1px solid var(--line)}.tags{display:flex;gap:.4rem;flex-wrap:wrap}.tags a{border:1px solid var(--line);padding:.2rem .6rem;font-size:.9rem}
.meta{font-size:.83rem;color:var(--muted);overflow-wrap:anywhere}.reading{background:#fffdf8;border:1px solid var(--line);padding:clamp(1rem,3vw,2rem);margin:1rem 0}.reading p{max-width:78ch}.trail{border-left:2px solid var(--gold);padding-left:1rem}
@media(max-width:43rem){.grid{grid-template-columns:minmax(0,1fr)}}"""
write('atlas-web.css',css)
html_paths=[]
def page(path,title,body,lead=''):
    rel=path.strip('/')+'/index.html' if path!='/' else'index.html'
    canon=ORIGIN+path
    text='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+h(title)+' · Perspective Beyond</title><meta name="description" content="'+h(lead or 'Atlas de pensamiento: textos, conceptos, fuentes y relaciones navegables.')+'"><link rel="canonical" href="'+h(canon)+'"><link rel="stylesheet" href="/atlas-web.css"></head><body><main><header><p class="kicker">Perspective Beyond · Atlas completo en la web</p><h1>'+h(title)+'</h1>'+('<p class="lead">'+h(lead)+'</p>'if lead else'')+'<nav class="actions">'+a('/','Inicio')+a('/entrada/','Entrada para asistentes')+a('/fichas/','Fichas')+a('/conceptos/','Conceptos')+a('/relaciones/','Relaciones')+a('/clusters/','Clústeres')+a('/archivos/','Todos los archivos')+'</nav></header><section class="body">'+body+'</section><footer><p>'+a('/edicion/','Edición, integridad y procedencia')+' · '+a('/llms.txt','Guía en texto')+' · '+a('/perspective-beyond/atlas/','Atlas interactivo')+'</p><p class="meta">Repositorio canónico: '+a('https://github.com/dakleyer/perspective-beyond/tree/'+REVISION,'Perspective Beyond · '+REVISION[:7])+'. Esta edición permite recorrer los textos y relaciones desde páginas HTML, sin cuenta ni JavaScript.</p></footer></main></body></html>\n'
    write(rel,text);html_paths.append('/'+rel)
def list_page(path,title,items,render,lead='',size=60):
    total=max(1,math.ceil(len(items)/size))
    def url(i):
        return path if i==0 else path+'pagina-'+str(i+1)+'/'
    for p in range(total):
        pages='<nav class="pager" aria-label="Páginas">'+''.join(a(url(i),str(i+1))for i in range(total))+'</nav>'if total>1 else''
        body='<p class="meta">'+str(len(items))+' elementos · página '+str(p+1)+' de '+str(total)+'</p>'+pages+'<ul class="entries">'+''.join('<li>'+render(x)+'</li>'for x in items[p*size:(p+1)*size])+'</ul>'+pages
        page(url(p),title,body,lead)
def node_card(n):
    return '<h2>'+a(node_path(n),n['title'])+'</h2><p class="meta">'+h('Concepto'if n['type']=='concepto'else'Ficha')+' · '+h(' / '.join(graph['clusters'][c]for c in n['clusters']))+'</p>'+paras((n.get('summary')or n.get('reading')or'')[:420])
ordered=sorted(nodes.values(),key=lambda n:n['title'].casefold())
fichas=[n for n in ordered if n['type']=='ficha']
concepts=[n for n in ordered if n['type']=='concepto']
list_page('/fichas/','Fichas y fuentes',fichas,node_card,'Cada ficha reúne su pensamiento, procedencia y relaciones con el resto del Atlas.')
list_page('/conceptos/','Conceptos',concepts,node_card,'Las ideas del corpus, enlazadas con sus textos y casos.')
all_relations=edges+navigation
adj=defaultdict(list)
relation_where={}
for i,e in enumerate(all_relations):
    path='/relaciones/' if i//60==0 else'/relaciones/pagina-'+str(i//60+1)+'/'
    anchor='r-'+sha256(e[0].encode()).hexdigest()[:16]
    relation_where[e[0]]=path+'#'+anchor
    adj[e[1]].append(e);adj[e[2]].append(e)
def relation_card(e):
    return '<div id="'+h(relation_where[e[0]].split('#')[1])+'"><h2>'+a(node_path(nodes[e[1]]),nodes[e[1]]['title'])+' → '+a(node_path(nodes[e[2]]),nodes[e[2]]['title'])+'</h2><p><strong>'+h(e[3])+'</strong></p>'+paras(e[4])+('<p class="meta">Procedencia: '+a(original_url(e[5]),e[5])+'</p>'if e[5]and e[5].startswith(('http://','https://'))else'')+'<p class="meta">'+h(e[0])+'</p></div>'
list_page('/relaciones/','Relaciones del Atlas',all_relations,relation_card,'Cada conexión conserva su dirección, significado y procedencia. Los enlaces de navegación se identifican por separado.',size=60)
for n in ordered:
    path=node_path(n)
    primary=n.get('reading')or n.get('summary')or''
    body='<p class="meta">'+h('Concepto'if n['type']=='concepto'else'Ficha')+' · '+h(n['id'])+'</p><div class="tags">'+''.join(a('/clusters/'+c+'/',graph['clusters'][c])for c in n['clusters'])+'</div><section class="reading">'+paras(primary)+'</section>'
    body+='<h2>Composición y perspectivas</h2><div class="tags">'+''.join(a('/etiquetas/'+tag+'/',graph['topics'][tag]+' '+format(weight*100,'.2f')+' %')for tag,weight in sorted(n['tagWeights'].items(),key=lambda x:-x[1]))+'</div>'
    if n.get('readingSource'):
        source=n['readingSource'];body+='<p class="meta">Pasaje: '+h(source['section'])+' · lectura registrada '+h(source['observed'])+' · '+a(original_url(source['url']),'Fuente del pasaje')+'</p>'
    refs=[]
    if n.get('documentId')in docs:refs.append(a(doc_path(docs[n['documentId']]),'Documento de origen y sus fichas'))
    if n.get('original'):refs.append(a(original_url(n['original']),'Publicación de origen'))
    if n.get('commitUrl'):refs.append(a(n['commitUrl'],'Revisión de investigación'))
    refs.append(a('/perspective-beyond/atlas/posicionamiento/fichas/'+n['id']+'.json','Registro de datos'))
    refs.append(a(path+'lectura.txt','Leer esta ficha en texto UTF-8'))
    body+='<p class="actions">'+''.join(refs)+'</p>'
    relations=list({e[0]:e for e in adj[n['id']]}.values())
    pages=max(1,math.ceil(len(relations)/45))
    def npage(i):
        return path if i==0 else path+'relaciones-'+str(i+1)+'/'
    for i in range(pages):
        nav='<nav class="pager" aria-label="Relaciones de esta ficha">'+''.join(a(npage(j),'Relaciones '+str(j+1))for j in range(pages))+'</nav>'if pages>1 else''
        part=body if i==0 else'<p>'+a(path,'Volver al pensamiento y las fuentes de esta ficha')+'</p>'
        part+='<h2>Relaciones de esta pieza</h2><p>'+str(len(relations))+' conexiones en el Atlas.</p>'+nav+'<ul class="entries">'
        for e in relations[i*45:(i+1)*45]:
            other=nodes[e[2]if e[1]==n['id']else e[1]]
            part+='<li><h3>'+('→ 'if e[1]==n['id']else'← ')+a(node_path(other),other['title'])+'</h3><p><strong>'+h(e[3])+'</strong></p>'+paras(e[4])+'<p class="meta">'+a(relation_where[e[0]],'Leer esta relación en el conjunto del Atlas')+'</p></li>'
        part+='</ul>'+nav
        page(npage(i),n['title'],part)
    plain='# '+n['title']+'\n\n'+primary+'\n\nFicha web: '+ORIGIN+path+'\n\nRELACIONES\n'+''.join(nodes[e[1]]['title']+' → '+nodes[e[2]]['title']+'\n'+e[3]+'. '+e[4]+'\n'+ORIGIN+relation_where[e[0]]+'\n\n'for e in relations)
    write(path.strip('/')+'/lectura.txt',plain)
    # Text is available beside every HTML ficha without changing the source record.
doc_items=sorted(docs.values(),key=lambda d:d['title'].casefold())
for d in doc_items:
    body='<p>'+a(original_url(d['url']),'Publicación de origen')+'</p><h2>Fichas de este documento</h2><ul class="entries">'+''.join('<li>'+node_card(nodes[k])+'</li>'for k in d['fichas'])+'</ul>'
    page(doc_path(d),d['title'],body)
list_page('/documentos/','Documentos de origen',doc_items,lambda d:'<h2>'+a(doc_path(d),d['title'])+'</h2><p>'+str(len(d['fichas']))+' fichas de lectura.</p>')
for cluster,label in graph['clusters'].items():
    items=[n for n in ordered if cluster in n['clusters']]
    list_page('/clusters/'+cluster+'/',label,items,node_card,'Un recorrido de la misma constelación, con relaciones hacia sus otros clústeres.')
page('/clusters/','Clústeres de la constelación','<div class="grid">'+''.join('<section class="card"><h2>'+a('/clusters/'+c+'/',label)+'</h2><p>'+str(sum(c in n['clusters']for n in ordered))+' fichas y conceptos.</p></section>'for c,label in graph['clusters'].items())+'</div>')
for tag,label in graph['topics'].items():
    items=sorted((n for n in ordered if n['tagWeights'].get(tag,0)>0),key=lambda n:-n['tagWeights'][tag])
    list_page('/etiquetas/'+tag+'/',label,items,lambda n:node_card(n)+'<p class="meta">Peso en esta ficha: '+format(n['tagWeights'][tag]*100,'.2f')+' %</p>')
page('/etiquetas/','Etiquetas y perspectivas','<div class="tags">'+''.join(a('/etiquetas/'+t+'/',label)for t,label in graph['topics'].items())+'</div>')
def archive_card(record):
    path=record['webPath']
    return '<h2>'+a(path,record['canonicalPath'].removeprefix('docs/'))+'</h2><p class="meta">'+format(record['bytes'],',')+' bytes · SHA-256 '+record['sha256']+'</p>'
list_page('/archivos/','Todos los archivos del Atlas',manifest,archive_card,'Los '+format(len(manifest),',').replace(',','.')+' archivos de la edición canónica están disponibles desde este servidor, con su contenido original.',size=80)
entry_text='''ATLAS COMPLETO · ENTRADA PARA ASISTENTES

Esta web contiene la edición completa del Atlas de Perspective Beyond. Puedes recorrerla mediante HTML, sin iniciar sesión, sin ejecutar JavaScript y sin abrir GitHub.
Empieza por la pregunta del usuario y elige el clúster o las etiquetas pertinentes. Conserva la configuración de alcance y el formato que te haya solicitado.
Cada ficha contiene su texto de lectura, composición, procedencia y relaciones. Sigue las conexiones explicadas para comprender el mecanismo. Las páginas de relaciones permiten leer el conjunto en ambos sentidos.
Usa los nombres legibles en tu respuesta y enlaza las páginas web de las fichas. Conserva la secuencia temporal de los originales; al desarrollar una aplicación nueva, preséntala como una elaboración sobre el pensamiento de origen.
Si el usuario pide una web, un documento, audio o vídeo, utiliza este pensamiento como contenido y tus herramientas para darle ese formato.
'''+ '\nRECORRIDOS\n'+'\n'.join(label+': '+ORIGIN+path for label,path in [('Clústeres','/clusters/'),('Etiquetas','/etiquetas/'),('Fichas','/fichas/'),('Conceptos','/conceptos/'),('Relaciones','/relaciones/'),('Documentos','/documentos/'),('Todos los archivos','/archivos/'),('Fuentes autocontenidas','/perspective-beyond/atlas/asistentes/')])+'\n\nLa edición de origen y las huellas de los archivos están en '+ORIGIN+'/edicion/ . El repositorio de GitHub conserva la fuente canónica; la lectura del Atlas puede completarse en esta web.\n'
write('entrada.txt',entry_text)
page('/entrada/','Entrada para asistentes',paras(entry_text)+'<h2>Entradas por clúster</h2><ul>'+''.join('<li>'+a('/clusters/'+c+'/',label)+'</li>'for c,label in graph['clusters'].items())+'</ul><p>'+a('/entrada.txt','Abrir estas instrucciones como texto UTF-8')+'</p>','Una sola entrada web para recorrer los textos y las relaciones del Atlas completo.')
page('/','Una constelación de pensamiento, abierta en la web','<div class="facts"><strong>'+format(len(fichas),",").replace(",",".")+' fichas</strong><strong>'+str(len(concepts))+' conceptos</strong><strong>'+format(len(edges),",").replace(",",".")+' relaciones</strong><strong>'+str(sum(n["clusters"]==["dialogos"]for n in fichas))+' diálogos</strong></div><p>Explora el pensamiento desde sus textos, casos y conexiones. Esta edición reúne los archivos completos del Atlas y una red de páginas HTML para recorrerlo como persona o con tu asistente.</p><div class="actions"><a class="button" href="/entrada/">Conecta tu asistente</a><a class="button secondary" href="/clusters/">Explorar los clústeres</a>'+a('/perspective-beyond/atlas/','Abrir el mapa interactivo')+'</div><h2>Elige una perspectiva</h2><div class="grid">'+''.join('<section class="card"><h2>'+a('/clusters/'+c+'/',label)+'</h2><p>'+str(sum(c in n['clusters']for n in ordered))+' piezas conectadas con el corpus.</p></section>'for c,label in graph['clusters'].items())+'</div><section class="card"><h2>El Atlas completo, pieza a pieza</h2><p>'+a('/fichas/','Leer las fichas')+' · '+a('/conceptos/','Comprender los conceptos')+' · '+a('/relaciones/','Seguir las relaciones')+' · '+a('/etiquetas/','Cruzar perspectivas')+'</p><p>'+a('/documentos/','Documentos de origen')+' · '+a('/archivos/','Todos los archivos publicados')+' · '+a('/perspective-beyond/atlas/asistentes/','Fuentes autocontenidas para crear con tu asistente')+'</p></section>','Una web completa para personas y asistentes. El mismo corpus, navegable mediante textos, conceptos y relaciones.')
edition={'canonicalRepository':'https://github.com/dakleyer/perspective-beyond','canonicalRevision':REVISION,'canonicalEdition':graph['edition'],'publicOrigin':ORIGIN,'canonicalFiles':len(manifest),'canonicalBytes':sum(m['bytes']for m in manifest),'fichas':len(fichas),'concepts':len(concepts),'relations':len(edges),'navigationLinks':len(navigation),'documents':len(docs),'dialogues':sum(n['clusters']==['dialogos']for n in fichas),'allCanonicalFilesIdentical':True}
write('edicion/archivos.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
write('edicion/edicion.json',json.dumps(edition,ensure_ascii=False,indent=2)+'\n')
page('/edicion/','Edición y procedencia','<p>Esta publicación reproduce los '+str(len(manifest))+' archivos de la edición canónica, con sus bytes originales. La capa HTML de lectura reúne las fichas y relaciones del mismo grafo.</p><p>'+a('https://github.com/dakleyer/perspective-beyond/tree/'+REVISION,'Revisión canónica '+REVISION)+'</p><p>'+a('/edicion/edicion.json','Metadatos de edición')+' · '+a('/edicion/archivos.json','Inventario y SHA-256 de todos los archivos')+'</p><p>'+str(edition['canonicalBytes'])+' bytes de archivos canónicos · '+str(len(nodes))+' piezas · '+str(len(edges))+' relaciones del grafo · '+str(len(navigation))+' enlaces de navegación.</p>')
write('llms.txt','# Perspective Beyond · Atlas completo\n\n> Textos, conceptos y relaciones disponibles en HTML público. No requieren GitHub, inicio de sesión ni JavaScript.\n\n'+entry_text)
all_html=sorted(set(html_paths+['/'+m['webPath'].lstrip('/')for m in manifest if m['webPath'].endswith('.html')]))
# HTML sitemap entries use their directly served file paths.
sitemaps=[]
for start in range(0,len(all_html),1000):
    name='sitemaps/parte-'+str(start//1000+1)+'.xml'
    content='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+h(ORIGIN+p)+'</loc></url>'for p in all_html[start:start+1000])+'</urlset>'
    write(name,content);sitemaps.append('/'+name)
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<sitemap><loc>'+h(ORIGIN+p)+'</loc></sitemap>'for p in sitemaps)+'</sitemapindex>')
write('robots.txt','User-agent: *\nAllow: /\n\nSitemap: '+ORIGIN+'/sitemap.xml\n')
write('404.html','<!doctype html><html lang="es"><meta charset="utf-8"><title>Recorrer el Atlas</title><h1>Recorrer el Atlas</h1><p>'+a('/entrada/','Abrir la entrada de lectura del Atlas')+'</p></html>')
print(json.dumps(edition|{'newHTMLPages':len(html_paths),'totalFiles':sum(p.is_file()for p in OUT.rglob('*'))},ensure_ascii=False,indent=2))

