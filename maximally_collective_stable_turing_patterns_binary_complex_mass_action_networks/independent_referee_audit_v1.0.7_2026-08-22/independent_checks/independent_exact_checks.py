#!/usr/bin/env python3
"""Independent exact/adversarial checks for the v1.0.7 referee audit.

This file deliberately imports no module from the submitted repository.  It
constructs the network from the displayed reaction list and re-derives the
objects tested below.
"""

from __future__ import annotations

from itertools import combinations
import json
import math
from pathlib import Path
import random

import numpy as np
import sympy as sp


Q = sp.Rational


def network(m: int):
    """Return (Y, Gamma) from the indexed reaction list, species X1..Xm,Z."""
    if m < 3:
        raise ValueError("m must be at least 3")
    n = m + 1
    reactions: list[tuple[list[int], list[int]]] = []

    def complex_(terms: dict[int, int]) -> list[int]:
        out = [0] * n
        for species, coefficient in terms.items():
            out[species] = coefficient
        return out

    reactions.append((complex_({}), complex_({0: 1})))
    for i_math in range(2, m - 1):
        reactions.append(
            (complex_({0: 1, i_math - 1: 1}),
             complex_({0: 1, i_math: 1}))
        )
    reactions.append(
        (complex_({0: 1, m - 2: 1}), complex_({m - 1: 2}))
    )
    reactions.append((complex_({m - 1: 2}), complex_({1: 1})))
    reactions.append((complex_({m: 2}), complex_({0: 1, m - 1: 1})))
    reactions.append((complex_({0: 1, m - 1: 1}), complex_({m: 2})))
    Y = sp.Matrix.hstack(*(sp.Matrix(src) for src, _ in reactions))
    Gamma = sp.Matrix.hstack(
        *(sp.Matrix(dst) - sp.Matrix(src) for src, dst in reactions)
    )
    assert Y.cols == m + 2
    assert all(sum(Y[:, j]) <= 2 for j in range(Y.cols))
    assert all(sum(Y[:, j] + Gamma[:, j]) <= 2 for j in range(Y.cols))
    return Y, Gamma


def jacobian_factor(m: int, a=Q(1), b=Q(1)) -> sp.Matrix:
    Y, Gamma = network(m)
    flux = [a] * m + [b, b]
    return Gamma * sp.diag(*flux) * Y.T


def conservation(m: int) -> sp.Matrix:
    return sp.Matrix([0] + [4] * (m - 2) + [2, 1])


def homogeneous_kernel(m: int) -> sp.Matrix:
    return sp.Matrix([2] + [-2] * (m - 2) + [0, 1])


def signed_minor(M: sp.Matrix, subset: tuple[int, ...]) -> sp.Expr:
    if not subset:
        return sp.Integer(1)
    block = M.extract(subset, subset)
    return sp.factor((-1) ** len(subset) * block.det())


def critical_data(m: int):
    K = lambda i: 91 * m - 181 - i
    r = [Q(1)]
    r += [-Q(K(i), 63 * (m - 2)) for i in range(2, m)]
    r += [-Q(2, 9), Q(5, 14)]
    d = [Q(23, 63)]
    d += [Q(1, K(i)) for i in range(2, m)]
    d += [Q(1, 7), Q(16, 45)]
    ell = [-Q(266, 815)]
    ell += [Q(78260 * (m - 2), 163 * (91 * m - 180 - i))
            for i in range(2, m)]
    ell += [Q(18368, 7335), Q(1)]
    return sp.Matrix(r), sp.diag(*d), sp.Matrix(ell)


