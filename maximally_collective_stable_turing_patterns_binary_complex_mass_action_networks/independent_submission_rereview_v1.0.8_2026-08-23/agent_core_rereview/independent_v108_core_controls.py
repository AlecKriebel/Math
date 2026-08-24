#!/usr/bin/env python3
"""Independent exact controls for the v1.0.8 core rereview.

The reaction matrices and Hessian contraction are reconstructed directly from
the indexed reaction list.  No project module, certificate, or verifier is
imported.  Claimed closed forms occur only on comparison sides.
"""

from __future__ import annotations

import itertools
import json

import sympy as sp


def reaction_matrices(m: int, a=sp.Integer(1), b=sp.Integer(1)):
    """Return (Y, Gamma, A) in manuscript reaction order."""
    assert m >= 3
    n = m + 1

    def vec(entries=None):
        out = [0] * n
        for index, value in (entries or {}).items():
            out[index] = value
        return out

    sources = [vec()]
    targets = [vec({0: 1})]

    for i in range(1, m - 2):  # X1+X_{i+1} -> X1+X_{i+2}
        sources.append(vec({0: 1, i: 1}))
        targets.append(vec({0: 1, i + 1: 1}))

    sources.extend(
        [
            vec({0: 1, m - 2: 1}),
            vec({m - 1: 2}),
            vec({m: 2}),
            vec({0: 1, m - 1: 1}),
        ]
    )
    targets.extend(
        [
            vec({m - 1: 2}),
            vec({1: 1}),
            vec({0: 1, m - 1: 1}),
            vec({m: 2}),
        ]
    )

    Y = sp.Matrix.hstack(*(sp.Matrix(column) for column in sources))
    target = sp.Matrix.hstack(*(sp.Matrix(column) for column in targets))
    gamma = target - Y
    fluxes = [a] * m + [b, b]
    assert len(fluxes) == Y.cols == m + 2
    A = sp.simplify(gamma * sp.diag(*fluxes) * Y.T)
    return Y, gamma, A, fluxes


def hessian_contraction(Y, gamma, fluxes, u, v):
    """Evaluate the mass-action Hessian B(u,v) at the unit equilibrium."""
    values = []
    for column in range(Y.cols):
        y = Y[:, column]
        yu = (y.T * u)[0]
        yv = (y.T * v)[0]
        diagonal_correction = sum(y[i] * u[i] * v[i] for i in range(Y.rows))
        values.append(fluxes[column] * (yu * yv - diagonal_correction))
    return sp.simplify(gamma * sp.Matrix(values))


def adjacency(A):
    return {
        j: {i for i in range(A.rows) if i != j and sp.simplify(A[i, j]) != 0}
        for j in range(A.cols)
    }


def strongly_connected_components(vertices, edges):
    vertices = set(vertices)

    def reachable(seed, reverse=False):
        seen = {seed}
        frontier = [seed]
        while frontier:
            current = frontier.pop()
            if reverse:
                next_vertices = {u for u in vertices if current in edges[u]}
            else:
                next_vertices = edges[current] & vertices
            for nxt in next_vertices - seen:
                seen.add(nxt)
                frontier.append(nxt)
        return seen

    components = []
    unused = set(vertices)
    while unused:
        seed = next(iter(unused))
        component = reachable(seed) & reachable(seed, reverse=True)
        components.append(frozenset(component))
        unused -= component
    return components


