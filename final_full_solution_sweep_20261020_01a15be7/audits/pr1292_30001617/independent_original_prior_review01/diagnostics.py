"""Finite exact checks only; infinite theorem is proved in DERIVATION.md."""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict,Counter
import json,sys
STAGES=[(1,3,F(1,8)),(4,2,F(1,128))]
N=sum(m*L for m,L,a in STAGES)
COUNTS=Counter()
def check(ok,cat):
 COUNTS[cat]+=1
 if not ok:raise RuntimeError('check failed: '+cat)
def model(bits,stop=True,early_negative=False,carry=False):
 ds=[];blocks=[];stages=[];prior_active=True
 for m,L,a in STAGES:
  root=int(m**.5)
  if root*root!=m:raise RuntimeError('use square m for rational diagnostics')
  start=len(ds);active=prior_active if carry else True;first=None
  for h in range(L):
   s=len(ds);chunk=bits[s:s+m];on=active;local=on;bd=[]
   for r in chunk:
    bd.append(a/F(root)*r if local else F(0))
    if early_negative and r==-1:local=False
   ds.extend(bd);blocks.append((s,m,a,on,chunk,tuple(bd)))
   if on and all(r==1 for r in chunk):
    if first is None:first=s
    if stop:active=False
  prior_active=active;stages.append((start,len(ds),m,L,a,first))
 fn=[F(0)]
 for d in ds:fn.append(fn[-1]+d)
 return ds,fn,blocks,stages
paths=[]
for bits in product((-1,1),repeat=N):
 ds,fn,blocks,stages=model(bits);paths.append((bits,ds,fn,blocks,stages))
 check(sum(d*d for d in ds)<=sum(L*a*a for m,L,a in STAGES),'total_square_budget')
 for s,m,a,on,chunk,bd in blocks:
  check(sum(d*d for d in bd)==(a*a if on else 0),'whole_active_or_inactive_square')
  if not on:check(all(d==0 for d in bd),'inactive_increments_zero')
  if on and -1 in chunk and chunk[-1]==1:
   check(bd[-1]!=0,'negative_sign_does_not_stop_inside_block')
 for start,end,m,L,a,first in stages:
  check(ds[start]!=0,'stage_always_resets_active')
  check(sum(d*d for d in ds[start:end])<=L*a*a,'stage_square_budget')
  if first is not None:
   root=int(m**.5);R=fn[-1]-fn[end]
   check(fn[-1]-fn[first]==a*root+R,'successful_start_pathwise_sum')
   check(sum(d*d for d in ds[first:])==a*a+sum(d*d for d in ds[end:]),'successful_start_tail_identity')
   check(all(d==0 for d in ds[first+m:end]),'post_success_zero')
 # This is a finite terminal function on each depth-N dyadic atom.
 for n in range(N+1):
  check(fn[-1]-fn[n]==sum(ds[n:],F(0)),'finite_terminal_tail_identity')
# Every atom/prefix: zero conditional mean, predictable coefficient, terminal average.
for n in range(N):
 groups=defaultdict(list)
 for x in paths:groups[x[0][:n]].append(x)
 for pref,vals in groups.items():
  check(sum(x[1][n] for x in vals)==0,'prefix_conditional_mean_zero')
  check(len({x[1][n]*x[0][n] for x in vals})==1,'prefix_predictable_coefficient')
  check(sum(x[2][-1] for x in vals)/len(vals)==vals[0][2][n],'genuine_dyadic_terminal_average')
for i in range(N):
 for j in range(i+1,N):check(sum(x[1][i]*x[1][j] for x in paths)==0,'difference_orthogonality')
check(sum(x[2][-1]**2 for x in paths)==sum(sum(d*d for d in x[1]) for x in paths),'L2_isometry')
for k,(m,L,a) in enumerate(STAGES):
 failures=sum(x[4][k][-1] is None for x in paths)
 check(F(failures,len(paths))==(1-F(1,2**m))**L,'exact_stage_failure_probability')
# Positive/negative branches of one same-atom realized tail: no title/claim assumptions.
m,L,a=STAGES[1];start=STAGES[0][0]*STAGES[0][1]
for pref in product((-1,1),repeat=start):
 vals=[x for x in paths if x[0][:start]==pref]
 qs=[sum(d*d for d in x[1][start:]) for x in vals]
 check(min(qs)==a*a and max(qs)==L*a*a,'within_atom_realized_tail_variation')
# A chosen successful-start index need not be a stopping time.
start_zero={x[4][0][-1]==0 for x in paths}
check(start_zero=={False,True},'successful_start_zero_not_F0_measurable')
# Deliberate mutations must actually falsify a relevant identity.
check(sum(F(1,8)*x[0][0] if x[0][0]==1 else 0 for x in paths)!=0,'REJECT_anticipative_activation_nonzero_mean')
no_stop=early=carry=0
for bits,ds,fn,blocks,stages in paths:
 bd,bf,bb,bs=model(bits,stop=False)
 for start,end,m,L,a,first in bs:
  if first is not None and bf[-1]-bf[first] != a*int(m**.5)+(bf[-1]-bf[end]):no_stop+=1
 ed,ef,eb,es=model(bits,early_negative=True)
 if any(on and sum(d*d for d in vals)!=a*a for s,m,a,on,chunk,vals in eb):early+=1
 cd,cf,cb,cs=model(bits,carry=True)
 if cd[cs[1][0]]==0:carry+=1
check(no_stop>0,'REJECT_no_post_success_stop_breaks_tail_identity')
check(early>0,'REJECT_early_negative_stop_breaks_whole_block_square')
check(carry>0,'REJECT_carry_inactive_state_breaks_next_stage_positive_block')
# Exact dyadic geometry for zero extension at rational sample points.
for n in range(8):
 for j in range(2**n):
  left=F(j,2**n);right=F(j+1,2**n);x=(left+right)/2
  check(0<=left<=x<right<=1 and right-left==F(1,2**n),'zero_extension_dyadic_geometry')
# Deterministic future-budget instance, not the analytic infinite parameter selection.
check(STAGES[1][1]*STAGES[1][2]**2<=F(1,2)*STAGES[0][2]**2,'finite_future_budget_example')
print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'paths':len(paths),'digits':N,'stages':[{'m':m,'L':L,'a':str(a)} for m,L,a in STAGES],'checks':sum(COUNTS.values()),'categories':dict(sorted(COUNTS.items())),'mutation_counterexamples':{'without_post_success_stop':no_stop,'early_negative_stop':early,'carried_inactive_state':carry},'scope':'Exact finite algebra only; no infinite-stage computation or analytic parameter execution; no historical PR check-count reproduction claimed.'},indent=2))
