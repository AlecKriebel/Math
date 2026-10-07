#!/usr/bin/env python3
"""Algebra/finite consistency checks, not a proof verifier or PDE solver."""
import argparse,json,random,math
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--mutate',choices=['proximal-sign','pressure-sign','omit-vacuum','freeze-scale']);a=p.parse_args()
checks=[]
def check(name,condition):
    checks.append(name)
    if not condition:raise AssertionError(name)
# Exact Barenblatt signed-pressure equation in several rational dimensions/exponents.
t,z,A=s.symbols('t z A',positive=True)
for d in (1,2,3,5):
 for m in (s.Rational(3,2),s.Integer(2),s.Rational(5,2),s.Integer(3),s.Integer(5)):
  b=1/(d*(m-1)+2);l=d*b*(m-1);q=A*t**(-l)-b*z/(2*t)
  residual=s.diff(q,t)-b*b*z/t**2+(m-1)*q*d*b/t
  check(f'barenblatt-pressure:d={d},m={m}',s.simplify(residual)==0)
# Pointwise cancellation (6.5), before integration.
r,U,q,P,h,R,m=s.symbols('r U q P h R m')
g=(m-1)*q*h-R
lhs=-(m-1)*U*h+r*g-(m-1)*P*h
rhs=-(m-1)*(U-q*r+P)*h-r*R
if a.mutate=='pressure-sign':rhs=-(m-1)*(U-q*r+P)*h+r*R
check('signed-relative-energy-cancellation',s.expand(lhs-rhs)==0)
# Exact compactly supported 1D proximal density, x=0, eps=1/3, m=2.
y=s.symbols('y');eps=s.Rational(1,3);density=s.Rational(3,4)*(1-y*y)
check('proximal-density-mass',s.integrate(density,(y,-1,1))==1)
first=s.integrate(y*y*density/eps,(y,-1,1));pressure=s.integrate(density*density,(y,-1,1))
if a.mutate=='proximal-sign':pressure=-pressure
check('proximal-first-variation-sign',first==pressure)
# Fenchel positivity and domination of the vacuum residual.
rng=random.Random(30004633)
for k in range(300):
 m=1.05+rng.random()*4.95;qv=-3+6*rng.random();rv=10**(-8+10*rng.random())
 rho=(((m-1)/m)*max(qv,0))**(1/(m-1))
 ev=rv**m/(m-1)-qv*rv+rho**m
 check(f'fenchel-nonnegative:{k}',ev>=-1e-9*(1+rv**m))
 if qv<0:check(f'vacuum-linear-control:{k}',ev+1e-12>=(-qv)*rv)
rv=1e-9;qv=-1.;ev=rv*rv-qv*rv
if a.mutate=='omit-vacuum':ev=rv*rv
check('vacuum-term-is-essential',rv<=ev)
# Projection identity with weighted cells and nonconstant proximal maps.
for k in range(100):
 xs=[rng.uniform(-3,3) for _ in range(4)];ys=[[rng.uniform(-3,3) for _ in range(3)] for _ in range(4)]
 weights=[rng.random()+.1 for _ in range(4)];sw=sum(weights);weights=[w/sw for w in weights]
 eps=.1+rng.random();u=lambda x:math.sin(x)
 bary=[sum(v)/3 for v in ys];vel=[(b-x)/eps for b,x in zip(bary,xs)]
 lhs=-sum(w*v*u(x) for w,v,x in zip(weights,vel,xs))
 rhs=sum(w*sum((x-y)*u(x)/eps for y in cell)/3 for w,x,cell in zip(weights,xs,ys))
 check(f'weighted-projection-identity:{k}',abs(lhs-rhs)<1e-12)
# Frozen displacement with a constant velocity; exact Young-bound scaling.
eps=.01;dt=.003;V=2.;u=1.;F=dt*V*u/eps;bound=dt*(V*V+u*u)/(2*eps)
if a.mutate=='freeze-scale':bound*=eps
check('frozen-defect-epsilon-scaling',F<=bound)
# Energy upper bound versus reference map: node resets are minima.
for k in range(100):
 old=rng.random()*10;trials=[old]+[rng.random()*20 for _ in range(20)]
 new=min(trials)
 check(f'node-minimum-downward:{k}',new<=old)
result={'status':'PASS','checks':len(checks),'kind':'symbolic and finite consistency checks only','mutation':a.mutate}
print(json.dumps(result,sort_keys=True))
