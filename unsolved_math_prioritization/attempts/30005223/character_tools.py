#!/usr/bin/env python3
"""Exact locally authored character-table and residual-zero controls. No imported executable code."""
from functools import lru_cache
from collections import Counter
from fractions import Fraction
import math,json
C=Counter()
def ck(v,key):assert v,key;C[key]+=1
@lru_cache(None)
def parts(n,cap=None):
 if n==0:return ((),)
 if cap is None:cap=n
 return tuple((j,)+p for j in range(min(cap,n),0,-1) for p in parts(n-j,j))
@lru_cache(None)
def hooks(lam):
 return tuple(lam[i]-j+sum(row>j for row in lam[i+1:]) for i in range(len(lam)) for j in range(lam[i]))
@lru_cache(None)
def strip(lam,t):
 l=len(lam);B={lam[i]+l-1-i for i in range(l)};out=[]
 for b in B:
  a=b-t
  if a<0 or a in B:continue
  Bs=sorted(B-{b}|{a},reverse=True);nu=tuple(x-l+1+i for i,x in enumerate(Bs));nu=tuple(x for x in nu if x)
  sign=(-1)**sum(a<x<b for x in B);out.append((nu,sign))
 return tuple(out)
@lru_cache(None)
def character(lam,mu):
 if not mu:return int(not lam)
 return sum(e*character(nu,mu[1:]) for nu,e in strip(lam,mu[0]))
@lru_cache(None)
def paths(lam,mu):
 if not mu:return int(not lam)
 return sum(paths(nu,mu[1:]) for nu,e in strip(lam,mu[0]))
def centralizer(mu):
 c=Counter(mu);v=1
 for t,n in c.items():v*=t**n*math.factorial(n)
 return v
def types(lam,mu):
 hs=hooks(lam);I=not any(x%mu[0]==0 for x in hs);II=any(not any(x%t==0 for x in hs) for t in mu)
 III=any(sum(x//t for x in mu if x%t==0)>sum(x%t==0 for x in hs) for t in range(2,sum(mu)+1))
 return I,II,III
def mobius(n):
 sign=1;p=2
 while p*p<=n:
  if n%p==0:
   n//=p;sign=-sign
   if n%p==0:return 0
   while n%p==0:n//=p
  p+=1
 if n>1:sign=-sign
 return sign
