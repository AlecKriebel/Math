#!/usr/bin/env python3
"""Exact mollification, killed-heat matrix and scaling controls; no SPDE simulation."""
from fractions import Fraction as F
import json
checks=0

def ok(x):
 global checks
 assert x
 checks+=1

def g(x):return min(x,F(1))
def G(x):return x*x/2 if x<=1 else x-F(1,2)
def a(x):return abs(x)
def A(x):return x*abs(x)/2
for fun,primitive in [(g,G),(a,A)]:
 for eps in [F(1,2**k) for k in range(1,9)]:
  smooth=lambda x:(primitive(x+eps)-primitive(x-eps)-primitive(eps)+primitive(-eps))/(2*eps)
  ok(smooth(F(0))==0)
  xs=[F(i,37) for i in range(-111,112)]
  for x in xs:
   ok(abs(smooth(x)-fun(x))<=eps);ok(abs(smooth(x))<=abs(x))
   derivative=(fun(x+eps)-fun(x-eps))/(2*eps);ok(abs(derivative)<=1)
  for x,y in zip(xs,xs[1:]):ok(abs(smooth(y)-smooth(x))<=y-x)
for n in range(1,14):
 P=[[F(abs(i-j)==1,2) for j in range(n)] for i in range(n)]
 Q=[[F(i==j) for j in range(n)] for i in range(n)]
 for power in range(12):
  for row in Q:ok(all(x>=0 for x in row));ok(sum(row)<=1)
  Q=[[sum(Q[i][k]*P[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
for N in range(2,33):
 h=F(1,N)
 for gamma in [F(1,3),F(1),F(7,2)]:
  for j in range(1,17):
   tau=gamma*h*h/j;ok((tau/h)**2<=gamma*tau)
   c=gamma/F(j);ok(c*h*h==tau)
  for q in range(1,9):
   for f in [F(-2,3),F(0),F(1,5),F(1)]:
    tau=h*h;gaussian_exponent=(q*q-q)*N*f*f*tau/2
    ok(gaussian_exponent==F(q*(q-1),2)*N*f*f*tau)
    if q==1:ok(gaussian_exponent==0)
print(json.dumps(dict(status='PASS',assertions=checks,scope='finite exact coefficient, semigroup and scaling controls; published analytic estimates and approximation bridge are not simulations'),indent=2,sort_keys=True))
