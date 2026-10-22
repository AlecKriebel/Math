#!/usr/bin/env python3
"""Exact, reproducible controls for ATTEMPT_3.md. No network or third-party data."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb


def shuffle_histogram_dp(horizontal, vertical):
    # State is consumed projection lengths and final letter. Values count corners.
    states = {(0, 0, ''): Counter({0: 1})}
    for _ in range(len(horizontal) + len(vertical)):
        following = {}
        for (i, j, last), polynomial in states.items():
            choices = []
            if i < len(horizontal):
                choices.append((horizontal[i], i + 1, j))
            if j < len(vertical):
                choices.append((vertical[j], i, j + 1))
            for step, ni, nj in choices:
                shift = int(last + step in ('NW', 'ES'))
                target = following.setdefault((ni, nj, step), Counter())
                for degree, coefficient in polynomial.items():
                    target[degree + shift] += coefficient
        states = following
    result = Counter()
    for polynomial in states.values():
        result.update(polynomial)
    return result


def exhaustive_histogram(horizontal, vertical):
    """Independent enumeration: choose horizontal positions and inspect every word."""
    length = len(horizontal) + len(vertical)
    result = Counter()
    mixed = 0
    for horizontal_positions in combinations(range(length), len(horizontal)):
        positions = set(horizontal_positions)
        hi = vi = 0
        word = []
        for i in range(length):
            if i in positions:
                word.append(horizontal[hi]); hi += 1
            else:
                word.append(vertical[vi]); vi += 1
        nw = sum(word[i:i+2] == ['N', 'W'] for i in range(length-1))
        es = sum(word[i:i+2] == ['E', 'S'] for i in range(length-1))
        result[nw+es] += 1
        mixed += int(nw > 0 and es > 0)
        # Both projections are Dyck; additionally verify the merged path itself.
        x = y = 0
        for step in word:
            x += (step == 'E') - (step == 'W')
            y += (step == 'N') - (step == 'S')
            assert x >= 0 and y >= 0
        assert x == y == 0
    return result, mixed


def formulas(n):
    mountain = Counter({0: comb(n+2, 2)**2,
                        1: n*(n+1)*(n+2)**2//3,
                        2: 2*comb(n+2, 4) if n >= 2 else 0})
    k = comb(n+1, 2)**2
    alternating = mountain.copy()
    alternating[0] -= k
    alternating[2] += k
    return alternating, mountain


def evaluate(histogram, a):
    return sum(count*a**degree for degree, count in histogram.items())


def shifted(histogram):
    maximum = max(histogram, default=0)
    return [sum(count * comb(degree, k) * (-1)**(degree-k)
                for degree, count in histogram.items() if degree >= k)
            for k in range(maximum+1)]


def signed_kernel(h, v):
    r, l, u, d = h.count('E'), h.count('W'), v.count('N'), v.count('S')
    return sum((-1 if (u-j) % 2 else 1)*comb(r+u,j)*comb(l+d,u+d-j)
               for j in range(r+u+1) if 0 <= u+d-j <= l+d)


def marked_corner_derivative(h, v):
    total = 0
    for i, hs in enumerate(h):
        for j, vs in enumerate(v):
            if (hs, vs) in [('W','N'), ('E','S')]:
                total += signed_kernel(h[:i],v[:j]) * signed_kernel(h[i+1:],v[j+1:])
    return total


def main():
    for n in range(1,41):
        alternating, mountain = formulas(n)
        assert shuffle_histogram_dp('EWEW','N'*n+'S'*n) == +alternating
        assert shuffle_histogram_dp('EEWW','N'*n+'S'*n) == +mountain
        for h, polynomial in [('EWEW',alternating),('EEWW',mountain)]:
            assert evaluate(polynomial,-1) == comb(n+2,2)
            assert sum(polynomial.values()) == comb(2*n+4,4)
            assert marked_corner_derivative(h,'N'*n+'S'*n) == shifted(polynomial)[1]
    print('Exact DP agrees with the symbolic family for n=1,...,40.')
    n = 13
    alt, mount = formulas(n)
    for h, expected in [('EWEW', alt), ('EEWW', mount)]:
        histogram, mixed = exhaustive_histogram(h, 'N'*n+'S'*n)
        assert histogram == expected
        assert mixed == (comb(n+1,2)**2 if h == 'EWEW' else 0)
        print(f'n=13, H={h}, exact histogram={dict(sorted(histogram.items()))}, mixed={mixed}.')
    g = alt + mount
    assert shifted(g) == [210, -182, 13741]
    print(f'ABM (P2) counterexample: G_13(a)={dict(sorted(g.items()))}; coefficients in a+1={shifted(g)}.')
    alt, _ = formulas(8)
    assert evaluate(alt,Fraction(-1,2)) == -42
    print('Fixed shuffle class, n=8, H=EWEW, a=-1/2: -42.')
    alt, mount = formulas(21)
    g = alt + mount
    assert evaluate(g,Fraction(-9,10)) == Fraction(-6919,100)
    print('Fixed vertical projection, n=21, horizontal half-length=2, a=-9/10: -6919/100.')
    print('These are refined-projection counterexamples, NOT counterexamples to ABM Conjectures 10 or 11.')


if __name__ == '__main__':
    main()
