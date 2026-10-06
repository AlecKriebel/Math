from fractions import Fraction as F
from collections import Counter
from itertools import product
import json,sympy as sp
C=Counter()
def ck(x,label):
    assert x,label
    C[label]+=1
def pow2(n):return F(2**n) if n>=0 else F(1,2**(-n))
def h(n):return 1-pow2(-n-1) if n>=0 else pow2(n-1)
def a(n):return pow2(-abs(n))
def cumulative(n):
    return F(3,2)*pow2(-n)-F(1,2)*pow2(-2*n) if n>=0 else 3*pow2(n)-2*pow2(2*n)
def flux(n):return 2-cumulative(n)
def B(n):return flux(n)/(h(n+1)-h(n))
def mu(n):return 1+B(n-1)+B(n)+a(n)*(3-a(n))
def edge(n,m):return a(n)*a(m)+(B(min(n,m)) if abs(n-m)==1 else 0)
for n in range(-80,81):
    ck(0<h(n)<1,'positive_bounded_harmonic_density')
    ck(1<=flux(n)<2,'uniform_positive_nearest_current')
    ck(B(n)>0 and mu(n)>0,'finite_positive_local_mass')
    ck(cumulative(n)-cumulative(n-1)==3*a(n)*(F(1,2)-h(n)),'exact_infinite_rank_one_tail_formula')
    ck(B(n)*(h(n+1)-h(n))-B(n-1)*(h(n)-h(n-1))+3*a(n)*(F(1,2)-h(n))==0,'infinite_chain_harmonicity_with_exact_tails')
    ck(mu(n)==1+B(n-1)+B(n)+a(n)*(3-a(n)),'exact_Markov_row_sum')
    ck(mu(n)*h(n)==h(n)+B(n-1)*h(n-1)+B(n)*h(n+1)+a(n)*(F(3,2)-a(n)*h(n)),'infinite_sigmafinite_invariant_measure')
for n,m in product(range(-10,11),repeat=2):
    if n==m:continue
    ck(edge(n,m)>0 and edge(n,m)==edge(m,n),'strict_positive_symmetric_all_pair_conductance')
    ck(h(n)*edge(n,m)!=h(m)*edge(n,m),'nonreversible_invariant_flux')
# Count-only displacement-gated matching controls on finite cyclic groups.
patterns=0
for N in range(2,6):
 def sh(x,k):return x[k:]+x[:k]
 def dist(i,j):return min((i-j)%N,(j-i)%N)
 def U(i,j):return {k for k in range(N) if min(dist(k,i),dist(k,j))<=dist(i,j)}
 for eta in product(range(3),repeat=N):
  for d in range(1,N):
   tau=[]
   for s in range(N):
    ts=[t for t in range(N) if (t-s)%N in {d,(-d)%N} and t!=s and eta[s]==eta[t]==1 and sum(eta[u] for u in U(s,t))==2]
    ck(len(ts)<=1,'count_only_gated_partner_unique')
    tau.append(ts[0] if ts else s)
   ck(all(tau[tau[s]]==s for s in range(N)),'count_only_matching_involution')
   ck(all(sum(eta[s] for s in range(N) if tau[s]==t)==eta[t] for t in range(N)),'count_only_multiplicity_preservation')
 for seed in product(range(3),repeat=N):
  if not any(seed) or seed!=min(sh(seed,t) for t in range(N)):continue
  patterns+=1;states=sorted(set(sh(seed,t) for t in range(N)));idx={x:i for i,x in enumerate(states)};equations=[]
  mass=sum(x[0] for x in states);q=[F(x[0],mass) for x in states]
  for d in range(1,N):
   K=[[F(int(i==j)) for j in range(len(states))] for i in range(len(states))]
   for i,x in enumerate(states):
    for t in (d,(-d)%N):
     w=F(1,2)*x[t]*F(3,8)**sum(x[u] for u in U(0,t))
     K[i][idx[sh(x,t)]]+=w;K[i][i]-=w
   for row in K:ck(sum(row)==1 and min(row)>=0,'finite_rational_void_upper_surrogate_Markov')
   for j in range(len(states)):
    ck(sum(q[i]*K[i][j] for i in range(len(states)))==q[j],'Palm_weights_invariant_each_displacement_gate')
    equations.append([K[i][j]-int(i==j) for i in range(len(states))])
  mat=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in row] for row in equations])
  ck(mat.rank()==len(states)-1,'displacement_only_gates_force_Palm_finite_control')
print(json.dumps({'status':'PASS_CONTROLS_ONLY','counts':dict(sorted(C.items())),'assertions':sum(C.values()),'finite_orbit_patterns':patterns,'infinite_counterexample':'Infinite sums reduced to exact geometric-tail formulas; no truncation used in the checked stationary equations. One all-pair positive reversible chain, not ALL Cox tests.','finite_scope':'Finite matching controls and rational void upper surrogate 3/8; no claim that surrogate equals exp(-1).','theorem_scope':'Discrete sigma-finite proof remains analytic; full non-discrete repair unproved.'},sort_keys=True,indent=2))
