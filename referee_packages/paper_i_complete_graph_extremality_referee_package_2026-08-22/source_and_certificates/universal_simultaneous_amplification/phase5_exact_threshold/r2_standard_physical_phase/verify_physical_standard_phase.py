#!/usr/bin/env python3
"""Independent exact verifier for the physical standard-sector phase theorem.

This file deliberately imports no discovery code.  It reconstructs the signed
P/Q/R quotient, the physical two-feature operator, the radial Poisson reward,
the Schur complement, and every algebraic certificate used in
``PHYSICAL_STANDARD_PHASE_THEOREM.md``.  All arithmetic is exact SymPy integer
or rational arithmetic.
"""

from __future__ import annotations

from math import comb

import sympy as sp


def rat(p: int, q: int = 1) -> sp.Rational:
    return sp.Rational(p, q)


def nonnegative(vector: sp.Matrix) -> bool:
    return all(value >= 0 for value in vector)


def positive(vector: sp.Matrix) -> bool:
    return all(value > 0 for value in vector)


def radial_gradient(N: int) -> list[sp.Rational]:
    """Solve (N-k)d_k-(k-1)d_(k-1)=2N(1/k-c0)."""

    c0 = rat(2**N - 1, N * 2 ** (N - 1))
    d = [rat(0) for _ in range(N + 1)]
    for k in range(1, N):
        d[k] = sp.cancel(
            (2 * N * (rat(1, k) - c0) + (k - 1) * d[k - 1]) / (N - k)
        )
    assert sp.cancel(-(N - 1) * d[N - 1] - 2 * N * (rat(1, N) - c0)) == 0
    return d


def radial_audit(N: int) -> None:
    d = radial_gradient(N)
    for k in range(1, N):
        tail = sum(comb(N - 1, r) for r in range(k, N))
        closed_defect = rat(4 * tail, 2**N * (N - 1) * comb(N - 2, k - 1))
        assert sp.cancel(rat(2, k) - d[k] - closed_defect) == 0
        assert d[k] <= rat(2, k)
        assert d[k] >= rat(2 * (N - 2), N * k)


def signed_quotient(N: int):
    """Return H,S,C,D,Q and channel indices in the theorem's orientation."""

    good = [("P", k) for k in range(1, N)] + [("R", k) for k in range(1, N)]
    bad = [("Q", k) for k in range(1, N + 1)]
    channels = good + bad
    index = {channel: j for j, channel in enumerate(channels)}
    H = sp.zeros(len(channels))

    def add(row, channel, value):
        if channel in index and value:
            H[index[row], index[channel]] += value

    for k in range(1, N):
        row = ("P", k)
        add(row, ("P", k), rat(k, 2 * N))
        add(row, ("P", k + 1), rat(N - k - 1, 2 * N))
        add(row, ("Q", k + 1), rat(1, 2 * N))

    for k in range(1, N + 1):
        row = ("Q", k)
        add(row, ("Q", k), rat(k * k - 1, 2 * k * N))
        add(row, ("Q", k + 1), rat(N - k, 2 * N))
        add(row, ("P", k - 1), -rat(k - 1, 2 * k * N))
        add(row, ("P", k), -rat(N - k, 2 * k * N))
        add(row, ("R", k - 1), -rat((k - 1) ** 2, 2 * k * N))
        add(row, ("R", k), -rat((k - 1) * (N - k), 2 * k * N))

    for k in range(1, N):
        row = ("R", k)
        add(
            row,
            ("R", k),
            rat(k, 2 * N) + rat((k - 1) * (N - k), 2 * k * N),
        )
        add(row, ("R", k + 1), rat(N - k - 1, 2 * N))
        add(row, ("R", k - 1), rat((k - 1) ** 2, 2 * k * N))
        add(row, ("Q", k), rat(1, 2 * k * N))
        add(row, ("P", k - 1), rat(k - 1, 2 * k * N))
        add(row, ("P", k), rat(N - k, 2 * k * N))

    g = len(good)
    S = H[:g, :g]
    C = H[:g, g:]
    D = -H[g:, :g]
    Q = H[g:, g:]
    assert nonnegative(S) and nonnegative(C) and nonnegative(D) and nonnegative(Q)
    return H, S, C, D, Q, good, bad, index