def quadratic_B(m: int, u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    out = [sp.Integer(0)] * (m + 1)
    x1, xm1, xm, z = 0, m - 2, m - 1, m
    out[0] = -(u[x1] * v[xm1] + u[xm1] * v[x1]) + 2 * u[z] * v[z] \
        - (u[x1] * v[xm] + u[xm] * v[x1])
    out[1] = -(u[x1] * v[1] + u[1] * v[x1]) + 2 * u[xm] * v[xm]
    for i in range(2, m - 1):
        out[i] = u[x1] * v[i - 1] + u[i - 1] * v[x1] \
            - u[x1] * v[i] - u[i] * v[x1]
    out[xm] = 2 * (u[x1] * v[xm1] + u[xm1] * v[x1]) \
        - 4 * u[xm] * v[xm] + 2 * u[z] * v[z] \
        - (u[x1] * v[xm] + u[xm] * v[x1])
    out[z] = -4 * u[z] * v[z] + 2 * (u[x1] * v[xm] + u[xm] * v[x1])
    return sp.Matrix(out)


def printed_w0(m: int) -> sp.Matrix:
    vals = [Q(182448 * m - 373417, 31752 * (8 * m - 17))]
    w02 = Q(1008 * m * m - 20459 * m + 37138,
            31752 * (m - 2) * (8 * m - 17))
    vals += [w02 - Q(i - 2, 126 * (m - 2)) for i in range(2, m)]
    vals += [-Q(1, 81), Q(16861 * m - 34044, 7938 * (8 * m - 17))]
    return sp.Matrix(vals)


def reachability_sccs(A: sp.Matrix, subset: tuple[int, ...]):
    vertices = set(subset)
    edges = {j: {i for i in vertices if i != j and A[i, j] != 0}
             for j in vertices}

    def reachable(start: int):
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in edges[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    reaches = {v: reachable(v) for v in vertices}
    remaining = set(vertices)
    components = []
    while remaining:
        v = min(remaining)
        component = {w for w in remaining if w in reaches[v] and v in reaches[w]}
        components.append(tuple(sorted(component)))
        remaining -= component
    return components


def check_scc_exhaustion(m: int, b: sp.Rational):
    A = jacobian_factor(m, Q(1), b)
    n = m + 1
    allowed_cycles = {tuple(range(0, m - 1)), tuple(range(1, m))}
    boundary = {0, m - 1, m}
    failures = []
    for size in range(1, m):
        for subset in combinations(range(n), size):
            for component in reachability_sccs(A, subset):
                if len(component) == 1:
                    if A[component[0], component[0]] >= 0:
                        failures.append((subset, component, "nonnegative singleton"))
                elif component not in allowed_cycles and not set(component) <= boundary:
                    failures.append((subset, component, "unclassified SCC"))
    return failures


def polynomial_in_x_z_s(expr, x, y, s=None):
    variables = (x, y) if s is None else (x, y, s)
    poly = sp.Poly(sp.expand(expr), *variables)
    mapped = {}
    for powers, coefficient in poly.terms():
        y_power = powers[1]
        assert y_power % 2 == 0
        key = (powers[0], y_power // 2) if s is None else (
            powers[0], y_power // 2, powers[2]
        )
        mapped[key] = sp.factor(coefficient)
    return {key: value for key, value in mapped.items() if value != 0}


def modulus_certificates():
    x, y, s, A, U = sp.symbols("x y s A U", real=True)
    lam = x + sp.I * y

    def abs2(expr):
        return sp.expand(expr * sp.conjugate(expr))

    P = lam**4 + 12 * lam**3 + 42 * lam**2 + 47 * lam + 16
    R = 5 * lam**2 + 33 * lam + 16
    E35 = abs2(1 + lam) * abs2(P) - abs2(R)
    c35 = polynomial_in_x_z_s(E35, x, y)

    t = 1 + s
    g1 = lam + 2 + Q(23, 63) * t
    gm = lam + 5 + Q(1, 7) * t
    gz = lam + 4 + Q(16, 45) * t
    F = g1 * gm * gz - 4 * g1 - 4 * gm + gz
    G = gz * (4 * g1 + gm) - 36
    E77 = (Q(91, 90)**2 + y**2) * abs2(F) - abs2(G)
    c77 = polynomial_in_x_z_s(E77, x, y, s)
    E84 = Q(91, 90)**2 * (1 + A * x + y**2 / 3) * abs2(F) - abs2(G)
    c84 = polynomial_in_x_z_s(E84, x, y, s)

    F0 = lam**3 + 11 * lam**2 + 31 * lam + 16
    E22 = (1 + (U + Q(1, 4)) * x + Q(5, 4) * y**2) * abs2(F0) - abs2(R)
    c22 = polynomial_in_x_z_s(E22, x, y)

    def rational_positive(coeffs):
        return all(value.is_Rational and value > 0 for value in coeffs.values())

    def poly_nonnegative_in(parameter, coeffs, require_positive_at_positive=False):
        bad = []
        for key, coefficient in coeffs.items():
            p = sp.Poly(coefficient, parameter)
            if any(c < 0 for c in p.all_coeffs()):
                bad.append((key, coefficient, "negative parameter coefficient"))
            if require_positive_at_positive and coefficient == 0:
                bad.append((key, coefficient, "zero coefficient"))
        return bad

    def axes_present(coeffs, dimensions):
        axes = []
        for axis in range(dimensions):
            axes.append(any(key[axis] > 0 and sum(key[j] for j in range(dimensions) if j != axis) == 0
                            for key in coeffs))
        return axes

    return {
        "E35": {"terms": len(c35), "all_coefficients_strictly_positive": rational_positive(c35),
                "constant_absent": (0, 0) not in c35, "positive_pure_axes": axes_present(c35, 2)},
        "E77": {"terms": len(c77), "all_coefficients_strictly_positive": rational_positive(c77),
                "constant_absent": (0, 0, 0) not in c77, "positive_pure_axes": axes_present(c77, 3)},
        "E84": {"terms": len(c84), "parameter_coefficient_failures": poly_nonnegative_in(A, c84, True),
                "constant_absent": (0, 0, 0) not in c84, "positive_pure_axes": axes_present(c84, 3)},
        "E22": {"terms": len(c22), "parameter_coefficient_failures": poly_nonnegative_in(U, c22),
                "constant_absent": (0, 0) not in c22, "positive_pure_axes": axes_present(c22, 2)},
    }


def exact_checks():
    report = {"construction": {}, "scc": {}, "omission_minors": {},
              "critical_and_cubic": {}, "modulus_certificates": {}}
    for m in range(3, 8):
        Y, Gamma = network(m)
        c = conservation(m)
        rho = homogeneous_kernel(m)
        A = jacobian_factor(m, Q(2), Q(3))
        report["construction"][str(m)] = {
            "shape_Y": list(Y.shape),
            "shape_Gamma": list(Gamma.shape),
            "rank": Gamma.rank(),
            "left_conservation_zero": bool((c.T * Gamma).is_zero_matrix),
            "kernel_dimension": len(Gamma.nullspace()),
            "A_rho_zero": bool((A * rho).is_zero_matrix),
        }
        report["scc"][f"m{m}_generic"] = check_scc_exhaustion(m, Q(3))
        report["scc"][f"m{m}_b_eq_2a"] = check_scc_exhaustion(m, Q(2))

        h = [sp.Integer(i + 2) for i in range(m + 1)]
        J = A * sp.diag(*h)
        omissions = {}
        full = tuple(range(m + 1))
        for omitted in range(m + 1):
            kept = tuple(i for i in full if i != omitted)
            got = signed_minor(J, kept)
            prod_x = sp.prod(h[:m])
            if omitted == m:
                expected = -2 * Q(2) ** (m - 1) * Q(3) * prod_x
            elif 1 <= omitted <= m - 2:
                expected = 16 * Q(2) ** (m - 1) * Q(3) * h[m] * prod_x / h[omitted]
            else:
                expected = 0
            omissions[str(omitted)] = bool(sp.factor(got - expected) == 0)
        report["omission_minors"][str(m)] = omissions

        Aunit = jacobian_factor(m)
        r, D, ell = critical_data(m)
        Brr = quadratic_B(m, r, r)
        w0 = printed_w0(m)
        w2 = (Aunit - 4 * D).inv() * (-Brr / 4)
        numerator = sp.factor((ell.T * (quadratic_B(m, r, w0)
                              + quadratic_B(m, r, w2) / 2))[0])
        denominator = sp.factor((ell.T * r)[0])
        cubic = sp.factor(numerator / denominator)
        report["critical_and_cubic"][str(m)] = {
            "right_kernel": bool(((Aunit - D) * r).is_zero_matrix),
            "left_kernel": bool((ell.T * (Aunit - D)).is_zero_matrix),
            "ell_r_negative": bool(denominator < 0),
            "ell_D_r_negative": bool((ell.T * D * r)[0] < 0),
            "w0_equation": bool((Aunit * w0 + Brr / 4).is_zero_matrix),
            "w0_gauge": bool((conservation(m).T * w0)[0] == 0),
            "w2_equation": bool(((Aunit - 4 * D) * w2 + Brr / 4).is_zero_matrix),
            "cubic_numerator_positive": bool(numerator > 0),
            "cubic_negative": bool(cubic < 0),
            "cubic": str(cubic),
        }

    report["modulus_certificates"] = modulus_certificates()
    return report


def random_falsification(seed=20260822, trials=80):
    rng = random.Random(seed)
    failures = []
    worst_margin = math.inf
    cases = 0
    for m in range(3, 9):
        n = m + 1
        for trial in range(trials):
            a = 10 ** rng.uniform(-4, 4)
            b = 2 * a if trial == 0 else 10 ** rng.uniform(-4, 4)
            h = np.array([10 ** rng.uniform(-4, 4) for _ in range(n)])
            A = np.array(jacobian_factor(m, sp.Float(a), sp.Float(b)), dtype=float)
            J = A @ np.diag(h)
            for size in range(1, m):
                for subset in combinations(range(n), size):
                    eig = np.linalg.eigvals(J[np.ix_(subset, subset)])
                    margin = -float(np.max(eig.real))
                    scale = max(1.0, float(np.linalg.norm(J[np.ix_(subset, subset)], ord=np.inf)))
                    worst_margin = min(worst_margin, margin / scale)
                    cases += 1
                    if margin <= -1e-8 * scale:
                        failures.append({"m": m, "trial": trial, "subset": subset,
                                         "a": a, "b": b, "h": h.tolist(),
                                         "max_real": float(np.max(eig.real)), "scale": scale})
                        return {"cases": cases, "failures": failures,
                                "worst_normalized_hurwitz_margin": worst_margin}
            core_eig = np.linalg.eigvals(J[:m, :m])
            if not np.any(core_eig.real > 0):
                failures.append({"m": m, "trial": trial, "kind": "core no positive-real-part eigenvalue"})
                return {"cases": cases, "failures": failures,
                        "worst_normalized_hurwitz_margin": worst_margin}
    return {"cases": cases, "failures": failures,
            "worst_normalized_hurwitz_margin": worst_margin}


def scaled_spectral_falsification():
    cases = []
    for m in (3, 4, 5, 10, 149):
        nu = m - 2
        kappa = 1 / math.sqrt(3) if nu == 1 else math.sqrt(5) / 2
        endpoints = (kappa / math.sqrt(nu), 90 * nu / (90 * nu + 1))
        A = np.array(jacobian_factor(m), dtype=float)
        _, Dsym, _ = critical_data(m)
        D = np.array(Dsym, dtype=float)
        for label, L in zip(("L0", "L1"), endpoints):
            h = np.ones(m + 1)
            for i_math in range(2, m):
                Ki = 91 * m - 181 - i_math
                Kim1 = 91 * m - 181 - (i_math - 1)
                h[i_math - 1] = Ki / (L * Kim1)
            H = np.diag(h)
            row = {"m": m, "endpoint": label, "L": L}
            for t in (0, 1, 4, 9, 25):
                eig = np.linalg.eigvals(H @ (A - t * D))
                ordered = np.sort(eig.real)[::-1]
                if t == 0:
                    row[f"t{t}_largest"] = float(ordered[0])
                    row[f"t{t}_largest_nonzero"] = float(ordered[1])
                elif t == 1:
                    row[f"t{t}_largest"] = float(ordered[0])
                    row[f"t{t}_largest_noncritical"] = float(ordered[1])
                else:
                    row[f"t{t}_largest"] = float(ordered[0])
            dphys = h * np.diag(D)
            xstar = 1 / h
            row["chi_D_computed"] = float(dphys.max() / dphys.min())
            row["chi_H_computed"] = float(xstar.max() / xstar.min())
            row["contrast_product"] = row["chi_D_computed"] * row["chi_H_computed"]
            row["expected_product"] = 23 * (91 * nu - 1) / 63
            cases.append(row)
    return cases


def main():
    exact = exact_checks()
    random_result = random_falsification()
    scaled = scaled_spectral_falsification()
    payload = {"implementation_independence": "No submitted module imported",
               "arithmetic": {"exact_sections": ["construction", "scc", "omission_minors",
                                                    "critical_and_cubic", "modulus_certificates"],
                              "floating_sections": ["random_falsification", "scaled_spectral_falsification"]},
               "exact": exact, "random_falsification": random_result,
               "scaled_spectral_falsification": scaled}
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
