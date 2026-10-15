"""Exact scope control: fixed pants-type law is not the all-type area mixture.
Uses the displayed product density in the fixed-type source, i.e. Dirichlet2.
This is a model comparison, not a theorem about the original all-type ensemble.
"""
from fractions import Fraction as F
from math import comb,log,log1p,sqrt
import json
checks=0
for n in range(2,25):
 b=2*n-2; M=b+1
 for x in [F(1,10),F(1,4),F(1,2),F(3,4),F(9,10)]:
  # Integer Beta2,b survival from its full Bernstein/binomial tail.
  survival=1-sum((F(comb(M,k))*x**k*(1-x)**(M-k) for k in range(2,M+1)),F(0))
  formula=(1-x)**b*(1+b*x)
  assert survival==formula
  checks+=1
rows=[]
for g in [10,100,1000,10000,1000000]:
 n=3*g-3;x=1/sqrt(g);b=2*n-2
 rows.append({'g':g,'n':n,'log_upper_bound_on_expected_window_count':log(n)+b*log1p(-x)+log1p(b*x)})
print(json.dumps({'status':'PASS','exact_checks':checks,'comparison':'Conditional pants Dirichlet2,n law has mesoscopic window mean tending to0; original all-type target has proposed limit log2/2. Hence the fixed-topology theorem cannot be substituted for the full random-type mixture.','finite_diagnostics_not_enclosures':rows},indent=2,sort_keys=True))
