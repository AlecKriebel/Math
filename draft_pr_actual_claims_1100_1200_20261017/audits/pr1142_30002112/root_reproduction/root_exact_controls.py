"""Independent finite arithmetic diagnostics; no numerical geometric existence claim."""
from fractions import Fraction as F
from math import comb
from collections import Counter
import argparse,json,hashlib
from pathlib import Path

def need(ok,message):
 if not ok:raise RuntimeError(message)
def dim(m,l):return comb(l+m,m) if l>=0 else 0
def multiplicity(m,l,wrong=False):return dim(m,l)-(0 if wrong else dim(m,l-2))
def compositions(total,parts):
 if parts==1:yield (total,);return
 for a in range(total+1):
  for rest in compositions(total-a,parts-1):yield (a,)+rest
def at_rank(groups,k):
 for value,count in sorted(groups.items()):
  if k<=count:return value
  k-=count
 raise RuntimeError('Truncated spectrum insufficient')
def rank_case(m,q,wrong_index=False,wrong_gap=False,wrong_trace=False):
 T=q*(q+m-1);N=comb(q+m-1,m)+comb(q+m-2,m)
 sphere=Counter({l*(l+m-1):multiplicity(m,l,wrong_trace) for l in range(q+2)})
 prefix=sum(c for v,c in sphere.items() if v<T)
 need(prefix==N,'Harmonic trace subtraction and prefix count')
 groups=sphere.copy();groups[0]+=1
 groups[F(T)-F(1,q+1) if wrong_gap else F(T)+F(1,q+1)]+=3
 k=N+(1 if wrong_index else 2)
 need(at_rank(groups,k)==T,'Exact rank must count both boundary zeros and a strict inner gap')
 return k

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--mutant',choices=['wrong-index','wrong-gap','omit-harmonic-trace','invert-rescale','wrong-volume-exponent']);a=ap.parse_args()
 if a.mutant=='wrong-index':rank_case(2,1,wrong_index=True)
 if a.mutant=='wrong-gap':rank_case(2,1,wrong_gap=True)
 if a.mutant=='omit-harmonic-trace':rank_case(2,3,wrong_trace=True)
 if a.mutant=='invert-rescale':
  scale=F(3,2);S=F(7);area=S/scale**3
  need(area*(1/scale)**3==S,'Exact area rescaling direction')
 if a.mutant=='wrong-volume-exponent':need(F(3,2)*(1+F(2,2))==F(4,3),'Isoperimetric volume exponent')
 counts=Counter()
 for m in range(2,9):
  for l in range(8):
   actual=sum(1 for row in compositions(l,m+1))
   need(actual==dim(m,l),'Homogeneous monomial enumeration')
   lower=sum(1 for row in compositions(l-2,m+1)) if l>=2 else 0
   need(actual-lower==multiplicity(m,l),'Trace dimension subtraction')
   counts['enumerated_homogeneous_degrees']+=1
 for m in range(2,25):
  for q in range(1,101):
   k=rank_case(m,q)
   if q>=m:
    need(k<=2**(m+2)*q**m,'Dimension-only rank bound')
    need(k*k<=16**m*q**(2*m),'Universal Cm<=16 consequence')
    counts['large_q_rank_bounds']+=1
   counts['weighted_union_exact_ranks']+=1
 for m in range(2,65):
  need(F(m,m+1)*(1+F(2,m))==F(m+2,m+1),'Isoperimetric volume exponent')
  for scale in [F(2,3),F(9,10),F(10,9),F(3,2)]:
   S=F(m+3,m+1);lam=F(2*m+1,3);area=S/scale**m
   need(area*scale**m==S,'Exact area normalization')
   new_lam=lam/scale**2
   need(new_lam**m*S*S==lam**m*area*area,'Normalized eigenvalue scale invariance')
   counts['exact_rescaling_checks']+=1
  for rho in [F(1,2),F(2),F(10**6)]:
   for K in [F(1,10),F(3),F(10**12)]:
    old=None
    for t in range(2,21):
     q=t**m;A=F(q)+rho
     need(A/(q*q)<=(1+rho)/q,'Area-growth inequality')
     upper=K*(1+rho)/t**m+F(16,t*t)
     simple=(K*(1+rho)+16)/t**2
     need(upper<=simple,'Dimension-uniform subsequence upper estimate')
     if old is not None:need(upper<old,'Strictly decaying reciprocal upper bound')
     old=upper;counts['rational_subsequence_growth_checks']+=1
 result={'status':'PASS','counts':dict(counts),'limits':'Finite homogeneous-monomial enumeration, weighted spectra, scaling and algebra controls supplement the written universal proof. Synthetic high-gap cavity spectra are assumptions supplied by established existence inputs, not actual numerical smooth embeddings.','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
