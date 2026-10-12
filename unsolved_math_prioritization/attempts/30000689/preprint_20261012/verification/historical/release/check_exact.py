#!/usr/bin/env python3
"""Exact finite controls for the missing-face proof; standard library only.

No floating point, packages, network, or file mutations. These are consistency
checks, not a finite proof of the universal theorem or a sphere recognizer.
"""
import itertools as it
import json
import math
from collections import Counter


def faces_from_facets(facets):
    return {tuple(c) for f in facets for k in range(len(f)+1)
            for c in it.combinations(sorted(f), k)}


def stellar_example(d):
    # Boundary of a (2d+1)-simplex, stellarly subdivided at a d-face.
    old = set(range(2*d+2))
    t = frozenset(range(d+1))
    new = 2*d+2
    facets = []
    for omitted in old:
        f = old-{omitted}
        if t <= f:
            facets.extend((f-{v}) | {new} for v in t)
        else:
            facets.append(f)
    s = faces_from_facets(facets)
    tt = tuple(sorted(t))
    assert tt not in s
    assert all(tt[:i]+tt[i+1:] in s for i in range(d+1))
    k = {f for f in s if len(f) <= d+1}
    l = k | {tt}
    n = 2*d+3
    complete = {c for j in range(d+2) for c in it.combinations(range(n),j)}
    assert l == complete
    f = [sum(len(a)==j for a in s) for j in range(2*d+2)]
    r = 2*d+1
    h = [sum((-1)**(i-j)*math.comb(r-j,i-j)*f[j]
             for j in range(i+1)) for i in range(r+1)]
    assert h == h[::-1]
    return s,k,l,dict(d=d,vertices=n,faces_including_empty=f,h=h,
                     missing_face=list(tt),augmented_is_full_flores_skeleton=True)


def monomials(n,k,faces):
    return [m for m in it.combinations_with_replacement(range(n),k)
            if tuple(sorted(set(m))) in faces]


def rank_mod(rows,p):
    basis={}
    for row in rows:
        a={i:x%p for i,x in row.items() if x%p}
        while a:
            pivot=min(a)
            if pivot not in basis:
                inv=pow(a[pivot],-1,p)
                basis[pivot]={i:v*inv%p for i,v in a.items()}
                break
            factor=a[pivot]
            for i,v in basis[pivot].items():
                value=(a.get(i,0)-factor*v)%p
                if value:a[i]=value
                else:a.pop(i,None)
    return len(basis)


def quotient_dimension(faces,n,r,k,p=101):
    top=monomials(n,k,faces)
    idx={m:i for i,m in enumerate(top)}
    lower=monomials(n,k-1,faces)
    rows=[]
    # Vandermonde parameters. Every maximal sphere face has an invertible
    # parameter submatrix because its vertex labels are distinct mod p.
    for m in lower:
        for power in range(r):
            row={}
            for v in range(n):
                mv=tuple(sorted(m+(v,)))
                if mv in idx:row[idx[mv]]=pow(v+1,power,p)
            rows.append(row)
    rank=rank_mod(rows,p)
    return dict(monomials=len(top),relations_rank=rank,dimension=len(top)-rank)


def flores_cycle(d):
    vertices=range(2*d+3)
    ds=list(it.combinations(vertices,d+1))
    boundary=Counter()
    cells=0
    crossings=0
    for i,a in enumerate(ds):
        for b in ds[i+1:]:
            if set(a)&set(b):continue
            cells+=1
            for j in range(d+1):
                boundary[(a[:j]+a[j+1:],b)]^=1
                boundary[(b[:j]+b[j+1:],a)]^=1
            union=sorted(a+b)
            # Exact oriented-matroid criterion for two disjoint d-simplices
            # on the moment curve in R^(2d): their vertices alternate.
            if tuple(union[::2])==a or tuple(union[::2])==b:
                crossings+=1
    assert not any(boundary.values())
    assert crossings==2*d+3 and crossings%2==1
    return dict(d=d,deleted_product_cells=cells,boundary_nonzero_cells=0,
                moment_curve_crossings=crossings,evaluation_mod_2=1)


def flag_control(s):
    # Barycentric vertices are nonempty faces; edges are comparable pairs.
    vertices=[frozenset(x) for x in s if x]
    cliques=0
    for a,b,c in it.combinations(vertices,3):
        if all(x<=y or y<=x for x,y in [(a,b),(a,c),(b,c)]):
            order=sorted([a,b,c],key=len)
            assert order[0]<order[1]<order[2]
            cliques+=1
    return dict(barycentric_vertices=len(vertices),triangle_cliques=cliques,
                missing_triangles=0)


def main():
    out={'scope':'Finite controls only; the universal proof is in PROOF.md.',
         'stellar_examples':[], 'quotient_controls':[], 'flores_cycles':[]}
    for d in range(1,5):
        s,k,l,record=stellar_example(d)
        out['stellar_examples'].append(record)
        out['flores_cycles'].append(flores_cycle(d))
        if d<=2:
            n=2*d+3;r=2*d+1
            sd=quotient_dimension(s,n,r,d)
            su=quotient_dimension(s,n,r,d+1)
            ld=quotient_dimension(l,n,r,d)
            lu=quotient_dimension(l,n,r,d+1)
            assert sd['dimension']==su['dimension']==ld['dimension']==record['h'][d]
            assert lu['dimension']==ld['dimension']+1
            out['quotient_controls'].append(dict(d=d,field_prime=101,
               source_degree_d=sd,source_degree_d_plus_one=su,
               augmented_degree_d=ld,augmented_degree_d_plus_one=lu))
        if d==2:out['flag_control']=flag_control(s)
    out['metastable_inequality']=[dict(d=d,lhs=4*d,rhs=3*d+3,
        applies=4*d>=3*d+3) for d in range(1,9)]
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
