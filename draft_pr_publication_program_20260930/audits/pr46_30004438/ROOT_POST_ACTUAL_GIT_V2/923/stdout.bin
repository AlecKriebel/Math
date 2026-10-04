#!/usr/bin/env python3
"""Exact checks of a known Kozhasov-Kummer open-family construction."""
from pathlib import Path
import json
import sympy as s
z=s.symbols('z'); checks={}
def ck(name,value):
 assert bool(value),name
 checks[name]='PASS'
def homogeneous_at(poly,p,q,d):
 return s.Poly(sum(poly.nth(j)*p.as_expr()**j*q.as_expr()**(d-j) for j in range(d+1)),z)
for d in range(2,7):
 p=s.Poly(s.prod(z+2*j-1 for j in range(1,d+1)),z)
 q=s.Poly(s.prod(z+2*j for j in range(1,d+1)),z)
 ck(f'd{d}_degrees',p.degree()==q.degree()==d)
 ck(f'd{d}_positive_coefficients',all(a>0 for a in p.all_coeffs()+q.all_coeffs()))
 ck(f'd{d}_coprime',s.gcd(p,q).degree()==0)
 res=[s.cancel(p.eval(-2*j)/q.diff().eval(-2*j)) for j in range(1,d+1)]
 ck(f'd{d}_negative_residues',all(a<0 for a in res))
 ck(f'd{d}_partial_fractions',s.cancel(p.as_expr()/q.as_expr()-1-sum(res[j-1]/(z+2*j) for j in range(1,d+1)))==0)
 ck(f'd{d}_simple_poles',s.gcd(q,q.diff()).degree()==0)
 F=p-s.Poly(z,z)*q
 ck(f'd{d}_all_fixed_points_real',F.count_roots(-s.oo,s.oo)==F.degree())
 if d<=4:
  pp=homogeneous_at(p,p,q,d);qq=homogeneous_at(q,p,q,d);e=d*d
  ck(f'd{d}_iterate2_degrees',pp.degree()==qq.degree()==e)
  ck(f'd{d}_iterate2_positive',all(a>0 for a in pp.all_coeffs()+qq.all_coeffs()))
  ck(f'd{d}_iterate2_coprime',s.gcd(pp,qq).degree()==0)
  ck(f'd{d}_iterate2_real_simple_poles',qq.count_roots(-s.oo,s.oo)==e and s.gcd(qq,qq.diff()).degree()==0)
  FF=pp-s.Poly(z,z)*qq
  ck(f'd{d}_iterate2_real_fixed_points',FF.count_roots(-s.oo,s.oo)==FF.degree())
x,y,b,A=s.symbols('x y b A',real=True)
ck('single_residue_imaginary_identity',s.simplify(s.im(A/(x+s.I*y-b))+A*y/((x-b)**2+y*y))==0)
r={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Finite exact controls of an existing all-degree, all-period proof; not a novelty claim or exhaustive periodic-point test.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
