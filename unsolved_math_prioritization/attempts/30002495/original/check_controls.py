#!/usr/bin/env python3
"""Exact finite controls only; no numerical assertion about RH or limiting norms."""
import json
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path


def factor(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0)+1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0)+1
    return out


def mu(n):
    f = factor(n)
    return 0 if any(e > 1 for e in f.values()) else (-1)**len(f)


def logvec(x):
    x = Q(x)
    out = Counter(factor(x.numerator))
    for p, e in factor(x.denominator).items():
        out[p] -= e
    return {p: Q(e) for p, e in out.items() if e}


def plus(a, b, scale=Q(1)):
    out = dict(a)
    for p, e in b.items():
        out[p] = out.get(p, Q(0))+scale*e
        if not out[p]:
            del out[p]
    return out


def scaled(a, c):
    return {p: c*e for p, e in a.items() if c*e}


def lamvec(n):
    f = factor(n)
    return {next(iter(f)): Q(1)} if len(f) == 1 else {}


def floor(x):
    return x.numerator//x.denominator


def frac(x):
    return x-floor(x)


def main():
    counts = Counter()
    maxn = 3000
    mus = [0]+[mu(n) for n in range(1, maxn+1)]
    M = [0]
    for n in range(1, maxn+1):
        M.append(M[-1]+mus[n])
    for n in range(1, maxn+1):
        ds = [d for d in range(1, n+1) if n % d == 0]
        assert sum(mus[d] for d in ds) == (n == 1)
        counts['mobius_divisor_cancellation'] += 1
        lhs = scaled(logvec(n), mus[n])
        rhs = {}
        for d in ds:
            rhs = plus(rhs, lamvec(d), -mus[n//d])
        assert lhs == rhs
        counts['logarithmic_convolution_prime_vectors'] += 1
        assert sum(M[n//d] for d in range(1, n+1)) == 1
        counts['summatory_divisor_inversion'] += 1

    psi = [{}]
    for n in range(1, 302):
        psi.append(plus(psi[-1], lamvec(n)))
    for n in range(1, 301):
        for offset in [Q(0), Q(1, 3), Q(2, 3)]:
            x = Q(n)+offset
            ilog = {}
            i2 = Q(0)
            for k in range(1, n+1):
                b = min(Q(k+1), x)
                if b <= k:
                    continue
                ilog = plus(ilog, logvec(b/Q(k)), M[k])
                i2 += M[k]*(Q(1, k)-1/b)
            rlog = {}
            rconst = Q(0)
            for k in range(1, n+1):
                y = x/k
                rlog = plus(rlog, psi[floor(y)], mus[k])
                rconst -= mus[k]*(y-1)
            assert -x*i2-rconst == 0
            assert plus(ilog, rlog, Q(-1)) == scaled(logvec(x), M[n])
            counts['exact_real_mobius_integral_equation'] += 1

    for N in range(1, 25):
        for exponent in [1, 2]:
            cs = [Q(0)]+[Q(mus[n], n**exponent) for n in range(1, N+1)]
            A = sum((cs[n]/n for n in range(1, N+1)), Q(0))
            for den in range(1, 6):
                for num in range(1, 2*N+4):
                    t = Q(num, den)
                    lhs = -sum((cs[n]*frac(t/n) for n in range(1, N+1)), Q(0))
                    rhs = sum((cs[n]*floor(t/n) for n in range(1, N+1)), Q(0))-t*A
                    assert lhs == rhs
                    counts['damped_fractional_part_decomposition'] += 1
                    if t < 1:
                        assert lhs == -t*A
                        counts['below_one_tail_coefficient'] += 1
    for den in range(1, 8):
        for num in range(1, 701):
            t = Q(num, den)
            z = sum(mus[n]*floor(t/n) for n in range(1, floor(t)+1))
            assert z == (t >= 1)
            counts['rational_floor_mobius_identity'] += 1

    # Exact norm controls: N=k^4, so all amplitudes/powers used are rational.
    for k in range(1, 101):
        N = Q(k**4)
        measure = 1/N-1/(2*N)
        for amp_power, expected in [(Q(k**2), Q(1, 2*k**2)),
                                    (Q(k**3), Q(1, 2*k)),
                                    (Q(k**4), Q(1, 2))]:
            assert amp_power*measure == expected
            counts['escaping_mass_exact_moments'] += 1

    # Compact-support expansion: f(t)=t^2 times a signed step function.
    intervals = [(Q(1, 3), Q(4, 3), Q(2)),
                 (Q(5, 3), Q(11, 3), Q(-3, 2)),
                 (Q(4), Q(6), Q(1, 5))]
    C = sum((c*(b*b-a*a)/2 for a, b, c in intervals), Q(0))
    for den in range(1, 9):
        for num in range(den, 6*den+1):
            a = Q(num, den)
            direct = Q(0)
            tails = Q(0)
            for l, r, c in intervals:
                breaks = sorted({l, r}|{a*j for j in range(floor(l/a), floor(r/a)+2) if l<a*j<r})
                for u, v in zip(breaks, breaks[1:]):
                    m = floor((u+v)/(2*a))
                    direct += c*((v*v-u*u)/(2*a)-m*(v-u))
                for j in range(1, floor(r/a)+1):
                    u = max(l, a*j)
                    if r > u:
                        tails += c*(r-u)
            assert direct == C/a-tails
            counts['compact_support_tail_expansion'] += 1

    assert Q(1, 2)-Q(3, 2)*Q(1, 3) == 0
    assert Q(1, 2)-3*Q(1, 3)+Q(9, 4)*Q(1, 4) == Q(1, 16)
    assert 1/(1+Q(1, 2)) == Q(2, 3)
    counts['two_exponential_kernel_constants'] += 3
    for den in range(2, 52):
        for num in range(1, den):
            z = Q(num, den)
            assert z*(Q(1, 2)-Q(3, 2)*Q(1, 3)) == 0
            assert (z-z*z)/2 > 0
            counts['unilateral_bilateral_separation'] += 1
    assert (Q(1, 2)-Q(1, 4))/2 == Q(1, 8)
    counts['negative_shift_pairing'] += 1
    result = {'schema': 'nyman-real-variable-exact-controls-v1',
              'arithmetic': 'Python standard-library integers and Fraction; logarithms represented by rational prime-exponent vectors',
              'counts': dict(sorted(counts.items())), 'total_assertion_groups': sum(counts.values()),
              'status': 'PASS',
              'limits': ['Finite identities and exact constants only.',
                         'No computation of enormous diagonal cutoffs.',
                         'No test certifies an asymptotic, an infinite-dimensional density, RH, or the methodological equivalence.']}
    return result


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
