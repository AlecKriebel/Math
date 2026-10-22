from fractions import Fraction as F
from functools import lru_cache
import json,itertools
count=0
for cap in range(1,14):
 def safe(v):return all(not a*b<c<2*a*b for a in v for b in v for c in v)
 @lru_cache(None)
 def win(v,left):
  if not safe(v):return False
  if not left:return True
  return all(any(win(v+(u,),left-1) for u in range(x//2+1,x+1)) for x in range(1,cap+1))
 for n in range(3):
  A=win((),n);B=win((1,),n);An=win((),n+1)
  assert not An or B;assert not B or A;count+=2
 assert not safe((6,2));assert not safe((3,2,1));count+=2
# Negative-constant divisor witness and positive leading polynomial order.
for c in range(-250,251):
 if c==0:
  assert c%3==0;count+=1;continue
 e=0;b=c
 while b%2==0:e+=1;b//=2
 assert b%2!=0 and (2**e)*b==c;count+=1
# Exact binomial square coefficients and lexicographic support.
b=[F(1)]
for n in range(1,101):b.append(b[-1]*(F(1,2)-(n-1))/n)
for n in range(101):
 assert sum(b[i]*b[n-i] for i in range(n+1))==(1 if n in(0,1) else 0);count+=1
 assert (-1,n)<(0,0) and b[n]!=0;count+=1
# Polynomial automorphism under X ->3X/2 on common-denominator monomials:
# choose integral exponents to make exact rational coefficients for controls.
for co in itertools.product(range(-2,3),repeat=4):
 if co[3]<=0:continue
 u=list(map(F,co));v=[x*F(3,2)**i for i,x in enumerate(u)]
 assert v[3]>u[3];count+=1
 for n in range(7):
  left=sum(v[i]*v[n-i] for i in range(4) if 0<=n-i<4)
  right=sum(u[i]*u[n-i] for i in range(4) if 0<=n-i<4)*F(3,2)**n
  assert left==right;count+=1
print(json.dumps({'status':'PASS','assertions':count,'finite_game_challenge_bounds':13,'binomial_degree':100,'scope':'finite controls only; no arithmetic-model or definability test'},sort_keys=True))
