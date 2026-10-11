#!/usr/bin/env python3
"""Independent exact finite controls; universal proof is audited separately."""
from fractions import Fraction as F
from itertools import product
import json
n=0;categories={}
def ck(c,x):
 global n
 assert x,c;n+=1;categories[c]=categories.get(c,0)+1
# Independent visual transcription of Figure1's upper bipartite graph.
rows=[{0,2,3,4},{1,2,3,4},{2,5,6},{3,5,6},{4,5,6},{0,1,5},{0,1,6}]
b=[5,5,3,3,3,4,4];q=[4,4,3,3,3,5,5]
for complement,k in [(False,13),(True,14)]:
 R=[set(range(7))-s if complement else s for s in rows]
 cols=[{i for i in range(7)if j in R[i]}for j in range(7)]
 ck('source',len({tuple(sorted(s))for s in cols})==7)
 for i in range(7):ck('source',sum(q[j]for j in R[i])==k)
 for j in range(7):ck('source',sum(b[i]for i in cols[j])==k)
 ck('source',max(map(len,R))==4)
 for i,j in product(range(7),repeat=2):
  if i!=j:ck('incomparability',bool(cols[i]-cols[j]))
 # Build all actual twin vertices; graph reachability uses set unions.
 Atypes=[i for i in range(7)for _ in range(k)]+[7]*(108-7*k)
 Btypes=[i for i in range(7)for _ in range(b[i])]
 Ctypes=[i for i in range(7)for _ in range(q[i])]
 AB=[{j for j,t in enumerate(Btypes)if a==7 or t not in cols[a]}for a in Atypes]
 CB=[{j for j,t in enumerate(Btypes)if t in cols[c]}for c in Ctypes]
 BA=[{i for i,s in enumerate(AB)if j in s}for j in range(27)]
 BC=[{i for i,s in enumerate(CB)if j in s}for j in range(27)]
 ck('blowup',len(Atypes)+len(Btypes)+len(Ctypes)==162)
 for s in AB:ck('blowup',len(s)>=27-k)
 for s in BA:ck('blowup',len(s)*27>=108*(27-k))
 for s in CB:ck('blowup',len(s)>=k)
 for s in BC:ck('blowup',len(s)>=k)
 for s in CB:ck('blowup',len(set().union(*(BA[j]for j in s)))==108-k)
# Boundary rigidity, including repeated C columns and extra universal A rows.
def family(m,na,nc,k):
 Pm=[v for v in range(1<<m)if v.bit_count()>=m-k]
 Qm=[v for v in range(1<<m)if v.bit_count()>=k]
 Ps=[p for p in product(Pm,repeat=na)if all(sum((v>>j)&1 for v in p)*m>=(m-k)*na for j in range(m))]
 Qs=[q for q in product(Qm,repeat=nc)if all(sum((v>>j)&1 for v in q)*m>=k*nc for j in range(m))]
 full=nonfull=repeat=extra=0
 for p in Ps:
  for q in Qs:
   reaches=[sum(bool(v&w)for v in p)for w in q];mx=max(reaches)
   if mx==na:full+=1;continue
   nonfull+=1
   ck('rigidity',all(v.bit_count()==k for v in q))
   ck('rigidity',all(sum((v>>j)&1 for v in q)*m==k*nc for j in range(m)))
   types=set(q);miss={w:{i for i,v in enumerate(p)if not(v&w)}for w in types}
   for w,inds in miss.items():
    ck('missed',bool(inds));ck('missed',all(p[i]==((1<<m)-1)^w for i in inds))
   ck('missed',sum(map(len,miss.values()))==len(set().union(*miss.values())))
   degrees=[sum((w>>j)&1 for w in types)for j in range(m)];Delta=max(degrees);t=min(map(len,miss.values()))
   ck('universal_bound',t*Delta*m<=k*na)
   ck('universal_bound',F(mx,na)>=1-F(k,m*Delta))
   repeat+=len(types)<len(q);extra+=sum(map(len,miss.values()))<na
 return {'parts':[na,m,nc],'theta':str(F(k,m)),'full':full,'nonfull':nonfull,'repeated_column_cases':repeat,'additional_A_cases':extra}
small=[family(3,3,3,1),family(3,3,3,2),family(4,3,4,2)]
# Zero universal class: identity template with theta1/2, d1, n2.
theta=F(1,2);d=1;count=2;ck('zero_residual',1-count*theta/d==0)
# All16 integer possibilities: actual invariant minima are not evaluated.
gaps=[]
for d,e in product(range(1,5),repeat=2):
 gap=abs(F(13,27*d)-F(14,27*e));ck('integer_gap',gap>=F(1,108));gaps.append(gap)
ck('integer_gap',min(gaps)==F(1,108))
# Turn2 matching certificates and universal equal-value example.
for j in range(1,41):
 y=F(1,4)+F(j,480)
 if y>F(1,3):continue
 ck('template',1-2*y>=y);ck('template',F(3,8)>=y);ck('template',2*y>=1-2*y)
# Turn1 union-bound envelope in rational form after log inequalities.
for i in range(1,101):
 u=F(i,100);ck('sampling',F(6,100)*(1+2*u+u*u)<=F(24,100)<1)
print(json.dumps({'status':'PASS','exact_assertions':n,'categories':categories,'boundary_census':small,'minimum_integer_gap':str(min(gaps)),'scope':'Independent exact finite controls, including repeated C types and additional A vertices. No computation of the true d minima, psi values or their order is claimed.'},indent=2,sort_keys=True))
