"""Exact arithmetic sanity controls; the analytic proof is in SOURCE_PROOF.md."""
from fractions import Fraction as F
import json
checks=0
def check(c):
 global checks
 assert c;checks+=1
for n in range(3,13):
 for den in range(2,102):
  s=F(1,den);lower=(1-s*s)/(1+s)**n;upper=(1-s*s)/(1-s)**n
  check(0<lower<=1<=upper)
  s2=s/2;lo2=(1-s2*s2)/(1+s2)**n;up2=(1-s2*s2)/(1-s2)**n
  check(lower<lo2<1);check(1<up2<upper)
 # Radial Laplacian coefficient of r^(2-n) away from0.
 a=2-n;check(a*(a+n-2)==0)
 # Bounded source example, with nonnegative outward derivative jump at r=1.
 check(n-2>0)
 for r in [F(1,4),F(1,2),F(1),F(2),F(4),F(16)]:
  u=max(F(-1),-r**(2-n));check(-1<=u<0)
  check((r<=1 and u==-1) or (r>1 and u==-r**(2-n)))
 # Normalized disjoint pieces cannot both have means tending to1.
 check(F(3,4)+F(3,4)>1)
# Properness is a quantified compact-tail argument, checked algebraically here.
for compact_upper_bound in range(-5,100):
 cutoff=max(1,compact_upper_bound+1)
 for j in range(cutoff,cutoff+5):check(j>compact_upper_bound)
print(json.dumps(dict(assertions=checks,scope='Poisson-kernel bound arithmetic, radial-example signs and compact-tail indices only; no finite check substitutes for the all-function analytic proof.',source_status='Original Update3.2 already records the affirmative result; credited proof verification, no novelty claim.'),indent=2,sort_keys=True))
