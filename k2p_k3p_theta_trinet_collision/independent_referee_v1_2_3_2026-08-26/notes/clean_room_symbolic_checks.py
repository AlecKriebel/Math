#!/usr/bin/env python3
"""Clean-room symbolic checks derived only from the manuscript equations.

This file deliberately imports no packet module and reads no packet certificate.
It reconstructs the compact K2P and quartic K3P factorizations, the selected
Jacobian minors, and the K3P fixed-output tangent identity with SymPy 1.14.
"""

from itertools import product

import sympy as sp


Q = sp.Rational
CHARS = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)


def core(U, V, A2, A3, B2, B3, d2, d3, y, z):
    x = y ^ z
    return sp.expand(
        d2 * d3 * A2[y] * A3[z] * U[x]
        + d2 * (1 - d3) * A2[y] * B3[z] * U[y] * V[z]
        + (1 - d2) * d3 * B2[y] * A3[z] * V[y] * U[z]
        + (1 - d2) * (1 - d3) * B2[y] * B3[z] * V[x]
    )


def theta_coordinate(E1, D2, D3, U, V, A2, A3, B2, B3, d2, d3, row):
    x, y, z = row
    if x ^ y ^ z:
        return sp.Integer(0)
    return sp.expand(
        E1[x] * D2[y] * D3[z]
        * core(U, V, A2, A3, B2, B3, d2, d3, y, z)
    )


def inverse_patterns(q):
    out = {}
    for states in product(range(4), repeat=3):
        value = 0
        for labels in product(range(4), repeat=3):
            sign = sp.prod(CHARS[label][state] for label, state in zip(labels, states))
            value += Q(sign, 64) * q[labels]
        out[states] = sp.simplify(value)
    return out


def transition_kernel(eigen):
    one, c, g, t = eigen
    return (
        (one + c + g + t) / 4,
        (one + c - g - t) / 4,
        (one - c + g - t) / 4,
        (one - c - g + t) / 4,
    )


def direct_theta_patterns(K, U, V, S, T):
    """Ordinary-state pruning on the four literal retained-edge graphs."""
    nodes = ("rho", "u", "p", "q", "r2", "r3", "1", "2", "3")
    arcs = (
        ("rho", "1", K, "rho_1"), ("rho", "u", K, "rho_u"),
        ("u", "p", U, "u_p"), ("u", "q", V, "u_q"),
        ("p", "r2", S, "p_r2"), ("q", "r2", T, "q_r2"),
        ("p", "r3", S, "p_r3"), ("q", "r3", T, "q_r3"),
        ("r2", "2", K, "r2_2"), ("r3", "3", K, "r3_3"),
    )
    topological = ("rho", "u", "q", "p", "r3", "r2", "3", "2", "1")
    probabilities = {}
    for pattern in product(range(4), repeat=3):
        mixture = 0
        for parent2, parent3 in product(("p", "q"), repeat=2):
            kept = [arc for arc in arcs
                    if not (arc[1] == "r2" and arc[0] != parent2)
                    and not (arc[1] == "r3" and arc[0] != parent3)]
            children = {node: [] for node in nodes}
            for parent, child, eigen, edge_id in kept:
                children[parent].append((child, transition_kernel(eigen), edge_id))
            likelihood = {}
            observed = {"1": pattern[0], "2": pattern[1], "3": pattern[2]}
            for node in reversed(topological):
                if node in observed:
                    likelihood[node] = [sp.Integer(state == observed[node]) for state in range(4)]
                    continue
                values = [sp.Integer(1)] * 4
                for child, kernel, _ in children[node]:
                    contribution = [
                        sum(kernel[parent_state ^ child_state] * likelihood[child][child_state]
                            for child_state in range(4))
                        for parent_state in range(4)
                    ]
                    values = [sp.expand(a * b) for a, b in zip(values, contribution)]
                likelihood[node] = values
            mixture += sum(likelihood["rho"]) / 16  # root 1/4 and switching 1/4
        probabilities[pattern] = sp.simplify(mixture)
    return probabilities


def direct_star_patterns(alpha, beta, gamma):
    matrices = [transition_kernel(edge) for edge in (alpha, beta, gamma)]
    probabilities = {}
    for pattern in product(range(4), repeat=3):
        probabilities[pattern] = sp.simplify(sum(
            sp.prod(matrix[root ^ state] for matrix, state in zip(matrices, pattern))
            for root in range(4)
        ) / 4)
    return probabilities


def assert_positive(values, label):
    bad = [(key, sp.N(value, 40)) for key, value in values.items() if sp.N(value, 50) <= 0]
    assert not bad, f"{label} nonpositive values: {bad}"


