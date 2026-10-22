"""Own exact identity controls for the oscillatory initial-tangent example."""
import sympy as s
import json
from collections import Counter
C=Counter()
def ck(ok,k):
 assert ok,k
 C[k]+=1
t=s.symbols('t',positive=True)
h=t*(1+s.sin(s.log(t))/10)
hp=1+(s.sin(s.log(t))+s.cos(s.log(t)))/10
hpp=(s.cos(s.log(t))-s.sin(s.log(t)))/(10*t)
ck(s.simplify(s.diff(h,t)-hp)==0,'derivative_identity')
ck(s.simplify(s.diff(hp,t)-hpp)==0,'second_derivative_identity')
q=s.symbols('q',positive=True)
ck(s.simplify((1+1/q**2).subs(q,s.Rational(4,5)))==s.Rational(41,16),'speed_bound')
ck(s.Rational(41,16)<4,'strict_admissibility_constant')
phase=s.symbols('phase',real=True)
pp=1+(s.sin(phase)+s.cos(phase))/10
ck(pp.subs(phase,0)==s.Rational(11,10),'tangent_phase')
ck(pp.subs(phase,s.pi)==s.Rational(9,10),'tangent_phase')
ck((1+s.sin(phase)/10).subs(phase,s.pi/2)==s.Rational(11,10),'secant_phase')
ck((1+s.sin(phase)/10).subs(phase,3*s.pi/2)==s.Rational(9,10),'secant_phase')
ck(s.Rational(25,16)<3,'first_quadrant_bound')
for i in range(201):
 Q=s.Rational(4,5)+s.Rational(i,500)
 ck(1+1/Q**2<=s.Rational(41,16),'exact_slope_controls')
for n in range(23,101):
 # Phase-zero factor is negative whenever theta=1/n is small enough;
 # this algebraic control does not pretend log(1/n) is phase zero.
 ck(s.Rational(221,100)-s.Rational(n,10)<0,'negative_phase_factor')
 ck(s.Rational(181,100)+s.Rational(n,10)>0,'positive_phase_factor')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Exact identity controls for a nonoptimal, nonconfining admissible prefix. Analytic phase sequences prove nonexistence of its initial tangent. No original optimizer counterexample.'},indent=2,sort_keys=True))
