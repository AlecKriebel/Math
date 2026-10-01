#!/usr/bin/env python3
"""Reviewer's own standard-library diagnostic checker; no imported project code."""
from itertools import combinations
from collections import Counter
from math import comb
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent
P=ROOT
checks=Counter()
def check(ok, kind):
    if not ok: raise AssertionError(kind)
    checks[kind]+=1

def closure(tops):
    faces={frozenset()}
    for top in tops:
        for n in range(1,len(top)+1):
            faces.update(frozenset(x) for x in combinations(top,n))
    return faces

def vectors(faces,D):
    return [sum(len(x)==n for x in faces) for n in range(D+2)]

def polynomial(f,D):
    # Build sum f[i]*(t-1)^(D+1-i) by repeated multiplication, ascending powers.
    ans=[0]*(D+2)
    for i,value in enumerate(f):
        p=[value]
        for j in range(D+1-i):
            out=[0]*(len(p)+1)
            for k,v in enumerate(p): out[k]-=v;out[k+1]+=v
            p=out
        for k,v in enumerate(p): ans[k]+=v
    return ans[::-1]

def boundary(tops,D):
    count=Counter(frozenset(x) for T in tops for x in combinations(T,D))
    check(set(count.values())<={1,2},'ridge_incidence')
    return closure([x for x,n in count.items() if n==1])

def inspect(tops,D):
    faces=closure(tops);bound=boundary(tops,D)
    f=vectors(faces,D); h=polynomial(f,D)
    vi=f[1]-vectors(bound,D)[1]
    q=f[2]-D*f[1]+comb(D+1,2)-vi
    check(q==h[2]-vi,'h2_normalization')
    check(h[D]+(D+1)*h[D+1]==vi,'actual_interior_vertex_identity')
    apex=('cone',0)
    cap=faces|{x|{apex} for x in bound}
    fcap=vectors(cap,D)
    check(fcap[1]==f[1]+1 and fcap[2]==f[2]+f[1]-vi,'cone_face_counts')
    check(fcap[2]-(D+1)*fcap[1]+comb(D+2,2)==q,'cone_g2')
    check({x-{apex} for x in cap if apex in x}==bound,'apex_link')
    return q,vi,faces,bound

def rank_mod2(columns):
    basis={}
    for col in columns:
        while col:
            k=col.bit_length()-1
            if k not in basis: basis[k]=col;break
            col^=basis[k]
    return len(basis)

def betti(faces,D):
    layers=[list(x for x in faces if len(x)==n+1) for n in range(D+1)]
    ranks=[0]
    for n in range(1,D+1):
        index={x:i for i,x in enumerate(layers[n-1])}
        columns=[]
        for cell in layers[n]:
            columns.append(sum(1<<index[cell-{v}] for v in cell))
        ranks.append(rank_mod2(columns))
    ranks.append(0)
    return [len(layers[n])-ranks[n]-ranks[n+1] for n in range(D+1)]

# Coefficient-basis check is exhaustive for the linear h2 formula, for each dimension.
for D in range(2,18):
    for i in range(D+2):
        f=[0]*(D+2);f[i]=1
        expected=comb(D+1,2) if i==0 else -D if i==1 else 1 if i==2 else 0
        check(polynomial(f,D)[2]==expected,'coefficient_basis')
    for r in range(1,25):
        check(r*comb(D+1,2)-D*r*(D+1)+comb(D+1,2)==(1-r)*comb(D+1,2),'disconnected_offset')
    v=D+2;e=comb(v,2)
    check(e-D*v+comb(D+1,2)-v==-(D+1),'closed_offset')

for D in range(2,8):
    tops={frozenset(range(D+1))}
    for n in range(9):
        q,vi,faces,bound=inspect(tops,D)
        check((q,vi)==(0,0),'boundary_stacked_balls')
        if n<8:
            facet=min((x for x in bound if len(x)==D),key=lambda x:sorted(x))
            old=vectors(faces,D)
            tops.add(facet|{D+n+1})
            new=vectors(closure(tops),D)
            check((new[1]-old[1],new[2]-old[2])==(1,D),'stacking_increments')
    # Nonzero interior-vertex control absent from original explicit complexes.
    original=frozenset(range(D+1));a=D+1
    interior_tops={original-{v}|{a} for v in original}
    q,vi,_,_=inspect(interior_tops,D)
    check((q,vi)==(0,1),'interior_stellar_simplex')

solid=[]
for D in range(2,6):
    for t in (3,4,5,6):
        tops=set()
        for a in range(t):
            lo,hi=sorted((a,(a+1)%t))
            # Monotone paths in edge x (D-1)-simplex; choose horizontal jump.
            for jump in range(D):
                path={(lo,j) for j in range(jump+1)}|{(hi,j) for j in range(jump,D)}
                tops.add(frozenset(path))
        q,vi,faces,bound=inspect(tops,D)
        check(len(tops)==D*t and vectors(faces,D)[1]==D*t,'product_sizes')
        check(sum((-1)**(len(x)-1) for x in faces if x)==0,'product_euler')
        if D==3:
            check(betti(faces,3)==[1,1,0,0],'solid_torus_homology_mod2')
            check(betti(bound,2)==[1,2,1],'torus_boundary_homology_mod2')
            for vertex in [next(iter(x)) for x in bound if len(x)==1]:
                link={x-{vertex} for x in bound if vertex in x}
                edges=[x for x in link if len(x)==2]
                deg=Counter(v for edge in edges for v in edge)
                check(set(deg.values())=={2} and betti(link,1)==[1,1],'boundary_vertex_link_cycle')
            solid.append({'cycle_vertices':t,'q':q,'f_vector':vectors(faces,D)[1:],
                          'boundary_f_vector':vectors(bound,D-1)[1:],'boundary_euler':0})
receipt=json.loads((P/'verification.json').read_text())
check(receipt['solid_torus_diagnostics']==solid,'original_receipt_diagnostics_match')
check(sum(receipt['categories'].values())==receipt['assertions']==4310,'original_receipt_count_consistent')
prov=json.loads((P/'provenance.json').read_text())
for f,k in [('SOURCE_STATUS.md','artifact_sha256'),('verify.py','verifier_sha256'),('verification.json','verification_sha256'),('source_record.json','source_record_sha256')]:
    check(hashlib.sha256((P/f).read_bytes()).hexdigest()==prov[k],'package_hash_matches')
print(json.dumps({'status':'PASS','reviewer_assertions':sum(checks.values()),'checks':dict(checks),
                  'solid_torus_diagnostics':solid,
                  'scope':'Independent finite normalization and example checks; not a boundary-finiteness proof. Original verify.py inspected but not executed.',
                  'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
