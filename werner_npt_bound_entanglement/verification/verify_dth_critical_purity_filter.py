#!/usr/bin/env python3
"""Dependency-free exact checks for the critical purity filter."""

from fractions import Fraction as Q
import random


D = 3
N = D**3


def digits(k):
    return (k // 9, (k // 3) % 3, k % 3)


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def hs(a, b):
    return sum(a[i][j] * b[i][j] for i in range(len(a)) for j in range(len(a)))


def marginal(a, site):
    out = [[Q(0) for _ in range(D)] for _ in range(D)]
    for i in range(N):
        ii = digits(i)
        for j in range(N):
            jj = digits(j)
            if all(ii[k] == jj[k] for k in range(3) if k != site):
                out[ii[site]][jj[site]] += a[i][j]
    return out


def build_projection(a):
    qs = [marginal(a, s) for s in range(3)]
    out = [[Q(int(i == j), 27) for j in range(N)] for i in range(N)]
    for s in range(3):
        for i in range(N):
            ii = digits(i)
            for j in range(N):
                jj = digits(j)
                if all(ii[k] == jj[k] for k in range(3) if k != s):
                    value = qs[s][ii[s]][jj[s]]
                    if ii[s] == jj[s]:
                        value -= Q(1, 3)
                    out[i][j] += value / 9
    return qs, out


def random_trace_one_symmetric(seed=20260801):
    rng = random.Random(seed)
    r = [[Q(rng.randint(-3, 3)) for _ in range(7)] for _ in range(N)]
    a = [[sum(r[i][k] * r[j][k] for k in range(7)) for j in range(N)] for i in range(N)]
    tr = trace(a)
    return [[x / tr for x in row] for row in a]


def main():
    omega = random_trace_one_symmetric()
    assert trace(omega) == 1
    qs, proj = build_projection(omega)

    # The residual is orthogonal to the scalar and every one-body matrix unit.
    residual = [[omega[i][j] - proj[i][j] for j in range(N)] for i in range(N)]
    assert trace(residual) == 0
    for s in range(3):
        assert marginal(residual, s) == [[Q(0) for _ in range(D)] for _ in range(D)]

    sum_q_purity = sum(hs(q, q) for q in qs)
    asserted_norm = (3 * sum_q_purity - 2) / 27
    assert hs(proj, proj) == asserted_norm
    assert hs(omega, omega) == hs(proj, proj) + hs(residual, residual)

    # Exact scalar arithmetic in the critical application.
    p = Q(29, 21)
    ell = (1 + 3 * p) / 108
    boundary_gap = (1 + p) / 32 - Q(1, 16) - ell / 4
    assert boundary_gap == 0

    # The derivative of F^2/4+(1-F)^2 L is positive for F >= 1/2,
    # because L <= 5/54.
    assert Q(1, 4) - Q(5, 54) > 0
    print("PASS: exact one-body projection and 29/21 critical filter")


if __name__ == "__main__":
    main()

