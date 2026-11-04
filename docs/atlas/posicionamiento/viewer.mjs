import {readPosition,positionMap,positionParams} from '../positioning.mjs';
const get=id=>document.getElementById(id),ns='http://www.w3.org/2000/svg';
const initial=new URLSearchParams(location.search),embedded=initial.get('embed')==='1';
if(embedded)document.body.classList.add('embed');
const number=new Intl.NumberFormat('es'),percent=new Intl.NumberFormat('es',{style:'percent',maximumFractionDigits:2});
const element=(tag,text)=>{const n=document.createElement(tag);if(text)n.textContent=text;return n;};
const svg=(tag,attrs)=>{const n=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);return n;};
function link(url,label){const a=element('a',label);a.href=url;return a;}
const type=n=>n.type==='ficha'?'Ficha':n.type==='concepto'?'Concepto':'Documento de origen';
async function start(){
 const response=await fetch('../mapa/grafo.json?v=posicionamiento-2');if(!response.ok)throw Error('El Atlas no está disponible ahora.');const graph=await response.json();
 const all=new Map(graph.nodes.map(n=>[n.id,n])),labels=new Map(Object.entries(graph.topics).map(([k,v])=>['tema:'+k,v]));
 for(const[k,v]of Object.entries(graph.clusters))labels.set('cluster:'+k,v);
 for(const[k,v]of Object.entries(graph.voices))labels.set('voz:'+k,v.label);
 for(const n of graph.nodes)if(n.type==='concepto')labels.set('concepto:'+n.id,n.title);
 const weights=new Map();let result,selected,byId;
 for(const[k,label]of labels)get('topic').add(new Option(label,k));
 get('site').add(new Option('Toda la constelación','all'));for(const[k,v]of Object.entries(graph.clusters))get('site').add(new Option(v,k));
 for(const d of graph.documents){const o=element('option');o.value=d.url;o.label=d.title;get('positions').append(o);}
 for(const n of graph.nodes){const o=element('option');o.value=n.id;o.label=n.title;get('positions').append(o);}
 function bridges(){
  const selected=get('bridge').value,keys=Object.keys(graph.entryRoutes.clusters[get('site').value]?.porous??{});
  get('bridge').replaceChildren(...keys.map(id=>{const e=graph.edges.find(e=>e[0]==='documento:'+id);return new Option(e?all.get(e[1]).title+' → '+all.get(e[2]).title:id,id);}));
  if(keys.includes(selected))get('bridge').value=selected;get('bridge-field').hidden=get('mode').value!=='porous';
 }
 function weightRows(){
  get('weights').replaceChildren();const total=[...weights.values()].reduce((s,v)=>s+Number(v),0);
  for(const[k,v]of weights){const row=element('div');row.className='weight-row';const input=element('input');input.type='number';input.min='.0001';input.max='10000';input.step='any';input.value=v;input.required=true;input.setAttribute('aria-label','Peso de '+labels.get(k));input.addEventListener('input',()=>{weights.set(k,input.value);const total=[...weights.values()].reduce((s,v)=>s+Number(v),0);for(const r of get('weights').children)r.querySelector('.weight-share').textContent=total>0?percent.format(Number(weights.get(r.dataset.key))/total):'';});
   const share=element('span',total>0?percent.format(Number(v)/total):'');share.className='weight-share';row.dataset.key=k;
   const remove=element('button','Quitar');remove.type='button';remove.className='secondary';remove.addEventListener('click',()=>{weights.delete(k);weightRows();});row.append(element('span',labels.get(k)),input,share,remove);get('weights').append(row);}
 }
 get('add-weight').addEventListener('click',()=>{if(!weights.has(get('topic').value)&&weights.size<20){weights.set(get('topic').value,1);weightRows();}});
 get('mode').addEventListener('change',bridges);get('site').addEventListener('change',bridges);
 const mapURL=(r,embed=false)=>{const u=new URL('./',location.href);u.search=positionParams(r);if(embed)u.searchParams.set('embed','1');return u;};
 function inspect(id){
  selected=id;const n=byId.get(id);get('node-meta').textContent=type(n)+' · '+(n.distance===0?'posicionamiento':n.distance===1?'una conexión desde el documento':n.distance+' conexiones desde el documento');get('node-title').textContent=n.title;get('node-summary').textContent=n.summary||n.readingSummary||'';
  get('composition').replaceChildren();get('profile-title').hidden=!Object.keys(n.tagWeights??{}).length;
  for(const[k,w]of Object.entries(n.tagWeights??{}).sort((a,b)=>b[1]-a[1])){const row=element('div');row.className='composition-row';const bar=element('progress');bar.max=1;bar.value=w;bar.setAttribute('aria-label',graph.topics[k]+' '+percent.format(w));row.append(element('span',graph.topics[k]),element('strong',percent.format(w)),bar);get('composition').append(row);}
  const next=new URL('./',location.href);const p=positionParams(result.request);p.set('posicionamiento',n.type==='documento'?result.position.url:n.id);next.search=p;
  get('node-links').replaceChildren(link(n.url,n.type==='documento'?'Abrir documento de origen':'Abrir ficha'),link(next.href,'Usar como posicionamiento'));
  if(n.original&&n.original!==n.url)get('node-links').append(link(n.original,'Documento de origen'));
  get('node-edges').replaceChildren();for(const e of result.edges.filter(e=>e.from===id||e.to===id)){const other=byId.get(e.from===id?e.to:e.from);const li=element('li');li.append(element('strong',(e.from===id?'→ ':'← ')+other.title),element('p',e.reading||e.kind));get('node-edges').append(li);}
  for(const b of get('node-list').querySelectorAll('button'))b.setAttribute('aria-current',String(b.dataset.id===id));
  for(const dot of get('graph').querySelectorAll('.map-dot'))dot.classList.toggle('selected',dot.dataset.id===id);
 }
 function draw(){
  const plot=get('graph');plot.replaceChildren();const groups=result.layers.map(l=>result.nodes.filter(n=>n.distance===l.distance)),radii=[0];
  for(let i=1;i<groups.length;i++)radii[i]=Math.max(radii[i-1]+75,groups[i].length*27/(2*Math.PI));
  const radius=Math.max(255,(radii.findLast((_,i)=>groups[i].length)??0)+35),center=radius;plot.setAttribute('viewBox',`0 0 ${radius*2} ${radius*2}`);
  const defs=svg('defs',{}),marker=svg('marker',{id:'pos-arrow',markerWidth:7,markerHeight:7,refX:6,refY:3,orient:'auto',viewBox:'0 0 6 6'});marker.append(svg('path',{d:'M0 0 L6 3 L0 6 Z',fill:'#758d94'}));defs.append(marker);plot.append(defs);
  const positions=new Map();groups.forEach((group,d)=>{if(d&&group.length)plot.append(svg('circle',{class:'ring',cx:center,cy:center,r:radii[d]}));group.forEach((n,i)=>{const a=-Math.PI/2+i*2*Math.PI/group.length+d*.2;positions.set(n.id,{x:center+radii[d]*Math.cos(a),y:center+radii[d]*Math.sin(a),r:d?12:20});});});
  for(const e of result.edges){if(!e.route&&!get('extra').checked)continue;const a=positions.get(e.from),b=positions.get(e.to);if(!a||!b)continue;const dx=b.x-a.x,dy=b.y-a.y,length=Math.hypot(dx,dy);if(!length)continue;const x=dx/length,y=dy/length;plot.append(svg('line',{x1:a.x+x*a.r,y1:a.y+y*a.r,x2:b.x-x*(b.r+2),y2:b.y-y*(b.r+2),class:e.route?'map-edge':'map-edge cross','marker-end':'url(#pos-arrow)'}));}
  result.nodes.forEach((n,i)=>{const p=positions.get(n.id),dot=svg('g',{class:'map-dot '+n.type+(n.id===selected?' selected':''),role:'button',tabindex:0,'aria-label':n.title});dot.dataset.id=n.id;const title=svg('title',{});title.textContent=n.title;const label=svg('text',{x:p.x,y:p.y});label.textContent=i+1;dot.append(title,svg('circle',{cx:p.x,cy:p.y,r:p.r}),label);dot.addEventListener('click',()=>inspect(n.id));dot.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();inspect(n.id);}});plot.append(dot);});
 }
 function display(r){
  result=r;selected=r.center;byId=new Map(r.nodes.map(n=>[n.id,n]));get('result').hidden=false;get('map-title').textContent=r.position.title;get('map-info').textContent=r.position.url;
  get('stats').replaceChildren(...[number.format(r.budget.used)+' / '+number.format(r.budget.limit)+' tokens de lectura',r.selected+' fichas y conceptos seleccionados',r.shown+' piezas visibles'].map(x=>element('strong',x)));
  get('frontier').textContent=(r.omittedInDiagram?r.omittedInDiagram+' piezas adicionales están en la lectura descargable. ':'')+(r.budget.nextBlock?'La siguiente incorporación necesita '+Math.max(0,r.budget.used+r.budget.nextBlock-r.budget.limit)+' tokens más.':'El recorrido ha incluido todas las piezas alcanzables de esta selección.');
  get('node-list').replaceChildren(...r.nodes.map(n=>{const li=element('li'),b=element('button',n.title+' · '+type(n));b.type='button';b.dataset.id=n.id;b.addEventListener('click',()=>inspect(n.id));li.append(b);return li;}));
  get('reading').textContent=r.reading;get('accounting').textContent='Cuenta de lectura con '+r.budget.encoding+': '+r.budget.accounting;
  get('document-cards').replaceChildren(...(r.position.fichas.length?r.position.fichas:r.position.entrySources??[]).map(id=>{const li=element('li');li.append(link(all.get(id).url,all.get(id).title));return li;}));
  get('open-full').hidden=!embedded;get('open-full').href=mapURL(r.request).href;get('status').textContent='';for(const id of ['copy-link','copy-assistant','download-text','download-json'])get(id).disabled=false;draw();inspect(selected);
 }
 function update(p,change){try{display(positionMap(graph,readPosition(p,graph)));if(change)history.replaceState(null,'',mapURL(result.request));}catch(e){get('status').textContent=e.message;for(const id of ['copy-link','copy-assistant','download-text','download-json'])get(id).disabled=true;}}
 get('settings').addEventListener('submit',e=>{e.preventDefault();const p=new URLSearchParams(new FormData(get('settings')));for(const key of ['rol','lectura','enfoque','instruccion'])if(initial.has(key))p.set(key,initial.get(key));for(const[k,v]of weights)p.append('peso',k+':'+v);if(!get('only').checked)p.delete('solo');update(p,true);});
 get('extra').addEventListener('change',draw);
 async function copy(text){get('copy-fallback').value=text;try{await navigator.clipboard.writeText(text);get('status').textContent='Copiado.';}catch{get('copy-fallback').hidden=false;get('copy-fallback').focus();get('copy-fallback').select();}}
 get('copy-link').addEventListener('click',()=>copy(mapURL(result.request).href));
 get('copy-assistant').addEventListener('click',()=>{const u=new URL('https://raw.githubusercontent.com/dakleyer/perspective-beyond/main/docs/atlas/posicionamiento/entrada.txt');u.search=positionParams(result.request);for(const key of ['rol','lectura','instruccion'])if(initial.has(key))u.searchParams.set(key,initial.get(key));copy(u.href);});
 function download(text,name,mime){const u=URL.createObjectURL(new Blob([text],{type:mime})),a=link(u,name);a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000);}
 get('download-text').addEventListener('click',()=>download(result.reading,'atlas-posicionamiento.md','text/markdown;charset=utf-8'));
 get('download-json').addEventListener('click',()=>download(JSON.stringify(result,null,2),'atlas-posicionamiento.json','application/json;charset=utf-8'));
 let request;try{request=readPosition(initial,graph);}catch(e){get('status').textContent=e.message;}
 const defaults=request??readPosition(new URLSearchParams(),graph);
 get('position').value=request?.posicionamiento??initial.get('posicionamiento')??initial.get('centro')??defaults.posicionamiento;get('tokens').value=defaults.tokens;get('limit').value=defaults.max;get('site').value=defaults.site??all.get(defaults.position.focus??defaults.position.seeds?.[0]??defaults.position.fichas[0])?.clusters[0]??'all';get('mode').value=defaults.modo;get('network').value=defaults.red;get('direction').value=defaults.sentido;bridges();if(defaults.puente)get('bridge').value=defaults.puente;
 for(const p of defaults.pesos)weights.set(p.tag,p.value);get('only').checked=defaults.solo;weightRows();get('settings').hidden=embedded;if(request)display(positionMap(graph,request));
}
start().catch(e=>get('status').textContent=e.message);
