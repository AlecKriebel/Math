"""New adversarial mechanisms: true GF(4), exhaustive square-order boundary,
three-line dependence and biased point retention. No candidate/family code imports.
"""
from array import array
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from itertools import product, combinations
from math import comb
from pathlib import Path
import json
checks=Counter()
def require(x,k):
 checks[k]+=1
 if not x:raise AssertionError(k)
def multiply(a,b):
 raw=0
 for i in range(2):
  if b>>i&1:raw^=a<<i
 if raw&4:raw^=7
 return raw
def inverse(a):
 if not a:raise ZeroDivisionError
 return multiply(a,a)
def normalized(v):
 z=next(x for x in v if x)
 return tuple(multiply(x,inverse(z)) for x in v)
q=4
for a,b,c in product(range(4),repeat=3):
 require(multiply(a,b)==multiply(b,a),'field_axioms')
 require(multiply(a,b^c)==multiply(a,b)^multiply(a,c),'field_axioms')
 require(multiply(multiply(a,b),c)==multiply(a,multiply(b,c)),'field_axioms')
for a in range(1,4):require(multiply(a,inverse(a))==1,'field_inverse')
points=sorted({normalized(v) for v in product(range(4),repeat=3) if any(v)})
lines=[]
for a in points:
 mask=0
 for i,v in enumerate(points):
  dot=0
  for x,y in zip(a,v):dot^=multiply(x,y)
  if dot==0:mask|=1<<i
 lines.append(mask)
n=len(points);limit=1<<n;universe=limit-1
require(n==len(lines)==21 and len(set(lines))==21,'plane_counts')
for L in lines:require(L.bit_count()==5,'line_lengths')
for L,M in combinations(lines,2):require((L&M).bit_count()==1,'line_meets')
pointcovers=[sum(1<<j for j,L in enumerate(lines) if L>>i&1) for i in range(n)]
for x in pointcovers:require(x.bit_count()==5,'point_degrees')
for i,j in combinations(range(n),2):require((pointcovers[i]&pointcovers[j]).bit_count()==1,'point_joins')
# GF(2) inside GF(4) gives a tight, genuinely square-order Baer boundary.
baer=sum(1<<i for i,v in enumerate(points) if all(x in (0,1) for x in v))
require(baer.bit_count()==7,'baer_size')
intersection_hist=Counter((baer&L).bit_count() for L in lines)
require(intersection_hist==Counter({1:14,3:7}),'baer_line_sections')
for i in range(n):
 if baer>>i&1:
  tangent_count=sum((baer&L)==1<<i for L in lines)
  require(tangent_count==2,'baer_tangent_minimality')
  require(not all((baer^(1<<i))&L for L in lines),'baer_deletion_negative_control')
require(all(baer&L for L in lines) and not any(baer&L==L for L in lines),'baer_nontrivial_blocker')
a=baer.bit_count()-q-1
require(a*a==q,'square_order_bruen_equality')
# Coverage recurrence optimizes ALL nonempty sections in every actual PG(2,4) R.
# A proper feasible subset can be reached by deleting a point while retaining
# the same covered lines; this is a complete recurrence, including empty R.
hit=array('I',[0])*limit
tau=array('B',[0])*limit
ordinary_by_size=Counter(); minimal_by_size=Counter(); tau_hist=Counter({0:1})
nontrivial=0;good_lower_failures=0;empty_count=0;full_count=0
for R in range(1,limit):
 low=R&-R;hit[R]=hit[R^low]|pointcovers[low.bit_length()-1]
 best=R.bit_count();bits=R
 while bits:
  bit=bits&-bits;smaller=R^bit
  if hit[smaller]==hit[R]:best=min(best,tau[smaller])
  bits^=bit
 tau[R]=best;tau_hist[best]+=1
 if hit[R]==universe:
  ordinary_by_size[R.bit_count()]+=1
  if best==R.bit_count():minimal_by_size[R.bit_count()]+=1
  if hit[universe^R]==universe:
   nontrivial+=1
   if best<7:good_lower_failures+=1
 else:empty_count+=1
# R=0 was omitted from the loop.
empty_count+=1
for R in range(limit):
 full_line=(hit[universe^R]!=universe)
 if full_line:full_count+=1
 require(not(full_line and hit[R]!=universe),'empty_full_global_disjointness')
require(sum(tau_hist.values())==limit,'all_subset_census')
require(empty_count==full_count,'complement_exception_symmetry')
require(empty_count<=n*(1<<(n-q-1)),'exceptional_union_bound')
require(good_lower_failures==0,'all_q4_good_event_integer_bound')
require(tau[baer]==7,'baer_transversal_optimum')
require(tau[0]==0,'empty_tau')
for L in lines:
 require(tau[L]==5,'whole_line_lower_bound_countercontrol')
 for i in range(n):
  if L>>i&1:require(tau[L^(1<<i)]==4,'line_subset_countercontrol')
