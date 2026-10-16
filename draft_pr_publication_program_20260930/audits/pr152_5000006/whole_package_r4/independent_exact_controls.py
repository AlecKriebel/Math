from fractions import Fraction as Q
from pathlib import Path
from math import gcd
import json
R=Path(__file__).resolve().parent
counts={}
def ck(n,v):
 if not v:raise RuntimeError(n)
 counts[n]=counts.get(n,0)+1
# A second implementation constructs intervals directly from the printed
# four branches instead of sampling endpoint angle pairs like the package.
for n in range(3,129):
 d=Q(n-2,n);h=n//2;M=n-2
 for parity in ('sum','difference'):
  for s in range(-n,n+1):
   if parity=='sum': lo=max(Q(0),Q(2*s,n)-1);hi=min(d,Q(2*(s-1),n));expected=(n-1-s)%M
   else: lo=max(Q(0),Q(2*(1-s),n));hi=min(d,1-Q(2*s,n));expected=(s-1)%M
   if lo>hi:continue
   intervals=[]
   for k in range(n-1):
    if parity=='sum':
     if s!=n-k-1:continue
     if n%2==0:
      clauses=[(k<=h-1,max(Q(0),Q(h-k-1,h)),d),(k>=h-1,Q(0),min(d,Q(n-k-2,h)))]
     else:
      clauses=[(k<=h-1,max(Q(0),Q(n-2*(k+1),n)),d),(k>=h,Q(0),min(d,Q(2*(n-k-2),n)))]
    else:
     if n%2==0:
      clauses=[(k<=h-1 and s==k+1,Q(0),min(d,Q(h-k-1,h))),(k>=h-1 and s==k+3-n,max(Q(0),Q(n-k-2,h)),d)]
     else:
      clauses=[(k<=h+1 and s==k+1,Q(0),min(d,Q(n-2*(k+1),n))),(k>=h and s==k+3-n,max(Q(0),Q(2*(n-k-2),n)),d)]
    for ok,a,b in clauses:
     a=max(a,lo);b=min(b,hi)
     if ok and a<=b:ck('literal_clause_label',k%M==expected);intervals.append((a,b))
   ck('source_intervals_nonempty',bool(intervals))
   intervals.sort();a,b=intervals[0];ck('source_left_endpoint',a==lo)
   for c,e in intervals[1:]:ck('source_no_interval_gap',c<=b);b=max(b,e)
   ck('source_right_endpoint',b==hi)
 # Whole cone winding ambiguity independently: multiply original cone
 # angle by n/(2pi) in the dictionary congruence.
 r=M if n%2 else M//2
 ck('cone_lift_modulo',n*r%M==0)
 for m in range(r):
  for e in ([0] if n%2 else [0,1]):
   K=(2*m+1-e)%M
   rev=(-m-(e==0))%r
   ck('intrinsic_reversal',(2*rev+1-e)%M==(-K)%M)
# Independent marked-hexagon algebra controls in a larger box.
for p in range(-40,41):
 for q in range(-40,41):
  if gcd(p,q)!=1:continue
  s=(p+q)%3;scale=2 if s==2 else 1
  w2={0:Q(3,4),1:Q(1,4),2:Q(1)}[s]
  expected=Q(4,3) if s==0 else Q(4)
  ck('hex_length_weight',Q(scale*scale)/w2==expected)
  for a,b in [(q,p),(p-q,p)]:
   ck('hex_dihedral_norm',a*a-a*b+b*b==p*p-p*q+q*q)
   ck('hex_dihedral_residue',(a+b)%3 in {s,(-s)%3})
   ck('hex_dihedral_primitive',gcd(a,b)==1)
receipt={'status':'PASS','range_n':[3,128],'hex_box':[-40,40],'counts':counts,'exact_checks':sum(counts.values()),'scope':'Independent finite interval-union certificates from literal Fuchs branches; all feasible angle intervals covered for tested n. Independent cone winding/reversal and marked-lattice algebra. Universal lemmas are proved in DERIVATIONS.md, not inferred from this range.'}
(R/'artifacts'/'INDEPENDENT_EXACT_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
