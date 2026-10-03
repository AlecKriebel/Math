from fractions import Fraction as F
from math import comb
import json
checks=0
def ck(x):
 global checks
 checks+=1
 assert x
summaries=[]
for q in range(1,31):
 n=5*q; R={0,2,3}; kept=[a for a in range(n) if a%5 in R]
 counts={(j,a):1 for j in range(3) for a in kept}
 dual={key:F(0) for key in counts}; doubles=triples=zero=0
 w=lambda a:F(1,3) if a%5==0 else F(1,2)
 for a in range(n):
  for b in range(n):
   t=(a,b,(-a-b)%n); inc=[(j,x) for j,x in enumerate(t) if x%5 in R]
   if len(inc)<2:continue
   iszero=all(x%5==0 for x in t)
   if len(inc)==2:doubles+=1;v=F(1,2*q)
   else:triples+=1;v=F(1,q) if iszero else F(0)
   zero+=iszero
   ck(sum(w(x) for _,x in inc)>=1)
   for key in inc:counts[key]+=1;dual[key]+=v
 ck((zero,triples,doubles)==(q*q,7*q*q,6*q*q))
 ck(triples+doubles+3==13*q*q+3)
 ck(triples*3+doubles+3*comb(3*q,2)==comb(9*q,2))
 ck(3*sum(w(a) for a in kept)==4*q)
 ck(sum(w(a) for a in kept)==F(4*q,3))
 ck(F(zero,q)+F(doubles,2*q)==4*q)
 for (j,a),cnt in counts.items():
  ck(cnt==(3*q+1 if a%5==0 else 4*q+1))
  ck(dual[j,a]==1)
 ck(max(counts.values())==4*q+1)
 ck(sum(v==4*q+1 for v in counts.values())==6*q)
 ck(13*q*q+3<(4*q+1)**2)
 if q>=3:ck(F(9*q,2)>4*q+1)
 summaries.append({'q':q,'lines':9*q,'points':13*q*q+3,'mpl':4*q+1,'cover_optimum':4*q})
print(json.dumps({'assertions':checks,'q_range':[1,30],'scope':'Exact finite incidence controls; infinite family proved analytically','examples':[summaries[0],summaries[-1]]},indent=2,sort_keys=True))
