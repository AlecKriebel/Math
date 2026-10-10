"""Exact symbolic controls for a nonconvex admissible single-barrier prefix."""
import sympy as s
import json
th=s.symbols('theta',real=True);h=th+s.sin(10*th)/20;r=s.exp(h)
x=r*s.cos(th);y=r*s.sin(th);checks=0
def zero(v):
 global checks
 assert s.simplify(s.trigsimp(v))==0;checks+=1
cur=s.diff(x,th)*s.diff(y,th,2)-s.diff(y,th)*s.diff(x,th,2)
expected=1+s.diff(h,th)**2-s.diff(h,th,2)
zero(cur/r**2-expected)
zero(expected.subs(th,s.pi/20)-7);zero(expected.subs(th,3*s.pi/20)+3)
zero(s.diff(x,th).subs(th,0)-s.Rational(3,2));zero(s.diff(y,th).subs(th,0)-1)
q=s.symbols('q',real=True);zero(5*q*q-(1+q*q)-(2*q-1)*(2*q+1))
for k in range(101):
 z=s.Rational(1,2)+s.Rational(k,100)
 assert 1+1/(z*z)<=5;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'curvature_factor_values':[7,-3],'initial_theta_derivative':['3/2','1'],'clock_bound_squared':5,'construction_speed':3,'limitations':'Admissible nonconvex prefix only. No confining barrier or minimizer is certified.'},indent=2))
