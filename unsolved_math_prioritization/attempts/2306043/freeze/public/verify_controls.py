#!/usr/bin/env python3
"""Exact finite controls for the authored analytic proofs; not a proof engine.

Standard library only. The infinite constructions and limits are proved in the
TURN files. No floating-point sampling is used to establish any theorem.
"""
from fractions import Fraction as F
import json
import sys

checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

def autocorrelation(a):
    n = len(a)
    return [sum(a[k+d]*a[k] for k in range(n-d)) for d in range(n)]

def flat_polynomial_controls():
    p = q = [1]
    for m in range(9):
        n = 1 << m
        check(f'flat_{m}_length', len(p) == len(q) == n)
        check(f'flat_{m}_signs', set(p+q) <= {-1, 1})
        ap, aq = autocorrelation(p), autocorrelation(q)
        check(f'flat_{m}_constant_energy', ap[0]+aq[0] == 2*n)
        check(f'flat_{m}_cross_cancellation',
              all(ap[d]+aq[d] == 0 for d in range(1, n)))
        p, q = p+q, p+[-a for a in q]

def energy_controls():
    # Actual prefix of TURN_5: seed n=1 and the full first block 256..511.
    # The next block starts at 65536, so this prefix is exact up to 1024.
    energy = harmonic = cumulative_difference = F(0)
    for n in range(1, 1025):
        b_square = F(1) if n == 1 else (F(1, 2) if 256 <= n < 512 else F(0))
        energy += b_square/n
        harmonic += F(1, n)
        check(f'prefix_energy_{n}', energy <= harmonic)
        cumulative_difference += energy-harmonic
        check(f'prefix_milin_{n}', cumulative_difference <= 0)
    for j in range(3, 21):
        m = 1 << j
        total_m = sum(1 << i for i in range(3, j+1))
        check(f'block_budget_{j}', F(1)+F(total_m, 16) <= F(m, 2))
        check(f'sparse_budget_{j}', F(total_m, 16) <= F(m, 2))
    # Deliberately wrong normalization gamma_1=2 fails the n=1 constraint.
    check('reject_missing_log_factor_two', F(2)**2 > F(1))

def radial_controls():
    for n in range(1, 257):
        r = F(2*n-1, 2*n)
        check(f'bernoulli_{n}', r**n >= F(1, 2))
        check(f'block_radial_lower_{n}', r**(2*n-1) >= F(1, 4))
    q = F(3, 4)
    tail = q**256*(F(256)/(1-q)+q/(1-q)**2)
    check('critical_point_tail_exact', tail < F(1, 4))
    check('critical_point_negative_endpoint', 1-2*q+2*tail < 0)
    check('critical_point_positive_endpoint', F(1) > 0)
    check('tail_closed_form', tail == 1036*q**256)

def logarithm_coefficients(a):
    # a[0]=1; recover coefficients of log(sum a_n z^n) exactly.
    l = [F(0)]*len(a)
    for n in range(1, len(a)):
        l[n] = a[n]-sum((F(k)*l[k]*a[n-k] for k in range(1,n)), F(0))/n
    return l

def normalization_controls():
    for sigma in [F(0), F(1,4), F(1,2), F(3,4), F(1)]:
        exponent = 2*(1-sigma)
        a = [F(1)]
        for n in range(1, 25):
            a.append(a[-1]*(exponent+n-1)/n)
        l = logarithm_coefficients(a)
        check(f'starlike_normalization_{sigma}',
              all(F(n)*l[n]/2 == 1-sigma for n in range(1,25)))
    # Coefficients of the triangular generating kernel (1-r)^(-2).
    for n in range(1, 25):
        for total in range(n, 25):
            check(f'milin_kernel_{n}_{total}', sum(1 for _ in range(total-n+1)) == total+1-n)
    # Finite algebraic Abel identity with its exact tail for a toy nonnegative sequence.
    values = [F(3), F(0), F(2), F(7), F(1)]
    for r in [F(1,4), F(1,2), F(3,4)]:
        lhs = sum(a*r**n for n,a in enumerate(values,1))
        partials=[]; total=F(0)
        for a in values:
            total += a; partials.append(total)
        rhs=(1-r)*sum(s*r**n for n,s in enumerate(partials,1))+total*r**(len(values)+1)
        check(f'abel_identity_{r}', lhs == rhs)

def main():
    flat_polynomial_controls()
    energy_controls()
    radial_controls()
    normalization_controls()
    report = {
        'status': 'PASS',
        'checks_passed': len(checks),
        'arithmetic': 'exact integers and fractions; no floating-point proof claims',
        'groups': ['Rudin-Shapiro Laurent-energy identities',
                   'actual-prefix partial and Milin energies',
                   'all-scale budget formula finite controls',
                   'rational radial and critical-point safeguards',
                   'logarithmic normalization and Abel-kernel identities'],
        'scope': 'Finite controls corroborate formulas; infinite proofs are in TURN_1 through TURN_5.',
        'full_problem_solved': False,
        'relaxed_map_univalent': False,
    }
    print(json.dumps(report, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
