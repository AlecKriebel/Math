#!/usr/bin/env python3
from itertools import combinations_with_replacement,product
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json
counts={};staircases=0

def ck(cat,x):
 assert x,cat
 counts[cat]=counts.get(cat,0)+1
for t in range(1,7):
 for ms in combinations_with_replacement(range(1,8),t):
  staircases+=1;m=(0,)+ms;d=tuple(m[i]-m[i-1] for i in range(1,t+1));length=sum(ms);M=2*(length+t+2)
  for i in range(1,t+2):
   for j in range(1,t+1):
    u=m[j]-m[i-1]+i-j
    upper=d[i-1] if i<=j else d[j-1]
    desired={e for e in range(upper) if e>=u+(i<=j)}
    weighted={e for e in range(upper) if M*(e-u)+i-j>0}
    ck('parameter_weight_ranges',desired==weighted)
    for e in range(upper):ck('no_zero_parameter_weights',M*(e-u)+i-j!=0)
  ck('canonical_colength',length==sum(m[1:]))
# Monomial comparisons within a prescribed finite degree range.
for D in range(1,13):
 M=2*(D+2)
 mon=[(a,b) for a in range(D+1) for b in range(D+1-a)]
 for a,b in mon:
  for c,d in mon:
   expected=a+b<c+d or (a+b==c+d and a>c)
   ck('negative_degree_lex_comparison',expected==(-M*(a+b)+a>-M*(c+d)+c))
# Formal inverse certificates: (1+yW)*sum(-yW)^j =1 modulo y^B.
def mul(a,b,B):
 out=[F(0)]*B
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<B:out[i+j]+=x*y
 return out
for B in range(2,17):
 for w in product(range(-2,3),repeat=3):
  v=[F(0)]+list(map(F,w));v=(v+[F(0)]*B)[:B]
  p=[F(1)]+[F(0)]*(B-1);inv=[F(0)]*B
  for j in range(B):
   inv=[x+(-1)**j*y for x,y in zip(inv,p)];p=mul(p,v,B)
  unit=v.copy();unit[0]=1
  ck('completed_ring_unit_certificate',mul(unit,inv,B)==[F(1)]+[F(0)]*(B-1))
r={'status':'PASS','assertions':sum(counts.values()),'categories':counts,'monomial_staircases':staircases,'artifact_sha256':sha256(Path('KNOWN_RESULT.md').read_bytes()).hexdigest(),'limits':'Exact convention matching and formal unit checks only; the published isomorphism theorem is credited rather than independently reproved.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
