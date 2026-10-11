"""Own exact arithmetic controls from independently derived equations; no input code."""
from fractions import Fraction as F
import json
from itertools import product

rows=[]
for n in [0,1,2,7,31,127]:
 for r in [0,1,2,5,12]:
  nf=F(1);corr=F(1)
  for k in range(n,n+r):nf*=F(k+1,k+2);corr*=F(k,k+2)
  assert nf==F(n+1,n+r+1)
  if r:assert corr==F(n*(n+1),(n+r)*(n+r+1))
  gap=(1-corr)/2
  assert gap<=F(r,n+r+1)<=F(r,n+1)
  rows.append({'n':n,'r':r,'no_flip':str(nf),'correlation':str(corr),'mismatch':str(gap),'tv':str(1-nf)})
truth=[]
for a,b,c in product([-1,1],repeat=3):
 e=abs(int(a!=c)-int(b!=c));assert e<=int(a!=b)
 truth.append({'x':a,'future_x':b,'fixed_comparison':c,'indicator_error':e,'pair_mismatch':int(a!=b)})
eachn=[]
for n in [0,1,10,1000]:
 eachn.append({'n':n,'per_n_B':'X_n','zeroth_error':0,'metric_expectation_upper_bound':str(F(1,n+1)),'one_fixed_comparison':False})
escaping=[]
for n in [0,1,10,1000]:
 for M in [0,1,7,100]:
  nohit=F(1,2)
  for k in range(n,n+M):nohit*=F(k+1,k+2)
  assert nohit==F(n+1,2*(n+M+1))
  escaping.append({'n':n,'M':M,'first_hit_tail':str(nohit),'tight_as_n_grows':False})
summable=[]
for n in [0,1,7]:
 for N in [n,n+1,n+19]:
  p=F(1)
  for k in range(n,N+1):p*=1-F(1,(k+2)**2)
  expected=F(n+1,n+2)*F(N+3,N+2);assert p==expected
  summable.append({'n':n,'N_inclusive':N,'no_future_flips_to_N':str(p),'infinite_no_flip_limit':str(F(n+1,n+2))})
print(json.dumps({'schema':'pr45-own-original-hostile-controls/v1','rare_flip_equation_rows':rows,'complete_metric_indicator_truth_table':truth,'each_n_coupling_loophole':eachn,'escaping_offset_rows':escaping,'summable_flip_boundary':summable,'scaled_metric_law':{'original_endpoints':[0,1],'two_times_metric_endpoints':[0,2]},'limits':'arithmetic and hostile boundary examples only; full-path all-fixed-coupling proof remains written'},indent=2))
