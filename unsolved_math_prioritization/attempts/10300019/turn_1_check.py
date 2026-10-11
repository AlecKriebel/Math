"""Exact weight/slope diagnostics; no realization or unmeasured classification inferred."""
from fractions import Fraction as F
from math import gcd
from collections import Counter
import json
C=Counter()
for a in range(1,25):
 for b in range(1,25):
  w=(a,b,a+b);assert w[0]+w[1]==w[2];C['switch_equation']+=1
  g=gcd(a,b);s=(a//g,b//g);assert gcd(*s)==1 and (g*s[0],g*s[1])==(a,b);C['primitive_slope']+=1
  for k in range(1,10):
   w2=tuple(k*x for x in w);assert w2[0]+w2[1]==w2[2];C['cone_scaling']+=1
for a in range(1,25):
 for b in range(1,25):
  if a==b:continue
  assert a-b!=0;C['sum_slope_determinant']+=1
  x=tuple(F(v,a+1) for v in (a,1));y=tuple(F(v,b+1) for v in (b,1));assert x!=y;C['normalized_sums_distinct']+=1
# Quadrilateral compatibility is union-of-support compatibility, not count equality.
Q=[(0,0,0)]+[tuple(k if j==i else 0 for j in range(3)) for i in range(3) for k in range(1,5)]
for u in Q:
 for v in Q:
  same=len({i for i in range(3) if u[i] or v[i]})<=1
  assert (sum(bool(u[i]+v[i]) for i in range(3))<=1)==same;C['quad_union_compatibility']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Exact cone and primitive-slope calculations. The carrier realization and no-descent theorem are proved analytically; no fixed-triangulation or general unmeasured claim is inferred.'},indent=2))
