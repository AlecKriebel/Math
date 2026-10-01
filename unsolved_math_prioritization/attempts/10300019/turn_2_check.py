"""Exact monotone compression and order-amalgamation controls."""
from fractions import Fraction as F
from collections import Counter
import json
C=Counter();a=F(1,2)
def h(t,sign):
 lo,hi=(F(-2,3),F(-1,3)) if sign<0 else (F(1,3),F(2,3))
 if t<=-a:return -1+(t+1)*(lo+1)/(1-a)
 if t<=a:return lo+(t+a)*(hi-lo)/(2*a)
 return hi+(t-a)*(1-hi)/(1-a)
X=[F(k,120) for k in range(-120,121)]
for sign in (-1,1):
 assert h(F(-1),sign)==-1 and h(F(1),sign)==1;C['fixed_endpoints']+=1
 for u in [F(k,20) for k in range(21)]:
  Y=[(1-u)*t+u*h(t,sign) for t in X]
  for x,y in zip(Y,Y[1:]):assert x<y;C['isotopy_strict_order']+=1
 for t in X:
  if -a<=t<=a:
   assert (F(-3,4)<h(t,sign)<F(-1,4)) if sign<0 else (F(1,4)<h(t,sign)<F(3,4));C['separated_subcollars']+=1
# Arbitrary increasing internal maps preserve the fixed cross-label order.
for x in [F(k,20) for k in range(21)]:
 for y in [F(k,20) for k in range(21)]:
  j0=lambda z:F(-2,3)+z/3;j1=lambda z:F(1,3)+z/3
  assert j0(x)<j1(y) and j0(x*x)<j1(y*y*y);C['independent_holonomy_stack']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Exact product-fiber formulas only. Normal product charts and global lamination gluing are proved analytically; no general branched-carrier equivalence is inferred.'},indent=2))
