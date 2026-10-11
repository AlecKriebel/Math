#!/usr/bin/env python3
"""Exact finite controls for the bilinear Witt group F_2. No floating point.
These checks test the algebra adapter, not the universal geometric theorem.
"""
from itertools import product
from pathlib import Path
import json

def rank(vectors):
    pivots = {}
    for v in vectors:
        while v:
            k = v.bit_length()-1
            if k in pivots: v ^= pivots[k]
            else:
                pivots[k] = v
                break
    return len(pivots)

def basis(vectors):
    out=[]
    for v in vectors:
        if rank(out+[v])>len(out):out.append(v)
    return out

def pair(rows,x,y):
    value=0
    for i,r in enumerate(rows):
        if (x>>i)&1:value^=(r&y).bit_count()&1
    return value

def lagrangian(rows, vectors):
    if not vectors:return []
    n=len(vectors)
    assert n%2==0
    v=next(x for x in range(1,1<<len(rows)) if rank(vectors+[x])==n and pair(rows,x,x)==0)
    w=next(x for x in vectors if pair(rows,v,x))
    complement=[]
    for x in vectors:
        b=pair(rows,x,v)
        a=pair(rows,x,w)^(b*pair(rows,w,w))
        complement.append(x^(v if a else 0)^(w if b else 0))
    complement=basis(complement)
    assert len(complement)==n-2
    return [v]+lagrangian(rows,complement)

def matrix_from_mask(n,mask):
    rows=[0]*n;k=0
    for i in range(n):
        for j in range(i,n):
            if (mask>>k)&1:
                rows[i]|=1<<j;rows[j]|=1<<i
            k+=1
    return rows

def check_lagrangian(rows,L):
    n=len(rows)
    return rank(L)==n//2 and all(pair(rows,x,y)==0 for x in L for y in L)

result={'arithmetic':'exact F_2 bit operations','universal_geometric_theorem_tested':False,'exhaustive_dimensions':[]}
for n in range(6):
    count=alternating=metabolic=0
    for mask in range(1<<(n*(n+1)//2)):
        rows=matrix_from_mask(n,mask)
        if rank(rows)!=n:continue
        count+=1
        alternating+=all(not ((rows[i]>>i)&1) for i in range(n))
        if n%2==0:
            L=lagrangian(rows,[1<<i for i in range(n)])
            assert check_lagrangian(rows,L)
            metabolic+=1
    result['exhaustive_dimensions'].append(dict(dimension=n,nonsingular_symmetric=count,alternating_nonsingular=alternating,verified_metabolic=metabolic,odd_rank_obstruction=bool(n%2)))
controls={'hyperbolic_plane':[2,1],'identity_rank_two':[1,2],'identity_rank_one':[1]}
result['countercontrols']={}
for name,rows in controls.items():
    n=len(rows);L=lagrangian(rows,[1<<i for i in range(n)]) if n%2==0 else None
    result['countercontrols'][name]={'rows_bitmask':rows,'rank':rank(rows),'alternating':all(not ((rows[i]>>i)&1) for i in range(n)),'lagrangian_bitmask':L,'witt_class_rank_parity':n%2}
result['RP_controls_provenance']='Analytic cohomology-ring and orientation formulas; not computed triangulations.'
result['oriented_product_control']={'space':'S^(2j+1) x S^(2j+1), j>=0','dimension':'4j+2','middle_pairing':[[0,1],[1,0]],'middle_rank':2,'witt_class':0,'provenance':'Analytic Kunneth/intersection calculation; explicit nonzero-middle-homology target control.'}
result['RP_dimension_controls']=[{'j':j,'dimension':4*j+2,'middle_mod2_rank':1,'middle_pairing':[[1]],'integrally_orientable':False,'target_counterexample':False} for j in range(5)]
Path(__file__).with_name('EXACT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
