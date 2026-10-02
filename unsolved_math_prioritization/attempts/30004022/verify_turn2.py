#!/usr/bin/env python3
"""Exact analytic-ansatz controls; no numerical Cauchy-transform tolerance."""
import json
from fractions import Fraction as F
from collections import Counter
import sympy as sp

C=Counter()
def ck(group,cond):
    if not cond:raise AssertionError(group)
    C[group]+=1
p,s=sp.symbols('p s',real=True)
z=-sp.I*s
G=(1-p)/(z+p)+p/(z-(1-p))
t=p*(1-p)
imag=sp.factor(sp.im(sp.together(z*G)))
expected=s*t*(2*p-1)/((s*s+p*p)*(s*s+(1-p)**2))
ck('symbolic_cauchy_identity',sp.factor(imag-expected)==0)
ck('centered_input',sp.expand((1-p)*(-p)+p*(1-p))==0)
ck('variance_identity',sp.expand((1-p)*p*p+p*(1-p)**2-t)==0)
ck('third_centered_moment',sp.expand((1-p)*(-p)**3+p*(1-p)**3-t*(1-2*p))==0)
ck('reflection_identity',sp.factor(expected.subs(p,1-p)+expected)==0)
ck('symmetric_boundary',sp.simplify(expected.subs(p,sp.Rational(1,2)))==0)
for v in (0,1):ck('deterministic_boundary',sp.simplify(expected.subs(p,v))==0)
ck('large_imaginary_axis_leading_term',sp.limit(s**3*expected,s,sp.oo)==t*(2*p-1))

def pairmul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def pairinv(a):
    d=a[0]*a[0]+a[1]*a[1]
    return a[0]/d,-a[1]/d

for den in range(2,31):
    for num in range(1,den):
        pp=F(num,den);tt=pp*(1-pp)
        for ss in [F(1,8),F(1,2),F(1),F(3),F(10)]:
            # Evaluate the two-point Cauchy transform using rational complex
            # pairs, separately from the symbolic simplification above.
            ga=pairinv((pp,-ss));gb=pairinv((pp-1,-ss))
            gg=((1-pp)*ga[0]+pp*gb[0],(1-pp)*ga[1]+pp*gb[1])
            actual=pairmul((F(0),-ss),gg)[1]
            want=ss*tt*(2*pp-1)/((ss*ss+pp*pp)*(ss*ss+(1-pp)**2))
            ck('rational_complex_direct_identity',actual==want)
            ck('strict_sign_or_even_boundary',actual==0 if pp==F(1,2) else actual*(2*pp-1)>0)
            # Any symmetric two-point target gives a real zG(z) on iR+.
            yy=ss;xx=F(3,2)
            a=pairinv((-xx,yy));b=pairinv((xx,yy))
            target=pairmul((F(0),yy),((a[0]+b[0])/2,(a[1]+b[1])/2))
            ck('symmetric_target_reality',target[1]==0 and target[0]==yy*yy/(yy*yy+xx*xx))

print(json.dumps({'problem_id':30004022,'turn':2,'status':'PASS','counts':dict(sorted(C.items())),
    'exact_assertions':sum(C.values()),'arithmetic':'exact symbolic identities and rational complex pairs',
    'scope':'Explicit-family controls. General arbitrary-measure rigidity is the separate analytic proof in TURN_2.md. Original broader representation problem remains unresolved.'},indent=2,sort_keys=True))
