#!/usr/bin/env python3
"""Exact finite controls for the monotone maximal-inequality route. Not an endpoint proof."""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from collections import Counter
import json
C=Counter()
def ck(p,k):
 C[k]+=1
 if not p:raise AssertionError(k)
curves=list(combinations_with_replacement(range(3),3));signs=list(product((-1,1),repeat=3))
for fs in product(curves,repeat=3):
 Emax=F(0)
 for eps in signs:
  val=[sum(eps[i]*fs[i][j] for i in range(3)) for j in range(3)]
  Emax+=F(max(v*v for v in val),len(signs))
 ck(Emax<=4*sum(f[-1]**2 for f in fs),'deterministic_monotone_Rademacher_L2')
# Exact threshold representation and Jensen on a selected family of varying curves.
for fs in list(product(curves,repeat=3))[::29]:
 w=[f[-1] for f in fs]
 probs=[]
 for f in fs:
  if f[-1]==0:probs.append([F(1),F(0),F(0)])
  else:probs.append([F(f[0],f[-1]),F(f[1]-f[0],f[-1]),F(f[2]-f[1],f[-1])])
 for i,j in product(range(3),repeat=2):ck(w[i]*sum(probs[i][:j+1])==fs[i][j],'threshold_CDF_representation')
 for eps in signs:
  raw=max(abs(sum(eps[i]*fs[i][j] for i in range(3))) for j in range(3))**2
  randomized=F(0)
  for ts in product(range(3),repeat=3):
   probability=probs[0][ts[0]]*probs[1][ts[1]]*probs[2][ts[2]]
   val=[sum(eps[i]*w[i] for i in range(3) if ts[i]<=j) for j in range(3)]
   randomized+=probability*max(v*v for v in val)
  ck(raw<=randomized,'threshold_Jensen_maximum')
# Conditional parent activation: three independent bounded offspring curves,
# with exact EX(lambda_j)=lambda_j and arbitrary nested known parent counts.
X=[]
for b1,b2 in product(range(4),repeat=2):X.append(tuple(2+int(b1<j)+int(b2<j) for j in (1,2,3)))
lam=[F(5,2),F(3),F(7,2)];activation=[1,2,3];means=[F(0)]*3;maxsquare=F(0)
for config in product(X,repeat=3):
 R=[sum(config[i][j] for i in range(activation[j]))-lam[j]*activation[j] for j in range(3)]
 for j in range(3):means[j]+=R[j]/len(X)**3
 maxsquare+=max(r*r for r in R)/len(X)**3
for mean in means:ck(mean==0,'conditional_generation_centering')
endpoint_moment=sum(F(f[-1]**2,len(X)) for f in X)
ck(maxsquare<=16*3*endpoint_moment,'conditional_monotone_process_moment_bound')
# Every compact above1 has a finite small-interval partition, explicitly at p=2.
for a,b in [(F(11,10),F(4)),(F(3,2),F(10)),(F(2),F(7))]:
 step=(a*a-a)/2;x=a;pieces=0
 while x<b:
  y=min(b,x+step);ck(x<y<x*x,'finite_partition_small_interval');ck(0<y/(x*x)<1,'geometric_increment_ratio');x=y;pieces+=1
 ck(x==b and pieces<1000,'compact_partition_terminates')
# Genuine p=3/2 arithmetic, without introducing a variance assumption.
for r in [F(11,10),F(5,4),F(3,2),F(2),F(7,3)]:
 a=r*r;upper=r**3;b=(a+upper)/2
 ck(a<b<upper,'p_three_halves_interval_condition')
# Exact discrete rotation controls for the mean of the bounded two-jump model.
for M in (16,32):
 for shift in range(1,6):
  T=[F(2*j+1,M) for j in range(M)];V=[(t+F(2*shift,M))%2 for t in T]
  ck(sorted(V)==T,'uniform_circle_rotation')
  for j in range(1,M):
   t=F(2*j,M);mean=F(sum(2+int(u<=t)+int(v<=t) for u,v in zip(T,V)),M)
   ck(mean==2+t,'bounded_offspring_mean_parameter')
# The actual continuous-model mixed-increment lower event has exact rational mass.
for n in range(5,101):
 delta=F(1,2**n);tailband=F(4,n)-F(4,n+1)
 ck(tailband==F(4,n*(n+1)),'Pareto_logscale_band_mass')
 ck(delta*tailband/4==delta/F(n*(n+1)),'clustered_jump_event_probability')
 for theta,eta in product([F(1,8),F(1,4),F(3,8)],[F(5,8),F(3,4),F(7,8)]):
  T=1-theta*delta;D=eta*delta;V=(T+D)%2
  X=lambda time:2+int(T<=time)+int(V<=time)
  ck(X(1)-X(1-delta)==X(1+delta)-X(1)==1,'two_adjacent_actual_jumps')
# Along n=r*m, every strictly-above-half Holder exponent has exponential/polynomial divergence.
for r in (1,2,3,5,10,31):
 for m in range(3,81):
  q=F(2**m,(r*m)*(r*m+1));qp=F(2**(m+1),(r*(m+1))*(r*(m+1)+1))
  ck(qp>=F(9,8)*q,'mixed_bound_ratio_growth_control')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Finite exact monotone-grid, random-threshold, conditional-centering, partition and clustered-jump controls. General p in(1,2], arbitrary processes, uniform convergence and failure of every Holder exponent are proved analytically. Exact X log X endpoint is not proved.'},indent=2,sort_keys=True))
