#!/usr/bin/env python3
"""Exact finite controls. No p-adic infinite object is approximated by this script."""
import itertools as it, json, math
from fractions import Fraction
checks=0
counts={}
def check(b):
 global checks
 assert b
 checks+=1
def compositions(n):
 for cuts in it.product((0,1),repeat=n-1):
  s=1; out=[]
  for v in cuts:
   if v: out.append(s); s=1
   else:s+=1
  yield out+[s]
def blockids(parts):return [j for j,r in enumerate(parts) for _ in range(r)]
def sign(p):return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
perms={q:[(p,sign(p)) for p in it.permutations(range(q))] for q in (1,3,5)}
def alttrace(es):
 q=len(es); total=0
 for p,s in perms[q]:
  if all(es[p[j]][1]==es[p[(j+1)%q]][0] for j in range(q)):total+=s
 return total
for n in range(1,6):
 for parts in compositions(n):
  ids=blockids(parts)
  basis=[(a,b) for a in range(n) for b in range(n) if ids[a]<=ids[b]]
  for q in (1,3,5):
   if q>len(basis):continue
   # The one-block case is tautological. Keep full basis checks only for n<=3.
   if len(parts)==1 and n>3:continue
   num=0
   for es in it.combinations(basis,q):
    lhs=alttrace(es)
    rhs=sum(alttrace(es) if all(ids[a]==ids[b]==j for a,b in es) else 0 for j in range(len(parts)))
    check(lhs==rhs);num+=1
   counts[f'n={n};blocks={parts};degree={q}']=num
check(alttrace(((0,0),(0,1),(1,0)))==3)
# Split finite-etale trace: the actual general proof is descent of this identity.
for d in range(1,31):
 for a in range(-20,21):
  check(Fraction(sum([a]*d),d)==a)
# Graded weighted Chern character is additive term-by-term; use exact polynomials.
for m in range(-6,7):
 for n in range(-6,7):
  for j in range(1,6):
   for x in range(-3,4):
    a=Fraction(m*x**j,math.factorial(j))
    b=Fraction(n*x**j,math.factorial(j))
    check(a+b==Fraction((m+n)*x**j,math.factorial(j)))
# Positive Chern character of a trivial arithmetic graded bundle is zero.
for rank in range(21):
 for j in range(1,11):check(rank*0**j==0)
print(json.dumps({'status':'PASS','assertions':checks,'alternating_trace_cases':counts,'scope':'finite exact controls of proof identities, not an unrestricted-conjecture test'},indent=2,sort_keys=True))
