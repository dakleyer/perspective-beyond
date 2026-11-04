#!/usr/bin/env node
/** Verify published Atlas identities and relationships across all ancestor editions. */
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';
const ref=process.argv[2]??'HEAD';
const repo=process.argv[3]??resolve(dirname(fileURLToPath(import.meta.url)),'..');
const git=(...args)=>execFileSync('git',['-C',repo,...args],{encoding:'utf8',maxBuffer:40e6});
if(ref==='--self-test'){selfTest();process.exit(0);}
const paths=['docs/data/atlas.json','docs/atlas/global-catalog.json','docs/atlas/dialogos/publico.json'];
const refs=git('rev-list','--reverse',ref,'--',...paths).trim().split('\n').filter(Boolean);
function read(commit,path){return JSON.parse(git('show',commit+':'+path));}
function records(commit){
 const exists=new Set(git('ls-tree','-r','--name-only',commit,'--',...paths).trim().split('\n'));
 const base=exists.has(paths[0])?read(commit,paths[0]):{},overlay=exists.has(paths[1])?read(commit,paths[1]):{};
 return {fichas:[...base.sources??[],...overlay.sources??[]],concepts:[...base.concepts??[],...overlay.concepts??[]],
  relations:[...base.documentRelations??[],...overlay.relations??[]],conceptRelations:[...base.relations??[],...overlay.concept_relations??[]],
  dialogues:exists.has(paths[2])?read(commit,paths[2]).cards:[]};
}
const now=records(ref),current=Object.fromEntries(Object.entries(now).map(([k,v])=>[k,new Map(v.map(r=>[r.id,r]))]));
const errors=[],seen=new Set();
function fail(item){const key=JSON.stringify(item);if(!seen.has(key)){seen.add(key);errors.push(item);}}
for(const commit of refs){
 const old=records(commit);
 compareRecords(old,current,commit,fail);
}
function compareRecords(old,current,commit,fail){
 for(const[k,items]of Object.entries(old))for(const item of items){
  const present=current[k].get(item.id);
  if(!present){fail({kind:'missing_record',collection:k,id:item.id,firstChecked:commit});continue;}
  if(k==='relations'||k==='conceptRelations'){
   if(item.from!==present.from||item.to!==present.to)fail({kind:'changed_relation_endpoints',collection:k,id:item.id,commit});
  }
  for(const field of ['title','url','definition','reading','body'])if(typeof item[field]==='string'&&item[field].trim()&&!(typeof present[field]==='string'&&present[field].trim()))fail({kind:'emptied_content',collection:k,id:item.id,field,commit});
  if(k==='concepts')for(const source of item.sources??[])if(!present.sources?.includes(source))fail({kind:'missing_concept_source',id:item.id,source,commit});
 }
}
function selfTest(){
 const original={fichas:[{id:'S1',title:'Source one',url:'https://example.test/one'},{id:'S2',title:'Source two',url:'https://example.test/two'}],concepts:[{id:'C1',sources:['S1']}],relations:[{id:'R1',from:'S1',to:'S2',reading:'A documented comparison.'}],conceptRelations:[],dialogues:[{id:'D1',body:'A preserved thought.'}]};
 const cases=[
  ['unchanged',()=>{},false],
  ['additive',d=>d.fichas.push({id:'S3',title:'Source three',url:'https://example.test/three'}),false],
  ['missing ficha',d=>d.fichas.pop(),true],
  ['missing relation',d=>d.relations.pop(),true],
  ['changed endpoints',d=>d.relations[0].to='S1',true],
  ['lost concept association',d=>d.concepts[0].sources=[],true],
  ['emptied dialogue',d=>d.dialogues[0].body='',true]
 ];
 for(const[name,change,shouldFail]of cases){const data=structuredClone(original);change(data);const maps=Object.fromEntries(Object.entries(data).map(([k,v])=>[k,new Map(v.map(r=>[r.id,r]))]));const errors=[];compareRecords(original,maps,'fixture',e=>errors.push(e));if(Boolean(errors.length)!==shouldFail)throw Error('Preservation self-test failed: '+name);}
 console.log(JSON.stringify({selfTests:cases.length,passed:cases.length}));
}
const graphPath='docs/atlas/mapa/grafo.json',graph=read(ref,graphPath),graphEdges=new Map(graph.edges.map(e=>[e[0],e]));
const graphRefs=git('rev-list','--reverse',ref,'--',graphPath).trim().split('\n').filter(Boolean);
for(const commit of graphRefs)for(const edge of read(commit,graphPath).edges){
 const present=graphEdges.get(edge[0]);
 if(!present)fail({kind:'missing_graph_relation',id:edge[0],commit});
 else if(edge[1]!==present[1]||edge[2]!==present[2])fail({kind:'changed_graph_relation_endpoints',id:edge[0],commit});
}
const nodeIds=new Set(graph.nodes.map(n=>n.id));
if(nodeIds.size!==graph.nodes.length)fail({kind:'duplicate_graph_node'});
if(graphEdges.size!==graph.edges.length)fail({kind:'duplicate_graph_relation'});
for(const e of graph.edges)if(!nodeIds.has(e[1])||!nodeIds.has(e[2]))fail({kind:'dangling_graph_relation',id:e[0]});
for(const n of graph.nodes)if(n.tagWeights&&Math.abs(Object.values(n.tagWeights).reduce((a,b)=>a+b,0)-1)>1e-9)fail({kind:'invalid_composition',id:n.id});
const deleted=git('log','--format=','--diff-filter=D','--name-only',ref,'--','docs').trim().split('\n').filter(Boolean);
for(const path of new Set(deleted))fail({kind:'deleted_published_path',path});
const result={ref:git('rev-parse',ref).trim(),catalogueEditions:refs.length,graphEditions:graphRefs.length,
 fichas:graph.nodes.filter(n=>n.type==='ficha').length,concepts:graph.nodes.filter(n=>n.type==='concepto').length,
 graphRelations:graph.edges.length,dialogues:now.dialogues.length,historicalMissingRecords:errors.length,
 deletedPublishedPaths:[...new Set(deleted)],errors,pass:errors.length===0};
console.log(JSON.stringify(result,null,2));
if(!result.pass)process.exitCode=1;
