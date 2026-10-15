from fractions import Fraction as F
import random,json
rng=random.Random(780001205);checks=0;allocation_cases=0

def check(x):
 global checks
 assert x;checks+=1
# Exact rational Householder projections and the universal two-coordinate bound.
for n in range(2,13):
 for case in range(12):
  v=[F(rng.randrange(-5,6)) for _ in range(n)]
  if not any(v):v[0]=F(1)
  vv=sum(x*x for x in v);Q=[[F(i==j)-2*v[i]*v[j]/vv for j in range(n)] for i in range(n)]
  rank=rng.randrange(n+1);P=[[sum(Q[i][k]*Q[j][k] for k in range(rank)) for j in range(n)] for i in range(n)]
  check(sum(P[i][i] for i in range(n))==rank)
  for i in range(n):
   for j in range(n):
    check(sum(P[i][k]*P[k][j] for k in range(n))==P[i][j]);check(4*P[i][j]**2<=1 if i!=j else 0<=P[i][i]<=1)
    if i!=j:
     check(P[i][j]**2<=P[i][i]*P[j][j]);check(P[i][j]**2<=(1-P[i][i])*(1-P[j][j]))
# Exact core budgets for all even L and smaller even l in a finite control range.
for l in range(4,17,2):
 for L in range(l,65,2):
  k=L//l;R=L*L-k*k*l*l;check(R%4==0);check(k*k*(l*l//4)+R//4==L*L//4)
# Torus cut counts: one positive edge of each orientation at every vertex.
for l in [4,6,8]:
 for k in range(1,7):
  L=k*l;cuts=0
  for x in range(L):
   for y in range(L):
    for xx,yy in [((x+1)%L,y),(x,(y+1)%L)]:
     # Include wrapping seams even when k=1: the target boxes are open.
     if (x//l,y//l)!=(xx//l,yy//l) or (x==L-1 and xx==0) or (y==L-1 and yy==0):cuts+=1
  check(cuts==2*L*L//l)

def envelope(values,q):
 best=values[q];pair=(q,q)
 for a in range(q+1):
  for b in range(q,len(values)):
   if a==b:continue
   v=F(b-q,b-a)*values[a]+F(q-a,b-a)*values[b]
   if v<best:best=v;pair=(a,b)
 return best,pair

def allocations(values,blocks):
 d={0:F(0)}
 for _ in range(blocks):
  nd={}
  for old,cost in d.items():
   for rank,value in enumerate(values):
    total=old+rank;candidate=cost+value
    if total not in nd or candidate<nd[total]:nd[total]=candidate
  d=nd
 return d
for N in [4,8,12]:
 q=N//4
 for case in range(30):
  values=[F(rng.randrange(-30,1),rng.randrange(1,5)) for _ in range(N+1)];values[0]=values[N]=F(0)
  C,(a,b)=envelope(values,q);check(C<=values[q])
  for blocks in range(1,9):
   d=allocations(values,blocks);check(d[blocks*q]>=blocks*C);allocation_cases+=1
  if a!=b:
   denom=b-a;count_a=b-q;count_b=q-a;check(count_a*a+count_b*b==denom*q);check(count_a*values[a]+count_b*values[b]==denom*C)
   d=allocations(values,denom);check(d[denom*q]==denom*C)
print(json.dumps(dict(assertions=checks,allocation_dynamic_program_cases=allocation_cases,scope='Exact finite controls for boundary estimates, particle budgets and all-rank convexification; no global flux optimizer certified.'),indent=2,sort_keys=True))