def compact_k2p():
    eta = sp.sqrt(71)
    K = (1, Q(1, 2), Q(1, 2), Q(1, 2))
    U = (1, Q(4, 5), Q(19, 30), Q(4, 5))
    V = (1, Q(7, 240), Q(239, 360), Q(7, 240))
    S = (1, Q(1, 4), Q(1, 2), Q(1, 4))
    T = (1, Q(1, 3), Q(1, 27), Q(1, 3))
    P = (1, Q(151, 36) / eta, Q(107, 162), Q(151, 36) / eta)
    R = (1, eta / 40, Q(31, 120), eta / 40)

    M = {(y, z): core(U, V, S, S, T, T, Q(1, 2), Q(1, 2), y, z)
         for y, z in product(range(4), repeat=2)}
    for y, z in product(range(4), repeat=2):
        assert sp.simplify(M[y, z] - P[y ^ z] * R[y] * R[z]) == 0
    assert M[0, 1] == Q(151, 1440)
    assert M[1, 1] == Q(71, 1600)

    alpha = tuple(sp.simplify(K[i] ** 2 * P[i]) for i in range(4))
    beta = tuple(sp.simplify(K[i] * R[i]) for i in range(4))
    qn = {}
    qt = {}
    for labels in product(range(4), repeat=3):
        x, y, z = labels
        qn[labels] = (sp.simplify(K[x] ** 2 * K[y] * K[z] * M[y, z])
                      if not (x ^ y ^ z) else sp.Integer(0))
        qt[labels] = (sp.simplify(alpha[x] * beta[y] * beta[z])
                      if not (x ^ y ^ z) else sp.Integer(0))
        assert sp.simplify(qn[labels] - qt[labels]) == 0
    pp = inverse_patterns(qn)
    direct_network = direct_theta_patterns(K, U, V, S, T)
    direct_tree = direct_star_patterns(alpha, beta, beta)
    assert all(sp.simplify(pp[key] - direct_network[key]) == 0 for key in pp)
    assert all(sp.simplify(pp[key] - direct_tree[key]) == 0 for key in pp)
    assert_positive(pp, "compact K2P pattern")
    minimum = min(pp.values(), key=lambda value: float(sp.N(value, 50)))
    assert sp.simplify(minimum - Q(1188799, 79626240)) == 0
    assert sp.simplify(sum(pp.values()) - 1) == 0

    # Selected rank-nine minor from the manuscript, reconstructed by symbolic
    # differentiation of the four-switching map rather than from stored entries.
    rC, rG, uC, uG, vC, vG, a2C, a2G, b2C = sp.symbols(
        "rC rG uC uG vC vG a2C a2G b2C"
    )
    rho1 = (1, rC, rG, rC)
    E1 = tuple(rho1[i] * K[i] for i in range(4))
    UU = (1, uC, uG, uC)
    VV = (1, vC, vG, vC)
    AA2 = (1, a2C, a2G, a2C)
    BB2 = (1, b2C, T[2], b2C)
    rows = ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 1, 0), (1, 2, 3),
            (1, 3, 2), (2, 0, 2), (2, 1, 3), (2, 2, 0))
    columns = (rC, rG, uC, uG, vC, vG, a2C, a2G, b2C)
    expressions = [theta_coordinate(E1, K, K, UU, VV, AA2, S, BB2, T,
                                    Q(1, 2), Q(1, 2), row) for row in rows]
    substitution = {rC: K[1], rG: K[2], uC: U[1], uG: U[2],
                    vC: V[1], vG: V[2], a2C: S[1], a2G: S[2], b2C: T[1]}
    J = sp.Matrix([[sp.diff(expr, variable).subs(substitution)
                    for variable in columns] for expr in expressions])
    determinant = sp.factor(J.det())
    claimed = -Q(7**2 * 11**2 * 19 * 107 * 151**2 * 15013,
                 2**60 * 3**25 * 5**10)
    assert determinant == claimed

    print("compact K2P factorization, independent pruning, 64 coordinates, minimum, and rank-9 determinant: PASS")


