#!/usr/bin/env python3
"""Exact identity checks for TURN_2.md; the interval signs are proved in its text."""
import sympy as s, json
from pathlib import Path
a,v,r=s.symbols('a v r',real=True)
checks=0
def ck(x):
 global checks
 assert s.simplify(x)==0, x
 checks+=1
ck(4*(a+3)-(3*a+1)*(3-a)**2-(1-a)*(3*a*a-14*a+3))
ck((a+3)**3-16*(3*a+1)-(1-a)**2*(a+11))
D=1+a*v; E=D**2-s.Rational(8,9)*(1-a*a)
P=16*a*a*(1-v)*(32*D+(1-a)**2*(1-v))-81*E**2
ck(s.diff(P,v,2)+4*a*a*(243*a*a*v*v+64*a*a+486*a*v+272*a+163))
ck(P.subs(v,s.Rational(1,3))+(19*a*a-38*a+3)*(35*a*a+74*a+3)/9)
ck(P.subs(v,-s.Rational(1,3))+(43*a*a-98*a+3)*(11*a*a+62*a+3)/9)
for p,lo,hi in [(19*a*a-38*a+3,-s.Rational(101,36),-16),(43*a*a-98*a+3,-s.Rational(437,36),-52)]:
 ck(p.subs(a,s.Rational(1,6))-lo);ck(p.subs(a,1)-hi)
ck((3*a*a-14*a+3).subs(a,s.Rational(1,6))-s.Rational(3,4))
A=1-a*r*r;b=a-r*r
ck(A*A+b*b*r*r+A*b*(1+r*r)-(1+a)*(1-r*r)*(1-r**4))
x=s.symbols('x',real=True)
Pabs2=a*a*(1-r*r)**2+4*r*r+4*a*r*(1+r*r)*x+4*a*a*r*r*x*x
ck((1+r*r+2*a*r*x)**2-Pabs2-(1-a*a)*(1-r*r)**2)
R=3-2*s.sqrt(2)
ck((1+R*R)/(2*R)-3)
ck((1-R*R)**2/(1+R*R)**2-s.Rational(8,9))
ck(R*R/(1-R*R)**2-s.Rational(1,32))
# All-parameter boundary formulas, checked symbolically before any squaring.
y2=r*r*(1-a)**2*(1+r*r-2*r*x)
den=(1-a*r*r)**2+(a-r*r)**2*r*r+2*(1-a*r*r)*(a-r*r)*r*x
odds=s.cancel(y2/(den-y2))
ck(odds.subs({r:R,x:3*v})-(1-a)**2*(1-v)/(32*D))
# Failed scalar bound has rigorously positive first-order coefficient.
coef=s.Rational(3,4)-1/s.sqrt(2)
assert coef>0;checks+=1
out={'status':'PASS','symbolic_identity_and_sign_checks':checks,'floating_diagnostics_used_as_proof':False,'scope':'Turn 2 subcase proof identities only; general interior jets and modulus comparison remain unresolved'}
print(json.dumps(out,indent=2))
Path(__file__).with_name('TURN_2_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
