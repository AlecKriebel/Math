"""Exact scalar obstruction and critical-exponent controls; not a SIRSN model."""
from fractions import Fraction as F
import json
count=0
for N in (1,2,3,5,10,20,40):
 probabilities={2**n:F(1,2**(n+1)*n*n) for n in range(1,N+1)}
 probabilities[1]=1-sum(probabilities.values())
 d=sum(D*p for D,p in probabilities.items())
 assert probabilities[1]>=F(1,2) and 1<=d<2;count+=1
 for un in range(1,120):
  u=F(un,3)
  h=sum(D*p for D,p in probabilities.items() if D*D>u)
  for kn in range(1,51):
   K=F(kn,4)
   tail=sum(D*p for D,p in probabilities.items() if D>K)
   assert h<=2*K*K/u+tail;count+=1
   event=sum(p for D,p in probabilities.items() if D*D>u and D<=K)
   assert event<=2*K/u;count+=1
for j in range(5,1001):
 assert F(2*j*j,(j+1)**2)>=F(4,3);count+=1
for n in range(2,201):
 assert F(1,n*n)<F(1,n*(n-1));count+=1
# In dimension two, a translation difference proportional to t gives
# radial traffic exponent (1-beta)+1=2-beta, critical at beta=3.
for bn in range(41,91):
 beta=F(bn,20)
 assert ((2-beta)<=-1)==(beta>=3);count+=1
print(json.dumps({'status':'PASS_EXACT_OBSTRUCTION_CONTROLS','exact_assertions':count,'scope':'Finite truncations of a scalar non-SIRSN mark model, geometric-bound compatibility, divergent-series ratio and fractional-perimeter exponent. The model is not an original counterexample.'},indent=2))
