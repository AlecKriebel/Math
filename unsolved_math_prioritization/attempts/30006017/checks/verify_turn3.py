#!/usr/bin/env python3
"""Exact algebra for interval normalization, moment ratios and the Abel-cutoff obstruction."""
from fractions import Fraction as Q
from math import comb
import json
count=0
def check(v):
 global count
 assert v
 count+=1
# Triangular excursion e(t)=min(t,1-t): F(alpha)=1/[2(alpha+1)].
# The min kernel integrates to (1-u)^2/4 at separation u.
for alpha in range(2,301):
 integral=Q(1,4)*(Q(1,alpha-1)-Q(2,alpha)+Q(1,alpha+1))
 check(alpha*(alpha-1)*integral==Q(1,2*(alpha+1)))
# The normalized finite mean measure is the arcsine law; exact Gamma/Beta recurrence.
previous=Q(1)
for m in range(1,401):
 moment=Q(comb(2*m,m),4**m)
 check(moment==previous*Q(2*m-1,2*m))
 previous=moment
# Covariance of the random-phase Abel residual (sin,cos variances 1/2, covariance 0).
for den in range(1,75):
 for num in range(1,den+1):
  z=Q(num,den); a=Q(1,7)
  ccos=a*z/(1+z*z); csin=-a/(1+z*z)
  variance=(ccos*ccos+csin*csin)/2
  check(variance==a*a/(2*(1+z*z)))
  error_to_limit=(ccos*ccos+(csin+a)**2)/2
  check(error_to_limit==a*a*z*z/(2*(1+z*z)))
  check(error_to_limit<=a*a*z*z/2)
# Sharp cutoff has alternating zero and nondegenerate laws at even/odd multiples of pi.
for m in range(300):
 ct=Q(1) if m%2==0 else Q(-1)
 variance=Q(1,49)*(1-ct)
 check(variance==(0 if m%2==0 else Q(2,49)))
print(json.dumps({'status':'PASS','assertions':count,'coverage':['interval-power normalization for a triangular excursion','finite mean-measure Gamma/Beta moment ratios','random-phase Abel L2 formula','nonconvergent sharp-cutoff subsequence variances'],'scope':'Exact controls supplement the continuum theorem; no finite-polygon area transfer is certified.'},indent=2,sort_keys=True))
