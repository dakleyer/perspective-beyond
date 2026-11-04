(()=>{'use strict';
const root=document.getElementById('pb-institutional-atlas');if(!root)return;
let context;try{context=JSON.parse(root.dataset.pbivContext);}catch{return;}
const translations={es:{concept:'Concepto',page:'Lectura en esta web',ficha:'Ficha del Atlas',source:'Esta página',concepts:'CONCEPTOS',readings:'LECTURAS CONECTADAS',read:'Leer esta conexión',copied:'Pregunta y entrada copiadas.',error:'Puedes seleccionar y copiar el texto de la pregunta.',loadError:'Las lecturas siguen disponibles en los enlaces de esta página.'},en:{concept:'Concept',page:'Reading on this website',ficha:'Atlas card',source:'This page',concepts:'CONCEPTS',readings:'CONNECTED READINGS',read:'Read this connection',copied:'Question and entry copied.',error:'You can select and copy the question text.',loadError:'The readings remain available through the links on this page.'},fr:{concept:'Concept',page:'Lecture sur ce site',ficha:'Fiche de l’Atlas',source:'Cette page',concepts:'CONCEPTS',readings:'LECTURES RELIÉES',read:'Lire ce lien',copied:'Question et entrée copiées.',error:'Vous pouvez sélectionner et copier le texte.',loadError:'Les lectures restent disponibles dans les liens de cette page.'}};
const t=translations[context.lang]||translations.es,SVG='http://www.w3.org/2000/svg';let record,loaded=false;
function el(tag,attrs={},text){const n=document.createElement(tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);if(text!==undefined)n.textContent=text;return n;}
function svg(tag,attrs={},text){const n=document.createElementNS(SVG,tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);if(text!==undefined)n.textContent=text;return n;}
function wrap(text,max=28,lines=3){const words=text.split(/\s+/),out=[];let line='';for(const w of words){if(line&&line.length+w.length+1>max){out.push(line);line=w;}else line+=(line?' ':'')+w;}if(line)out.push(line);if(out.length>lines){out.length=lines;out[lines-1]=out[lines-1].replace(/[.,:;]$/,'')+'…';}return out;}
function choose(id){const item=id===record.source.id?{...record.source,type:'source'}:record.nodes.find(n=>n.id===id);if(!item)return;
 root.querySelectorAll('[data-pbiv-node]').forEach(n=>{const selected=n.dataset.pbivNode===id;n.dataset.selected=String(selected);if(n.tagName==='BUTTON')n.setAttribute('aria-pressed',String(selected));});
 root.querySelectorAll('[data-pbiv-edge]').forEach(n=>{n.dataset.selected=String(n.dataset.from===id||n.dataset.to===id);});
 const area=root.querySelector('[data-pbiv-selection]');area.replaceChildren(el('p',{class:'pbiv-type'},t[item.type]),el('h3',{},item.title));
 if(item.summary)area.append(el('p',{},item.summary));
 if(item.type==='source')area.append(el('p',{},record.question));else if(item.relation)area.append(el('p',{},item.relation));
 area.append(el('a',{href:item.url},t.read+' ↗'));
}
function render(r){record=r;if(!context.known){const nextId='page:'+context.key;record={...r,source:{id:nextId,title:context.title,url:context.url,summary:'',fichas:[]},edges:r.edges.map(e=>({...e,from:e.from===r.source.id?nextId:e.from,to:e.to===r.source.id?nextId:e.to}))};}
 const stage=svg('svg',{viewBox:'0 0 960 650',role:'group','aria-label':context.title});
 stage.append(svg('title',{},context.title),svg('desc',{},root.querySelector('.pbiv-guide').textContent));
 const positions=new Map([[record.source.id,{x:480,y:74,w:370,h:94}]]),concepts=record.nodes.filter(n=>n.type==='concept'),readings=record.nodes.filter(n=>n.type!=='concept');
 concepts.forEach((n,i)=>positions.set(n.id,{x:166,y:255+i*140,w:274,h:88}));readings.forEach((n,i)=>positions.set(n.id,{x:775,y:183+i*103,w:292,h:84}));
 stage.append(svg('text',{x:30,y:182,class:'pbiv-map-label'},t.concepts),svg('text',{x:630,y:132,class:'pbiv-map-label'},t.readings));
 for(const e of record.edges){const a=positions.get(e.from),b=positions.get(e.to);if(!a||!b)continue;const c=(a.x+b.x)/2;const path=svg('path',{d:`M ${a.x} ${a.y} C ${c} ${a.y}, ${c} ${b.y}, ${b.x} ${b.y}`,class:'pbiv-edge','data-pbiv-edge':'','data-from':e.from,'data-to':e.to});path.append(svg('title',{},e.label));stage.append(path);}
 for(const n of [{...record.source,type:'source'},...record.nodes]){const p=positions.get(n.id),group=svg('g',{class:'pbiv-node',role:'button',tabindex:'0','aria-label':n.title,'data-pbiv-node':n.id,'data-kind':n.type});group.append(svg('title',{},n.title),svg('rect',{x:p.x-p.w/2,y:p.y-p.h/2,width:p.w,height:p.h,rx:9}));const lines=wrap(n.title,n.type==='source'?40:30,3),text=svg('text',{'text-anchor':'middle'});lines.forEach((line,i)=>text.append(svg('tspan',{x:p.x,y:p.y-(lines.length-1)*10+i*20},line)));group.append(text);group.addEventListener('click',()=>choose(n.id));group.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();choose(n.id);}});stage.append(group);}
 root.querySelector('[data-pbiv-map]').replaceChildren(stage);
 const mobile=root.querySelector('[data-pbiv-mobile]');for(const n of [{...record.source,type:'source'},...record.nodes]){const b=el('button',{type:'button','data-pbiv-node':n.id,'aria-pressed':'false'},t[n.type]+' · '+n.title);b.addEventListener('click',()=>choose(n.id));mobile.append(b);}
 choose(record.source.id);root.dataset.ready='true';
}
root.querySelector('.pbiv-main').addEventListener('toggle',async event=>{if(!event.target.open||loaded)return;loaded=true;try{const response=await fetch(context.registry,{credentials:'omit'});if(!response.ok)throw Error('Unavailable');const data=await response.json();render(data.pages[context.key]||data.pages[data.defaults[context.cluster]]);}catch{loaded=false;root.querySelector('[data-pbiv-selection]').textContent=t.loadError;} });
root.querySelector('[data-pbiv-copy]').addEventListener('click',async()=>{const status=root.querySelector('[data-pbiv-copy-status]');try{await navigator.clipboard.writeText(root.querySelector('.pbiv-prompt').value);status.textContent=t.copied;}catch{root.querySelector('.pbiv-prompt').select();status.textContent=t.error;}});
const main=document.querySelector('main');if(main&&!main.contains(root))main.append(root);
// Upgrade the earlier entry in its existing place while retaining its original source markup.
const legacy=document.getElementById('constelacion-nueva-perspectiva');
if(legacy&&!legacy.contains(root)){
 const alias=legacy.id;legacy.id=alias+'-previous';legacy.hidden=true;legacy.classList.add('pbiv-previous-entry');legacy.setAttribute('aria-hidden','true');legacy.insertAdjacentElement('afterend',root);root.prepend(el('span',{id:alias,class:'pbiv-legacy-anchor','aria-hidden':'true'}));
}
const pageHeading=document.querySelector('main h1')||document.querySelector('h1');
if(pageHeading&&!root.contains(pageHeading)){
 const label=context.lang==='en'?'Explore the map of this reading':context.lang==='fr'?'Explorer la carte de cette lecture':'Explorar el mapa de esta lectura';
 const shortcut=el('p',{class:'pbiv-shortcut'}),link=el('a',{href:'#pb-institutional-atlas'},label+' →');
 link.addEventListener('click',()=>{root.querySelector('.pbiv-main').open=true;});shortcut.append(link);pageHeading.insertAdjacentElement('afterend',shortcut);
}
})();
