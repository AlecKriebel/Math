#!/usr/bin/env python3
"""Independent mechanisms: Lie derivations, symbolic determinants, Kronecker ad.

Uses the existing SymPy environment. No deposited module is imported. Checks
are explicit exceptions and retain their meaning under Python optimization.
"""
from collections import defaultdict
from itertools import product
import json
import sympy as s

def require(p,m):
    if not p:raise RuntimeError(m)
def clean(p):return {w:c for w,c in p.items() if c}
def add(a,b,sign=1):
    q=defaultdict(int,a)
    for w,c in b.items():q[w]+=sign*c
    return clean(q)
def mul(a,b):
    q=defaultdict(int)
    for u,c in a.items():
        for v,d in b.items():q[u+v]+=c*d
    return clean(q)
def bracket(a,b):return add(mul(a,b),mul(b,a),-1)
x=[{(i,):1} for i in range(3)];zero={}
DA=[bracket(x[1],x[0]),bracket(x[0],x[1]),zero]
DB=[zero,bracket(x[2],x[1]),bracket(x[1],x[2])]
def derive(p,D):
    q={}
    for w,c in p.items():
        for j,letter in enumerate(w):
            for v,d in D[letter].items():
                q=add(q,{w[:j]+v+w[j+1:]:c*d})
    return q
images=[add(derive(DB[i],DA),derive(DA[i],DB),-1) for i in range(3)]
longitudes=[bracket(x[1],x[2]),bracket(x[2],x[0]),bracket(x[0],x[1])]
require(images==[bracket(longitudes[i],x[i]) for i in range(3)],'commutator Lie action versus longitude leading terms')

r,t,u,v,w=s.symbols('r t u v w')
M=s.Matrix([[1,0,0,0,0,0],[1,1,1,0,0,0],[1,-1,1,0,0,0],
            [1,r,r*r,0,0,1],[1,t,t*t,1,5,v],[1,u,u*u,5,1,w]])
require(s.expand(M.det())==-48,'entire symbolic six-row determinant')
require(s.Matrix([[1,0,0,0],[1,1,1,0],[1,-1,1,0],[1,t,t*t,1]]).det()==2,'symbolic span determinant')
require(s.Matrix([[2,0,0],[0,2,0],[2,2,-4]]).det()==-16,'concordance test determinant')
require(s.Matrix([[1,5],[5,1]]).det()==-24,'component determinant')

X=s.Matrix([[0,1,1,1],[1,0,0,0],[0,-1,0,0],[-1,-1,-1,1]])
Y=s.Matrix([[0,0,-1,1],[-1,-1,1,1],[-1,0,0,0],[0,0,-1,-1]])
I=s.eye(4)
ad={1:s.kronecker_product(X,I)-s.kronecker_product(I,X.T),
    2:s.kronecker_product(Y,I)-s.kronecker_product(I,Y.T)}
def traceword(word):
    z=s.eye(16)
    for a in word:z=z*ad[a]
    return s.trace(z)
word=(1,1,2,1,2,2,2)
require(traceword(word)==6 and traceword(word[::-1])==-6,'Kronecker adjoint witness')
# This is an odd-wheel coloring boundary check, not a theorem about the minimum
# finite-type kernel order or all degree-six diagram classes.
def orbit(a):return {a[j:]+a[:j] for j in range(len(a))}
palindromic=0
for n in (1,3,5):
    for a in product((1,2),repeat=n):
        require(a[::-1] in orbit(a),'all short odd binary cyclic colorings reversible')
        palindromic+=1
require(word[::-1] not in orbit(word),'seven-wheel coloring is not cyclically reversed')

z=s.symbols('z')
alex={}
for p,q in [(2,3),(3,4)]:
    genus=(p-1)*(q-1)//2
    delta=s.cancel(z**(-genus)*(1-z)*(1-z**(p*q))/((1-z**p)*(1-z**q)))
    value=s.limit(s.diff(delta,z,2),z,1)/2
    require(value==s.Rational((p*p-1)*(q*q-1),24),'independent normalized Alexander derivative')
    alex[f'{p},{q}']=int(value)

# Connectivity of [1]+1/[2], directly from the two elementary endpoint pairings.
edges=[('aNW','aSE'),('aNE','aSW'),('bNW','bSW'),('bNE','bSE'),
       ('aNE','bNW'),('aSE','bSW')]
parts=[{a,b} for a,b in edges]
changed=True
while changed:
    changed=False
    for i in range(len(parts)):
        for j in range(i):
            if parts[i]&parts[j]:parts[j]|=parts.pop(i);changed=True;break
        if changed:break
outer={'aNW','aSW','bNE','bSE'}
require({frozenset(p&outer) for p in parts}=={frozenset({'aNW','aSW'}),frozenset({'bNE','bSE'})},'vertical connectivity and no closed internal component')
print(json.dumps({'status':'PASS','sympy':s.__version__,
    'independent_mechanisms':['free associative Lie derivations of the braid commutator','symbolic full-parameter determinants','Kronecker adjoint action','normalized Alexander derivative','elementary endpoint connectivity graph'],
    'lie_action_components_verified':3,'symbolic_determinants':[-48,2,-16,-24],
    'adjoint_trace':6,'reversed_trace':-6,'short_odd_binary_colorings':palindromic,
    'Alexander_Conway_values':alex,'rational_tangle_vertical_connectivity':True,
    'scope':'Exact algebra corroboration. Does not replace universal free-exterior topology, classification, 1T survival or integration, and does not claim a minimum kernel order.'},indent=2))
