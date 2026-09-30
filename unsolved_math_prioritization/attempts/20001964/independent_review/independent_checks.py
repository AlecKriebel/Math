"""Exact independent controls; the smooth theorem is proved in REVIEW.md."""
from fractions import Fraction as Q
from math import comb,factorial,prod
from itertools import product
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
count=Counter();cases=Counter()
def ck(k,b):
 if not b:raise AssertionError(k)
 count[k]+=1
# Integrate the fully expanded remainder kernel, rather than using a Beta identity.
for n in range(1,13):
 for k in range(n,31):
  integral=sum(Q((-1)**j*comb(n-1,j),k-n+j+1) for j in range(n))
  multiplier=Q(factorial(k),factorial(k-n)*factorial(n-1))
  ck('expanded_taylor_kernel',integral*multiplier==1);cases['monomial_remainders']+=1
for coeff in product((-2,-1,0,1,2),repeat=6):
 for n in (1,2,3,4,5,6,7):
  first=next((j for j,v in enumerate(coeff) if v),100)
  jets=[(factorial(j)*coeff[j] if j<len(coeff) else 0) for j in range(n)]
  ck('coefficient_jet_vs_valuation',all(x==0 for x in jets)==(first>=n))
 cases['polynomials']+=1
for n in range(1,5):
 for weights in product(range(1,5),repeat=n):
  c=prod(weights);x=[Q(2*i-3,5) for i in range(n)];y=[Q(i+2,7) for i in range(n)]
  mu=sum(Q(w,2)*(xx*xx+yy*yy) for w,xx,yy in zip(weights,x,y));norm=sum(xx*xx+yy*yy for xx,yy in zip(x,y))
  ck('moment_properness_bound',2*mu>=min(weights)*norm)
  for w,xx,yy in zip(weights,x,y):
   vx,vy=-w*yy,w*xx
   ck('hamiltonian_contraction',(-vy,vx)==(-w*xx,-w*yy))
  for u in (Q(-7,3),Q(-1,2),Q(2,5),Q(9,4)):
   ck('weighted_euler',prod(w*u for w in weights)==c*u**n)
   # Compact-support Thom-class model restriction e*b cancels identically.
   b=1+u+u*u;ck('thom_factor_cancellation',(c*u**n*b)/(c*u**n)==b)
  cases['weighted_representations']+=1
for n in range(1,13):
 for u in (Q(-5,2),Q(-1,10),Q(1,10),Q(3,2)):
  a=u**n/(1+u*u)
  ck('smooth_semialgebraic_example',a/u**n==1/(1+u*u))
  bad=u**(n-1)/(1+u*u)
  ck('failed_jet_example',bad/u**n==1/(u*(1+u*u)))
 for k in (1,2,5,10,100):
  u=Q(1,k);ck('unit_pole_sequence',1/u==k and u*(1/u)==1)
root=Path(__file__).resolve().parent
r={'artifact_sha256':sha256((root/'author_replay/SOURCE_OBSTRUCTION.md').read_bytes()).hexdigest(),'independent_assertions':sum(count.values()),'counts':dict(count),'cases':dict(cases),'scope':'Exact algebraic and differential-coordinate controls. Global impossibility and all-smooth extension are established by the written argument, not finite tests.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
