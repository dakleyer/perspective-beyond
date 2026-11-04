"""Check additive Atlas releases against an existing Git commit.

No historical payload is written to disk. Reweighting and reading costs may
change; source text, stable IDs, provenance and relationships remain inspectable.
"""
from pathlib import Path
import argparse,json,re,subprocess,sys

SECTIONS={'docs/data/atlas.json':['sources','concepts','relations','documentRelations','readingLinks','articleMaps'],
 'docs/atlas/global-catalog.json':['sources','relations','concepts','concept_relations','editorial_cards'],
 'docs/atlas/mapa/grafo.json':['nodes','edges','documents'],
 'docs/atlas/dialogos/publico.json':['cards','concepts','relations']}
DERIVED={'tagWeights','source_tag_weights','contextTokens','tokenCost','tokenCosts','weights'}
def key(x):
 if isinstance(x,dict):return str(x.get('id',x.get('source',json.dumps(x,sort_keys=True))))
 if isinstance(x,list):return str(x[0])
 return str(x)
def index(values):
 if isinstance(values,dict):return values
 return {key(x):x for x in values}
def preserve(old,new,path,issues):
 if old==new:return
 if isinstance(old,dict)and isinstance(new,dict):
  for k,v in old.items():
   if k in DERIVED:continue
   if k not in new:issues.append(path+'/'+k+': field removed')
   else:preserve(v,new[k],path+'/'+k,issues)
 elif isinstance(old,list)and isinstance(new,list):
  if old and isinstance(old[0],dict)and ('id'in old[0]or'source'in old[0]):
   before=index(old);after=index(new)
   for k,v in before.items():
    if k not in after:issues.append(path+'/'+k+': record removed')
    else:preserve(v,after[k],path+'/'+k,issues)
  else:
   for v in old:
    if v not in new:issues.append(path+': list item removed')
 elif isinstance(old,str)and isinstance(new,str):
  if old and old not in new:issues.append(path+': previous text replaced or truncated')
 else:issues.append(path+': previous value changed')
def compare_section(before,after,path):
 issues=[];a=index(before);b=index(after)
 if isinstance(after,list)and len(b)!=len(after):issues.append(path+': duplicate stable IDs')
 for id_,old in a.items():
  if id_ not in b:issues.append(path+'/'+id_+': stable ID removed')
  elif isinstance(old,list)and old!=b[id_]:issues.append(path+'/'+id_+': relationship payload or direction changed')
  else:preserve(old,b[id_],path+'/'+id_,issues)
 return issues
def graph_issues(g):
 issues=[];nodes=g['nodes'];ids={n['id']for n in nodes};fields=g['edgeFields'];fi=fields.index('from');ti=fields.index('to');edgeids=[e[0]for e in g['edges']]
 if len(ids)!=len(nodes):issues.append('graph: duplicate node IDs')
 if len(set(edgeids))!=len(edgeids):issues.append('graph: duplicate edge IDs')
 for e in g['edges']:
  if e[fi]not in ids or e[ti]not in ids:issues.append('graph/'+str(e[0])+': dangling endpoint')
 return issues
def run(repo,base,head):
 def git(*a):return subprocess.check_output(['git','-C',str(repo),*a])
 for ref in(base,head):
  if not re.fullmatch(r'[a-f0-9]{40}',ref):raise ValueError('Use exact commit SHAs')
 result={'base':base,'head':head,'sections':{},'issues':[]}
 for path,sections in SECTIONS.items():
  new=json.loads(git('show',head+':'+path));old=json.loads(git('show',base+':'+path))
  for section in sections:
   before=old.get(section,{});after=new.get(section,{})
   result['sections'][path+'#'+section]={'before':len(before),'after':len(after)}
   result['issues']+=compare_section(before,after,path+'#'+section)
  if path.endswith('/grafo.json'):result['issues']+=graph_issues(new)
 removed=git('diff','--name-only','--diff-filter=D',base,head,'--','docs/atlas','docs/data').decode().splitlines()
 result['issues'] += [p+': tracked Atlas file removed'for p in removed]
 public=json.loads(git('show',head+':docs/atlas/dialogos/publico.json'))
 norm=lambda s:re.sub(r'\s+',' ',s).strip()
 for c in public['cards']:
  path='docs/atlas/dialogos/textos/'+c['id'].lower()+'.txt'
  try:text=git('show',head+':'+path).decode()
  except subprocess.CalledProcessError:result['issues'].append(path+': full text missing');continue
  if norm(c['body'])not in norm(text):result['issues'].append(path+': body missing or truncated')
 result['pass']=not result['issues'];return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',default='.');p.add_argument('--base',required=True);p.add_argument('--head',required=True);p.add_argument('--out');a=p.parse_args()
 report=run(Path(a.repo),a.base,a.head);text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
 if a.out:Path(a.out).write_text(text,encoding='utf8')
 print(text);sys.exit(0 if report['pass']else 1)
