#!/usr/bin/env python3
"""Bounded exact source-consistency diagnostics, not a proof of the target."""
from fractions import Fraction as F
from math import comb, factorial
from collections import Counter
import json

checks = Counter()
def check(condition, category):
    assert condition, category
    checks[category] += 1

# Gamma(m+3/2)/sqrt(pi), all coefficients rational.
def half_gamma(m):
    return F(factorial(2*m+2), 4**(m+1)*factorial(m+1))

def laguerre_half_integral(k):
    coefficients = [F((-1)**j * comb(k,j),factorial(j)) for j in range(k+1)]
    return sum((a*b*half_gamma(j+l)
                for j,a in enumerate(coefficients)
                for l,b in enumerate(coefficients)),F(0))

# q_n = E Tr(sqrt(XX*))/sqrt(pi) from the orthogonal-polynomial kernel.
q=[F(0)]
for k in range(30):
    increment = laguerre_half_integral(k)
    check(increment>0,'positive_exact_laguerre_integrals')
    q.append(q[-1]+increment)
check(q[1]==F(1,2),'initial_moments')
check(q[2]==F(11,8),'initial_moments')
for n in range(1,30):
    check(q[n+1] == (2+F(3,4*n*n))*q[n]-q[n-1], 'square_complex_recurrence')
    # All terms positive: squaring removes the n^(3/2) factors exactly.
    check(q[n]**2*(n+1)**3 > q[n+1]**2*n**3,
          'strict_complex_normalized_decrements')

# Integer polynomial residue in Hutnik v2 Proposition 3.4.
for n in range(3,101):
    residue=4*n**3-4*n**2-13*n+4
    check(residue>0, 'real_coefficient_ratio_residue')
    left=F((2*n+1)**2*(n+1),4*n*(n+2)**2)
    right=(1-F(1,2*n))**2
    check(left<right, 'real_first_diagonal_ratio')

# Finite rational checks of the harmonic estimate used at n>=4.
harmonic=F(0)
for n in range(1,101):
    harmonic += F(1,n)
    if n>=4:
        check(harmonic+F(13,15)<F(3*n,4), 'real_harmonic_comparison')

receipt={'status':'passed','arithmetic':'exact Python integers and fractions',
         'checks':dict(checks),'total_assertions':sum(checks.values()),
         'complex_dimensions':30,
         'scope':'Finite normalization/recurrence/algebra checks only; no certification of the real proof or all-dimensional target'}
print(json.dumps(receipt,indent=2))
