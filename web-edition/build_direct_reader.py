"""Build a directly served text edition for readers unable to open the hosted mirror."""
from pathlib import Path
from hashlib import sha256
from collections import Counter,defaultdict
import json
ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
OUT=ROOT/'direct-reader';OUT.mkdir(exist_ok=True)
raw=(DIST/'perspective-beyond/atlas/mapa/grafo.json').read_bytes()
digest=sha256(raw).hexdigest();g=json.loads(raw)
prefix='atlas-'+digest[:8]+'-'
base='https://tegrity.ai/wp-content/uploads/2026/11/'
entry='https://tegrity.ai/atlas-reader/'
files={};records={};node_packet={};edge_packet={}
def filename(kind,i=None):return prefix+kind+('-'+str(i+1).zfill(3)if i is not None else'')+'.txt'
def put(name,obj):
 records[name]=obj
 data=('# Perspective Beyond · Lectura directa del Atlas\n\nTexto público para personas y asistentes. Cada registro conserva sus identificadores y enlaces.\n\n```json\n'+json.dumps(obj,ensure_ascii=False,indent=2)+'\n```\n').encode()
 assert len(data)<1_950_000
 files[name]=data
def chunks(items,limit=90000):
 groups=[];current=[];size=0
 for item in items:
  n=len(json.dumps(item,ensure_ascii=False,indent=2).encode())
  if current and size+n>limit:groups.append(current);current=[];size=0
  current.append(item);size+=n
 if current:groups.append(current)
 return groups
node_chunks=chunks(g['nodes']);edge_chunks=chunks(g['edges'])
for i,rows in enumerate(node_chunks):
 for n in rows:node_packet[n['id']]=base+filename('fichas',i)
for i,rows in enumerate(edge_chunks):
 for e in rows:edge_packet[e[0]]=base+filename('relaciones',i)
by_node=defaultdict(list)
for e in g['edges']:
 by_node[e[1]].append(e);by_node[e[2]].append(e)
config='Conserva punto de entrada, modo, pesos, etiquetas, alcance y propósito de la URL del visitante. Si no están elegidos, lee la orientación, pregunta qué quiere comprender, resolver o crear y ofrece dos o tres entradas pertinentes. En modo cerrado consulta contenido del clúster permitido; en poroso sigue el puente elegido; en federado sigue las relaciones registradas.'
def ficha_link(sid):return {'id':sid,'title':next(n['title']for n in g['nodes']if n['id']==sid),'url':node_packet[sid],'locate':'Busca el registro con id '+sid+' en nodes.'}
for i,rows in enumerate(node_chunks):
 ids={n['id']for n in rows};links={}
 for sid in ids:
  related=by_node[sid]
  links[sid]={'relationCount':len(related),'allRelationFiles':sorted({edge_packet[e[0]]for e in related}),
   'outgoingExamples':[{ 'id':e[0],'to':e[2],'relationUrl':edge_packet[e[0]],'targetUrl':node_packet[e[2]]}for e in [e for e in related if e[1]==sid][:12]],
   'incomingExamples':[{ 'id':e[0],'from':e[1],'relationUrl':edge_packet[e[0]],'sourceUrl':node_packet[e[1]]}for e in [e for e in related if e[2]==sid][:12]],
   'readAll':'Los ejemplos ayudan a empezar. Para todas las conexiones abre allRelationFiles y conserva las filas cuyo from o to sea '+sid+'.'}
 put(filename('fichas',i),{'schema':'atlas/direct-nodes-v1','entry':entry,'graphSha256':digest,'configurationRule':config,'nodes':rows,'connections':links})
for i,rows in enumerate(edge_chunks):
 put(filename('relaciones',i),{'schema':'atlas/direct-edges-v1','entry':entry,'graphSha256':digest,
 'columns':g.get('edgeColumns')or['id','from','to','label','reading','evidence','kind'],'edges':rows,
 'endpoints':{sid:ficha_link(sid)for sid in sorted({e[j]for e in rows for j in [1,2]})}})
