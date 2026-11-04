/** Build one assistant-facing source from an existing Atlas positioning. */
import {positionParams} from '../positioning.mjs';
export const SOURCE_VERSION='perspective-beyond/assistant-source-v1';
export const FORMATS={
 conversacion:['Conversation','Explain the thought, answer the question and relate the ideas in this selection.'],
 web:['Web page','Create a complete, readable and mobile-responsive HTML page. Explain the mechanism, integrate a brief relationship map and retain titled links to the originals.'],
 audio:['Audio','Prepare a spoken text with an opening, development and closing. Integrate attribution naturally. With an available voice tool, generate audio from that text.'],
 video:['Video','Prepare an audiovisual script with narration, scenes, visual aids and duration per scene. With available audiovisual tools, produce the video from that script.'],
 documento:['Document','Develop a structured explanation or a proposal for the reader\'s case, drawing on the included texts and relationships.']
};
const clean=v=>String(v??'').replace(/\r\n?/g,'\n').trim();
const link=(label,url)=>'['+clean(label).replace(/[\[\]]/g,'')+']('+url+')';
function labelFor(tag,g){
 const at=tag.indexOf(':'),kind=tag.slice(0,at),id=tag.slice(at+1);
 return kind==='tema'?g.topics[id]:kind==='cluster'?g.clusters[id]:kind==='voz'?g.voices[id]?.label:g.nodes.find(n=>n.id===id)?.title;
}
export function assistantSource(result,g,options={}){
 if(!result?.selection?.length)throw Error('Expand the reading to include at least one card or concept.');
 if(result.edition!==g.edition)throw Error('The reading and map must belong to the same edition.');
 const format=options.format??'conversacion';
 if(!Object.hasOwn(FORMATS,format))throw Error('Choose conversation, web, audio, video or document.');
 const role=g.sessionProfiles.roles[result.request.rol],purpose=g.sessionProfiles.purposes[result.request.lectura];
 if(!role||!purpose)throw Error('Choose an Atlas role and purpose.');
 const selected=new Map(result.selection.map(n=>[n.id,n]));
 const universe=new Map([...g.edges,...(g.navigation??[])].map(e=>[e[0],e]));
 const routes=result.selection.flatMap(n=>n.routeEdge?[universe.get(n.routeEdge)]:[]).filter(Boolean);
 const extras=result.edges.map(e=>universe.get(e.id)).filter(e=>e&&selected.has(e[1])&&selected.has(e[2])&&!routes.some(r=>r[0]===e[0]))
  .sort((a,b)=>(a[6]==='documento'?0:1)-(b[6]==='documento'?0:1)||a[0].localeCompare(b[0])).slice(0,8);
 const edges=[...new Map([...routes,...extras].map(e=>[e[0],e])).values()];
 if(edges.some(e=>!selected.has(e[1])||!selected.has(e[2])))throw Error('A relationship does not resolve both its cards.');
 const atlas='https://dakleyer.github.io/perspective-beyond/atlas/',config=positionParams(result.request);
 const scope={closed:'Closed',porous:'Porous',federated:'Federated'}[result.request.modo];
 const title=options.title??result.position.title,aim=clean(options.instruction??result.request.instruccion);
 const lines=[
 '# '+title,'Self-contained assistant source · Perspective Beyond','',
 '## Start here',
 "At this stage, the Atlas complements navigation and understanding of the websites. Each page is an entry point to its cards, concepts, cases and sources; it retains the source URL and allows readers to go deeper, relate ideas and return to the original text. The test compares these directed reading paths with conventional web navigation through tokens consumed, source relevance and corpus understanding.",
 'This source brings together an Atlas selection: thought, texts, relationships, provenance and configuration. Work with this file as the initial context; you can use it without opening the links. Links allow you to return to the originals and expand the reading when the user requests it.',
 'Initial format: '+FORMATS[format][0]+'. '+FORMATS[format][1],
 'If the user requests another format, retain the thought and change its presentation. If they have not yet stated a goal, ask what they want to understand or create.',
 'Role: '+role[0]+'. '+role[1],'Purpose: '+purpose[0]+'. '+purpose[1],
 ...(aim?['Visitor\'s instruction: '+aim]:[]),
 'First explain the mechanism supporting the ideas. Use relationships to connect the pieces, retain their direction and respect the sources\' temporal sequence. In a new application, identify the proposal as such.',
 'For a voice guided by a person or institution, retain their vocabulary and way of reasoning documented here; attribute their ideas by name. Literal quotations come from the included passages.',
 'Deliver the result in clear, affirmative and natural language. Technical identifiers help consult the source; use readable names in the result.','',
 '## Configuration of this source',
 '- Entry point: '+link(result.position.title,result.position.url),
 '- Scope: '+scope+(result.request.site&&result.request.site!=='all'?' · '+g.clusters[result.request.site]:''),
 '- Combination: '+(result.request.pesos.length?result.request.pesos.map(w=>labelFor(w.tag,g)+' '+(100*w.normalized).toFixed(2)+' %').join(' · '):'Balanced focus among the pieces in the reading path'),
 '- Selection: '+result.selection.length+' cards and concepts · '+edges.length+' included relationships',
 '- Source reading: budget '+result.budget.limit+' tokens · '+result.budget.used+' used · '+result.budget.encoding,
 '- Map edition: '+g.edition,'- Format version: '+SOURCE_VERSION,
 ...(options.revision?['- Source revision: https://github.com/dakleyer/perspective-beyond/commit/'+options.revision]:[]),'',
 '## Thought and texts',
 ...result.selection.flatMap(n=>['','### '+n.title,
  'Reference: '+n.id+' · '+(n.type==='concepto'?'Concept':'Card')+' · '+n.clusters.map(c=>g.clusters[c]).join(' / '),'',
  clean(n.reading??n.summary),'',
  'Composition: '+Object.entries(n.tagWeights??{}).map(([k,v])=>g.topics[k]+' '+(v*100).toFixed(2)+' %').join(' · '),
  'Card: '+n.url,...(n.original&&n.original!==n.url?['Original: '+n.original]:[]),
  ...(n.readingSource?['Passage: '+n.readingSource.section+' · '+n.readingSource.url+' · reading recorded '+n.readingSource.observed]:[])]),
 '','## Relationships for thinking with this selection',
 ...edges.flatMap(e=>['','### '+selected.get(e[1]).title+' → '+selected.get(e[2]).title,
  'Reference: '+e[0]+' · Type: '+e[3],clean(e[4]),...(e[5]?['Relationship source: '+e[5]]:[])]),
 '','## Create another reading',
 'The output format can be changed using this same content. To expand the cards or change their weights, create another positioning and export a new source.',
 'Web configuration: '+atlas+'posicionamiento/?'+config.toString(),'Central Atlas: '+atlas,
 'Product and protocol: '+atlas+'asistentes/README.md',''];
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
 return '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(source.title)+' · Assistant source</title><meta name="description" content="Fuente autocontenida de pensamiento, relaciones e instrucciones para crear con tu asistente."><style>'+css+'</style></head><body><main><header><p class="kicker">Perspective Beyond · Assistant source</p><p class="lead">One thought file. Different ways to create it.</p><nav class="actions"><a class="button" href="'+esc(slug)+'.txt">Give this source to my assistant</a><a class="button secondary" href="'+esc(slug)+'.txt" download>Download text</a><a href="../">View the product</a></nav></header><article>'+body.join('\n')+'</article><footer>The same Atlas selection, available as a readable page and UTF-8 text. <a href="../../">Explorar el Atlas</a></footer></main></body></html>\n';
}

