#!/usr/bin/env python3
"""Fresh exact scalar/finite controls for the proof's sensitive steps.
These are diagnostic models, never asserted to be valid SIRSNs.
No reviewed module is imported or executed.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import datetime,json,os
R=Path(__file__).resolve().parent
checks=[]
def check(name,value,detail):
 if not value:raise ValueError(name)
 checks.append({'name':name,'result':'PASS','detail':detail})
def main():
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 # Euclidean area expansions and finite dyadic major-road sums, no geometry
 # or simulated route law substituted for the written set inclusion.
 for n in [F(1),F(7,2),F(13)]:
  check('unit_strip_'+str(n),(n+2)**2-n*n==4*n+4,str(4*n+4))
  for r in [F(1,4),F(1),F(19,3)]:
   check('annular_area_'+str(n)+'_'+str(r),(n+4*r)**2-(n+2*r)**2==4*n*r+12*r*r,str(4*n*r+12*r*r))
 for J in range(10):
  radii=[F(2**j) for j in range(J+1)];Rcut=F(2**J)
  check('dyadic_sum_'+str(J),sum(radii)==2*Rcut-1 and sum(radii)<=2*Rcut,str(sum(radii)))
  n=F(17,3);p=F(5,4)
  check('dyadic_middle_bound_'+str(J),sum(p*(4*n+12*r) for r in radii)<=4*p*n*(J+1)+24*p*Rcut,str(sum(p*(4*n+12*r) for r in radii)))
 # Every term of the shifted Poisson factorial-moment identity, including
 # strict >k at k=0,1 where the factorial prefactor makes missing terms zero.
 for mu in [F(1,3),F(3),F(19,2)]:
  for k in [0,1,2,6]:
   mmax=12
   left=sum(F(m*(m-1))*mu**m/F(factorial(m)) for m in range(mmax+1) if m>k)
   right=mu**2*sum(mu**j/F(factorial(j)) for j in range(mmax-1) if j>k-2)
   check('poisson_factorial_shift_'+str(mu)+'_'+str(k),left==right,str(left))
 # Strict versus nonstrict atom cutoff and the tail integral formula for a
 # finite positive atomic variable. Integrals are exact rectangular areas.
 atoms=[(F(1),F(1,6)),(F(4),F(1,2)),(F(11),F(1,3))]
 for t in [F(1),F(2),F(4),F(7),F(11)]:
  strict=sum(x*p for x,p in atoms if x>t)
  integral=sum(max(x-t,F(0))*p for x,p in atoms)
  ptail=sum(p for x,p in atoms if x>t)
  ge=sum(x*p for x,p in atoms if x>=t)
  half_strict=sum(x*p for x,p in atoms if x>t/2)
  check('layer_cake_'+str(t),strict==t*ptail+integral,str(strict))
  check('atom_half_cutoff_'+str(t),ge<=half_strict,{'nonstrict':str(ge),'half_strict':str(half_strict)})
  if t in [1,4,11]:check('strict_atom_gap_'+str(t),ge>strict,{'gap':str(ge-strict)})
 for d in [F(0),F(1),F(4),F(11)]:
  for c in [F(1,4),F(1),F(3)]:
   cutoff=F(3);upper=F(3)
   left=c*d*(c*d>=cutoff);right=upper*d*(upper*d>=cutoff)
   check('scale_uniform_sup_'+str(d)+'_'+str(c),left<=right,{'left':str(left),'right':str(right)})
 # Exact infinite geometric atomic laws are specified by q and normalization
 # A. Partial mass/mean plus exact remainders check the credited series. Their
 # scalar tails show finite mean does not imply the fourth-order rate.
 for q in [2,4,5]:
  a=1-F(1,2**q);mean=a/(1-F(1,2**(q-1)))
  for m in range(8):
   mass=sum(a*F(1,2**(q*j)) for j in range(m+1));rem=F(1,2**(q*(m+1)))
   partial=sum(a*F(1,2**((q-1)*j)) for j in range(m+1));meanrem=mean*F(1,2**((q-1)*(m+1)))
   check('atomic_mass_'+str(q)+'_'+str(m),mass+rem==1,str(rem))
   check('atomic_mean_'+str(q)+'_'+str(m),partial+meanrem==mean,str(mean))
   normalized=F(2**(4*m))*rem
   expected=F(2**max((4-q)*m-q,0),2**max(-((4-q)*m-q),0))
   check('fourth_order_strict_tail_'+str(q)+'_'+str(m),normalized==expected,str(normalized))
  if q==4:check('critical_tail_not_little_o',F(2**(4*7),2**(4*8))==F(1,16),'positive constant at every dyadic cutoff')
  if q==5:check('fifth_order_atomic_fourth_moment',a/(1-F(1,2))==F(31,16),'exact convergent fourth-moment series')
 # Independence in the count sandwich cannot be replaced by a correlated
 # random count: this two-state model falsifies that algebraic shortcut only.
 ef=F(1,2);prob=F(1,2);joint=F(0)
 check('dependent_count_factorization_rejected',joint<ef*prob,{'joint':str(joint),'false_product':str(ef*prob)})
 obj={'status':'PASS_OWN_INDEPENDENT_EXACT_MATH_BOUNDARY_CONTROLS','pid':os.getpid(),'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':len(checks),'failed':0,'checks':checks,'scope':'Exact finite algebra, Poisson series coefficients and scalar atomic-law boundary diagnostics. Not SIRSN constructions, not proof by computation, not a new substantive target attempt.','candidate_helper_imports_or_execution':False,'new_substantive_attempts':0,'audit_turns':0}
 (R/'INDEPENDENT_MATH_BOUNDARY_RESULTS.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps({k:v for k,v in obj.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
