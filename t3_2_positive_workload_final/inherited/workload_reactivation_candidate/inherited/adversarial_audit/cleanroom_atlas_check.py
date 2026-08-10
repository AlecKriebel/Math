#!/usr/bin/env python3
"""Clean-room exact replay of the T3-2 two-active workload atlas.

This script imports no code from the submitted package.
"""
from itertools import product, permutations
from fractions import Fraction
from collections import defaultdict

NAMES = ["0","A","B","C","2A","2B","2C","AB","AC","BC"]
VECS = [(0,0,0),(1,0,0),(0,1,0),(0,0,1),(2,0,0),(0,2,0),(0,0,2),(1,1,0),(1,0,1),(0,1,1)]
WORKLOADS = [(1,1,0),(2,3,0),(1,2,0),(1,3,0)]

def dot(a,b): return sum(x*y for x,y in zip(a,b))

def rref(rows):
    A=[list(map(Fraction,r)) for r in rows if any(r)]
    m=len(A); rr=0
    for c in range(3):
        p=next((i for i in range(rr,m) if A[i][c]),None)
        if p is None: continue
        A[rr],A[p]=A[p],A[rr]
        z=A[rr][c]; A[rr]=[x/z for x in A[rr]]
        for i in range(m):
            if i!=rr and A[i][c]:
                z=A[i][c]; A[i]=[A[i][j]-z*A[rr][j] for j in range(3)]
        rr+=1
    return A[:rr]

def rank(rows): return len(rref(rows))

def block_rows(block):
    ids=sorted(block); root=VECS[ids[0]]
    return [tuple(VECS[i][j]-root[j] for j in range(3)) for i in ids[1:]]

def positive_active_null(rows):
    R=rref(rows)
    if len(R)==3: return None
    for qa in range(1,9):
        for qb in range(1,9):
            qc=None; ok=True
            for a,b,c in R:
                rhs=-(a*qa+b*qb)
                if c:
                    val=rhs/c
                    if qc is None: qc=val
                    elif qc!=val: ok=False; break
                elif rhs!=0:
                    ok=False; break
            if ok:
                qc=Fraction(0) if qc is None else qc
                q=(Fraction(qa),Fraction(qb),qc)
                if all(sum(row[j]*q[j] for j in range(3))==0 for row in R):
                    return q
    return None

def top_kind(block,h):
    values={i:dot(h,VECS[i]) for i in block}; mx=max(values.values())
    top={i for i,v in values.items() if v==mx}
    if len(top)==len(block): return "shielded"
    if any(VECS[i][0]+VECS[i][1]>=2 for i in top): return "available"
    K={j for i in top for j in (0,1) if VECS[i][j]}
    if all(sum(VECS[i][j] for j in K)==1 for i in block): return "shielded"
    if any(sum(VECS[i])==1 for i in top): return "available"
    has_service=any(VECS[i][2] for i in top)
    if has_service and any(VECS[i][2] for i in block-top): return "available"
    return "shielded"

def perm_block(block,p):
    out=set()
    for idx in block:
        z=[0,0,0]
        for i in range(3): z[p[i]]=VECS[idx][i]
        out.add(VECS.index(tuple(z)))
    return frozenset(out)

S1={frozenset([3,6]),frozenset([0,1,4,9])}
S2={frozenset([0,3,6]),frozenset([1,4,9])}

def service(block1,block2):
    for p in permutations(range(3)):
        pair={perm_block(block1,p),perm_block(block2,p)}
        if pair==S1 or pair==S2: return True
    return False

def main():
    counts=defaultdict(int); bad=[]
    for h in WORKLOADS:
        for assignment in product(range(3), repeat=10):
            b1=frozenset(i for i,a in enumerate(assignment) if a==1)
            b2=frozenset(i for i,a in enumerate(assignment) if a==2)
            if len(b1)<2 or len(b2)<2: continue
            counts['assignments']+=1
            if top_kind(b1,h)!="shielded" or top_kind(b2,h)!="shielded": continue
            counts['shielded']+=1
            rows=block_rows(b1)+block_rows(b2)
            if positive_active_null(rows) is not None:
                counts['common_invariant']+=1; continue
            deficiency=len(b1)+len(b2)-2-rank(rows)
            counts[f'deficiency_{deficiency}']+=1
            if deficiency==0: counts['deficiency_zero']+=1
            elif deficiency==1 and service(b1,b2): counts['service']+=1
            else: bad.append((h,b1,b2,deficiency))
    expected={
        'assignments':187488,'shielded':446,'common_invariant':382,
        'deficiency_0':60,'deficiency_zero':60,'deficiency_1':4,'service':4,
    }
    got=dict(counts)
    assert not bad, bad[:3]
    for k,v in expected.items(): assert got.get(k)==v,(k,got.get(k),v)
    print('CLEANROOM ATLAS CHECK PASSED')
    print(got)

if __name__=='__main__': main()