def check_scc_and_schur():
    a, b = sp.symbols("a b", positive=True)
    expected_schur = sp.Matrix(
        [
            [-(a + b), -a, -b],
            [-a, -a, 2 * a],
            [2 * a - b, 2 * a, -(4 * a + b)],
        ]
    )
    assert sp.factor(expected_schur.det()) == 2 * a**2 * b

    schur_dimensions = []
    for m in range(3, 9):
        _, _, A_symbolic, _ = reaction_matrices(m, a, b)
        core = A_symbolic[:m, :m]
        if m == 3:
            actual_schur = core
            interior_det = sp.Integer(1)
        else:
            boundary = [0, 1, m - 1]
            interior = list(range(2, m - 1))
            B = core.extract(boundary, boundary)
            C = core.extract(boundary, interior)
            E = core.extract(interior, interior)
            F = core.extract(interior, boundary)
            interior_det = sp.factor(E.det())
            assert interior_det == (-a) ** (m - 3)
            assert sp.factor(E.inv()[-1, 0]) == -1 / a
            actual_schur = sp.simplify(B - C * E.inv() * F)
        assert actual_schur.equals(expected_schur)
        assert sp.factor(core.det() - interior_det * expected_schur.det()) == 0
        schur_dimensions.append(m)

    exhaustive_records = []
    for m in range(3, 9):
        for label, avalue, bvalue in (
            ("generic", sp.Integer(3), sp.Integer(5)),
            ("b=2a", sp.Integer(3), sp.Integer(6)),
        ):
            _, _, A, _ = reaction_matrices(m, avalue, bvalue)
            edges = adjacency(A)
            cycle1 = frozenset(range(0, m - 1))
            cycle2 = frozenset(range(1, m))
            triad = frozenset((0, m - 1, m))
            sets_checked = 0
            for size in range(1, m):
                for retained in itertools.combinations(range(m + 1), size):
                    sets_checked += 1
                    for component in strongly_connected_components(retained, edges):
                        if len(component) == 1:
                            assert A[next(iter(component)), next(iter(component))] < 0
                        else:
                            assert component in (cycle1, cycle2) or component <= triad
            if label == "b=2a":
                assert A[m - 1, 0] == 0
                assert 0 not in edges[0]  # no self loops in the adjacency structure
                assert (m - 1) not in edges[0]  # X1 -> Xm is deleted
            exhaustive_records.append(
                {"m": m, "case": label, "retained_sets": sets_checked}
            )
    return {"schur_dimensions": schur_dimensions, "scc": exhaustive_records}


def K(m, i):
    return 91 * m - 181 - i


def critical_data(m):
    r = [sp.Integer(1)]
    r.extend(-sp.Rational(K(m, i), 63 * (m - 2)) for i in range(2, m))
    r.extend((sp.Rational(-2, 9), sp.Rational(5, 14)))

    d = [sp.Rational(23, 63)]
    d.extend(sp.Rational(1, K(m, i)) for i in range(2, m))
    d.extend((sp.Rational(1, 7), sp.Rational(16, 45)))

    ell = [sp.Rational(-266, 815)]
    ell.extend(
        sp.Rational(78260 * (m - 2), 163 * K(m, i - 1))
        for i in range(2, m)
    )
    ell.extend((sp.Rational(18368, 7335), sp.Integer(1)))
    return sp.Matrix(r), sp.diag(*d), sp.Matrix(ell)


def claimed_cubic_numerator(m):
    hfrak = sum(sp.Rational(1, K(m, j)) for j in range(1, m - 1))
    q = (
        589180301 * m**3
        - 3500015940 * m**2
        + 6930529579 * m
        - 4574434500
    )
    p_r = (
        68605040480814208768 * m**4
        - 550882186169626030957 * m**3
        + 1658612632937449670852 * m**2
        - 2219226476204103501323 * m
        + 1113379274975809565700
    )
    p_c = (
        652054120726848 * m**4
        - 5151971981328467 * m**3
        + 15265080924982572 * m**2
        - 20102347725659113 * m
        + 9927281930180400
    )
    R = sp.Rational(p_r, 286118780220 * (8 * m - 17) * q)
    C = -sp.Rational(215 * p_c, 11645046 * (8 * m - 17) * q)
    return sp.factor(R + C * hfrak)


def check_direct_cubic_contractions():
    records = []
    for m in (3, 4, 5, 8, 12):
        Y, gamma, A, fluxes = reaction_matrices(m)
        r, D, ell = critical_data(m)
        assert (A - D) * r == sp.zeros(m + 1, 1)
        assert (ell.T * (A - D)) == sp.zeros(1, m + 1)

        Brr = hessian_contraction(Y, gamma, fluxes, r, r)
        rhs = -Brr / 4
        c = sp.Matrix([0] + [4] * (m - 2) + [2, 1])
        right_zero = sp.Matrix([2] + [-2] * (m - 2) + [0, 1])
        augmented = A.row_join(right_zero).col_join(
            sp.Matrix([[*c.T, 0]])
        )
        solution = augmented.inv() * rhs.col_join(sp.Matrix([0]))
        w0 = solution[: m + 1, :]
        multiplier = solution[m + 1]
        assert multiplier == 0
        assert A * w0 == rhs
        assert (c.T * w0)[0] == 0

        w2 = (A - 4 * D).inv() * rhs
        assert (A - 4 * D) * w2 == rhs
        direct = sp.factor(
            (
                ell.T
                * (
                    hessian_contraction(Y, gamma, fluxes, r, w0)
                    + hessian_contraction(Y, gamma, fluxes, r, w2) / 2
                )
            )[0]
        )
        claimed = claimed_cubic_numerator(m)
        assert sp.factor(direct - claimed) == 0
        records.append(
            {
                "m": m,
                "numerator_positive": bool(direct > 0),
                "ell_r_negative": bool((ell.T * r)[0] < 0),
                "cubic_negative": bool(direct / (ell.T * r)[0] < 0),
                "numerator_digits": len(str(abs(int(sp.numer(direct))))),
            }
        )
    return records


