"""Independent exact finite controls for priority implications, not RWRE simulation."""
from fractions import Fraction as F
from itertools import product
from math import ceil,log,sqrt
import json,hashlib
from pathlib import Path

assertions=0
def ck(b):
 global assertions
 assertions+=1
 assert b

def coarse(mu,al,w,shift):
 d={}
 for i,(a,b) in enumerate(zip(mu,al)):
  j=(i-shift)//w;d[j]=d.get(j,F(0))+a-b
 return sum(map(abs,d.values()))

def crossed_alpha(al,m,sfine,M,starget):
 groups={}
 for i,a in enumerate(al):groups.setdefault((i-sfine)//m,[]).append((i,a))
 return sum(a for group in groups.values() if len({(i-starget)//M for i,a in group})>1 for i,a in group)

# General arbitrary-alignment comparison: L_target <= L_fine + 2 alpha(B).
# B is the union of complete fine cells split by target boundaries.
# Enumerate strictly positive rational distributions and arbitrary 1D interval grids.
for n in range(2,8):
 for v in product((1,2),repeat=n):
  mu=[F(x,sum(v)) for x in v]
  al=[F(1,n) for _ in v]
  for m in range(1,5):
   for M in range(1,6):
    for s in range(m):
     for t in range(M):
      ck(coarse(mu,al,M,t)<=coarse(mu,al,m,s)+2*crossed_alpha(al,m,s,M,t))

# Weak convergence alone cannot control a slowly diverging coarse scale.
# Abstract probability measures, not a claim of an RWRE counterexample.
controls=[]
for r in (10,20,40,80):
 m=4 # can diverge independently, e.g. m=ceil(log log N); ratio m/(2rm)=1/(2r).
 L=2*r*m
 al=[F(1,L)]*L
 mu=[F(2,L) if (i//m)%2==0 else F(0) for i in range(L)]
 ck(sum(mu)==1)
 ck(coarse(mu,al,m,0)==1)
 # Scaled coordinate in [0,1]: any 1-Lipschitz f changes at most 1/r over a pair.
 # Coupling moves the missing half-block mass by at most m/L; W1 <= m/(2L).
 ck(F(m,2*L)==F(1,4*r))
 for M in (8,16,32,64,128):
  for shift in range(M):
   c=coarse(mu,al,M,shift)
   ck(c<=F(2*m,M)+F(2*m,L))
 controls.append({'r':r,'slow_scale_L1':'1','Wasserstein1_upper':str(F(1,4*r))})

# Copying a target law along added spatial coordinates violates iid.
# Replacing the copies by independent laws changes projected quenched distribution.
q=F(1,2);s=F(5,16) # p takes 1/4,3/4 equiprobably, E[p^2]=5/16.
native_var=s*s-q**4
independent_lift_var=s*(s+q*q)/2-q**4
ck(native_var-independent_lift_var==s*(s-q*q)/2)
ck(native_var>independent_lift_var)

# Uniform ellipticity static theorem cannot directly contain a NE-directed encoding:
# the two backward coordinate transition probabilities are exactly zero.
for p in (F(1,100),F(1,4),F(1,2),F(99,100)):
 ne=[p,1-p,F(0),F(0)]
 ck(sum(ne)==1)
 ck(min(ne)==0)

receipt={'assertions':assertions,'coarsening_bound_verified':True,'abstract_weak_vs_coarse_controls':controls,'lift_native_variance':str(native_var),'lift_independent_copy_variance':str(independent_lift_var),'scope':'Finite exact checks support analytic implication/non-implication notes; no literature theorem or RWRE asymptotic is numerically certified.'}
p=Path(__file__).with_name('implication_checks_receipt.json');p.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
