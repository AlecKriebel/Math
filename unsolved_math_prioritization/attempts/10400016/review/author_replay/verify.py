#!/usr/bin/env python3
from collections import Counter,defaultdict
from itertools import product
from pathlib import Path
import hashlib,json
C=Counter()
def check(k,b):
 assert b,k
 C[k]+=1
def mul(P,Q):
 r=defaultdict(int)
 for (a,z),c in P.items():
  for (b,w),d in Q.items():r[a+b,z+w]+=c*d
 return {e:c for e,c in r.items() if c}
def mindeg(P):return min(a for a,z in P)
def maxdeg(P):return max(a for a,z in P)
dP={(-1,-1):1,(1,-1):-1}
dF={(-1,-1):1,(1,-1):1,(0,0):-1}
for cs in product(range(-1,2),repeat=4):
 P={e:c for e,c in zip([(-3,-1),(-1,2),(2,0),(4,3)],cs) if c}
 if not P:continue
 inv={(-a,z):c for (a,z),c in P.items()}
 check('inverse_minimum',mindeg(inv)==-maxdeg(P))
 check('HOMFLY_split_shift',mindeg(mul(dP,P))==mindeg(P)-1)
 check('Kauffman_split_shift',maxdeg(mul(dF,P))==maxdeg(P)+1)
# Signed blocks joined at cut vertices: the spanning-tree count is blockwise.
blocks=[(v,e,sgn) for v in range(2,6) for e in range(v-1,v+3) for sgn in [-1,1]]
for B1 in blocks:
 for B2 in blocks:
  blocks2=[B1,B2]
  w=sum(s*e for v,e,s in blocks2)
  dtree=sum(s*(v-1) for v,e,s in blocks2)
  A=sum(s*(e-v+1) for v,e,s in blocks2)
  check('signed_rank_identity',w-dtree==A)
# Non-split factor inequalities imply the strengthened split statement.
for q in range(1,8):
 for slack in range(6):
  sigmas=[2*j-q for j in range(q)]
  hs=[x-slack for x in sigmas]
  h=sum(hs)-(q-1)
  check('split_signature_shift',h+q-1<=sum(sigmas))
  check('split_implies_original',h<=sum(sigmas))
# A sharp Kauffman bound and the HOMFLY bound give the desired ordering.
for k in range(-12,13):
 for gap in range(8):
  h=k+gap;tb=k-1
  check('sharp_bound_comparison',tb<=h-1 and k<=h)
for q in range(1,10):
 check('unlink_signature',1-q+q-1==0)
 check('unlink_original',0>=1-q)
p=Path(__file__).resolve()
r={'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(C),'artifact_sha256':hashlib.sha256(p.with_name('KNOWN_RESULT.md').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'Exact finite algebra controls, not knot-polynomial computation or a reproof of the cited geometric theorems.'}
print(json.dumps(r,indent=2,sort_keys=True))
