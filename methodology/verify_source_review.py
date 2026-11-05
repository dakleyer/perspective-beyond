"""Check an incremental source-review bundle using Python's standard library.

Usage: python verify_source_review.py examples/source-review-cycle.json
       python verify_source_review.py examples/source-review-cycle.json --self-test
"""
import argparse,copy,hashlib,json
from pathlib import Path

def fingerprint(record):
    return hashlib.sha256(json.dumps(record,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def validate(bundle):
    errors=[];nodes=bundle['nodes'];edges=bundle['relations'];items=bundle['items'];base=bundle['baseline']
    ni={n['id']:n for n in nodes};ei={e['id']:e for e in edges};ii={i['id'] for i in items}
    if len(ni)!=len(nodes):errors.append('duplicate node ID')
    if len(ei)!=len(edges):errors.append('duplicate edge ID')
    for nid in base['node_ids']:
        if nid not in ni:errors.append('missing prior node '+nid)
    for eid in base['relation_ids']:
        if eid not in ei:errors.append('missing prior edge '+eid)
    allowed={d['node_id']:d for d in bundle.get('enrichments',[])}
    for nid,h in base.get('node_hashes',{}).items():
        if nid in ni and fingerprint(ni[nid])!=h:
            change=allowed.get(nid,{})
            if change.get('prior_node_hash')!=h or not change.get('reason') or not change.get('prior_description'):
                errors.append('unrecorded change to prior node '+nid)
    for eid,h in base.get('relation_hashes',{}).items():
        if eid in ei and fingerprint(ei[eid])!=h:errors.append('changed prior edge '+eid)
    for n in nodes:
        if n.get('record_type')!='node' or not n.get('description','').strip():errors.append('invalid node '+n['id'])
        if not n.get('item_refs') or any(r['item_id'] not in ii or not r.get('locator') for r in n.get('item_refs',[])):
            errors.append('unlocated node source '+n['id'])
    for e in edges:
        a=e.get('from',e.get('source'));b=e.get('to',e.get('target'))
        if a not in ni or b not in ni:errors.append('unresolved edge endpoint '+e['id'])
        if e.get('from',a)!=e.get('source',a) or e.get('to',b)!=e.get('target',b):errors.append('conflicting endpoint aliases '+e['id'])
        if not e.get('predicate') or not e.get('reason','').strip():errors.append('unexplained edge '+e['id'])
        if e.get('semantic_direction') not in ['directed','symmetric','inverse_available']:errors.append('invalid direction '+e['id'])
        if not e.get('item_refs') or any(r['item_id'] not in ii for r in e.get('item_refs',[])):errors.append('unresolved edge source '+e['id'])
        if any(k in e for k in ['abcd','jf_roles','global_score']):errors.append('situated assessment placed on edge '+e['id'])
    for d in bundle.get('decisions',[]):
        if not d.get('source_locator') or not d.get('reason'):errors.append('unlocated review decision')
        if any(n not in ni for n in d.get('output_node_ids',[])):errors.append('review decision points to missing node')
    return errors

def self_test(bundle):
    cases=[]
    def run(name,mutate):
        b=copy.deepcopy(bundle);mutate(b);errors=validate(b);cases.append({'case':name,'rejected':bool(errors)})
    run('missing earlier node',lambda b:b['nodes'].__setitem__(slice(None),[n for n in b['nodes'] if n['id']!=b['baseline']['node_ids'][0]]))
    run('changed earlier relation',lambda b:b['relations'][0].__setitem__('predicate','replaced meaning'))
    run('missing relationship reason',lambda b:b['relations'][-1].__setitem__('reason',''))
    run('unresolved source',lambda b:b['nodes'][-1]['item_refs'][0].__setitem__('item_id','missing-item'))
    run('global epistemic label',lambda b:b['relations'][-1].__setitem__('abcd','A'))
    return cases

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('bundle',type=Path);p.add_argument('--self-test',action='store_true');a=p.parse_args()
    b=json.loads(a.bundle.read_bytes());errors=validate(b)
    result={'result':'pass' if not errors else 'fail','nodes':len(b['nodes']),'relations':len(b['relations']),'errors':errors}
    if a.self_test:
        cases=self_test(b);result['negative_cases']=cases
        if not all(c['rejected'] for c in cases):result['result']='fail'
    print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(result['result']!='pass')
