// From this directory: node test.mjs
import fs from 'node:fs';import assert from 'node:assert/strict';
import {positionMap,readPosition} from '../../../positioning.mjs';
const graph=JSON.parse(fs.readFileSync(new URL('../../../mapa/grafo.json',import.meta.url)));
let previous=[];
for(const tokens of [1000,1500,2000,3000,4000,8000]){
 const r=positionMap(graph,readPosition(new URLSearchParams({posicionamiento:'imsv',site:'imsv',modo:'closed',tokens:String(tokens)}),graph));
 assert(r.budget.used<=tokens);assert(previous.every((id,i)=>r.selection[i]?.id===id));assert(r.selection.every(n=>n.clusters.every(x=>x==='imsv')));previous=r.selection.map(n=>n.id);
 if(tokens>=2000)for(const group of r.position.coverageGroups)assert(group.candidates.some(id=>previous.includes(id)),group.id);
 if(tokens===2000){assert(!previous.some(x=>x.startsWith('np-')));for(const text of ['20 de noviembre de 2024','Asamblea General','Consejo','Tegrity.AI','Instituto del Totonacapan','LatinoEmpresa','OÜ JUBAP','3 de agosto de 2026','francés','1898'])assert(r.reading.includes(text),text);}
}
for(const id of ['T1709','S11','L001'])assert(graph.nodes.find(n=>n.id===id).reading.length>400,id);
console.log('PASS: institutional coverage, question facts, budgets, closed scope and monotonic prefixes.');