def physical_reward(N: int, good, bad):
    d = radial_gradient(N)
    q = sp.zeros(N, 1)
    for k in range(1, N + 1):
        q[k - 1] = (N - k) * d[k] + rat((N + 1) * (k - 1), k) * d[k - 1]
    gamma_s = sp.zeros(len(good), 1)
    for j, (kind, k) in enumerate(good):
        if kind == "P":
            gamma_s[j] = k * d[k]
        else:
            gamma_s[j] = N * d[k] + rat((N + 1) * (k - 1), k) * d[k - 1]
    gamma = gamma_s.col_join(-q)
    assert positive(q)
    return d, q, gamma_s, gamma


def phase_source(N: int, good, bad) -> sp.Matrix:
    sigma = sp.zeros(1, len(good) + len(bad))
    for j, (kind, k) in enumerate(good):
        if kind == "R":
            sigma[j] = rat(comb(N - 2, k - 1), 2 ** (N - 2))
    assert sum(sigma) == 1
    return sigma


def schur_data(N: int):
    H, S, C, D, Q, good, bad, _index = signed_quotient(N)
    _d, q, gamma_s, gamma = physical_reward(N, good, bad)
    sigma = phase_source(N, good, bad)
    g = len(good)
    sigma_s = sigma[:, :g]
    RS = (sp.eye(g) - S).inv()
    RQ = (sp.eye(N) - Q).inv()
    h = RQ * q
    r0 = gamma_s - C * h
    f0 = RS * r0
    A = RS * C * RQ * D
    direct = (sigma * (sp.eye(H.rows) - H).inv() * gamma)[0]
    reduced = (sigma_s * (sp.eye(g) + A).inv() * f0)[0]
    assert sp.cancel(direct - reduced) == 0
    return sp.cancel(direct), (H, S, C, D, Q, good, bad, sigma_s, q, gamma_s, RS, RQ, h, r0, f0, A)


def standard_step(N: int, a: list[sp.Rational], b: list[sp.Rational]):
    """Physical complete two-feature recurrence, with a_N retained as zero."""

    ap = [rat(0) for _ in range(N + 1)]
    bp = [rat(0) for _ in range(N + 1)]
    for k in range(1, N + 1):
        ap[k] = rat(k, 2 * N) * a[k]
        if k < N:
            ap[k] += rat(N - k, 2 * N) * a[k + 1] - rat(1, 2 * N) * b[k + 1]

        bp[k] = rat(k, 2 * N) * b[k]
        if k < N:
            bp[k] += rat(N - k - 1, 2 * N) * b[k + 1]
        if k > 1:
            bp[k] += rat(k - 1, 2 * k * N) * a[k - 1]
            bp[k] += rat((k - 1) ** 2, 2 * k * N) * b[k - 1]
        bp[k] += rat(N - k + 1, 2 * k * N) * a[k]
        bp[k] += rat(k * (N - k) - (N - k + 1), 2 * k * N) * b[k]
    return ap, bp


def physical_operator(N: int) -> sp.Matrix:
    """K on (a_1,...,a_(N-1),b_1,...,b_N), with a_N=0."""

    size = 2 * N - 1
    K = sp.zeros(size)
    for column in range(size):
        a = [rat(0) for _ in range(N + 1)]
        b = [rat(0) for _ in range(N + 1)]
        if column < N - 1:
            a[column + 1] = 1
        else:
            b[column - (N - 1) + 1] = 1
        ap, bp = standard_step(N, a, b)
        values = ap[1:N] + bp[1 : N + 1]
        for row, value in enumerate(values):
            K[row, column] = value
    return K


def normalization_audit(N: int) -> None:
    """Verify quotient conjugacy and both normalization constants exactly."""

    H, _S, _C, _D, _Q, good, bad, _index = signed_quotient(N)
    d, _q, _gamma_s, gamma = physical_reward(N, good, bad)
    sigma = phase_source(N, good, bad)
    K = physical_operator(N)
    size = 2 * N - 1

    # T(a,b)=(P=a,R=b,Q=a-b), with the physical gauge a_N=0.
    T = sp.zeros(H.rows, size)
    phase_index = {channel: j for j, channel in enumerate(good + bad)}
    for k in range(1, N):
        acol = k - 1
        bcol = (N - 1) + (k - 1)
        T[phase_index[("P", k)], acol] = 1
        T[phase_index[("R", k)], bcol] = 1
        T[phase_index[("Q", k)], acol] = 1
        T[phase_index[("Q", k)], bcol] = -1
    T[phase_index[("Q", N)], 2 * N - 2] = -1
    assert H * T == T * K

    n = N + 1
    source = sp.zeros(size, 1)
    for k in range(1, N):
        source[k - 1] = rat(k, 2 * n * (N - 1)) * d[k]
    for k in range(1, N + 1):
        value = rat(N, 2 * n * (N - 1)) * d[k]
        if k > 1:
            value += rat(k - 1, 2 * k * (N - 1)) * d[k - 1]
        source[(N - 1) + (k - 1)] = value
    source_scale = 2 * n * (N - 1)
    assert gamma == source_scale * T * source

    output = sp.zeros(1, size)
    for k in range(1, N + 1):
        pi = rat(comb(N - 1, k - 1), 2 ** (N - 1))
        output[0, (N - 1) + (k - 1)] = pi * rat(N - k, n * (N - 1))
    assert sigma * T == 2 * n * output

    phase_value = (sigma * (sp.eye(H.rows) - H).inv() * gamma)[0]
    physical_value = (output * (sp.eye(size) - K).inv() * source)[0]
    assert sp.cancel(phase_value - 4 * n * n * (N - 1) * physical_value) == 0


