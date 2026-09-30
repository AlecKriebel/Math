#!/usr/bin/env python3
"""Independent exact finite diagnostics; no general-topology certificate."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import itertools
import json
import hashlib
import sympy as S

checks={}
def ck(name,value):
    assert bool(value),name
    checks[name]=checks.get(name,0)+1

# A different finite model: complete-graph heat kernels at t=log(2).
for n in range(2,10):
    z=F(1,2**n)
    P=[[F(1,n)+z*(int(i==j)-F(1,n)) for j in range(n)] for i in range(n)]
    G=[[F(1)+(n*int(i==j)-1)*F(1,1+2*n) for j in range(n)] for i in range(n)]
    dist=[[G[i][i]+G[j][j]-2*G[i][j] for j in range(n)] for i in range(n)]
    for i in range(n):
        ck("complete_kernel_mass",sum(P[i])==1 and all(x>0 for x in P[i]))
        for j in range(n):
            ck("complete_density_semigroup",
               sum(P[i][k]*P[k][j] for k in range(n))==
               F(1,n)+z*z*(int(i==j)-F(1,n)))
            ck("complete_Hilbert_metric",
               dist[i][j]==(F(0) if i==j else F(2*n,1+2*n)))
    left=sum(F(1,n)*P[i][j]*dist[i][j] for i in range(n) for j in range(n))
    right=F(2*(n-1),1+2*n)*(1-z)
    ck("stationary_trace_increment",left==right)

# Odd dyadic Fourier blocks: each contributes a fixed positive harmonic amount.
for j in range(1,11):
    m0=2**j
    odds=list(range(m0+1,2*m0,2))
    ck("odd_block_cardinality",len(odds)==m0//2)
    ck("odd_block_harmonic_lower",sum((F(1,m) for m in odds),F(0))>=F(1,4))

# Independently aggregate the infinite tail into one state, retaining the EXACT
# infinite hub masses, total hub exit rate, and antisymmetric eigenvalue.
for m in range(1,7):
    mass=[F(7,15),F(7,15)]+[F(1,16**j) for j in range(1,m+1)]+[F(1,15*16**m)]
    rates=[F(2**j) for j in range(1,m+1)]+[F(15*2**m,7)]
    N=len(mass)
    Q=[[F(0) for j in range(N)] for i in range(N)]
    Q[0][1]=Q[1][0]=F(1)
    for k,r in enumerate(rates,2):
        Q[k][0]=Q[k][1]=r/2
        Q[0][k]=Q[1][k]=mass[k]*r/(2*mass[0])
    for i in range(N):Q[i][i]=-sum(Q[i])
    ck("tail_aggregate_mass",sum(mass)==1)
    ck("exact_hub_rate", -Q[0][0]==F(113,98))
    for i,j in itertools.product(range(N),repeat=2):
        ck("tail_aggregate_reversibility",mass[i]*Q[i][j]==mass[j]*Q[j][i])
    f=[F(1),F(-1)]+[F(0)]*(N-2)
    for i in range(N):
        ck("exact_hub_eigenvalue",sum(Q[i][j]*f[j] for j in range(N))==-F(211,98)*f[i])
        reset=sum((Q[i][j]+mass[j]-int(i==j))*f[j] for j in range(N))
        ck("exact_reset_eigenvalue",reset==-F(309,98)*f[i])
    coupling2=sum(mass[k]*rates[k-2]**2/(4*mass[0]) for k in range(2,N))
    ck("coupling_squared_norm_bound",coupling2<=F(5,28))
    # On the symmetric hub/leaf subspace the extreme bounded-perturbation
    # eigenvalue has modulus (1+sqrt(1+8*coupling2))/2 < 2.
    ck("bounded_perturbation_below_two",1+8*coupling2<9)
    variables=S.symbols("x:"+str(N))
    energy=-sum(S.Rational(mass[i].numerator,mass[i].denominator)*variables[i]*
                sum(S.Rational(Q[i][j].numerator,Q[i][j].denominator)*variables[j]
                    for j in range(N)) for i in range(N))
    edges=sum(S.Rational((mass[i]*Q[i][j]).numerator,(mass[i]*Q[i][j]).denominator)*
              (variables[i]-variables[j])**2 for i in range(N) for j in range(i+1,N))
    ck("symbolic_Dirichlet_identity",S.expand(energy-edges)==0)

# Exact spike integrals, including the critical dimension comparison.
for n in range(1,25):
    r=2**n
    spike=F(factorial(4)*r**4,(2*r)**5)
    ck("eight_dimensional_spike_decay",spike==F(3,4*r))
    critical=F(factorial(3)*r**4,(2*r)**4)
    ck("six_dimensional_critical_spike",critical==F(3,8))
    stronger=F(factorial(5)*r**4,(2*r)**6)
    ck("ten_dimensional_spike_decay",stronger==F(15,8*r*r))

# The midpoint is separated from either hub by half their Hilbert distance.
for D in (F(1,8),F(1),F(10)):
    huba,mid,hubb=F(0),D/2,D
    witness=lambda x:min(F(1),2*abs(x-mid)/D)
    ck("midpoint_continuous_witness",
       witness(mid)==0 and witness(huba)==witness(hubb)==1)
    ck("midpoint_mixture_limit",(witness(huba)+witness(hubb))/2==1)

root=Path(__file__).resolve().parent
result={"status":"PASS","exact_assertions":sum(checks.values()),"checks":checks,
 "artifact_sha256":hashlib.sha256((root/"author_replay/PARTIAL.md").read_bytes()).hexdigest(),
 "scope":"Independent complete-graph spectral/trace identities, exact tail-aggregated "
         "reversible generators, symbolic energies, spike integrals and midpoint controls. "
         "Infinite-dimensional and source-scope arguments are in REVIEW.md."}
(root/"independent_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
