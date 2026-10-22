#!/usr/bin/env python3
"""Own exact checks of the partial deterministic construction; no stochastic simulation."""
from fractions import Fraction as F
import json
q=F(1,16);C=(1+q*q)/(1+q);tests=0

def ck(x):
 global tests
 assert x
 tests+=1

def rate(v):
 n,y=v
 if y:return q**(abs(n)+abs(y))
 if n:return C*q**(abs(n)-1)
 return 2*q/(1+q)

def edge(u,v):return tuple(sorted((u,v)))
def weight(e):
 u,v=e
 if u[1]==v[1]==0 and v[0]==u[0]+1:return q**min(abs(u[0]),abs(v[0]))
 if u[1]!=0 and u[1]==v[1] and u[0]%2==0 and v[0]==u[0]+1:return rate(u)+rate(v)
 return F(0)
def around(v):
 n,y=v
 return [edge(v,w) for w in [(n-1,y),(n+1,y),(n,y-1),(n,y+1)]]
def field(e):
 x=weight(e)
 return -x+sum(rate(v)*x*x/sum(weight(f)**2 for f in around(v)) for v in e)
maxD=F(0)
for n in range(-20,21):
 for y in range(-8,9):
  v=(n,y);ck(0<rate(v)<=1);ck(sum(weight(e)**2 for e in around(v))>0)
  for e in around(v):ck(field(e)==0)
for n in range(-30,31):
 e=edge((n,0),(n+1,0));x=weight(e);D=0
 for v in e:
  S=sum(weight(f)**2 for f in around(v));a=x*x/S
  D+=2*rate(v)/x*a*(1-a)
 ck(D==(F(17,257) if n in [-1,0] else F(32,257)))
 maxD=max(maxD,D)
eta=F(1,100);row_bound=2*maxD/(1-eta)*((1+eta)/(1-eta))**4
ck(row_bound<F(1,3));ck(1-2*maxD==F(193,257))
line_mass=2/(1-q);line_rate=2*q/(1+q)+2*C/(1-q);ck(line_mass==line_rate)
# Exact finite checks of polynomial-volume versus exponential tree generation.
for d in range(2,8):
 for n in [2,3,5]:
  for L in [1,2,4]:
   k=1
   while n**k<=(2*L*k+1)**d:k+=1
   ck(n**k>(2*L*k+1)**d)
print(json.dumps({'status':'PASS','exact_assertions':tests,'q':str(q),'line_rates_constant':str(C),'max_relative_Jacobian_D':str(maxD),'linear_contraction_rate':str(1-2*maxD),'relative_box_radius':str(eta),'nonlinear_row_correction_bound':str(row_bound),'certified_nonlinear_contraction_lower_bound':'2/3','line_total_weight':str(line_mass),'stochastic_survival_claimed':False},indent=2)+'\n',end='')
