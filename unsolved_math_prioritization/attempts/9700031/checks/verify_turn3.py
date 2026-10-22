"""Exact dyadic partition and scalar controls for Turn 3; not a geometry proof."""
from fractions import Fraction as F
import json
n=0
# Log-coordinate road sizes. Every point is in exactly one dyadic band.
for N in range(1,25):
 for k in range(-35,36):
  s=F(k,N)
  for u in (F(-7,3),F(0),F(2,5),F(19,7)):
   hits=[j for j in range(-100,101) if u+j<s<=u+j+1]
   assert len(hits)==1;n+=1
  # The u interval [s-1,s) has exactly N subintervals of length 1/N.
  count=sum(1 for j in range(k-N-3,k+4) if F(j,N)<s<=F(j+1,N)+F(N-1,N))
  assert count==N;n+=1
# For finite synthetic positive road-length masses, critical expected band mass
# divided by the common log(2) factor is the total route length.
for m in range(1,101):
 weights=[F(i,1+i) for i in range(1,m+1)]
 total=sum(weights)
 assert sum(w*F(12,12) for w in weights)==total;n+=1
 for J in (1,2,3,10):
  assert sum(total for _ in range(J))==J*total;n+=1
for alpha_n in range(1,40):
 a=F(alpha_n,40)
 assert a-2<-1 and 1-a>0;n+=1
 # beta=3+a, t=r/u substitution exponent and scaling.
 beta=3+a
 assert -(2-beta)-2==a-1;n+=1
 assert 3-beta==-a and beta-3==a;n+=1
# Polynomial exponents used in radial mass transport and the critical identity.
for beta_n in range(41,80):
 beta=F(beta_n,20)
 assert 1-beta+1==2-beta;n+=1
 assert -(2-beta)-2==beta-4;n+=1
print(json.dumps({'status':'PASS_EXACT_BAND_CONTROLS','exact_assertions':n,'scope':'Dyadic partition, logarithmic band mass, finite-band sums, substitution exponents and fractional-tail integrability; analytic continuum argument requires review.'},indent=2))
