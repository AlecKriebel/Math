#!/usr/bin/env python3
"""Exact exponent, parabolic-grid and killed-mass controls; not a simulation of the exit probability."""
from fractions import Fraction as F
from math import ceil
import json
checks=0

def ok(x):
 global checks
 assert x
 checks+=1
p=64;a=F(3,8);eps=F(1,32);gamma=F(5,4)
ok(F(1,2)-a-F(3,p)==F(5,64));ok(eps*p==2);ok(1-(gamma-1+eps)/a==F(1,4));ok(1/a<3)
for j in range(31):
 horizontal=(4**j+1)*2**j;vertical=4**j*(2**j+1)
 ok(horizontal+vertical<=4*8**j)
for i in range(1,50):
 q=F(i,100);amin=F(1,4)/(1-q);aa=(amin+F(1,2))/2
 ee=(aa*(1-q)-F(1,4))/2
 pp=ceil(max(F(3)/(F(1,2)-aa),q/ee,F(2)))+2
 ok(aa>amin);ok(aa<F(1,2)-F(3,pp));ok(ee>0);ok(ee*pp>=q);ok(1-(F(1,4)+ee)/aa>q)
# Radius/height identities for the concrete Hölder exponent 3/8.
for n in range(2,31):
 d=F(1,n**8);R=F(n**4);H=R/(2*F(1,n**3));x0=F(1,2)
 ok(H**8*d**3==(R/2)**8);ok(x0-d>=0);ok(x0+d<=1);ok(2*d*(R/2)==d*R)
 ok(H**8*x0**3>=R**8)
# Sub-Markov finite heat-walk powers preserve the unweighted mass inequality.
for n in range(1,17):
 P=[[F(abs(i-j)==1,2) for j in range(n)] for i in range(n)]
 v=[F((i+1)**2) for i in range(n)];initial=sum(v)
 for step in range(21):
  ok(all(x>=0 for x in v));ok(sum(v)<=initial)
  old=sum(v);v=[sum(P[i][j]*v[j] for j in range(n)) for i in range(n)];ok(sum(v)<=old)
print(json.dumps(dict(status='PASS',assertions=checks,general_tail_exponents=49,scope='finite exact controls; stopping times, conditional mass inequality and continuum chaining are proved analytically'),sort_keys=True,indent=2))
