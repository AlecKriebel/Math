#!/usr/bin/env python3
"""Exact controls for final partial bounds; not a stochastic percolation certificate."""
from fractions import Fraction as Q
import sympy as s
import json
n=0
def ck(x):
 global n
 assert bool(x);n+=1
q=Q(1,16);C=(1+q*q)/(1+q);eta=Q(1,100);Dmax=Q(32,257)
rho=2*Dmax/(1-eta)*((1+eta)/(1-eta))**4
ck(rho<Q(1,3));ck(q*q/(1+q)==Q(1,272));ck(Q(1,272)<Q(1,150))
ck(2/(1-q)+2*q*(1+q)/(1-q)**2==Q(514,225))
for M in range(2,31):
 residual=C*q**(M-1)*q*q/(1+q*q)
 ck(residual==q**(M+1)/(1+q));ck(residual/q**(M-1)==Q(1,272))
 bound=3*q**(M+1)/(1+q)+2*(1+C)*q**M/(1-q)
 ck(bound>0)
 ck(bound<5*q**M)
# Direct finite weighted Lyapunov-gradient identity, independently of stationarity.
for edges in [[(0,1),(1,2)],[(0,1),(1,2),(2,0)],[(0,1),(1,2),(2,3),(3,0)],[(0,1),(0,2),(0,3)]]:
 V=max(max(e) for e in edges)+1;xs=s.symbols('x:'+str(len(edges)),positive=True);ps=s.symbols('p:'+str(V),positive=True)
 sums=[sum(xs[i]**2 for i,e in enumerate(edges) if v in e) for v in range(V)]
 L=-sum(xs)+sum(ps[v]*s.log(sums[v])/2 for v in range(V))
 for i,e in enumerate(edges):
  F=-xs[i]+sum(ps[v]*xs[i]**2/sums[v] for v in e)
  ck(s.cancel(xs[i]*s.diff(L,xs[i])-F)==0)
print(json.dumps({'status':'PASS','exact_assertions':n,'relative_box':'1/100','endpoint_relative_residual':'1/272','contraction_lower_bound':'2/3','total_rate':'514/225','finite_tail_bound':'less than 5*(1/16)^M for M>=2','stochastic_percolation_claimed':False},indent=2))
