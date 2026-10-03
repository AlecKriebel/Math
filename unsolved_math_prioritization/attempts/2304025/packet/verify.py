#!/usr/bin/env python3
"""Exact finite controls, not a proof of the unrestricted analytic infimum."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

checks = 0

def require(condition):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(f"Failed check {checks}")

def convolve(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c

def fourier(alpha, n):
    """Returns c_k(alpha)/C(alpha), 0 <= k <= n, as exact rationals."""
    r = [F(1)]
    for k in range(n):
        r.append(r[-1] * (F(k)-alpha)/(F(k)+alpha+1))
    return r

def energy(p, alpha):
    r = fourier(alpha, len(p)-1)
    return sum(F(p[i]*p[j])*r[abs(i-j)]
               for i in range(len(p)) for j in range(len(p)))

def c_ratio(alpha):
    """C(alpha+1)/C(alpha)."""
    return 2*(2*alpha+1)/(alpha+1)

def interval_energy(n, alpha):
    return energy([1]*n, alpha) if n else F(0)

# Fourier signs and the finite telescoping identity behind the infinite sum.
# c_0 + 2 sum_{k=1}^N c_k = -(N+alpha+1)c_{N+1}/alpha.
for a in (F(1,4), F(1,2), F(3,4)):
    r = fourier(a, 101)
    require(all(x < 0 for x in r[1:]))
    require(all(r[k+1] > r[k] for k in range(1,101)))
    for n in range(0,100):
        require(1 + 2*sum(r[1:n+1]) == -(n+a+1)*r[n+1]/a)

# Full finite controls for all five-coefficient sequences in {-1,0,1}.
# No restriction to monic is needed for the elementary lower bounds.
sequences = [list(p) for p in product((-1,0,1), repeat=5) if any(p)]
for a in (F(1,4), F(1,2), F(3,4), F(1)):
    for p in sequences:
        ep = energy(p,a)
        require(ep >= 1)
        if a < 1:
            require((ep == 1) == (sum(x*x for x in p) == 1))
        q = convolve([1,-1],p)
        eq = energy(q,a)
        require(eq == c_ratio(a)*energy(p,a+1))
        require(eq >= 2)
        if a < 1:
            require(eq > 2)
        pos = [max(x,0) for x in q]
        neg = [max(-x,0) for x in q]
        require(eq >= energy(pos,a) + energy(neg,a))

# Level-set/isoperimetric inequality for all nonnegative length-five sequences
# with coefficients at most two, and the higher multiplicity mass bounds.
for a in (F(1,4),F(1,2),F(3,4)):
    for tup in product((0,1,2), repeat=5):
        if not any(tup):
            continue
        require(energy(tup,a) >= interval_energy(sum(tup),a))
    for p in sequences:
        q = convolve([1,-2,1],p)
        mass = sum(max(x,0) for x in q)
        require(mass >= 2)
        require(energy(q,a) >= 2*interval_energy(2,a))
        require(energy(q,a) == c_ratio(a)*c_ratio(a+1)*energy(p,a+2))

# The six exact integer witnesses.
factor_lists = [[1],[1,2],[1,2,3],[1,2,3,5],
                [1,2,3,5,7],[1,2,3,4,5,7]]
witnesses = []
for m, ns in enumerate(factor_lists, start=1):
    q, p = [1], [1]
    for n in ns:
        q = convolve(q,[1]+[0]*(n-1)+[-1])
        p = convolve(p,[1]*n)
    reconstructed = p
    for _ in range(m):
        reconstructed = convolve(reconstructed,[1,-1])
    require(q == reconstructed)
    require(p[-1] == 1)
    require(all(x in (-1,0,1) for x in q))
    require(sum(x*x for x in q) == 2*m)
    require(sum(x>0 for x in q) == sum(x<0 for x in q) == m)
    for exponent in range(m):
        require(sum(qj*j**exponent for j,qj in enumerate(q)) == 0)
    require(sum(qj*j**m for j,qj in enumerate(q)) != 0)
    require(energy(p,F(m))*F(__import__('math').comb(2*m,m)) == 2*m)
    witnesses.append({'m':m,'factors':ns,'P_coefficients':p,
                      'difference_coefficients':q,'squared_norm':2*m})

# General binary construction: distinct subset sums checked through m=10.
for m in range(1,11):
    q = [1]
    for j in range(m):
        q = convolve(q,[1]+[0]*(2**j-1)+[-1])
    require(len(q) == 2**m)
    require(all(x in (-1,1) for x in q))
    require(sum(x*x for x in q) == 2**m)
    for exponent in range(m):
        require(sum(qj*j**exponent for j,qj in enumerate(q)) == 0)

# Geometric-sum exact formulas and clustered upper-bound identities.
limits = []
for a in (F(1,4),F(1,2),F(3,4)):
    for n in range(2,16):
        r = fourier(a,2*n+1)
        require(c_ratio(a)*energy([1]*n,a+1) == 2*(1-r[n]))
        q = [0]*(2*n+2)
        q[0],q[n],q[n+1],q[2*n+1] = 1,-1,-1,1
        exact = 4-4*r[n]-4*r[n+1]+2*r[2*n+1]+2*r[1]
        require(energy(q,a) == exact)
        limit = 2*(a+2)/(a+1)
        require(exact > limit)
        require(exact >= 4/(a+1))
    limits.append({'alpha':str(a),'lower_over_C_alpha':str(4/(a+1)),
                   'cluster_upper_over_C_alpha':str(2*(a+2)/(a+1))})

# Limited diagnostic search: coefficients {-1,0,1}, degree at most six.
# These minima are only finite-box records, not claims about F.
box_minima=[]
for a in (F(1,2),F(3,2),F(5,2),F(7,2)):
    best=None
    for degree in range(7):
        for prefix in product((-1,0,1),repeat=degree):
            p=prefix+(1,)
            e=energy(p,a)
            if best is None or e<best[0]:
                best=e,p
    box_minima.append({'lambda':str(a),'degree_max':6,'alphabet':[-1,0,1],
                      'energy_over_C_lambda':str(best[0]),'coefficients':list(best[1])})

result={'status':'PASS','exact_assertions':checks,
        'scope':'Finite exact controls only; universal inequalities and limits require PROOF.md.',
        'integer_witnesses':witnesses,'fractional_bounds':limits,
        'finite_box_diagnostics':box_minima}
text=json.dumps(result,indent=2,sort_keys=True)+'\n'
Path(__file__).with_name('verification.json').write_text(text)
print(text)
