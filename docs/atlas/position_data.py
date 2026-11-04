"""Document provenance, editable ficha compositions and reference token costs."""
from collections import defaultdict
from hashlib import sha256
from html.parser import HTMLParser
import json,math,os,re,sys
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,urljoin,parse_qsl,urlencode
from urllib.request import Request,urlopen
from atlas_topics import RULES,plain

ROOT=Path(__file__).resolve().parent
PUBLIC_ROOT=ROOT/'site' if (ROOT/'site').is_dir() else ROOT
ATLAS='https://dakleyer.github.io/perspective-beyond/atlas/'
LANDINGS={'eu':'E2','net':'N2','us':'U2','tegrity':'T1573','imsv':'S14',
 'totonacapan':'np-biografia','mobility':'E1953','latinoempresa':'L002','research':'GH049','dialogos':'D-067'}
EDITORIAL={
 'E2':{'empresa':45,'transformacion':25,'perspectiva':15,'decision':10,'navegacion':5},
 'N2':{'capacidad-humana':35,'empresa':25,'transformacion':25,'documentacion':10,'navegacion':5},
 'U2':{'empresa':40,'transformacion':35,'decision':10,'aprendizaje':10,'navegacion':5},
 'D-285':{'empresa':35,'transformacion':25,'representacion':20,'matematicas':10,'aprendizaje':5,'evidencia':5},
}

def normalized_url(value):
 u=urlsplit(value);query=[(k,v) for k,v in parse_qsl(u.query,keep_blank_values=True) if not k.startswith('utm_') and k not in {'gclid','fbclid'}]
 return urlunsplit(('https',u.netloc.lower().removeprefix('www.'),u.path.rstrip('/') or '/',urlencode(sorted(query)),''))

def normalize_weights(values):
 values={k:float(v) for k,v in values.items() if float(v)>0};total=sum(values.values())
 assert total>0
 exact={k:v/total*10000 for k,v in values.items()};units={k:math.floor(v) for k,v in exact.items()}
 for k in sorted(exact,key=lambda k:(-(exact[k]-units[k]),k))[:10000-sum(units.values())]:units[k]+=1
 return {k:v/10000 for k,v in sorted(units.items()) if v}

