"""Fresh labelled-permutation checks, independent of submitted enumeration/checkers.

Full zeta probabilities are rational after cancelling pi^(2n). Cotangent-series
recursion extracts the true weights from sin/cos. Every labelled permutation is
individually traversed through n=8, before cycle-type aggregation. This checks
normalization and labelled ordered selections including repeated cycle sizes.
Finite identities only, not certification of geometric inputs/asymptotic limits.
"""
from fractions import Fraction as F
from itertools import permutations,product
from collections import Counter
from math import factorial,prod
import json

N=8;check_counts=Counter();c=[F(1)];a=[F(0)]
def check(v,name):
 assert v,name
 check_counts[name]+=1
for n in range(1,N+1):
 c.append(F((-1)**n,factorial(2*n))-sum((F((-1)**j,factorial(2*j+1))*c[n-j] for j in range(1,n+1)),F(0)))
 a.append(-c[n]/(4*n))
check(a[1]==F(1,12),'cotangent_true_weight')
check(a[2]==F(1,360),'cotangent_true_weight')
check(a[3]==F(1,5670),'cotangent_true_weight')
# Recurrence from direct differentiation of the exponential generating function.
h=[F(1)]
for n in range(1,N+1):h.append(sum((j*a[j]*h[n-j] for j in range(1,n+1)),F(0))/n)
rows=[]
for n in range(1,N+1):
 types=Counter()
 for p in permutations(range(n)):
  seen=set();lengths=[]
  for j in range(n):
   if j in seen:continue
   k=j;length=0
   while k not in seen:seen.add(k);length+=1;k=p[k]
   lengths.append(length)
  types[tuple(sorted(lengths))]+=1
 check(sum(types.values())==factorial(n),'all_labelled_permutations_traversed')
 def weight(t):return prod(j*a[j] for j in t)
 mass=sum((number*weight(t) for t,number in types.items()),F(0))
 check(mass/factorial(n)==h[n],'permutation_normalization_vs_differential_recurrence')
 for t,number in types.items():
  C=Counter(t)
  check(number==F(factorial(n),prod(j**m*factorial(m) for j,m in C.items())),'actual_cycle_type_enumeration')
 for r in [1,2,3]:
  for labels in product(range(1,n+1),repeat=r):
   needs=Counter(labels);total=sum(labels)
   actual=F(0)
   for t,number in types.items():
    C=Counter(t);choose=prod(prod(range(C[j]-m+1,C[j]+1)) if C[j]>=m else 0 for j,m in needs.items())
    actual+=number*weight(t)*choose/mass
   expect=prod(a[j] for j in labels)*h[n-total]/h[n] if total<=n else F(0)
   check(actual==expect,'ordered_cycle_factorial_moments_r1_to_r3')
 # A genuinely bivariate pgf identity for two disjoint sets of cycle sizes.
 even=set(range(2,n+1,2));odd=set(range(1,n+1,2));u=F(2,3);v=F(5,4)
 hp=[F(1)]
 for m in range(1,n+1):hp.append(sum((j*a[j]*(u if j in even else v)*hp[m-j] for j in range(1,m+1)),F(0))/m)
 direct=sum((number*weight(t)*u**sum(j in even for j in t)*v**sum(j in odd for j in t) for t,number in types.items()),F(0))/mass
 check(direct==hp[n]/h[n],'disjoint_window_bivariate_pgf')
 rows.append({'n':n,'labelled_permutations':factorial(n),'cycle_types':len(types)})
print(json.dumps({'status':'PASS','families':dict(sorted(check_counts.items())),'total_exact_assertions':sum(check_counts.values()),'labelled_permutations_traversed':sum(r['labelled_permutations'] for r in rows),'rows':rows,'limits':'Finite exact structural controls only; neither geometric nor asymptotic certification.'},indent=2,sort_keys=True))
