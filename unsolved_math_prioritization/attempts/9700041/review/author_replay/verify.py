#!/usr/bin/env python3
"""Bounded exact controls for the torus metric and fast-leaf completion examples."""
from fractions import Fraction as F
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json
C=Counter()
def ck(p,k):
 assert p,k
 C[k]+=1
for n,beta in [(3,-1),(4,0),(6,1)]:
 def add(x,y):return (x[0]+y[0],x[1]+y[1])
 def mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]+beta*x[1]*y[1])
 def scale(c,x):return (c*x[0],c*x[1])
 roots=[(F(1),F(0))]
 for _ in range(n):roots.append(mul(roots[-1],(F(0),F(1))))
 ck(roots[-1]==roots[0],'cyclotomic_period')
 eig=[]
 for k in range(n):
  lam=scale(n*n,add((F(2),F(0)),scale(-1,add(roots[k],roots[-k%n]))))
  ck(lam[1]==0 and lam[0]>=0 and lam[0].denominator==1,'integer_cycle_eigenvalue')
  eig.append(int(lam[0]))
  for j in range(n):
   lhs=scale(n*n,add(add(roots[(k*(j+1))%n],roots[(k*(j-1))%n]),scale(-2,roots[(k*j)%n])))
   ck(lhs==scale(-lam[0],roots[(k*j)%n]),'cycle_Fourier_eigenvector')
 ck(eig.count(0)==1,'irreducible_cycle_zero_mode')
 rows={}
 for s in [1,2]:
  vals=[]
  for d in range(n):
   z=(F(0),F(0))
   for k in range(n):z=add(z,scale(F(1,n*2**(s*eig[k])),roots[(k*d)%n]))
   ck(z[1]==0 and z[0]>0,'exact_transition_probability')
   vals.append(z[0])
  ck(sum(vals)==1,'transition_row_mass')
  rows[s]=vals
 for d in range(n):ck(sum(rows[1][j]*rows[1][(d-j)%n] for j in range(n))==rows[2][d],'Chapman_Kolmogorov')
 # Fourier-resolvent squared row distance on the two-dimensional grid.
 d2={}
 for dx,dy in product(range(n),repeat=2):
  z=(F(0),F(0))
  for k,l in product(range(n),repeat=2):
   phase=roots[(k*dx+l*dy)%n]
   real=scale(F(1,2),add(phase,roots[(-k*dx-l*dy)%n]))
   z=add(z,scale(F(2,1+2*(eig[k]+eig[l])),add((F(1),F(0)),scale(-1,real))))
  ck(z[1]==0 and z[0]>=0,'two_dimensional_resolvent_metric_nonnegative')
  ck((z[0]==0)==(dx==dy==0),'finite_metric_separates_points')
  d2[dx,dy]=z[0]
 for u,v in product(d2,repeat=2):
  inner=(d2[u]+d2[v]-d2[(u[0]-v[0])%n,(u[1]-v[1])%n])/2
  ck(d2[u]*d2[v]>=inner*inner,'Hilbert_distance_Cauchy_Schwarz')
 # Exact stationary increment/trace identity for the finite one-dimensional case.
 d1=[]
 for d in range(n):
  val=F(0)
  for k in range(n):
   real=scale(F(1,2),add(roots[(k*d)%n],roots[(-k*d)%n]))[0]
   val+=F(2,1+2*eig[k])*(1-real)
  d1.append(val)
 left=sum(rows[1][d]*d1[d] for d in range(n))
 right=sum(F(2,1+2*lam)*(1-F(1,2**lam)) for lam in eig)
 ck(left==right,'stationary_increment_trace_identity')
# Dyadic odd harmonic blocks give a uniform positive divergence contribution.
for j in range(1,11):
 odds=range(2**j+1,2**(j+1),2)
 harmonic=sum((F(1,m) for m in odds),F(0))
 ck(harmonic>=F(1,4),'odd_harmonic_block_lower_bound')
 for m in odds:ck(F(4*(2*m+1),1+160*m*m)>=F(8,161*m),'torus_divergence_term_lower_bound')
# Truncated star chains preserve reversibility and a uniformly bounded perturbation.
for m in range(1,13):
 pi=[(1-sum(F(1,16**j) for j in range(1,m+1)))/2]*2+[F(1,16**j) for j in range(1,m+1)]
 n=m+2;Q=[[F(0) for _ in range(n)] for _ in range(n)]
 Q[0][1]=Q[1][0]=1
 for j in range(1,m+1):
  idx=j+1
  Q[idx][0]=Q[idx][1]=F(2**j,2)
  Q[0][idx]=Q[1][idx]=pi[idx]*Q[idx][0]/pi[0]
 for i in range(n):Q[i][i]=-sum(Q[i])
 ck(sum(pi)==1 and pi[0]>=F(7,15),'star_probability_mass')
 for i,j in product(range(n),repeat=2):ck(pi[i]*Q[i][j]==pi[j]*Q[j][i],'star_detailed_balance')
 for row in Q:ck(sum(row)==0,'star_generator_row_sum')
 f=[F(1),F(-1)]+[F(0)]*m
 lam=2+sum(Q[0][2:])
 for i in range(n):ck(sum(Q[i][j]*f[j] for j in range(n))==-lam*f[i],'hub_antisymmetric_eigenfunction')
 b2=sum(pi[j+1]*F(2**j,2)**2/pi[0] for j in range(1,m+1))
 ck(b2<=F(5,28),'uniform_squared_coupling_norm')
 for phase in range(4):
  f=[F(((i+phase)%5)-2) for i in range(n)]
  energy=-sum(pi[i]*f[i]*sum(Q[i][j]*f[j] for j in range(n)) for i in range(n))
  edges=sum(pi[i]*Q[i][j]*(f[i]-f[j])**2 for i in range(n) for j in range(i+1,n))
  ck(energy==edges>=0,'nonnegative_Dirichlet_form')
ck(F(1,15)+2*F(7,15)==1,'infinite_star_mass_identity')
ck(F(15,14)*F(1,7)==F(15,98),'infinite_hub_leaf_rate')
ck(2+F(15,98)==F(211,98) and 3+F(15,98)==F(309,98),'hub_eigenvalues_before_and_after_reset')
for n in range(1,41):
 r=2**n;pi=F(1,16**n)
 ck(F(24,1)/(pi*(2*r)**5)==F(3,4*r),'weighted_leaf_spike_integral')
ck(F(2)*F(5,28)<1,'finite_rank_perturbation_bound')
here=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(sorted(C.items())),
 'artifact_sha256':hashlib.sha256((here/'PARTIAL.md').read_bytes()).hexdigest(),
 'scope':'Finite exact Fourier/semigroup/resolvent and reversible-generator controls; global convergence, completion and entrance-state claims use the written analytic proofs.'}
(here/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
