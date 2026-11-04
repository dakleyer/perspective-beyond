import {parseFocusWeights} from './session-config.mjs';

export const VERSION='perspective-beyond/positioning-v1';
const cmp=(a,b)=>a<b?-1:a>b?1:0;
export function canonicalURL(raw,fragment=false){
 try{const u=new URL(raw);u.protocol='https:';u.hostname=u.hostname.toLowerCase().replace(/^www\./,'');u.pathname=u.pathname.replace(/\/$/,'')||'/';
  for(const k of [...u.searchParams.keys()])if(/^utm_/i.test(k)||['gclid','fbclid'].includes(k))u.searchParams.delete(k);
  u.searchParams.sort();if(!fragment)u.hash='';return u.href;
 }catch{return '';}
}
export function resolvePosition(graph,value){
 const selected=graph.positionings[value];
 if(selected)value=selected.source??selected.url;
 const nodes=new Map(graph.nodes.map(n=>[n.id,n]));
 const exact=nodes.get(value);
 if(exact?.type==='concepto')return {id:exact.id,title:exact.title,url:exact.url,fichas:[exact.id],type:'concepto',focus:exact.id,
  header:'# Posicionamiento · '+exact.title+'\nConcepto de entrada: '+exact.url+'\n\n',headerTokens:exact.positionHeaderTokens};
 let focus=exact;
 if(!focus&&canonicalURL(value,true)){
  const url=canonicalURL(value,true);
  const matches=graph.nodes.filter(n=>[n.url,n.original,...(n.aliases??[])].some(u=>u&&canonicalURL(u,true)===url));
  // A plain document URL may contain several fichas. Preserve that grouping.
  if(matches.length===1)focus=matches[0];
 }
 let document=focus?.documentId?graph.documents.find(d=>d.id===focus.documentId):graph.documents.find(d=>d.id===value);
 if(!document){const url=canonicalURL(value);document=graph.documents.find(d=>canonicalURL(d.url)===url||d.aliases.some(a=>canonicalURL(a)===url));}
 if(!document)throw Error('El posicionamiento no corresponde a un documento o ficha del Atlas.');
 return {...document,type:'documento',focus:focus?.id??null,seeds:focus?[focus.id]:(document.entrySources??document.fichas)};
}
function integer(params,key,fallback,min,max){
 const raw=params.get(key)??String(fallback),n=Number(raw);
 if(!/^\d+$/.test(raw)||!Number.isSafeInteger(n)||n<min||n>max)throw Error(key+' debe estar entre '+min+' y '+max+'.');return n;
}
export function readPosition(params,graph){
 const point=params.get('posicionamiento')??params.get('desde')??params.get('centro')??params.get('site')??'imsv';
 const position=resolvePosition(graph,point);
 const mode=params.get('modo')??'federated',site=params.get('site');
 if(!['closed','porous','federated'].includes(mode))throw Error('Elige un alcance Cerrado, Poroso o Federado.');
 if(site&&site!=='all'&&!Object.hasOwn(graph.clusters,site))throw Error('Elige un clúster del Atlas.');
 if(mode!=='federated'&&(!site||!Object.hasOwn(graph.clusters,site)))throw Error('El posicionamiento necesita un clúster para ese alcance.');
 const allowed=[...Object.keys(graph.topics).map(k=>'tema:'+k),...Object.keys(graph.clusters).map(k=>'cluster:'+k),
  ...Object.keys(graph.voices??{}).map(k=>'voz:'+k),...graph.nodes.filter(n=>n.type==='concepto').map(n=>'concepto:'+n.id)];
 const tokens=params.getAll('peso').map(p=>/^(tema|cluster|voz|concepto):/i.test(p)?p:'tema:'+p);
 const parsed=parseFocusWeights(tokens,allowed);
 if(parsed.errors.length)throw Error(parsed.errors.join(' '));
 const total=[...parsed.weights.values()].reduce((a,b)=>a+b,0);
 const weights=[...parsed.weights].sort(([a],[b])=>cmp(a,b)).map(([tag,value])=>({tag,value,normalized:value/total}));
 const strict=params.get('solo')==='1';
 if(strict&&!weights.some(w=>w.tag.startsWith('tema:')))throw Error('Elige al menos una etiqueta temática para la selección exclusiva.');
 const rol=params.get('rol')??'lector',lectura=params.get('lectura')??'explore';
 const enfoque=params.get('enfoque')??(weights.length?'personalizado':'parejo');
 if(!['parejo','transversal','personalizado'].includes(enfoque))throw Error('Elige un enfoque de lectura del Atlas.');
 if(!Object.hasOwn(graph.sessionProfiles.roles,rol)||!Object.hasOwn(graph.sessionProfiles.purposes,lectura))throw Error('Elige un rol y un propósito del Atlas.');
 return {posicionamiento:point,position,tokens:integer(params,'tokens',2000,64,2000000),max:integer(params,'max',60,1,120),rol,lectura,enfoque,instruccion:(params.get('instruccion')??'').slice(0,500),
  red:params.get('red')??'ideas',sentido:params.get('sentido')??'ambas',modo:mode,site,puente:mode==='porous'?params.get('puente'):null,
  solo:strict,pesos:weights};
}
export function nodeText(node,topics){
 const tags=Object.entries(node.tagWeights).sort(([a],[b])=>cmp(a,b)).map(([k,v])=>topics[k]+' '+(v*100).toFixed(2)+'%').join('; ');
 return '## '+node.title+'\n'+(node.reading??node.summary)+'\nEtiquetas: '+tags+'\nFicha: '+node.url+'\n'+(node.original?'Documento de origen: '+node.original+'\n':'')+'\n';
}
export function edgeText(edge,nodes){return nodes.get(edge[1]).title+' → '+nodes.get(edge[2]).title+' · '+edge[3]+'. '+edge[4]+(edge[5]?'\nFuente de la relación: '+edge[5]:'')+'\n\n';}