def symbolic_certificates() -> None:
    """Audit the all-order polynomial identities; signs are coefficientwise."""

    N, k, a, m = sp.symbols("N k a m", integer=True, positive=True)
    x, y, d1, d2 = sp.symbols("x y d1 d2", positive=True)

    # The two normalization factors are identities, not fitted constants.
    phase_weight = sp.binomial(N - 2, k - 1) / 2 ** (N - 2)
    physical_weight = sp.binomial(N - 1, k - 1) / 2 ** (N - 1)
    physical_weight *= (N - k) / (N - 1)
    assert sp.combsimp(phase_weight - 2 * physical_weight) == 0

    # Local symbolic conjugacy of the P and R rows.  Substituting
    # P=a, R=b, Q=a-b in the signed quotient gives the physical recurrence.
    ak, ak1, bk, bk1, akm1, bkm1 = sp.symbols(
        "ak ak1 bk bk1 akm1 bkm1"
    )
    phase_P = k * ak / (2 * N) + (N - k - 1) * ak1 / (2 * N)
    phase_P += (ak1 - bk1) / (2 * N)
    physical_P = k * ak / (2 * N) + (N - k) * ak1 / (2 * N) - bk1 / (2 * N)
    assert sp.expand(phase_P - physical_P) == 0
    phase_R = (k / (2 * N) + (k - 1) * (N - k) / (2 * k * N)) * bk
    phase_R += (N - k - 1) * bk1 / (2 * N)
    phase_R += (k - 1) ** 2 * bkm1 / (2 * k * N)
    phase_R += (ak - bk) / (2 * k * N)
    phase_R += (k - 1) * akm1 / (2 * k * N)
    phase_R += (N - k) * ak / (2 * k * N)
    physical_R = k * bk / (2 * N) + (N - k - 1) * bk1 / (2 * N)
    physical_R += (k - 1) * akm1 / (2 * k * N)
    physical_R += (k - 1) ** 2 * bkm1 / (2 * k * N)
    physical_R += (N - k + 1) * ak / (2 * k * N)
    physical_R += (k * (N - k) - (N - k + 1)) * bk / (2 * k * N)
    assert sp.expand(phase_R - physical_R) == 0

    # W residual, k=2, after the radial lower/upper bounds.
    W1_residual = 2 * N**2 * d1 - (N - 1) * d1 - (N - 1) * d1
    assert sp.factor(W1_residual - 2 * (N**2 - N + 1) * d1) == 0
    W2_residual = 2 * N * d1 - rat(3, 4) / N * (2 * N * d1)
    W2_residual -= (N - 2) / (2 * N) * (8 * N * d2 / 3)
    W2_residual -= (N - 2) * d2 + (N + 1) * d1 / 2
    expected_W2 = (3 * N - 4) * d1 / 2 - 7 * (N - 2) * d2 / 3
    assert sp.expand(W2_residual - expected_W2) == 0
    lower2 = (3 * N - 4) * rat(1, 2) * (2 * (N - 2) / N) - 7 * (N - 2) * rat(1, 3)
    assert sp.factor(lower2 - 2 * (N - 2) * (N - 6) / (3 * N)) == 0

    # Interior W residual A_k d_(k-1)-B_k d_k.
    Wk = 4 * N * (k - 1) * x / k
    Wnext = 4 * N * k * y / (k + 1)
    qk = (N - k) * y + (N + 1) * (k - 1) * x / k
    residual = Wk - (k * k - 1) * Wk / (2 * k * N) - (N - k) * Wnext / (2 * N) - qk
    Ak = (k - 1) * (3 * k * N - 2 * k * k - k + 2) / k**2
    Bk = (3 * k + 1) * (N - k) / (k + 1)
    assert sp.factor(residual - Ak * x + Bk * y) == 0

    P = 2 * N**2 * k + N * k**3 - 8 * N * k**2 - 5 * N * k + 2 * N
    P += 4 * k**3 + 6 * k**2 - 2 * k - 4
    radial_lower = sp.factor(Ak * 2 * (N - 2) / (N * (k - 1)) - Bk * 2 / k)
    assert sp.factor(radial_lower - 2 * P / (N * k**2 * (k + 1))) == 0
    shifted_P = a**4 + a**3 * m + 10 * a**3 + 5 * a**2 * m + 37 * a**2
    shifted_P += 60 * a + 2 * a * m * (m - 1) + 6 * m**2 - 22 * m + 32
    assert sp.expand(P.subs({N: a + m + 3, k: a + 3}) - shifted_P) == 0
    assert sp.discriminant(6 * m**2 - 22 * m + 32, m) == -284

    # The W comparison is used only for nonnegativity of r_0.
    p_reward_residual = k * y - (4 * N * k * y / (k + 1)) / (2 * N)
    assert sp.factor(p_reward_residual - k * (k - 1) * y / (k + 1)) == 0
    r_reward_residual = N * y + (N + 1) * (k - 1) * x / k
    r_reward_residual -= (4 * N * (k - 1) * x / k) / (2 * k * N)
    expected_r_reward = N * y + (k - 1) * (N + 1 - 2 / k) * x / k
    assert sp.factor(r_reward_residual - expected_r_reward) == 0

    # Bad exit/retention row sums and the separate constant lower barrier.
    bad_exit_sum = ((k - 1) + (N - k) + (k - 1) ** 2 + (k - 1) * (N - k)) / (2 * k * N)
    assert sp.factor(bad_exit_sum - (N - 1) / (2 * N)) == 0
    bad_row_sum = (k * k - 1) / (2 * k * N) + (N - k) / (2 * N)
    assert sp.factor(bad_row_sum - (rat(1, 2) - 1 / (2 * k * N))) == 0
    comparison_gap = (1 - bad_row_sum) - (N - 1) / (2 * N)
    assert sp.factor(comparison_gap - (k + 1) / (2 * k * N)) == 0
    constant_residual = 4 * N * (1 - bad_row_sum) - 2 * N
    assert sp.factor(constant_residual - 2 / k) == 0

    # For k>=2 the radial upper bounds give q_k<=2N with a visible margin.
    q_upper = 2 * (N - k) / k + 2 * (N + 1) / k
    assert sp.factor(2 * N - q_upper - 2 * ((N + 1) * (k - 2) + 1) / k) == 0

    # Re-entry z residual.  The P residual is constant; the R numerator is Z.
    p_residual = 1 / N - k / (2 * N**2) - (N - k - 1) / (2 * N**2) - 1 / (2 * N)
    assert sp.factor(p_residual - rat(1, 2) / N**2) == 0
    z = lambda j: 2 / (N + j)
    r_self = k / (2 * N) + (k - 1) * (N - k) / (2 * k * N)
    r_residual = z(k) - r_self * z(k)
    r_residual -= (N - k - 1) * z(k + 1) / (2 * N)
    r_residual -= (k - 1) ** 2 * z(k - 1) / (2 * k * N)
    r_residual -= (k - 1) / (2 * k * N**2)
    r_residual -= (N - k) / (2 * k * N**2)
    r_residual -= 1 / (2 * k * N)
    shifted_r = sp.factor(r_residual.subs({N: a + m + 1, k: a + 1}))
    numerator, denominator = sp.together(shifted_r).as_numer_denom()
    Z = 4 * a**4 + 14 * a**3 * m + 18 * a**3
    Z += 14 * a**2 * m**2 + 40 * a**2 * m + 30 * a**2
    Z += 4 * a * m**3 + 24 * a * m**2 + 36 * a * m + 20 * a
    Z += 3 * m**3 + 8 * m**2 + 9 * m + 4
    expected_denominator = 2 * (a + 1) * (a + m + 1) ** 2
    expected_denominator *= (2 * a + m + 1) * (2 * a + m + 2) * (2 * a + m + 3)
    assert sp.expand(numerator - Z) == 0
    assert sp.factor(denominator - expected_denominator) == 0
    assert all(coefficient > 0 for coefficient in sp.Poly(Z, a, m).coeffs())

    # Upper and lower first-phase scalar inequalities and the tail sum.
    upper_R_lhs = 2 * (2 * N**2 + 4 * N * k - 3 * N + 1) / (N * k)
    upper_R_reward = 2 * (2 * N + 1) / k
    assert sp.factor(upper_R_lhs - upper_R_reward - 2 * (4 * N * k - 4 * N + 1) / (N * k)) == 0
    lower_reward = 2 * (N - 2) / k + 2 * (N + 1) * (N - 2) / (N * k) - 2 / k
    assert sp.factor(lower_reward - (4 * N - 8 - 4 / N) / k) == 0
    lower_gap = 4 * N - 8 - 4 / N - (2 * k + N - 1)
    assert sp.factor(lower_gap - (3 * N - 7 - 2 * k - 4 / N)) == 0
    c = 2 / (N + 1)
    tail = sp.factor(2 * N - 8 * N * c / (1 - c))
    assert sp.factor(tail - 2 * N * (N - 9) / (N - 1)) == 0


