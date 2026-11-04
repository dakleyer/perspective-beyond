import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {readPosition,positionMap} from '../positioning.mjs';
import {assistantSource,sourceHTML,FORMATS} from './source.mjs';
const graph=JSON.parse(await readFile(new URL('../mapa/grafo.json',import.meta.url)));
const before=JSON.stringify(graph),index=JSON.parse(await readFile(new URL('ejemplos/index.json',import.meta.url)));
let checks=0;
function check(fn){fn();checks++;}
for(const example of index.examples){
 const result=positionMap(graph,readPosition(new URLSearchParams(example.configuration),graph));
 const text=await readFile(new URL(example.text,import.meta.url),'utf8');
 const prepared=assistantSource(result,graph,{title:example.title,format:example.format,revision:index.revision});
 check(()=>assert.equal(prepared.text,text));
 for(const format of Object.keys(FORMATS)){
  const source=assistantSource(result,graph,{format});
  check(()=>assert.deepEqual(source.selection,result.selection.map(n=>n.id)));
  check(()=>assert.equal(source.text.includes(FORMATS[format][1]),true));
  check(()=>assert.equal(result.selection.every(n=>source.text.includes(n.reading??n.summary)),true));
  check(()=>assert.equal(source.text.includes(result.request.instruccion),true));
  const allowed=new Set([...result.selection.map(n=>n.routeEdge),...result.edges.map(e=>e.id)]);
  check(()=>assert.equal(source.relations.every(id=>allowed.has(id)),true));
 }
 const html=sourceHTML(prepared);
 check(()=>assert.equal(/<script|<link[^>]+stylesheet|<iframe|<img/i.test(html),false));
 check(()=>assert.equal(prepared.selection.every(id=>html.includes(id)),true));
}
const closed=positionMap(graph,readPosition(new URLSearchParams('posicionamiento=N1287&tokens=2000&modo=closed&site=net'),graph));
const closedSource=assistantSource(closed,graph);
check(()=>assert.equal(closed.selection.every(n=>n.clusters.every(c=>c==='net')),true));
check(()=>assert.equal(closedSource.selection.length,closed.selection.length));
const hostile=sourceHTML({title:'<script>unsafe</script>',text:'# <script>unsafe</script>\n[jump](javascript:alert(1))'});
check(()=>assert.equal(hostile.includes('<script>unsafe'),false));
check(()=>assert.equal(hostile.includes('href="javascript:'),false));
check(()=>assert.throws(()=>assistantSource({...closed,selection:[]},graph),/Expand/));
check(()=>assert.throws(()=>assistantSource(closed,graph,{format:'unknown'}),/Choose/));
check(()=>assert.throws(()=>assistantSource({...closed,edition:'other'},graph),/edition/));
check(()=>assert.equal(JSON.stringify(graph),before));
console.log(JSON.stringify({checks,passed:checks,examples:index.examples.length,formats:Object.keys(FORMATS).length,substrateUnchanged:true},null,2));

