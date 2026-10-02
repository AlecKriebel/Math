#!/usr/bin/env python3
"""Symbolic resultant and finite exact real-root checks; scope stated in proof."""
import sympy as s
import json
x,T,B,D=s.symbols('x T B D');p=(x*x-T*T)**2-B*B*D*x-B*B*T*T
claimed=-B**4*(27*B**4*D**4-288*B**2*D**2*T**4+256*B**2*T**6+256*D**2*T**6-256*T**8)
assert s.expand(s.resultant(p,s.diff(p,x),x)-claimed)==0
n=1;sturm=0;degenerate=0
for b in range(-4,5):
 for d in range(-4,5):
  L=1+abs(b)+abs(d);t=4*L
  assert t*t-max(abs(b),abs(d))*(t+L)>(t-L)**2 and t*t+max(abs(b),abs(d))*(t+L)<(t+L)**2;n+=1
  assert s.Rational(max(abs(b),abs(d)),2*(t-L))<s.Rational(1,6);n+=1
  if b:
   poly=s.Poly(p.subs({B:b,D:d,T:t}),x)
   assert poly.count_roots(-s.oo,s.oo)==4 and s.discriminant(poly.as_expr(),x)!=0;n+=1;sturm+=1
  else:
   assert t!=0 and t*t+d*t>0 and t*t-d*t>0;n+=1;degenerate+=1
print(json.dumps({'assertions':n,'symbolic_resultant_identity':True,'exact_sturm_four_real_root_cases':sturm,'B_zero_cases':degenerate,'scope':'Finite integer-parameter controls and an exact symbolic discriminant identity; the proof supplies all real and algebraically closed parameter cases.'},indent=2,sort_keys=True))
