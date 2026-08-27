#!/usr/bin/env python3
"""Clean-room exact checks reconstructed from the v1.2.6 manuscript.

This script imports no packet code and reads no packet certificates.  It uses
SymPy only for exact polynomial algebra, determinants, and algebraic numbers.
"""

from itertools import permutations, product

import sympy as sp


A, C, G, T = range(4)
NAMES = "ACGT"
HADAMARD = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)


def nz(expr):
    return sp.factor(expr) != 0


def positive(expr):
    sign = sp.sign(sp.simplify(expr))
    if sign not in (sp.S.One, 1):
        raise AssertionError(f"not positive: {expr!s}; sign={sign!s}; N={sp.N(expr, 30)!s}")


def transition_row(vec):
    return tuple(
        sp.expand(sum(HADAMARD[x][state] * vec[x] for x in range(4)) / 4)
        for state in range(4)
    )


def assert_stochastic(vec):
    assert vec[0] == 1
    for eigen in vec[1:]:
        positive(eigen)
        positive(1 - eigen)
    for entry in transition_row(vec):
        positive(entry)


def theta_fourier(E1, D2, D3, U, V, A2, B2, A3, B3, d2, d3):
    out = {}
    for x, y, z in product(range(4), repeat=3):
        if x ^ y ^ z:
            out[x, y, z] = sp.S.Zero
            continue
        core = (
            d2 * d3 * A2[y] * A3[z] * U[y ^ z]
            + d2 * (1 - d3) * A2[y] * B3[z] * U[y] * V[z]
            + (1 - d2) * d3 * B2[y] * A3[z] * V[y] * U[z]
            + (1 - d2) * (1 - d3) * B2[y] * B3[z] * V[y ^ z]
        )
        out[x, y, z] = sp.expand(E1[x] * D2[y] * D3[z] * core)
    return out


def symmetric_core(U, V, S, Tvec):
    return {
        (y, z): sp.expand(
            (
                S[y] * S[z] * U[y ^ z]
                + S[y] * Tvec[z] * U[y] * V[z]
                + Tvec[y] * S[z] * U[z] * V[y]
                + Tvec[y] * Tvec[z] * V[y ^ z]
            )
            / 4
        )
        for y, z in product(range(4), repeat=2)
    }


def star_fourier(alpha, beta, gamma):
    return {
        (x, y, z): (
            sp.expand(alpha[x] * beta[y] * gamma[z]) if not (x ^ y ^ z) else sp.S.Zero
        )
        for x, y, z in product(range(4), repeat=3)
    }


def inverse_fourier(q):
    return {
        (i, j, k): sp.expand(
            sum(
                HADAMARD[x][i] * HADAMARD[y][j] * HADAMARD[z][k] * q[x, y, z]
                for x, y, z in product(range(4), repeat=3)
            )
            / 64
        )
        for i, j, k in product(range(4), repeat=3)
    }


def transition_matrix(vec):
    row = transition_row(vec)
    return tuple(tuple(row[parent ^ child] for child in range(4)) for parent in range(4))


def displayed_pruning(root_leaf, root_u, U, V, A2, B2, A3, B3, D2, D3, d2, d3):
    """Ordinary-state pruning on the four literal retained rooted graphs."""
    matrices = [transition_matrix(edge) for edge in (root_leaf, root_u, U, V, A2, B2, A3, B3, D2, D3)]
    RK, RU, MU, MV, MA2, MB2, MA3, MB3, MD2, MD3 = matrices

    def retic_branch(parent_matrix, pendant_matrix, observed):
        return tuple(
            sp.expand(sum(parent_matrix[parent][retic] * pendant_matrix[retic][observed] for retic in range(4)))
            for parent in range(4)
        )

    out = {}
    for obs1, obs2, obs3 in product(range(4), repeat=3):
        total = 0
        for parent2, parent3 in product(("p", "q"), repeat=2):
            weight = (d2 if parent2 == "p" else 1 - d2) * (d3 if parent3 == "p" else 1 - d3)
            branches_p, branches_q = [], []
            (branches_p if parent2 == "p" else branches_q).append(retic_branch(MA2 if parent2 == "p" else MB2, MD2, obs2))
            (branches_p if parent3 == "p" else branches_q).append(retic_branch(MA3 if parent3 == "p" else MB3, MD3, obs3))
            like_p = tuple(sp.prod(branch[state] for branch in branches_p) for state in range(4))
            like_q = tuple(sp.prod(branch[state] for branch in branches_q) for state in range(4))
            like_u = tuple(
                sp.expand(sum(MU[u][p] * like_p[p] for p in range(4)) * sum(MV[u][q] * like_q[q] for q in range(4)))
                for u in range(4)
            )
            switching_prob = sp.expand(
                sum(
                    RK[root][obs1] * sum(RU[root][u] * like_u[u] for u in range(4))
                    for root in range(4)
                )
                / 4
            )
            total += weight * switching_prob
        out[obs1, obs2, obs3] = sp.expand(total)
    return out


