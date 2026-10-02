#!/usr/bin/env python3
"""Exact controls for TURN_4; the analytic theorems and interval arguments are in the proof."""
import sympy as S,json,math
from fractions import Fraction as Q
from pathlib import Path
r,s,y,a,X=S.symbols('r s y a X',real=True)
checks=0
def ck(v):
 global checks
 assert S.simplify(v)==0,v
 checks+=1
p=(s+r*r)*(1-s*s)-(s-r*r)*(1+r)**2
ck(p-(r-s)*(r**3+r*r*s+2*r*r+r*s+2*r+s*s))
p=2*(y-r)-(1-r)*y*((1+y)**2-2)
ck(p-(1-y)*((1-r)*y*y+3*(1-r)*y-2*r))
ck(((1-r)*y*y+3*(1-r)*y-2*r).subs(y,r)-r*(1-2*r-r*r))
X02=(s*s-r**4)*(1-s*s)/(1-r*r)**2
ck(s*s-X02-(r*r-s*s)**2/(1-r*r)**2)
# Discriminant of the Schur value-region quadratic, divided by its positive factor.
f=(s*s-r**4)-2*a*r*(1-r*r)*X+a*a*r*r*(1-s*s)
ck(S.discriminant(f,a)/(4*r*r)-(1-r*r)**2*(X*X-X02))
R=(3-S.sqrt(5))/2
ck(R*R-3*R+1)
ck((1-R*R)/(2*R)-S.sqrt(5)/2)
ck((1+R)/(1-R)-S.sqrt(5))
assert R<S.sqrt(2)-1; checks+=1
ck((r*r/(1-r*r)**2)/(r/(1+r)**2)-r/(1-r)**2)
# Rational arctan/log separation. pi>31/10 and atan(t)>=t-t^3/3 are external elementary facts.
atan_lower=Q(31,40)+Q(1,21)-Q(1,3*21**3)
assert atan_lower>Q(81,100);checks+=1
exp_lower=sum(Q(81,50)**n/math.factorial(n) for n in range(8))
assert exp_lower>5;checks+=1
assert Q(5,4)>Q(11,10)**2;checks+=1
# Polarization coefficient identity for any symmetric 2x2 matrix is representative of the finite-vector identity.
b11,b12,b22,p1,p2,q1,q2=S.symbols('b11 b12 b22 p1 p2 q1 q2')
def quad(x,y):return b11*x*x+2*b12*x*y+b22*y*y
ck(quad(p1+q1,p2+q2)-quad(p1-q1,p2-q2)-4*(b11*p1*q1+b12*(p1*q2+p2*q1)+b22*p2*q2))
out={'status':'PASS','exact_checks':checks,'arctan_rational_lower':str(atan_lower),'exp_rational_lower':str(exp_lower),'floating_point_used_as_proof':False,'scope':'Exact geometry, value-region, constant and polarization identities; full analytic reasoning is in TURN_4.md','full_candidate_pending_independent_review':True}
print(json.dumps(out,indent=2));Path(__file__).with_name('TURN_4_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
