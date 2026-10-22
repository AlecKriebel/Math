#!/usr/bin/env python3
"""Exact finite normalization controls; not an existence or limit proof.
Requires SymPy from its standard package distribution. No source code imported.
"""
import json
from fractions import Fraction as Q
from math import factorial
import sympy as s
checks=0
def eq(a,b):
    global checks
    assert s.simplify(s.sympify(a-b).rewrite(s.exp))==0,(a,b)
    checks+=1
x,xb,r,H,k,a,R,h=s.symbols('x xb r H k a R h',nonzero=True)
A=s.Matrix([[0,1],[x,0]])
Ad=s.Matrix([[0,xb/H**2],[H**2,0]])
comm=A*Ad-Ad*A
for z,w in zip(comm,s.diag(H**2-x*xb/H**2,-H**2+x*xb/H**2)):eq(z,w)
eq((H**2-r**2/H**2).subs(H,s.sqrt(r)*s.exp(h)),2*r*s.sinh(2*h))
# Original holomorphic frame to the unitary fiducial frame.
g=s.diag(H**s.Rational(-1,2),H**s.Rational(1,2))
for z,w in zip(g.inv()*A*g,s.Matrix([[0,H],[x/H,0]])):eq(z,w)
for z,w in zip(g*s.diag(H,1/H)*g,s.eye(2)):eq(z,w)
# R=a^3, epsilon=a^2, H_11=a^-1 k: exact adjoint scaling.
for z,w in zip((a**6*Ad).subs(H,k/a),s.Matrix([[0,xb*a**8/k**2],[a**4*k**2,0]])):eq(z,w)
# The scalar radial equation and rho substitution have the exact factor 1/2.
z=s.symbols('z',positive=True); f=s.Function('f')
rho=s.Rational(8,3)*R*r**s.Rational(3,2)
q=f(rho)
lhs=s.expand(r**2*s.diff(q,r,2)+r*s.diff(q,r))
expected=s.Rational(9,4)*(rho**2*s.Subs(s.diff(f(z),z,2),z,rho)+rho*s.Subs(s.diff(f(z),z),z,rho))
eq(lhs,expected)
eq(8*R**2*r**3/(s.Rational(9,4)*rho**2),s.Rational(1,2))
# Ramified eigenvectors and their Hermitian Gram matrix.
t,tb=s.symbols('t tb',nonzero=True)
V=s.Matrix([[1,1],[t,-t]]); Vstar=s.Matrix([[1,tb],[1,-tb]])
for z,w in zip(A.subs(x,t*t)*V,V*s.diag(t,-t)):eq(z,w)
G=Vstar*s.diag(H,1/H)*V
for z,w in zip(G,s.Matrix([[H+t*tb/H,H-t*tb/H],[H-t*tb/H,H+t*tb/H]])):eq(z,w)
for z,w in zip(G.subs(tb,r/t).subs(H,s.sqrt(r)*s.exp(h)),2*s.sqrt(r)*s.Matrix([[s.cosh(h),s.sinh(h)],[s.sinh(h),s.cosh(h)]])):eq(z,w)
# Basepoint and Bergman-kernel coordinate change s=-2/t.
t0,t1,t2,q0,q1=s.symbols('t0 t1 t2 q0 q1',nonzero=True)
eq((2/t0**2)*(2/t1**2)/(-2/t0+2/t1)**2,1/(t0-t1)**2)
eq(4/(-2/t)**2,t*t);eq(-2/(-2/t),t)
# EO differentials: dt signs incorporated in scalar coefficients.
K=1/(4*t*(t0*t0-t*t))
w03=s.residue(K*(-1/(t-t1)**2/(-t-t2)**2-1/(t-t2)**2/(-t-t1)**2),t,0)
w11=s.residue(K*(-1/(4*t*t)),t,0)
eq(w03,-1/(2*t0**2*t1**2*t2**2));eq(w11,-1/(16*t0**4))
eq(s.Rational(1,12)+s.Rational(1,48),s.Rational(5,48))
eq(s.Rational(1,24)+s.Rational(7,192),s.Rational(5,64))
# Riccati coefficients independently compared with logarithm of the Airy amplitude.
N=20
c=[Q(1)]
for n in range(1,N+1):
    c.append(-Q(1,2)*(Q(4-3*n,2)*c[n-1]+sum((c[i]*c[n-i] for i in range(1,n)),Q(0))))
    eq(2*c[n]+Q(4-3*n,2)*c[n-1]+sum((c[i]*c[n-i] for i in range(1,n)),Q(0)),0)
amp=[Q(1)]
for j in range(N):amp.append(amp[-1]*Q((6*j+1)*(6*j+5),48*(j+1)))
# log(A)'=A'/A yields an independent triangular formula for log coefficients.
log=[Q(0)]
for j in range(1,N+1):
    log.append(amp[j]-sum((Q(i,j)*log[i]*amp[j-i] for i in range(1,j)),Q(0)))
for j in range(1,N):eq(log[j],Q(2, -3*j)*c[j+1])
eq(c[1],Q(-1,4));eq(c[2],Q(-5,32));eq(log[1],Q(5,48));eq(log[2],Q(5,64))
# Airy differential equation coefficient recurrence for its amplitude.
# Let psi=e^(2t^3/3hbar)t^-1/2 A(hbar/t^3), x=t^2.
# Substitution gives a_(j+1)/a_j=(6j+1)(6j+5)/(48(j+1)).
for j in range(N):eq(48*(j+1)*amp[j+1]-(6*j+1)*(6*j+5)*amp[j],0)
# Exact negative controls: wrong EO pullback sign and wrong small-R scaling fail.
assert w11 != 1/(16*t0**4);checks+=1
assert (a**6*Ad[1,0]).subs(H,k/a) != a**6*k*k;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'riccati_orders':N,
    'first_stable_coefficients':[str(log[1]),str(log[2])],
    'scope':'Finite algebra and normalization only. Radial existence, smooth asymptotics and all-order EO/DM theorem are sourced analytic inputs; no numerical or Stokes convergence claim.'},indent=2,sort_keys=True))
