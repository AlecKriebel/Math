#!/usr/bin/env python3
"""Independent exact audit of the public Argus 11000263 Burau witness.

This implementation was written from the mathematical presentation and standard
Burau block. No third-party verifier code is imported, copied, or executed.
Prior art: https://github.com/Argus-AiTeam/argus-mathematics/tree/5abed447441b42dbe9f735e8b2960ee0a0705235/results/11000263
Only Python's standard library is needed. This is a bounded regression test,
not a substitute for the all-index proof in AUDIT.md.
"""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    return [[sum(x*y for x, y in zip(r, c)) for c in zip(*b)] for r in a]


def inv(a):
    n = len(a)
    m = [row[:] + unit for row, unit in zip(a, eye(n))]
    for k in range(n):
        p = next(i for i in range(k, n) if m[i][k])
        m[k], m[p] = m[p], m[k]
        divisor = m[k][k]
        m[k] = [x/divisor for x in m[k]]
        for i in range(n):
            if i != k:
                c = m[i][k]
                m[i] = [x-c*y for x, y in zip(m[i], m[k])]
    return [row[n:] for row in m]


def rank(a):
    m = [row[:] for row in a]
    row = 0
    for j in range(len(m[0])):
        p = next((i for i in range(row, len(m)) if m[i][j]), None)
        if p is None:
            continue
        m[row], m[p] = m[p], m[row]
        d = m[row][j]
        m[row] = [x/d for x in m[row]]
        for i in range(row+1, len(m)):
            c = m[i][j]
            m[i] = [x-c*y for x, y in zip(m[i], m[row])]
        row += 1
    return row


def braid(n, i, u):
    a = eye(n)
    j = i-1
    a[j][j], a[j][j+1] = 1-u, u
    a[j+1][j], a[j+1][j+1] = Q(1), Q(0)
    return a


def run_case(n, q, u):
    q, u = Q(q), Q(u)
    unit = eye(n)
    zero = scale(0, unit)
    b = {i: braid(n, i, u) for i in range(1, n)}
    checks = 0

    def equal(a, c):
        nonlocal checks
        assert a == c
        checks += 1

    def word(indices):
        a = unit
        for i in indices:
            a = mul(a, b[i])
        return a

    # Whole-word inverse is computed by exact Gaussian elimination.
    def bar(indices):
        return inv(word(indices))

    for i in b:
        equal(mul(b[i], inv(b[i])), unit)
        for j in b:
            if abs(i-j) > 1:
                equal(mul(b[i], b[j]), mul(b[j], b[i]))
            if j == i+1:
                equal(word([i, j, i]), word([j, i, j]))

    x = {2: sub(add(scale(q, inv(b[1])), scale(1-q, unit)), b[1])}
    for k in range(3, n+1):
        factor = sub(scale(q**(k-1), bar(range(k-1, 0, -1))), word(range(1, k)))
        x[k] = mul(factor, x[k-1])

    coefficient = Q(1)
    for k in range(2, n+1):
        coefficient *= q**(k-1)-u
        a = [Q(0)] * n
        a[k-2], a[k-1] = u**(2-k), -u**(1-k)
        covector = [Q(-1), Q(1)] + [Q(0)]*(n-2)
        expected = [[coefficient*r*c for c in covector] for r in a]
        equal(x[k], expected)

    # R_2 and every legal R_k, including the row called terminal in the
    # alternative presentation with one additional braid strand.
    left2 = mul(sub(add(scale(q, inv(b[2])), scale(1-q, unit)), b[2]), x[2])
    right2 = mul(sub(scale(q, bar([2, 1])), word([1, 2])), x[2])
    equal(left2, right2)
    for k in range(3, n):
        left = sub(scale(q**(k-1), bar(range(k, 1, -1))), word(range(2, k+1)))
        right = sub(scale(q**(k-1), bar(range(k, 0, -1))), word(range(1, k+1)))
        equal(mul(left, x[k]), mul(right, x[k]))

    equal(mul(b[1], x[2]), scale(-u, x[2]))
    twist = word([1, 2, 1, 2, 1, 2])
    equal(mul(twist, x[3]), scale(u**3, x[3]))
    expected_rank = 0 if u in [q, q*q] else 1
    assert rank(x[3]) == expected_rank
    checks += 1
    if u == q**3 and n >= 4:
        equal(x[4], zero)
        assert rank(x[3]) == 1
        checks += 1
    return {"strands": n, "q": str(q), "u": str(u), "checks": checks,
            "rank_X3": expected_rank, "status": "passed"}


def main():
    params = [(2, 3), (2, 8), (3, 27), (2, 2), (2, 4), (Q(2, 3), Q(8, 27))]
    cases = [run_case(n, q, u) for n, (q, u) in product(range(3, 10), params)]
    receipt = {"status": "passed", "arithmetic": "fractions.Fraction",
               "case_count": len(cases), "equality_and_rank_checks": sum(c['checks'] for c in cases),
               "scope": "B_n for 3<=n<=9; legal rows R_2,...,R_(n-1), both indexing readings, formula, braid relations, twists, degeneracies",
               "cases": cases}
    target = Path(__file__).with_name('verification.json')
    target.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k:v for k,v in receipt.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
