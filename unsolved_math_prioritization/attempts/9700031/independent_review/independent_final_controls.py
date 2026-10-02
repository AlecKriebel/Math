#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product,permutations
from math import factorial
import json
n=0
# Arbitrary asymmetric pair array: finite group average still matches ordered average.
for k in range(2,8):
 a={(i,j):F(7*i-3*j+i*j+11,(i+1)*(j+1)) for i in range(k) for j in range(k) if i!=j}
 assert sum(a.values())/k/(k-1)==sum(a[p[0],p[1]] for p in permutations(range(k)))/factorial(k);n+=1
# Importance thinning under strongly unequal probabilities, independently enumerated.
for k in range(2,9):
 probs=[F(1,2**(i+1)) for i in range(k)]
 a={(i,j):F((i+2)*(j+3),i+j+1) for i in range(k) for j in range(k) if i!=j}
 expected=F(0)
 for bits in product([0,1],repeat=k):
  weight=F(1)
  for i,b in enumerate(bits):weight*=probs[i] if b else 1-probs[i]
  expected+=weight*sum(a[i,j]*bits[i]*bits[j]/probs[i]/probs[j] for i,j in a);n+=1
 assert expected==sum(a.values());n+=1
 # Overlap fraction vanishes, rather than incorrectly assuming all pairs independent.
 overlap=sum(1 for i,j in a for v,w in a if {i,j}&{v,w})
 assert overlap==k*(k-1)*(4*k-6);n+=1
# Scalar heavy-tail truncations, including large marks rather than only small u.
for N in range(1,13):
 p={2**j:F(1,2**(j+1)*j*j) for j in range(1,N+1)};p[1]=1-sum(p.values());d=sum(x*w for x,w in p.items());assert d<2;n+=1
 for exponent in range(-3,2*N+3):
  u=F(2)**exponent
  for kexp in range(-2,N+3):
   K=F(2)**kexp
   h=sum(x*w for x,w in p.items() if x*x>u);tail=sum(x*w for x,w in p.items() if x>K)
   event=sum(w for x,w in p.items() if x*x>u and x<=K)
   assert h<=2*K*K/u+tail and event<=2*K/u;n+=2
print(json.dumps({'status':'PASS','independent_exact_assertions':n,'scope':'Finite permutation/unequal-thinning identities and heavy-mark scalar controls. No routing model, analytic proof certification or original counterexample.'},indent=2))
