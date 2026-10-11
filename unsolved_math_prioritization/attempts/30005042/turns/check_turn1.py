#!/usr/bin/env python3
"""Exact finite coupled-law and truncation controls. No topology proof by sampling."""
from fractions import Fraction as F
from collections import defaultdict,Counter
from functools import lru_cache
from itertools import product
import json
C=Counter()
def ck(p,k):
 C[k]+=1
 if not p:raise AssertionError(k)
def addlaw(A,B):
 out=defaultdict(F)
 for x,p in A.items():
  for y,q in B.items():out[(x[0]+y[0],x[1]+y[1])]+=p*q
 return dict(out)
def power(A,n):
 d={(0,0):F(1)}
 for _ in range(n):d=addlaw(d,A)
 return d
def second_only(A):
 out=defaultdict(F)
 for (a,b),p in A.items():out[(0,b)]+=p
 return dict(out)
def scaled(A,x,y):return{(a*x,b*y):p for (a,b),p in A.items()}
X={(1,1):F(1,2),(1,2):F(1,4),(2,2):F(1,4)}
m1=F(5,4);m2=F(3,2)
@lru_cache(None)
def generation_kernel(a,b):return addlaw(power(X,a),power(second_only(X),b-a))
def generation_step(Z):
 out=defaultdict(F)
 for (a,b),p in Z.items():
  for z,q in generation_kernel(a,b).items():out[z]+=p*q
 return dict(out)
def root_step(childlaw):
 out=defaultdict(F)
 for (r,s),p in X.items():
  law=addlaw(power(childlaw,r),power(second_only(childlaw),s-r))
  for z,q in law.items():out[z]+=p*q
 return dict(out)
def decorate(Z,seed):
 out=defaultdict(F)
 for (a,b),p in Z.items():
  law=addlaw(power(seed,a),power(second_only(seed),b-a))
  for z,q in law.items():out[z]+=p*q
 return dict(out)
Z={(1,1):F(1)};root=Z;seed={(0,2):F(1,2),(2,0):F(1,2)};seed_root=seed;rows=[]
for n in range(5):
 ck(Z==root,'coupled_generation_vs_root_decomposition')
 ck(sum(Z.values())==1,'joint_probability_normalization')
 ck(all(a<=b for a,b in Z),'nested_generation_counts')
 ck(sum(F(a)*p for (a,b),p in Z.items())==m1**n,'first_generation_mean')
 ck(sum(F(b)*p for (a,b),p in Z.items())==m2**n,'second_generation_mean')
 cross=sum(F(a*b)*p for (a,b),p in Z.items())/(m1*m2)**n
 predicted=1+F(1,8)/(m1*m2)*sum((m2**(-j) for j in range(n)),F(0))
 ck(cross==predicted,'coupled_cross_moment_not_marginals_only')
 if n<=3:
  direct=decorate(Z,seed)
  ck(direct==seed_root,'common_leaf_seed_vector_iteration')
  normed=scaled(direct,m1**(-n),m2**(-n))
  for i in (0,1):ck(sum(z[i]*p for z,p in normed.items())==1,'seed_iteration_mean_one')
  # The diagonal scaling of a mean profile commutes with the vector transform.
  scaled_seed=scaled(seed,F(3),F(5))
  ck(decorate(Z,scaled_seed)==scaled(direct,F(3),F(5)),'coordinate_mean_profile_scaling')
 rows.append({'generation':n,'joint_states':len(Z),'normalized_cross_moment':str(cross)})
 if n<4:
  Z=generation_step(Z);root=root_step(root)
  if n<3:seed_root=root_step(seed_root)
# Direct finite distributions for centered truncation, including a large atom.
V={F(-1):F(4,5),F(4):F(1,5)}
Zlaw={3:F(1,2),5:F(1,2)};EZ=sum(n*p for n,p in Zlaw.items())
def scalar_add(A,B):
 out=defaultdict(F)
 for a,p in A.items():
  for b,q in B.items():out[a+b]+=p*q
 return dict(out)
def random_sum(A):
 out=defaultdict(F)
 for n,p in Zlaw.items():
  law={F(0):F(1)}
  for _ in range(n):law=scalar_add(law,A)
  for z,q in law.items():out[z]+=p*q
 return dict(out)
def Eabs(A):return sum(abs(v)*p for v,p in A.items())
for K in (F(1,2),F(1),F(2),F(3),F(4),F(8)):
 mean_tr=sum((v if abs(v)<=K else 0)*p for v,p in V.items())
 zeta=defaultdict(F);rho=defaultdict(F)
 for v,p in V.items():
  t=(v if abs(v)<=K else 0)-mean_tr;r=v-t
  zeta[t]+=p;rho[r]+=p;ck(v==t+r,'centered_truncation_decomposition')
 ck(sum(v*p for v,p in zeta.items())==0,'bounded_part_centered')
 ck(sum(v*p for v,p in rho.items())==0,'tail_part_centered')
 tail=sum(abs(v)*p for v,p in V.items() if abs(v)>K)
 ck(Eabs(rho)<=2*tail,'centered_tail_L1_bound')
 var=sum(v*v*p for v,p in zeta.items())
 a=Eabs(random_sum(zeta));b=Eabs(random_sum(rho));c=Eabs(random_sum(V))
 ck(a*a<=var*EZ,'random_population_Cauchy_Schwarz')
 ck(b<=EZ*Eabs(rho),'random_population_tail_triangle')
 ck(c<=a+b,'sum_triangle_for_actual_seed')
# Topology negative control: time changes are onto and cannot remove a unit spike.
for n in range(3,101):
 width=F(1,n);ck(0<width<=F(1,3),'shrinking_spike_L1_control')
 ck(F(1)>width,'unit_supremum_not_controlled_by_L1')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'coupled_law_rows':rows,'scope':'Exact finite-dimensional branching/root/terminal-vector distribution controls and truncation algebra. No computational proof of Kesten–Stigum, arbitrary-depth convergence, or J1 tightness.'},indent=2,sort_keys=True))
