#!/usr/bin/env python3
if not __debug__:
 raise SystemExit('Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O')

import sympy as sp
from itertools import combinations
from common import Avec
for m in [3,4,5,6,8,10]:
 A=Avec(m);h=[sp.Rational(i+2,i+1) for i in range(m+1)];d=[sp.Rational(2*i+3,i+2) for i in range(m+1)]
 J=A*sp.diag(*h);n=m+1
 beta=[]
 for k in range(1,n+1):
  total=0
  for I in combinations(range(n),n-k):
   Ic=[j for j in range(n) if j not in I]
   det=sp.Integer(1) if not I else J.extract(I,I).det()
   total += (-1)**len(I)*det*sp.prod(d[j] for j in Ic)
  beta.append(sp.factor(total))
 expected=sp.factor(2*sp.prod(h[:m])*(8*h[m]*sum(d[j]/h[j] for j in range(1,m-1))-d[m]))
 assert sp.factor(beta[0]-expected)==0
 assert all(x>0 for x in beta[1:])
print('DIFFUSION_CRITERION_PASS')
