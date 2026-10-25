#!/usr/bin/env python3
"""Read-only independent exact scope controls; use the existing shared SymPy runtime."""
import json
import sympy as s
x,a,beta,m,v=s.symbols('x a beta m v',real=True)
p=x**3-s.Rational(3,20)*x
P0=lambda q:s.expand((q.subs(x,x/2-s.Rational(1,4))+q.subs(x,x/2+s.Rational(1,4)))/2)
phi=lambda q:s.integrate(x*q,(x,-s.Rational(1,2),s.Rational(1,2)))
assert s.integrate(p,(x,-s.Rational(1,2),s.Rational(1,2)))==phi(p)==0
assert phi(P0(p))==s.Rational(1,320)
C=1+beta/4;den=1+beta*m;variance=v-m*m
det=(C-(1+beta**2*variance)/den**2)*(C-1)-beta**2*variance/den**2
cert=beta**2*((C*m-s.Rational(1,4))**2+C*(m-v))/den**2
assert s.factor(det-cert)==0
poly=7*(2-a)**3-5*(2+a)*(4-13*a*a)
positive=172*(a-s.Rational(13,43))**2+s.Rational(12,43)+58*a**3
assert s.expand(poly-positive)==0
assert 16*s.Rational(21,25)/(1-s.Rational(21,25))==84
assert s.Rational(181,2)+s.Rational(35,24)*84==213
assert s.expand(25-50*a-(16-100*a*a)-(100*(a-s.Rational(1,4))**2+s.Rational(11,4)))==0
print(json.dumps({'status':'PASS','sympy':s.__version__,'source_kernel_countercontrol':'phi(p)=0; phi(P0 p)=1/320','rank_one_determinant_difference':'0','continuous_polynomial_difference':'0','parameter_sum':'84','log_distortion':'213','scope':'Exact algebra only; no repair, no infinite-dimensional proof or historical-priority certification.'},indent=2))