# Triple-empty events distinguish concurrence from a projective triangle.
# Monochromatic-line indicators are pairwise independent at p=1/2 but are
# NOT jointly independent on triangle triples.
triple_types=Counter();ratios=Counter()
for L,M,N in combinations(lines,3):
 common=L&M&N;union=L|M|N;concurrent=bool(common)
 require(union.bit_count()==(3*q+1 if concurrent else 3*q),'three_line_union_geometry')
 triple_types['concurrent' if concurrent else 'triangle']+=1
 marginal=Fraction(1,2**(q+1));joint=Fraction(1,2**union.bit_count())
 ratio=joint/marginal**3
 require(ratio==(4 if concurrent else 8),'triple_empty_dependence')
 mono=2*joint;mono_marginal=2*marginal
 require(mono/mono_marginal**3==(1 if concurrent else 2),'pairwise_vs_joint_monochromatic_negative_control')
 ratios[str(ratio)]+=1
require(triple_types==Counter({'concurrent':210,'triangle':1120}),'triple_type_census')
# Biasing point retention is a control of assumption dependence, not a
# proposed change to the original half-point conjecture.
bias_rows=[]
for p in [Fraction(1,3),Fraction(2,5),Fraction(1,2),Fraction(4,5)]:
 empty=(1-p)**(q+1);full=p**(q+1)
 joint_empty=(1-p)**(2*q+1);joint_full=p**(2*q+1)
 require(joint_empty/empty**2==1/(1-p),'biased_empty_correlation')
 require(joint_full/full**2==1/p,'biased_full_correlation')
 # Exact size census is a sufficient statistic under iid biased retention.
 empty_by_size={k:comb(n,k)-ordinary_by_size[k] for k in range(n+1)}
 weighted_empty=sum((empty_by_size[k]*p**k*(1-p)**(n-k) for k in range(n+1)),Fraction())
 weighted_full=sum((empty_by_size[n-k]*p**k*(1-p)**(n-k) for k in range(n+1)),Fraction())
 require(weighted_empty<=n*empty and weighted_full<=n*full,'biased_exception_union_bounds')
 require((weighted_empty==weighted_full)==(p==Fraction(1,2)),'half_retention_symmetry_assumption')
 bias_rows.append({'point_retention':str(p),'exact_empty_event':str(weighted_empty),'exact_full_event':str(weighted_full),'empty_joint_over_product':str(joint_empty/empty**2),'full_joint_over_product':str(joint_full/full**2)})
# Shortening full lines destroys the blocker-complement encoding.
for L in lines:
 complement=universe^L
 for t in (2,3,4):
  short_edges=sum(comb((M&complement).bit_count(),t) for M in lines)
  require(short_edges==(n-1)*comb(q,t)>0,'short_edge_encoding_countercontrol')
# Actual repaired sets for the equality blocker: every point is forced by
# a tangent section, so each repair outcome is exactly that seven-point B.
baer_indices=[i for i in range(n) if baer>>i&1]
rho=Fraction(2,5);average=Fraction();linear_upper=rho*7+sum((1-rho)**((baer&L).bit_count()) for L in lines)
for z in range(1<<7):
 T=sum(1<<baer_indices[i] for i in range(7) if z>>i&1);fixed=T;missed=0
 for L in lines:
  section=L&baer
  if not(section&T):fixed|=section&-section;missed+=1
 require(fixed==baer,'baer_actual_repair_forced_by_tangents')
 require(fixed.bit_count()<=T.bit_count()+missed,'baer_colliding_repair_upper')
 average+=rho**z.bit_count()*(1-rho)**(7-z.bit_count())*fixed.bit_count()
require(average==7 and average<=linear_upper,'baer_exact_repair_expectation')
# The baseline's special rho is rightly restricted to sufficiently large q.
# Here m=1 and log(5)>1, so literal finite-order use would be invalid.
require(min((L&baer).bit_count() for L in lines)==1,'small_order_rho_domain_countercontrol')
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','new_control_mechanisms':['actual GF(4) field and square-order Baer equality boundary','exhaustive nonempty-section tau recurrence on PG(2,4)','three-line concurrence versus triangle dependence','biased retention assumption controls','actual tangent-forced repairs and shortened-edge complement failure'],'all_retained_subsets':limit,'checks_by_mechanism':dict(checks),'checks_total':sum(checks.values()),'q4_ordinary_blocker_size_census':dict(sorted(ordinary_by_size.items())),'q4_minimal_blocker_size_census':dict(sorted(minimal_by_size.items())),'q4_tau_census':dict(sorted(tau_hist.items())),'q4_no_empty_no_full_good_sets':nontrivial,'q4_good_lower_bound_failures':good_lower_failures,'q4_empty_event_count':empty_count,'q4_full_event_count':full_count,'baer_points':[points[i] for i in baer_indices],'baer_line_intersection_census':dict(intersection_hist),'baer_exact_repair_expectation':str(average),'baer_linear_repair_bound':str(linear_upper),'three_line_types':dict(triple_types),'bias_controls':bias_rows,'scope':'Finite q=4 diagnostics, not an asymptotic proof or new central attempt.'}
(Path(__file__).parent/'FRESH_CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('bias_controls','baer_points')},indent=2))
