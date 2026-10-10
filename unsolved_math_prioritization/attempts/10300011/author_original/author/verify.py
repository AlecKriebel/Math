#!/usr/bin/env python3
"""Finite diagnostics and integrity bindings, never a topological proof checker."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

EXPECTED = {'schema':'sublamination-scoped-claims-v1','problem_id':10300011,'catalog_id':'AMR-102-0011','rank':1004,'status':'unsolved','turns_used':5,'turns_budget':5,'general_solution':False,'novelty_claim':False,'independent_review':'pending','claim_ids':['finite_compact_leaf_characterization','circle_suspension_exclusion','intrinsic_weight_data_obstruction','regular_cover_witness_descent','carrier_containment_gap'],'verification_scope':'finite diagnostics and metadata; not a formal proof of topology'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def pairs(items):
    out = {}
    for k, v in items:
        require(k not in out, 'duplicate JSON key')
        out[k] = v
    return out

def invalid_constant(value):
    raise ValueError('nonfinite JSON constant')

def read_json(path, limit=2_000_000):
    p=Path(path)
    require(p.is_file() and not p.is_symlink(), 'expected regular nonsymlink JSON file')
    raw=p.read_bytes()
    require(len(raw)<=limit, 'JSON too large')
    return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=invalid_constant)

def validate_claims(value):
    require(type(value) is dict and set(value)==set(EXPECTED),'claim key set mismatch')
    for key, expected in EXPECTED.items():
        require(type(value[key]) is type(expected),'claim type mismatch: '+key)
        require(value[key]==expected,'claim value mismatch: '+key)
    return True

def graph_blocks(vertices, edges, retained):
    require(type(vertices) is int and vertices>0,'bad vertex count')
    require(type(edges) is list and len(edges)>0,'empty edges')
    require(type(retained) is list and len(retained)>0,'retain at least one edge')
    require(all(type(i) is int and 0<=i<len(edges) for i in retained),'bad retained edge')
    require(len(set(retained))==len(retained),'duplicate retained edge')
    degree=[0]*vertices
    parent=list(range(vertices))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]
            i=parent[i]
        return i
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b: parent[b]=a
    for edge in edges:
        require(type(edge) is list and len(edge)==2,'bad edge')
        a,b=edge
        require(type(a) is int and type(b) is int and 0<=a<vertices and 0<=b<vertices,'bad edge endpoint')
        degree[a]+=1; degree[b]+=1
        union(a,b)
    require(len({find(v) for v in range(vertices)})==1,'disconnected graph')
    require(all(d in (1,2) for d in degree),'not a path/cycle degree profile')
    parent[:]=range(vertices)
    keep=set(retained)
    for i,(a,b) in enumerate(edges):
        if i not in keep: union(a,b)
    groups={}
    for v in range(vertices): groups.setdefault(find(v),[]).append(v)
    result=[]
    for vv in groups.values():
        s=set(vv)
        caps=sum(degree[v]==1 for v in vv)
        boundary=sum((a in s)+(b in s) for i,(a,b) in enumerate(edges) if i in keep)
        require(caps<=1,'two twisted endpoints in a merged block')
        require(boundary==2-caps,'incorrect remaining horizontal boundary count')
        result.append((len(vv),caps,boundary))
    return sorted(result)

def diagnostics():
    graph_count=0
    for n in range(1,13):
        for kind in ('path','cycle'):
            vertices=n+1 if kind=='path' else n
            edges=[[i,i+1] for i in range(n)] if kind=='path' else [[i,(i+1)%n] for i in range(n)]
            for mask in range(1,2**n):
                graph_blocks(vertices,edges,[i for i in range(n) if mask>>i&1])
                graph_count+=1
    require(graph_blocks(1,[[0,0]],[0])==[(1,0,2)],'self-loop degree control')
    require(graph_blocks(2,[[0,1]],[0])==[(1,1,1),(1,1,1)],'two twisted endpoints separated control')
    negative_graphs=[(2,[[0,1]],[]),(True,[[0,0]],[0]),(2,[[0,2]],[0]),(2,[[0,1]],[True]),(2,[[0,1]],[0,0]),(4,[[0,1],[2,3]],[0]),(4,[[0,1],[0,2],[0,3]],[0]),(2,[[0,1,0]],[0])]
    rejected=0
    for args in negative_graphs:
        try: graph_blocks(*args)
        except ValueError: rejected+=1
        else: raise ValueError('malformed graph accepted')
    arithmetic=0
    for g in range(2,31):
        free_rank=2*(g-1)+2-1
        betti=free_rank+1
        require(free_rank==2*g-1 and free_rank>=3,'surface free rank failed')
        require(betti==2*g and betti!=2,'vertical torus Betti obstruction failed')
        require((2-2*(g-1)-2)==2-2*g,'surface Euler characteristic failed')
        arithmetic+=3
    return {'graph_masks_checked':graph_count,'special_graph_checks':2,'malformed_graphs_rejected':rejected,'surface_arithmetic_checks':arithmetic}

def verify_sources(root, source_dir):
    sources=read_json(root/'SOURCE_PINS.json')['sources']
    for item in sources:
        p=Path(source_dir)/item['filename']
        require(p.is_file() and not p.is_symlink(),'missing/nonregular source')
        b=p.read_bytes()
        require(len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],'source bytes mismatch: '+item['filename'])
    return len(sources)

def verify_corpora(root, corpus_dir):
    binding=read_json(root/'CORPUS_BINDINGS.json')
    loaded={}
    for item in binding['corpora']:
        p=Path(corpus_dir)/item['name']
        require(p.is_file() and not p.is_symlink(),'missing/nonregular corpus')
        b=p.read_bytes()
        require(len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],'corpus bytes mismatch: '+item['name'])
        obj=json.loads(b)
        require(len(obj)==item['record_count'],'corpus record count mismatch')
        loaded[item['name']]=obj
    records=[x for x in loaded['problems.json'] if x['id']==10300011]
    require(len(records)==1,'target record multiplicity mismatch')
    record=records[0]
    inherited=loaded['research_results.json']['AMR-102-0011']
    for obj,key in [(record,'matched_record_sha256'),(inherited,'inherited_research_sha256')]:
        require(hashlib.sha256(json.dumps(obj,sort_keys=True).encode()).hexdigest()==binding[key],'selected record hash mismatch')
    return {'problems':15458,'research_results':6701,'selected_record_matches':1}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path)
    parser.add_argument('--sources-dir',type=Path)
    parser.add_argument('--corpora-dir',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    validate_claims(read_json(args.input or root/'CLAIMS.json'))
    ledger=read_json(root/'APPROACH_LEDGER.json')
    require(ledger['problem_id']==10300011 and ledger['total_substantive_turns']==5,'ledger mismatch')
    require([x['turn'] for x in ledger['approaches']]==[1,2,3,4,5],'turn sequence mismatch')
    result={'status':'PASS_SCOPED_CONTROLS','problem_id':10300011,'general_solution':False,'topological_proof_machine_verified':False,**diagnostics()}
    if args.sources_dir is not None: result['source_files_matched']=verify_sources(root,args.sources_dir)
    if args.corpora_dir is not None: result['corpora_matched']=verify_corpora(root,args.corpora_dir)
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,TypeError,UnicodeError,OSError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(2)
