#!/usr/bin/env python3
"""Finite/numerical pinning-identity checks; not a general proof verifier."""
import argparse,math,random,json,itertools
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--mutate',choices=['mass-scale','kkt-sign','covariance-sign']);a=p.parse_args()
count=0
def check(name,v):
 global count
 count+=1
 if not v:raise AssertionError(name)
z=s.symbols('z');f=3-48*z*z;c=s.Rational(1,192)
check('exact-m2-d1-mass',s.integrate(f,(z,-s.Rational(1,4),s.Rational(1,4)))==1)
P=s.integrate(f*f,(z,-s.Rational(1,4),s.Rational(1,4)))
C=s.integrate(z*z*f,(z,-s.Rational(1,4),s.Rational(1,4)))/c
if a.mutate=='covariance-sign':C=-C
check('quadratic-test-exact-cancellation',P==C==s.Rational(12,5))
rng=random.Random(3000463305);aa=.25
for d,m,n in itertools.product((1,2,3),(1.5,2.,3.,4.),(2,3,5)):
 power=1/(m-1)
 I=math.pi**(d/2)*aa**(d+2*power)*math.gamma(power+1)/math.gamma(power+1+d/2)
 c=(m-1)/(2*m)*I**(m-1)
 mass=((m-1)/(2*m*c))**power*I
 if a.mutate=='mass-scale':mass*=2
 check(f'normalization:{d},{m},{n}',abs(mass-1)<1e-12)
 ell=aa*aa/(2*c);h=1/n;eps=c*h*h
 pressure=(math.pi**(d/2)*aa**(d+2*(power+1))*math.gamma(power+2)/math.gamma(power+2+d/2))/I**m
 cov=aa*aa/(c*(d+2*power+2))
 check(f'virial:{d},{m},{n}',abs(pressure-cov)<1e-10*(1+pressure))
 check(f'scaling-exclusion:{d},{m},{n}',abs((d*h*h/12)/eps-d/(12*c))<1e-10*(1+d/(12*c)))
 centers=[tuple((j+.5)*h for j in idx) for idx in itertools.product(range(n),repeat=d)]
 for sample in range(60):
  y=tuple(rng.uniform(-.1,1.1) for _ in range(d))
  costs=[sum((xj-yj)**2 for xj,yj in zip(x,y))/(2*eps) for x in centers]
  minimum=min(costs);uprime=max(ell-minimum,0)
  for ci in costs:
   lhs=ci+uprime
   if a.mutate=='kkt-sign':lhs=ci-uprime
   check(f'kkt:{d},{m},{n},{sample}',lhs>=ell-1e-10*(1+ell))
print(json.dumps({'status':'PASS','checks':count,'kind':'finite numerical and exact symbolic consistency only','mutation':a.mutate},sort_keys=True))
