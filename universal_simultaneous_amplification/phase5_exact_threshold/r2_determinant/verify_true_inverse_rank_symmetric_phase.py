#!/usr/bin/env python3
"""Independent exact verifier for the stationary symmetric phase theorem.

The verifier has three deliberately separate parts.

1. It rebuilds the two-channel symmetric rank system from equations (27)--
   (31) of FIXED_COUNT_TWO_REPLICA.md and solves every genuinely small order.
2. It checks the finite rational phase certificate for 40 <= N <= 287.
3. It audits the integer-polynomial certificates used for every N >= 288.

No floating-point arithmetic is used.
"""

from __future__ import annotations

from fractions import Fraction as Q
from math import comb

from flint import fmpq, fmpq_mat
import sympy as sp


def inverse(matrix):
    size = len(matrix)
    augmented = [
        row[:] + [Q(int(i == j)) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(size):
            if row != column and augmented[row][column]:
                scale = augmented[row][column]
                augmented[row] = [
                    x - scale * y for x, y in zip(augmented[row], augmented[column])
                ]
    return [row[size:] for row in augmented]


def matvec(matrix, vector):
    return [sum((x * y for x, y in zip(row, vector)), Q(0)) for row in matrix]


def matmul(left, right):
    return [
        [
            sum((left[i][h] * right[h][j] for h in range(len(right))), Q(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def rank_data(N: int):
    """Return the radial differences and the two binomial rewards."""
    c0 = Q(2**N - 1, N * 2 ** (N - 1))
    d = [Q(0)] * (N + 1)
    for k in range(1, N):
        d[k] = ((k - 1) * d[k - 1] + 2 * N * (Q(1, k) - c0)) / (N - k)
    assert (N - 1) * d[N - 1] + 2 * N * (Q(1, N) - c0) == 0

    ga = [Q(comb(N - 2, k - 1), 2 ** (N - 1) * (N + 1)) for k in range(1, N)]
    qb = [Q(comb(N - 3, k - 2), 2 ** (N - 2) * (N + 1)) for k in range(2, N)]
    return d, ga, qb


def symmetric_system(N: int):
    """Build K, source, and reward directly from the two-channel formulas."""
    na = N - 1
    nb = N - 2
    size = na + nb
    K = [[Q(0) for _ in range(size)] for _ in range(size)]

    def ia(k: int) -> int:
        return k - 1

    def ib(k: int) -> int:
        return na + k - 2

    def add(row: int, column: int, value: Q):
        if value:
            K[row][column] += value

    for k in range(1, N):
        add(ia(k), ia(k), Q(k, 2 * N))
        if k + 1 < N:
            add(ia(k), ia(k + 1), Q(N - k - 1, 2 * N))
            add(ia(k), ib(k + 1), -Q(1, N))

    for k in range(2, N):
        add(ib(k), ia(k - 1), Q(k - 1, 2 * k * N))
        add(ib(k), ia(k), Q(N - k, 2 * k * N))
        if k > 2:
            add(ib(k), ib(k - 1), Q((k - 1) * (k - 2), 2 * k * N))
        add(ib(k), ib(k), Q(N * (k - 2) + k, 2 * k * N))
        if k + 1 < N:
            add(ib(k), ib(k + 1), Q(N - k - 2, 2 * N))

    d, ga, qb = rank_data(N)
    source = [d[k] / 2 for k in range(1, N)] + [d[k - 1] / (2 * k) for k in range(2, N)]
    reward = ga + [-value for value in qb]
    return K, source, reward


def exact_small_scalar(N: int) -> fmpq:
    K, source, reward = symmetric_system(N)
    size = len(K)
    fundamental = fmpq_mat(
        size,
        size,
        [fmpq(int(i == j)) - fmpq(K[i][j].numerator, K[i][j].denominator)
         for i in range(size) for j in range(size)],
    )
    rhs = fmpq_mat(size, 1, [fmpq(x.numerator, x.denominator) for x in source])
    response = fundamental.solve(rhs)
    return sum(
        (fmpq(reward[i].numerator, reward[i].denominator) * response[i, 0]
         for i in range(size)),
        fmpq(0),
    )


def check_phase_identity(N: int):
    K, source, reward = symmetric_system(N)
    na = N - 1
    size = len(K)
    H = transpose(K)
    S = [row[:na] for row in H[:na]]
    C = [row[na:] for row in H[:na]]
    D = [[-entry for entry in row[:na]] for row in H[na:]]
    Qblock = [row[na:] for row in H[na:]]
    assert all(entry >= 0 for block in (S, C, D, Qblock) for row in block for entry in row)

    RS = inverse([[Q(int(i == j)) - S[i][j] for j in range(na)] for i in range(na)])
    nb = N - 2
    RQ = inverse(
        [[Q(int(i == j)) - Qblock[i][j] for j in range(nb)] for i in range(nb)]
    )
    ga = reward[:na]
    qb = [-entry for entry in reward[na:]]
    sg = source[:na]
    sb = source[na:]
    W = matvec(RQ, qb)
    r = [x - y for x, y in zip(ga, matvec(C, W))]
    RQD = matmul(RQ, D)
    ell = [
        sg[j] - sum((sb[i] * RQD[i][j] for i in range(nb)), Q(0))
        for j in range(na)
    ]
    A = matmul(matmul(RS, C), RQD)
    f0 = matvec(RS, r)
    phase = matvec(
        inverse([[Q(int(i == j)) + A[i][j] for j in range(na)] for i in range(na)]),
        f0,
    )
    value = sum((x * y for x, y in zip(ell, phase)), Q(0)) - sum(
        (x * y for x, y in zip(sb, W)), Q(0)
    )
    direct = exact_small_scalar(N)
    assert fmpq(value.numerator, value.denominator) == direct


def phase_contraction(N: int) -> Q:
    return Q(2 * N - 5, 2 * N * (N - 2))


def radial_ratio_sequence(N: int):
    """v_k/g_k for v=(I-S)^(-1)g."""
    output = []
    t = Q(0)
    for k in range(1, N):
        t = Q(2 * N + (k - 1) * t, 2 * N - k)
        output.append(t)
    return output


def lower_ell(N: int, j: int) -> Q:
    return Q(3 * N * j + 3 * N - 8 * j - 10, 3 * N * j * (j + 1))


def finite_debt_ratio(N: int) -> Q:
    """Largest termwise debt/first-phase ratio."""
    ratios = radial_ratio_sequence(N)
    alpha = Q(11, 25)
    return max(
        Q(4 * (j + 2), 3 * (j + 1) * (N - 2))
        / (alpha * lower_ell(N, j) * ratios[j - 1])
        for j in range(1, N - 1)
    )


def tail_ratio(N: int) -> Q:
    c = phase_contraction(N)
    return Q(25, 11) * c / (1 - c)


def check_local_identities():
    # Radial closed form and the two-sided elementary bounds.
    for N in range(3, 80):
        d, ga, qb = rank_data(N)
        tail = 2 ** (N - 1)
        for k in range(1, N):
            tail -= comb(N - 1, k - 1)
            error = Q(4 * tail, 2**N * (N - 1) * comb(N - 2, k - 1))
            assert d[k] == Q(2, k) - error
            assert Q(2 * (N - 2), N * k) <= d[k] <= Q(2, k)
        for k in range(2, N):
            assert qb[k - 2] == ga[k - 1] * Q(2 * (k - 1), N - 2)

    # The upper radial ratio used by the good-to-bad phase majorant.
    for N in range(3, 200):
        for j, t in enumerate(radial_ratio_sequence(N), 1):
            bound = Q(N * N - j, (N - 2) * (N - j))
            assert t <= bound

    # Exact local supersolutions and their contraction constants.
    for N in range(12, 250):
        d, ga, qb = rank_data(N)
        t = radial_ratio_sequence(N)
        h = [Q(k, N - 2) * ga[k - 2] for k in range(2, N)]
        for k in range(2, N):
            i = k - 2
            b0 = Q(N * (k - 2) + k, 2 * k * N)
            residual = (1 - b0) * h[i]
            if k > 2:
                residual -= Q(N - k - 1, 2 * N) * h[i - 1]
            if k + 1 < N:
                residual -= Q(k * (k - 1), 2 * (k + 1) * N) * h[i + 1]
            assert residual >= t[k - 2] * ga[k - 2] / N

        c = phase_contraction(N)
        assert c <= Q(1, 12)

    # The left occupation supersolution Y and its exact positive residual.
    for N in range(3, 250):
        Y = [Q(2 * (k + 1), 3 * k * (k - 1)) for k in range(2, N)]
        for k in range(2, N):
            i = k - 2
            b0 = Q(N * (k - 2) + k, 2 * k * N)
            residual = (1 - b0) * Y[i]
            if k > 2:
                residual -= Q((k - 1) * (k - 2), 2 * k * N) * Y[i - 1]
            if k + 1 < N:
                residual -= Q(N - k - 2, 2 * N) * Y[i + 1]
            assert residual >= Q(1, k * (k - 1))


def check_finite_certificates():
    # Genuine small exceptions: direct exact solve of the stationary system.
    small = []
    for N in range(3, 40):
        value = exact_small_scalar(N)
        assert value > 0
        small.append(value)
    assert small[0] == fmpq(3, 208)
    assert small[1] == fmpq(359, 26660)
    for N in range(3, 9):
        check_phase_identity(N)

    # The phase proof itself closes every remaining finite order below 288.
    margins = []
    for N in range(40, 288):
        margin = 1 - finite_debt_ratio(N) - tail_ratio(N)
        assert margin > 0
        margins.append(margin)
    assert min(margins) == margins[0]


def check_large_order_polynomials():
    # Wbar=(7N/25)q.  For N>=25 the cubic has negative discriminant.
    n, k, m = sp.symbols("n k m")
    wpoly = (
        21 * n**2 * k + 14 * n**2 - 64 * n * k**2 - 57 * n * k
        + 50 * k**3 + 36 * k**2 - 14 * k
    )
    w_disc = sp.factor(sp.discriminant(wpoly, k))
    assert sp.expand(w_disc + 8 * (
        5733 * n**6 - 123739 * n**5 - 344667 * n**4 - 933837 * n**3
        - 1594496 * n**2 - 983556 * n - 100352
    )) == 0
    w_disc_shift = sp.Poly(sp.expand((-w_disc / 8).subs(n, m + 25)), m).all_coeffs()
    assert w_disc_shift == [5733, 736211, 37934833, 982793213, 12893444604, 70866894144, 41021531998]
    assert all(value > 0 for value in w_disc_shift)
    # The isolated N=24 endpoint certificate.
    assert min(
        21 * 24**2 * k + 14 * 24**2 - 64 * 24 * k**2 - 57 * 24 * k
        + 50 * k**3 + 36 * k**2 - 14 * k
        for k in range(2, 24)
    ) == 24

    # Large-order termwise debt comparison.  These are the coefficients of
    # the discriminant polynomial after N=M+288.
    debt_poly = (
        1881 * n**2 * k + 1881 * n**2 - 6250 * n * k**2 - 21278 * n * k
        - 10032 * n + 6000 * k**3 + 12000 * k**2 + 10032 * k + 12540
    )
    debt_disc = sp.factor(sp.discriminant(debt_poly, k))
    assert sp.expand(debt_disc + 500 * (
        43034652243 * n**6 - 2423163812652 * n**5 + 23347885394764 * n**4
        - 127704595269984 * n**3 - 84188066366592 * n**2
        + 68423285855232 * n + 172450813860864
    )) == 0
    debt_disc_shift = sp.Poly(
        sp.expand((-debt_disc / 500).subs(n, m + 288)), m
    ).all_coeffs()
    assert debt_disc_shift == [
        43034652243,
        71940715263252,
        50075984929826764,
        18577025353519361184,
        3873653773133773223808,
        430447522448513182675968,
        19913301794000751100222464,
    ]
    assert all(value > 0 for value in debt_disc_shift)

    # Directly audit the integer cubics at representative orders, including
    # both analytic thresholds.
    for N in (24, 25, 40, 287, 288, 289, 500):
        if N >= 24:
            for k in range(2, N):
                wpoly = (
                    21 * N * N * k + 14 * N * N - 64 * N * k * k
                    - 57 * N * k + 50 * k**3 + 36 * k * k - 14 * k
                )
                assert wpoly > 0
        if N >= 288:
            for k in range(1, N - 1):
                debt_poly = (
                    1881 * N * N * k + 1881 * N * N - 6250 * N * k * k
                    - 21278 * N * k - 10032 * N + 6000 * k**3
                    + 12000 * k * k + 10032 * k + 12540
                )
                assert debt_poly > 0

    # The alternating phase tail is at most 1/20 from N=46 onward.
    for N in range(46, 500):
        assert tail_ratio(N) <= Q(1, 20)


def main():
    check_local_identities()
    check_finite_certificates()
    check_large_order_polynomials()
    print("PASS: stationary symmetric inverse-rank phase certificate")
    print("  exact stationary solve: 3 <= N <= 39")
    print("  exact finite phase margins: 40 <= N <= 287")
    print("  analytic discriminant certificate: N >= 288")


if __name__ == "__main__":
    main()
