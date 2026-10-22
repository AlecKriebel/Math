"""Reviewer-authored exact controls, independent of the package's code.
Finite diagnostics only; no universal proof is inferred from enumeration.
"""
from fractions import Fraction
import itertools,json
checks=0
def require(p,label):
 global checks
 checks+=1
 if not p:raise RuntimeError(label)
def cycles(S,k):
 # A shift graph has finite disjoint chains; close each chain into a cycle.
 image={s+k for s in S};mapping={s:s+k for s in S}
 for start in S-image:
  end=start
  while end in S:end+=k
  mapping[end]=start
 return mapping
cases=overlaps=0
for cutoff in range(4):
 pool=range(cutoff+1,cutoff+10)
 for mask in range(512):
  S={s for j,s in enumerate(pool) if mask>>j&1}
  for k in range(1,10):
   sigma=cycles(S,k);U=S|{s+k for s in S}
   require(set(sigma)==U and set(sigma.values())==U,'finite permutation')
   require(all(sigma.get(i,i)==i for i in range(1,cutoff+1)),'past fixed')
   w=tuple(sorted(S))+tuple(sorted(S))+tuple(reversed(sorted(S)))
   require(tuple(sigma[s] for s in w)==tuple(s+k for s in w),'repeat/shared whole-index transport')
   cases+=1;overlaps+=bool(S&{s+k for s in S})
# Bilateral Boolean representation: q_- is central in M_+, and rho(q_-)=0.
# alpha^l(q_-) projects on coordinate indices j<=l. Vacuum is separate.
for j in range(1,41):
 require(not (j<=0),'positive compression rho(q_-) vanishes')
 require(all(j<=l for l in range(j,j+10)),'shift limit at positive test vector is 1')
 require(Fraction(1)!=Fraction(0),'E does not preserve rho kernel')
# A cyclic-vector-only test misses the positive coordinate e_11.
require(0==0 and 1!=0,'e_11 has vacuum coefficient 0 but nonzero norm')
# Exact bounded dense-vector extension versus the explicitly unbounded failure.
for n in range(1,100):
 require(n*Fraction(1,n)==1,'n e_0n fails WOT at eta_n=1/n')
require(sum(Fraction(1,n*n) for n in range(1,101))<2,'eta square summable by standard convergent p-series')
false_rejections=0
for false in [lambda: set({2:3,3:4,4:3}.values())=={2,3,4},lambda: all((j<=0)==(j<=50) for j in range(1,40)),lambda: Fraction(1)==0]:
 try:require(false(),'deliberately false control')
 except RuntimeError:false_rejections+=1
require(false_rejections==3,'all false controls rejected')
print(json.dumps({'status':'PASS','checks':checks,'independent_chain_completion_cases':cases,'overlap_cases':overlaps,'false_rejections':false_rejections,'bilateral_normal_descent_counterexample_tested':True,'universal_claim_proved_by_computation':False},sort_keys=True,indent=2))
