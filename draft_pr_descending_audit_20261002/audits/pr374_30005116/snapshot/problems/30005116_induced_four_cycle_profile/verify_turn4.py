#!/usr/bin/env python3
from fractions import Fraction as Q
from itertools import combinations,product
from math import prod
import json
C={}
def ck(x,s):
 assert x,s
 C[s]=C.get(s,0)+1

def profile_geq(x,c):
 if x==1:return c<=0
 if x<=Q(1,2):return c<=Q(3,2)*x*x
 q=1-x;r=1//q;d=((r+1)*q-1)/r
 A=(1+6*r*d+r*(r*r-r+1)*d*d)/(r+1)**3
 B=4*r*(r-1)*d/(r+1)**3
 z=q*q-c/3
 return z>=A or B*B*d>=(A-z)**2

for r in range(2,31):
 for j in range(1,8):
  a=1/(r+Q(j,8));b=Q(j,8)*a;q=r*a*a+b*b
  da=1/(2*r*(a-b));db=-r*da
  Lprime=4*r*a**3*da+4*b**3*db
  ck(Lprime==2*(a*a+a*b+b*b),'profile_derivative_identity')
  ck(-6*q+3*Lprime==-6*((r-1)*a*a-a*b)<=0,'high_density_monotonicity')
  f=3*(q*q-r*a**4-b**4)
  ck(f>=Q(3,2)*q*q,'profile_lower_bound')
  ck(0<=f<=Q(3,8),'profile_global_maximum')

values={Q(0):Q(0),Q(1,4):Q(3,32),Q(1):Q(0)}
for k in range(2,9):values[1-Q(1,k)]=Q(3*(k-1),k**3)
unions=joins=0
for p,t in product(values,repeat=2):
 for j in range(1,16):
  w=Q(j,16);v=1-w
  x=w*w*p+v*v*t;c=w**4*values[p]+v**4*values[t]
  ck(profile_geq(x,c),'disjoint_union_profile_grid')
  if x>Q(1,2):
   big=max(w,v);inside=p if w>v else t;q=1-x
   gap=Q(3,8)*(1-big)*q*q*(4-q)
   ck(big>=x and inside>=x,'largest_component_density')
   ck(profile_geq(x,c+gap),'strict_union_gap_grid');unions+=1
  x=1-w*w*(1-p)-v*v*(1-t)
  c=w**4*values[p]+v**4*values[t]+6*w*w*v*v*(1-p)*(1-t)
  ck(profile_geq(x,c),'complete_join_profile_grid');joins+=1

def comps(adj,mask):
 out=[];left=mask
 while left:
  todo=left&-left;seen=0
  while todo:
   bit=todo&-todo;todo-=bit
   if seen&bit:continue
   seen|=bit;v=bit.bit_length()-1
   todo|=adj[v]&mask&~seen
  out.append(seen);left&=~seen
 return out

def cotree(adj,mask):
 if mask.bit_count()<2:return True
 cs=comps(adj,mask)
 if len(cs)>1:return all(cotree(adj,c) for c in cs)
 cadj=[mask&~(adj[v]|1<<v) for v in range(len(adj))]
 cs=comps(cadj,mask)
 return len(cs)>1 and all(cotree(adj,c) for c in cs)

def p4free(adj):
 for vs in combinations(range(len(adj)),4):
  mask=sum(1<<v for v in vs)
  if sorted((adj[v]&mask).bit_count() for v in vs)==[1,1,2,2]:return False
 return True

def weighted(adj,m):
 n=len(m);D=sum(m);N=1<<n;non=[]
 for S in range(N):
  vertices=[i for i in range(n) if S>>i&1]
  non.append(sum(m[i] for i in vertices)**2-
             sum(m[i]*m[j] for i in vertices for j in vertices if adj[i]>>j&1))
 num=sum(m[i]*m[j]*non[adj[i]&adj[j]] for i in range(n) for j in range(n) if not(adj[i]>>j&1))
 e=sum(m[i]*m[j] for i in range(n) for j in range(n) if adj[i]>>j&1)
 return Q(e,D*D),Q(3*num,D**4)

def direct_c4(adj,m):
 num=0;n=len(m);D=sum(m)
 for I in product(range(n),repeat=4):
  if all(sum(bool(adj[I[i]]>>I[j]&1) for j in range(4) if i!=j)==2 for i in range(4)):
   num+=prod(m[i] for i in I)
 return Q(num,D**4)

by_order=[];weighted_cases=0
for n in range(1,7):
 es=list(combinations(range(n),2));found=0
 for bits in range(1<<len(es)):
  adj=[0]*n
  for k,(i,j) in enumerate(es):
   if bits>>k&1:adj[i]|=1<<j;adj[j]|=1<<i
  rec=cotree(adj,(1<<n)-1);pf=p4free(adj)
  ck(rec==pf,'independent_cograph_recognition')
  if not rec:continue
  found+=1;p,c=weighted(adj,[1]*n)
  ck(profile_geq(p,c),'all_small_cograph_profile')
  if n==4:
   for mass in ([i+1 for i in range(n)],[(i+1)**2 for i in range(n)]):
    p,c=weighted(adj,mass)
    ck(c==direct_c4(adj,mass),'weighted_direct_motif_reconstruction')
    ck(profile_geq(p,c),'weighted_cograph_profile');weighted_cases+=1
 by_order.append({'vertices':n,'labeled_graphs':1<<len(es),'cographs':found})
ck([r['cographs'] for r in by_order]==[1,2,8,52,472,5504],'cograph_count_control')
print(json.dumps({'assertions':sum(C.values()),'by_scope':C,
 'arithmetic':'exact rational radical comparison and integer weighted motif counts',
 'all_graph_recognition_by_order':by_order,
 'weighted_cograph_controls':weighted_cases,
 'strict_union_gap_cases':unions,'join_grid_cases':joins,
 'scope':'All-size cograph theorem is the written cotree induction, not this order-six enumeration.'},indent=2)+'\n',end='')
