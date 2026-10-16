from fractions import Fraction as F
from itertools import combinations,product
from collections import Counter
from math import comb
import json
checks=0;configs=0
def ck(x):
 global checks
 checks+=1
 assert x
for n in range(2,15):
 C=Counter()
 for y in product((-1,1),repeat=n):C[sum(y[i]!=y[(i+1)%n] for i in range(n))]+=1
 for j in range(n+1):ck(C[j]==(2*comb(n,j) if j%2==0 else 0))
 ck(sum(C.values())==2**n)
for n in range(2,7):
 for ticks in combinations(range(10),n):
  x=[F(t,10) for t in ticks];s=[x[i+1]-x[i] for i in range(n-1)]+[1+x[0]-x[-1]]
  for y in product((-1,1),repeat=n):
   marked=[s[i] for i in range(n) if y[i]!=y[(i+1)%n]]
   if not marked:continue
   t=min(marked);j=len(marked)
   best=min(min(abs(x[a]-x[b]),1-abs(x[a]-x[b])) for a in range(n) for b in range(a+1,n) if y[a]!=y[b])
   ck(best==t);ck(t<=F(1,j)<=F(1,2));configs+=1
for n in range(2,61):
 weights={j:F(2*comb(n,j),2**n) for j in range(0,n+1,2)};ck(sum(weights.values())==1)
 for den in [3,7,19,101]:
  t=F(1,den);tail=sum(w*max(F(0),1-j*t)**(n-1) for j,w in weights.items())
  ck(weights[0]<=tail<=1)
  for j in range(2,n+1,2):
   # Integral of the exact survival polynomial over[0,1/j] equals1/(nj).
   integral=sum(F((-1)**h*comb(n-1,h),j*(h+1)) for h in range(n))
   ck(integral==F(1,n*j))
print(json.dumps({'assertions':checks,'rational_opposite_pair_configurations':configs,'label_law_max_n':14,'simplex_tail_max_n':60,'scope':'Exact finite identities; random-spacing theorem proved analytically'},indent=2,sort_keys=True))
