"""Exact finite diagnostics for a piece-rotation argument, not Brownian simulation."""
from itertools import product
from fractions import Fraction
from collections import Counter
import json
from pathlib import Path
allwords=list(product((-1,1),repeat=3))
def piece(w,rule):
 if rule=='fixed2':return w[:2]
 level=1 if rule=='up' else -1
 x=0
 for i,e in enumerate(w,1):
  x+=e
  if x==level:return w[:i]
 return w
patterns=[('down',)*4,('up','down','up','down'),('fixed2','down','up','fixed2')]
cases=0;maxerror=0;prefix_checks=0
for pattern in patterns:
 counts=Counter()
 for words in product(allwords,repeat=4):
  pieces=[piece(w,r) for w,r in zip(words,pattern)]
  forward=[-e for p in pieces for e in p]
  backward=[-e for p in pieces for e in reversed(p)]
  counts[tuple(forward[:4])]+=1
  Y=[0];R=[0]
  for e in forward:Y.append(Y[-1]+e)
  for e in backward:R.append(R[-1]+e)
  j=0
  assert R[0]==Y[0]
  for p in pieces:
   T=len(p)
   assert 1<=T<=3
   for u in range(T+1):
    assert R[j+u]==Y[j]+Y[j+T]+Y[j+T-u]
   j+=T
   assert R[j]==Y[j]
  # The full finite W path includes every comparison time.
  omega=max(abs(Y[u]-Y[v]) for u in range(len(Y)) for v in range(max(0,u-3),min(len(Y),u+4)))
  error=max(abs(a-b) for a,b in zip(R,Y))
  assert error<=2*omega
  maxerror=max(maxerror,error);cases+=1
 for w in product((-1,1),repeat=4):
  assert counts[w]==len(allwords)**4//16
  prefix_checks+=1
# A modulus tail series with the same dyadic counting structure has a summable
# geometric majorant, since exp(4)>16 by its first four Taylor terms alone.
exp4_lower=sum(Fraction(4)**j/__import__('math').factorial(j) for j in range(4))
assert exp4_lower>16
ratio_majorant=Fraction(2,16);assert ratio_majorant<1
out={'passed':True,'finite_configurations':cases,'uniform_four_step_prefix_checks':prefix_checks,'maximum_grid_error_seen':maxerror,'exp4_rigorous_lower_bound':str(exp4_lower),'geometric_ratio_majorant':str(ratio_majorant),'scope':'Finite stopped-walk analogues verify exact rotation algebra, junction agreement, modulus inequality, and finite-prefix regeneration. They do not prove Brownian laws, the a.s. modulus estimate, or existence of the required random shift; those claims are separately justified or left open in PARTIAL.md.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
