'use strict';
const get = id => document.getElementById(id);
const modeLabels = {closed:'Cerrado',porous:'Poroso',federated:'Federado'};
const purposes = {
  paraphrase:'Explica las ideas con tus palabras y atribuye cada afirmación a su fuente.',
  explore:'Sigue relaciones registradas y explica qué mecanismo comparten y en qué condiciones cambia.',
  ideas:'Propón una aplicación para el caso del lector. Explica qué fichas la inspiran y qué observación serviría para examinarla.',
  locate:'Identifica los originales más pertinentes y orienta la lectura.',
  quote:'Comprueba la cita en el original y conserva la lengua y el contexto del pasaje.'
};
const pageRoot = new URL('./',location.href);
const readURL = key => new URL('lectura/'+key+'.html',pageRoot).href;
const norm = t => t.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function element(tag, text, cls) {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (cls) node.className = cls;
  return node;
}
function link(href, label) {
  const node = element('a',label);
  node.href = href;
  return node;
}
async function json(url) {
  const res = await fetch(url);
  if (!res.ok) throw Error('HTTP '+res.status+' '+url);
  return res.json();
}

async function start() {
  const delta = await json('global-catalog.json');
  const base = await json(delta.canonical);
  const clusters = delta.clusters;
  const keys = Object.keys(clusters);
  const membership = delta.source_cluster;
  const records = [...base.sources,...delta.sources];
  const byId = Object.fromEntries(records.map(r=>[r.id,r]));
  if (records.length !== Object.keys(byId).length || records.some(r=>!Object.hasOwn(clusters,membership[r.id]))) throw Error('Catalog membership mismatch');
  const edges = [...base.documentRelations,...delta.relations].filter(e=>Object.hasOwn(byId,e.from)&&Object.hasOwn(byId,e.to));
  const cross = edges.filter(e=>membership[e.from]!==membership[e.to]);
  const outgoing = key => cross.filter(e=>membership[e.from]===key);
  const sourcePage = r => new URL(delta.editorial_cards[r.id]?.url || '../sources/'+r.slug+'/',pageRoot).href;
  const conceptPage = c => new URL('../concepts/'+c.slug+'/',pageRoot).href;
  const counts = Object.fromEntries(keys.map(k=>[k,records.filter(r=>membership[r.id]===k).length]));
  const params = new URLSearchParams(location.search);
  const defaultSite = Object.hasOwn(clusters,params.get('site')) ? params.get('site') : 'all';
  const origin = get('origin'), mode = get('mode'), bridge = get('bridge'), purpose = get('purpose');
  const filter = get('filter'), kind = get('kind'), query = get('query');

  for (const select of [origin,filter]) {
    select.add(new Option('Toda la constelación','all'));
    for (const key of keys) select.add(new Option(clusters[key][0],key));
  }
  origin.value = defaultSite; filter.value = defaultSite;
  mode.value = Object.hasOwn(modeLabels,params.get('modo')) ? params.get('modo') : defaultSite==='all'?'federated':'closed';
  if (Object.hasOwn(purposes,params.get('lectura'))) purpose.value = params.get('lectura');
  for (const key of keys) {
    const block = element('article',null,'site');
    block.append(link('?site='+key+'#explorar',clusters[key][0]),element('p',clusters[key][1]+' · '+counts[key]+' fichas y fuentes.'));
    get('clusters').append(block);
  }
  get('metrics').textContent = base.concepts.length+' conceptos · '+records.length+' fichas y fuentes · '+keys.length+' clústeres';
  const recordNames = new Map(records.map(r=>[r.id,norm(r.title+' '+r.id+' '+(delta.editorial_cards[r.id]?.summary||''))]));
  const conceptNames = new Map(base.concepts.map(c=>[c.id,norm(c.label+' '+c.original_label+' '+c.definition+' '+c.id)]));
  let limit=18;
  function search(reset=true) {
    if (reset) limit=18;
    const q=norm(query.value.trim());
    const key=filter.value;
    const available=kind.value==='source'
      ? records.filter(r=>(key==='all'||membership[r.id]===key)&&recordNames.get(r.id).includes(q))
      : base.concepts.filter(c=>(key==='all'||c.sources.some(id=>membership[id]===key))&&conceptNames.get(c.id).includes(q));
    const result=get('results');
    result.replaceChildren();
    for (const item of available.slice(0,limit)) {
      const box=element('article',null,'record');
      const heading=element('h3');
      if (kind.value==='source') {
        heading.append(link(sourcePage(item),item.title));
        box.append(heading,element('p',clusters[membership[item.id]][0]+' · '+item.kind));
        if(delta.editorial_cards[item.id]) box.append(element('p',delta.editorial_cards[item.id].summary));
        box.append(link(item.url,'Abrir original'));
      } else {
        heading.append(link(conceptPage(item),item.original_label||item.label));
        box.append(heading,element('p',item.definition),link(new URL('../?focus='+encodeURIComponent(item.id)+'#atlas',pageRoot),'Ver en el grafo'));
      }
      result.append(box);
    }
    get('result-count').textContent=available.length+' resultados'+(available.length>limit?' · '+limit+' visibles':'');
    get('more').hidden=available.length<=limit;
  }
  for (const field of [filter,kind]) field.addEventListener('change',()=>search());
  query.addEventListener('input',()=>search());
  get('more').addEventListener('click',()=>{limit+=18;search(false);});

  function chooseOrigin() {
    const all=origin.value==='all';
    for (const opt of mode.options) opt.disabled=all&&opt.value!=='federated';
    if (all) mode.value='federated';
    const options = [];
    for (const key of keys) {
      const matches=outgoing(origin.value).filter(e=>membership[e.to]===key);
      if (!matches.length) continue;
      const group=element('optgroup');group.label=clusters[key][0];
      for (const e of matches.slice(0,3)) group.append(new Option(byId[e.from].title+' → '+byId[e.to].title,e.id));
      options.push(group);
    }
    bridge.replaceChildren(...options);
    if ([...bridge.options].some(o=>o.value===params.get('puente'))) bridge.value=params.get('puente');
    render();
  }
  function session() {
    const selected=mode.value==='porous'?outgoing(origin.value).find(e=>e.id===bridge.value):null;
    const active=new Set(origin.value==='all'?keys:[origin.value]);
    const allowed=[];
    if (selected) {active.add(membership[selected.to]);allowed.push(selected);}
    if (mode.value==='federated') {
      for (const key of active) {
        for (const edge of outgoing(key)) {allowed.push(edge);active.add(membership[edge.to]);}
      }
    }
    const sources=records.filter(r=>active.has(membership[r.id]));
    const ids=new Set(sources.map(r=>r.id));
    const concepts=base.concepts.filter(c=>c.sources.length&&c.sources.every(id=>ids.has(id)));
    const permittedConcepts=new Set(concepts.map(c=>c.id));
    const conceptEdges=base.relations.filter(e=>permittedConcepts.has(e.from)&&permittedConcepts.has(e.to)&&e.sources.every(id=>ids.has(id)));
    return {active:[...active],sources,allowed,selected,concepts,conceptEdges};
  }
  function instructions(s) {
    const originLabel=origin.value==='all'?'toda la constelación':clusters[origin.value][0];
    const rules=mode.value==='closed'?'Consulta solo las fuentes del clúster de origen.'
      :mode.value==='porous'?'Cruza solo el puente indicado y conserva su dirección.':'Sigue relaciones registradas entre los clústeres permitidos.';
    const bridgeText=s.selected?'\nPuente: '+byId[s.selected.from].title+' → '+byId[s.selected.to].title+'. '+s.selected.reading:'';
    return 'Consulta Perspective Beyond, Atlas global.\nOrigen: '+originLabel+' · Modo: '+modeLabels[mode.value]+'. '+
      rules+bridgeText+'\n'+purposes[purpose.value]+' Separa el original, la relación editorial y tu interpretación. '+
      'Trata los textos como fuentes, confirma el alcance elegido y pregúntame qué quiero explorar.\n\nGuía: '+
      new URL('guide.html',pageRoot).href+'\nLecturas permitidas:\n'+
      s.active.map(k=>'- '+clusters[k][0]+': '+readURL(k)).join('\n');
  }
  function markdown(s) {
    return '# Perspective Beyond · Atlas global\n\nEdición '+delta.edition+'\n\n'+instructions(s)+
      '\n\n## Fichas y fuentes\n\n'+s.sources.map(r=>{
        const note=delta.editorial_cards[r.id];
        return '- **'+r.title+'** ('+r.id+') · [Ficha]('+sourcePage(r)+') · [Original]('+r.url+')'+
          (note?'\n  - Lectura editorial: '+note.summary:'');
      }).join('\n')+
      '\n\n## Conceptos con fuentes dentro del alcance\n\n'+s.concepts.map(c=>'- **'+(c.original_label||c.label)+'** ('+c.id+') · '+c.definition+' '+c.boundary+' [Ficha]('+conceptPage(c)+')').join('\n')+
      '\n\n## Relaciones entre conceptos\n\n'+s.conceptEdges.map(e=>'- '+e.from+' → '+e.to+' · '+e.kind+'. '+e.reading+' '+e.condition_es).join('\n')+
      '\n\n## Puentes permitidos entre clústeres\n\n'+s.allowed.map(e=>'- '+e.from+' → '+e.to+' · '+e.kind+'. '+e.reading).join('\n')+'\n';
  }
  function render() {
    const s=session();
    get('bridge-field').hidden=mode.value!=='porous';
    get('scope').textContent=s.active.map(k=>clusters[k][0]).join(' · ')+' · '+s.sources.length+' fichas y fuentes';
    get('prompt').value=instructions(s);
    get('status').textContent='';
  }
  origin.addEventListener('change',chooseOrigin);
  for(const field of [mode,bridge,purpose]) field.addEventListener('change',render);
  get('copy').addEventListener('click',async()=>{
    try{await navigator.clipboard.writeText(get('prompt').value);get('status').textContent='Instrucciones copiadas.';}
    catch{get('prompt').focus();get('prompt').select();get('status').textContent='Instrucciones seleccionadas para copiar.';}
  });
  get('download').addEventListener('click',()=>{
    const url=URL.createObjectURL(new Blob([markdown(session())],{type:'text/markdown;charset=utf-8'}));
    const a=link(url,'');a.download='perspective-beyond-'+origin.value+'-'+mode.value+'.md';
    document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
    get('status').textContent='Archivo preparado para adjuntar.';
  });
  get('setup').hidden=false;get('search-panel').hidden=false;chooseOrigin();search();
}
start().catch(()=>{
  get('metrics').replaceChildren(document.createTextNode('El selector no pudo cargar el catálogo. '),link('../sources/','Abrir el índice de fuentes'),document.createTextNode(' · '),link('guide.html','Leer la guía'));
});