export function positionMap(graph,request){
 if(!['ideas','documentos'].includes(request.red)||!['ambas','salientes','entrantes'].includes(request.sentido))throw Error('Revisa el tipo o el sentido de las relaciones.');
 const all=new Map(graph.nodes.map(n=>[n.id,n]));
 const support=new Map();
 for(const e of graph.edges)if(e[6]==='apoyo'){if(!support.has(e[1]))support.set(e[1],new Set());support.get(e[1]).add(e[2]);}
 const voice=new Map(Object.entries(graph.voices??{}).map(([id,v])=>[id,new Set(v.sources)]));
 const allowed=new Set(request.modo==='federated'?Object.keys(graph.clusters):[request.site]);
 const universe=[...graph.edges,...(graph.navigation??[])];
 let bridge=null;
 if(request.modo==='porous'){
  bridge=universe.find(e=>e[0]===request.puente||e[0]==='documento:'+request.puente);
  if(!bridge)throw Error('Elige un puente registrado para ese posicionamiento.');
  const from=all.get(bridge[1]),to=all.get(bridge[2]);
  if(!from.clusters.includes(request.site)||to.clusters.includes(request.site))throw Error('El puente debe salir del clúster elegido.');
  to.clusters.forEach(k=>allowed.add(k));
 }
 const value=(node,key)=>{
  const at=key.indexOf(':'),type=key.slice(0,at),id=key.slice(at+1);
  if(type==='tema')return node.tagWeights[id]??0;
  if(type==='cluster')return node.clusters.includes(id)?1:0;
  if(type==='voz')return voice.get(id)?.has(node.id)?1:0;
  return node.id===id||support.get(node.id)?.has(id)?1:0;
 };
 const affinity=new Map(graph.nodes.map(n=>[n.id,request.pesos.length?request.pesos.reduce((s,p)=>s+p.normalized*value(n,p.tag),0):1]));
 const eligible=node=>node.clusters.every(k=>allowed.has(k))&&(request.red==='ideas'||node.type==='ficha')&&
  (request.modo!=='porous'||node.clusters.every(k=>k===request.site)||node.clusters.every(k=>k!==request.site))&&
  (!request.solo||request.pesos.some(p=>p.tag.startsWith('tema:')&&value(node,p.tag)>0));
 const seeds=(request.position.seeds??request.position.fichas).filter(id=>eligible(all.get(id))&&(request.modo!=='porous'||all.get(id).clusters.every(k=>k===request.site)));
 if(!seeds.length)throw Error('Las fichas del documento quedan fuera de esta selección. Ajusta las etiquetas, el alcance o el posicionamiento.');
 const activeEdges=universe.filter(e=>eligible(all.get(e[1]))&&eligible(all.get(e[2]))&&
  (request.red==='ideas'||['documento','navegacion'].includes(e[6]))&&
  (request.modo!=='porous'||all.get(e[1]).clusters.some(k=>all.get(e[2]).clusters.includes(k))||e[0]===bridge[0]));
 const adjacent=new Map();
 const arc=(from,to,e)=>{if(from===to)return;if(!adjacent.has(from))adjacent.set(from,[]);adjacent.get(from).push({to,edge:e});};
 for(const e of activeEdges){
  if(request.sentido!=='entrantes')arc(e[1],e[2],e);
  if(request.sentido!=='salientes'&&!(request.modo==='porous'&&e[0]===bridge[0]))arc(e[2],e[1],e);
 }
 for(const list of adjacent.values())list.sort((a,b)=>affinity.get(b.to)-affinity.get(a.to)||cmp(a.to,b.to)||cmp(a.edge[0],b.edge[0]));
 const visits=new Map(seeds.map(id=>[id,{distance:1,parent:null,edge:null}])),queue=[...seeds].sort((a,b)=>affinity.get(b)-affinity.get(a)||cmp(a,b));
 for(let i=0;i<queue.length;i++)for(const item of adjacent.get(queue[i])??[]){
  if(visits.has(item.to))continue;
  visits.set(item.to,{distance:visits.get(queue[i]).distance+1,parent:queue[i],edge:item.edge});queue.push(item.to);
 }
 const priority=id=>(.25+.75*affinity.get(id))/(1+visits.get(id).distance);
 const order=[...queue].sort((a,b)=>priority(b)-priority(a)||visits.get(a).distance-visits.get(b).distance||cmp(a,b));
 // This sequence is independent of the budget: increasing tokens preserves the selected prefix.
 const sequence=[],seen=new Set();
 for(const id of order){
  const path=[];for(let at=id;at&&!seen.has(at);at=visits.get(at).parent)path.push(at);
  for(const at of path.reverse()){seen.add(at);sequence.push(at);}
 }
 let used=request.position.headerTokens;const selected=[];let nextCost=null;
 if(used>request.tokens)throw Error('La cabecera del documento necesita '+used+' tokens. Amplía el presupuesto.');
 for(const id of sequence){
  const visit=visits.get(id),cost=all.get(id).contextTokens+(visit.edge?graph.edgeTokenCosts[visit.edge[0]]:0);
  if(used+cost>request.tokens){nextCost=cost;break;}used+=cost;selected.push(id);
 }
 const picked=new Set(selected);
 const root={id:request.position.id+'-entrada',title:request.position.title,type:request.position.type,
  url:request.position.url,original:request.position.url,summary:request.position.type==='documento'?'Documento desde el que se abre este posicionamiento.':'Concepto desde el que se abre este posicionamiento.',tags:[],tagWeights:{},clusters:[...allowed],distance:0,parent:null};
 const chosen=selected.map(id=>({...all.get(id),...visits.get(id),edge:undefined,routeEdge:visits.get(id).edge?.[0]??null,parent:visits.get(id).parent??root.id,affinity:affinity.get(id)}));
 // Display a connected prefix; the downloadable reading retains the entire selection.
 const visible=chosen.slice(0,Math.max(0,request.max-1)),visibleIds=new Set([root.id,...visible.map(n=>n.id)]);
 const edges=[];
 for(const n of visible){const v=visits.get(n.id);if(v.edge){const e=v.edge;edges.push({id:e[0],from:e[1],to:e[2],kind:e[3],reading:e[4],evidence:e[5],route:true});}
  else {const owned=request.position.fichas.includes(n.id);edges.push({id:'contiene:'+root.id+':'+n.id,from:root.id,to:n.id,
   kind:request.position.type==='concepto'?'concepto de entrada':owned?'ficha del documento':'lectura enlazada desde el documento',
   reading:owned?'Esta pieza abre la lectura desde su documento de origen.':'El documento de entrada enlaza esta lectura del Atlas.',route:true});}}
 for(const e of activeEdges)if(visibleIds.has(e[1])&&visibleIds.has(e[2])&&!edges.some(x=>x.id===e[0]))edges.push({id:e[0],from:e[1],to:e[2],kind:e[3],reading:e[4],evidence:e[5],route:false});
 const blocks=[request.position.header];
 for(const id of selected){const v=visits.get(id);if(v.edge)blocks.push(edgeText(v.edge,all));blocks.push(nodeText(all.get(id),graph.topics));}
 const maxDistance=Math.max(0,...chosen.map(n=>n.distance));
 return {schema:VERSION,edition:graph.edition,request:{...request,position:undefined},position:request.position,
  budget:{limit:request.tokens,used,remaining:request.tokens-used,nextBlock:nextCost,encoding:graph.tokenization.encoding,accounting:graph.tokenization.accounting},
  reachable:queue.length,selected:chosen.length,shown:visible.length+1,omittedByBudget:queue.length-chosen.length,omittedInDiagram:chosen.length-visible.length,
  layers:Array.from({length:maxDistance+1},(_,distance)=>({distance,selected:chosen.filter(n=>n.distance===distance).length,shown:visible.filter(n=>n.distance===distance).length+(distance===0?1:0)})),
  center:root.id,nodes:[root,...visible],edges,selection:chosen,reading:blocks.join('')};
}
export function positionParams(request){
 const p=new URLSearchParams({posicionamiento:request.posicionamiento,tokens:String(request.tokens),max:String(request.max),red:request.red,sentido:request.sentido,modo:request.modo});
 if(request.site)p.set('site',request.site);if(request.puente)p.set('puente',request.puente);if(request.solo)p.set('solo','1');
 p.set('rol',request.rol);p.set('lectura',request.lectura);p.set('enfoque',request.enfoque);if(request.instruccion)p.set('instruccion',request.instruccion);
 for(const w of request.pesos)p.append('peso',w.tag+':'+w.value);return p;
}
