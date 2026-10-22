#!/usr/bin/env python3
"""Independent exact Laurent controls. No knot realization is inferred."""
from collections import defaultdict,Counter
from itertools import product
from pathlib import Path
import hashlib,json
C=Counter()
def check(k,b):
 assert b,k
 C[k]+=1
def add(*polys):
 d=defaultdict(int)
 for P in polys:
  for e,c in P.items():d[e]+=c
 return {e:c for e,c in d.items() if c}
def times(P,Q):
 d=defaultdict(int)
 for (a,b),c in P.items():
  for (x,y),v in Q.items():d[a+x,b+y]+=c*v
 return {e:c for e,c in d.items() if c}
def scale(P,c):return {e:c*v for e,v in P.items() if c*v}
def deg(P):return max((j for i,j in P),default=float('-inf'))
def lead(P,j):return {i:c for (i,b),c in P.items() if b==j}
def subst(P):return {(-2*i,2*j):c for (i,j),c in P.items()}
def parity(P):return {e:c%2 for e,c in P.items() if c%2}
dP={(-1,-1):1,(1,-1):-1};dF={(-1,-1):1,(1,-1):1,(0,0):-1}
support=[(-3,-2),(-1,1),(2,1),(4,3)]
for coeffs in product(range(-2,3),repeat=4):
 P={e:c for e,c in zip(support,coeffs) if c}
 if not P:continue
 check('HOMFLY_normalization',deg(times(P,dP))==deg(P)-1)
 check('Kauffman_normalization',deg(times(P,dF))==deg(P))
 check('injective_support_substitution',len(subst(P))==len(P))
 check('degree_doubling',deg(subst(P))==2*deg(P))
 for f in [-5,-1,0,2,7]:
  shifted=times(P,{(2*f,0):1})
  check('framing_degree',deg(shifted)==deg(P))
  check('framing_top_parity_nonvanishing',bool(parity({(i,0):c for i,c in lead(shifted,deg(P)).items()}))==bool(parity({(i,0):c for i,c in lead(P,deg(P)).items()})))
 # Opposite-clasp mirroring changes first exponents and Alexander signs only.
 mirrored={(-i,j):c*(-1 if j%2 else 1) for (i,j),c in P.items()}
 check('mirror_degree',deg(mirrored)==deg(P))
# Exhaustive residual correction at, below and above prescribed top degree.
F={(0,2):2,(1,2):1,(-1,0):3};S=subst(F)
for lo,top,hi in product(range(-3,4),repeat=3):
 Q={e:c for e,c in [((0,2),lo),((0,4),top),((0,6),hi)] if c}
 R=add(S,scale(Q,2))
 check('congruence',parity(R)==parity(S))
 recovered={e:c//2 for e,c in add(R,scale(S,-1)).items()}
 check('unique_integral_residual',recovered==Q)
 check('upper_bound_iff', (deg(R)<=4)==(hi==0))
 check('odd_top_survives',bool(lead(R,4)))
# Clasp leading-degree separation, allowing several framing coefficients.
for r in range(1,12):
 for c in [-4,-1,1,6]:
  R={(-3,r):c,(2,0):7,(1,-2):-2}
  PG=add(times({(2,0):1},dP),times({(1,1):1},add(R,{(0,0):1})))
  check('clasp_positive_degree',deg(PG)==r+1)
  check('clasp_unknot_normalized_degree',deg(PG)+1==r+2)
# Explicit exceptional control: dropping r>0 can break the conclusion.
R={(0,0):-1};PG=add(times({(2,0):1},dP),times({(1,1):1},add(R,{(0,0):1})))
check('r_zero_exception',deg(PG)+1==0 and deg(R)+2==2)
for d in range(2,20):
 R={(0,2*d):1,(1,2*d+2):2};F={(0,d):1}
 check('odd_top_no_upper',parity(R)==parity(subst(F)) and deg(R)>2*d)
 for e in range(1,d):
  F={(0,d):2,(1,d):4,(-2,e):1};R={(-2*(-2),2*e):1}
  check('even_top_loss',parity(R)==parity(subst(F)) and deg(R)<2*d)
p=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(C),'artifact_sha256':hashlib.sha256((p/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'Independent finite Laurent-ring controls only; no diagram, knot invariant, or knot counterexample is computed.'}
(p/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r))
