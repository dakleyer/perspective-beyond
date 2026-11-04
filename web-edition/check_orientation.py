"""Check the orientation projection without changing the source graph."""
from pathlib import Path
from collections import Counter,deque
import json
R=Path(__file__).resolve().parent
m=json.loads((R/'dist/orientacion/modelo.json').read_bytes())
g=json.loads((R/'dist/perspective-beyond/atlas/mapa/grafo.json').read_bytes())
nodes={n['id']:n for n in g['nodes']};edges={e[0]:e for e in g['edges']}
checks=0
def check(condition,message):
 global checks
 if not condition:raise AssertionError(message)
 checks+=1
check(set(m['memberships'])==set(nodes),'All fichas and concepts must be mapped')
check(set(m['primary'])==set(nodes),'Every piece needs a primary entry')
check(sum(a['primaryCount']for a in m['areas'])==len(nodes),'Primary areas must partition the substrate')
for sid,weights in m['memberships'].items():
 check(abs(sum(weights.values())-1)<1e-8,'Area profile does not sum to one: '+sid)
 check(m['primary'][sid]in weights,'Primary entry not represented: '+sid)
mapped=[]
for b in m['bridges']:
 check(b['count']==len(b['edgeIds']),'Bridge count mismatch')
 for rid in b['edgeIds']:
  e=edges[rid]
  check(m['primary'][e[1]]==b['from']and m['primary'][e[2]]==b['to'],'Incorrect bridge mapping')
  mapped.append(rid)
check(len(mapped)==len(set(mapped)),'An original relation was counted twice')
internal=sum(a['internalRelations']for a in m['areas'])
check(internal+len(mapped)==len(edges),'Every relation must be internal or in a bridge')
check(set(g['topics'])==set(t for a in m['areas']for t in a['tags']),'A theme is missing')
seed_counts=Counter(s for i in m['intents']for s in i['seeds'])
check(max(seed_counts.values())<=3,'Reading paths are becoming radial')
check(len(seed_counts)>=24,'Too few distinct points of entry')
adj={sid:{}for sid in nodes}
for e in g['edges']+g.get('navigation',[]):adj[e[1]][e[2]]=e;adj[e[2]][e[1]]=e
routes=[]
for intent in m['intents']:
 check(len(set(intent['seeds']))==3,'Each path needs three distinct candidate entries')
 for sid in intent['seeds']:check(sid in nodes,'Unknown entry')
 start=intent['seeds'][0]
 distance={start:0};parents={};q=deque([start])
 while q:
  at=q.popleft()
  for dest in adj[at]:
   if dest not in distance:distance[dest]=distance[at]+1;parents[dest]=(at,adj[at][dest]);q.append(dest)
 hops=[distance.get(s)for s in intent['seeds'][1:]]
 check(all(x is not None and x<=6 for x in hops),'A reading path is not connected in the real graph: '+intent['id'])
 paths=[]
 for target in intent['seeds'][1:]:
  path=[];at=target
  while at!=start:
   at,e=parents[at];path.append({'id':e[0],'kind':e[6]})
  paths.append(list(reversed(path)))
 routes.append({'id':intent['id'],'question':intent['question'],'candidateEntries':intent['seeds'],'graphDistances':hops,'supportPaths':paths})
for file in ['index.html','entrada/index.html']:
 text=(R/'dist'/file).read_text(encoding='utf8')
 check(text.count('atlas-orientation:start')==1,'Missing or duplicate first orientation: '+file)
 check(m['publicEntry']in text,'Own-domain entry missing: '+file)
for file in ['entrada.txt','llms.txt']:
 text=(R/'dist'/file).read_text(encoding='utf8')
 check(text.count('PRIOR ORIENTATION')==1,'Missing or duplicate assistant protocol: '+file)
 check(m['configurationRule']in text,'Existing user configuration not preserved: '+file)
report={'checks':checks,'passed':checks,'areas':len(m['areas']),'bridges':len(m['bridges']),'coveredPieces':len(nodes),
'originalRelations':len(edges),'internalRelations':internal,'interAreaRelations':len(mapped),'distinctCandidateEntries':len(seed_counts),
'maximumReusedEntry':max(seed_counts.values()),'routes':routes,'sourceGraphSha256':m['sourceGraphSha256'],'pass':True}
(R/'orientation_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))

