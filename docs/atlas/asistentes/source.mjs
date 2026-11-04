/** Build one assistant-facing source from an existing Atlas positioning. */
import {positionParams} from '../positioning.mjs';
export const SOURCE_VERSION='perspective-beyond/assistant-source-v1';
export const FORMATS={
 conversacion:['Conversación','Explica el pensamiento, responde a la pregunta y relaciona las ideas de esta selección.'],
 web:['Página web','Crea una página HTML completa, legible y adaptable a móvil. Explica el mecanismo, integra un mapa breve de relaciones y conserva enlaces titulados a los originales.'],
 audio:['Audio','Prepara un texto hablado con apertura, desarrollo y cierre. Integra la atribución con naturalidad. Con una herramienta de voz disponible, genera el audio a partir de ese texto.'],
 video:['Vídeo','Prepara un guion audiovisual con narración, escenas, ayudas visuales y duración por escena. Con herramientas audiovisuales disponibles, produce el vídeo a partir de ese guion.'],
 documento:['Documento','Desarrolla una explicación estructurada o una propuesta para el caso del lector, apoyándote en los textos y relaciones incluidos.']
};
const clean=v=>String(v??'').replace(/\r\n?/g,'\n').trim();
const link=(label,url)=>'['+clean(label).replace(/[\[\]]/g,'')+']('+url+')';
function labelFor(tag,g){
 const at=tag.indexOf(':'),kind=tag.slice(0,at),id=tag.slice(at+1);
 return kind==='tema'?g.topics[id]:kind==='cluster'?g.clusters[id]:kind==='voz'?g.voices[id]?.label:g.nodes.find(n=>n.id===id)?.title;
}
export function assistantSource(result,g,options={}){
 if(!result?.selection?.length)throw Error('Amplía la lectura para incluir al menos una ficha o concepto.');
 if(result.edition!==g.edition)throw Error('La lectura y el mapa deben pertenecer a la misma edición.');
 const format=options.format??'conversacion';
 if(!Object.hasOwn(FORMATS,format))throw Error('Elige conversación, web, audio, vídeo o documento.');
 const role=g.sessionProfiles.roles[result.request.rol],purpose=g.sessionProfiles.purposes[result.request.lectura];
 if(!role||!purpose)throw Error('Elige un rol y un propósito del Atlas.');
 const selected=new Map(result.selection.map(n=>[n.id,n]));
 const universe=new Map([...g.edges,...(g.navigation??[])].map(e=>[e[0],e]));
 const routes=result.selection.flatMap(n=>n.routeEdge?[universe.get(n.routeEdge)]:[]).filter(Boolean);
 const extras=result.edges.map(e=>universe.get(e.id)).filter(e=>e&&selected.has(e[1])&&selected.has(e[2])&&!routes.some(r=>r[0]===e[0]))
  .sort((a,b)=>(a[6]==='documento'?0:1)-(b[6]==='documento'?0:1)||a[0].localeCompare(b[0])).slice(0,8);
 const edges=[...new Map([...routes,...extras].map(e=>[e[0],e])).values()];
 if(edges.some(e=>!selected.has(e[1])||!selected.has(e[2])))throw Error('Una relación no resuelve sus dos fichas.');
 const atlas='https://dakleyer.github.io/perspective-beyond/atlas/',config=positionParams(result.request);
 const scope={closed:'Cerrado',porous:'Poroso',federated:'Federado'}[result.request.modo];
 const title=options.title??result.position.title,aim=clean(options.instruction??result.request.instruccion);
 const lines=[
 '# '+title,'Fuente autocontenida para asistentes · Perspective Beyond','',
 '## Empieza aquí',
 'Esta fuente reúne una selección del Atlas: pensamiento, textos, relaciones, procedencia y configuración. Trabaja con este archivo como contexto inicial; puedes usarlo sin abrir los enlaces. Los enlaces permiten volver a los originales y ampliar la lectura cuando el usuario lo pida.',
 'Formato inicial: '+FORMATS[format][0]+'. '+FORMATS[format][1],
 'Si el usuario pide otro formato, conserva el pensamiento y cambia su forma de presentación. Si todavía no ha planteado un objetivo, pregúntale qué quiere comprender o crear.',
 'Rol: '+role[0]+'. '+role[1],'Propósito: '+purpose[0]+'. '+purpose[1],
 ...(aim?['Indicación del visitante: '+aim]:[]),
 'Explica primero el mecanismo que sostiene las ideas. Usa las relaciones para conectar las piezas, conserva su dirección y respeta la secuencia temporal de las fuentes. En una aplicación nueva, identifica la propuesta como tal.',
 'Para una voz guiada por una persona o institución, conserva su vocabulario y su forma de razonar documentados aquí; atribuye sus ideas por su nombre. Las citas literales proceden de los pasajes incluidos.',
 'Entrega el resultado con lenguaje claro, afirmativo y natural. Los identificadores técnicos ayudan a consultar la fuente; en el resultado utiliza nombres legibles.','',
 '## Configuración de esta fuente',
 '- Punto de entrada: '+link(result.position.title,result.position.url),
 '- Alcance: '+scope+(result.request.site&&result.request.site!=='all'?' · '+g.clusters[result.request.site]:''),
 '- Combinación: '+(result.request.pesos.length?result.request.pesos.map(w=>labelFor(w.tag,g)+' '+(100*w.normalized).toFixed(2)+' %').join(' · '):'Enfoque parejo entre las piezas del recorrido'),
 '- Selección: '+result.selection.length+' fichas y conceptos · '+edges.length+' relaciones incluidas',
 '- Lectura de origen: presupuesto '+result.budget.limit+' tokens · '+result.budget.used+' utilizados · '+result.budget.encoding,
 '- Edición del mapa: '+g.edition,'- Versión del formato: '+SOURCE_VERSION,
 ...(options.revision?['- Revisión de origen: https://github.com/dakleyer/perspective-beyond/commit/'+options.revision]:[]),'',
 '## Pensamiento y textos',
 ...result.selection.flatMap(n=>['','### '+n.title,
  'Referencia: '+n.id+' · '+(n.type==='concepto'?'Concepto':'Ficha')+' · '+n.clusters.map(c=>g.clusters[c]).join(' / '),'',
  clean(n.reading??n.summary),'',
  'Composición: '+Object.entries(n.tagWeights??{}).map(([k,v])=>g.topics[k]+' '+(v*100).toFixed(2)+' %').join(' · '),
  'Ficha: '+n.url,...(n.original&&n.original!==n.url?['Original: '+n.original]:[]),
  ...(n.readingSource?['Pasaje: '+n.readingSource.section+' · '+n.readingSource.url+' · lectura registrada '+n.readingSource.observed]:[])]),
 '','## Relaciones para pensar con esta selección',
 ...edges.flatMap(e=>['','### '+selected.get(e[1]).title+' → '+selected.get(e[2]).title,
  'Referencia: '+e[0]+' · Tipo: '+e[3],clean(e[4]),...(e[5]?['Fuente de la relación: '+e[5]]:[])]),
 '','## Crear otra lectura',
 'El formato de salida se puede cambiar sobre este mismo contenido. Para ampliar las fichas o cambiar sus pesos, crea otro posicionamiento y exporta una nueva fuente.',
 'Configuración web: '+atlas+'posicionamiento/?'+config.toString(),'Atlas central: '+atlas,
 'Producto y protocolo: '+atlas+'asistentes/README.md',''];
 return {schema:SOURCE_VERSION,title,format,text:lines.join('\n'),selection:[...selected.keys()],relations:edges.map(e=>e[0]),
  edition:g.edition,role:result.request.rol,purpose:result.request.lectura,configuration:config.toString(),readingBudget:{...result.budget},selfContained:true};
}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function inline(text){
 const pattern=/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)|(https?:\/\/[^\s<>]+)/g;
 let out='',last=0;
 for(const m of text.matchAll(pattern)){
  out+=esc(text.slice(last,m.index));out+='<a href="'+esc(m[2]??m[3])+'">'+esc(m[1]??m[3])+'</a>';last=m.index+m[0].length;
 }
 return out+esc(text.slice(last));
}
export function sourceHTML(source,{slug='fuente',css='body{font:1rem/1.7 system-ui;max-width:75ch;margin:2rem auto;padding:1rem}a,p{overflow-wrap:anywhere}'}={}){
 let list=false;const body=[];
 for(const line of source.text.split('\n')){
  if(!line.startsWith('- ')&&list){body.push('</ul>');list=false;}if(!line)continue;
  if(/^#{1,3} /.test(line)){const level=line.indexOf(' ');body.push('<h'+level+'>'+inline(line.slice(level+1))+'</h'+level+'>');}
  else if(line.startsWith('- ')){if(!list){body.push('<ul>');list=true;}body.push('<li>'+inline(line.slice(2))+'</li>');}
  else body.push('<p>'+inline(line)+'</p>');
 }
 if(list)body.push('</ul>');
 return '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(source.title)+' · Fuente para asistentes</title><meta name="description" content="Fuente autocontenida de pensamiento, relaciones e instrucciones para crear con tu asistente."><style>'+css+'</style></head><body><main><header><p class="kicker">Perspective Beyond · Fuente para asistentes</p><p class="lead">Un archivo de pensamiento. Distintas formas de crearlo.</p><nav class="actions"><a class="button" href="'+esc(slug)+'.txt">Dar esta fuente a mi asistente</a><a class="button secondary" href="'+esc(slug)+'.txt" download>Descargar texto</a><a href="../">Ver el producto</a></nav></header><article>'+body.join('\n')+'</article><footer>La misma selección del Atlas, disponible como página legible y como texto UTF-8. <a href="../../">Explorar el Atlas</a></footer></main></body></html>\n';
}

