import fs from 'node:fs';import path from 'node:path';import {fileURLToPath,pathToFileURL} from 'node:url';
const here=process.argv.includes('--base')?path.resolve(process.argv[process.argv.indexOf('--base')+1]):path.dirname(fileURLToPath(import.meta.url));
const {readPosition,positionMap}=await import(pathToFileURL(path.join(here,'../positioning.mjs')));
const profiles=JSON.parse(fs.readFileSync(path.join(here,'profiles.json'))),graph=JSON.parse(fs.readFileSync(path.join(here,'../mapa/grafo.json')));
for(const d of profiles.documents){const at=graph.documents.findIndex(x=>x.id===d.id);if(at<0)graph.documents.push(d);else graph.documents[at]=d;}
let checks=0;const out=process.argv.includes('--out')?path.resolve(process.argv[process.argv.indexOf('--out')+1]):null;if(out)fs.mkdirSync(out,{recursive:true});
for(const profile of profiles.pages){const actual=positionMap(graph,readPosition(new URLSearchParams(profile.params),graph)),saved=JSON.parse(fs.readFileSync(path.join(here,'selections',profile.selection))).result;
 const compare=value=>JSON.stringify(value,(key,v)=>key==='affinity'?Number(v.toFixed(12)):v);
 for(const key of ['nodes','edges','budget','selection','reading']){if(compare(actual[key])!==compare(saved[key]))throw Error(profile.key+': '+key+' differs');checks++;}
 if(out)fs.writeFileSync(path.join(out,profile.selection),JSON.stringify({schema:'mind-atlas/page-window-v1',graphSHA256:profiles.graphSHA256,profile,result:actual})+'\n');
}
console.log(JSON.stringify({pages:profiles.pages.length,checks,identical:true}));

