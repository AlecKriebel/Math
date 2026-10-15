#!/usr/bin/env python3
"""Exact finite controls; the all-degree and Galois arguments are in PROOF.md."""
from fractions import Fraction as F
from itertools import product, permutations, combinations
import json
count=0

def check(x):
    global count
    assert x
    count+=1

def add(*ps):
    o={}
    for p in ps:
        for a,c in p.items():o[a]=o.get(a,F(0))+c
    return {a:c for a,c in o.items() if c}
def scale(p,c):return {a:v*c for a,v in p.items() if v*c}
def mul(p,q):
    o={}
    for a,c in p.items():
        for b,d in q.items():
            k=tuple(x+y for x,y in zip(a,b));o[k]=o.get(k,F(0))+c*d
    return {a:c for a,c in o.items() if c}
def powp(p,k):
    o={(0,)*len(next(iter(p))):F(1)}
    for _ in range(k):o=mul(o,p)
    return o
def atom(a,c=1):return {tuple(a):F(c)}
def evalp(p,v):return sum(c*__import__('functools').reduce(lambda a,b:a*b,(x**i for x,i in zip(v,k)),F(1)) for k,c in p.items())
def det(A):
    A=[[F(x) for x in row] for row in A];n=len(A);out=F(1)
    for k in range(n):
        pivot=next((j for j in range(k,n) if A[j][k]),None)
        if pivot is None:return F(0)
        if pivot!=k:A[k],A[pivot]=A[pivot],A[k];out=-out
        d=A[k][k];out*=d
        for j in range(k+1,n):
            q=A[j][k]/d
            for l in range(k+1,n):A[j][l]-=q*A[k][l]
    return out

f=add(atom((4,0,0)),atom((1,3,0)),atom((0,4,0)),atom((2,1,1),-3),atom((1,2,1),-4),atom((2,0,2),2),atom((1,0,3)),atom((0,1,3)),atom((0,0,4)))
one=atom((0,0,0));p=add(one,f);g=add(one,atom((2,0,0),-1),atom((0,2,0),-1),atom((0,0,2),-1))
indices=[a for a in product(range(5),repeat=3) if sum(a)<=4]
m={a:F(int(a==(0,0,0))-int(a==(4,0,0))) for a in indices}
check(len(indices)==35);check(sum(p.get(a,0)*m[a] for a in indices)==0);check(m[(0,0,0)]==1);check(m[(4,0,0)]==-1)
q=add(one,atom((4,0,0)));check(sum(q.get(a,0)*m[a] for a in indices)==0);check(add(q,scale(one,-1))==powp(atom((2,0,0)),2))
check(g[(0,0,0)]==1);check(f.get((0,0,0),0)==0);check(all(sum(a)==4 for a in f))
# Norm determinant of multiplication by x+t*y+t^2*z modulo t^4-t+1.
x,y,z=[atom(a) for a in [(1,0,0),(0,1,0),(0,0,1)]]
T=[{},one,{},{}]
def tred(k):
    if k<4:return {k:1}
    a=tred(k-3);b=tred(k-4);o=a.copy()
    for j,c in b.items():o[j]=o.get(j,0)-c
    return {j:c for j,c in o.items() if c}
A=[[{} for j in range(4)] for i in range(4)]
for j in range(4):
    for shift,poly in enumerate([x,y,z]):
        for i,c in tred(j+shift).items():A[i][j]=add(A[i][j],scale(poly,c))
D={}
for pi in permutations(range(4)):
    v=one
    for i in range(4):v=mul(v,A[i][pi[i]])
    sign=(-1)**sum(pi[i]>pi[j] for i in range(4) for j in range(i+1,4))
    D=add(D,scale(v,sign))
check(D==f)
# Finite field checks for h=t^4-t+1.
def rem(a,b,p):
    a=[v%p for v in a]
    while len(a)>=len(b):
        c=a[-1]*pow(b[-1],-1,p)%p;k=len(a)-len(b)
        for j,v in enumerate(b):a[k+j]=(a[k+j]-c*v)%p
        while a and a[-1]==0:a.pop()
    return a
