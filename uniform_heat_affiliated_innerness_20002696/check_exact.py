#!/usr/bin/env python3
"""Exact finite-dimensional diagnostics. These do not prove infinite-domain claims."""
from fractions import Fraction as F
from itertools import product
from math import comb
import json
from pathlib import Path

def zeros(d): return [[F(0) for _ in range(d)] for _ in range(d)]
def eye(d):
    a=zeros(d)
    for i in range(d): a[i][i]=F(1)
    return a

def add(a,b): return [[x+y for x,y in zip(u,v)] for u,v in zip(a,b)]
def scale(a,c): return [[c*x for x in row] for row in a]
def transpose(a): return list(map(list,zip(*a)))
def mul(a,b):
    d=len(a)
    return [[sum((a[i][k]*b[k][j] for k in range(d)),F(0)) for j in range(d)] for i in range(d)]
def kron(a,b):
    d,e=len(a),len(b)
    return [[a[i//e][j//e]*b[i%e][j%e] for j in range(d*e)] for i in range(d*e)]
def inner(a,b):
    d=len(a)
    return sum((a[i][j]*b[i][j] for i in range(d) for j in range(d)),F(0))/d

d=4; one=eye(d)
c=[F(1),F(2),F(3),F(4)]; q=F(1,d); rates=[x*x*q for x in c]
ps=[]
for n in range(d):
    p=zeros(d);p[n][n]=F(1);ps.append(p)
xi=zeros(d*d)
for cn,p in zip(c,ps):xi=add(xi,scale(kron(p,p),cn))
def delta(x):
    k=add(kron(x,one),scale(kron(one,transpose(x)),F(-1)))
    return mul(k,xi) # Removing the common factor i preserves all inner products.
def generator(x):
    return [[(rates[i]+rates[j])*x[i][j] if i!=j else F(0) for j in range(d)] for i in range(d)]
basis=[]
for i,j in product(range(d),repeat=2):
    e=zeros(d);e[i][j]=F(1);basis.append(e)
ds=[delta(x) for x in basis]
checks=0
for i,x in enumerate(basis):
    for j,y in enumerate(basis):
        assert inner(ds[i],ds[j])==inner(x,generator(y));checks+=1
assert delta(one)==zeros(d*d)
# Leibniz with the second action on the left by y^T.
for x,y in product(basis,repeat=2):
    rhs=add(mul(kron(x,one),delta(y)),mul(kron(one,transpose(y)),delta(x)))
    assert delta(mul(x,y))==rhs;checks+=1
# Rational surrogate b_n for the exact heat formula tests CP-unital/trace structure.
b=[F(1,2),F(2,3),F(3,4),F(4,5)]
def heat(x):
    return [[x[i][j] if i==j else b[i]*b[j]*x[i][j] for j in range(d)] for i in range(d)]
assert heat(one)==one
for x in basis:
    assert sum(heat(x)[i][i] for i in range(d))==sum(x[i][i] for i in range(d));checks+=1
moments=[]
for n in [1,2,3,4,8,16,32]:
    m2=sum(F(comb(n,k),2**n)*(2*k-n)**2 for k in range(n+1))
    m4=sum(F(comb(n,k),2**n)*(2*k-n)**4 for k in range(n+1))
    assert m2==n and m4==3*n*n-2*n
    # Threshold squared avoids floating point.
    probability=sum((F(comb(n,k),2**n) for k in range(n+1) if 2*(2*k-n)**2>=n),F(0))
    assert probability>=F(1,12)
    moments.append({'n':n,'second':str(m2),'fourth':str(m4),'tail_probability':str(probability)})
    checks+=3
result={'status':'pass','exact_assertions':checks,'dimension':d,'method':'Python standard-library rational arithmetic','generator_rates':[str(a) for a in rates],'rademacher_moments':moments,'scope':'Finite-matrix trace normalization, opposite-action Leibniz identity, heat unital/trace checks, and binomial moment diagnostics. Infinite-dimensional conclusions rely on PROOF.md.'}
Path(__file__).with_name('exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
