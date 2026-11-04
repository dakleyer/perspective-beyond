// Browser and CLI use the same versioned traversal.
import {parseFocusWeights} from '../session-config.mjs';
export const VERSION = 'perspective-beyond/radius-v1';
export const DEFAULTS = Object.freeze({centro:'T1499', radio:2, max:16, red:'documentos', sentido:'ambas'});
const compare = (a,b) => a<b ? -1 : a>b ? 1 : 0;

function options(params, name, values) {
  const value=params.get(name)??DEFAULTS[name];
  if(!values.includes(value))throw Error(`Valor de ${name} no válido: ${value}.`);
  return value;
}

function integer(params, name, min, max) {
  const raw=params.get(name)??String(DEFAULTS[name]);
  const value=Number(raw);
  if(!/^\d+$/.test(raw)||!Number.isInteger(value)||value<min||value>max)
    throw Error(`${name} debe estar entre ${min} y ${max}.`);
  return value;
}

export function readRequest(params, topics) {
  const centro=(params.get('centro')??DEFAULTS.centro).trim();
  if(!centro)throw Error('Elige una ficha, concepto o URL de origen.');
  const supplied=params.getAll('peso');
  const parsed=parseFocusWeights(supplied.map(token=>/^tema:/i.test(token)?token:'tema:'+token),Object.keys(topics).map(key=>'tema:'+key),Object.keys(topics).length);
  if(parsed.errors.length)throw Error(parsed.errors.join(' '));
  const weights=new Map([...parsed.weights].map(([key,value])=>[key.slice(5),value]));
  const strict=params.get('solo')==='1';
  if(strict&&!weights.size)throw Error('Añade al menos un peso para limitar por etiquetas.');
  const sorted=[...weights].sort(([a],[b])=>compare(a,b));
  const sum=sorted.reduce((total,[,value])=>total+value,0);
  return {
    centro, radio:integer(params,'radio',0,4), max:integer(params,'max',1,60),
    red:options(params,'red',['documentos','ideas']), sentido:options(params,'sentido',['ambas','salientes','entrantes']),
    solo:strict,
    pesos:sorted.map(([tag,value])=>({tag,value,normalized:value/sum})),
  };
}

function normalizedUrl(raw) {
  try {
    const url=new URL(raw);
    if(!['http:','https:'].includes(url.protocol))return '';
    for(const key of [...url.searchParams.keys()]) {
      if(/^utm_/i.test(key)||['gclid','fbclid'].includes(key))url.searchParams.delete(key);
    }
    url.searchParams.sort();
    const path=url.pathname.replace(/\/$/,'')||'/';
    return url.host.toLowerCase().replace(/^www\./,'')+path+url.search+url.hash;
  } catch {
    return '';
  }
}

export function resolveCenter(graph, value) {
  const exact=graph.nodes.find(node=>node.id===value);
  if(exact)return exact;
  const url=normalizedUrl(value);
  const matches=url
    ? graph.nodes.filter(node=>[node.url,node.original,...node.aliases].some(alias=>alias&&normalizedUrl(alias)===url))
    : graph.nodes.filter(node=>node.id.toLowerCase()===value.toLowerCase());
  if(matches.length>1)throw Error('La URL corresponde a varias fichas. Usa un ID: '+matches.slice(0,12).map(n=>n.id).join(', ')+'.');
  if(!matches.length)throw Error('Ese ID o URL no figura en esta edición del Atlas.');
  return matches[0];
}

