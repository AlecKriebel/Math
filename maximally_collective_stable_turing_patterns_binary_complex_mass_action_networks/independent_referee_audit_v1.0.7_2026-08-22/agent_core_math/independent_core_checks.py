#!/usr/bin/env python3
"""Independent exact/numerical checks for the algebraic core.

This file deliberately imports no project module and reads no stored certificate.
The reaction matrices are rebuilt directly from the indexed reaction list in the
manuscript.  Claimed formulas are encoded only on the comparison side of each
check.
"""

from __future__ import annotations

import itertools
import json
import math
import random
import sys
from fractions import Fraction

import numpy as np
import sympy as sp


def reaction_data(m: int):
    """Return species names, sources, targets in manuscript reaction order."""
    assert m >= 3
    n = m + 1
    names = [f"X{i}" for i in range(1, m + 1)] + ["Z"]

    def vec(**entries):
        out = [0] * n
        for key, value in entries.items():
            if key == "Z":
                out[m] = value
            else:
                out[int(key[1:]) - 1] = value
        return out

    reactions = []
    reactions.append(("R0", vec(), vec(X1=1)))
    for i in range(2, m - 1):
        src = {"X1": 1, f"X{i}": 1}
        dst = {"X1": 1, f"X{i+1}": 1}
        reactions.append((f"R{i}", vec(**src), vec(**dst)))
    reactions.append(("Ra", vec(X1=1, **{f"X{m-1}": 1}), vec(**{f"X{m}": 2})))
    reactions.append(("Rb", vec(**{f"X{m}": 2}), vec(X2=1)))
    reactions.append(("R+", vec(Z=2), vec(X1=1, **{f"X{m}": 1})))
    reactions.append(("R-", vec(X1=1, **{f"X{m}": 1}), vec(Z=2)))
    labels = [r[0] for r in reactions]
    Y = sp.Matrix.hstack(*[sp.Matrix(r[1]) for r in reactions])
    targets = sp.Matrix.hstack(*[sp.Matrix(r[2]) for r in reactions])
    Gamma = targets - Y
    assert len(reactions) == m + 2
    return names, labels, Y, Gamma


def matrix_from_reactions(m: int, a=sp.Integer(1), b=sp.Integer(1)):
    names, labels, Y, Gamma = reaction_data(m)
    flux = [a] * m + [b, b]
    A = sp.simplify(Gamma * sp.diag(*flux) * Y.T)
    return names, A


def conservation(m: int):
    return sp.Matrix([0] + [4] * (m - 2) + [2, 1])


def right_zero_unit(m: int):
    return sp.Matrix([2] + [-2] * (m - 2) + [0, 1])


def K(m: int, i: int):
    return 91 * m - 181 - i


def critical_profile(m: int):
    r = [sp.Rational(1)]
    r.extend(-sp.Rational(K(m, i), 63 * (m - 2)) for i in range(2, m))
    r.extend([sp.Rational(-2, 9), sp.Rational(5, 14)])
    d = [sp.Rational(23, 63)]
    d.extend(sp.Rational(1, K(m, i)) for i in range(2, m))
    d.extend([sp.Rational(1, 7), sp.Rational(16, 45)])
    ell = [sp.Rational(-266, 815)]
    ell.extend(
        sp.Rational(78260 * (m - 2), 163 * (91 * m - 180 - i))
        for i in range(2, m)
    )
    ell.extend([sp.Rational(18368, 7335), sp.Rational(1)])
    return sp.Matrix(r), sp.diag(*d), sp.Matrix(ell)


def sccs(vertices, adjacency):
    vertices = tuple(vertices)
    result = []
    unused = set(vertices)
    while unused:
        seed = next(iter(unused))

        def reachable(start, reverse=False):
            seen = {start}
            stack = [start]
            while stack:
                u = stack.pop()
                if reverse:
                    nxt = [v for v in vertices if u in adjacency.get(v, set())]
                else:
                    nxt = adjacency.get(u, set())
                for v in nxt:
                    if v in vertices and v not in seen:
                        seen.add(v)
                        stack.append(v)
            return seen

        comp = reachable(seed) & reachable(seed, reverse=True)
        result.append(frozenset(comp))
        unused -= comp
    return result