def reduce_num(expr, generators):
    num, _ = sp.fraction(sp.cancel(expr))
    return sp.expand(generators.reduce(sp.Poly(num, *generators.gens).as_expr())[1])


def assert_dict_equal(left, right, reducer=sp.simplify):
    assert left.keys() == right.keys()
    for key in left:
        rem = reducer(left[key] - right[key])
        if rem != 0:
            raise AssertionError(f"mismatch at {key}: {rem}")


def exact_min(values):
    items = list(values.items())
    return min(items, key=lambda kv: float(sp.N(kv[1], 40)))


def k2p_simple_checks():
    eta = sp.sqrt(71)
    K = (1, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2))
    U = (1, sp.Rational(4, 5), sp.Rational(19, 30), sp.Rational(4, 5))
    V = (1, sp.Rational(7, 240), sp.Rational(239, 360), sp.Rational(7, 240))
    S = (1, sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(1, 4))
    Tv = (1, sp.Rational(1, 3), sp.Rational(1, 27), sp.Rational(1, 3))
    for edge in (K, U, V, S, Tv):
        assert_stochastic(edge)
    assert transition_row(K) == tuple(map(sp.Rational, (5, 1, 1, 1), (8, 8, 8, 8)))
    K2 = tuple(sp.expand(v * v) for v in K)
    assert transition_row(K2) == tuple(map(sp.Rational, (7, 3, 3, 3), (16, 16, 16, 16)))

    P = (1, sp.Rational(151, 36) / eta, sp.Rational(107, 162), sp.Rational(151, 36) / eta)
    R = (1, eta / 40, sp.Rational(31, 120), eta / 40)
    M = symmetric_core(U, V, S, Tv)
    for y, z in product(range(4), repeat=2):
        assert sp.simplify(M[y, z] - P[y ^ z] * R[y] * R[z]) == 0
    alpha = tuple(sp.expand(K[x] ** 2 * P[x]) for x in range(4))
    beta = tuple(sp.expand(K[x] * R[x]) for x in range(4))
    for edge in (alpha, beta):
        assert_stochastic(edge)

    qn = theta_fourier(K2, K, K, U, V, S, Tv, S, Tv, sp.Rational(1, 2), sp.Rational(1, 2))
    qt = star_fourier(alpha, beta, beta)
    assert_dict_equal(qn, qt)
    pn, pt = inverse_fourier(qn), inverse_fourier(qt)
    assert_dict_equal(pn, pt)
    pruned = displayed_pruning(K, K, U, V, S, Tv, S, Tv, K, K, sp.Rational(1, 2), sp.Rational(1, 2))
    assert_dict_equal(pruned, pt)
    min_key, min_value = exact_min(pn)
    assert sp.simplify(min_value - sp.Rational(1188799, 79626240)) == 0
    assert sp.simplify(sum(pn.values()) - 1) == 0
    for value in pn.values():
        positive(value)
    return {"minimum_pattern": "".join(NAMES[i] for i in min_key), "alpha": alpha, "beta": beta}


