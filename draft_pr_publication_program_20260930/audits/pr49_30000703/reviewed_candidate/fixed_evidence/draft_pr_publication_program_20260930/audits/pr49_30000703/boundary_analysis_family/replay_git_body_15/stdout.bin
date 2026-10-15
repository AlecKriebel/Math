#!/usr/bin/env python3
"""Exact diagnostic identities; no numerical certificate for reflection theorems."""
from pathlib import Path
import json
import sympy as s
x,y,r,u=s.symbols('x y r u',real=True)
z=x+s.I*y
checks={}
def ck(n,v):
 assert bool(v),n
 checks[n]='PASS'
w=(1-z)/(1+z)
ck('cayley_real_part',s.factor(s.re(w)-(1-x*x-y*y)/((1+x)**2+y*y))==0)
ck('cayley_derivative',s.cancel(s.diff((1-s.Symbol('z'))/(1+s.Symbol('z')),s.Symbol('z'))+2/(1+s.Symbol('z'))**2)==0)
ck('exponential_distortion',s.cancel((2*u*s.exp(-u)/(1-s.exp(-2*u))-u/s.sinh(u)).rewrite(s.exp))==0)
ck('exponential_limit',s.limit(u/s.sinh(u),u,0)==1)
ck('square_distortion',s.cancel((1-r*r)*2*r/(1-r**4)-2*r/(1+r*r))==0)
ck('square_limit',s.limit(2*r/(1+r*r),r,1)==1)
ck('square_deficit',s.factor(1-2*r/(1+r*r)-(1-r)**2/(1+r*r))==0)
# Triangle estimate behind the point-to-arc argument, checked with exact radii.
for j in range(1,21):
 delta=s.Rational(1,j)
 for a in (s.Rational(1,4),s.Rational(1,3),s.Rational(2,5)):
  # |xi-1| <= a*delta, |z-xi| < delta/2 imply |z-1| < delta.
  ck(f'arc_margin_{j}_{a}',a*delta+delta/2<delta)
q=s.symbols('q')
f=s.exp(-(1-q)/(1+q))
ck('example_boundary_value',f.subs(q,1)==1)
ck('example_derivative',s.diff(f,q).subs(q,1)==s.Rational(1,2))
out={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Exact formula and quantifier-margin controls; the published reflection theorem is an imported analytic result, not a computed claim.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
