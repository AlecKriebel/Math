#!/usr/bin/env python3
"""Exact controls for OWR-1188-004. No network or source documents needed.
Standard library only. This verifies finite certificates, not Galois descent.
"""
from fractions import Fraction as F
from itertools import permutations, combinations
from pathlib import Path
import json

class G:
    __slots__=('r','s')
    def __init__(self,r=0,s=0):
        if isinstance(r,G): self.r,self.s=r.r,r.s
        else:self.r,self.s=F(r),F(s)
    def __add__(self,o):
        o=G(o);return G(self.r+o.r,self.s+o.s)
    __radd__=__add__
    def __neg__(self):return G(-self.r,-self.s)
    def __sub__(self,o):return self+-G(o)
    def __rsub__(self,o):return G(o)+-self
    def __mul__(self,o):
        o=G(o);return G(self.r*o.r-self.s*o.s,self.r*o.s+self.s*o.r)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=G(o);d=o.r*o.r+o.s*o.s
        return G((self.r*o.r+self.s*o.s)/d,(self.s*o.r-self.r*o.s)/d)
    def __rtruediv__(self,o):return G(o)/self
    def __pow__(self,n):
        if n<0:return (1/self)**-n
        v=G(1)
        for _ in range(n):v=v*self
        return v
    def __eq__(self,o):
        o=G(o);return self.r==o.r and self.s==o.s
    def __hash__(self):return hash((self.r,self.s))
    def conjugate(self):return G(self.r,-self.s)
    def serial(self):return [str(self.r),str(self.s)]

COUNT=0
def ck(v):
    global COUNT
    COUNT+=1
    assert v, f'assertion {COUNT} failed'

def point(x):return (G(1),G(0)) if x is None else (G(x),G(1))
def norm(p):return point(None) if p[1]==0 else point(p[0]/p[1])
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def matmul(a,b):return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(2)),G(0)) for j in range(2)) for i in range(2))
def act(m,p):return norm(tuple(sum((m[i][j]*p[j] for j in range(2)),G(0)) for i in range(2)))
def triple_matrix(t):
    a,b,c=t
    # Columns beta*b and alpha*a take 0,infinity,1 to a,b,c.
    beta=cross(a,c);alpha=-cross(b,c)
    return ((beta*b[0],alpha*a[0]),(beta*b[1],alpha*a[1]))
def projmat(m):
    flat=sum(m,());v=next(x for x in flat if x!=0)
    return tuple(x/v for x in flat)

def autos(points):
    found=[]
    for perm in permutations(range(len(points)),3):
        m=triple_matrix([points[j] for j in perm])
        ck(m[0][0]*m[1][1]-m[0][1]*m[1][0]!=0)
        for j in range(3):ck(act(m,points[j])==points[perm[j]])
        images=[act(m,p) for p in points]
        if set(images)==set(points):found.append([points.index(p) for p in images])
    return found

def invariant4(ps):
    a,b,c,d=ps
    lam=cross(a,c)*cross(b,d)/(cross(a,d)*cross(b,c))
    ck(lam!=0 and lam!=1)
    return 256*(lam*lam-lam+1)**3/(lam*lam*(lam-1)**2)

def main():
    a=G(2,2); b=-1/a.conjugate()
    ps=[point(0),point(None),point(1),point(-1),point(a),point(b)]
    ck(len(set(ps))==6);ck(b==G(F(-1,4),F(-1,4)))
    good=autos(ps);ck(good==[list(range(6))])
    rows=[]
    for ids in combinations(range(6),4):
        v=invariant4([ps[j] for j in ids])
        # Full permutation independence, using all 24 arrangements.
        for q in permutations(ids):ck(invariant4([ps[j] for j in q])==v)
        rows.append({'subset':list(ids),'J':v.serial()})
    ck(len({tuple(r['J']) for r in rows})==15)
    A=((G(0),G(-1)),(G(1),G(0)))
    anti=[ps.index(act(A,tuple(x.conjugate() for x in p))) for p in ps]
    ck(anti==[1,0,3,2,5,4]);ck(projmat(matmul(A,A))==projmat(((G(1),G(0)),(G(0),G(1)))))
    # Negative control: the superficially similar candidate a=2+i has extra symmetry.
    olda=G(2,1);oldps=ps[:4]+[point(olda),point(-1/olda.conjugate())]
    oldautos=autos(oldps);ck(len(oldautos)==2)
    # Elliptic translation matrices for several distinct root triples.
    # The generic symbolic identities are checked separately by verify_symbolic.py.
    triples=[(G(0),G(1),G(3)),(G(1),G(2),G(5)),(G(0),G(0,1),G(2,3)),(G(-2),G(4,1),G(4,-1))]
    elliptic_checks=0
    for roots in triples:
        mats=[]
        for j,e in enumerate(roots):
            u,v=[roots[t] for t in range(3) if t!=j]
            M=((e,u*v-e*(u+v)),(G(1),-e));mats.append(M)
            d=(e-u)*(e-v)
            ck(M[0][0]*M[1][1]-M[0][1]*M[1][0]==-d)
            ck(matmul(M,M)==((d,G(0)),(G(0),d)));elliptic_checks+=2
        for j,l in permutations(range(3),2):
            other=3-j-l
            ck(projmat(matmul(mats[j],mats[l]))==projmat(mats[other]));elliptic_checks+=1
        ck(len({projmat(M) for M in mats})==3)
    report={'status':'pass','arithmetic':'fractions in Q(i), exact','assertions':COUNT,
            'mobius_candidates_per_configuration':120,'sharp_example_automorphisms':good,
            'rejected_example_automorphisms':oldautos,'four_subset_J_values':rows,
            'antipodal_permutation':anti,'elliptic_matrix_assertions':elliptic_checks,
            'limits':'Finite certificates only; classification, Hilbert 90, conic descent and universal cocycle arguments are proved or cited in PROOF.md.'}
    target=Path(__file__).with_name('CONTROL_RESULTS.json')
    if target.exists():assert json.loads(target.read_text())==report, 'Saved certificate differs'
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':main()
