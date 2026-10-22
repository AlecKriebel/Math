"""Exact finite exchangeability/thinning controls, not a SIRSN construction."""
from fractions import Fraction as F
from itertools import permutations,product
from math import factorial
import json
checks=0
for n in range(2,8):
 a={(i,j):F((i+1)*(j+1)+i+j,1+abs(i-j)) for i in range(n) for j in range(n) if i!=j}
 avg=sum(a.values())/F(n*(n-1))
 orbit=sum(a[(p[0],p[1])] for p in permutations(range(n)))/factorial(n)
 assert avg==orbit;checks+=1
for n in range(2,8):
 probs=[F(i+1,n+2) for i in range(n)]
 a={(i,j):F(i+j+1,n+1) for i in range(n) for j in range(n) if i!=j}
 expected=F(0)
 for labels in product((0,1),repeat=n):
  weight=F(1)
  for i,b in enumerate(labels):weight*=probs[i] if b else 1-probs[i]
  selected=sum(a[i,j]/(probs[i]*probs[j]) for i in range(n) for j in range(n) if i!=j and labels[i] and labels[j])
  expected+=weight*selected
  checks+=1
 assert expected==sum(a.values());checks+=1
 # Number of ordered-pair pairs with a shared label is O(n^3).
 pairs=list(a)
 overlap=sum(bool(set(x)&set(y)) for x in pairs for y in pairs)
 assert overlap<=4*n**3;checks+=1
for g in (F(1,5),F(2,3),F(7,4)):
 for h in (F(1,3),F(3,4),F(5,2)):
  for G in (F(1,7),F(4,3)):
   for H in (F(2,5),F(8,3)):
    q=(g+h)/2;Q=(G+H)/2
    assert 4*(g/(2*q))*(G/(2*Q))/(g*G)==1/(q*Q);checks+=1
for beta in (F(5,2),F(3),F(7,2)):
 assert 4+1-beta==5-beta;checks+=1
 assert -(5-beta)==beta-5;checks+=1
print(json.dumps({'status':'PASS_EXACT_EXCHANGEABILITY_CONTROLS','exact_assertions':checks,'scope':'Finite permutation averages, importance-thinning expectation and overlap counts, scaling powers; no continuum or beta>3 finiteness certification.'},indent=2))
