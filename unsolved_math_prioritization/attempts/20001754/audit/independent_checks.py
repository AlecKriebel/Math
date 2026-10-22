#!/usr/bin/env python3
"""Independent exact controls for the audit; analytic conclusions are in AUDIT_REPORT.md."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sympy as s

def mm(a,b):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2)) for i in range(2) for j in range(2))
def trans(a): return (a[0],a[2],a[1],a[3])
def generated(*gs):
    seen={(1,0,0,1)}
    while True:
        more=seen|{mm(a,g) for a in seen for g in gs}
        if more==seen: return sorted(seen)
        assert len(more)<100
        seen=more
S=(0,1,1,0); R=(-1,0,-1,1); T=(1,0,1,-1); J=(-1,0,0,1)
G=generated(S,R); H=generated(S,T)
assert len(G)==6 and len(H)==12
assert mm(J,R)==(1,0,-1,1)
M=(Q(1),Q(-1,2),Q(-1,2),Q(1))
assert all(mm(mm(trans(g),M),g)==M for g in G)
# Independent spectral diagonalization of q by a=(x+y)/sqrt(2), b=(x-y)/sqrt(2).
a,b=s.symbols('a b',real=True)
x=(a+b)/s.sqrt(2); y=(a-b)/s.sqrt(2)
assert s.expand(x*x+y*y-x*y)==a*a/2+3*b*b/2
n,B=s.symbols('n B',positive=True)
Z=(s.pi/(B/2))**(n/2)*(s.pi/(3*B/2))**(n/2)
assert s.simplify(Z-(2*s.pi/B)**n/3**(n/2))==0
# The integral of q times its Gaussian is minus the beta derivative of Z.
raw_mass=s.simplify(Z+s.diff(Z,B))
normalizer=(s.sqrt(3)/(2*s.pi))**n*B**(n+1)/(B-n)
assert s.simplify(raw_mass*normalizer)==1
assert s.simplify(s.diff(normalizer,B)/normalizer-n*(B-n-1)/(B*(B-n)))==0
# Work with the squared edge-mass ratio to avoid all floating-point comparisons.
r2=lambda k:Q(81,64)*Q(3,4)**k
assert r2(1)==Q(243,256)<1
assert all(r2(k+1)/r2(k)==Q(3,4) for k in range(1,50))
# Reciprocal-covolume values after rescaling unimodular lattices to minimum 1.
assert (s.sqrt(2))**8==16 and 2**24==16777216
result={
 'status':'PASS',
 'rebasing_matrices':[list(g) for g in G],
 'alternative_group_order':len(H),
 'spectral_eigenvalues':['1/2','3/2'],
 'gaussian_mass_identity':'integral((1-q)e^(-beta*q)) = Z(beta)*(1-n/beta)',
 'normalizer':'(sqrt(3)/(2*pi))^n * beta^(n+1)/(beta-n)',
 'squared_edge_ratio_at_n1':str(r2(1)),
 'squared_edge_ratio_recurrence':'3/4',
 'scope':'Exact identities and finite controls; all-dimensional inequalities proved in the report.'
}
print(json.dumps(result,indent=2))
