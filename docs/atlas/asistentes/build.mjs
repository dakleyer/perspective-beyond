import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {readPosition,positionMap} from '../positioning.mjs';
import {assistantSource,sourceHTML,SOURCE_VERSION} from './source.mjs';
const root=dirname(fileURLToPath(import.meta.url));
const revision=process.argv[2];
if(!revision||!/^[a-f0-9]{40}$/.test(revision))throw Error('Indica la revisión pública de origen.');
const graphBytes=await readFile(resolve(root,'../mapa/grafo.json'));
const graph=JSON.parse(graphBytes),css=await readFile(resolve(root,'asistentes.css'),'utf8');
const examples=[
 {slug:'arquitectura-y-lenguajes',title:'Pensar entre lenguajes y oficios',description:'La arquitectura como capacidad para reconocer estructuras y construir traducciones que sirven para operar.',point:'D-285',weights:[['empresa',50],['matematicas',50]],role:'embajador',purpose:'paraphrase',format:'conversacion',instruction:'Explica el pensamiento documentado de Iván Abril con su vocabulario arquitectónico y un ejemplo de traducción entre dos oficios.'},
 {slug:'conocimiento-tacito',title:'Conservar la capacidad que hace funcionar las cosas',description:'Conocimiento tácito, juicio de campo y transmisión de capacidades en los Tiger Teams.',point:'N1287',weights:[['capacidad-humana',70],['empresa',30]],role:'consultor',purpose:'ideas',format:'web',instruction:'Explica cómo conservar el juicio de las personas al rediseñar una organización; muestra el mecanismo y su aplicación práctica.'},
 {slug:'integridad-estructural',title:'Observar la estructura que sostiene una decisión',description:'Conciencia estructural y relaciones entre integridad, representación y sistemas adaptativos.',point:'T1499',weights:[['representacion',50],['evidencia',50]],role:'investigador',purpose:'explore',format:'audio',instruction:'Prepara una explicación hablada de las ideas y de las relaciones documentadas en esta selección.'},
 {slug:'valor-y-ejecucion',title:'De una intención empresarial a una capacidad operativa',description:'Creación de valor, coordinación entre actores y ejecución en el entorno americano.',point:'U2',weights:[['empresa',60],['transformacion',40]],role:'consultor',purpose:'ideas',format:'video',instruction:'Explica cómo se convierte una intención de negocio en ejecución coordinada y capacidad que permanece.'}
];
await mkdir(resolve(root,'ejemplos'),{recursive:true});
const records=[];
for(const example of examples){
 const params=new URLSearchParams({posicionamiento:example.point,tokens:'2000',modo:'federated',rol:example.role,lectura:example.purpose,instruccion:example.instruction});
 for(const[k,v]of example.weights)params.append('peso',k+':'+v);
 const result=positionMap(graph,readPosition(params,graph));
 const source=assistantSource(result,graph,{title:example.title,format:example.format,revision});
 const textName='ejemplos/'+example.slug+'.txt',htmlName='ejemplos/'+example.slug+'.html';
 await writeFile(resolve(root,textName),source.text);
 await writeFile(resolve(root,htmlName),sourceHTML(source,{slug:example.slug,css}));
 records.push({...example,configuration:source.configuration,text:textName,html:htmlName,selected:source.selection,relations:source.relations,
  bytes:Buffer.byteLength(source.text),sha256:createHash('sha256').update(source.text).digest('hex'),readingBudget:source.readingBudget});
}
await writeFile(resolve(root,'ejemplos/index.json'),JSON.stringify({schema:SOURCE_VERSION,revision,edition:graph.edition,
 graphSha256:createHash('sha256').update(graphBytes).digest('hex'),examples:records},null,2)+'\n');
const cards=records.map(e=>'<section class="card"><p class="kicker">'+e.selected.length+' piezas · '+e.relations.length+' relaciones</p><h2>'+e.title+'</h2><p>'+e.description+'</p><p><small>Texto UTF-8 · '+(e.bytes/1024).toFixed(1)+' KB</small></p><div class="actions"><a class="button" href="'+e.text+'">URL para tu asistente</a><a href="'+e.html+'">Leer la fuente</a></div></section>').join('\n');
const html='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fuentes para asistentes · Perspective Beyond</title><meta name="description" content="Un archivo compacto del Atlas reúne pensamiento, textos, relaciones e instrucciones para conversar o crear una web, un audio o un vídeo con tu asistente."><link rel="canonical" href="https://dakleyer.github.io/perspective-beyond/atlas/asistentes/"><link rel="stylesheet" href="asistentes.css?v=fuentes-1"></head><body><main><header><p class="kicker">Perspective Beyond · Atlas de pensamiento</p><h1>Una fuente de pensamiento.<br>Muchas formas de crear.</h1><p class="lead">Una web para explorar como persona. Una fuente autocontenida para trabajar con tu asistente. Las dos nacen del mismo Atlas.</p><p>Elige una lectura y entrega su URL a tu asistente. El archivo ya reúne los textos, sus relaciones, las fuentes y las indicaciones de trabajo. A partir de ahí puedes conversar, preparar una página web, crear un audio, desarrollar un vídeo o dar forma a un documento.</p><nav class="actions"><a class="button" href="#fuentes">Elegir una fuente</a><a class="button secondary" href="../posicionamiento/">Preparar mi propia fuente</a><a href="README.md">Cómo funciona</a><a href="../">Explorar el Atlas</a></nav></header><ol class="steps"><li><strong>Elige el pensamiento.</strong><br>Un documento de entrada, sus fichas y las ideas cercanas que ayudan a comprenderlo.</li><li><strong>Entrega una sola URL.</strong><br>La selección y la configuración están escritas dentro del archivo.</li><li><strong>Pide lo que quieres crear.</strong><br>El asistente transforma esa base en conversación, web, audio, vídeo o documento.</li></ol><section id="fuentes"><p class="kicker">Cuatro entradas para empezar</p><h2>Fuentes listas para usar</h2><p>Cada una abre una perspectiva concreta del corpus. Puedes cambiar el formato de salida en tu conversación con el asistente.</p><div class="grid">'+cards+'</div></section><section class="card"><p class="kicker">Tu posicionamiento</p><h2>Una lectura hecha a tu medida</h2><p>Selecciona un documento o una ficha, combina etiquetas y elige cuánto pensamiento quieres llevar. En el mini mapa encontrarás «Descargar fuente para mi asistente»: un archivo con el contenido y su configuración.</p><p><a href="../posicionamiento/">Abrir el selector de posicionamiento →</a></p></section><footer><p>Los textos de salida los crea el asistente que utilice el lector, con sus herramientas de texto, voz, web o vídeo. El Atlas aporta el pensamiento, las relaciones y la procedencia.</p><p><a href="README.md">Producto y protocolo</a> · <a href="ejemplos/index.json">Fuentes de esta edición</a> · <a href="https://github.com/dakleyer/perspective-beyond">GitHub</a></p></footer></main></body></html>\n';
await writeFile(resolve(root,'index.html'),html);
console.log(JSON.stringify({examples:records.map(r=>({slug:r.slug,selected:r.selected.length,relations:r.relations.length,bytes:r.bytes}))},null,2));

