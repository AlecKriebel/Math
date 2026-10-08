"""Exact normalization/order controls, separate from the author program."""
from fractions import Fraction as Q
from math import factorial
from itertools import permutations,product
from collections import Counter
from pathlib import Path
from hashlib import sha256
import random,json
C=Counter();rng=random.Random(30003818)
def ck(k,v):
 if not v:raise AssertionError(k)
 C[k]+=1
def trim(p):
 p=list(p)
 while len(p)>1 and p[-1]==0:p.pop()
 return p
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def scale(p,c):return trim([c*x for x in p])
def mul(a,b):
 c=[Q(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def power(p,n):
 out=[Q(1)]
 for _ in range(n):out=mul(out,p)
 return out
def val(p,x):return sum(a*x**i for i,a in enumerate(p))
# Compute the exit Laplace transform from the ODE and from a formal sinh quotient.
ode=[[Q(1),Q(-1)]];quot=[]
for n in range(10):
 numerator=scale(power([Q(1),Q(-1)],2*n+1),Q(1,factorial(2*n+1)))
 q=numerator
 for j in range(1,n+1):q=add(q,scale(quot[n-j],-Q(1,factorial(2*j+1))))
 quot.append(q)
 if n:
  previous=ode[-1];p=[Q(0),Q(0)]+[x/Q((i+1)*(i+2)) for i,x in enumerate(previous)];p[1]=-sum(p);ode.append(trim(p))
 ck('exit_transform_ODE_vs_sinh',trim(ode[n])==trim(quot[n]))
 ck('exit_transform_boundary',val(quot[n],Q(1))==0 and val(quot[n],Q(0))==int(n==0))
for den in range(2,15):
 for j in range(1,den):
  r=Q(j,den)
  ck('exit_probabilities',val(quot[0],r)+val(quot[0],1-r)==1)
  for L in (Q(1,3),Q(1),Q(7,4)):
   ck('exit_time_mean_factor_two',-2*L*L*(val(quot[1],r)+val(quot[1],1-r))==L*L*r*(1-r))
   for n in range(1,51):
    ck('flux_prefactor',Q(1,2)*Q(2,1)/L*Q(n,1)/L==Q(n,1)/L**2)
    ck('right_flux_sign',-((-1)**n)==(-1)**(n+1))
def kernel_mass(z,A):
 left=min(A,key=lambda x:(z-x)%1);right=min(A,key=lambda x:(x-z)%1)
 dl=(z-left)%1;dr=(right-z)%1;ell=dl+dr
 result={x:Q(0) for x in A};result[left]+=dr/ell;result[right]+=dl/ell
 ck('next_target_total_mass',sum(result.values())==1)
 if len(A)==1:ck('singleton_both_endpoints',ell==1 and next(iter(result.values()))==1)
 return result
ordercases=0
for m in range(1,7):
 for rep in range(3):
  targets=tuple(sorted(Q(x,23) for x in rng.sample(range(1,23),m)))
  start=Q(2*rep+1,46)
  if start in targets:continue
  weights=[]
  for perm in permutations(targets):
   A=set(targets);z=start;prob=Q(1)
   for target in perm:
    # Local probability can be zero for an impossible order.
    K=kernel_mass(z,A);prob*=K[target];A.remove(target);z=target
   weights.append(prob)
  ck('all_order_mass',sum(weights)==1)
  ck('possible_order_count',sum(w>0 for w in weights)==2**(m-1))
  ordercases+=1
# Independently reconstruct physical hitting times and check the strict regions partition.
for k in (1,2,3):
 for m in range(1,5):
  for rep in range(15):
   times=rng.sample(range(1,1000),k*m);h=[times[i*m:(i+1)*m] for i in range(k)]
   recon=[]
   for row in h:
    pi=sorted(range(m),key=lambda j:row[j]);increments=[];prev=0
    for j in pi:increments.append(row[j]-prev);prev=row[j]
    rebuilt=[0]*m
    for r,j in enumerate(pi):rebuilt[j]=sum(increments[:r+1])
    ck('physical_time_reconstruction',rebuilt==row and min(increments)>0);recon.append(rebuilt)
   number=0
   for labels in product(range(k),repeat=m):
    number+=all(recon[labels[j]][j]<recon[i][j] for j in range(m) for i in range(k) if i!=labels[j])
   ck('ownership_regions_partition',number==1)
# Factorial error envelope, using certified rational alternating bounds on exp(-z).
for z in (Q(0),Q(1,4),Q(1,2),Q(1),Q(2),Q(4)):
 exact_lo=sum((-z)**j/Q(factorial(j)) for j in range(42))
 exact_hi=sum((-z)**j/Q(factorial(j)) for j in range(41))
 ck('exp_interval_order',exact_lo<=exact_hi)
 for M in range(9):
  S=sum((-z)**j/Q(factorial(j)) for j in range(M+1));bound=z**(M+1)/factorial(M+1)
  ck('factorial_envelope',max(abs(exact_lo-S),abs(exact_hi-S))<=bound)
root=Path(__file__).resolve().parent
result={'artifact_sha256':sha256((root.parent/'reference'/'JOINT_LAW.md').read_bytes()).hexdigest(),'independent_assertions':sum(C.values()),'categories':dict(C),'target_order_configurations':ordercases,'scope':'Exact exit-transform ODE/series identities, harmonic target-order probabilities, physical-time region partitions and certified Taylor envelopes. These finite controls do not replace the Brownian proof.'}
print(json.dumps(result))
