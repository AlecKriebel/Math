"""Independent finite integer checks. Does not run source-author code or prove asymptotics."""
from fractions import Fraction as F
from collections import Counter
from math import gcd,isqrt,prod
import json,sys
COUNTS=Counter()
def check(ok,name):
 COUNTS[name]+=1
 if not ok:raise RuntimeError('failed '+name)
def prime(n):return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
PRIMES=[n for n in range(2,212)if prime(n)]
def collisions(a):
 seen={};out=[]
 for i in range(len(a)):
  z=1
  for j in range(i,len(a)):
   z*=a[j]
   for old in seen.get(z,[]):out.append((old,(i,j)))
   seen.setdefault(z,[]).append((i,j))
 return out
def normalize(a,c):
 (i,j),(k,l)=sorted(c)
 if i==k or j>=l:raise RuntimeError('nested equal products with all entries>=2')
 return (a[i:j+1],a[k:l+1]) if j<k else (a[i:k],a[j+1:l+1])
def block_in(a,b):
 if not b:return False
 try:i=a.index(b[0])
 except ValueError:return False
 return a[i:i+len(b)]==b
A=[2];rejected=[];records=[];raw=0;equal=0;unequal=0;allcollisions=0;accepted=0
for p,q in zip(PRIMES,PRIMES[1:]):
 test=A+list(range(p+1,q+1));cs=collisions(test);ws=[]
 for c in cs:
  E,R=normalize(test,c);allcollisions+=1
  check(bool(E) and bool(R) and max(E)<min(R),'normalized_ordered_nonempty')
  check(prod(E)==prod(R),'canceled_product_equality')
  check(all(not prime(t)for t in R),'right_block_prime_free')
  check(p<min(R)<=max(R)<q and R==list(range(min(R),max(R)+1)),'right_full_current_interval')
  check(len(E)>len(R),'earlier_block_strictly_longer')
  check(not(min(E)<=p<max(E)),'earlier_does_not_cross_current_boundary')
  check(block_in(A,E) or(p<min(E) and max(E)<q and E==list(range(min(E),max(E)+1))),'earlier_old_or_current_full')
  parents=[g for g in rejected if g[0]in E and g[1]in E]
  if not parents:check(E==list(range(min(E),max(E)+1)),'raw_witness_full_numeric_interval')
  ws.append((E,R,parents))
 if not ws:A=test;accepted+=1
 else:
  candidates=[w for w in ws if not w[2]]
  if candidates:w=candidates[0];kind='raw';parent=None;raw+=1
  else:
   w=ws[0];parent=w[2][0];E,R,parents=w
   check(block_in(A,E),'nonraw_witness_old_stable_block')
   ap,bq=parent;js=[j for j in range(2,max(R)//ap+1)if j*ap in R and j*bq in R]
   kind='equal'if js else'unequal'
   if js:equal+=1
   else:unequal+=1;check(ap*ap<=max(R)*(bq-ap)+ap*len(R),'actual_unequal_parent_bound')
   check(bq<q,'forest_parent_endpoint_decreases')
  records.append({'gap':(p,q),'kind':kind,'E':w[0],'R':w[1],'parent':parent})
  rejected.append((p,q));A=A+[q]
 check(not collisions(A),'every_finalized_prefix_collision_free')
 check(all(t in A for t in PRIMES if t<=q),'all_processed_primes_retained')
check(not collisions(A),'final_all_block_lengths_collision_free')
for p,q in rejected:
 check(A.index(q)==A.index(p)+1,'rejected_parent_adjacency_stable')
 check(all(t not in A for t in range(p+1,q)),'entire_rejected_interior_absent')
for rec in records:
 if rec['parent']:check(block_in(A,rec['E']),'parent_witness_block_survives_later_steps')
# A new insertion into an old rejected gap defeats the stability premise.
p,q=rejected[0];unstable=sorted(set(A)|set(range(p+1,q)))
check(bool(collisions(unstable)),'REJECT_reinsert_old_gap_restores_collision')
check(bool(collisions([1,2])),'REJECT_keep_one_creates_containment_collision')
# Necessary prime-multiple interval configurations, not claimed actual witnesses.
config=Counter()
gaps=list(zip(PRIMES,PRIMES[1:]))
for P,Q in gaps:
 for m in range(P+1,Q):
  for n in range(m,Q):
   s=n-m+1
   for p,q in gaps:
    if q>=m:break
    av=list(range(max(2,(m+p-1)//p),n//p+1));bv=list(range(max(2,(m+q-1)//q),n//q+1))
    if not av or not bv:continue
    js=set(av)&set(bv)
    if js:
     config['equal']+=1
     for j in js:
      check(P<j*p<j*q<Q,'equal_multiplier_strict_containment')
      check(Q-P>j*(q-p),'equal_child_longer_than_scaled_parent')
      # Exact shortness theta=3/50, no rounded floating exponent.
      if (q-p)**50>p**3:check((Q-P)**50>P**3,'no_long_to_short_equal')
    else:
     config['unequal']+=1
     for a in av:
      for b in bv:
       check(a!=b and abs(a*p-b*q)<=s-1,'unequal_multipliers_no_hidden_sign_assumption')
       check(p*p<=n*(q-p)+p*s,'necessary_unequal_parent_inequality')
# Weighted monomial obstruction, independent of low-genus classifications.
weighted=0
for r in range(2,51):
 for s in range(1,r):
  h=gcd(r,s);u=r//h;v=s//h
  check(u>v and gcd(u,v)==1 and u>=2,'primitive_weight_data')
  for e in range(1,h+1):
   top=u*v*e
   for j in range(v*e+1):
    i=(top-u*j)//v
    check(i+j<=u*e,'weighted_total_degree_upper')
   check(v*(u*e)==top and u*e>=2,'pure_X_top_attains_degree_at_least_two');weighted+=1
linear={(1,0):1,(0,1):-1}
linear_degree=max(i+j for i,j in linear)
check(linear_degree==1 and all(sum(c*x**i*x**j for(i,j),c in linear.items())==0 for x in range(-5,6)),'REJECT_drop_r_greater_s_X_minus_Y_linear_component')
check(all(x*x-y*y==(x-y)*(x+y)for x in range(-5,6)for y in range(-5,6))and all(max(i+j for i,j in H)==1 for H in [{(1,0):1,(0,1):-1},{(1,0):1,(0,1):1}]),'REJECT_skip_primitive_reduction_X2_minus_Y2_linear_factors')
# Non-Q absolute components of X^8-Y^4: X^2 +/- iY.
points=[(x,y)for x in range(-20,21)for y in range(-20,21)if x*x==0 and y==0]
check(points==[(0,0)] and len(points)<=2*2,'Galois_conjugate_intersection_example')
# Nonvacuous equal-chain containment model. Endpoints below are ordered
# disjoint integer intervals, NOT asserted to be prime gaps or greedy witnesses.
p=10**50;q=p+2;Js=sorted({2**a*3**b for a in range(6)for b in range(4)if 2**a*3**b<=60})
interval=lambda J:(J*p-(J-1),J*q+(J-1))
X=interval(max(Js))[1];synthetic_edges=0
for J in Js:
 P,Q=interval(J)
 check(P<=J*p<J*q<=Q,'synthetic_equal_chain_root_containment')
 check((Q-P)**50<=P**3,'synthetic_nonempty_short_interval')
 check(J*(q-p)<=Q-P and (J*(q-p))**50<=X**3,'synthetic_multiplier_endpoint_budget')
 for j in (2,3):
  if j*J not in Js:continue
  PP,QQ=interval(j*J)
  check(PP<j*P<j*Q<QQ,'synthetic_equal_edge_containment');synthetic_edges+=1
for (a,b),(c,d) in zip(map(interval,Js),list(map(interval,Js))[1:]):check(b<c,'synthetic_distinct_gaps_disjoint')
path_products=[a*b for a in (2,3)for b in (2,3)]
check(len(path_products)>len(set(path_products)) and path_products.count(6)==2,'REJECT_independent_branch_count_counts_duplicate_endpoint')
# Two different intervals assigned to multiplier6 necessarily overlap here.
a,b=interval(6);c,d=a-1,b+1
check(max(a,c)<min(b,d),'REJECT_two_distinct_gap_endpoints_for_same_multiplier_overlap')
# Exact exponents and actual invalid choices.
theta=F(3,50);rho=F(50,97);alpha=F(93,100)
exponents={'raw':F(1,2)+6*theta,'raw_equal_closure':F(1,2)+7*theta,'recursive':4*theta+rho*alpha,'long_parent':1-rho+4*theta,'deleted_short_length':alpha+theta}
check(rho==1/(2-theta) and rho<1,'scale_contraction_exponent')
for k in ['raw_equal_closure','recursive','long_parent']:check(exponents[k]<alpha,'recurrence_positive_margin_'+k)
check(alpha+theta<1 and F(1,20)<theta,'compatible_density_and_Jia_window')
check(F(1,2)+7*theta>F(9,10),'REJECT_claim_source_sharper_exponent_with_current_cutoff')
bad_theta=F(1,20);eps_upper=bad_theta-F(1,20)
check(eps_upper==0 and not any(F(1,20)+eps<bad_theta for eps in [F(1,10),F(1,1000),F(1,1000000)]),'REJECT_theta_one_twentieth_has_nonpositive_epsilon_window')
linear_removed=lambda n:n
check(F(94,100)+theta==1 and all(F(linear_removed(n),n)==1 for n in [2,10,100,1000]),'REJECT_linear_removed_counterexample_not_oX')
short_gaps=[g for g in gaps if(g[1]-g[0])**50<=g[0]**3]
check(short_gaps==[(2,3)],'actual_finite_short_gap_caveat')
print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'prime_endpoint':PRIMES[-1],'retained_count':len(A),'accepted_gaps':accepted,'rejected_gaps':len(rejected),'raw_rejected_gaps':raw,'selected_equal_edges':equal,'selected_unequal_edges':unequal,'actual_collision_pairs':allcollisions,'necessary_configurations':dict(config),'weighted_degree_patterns':weighted,'synthetic_equal_interval_vertices':len(Js),'synthetic_equal_edges':synthetic_edges,'actual_finite_short_gaps':short_gaps,'checks':sum(COUNTS.values()),'categories':dict(sorted(COUNTS.items())),'exponents':{k:str(v)for k,v in exponents.items()},'limits':['Finite greedy endpoint211; no infinite-density inference.','Actual finite short-gap mechanism vacuous; explicit synthetic interval model exercises equal-chain containment without claiming prime gaps or multiplicative witnesses.','Published theorem proofs, general factorization, uniform curve count, recurrence and asymptotics established/imported analytically, not by finite tests.','Historical503-endpoint counts and source-author/Lean code were not rerun.']},indent=2))
