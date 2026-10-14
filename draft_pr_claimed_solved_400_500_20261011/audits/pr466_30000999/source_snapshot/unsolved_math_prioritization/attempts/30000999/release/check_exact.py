#!/usr/bin/env python3
"""Finite exact transcription/algebra controls; not a substitute for the proof.

Python standard library only. No network, randomized checks, or numerical OT.
"""
from fractions import Fraction as F
from math import comb, factorial, prod
import json

counts = {}
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1

def cmul(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])

def cpow(z, k):
    out = (F(1),F(0))
    for _ in range(k):
        out = cmul(out,z)
    return out

def add(z,w):
    return (z[0]+w[0],z[1]+w[1])

def sphere_moment(exp):
    if any(e % 2 for e in exp):
        return F(0)
    m=sum(exp)//2
    return F(prod(prod(range(1,e,2)) for e in exp),
             prod(len(exp)+2*j for j in range(m)))

def polynomial_moment(coeff, k):
    """Direct multinomial expansion on S^(len(coeff)-1)."""
    zero=(0,)*len(coeff)
    poly={zero:(F(1),F(0))}
    for _ in range(k):
        nxt={}
        for exp,z in poly.items():
            for j,w in enumerate(coeff):
                e=list(exp);e[j]+=1;e=tuple(e)
                nxt[e]=add(nxt.get(e,(F(0),F(0))),cmul(z,w))
        poly=nxt
    return sum(z[0]*sphere_moment(e) for e,z in poly.items())

def eigen(n,k):
    assert k % 2 == 0
    m=k//2
    return (-1)**m * prod(F(2*j+1,n-1+2*j) for j in range(m))

# Polynomial harmonicity, by a coefficient-wise independent differentiation.
for k in range(2,25,2):
    terms={(k-j,j): F((-1)**(j//2)*comb(k,j)) for j in range(0,k+1,2)}
    lap={}
    for (i,j),a in terms.items():
        if i>=2:lap[i-2,j]=lap.get((i-2,j),F(0))+a*i*(i-1)
        if j>=2:lap[i,j-2]=lap.get((i,j-2),F(0))+a*j*(j-1)
    check('harmonic_polynomial',all(v==0 for v in lap.values()))
    check('even_polynomial',all((i+j)%2==0 for i,j in terms))

# Direct integration in rational orthonormal equator frames.
# Each Householder matrix carries e1 to a rational unit u.
for n in range(3,7):
    for seed in (1,2,3):
        t=[F(seed+j,seed+2*n) for j in range(n-1)]
        s=sum(x*x for x in t)
        u=[(1-s)/(1+s)]+[2*x/(1+s) for x in t]
        check('rational_unit_vector',sum(x*x for x in u)==1)
        v=[F(1)-u[0]]+[-x for x in u[1:]]
        v2=sum(x*x for x in v)
        Q=[[F(i==j)-2*v[i]*v[j]/v2 for j in range(n)] for i in range(n)]
        for i in range(n):
            check('householder_first_column',Q[i][0]==u[i])
            for j in range(n):
                check('householder_orthonormal',sum(Q[r][i]*Q[r][j] for r in range(n))==F(i==j))
        coeff=[(Q[0][j],Q[1][j]) for j in range(1,n)]
        for k in range(2,11,2):
            actual=polynomial_moment(coeff,k)
            expected=eigen(n,k)*cpow((u[0],u[1]),k)[0]
            check('equator_eigenvalue_direct_moment',actual==expected)

# Independent beta moment equality against multinomial sphere moments.
for n in range(3,9):
    for ell in range(0,13):
        actual=sum(F(comb(ell,j))*sphere_moment((2*j,2*(ell-j))+(0,)*(n-2)) for j in range(ell+1))
        expected=prod(F(2*(j+1),n+2*j) for j in range(ell))
        check('two_coordinate_beta_moment',actual==expected)

# n=4 specialization of the rigorous lower bound (3), a=1/2.
# Its p-th power is rational for positive integer p; it must grow unbounded.
# For every k>=2, it is >= p*(k-1)/2^(2p), proved by (k+2)/(2k)>=1/2.
ratio_power_samples=[]
for p in (1,2,3,4,8):
    for k in (2,4,8,16,32,64,128):
        check('dimension_four_eigenvalue',abs(eigen(4,k))==F(1,k+1))
        M2=F(1,k+1)
        Mp_power=F(2,p*(k-1)+2)
        full=F(k+2,2*k)**p*F(1,2)**(p-1)*M2**p/(abs(eigen(4,k))**p*Mp_power)
        simplified=F(k+2,2*k)**p*F(1,2)**(p-1)*F(p*(k-1)+2,2)
        check('dimension_four_ratio_power',full==simplified)
        check('dimension_four_linear_growth_bound',full>=F(p*(k-1),2**(2*p)))
        if k in (2,16,128):ratio_power_samples.append({'p':p,'k':k,'lower_ratio_to_power_p':str(full)})

print(json.dumps({
    'status':'PASS',
    'arithmetic':'fractions.Fraction only; exact rational controls',
    'counts':counts,
    'total_checks':sum(counts.values()),
    'ratio_power_samples':ratio_power_samples,
    'limitations':[
        'Finite tests do not prove the all-degree moment formula or asymptotic.',
        'No discretized Wasserstein estimate is used as a proof.',
        'Analytic claims are justified in PROOF.md, including positivity and transport-flow existence.'
    ]},indent=2,sort_keys=True))
