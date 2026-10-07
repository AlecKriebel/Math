"""Exact rational/radical controls. No solver or third-party data required."""
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
import json
from pathlib import Path
P=[(9,9),(-3,0),(6,3),(7,-4),(2,10),(8,0)]
M=[[sum((a-b)**2 for a,b in zip(p,q)) for q in P] for p in P]
scale=10**6
lo=[[Q(isqrt(v*scale*scale),scale) for v in row] for row in M]
hi=[[Q(isqrt(v*scale*scale)+(isqrt(v*scale*scale)**2!=v*scale*scale),scale) for v in row] for row in M]
y=[Q(v,2) for v in [0,1,1,0,1,1]]
support=[(2,4),(1,2),(2,5),(2,5),(2,4),(2,5)]
x=[[Q(int(i in support[j]),2)for j in range(6)] for i in range(6)]
count=0
def check(b):
 global count
 if not b:
  raise AssertionError('certificate check failed')
 count+=1
check(sum(y)==2)
for i in range(6):
 for j in range(6):
  check(0<=x[i][j]<=y[i]<=1)
  check(lo[i][j]**2<=M[i][j]<=hi[i][j]**2)
for j in range(6):check(sum(x[i][j]for i in range(6))==1)
FL=sum(lo[i][j]*x[i][j]for i in range(6)for j in range(6))
FU=sum(hi[i][j]*x[i][j]for i in range(6)for j in range(6))
rows=[]
for S in combinations(range(6),2):
 # The square root is increasing, so nearest centers can be picked exactly.
 nearest=[min(S,key=lambda i:M[i][j])for j in range(6)]
 L=sum(lo[i][j]for j,i in enumerate(nearest)); U=sum(hi[i][j]for j,i in enumerate(nearest))
 check(L-FU>Q(29,50))
 rows.append(dict(centers=S,nearest=nearest,lower=str(L),upper=str(U)))
best=next(r for r in rows if r['centers']==(1,2))
for row in rows:
 if row is not best:check(Q(row['lower'])>Q(best['upper']))
check(Q(best['lower'])-FU>Q(29,50))
check(Q(29,50)-4*6*Q(1,100)==Q(17,50))
check(sum(x[i][j] for i in range(6) for j in range(6) if i!=j)==4)
check((Q(best['lower'])-FU)/10-Q(8,1000)>Q(1,20))
# Replicated configurations: each pair of facility labels, including same-site pairs.
replicated_pairs=0
for r in range(1,9):
 for a,b in combinations(range(6*r),2):
  S=(a//r,b//r)
  lower=r*sum(min(lo[i][j]for i in S)for j in range(6))
  check(lower-r*FU>Q(29*r,50))
  replicated_pairs+=1
 check(Q(29*r,50)-4*(6*r)*Q(1,100)==Q(17*r,50))
# Covariance of limiting pair distances: 1 on diagonal, 1/4 for shared endpoint.
# The representation (V_i+V_j-2 W_ij)/(2 sqrt(2)) gives variance 1,
# with independent Var(V_i)=2, Var(W_ij)=1.
pairs=list(combinations(range(6),2))
cov=[[Q(1)if a==b else Q(1,4)if set(a)&set(b)else Q(0)for b in pairs]for a in pairs]
# Exact LDL positive definiteness as an additional finite check.
N=len(cov); L=[[Q(int(i==j))for j in range(N)]for i in range(N)];D=[]
for i in range(N):
 D.append(cov[i][i]-sum(L[i][h]**2*D[h]for h in range(i)))
 check(D[i]>0)
 for j in range(i+1,N):L[j][i]=(cov[j][i]-sum(L[j][h]*L[i][h]*D[h]for h in range(i)))/D[i]
# Exact systematic rounding, all small opening vectors with denominator 4.
# Ball-coverage equality holds for every consecutive interval.
from itertools import product
roundings=0
for n in range(2,7):
 for weights in product(range(5),repeat=n):
  if sum(weights)%4 or not 0<sum(weights)//4<n:continue
  k=sum(weights)//4
  cumulative=[0]
  for w in weights:cumulative.append(cumulative[-1]+w)
  selections=[]
  for phase in [Q(1,2),Q(3,2),Q(5,2),Q(7,2)]:
   S=[i for i in range(n)if any(cumulative[i]<=phase+4*t<cumulative[i+1]for t in range(k))]
   check(len(S)==k);selections.append(S)
  for a in range(n):
   for b in range(a,n):
    hits=sum(any(a<=i<=b for i in S)for S in selections)
    check(Q(hits,4)==min(Q(1),Q(sum(weights[a:b+1]),4)))
  roundings+=1
report=dict(exact_assertions=count,points=P,squared_distance_matrix=M,fractional_support_by_client=support,y=list(map(str,y)),fractional_cost_interval=[str(FL),str(FU)],integer_optimum_interval=[best['lower'],best['upper']],certified_gap_lower=str(Q(best['lower'])-FU),center_pair_certificates=rows,systematic_rounding_vectors=roundings,replicated_center_pairs_checked=replicated_pairs,gaussian_limit_covariance_ldl=list(map(str,D)),limitations=['Fractional point is a feasible upper bound; no exact LP optimum claimed.','Finite controls supplement the written universal proofs.','No Monte Carlo probability estimate or joint n,d asymptotic theorem.'])
path=Path(__file__).with_name('verification.json');path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k in ['exact_assertions','fractional_cost_interval','integer_optimum_interval','certified_gap_lower','systematic_rounding_vectors']},indent=2))