def finite_barrier_audit(N: int) -> None:
    """Reconstruct every vector inequality directly at exact finite orders."""

    _phi, data = schur_data(N)
    _H, S, C, D, Q, good, _bad, sigma, q, gamma_s, RS, RQ, h, r0, f0, A = data
    d = radial_gradient(N)
    one_q = sp.ones(N, 1)
    one_s = sp.ones(len(good), 1)

    assert D * one_s == rat(N - 1, 2 * N) * one_q
    for k, value in enumerate(Q * one_q, start=1):
        assert value == rat(1, 2) - rat(1, 2 * k * N)
    assert nonnegative(one_q - RQ * D * one_s)

    W = sp.zeros(N, 1)
    W[0] = 2 * N * N * d[1]
    W[1] = 2 * N * d[1]
    for k in range(3, N + 1):
        W[k - 1] = rat(4 * N * (k - 1), k) * d[k - 1]
    assert nonnegative((sp.eye(N) - Q) * W - q)
    assert nonnegative(W - h)
    assert nonnegative(gamma_s - C * W)
    assert nonnegative(r0) and nonnegative(f0)

    z = sp.zeros(len(good), 1)
    for j, (kind, k) in enumerate(good):
        z[j] = rat(1, N) if kind == "P" else rat(2, N + k)
    assert positive((sp.eye(len(good)) - S) * z - C * one_q)
    contraction = rat(2, N + 1)
    assert nonnegative(contraction * one_s - A * one_s)

    u = sp.Matrix([4 if kind == "P" else 8 * N for kind, _k in good])
    assert nonnegative((sp.eye(len(good)) - S) * u - gamma_s)
    assert nonnegative(u - f0)

    assert nonnegative(2 * N * one_q - q)
    constant_bad = 4 * N * one_q
    assert nonnegative((sp.eye(N) - Q) * constant_bad - q)
    assert nonnegative(constant_bad - h)
    if N >= 7:
        ell = sp.Matrix([0 if kind == "P" else 2 * N for kind, _k in good])
        assert nonnegative(r0 - (sp.eye(len(good)) - S) * ell)
        assert nonnegative(f0 - ell)
        assert (sigma * f0)[0] >= 2 * N


EXPECTED = {
    2: rat(24, 11),
    3: rat(261, 40),
    4: rat(343400, 28657),
    5: rat(2268275, 128288),
    6: rat(5758562957, 248448224),
    7: rat(141339691089527, 4988552903680),
    8: rat(15468663676289, 466560376100),
    9: rat(19782952499295763, 524622207176704),
}


def main() -> None:
    symbolic_certificates()
    print("PASS (ALL N): shifted W and z polynomials, first-phase bounds, tail identity")

    for N in range(2, 13):
        radial_audit(N)
        normalization_audit(N)
    print("PASS (EXACT): radial formula and physical quotient normalization, N=2..12")

    for N in range(6, 16):
        finite_barrier_audit(N)
    print("PASS (EXACT): direct reconstruction of every barrier, N=6..15")

    for N, expected in EXPECTED.items():
        value, _data = schur_data(N)
        assert value == expected
        assert value > 0
        print(f"Phi_{N} = {value}")
    print("PASS (EXACT): physical Schur values N=2..9")


if __name__ == "__main__":
    main()
