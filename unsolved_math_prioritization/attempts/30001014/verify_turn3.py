#!/usr/bin/env python3
"""Finite free-word and mapping-torus boundary controls; no nonminimal norm simulation."""
from fractions import Fraction as F
from itertools import product
import json
checks=0
def ok(x):
 global checks
 assert x
 checks+=1
def reduce(w):
 s=[]
 for a in w:
  if s and s[-1]==-a:s.pop()
  else:s.append(a)
 return tuple(s)
def power(k):return (1,)*k if k>=0 else (-1,)*(-k)
words={()}
for length in range(1,6):
 for w in product((1,-1,2,-2),repeat=length):words.add(reduce(w))
for w in sorted(words):
 orbit=[reduce(power(n)+w) for n in range(-12,13)]
 ok(len(set(orbit))==25)
 for n,z in zip(range(-12,12),orbit[:-1]):ok(reduce((1,)+z)==reduce(power(n+1)+w))
f=lambda t:max(F(0),1-4*abs(t-F(1,2)))
ok(f(F(0))==0);ok(f(F(1))==0);ok(f(F(1,2))==1)
for i,j in product(range(21),repeat=2):
 t,s=F(i,20),F(j,20);ok(0<=f(t)*f(s)<=1)
 if i in (0,20) or j in (0,20):ok(f(t)*f(s)==0)
# Finite permutation analogues of the twisted boundary rule.
for n in range(1,41):
 v=[F(i*i-3*i+1,7) for i in range(n)];theta=lambda a:[a[(i-1)%n] for i in range(n)]
 end=theta(v)
 for i in range(n):ok(end[i]==v[(i-1)%n])
 for t in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
  section=[(1-t)*a+t*b for a,b in zip(v,end)]
  if t==0:ok(section==v)
  if t==1:ok(section==end)
print(json.dumps({'status':'PASS','assertions':checks,'reduced_words':len(words),'scope':'Finite orbit, bump and boundary identities only; ideal tensor injectivity, kernel detection and connectedness are proved analytically'},indent=2,sort_keys=True))
