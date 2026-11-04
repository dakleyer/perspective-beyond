import {calculate,readRequest,shareParams} from './radius.mjs';

const get=id=>document.getElementById(id);
const svgNamespace='http://www.w3.org/2000/svg';
const params=new URLSearchParams(location.search);
const embedded=params.get('embed')==='1';
if(embedded)document.body.classList.add('embed');
function positioningURL(embeddedMap=false){
 const url=new URL('../posicionamiento/',location.href);url.searchParams.set('posicionamiento',params.get('centro')??'imsv');
 url.searchParams.set('tokens',params.get('tokens')??'2000');
 for(const key of ['max','red','sentido','solo','site','modo','puente','rol','lectura','instruccion'])if(params.has(key))url.searchParams.set(key,params.get(key));
 for(const peso of params.getAll('peso'))url.searchParams.append('peso',peso);if(embeddedMap)url.searchParams.set('embed','1');return url;
}

function element(tag,text) {
  const node=document.createElement(tag);
  if(text)node.textContent=text;
  return node;
}
function svgElement(tag,attributes={}) {
  const node=document.createElementNS(svgNamespace,tag);
  for(const [key,value] of Object.entries(attributes))node.setAttribute(key,value);
  return node;
}
function link(url,label) {
  if(!url||!/^https?:\/\//i.test(url))return null;
  const a=element('a',label);
  a.href=url;
  a.target='_blank';
  a.rel='noopener';
  return a;
}
function mapURL(request,embed=false) {
  const url=new URL('./',location.href);
  url.search=shareParams(request);
  if(embed)url.searchParams.set('embed','1');
  return url;
}
const percent=new Intl.NumberFormat('es',{style:'percent',maximumFractionDigits:1});
const typeName=node=>node.type==='ficha'?'Card':'Concept';
const distanceName=distance=>distance===0?'centro':distance===1?'1 salto':distance+' saltos';

async function start() {
  const response=await fetch('grafo.json');
  if(!response.ok)throw Error('El grafo no está disponible en este momento.');
  const graph=await response.json();
  const form=get('settings');
  const weights=new Map();
  const labels=graph.topics;
  const topic=get('topic');
  const items=get('node-list');
  const plot=get('graph');
  let result,selected,selectedById=new Map();

  for(const [tag,label] of Object.entries(labels))topic.add(new Option(label,tag));
  const suggestions=document.createDocumentFragment();
  for(const node of graph.nodes) {
    const option=element('option');
    option.value=node.id;
    option.label=node.title;
    suggestions.append(option);
  }
  get('suggestions').append(suggestions);

  function weightRows() {
    get('weights').replaceChildren();
    for(const [tag,value] of weights) {
      const row=element('div');
      row.className='weight-row';
      const input=element('input');
      input.type='number'; input.min='0'; input.max='10000'; input.step='any'; input.required=true; input.value=value;
      input.setAttribute('aria-label','Weight of '+labels[tag]);
      input.addEventListener('input',()=>weights.set(tag,input.value));
      const remove=element('button','Remove');
      remove.type='button'; remove.className='secondary';
      remove.setAttribute('aria-label','Quitar '+labels[tag]);
      remove.addEventListener('click',()=>{weights.delete(tag);weightRows();topic.focus();});
      row.append(element('span',labels[tag]),input,remove);
      get('weights').append(row);
    }
    if(!weights.size)get('only').checked=false;
    get('only').disabled=!weights.size;
  }
  get('add-weight').addEventListener('click',()=>{
    if(!weights.has(topic.value)) {
      weights.set(topic.value,'1');
      weightRows();
    }
    get('weights').querySelector(`[aria-label="Weight of ${CSS.escape(labels[topic.value])}"]`)?.focus();
  });

  function inspect(id) {
    selected=id;
    const node=selectedById.get(id);
    const where=node.clusters.map(key=>graph.clusters[key]).join(' · ');
    get('node-meta').textContent=typeName(node)+' · '+where+' · '+distanceName(node.distance);
    get('node-title').textContent=node.title;
    get('node-summary').textContent=node.summary;
    get('node-tags').textContent=node.tagWeights?Object.entries(node.tagWeights).sort((a,b)=>b[1]-a[1]).map(([tag,w])=>labels[tag]+' '+percent.format(w)).join(' · '):node.tags.map(tag=>labels[tag]).join(' · ');
    const links=[link(node.url,'Open card'),link(node.original,'Fuente original')];
    if(node.commitUrl)links.push(link(node.commitUrl,'Commit '+node.commit.slice(0,8)));
    const next={...result.request,centro:id,red:node.type==='concepto'?'ideas':result.request.red};
    links.push(link(mapURL(next).href,'Centrar un mapa en este nodo'));
    get('node-links').replaceChildren(...links.filter(Boolean));
    const connections=get('node-edges');
    connections.replaceChildren();
    const visibleEdges=result.edges.filter(edge=>edge.from===id||edge.to===id);
    for(const edge of visibleEdges.sort((a,b)=>Number(b.route)-Number(a.route))) {
      const outbound=edge.from===id;
      const other=selectedById.get(outbound?edge.to:edge.from);
      const li=element('li');
      li.append(element('strong',(outbound?'→ ':'← ')+other.title+' · '+edge.kind));
      if(edge.reading)li.append(element('p',edge.reading));
      if(edge.condition)li.append(element('p',edge.condition));
      const evidence=link(edge.evidence,'Evidencia de la relación');
      if(evidence)li.append(evidence);
      connections.append(li);
    }
    if(!visibleEdges.length)connections.append(element('li','Este nodo aparece sin relaciones en la selección.'));
    for(const button of items.querySelectorAll('button'))button.setAttribute('aria-current',String(button.dataset.id===id));
    for(const dot of plot.querySelectorAll('.map-dot'))dot.classList.toggle('selected',dot.dataset.id===id);
  }

  function draw() {
    plot.replaceChildren();
    const groups=result.layers.map(layer=>result.nodes.filter(node=>node.distance===layer.distance));
    const radii=[0];
    for(let index=1;index<groups.length;index++) {
      radii[index]=Math.max(radii[index-1]+72,groups[index].length*27/(2*Math.PI));
    }
    const size=Math.max(260,(radii.findLast((_,i)=>groups[i].length)??0)+34)*2;
    const center=size/2;
    plot.setAttribute('viewBox',`0 0 ${size} ${size}`);
    const defs=svgElement('defs');
    const marker=svgElement('marker',{id:'arrow',markerWidth:7,markerHeight:7,refX:6,refY:3,orient:'auto',viewBox:'0 0 6 6'});
    marker.append(svgElement('path',{d:'M0 0 L6 3 L0 6 Z',fill:'#758d94'}));
    defs.append(marker);
    plot.append(defs);
    const positions=new Map();
    for(const [distance,group] of groups.entries()) {
      if(distance&&group.length)plot.append(svgElement('circle',{class:'ring',cx:center,cy:center,r:radii[distance]}));
      group.forEach((node,index)=>{
        const angle=-Math.PI/2+index*2*Math.PI/group.length+(distance>1?distance*.24:0);
        positions.set(node.id,{x:center+radii[distance]*Math.cos(angle),y:center+radii[distance]*Math.sin(angle),r:distance?11:18});
      });
    }
    for(const edge of result.edges) {
      if(!edge.route&&!get('extra').checked)continue;
      const from=positions.get(edge.from),to=positions.get(edge.to);
      if(from===to)continue;
      const dx=to.x-from.x,dy=to.y-from.y,length=Math.hypot(dx,dy);
      const x=dx/length,y=dy/length;
      const line=svgElement('line',{x1:from.x+x*from.r,y1:from.y+y*from.r,x2:to.x-x*(to.r+2),y2:to.y-y*(to.r+2),
        class:edge.route?'map-edge':'map-edge cross','marker-end':'url(#arrow)'});
      plot.append(line);
    }
    result.nodes.forEach((node,index)=>{
      const {x,y,r}=positions.get(node.id);
      const dot=svgElement('g',{class:'map-dot'+(node.type==='concepto'?' concept':'')+(node.id===selected?' selected':''),
        role:'button',tabindex:0,'aria-label':`${index+1}. ${node.title}`});
      dot.dataset.id=node.id;
      const title=svgElement('title');
      title.textContent=node.title;
      const number=svgElement('text',{x,y});
      number.textContent=index+1;
      dot.append(title,svgElement('circle',{cx:x,cy:y,r}),number);
      dot.addEventListener('click',()=>inspect(node.id));
      dot.addEventListener('keydown',event=>{
        if(event.key==='Enter'||event.key===' ') {event.preventDefault();inspect(node.id);}
      });
      plot.append(dot);
    });
  }

  function display(next) {
    result=next;
    selected=result.center;
    selectedById=new Map(result.nodes.map(node=>[node.id,node]));
    get('map-title').textContent=selectedById.get(selected).title;
    const count=result.shown===1?'1 nodo visible':result.shown+' nodos visible';
    get('map-info').textContent=`${count} de ${result.reachable} al alcance · radio ${result.request.radio} · `+
      (result.request.pesos.length?result.request.pesos.map(p=>labels[p.tag]+' '+percent.format(p.normalized)).join(' · '):'sin ponderación temática');
    items.replaceChildren();
    for(const node of result.nodes) {
      const li=element('li');
      const button=element('button',node.title+' · '+typeName(node)+' · '+distanceName(node.distance));
      button.type='button'; button.dataset.id=node.id;
      button.addEventListener('click',()=>inspect(node.id));
      li.append(button);items.append(li);
    }
    get('open-full').href=mapURL(result.request).href;
    get('positioning-upgrade').href=positioningURL().href;
    get('open-full').hidden=!embedded;
    get('result').hidden=false;
    get('status').textContent='';
    for(const id of ['copy-link','copy-embed','download'])get(id).disabled=false;
    draw();
    inspect(selected);
  }

  function update(request,changeAddress) {
    try {
      display(calculate(graph,request));
      if(changeAddress)history.replaceState(null,'',mapURL(result.request));
    } catch(error) {
      get('status').textContent=error.message;
    }
  }
  form.addEventListener('submit',event=>{
    event.preventDefault();
    get('copy-fallback').hidden=true;
    const config=new URLSearchParams(new FormData(form));
    for(const [tag,value] of weights)config.append('peso',tag+':'+value);
    if(get('only').checked)config.set('solo','1');
    try {update(readRequest(config,labels),true);}
    catch(error) {get('status').textContent=error.message;}
  });
  get('extra').addEventListener('change',draw);
  async function copy(text) {
    try {
      await navigator.clipboard.writeText(text);
      get('status').textContent='Copied.';
    } catch {
      const field=get('copy-fallback');
      field.hidden=false;field.value=text;field.focus();field.select();
    }
  }
  get('copy-link').addEventListener('click',()=>copy(mapURL(result.request).href));
  get('copy-embed').addEventListener('click',()=>{
    const url=mapURL(result.request,true).href.replaceAll('&','&amp;');
    copy(`<iframe src="${url}" title="Mapa de relationships · Perspective Beyond" loading="lazy" style="width:100%;height:720px;border:0"></iframe>`);
  });
  get('download').addEventListener('click',()=>{
    const blob=new Blob([JSON.stringify(result,null,2)+'\n'],{type:'application/json;charset=utf-8'});
    const url=URL.createObjectURL(blob);
    const a=element('a');a.href=url;a.download='perspective-beyond-'+result.center+'.json';
    document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  let initial;
  try {initial=readRequest(params,labels);}
  catch(error) {get('status').textContent=error.message;}
  const defaults=initial??readRequest(new URLSearchParams(),labels);
  get('center').value=initial?.centro??params.get('centro')??defaults.centro;
  get('radius').value=defaults.radio;get('limit').value=defaults.max;
  get('network').value=defaults.red;get('direction').value=defaults.sentido;
  for(const peso of defaults.pesos)weights.set(peso.tag,String(peso.value));
  get('only').checked=defaults.solo;
  weightRows();
  get('weight-settings').open=weights.size>0;
  form.hidden=embedded;
  if(initial)update(initial,false);
}
if(embedded&&params.get('metodo')!=='saltos')location.replace(positioningURL(true));
else start().catch(error=>{get('status').textContent=error.message;});
