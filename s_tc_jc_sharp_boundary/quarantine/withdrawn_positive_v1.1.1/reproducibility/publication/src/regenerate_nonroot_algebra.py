#!/usr/bin/env python3
"""Regenerate bounded nonroot JC atlas signatures from primitive cycle/theta graphs.

This program does not read the distributed atlas summaries. It enumerates the
four directed theta event cores, every strong or completable weak selected
occupancy, and every outgoing-label permutation. For each ordered four-port
restriction it constructs the four displayed-tree descendant-mask tensor,
computes the seven exact JC invariant zero/nonzero bits, and writes canonical
strong and weak signature files. A companion C++ program performs the directed
submask join.

The exact-zero test is modular but deterministic and rigorous: coordinate
polynomials have coefficient l1 norm at most 9, and the largest invariant has
coefficient l1 norm below 64 and degree five. Hence every integer coefficient
has absolute value below 64*9**5 < 2^31-1. Vanishing modulo p=2^31-1 is
therefore equivalent to vanishing over Z after the complete sparse expansion.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import importlib.util
import json
from pathlib import Path
import struct
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
PUB = HERE.parent
ROOT = PUB.parent
EXACT = ROOT / "exact_release"
OUT = PUB / "certificates"
OUT.mkdir(parents=True, exist_ok=True)

# Load the primitive structural enumerator and the independently derived event cores.
def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

STRUCT = load_module("primitive_nonroot", HERE / "regenerate_nonroot_topology_atlases.py")
CORE = load_module("primitive_cores", EXACT / "src" / "core_enumerator.py")

P = 2_147_483_647
JC_REPS = (
    (0,0,0,0),(0,0,1,1),(0,1,0,1),(0,1,1,0),(0,1,2,3),
    (1,0,0,1),(1,0,1,0),(1,0,2,3),(1,1,0,0),(1,1,1,1),
    (1,1,2,2),(1,2,0,3),(1,2,1,2),(1,2,2,1),(1,2,3,0),
)
# Invariant coordinate indices refer to A,...,O, i.e. JC_REPS[1:].
INVARIANTS = (
    (((8,),1),((9,),-1),((11,),-1),((12,),1)),
    (((8,),1),((0,7),-1),((1,5),-1),((2,4),1)),
    (((6,10),1),((4,12),-1)),
    (((10,10),1),((1,4,7),-1)),
    (((1,11),1),((3,10),-1),((1,1,5),-1),((1,2,4),1)),
    (((1,4,13),1),((1,6,7),-1),((2,4,10),-1),((3,4,7),1)),
)
NEW_INV = json.loads((OUT/'quartet_invariant_exact_certificate.json').read_text())["new_invariant"]
INVARIANTS = INVARIANTS + (tuple((tuple(indices), int(coeff)) for coeff, indices in NEW_INV),)
assert len(INVARIANTS) == 7
assert max(sum(abs(c) for _m,c in inv) * 9**max(len(m) for m,_c in inv) for inv in INVARIANTS) < P

CHOICES = ((0,0),(0,1),(1,0),(1,1))
CHOICE_INDEX = {c:i for i,c in enumerate(CHOICES)}
CUBE_ACTIONS = tuple(sorted({
    tuple(CHOICE_INDEX[tuple(choice[order[i]] ^ flips[i] for i in range(2))] for choice in CHOICES)
    for order in ((0,1),(1,0)) for flips in CHOICES
}))
assert len(CUBE_ACTIONS) == 8


def digest_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def weak_compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total-first, parts-1):
            yield (first,) + rest


def lift(vertices, edges, selected_leaves, dummy_parents):
    rename = lambda v: "IN" if v == "S" else v
    vv = {rename(v): ("T" if v == "S" else c) for v,c in vertices.items()}
    ee = [(rename(u),rename(v)) for u,v in edges]
    vv.update({"ROOT":"S","LIN":"L"})
    ee.extend((("ROOT","IN"),("ROOT","LIN")))
    leaves = [(rename(v), label) for v,label in selected_leaves]
    for index,(parent,label) in enumerate(leaves):
        name=f"L{label}"; vv[name]="L"; ee.append((parent,name)); leaves[index]=(name,label)
    for index,parent in enumerate(dummy_parents):
        name=f"Z{index}"; vv[name]="L"; ee.append((rename(parent),name))
    leaves.append(("LIN", max(label for _v,label in leaves)+1 if leaves else 1))
    return {"vertices":vv,"edges":tuple(ee),"leaf_labels":dict(leaves)}


def build_weak(core, selected_sink_indices, counts):
    vertices=dict(core['vertex_types']); edges=[]; selected_parents=[]; dummy_parents=[]
    occupied={i for i,c in enumerate(counts) if c}
    repair=core['repairs'][0]
    for si,(seg,count) in enumerate(zip(core['directed_segments'],counts)):
        chain=[seg['tail']]
        for j in range(count):
            v=f"P{si}_{j}"; vertices[v]='T'; chain.append(v); selected_parents.append(v)
        if si in repair and si not in occupied:
            v=f"D{si}"; vertices[v]='T'; chain.append(v); dummy_parents.append(v)
        chain.append(seg['head']); edges.extend(zip(chain,chain[1:]))
    sinks=tuple(sorted(v for v,c in vertices.items() if c=='X'))
    for i,sink in enumerate(sinks):
        (selected_parents if i in selected_sink_indices else dummy_parents).append(sink)
    selected=[(parent,i+1) for i,parent in enumerate(selected_parents)]
    network=lift(vertices,edges,selected,dummy_parents)
    all_sinks_selected=len(selected_sink_indices)==len(sinks)
    selected_strong=all_sinks_selected and any(set(rep)<=occupied for rep in core['repairs'])
    return network, selected_strong


def weak_patterns(k: int):
    _raw,cores=CORE.enumerate_cores(); result=[]
    for ci,core in enumerate(cores):
        sinks=tuple(sorted(v for v,c in core['vertex_types'].items() if c=='X'))
        for j in range(min(len(sinks),k)+1):
            for ss in combinations(range(len(sinks)),j):
                for counts in weak_compositions(k-j,len(core['directed_segments'])):
                    network,strong=build_weak(core,ss,counts)
                    result.append((ci,ss,counts,network,strong))
    return result


def build_strong_from_role(data, k: int):
    vertices,paths,edges,entry,retics,bits,_lens=data
    vv={str(v):('R' if v in retics else 'T') for v in range(len(vertices))}
    ee=[]
    for bit,(u,v,*_) in zip(bits,edges):
        a,b=(u,v) if bit==0 else (v,u); ee.append((str(a),str(b)))
    outs=[v for v in range(len(vertices)) if not vertices[v]['pole'] and v!=entry]
    assert len(outs)==k
    selected=[(str(v),i+1) for i,v in enumerate(outs)]
    # Lift with the actual entry as the incoming attachment, not the event-core S name.
    vv['S']='S'; vv['LIN']='L'; ee.extend((('S',str(entry)),('S','LIN')))
    leaf_labels={'LIN':k+1}
    for parent,label in selected:
        name=f'L{label}';vv[name]='L';ee.append((parent,name));leaf_labels[name]=label
    return {'vertices':vv,'edges':tuple(ee),'leaf_labels':leaf_labels}, outs


def reticulations(network):
    return tuple(sorted(v for v,c in network['vertices'].items() if c in {'R','X'}))


def full_descendant_signatures(network):
    edges=network['edges']; labels=network['leaf_labels']; rs=reticulations(network)
    assert len(rs)==2
    signatures=[[] for _ in edges]
    for choice in CHOICES:
        excluded=set()
        for r,bit in zip(rs,choice):
            incoming=tuple(i for i,(u,v) in enumerate(edges) if v==r)
            assert len(incoming)==2,(r,incoming)
            excluded.add(incoming[1-bit])
        selected=[i for i in range(len(edges)) if i not in excluded]
        children=defaultdict(list)
        for i in selected:children[edges[i][0]].append(edges[i][1])
        cache={}
        def descend(v):
            if v in cache:return cache[v]
            if v in labels:ans=1<<(labels[v]-1)
            else:
                ans=0
                for w in children.get(v,()):ans|=descend(w)
            cache[v]=ans;return ans
        selected_set=set(selected)
        for i,(u,v) in enumerate(edges):signatures[i].append(descend(v) if i in selected_set else 0)
    return tuple(tuple(x) for x in signatures)


def subset_transports(total: int):
    subsets=tuple(combinations(range(1,total+1),4))
    tables=[]
    for q in subsets:
        position={label:i for i,label in enumerate(q)}
        arr=[]
        for mask in range(1<<total):
            value=0
            for label,pos in position.items():
                if mask>>(label-1)&1:value|=1<<pos
            arr.append(value)
        tables.append(tuple(arr))
    return subsets,tuple(tables)


def reduced_type(full_signatures, transport):
    signatures=[]
    for sig in full_signatures:
        item=tuple(transport[m] for m in sig)
        if any(item):signatures.append(item)
    signatures=tuple(sorted(set(signatures)))
    return min(tuple(sorted(tuple(sig[i] for i in action) for sig in signatures)) for action in CUBE_ACTIONS)

# Sparse polynomial arithmetic modulo P.
def p_add(a,b):
    out=dict(a)
    for m,c in b.items():
        v=(out.get(m,0)+c)%P
        if v:out[m]=v
        elif m in out:del out[m]
    return out

def p_mul(a,b):
    if not a or not b:return {}
    if len(a)>len(b):a,b=b,a
    out={}
    for ma,ca in a.items():
        for mb,cb in b.items():
            m=tuple(x+y for x,y in zip(ma,mb));out[m]=(out.get(m,0)+ca*cb)%P
    return {m:c for m,c in out.items() if c}


def coordinate_sparse(tensor_type):
    n=len(tensor_type)+2; zero=(0,)*n
    coords=[]
    for assignment in JC_REPS[1:]:
        total={}
        for ci,choice in enumerate(CHOICES):
            edge_exp=[0]*len(tensor_type)
            for ei,sig in enumerate(tensor_type):
                mask=sig[ci];ch=0
                for pos in range(4):
                    if mask>>pos&1:ch^=assignment[pos]
                if ch:edge_exp[ei]=1
            base=tuple(edge_exp+[0,0])
            terms=[]
            # l0,l1 are final variables.
            def mon(e0,e1,c):
                x=list(base);x[-2]=e0;x[-1]=e1;return (tuple(x),c%P)
            if choice==(0,0):terms=[mon(1,1,1)]
            elif choice==(0,1):terms=[mon(1,0,1),mon(1,1,-1)]
            elif choice==(1,0):terms=[mon(0,1,1),mon(1,1,-1)]
            else:terms=[mon(0,0,1),mon(1,0,-1),mon(0,1,-1),mon(1,1,1)]
            for m,c in terms:total[m]=(total.get(m,0)+c)%P
        coords.append({m:c for m,c in total.items() if c})
    return tuple(coords)


def coordinate_eval(tensor_type, seed):
    vals=[(seed+37*i+11)%P or 2 for i in range(len(tensor_type)+2)]
    l0,l1=vals[-2:];outs=[]
    for assignment in JC_REPS[1:]:
        total=0
        for ci,choice in enumerate(CHOICES):
            weight=(l0 if choice[0]==0 else 1-l0)*(l1 if choice[1]==0 else 1-l1)%P
            term=weight
            for ei,sig in enumerate(tensor_type):
                mask=sig[ci];ch=0
                for pos in range(4):
                    if mask>>pos&1:ch^=assignment[pos]
                if ch:term=term*vals[ei]%P
            total=(total+term)%P
        outs.append(total)
    return outs


def invariant_eval(coords,inv):
    ans=0
    for mon,c in inv:
        t=c%P
        for i in mon:t=t*coords[i]%P
        ans=(ans+t)%P
    return ans


def invariant_sparse(coords,inv):
    n=len(next(iter(coords[0]))) if coords[0] else 0
    zero=(0,)*n;ans={}
    cache={():{zero:1}}
    for mon,c in inv:
        key=tuple(sorted(mon))
        if key not in cache:
            t={zero:1}
            for i in key:t=p_mul(t,coords[i])
            cache[key]=t
        term={m:(c*v)%P for m,v in cache[key].items()}
        ans=p_add(ans,term)
    return ans

TYPE_BITS={}
def type_bits(tensor_type):
    if tensor_type in TYPE_BITS:return TYPE_BITS[tensor_type]
    evals=[coordinate_eval(tensor_type,s) for s in (101,1009,10007)]
    sparse=None;bits=0
    for j,inv in enumerate(INVARIANTS):
        nonzero=any(invariant_eval(c,inv) for c in evals)
        if not nonzero:
            if sparse is None:sparse=coordinate_sparse(tensor_type)
            nonzero=bool(invariant_sparse(sparse,inv))
        if nonzero:bits|=1<<j
    TYPE_BITS[tensor_type]=bits
    return bits


def ordered_quartets(total):return tuple(permutations(range(1,total+1),4))

def permutation_transports(k,quartets):
    lookup={q:i for i,q in enumerate(quartets)}; result=[]
    for perm in permutations(range(1,k+1)):
        inv={new:old for old,new in enumerate(perm,1)};inv[k+1]=k+1
        result.append(tuple(lookup[tuple(inv[x] for x in q)] for q in quartets))
    return tuple(result)


PERMUTED_TYPE_CACHE={}
def permuted_type(tensor_type, position_perm):
    key=(tensor_type,position_perm)
    if key in PERMUTED_TYPE_CACHE:return PERMUTED_TYPE_CACHE[key]
    transformed=[]
    for sig in tensor_type:
        item=[]
        for mask in sig:
            value=0
            for oldpos,newpos in enumerate(position_perm):
                if mask>>oldpos&1:value|=1<<newpos
            item.append(value)
        transformed.append(tuple(item))
    transformed=tuple(sorted(set(transformed)))
    result=min(tuple(sorted(tuple(sig[i] for i in action) for sig in transformed)) for action in CUBE_ACTIONS)
    PERMUTED_TYPE_CACHE[key]=result
    return result

def deck(network, quartets, subset_info):
    subsets,tables=subset_info;lookup={q:i for i,q in enumerate(quartets)}
    fs=full_descendant_signatures(network);out=bytearray(len(quartets))
    for subset,transport in zip(subsets,tables):
        base=reduced_type(fs,transport)
        for ordered in permutations(subset):
            # old position is the sorted-subset position; new position is its position in ordered.
            posperm=tuple(ordered.index(label) for label in subset)
            out[lookup[ordered]]=type_bits(permuted_type(base,posperm))
    return bytes(out)

SPECIAL_CORE_CODE="('TP', 'TP', ((-1, 'TS', 1), (1, 'R', -1), (1, 'R', -1)))"

def strong_base(k):
    # STRUCT p counts the distinguished incoming vertex as one port.
    _pres,roles=STRUCT.enumerate_theta_role(k+1)
    records=[]
    for data in roles.values():
        v,paths,edges,entry,ret,bits,_lens=data
        event=repr(STRUCT.theta_event_core_code(v,paths,edges,entry,ret,bits))
        if k==6 and event!=SPECIAL_CORE_CODE:continue
        network,outs=build_strong_from_role(data,k)
        records.append((data,network,outs))
    return records


def regenerate(k:int):
    total=k+1;quartets=ordered_quartets(total);mask_tables=subset_transports(total)
    perm_trans=permutation_transports(k,quartets)
    strong_records=strong_base(k);weak_records=weak_patterns(k)
    print(f'[atlas k={k}] strong base roles {len(strong_records)} weak roles {len(weak_records)} quartets {len(quartets)}',flush=True)
    strong_decks=[];strong_codes=[]
    for idx,(data,network,outs) in enumerate(strong_records):
        d=deck(network,quartets,mask_tables);strong_decks.append(d)
        strong_codes.append(data)
        if (idx+1)%10==0: print(f'[atlas k={k}] strong decks {idx+1}/{len(strong_records)} types {len(TYPE_BITS)}',flush=True)
    weak_decks=[];weak_status=[]
    for idx,(_ci,_ss,_counts,network,status) in enumerate(weak_records):
        weak_decks.append(deck(network,quartets,mask_tables));weak_status.append(status)
        if (idx+1)%100==0: print(f'[atlas k={k}] weak decks {idx+1}/{len(weak_records)} types {len(TYPE_BITS)}',flush=True)
    print(f'[atlas k={k}] unique reduced tensor types {len(TYPE_BITS)}',flush=True)
    strong_matrix=np.frombuffer(b''.join(strong_decks),dtype=np.uint8).reshape(len(strong_decks),len(quartets))
    weak_matrix=np.frombuffer(b''.join(weak_decks),dtype=np.uint8).reshape(len(weak_decks),len(quartets))
    strong_map={}
    perms=tuple(permutations(range(1,k+1)))
    for data,row in zip(strong_codes,strong_matrix):
        v,paths,edges,entry,ret,bits,_lens=data
        outs=[x for x in range(len(v)) if not v[x]['pole'] and x!=entry]
        for perm,trans in zip(perms,perm_trans):
            sig=row[np.asarray(trans,dtype=np.int32)].tobytes()
            labels=dict(zip(outs,perm));code=repr(STRUCT.theta_code(v,paths,edges,entry,ret,bits,labels,True))
            if sig in strong_map: assert strong_map[sig]==code
            strong_map[sig]=code
    weak_map={}
    weak_status_array=np.asarray(weak_status,dtype=np.uint8)
    for trans in perm_trans:
        transported=weak_matrix[:,np.asarray(trans,dtype=np.int32)]
        unique,inverse=np.unique(transported,axis=0,return_inverse=True)
        for ui,row in enumerate(unique):
            statuses=set(weak_status_array[inverse==ui].tolist())
            assert len(statuses)==1
            sig=row.tobytes();status=bool(next(iter(statuses)))
            if sig in weak_map: assert weak_map[sig]==status
            weak_map[sig]=status
    strong=sorted(strong_map);weak=sorted(weak_map)
    assert len(strong)==len(set(strong_map.values())), 'non-T signature collision'
    mixed=0
    # Exact-equal signatures must be selected-strong; graph replay remains a separate certificate.
    equal=set(strong)&set(weak)
    assert all(weak_map[s] for s in equal)
    strong_path=OUT/f'theta_k{k}_strong_signatures.bin';weak_path=OUT/f'theta_k{k}_weak_signatures.bin'
    strong_path.write_bytes(b''.join(strong));weak_path.write_bytes(b''.join(weak))
    result={
      'status':'EXACTLY COMPUTED FROM PRIMITIVE GRAPHS', 'outgoing_count':k,
      'ordered_quartets':len(quartets),'bytes_per_signature':len(quartets),
      'strong_base_roles':len(strong_records),'weak_role_presentations':len(weak_records),
      'strong_signatures':len(strong),'weak_signatures':len(weak),'equal_signatures':len(equal),
      'non_T_strong_signature_collisions':0,'mixed_strength_signatures':mixed,
      'reduced_tensor_types':len(TYPE_BITS),
      'strong_sha256':digest_bytes(strong_path.read_bytes()),'weak_sha256':digest_bytes(weak_path.read_bytes()),
    }
    (OUT/f'theta_k{k}_regenerated.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,choices=(5,6));args=ap.parse_args()
    result=regenerate(args.k)
    expected={5:(8520,16590,8520,360,1512),6:(10980,218925,10980,840,2856)}[args.k]
    assert (result['strong_signatures'],result['weak_signatures'],result['equal_signatures'],result['ordered_quartets'],result['weak_role_presentations'])==expected
    print('ALL PRIMITIVE NONROOT ALGEBRA CHECKS PASSED')
if __name__=='__main__':main()