for cid,label in g['clusters'].items():
 nodes=[n for n in g['nodes']if cid in n['clusters']]
 pieces=[{'id':n['id'],'title':n['title'],'type':n['type'],'summary':n.get('summary')or(n.get('reading')or'')[:300],
 'tagWeights':n['tagWeights'],'url':node_packet[n['id']],'original':n.get('original')}for n in sorted(nodes,key=lambda n:n['title'].casefold())]
 parts=[]
 for i in range(0,len(pieces),60):
  page=pieces[i:i+60];name=filename('indice-'+cid,i//60)
  put(name,{'schema':'atlas/direct-cluster-index-v1','cluster':cid,'page':i//60+1,'pieces':page,'entry':entry})
  parts.append({'url':base+name,'from':page[0]['title'],'to':page[-1]['title'],'count':len(page)})
 put(filename('cluster-'+cid),{'schema':'atlas/direct-cluster-v1','cluster':cid,'title':label,'entry':entry,'configurationRule':config,
 'count':len(nodes),'themes':dict(Counter(t for n in nodes for t in n['tagWeights'])),
 'indexParts':parts,'findById':base+filename('localizador')})
put(filename('documentos'),{'schema':'atlas/direct-documents-v1','documents':g['documents'],'fichaUrls':node_packet})
put(filename('navegacion'),{'schema':'atlas/direct-navigation-v1','navigation':g.get('navigation',[]),'fichaUrls':node_packet})
orientation=json.loads((DIST/'orientacion/resumen.json').read_bytes())
for n in orientation['entryCards'].values():n['directUrl']=node_packet[n['id']]
put(filename('orientacion'),orientation)
index={'schema':'atlas/direct-entry-v1','entry':entry,'purpose':'Atlas íntegro de fichas, conceptos y relaciones, servido como texto en Tegrity.AI. No requiere el dominio chatgpt.site ni GitHub para recorrer el grafo.',
 'configurationRule':config,'graphSha256':digest,'edition':g['edition'],
 'parameters':{'cluster':'ID de clúster de la lista; varios separados por coma.','alcance':'cerrado, poroso o federado. Poroso requiere puente elegido.','posicionamiento':'ID de ficha, documento o URL de origen.','rol':'lector, embajador, consultor, investigador o personalizado.','lectura':'paraphrase, explore, ideas, locate o quote.','enfoque':'parejo, transversal o personalizado.','peso':'Parámetro repetible etiqueta:peso. Conserva los pesos del lector.','tokens':'Presupuesto de lectura solicitado.','instruccion':'Instrucciones del lector para esta sesión.'},
 'scopeRule':'Una selección previa prevalece. En una URL parcial pregunta solo por lo que falta. Sin selección, orienta desde la pregunta. Los enlaces de un archivo no amplían el alcance acordado.',
 'counts':{'fichas':sum(n['type']=='ficha'for n in g['nodes']),'concepts':sum(n['type']=='concepto'for n in g['nodes']),'relations':len(g['edges']),'navigation':len(g.get('navigation',[])),'documents':len(g['documents'])},
 'orientation':base+filename('orientacion'),
 'clusters':[{'id':c,'title':t,'url':base+filename('cluster-'+c),'count':sum(c in n['clusters']for n in g['nodes'])}for c,t in g['clusters'].items()],
 'lookup':{'url':base+filename('localizador'),'instruction':'Busca el ID de la ficha o relación. Abre su archivo y localiza el registro por su ID. Los enlaces connections llevan a las fichas vecinas y a la relación completa.'},
 'documents':base+filename('documentos'),'navigation':base+filename('navegacion'),
 'nodeParts':[base+filename('fichas',i)for i in range(len(node_chunks))],
 'edgeParts':[base+filename('relaciones',i)for i in range(len(edge_chunks))]}
put(filename('entrada'),index)
put(filename('localizador'),{'schema':'atlas/direct-lookup-v1','entry':entry,'nodes':node_packet,'edgeFiles':index['edgeParts']})
manifest=[]
for name,data in files.items():
 (OUT/name).write_bytes(data);manifest.append({'name':name,'url':base+name,'bytes':len(data),'sha256':sha256(data).hexdigest()})
# Reconstruct every original record from the publication, without inferred or lost fields.
back_nodes=[n for name,obj in records.items()if name.startswith(prefix+'fichas-')for n in obj['nodes']]
back_edges=[e for name,obj in records.items()if name.startswith(prefix+'relaciones-')for e in obj['edges']]
assert back_nodes==g['nodes']and back_edges==g['edges']
assert len(node_packet)==len(g['nodes'])and len(edge_packet)==len(g['edges'])
report={'graphSha256':digest,'nodesUnchanged':True,'edgesUnchanged':True,'counts':index['counts'],'files':manifest,'entry':entry,'textEntry':base+filename('entrada'),'bytes':sum(len(d)for d in files.values()),'largest':max(len(d)for d in files.values()),'pass':True}
(OUT/'publication-plan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in report.items()if k!='files'}|{'fileCount':len(files)},ensure_ascii=False,indent=2))