def k2p_rank_and_family_checks():
    K = (1, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2))
    U0 = (1, sp.Rational(4, 5), sp.Rational(19, 30), sp.Rational(4, 5))
    V0 = (1, sp.Rational(7, 240), sp.Rational(239, 360), sp.Rational(7, 240))
    S0 = (1, sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(1, 4))
    T0 = (1, sp.Rational(1, 3), sp.Rational(1, 27), sp.Rational(1, 3))
    vars_ = sp.symbols("rC rG uC uG vC vG a2C a2G b2C")
    rC, rG, uC, uG, vC, vG, a2C, a2G, b2C = vars_
    root1 = (1, rC, rG, rC)
    E1 = tuple(root1[i] * K[i] for i in range(4))
    U = (1, uC, uG, uC)
    V = (1, vC, vG, vC)
    A2 = (1, a2C, a2G, a2C)
    B2 = (1, b2C, T0[G], b2C)
    F = theta_fourier(E1, K, K, U, V, A2, B2, S0, T0, sp.Rational(1, 2), sp.Rational(1, 2))
    rows = [(A, C, C), (A, G, G), (C, A, C), (C, C, A), (C, G, T), (C, T, G), (G, A, G), (G, C, T), (G, G, A)]
    J = sp.Matrix([F[row] for row in rows]).jacobian(vars_)
    subs = {rC: K[C], rG: K[G], uC: U0[C], uG: U0[G], vC: V0[C], vG: V0[G], a2C: S0[C], a2G: S0[G], b2C: T0[C]}
    determinant = sp.factor(J.subs(subs).det())
    target = -sp.Rational(7**2 * 11**2 * 19 * 107 * 151**2 * 15013, 2**60 * 3**25 * 5**10)
    assert determinant == target

    u, v, w, x, a, b, c, d = sp.symbols("u v w x a b c d")
    MAC = (a * u + c * w) / 2
    MAG = (b * v + d * x) / 2
    MCC = (a**2 + 2 * a * c * u * w + c**2) / 4
    MGG = (b**2 + 2 * b * d * v * x + d**2) / 4
    MCG = (a * b * u + a * d * u * x + b * c * v * w + c * d * w) / 4
    MCT = (a**2 * v + 2 * a * c * u * w + c**2 * x) / 4
    equations = (MCG**2 - MAC**2 * MGG, MCT**2 * MGG - MAG**2 * MCC**2)
    family_jac = sp.factor(sp.Matrix(equations).jacobian((v, x)).det().subs({
        u: U0[C], v: U0[G], w: V0[C], x: V0[G], a: S0[C], b: S0[G], c: T0[C], d: T0[G]
    }))
    assert family_jac == sp.Rational(675554683609333, 194995116803358720000000)
    return determinant, family_jac


def fixed_order_counterexample_checks():
    def kv(s, g):
        return (1, sp.Rational(s), sp.Rational(g), sp.Rational(s))

    E1 = kv(sp.Rational(69, 100), sp.Rational(4, 5))
    U = kv(sp.Rational(53, 100), sp.Rational(23, 100))
    V = kv(sp.Rational(23, 50), sp.Rational(3, 20))
    A2 = kv(sp.Rational(9, 25), sp.Rational(89, 100))
    B2 = kv(sp.Rational(19, 50), sp.Rational(17, 50))
    A3 = kv(sp.Rational(9, 20), sp.Rational(21, 100))
    B3 = kv(sp.Rational(3, 25), sp.Rational(39, 50))
    D2 = kv(sp.Rational(17, 100), sp.Rational(19, 100))
    D3 = kv(sp.Rational(49, 100), sp.Rational(27, 100))
    for edge in (E1, U, V, A2, B2, A3, B3, D2, D3):
        assert_stochastic(edge)
    q = theta_fourier(E1, D2, D3, U, V, A2, B2, A3, B3, sp.Rational(3, 5), sp.Rational(11, 50))

    def q_for_order(pattern, order):
        old = [None, None, None]
        for new_pos, old_pos in enumerate(order):
            old[old_pos] = pattern[new_pos]
        return q[tuple(old)]

    def invariant(order):
        return sp.factor(
            q_for_order((A, G, G), order)
            * q_for_order((G, A, G), order)
            * q_for_order((C, C, A), order) ** 2
            - q_for_order((A, A, A), order)
            * q_for_order((G, G, A), order)
            * q_for_order((T, C, G), order) ** 2
        )

    vals = [invariant(order) for order in permutations(range(3))]
    assert all(value < 0 for value in vals), vals
    assert len(set(vals)) == 3
    assert all(vals.count(value) == 2 for value in set(vals))
    p = inverse_fourier(q)
    min_key, min_value = exact_min(p)
    assert min_value == sp.Rational(2920987217429243, 200000000000000000)
    for value in p.values():
        positive(value)
    return vals, "".join(NAMES[i] for i in min_key)


