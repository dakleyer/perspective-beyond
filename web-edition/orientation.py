"""A compact, traceable orientation layer above the unchanged Atlas graph."""
from pathlib import Path
from collections import Counter,defaultdict
from hashlib import sha256
from html import escape
from urllib.parse import quote,urlsplit
import json,math,re,textwrap

HERE=Path(__file__).resolve().parent
PUBLIC_ENTRY='https://tegrity.ai/atlas-orientation/'
DIRECT_READER='https://tegrity.ai/atlas-reader/'
CONFIG_RULE='Retain the objective, entry point, mode, tags, weights and scope already indicated by the user or their URL. In closed mode, offer only cards from the permitted cluster. Do not ask again for a selection already resolved.'
AREAS=[
{'id':'perspectiva','title':'Changing the question','question':'What are we leaving out when formulating the problem?','description':'Observation frames, representations, limits of knowledge and translation between domains.','tags':['perspectiva','representacion','mundo-abierto','cartografia'],'seeds':['D-285','E1731','T1499']},
{'id':'formalizacion','title':'Formalising and testing','question':'What structure can be formulated and what observation allows it to be examined?','description':'Mathematical models, indeterminacy, experiments and evidence provenance.','tags':['matematicas','experimentacion','evidencia','documentacion'],'seeds':['N1817','N1828','sac-0b460b7d138063']},
{'id':'gobierno','title':'Governing decisions','question':'Who can decide and what control is sufficient?','description':'Authority, delegation, responsibility, AI integrity, standards and legitimacy.','tags':['autoridad','decision','control-minimo','integridad-ia','estandares','legitimidad'],'seeds':['T2729','GH021','T1475']},
{'id':'intervencion','title':'Making it happen','question':'How can intention become a capability that works?','description':'Transformation, value creation, distributed coordination, mobility and fieldwork.','tags':['empresa','transformacion','agentes','movilidad','compromisos','casos'],'seeds':['E1628','N1274','N1805','U2']},
{'id':'capacidad','title':'Preserving and transmitting capability','question':'What do people know how to do and how can that capability continue?','description':'Tacit knowledge, learning, human intelligence debt, community and lived experience.','tags':['capacidad-humana','aprendizaje','memoria-territorio','espiritualidad','encuentros'],'seeds':['N1287','T874','T1472','np-coaching','D-018']},
{'id':'adaptacion','title':'Sustaining value and adaptation','question':'What changes regime and what enables continued operation?','description':'Economics, liquidity, early warnings, constraints and adaptation to changing conditions.','tags':['economia','cambio-regimen','geopolitica','empresa','mundo-abierto'],'seeds':['T1387','N1826','E1654','D-137']},
{'id':'fuentes','title':'Finding the sources','question':'Where is the document and how is the corpus navigated?','description':'Entries, indexes and source locators. A navigation aid for the other reading paths.','tags':['navegacion'],'seeds':['N250','np-biografia']}
]
INTENTS=[
{'id':'transformacion','question':'A transformation is blocked: where should we intervene?','areas':['perspectiva','intervencion'],'seeds':['E1628','E1731','N1274'],'reason':'First change the level of observation; then connect a specific intervention with execution capability.'},
{'id':'racionalizacion','question':'There is complexity and unused capability: how can value be found?','areas':['intervencion','adaptacion'],'seeds':['E1704','E1662','E1654'],'reason':'Relate rationalisation and value discovery to a documented business case.'},
{'id':'tacito','question':'Modernisation is losing operators\' know-how.','areas':['capacidad','intervencion'],'seeds':['N1287','T874','T1472'],'reason':'Start with tacit knowledge; compare it with human intelligence debt and capability attribution.'},
{'id':'autoridad','question':'An agent can act, but what authority and control does it need?','areas':['gobierno','formalizacion'],'seeds':['T2729','GH021','T1499'],'reason':'Open the sufficient-control architecture and its conditions before expanding towards structural awareness.'},
{'id':'logistica','question':'How can many operational entities be coordinated in real time?','areas':['intervencion','adaptacion'],'seeds':['N864','N1805','N1803'],'reason':'Compare GEPLAN\'s logistics intelligence with xSeil\'s orchestration and routing mechanisms.'},
{'id':'regimen','question':'The rules have changed: what signals enable a timely response?','areas':['adaptacion','gobierno'],'seeds':['T1387','N1826','N1831'],'reason':'Combine sufficient change detection with liquidity and factor cascades in a case.'},
{'id':'matematicas','question':'I want to examine the mathematical formulation and its boundaries.','areas':['formalizacion','perspectiva'],'seeds':['N1817','N1815','sac-0b460b7d138063'],'reason':'Start with Companion Paper II v2.1 (N1817), which consolidates the formulation and resource accounting. N1815 retains the earlier v5 note as an antecedent to that revision. Then examine the dimensions of indeterminacy left open by the representation.'},
{'id':'pensamiento','question':'I want to understand Iván Abril\'s way of thinking.','areas':['perspectiva','capacidad'],'seeds':['D-285','np-coaching','D-137'],'reason':'Open a reflection on the architect\'s craft and continue towards experience, learning and economic promises.'},
{'id':'comunidad','question':'How is knowledge transmitted between people and communities?','areas':['capacidad','perspectiva'],'seeds':['np-coaching','N1287','D-018'],'reason':'Examine lived learning, tacit knowledge and spiritual experience within their own contexts.'},
{'id':'integracion','question':'How can a transaction between businesses become execution and value?','areas':['intervencion','gobierno'],'seeds':['U2','E1662','N1274'],'reason':'Start with business integration and continue through existing value and team coordination.'},
{'id':'atribucion','question':'An AI appears to perform well: who is contributing the capability?','areas':['capacidad','gobierno'],'seeds':['T1472','T1475','T874'],'reason':'Relate attribution, its measurement protocol and human intelligence debt.'}
]
H=lambda v:escape(str(v),quote=True)
def uri(n):
    kind='conceptos'if n['type']=='concepto'else'fichas'
    return '/'+kind+'/'+quote(n['id'],safe='')+'/'
