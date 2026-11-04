"""A compact, traceable orientation layer above the unchanged Atlas graph."""
from pathlib import Path
from collections import Counter,defaultdict
from hashlib import sha256
from html import escape
from urllib.parse import quote,urlsplit
import json,math,re,textwrap

HERE=Path(__file__).resolve().parent
PUBLIC_ENTRY='https://tegrity.ai/atlas-orientation/'
CONFIG_RULE='Conserva el objetivo, punto de entrada, modo, etiquetas, pesos y alcance ya indicados por el usuario o por su URL. En un modo cerrado, ofrece solamente fichas del clúster permitido. No vuelvas a pedir una selección ya resuelta.'
AREAS=[
{'id':'perspectiva','title':'Cambiar la pregunta','question':'¿Qué estamos dejando fuera al formular el problema?','description':'Marcos de observación, representaciones, límites del conocimiento y traducción entre dominios.','tags':['perspectiva','representacion','mundo-abierto','cartografia'],'seeds':['D-285','E1731','T1499']},
{'id':'formalizacion','title':'Formalizar y contrastar','question':'¿Qué estructura se puede formular y qué observación permite examinarla?','description':'Modelos matemáticos, indeterminación, experimentos y procedencia de la evidencia.','tags':['matematicas','experimentacion','evidencia','documentacion'],'seeds':['N1817','N1828','sac-0b460b7d138063']},
{'id':'gobierno','title':'Gobernar decisiones','question':'¿Quién puede decidir y qué control resulta suficiente?','description':'Autoridad, delegación, responsabilidad, integridad de IA, estándares y legitimidad.','tags':['autoridad','decision','control-minimo','integridad-ia','estandares','legitimidad'],'seeds':['T2729','GH021','T1475']},
{'id':'intervencion','title':'Hacer que suceda','question':'¿Cómo pasar de la intención a una capacidad que funciona?','description':'Transformación, creación de valor, coordinación distribuida, movilidad y trabajo de campo.','tags':['empresa','transformacion','agentes','movilidad','compromisos','casos'],'seeds':['E1628','N1274','N1805','U2']},
{'id':'capacidad','title':'Conservar y transmitir capacidad','question':'¿Qué saben hacer las personas y cómo puede continuar esa capacidad?','description':'Conocimiento tácito, aprendizaje, deuda de inteligencia humana, comunidad y experiencia vivida.','tags':['capacidad-humana','aprendizaje','memoria-territorio','espiritualidad','encuentros'],'seeds':['N1287','T874','T1472','np-coaching','D-018']},
{'id':'adaptacion','title':'Sostener valor y adaptación','question':'¿Qué cambia de régimen y qué permite seguir operando?','description':'Economía, liquidez, alertas tempranas, restricciones y adaptación ante condiciones cambiantes.','tags':['economia','cambio-regimen','geopolitica','empresa','mundo-abierto'],'seeds':['T1387','N1826','E1654','D-137']},
{'id':'fuentes','title':'Encontrar las fuentes','question':'¿Dónde está el documento y cómo se recorre el corpus?','description':'Entradas, índices y localizadores de fuentes. Es una ayuda de navegación para los otros recorridos.','tags':['navegacion'],'seeds':['N250','np-biografia']}
]
INTENTS=[
{'id':'transformacion','question':'Una transformación está bloqueada: ¿por dónde intervenir?','areas':['perspectiva','intervencion'],'seeds':['E1628','E1731','N1274'],'reason':'Primero cambia el nivel de observación; después conecta una intervención concreta con la capacidad de ejecución.'},
{'id':'racionalizacion','question':'Hay complejidad y capacidades desaprovechadas: ¿cómo encontrar valor?','areas':['intervencion','adaptacion'],'seeds':['E1704','E1662','E1654'],'reason':'Relaciona racionalización y descubrimiento de valor con un caso empresarial documentado.'},
{'id':'tacito','question':'La modernización está perdiendo el saber de quienes operan.','areas':['capacidad','intervencion'],'seeds':['N1287','T874','T1472'],'reason':'Empieza por el conocimiento tácito; contrástalo con deuda de inteligencia humana y atribución de la capacidad.'},
{'id':'autoridad','question':'Un agente puede actuar, pero ¿qué autoridad y control necesita?','areas':['gobierno','formalizacion'],'seeds':['T2729','GH021','T1499'],'reason':'Abre la arquitectura de control suficiente y sus condiciones antes de ampliar hacia la conciencia estructural.'},
{'id':'logistica','question':'¿Cómo coordinar muchas entidades operativas en tiempo real?','areas':['intervencion','adaptacion'],'seeds':['N864','N1805','N1803'],'reason':'Compara la inteligencia logística de GEPLAN con los mecanismos de orquestación y ruteo de xSeil.'},
{'id':'regimen','question':'Las reglas han cambiado: ¿qué señales permiten responder a tiempo?','areas':['adaptacion','gobierno'],'seeds':['T1387','N1826','N1831'],'reason':'Combina detección suficiente de cambio con liquidez y cascadas de factores en un caso.'},
{'id':'matematicas','question':'Quiero examinar la formulación matemática y sus límites.','areas':['formalizacion','perspectiva'],'seeds':['N1817','N1815','sac-0b460b7d138063'],'reason':'Empieza por Companion Paper II v2.1 (N1817), que consolida la formulación y la contabilidad de recursos. N1815 conserva la nota v5 anterior como antecedente de esa revisión. Después examina las dimensiones de indeterminación que la representación deja abiertas.'},
{'id':'pensamiento','question':'Quiero entender la forma de pensar de Iván Abril.','areas':['perspectiva','capacidad'],'seeds':['D-285','np-coaching','D-137'],'reason':'Abre una reflexión sobre el oficio del arquitecto y sigue hacia experiencia, aprendizaje y promesas económicas.'},
{'id':'comunidad','question':'¿Cómo se transmite conocimiento entre personas y comunidades?','areas':['capacidad','perspectiva'],'seeds':['np-coaching','N1287','D-018'],'reason':'Examina aprendizaje vivido, conocimiento tácito y experiencia espiritual mediante sus contextos propios.'},
{'id':'integracion','question':'¿Cómo convertir una operación entre empresas en ejecución y valor?','areas':['intervencion','gobierno'],'seeds':['U2','E1662','N1274'],'reason':'Empieza por integración empresarial y continúa por valor existente y coordinación de equipos.'},
{'id':'atribucion','question':'Una IA parece rendir bien: ¿quién está aportando la capacidad?','areas':['capacidad','gobierno'],'seeds':['T1472','T1475','T874'],'reason':'Relaciona atribución, su protocolo de medición y la deuda de inteligencia humana.'}
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
      'purpose':'Entender el corpus y elegir un posicionamiento antes de configurar el asistente.',
      'publicEntry':PUBLIC_ENTRY,'configurationRule':CONFIG_RULE,
      'flow':['Comprender el mapa superior','Formular la pregunta del visitante','Elegir un área y dos o tres fichas','Ajustar perspectiva, alcance y tokens','Abrir la lectura y revisar el posicionamiento'],
      'distinction':{'areas':'Qué pregunta o mecanismo quieres explorar.','clusters':'En qué contexto institucional, de práctica o de investigación aparece.','fichas':'Qué textos y casos sostienen esa lectura.','posicionamiento':'El documento o ficha concreto desde el que se empieza a recorrer.'},
      'counts':{'fichas':sum(n['type']=='ficha'for n in nodes.values()),'concepts':sum(n['type']=='concepto'for n in nodes.values()),'relations':len(graph['edges']),'clusters':len(graph['clusters']),'tags':len(graph['topics'])},
      'areas':[{k:v for k,v in a.items()if k!='members'}for a in areas],
      'bridges':[{k:v for k,v in b.items()if k!='edgeIds'}for b in bridges],'intents':INTENTS,
      'clusters':graph['clusters'],'topics':graph['topics'],
      'entryCards':{s:{'id':s,'title':nodes[s]['title'],'clusters':nodes[s]['clusters'],'web':summary_origin(root)+uri(nodes[s]),'original':nodes[s].get('original'),'documentId':nodes[s].get('documentId')}for s in dict.fromkeys(s for i in INTENTS for s in i['seeds'])}}
    full=summary|{'areas':areas,'bridges':bridges,'memberships':memberships,'primary':primary}
    def write(path,data):
        p=out/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data,encoding='utf8',newline='\n')
    def wrapper(title,body):
        return '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+H(title)+' · Atlas</title><link rel="stylesheet" href="/atlas-web.css"></head><body><main><header><p class="kicker">Atlas · Primero orientarse, después posicionarse</p><h1>'+H(title)+'</h1><nav class="actions">'+link('/','Atlas completo')+link('/orientacion/','Mapa superior')+link('/entrada/','Entrada para asistentes')+link('/orientacion/lectura.txt','Resumen en texto')+'</nav></header><div class="body">'+body+'</div><footer>'+link('/fichas/','Todas las fichas')+' · '+link('/orientacion/modelo.json','Mapa y correspondencias')+'</footer></main></body></html>\n'
    seed_card=lambda sid:'<li><strong>'+link(uri(nodes[sid]),nodes[sid]['title'])+'</strong><p class="meta">'+H(sid)+' · '+H(' / '.join(graph['clusters'][c]for c in nodes[sid]['clusters']))+'</p>'+('<p>'+link(nodes[sid]['original'],'Publicación de origen')+'</p>'if nodes[sid].get('original')else'')+'</li>'
    positions={'perspectiva':(170,100),'formalizacion':(500,90),'gobierno':(830,110),'intervencion':(220,310),'capacidad':(550,310),'adaptacion':(860,330),'fuentes':(510,500)}
    svg=['<svg role="img" aria-label="Mapa de las áreas superiores del Atlas y sus principales puentes" viewBox="0 0 1050 590" style="width:100%;height:auto"><title>Una constelación, varias preguntas de entrada</title>']
    for b in sorted(bridges,key=lambda b:-b['count'])[:14]:
        x1,y1=positions[b['from']];x2,y2=positions[b['to']]
        svg.append('<a href="/orientacion/puentes/'+b['from']+'-'+b['to']+'/"><path d="M'+str(x1)+' '+str(y1)+' L'+str(x2)+' '+str(y2)+'" stroke="#b7b8a8" stroke-width="'+str(1+math.log1p(b['count'])/4)+'" fill="none"><title>'+H(area_map[b['from']]['title']+' → '+area_map[b['to']]['title']+': '+str(b['count'])+' relaciones')+'</title></path></a>')
    for a in areas:
        x,y=positions[a['id']]
        words=textwrap.wrap(a['title'],width=25)
        label=''.join('<tspan x="'+str(x)+'" y="'+str(y-19+j*21)+'">'+H(line)+'</tspan>'for j,line in enumerate(words))
        svg.append('<a href="/orientacion/'+a['id']+'/"><rect x="'+str(x-138)+'" y="'+str(y-48)+'" width="276" height="96" rx="8" fill="#fffdf8" stroke="#98733d"/><text text-anchor="middle" fill="#172d39" style="font:18px Georgia,serif">'+label+'</text><text x="'+str(x)+'" y="'+str(y+29)+'" text-anchor="middle" fill="#425b65" style="font:14px system-ui">'+str(a['primaryCount'])+' piezas de entrada</text></a>')
    svg.append('</svg>')
    intro='<p class="lead">El hilo del Atlas relaciona cómo observamos una realidad, cómo decidimos y actuamos en ella y qué capacidades permiten sostener y revisar lo conseguido.</p><p>Antes de pedir un clúster o una ficha, comprende qué preguntas recorre el corpus. Las áreas agrupan sus temas; los clústeres muestran los contextos donde esas ideas se trabajan. La constelación es una y sus áreas se cruzan.</p><section class="reading"><h2>Cómo elegir una entrada</h2><ol><li>Pregunta al visitante qué quiere comprender, resolver o crear.</li><li>Identifica una o dos áreas del mapa y ofrece dos o tres fichas concretas.</li><li>Explica por qué sirven para esa pregunta. Después acuerda alcance, enfoque y presupuesto de lectura.</li><li>Si la pregunta es amplia, ofrece dos recorridos y una sola pregunta de aclaración.</li></ol></section>'
    body=intro+'<p>'+H(CONFIG_RULE)+'</p>'+''.join(svg)+'<h2>Las grandes preguntas</h2><div class="grid">'
    for a in areas:
        body+='<section class="card"><h2>'+link('/orientacion/'+a['id']+'/',a['title'])+'</h2><p><strong>'+H(a['question'])+'</strong></p><p>'+H(a['description'])+'</p><p class="meta">'+str(a['memberCount'])+' piezas relacionadas · '+str(a['primaryCount'])+' con esta área como entrada principal.</p></section>'
    body+='</div><h2>De una pregunta a un posicionamiento</h2><ul class="entries">'
    for i in INTENTS:
        body+='<li><h3>'+H(i['question'])+'</h3><p>'+H(i['reason'])+'</p><ul>'+''.join(seed_card(s)for s in i['seeds'])+'</ul></li>'
    body+='</ul><h2>Las correspondencias son comprobables</h2><p>Las agrupaciones superiores se calculan a partir de las etiquetas ya presentes. Los puentes resumen relaciones existentes y conservan sus identificadores y ejemplos. Cada ficha tiene una entrada principal y puede participar en varias áreas.</p><p>'+link('/orientacion/resumen.json','Resumen estructurado')+' · '+link('/orientacion/modelo.json','Correspondencias completas')+' · '+link('/orientacion/lectura.txt','Lectura breve para el asistente')+'</p>'
    write('orientacion/index.html',wrapper('Comprender el Atlas antes de elegir dónde entrar',body))
    for a in areas:
        text='<p class="lead">'+H(a['question'])+'</p><p>'+H(a['description'])+'</p><h2>Temas de esta área</h2><div class="tags">'+''.join(link('/etiquetas/'+t+'/',graph['topics'][t])for t in a['tags'])+'</div><h2>Entradas concretas</h2><ul class="entries">'+''.join(seed_card(s)for s in a['seeds'])+'</ul><h2>Puentes hacia otras preguntas</h2><ul>'
        for b in bridges:
            if b['from']==a['id']:text+='<li>'+link('/orientacion/puentes/'+b['from']+'-'+b['to']+'/',area_map[b['to']]['title'])+' · '+str(b['count'])+' relaciones registradas.</li>'
        text+='</ul><h2>Fichas y conceptos del área</h2><ul>'+''.join('<li>'+link(uri(nodes[s]),nodes[s]['title'])+'</li>'for s in a['members'])+'</ul>'
        write('orientacion/'+a['id']+'/index.html',wrapper(a['title'],text))
    by_edge={e[0]:e for e in graph['edges']}
    for b in bridges:
        text='<p>'+str(b['count'])+' relaciones del grafo conectan estas dos áreas mediante sus entradas principales.</p><h2>Ejemplos de lectura</h2><ul class="entries">'
        for e in b['examples']:
            text+='<li><h3>'+link(uri(nodes[e['from']]),nodes[e['from']]['title'])+' → '+link(uri(nodes[e['to']]),nodes[e['to']]['title'])+'</h3><p><strong>'+H(e['kind'])+'</strong></p><p>'+H(e['reading'])+'</p><p class="meta">'+H(e['id'])+'</p></li>'
        text+='</ul><details><summary>Identificadores de las relaciones agrupadas</summary><p>'+H(', '.join(b['edgeIds']))+'</p></details>'
        write('orientacion/puentes/'+b['from']+'-'+b['to']+'/index.html',wrapper(area_map[b['from']]['title']+' → '+area_map[b['to']]['title'],text))
    lines=['ATLAS · ORIENTACIÓN ANTES DEL POSICIONAMIENTO','',
    'El corpus conecta pensamiento arquitectónico, investigación, intervención empresarial y experiencia humana. Sus fichas forman una red de relaciones documentadas. Primero entiende el mapa superior; después acuerda una entrada concreta con el visitante.',
    'No empieces pidiendo un clúster a quien todavía no conoce el corpus. Pregunta qué quiere comprender, resolver o crear. Propón dos o tres fichas y explica el mecanismo que las hace pertinentes. Un área expresa una pregunta; un clúster expresa un contexto. El posicionamiento es el documento o ficha elegido.',
    '',CONFIG_RULE,'Entrada en dominio propio: '+PUBLIC_ENTRY,'','MAPA DE ÁREAS']
    for a in areas:
        lines+=['',a['title']+' — '+a['question'],a['description'],'Temas: '+', '.join(graph['topics'][t]for t in a['tags'])+'.',
        'Entradas: '+'; '.join(s+' · '+nodes[s]['title']for s in a['seeds'][:3]),'Ampliar: '+summary_origin(root)+'/orientacion/'+a['id']+'/']
    lines+=['','PREGUNTAS Y ENTRADAS']
    for i in INTENTS:lines+=[i['question']+' → '+', '.join(i['seeds'])+'. '+i['reason']]
    lines+=['','LOCALIZAR UNA FICHA','Para abrir un ID de ficha usa '+summary_origin(root)+'/fichas/ID/ . Los conceptos se abren en /conceptos/ID/. El resumen estructurado enlaza también la publicación de origen de cada entrada.',
    '','PASO SIGUIENTE','Abre dos fichas, comprueba su contexto y ofrece el recorrido. Ajusta la selección según lo que encuentre el visitante. Para configuraciones heredadas, conserva los parámetros de la URL original. Cuando ya haya un objetivo explícito, trabaja desde él.',
    'Mapa superior: '+summary_origin(root)+'/orientacion/','Todas las fichas: '+summary_origin(root)+'/fichas/','Correspondencias completas: '+summary_origin(root)+'/orientacion/modelo.json','']
    write('orientacion/lectura.txt','\n'.join(lines))
    write('orientacion/resumen.json',json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    write('orientacion/modelo.json',json.dumps(full,ensure_ascii=False,indent=2)+'\n')
    integrate_entry(root)
    assert sha256(gpath.read_bytes()).hexdigest()==before
    return full

def integrate_entry(root):
    out=root/'dist'
    note='Antes de elegir un posicionamiento, lee el mapa superior: '+PUBLIC_ENTRY+' . Allí están las grandes preguntas del corpus, sus puentes y las fichas para empezar. Si el visitante todavía no conoce el Atlas, parte de su intención y ofrece dos o tres entradas concretas. '+CONFIG_RULE
    marker='<!-- atlas-orientation:start -->'
    block=marker+'<section class="reading"><p class="kicker">Primero orientarse</p><h2>'+link(PUBLIC_ENTRY,'Comprender el Atlas antes de elegir dónde entrar')+'</h2><p>Un mapa de las grandes preguntas, sus conexiones y las fichas desde las que empezar.</p><p>'+link('/orientacion/','Explorar las áreas y sus puentes')+'</p></section><!-- atlas-orientation:end -->'
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
        text=re.sub(r'\nORIENTACIÓN PREVIA\n.*?\nFIN DE ORIENTACIÓN\n','\n',text,flags=re.S)
        title,separator,rest=text.partition('\n')
        path.write_text(title+'\n\nORIENTACIÓN PREVIA\n'+note+'\nFIN DE ORIENTACIÓN\n'+rest,encoding='utf8',newline='\n')
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

