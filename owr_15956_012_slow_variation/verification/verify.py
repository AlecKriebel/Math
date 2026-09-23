#!/usr/bin/env python3
"""Exact finite checks accompanying the analytic proof; not formal verification.
Run with Python >=3.9. No third-party dependencies or network access.
"""
from fractions import Fraction as Q
from itertools import product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def summatory(values, n, odd=False):
    return sum((values[i] for i in range(1, n + 1) if not odd or i % 2), Q(0))


def local_value(n, weights):
    value = Q(1)
    for p, seq in weights.items():
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        if exponent:
            if exponent >= len(seq):
                return Q(0)
            value *= seq[exponent]
    return value if n == 1 else Q(0)


def main():
    counts = {'multiplicative_fixtures': 0, 'decompositions': 0,
              'dilation_bounds': 0, 'finite_sum_bounds': 0,
              'convolution_inequalities': 0, 'example_checks': 0}
    # All 3^5 choices. Unlisted prime powers have weight zero.
    # This includes a1=0, a2>0 and a2 != a1^2, so complete
    # multiplicativity cannot be silently substituted in the main identity.
    for choices in product((Q(0), Q(1, 2), Q(2)), repeat=5):
        weights = {2: (Q(1), *choices[:3]), 3: (Q(1), choices[3]),
                   5: (Q(1), choices[4])}
        values = [Q(0)] + [local_value(n, weights) for n in range(1, 513)]
        F, G = [Q(0)], [Q(0)]
        for n in range(1, 513):
            F.append(F[-1] + values[n])
            G.append(G[-1] + (values[n] if n % 2 else 0))
        a = weights[2]
        A = sum(a)
        for x in range(1, 65):
            require(F[x] == sum(a[k] * G[x // (2**k)] for k in range(4)),
                    'Prime-power decomposition failed')
            counts['decompositions'] += 1
            require(F[x] <= A * G[x], 'Finite local-sum lower bound failed')
            counts['finite_sum_bounds'] += 1
            for K in range(4):
                require(sum(a[:K+1]) * G[x] <= F[(2**K)*x],
                        'Fixed-dilation upper bound failed')
                counts['dilation_bounds'] += 1
        counts['multiplicative_fixtures'] += 1
    # Check the independent increment inequality in a more general setting:
    # arbitrary nonnegative staircase increments and convolution kernels.
    for increments in product((0, 1, 3), repeat=4):
        g = [Q(0)]
        for increment in increments:
            g.append(g[-1] + increment)
        for tail in product((Q(0), Q(1, 2), Q(2)), repeat=3):
            a = (Q(1), *tail)
            h = [sum(a[k]*g[n-k] for k in range(min(n, 3)+1))
                 for n in range(5)]
            for n in range(1, 5):
                for K in range(4):
                    previous = max(0, n-K)
                    lhs = sum(a)*g[n]-h[n]
                    rhs = sum(a[:K+1])*(h[n]-h[previous])+sum(a[K+1:])*h[n]
                    require(0 <= lhs <= rhs, 'Independent increment bound failed')
                    counts['convolution_inequalities'] += 1
    # f(n)=1/n: exact harmonic identity and analytic constants 1/2 vs 3/4.
    harmonic = [Q(0)]
    for n in range(1, 257):
        harmonic.append(harmonic[-1] + Q(1, n))
    for n in range(1, 257):
        odd = sum((Q(1, i) for i in range(1, n+1, 2)), Q(0))
        require(odd == harmonic[n] - harmonic[n//2]/2, 'Harmonic identity failed')
        require(Q(1, 2) <= odd/harmonic[n], 'Harmonic lower bound failed')
        counts['example_checks'] += 1
    require(1-Q(1, 2) == Q(1, 2) and 1-Q(1, 4) == Q(3, 4),
            'Geometric-series constants failed')
    # Infinite A, and a finite-A bounded sum: support at powers of two.
    for n in range(1, 513):
        L = n.bit_length()-1
        support = [m for m in range(1, n+1) if m & (m-1) == 0]
        require(len(support) == L+1, 'Power-of-two support count failed')
        finite_weight = sum((Q(1, m) for m in support), Q(0))
        require(finite_weight == 2-Q(1, 2**L), 'Bounded geometric sum failed')
        counts['example_checks'] += 1
    # Index-one control: f=1 has F(2n)/F(n)=2 and odd proportion 1/2,
    # so its behavior cannot justify the unweighted formula (A=infinity).
    for n in range(2, 513, 2):
        require(sum(1 for k in range(1, n+1) if k % 2) == n//2,
                'Index-one control failed')
        counts['example_checks'] += 1
    print(json.dumps({'status': 'PASS', 'arithmetic': 'exact rational/integer',
                      'scope': 'finite identities and examples only; see paper for limit proof',
                      'checks': counts}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
