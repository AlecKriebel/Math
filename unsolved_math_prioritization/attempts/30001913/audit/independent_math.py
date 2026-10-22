"""Supplementary independent exact controls. No author code is imported.
Run with python -I -S independent_math.py, also with -O.
These checks do not formally prove the geometric assertions.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import factorial, gcd
import json

checks=0

def need(ok,label):
    global checks
    checks+=1
    if not ok: raise ValueError(label)

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

vertices=((1,0,0),(0,1,0),(0,0,1),(-4,-2,-1))
facets={}
for inds in combinations(range(4),3):
    a,b,c=(vertices[i] for i in inds); n=cross(sub(b,a),sub(c,a));content=gcd(*n);n=tuple(v//content for v in n);height=dot(n,a)
    other=next(vertices[i] for i in range(4) if i not in inds)
    if dot(n,other)>height:n=tuple(-v for v in n);height=-height
    need(height==1,'independently derived reflexive facet height')
    facets[n]=(inds,content)
need(set(facets)=={(1,1,1),(1,1,-7),(1,-3,1),(-1,1,1)},'all primitive facet normals')
need([sum(w*v[i] for w,v in zip((4,2,1,1),vertices)) for i in range(3)]==[0,0,0],'strict positive barycentric origin')
areas=sorted(content for n,(inds,content) in facets.items() if n!=(-1,1,1))
need(areas==[1,1,2],'two unimodular faces and one area-two face')
need(sorted(gcd(*sub(a,b)) for a,b in combinations(vertices,2))==[1,1,1,1,1,2],'edge lattice lengths')
U=(2,1,1);V=(-1,-1,0)
for exponent,uv in [((1,1,0),(0,-1)),((1,0,1),(1,1)),((-3,-2,-1),(-1,1)),((-1,-1,0),(0,1)),((0,0,0),(0,0))]:
    need(tuple(uv[0]*U[i]+uv[1]*V[i] for i in range(3))==exponent,'face character transform')
need(cross(U,V)==(1,-1,-1),'saturated difference-lattice basis')
# Quadratic discriminant, and rational parametrizations of every exceptional curve.
for a in (-4,0,4):
    for s in (Fraction(2),Fraction(3),Fraction(5,2),Fraction(-2)):
        u=-s*s
        # sqrt(-4u)=2s; a=0 has (u+1)^2, a=+-4 has (u-1)^2.
        root=2*s*(u+1 if a==0 else u-1)
        need(root*root==a*a*u*u-4*u*(u+1)**2,'exceptional discriminant square after U=-s^2')
        for sign in (-1,1):
            v=(-a*u+sign*root)/(2*(u+1)**2)
            need((u+1)**2*v*v+a*u*v+u==0,'rational normalization parameter substitution')
# Polynomial-in-a Laurent multiplication, independent from the author scalar specializations.
terms=(((1,0,0,0),1),((0,1,0,0),1),((0,0,1,0),1),((-4,-2,-1,0),1),((-2,-1,0,0),2),((-1,0,0,1),1))
expansion={(0,0,0,0):1};period_polynomials=[]
for degree in range(15):
    actual={e[3]:v for e,v in expansion.items() if e[:3]==(0,0,0)}
    expected=defaultdict(int)
    # Enumerate multiplicities of the three negative monomials; solve all three balances.
    for ell in range(degree+1):
        for mid in range(degree+1):
            for power_a in range(degree+1):
                counts=(4*ell+2*mid+power_a,2*ell+mid,ell,ell,mid,power_a)
                if sum(counts)!=degree:continue
                denominator=1
                for c in counts:denominator*=factorial(c)
                expected[power_a]+=factorial(degree)//denominator*2**mid
    need(actual==dict(expected),'symbolic constant-term polynomial at degree '+str(degree))
    period_polynomials.append(actual)
    new=defaultdict(int)
    for e,c in expansion.items():
        for f,d in terms:new[tuple(x+y for x,y in zip(e,f))]+=c*d
    expansion=dict(new)
need([sum(v*4**e for e,v in p.items()) for p in period_polynomials[:10]]==[1,0,8,0,120,0,2240,0,47320,0],'independent initial F4 period')
for n,p in enumerate(period_polynomials):
    need(p.get(0,0)==(factorial(n)//factorial(n//4)**4 if n%4==0 else 0),'F0 quartic period')
    need(all((2*k-n)%4==0 for k in p),'support parity for a-sign change')
# Covering-space relation, not just local matrix ranks.
A=(1,2,0,1);B=(1,0,-2,1);C=(1,-2,2,-3);I=(1,0,0,1)
def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def power(a,n):
    out=I
    for _ in range(n):out=mul(out,a)
    return out

def rank_minus_I(a):
    x=(a[0]-1,a[1],a[2],a[3]-1)
    return 0 if x==(0,0,0,0) else (2 if x[0]*x[3]!=x[1]*x[2] else 1)
need(mul(mul(A,B),C)==I,'punctured-sphere relation')
for m in range(1,161):
    am=(1,2*m,0,1);cm=tuple((-1)**m*x for x in (1-2*m,2*m,-2*m,1+2*m))
    need(power(A,m)==am and power(C,m)==cm,'closed monodromy powers')
    prod=am
    for j in range(m-1,-1,-1):
        bj=mul(mul((1,-2*j,0,1),B),(1,2*j,0,1));prod=mul(prod,bj)
        need(rank_minus_I(bj)==1,'ramification at lifted finite point')
    need(mul(prod,cm)==I,'full covering monodromy relation')
    need(rank_minus_I(am)+m+rank_minus_I(cm)-4==(m-1 if m%2 else m-2),'defect formula')
    need(am[1]!=0 and B[2]!=0,'independent fixed lines prove irreducibility')
print(json.dumps({'problem_id':30001913,'independent_exact_checks':checks,'symbolic_period_degrees':list(range(15)),'covering_degrees':list(range(1,161)),'status':'all supplementary checks passed','formal_geometric_verification':False},sort_keys=True))