def k2p_continuous_time_checks():
    ell, tt = sp.symbols("ell tt")
    f = 634127002560 * ell**3 - 2160769703472 * ell**2 + 1746884136303 * ell - 169873318739
    lo = sp.Rational(1073231219980, 10**12)
    hi = sp.Rational(1073231219981, 10**12)
    assert sp.count_roots(f, lo, hi) == 1
    L = sp.CRootOf(f, 1)
    assert lo < L < hi
    tval = sp.sqrt(1423)
    v = sp.Rational(73394329, 14503216) * ell**2 - sp.Rational(1453474193, 248626560) * ell + sp.Rational(4133719, 3669120)
    x = -sp.Rational(366971645, 99450624) * ell**2 + sp.Rational(4259402513, 340973568) * ell - sp.Rational(42362455, 5031936)
    K = (1, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2))
    U = (1, sp.Rational(3, 4), v, sp.Rational(3, 4))
    V = (1, sp.Rational(1, 16), x, sp.Rational(1, 16))
    S = (1, sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(1, 5))
    Tv = (1, sp.Rational(7, 30), sp.Rational(1, 15), sp.Rational(7, 30))
    P = (1, sp.Rational(79, 4) * tt / 1423, sp.Rational(73394329, 4762633008) * ell**2 + sp.Rational(368713223407, 81645137280) * ell - sp.Rational(4985775401, 1204882560), sp.Rational(79, 4) * tt / 1423)
    R = (1, tt / 240, ell / 4, tt / 240)
    ideal = sp.groebner((f, tt**2 - 1423), ell, tt, order="lex", domain=sp.QQ)
    red = lambda expr: reduce_num(expr, ideal)
    M = symmetric_core(U, V, S, Tv)
    for y, z in product(range(4), repeat=2):
        assert red(M[y, z] - P[y ^ z] * R[y] * R[z]) == 0
    alpha = tuple(sp.expand(K[i] ** 2 * P[i]) for i in range(4))
    beta = tuple(sp.expand(K[i] * R[i]) for i in range(4))
    qn = theta_fourier(tuple(e**2 for e in K), K, K, U, V, S, Tv, S, Tv, sp.Rational(1, 2), sp.Rational(1, 2))
    qt = star_fourier(alpha, beta, beta)
    assert_dict_equal(qn, qt, red)

    algebraic_subs = {ell: L, tt: tval}
    for edge in (K, U, V, S, Tv, alpha, beta):
        edge_at = tuple(sp.simplify(sp.sympify(e).subs(algebraic_subs)) for e in edge)
        assert_stochastic(edge_at)
        s, g = edge_at[C], edge_at[G]
        positive(g - s**2)
    margins = []
    for edge in (K, U, V, S, Tv, alpha, beta):
        e = tuple(sp.simplify(sp.sympify(z).subs(algebraic_subs)) for z in edge)
        margins.append(sp.simplify(e[G] - e[C] ** 2))
    assert min(margins, key=lambda z: float(sp.N(z, 30))) == sp.Rational(11, 900)

    # Resolve the r3 reticulation through its p-parent, leaving the r2
    # reticulation in place.  This is the displayed child used in the
    # fixed-leaf-order diagnosis.
    child_q = {}
    for a0, b0, c0 in product(range(4), repeat=3):
        if a0 ^ b0 ^ c0:
            child_q[a0,b0,c0] = sp.S.Zero
        else:
            child_core = (S[b0] * S[c0] * U[b0 ^ c0] + Tv[b0] * S[c0] * V[b0] * U[c0]) / 2
            child_q[a0,b0,c0] = sp.expand(K[a0]**2 * K[b0] * K[c0] * child_core)

    def child_coordinate(pattern, order):
        old = [None, None, None]
        for new_pos, old_pos in enumerate(order):
            old[old_pos] = pattern[new_pos]
        return child_q[tuple(old)]

    def child_invariant(order):
        return sp.factor(
            child_coordinate((A,G,G),order)
            * child_coordinate((G,A,G),order)
            * child_coordinate((C,C,A),order)**2
            - child_coordinate((A,A,A),order)
            * child_coordinate((G,G,A),order)
            * child_coordinate((T,C,G),order)**2
        ).subs(ell,L)

    q123 = child_invariant((0,1,2))
    q132 = child_invariant((0,2,1))
    positive(q123 + sp.Rational(19200, 10**13))
    positive(-sp.Rational(19199, 10**13) - q123)
    positive(q132 - sp.Rational(34284, 10**13))
    positive(sp.Rational(34286, 10**13) - q132)

    p = inverse_fourier({key: sp.simplify(value.subs(algebraic_subs)) for key, value in qt.items()})
    min_key, pmin = exact_min(p)
    lower = sp.Rational(149867914232177, 10**16)
    upper = sp.Rational(149867914232311, 10**16)
    positive(pmin - lower)
    positive(upper - pmin)
    for value in p.values():
        positive(value)
    pruned_symbolic = displayed_pruning(K, K, U, V, S, Tv, S, Tv, K, K, sp.Rational(1,2), sp.Rational(1,2))
    inverse_symbolic = inverse_fourier(qt)
    assert_dict_equal(pruned_symbolic, inverse_symbolic, red)

    # Reconstruct the manuscript's selected rank-nine minor afresh.
    rC, rG, uC, uG, vC, vG, a2C, a2G, b2C = vars_ = sp.symbols("crC crG cuC cuG cvC cvG ca2C ca2G cb2C")
    root1 = (1, rC, rG, rC)
    E1 = tuple(root1[i] * K[i] for i in range(4))
    Uv = (1, uC, uG, uC)
    Vv = (1, vC, vG, vC)
    A2 = (1, a2C, a2G, a2C)
    B2 = (1, b2C, Tv[G], b2C)
    F = theta_fourier(E1, K, K, Uv, Vv, A2, B2, S, Tv, sp.Rational(1, 2), sp.Rational(1, 2))
    rows = [(A, C, C), (A, G, G), (C, A, C), (C, C, A), (C, G, T), (C, T, G), (G, A, G), (G, C, T), (G, G, A)]
    J = sp.Matrix([F[row] for row in rows]).jacobian(vars_)
    base = {rC: K[C], rG: K[G], uC: U[C], uG: U[G], vC: V[C], vG: V[G], a2C: S[C], a2G: S[G], b2C: Tv[C]}
    det = sp.cancel(J.subs(base).det())
    det_red = sp.rem(sp.Poly(sp.fraction(det)[0], ell), sp.Poly(f, ell)).as_expr() / sp.fraction(det)[1]
    det_at = sp.simplify(det_red.subs(ell, L))
    low_det = -sp.Rational(4129735, 10**28)
    high_det = -sp.Rational(4129729, 10**28)
    positive(det_at - low_det)
    positive(high_det - det_at)
    return L, pmin, det_at, "".join(NAMES[i] for i in min_key), q123, q132


