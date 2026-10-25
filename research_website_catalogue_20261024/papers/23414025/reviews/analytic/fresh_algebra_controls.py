#!/usr/bin/env python3
"""Fresh exact controls; no imports from the submitted checker.

Derivation-space linear systems and polynomial SL2 determinant identities are
distinct from testing the published list of post-Lie products at group points.
These do not certify the global integration/topology argument.
"""
from fractions import Fraction as Q
from itertools import permutations, product
from pathlib import Path
import hashlib,json

def need(p,s):
    if not p: raise RuntimeError(s)

def rank(rows):
    a=[list(map(Q,row)) for row in rows];r=0
    if not a:return 0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r]
        t=a[r][c];a[r]=[x/t for x in a[r]]
        for i in range(r+1,len(a)):
            if a[i][c]:
                t=a[i][c];a[i]=[x-t*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def matunit(n,i,j):return [[int((k,l)==(i,j)) for l in range(n)] for k in range(n)]

def sl(n):
    off=[(i,j) for i in range(n) for j in range(n) if i!=j]
    mats=[matunit(n,i,j) for i,j in off]
    mats += [sub(matunit(n,i,i),matunit(n,i+1,i+1)) for i in range(n-1)]
    def coords(a):return [a[i][j] for i,j in off]+[sum(a[j][j] for j in range(i+1)) for i in range(n-1)]
    return [[coords(sub(mm(a,b),mm(b,a))) for b in mats] for a in mats]

def bracket(c,x,y):
    n=len(c);return [sum(x[i]*y[j]*c[i][j][k] for i in range(n) for j in range(n)) for k in range(n)]

def analyze(name,c,derivations=False):
    n=len(c);unit=[[int(i==j) for j in range(n)] for i in range(n)]
    for i,j,k in product(range(n),repeat=3):
        a=bracket(c,unit[i],c[j][k]);b=bracket(c,unit[j],c[k][i]);d=bracket(c,unit[k],c[i][j])
        need(all(x+y+z==0 for x,y,z in zip(a,b,d)),name+' Jacobi')
    ad=[[[c[i][j][k] for j in range(n)] for k in range(n)] for i in range(n)]
    traces=[sum(a[i][i] for i in range(n)) for a in ad]
    killing=[[sum(a[i][j]*b[j][i] for i in range(n) for j in range(n)) for b in ad] for a in ad]
    result=dict(dimension=n,jacobi_triples=n**3,derived_rank=rank([c[i][j] for i,j in product(range(n),repeat=2)]),adjoint_traces=traces,killing_rank=rank(killing),inner_derivation_dimension=rank([sum(a,[]) for a in ad]))
    if derivations:
        equations=[]
        for i,j,k in product(range(n),repeat=3):
            row=[0]*(n*n)
            for t in range(n):
                row[k*n+t]+=c[i][j][t]
                row[t*n+i]-=c[t][j][k]
                row[t*n+j]-=c[i][t][k]
            equations.append(row)
        result['derivation_dimension']=n*n-rank(equations)
        result['derivation_equations']=len(equations)
    return result

# Tiny polynomial ring Z[a,b,c,d] for exact, all-parameter identities.
class P:
    def __init__(self,d=0):self.d={k:v for k,v in (d if isinstance(d,dict) else {(0,0,0,0):d}).items() if v}
    def __add__(self,o):
        o=o if isinstance(o,P) else P(o);d=self.d.copy()
        for k,v in o.d.items():d[k]=d.get(k,0)+v
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.d.items()})
    def __sub__(self,o):return self+-o if isinstance(o,P) else self+(-o)
    def __rsub__(self,o):return P(o)+-self
    def __mul__(self,o):
        o=o if isinstance(o,P) else P(o);d={}
        for k,v in self.d.items():
            for l,w in o.d.items():
                m=tuple(x+y for x,y in zip(k,l));d[m]=d.get(m,0)+v*w
        return P(d)
    __rmul__=__mul__
    def __eq__(self,o):return self.d==(o.d if isinstance(o,P) else P(o).d)

def det(a):
    n=len(a);s=P()
    for perm in permutations(range(n)):
        inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=P((-1)**inversions)
        for i,j in enumerate(perm):term=term*a[i][j]
        s=s+term
    return s

