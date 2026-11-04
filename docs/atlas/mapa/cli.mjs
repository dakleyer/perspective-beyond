import {readFile} from 'node:fs/promises';
import {calculate,readRequest} from './radius.mjs';
import {positionMap,readPosition} from '../positioning.mjs';

try {
  const [query,graphPath]=process.argv.slice(2);
  if(!query||query==='--help') {
    console.log('node cli.mjs "centro=GH049&radio=2&peso=matematicas:0.5" [ruta-a-grafo.json]');
  } else {
    const graph=JSON.parse(await readFile(graphPath??new URL('./grafo.json',import.meta.url),'utf8'));
    const parameters=/^https?:\/\//i.test(query)?new URL(query).searchParams:new URLSearchParams(query);
    const result=parameters.has('posicionamiento')||parameters.has('tokens')?positionMap(graph,readPosition(parameters,graph)):calculate(graph,readRequest(parameters,graph.topics));
    console.log(JSON.stringify(result,null,2));
  }
} catch(error) {
  console.error(error.message);
  process.exitCode=1;
}