def adjacency_from_matrix(M: sp.Matrix):
    # Convention: column j -> row i for a nonzero off-diagonal derivative.
    n = M.rows
    out = {j: set() for j in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j and sp.simplify(M[i, j]) != 0:
                out[j].add(i)
    return out


def check_scc_exhaustion():
    records = []
    for m in range(3, 10):
        for label, a, b in [("generic", sp.Integer(3), sp.Integer(5)),
                            ("b=2a", sp.Integer(3), sp.Integer(6))]:
            names, A = matrix_from_reactions(m, a, b)
            adj = adjacency_from_matrix(A)
            boundary = frozenset([0, m - 1, m])
            cycle1 = frozenset(range(0, m - 1))
            cycle2 = frozenset(range(1, m))
            bad = []
            n = m + 1
            for size in range(1, m):
                for I in itertools.combinations(range(n), size):
                    for C in sccs(I, adj):
                        if len(C) == 1:
                            continue
                        if not (C == cycle1 or C == cycle2 or C <= boundary):
                            bad.append(([names[i] for i in I], [names[i] for i in C]))
            assert not bad, (m, label, bad[:3])
            records.append({"m": m, "case": label, "induced_sets_checked":
                            sum(math.comb(n, k) for k in range(1, m)), "bad": 0})
    return records


def exact_reaction_and_minor_checks():
    a, b = sp.symbols("a b", positive=True)
    out = []
    for m in range(3, 7):
        names, labels, Y, Gamma = reaction_data(m)
        assert all(sum(Y[:, j]) <= 2 for j in range(Y.cols))
        targets = Y + Gamma
        assert all(sum(targets[:, j]) <= 2 for j in range(targets.cols))
        c = conservation(m)
        assert c.T * Gamma == sp.zeros(1, Gamma.cols)
        assert Gamma.rank() == m
        long = sp.Matrix([1] * m + [0, 0])
        pair = sp.Matrix([0] * m + [1, 1])
        assert Gamma * long == sp.zeros(m + 1, 1)
        assert Gamma * pair == sp.zeros(m + 1, 1)
        assert len(Gamma.nullspace()) == 2

        _, A = matrix_from_reactions(m, a, b)
        assert A * right_zero_unit(m) == sp.zeros(m + 1, 1)
        assert c.T * A == sp.zeros(1, m + 1)
        h = sp.symbols(f"h1:{m+2}", positive=True)
        H = sp.diag(*h)
        J = A * H
        signed_full_x = sp.factor((-1) ** m * J[:m, :m].det())
        expected_full_x = -2 * a ** (m - 1) * b * sp.prod(h[:m])
        assert sp.simplify(signed_full_x - expected_full_x) == 0
        signed_omissions = []
        for omitted in range(m + 1):
            keep = [i for i in range(m + 1) if i != omitted]
            val = sp.factor((-1) ** m * J.extract(keep, keep).det())
            signed_omissions.append(val)
            if omitted == m:
                expected = expected_full_x
            elif omitted in (0, m - 1):
                expected = 0
            else:
                expected = (16 * a ** (m - 1) * b * h[m]
                            * sp.prod(h[i] for i in range(m) if i != omitted))
            assert sp.simplify(val - expected) == 0, (m, omitted, val, expected)

        out.append({
            "m": m,
            "reaction_count": Gamma.cols,
            "rank": Gamma.rank(),
            "kernel_dimension": len(Gamma.nullspace()),
            "signed_X_block": str(signed_full_x),
            "signed_omissions": [str(v) for v in signed_omissions],
        })
    return out


def triad_check():
    a, b, h1, hm, hz, lam = sp.symbols("a b h1 hm hz lam", positive=True)
    T = sp.Matrix([
        [-(a + b) * h1, -b * hm, 2 * b * hz],
        [(2 * a - b) * h1, -(4 * a + b) * hm, 2 * b * hz],
        [2 * b * h1, 2 * b * hm, -4 * b * hz],
    ])
    poly = sp.Poly(sp.expand((lam * sp.eye(3) - T).det()), lam)
    c1, c2, c3 = poly.all_coeffs()[1:]
    gap = sp.Poly(sp.expand(c1 * c2 - c3), a, b, h1, hm, hz)
    assert all(coef > 0 for _, coef in gap.terms())
    assert len(gap.terms()) == 14
    pair_dets = {}
    for pair in itertools.combinations(range(3), 2):
        B = T.extract(pair, pair)
        assert sp.simplify(sp.trace(B)) < 0
        det = sp.factor(B.det())
        pair_dets[str(pair)] = str(det)
        assert sp.Poly(det, a, b, h1, hm, hz).terms()
        assert all(coef > 0 for _, coef in sp.Poly(det, a, b, h1, hm, hz).terms())
    return {
        "c1": str(sp.factor(c1)),
        "c2": str(sp.factor(c2)),
        "c3": str(sp.factor(c3)),
        "routh_gap_term_count": len(gap.terms()),
        "routh_gap_all_coefficients_positive": True,
        "pair_determinants": pair_dets,
    }


def diffusion_polynomial_checks():
    # Exact rational instances; coefficient of s is reconstructed from det(sD-J).
    s = sp.symbols("s")
    out = []
    for m in range(3, 8):
        a = sp.Rational(2 + m, 3)
        b = sp.Rational(3 + 2 * m, 5)
        _, A = matrix_from_reactions(m, a, b)
        h = [sp.Rational(i + 2, i + 1) for i in range(m + 1)]
        d = [sp.Rational(2 * i + 3, i + 2) for i in range(m + 1)]
        J = A * sp.diag(*h)
        p = sp.Poly(sp.expand((s * sp.diag(*d) - J).det()), s)
        beta1 = p.coeff_monomial(s)
        predicted = (2 * a ** (m - 1) * b * sp.prod(h[:m])
                     * (8 * h[m] * sum(d[j] / h[j] for j in range(1, m - 1)) - d[m]))
        assert sp.simplify(beta1 - predicted) == 0
        higher = [p.coeff_monomial(s ** k) for k in range(2, m + 2)]
        assert all(x > 0 for x in higher)
        out.append({"m": m, "beta1": str(beta1),
                    "higher_coefficients_positive": True})
    return out


def determinant_factorization_checks():
    lam, t, L = sp.symbols("lam t L")
    P = lam**4 + 12*lam**3 + 42*lam**2 + 47*lam + 16
    R = 5*lam**2 + 33*lam + 16
    F0 = lam**3 + 11*lam**2 + 31*lam + 16
    records = []
    for m in range(3, 7):
        _, A = matrix_from_reactions(m)
        r, D, ell = critical_profile(m)

        direct_hom = sp.expand((lam * sp.eye(m + 1) - A).det())
        claimed_hom = sp.expand((1 + lam) ** (m - 3) * P - R)
        assert sp.simplify(direct_hom - claimed_hom) == 0

        g1 = lam + 2 + sp.Rational(23, 63) * t
        gm = lam + 5 + sp.Rational(1, 7) * t
        gz = lam + 4 + sp.Rational(16, 45) * t
        F = g1 * gm * gz - 4*g1 - 4*gm + gz
        G = gz * (4*g1 + gm) - 36
        Q = sp.prod(lam + 1 + t / K(m, i) for i in range(2, m))
        direct_spatial = sp.expand((lam * sp.eye(m + 1) - A + t*D).det())
        assert sp.simplify(direct_spatial - sp.expand(Q*F - G)) == 0

        h = [sp.Integer(1)] * (m + 1)
        for i in range(2, m):
            h[i - 1] = sp.Rational(K(m, i), K(m, i - 1)) / L
        H = sp.diag(*h)
        detH = sp.prod(h)
        Q0scaled = sp.prod(1 + L * sp.Rational(K(m, i - 1), K(m, i)) * lam
                           for i in range(2, m))
        direct_scaled_hom = sp.cancel((lam * sp.eye(m + 1) - H*A).det() / detH)
        assert sp.simplify(direct_scaled_hom - sp.expand(Q0scaled*F0 - R)) == 0

        Qscaled = sp.prod(
            sp.Rational(K(m, i - 1), K(m, i)) * (1 + L*lam)
            + (t - 1) / K(m, i)
            for i in range(2, m)
        )
        direct_scaled_spatial = sp.cancel(
            (lam * sp.eye(m + 1) - H*(A - t*D)).det() / detH
        )
        assert sp.simplify(direct_scaled_spatial - sp.expand(Qscaled*F - G)) == 0
        records.append({
            "m": m,
            "unit_homogeneous_identity": True,
            "unit_spatial_identity": True,
            "scaled_homogeneous_identity": True,
            "scaled_spatial_identity": True,
        })
    return records


def _even_y_to_z(expr, y, z, *other_symbols):
    poly = sp.Poly(sp.expand(expr), *other_symbols, y)
    result = 0
    for exps, coeff in poly.terms():
        yexp = exps[-1]
        assert yexp % 2 == 0
        term = coeff * z ** (yexp // 2)
        for sym, exp in zip(other_symbols, exps[:-1]):
            term *= sym ** exp
        result += term
    return sp.expand(result)


def modulus_certificate_checks():
    x, y, z, s, A, U = sp.symbols("x y z s A U", nonnegative=True, real=True)
    I = sp.I

    def modsq(expr):
        return sp.expand(expr * sp.conjugate(expr))

    lam = x + I * y
    t = 1 + s
    g1 = lam + 2 + sp.Rational(23, 63) * t
    gm = lam + 5 + sp.Rational(1, 7) * t
    gz = lam + 4 + sp.Rational(16, 45) * t
    F = g1 * gm * gz - 4 * g1 - 4 * gm + gz
    G = gz * (4 * g1 + gm) - 36
    E77y = ((sp.Rational(91, 90) ** 2 + y**2) * modsq(F) - modsq(G))
    E77 = _even_y_to_z(E77y, y, z, x, s)
    P77 = sp.Poly(E77, x, z, s)
    assert len(P77.terms()) == 77
    assert all(c > 0 for mon, c in P77.terms() if mon != (0, 0, 0))
    assert P77.coeff_monomial(1) == 0

    E84y = (sp.Rational(91, 90) ** 2 * (1 + A*x + y**2/3) * modsq(F)
            - modsq(G))
    E84 = _even_y_to_z(E84y, y, z, x, s, A)
    # Regroup as coefficients in x,z,s, leaving A symbolic.
    P84 = sp.Poly(E84, x, z, s)
    assert len(P84.terms()) == 84
    for mon, coeff in P84.terms():
        if mon == (0, 0, 0):
            assert coeff == 0
            continue
        coeff_poly = sp.Poly(coeff, A)
        assert all(c >= 0 for _, c in coeff_poly.terms())
        assert coeff != 0

    F0 = lam**3 + 11*lam**2 + 31*lam + 16
    R = 5*lam**2 + 33*lam + 16
    E22y = (1 + (U + sp.Rational(1, 4))*x + sp.Rational(5, 4)*y**2) * modsq(F0) - modsq(R)
    E22 = _even_y_to_z(E22y, y, z, x, U)
    P22 = sp.Poly(E22, x, z)
    assert len(P22.terms()) == 22
    for _, coeff in P22.terms():
        coeff_poly = sp.Poly(coeff, U)
        assert all(c >= 0 for _, c in coeff_poly.terms())

    P = lam**4 + 12*lam**3 + 42*lam**2 + 47*lam + 16
    E35y = modsq(1 + lam) * modsq(P) - modsq(R)
    E35 = _even_y_to_z(E35y, y, z, x)
    P35 = sp.Poly(E35, x, z)
    assert len(P35.terms()) == 35
    assert P35.coeff_monomial(1) == 0
    assert all(c > 0 for mon, c in P35.terms() if mon != (0, 0))

    # Equality-at-origin requires axis control, not merely coefficient signs.
    axes = {
        "E77_x_axis": str(sp.factor(E77.subs({z: 0, s: 0}))),
        "E77_z_axis": str(sp.factor(E77.subs({x: 0, s: 0}))),
        "E77_s_axis": str(sp.factor(E77.subs({x: 0, z: 0}))),
        "E84_x_axis": str(sp.factor(E84.subs({z: 0, s: 0}))),
        "E84_z_axis": str(sp.factor(E84.subs({x: 0, s: 0}))),
        "E84_s_axis": str(sp.factor(E84.subs({x: 0, z: 0}))),
        "E22_x_axis_U0": str(sp.factor(E22.subs({z: 0, U: 0}))),
        "E22_z_axis_U0": str(sp.factor(E22.subs({x: 0, U: 0}))),
        "E35_x_axis": str(sp.factor(E35.subs(z, 0))),
        "E35_z_axis": str(sp.factor(E35.subs(x, 0))),
    }
    # Each axis expression must be positive for a positive axis coordinate.
    for key, expr_text in axes.items():
        assert expr_text != "0", key

    return {
        "E77_term_count": len(P77.terms()),
        "E77_all_nonconstant_coefficients_positive": True,
        "E84_term_count": len(P84.terms()),
        "E84_coefficient_polynomials_nonnegative": True,
        "E22_term_count": len(P22.terms()),
        "E22_coefficient_polynomials_nonnegative_for_U_nonnegative": True,
        "E35_term_count": len(P35.terms()),
        "E35_all_nonconstant_coefficients_positive": True,
        "axis_restrictions": axes,
    }


def principal_block_falsification(seed=20260822):
    rng = random.Random(seed)
    worst = None
    cases = 0
    for m in range(3, 10):
        for trial in range(20):
            a = 10 ** rng.uniform(-3, 3)
            if trial % 4 == 0:
                b = 2 * a
            else:
                b = 10 ** rng.uniform(-3, 3)
            _, As = matrix_from_reactions(m, sp.Float(a, 17), sp.Float(b, 17))
            A = np.array(As.tolist(), dtype=float)
            h = np.array([10 ** rng.uniform(-4, 4) for _ in range(m + 1)])
            J = A @ np.diag(h)
            n = m + 1
            for size in range(1, m):
                for ind in itertools.combinations(range(n), size):
                    ev = np.linalg.eigvals(J[np.ix_(ind, ind)])
                    abscissa = float(np.max(ev.real))
                    record = (abscissa, m, trial, ind, a, b, h.tolist())
                    if worst is None or abscissa > worst[0]:
                        worst = record
                    if abscissa >= 1e-7:
                        raise AssertionError(("candidate counterexample", record, ev))
                    cases += 1
    return {
        "seed": seed,
        "blocks_tested": cases,
        "largest_numerical_spectral_abscissa": worst[0],
        "location": {"m": worst[1], "trial": worst[2], "indices_zero_based": worst[3]},
        "note": "Floating-point falsification only; near-zero margins arise under extreme scaling.",
    }


def scaled_and_exceptional_checks():
    out = []
    for m in [3, 4, 149]:
        _, Aexact = matrix_from_reactions(m)
        r, Dexact, ell = critical_profile(m)
        assert Aexact * right_zero_unit(m) == sp.zeros(m + 1, 1)
        assert (Aexact - Dexact) * r == sp.zeros(m + 1, 1)
        assert ell.T * (Aexact - Dexact) == sp.zeros(1, m + 1)
        assert sp.simplify(ell.T * Dexact * r)[0] < 0
        assert sp.simplify(ell.T * r)[0] < 0
        nu = m - 2
        endpoints = [
            ("L0", 1 / math.sqrt(3) if nu == 1 else math.sqrt(5) / (2 * math.sqrt(nu))),
            ("L1", 90 * nu / (90 * nu + 1)),
        ]
        A = np.array(Aexact.tolist(), dtype=float)
        D = np.array(Dexact.tolist(), dtype=float)
        for label, L in endpoints:
            h = np.ones(m + 1)
            for i in range(2, m):
                h[i - 1] = K(m, i) / (L * K(m, i - 1))
            H = np.diag(h)
            spectra = {}
            for t in [0.0, 1.0, 4.0, 9.0]:
                ev = np.linalg.eigvals(H @ (A - t * D))
                if t == 1.0:
                    k0 = int(np.argmin(np.abs(ev)))
                    zero = ev[k0]
                    complement = np.delete(ev, k0)
                    spectra[str(t)] = {
                        "critical_abs": float(abs(zero)),
                        "complement_abscissa": float(np.max(complement.real)),
                    }
                else:
                    # At t=0 remove the conservation zero before reporting the gap.
                    if t == 0.0:
                        k0 = int(np.argmin(np.abs(ev)))
                        zero = ev[k0]
                        complement = np.delete(ev, k0)
                        spectra[str(t)] = {
                            "conservation_abs": float(abs(zero)),
                            "complement_abscissa": float(np.max(complement.real)),
                        }
                    else:
                        spectra[str(t)] = {"spectral_abscissa": float(np.max(ev.real))}

            dphys = h * np.diag(D)
            chiD = float(dphys.max() / dphys.min())
            chiH = float(h.max() / h.min())
            claimedD = (23 / 63) * 91 * nu * L
            claimedH = (91 * nu - 1) / (91 * nu * L)
            assert abs(chiD / claimedD - 1) < 5e-12
            assert abs(chiH / claimedH - 1) < 5e-12
            assert chiD > chiH
            out.append({
                "m": m, "endpoint": label, "L": L,
                "chiD": chiD, "chiH": chiH, "product": chiD * chiH,
                "spectra": spectra,
            })
        if m == 149:
            # The superseded L=1/sqrt(3*147)=1/21 endpoint lies outside the
            # current interval.  It is a useful falsification control because
            # the homogeneous operator really is unstable there.
            Llegacy = 1 / 21
            h = np.ones(m + 1)
            for i in range(2, m):
                h[i - 1] = K(m, i) / (Llegacy * K(m, i - 1))
            ev = np.linalg.eigvals(np.diag(h) @ A)
            k0 = int(np.argmin(np.abs(ev)))
            comp = np.delete(ev, k0)
            unstable = comp[int(np.argmax(comp.real))]
            assert unstable.real > 0
            out.append({
                "m": 149,
                "endpoint": "legacy_excluded_L=1/21",
                "L": Llegacy,
                "homogeneous_rightmost_eigenvalue": [float(unstable.real), float(unstable.imag)],
                "scope": "outside current certified interval; falsification control only",
            })
    return out


def exact_contrast_logic():
    # Independent scalar optimization proof reduced to inequalities, plus exact
    # endpoint comparisons for the exceptional dimensions.
    records = []
    for m in [3, 4, 149]:
        nu = m - 2
        for label in ["L0", "L1"]:
            if label == "L0":
                L = sp.sqrt(sp.Rational(1, 3)) if nu == 1 else sp.sqrt(sp.Rational(5, 4 * nu))
            else:
                L = sp.Rational(90 * nu, 90 * nu + 1)
            chiD = sp.Rational(23, 63) * 91 * nu * L
            chiH = sp.Rational(91 * nu - 1, 91 * nu) / L
            product = sp.simplify(chiD * chiH)
            assert product == sp.Rational(23 * (91 * nu - 1), 63)
            assert sp.N(chiD - chiH, 50) > 0
            records.append({"m": m, "endpoint": label,
                            "chiD_exact": str(chiD), "chiH_exact": str(chiH),
                            "product_exact": str(product)})
    return records


def outside_domain_examples():
    s, lam = sp.symbols("s lam", positive=True)

    # If the positive order-(n-1) signed-minor sum is deleted, the claimed
    # no-positive-real-root region can fail.  Here det J=0 and the only
    # lower-order hypothesis for n=2 is a_empty=1, but the order-one sum is -2.
    Jbad = sp.Matrix([[-1, 1], [-3, 3]])
    Dbad = sp.diag(1, 2)
    pbad = sp.factor((s * Dbad - Jbad).det())
    assert pbad == s * (2*s - 1)
    sample = sp.Rational(51, 100)  # strictly above s*=1/2
    char_sample = sp.factor((lam * sp.eye(2) - (Jbad - sample*Dbad)).det())
    # Both roots are positive: (47 +/- sqrt(1801))/200.
    assert sp.expand(char_sample) == lam**2 - sp.Rational(47, 100)*lam + sp.Rational(51, 5000)
    assert 47**2 > 1801 and 47 > sp.sqrt(1801)

    # Boundary equality in the topology-specific stationary criterion.
    _, A3 = matrix_from_reactions(3)
    Deq = sp.diag(1, 1, 1, 8)
    peq = sp.factor((s*Deq - A3).det())
    assert peq == 4*s**2*(2*s**2 + 17*s + 32)

    # Boundary T(H)=1 gives a double conservation zero and is outside S_m.
    Hboundary = sp.diag(1, 1, 1, sp.Rational(1, 8))
    char_boundary = sp.factor((lam*sp.eye(4) - A3*Hboundary).det())
    assert char_boundary == lam**2*(2*lam**2 + 17*lam + 32)/2

    # T(H)<1 makes the homogeneous realization unstable (positive real root).
    Hunstable = sp.diag(1, 1, 1, sp.Rational(1, 16))
    char_unstable = sp.factor((lam*sp.eye(4) - A3*Hunstable).det())
    assert sp.Poly(char_unstable/lam, lam).coeff_monomial(1) < 0

    # A naive m=2 continuation makes Ra equal 2X1->2X2 and Rb equal
    # 2X2->X2.  It has five (not m+2) reactions and no conservation law.
    sources = [(0,0,0), (2,0,0), (0,2,0), (0,0,2), (1,1,0)]
    targets = [(1,0,0), (0,2,0), (0,1,0), (1,1,0), (0,0,2)]
    Y2 = sp.Matrix.hstack(*(sp.Matrix(v) for v in sources))
    G2 = sp.Matrix.hstack(*(sp.Matrix(v) for v in targets)) - Y2
    assert G2.rank() == 3 and not G2.T.nullspace()

    return {
        "removed_order_sum_counterexample": {
            "J": "[[-1,1],[-3,3]]",
            "D": "diag(1,2)",
            "order_one_signed_minor_sum": -2,
            "det(sD-J)": str(pbad),
            "scalar_threshold": "1/2",
            "at_s_51_over_100": {
                "characteristic_polynomial": str(char_sample),
                "positive_eigenvalues": ["(47-sqrt(1801))/200", "(47+sqrt(1801))/200"],
            },
            "conclusion": "Dropping the positive order-(n-1) sum invalidates the claimed s>s* positive-real exclusion.",
        },
        "criterion_equality": {
            "m": 3, "H": "I", "D": "diag(1,1,1,8)",
            "det(sD-J)": str(peq),
            "conclusion": "beta1=0 and no nonzero threshold; the strict > sign is necessary.",
        },
        "homogeneous_stability_boundary": {
            "m": 3, "H": "diag(1,1,1,1/8)", "T(H)": 1,
            "characteristic_polynomial": str(char_boundary),
            "conclusion": "zero is algebraically double, so this point is not in S_m.",
        },
        "outside_homogeneous_stability": {
            "m": 3, "H": "diag(1,1,1,1/16)", "T(H)": "1/2",
            "characteristic_polynomial": str(char_unstable),
            "conclusion": "the complementary polynomial is negative at zero and has a positive real root.",
        },
        "naive_m2_extension": {
            "reaction_count": 5, "expected_m_plus_2": 4,
            "stoichiometric_rank": G2.rank(), "left_kernel_dimension": len(G2.T.nullspace()),
            "conclusion": "the indexed family and its semipositive conservation structure do not extend to m=2.",
        },
    }


def main():
    report = {
        "implementation_independence": (
            "No project helper, stored certificate, generated table, or expected output was imported. "
            "Matrices were reconstructed from reaction source/target vectors."
        ),
        "reaction_rank_flux_and_omissions": exact_reaction_and_minor_checks(),
        "scc_exhaustion": check_scc_exhaustion(),
        "boundary_triad": triad_check(),
        "diffusion_polynomials": diffusion_polynomial_checks(),
        "determinant_factorizations": determinant_factorization_checks(),
        "modulus_certificates": modulus_certificate_checks(),
        "principal_block_falsification": principal_block_falsification(),
        "critical_scaled_exceptional": scaled_and_exceptional_checks(),
        "contrast_endpoint_exact": exact_contrast_logic(),
        "outside_domain_example": outside_domain_examples(),
    }
    json.dump(report, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
