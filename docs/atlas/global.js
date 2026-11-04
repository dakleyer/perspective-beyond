'use strict';
const get = id => document.getElementById(id);
const modeLabels = {closed:'Cerrado',porous:'Poroso',federated:'Federado'};
const pageRoot = new URL('./',location.href);
const rawRoot = 'https://raw.githubusercontent.com/dakleyer/perspective-beyond/main/docs/atlas/';
const readURL = key => new URL('lectura/'+key+'.html',pageRoot).href;
const radiusURL = (id,red='documentos') => new URL('mapa/?'+new URLSearchParams({centro:id,red}),pageRoot).href;
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
  base.concepts.push(...(delta.concepts||[]));
  base.relations.push(...(delta.concept_relations||[]));
  const clusters = delta.clusters;
  const {roles,purposes} = delta.session_profiles;
  const {topics,source_tags:sourceTags} = delta;
  const keys = Object.keys(clusters);
  const membership = delta.source_cluster;
  const records = [...base.sources,...delta.sources];
  const byId = Object.fromEntries(records.map(r=>[r.id,r]));
  if (records.length !== Object.keys(byId).length || records.some(r=>!Object.hasOwn(clusters,membership[r.id]))) throw Error('Catalog membership mismatch');
  const edges = [...base.documentRelations,...delta.relations].filter(e=>Object.hasOwn(byId,e.from)&&Object.hasOwn(byId,e.to));
  const cross = edges.filter(e=>membership[e.from]!==membership[e.to]);
  const outgoing = key => cross.filter(e=>membership[e.from]===key);
  const sourcePage = r => new URL(delta.editorial_cards[r.id]?.url || '../sources/'+r.slug+'/',pageRoot).href;
  const conceptPage = c => new URL(c.url||'../concepts/'+c.slug+'/',pageRoot).href;
  const counts = Object.fromEntries(keys.map(k=>[k,records.filter(r=>membership[r.id]===k).length]));
  const params = new URLSearchParams(location.search);
  const defaultSite = Object.hasOwn(clusters,params.get('site')) ? params.get('site') : 'all';
  const origin = get('origin'), mode = get('mode'), bridge = get('bridge'), purpose = get('purpose');
  const role = get('role'), custom = get('custom-role');
  const filter = get('filter'), kind = get('kind'), query = get('query');
  const topicFilter = get('topic-filter'), onlyTopics = get('only-topics');
  const profile = get('focus-profile'), target = get('focus-target'), focusRows = get('focus-rows');
  const profiles = ['parejo','transversal','personalizado'];
  const weights = new Map();
  const initialWeights = params.getAll('peso').slice(0,20);
  onlyTopics.checked = params.get('solo')==='1';
  let focusItems = new Map(), focusScope = '', restoreFocus = true;
  if (profiles.includes(params.get('enfoque'))) profile.value = params.get('enfoque');
  query.value = params.get('buscar') || '';

  for (const select of [origin,filter]) {
    select.add(new Option('Toda la constelación','all'));
    for (const key of keys) select.add(new Option(clusters[key][0],key));
  }
  origin.value = defaultSite; filter.value = defaultSite;
  mode.value = Object.hasOwn(modeLabels,params.get('modo')) ? params.get('modo') : defaultSite==='all'?'federated':'closed';
  for (const [select,choices] of [[role,roles],[purpose,purposes]]) {
    for (const [key,[label]] of Object.entries(choices)) select.add(new Option(label,key));
  }
  if (Object.hasOwn(roles,params.get('rol'))) role.value = params.get('rol');
  if (Object.hasOwn(purposes,params.get('lectura'))) purpose.value = params.get('lectura');
  custom.value = (params.get('instruccion')||'').slice(0,custom.maxLength);
  get('role-options').open = Boolean(custom.value)||role.value==='personalizado';
  for (const [key,topic] of Object.entries(topics)) topicFilter.add(new Option(topic.label,key));
  if (Object.hasOwn(topics,params.get('etiqueta'))) topicFilter.value=params.get('etiqueta');
  for (const key of keys) {
    const block = element('article',null,'site');
    block.append(link('?site='+key+'#explorar',clusters[key][0]),element('p',clusters[key][1]+' · '+counts[key]+' fichas y fuentes.'));
    get('clusters').append(block);
  }
  get('metrics').textContent = base.concepts.length+' conceptos · '+records.length+' fichas y fuentes · '+keys.length+' clústeres';
  const recordNames = new Map(records.map(r=>[r.id,norm([
    r.title,r.id,delta.editorial_cards[r.id]?.summary||'',
    ...sourceTags[r.id].map(key=>topics[key].label)
  ].join(' '))]));
  const conceptNames = new Map(base.concepts.map(c=>[c.id,norm(c.label+' '+c.original_label+' '+c.definition+' '+c.id)]));
  let limit=18;
  function search(reset=true) {
    if (reset) limit=18;
    const q=norm(query.value.trim());
    const key=filter.value;
    const tag=topicFilter.value;
    const matches=sid=>(key==='all'||membership[sid]===key)&&(!tag||sourceTags[sid]?.includes(tag));
    const available=kind.value==='source'
      ? records.filter(r=>matches(r.id)&&recordNames.get(r.id).includes(q))
      : base.concepts.filter(c=>((key==='all'&&!tag)||c.sources.some(matches))&&conceptNames.get(c.id).includes(q));
    const result=get('results');
    result.replaceChildren();
    for (const item of available.slice(0,limit)) {
      const box=element('article',null,'record');
      const heading=element('h3');
      if (kind.value==='source') {
        heading.append(link(sourcePage(item),item.title));
        box.append(heading,element('p',clusters[membership[item.id]][0]+' · '+item.kind));
        if(delta.editorial_cards[item.id]) box.append(element('p',delta.editorial_cards[item.id].summary));
        if(sourceTags[item.id].length)box.append(element('p',sourceTags[item.id].map(key=>topics[key].label).join(' · ')));
        box.append(link(item.url,'Abrir original'),document.createTextNode(' · '),link(radiusURL(item.id),'Mapa alrededor de esta ficha'));
      } else {
        heading.append(link(conceptPage(item),item.original_label||item.label));
        box.append(heading,element('p',item.definition),link(item.url?conceptPage(item):new URL('../?focus='+encodeURIComponent(item.id)+'#atlas',pageRoot),'Ver en el grafo'),
          document.createTextNode(' · '),link(radiusURL(item.id,'ideas'),'Mapa alrededor de este concepto'));
      }
      result.append(box);
    }
    get('result-count').textContent=available.length+' resultados'+(available.length>limit?' · '+limit+' visibles':'');
    get('more').hidden=available.length<=limit;
  }
  for (const field of [filter,kind,topicFilter]) field.addEventListener('change',()=>search());
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
  function focusTargets(s) {
    const signature=s.active.join('|');
    if (signature===focusScope) return;
    focusScope=signature;
    const prior=target.value;
    const active=new Set(s.active);
    const matches=ids=>ids.some(id=>active.has(membership[id]));
    const groups=[
      ['Clústeres',s.active.map(k=>['cluster:'+k,clusters[k][0]])],
      ['Etiquetas temáticas',Object.entries(topics).filter(([,v])=>matches(v.sources)).map(([k,v])=>['tema:'+k,v.label])],
      ['Perspectivas documentadas',Object.entries(delta.focus_voices||{}).filter(([,v])=>matches(v.sources)).map(([k,v])=>['voz:'+k,v.label])],
      ['Etiquetas conceptuales',base.concepts.filter(c=>matches(c.sources)).map(c=>['concepto:'+c.id,c.original_label||c.label]).sort((a,b)=>a[1].localeCompare(b[1],'es'))]
    ];
    focusItems=new Map(groups.flatMap(([,items])=>items));
    target.replaceChildren(...groups.filter(([,items])=>items.length).map(([label,items])=>{
      const options=element('optgroup');options.label=label;
      options.append(...items.map(([key,name])=>new Option(name,key)));
      return options;
    }));
    if (focusItems.has(prior)) target.value=prior;
    for (const key of weights.keys()) if(!focusItems.has(key)) weights.delete(key);
    if (restoreFocus) {
      restoreFocus=false;
      for(const token of initialWeights){
        const at=token.lastIndexOf(':');
        const key=token.slice(0,at), weight=Number(token.slice(at+1));
        if(focusItems.has(key)&&Number.isFinite(weight)&&weight>=0&&weight<=10000)weights.set(key,weight);
      }
      if(weights.size)profile.value='personalizado';
    }
    drawWeightRows();
  }
  function drawWeightRows() {
    focusRows.replaceChildren();
    for(const [key,value] of weights) {
      const label=focusItems.get(key);
      const row=element('div',null,'focus-row');row.dataset.key=key;
      const input=element('input');
      input.type='number';input.min='0';input.max='10000';input.step='any';input.value=value;
      input.setAttribute('aria-label','Peso relativo de '+label);
      input.addEventListener('input',()=>{
        const n=input.valueAsNumber;
        weights.set(key,Number.isFinite(n)?Math.min(10000,Math.max(0,n)):0);
        render();
      });
      const remove=element('button','Quitar','secondary');remove.type='button';
      remove.setAttribute('aria-label','Quitar peso de '+label);
      remove.addEventListener('click',()=>{weights.delete(key);drawWeightRows();render();target.focus();});
      row.append(element('span',label),input,element('span',null,'focus-percent'),remove);
      focusRows.append(row);
    }
  }
  function weighting() {
    const picked=[...weights].filter(([,value])=>value>0);
    if(profile.value!=='personalizado'||!picked.length) return {profile:profile.value==='transversal'?'transversal':'parejo',items:[]};
    const total=picked.reduce((sum,[,value])=>sum+value,0);
    const items=picked.map(([key,weight])=>{
      const exact=weight/total*1000;
      const tenths=Math.floor(exact);
      return {key,weight,label:focusItems.get(key),tenths,remainder:exact-tenths};
    });
    const spare=1000-items.reduce((sum,x)=>sum+x.tenths,0);
    for(const item of [...items].sort((a,b)=>b.remainder-a.remainder).slice(0,spare))item.tenths++;
    const topicKeys=items.filter(item=>item.key.startsWith('tema:')).map(item=>item.key.slice(5));
    return {profile:'personalizado',items,topicKeys,strict:onlyTopics.checked&&topicKeys.length>0};
  }
  function filteredSession(s,f) {
    if(!f.strict)return s;
    const sources=s.sources.filter(r=>f.topicKeys.some(key=>sourceTags[r.id].includes(key)));
    const ids=new Set(sources.map(r=>r.id));
    const concepts=s.concepts.filter(c=>c.sources.every(id=>ids.has(id)));
    const conceptIds=new Set(concepts.map(c=>c.id));
    const conceptEdges=s.conceptEdges.filter(e=>conceptIds.has(e.from)&&conceptIds.has(e.to)&&e.sources.every(id=>ids.has(id)));
    const allowed=s.allowed.filter(e=>ids.has(e.from)&&ids.has(e.to));
    return {...s,sources,concepts,conceptEdges,allowed};
  }
  const percent = n => (n/10).toLocaleString('es',{maximumFractionDigits:1})+' %';
  function focusInstruction(f) {
    if(f.profile==='transversal')return 'Enfoque transversal. Recorre conexiones entre perspectivas permitidas y explica qué aportan en conjunto.';
    if(f.profile==='parejo')return 'Enfoque parejo. Da atención equilibrada a las perspectivas pertinentes dentro del alcance.';
    return 'Enfoque ponderado. '+f.items.map(x=>x.label+' '+percent(x.tenths)).join(' · ')+
      '. Usa este reparto como prioridad de lectura y síntesis. Si una ficha encaja en varias etiquetas, utilízala una vez.'+
      (f.strict?' Usa solo fichas con al menos una de estas etiquetas: '+f.topicKeys.map(key=>topics[key].label).join(', ')+
        '. Conserva relaciones entre fichas que cumplan el filtro.\nÍndices temáticos: '+
        f.topicKeys.map(key=>new URL('temas/'+key+'.txt',pageRoot).href).join(' · '):'');
  }
  function instructions(s,f) {
    const originLabel=origin.value==='all'?'toda la constelación':clusters[origin.value][0];
    const rules=mode.value==='closed'?'Consulta solo las fuentes del clúster de origen.'
      :mode.value==='porous'?'Cruza solo el puente indicado y conserva su dirección.':'Sigue relaciones registradas entre los clústeres permitidos.';
    const bridgeText=s.selected?'\nPuente: '+byId[s.selected.from].title+' → '+byId[s.selected.to].title+'. '+s.selected.reading:'';
    const [roleLabel,roleRule]=roles[role.value];
    const [purposeLabel,purposeRule]=purposes[purpose.value];
    const customText=custom.value.trim();
    return 'Abre la entrada de Perspective Beyond: '+textEntry(f)+'\nOrigen: '+originLabel+' · Modo: '+modeLabels[mode.value]+'. '+
      rules+bridgeText+'\nRol: '+roleLabel+'. '+roleRule+'\nPropósito: '+purposeLabel+'. '+purposeRule+'\n'+focusInstruction(f)+
      (customText?'\nInstrucción del lector: '+customText:'')+
      '\nAplica esta configuración. Separa el original, la relación editorial y tu interpretación. '+
      'Si todavía no hay una pregunta, pregunta qué quiere explorar el lector.\n\nGuía: '+
      new URL('guide.html',pageRoot).href+'\nLecturas permitidas:\n'+
      s.active.map(k=>'- '+clusters[k][0]+': '+readURL(k)).join('\n');
  }
  function setConfiguration(url,f) {
    url.searchParams.set('config','1');
    url.searchParams.set('rol',role.value);
    url.searchParams.set('lectura',purpose.value);
    url.searchParams.set('enfoque',f.profile);
    for(const item of f.items)url.searchParams.append('peso',item.key+':'+item.weight);
    if(f.strict)url.searchParams.set('solo','1');
    const customText=custom.value.trim();
    if(customText)url.searchParams.set('instruccion',customText);
    return url.href;
  }
  function textEntry(f=weighting(),root=pageRoot) {
    const entries=delta.text_entries;
    const selected=entries.clusters[origin.value];
    const path=origin.value==='all'?entries.global
      :mode.value==='porous'?selected.porous[bridge.value]:selected[mode.value];
    if(!path) throw Error('No plain-text entry for the selected scope');
    return setConfiguration(new URL(path,root),f);
  }
  function webEntry(f=weighting()) {
    const url=new URL('./#asistente',pageRoot);
    if(origin.value!=='all')url.searchParams.set('site',origin.value);
    url.searchParams.set('modo',mode.value);
    if(mode.value==='porous')url.searchParams.set('puente',bridge.value);
    return setConfiguration(url,f);
  }
  function markdown(s) {
    const f=weighting();
    s=filteredSession(s,f);
    return '# Perspective Beyond · Atlas global\n\nEdición '+delta.edition+'\n\n'+instructions(s,f)+
      '\n\n## Fichas y fuentes\n\n'+s.sources.map(r=>{
        const note=delta.editorial_cards[r.id];
        const tags=sourceTags[r.id].map(key=>'tema:'+key).join(' · ');
        return '- **'+r.title+'** ('+r.id+') · [Ficha]('+sourcePage(r)+') · [Original]('+r.url+')'+(tags?' · '+tags:'')+
          (note?'\n  - Lectura editorial: '+note.summary:'');
      }).join('\n')+
      '\n\n## Conceptos con fuentes dentro del alcance\n\n'+s.concepts.map(c=>'- **'+(c.original_label||c.label)+'** ('+c.id+') · '+c.definition+' '+c.boundary+' [Ficha]('+conceptPage(c)+')').join('\n')+
      '\n\n## Relaciones entre conceptos\n\n'+s.conceptEdges.map(e=>'- '+e.from+' → '+e.to+' · '+e.kind+'. '+(e.reading||e.relation_es||e.predicate||'')+' '+(e.condition_es||'')).join('\n')+
      '\n\n## Puentes permitidos entre clústeres\n\n'+s.allowed.map(e=>'- '+e.from+' → '+e.to+' · '+e.kind+'. '+e.reading).join('\n')+'\n';
  }
  function render() {
    const s=session();
    focusTargets(s);
    const f=weighting();
    const scoped=filteredSession(s,f);
    get('focus-editor').hidden=profile.value!=='personalizado';
    onlyTopics.disabled=!f.topicKeys?.length;
    const rendered=new Map(f.items.map(item=>[item.key,percent(item.tenths)]));
    for(const row of focusRows.children)row.querySelector('.focus-percent').textContent=rendered.get(row.dataset.key)||'0 %';
    get('focus-preview').textContent=profile.value==='personalizado'&&!f.items.length
      ?'Añade un peso positivo para personalizar la lectura. Ahora se reparte de forma pareja.' : focusInstruction(f);
    get('bridge-field').hidden=mode.value!=='porous';
    get('scope').textContent=s.active.map(k=>clusters[k][0]).join(' · ')+' · '+scoped.sources.length+' fichas y fuentes';
    get('role-help').textContent=roles[role.value][1];
    get('entry-url').href=textEntry(f);
    get('entry-mirror').href=textEntry(f,rawRoot);
    get('web-entry').href=webEntry(f);
    get('prompt').value=instructions(s,f);
    get('status').textContent='';
  }
  origin.addEventListener('change',chooseOrigin);
  for(const field of [mode,bridge,purpose,profile,onlyTopics]) field.addEventListener('change',render);
  role.addEventListener('change',()=>{
    if(role.value==='personalizado')get('role-options').open=true;
    render();
  });
  custom.addEventListener('input',render);
  get('focus-add').addEventListener('click',()=>{
    const key=target.value;
    if(!focusItems.has(key)||(!weights.has(key)&&weights.size>=20))return;
    if(!weights.has(key)) {weights.set(key,100);drawWeightRows();}
    render();
    [...focusRows.children].find(row=>row.dataset.key===key)?.querySelector('input').focus();
  });
  get('copy-url').addEventListener('click',async()=>{
    try{await navigator.clipboard.writeText(textEntry());get('status').textContent='URL copiada. Pégala en tu asistente.';}
    catch{get('entry-url').focus();get('status').textContent='Puedes copiar la dirección del enlace «Abrir URL de esta selección».';}
  });
  get('copy-config').addEventListener('click',async()=>{
    try{await navigator.clipboard.writeText(webEntry());get('status').textContent='Enlace a la configuración web copiado.';}
    catch{get('web-entry').focus();get('status').textContent='Puedes copiar la dirección del enlace «Abrir esta configuración web».';}
  });
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
