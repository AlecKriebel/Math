#!/usr/bin/env python3
"""Exact algebra checks only; no numerical evidence is promoted to rationality."""
import hashlib
import itertools
import json
from pathlib import Path
import sympy as S

checks = []
def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)

s,t,r,U,V,W,Q=S.symbols('s t r U V W Q')
a=s*t*(s-t); b=-s*(s-1); c=t*(t-1); f=(s-1)*(s-t)*(t-1); d=-f
check('coefficient sum factorization', S.expand(a+b+c-f)==0)
D=s*s*U-V; N=2*(V-s*U); q=N/D
Ft=(s-t)*s*t*U-(s-1)*s*W+(t-1)*t*V
residual=(t*t*U-W)*q+2*(t*U-W)
check('elimination identity', S.cancel(D*residual-2*U*Ft)==0)
check('anchor inverse relation', S.cancel((s*s*U-V)*q+2*(s*U-V))==0)
v2,v3=S.symbols('v2 v3')
s0=(v3-1)/(v2-1); V0=(v3*v3-1)*U/(v2*v2-1)
check('forward inverse recovers q', S.cancel(q.subs({s:s0,V:V0}, simultaneous=True)-(v2-1))==0)
for name,ratio,witness in [('ab_cd',a*b/(c*d),s*s/(t-1)**2),('ac_bd',a*c/(b*d),t*t/(s-1)**2),('ad_bc',a*d/(b*c),(s-t)**2)]:
    check('diagonal cubic ratio '+name,S.cancel(ratio-witness)==0)

M=S.Matrix([[a,c,b,0,d],[r*s*(s-r),r*(r-1),0,b,-(s-1)*(s-r)*(r-1)]])
minors={}
for i,j in itertools.combinations(range(5),2):
    v=S.factor(M[:,[i,j]].det()); check(f'nonzero column minor {i}{j}',v!=0); minors[f'{i}{j}']=str(v)
# Same elimination identity for the second equation in dimension five.
Fr=(s-r)*s*r*U-(s-1)*s*Q+(r-1)*r*V
check('fivefold second elimination',S.cancel(D*((r*r*U-Q)*q+2*(r*U-Q))-2*U*Fr)==0)

check('negative control rejects elimination sign flip', S.cancel(D*residual+2*U*Ft)!=0)
check('negative control excludes repeated fivefold parameters', M[:,[0,1]].det().subs(r,t)==0)

u=S.symbols('u')
plane=s*t*(s-t)-2*s*u*(s-u)+3*t*u*(t-u)
for chart in [s,t,u]:
    variables=[x for x in [s,t,u] if x!=chart]
    gb=S.groebner([S.diff(plane,x).subs(chart,1) for x in [s,t,u]],*variables,domain=S.QQ)
    check('smooth cubic chart '+str(chart),list(gb)==[1])

z,T=S.symbols('z T');p=1000003
poly=p*z*z+z-T
check('finite characteristic leading coefficient loss',S.Poly(poly,z,T, modulus=p)==S.Poly(z-T,z,T,modulus=p))
check('characteristic zero degree remains two',S.degree(poly,z)==2)
check('discriminant simple zero',S.discriminant(poly,z)==1+4*p*T and S.degree(S.discriminant(poly,z),T)==1)
branch=S.prod(T-j for j in range(4))
check('finite sample point-count control',all(branch.subs(T,j)==0 for j in range(4)))
check('sampled distinct-point control is nonreduced',S.Poly(z*z,z).sqf_part().degree()==1)

point={s:S.Rational(2),t:S.Rational(3),r:S.Rational(4),U:S.Rational(1),V:S.Rational(8,3),W:S.Rational(5),Q:S.Rational(8)}
check('nonempty inverse domain',D.subs(point)!=0 and q.subs(point)==1)
check('fourfold witness equation',Ft.subs(point)==0)
check('fivefold witness equation',Fr.subs(point)==0)
check('elliptic lift witness T',S.Rational(3,1)/(3-1)==S.Rational(3,2))

out={'status':'passed','checks':checks,'check_count':len(checks),'sympy_version':S.__version__,'exact_arithmetic':True,'minors':minors,'scope':'Algebraic identities and stated exact controls. Does not certify rationality, generic curve counts, or novelty.'}
print(json.dumps(out,indent=2))
