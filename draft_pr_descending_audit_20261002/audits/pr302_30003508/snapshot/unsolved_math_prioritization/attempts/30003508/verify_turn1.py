#!/usr/bin/env python3
"""Exact local-jet and normal-equation controls; not a proof of empirical convergence."""
import sympy as s,json
from pathlib import Path
x,y=s.symbols('x y',real=True)
S=s.Matrix([[2+x*x,x*y/4],[x*y/4,3+y*y]])
b=s.Matrix([sum(s.diff(S[i,j],[x,y][i]) for i in range(2)) for j in range(2)])
assert b==s.Matrix([9*x/4,9*y/4])
th=s.Matrix([S[0,0],S[1,1],S[0,1],b[0],b[1]])
checks=1
for u in [x,y,x*x/2,y*y/2,x*y,x*x*y+x*y*y,s.exp(x+y)]:
 J=s.Matrix([s.diff(u,x,2),s.diff(u,y,2),2*s.diff(u,x,y),s.diff(u,x),s.diff(u,y)])
 flux=S*s.Matrix([s.diff(u,x),s.diff(u,y)])
 assert s.simplify(J.dot(th)-s.diff(flux[0],x)-s.diff(flux[1],y))==0;checks+=1
# Affine/quadratic jets form a basis at the origin; the mixed coordinate has factor two.
polys=[x*x/2,y*y/2,x*y/2,x,y]
mat=s.Matrix([[s.diff(u,x,2),s.diff(u,y,2),2*s.diff(u,x,y),s.diff(u,x),s.diff(u,y)] for u in polys]).subs({x:0,y:0})
assert mat==s.eye(5);checks+=1
# Scalar spectral factor bookkeeping: two outer factors and middle functions.
k=s.symbols('k',positive=True)
assert s.expand(k*(k*k)*k-k**4)==0;checks+=1
assert s.simplify(k*(k*k*s.log(k))*k-k**4*s.log(k))==0;checks+=1
out={'status':'PASS','exact_checks':checks,'scope':'Differential jet coordinates, local spanning example, spectral weights; no statistical or global elliptic theorem inferred from finite checks','substantive_author_turns':1,'full_original_resolved':False}
print(json.dumps(out,indent=2));Path(__file__).with_name('TURN_1_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
