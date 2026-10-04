from fractions import Fraction as F
import json
checks=0
def check(x):
 global checks
 assert x;checks+=1
# Constants in the energy contradiction, for every tested ambient dimension.
for n in range(3,31):
 s=n-2;C=2**s;eps=F(1,4*C*s)
 check(C*s*eps==F(1,4))
 check(F(1,4**s)<=F(1,4));check(C*s*eps+F(1,4**s)<=F(1,2))
 for j in range(1,31):
  delta=F(1,j);D=delta/4;Jmin=D**(-s)
  check(delta**(-s)/Jmin==F(1,4**s))
 # Pointwise nearest-support estimate, expressed in scalar distance bounds.
 for d in [F(1,3),F(1),F(3)]:
  for e in [F(1,100),F(1,5)]:
   for b in [d,2*d,5*d]:
    a=d+e+b;factor=2+e/d
    check(a<=factor*b);check(b**(-s)<=factor**s*a**(-s))
 # Power-weakened integral upper bound has positive finite exponent.
 for eta in [F(1,10),F(1,2),F(1),F(2)]:check(eta>0 and F(C)/eta>0)
# Exact quadratic energy variation identity and its first-order coefficient.
for J in [F(1),F(2),F(5)]:
 for L in [F(1),F(3),F(7)]:
  for N in [F(2),F(4),F(9)]:
   for t in [F(0),F(1,10),F(1,2),F(1)]:
    check((1-t)**2*J+2*t*(1-t)*L+t*t*N==J+2*(L-J)*t+(J-2*L+N)*t*t)
# Dyadic kernel lower bound and mass Cauchy lower bound.
for j in range(1,513):
 d=F(1,j);partial=sum((F(2)**(k-1) for k in range(13) if d<=F(1,2**k)),F(0));check(partial<=1/d)
for k in range(13):
 N=2**k;check(N*F(1,N)**2==F(1,N));check(F(2)**(k-1)*F(1,N)==F(1,2))
print(json.dumps(dict(assertions=checks,scope='Exact constants, distance inequalities, first-variation algebra and dyadic sharpness sanity checks; the all-set proof is TURN_1.md.',method='No finite computation certifies polarity or capacitability.'),indent=2,sort_keys=True))
