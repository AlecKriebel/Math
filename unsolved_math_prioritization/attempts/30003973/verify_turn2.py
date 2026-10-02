#!/usr/bin/env python3
"""Exact independence-system controls; no graph equivalence claimed."""
import json
from collections import defaultdict
counts={}
def ck(x,k):
    assert x,k
    counts[k]=counts.get(k,0)+1

def down(s):
    F=0;t=s
    while True:
        F|=1<<t
        if t==0:return F
        t=(t-1)&s

def family(mm):
    F=0
    for s in mm:F|=down(s)
    return F

def maxima(F,m):
    return [s for s in range(1<<m) if F>>s&1 and not any(F>>(s|1<<i)&1 for i in range(m) if not(s>>i&1))]

def product(A,B,m):
    # Direct all-member definition, intentionally independent of maximal-only code.
    out=0
    for a in range(1<<m):
        if A>>a&1:
            for b in range(1<<m):
                if B>>b&1:out|=1<<(a|b)
    return out

A=family([2,9,17,28]);B=family([1,10,18,28]);D=family([11,19,29,30]);full=(1<<32)-1
ck(product(A,A,5)==D,'explicit_A_square')
ck(product(B,B,5)==D,'explicit_B_square')
ck(A>>9&1 and B>>18&1,'explicit_cross_members')
ck(not D>>(9|18)&1,'explicit_cross_escape')
ck(product(A,B,5)&~D!=0,'mixed_condition_not_automatic')
ck(product(A,D,5)==full,'explicit_A_cube_full')
ck(product(B,D,5)==full,'explicit_B_cube_full')
for F in [A,B,D]:
    for s in range(32):
        if F>>s&1:ck(F&down(s)==down(s),'explicit_downward_closure')

# Exhaust all ideals by lower/upper slices, not by sampling antichains.
def ideals(m):
    if m==0:return [0,1]
    lower=ideals(m-1);shift=1<<(m-1)
    return [a|(b<<shift) for a in lower for b in lower if b&a==b]

rows=[]
for m in range(1,6):
    sub=[down(s) for s in range(1<<m)]
    # Maximal-element multiplication is checked separately against direct products.
    def fast(F,G):
        out=0
        for a in maxima(F,m):
            for b in maxima(G,m):out|=sub[a|b]
        return out
    seen={};families=0;unrestricted=ideals(m)
    ck(len(unrestricted)==[0,3,6,20,168,7581][m],'Dedekind_count')
    for F in unrestricted:
        if not all(F>>(1<<i)&1 for i in range(m)):continue
        families+=1;sq=fast(F,F);cube=fast(F,sq)
        ck(sq==product(F,F,m),'fast_square_matches_direct')
        ck(cube==product(F,sq,m),'fast_cube_matches_direct')
        if sq in seen:ck(cube==seen[sq],'same_square_same_cube_bounded')
        else:seen[sq]=cube
    rows.append({'ground_set_size':m,'all_downward_families':len(unrestricted),'singleton_complete_families':families,'distinct_squares':len(seen)})
ck(sum(r['singleton_complete_families'] for r in rows)==7020,'family_total')
# Verify the conditional transfer on all equal-square pairs at m<=4.
checked=0
for m in range(1,5):
    groups=defaultdict(list)
    for F in ideals(m):
        if all(F>>(1<<i)&1 for i in range(m)):groups[product(F,F,m)].append(F)
    for D,gg in groups.items():
        for F in gg:
            for G in gg:
                if product(F,G,m)&~D==0:
                    ck(product(F,D,m)==product(G,D,m),'conditional_transfer_bounded');checked+=1
print(json.dumps({'problem_id':30003973,'status':'PASS','assertions':sum(counts.values()),'counts':counts,'exhaustive_rows':rows,'conditional_pairs_max_ground_size':4,'conditional_pairs':checked,'abstract_mixed_counterexample_maxima':{'A':[2,9,17,28],'B':[1,10,18,28],'common_square':[11,19,29,30]},'scope':'Exact bounded independence-system controls. The explicit example only refutes automatic mixed-product inclusion; both cubes agree. No universal graph pair or general odd-power transfer follows from this scan.'},indent=2,sort_keys=True))
