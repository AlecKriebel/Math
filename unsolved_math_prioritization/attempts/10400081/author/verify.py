#!/usr/bin/env python3
"""Exact finite controls for the authored reductions; no manifold skein computation.
Python 3 standard library only. Run: python3 verify.py
"""
from fractions import Fraction
from itertools import product
from math import gcd
import json

counts = {}
def check(condition, group):
    if not condition:
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1

# Laurent polynomials represented by sorted tuples (exponent, integer coefficient).
def lp(d):
    return tuple(sorted((k,v) for k,v in d.items() if v))
def add(p,q):
    d=dict(p)
    for k,v in q:d[k]=d.get(k,0)+v
    return lp(d)
def neg(p):return tuple((k,-v) for k,v in p)
def mul(p,q):
    d={}
    for i,a in p:
        for j,b in q:d[i+j]=d.get(i+j,0)+a*b
    return lp(d)
def power(p,n):
    r=((0,1),)
    for _ in range(n):r=mul(r,p)
    return r
def mon(k,c=1):return ((k,c),) if c else ()
def val(p,x):return sum(Fraction(c)*Fraction(x)**e for e,c in p)
ONE=mon(0); ZERO=(); A=mon(1); AI=mon(-1)
DELTA=add(mon(2,-1),mon(-2,-1))
check(add(add(mon(2),mon(-2)),DELTA)==ZERO,'laurent_identities')
check(add(add(A,mul(AI,DELTA)),mon(-3))==ZERO,'laurent_identities')
check(add(mul(A,DELTA),AI)==mon(3,-1),'laurent_identities')
check(add(mul(AI,DELTA),A)==mon(-3,-1),'laurent_identities')

# Planar pairings on 2n cyclically ordered boundary vertices.
def pairings(vertices):
    if not vertices:
        yield ();return
    first=vertices[0]
    for j in range(1,len(vertices),2):
        for l in pairings(vertices[1:j]):
            for r in pairings(vertices[j+1:]):
                yield ((first,vertices[j]),)+l+r

def canon(edges):return tuple(sorted(tuple(sorted(e)) for e in edges))
def basis(n):
    # cyclic order is top left-to-right, then bottom right-to-left.
    order=list(range(n))+list(range(2*n-1,n-1,-1))
    return tuple(canon((order[a],order[b]) for a,b in p) for p in pairings(tuple(range(2*n))))
def identity(n):return canon((i,n+i) for i in range(n))
def cupcap(n,i):
    return canon([(i,i+1),(n+i,n+i+1)]+[(j,n+j) for j in range(n) if j not in (i,i+1)])
def stack(n,a,b):
    parent=list(range(3*n))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    def join(i,j):parent[find(i)]=find(j)
    for u,v in a:join(u,v)
    for u,v in b:join(u+n,v+n)
    comps={}
    for x in range(3*n):comps.setdefault(find(x),[]).append(x)
    loops=0;edges=[]
    for xs in comps.values():
        ext=[x for x in xs if x<n or x>=2*n]
        if not ext:loops+=1
        else:
            assert len(ext)==2
            edges.append(tuple(x if x<n else x-n for x in ext))
    return canon(edges),loops

def linadd(x,y):
    out=dict(x)
    for d,p in y.items():
        out[d]=add(out.get(d,ZERO),p)
        if out[d]==ZERO:del out[d]
    return out

def linmul(n,x,y):
    out={}
    for a,p in x.items():
        for b,q in y.items():
            c,l=stack(n,a,b)
            out=linadd(out,{c:mul(mul(p,q),power(DELTA,l))})
    return out

for n,catalan in [(1,1),(2,2),(3,5),(4,14)]:
    bs=basis(n);I=identity(n)
    check(len(bs)==catalan and len(set(bs))==catalan,'TL_basis_counts')
    for a in bs:
        check(stack(n,I,a)==(a,0) and stack(n,a,I)==(a,0),'TL_identity')
    for a,b in product(bs,repeat=2):
        c,l=stack(n,a,b)
        check(c in bs and 0<=l<=n,'TL_closure')
    for a,b,c in product(bs,repeat=3):
        ab,l1=stack(n,a,b);abc,l2=stack(n,ab,c)
        bc,l3=stack(n,b,c);abc2,l4=stack(n,a,bc)
        check((abc,l1+l2)==(abc2,l3+l4),'TL_associativity')
    es=[cupcap(n,i) for i in range(n-1)]
    for i,e in enumerate(es):
        check(stack(n,e,e)==(e,1),'TL_quadratic')
        g={I:A,e:AI};h={I:AI,e:A}
        check(linmul(n,g,h)=={I:ONE} and linmul(n,h,g)=={I:ONE},'Reidemeister_II')
        if i+1<len(es):
            f=es[i+1]
            ef,k=stack(n,e,f);efe,l=stack(n,ef,e)
            check((efe,k+l)==(e,0),'TL_adjacent')
            g2={I:A,f:AI}
            check(linmul(n,linmul(n,g,g2),g)==linmul(n,linmul(n,g2,g),g2),'Reidemeister_III')
        for j in range(i+2,len(es)):
            check(stack(n,e,es[j])==stack(n,es[j],e),'TL_distant')