def k3p_checks():
    h = sp.symbols("h")
    hrel = 5 * h**4 - 1
    H = 5 ** (-sp.Rational(1, 4))
    red = lambda expr: sp.rem(sp.Poly(sp.fraction(sp.cancel(expr))[0], h), sp.Poly(hrel, h)).as_expr()
    K = (1, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2))
    U = (1, h / 3, h, sp.Rational(1, 3))
    V = (1, h, h / 3, sp.Rational(1, 3))
    S = (1, 3 * h**2 / 4, sp.Rational(1, 4), sp.Rational(3, 10))
    Tv = (1, sp.Rational(1, 4), 3 * h**2 / 4, sp.Rational(3, 10))
    B = (1, h**2 / 2, h**2 / 2, h**2 / 2)
    P = (1, (5 * h**3 + h) / 4, (5 * h**3 + h) / 4, h**2)
    M = symmetric_core(U, V, S, Tv)
    for y, z in product(range(4), repeat=2):
        assert red(M[y, z] - P[y ^ z] * B[y] * B[z]) == 0
    alpha = (1, (5 * h**3 + h) / 16, (5 * h**3 + h) / 16, h**2 / 4)
    beta = (1, h**2 / 4, h**2 / 4, h**2 / 4)
    qn = theta_fourier(tuple(e**2 for e in K), K, K, U, V, S, Tv, S, Tv, sp.Rational(1, 2), sp.Rational(1, 2))
    qt = star_fourier(alpha, beta, beta)
    assert_dict_equal(qn, qt, red)
    at = tuple(sp.simplify(sp.sympify(z).subs(h, H)) for z in alpha)
    bt = tuple(sp.simplify(sp.sympify(z).subs(h, H)) for z in beta)
    for edge in (K, U, V, S, Tv, alpha, beta):
        assert_stochastic(tuple(sp.simplify(sp.sympify(z).subs(h, H)) for z in edge))
    assert len(set(tuple(sp.simplify(sp.sympify(z).subs(h, H)) for z in U[1:]))) == 3
    assert at[C] == at[G] and at[C] != at[T]
    assert bt[C] == bt[G] == bt[T]
    p = inverse_fourier({key: sp.simplify(value.subs(h, H)) for key, value in qt.items()})
    for value in p.values():
        positive(value)
    pruned = displayed_pruning(K, K, U, V, S, Tv, S, Tv, K, K, sp.Rational(1,2), sp.Rational(1,2))
    assert_dict_equal(pruned, inverse_fourier(qt), red)

    # Full rank and IFT linearization from the explicitly stated map.
    vars_ = sp.symbols("rC rG rT uG a2C a2G b2C b2G a3C a3G b3C b3G d2T d3T delta3")
    rC, rG, rT, uG, a2C, a2G, b2C, b2G, a3C, a3G, b3C, b3G, d2T, d3T, delta3 = vars_
    root1 = (1, rC, rG, rT)
    E1 = tuple(root1[i] * K[i] for i in range(4))
    Uv = (1, U[C], uG, U[T])
    A2 = (1, a2C, a2G, S[T])
    B2 = (1, b2C, b2G, Tv[T])
    A3 = (1, a3C, a3G, S[T])
    B3 = (1, b3C, b3G, Tv[T])
    D2 = (1, K[C], K[G], d2T)
    D3 = (1, K[C], K[G], d3T)
    F = theta_fourier(E1, D2, D3, Uv, V, A2, B2, A3, B3, sp.Rational(1, 2), delta3)
    rows = [(A,C,C),(A,G,G),(A,T,T),(C,A,C),(C,C,A),(C,G,T),(C,T,G),(G,A,G),(G,C,T),(G,G,A),(G,T,C),(T,A,T),(T,C,G),(T,G,C),(T,T,A)]
    J = sp.Matrix([F[row] for row in rows]).jacobian(vars_)
    base = {rC:K[C],rG:K[G],rT:K[T],uG:U[G],a2C:S[C],a2G:S[G],b2C:Tv[C],b2G:Tv[G],a3C:S[C],a3G:S[G],b3C:Tv[C],b3G:Tv[G],d2T:K[T],d3T:K[T],delta3:sp.Rational(1,2)}
    J0 = J.subs(base)
    det = sp.factor(J0.det())
    det_red = sp.factor(sp.rem(sp.Poly(sp.fraction(sp.cancel(det))[0], h), sp.Poly(hrel, h)).as_expr() / sp.fraction(sp.cancel(det))[1])
    target = h * (10 * h**2 + 1) / (2**61 * 3**4 * 5**14)
    assert red(det_red - target) == 0

    tangent = sp.Matrix([
        -sp.Rational(3,19)*h-sp.Rational(375,304)*h**3,
        -sp.Rational(621,152)*h+sp.Rational(1875,304)*h**3,
        0,
        -sp.Rational(6,19)+sp.Rational(60,19)*h**2,
        -sp.Rational(117,304)*h+sp.Rational(459,608)*h**3,
        -sp.Rational(75,608)*h-sp.Rational(195,304)*h**3,
        -sp.Rational(255,608)*h+sp.Rational(135,304)*h**3,
        sp.Rational(9,304)*h-sp.Rational(9,608)*h**3,
        -sp.Rational(117,304)*h+sp.Rational(459,608)*h**3,
        -sp.Rational(75,608)*h-sp.Rational(195,304)*h**3,
        -sp.Rational(255,608)*h+sp.Rational(135,304)*h**3,
        sp.Rational(9,304)*h-sp.Rational(9,608)*h**3,
        0,0,0,
    ])
    # Free columns: U_C and V_G, each increasing at unit speed.
    free_uc, free_vg = sp.symbols("free_uc free_vg")
    Ufree = (1, free_uc, uG, U[T])
    Vfree = (1, V[C], free_vg, V[T])
    Ffree = theta_fourier(E1, D2, D3, Ufree, Vfree, A2, B2, A3, B3, sp.Rational(1,2), delta3)
    Fcols = sp.Matrix([Ffree[row] for row in rows]).jacobian((free_uc, free_vg)).subs(base).subs({free_uc:U[C],free_vg:V[G]})
    residual = J0 * tangent + Fcols[:,0] + Fcols[:,1]
    assert all(red(item) == 0 for item in residual)

    margin1_derivative = sp.factor(1 - tangent[3] * U[T])
    assert red(margin1_derivative - (21 - 20*h**2)/19) == 0
    assert margin1_derivative.subs(h,H) > 0
    assert sp.S.One > 0
    # At the base, precisely the two advertised network CT margins vanish.
    all_edges = (K,U,V,S,Tv)
    zeros = []
    for ei, edge in enumerate(all_edges):
        edgeh = tuple(sp.simplify(sp.sympify(z).subs(h,H)) for z in edge)
        margins = (edgeh[C]-edgeh[G]*edgeh[T], edgeh[G]-edgeh[C]*edgeh[T], edgeh[T]-edgeh[C]*edgeh[G])
        for mi, margin in enumerate(margins):
            if sp.simplify(margin) == 0:
                zeros.append((ei,mi))
            else:
                positive(margin)
    assert zeros == [(1,0),(2,1)]
    for edge in (at,bt):
        for margin in (edge[C]-edge[G]*edge[T], edge[G]-edge[C]*edge[T], edge[T]-edge[C]*edge[G]):
            positive(margin)
    return det_red, margin1_derivative, exact_min(p)