def main():
    result={}
    for n in (2,3):
        r=analyze('sl'+str(n),sl(n),True)
        need(r['derived_rank']==n*n-1 and r['killing_rank']==n*n-1,'semisimple rank')
        need(r['derivation_dimension']==r['inner_derivation_dimension']==n*n-1,'all derivations inner')
        need(not any(r['adjoint_traces']),'semisimple unimodular')
        result['sl'+str(n)]=r
    # sl2 in basis H,E,F, acting on Sym^4(C^2), dimension 5.
    n=8;c=[[[0]*n for _ in range(n)] for _ in range(n)]
    def setc(i,j,k,v):c[i][j][k]=v;c[j][i][k]=-v
    setc(0,1,1,2);setc(0,2,2,-2);setc(1,2,0,1)
    for i in range(5):
        setc(0,3+i,3+i,4-2*i)
        if i>0:setc(1,3+i,3+i-1,i)
        if i<4:setc(2,3+i,3+i+1,4-i)
    r=analyze('sl2 semidirect Sym4',c)
    need(r['derived_rank']==8 and not any(r['adjoint_traces']),'perfect nonsemisimple source')
    need(r['killing_rank']==3 and all(not any(c[i][j]) for i in range(3,8) for j in range(3,8)),'nonzero abelian radical boundary')
    r['explicit_abelian_radical_dimension']=5;result['perfect_nonsemisimple_dimension8']=r
    # The displayed nonunimodular example has actual homomorphisms, not just
    # independent matrices with an invertible difference.
    c=[[[0]*3 for _ in range(3)] for _ in range(3)]
    c[0][1][1]=2;c[1][0][1]=-2
    result['remark4_source']=analyze('affine plus center',c)
    need(result['remark4_source']['adjoint_traces']==[2,0,0],'essential source trace')
    target=[[[0]*3 for _ in range(3)] for _ in range(3)]
    for i,j,k,v in [(0,1,1,2),(0,2,2,-2),(1,2,0,1)]:
        target[i][j][k]=v;target[j][i][k]=-v
    unit=[[int(i==j) for j in range(3)] for i in range(3)]
    j1=lambda x:[x[0],x[1],0]
    j2=lambda x:[0,0,x[2]]
    for i,j in product(range(3),repeat=2):
        need(j1(c[i][j])==bracket(target,j1(unit[i]),j1(unit[j])),'Remark4 j1 homomorphism')
        need(j2(c[i][j])==bracket(target,j2(unit[i]),j2(unit[j])),'Remark4 j2 homomorphism')
    need(rank([[x-y for x,y in zip(j1(e),j2(e))] for e in unit])==3,'Remark4 transverse difference')
    result['remark4_source']['homomorphism_basis_pairs']=18
    result['remark4_source']['difference_rank']=3
    # Polynomial conjugation by adj(p), with det(p) left symbolic.
    a,b,cvar,d=[P({tuple(int(i==j) for i in range(4)):1}) for j in range(4)]
    p=[[a,b],[cvar,d]];adj=[[d,-b],[-cvar,a]];delta=a*d-b*cvar
    H=[[1,0],[0,-1]];E=[[0,1],[0,0]];F=[[0,0],[1,0]]
    cols=[]
    for x in (H,E,F):
        q=mm(mm(adj,x),p);cols.append([q[0][0],q[0][1],q[1][0]])
    adp=[list(x) for x in zip(*cols)]
    need(det(adp)==delta*delta*delta,'Ad determinant polynomial')
    B=[row[:2]+[P(-int(i==2))] for i,row in enumerate(adp)]
    need(det(B)==-d*d*delta,'Remark4 determinant polynomial')
    # At det(p)=1 this is -d^2; nonzero at I, zero at Weyl element.
    result['symbolic_SL2_controls']={
        'polynomial_variables':['a','b','c','d'],
        'adjugate_conjugation_determinant':'(ad-bc)^3',
        'remark4_infinite_family_determinant':'-d^2(ad-bc), hence -d^2 on SL2',
        'negative_control':'At identity determinant -1, at [[0,-1],[1,0]] determinant 0; dropping unimodularity breaks global transitivity.'}
    result['status']='PASS'
    result['limits']='Exact finite-dimensional algebra and polynomial identities; no computational certificate for integration, transitivity, coverings, homology, or universal nonexistence.'
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name('fresh_algebra_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