def check_generic_sum_schema():
    """Verify independently the only dimension-dependent interior summation."""
    m, i = sp.symbols("m i", integer=True)
    count = m - 3
    origin = 91 * m - 181
    arithmetic_sum = (
        count * (origin**2 - origin)
        + (-2 * origin + 1) * count * (count - 1) / 2
        + count * (count - 1) * (2 * count - 1) / 6
    )
    printed = (m - 3) * (24571 * m**2 - 97470 * m + 96662) / 3
    assert sp.factor(arithmetic_sum - printed) == 0

    sigma = 1 / (sp.Integer(126) * (m - 2))
    denominator = sp.prod(K(m, j) for j in (-1, 0, 1, 2))
    Ti = sp.prod(K(m, i - 3 + j) for j in range(4)) / denominator
    Tiprev = sp.prod(K(m, i - 4 + j) for j in range(4)) / denominator
    W2 = sp.symbols("W2")
    wi = Ti * (W2 + sigma * K(m, 2) / 3) - sigma * K(m, i) / 3
    wprev = Tiprev * (W2 + sigma * K(m, 2) / 3) - sigma * K(m, i - 1) / 3
    assert sp.factor(wprev - (1 + 4 / K(m, i)) * wi - sigma) == 0
    return True


def check_shifted_cubic_sign_certificates():
    """Rebuild the all-dimensional sign argument from printed polynomials."""
    u = sp.symbols("u", nonnegative=True)
    m = u + 3
    q = (
        589180301 * m**3
        - 3500015940 * m**2
        + 6930529579 * m
        - 4574434500
    )
    p_r = (
        68605040480814208768 * m**4
        - 550882186169626030957 * m**3
        + 1658612632937449670852 * m**2
        - 2219226476204103501323 * m
        + 1113379274975809565700
    )
    p_c = (
        652054120726848 * m**4
        - 5151971981328467 * m**3
        + 15265080924982572 * m**2
        - 20102347725659113 * m
        + 9927281930180400
    )
    lower_numerator = (
        2729945147827667886720 * m**5
        - 27755132420474170999952 * m**4
        + 112813395868533457497683 * m**3
        - 229153280695458887386228 * m**2
        + 232620996871721820873517 * m
        - 94412163900120968220300
    )
    shifted = {}
    for name, polynomial in (
        ("Q", q),
        ("P_R", p_r),
        ("P_C", p_c),
        ("L", lower_numerator),
    ):
        coefficients = sp.Poly(sp.expand(polynomial), u).all_coeffs()
        assert coefficients and all(coefficient > 0 for coefficient in coefficients)
        shifted[name] = [int(coefficient) for coefficient in coefficients]

    # The harmonic estimate hfrak <= (m-2)/(90m-179) also proves ell^T r<0.
    ell_numerator_at_bound = sp.factor(
        7043400 * m
        - 13600927
        - 7043400 * (m - 2) / (90 * m - 179)
    )
    ell_num, ell_den = sp.fraction(ell_numerator_at_bound)
    assert all(c > 0 for c in sp.Poly(sp.expand(ell_num), u).all_coeffs())
    assert sp.Poly(sp.expand(ell_den), u).all_coeffs() == [90, 91]
    shifted["ell_lower_numerator"] = [
        int(coefficient)
        for coefficient in sp.Poly(sp.expand(ell_num), u).all_coeffs()
    ]
    return shifted


def main():
    result = {
        "scc_and_schur": check_scc_and_schur(),
        "direct_cubic": check_direct_cubic_contractions(),
        "generic_sum_and_recurrence": check_generic_sum_schema(),
        "shifted_cubic_sign_certificates": check_shifted_cubic_sign_certificates(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
