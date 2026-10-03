#!/usr/bin/env python3
"""Exact finite controls for the length theorem; topological upper bound is cited."""
from itertools import combinations,product
from fractions import Fraction as F
import json
n=0
def ck(x):
 global n
 assert x;n+=1
pairs=list(combinations(range(6),2));pairidx={p:i for i,p in enumerate(pairs)}
def inverse(w):return tuple(-a for a in w[::-1])
def trace(w):
 pos=list(range(6));counts=[0]*15
 for a in w:
  i=abs(a)-1;p=tuple(sorted((pos[i],pos[i+1])));counts[pairidx[p]]+=1 if a>0 else -1;pos[i],pos[i+1]=pos[i+1],pos[i]
 return tuple(pos),tuple(counts)
def linking(w):
 p,c=trace(w);ck(p==tuple(range(6)));ck(all(x%2==0 for x in c));return tuple(x//2 for x in c)
c=(1,2,3,4)*5;h=(5,4,3,2,1,1,2,3,4,5);z=(1,2,3,4,5)*6;r=c+inverse(h);target=c+c
lc=linking(c);lh=linking(h);lr=linking(r);lb=linking(target)
for k,(i,j)in enumerate(pairs):
 ck(lc[k]==int(j<5));ck(lh[k]==int(j==5));ck(lr[k]==(1 if j<5 else -1));ck(lb[k]==2*int(j<5))
# Faithful Artin action on F6, exact freely reduced words.
def reduce(w):
 out=[]
 for a in w:
  if out and out[-1]==-a:out.pop()
  else:out.append(a)
 return tuple(out)
def substitute(w,images):
 return reduce(a for x in w for a in (images[x-1]if x>0 else inverse(images[-x-1])))
def action(w):
 im=[(j,)for j in range(1,7)]
 for a in w:
  i=abs(a);g=[(j,)for j in range(1,7)]
  if a>0:g[i-1]=(i,i+1,-i);g[i]=(i,)
  else:g[i-1]=(i+1,);g[i]=(-(i+1),i,i+1)
  im=[substitute(x,g)for x in im]
 return im
ck(action(c+h)==action(z))
for i in range(1,6):
 ck(action((i,-i))==action(()))
 if i<5:ck(action((i,i+1,i))==action((i+1,i,i+1)))
 for j in range(i+2,6):ck(action((i,j))==action((j,i)))
# The conjugation orbit of r's linking vector consists of the six vertex patterns.
patterns={tuple(1 if k not in pair else -1 for pair in pairs) for k in range(6)}
conjugators=[(),(5,),(4,5),(3,4,5),(2,3,4,5),(1,2,3,4,5)]
observed={linking(b+r+inverse(b))for b in conjugators};ck(observed==patterns)
for v in patterns:ck(sum(v)==5)
ck(len(c+c)==40 and len(z)==30 and len(h+h)==20)
# Exact summed inequalities, valid without a bound on t_i.
for m in [0,10]:
 T=F(m,10)-4;ck(T.denominator==1);T=int(T)
 ck((T+2)//2==-1 and T//2==-2)
 lower=-((-5*T-10)//4) # ceil((5T+10)/4)
 ck(lower>-3)
# Bounded stress controls of the necessary inequalities, not the infinite proof.
stress=0
for first in product(range(-3,4),repeat=5):
 s=sum(first)
 if not all(first[i]+first[j]<=-1 for i,j in combinations(range(5),2)):continue
 ck(s<=-3)
 for T in [-4,-3]:
  t6=T-s
  ck(not all(x+t6<=-2 for x in first));stress+=1
print(json.dumps({'status':'PASS','exact_assertions':n,'linking_coordinates':15,'relation_conjugate_patterns':6,'bounded_integer_stress_cases':stress,'realized_lengths':[20,30,40],'scope':'Exact braid identities/linking and integer obstruction controls. The universal upper bound40 is the credited Baykur–Monden–Van Horn-Morris theorem; Hurwitz classification remains open here.'},indent=2,sort_keys=True))