h=[1,-1,0,0,1]
for deg in (1,2):
    for low in product(range(2),repeat=deg):check(bool(rem(h,list(low)+[1],2)))
cubic=[1,1,-1,1]
for t in range(3):check(sum(c*t**j for j,c in enumerate(cubic))%3!=0)
check([v%3 for v in [cubic[0],cubic[0]+cubic[1],cubic[1]+cubic[2],cubic[2]+cubic[3],cubic[3]]]==[v%3 for v in h])
check(sum(c*(-1)**j for j,c in enumerate(cubic))%3!=0)
# Exact explicit SOS identity, beta negative root of beta^3-4beta-1.
# Clear beta denominators before reducing: 4 beta^2 f=(beta U)^2-beta(beta V)^2.
B=atom((0,0,0,1))
f4={a+(0,):c for a,c in f.items()}
bU=add(atom((2,0,0,1),2),atom((0,2,0,2)),atom((0,1,1,1),-1),atom((0,0,2,1),2),atom((0,0,2,0)))
bV=add(atom((1,1,0,1),2),atom((0,2,0,0),-1),atom((1,0,1,0),2),atom((0,1,1,2)),atom((0,0,2,1),-1))
R=add(mul(bU,bU),scale(mul(B,mul(bV,bV)),-1),scale(mul(mul(B,B),f4),-4))
def bred(k):
    if k<3:return {k:1}
    a=bred(k-2);b=bred(k-3);o={j:4*c for j,c in a.items()}
    for j,c in b.items():o[j]=o.get(j,0)+c
    return o
out={}
for a,c in R.items():
    for j,d in bred(a[3]).items():out=add(out,atom(a[:3]+(j,),c*d))
check(out=={});check((-2)**3-4*(-2)-1<0);check((-1)**3-4*(-1)-1>0)
# General-position incidence and quadratic interpolation controls.
for roots in combinations(range(-3,5),4):
    for triple in combinations(roots,3):check(det([[1,t,t*t] for t in triple])!=0)
    rows=[]
    for a,b in combinations(roots,2):
        u,v,w=a*b,-a-b,1
        check(u+a*v+a*a*w==0);check(u+b*v+b*b*w==0)
        rows.append([u*u,u*v,u*w,v*v,v*w,w*w])
    vand=1
    for a,b in combinations(roots,2):vand*=b-a
    check(abs(det(rows))==vand*vand)
# Jet identities: arbitrary rational higher tails do not affect degree four
# once constant and linear jets vanish. Every coefficient is compared.
mons2=[a for a in product(range(3),repeat=3) if sum(a)==2]
for seed in range(1,80):
    a2={a:F(((seed+2*i)%9)-4,1+(i%3)) for i,a in enumerate(mons2)}
    b2={a:F(((3*seed+i)%11)-5,1+(i%4)) for i,a in enumerate(mons2)}
    at=add(a2,atom((3,0,0),seed),atom((0,0,7),-seed))
    bt=add(b2,atom((0,4,0),seed+1),atom((9,0,0),seed))
    full=add(mul(at,at),mul(g,mul(bt,bt)))
    lead={a:c for a,c in full.items() if sum(a)==4}
    check(lead==add(mul(a2,a2),mul(b2,b2)))
    check(all(sum(a)>=4 for a in full))
# Rational sample controls of norm nonnegativity and exact source example.
for v in product(range(-3,4),repeat=3):check(evalp(f,v)>=0);check(evalp(p,v)>=1)
check(F(32)+F(8,9)*(F(32)-F(34)-F(34))==0)
result={'status':'PASS','exact_assertions':count,'floating_diagnostics':0,'moment_entries':35,'moment_nonzero':{'0,0,0':'1','4,0,0':'-1'},'norm_terms':{','.join(map(str,a)):str(c) for a,c in sorted(f.items())},'scope':'Finite exact controls supplement the all-degree Taylor-jet and Galois proofs; no finite search certifies arbitrary-degree impossibility.'}
print(json.dumps(result,indent=2,sort_keys=True))
