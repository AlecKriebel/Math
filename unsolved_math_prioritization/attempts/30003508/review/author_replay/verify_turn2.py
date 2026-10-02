#!/usr/bin/env python3
"""Exact controls for the explicit finite-order boundary extension and spectral bookkeeping."""
import sympy as s,json
from pathlib import Path
alpha=[28,-112,210,-224,140,-48,7]
checks=0
for k in range(7):
 assert sum(a*(-j)**k for j,a in enumerate(alpha,1))==1;checks+=1
# The path-adjacency empirical pair kernel is symmetric and finite rank in N+1 features.
for n in range(1,9):
 B=s.zeros(n+1)
 for i in range(n):B[i,i+1]=B[i+1,i]=s.Rational(1,2*n)
 assert B==B.T;checks+=1
 assert B.rank()<=min(n+1,2*n);checks+=1
 assert sum(B)==1;checks+=1
 # Pair kernels need not be PSD; the spectral positive-part rule is essential.
 assert B[0,0]*B[1,1]-B[0,1]**2<0;checks+=1
x=s.symbols('x',positive=True)
assert s.limit(x*x*s.log(x),x,0,dir='+')==0;checks+=1
# Bounding-box net exponent: dimension2d and mesh2^{-j/(4d)} give cardinal exponentj/2.
d,j=s.symbols('d j',positive=True)
assert s.simplify(2*d*j/(4*d)-j/2)==0;checks+=1
assert s.simplify((4*d+8)+2-(4*d+10))==0;checks+=1
out={'status':'PASS','exact_checks':checks,'extension_order':6,'reflection_weights':alpha,'scope':'Extension matching, finite-rank symmetrized kernel and spectral-continuity controls; stochastic consistency is proved analytically in TURN_2.md','full_candidate_pending_review':True,'substantive_author_turns':2}
print(json.dumps(out,indent=2));Path(__file__).with_name('TURN_2_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
