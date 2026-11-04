import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {readPosition,positionMap} from '../positioning.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),profiles=JSON.parse(fs.readFileSync(path.join(here,'profiles.json'))),graph=JSON.parse(fs.readFileSync(path.join(here,'../mapa/grafo.json')));
for(const d of profiles.documents){const at=graph.documents.findIndex(x=>x.id===d.id);if(at<0)graph.documents.push(d);else graph.documents[at]=d;}
let checks=0;const out=process.argv.includes('--out')?path.resolve(process.argv[process.argv.indexOf('--out')+1]):null;if(out)fs.mkdirSync(out,{recursive:true});
for(const profile of profiles.pages){const actual=positionMap(graph,readPosition(new URLSearchParams(profile.params),graph)),saved=JSON.parse(fs.readFileSync(path.join(here,'selections',profile.selection))).result;
 for(const key of ['nodes','edges','budget','selection','reading']){if(JSON.stringify(actual[key])!==JSON.stringify(saved[key]))throw Error(profile.key+': '+key+' differs');checks++;}
 if(out)fs.writeFileSync(path.join(out,profile.selection),JSON.stringify({schema:'mind-atlas/page-window-v1',graphSHA256:profiles.graphSHA256,profile,result:actual})+'\n');
}
console.log(JSON.stringify({pages:profiles.pages.length,checks,identical:true}));
