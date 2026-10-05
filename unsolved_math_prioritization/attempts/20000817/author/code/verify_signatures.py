#!/usr/bin/env python3
"""Exact finite controls for AIM Hilbert Problem 16; no external data or CAS needed."""
from collections import Counter
from itertools import combinations, combinations_with_replacement
from fractions import Fraction
from math import comb
from pathlib import Path
import json


def add(a,b): return tuple(x+y for x,y in zip(a,b))
def unit(n,i): return tuple(int(i==j) for j in range(n))
def lower_sets(n,d):
    zero=(0,)*n
    sets={frozenset()}
    counts=[1]
    for _ in range(d):
        nxt=set()
        for D in sets:
            candidates={zero} if not D else {add(a,unit(n,i)) for a in D for i in range(n)}-D
            for a in candidates:
                if all(tuple(x-int(i==j) for j,x in enumerate(a)) in D for i in range(n) if a[i]):
                    nxt.add(D|{a})
        sets=nxt; counts.append(len(sets))
    return sets,counts

def generators(D,n):
    border={add(a,unit(n,i)) for a in D for i in range(n)}-D
    return sorted(a for a in border if all(tuple(x-int(i==j) for j,x in enumerate(a)) in D for i in range(n) if a[i]))

def tangent_nullity(D,n):
    # Taylor pair syzygies generate the first syzygy module for a monomial ideal.
    B=sorted(D); inds={a:i for i,a in enumerate(B)}; G=generators(D,n)
    rows=[]
    for i,j in combinations(range(len(G)),2):
        lcm=tuple(max(a,b) for a,b in zip(G[i],G[j]))
        multipliers=[tuple(a-b for a,b in zip(lcm,G[k])) for k in (i,j)]
        block=[{} for _ in B]
        for k,m,s in ((i,multipliers[0],1),(j,multipliers[1],-1)):
            for h,b in enumerate(B):
                out=add(m,b)
                if out in inds:
                    row=block[inds[out]]; col=k*len(B)+h
                    row[col]=row.get(col,0)+s
        rows.extend({k:Fraction(v) for k,v in row.items() if v} for row in block if row)
    piv={}
    for row in rows:
        while row:
            p=min(row)
            if p not in piv:
                c=row[p]; piv[p]={j:v/c for j,v in row.items()}; break
            c=row[p]
            for j,v in piv[p].items():
                row[j]=row.get(j,Fraction(0))-c*v
                if not row[j]: del row[j]
    return {'generators':len(G),'unknowns':len(G)*len(B),'rank':len(piv),'dimension':len(G)*len(B)-len(piv)}

def polynomial_mul(A,B):
    C={}
    for a,x in A.items():
        for b,y in B.items(): C[a+b]=C.get(a+b,0)+x*y
    return {a:x for a,x in C.items() if x}

def check_flat_model(e,Q):
    # Basis: unit, e linear-coordinate labels, q quadratic labels (total 8).
    q=7-e; assert len(Q)==q
    used=set(v for a in Q for v in a)
    V=sorted(used)
    V += [i for i in range(e) if i not in V][:4-len(V)]
    V=sorted(V); W=sorted(set(range(e))-set(V))
    R=[a for a in combinations_with_replacement(V,2) if a not in Q][:e-4]
    table={}
    for i in range(8): table[0,i]=table[i,0]={i:{0:1}}
    for j,a in enumerate(Q):
        x,y=(a[0]+1,a[1]+1); table[x,y]=table[y,x]={1+e+j:{0:1}}
    for w,a in zip(W,R):
        x,y=(a[0]+1,a[1]+1); table[x,y]=table[y,x]={1+w:{1:1}}
    def mult(A,B):
        out={}
        for a,ca in A.items():
            for b,cb in B.items():
                for c,cc in table.get((a,b),{}).items():
                    prod=polynomial_mul(polynomial_mul(ca,cb),cc)
                    for power,v in prod.items(): out.setdefault(c,{})[power]=out.setdefault(c,{}).get(power,0)+v
        return {i:{p:v for p,v in c.items() if v} for i,c in out.items() if any(c.values())}
    basis=[{i:{0:1}} for i in range(8)]
    for a in basis:
        for b in basis:
            for c in basis: assert mult(mult(a,b),c)==mult(a,mult(b,c))
    # Rank m^2 is q at t=0 and 3 over k(t); the output basis labels are distinct.
    assert len(Q)+len(R)==3
    assert len(set([1+e+j for j in range(q)]+[1+w for w in W]))==3
    assert all(set(a)<=set(V) for a in Q+tuple(R))
    return {'e':e,'q':q,'core':V,'promoted_pairs':R}


def main():
    totals=[]
    for n in range(1,8):
        Ds,counts=lower_sets(n,8)
        found=sum(max(map(sum,D))<=2 and sum(sum(a)==1 for a in D)>=4 for D in Ds)
        formula=sum(comb(n,e)*comb(e*(e+1)//2,7-e) for e in range(4,min(7,n)+1))
        assert found==formula
        totals.append({'ambient_dimension':n,'lower_set_counts_lengths_0_to_8':counts,'all_colength8_monomial_ideals':len(Ds),'nonsmoothable_component_signature':found})
    controls=0
    for e in range(4,8):
        for Q in combinations(tuple(combinations_with_replacement(range(e),2)),7-e):
            check_flat_model(e,Q); controls+=1
    D4={tuple(a) for a in [(0,0,0,0),(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0),(0,1,0,1),(0,0,1,1)]}
    collision=tangent_nullity(D4,4); assert collision['dimension']==33
    anchor={ (i,0,0,0) for i in range(8)}
    anchor_result=tangent_nullity(anchor,4); assert anchor_result['dimension']==32
    # Published collision ideal is obtained by swapping variables 2 and 4.
    published={tuple(a[i] for i in (0,3,2,1)) for a in D4}
    pub_result=tangent_nullity(published,4); assert pub_result['dimension']==33
    # A separate projective control: saturated intersection of disjoint curves.
    projective_gens=[(0,1,0,1),(0,0,1,1),(2,1,0,0),(2,0,1,0)]
    hvals={}
    for d in range(2,13):
        monomials=[(a,b,c,d-a-b-c) for a in range(d+1) for b in range(d-a+1) for c in range(d-a-b+1)]
        h=sum(not any(all(x>=y for x,y in zip(m,g)) for g in projective_gens) for m in monomials)
        assert h==3*d+2; hvals[d]=h
    D0={(0,)*4}|{unit(4,i) for i in range(4)}
    quadrics=[add(unit(4,i),unit(4,j)) for i,j in combinations_with_replacement(range(4),2)]
    tangent_histogram=Counter(tangent_nullity(D0|set(Q),4)['dimension'] for Q in combinations(quadrics,3))
    assert sum(tangent_histogram.values())==120 and min(tangent_histogram)==33
    out={'status':'PASS','arithmetic':'integer polynomial identities and rational Gaussian elimination','enumeration':totals,'flat_models_checked':controls,'associativity_checks_per_model':512,'collision_tangent':collision,'published_collision_tangent':pub_result,'anchor_tangent':anchor_result,'all_120_h143_tangent_dimensions':dict(sorted(tangent_histogram.items())),'projective_separating_ideal_hilbert_values':hvals,'limitations':['Finite controls do not prove component classification; the proof depends on CEVV Theorem 1.1.','Rational tangent ranks do not alone establish arbitrary-characteristic ranks.']}
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
