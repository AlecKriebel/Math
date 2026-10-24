#!/usr/bin/env python3
"""Exact torsion zeros, after a separate universal order-210 reduction."""
from pathlib import Path
import json
from math import gcd

def div(a,b):
 a=a[:]
 while len(a)>1 and a[-1]==0:a.pop()
 out=[0]*max(1,len(a)-len(b)+1)
 for i in range(len(a)-len(b),-1,-1):
  c=a[i+len(b)-1];assert b[-1]==1;out[i]=c
  for j,x in enumerate(b):a[i+j]-=c*x
 assert not any(a)
 while len(out)>1 and not out[-1]:out.pop()
 return out

def cyclo(n,memo={}):
 if n in memo:return memo[n]
 a=[-1]+[0]*(n-1)+[1]
 for d in range(1,n):
  if n%d==0:a=div(a,cyclo(d))
 memo[n]=a;return a

def powers(n,poly):
 deg=len(poly)-1;out=[];v=[1]+[0]*(deg-1)
 for k in range(n):
  out.append(v[:]);c=v[-1];v=[0]+v[:-1]
  for j,x in enumerate(poly[:-1]):v[j]-=c*x
 assert v==out[0]
 return out

def run():
 n=210;prime=421;g=next(x for x in range(2,prime) if pow(x,n,prime)==1 and all(pow(x,n//p,prime)!=1 for p in (2,3,5,7)))
 pol=cyclo(n);assert sum(c*pow(g,i,prime) for i,c in enumerate(pol))%prime==0;pw=powers(n,pol);modpw=[pow(g,k,prime) for k in range(n)];out=[]
 for row in json.loads(Path(__file__).with_name('dihedral_determinants.json').read_text()):
  terms=[(tuple(t['exponent']),t['coefficient']) for t in row['terms']];surv=[];zeros=[]
  for a in range(n):
   for b in range(n):
    inds=[((e[0]*a+e[1]*b)%n,c) for e,c in terms]
    if sum(modpw[k]*c for k,c in inds)%prime:continue
    surv.append([a,b]);v=[0]*(len(pol)-1)
    for k,c in inds:
     for j,x in enumerate(pw[k]):v[j]+=c*x
    if not any(v):zeros.append([a,b])
  out.append({'types':row['types'],'modular_survivors':len(surv),'exact_zero_exponents':zeros})
 return {'order_bound':n,'modular_prime':prime,'primitive_root_image':g,'cyclotomic_polynomial_low_to_high':pol,'results':out,'scope':'All torsion zeros only after the rank-index partition bound has been independently validated. Singular matrix kernels still require separate analysis.'}
if __name__=='__main__':
 out=run();Path(__file__).with_name('dihedral_torsion_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