def quartic_k3p():
    h = 5 ** (-Q(1, 4))
    K = (1, Q(1, 2), Q(1, 2), Q(1, 2))
    U0 = (1, h / 3, h, Q(1, 3))
    V0 = (1, h, h / 3, Q(1, 3))
    S0 = (1, 3 * h**2 / 4, Q(1, 4), Q(3, 10))
    T0 = (1, Q(1, 4), 3 * h**2 / 4, Q(3, 10))
    B = (1, h**2 / 2, h**2 / 2, h**2 / 2)
    P = (1, (5 * h**3 + h) / 4, (5 * h**3 + h) / 4, h**2)
    for y, z in product(range(4), repeat=2):
        value = core(U0, V0, S0, S0, T0, T0, Q(1, 2), Q(1, 2), y, z)
        assert sp.simplify(value - P[y ^ z] * B[y] * B[z]) == 0

    alpha = (1, (5 * h**3 + h) / 16, (5 * h**3 + h) / 16, h**2 / 4)
    beta = (1, h**2 / 4, h**2 / 4, h**2 / 4)
    qn = {}
    for labels in product(range(4), repeat=3):
        x, y, z = labels
        qn[labels] = (sp.simplify(K[x] ** 2 * K[y] * K[z]
                                  * core(U0, V0, S0, S0, T0, T0,
                                         Q(1, 2), Q(1, 2), y, z))
                      if not (x ^ y ^ z) else sp.Integer(0))
        tree = (sp.simplify(alpha[x] * beta[y] * beta[z])
                if not (x ^ y ^ z) else sp.Integer(0))
        assert sp.simplify(qn[labels] - tree) == 0
    pp = inverse_patterns(qn)
    direct_network = direct_theta_patterns(K, U0, V0, S0, T0)
    direct_tree = direct_star_patterns(alpha, beta, beta)
    assert all(sp.simplify(pp[key] - direct_network[key]) == 0 for key in pp)
    assert all(sp.simplify(pp[key] - direct_tree[key]) == 0 for key in pp)
    assert_positive(pp, "quartic K3P pattern")
    assert sp.simplify(sum(pp.values()) - 1) == 0

    # Full rank-15 minor and the two free coordinates used in the IFT argument.
    rC, rG, rT, uG = sp.symbols("rC rG rT uG")
    a2C, a2G, b2C, b2G, a3C, a3G, b3C, b3G = sp.symbols(
        "a2C a2G b2C b2G a3C a3G b3C b3G"
    )
    d2T, d3T, delta3, freeUC, freeVG = sp.symbols(
        "d2T d3T delta3 freeUC freeVG"
    )
    rho1 = (1, rC, rG, rT)
    E1 = tuple(rho1[i] * K[i] for i in range(4))
    UU = (1, freeUC, uG, Q(1, 3))
    VV = (1, h, freeVG, Q(1, 3))
    A2 = (1, a2C, a2G, Q(3, 10))
    A3 = (1, a3C, a3G, Q(3, 10))
    B2 = (1, b2C, b2G, Q(3, 10))
    B3 = (1, b3C, b3G, Q(3, 10))
    D2 = (1, Q(1, 2), Q(1, 2), d2T)
    D3 = (1, Q(1, 2), Q(1, 2), d3T)
    rows = tuple(row for row in product(range(4), repeat=3)
                 if not (row[0] ^ row[1] ^ row[2]) and row != (0, 0, 0))
    pivots = (rC, rG, rT, uG, a2C, a2G, b2C, b2G,
              a3C, a3G, b3C, b3G, d2T, d3T, delta3)
    expressions = [theta_coordinate(E1, D2, D3, UU, VV, A2, A3, B2, B3,
                                    Q(1, 2), delta3, row) for row in rows]
    base = {
        rC: K[1], rG: K[2], rT: K[3], uG: U0[2],
        a2C: S0[1], a2G: S0[2], b2C: T0[1], b2G: T0[2],
        a3C: S0[1], a3G: S0[2], b3C: T0[1], b3G: T0[2],
        d2T: K[3], d3T: K[3], delta3: Q(1, 2),
        freeUC: U0[1], freeVG: V0[2],
    }
    J = sp.Matrix([[sp.diff(expr, variable).subs(base) for variable in pivots]
                   for expr in expressions])
    determinant = sp.simplify(J.det())
    claimed = h * (10 * h**2 + 1) / (2**61 * 3**4 * 5**14)
    assert sp.simplify(determinant - claimed) == 0

    tangent = sp.Matrix((
        -Q(3, 19) * h - Q(375, 304) * h**3,
        -Q(621, 152) * h + Q(1875, 304) * h**3,
        0,
        -Q(6, 19) + Q(60, 19) * h**2,
        -Q(117, 304) * h + Q(459, 608) * h**3,
        -Q(75, 608) * h - Q(195, 304) * h**3,
        -Q(255, 608) * h + Q(135, 304) * h**3,
        Q(9, 304) * h - Q(9, 608) * h**3,
        -Q(117, 304) * h + Q(459, 608) * h**3,
        -Q(75, 608) * h - Q(195, 304) * h**3,
        -Q(255, 608) * h + Q(135, 304) * h**3,
        Q(9, 304) * h - Q(9, 608) * h**3,
        0, 0, 0,
    ))
    free_direction = sp.Matrix([
        (sp.diff(expr, freeUC) + sp.diff(expr, freeVG)).subs(base)
        for expr in expressions
    ])
    residual = J * tangent + free_direction
    assert all(sp.simplify(value) == 0 for value in residual)
    margin_u = sp.simplify(1 - tangent[3] / 3)
    assert sp.simplify(margin_u - (21 - 20 * h**2) / 19) == 0
    assert sp.N(margin_u, 40) > 0

    print("quartic K3P factorization, independent pruning, 64 coordinates, rank-15 determinant, and IFT tangent: PASS")


if __name__ == "__main__":
    compact_k2p()
    quartic_k3p()
    print("ALL CLEAN-ROOM SYMBOLIC CHECKS PASSED")
