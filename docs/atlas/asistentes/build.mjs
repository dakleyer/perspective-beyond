import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {readPosition,positionMap} from '../positioning.mjs';
import {assistantSource,sourceHTML,SOURCE_VERSION} from './source.mjs';
const root=dirname(fileURLToPath(import.meta.url));
const revision=process.argv[2];
if(!revision||!/^[a-f0-9]{40}$/.test(revision))throw Error('Specify the public source revision.');
const graphBytes=await readFile(resolve(root,'../mapa/grafo.json'));
const graph=JSON.parse(graphBytes),css=await readFile(resolve(root,'asistentes.css'),'utf8');
const examples=[
 {slug:'arquitectura-y-lenguajes',title:'Thinking between languages and trades',description:'Architecture as the capability to recognise structures and build translations that serve operations.',point:'D-285',weights:[['empresa',50],['matematicas',50]],role:'embajador',purpose:'paraphrase',format:'conversacion',instruction:'Explain Iván Abril\'s documented thought using his architectural vocabulary and an example of translation between two trades.'},
 {slug:'conocimiento-tacito',title:'Preserving the capability that makes things work',description:'Tacit knowledge, field judgement and capability transmission in Tiger Teams.',point:'N1287',weights:[['capacidad-humana',70],['empresa',30]],role:'consultor',purpose:'ideas',format:'web',instruction:'Explain how to preserve people\'s judgement when redesigning an organisation; show the mechanism and its practical application.'},
 {slug:'integridad-estructural',title:'Observing the structure supporting a decision',description:'Structural awareness and relationships between integrity, representation and adaptive systems.',point:'T1499',weights:[['representacion',50],['evidencia',50]],role:'investigador',purpose:'explore',format:'audio',instruction:'Prepare a spoken explanation of the ideas and relationships documented in this selection.'},
 {slug:'valor-y-ejecucion',title:'From business intention to operational capability',description:'Value creation, coordination between actors and execution in the American environment.',point:'U2',weights:[['empresa',60],['transformacion',40]],role:'consultor',purpose:'ideas',format:'video',instruction:'Explain how a business intention becomes coordinated execution and lasting capability.'}
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
const cards=records.map(e=>'<section class="card"><p class="kicker">'+e.selected.length+' pieces · '+e.relations.length+' relaciones</p><h2>'+e.title+'</h2><p>'+e.description+'</p><p><small>UTF-8 text · '+(e.bytes/1024).toFixed(1)+' KB</small></p><div class="actions"><a class="button" href="'+e.text+'">URL for your assistant</a><a href="'+e.html+'">Read the source</a></div></section>').join('\n');
const html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Assistant sources · Perspective Beyond</title><meta name="description" content="A compact Atlas file brings together thought, texts, relationships and instructions for conversing or creating a website, audio or video with your assistant."><link rel="canonical" href="https://dakleyer.github.io/perspective-beyond/atlas/asistentes/"><link rel="stylesheet" href="asistentes.css?v=fuentes-1"></head><body><main><header><p class="kicker">Perspective Beyond · Thought Atlas</p><h1>One source of thought.<br>Many ways to create.</h1><p class="lead">A website to explore as a person. A self-contained source to work with your assistant. Both come from the same Atlas.</p><p>Choose a reading and give its URL to your assistant. The file already brings together the texts, their relationships, sources and working instructions. From there you can converse, prepare a web page, create audio, develop a video or shape a document.</p><nav class="actions"><a class="button" href="#fuentes">Choose a source</a><a class="button secondary" href="../posicionamiento/">Prepare my own source</a><a href="README.md">How it works</a><a href="../">Explore the Atlas</a></nav></header><ol class="steps"><li><strong>Choose the thought.</strong><br>An entry document, its cards and the nearby ideas that help understand it.</li><li><strong>Give a single URL.</strong><br>The selection and configuration are written inside the file.</li><li><strong>Ask for what you want to create.</strong><br>The assistant transforms that base into conversation, web, audio, video or a document.</li></ol><section id="fuentes"><p class="kicker">Four entries to get started</p><h2>Ready-to-use sources</h2><p>Each opens a specific perspective on the corpus. You can change the output format in your conversation with the assistant.</p><div class="grid">'+cards+'</div></section><section class="card"><p class="kicker">Your positioning</p><h2>A reading tailored to you</h2><p>Select a document or card, combine tags and choose how much thought to take with you. In the mini-map you will find “Download source for my assistant”: a file with the content and its configuration.</p><p><a href="../posicionamiento/">Open the positioning selector →</a></p></section><footer><p>Output texts are created by the assistant the reader uses, with its text, voice, web or video tools. The Atlas supplies the thought, relationships and provenance.</p><p><a href="README.md">Product and protocol</a> · <a href="ejemplos/index.json">Sources in this edition</a> · <a href="https://github.com/dakleyer/perspective-beyond">GitHub</a></p></footer></main></body></html>\n';
await writeFile(resolve(root,'index.html'),html);
console.log(JSON.stringify({examples:records.map(r=>({slug:r.slug,selected:r.selected.length,relations:r.relations.length,bytes:r.bytes}))},null,2));

