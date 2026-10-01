"""Exact finite controls for the analytic argument; not a proof of asymptotics.

Uses only Python's standard library. The two rational assembly weight families
test structural identities independently of transcendental zeta evaluations.
"""
from fractions import Fraction as F
from math import factorial, prod
from collections import Counter
import json

checks = Counter()

def check(condition, family):
    assert condition, family
    checks[family] += 1

def compositions(n):
    if n == 0:
        yield ()
    else:
        for j in range(1, n + 1):
            for tail in compositions(n - j):
                yield (j,) + tail

def falling(x, r):
    return prod(range(x-r+1, x+1)) if r <= x else 0

for height_cutoff in (1, 2):
    a = [F(0)] + [sum((F(1, m**(2*j)) for m in range(1, height_cutoff+1)), F(0))/(2*j) for j in range(1, 11)]
    h = [F(1)]
    for n in range(1, 11):
        h.append(sum((j*a[j]*h[n-j] for j in range(1, n+1)), F(0))/n)
        comp = list(compositions(n))
        mass = [prod(a[j] for j in c)/factorial(len(c)) for c in comp]
        check(sum(mass, F(0)) == h[n], 'assembly_normalization')
        counts = [Counter(c) for c in comp]
        for j in range(1, n+1):
            for r in (1, 2, 3):
                observed = sum((w*falling(c[j], r) for w,c in zip(mass, counts)), F(0))/h[n]
                expected = a[j]**r*h[n-j*r]/h[n] if j*r <= n else F(0)
                check(observed == expected, 'single_factorial_moments')
            for k in range(j+1, n+1):
                observed = sum((w*c[j]*c[k] for w,c in zip(mass, counts)), F(0))/h[n]
                expected = a[j]*a[k]*h[n-j-k]/h[n] if j+k <= n else F(0)
                check(observed == expected, 'mixed_factorial_moments')
        # Uniformly mark each j-part with a rational, size-dependent chance.
        b = [F(0)] + [F(j, j+1) for j in range(1, n+1)]
        actual_first = sum((w*sum((b[j] for j in c), F(0)) for w,c in zip(mass, comp)), F(0))/h[n]
        expected_first = sum((a[j]*b[j]*h[n-j]/h[n] for j in range(1, n+1)), F(0))
        check(actual_first == expected_first, 'marked_first_moment')
        actual_second = sum((w*sum((b[c[i]]*b[c[l]] for i in range(len(c)) for l in range(len(c)) if i != l), F(0)) for w,c in zip(mass, comp)), F(0))/h[n]
        expected_second = sum((a[j]*b[j]*a[k]*b[k]*h[n-j-k]/h[n] for j in range(1,n) for k in range(1,n-j+1)), F(0))
        check(actual_second == expected_second, 'marked_second_factorial')
        # Dirichlet monomial integration gives exactly product 1/(2j).
        for c in comp:
            integrated = prod(F(factorial(2*j-1), factorial(2*j)) for j in c)/factorial(2*n-1)
            check(integrated == prod(F(1, 2*j) for j in c)/factorial(2*n-1), 'simplex_monomial_factor')

def D(g, k):
    return F(factorial(6*g-5-2*k)*2**(2*k-3), factorial(g-k)*factorial(3*g-3-k)*3**(g-k)) if k >= 2 else F(factorial(6*g-7), 2*factorial(g-1)*factorial(3*g-4)*3**(g-1))

for g in range(3, 51):
    for k in range(1, min(g-1, 12)):
        ratio = F(12*(g-k)*(3*g-3-k), (6*g-5-2*k)*(6*g-6-2*k))
        check(D(g,k+1)/D(g,k) == ratio, 'geometric_prefactor_ratio')

# The rational lower bound log(1+x)>x/(1+x) gives eta>1/220.
check(F(3,5)*F(1,11)-F(1,20) == F(1,220), 'tail_exponent_lower_bound')
# telescoping finite Euler product: B(1)^2 tends to 2.
for m in range(2, 101):
    check(prod(1-F(1,k*k) for k in range(2,m+1)) == F(m+1,2*m), 'Euler_product')
# Binomial coefficients for (1-z)^(-1/2) obey the exact recurrence.
for n in range(1, 101):
    cn = F(factorial(2*n), 4**n*factorial(n)**2)
    prev = F(factorial(2*n-2), 4**(n-1)*factorial(n-1)**2)
    check(cn/prev == F(2*n-1,2*n), 'binomial_ratio')

print(json.dumps({'status':'PASS','total_exact_assertions':sum(checks.values()),'families':dict(sorted(checks.items())), 'scope':'Finite algebraic controls only; the proof of limits and geometric inputs is in CANDIDATE.md and the cited primary sources.'}, indent=2, sort_keys=True))