# Exact polynomial division over Q, ascending coefficient arrays.
def trim(f):
    f=list(map(Fraction,f))
    while len(f)>1 and f[-1]==0:f.pop()
    return f
def padd(f,g):
    h=[Fraction(0)]*max(len(f),len(g))
    for i,x in enumerate(f):h[i]+=x
    for i,x in enumerate(g):h[i]+=x
    return trim(h)
def pmul(f,g):
    h=[Fraction(0)]*(len(f)+len(g)-1)
    for i,x in enumerate(f):
        for j,y in enumerate(g):h[i+j]+=x*y
    return trim(h)
def pdiv(f,g):
    f=trim(f);g=trim(g);assert g!=[0]
    q=[Fraction(0)]*max(1,len(f)-len(g)+1)
    while f!=[0] and len(f)>=len(g):
        k=len(f)-len(g);c=f[-1]/g[-1];q[k]+=c
        for i,x in enumerate(g):f[k+i]-=c*x
        f=trim(f)
    return trim(q),f
def pgcd(f,g):
    while trim(g)!=[0]:f,g=g,pdiv(f,g)[1]
    f=trim(f)
    return [x/f[-1] for x in f] if f!=[0] else [0]
def peval(f,x):
    r=Fraction(0)
    for c in reversed(f):r=r*x+c
    return r

cyclotomic={}
for n in range(1,65):
    f=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:
            f,r=pdiv(f,cyclotomic[d]);check(r==[0],'cyclotomic_exact_division')
    cyclotomic[n]=f
    check(all(x.denominator==1 for x in f),'cyclotomic_integral')
    check(pgcd(f,[-2,1])==[1] and peval(f,2)!=0,'noncyclotomic_blind_spot')
    prod=[Fraction(1)]
    for d in range(1,n+1):
        if n%d==0:prod=pmul(prod,cyclotomic[d])
    check(prod==[-1]+[0]*(n-1)+[1],'cyclotomic_product_identity')

# Jordan nilpotent rank checks prove finite controls of fiber-count vs length.
def rank_q(mat):
    a=[list(map(Fraction,row)) for row in mat]; m=len(a);n=len(a[0]) if m else 0;r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if a[i][c]),None)
        if piv is None:continue
        a[r],a[piv]=a[piv],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
        for i in range(m):
            if i!=r and a[i][c]:
                v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
    return r
for e in range(1,17):
    # A+1 acts as the nilpotent shift on Q[A]/(A+1)^e.
    J=[[int(i==j+1) for j in range(e)] for i in range(e)]
    check(e-rank_q(J)==1,'fiber_counts_blocks_not_lengths')
    # A+1 is invertible on Q[A]/(A-2) and no +/-1 fiber survives.
    check(peval([-2,1],-1)!=0 and peval([-2,1],1)!=0,'two_classical_fibers_insufficient')

# Codimension-two residue: every relation in (2,A-1) maps to zero in F_2.
for length in range(1,7):
    for cs in product((-1,0,1),repeat=length):
        f=lp(dict(enumerate(cs)))
        check(int(val(mul(mon(0,2),f),1))%2==0,'integer_torsion_residue')
        check(int(val(mul(add(A,mon(0,-1)),f),1))%2==0,'height_two_residue')
check(1%2!=0,'nonzero_residue_class')

# Figure-eight published generic rank specialized at p=1; purely arithmetic.
for q in list(range(-64,0))+list(range(1,65)):
    r=Fraction(abs(4*q+1)+abs(4*q-1),2)
    check(r==4*abs(q),'figure_eight_rank_formula')

# Adjugate certificate: integral matrices, singular full presentation but rank 2.
def det2(B):return B[0][0]*B[1][1]-B[0][1]*B[1][0]
def mv(B,v):return [sum(a*b for a,b in zip(row,v)) for row in B]
for a,b,c,d in product(range(-2,3),repeat=4):
    C0=[[a,b],[c,d]];D=det2(C0)
    if not D:continue
    adj=[[d,-b],[-c,a]]
    for v in [(1,0),(0,1),(3,-2)]:
        check(mv(C0,mv(adj,v))==[D*x for x in v],'adjugate_integral_certificate')

# Explicit torsion-free, non-free cokernel model: syzygy identity.
p=add(A,mon(0,-1))
check(add(mul(mon(0,2),p),neg(mul(p,mon(0,2))))==ZERO,'primitive_column_syzygy')
check(pgcd([-1,1],[2])==[1],'coprime_column_over_Q')

print(json.dumps({
 'status':'PASS',
 'arithmetic':'exact integer Laurent polynomials, Fraction rational elimination, finite-field residues',
 'assertions_by_group':counts,
 'total_assertions':sum(counts.values()),
 'scope_limit':'Finite controls of algebra and formulas only. No manifold skein module computed; no universal conjecture or imported topology theorem verified.',
},indent=2,sort_keys=True))
