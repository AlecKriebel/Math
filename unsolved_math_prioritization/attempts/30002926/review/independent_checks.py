#!/usr/bin/env python3
"""Independent exact diagnostics for the physical-clock obstruction."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
from math import factorial
from collections import Counter
import json
C=Counter()
def ck(group,b):
 assert b,group
 C[group]+=1

def solve(A,b):
 T=[[F(v) for v in row]+[F(y)] for row,y in zip(A,b)];n=len(b)
 for j in range(n):
  i=next(i for i in range(j,n) if T[i][j]);T[i],T[j]=T[j],T[i]
  v=T[j][j];T[j]=[x/v for x in T[j]]
  for i in range(n):
   if i!=j and T[i][j]:
    v=T[i][j];T[i]=[x-v*y for x,y in zip(T[i],T[j])]
 return [T[i][-1] for i in range(n)]
def mv(A,v):return [sum(a*x for a,x in zip(row,v)) for row in A]

type_cases=0
for fs in [(F(1,5),F(3,5)),(F(1,4),F(1,2),F(3,4)),(F(1,3),F(2,3),F(4,5))]:
 for raw in product((1,2),repeat=len(fs)):
  ps=[F(v,sum(raw)) for v in raw];I=sum(p/(1-f) for p,f in zip(ps,fs))
  for beta in (F(1,10),F(1,5),F(1,4),F(1,3)):
   rho=1-beta*I;c=1-beta
   if rho<=0:continue
   # Backward discounted first-moment generator on starting fitness.
   B=[[beta*f*ps[j]-(c*(1-f) if i==j else 0) for j in range(len(fs))] for i,f in enumerate(fs)]
   v=solve([[-x for x in row] for row in B],[1]*len(fs))
   ck('finite_type_resolvent_average',sum(p*x for p,x in zip(ps,v))==I/rho)
   ck('finite_type_resolvent_positive',all(x>0 for x in v))
   ck('finite_type_resolvent_formula',all(vv==(1+beta*f*I/rho)/(c*(1-f)) for vv,f in zip(v,fs)))
   # Laplace resolvent s>0, computed directly and from the renewal transform.
   for s in (F(1,3),F(1),F(3)):
    R=solve([[s*(i==j)-B[i][j] for j in range(len(fs))] for i in range(len(fs))],[1]*len(fs))
    ah=sum(p/(s+c*(1-f)) for p,f in zip(ps,fs))
    kh=beta*sum(p*f/(s+c*(1-f)) for p,f in zip(ps,fs))
    ck('finite_type_laplace_renewal',sum(p*x for p,x in zip(ps,R))==ah/(1-kh))
    ck('finite_type_discounted_laplace_bound',all(s*x<=1/rho for x in R))
   # Direct matrix powers against differentiated scalar renewal, twelve orders.
   g=[F(1)]*len(fs);direct=[]
   for n in range(12):direct.append(sum(p*x for p,x in zip(ps,g)));g=mv(B,g)
   out=[]
   for n in range(12):
    forcing=sum(p*(-c*(1-f))**n for p,f in zip(ps,fs))
    out.append(forcing+sum(beta*sum(p*f*(-c*(1-f))**j for p,f in zip(ps,fs))*out[n-1-j] for j in range(n)))
   ck('finite_type_time_derivatives',direct==out)
   type_cases+=1

# Exact genealogical partition with every pre-cut individual retained as a root.
trees=0;partitions=0
for n in range(2,7):
 for parents_tail in product(*(range(j) for j in range(1,n))):
  parents=(-1,)+parents_tail;trees+=1
  for cut in (1,max(1,n//2),n-1):
   for flags in product((False,True),repeat=n-cut):
    mutant={j for j,v in zip(range(cut,n),flags) if v}
    roots=list(range(cut))+sorted(mutant)
    groups={root:set() for root in roots}
    for root in roots:
     stack=[root]
     while stack:
      z=stack.pop();groups[root].add(z)
      stack.extend(j for j in range(cut,n) if parents[j]==z and j not in mutant)
    union=set().union(*groups.values())
    ck('genealogy_no_loss',union==set(range(n)))
    ck('genealogy_no_double_count',sum(map(len,groups.values()))==n)
    for j in range(n):
     z=j
     while z>=cut and z not in mutant:z=parents[z]
     ck('genealogy_most_recent_mutation',j in groups[z])
    # Fitness can coincide between different groups; classification remains disjoint.
    fit={r:F((r%3)+1,4) for r in roots}
    band={r for r in roots if fit[r]>F(1,2)}
    direct=sum(any(j in groups[r] and r in band for r in roots) for j in range(n))
    ck('genealogy_band_count',direct==sum(len(groups[r]) for r in band))
    partitions+=1

# A different tail family: mixtures of two beta(1,a) densities, all integrals exact.
mixtures=0
for a,b in ((2,3),(2,5),(3,6),(4,7)):
 for w in (F(1,4),F(1,2),F(3,4)):
  I=w*F(a,a-1)+(1-w)*F(b,b-1)
  for beta in (F(1,5),F(1,4),F(1,3)):
   rho=1-beta*I;c=1-beta
   if rho<=0:continue
   ck('mixture_uniform_constant',1+beta*I/rho==1/rho)
   for eps in (F(1,100),F(1,10),F(1,3)):
    tail=w*eps**a+(1-w)*eps**b
    integral=w*F(a,a-1)*eps**(a-1)+(1-w)*F(b,b-1)*eps**(b-1)
    ck('mixture_tail_integrability',tail/eps<=integral)
    ck('mixture_late_mutant_decay',2*(w*(eps/2)**a+(1-w)*(eps/2)**b)<=tail/2)
   mixtures+=1

# Gamma density ratio with half-integral shapes as well as integers:
# logarithmic derivative is independent of shape and mass.
for k in (F(1,2),F(3,2),F(2),F(7,2),F(5)):
 for q in (F(5,4),F(3,2),F(2),F(4)):
  for lam,c in product((F(1,4),F(3,4),F(1),F(5,3)),repeat=2):
   x=F(7,5)
   # log h(x) derivative, and chain rule applied to h(x/q).
   right=-(c*(q-1)/q)+((k-1)/(x/q)-lam)/q-((k-1)/x-lam)
   ck('gamma_ratio_log_derivative',right==(lam-c)*(q-1)/q)
   ck('gamma_constant_ratio_iff_clock',(right==0)==(lam==c))
# Rescaling s=c t sends a rate-c random variable t(1-f) to rate one.
for c in (F(1,4),F(1,2),F(3,4)):
 for t,x in product((F(2),F(5),F(10)),(F(1,3),F(1),F(2))):
  f=1-x/(c*t)
  ck('physical_to_clone_clock',c*t*(1-f)==x)
ck('advertised_distinct_limits',F(1,4)!=F(16,49))
ck('advertised_exponential_gap',F(1)-F(1+F(3,4),2)==F(1,8))
root=Path(__file__).resolve().parent
out={'verdict':'PASS_EXACT_INDEPENDENT_CONTROLS','assertions':sum(C.values()),'groups':dict(sorted(C.items())),'finite_type_cases':type_cases,'recursive_trees':trees,'genealogical_partitions':partitions,'mixture_cases':mixtures,'reviewed_artifact_sha256':sha256((root/'author_replay/CLOCK_OBSTRUCTION.md').read_bytes()).hexdigest(),'limitations':'Finite-type controls do not have essential supremum one and are used only to check the renewal mechanism; no simulation or proof of corrected-profile existence.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'assertions':out['assertions'],'verdict':out['verdict']}))