class Landing(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.hidden=0;self.main=0;self.anchors=[];self.current=None;self.para=None;self.paragraphs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in {'script','style','header','footer','nav'}:self.hidden+=1
  if tag=='main':self.main+=1
  if tag=='a' and not self.hidden and a.get('href'):self.current=[a['href'],[],self.main>0]
  if tag=='p' and not self.hidden:self.para=[]
 def handle_endtag(self,tag):
  if tag=='a' and self.current:
   self.anchors.append((self.current[0],' '.join(self.current[1]).strip(),self.current[2]));self.current=None
  if tag=='p' and self.para is not None:
   text=re.sub(r'\s+',' ',' '.join(self.para)).strip()
   if 90<=len(text)<=1200:self.paragraphs.append(text)
   self.para=None
  if tag in {'script','style','header','footer','nav'}:self.hidden=max(0,self.hidden-1)
  if tag=='main':self.main=max(0,self.main-1)
 def handle_data(self,text):
  if self.hidden:return
  if self.current:self.current[1].append(text)
  if self.para is not None:self.para.append(text)

def enrich_catalog(base,catalog):
 records=base['sources']+catalog['sources'];byid={r['id']:r for r in records}
 notes=catalog['editorial_cards'];membership=catalog['source_cluster']
 concepts=base['concepts']+catalog['concepts'];labels=defaultdict(list)
 for c in concepts:
  for sid in c['sources']:labels[sid].append(c.get('original_label') or c['label'])
 known=defaultdict(list)
 for r in records:known[normalized_url(r['url'])].append(r['id'])
 capture_file=PUBLIC_ROOT/'posicionamiento/landings.json'
 cached={}
 if os.environ.get('ATLAS_REFRESH_LANDINGS')!='1':
  if capture_file.exists():cached=json.loads(capture_file.read_bytes())
  elif (PUBLIC_ROOT/'global-catalog.json').exists():
   prior=json.loads((PUBLIC_ROOT/'global-catalog.json').read_bytes())
   cached=(prior.get('positioning') or {})|{'summaries':{sid:n.get('summary','') for sid,n in prior.get('editorial_cards',{}).items()}}
 observations=[];links=[]
 for cluster,sid in LANDINGS.items():
  # Research and Diálogos enter at their selected document rather than crawling a repository.
  if cluster in {'research','dialogos','latinoempresa'}:continue
  source=byid[sid];url=source['url']
  captured=next((r for r in cached.get('observations',[]) if r.get('source')==sid and 'error' not in r),None)
  if captured:
   observations.append(captured);links.extend(e for e in cached.get('navigation',[]) if e['from']==sid)
   if sid not in notes and cached.get('summaries',{}).get(sid):notes[sid]={'url':'../sources/'+source['slug']+'/','summary':cached['summaries'][sid],'question':''}
   continue
  try:
   body=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read()
   parser=Landing();parser.feed(body.decode('utf-8'))
   usable=[a for a in parser.anchors if a[2]] or parser.anchors
   seen=set()
   for href,label,_ in usable:
    absolute=urljoin(url,href);target=known.get(normalized_url(absolute),[])
    if not target or not label or href.startswith('#'):continue
    dest=next((x for x in target if membership[x]==cluster and x!=sid),next((x for x in target if x!=sid),None))
    if not dest or dest in seen:continue
    if byid[dest]['title'].lower() in {'legal notice','privacy policy','contact','contact us'}:continue
    seen.add(dest)
    links.append({'id':'position-nav-'+sid+'-'+dest,'from':sid,'to':dest,'kind':'reading linked from the document',
      'reading':'Desde «'+source['title']+'», el enlace «'+label[:160]+'» abre «'+byid[dest]['title']+'».',
      'evidence':url,'href':absolute})
    if len(seen)>=8:break
   if sid not in notes and parser.paragraphs:
    notes[sid]={'url':'../sources/'+source['slug']+'/', 'summary':parser.paragraphs[0][:600],'question':''}
   observations.append({'source':sid,'url':url,'sha256':sha256(body).hexdigest(),'links':len(seen)})
  except Exception as e:observations.append({'source':sid,'url':url,'error':type(e).__name__})
 assert all('error' not in r for r in observations),'A landing must be read successfully before refreshing its navigation'
 capture_file.parent.mkdir(parents=True,exist_ok=True)
 capture_file.write_text(json.dumps({'observed':'2026-11-04','observations':observations,'navigation':links,
  'summaries':{sid:notes.get(sid,{}).get('summary','') for sid in LANDINGS.values()}},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 overrides=catalog.get('tag_weight_overrides',EDITORIAL)
 reading_path=PUBLIC_ROOT/'posicionamiento/lecturas-fuentes.json'
 reading_records={r['id']:r for r in json.loads(reading_path.read_bytes())['records']} if reading_path.exists() else {}
 compositions={}
 for record in records:
  sid=record['id'];tags=catalog['source_tags'][sid]
  if sid in overrides:
   raw=dict(overrides[sid]);scale=sum(v for v in raw.values() if v>0)
   for tag in tags:
    if tag not in raw:raw=raw|{tag:scale*.02}
  else:
   excerpt=reading_records.get(sid,{}).get('text','')
   if excerpt:
    matches={tag:len(list(pattern.finditer(plain(excerpt)))) for tag,pattern in RULES.items()}
    tags=list(dict.fromkeys(tags+[tag for tag,count in sorted(matches.items(),key=lambda item:(-item[1],item[0])) if count>=2][:8]))
   fields=[(record['title'],4),(notes.get(sid,{}).get('summary',''),3),(' '.join(labels[sid]),1),(excerpt,2)]
   raw={tag:1+sum(weight*min(3,len(list(RULES[tag].finditer(plain(text))))) for text,weight in fields) for tag in tags}
  compositions[sid]=normalize_weights(raw)
  catalog['source_tags'][sid]=list(compositions[sid])
 for tag,topic in catalog['topics'].items():
  topic['sources']=[sid for sid,weights in compositions.items() if weights.get(tag,0)>0]
  topic['clusters']=sorted({membership[sid] for sid in topic['sources']})
 catalog['source_tag_weights']=compositions
 catalog['tag_weight_overrides']={sid:normalize_weights(profile) for sid,profile in overrides.items()}
 catalog['tag_weight_method']={'schema':'perspective-beyond/tag-composition-v1','unit':'proportion','sum':1,
  'method':'Editorial reading profile. Automatic compositions weight signals in the title (4), summary (3), linked concepts (1) and public extract when available (2), with a positive base for each previous tag. Explicit editorial profiles take precedence. Rounding to 10000 units.',
  'editorial_overrides':list(overrides),'editable':True}
 catalog['positioning']={'schema':'perspective-beyond/positioning-v1','url':'posicionamiento/',
  'defaultTokens':2000,'defaultSources':LANDINGS,
  'defaultDocuments':{key:notes.get(sid,{}).get('published_text_url') or notes.get(sid,{}).get('provenance',{}).get('url') or byid[sid]['url'] for key,sid in LANDINGS.items()},
  'navigation':links,'observations':observations}
 return catalog

def node_block(node,topics):
 tags='; '.join(topics[k]+' '+format(v*100,'.2f')+'%' for k,v in sorted(node['tagWeights'].items()))
 return '## '+node['title']+'\n'+node.get('reading',node['summary'])+'\nTags: '+tags+'\nCard: '+node['url']+'\n'+(
  'Source document: '+node['original']+'\n' if node.get('original') else '')+'\n'

def edge_block(edge,nodes):
 return nodes[edge[1]]['title']+' → '+nodes[edge[2]]['title']+' · '+edge[3]+'. '+edge[4]+(
  '\nRelationship source: '+edge[5] if edge[5] else '')+'\n\n'

def enrich_graph(graph,catalog):
 sys.path.insert(0,str(ROOT/'tokenizer_bot'))
 os.environ['TIKTOKEN_CACHE_DIR']=str(ROOT/'tokenizer_cache_bot')
 import tiktoken
 enc=tiktoken.get_encoding('o200k_base')
 public_root=ROOT/'site' if (ROOT/'site/dialogos/publico.json').exists() else ROOT
 public=json.loads((public_root/'dialogos/publico.json').read_bytes())
 dialogue_text={c['id']:c['body'] for c in public['cards']}
 reading_path=PUBLIC_ROOT/'posicionamiento/lecturas-fuentes.json'
 reading_records={r['id']:r for r in json.loads(reading_path.read_bytes())['records']} if reading_path.exists() else {}
 docs={};byid={n['id']:n for n in graph['nodes']};membership=catalog['source_cluster']
 for node in graph['nodes']:
  if node['type']=='ficha':
   weights=catalog['source_tag_weights'][node['id']]
   source=catalog['editorial_cards'].get(node['id'],{}).get('provenance',{}).get('url') or node['original']
   canonical=normalized_url(source)
   did='doc-'+sha256(canonical.encode()).hexdigest()[:18]
   if did not in docs:docs[did]={'id':did,'title':node['title'],'url':canonical,'fichas':[],'aliases':[]}
   docs[did]['fichas'].append(node['id']);node['documentId']=did
   docs[did]['aliases']+= [source]+node.get('aliases',[])
  else:
   refs=[e[1] for e in graph['edges'] if e[2]==node['id'] and e[6]=='apoyo']
   raw=defaultdict(float)
   for sid in refs:
    for k,v in catalog['source_tag_weights'][sid].items():raw[k]+=v
   weights=normalize_weights(raw or {'documentacion':1})
   node['sourceIds']=refs
  node['tagWeights']=weights
  node['tags']=list(weights)
  if node['id'] in dialogue_text:node['reading']=dialogue_text[node['id']]
  elif node['id'] in reading_records:
   record=reading_records[node['id']];node['reading']=record['text']
   node['readingSource']={k:record[k] for k in ['url','section','observed','sourceSha256']}
   node['readingSummary']=re.split(r'(?<=[.!?])\s+',record['text'])[0]
  node['contextTokens']=len(enc.encode(node_block(node,graph['topics'])))
  if node['type']=='concepto':node['positionHeaderTokens']=len(enc.encode('# Positioning · '+node['title']+'\nEntry concept: '+node['url']+'\n\n'))
 for document in docs.values():
  document['fichas'].sort();document['aliases']=sorted(set(document['aliases']))
  if len(document['fichas'])>5 and 'totonacapan.com' in document['url']:
   document['title']='Biografía de Iván Abril Palma · Instituto del Totonacapan'
  document['header']='# Positioning · '+document['title']+'\nSource document: '+document['url']+'\n\n'
  document['headerTokens']=len(enc.encode(document['header']))
 atlas_doc={'id':'doc-atlas','title':'Global Atlas · Perspective Beyond','url':ATLAS,'fichas':[],
  'entrySources':list(dict.fromkeys(LANDINGS.values())),'aliases':[],
  'header':'# Positioning · Global Atlas · Perspective Beyond\nSource document: '+ATLAS+'\n\n'}
 atlas_doc['headerTokens']=len(enc.encode(atlas_doc['header']))
 docs['doc-atlas']=atlas_doc
 for sid,groups in catalog.get('positioning',{}).get('overviewSources',{}).items():
  if sid in byid:docs[byid[sid]['documentId']]['coverageGroups']=groups
 graph['documents']=list(docs.values())
 graph['positionings']={k:{'source':sid,'document':byid[sid]['documentId'],'url':next(d['url'] for d in docs.values() if d['id']==byid[sid]['documentId'])} for k,sid in LANDINGS.items()}
 graph['positionings']['all']={'source':None,'document':'doc-atlas','url':ATLAS}
 graph['navigation']=[['navigation:'+e['id'],e['from'],e['to'],e['kind'],e['reading'],e['evidence'],'navegacion',''] for e in catalog['positioning']['navigation']]
 graph['edgeTokenCosts']={e[0]:len(enc.encode(edge_block(e,byid))) for e in graph['edges']+graph['navigation']}
 graph['voices']=catalog['focus_voices']
 graph['entryRoutes']=catalog['text_entries']
 graph['sessionProfiles']=catalog['session_profiles']
 graph['tokenization']={'encoding':'o200k_base','library':'tiktoken','version':tiktoken.__version__,
  'accounting':'Sum of independently encoded blocks: document header, card and incoming relationship. The budget applies to selected reading content.',
  'reference':'https://github.com/openai/tiktoken','nodeFormat':'positioning-node-v1','edgeFormat':'positioning-edge-v1'}
 return graph
