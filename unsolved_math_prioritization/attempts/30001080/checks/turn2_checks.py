"""Exact finite controls of isolated Cox pairs and joint-state period transports."""
from itertools import product
from fractions import Fraction as F
from collections import Counter
import json
import sympy as S
C=Counter()
def ck(b,k):assert b,k;C[k]+=1
def sh(v,t):return v[t:]+v[:t]
def dist(s,t,n):return min((s-t)%n,(t-s)%n)
def union(s,t,n):
 r=dist(s,t,n)
 return {u for u in range(n) if dist(u,s,n)<=r or dist(u,t,n)<=r}
def pair(eta,s,t):return s!=t and eta[s]==eta[t]==1 and sum(eta[i] for i in union(s,t,len(eta)))==2
def match(eta,mu,s):
 ts=[t for t in range(len(eta)) if pair(eta,s,t) and (mu[s]+mu[t])%2==1]
 ck(len(ts)<=1,'unique_partner')
 return ts[0] if ts else s
# All small integer counting measures, including multiple points and tied distances.
for n in range(1,6):
 mus=[tuple([1]*n),tuple((i%3) for i in range(n)),tuple((i*i+1)%3 for i in range(n))]
 for eta in product(range(3),repeat=n):
  for mu in mus:
   tau=[match(eta,mu,s) for s in range(n)]
   for s in range(n):ck(tau[tau[s]]==s,'matching_involution')
   ck([sum(eta[s] for s in range(n) if tau[s]==t) for t in range(n)]==list(eta),'counting_mass_preserved')
   for k in range(n):
    for s in range(n):ck(match(sh(eta,k),sh(mu,k),s)==(tau[(s+k)%n]-k)%n,'matching_covariance')
  for s in range(n):
   for t in range(n):
    if s==t:continue
    inserted=list(eta);inserted[s]+=1;inserted[t]+=1
    ck(pair(inserted,s,t)==all(eta[i]==0 for i in union(s,t,n)),'two_insertions_iff_void_including_atoms')
# Polynomial-in-q density identities: q=e^(-1), integer intensities.
for n in range(2,6):
 for mu in product(range(3),repeat=n):
  if not any(mu) or mu!=min(sh(mu,t) for t in range(n)):continue
  for gate_kind in (0,1):
   jump=[[{} for _ in range(n)] for _ in range(n)]
   for s in range(n):
    for t in range(n):
     if s!=t and (gate_kind==0 or (mu[s]+mu[t])%2==1):
      exponent=sum(mu[i] for i in union(s,t,n));jump[s][t]={exponent:mu[t]}
    rate=sum(F(mu[t])*F(3,8)**sum(mu[i] for i in union(s,t,n)) for t in range(n) if s!=t and (gate_kind==0 or (mu[s]+mu[t])%2==1))
    ck(rate<=1,'exact_row_upper_bound_q_le_3_over_8')
   for t in range(n):
    coefficients=Counter()
    for s in range(n):
     for e,v in jump[s][t].items():coefficients[e]+=mu[s]*v
     for e,v in jump[t][s].items():coefficients[e]-=mu[t]*v
    ck(all(v==0 for v in coefficients.values()),'Cox_spatial_balance_polynomial')
ck(F(1)+1+F(1,2)+F(1,6)+F(1,24)>F(8,3),'exp_one_gt_8_over_3')
# Hidden auxiliary state: n distinct marked rotations even when the measure is periodic.
patterns=0
for n in range(1,6):
 for mu in product(range(3),repeat=n):
  if not any(mu) or mu!=min(sh(mu,t) for t in range(n)):continue
  patterns+=1;mass=sum(mu);states=sorted(set(sh(mu,t) for t in range(n)))
  remaining={(v,t) for v in states for t in range(n)};gates=[]
  while remaining:
   v,t=min(remaining);gate={(v,t),(sh(v,t),(-t)%n)};remaining-=gate;gates.append(gate)
  matrices=[]
  for gate in gates:
   K=[[F(int(i==j)) for j in range(n)] for i in range(n)]
   for i in range(n):
    v=sh(mu,i)
    for t in range(n):
     w=F(v[t],(1+mass)**2)*int((v,t) in gate)
     K[i][(i+t)%n]+=w;K[i][i]-=w
   matrices.append(K)
  H=[t for t in range(n) if sh(mu,t)==mu]
  for t in H:
   K=[[F(0) for _ in range(n)] for _ in range(n)]
   for i in range(n):K[i][(i+t)%n if mu[i]>0 else i]=1
   matrices.append(K)
   for j in range(n):ck(sum(mu[i]*K[i][j] for i in range(n))==mu[j],'period_kernel_mass_preservation')
  q=[F(v,mass) for v in mu];equations=[]
  for K in matrices:
   for row in K:ck(sum(row)==1 and min(row)>=0,'joint_Markov_rows')
   for j in range(n):
    ck(sum(q[i]*K[i][j] for i in range(n))==q[j],'joint_Palm_invariance')
    equations.append([K[i][j]-int(i==j) for i in range(n)])
  A=S.Matrix([[S.Rational(v.numerator,v.denominator) for v in row] for row in equations])
  ck(A.rank()==n-1,'measure_only_tests_determine_full_marked_Palm_law')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'marked_orbit_patterns':patterns,'scope':'Finite exact controls only. Infinite measure identities, Poisson formula and source coverage are established in the written proofs and require independent review.'},sort_keys=True,indent=2))