def link(url,text):
    return '<a href="'+H(url)+'">'+H(text)+'</a>'
def build(root=HERE,own_origin='https://tegrity.ai',uploads='https://tegrity.ai/wp-content/uploads/2026/11/'):
    out=root/'dist';gpath=out/'perspective-beyond/atlas/mapa/grafo.json'
    raw=gpath.read_bytes();graph=json.loads(raw);before=sha256(raw).hexdigest()
    nodes={n['id']:n for n in graph['nodes']};area_map={a['id']:a for a in AREAS}
    for a in AREAS:
        assert all(s in nodes for s in a['seeds'])
    for i in INTENTS:assert all(s in nodes for s in i['seeds'])
    tag_areas=defaultdict(list)
    for a in AREAS:
        for t in a['tags']:tag_areas[t].append(a['id'])
    assert set(graph['topics'])<=set(tag_areas)
    memberships={};primary={}
    for n in nodes.values():
        weights=defaultdict(float)
        for t,w in n['tagWeights'].items():
            for area in tag_areas[t]:weights[area]+=w/len(tag_areas[t])
        assert abs(sum(weights.values())-1)<1e-8,n['id']
        memberships[n['id']]=dict(sorted(weights.items()))
        primary[n['id']]=sorted(weights,key=lambda a:(-weights[a],a))[0]
    bundles=defaultdict(list);internal=Counter()
    for e in graph['edges']:
        a,b=primary[e[1]],primary[e[2]]
        if a==b:internal[a]+=1
        else:bundles[(a,b)].append(e)
    bridges=[]
    for (a,b),rows in sorted(bundles.items()):
        informative=sorted(rows,key=lambda e:(not bool(e[4]),e[6]=='apoyo',e[0]))
        bridges.append({'from':a,'to':b,'count':len(rows),'kinds':dict(Counter(e[3]for e in rows)),
         'examples':[{'id':e[0],'from':e[1],'to':e[2],'kind':e[3],'reading':e[4],'evidence':e[5]}for e in informative[:3]],
         'edgeIds':[e[0]for e in rows]})
    areas=[]
    for a in AREAS:
        members=[k for k,v in memberships.items()if a['id']in v]
        members.sort(key=lambda k:(-memberships[k][a['id']],nodes[k]['title']))
        areas.append(a|{'members':members,'primaryCount':sum(v==a['id']for v in primary.values()),
         'memberCount':len(members),'internalRelations':internal[a['id']],
         'clusters':dict(Counter(c for k in members for c in nodes[k]['clusters']))})
    summary={'schema':'perspective-beyond/orientation-v1','sourceGraphSha256':before,'edition':graph['edition'],
      'purpose':'Understand the corpus and choose a positioning before configuring the assistant.',
      'publicEntry':PUBLIC_ENTRY,'directReader':DIRECT_READER,'configurationRule':CONFIG_RULE,
      'flow':['Understand the upper-level map','Formulate the visitor\'s question','Choose an area and two or three cards','Adjust perspective, scope and tokens','Open the reading and review the positioning'],
      'distinction':{'areas':'What question or mechanism you want to explore.','clusters':'In which institutional, practice or research context it appears.','fichas':'What texts and cases support that reading.','posicionamiento':'The specific document or card from which traversal begins.'},
      'counts':{'fichas':sum(n['type']=='ficha'for n in nodes.values()),'concepts':sum(n['type']=='concepto'for n in nodes.values()),'relations':len(graph['edges']),'clusters':len(graph['clusters']),'tags':len(graph['topics'])},
      'areas':[{k:v for k,v in a.items()if k!='members'}for a in areas],
      'bridges':[{k:v for k,v in b.items()if k!='edgeIds'}for b in bridges],'intents':INTENTS,
      'clusters':graph['clusters'],'topics':graph['topics'],
      'entryCards':{s:{'id':s,'title':nodes[s]['title'],'clusters':nodes[s]['clusters'],'web':summary_origin(root)+uri(nodes[s]),'original':nodes[s].get('original'),'documentId':nodes[s].get('documentId')}for s in dict.fromkeys(s for i in INTENTS for s in i['seeds'])}}
    full=summary|{'areas':areas,'bridges':bridges,'memberships':memberships,'primary':primary}
    def write(path,data):
        p=out/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data,encoding='utf8',newline='\n')
    def wrapper(title,body):
        return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+H(title)+' · Atlas</title><link rel="stylesheet" href="/atlas-web.css"></head><body><main><header><p class="kicker">Atlas · Orient first, then position</p><h1>'+H(title)+'</h1><nav class="actions">'+link('/','Complete Atlas')+link('/orientacion/','Upper-level map')+link('/entrada/','Assistant entry')+link('/orientacion/lectura.txt','Text summary')+'</nav></header><div class="body">'+body+'</div><footer>'+link('/fichas/','All cards')+' · '+link('/orientacion/modelo.json','Map and correspondences')+'</footer></main></body></html>\n'
    seed_card=lambda sid:'<li><strong>'+link(uri(nodes[sid]),nodes[sid]['title'])+'</strong><p class="meta">'+H(sid)+' · '+H(' / '.join(graph['clusters'][c]for c in nodes[sid]['clusters']))+'</p>'+('<p>'+link(nodes[sid]['original'],'Source publication')+'</p>'if nodes[sid].get('original')else'')+'</li>'
    positions={'perspectiva':(170,100),'formalizacion':(500,90),'gobierno':(830,110),'intervencion':(220,310),'capacidad':(550,310),'adaptacion':(860,330),'fuentes':(510,500)}
    svg=['<svg role="img" aria-label="Map of the Atlas\'s upper-level areas and main bridges" viewBox="0 0 1050 590" style="width:100%;height:auto"><title>One constellation, several entry questions</title>']
    for b in sorted(bridges,key=lambda b:-b['count'])[:14]:
        x1,y1=positions[b['from']];x2,y2=positions[b['to']]
        svg.append('<a href="/orientacion/puentes/'+b['from']+'-'+b['to']+'/"><path d="M'+str(x1)+' '+str(y1)+' L'+str(x2)+' '+str(y2)+'" stroke="#b7b8a8" stroke-width="'+str(1+math.log1p(b['count'])/4)+'" fill="none"><title>'+H(area_map[b['from']]['title']+' → '+area_map[b['to']]['title']+': '+str(b['count'])+' relaciones')+'</title></path></a>')
    for a in areas:
        x,y=positions[a['id']]
        words=textwrap.wrap(a['title'],width=25)
        label=''.join('<tspan x="'+str(x)+'" y="'+str(y-19+j*21)+'">'+H(line)+'</tspan>'for j,line in enumerate(words))
        svg.append('<a href="/orientacion/'+a['id']+'/"><rect x="'+str(x-138)+'" y="'+str(y-48)+'" width="276" height="96" rx="8" fill="#fffdf8" stroke="#98733d"/><text text-anchor="middle" fill="#172d39" style="font:18px Georgia,serif">'+label+'</text><text x="'+str(x)+'" y="'+str(y+29)+'" text-anchor="middle" fill="#425b65" style="font:14px system-ui">'+str(a['primaryCount'])+' entry pieces</text></a>')
    svg.append('</svg>')
    intro='<p class="lead">The Atlas connects how we observe a reality, how we decide and act within it, and what capabilities enable us to sustain and review what has been achieved.</p><p>Before asking for a cluster or card, understand the questions explored by the corpus. Areas group its topics; clusters show the contexts in which those ideas are developed. There is one constellation and its areas intersect.</p><section class="reading"><h2>How to choose an entry</h2><ol><li>Ask the visitor what they want to understand, solve or create.</li><li>Identify one or two map areas and offer two or three specific cards.</li><li>Explain why they serve that question. Then agree on scope, focus and reading budget.</li><li>If the question is broad, offer two paths and a single clarification question.</li></ol></section>'
    body=intro+'<p>'+H(CONFIG_RULE)+'</p>'+''.join(svg)+'<h2>The major questions</h2><div class="grid">'
    for a in areas:
        body+='<section class="card"><h2>'+link('/orientacion/'+a['id']+'/',a['title'])+'</h2><p><strong>'+H(a['question'])+'</strong></p><p>'+H(a['description'])+'</p><p class="meta">'+str(a['memberCount'])+' related pieces · '+str(a['primaryCount'])+' with this area as the main entry.</p></section>'
    body+='</div><h2>From a question to a positioning</h2><ul class="entries">'
    for i in INTENTS:
        body+='<li><h3>'+H(i['question'])+'</h3><p>'+H(i['reason'])+'</p><ul>'+''.join(seed_card(s)for s in i['seeds'])+'</ul></li>'
    body+='</ul><h2>Correspondences can be checked</h2><p>Upper-level groupings are calculated from existing tags. Bridges summarise existing relationships and retain their identifiers and examples. Each card has a main entry and may participate in several areas.</p><p>'+link('/orientacion/resumen.json','Structured summary')+' · '+link('/orientacion/modelo.json','Complete correspondences')+' · '+link('/orientacion/lectura.txt','Brief reading for the assistant')+'</p>'
    write('orientacion/index.html',wrapper('Understand the Atlas before choosing where to enter',body))
    for a in areas:
        text='<p class="lead">'+H(a['question'])+'</p><p>'+H(a['description'])+'</p><h2>Topics in this area</h2><div class="tags">'+''.join(link('/etiquetas/'+t+'/',graph['topics'][t])for t in a['tags'])+'</div><h2>Specific entries</h2><ul class="entries">'+''.join(seed_card(s)for s in a['seeds'])+'</ul><h2>Bridges to other questions</h2><ul>'
        for b in bridges:
            if b['from']==a['id']:text+='<li>'+link('/orientacion/puentes/'+b['from']+'-'+b['to']+'/',area_map[b['to']]['title'])+' · '+str(b['count'])+' recorded relationships.</li>'
        text+='</ul><h2>Cards and concepts in the area</h2><ul>'+''.join('<li>'+link(uri(nodes[s]),nodes[s]['title'])+'</li>'for s in a['members'])+'</ul>'
        write('orientacion/'+a['id']+'/index.html',wrapper(a['title'],text))
    by_edge={e[0]:e for e in graph['edges']}
    for b in bridges:
        text='<p>'+str(b['count'])+' graph relationships connect these two areas through their main entries.</p><h2>Reading examples</h2><ul class="entries">'
        for e in b['examples']:
            text+='<li><h3>'+link(uri(nodes[e['from']]),nodes[e['from']]['title'])+' → '+link(uri(nodes[e['to']]),nodes[e['to']]['title'])+'</h3><p><strong>'+H(e['kind'])+'</strong></p><p>'+H(e['reading'])+'</p><p class="meta">'+H(e['id'])+'</p></li>'
        text+='</ul><details><summary>Identifiers of grouped relationships</summary><p>'+H(', '.join(b['edgeIds']))+'</p></details>'
        write('orientacion/puentes/'+b['from']+'-'+b['to']+'/index.html',wrapper(area_map[b['from']]['title']+' → '+area_map[b['to']]['title'],text))
    lines=['ATLAS · ORIENTATION BEFORE POSITIONING','',
    'The corpus connects architectural thought, research, business intervention and human experience. Its cards form a network of documented relationships. First understand the upper-level map; then agree on a specific entry with the visitor.',
    'Do not start by asking someone unfamiliar with the corpus for a cluster. Ask what they want to understand, solve or create. Suggest two or three cards and explain the mechanism that makes them relevant. An area expresses a question; a cluster expresses a context. Positioning is the chosen document or card.',
    '',CONFIG_RULE,'Entry on the organisation\'s own domain: '+PUBLIC_ENTRY,'Direct reading of all clusters, cards and relationships: '+DIRECT_READER,'','AREA MAP']
    for a in areas:
        lines+=['',a['title']+' — '+a['question'],a['description'],'Topics: '+', '.join(graph['topics'][t]for t in a['tags'])+'.',
        'Entries: '+'; '.join(s+' · '+nodes[s]['title']for s in a['seeds'][:3]),'Explore further: '+summary_origin(root)+'/orientacion/'+a['id']+'/']
    lines+=['','QUESTIONS AND ENTRIES']
    for i in INTENTS:lines+=[i['question']+' → '+', '.join(i['seeds'])+'. '+i['reason']]
    lines+=['','LOCATE A CARD','To open a card ID, use '+summary_origin(root)+'/fichas/ID/ . Concepts open at /conceptos/ID/. The structured summary also links each entry\'s source publication.',
    '','NEXT STEP','Open two cards, check their context and offer the path. Adjust the selection according to what the visitor finds. For inherited configurations, retain the original URL parameters. When there is already an explicit objective, work from it.',
    'Upper-level map: '+summary_origin(root)+'/orientacion/','All cards: '+summary_origin(root)+'/fichas/','Complete correspondences: '+summary_origin(root)+'/orientacion/modelo.json','']
    write('orientacion/lectura.txt','\n'.join(lines))
    write('orientacion/resumen.json',json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    write('orientacion/modelo.json',json.dumps(full,ensure_ascii=False,indent=2)+'\n')
    integrate_entry(root)
    assert sha256(gpath.read_bytes()).hexdigest()==before
    return full

def integrate_entry(root):
    out=root/'dist'
    note='Direct Atlas reading on the organisation\'s own domain: '+DIRECT_READER+' . It offers all clusters, cards, concepts and relationships through Tegrity.AI text files. If this host returns 403 or cannot be opened, continue there while retaining the visitor\'s URL and configuration. Before choosing a positioning, read the upper-level map: '+PUBLIC_ENTRY+' . It contains the corpus\'s major questions, its bridges and cards to get started. If the visitor does not yet know the Atlas, start with their intention and offer two or three specific entries. '+CONFIG_RULE
    marker='<!-- atlas-orientation:start -->'
    block=marker+'<section class="reading"><p class="kicker">Direct reading on Tegrity.AI</p><h2>'+link(DIRECT_READER,'Connect your assistant to the Complete Atlas')+'</h2><p>All clusters, cards and relationships in public text files on the organisation\'s own domain.</p><p>'+link(PUBLIC_ENTRY,'Understand the Atlas before choosing where to enter')+' · '+link('/orientacion/','Explore areas and their bridges')+'</p></section><!-- atlas-orientation:end -->'
    for name in ['index.html','entrada/index.html']:
        path=out/name;html=path.read_text(encoding='utf8')
        if marker in html:html=re.sub(r'<!-- atlas-orientation:start -->.*?<!-- atlas-orientation:end -->',lambda m:block,html,flags=re.S)
        else:
            assert '<section class="body">'in html,name
            html=html.replace('<section class="body">','<section class="body">'+block,1)
        assert html.count(marker)==1,name
        path.write_text(html,encoding='utf8',newline='\n')
    for name in ['entrada.txt','llms.txt']:
        path=out/name;text=path.read_text(encoding='utf8')
        text=re.sub(r'\nPRIOR ORIENTATION\n.*?\nEND OF ORIENTATION\n','\n',text,flags=re.S)
        title,separator,rest=text.partition('\n')
        path.write_text(title+'\n\nPRIOR ORIENTATION\n'+note+'\nEND OF ORIENTATION\n'+rest,encoding='utf8',newline='\n')
    origin=summary_origin(root)
    paths=sorted('/'+p.relative_to(out).as_posix().removesuffix('index.html')for p in (out/'orientacion').rglob('index.html'))
    xml='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+H(origin+p)+'</loc></url>'for p in paths)+'</urlset>'
    (out/'sitemap-orientacion.xml').write_text(xml,encoding='utf8',newline='\n')
    path=out/'sitemap.xml';xml=path.read_text(encoding='utf8')
    loc=origin+'/sitemap-orientacion.xml'
    if loc not in xml:xml=xml.replace('</sitemapindex>','<sitemap><loc>'+H(loc)+'</loc></sitemap></sitemapindex>')
    path.write_text(xml,encoding='utf8',newline='\n')

def summary_origin(root):
    return json.loads((root/'dist/edicion/edicion.json').read_bytes())['publicOrigin']

if __name__=='__main__':
    model=build()
    print(json.dumps({'areas':len(model['areas']),'bridges':len(model['bridges']),'covered':len(model['memberships']),'relations':model['counts']['relations'],'sourceUnchanged':True},ensure_ascii=False,indent=2))

