#!/usr/bin/env python3
"""Exact scalar and finite-rank controls for the final author turn."""
from fractions import Fraction as Q
import json
count=0
def check(x):
 global count
 assert x
 count+=1
# Real controls of the complex-ratio triangle bound (the proof itself is complex).
for den in range(3,22):
 eps=Q(1,den)
 for b in (Q(1,7),Q(2,3),Q(5,4)):
  for e in (-eps,0,eps):
   for f in (-eps,0,eps):
    check(1+e>0)
    check(abs(b*(1+f)/(1+e)-b)<=4*b*eps)
# Balance equations and the exact condition for a logarithmic compatible window.
for aint in range(1,37):
 a=Q(aint,7)
 for sint in range(0,aint):
  sig=Q(sint,7); c=2/(a+sig); tau=(a-sig)/(a+sig)
  check(tau>0)
  check(a*c-1==tau)
  check(1-sig*c==tau)
  check(a*c>tau)
# Direct matrix-vector iteration of the compact clock model; independently compare formula.
for L in range(1,45):
 for rho,sigma in ((Q(1,4),Q(1,2)),(Q(2,7),Q(5,7)),(Q(3,8),Q(7,8))):
  f=[(rho/sigma)**j for j in range(L+1)]
  last=None
  for m in range(2*L+9):
   u=f[0]; formula=rho**min(m,L)*sigma**max(0,m-L)
   check(u==formula)
   check(0<u<=sigma**m)
   if last is not None:check(u/last==(rho if m-1<L else sigma))
   last=u
   f=[sigma*f[j+1] for j in range(L)]+[sigma*f[L]]
  # Sum of the whole exactly geometric tail, not just a truncated numerical sum.
  total=sum(rho**m for m in range(L))+rho**L/(1-sigma)
  check(total<=1/(1-sigma))
print(json.dumps({'status':'PASS','assertions':count,'coverage':['ratio perturbation constants','growth-envelope exponent balance','direct finite-rank clock iterations and full summability bound'],'scope':'Finite exact controls; no effective PDE remainder constants are inferred.'},indent=2,sort_keys=True))
