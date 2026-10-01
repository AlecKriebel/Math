#!/usr/bin/env python3
"""Finite check of stated classification against explicit diagonal-action models.
Topology, disks and necessity are proved in TURN_5.md, not by this enumeration.
"""
from math import gcd
from functools import lru_cache
from collections import Counter
import json
C=Counter()
def ck(x,k):
 assert x,k
 C[k]+=1
@lru_cache(None)
def multisets(n,types):
 if n==0:return ((),)
 if not types:return ()
 d,s=types[0];out=[]
 for k in range(n//d+1):
  out.extend(((d,s),)*k+t for t in multisets(n-k*d,types[1:]))
 return tuple(out)
def abstract_types(m):
 return tuple(sorted([(d,1) for d in range(1,m+1) if m%d==0]+[(d,-1) for d in range(1,m+1) if m%(2*d)==0]))
def criterion(m,t):
 neg=[d for d,s in t if s<0];pos=[d for d,s in t if s>0];c1=pos.count(1);D=set(d for d in pos if 1<d<m)
 if not neg:
  if m==1:return all(d==1 for d in pos)
  if c1>=2:return not D
  if c1==1:return len(D)<=1
  return len(D)<=2 and (len(D)<2 or gcd(*(m//d for d in D))==1)
 if m%2 or any(d!=m//2 for d in neg):return False
 if m==2:return True
 if c1>1:return False
 if c1==1:return D<={m//2}
 extra=D-{m//2}
 return len(extra)<=1 and all((m//e)>1 and (m//e)%2==1 for e in extra)
@lru_cache(None)
def model_set(m,n):
 if m==1:return {((1,1),)*n}
 out=set()
 divisors=[d for d in range(1,m+1) if m%d==0]
 for k in divisors:
  for l in divisors:
   if gcd(k,l)!=1:continue
   for coordinate in ('none','A','B'):
    initial=() if coordinate=='none' else ((1,1),)
    if len(initial)>n:continue
    choices={(m,1)}
    for axis,stabilizer in [('A',k),('B',l)]:
     if coordinate==axis or stabilizer==1:continue
     choices.add((m//stabilizer,1))
     if stabilizer==2:choices.add((m//2,-1))
    for t in multisets(n-len(initial),tuple(sorted(choices))):out.add(tuple(sorted(initial+t)))
 return out
rows=[]
for m in range(1,31):
 for n in range(11):
  actual=set(multisets(n,abstract_types(m)))
  formal={t for t in actual if criterion(m,t)}
  models=model_set(m,n)
  ck(formal==models,'all_enumerated_patterns_match_explicit_models')
  for t in models:ck(t in actual,'constructed_model_respects_domain_order')
  rows.append({'m':m,'n':n,'admitted':len(formal),'abstract':len(actual)})
# Stabilizer inclusion plus an equivariant-disk fixed-point forces equality.
for m in range(2,101):
 for d in range(2,m):
  if m%d:continue
  for e in range(1,m+1):
   if m%e:continue
   H={(d*j)%m for j in range(m//d)}
   if d%e==0 and e%m in H:ck(d==e,'axis_disk_double_divisibility')
# Examples distinguish this result from the weaker preceding filters.
examples=[(18,[(9,-1),(6,1),(2,1)]),(12,[(3,1),(6,1)]),(6,[(1,1),(2,1),(3,1)]),(4,[(1,1),(1,1),(2,1)])]
for m,t in examples:
 ck(all(m%(d*(2 if s<0 else 1))==0 for d,s in t),'excluded_example_abstract')
 ck(not criterion(m,t),'new_ambient_exclusion')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'tested_domain_orders':'1 through30','tested_component_counts':'0 through10','pattern_counts':rows,'scope':'Finite arithmetic equivalence with explicit diagonal-action local-circle models only. Equivariant Dehn hypotheses, disk argument, unlink constructions and the original hyperbolic completion gap require the written proof.'},indent=2))