export function calculate(graph, request) {
  if(graph.schema!=='perspective-beyond/graph-v1')throw Error('Versión de grafo incompatible.');
  const center=resolveCenter(graph,request.centro);
  const nodes=new Map(graph.nodes.map(node=>[node.id,node]));
  const affinity=new Map(graph.nodes.map(node=>[
    node.id,request.pesos.reduce((score,peso)=>score+(node.tags.includes(peso.tag)?peso.normalized:0),0)
  ]));
  const matches=id=>!request.solo||affinity.get(id)>0;
  const typeAllowed=id=>request.red==='ideas'||nodes.get(id).type==='ficha';
  if(!typeAllowed(center.id))throw Error('Para centrar un concepto, elige la red de ideas.');
  const edges=graph.edges.filter(edge=>request.red==='ideas'||edge[6]==='documento');
  const adjacent=new Map();
  function arc(from,to,edge) {
    if(from===to||!typeAllowed(to)||!matches(to))return;
    if(!adjacent.has(from))adjacent.set(from,[]);
    adjacent.get(from).push({to,edge});
  }
  for(const [id,from,to] of edges) {
    if(request.sentido!=='entrantes')arc(from,to,id);
    if(request.sentido!=='salientes')arc(to,from,id);
  }
  const byNeighbor=(a,b)=>affinity.get(b.to)-affinity.get(a.to)||compare(a.to,b.to)||compare(a.edge,b.edge);
  for(const neighbors of adjacent.values())neighbors.sort(byNeighbor);

  const visits=new Map([[center.id,{distance:0,parent:null,edge:null}]]);
  const queue=[center.id];
  for(let pos=0;pos<queue.length;pos++) {
    const current=queue[pos];
    const distance=visits.get(current).distance;
    if(distance===request.radio)continue;
    for(const {to,edge} of adjacent.get(current)??[]) {
      if(visits.has(to))continue;
      visits.set(to,{distance:distance+1,parent:current,edge});
      queue.push(to);
    }
  }
  const priority=(id)=> {
    const weighted=request.pesos.length ? 0.25+0.75*affinity.get(id) : 1;
    return weighted/(1+visits.get(id).distance);
  };
  const byPriority=(a,b)=>priority(b)-priority(a)||visits.get(a).distance-visits.get(b).distance||compare(a,b);
  const shown=new Set([center.id]);
  for(const id of queue.slice(1).sort(byPriority)) {
    const path=[];
    for(let current=id;!shown.has(current);current=visits.get(current).parent)path.push(current);
    if(shown.size+path.length<=request.max)for(const node of path.reverse())shown.add(node);
    if(shown.size===request.max)break;
  }
  const routes=new Set([...shown].map(id=>visits.get(id).edge).filter(Boolean));
  const resultNodes=[...shown].sort((a,b)=>visits.get(a).distance-visits.get(b).distance||byPriority(a,b)).map(id=>{
    const visit=visits.get(id);
    return {...nodes.get(id),distance:visit.distance,parent:visit.parent,routeEdge:visit.edge,
      affinity:affinity.get(id),priority:priority(id)};
  });
  const resultEdges=edges.filter(([,from,to])=>shown.has(from)&&shown.has(to)).map(
    ([id,from,to,kind,reading,evidence,layer,condition])=>({id,from,to,kind,reading,evidence,layer,condition,route:routes.has(id)})
  );
  const layers=Array.from({length:request.radio+1},(_,distance)=>({distance,reachable:0,shown:0}));
  for(const visit of visits.values())layers[visit.distance].reachable++;
  for(const node of resultNodes)layers[node.distance].shown++;
  for(const layer of layers)layer.omitted=layer.reachable-layer.shown;
  return {
    schema:VERSION, dataset:{edition:graph.edition,canonicalSha256:graph.canonicalSha256,catalogSha256:graph.catalogSha256},
    request:{...request,centro:center.id}, center:center.id, reachable:visits.size, shown:shown.size,
    omitted:visits.size-shown.size, layers, nodes:resultNodes, edges:resultEdges,
  };
}

export function shareParams(request) {
  const params=new URLSearchParams();
  for(const key of ['centro','radio','max','red','sentido'])params.set(key,request[key]);
  for(const peso of request.pesos)params.append('peso',peso.tag+':'+peso.value);
  if(request.solo)params.set('solo','1');
  return params;
}
