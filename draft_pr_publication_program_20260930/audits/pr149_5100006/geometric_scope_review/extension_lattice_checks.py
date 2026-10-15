#!/usr/bin/env python3
"""Independent exact rational divisor-coset diagnostics, full sn lattice.
This finite check supports but does not replace the infinite congruence proof.
"""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import math,json,datetime

def fracmod(x): return x % 1

def divisor(n,tau,sign):
 step=F(tau,n)
 # The g+ zeros are -K +/- v; g- zeros are +K +/- v.
 quarter=F(-1 if sign=='+' else 1,4)
 roots=[quarter+F(tau,2*n),quarter-F(tau,2*n)]
 counts=Counter()
 for j in range(n):
  for root in roots: counts[fracmod(root-j*step)]+=1
  for pole in [F(0),F(1,2)]: counts[fracmod(pole-j*step)]-=1
 return {point:order for point,order in counts.items() if order}

rows=[]
for n in range(3,101):
 for tau in range(1,(n+1)//2):
  if math.gcd(n,tau)!=1:continue
  should_constant=(n%4==2)
  for sign in ['+','-']:
   d=divisor(n,tau,sign)
   assert (len(d)==0)==should_constant,(n,tau,sign,d)
   poles={p:-order for p,order in d.items() if order<0}
   zeros={p:order for p,order in d.items() if order>0}
   if not should_constant:
    assert sum(poles.values())==2*n
    assert sum(zeros.values())==2*n
    assert len(poles)==(2*n if n%2 else n)
    assert set(poles.values())==({1} if n%2 else {2})
   rows.append({'n':n,'tau':tau,'focus':sign,'constant_divisor':not d,'uncancelled_distinct_poles':len(poles),'uncancelled_total_pole_order':sum(poles.values())})
result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_arithmetic':'fractions.Fraction','diagnostic_only_finite_range':True,'n_range':[3,100],'focus_cases':len(rows),'all_passed':True,'case_results':rows}
Path('extension_lattice_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['n_range','focus_cases','all_passed']}))
