#!/usr/bin/env python3
"""Exact checks for the authored partial results; requires SymPy."""
import sympy as s

t,R,a,d,e,alpha,beta=s.symbols('t R a d e alpha beta',real=True)
B=s.cos(t)+s.sin(t); C=s.cos(t)*s.sin(t)
H=s.sin(t)+1-s.cos(t); J=s.sin(t)**2/2
assert s.trigsimp(s.diff(H,t)-B)==0
assert s.trigsimp(s.diff(J,t)-C)==0
assert s.integrate(C*H,(t,0,2*s.pi))==0
assert s.integrate(C*H**2,(t,0,2*s.pi))==-s.pi/2
Q=s.pi*R*(-2*alpha+beta*R**2-R**4/2)
assert s.expand(Q.subs({alpha:s.Rational(1,2),beta:2})-s.pi*R*(-1+2*R**2-R**4/2))==0
z=-d/(2*a)+(e-a*d)*s.cos(2*t)/(2*(a*a+1))-(d+a*e)*s.sin(2*t)/(2*(a*a+1))
assert s.trigsimp(s.diff(z,t)+2*a*z+2*(d*s.cos(t)**2+e*s.sin(t)*s.cos(t)))==0
assert s.factor((e-a*d)**2+(d+a*e)**2)==(a*a+1)*(d*d+e*e)
# Verify the reciprocal-difference identity algebraically for independent radii.
r1,r2,b,c=s.symbols('r1 r2 b c',nonzero=True)
f=lambda r:a*r+b*r*r+c*r**3
lhs=s.factor((f(r2)-f(r1))/(r2-r1)-f(r1)/r1-f(r2)/r2)
assert s.simplify(lhs-(-a+c*r1*r2))==0
# Schwarzian flow identity: w'=f_r w, v'=f_rr w^2+f_r v,
# q'=f_rrr w^3+3 f_rr w v+f_r q.
w,v,q,fr,frr,frrr=s.symbols('w v q fr frr frrr',nonzero=True)
Sch=q/w-s.Rational(3,2)*(v/w)**2
flow=s.diff(Sch,w)*fr*w+s.diff(Sch,v)*(frr*w*w+fr*v)+s.diff(Sch,q)*(frrr*w**3+3*frr*w*v+fr*q)
assert s.simplify(flow-frrr*w*w)==0
print('PASS: reciprocal linearization, moments, two-cycle leading polynomial, pair identity, Schwarzian identity')
