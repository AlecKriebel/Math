#!/usr/bin/env python3
"""Modest exact-symbolic structure checks for the candidate's density chain.

This checks exponent/scaling identities only; it does not certify infinite-dimensional
measure theory, associativity, regularity, or the proposed counterexample.
"""
import json

def ordinal_sum(a,b):
    n,m=a; p,q=b
    return (n+p,q) if p else (n,m+q)

checks=0
for n in range(4):
 for m in range(4):
  for p in range(4):
   for q in range(4):
    for r in range(4):
     for h in range(4):
      a,b,c=(n,m),(p,q),(r,h)
      assert ordinal_sum(ordinal_sum(a,b),c)==ordinal_sum(a,ordinal_sum(b,c))
      checks+=1

# q_k(v; prepend_l(w,y)) uses d(prepend_l(w,y))=2**l*d(y).
# Its scales 2**(k-j+l)*d are precisely the first k scales of q_(k+l).
for k in range(12):
 for l in range(12):
  direct=list(range(k+l,0,-1))
  chained=[k-j+l for j in range(k)]+[l-j for j in range(l)]
  assert direct==chained
  checks+=1
print(json.dumps({'passed':True,'finite_identity_checks':checks,
 'scope':'Ordinal addition and Gaussian density scale chain only; no proof certification.'},indent=2))