def topology_and_dimension_checks():
    vertices = {"u", "p", "q", "r2", "r3"}
    core_edges = {frozenset(e) for e in (("u","p"),("u","q"),("p","r2"),("q","r2"),("p","r3"),("q","r3"))}
    def connected(without=None):
        remaining = vertices - ({without} if without else set())
        if not remaining:
            return True
        seen = {next(iter(remaining))}
        changed = True
        while changed:
            changed = False
            for edge in core_edges:
                ends = set(edge) - ({without} if without else set())
                if len(ends) == 2 and seen & ends and not ends <= seen:
                    seen |= ends
                    changed = True
        return seen == remaining
    assert connected() and all(connected(v) for v in vertices)
    assert len(core_edges) == 6 and len(vertices) == 5
    assert 20 - 9 + 6 == 17 and 20 - 9 == 11
    assert 29 - 15 + 9 == 23 and 29 - 15 == 14
    # In the compatible orientation, p and q each have exactly the two
    # reticulations as children, excluding tree-child status.
    children = {"p":{"r2","r3"}, "q":{"r2","r3"}}
    assert all(children[v] == {"r2","r3"} for v in ("p","q"))


def main():
    simple = k2p_simple_checks()
    k2p_det, family_det = k2p_rank_and_family_checks()
    fixed_vals, fixed_min = fixed_order_counterexample_checks()
    L, ct_min, ct_det, ct_min_key, q123, q132 = k2p_continuous_time_checks()
    k3p_det, margin_derivative, k3p_min = k3p_checks()
    topology_and_dimension_checks()
    print("INDEPENDENT MATHEMATICAL CHECKS PASSED")
    print(f"simple K2P minimum pattern: {simple['minimum_pattern']}")
    print(f"K2P rank determinant: {k2p_det}")
    print(f"symmetric-family Jacobian: {family_det}")
    print(f"fixed-order invariant values (three pairs): {sorted(set(fixed_vals))}")
    print(f"fixed-order minimum pattern: {fixed_min}")
    print(f"continuous-time root: {sp.N(L, 30)}")
    print(f"continuous-time minimum pattern/value: {ct_min_key} / {sp.N(ct_min, 30)}")
    print(f"continuous-time K2P rank determinant: {sp.N(ct_det, 30)}")
    print(f"displayed-child Q in orders 123/132: {sp.N(q123,20)} / {sp.N(q132,20)}")
    print(f"K3P rank determinant: {k3p_det}")
    print(f"first saturated-margin derivative: {margin_derivative}")
    print(f"K3P minimum pattern/value: {''.join(NAMES[i] for i in k3p_min[0])} / {sp.N(k3p_min[1],30)}")


if __name__ == "__main__":
    main()
