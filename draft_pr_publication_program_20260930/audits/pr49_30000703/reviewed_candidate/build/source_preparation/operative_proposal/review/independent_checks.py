#!/usr/bin/env python3
"""Independent formula controls for the credited local reflection criterion."""
from pathlib import Path
import json
import sympy as s
checks={}
def ck(name,v):
    assert bool(v),name
    checks[name]='PASS'
r,u,z=s.symbols('r u z',positive=True)
# Distinct non-automorphic powers all exhibit the same limiting distortion.
for k in range(2,17):
    phi=k*r**(k-1)/sum(r**(2*j) for j in range(k))
    ck(f'power_formula_{k}',s.cancel(phi-k*r**(k-1)*(1-r*r)/(1-r**(2*k)))==0)
    ck(f'power_limit_{k}',s.limit(phi,r,1)==1)
    ck(f'power_boundary_derivative_{k}',s.diff(z**k,z).subs(z,1)==k)
    ck(f'power_reflection_{k}',s.cancel(1/(1/z)**k-z**k)==0)
# Positive derivative values are not forced to be 1. An entire parameter
# family of singular inner examples has alpha=a/2.
w=(1-z)/(1+z)
ck('cayley_reflection',s.cancel(w.subs(z,1/z)+w)==0)
for a in [s.Rational(1,5),s.Rational(1,2),s.Integer(1),s.Rational(3,2),s.Integer(2),s.Integer(5)]:
    f=s.exp(-a*w)
    ck(f'singular_inner_value_{a}',f.subs(z,1)==1)
    ck(f'singular_inner_derivative_{a}',s.diff(f,z).subs(z,1)==a/2)
    phi=2*a*u*s.exp(-a*u)/(1-s.exp(-2*a*u))
    ck(f'singular_inner_distortion_{a}',s.cancel((phi-a*u/s.sinh(a*u)).rewrite(s.exp))==0)
    ck(f'singular_inner_limit_{a}',s.limit(phi,u,0)==1)
# Rational boundary points and disk points, with exact Euclidean radii.
for j in range(1,26):
    delta=s.Rational(1,j);v=delta/8
    X=(1-v*v)/(1+v*v);Y=2*v/(1+v*v)
    ck(f'boundary_point_{j}',X*X+Y*Y==1)
    ck(f'arc_margin_{j}',s.expand((X-1)**2+Y**2)<delta**2/4)
    rho=1-delta/8;Zx,Zy=rho*X,rho*Y
    ck(f'interior_point_{j}',Zx*Zx+Zy*Zy<1)
    ck(f'neighborhood_margin_{j}',s.expand((Zx-1)**2+Zy**2)<delta**2)
# The sign in the logarithmic radial derivative used after Hopf's lemma.
a=s.symbols('a',positive=True)
ck('log_modulus_radial_derivative',s.diff(-a*(1-r)/(1+r),r).subs(r,1)==a/2)
x,y=s.symbols('x y',real=True)
wc=(1-(x+s.I*y))/(1+(x+s.I*y))
ck('positive_cayley_realpart_identity',s.factor(s.re(wc)-(1-x*x-y*y)/((1+x)**2+y*y))==0)
result={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Exact example and quantifier-margin controls only. The imported published reflection theorem and analytic Hopf argument are audited in REVIEW.md, not established by these finite checks.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
