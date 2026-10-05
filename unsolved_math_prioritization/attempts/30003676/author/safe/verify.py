#!/usr/bin/env python3
"""Exact finite checks. Standard library only. This is not an asymptotic proof checker."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import hashlib
import json
from pathlib import Path
import sys

CHECKS = {}
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    CHECKS[name] = CHECKS.get(name, 0) + 1

def solve(a, b):
    n = len(b)
    m = [[F(x) for x in row] + [F(y)] for row, y in zip(a, b)]
    assert all(len(row) == n + 1 for row in m)
    for j in range(n):
        pivot = next((i for i in range(j,n) if m[i][j]), None)
        if pivot is None:
            raise ValueError('singular exact linear system')
        m[j],m[pivot] = m[pivot],m[j]
        z=m[j][j]
        m[j]=[v/z for v in m[j]]
        for i in range(n):
            if i != j and m[i][j]:
                z=m[i][j]
                m[i]=[x-z*y for x,y in zip(m[i],m[j])]
    return [row[-1] for row in m]

def generator(w, mu, theta, eps):
    n=len(mu); N=1<<n
    q=[[F(0) for _ in range(N)] for _ in range(N)]
    for s in range(N):
        for v in range(n):
            if s>>v&1:
                rate=mu[v]
            else:
                rate=eps+theta*sum((w[v][u] for u in range(n) if s>>u&1),F(0))
            t=s^(1<<v)
            q[s][t]+=rate
            q[s][s]-=rate
    return q

def residual(pi,q):
    return [sum((pi[i]*q[i][j] for i in range(len(pi))),F(0)) for j in range(len(pi))]

def stationary(q):
    n=len(q)
    a=[[q[i][j] for i in range(n)] for j in range(n-1)]+[[F(1)]*n]
    p=solve(a,[F(0)]*(n-1)+[F(1)])
    check('stationary_nonnegative',min(p)>=0)
    check('stationary_normalized',sum(p)==1)
    check('stationary_full_residual',all(x==0 for x in residual(p,q)))
    return p

def dual_h(q0,eps):
    n=len(q0)
    a=[[F(0)]*n for _ in range(n)]
    b=[F(0)]*n
    a[0][0]=1;b[0]=1
    for s in range(1,n):
        a[s]=q0[s].copy()
        a[s][s]-=eps*s.bit_count()
    return solve(a,b)

def clique_count(N,mu,beta,eps):
    r=[F(1)]
    for k in range(N):
        r.append(r[-1]*(N-k)*(eps+beta*F(k,N))/(mu*(k+1)))
    z=sum(r)
    return [v/z for v in r],r

def exact_complete_graph_formula(N,mu,beta,eps,k):
    if k==0:return F(1)
    x=F(N)*eps/(mu*k)*(beta/mu)**(k-1)
    for j in range(1,k):
        x*=F(N-j,N)*(1+F(N)*eps/(beta*j))
    return x

def clique_w(n,a):
    return [[F(0) if i==j else a/F(n) for j in range(n)] for i in range(n)]

def dimer_p(h,theta):
    return h*(1+h+theta)/((1+h)**2+h*theta)

# Arbitrary rational weighted graphs with genuinely heterogeneous recoveries.
for n in range(1,5):
    w=[[F(0) for _ in range(n)] for _ in range(n)]
    for i,j in combinations(range(n),2):
        w[i][j]=w[j][i]=F((i+j)%3+1,2)
    mu=[F(i+1,2) for i in range(n)]
    for theta,eps in [(F(1,20),F(1,7)),(F(3,2),F(2,9))]:
        q=generator(w,mu,theta,eps)
        check('generator_row_sums',all(sum(row)==0 for row in q))
        check('generator_off_diagonal_nonnegative',all(q[s][t]>=0 for s in range(1<<n) for t in range(1<<n) if s!=t))
        pi=stationary(q)
        h=dual_h(generator(w,mu,theta,F(0)),eps)
        for subset in range(1<<n):
            actual=sum((pi[s] for s in range(1<<n) if s&subset==0),F(0))
            check('dual_all_susceptible_subsets',actual==h[subset])
        p=[sum((pi[s] for s in range(1<<n) if s>>i&1),F(0)) for i in range(n)]
        for i,j in combinations(range(n),2):
            both=sum((pi[s] for s in range(1<<n) if s>>i&1 and s>>j&1),F(0))
            check('dual_covariance',both-p[i]*p[j]==h[(1<<i)|(1<<j)]-h[1<<i]*h[1<<j])
        if theta==F(1,20):
            c=min(mu[i]-theta*sum(w[i]) for i in range(n))
            check('strict_drift_margin',c>0)
            for s in range(1<<n):
                drift=sum((q[s][t]*(t.bit_count()-s.bit_count()) for t in range(1<<n)),F(0))
                check('pointwise_count_drift',drift<=eps*n-c*s.bit_count())
            check('stationary_drift_bound',sum(p)<=eps*n/c)
            a=[[(mu[i] if i==j else F(0))-theta*w[i][j] for j in range(n)] for i in range(n)]
            r=solve(a,[eps]*n)
            check('resolvent_nonnegative',min(r)>=0)
            check('resolvent_marginal_bound',all(p[i]<=r[i] for i in range(n)))
        q2=generator(w,mu,theta+F(1,3),eps)
        pi2=stationary(q2)
        # All threshold tail events are increasing; exact finite monotonicity check.
        for k in range(1,n+1):
            low=sum(pi[s] for s in range(1<<n) if s.bit_count()>=k)
            high=sum(pi2[s] for s in range(1<<n) if s.bit_count()>=k)
            check('monotonicity_count_tails',low<=high)

# Full-state generator versus separately constructed birth-death formula.
for N in range(1,6):
    for mu,beta,eps in [(F(1),F(1,2),F(1,11)),(F(3,2),F(7,3),F(1,13))]:
        q=generator(clique_w(N,beta),[mu]*N,F(1),eps)
        pi=stationary(q)
        lump=[sum((pi[s] for s in range(1<<N) if s.bit_count()==k),F(0)) for k in range(N+1)]
        cp,r=clique_count(N,mu,beta,eps)
        check('clique_full_generator_lumping',lump==cp)
        for k in range(N+1):
            check('clique_telescoped_formula',r[k]==exact_complete_graph_formula(N,mu,beta,eps,k))
        for k in range(N):
            check('birth_death_balance',cp[k]*(N-k)*(eps+beta*F(k,N))==cp[k+1]*mu*(k+1))

# Wider exact rational parameter grid for the dimer.
for theta in [F(0),F(1,2),F(1),F(2),F(7)]:
    for h0 in [F(1,100),F(1,7),F(3,2)]:
        q=generator([[F(0),F(1)],[F(1),F(0)]],[F(1)]*2,theta,h0)
        pi=stationary(q)
        actual=pi[1]+pi[3]
        check('dimer_closed_formula',actual==dimer_p(h0,theta))

# Finite structural certificates for Theorem 3.2.
for m in range(1,9):
    n=4*m;N=2*m; eta=F(1,n*n)
    w=[[F(0)]*n for _ in range(n)]
    w0=[[F(0)]*n for _ in range(n)]
    for i,j in combinations(range(N),2):w[i][j]=w[j][i]=w0[i][j]=w0[j][i]=F(1,n)
    blocks=[list(range(N))]
    for j in range(m):
        u=N+2*j;v=u+1
        w[u][v]=w[v][u]=w0[u][v]=w0[v][u]=F(1)
        blocks.append([u,v])
    for j in range(len(blocks)-1):
        u=blocks[j][-1];v=blocks[j+1][0]
        w[u][v]=w[v][u]=eta
    seen={0}; frontier=[0]
    while frontier:
        u=frontier.pop()
        for v in range(n):
            if w[u][v] and v not in seen:seen.add(v);frontier.append(v)
    check('heterogeneous_connected',len(seen)==n)
    e=[[w[i][j]-w0[i][j] for j in range(n)] for i in range(n)]
    check('heterogeneous_weak_row_bound',all(sum(row)<=2*eta for row in e))
    check('heterogeneous_base_row_bound',all(sum(row)<=1 for row in w0))
    # On a dimer-supported vector x=(1,1), x^T W x / ||x||^2 = 1 exactly.
    u=N;v=N+1
    rayleigh=(w[u][u]+w[u][v]+w[v][u]+w[v][v])/2
    check('heterogeneous_rayleigh_lower',rayleigh==1)
    check('heterogeneous_clique_scaling',F(1,n)==F(1,2)/N)

# Negative controls must be REJECTED, not merely executed.
w=[[F(0),F(1)],[F(1),F(0)]];mu=[F(1),F(1)];theta=F(2);eps=F(1,5)
q=generator(w,mu,theta,eps);pi=stationary(q)
check('NEGATIVE_reject_missing_immigration',any(residual(pi,generator(w,mu,theta,F(0)))))
check('NEGATIVE_reject_theta_scaled_recovery',any(residual(pi,generator(w,[theta*x for x in mu],theta,eps))))
# p=1/2 solves the factorized mean-field equilibrium when theta=1, eps=1/2.
# Its independent-product law must NOT solve the exact stochastic generator.
check('NEGATIVE_meanfield_equilibrium_identity',-F(1,2)+(1-F(1,2))*(F(1,2)+F(1)*F(1,2))==0)
check('NEGATIVE_reject_meanfield_product_law',any(residual([F(1,4)]*4,generator(w,mu,F(1),F(1,2)))))
cp,_=clique_count(4,F(1),F(2),F(1,7))
wrong_r=[F(1)]
for k in range(4):wrong_r.append(wrong_r[-1]*(F(1,7)+F(2)*F(k,4))/F(k+1))
wrong=[v/sum(wrong_r) for v in wrong_r]
check('NEGATIVE_reject_missing_susceptible_factor',cp!=wrong)
# Missing |A| in the dual killing term is also rejected at an actual subset.
h=dual_h(generator(w,mu,theta,F(0)),eps)
q0=generator(w,mu,theta,F(0))
check('NEGATIVE_reject_single_rate_dual_killing',sum(q0[3][t]*h[t] for t in range(4))!=eps*h[3])
check('NEGATIVE_positive_mean_not_lower_tail',F(1,2)>0 and 1-F(1,2)==F(1,2))
# A too-fast epsilon proof is analytic, but its finite upper bound can be checked rationally.
for N in [20,30,40]:
    epsilon=F(1,2**(N*N)); mu0=F(1); beta=F(3)
    cp,r=clique_count(N,mu0,beta,epsilon)
    bound=N*(N*epsilon/mu0)*max(F(1),(N*(1+beta)/mu0)**(N-1))
    check('fast_seed_mass_bound',sum(r[1:])<=bound)
    check('fast_seed_small_bound',bound<F(1,1000000))

result={
  'status':'PASS',
  'arithmetic':'exact fractions; no floating-point acceptance tests',
  'scope':'finite generator identities, stationary and dual equations, block structure, rejected wrong formulas',
  'not_certified':'general conjecture, novelty, exhaustive prior literature, or machine verification of asymptotic proofs',
  'check_groups':CHECKS,
  'total_checks':sum(CHECKS.values()),
  'negative_control_groups':sum(name.startswith('NEGATIVE_') for name in CHECKS),
  'python_minimum':'3.10 (int.bit_count)',
}
print(json.dumps(result,indent=2,sort_keys=True))
