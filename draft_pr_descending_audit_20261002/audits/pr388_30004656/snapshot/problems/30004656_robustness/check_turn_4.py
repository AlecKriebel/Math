from fractions import Fraction as F
from itertools import product
from math import prod,factorial
import json
c=0
def ck(v):
 global c
 c+=1;assert v
for k in range(1,7):
 for seed in range(1,21):
  vs=[[(seed*(i+1)*(j+2)+i*i-j)%9-4 for j in range(3)] for i in range(k)]
  energy=sum(x*x for v in vs for x in v)
  signed=sum(sum(sum(s[i]*vs[i][j] for i in range(k))**2 for j in range(3)) for s in product((-1,1),repeat=k))
  subsets=[sum(sum(t[i]*vs[i][j] for i in range(k))**2 for j in range(3)) for t in product((0,1),repeat=k)]
  ck(signed==2**k*energy);ck(energy<=4*max(subsets))
for r in range(1,31):
 for s in range(r+1):
  for a in range(41):
   t=F(a,20);D=(r-s)**2+r*s*t*t
   ck((s*t+2*(r-s))**2<=9*D)
for d in range(2,101):
 for m in range(1,21):
  odd=prod(range(1,2*m,2));mom=F(odd,prod(d+2*j for j in range(m)))
  ck(mom<=F(odd,d**m));ck(F(4**m*odd,factorial(2*m))==F(2**m,factorial(m)))
for d in range(2,101):
 for j in range(1,101):
  # Replace log2 by1, and v by d: the union exponent is at most-v-j.
  ck(d*(2*j+3)-8*(d*(j+2)+d+j)<=-d-j)
ck(F(3,4)-F(1,16)>=F(1,2));ck(2*6*256==3072);ck(F(1,3072)>=F(1,4096))
print(json.dumps({'assertions':c,'scope':'Exact finite energy, radial and chaining-constant controls; analytic proof supplies probability and uniformity'},indent=2,sort_keys=True))
