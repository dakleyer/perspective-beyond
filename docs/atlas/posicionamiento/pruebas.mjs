import assert from 'node:assert/strict';
import fs from 'node:fs';
import {readPosition,positionMap,positionParams,nodeText,edgeText,resolvePosition} from '../positioning.mjs';
const g=JSON.parse(fs.readFileSync(new URL('../mapa/grafo.json',import.meta.url),'utf8')),all=new Map(g.nodes.map(n=>[n.id,n])),results=[];
function test(name,fn){fn();results.push({name,pass:true});}
function run(query){return positionMap(g,readPosition(new URLSearchParams(query),g));}
test('Every ficha has one source document',()=>{const refs=g.documents.flatMap(d=>d.fichas);assert.equal(refs.length,1291);assert.equal(new Set(refs).size,1291);});
test('Every composition sums to 100 percent',()=>{for(const n of g.nodes)assert(Math.abs(Object.values(n.tagWeights).reduce((a,b)=>a+b,0)-1)<1e-9,n.id);});
test('The biography contains multiple fichas',()=>assert(g.documents.find(d=>d.url.includes('totonacapan.com/?page_id=413')).fichas.length>80));
test('A specific ficha is a specific entry',()=>assert.deepEqual(resolvePosition(g,'D-285').seeds,['D-285']));
test('A whole document retains its own fichas',()=>assert(resolvePosition(g,'https://totonacapan.com/?page_id=413').fichas.length>80));
test('Default European positioning starts at the landing',()=>{const r=readPosition(new URLSearchParams('posicionamiento=eu'),g);assert.equal(r.position.url,'https://jubap.eu/');assert.deepEqual(r.position.seeds,['E2']);});
test('Landing reads can continue through observed links',()=>{const r=run('posicionamiento=eu&tokens=2000&modo=closed&site=eu');assert(r.selected>1);assert(r.edges.some(e=>e.id.startsWith('navigation:')));});
test('Composed affinity multiplies both percentages',()=>{const r=run('posicionamiento=D-285&tokens=2000&peso=Empresa:50&peso=Matematicas:50');assert(Math.abs(r.selection.find(n=>n.id==='D-285').affinity-.225)<1e-12);});
const points=['D-285','D-271','E2','N2','U2','T1573','np-biografia','C01'];
const budgets=[500,1000,2000,4000,8000,16000];const probes=[];
for(const p of points)test('Budget expansion preserves the prefix: '+p,()=>{
 let previous=[];
 for(const b of budgets){
  const r=run('posicionamiento='+p+'&tokens='+b+'&peso=empresa:50&peso=matematicas:50');
  const ids=r.selection.map(n=>n.id);assert.deepEqual(ids.slice(0,previous.length),previous);assert(r.budget.used<=b);previous=ids;
  probes.push({position:p,budget:b,used:r.budget.used,selected:r.selected,reading:r.reading,positionHeader:r.position.headerTokens});
 }
});
test('Diagram size preserves the full reading selection',()=>{const a=run('posicionamiento=D-285&tokens=8000&max=3'),b=run('posicionamiento=D-285&tokens=8000&max=120');assert.deepEqual(a.selection,b.selection);assert.equal(a.reading,b.reading);assert.equal(a.shown,3);});
test('Every visible piece is connected to the entry',()=>{const r=run('posicionamiento=all&tokens=8000&max=15');const visible=new Set(r.nodes.map(n=>n.id));for(const n of r.nodes)if(n.id!==r.center)assert(visible.has(n.parent));});
test('Closed stays inside its cluster',()=>{const r=run('posicionamiento=D-285&tokens=8000&modo=closed&site=dialogos');assert(r.selection.every(n=>n.clusters.every(c=>c==='dialogos')));});
test('Porous crosses only its selected bridge',()=>{const r=run('posicionamiento=D-271&tokens=12000&modo=porous&site=dialogos&puente=dialogue-bridge-D-271-N1287');assert(r.selection.every(n=>n.clusters.every(c=>['dialogos','net'].includes(c))));for(const e of r.edges){if(!all.has(e.from)||!all.has(e.to))continue;if(!all.get(e.from).clusters.some(c=>all.get(e.to).clusters.includes(c)))assert.equal(e.id,'documento:dialogue-bridge-D-271-N1287');}});
test('Exclusive themes use positive ficha proportions',()=>{const r=run('posicionamiento=D-285&tokens=8000&peso=matematicas:100&solo=1');assert(r.selection.every(n=>n.tagWeights.matematicas>0));});
test('No duplicate ficha is introduced by multiple labels',()=>{const r=run('posicionamiento=D-285&tokens=12000&peso=empresa:60&peso=matematicas:40');assert.equal(new Set(r.selection.map(n=>n.id)).size,r.selected);});
test('URL roundtrip keeps the role and special instruction',()=>{const q=readPosition(new URLSearchParams('posicionamiento=D-285&tokens=4000&rol=consultor&lectura=ideas&instruccion=Tres+frases&peso=Empresa:50&peso=matematicas:50'),g);assert.deepEqual(readPosition(positionParams(q),g),q);});
test('Invalid positioning is reported',()=>assert.throws(()=>run('posicionamiento=missing-document'),/posicionamiento/));
test('A custom budget is validated',()=>{for(const v of ['0','-1','Infinity','2e3','2000001'])assert.throws(()=>run('tokens='+v));});
test('An unknown weight is reported',()=>assert.throws(()=>run('peso=unregistered:70&peso=empresa:30'),/peso/));
test('A source outside the closed scope is reported',()=>assert.throws(()=>run('posicionamiento=E2&modo=closed&site=dialogos'),/fuera/));
test('Both older point aliases resolve',()=>{const a=run('desde=D-285&tokens=2000'),b=run('centro=D-285&tokens=2000');assert.equal(a.reading,b.reading);});
test('Sufficient budget completes the reachable component',()=>{const r=run('posicionamiento=D-285&tokens=2000000&max=60');assert.equal(r.selected,r.reachable);assert.equal(r.omittedByBudget,0);});
test('Independent block costs agree with the selected records',()=>{for(const query of ['posicionamiento=D-285&tokens=4000','posicionamiento=eu&tokens=4000']){const r=run(query);const expected=r.position.headerTokens+r.selection.reduce((s,n)=>s+n.contextTokens+(n.routeEdge?g.edgeTokenCosts[n.routeEdge]:0),0);assert.equal(expected,r.budget.used);}});
test('Public source extracts retain their provenance',()=>{const records=JSON.parse(fs.readFileSync(new URL('lecturas-fuentes.json',import.meta.url))).records;assert(records.length>=150);for(const r of records){const n=all.get(r.id);assert.equal(n.reading,r.text);assert.equal(n.readingSource.url,r.url);assert.match(n.readingSource.sourceSha256,/^[a-f0-9]{64}$/);}});
test('The entry includes the article mechanism before expanding',()=>{const r=run('posicionamiento=N1826&tokens=3000&peso=cambio-regimen:70&peso=economia:30');assert.match(r.reading,/shared-resource authorization/);assert(r.selection.some(n=>n.id==='N1826'));});
test('Changing the composition preference changes the reading',()=>{const a=run('posicionamiento=D-285&tokens=4000&peso=empresa:100'),b=run('posicionamiento=D-285&tokens=4000&peso=matematicas:100');assert.notDeepEqual(a.selection.map(n=>n.id),b.selection.map(n=>n.id));});
test('A source mechanism retains its directly supported conceptual core',()=>{for(const point of ['T874','N1826']){const r=run('posicionamiento='+point+'&tokens=4000&peso=cambio-regimen:70&peso=economia:30');assert(r.localCore.length>0&&r.localCore.length<=4);for(const id of r.localCore)assert(g.edges.some(e=>e[1]===point&&e[2]===id&&e[6]==='apoyo'));}});
test('Documented use remains available before thematic expansion',()=>{const r=run('posicionamiento=T874&tokens=2400&peso=capacidad-humana:70&peso=integridad-ia:30');assert.equal(r.coreDocument,'T1400');assert(r.selection.findIndex(n=>n.id==='T1400')<=5);});
test('Configured web readings reproduce the engine and enforce closed scope',()=>{const index=JSON.parse(fs.readFileSync(new URL('configurados/index.json',import.meta.url)));assert.equal(index.configurations.length,7);for(const c of index.configurations){const packet=JSON.parse(fs.readFileSync(new URL('configurados/'+c.json,import.meta.url)));const r=positionMap(g,readPosition(positionParams({...packet.request,position:undefined}),g));assert.equal(packet.reading,r.reading);assert.equal(packet.budget.used,r.budget.used);if(c.mode==='closed')assert(packet.selection.every(n=>n.clusters.every(k=>k===c.site)));}});
console.log(JSON.stringify({tests:results.length,passed:results.filter(r=>r.pass).length,tokenProbes:probes.length}));
