#!/usr/bin/env python3
"""Independent finite/exact checks for the v1.0.8 PDE repair.

This file deliberately imports no manuscript/repository helper.  Finite matrix
checks support, but do not replace, the Fourier/Fredholm argument in the report.
"""

from __future__ import annotations

import json
import math

import numpy as np
import sympy as sp


def exact_A(m: int) -> sp.Matrix:
    n = m + 1
    A = sp.zeros(n)
    A[0, 0] = -2
    A[0, m - 2] = -1
    A[0, m - 1] = -1
    A[0, m] = 2
    A[1, 0] = -1
    A[1, 1] = -1
    A[1, m - 1] = 2
    for species in range(3, m):
        row = species - 1
        A[row, row - 1] = 1
        A[row, row] = -1
    A[m - 1, 0] = 1
    A[m - 1, m - 2] = 2
    A[m - 1, m - 1] = -5
    A[m - 1, m] = 2
    A[m, 0] = 2
    A[m, m - 1] = 2
    A[m, m] = -4
    return A


def exact_c(m: int) -> sp.Matrix:
    return sp.Matrix([0] + [4] * (m - 2) + [2, 1])


def exact_D(m: int) -> sp.Matrix:
    entries = [sp.Rational(23, 63)]
    entries.extend(sp.Rational(1, 91 * m - 181 - i) for i in range(2, m))
    entries.extend([sp.Rational(1, 7), sp.Rational(16, 45)])
    return sp.diag(*entries)


def exact_r(m: int) -> sp.Matrix:
    vals = [sp.Integer(1)]
    vals.extend(
        -sp.Rational(91 * m - 181 - i, 63 * (m - 2))
        for i in range(2, m)
    )
    vals.extend([-sp.Rational(2, 9), sp.Rational(5, 14)])
    return sp.Matrix(vals)


def exact_ell(m: int) -> sp.Matrix:
    vals = [-sp.Rational(266, 815)]
    vals.extend(
        sp.Rational(78260 * (m - 2), 163 * (91 * m - 180 - i))
        for i in range(2, m)
    )
    vals.extend([sp.Rational(18368, 7335), sp.Integer(1)])
    return sp.Matrix(vals)


def endpoint_L(m: int, which: str) -> sp.Expr:
    nu = m - 2
    if which == "L0":
        return 1 / sp.sqrt(3) if nu == 1 else sp.sqrt(5) / (2 * sp.sqrt(nu))
    if which == "L1":
        return sp.Rational(90 * nu, 90 * nu + 1)
    raise ValueError(which)


def exact_H(m: int, L: sp.Expr) -> sp.Matrix:
    vals = [sp.Integer(1)]
    for i in range(2, m):
        Ki = 91 * m - 181 - i
        Kim1 = 91 * m - 180 - i
        vals.append(sp.Rational(Ki, Kim1) / L)
    vals.extend([sp.Integer(1), sp.Integer(1)])
    return sp.diag(*vals)


def exact_checks(m: int) -> dict[str, object]:
    A, D, c, r, ell = exact_A(m), exact_D(m), exact_c(m), exact_r(m), exact_ell(m)
    B = A - D
    rho = A.nullspace()[0]
    assert (c.T * A) == sp.zeros(1, m + 1)
    assert A.rank() == m
    assert sp.simplify((c.T * rho)[0]) != 0
    assert B * r == sp.zeros(m + 1, 1)
    assert ell.T * B == sp.zeros(1, m + 1)
    assert B.rank() == m
    assert sp.simplify((ell.T * r)[0]) < 0
    assert sp.simplify((ell.T * D * r)[0]) < 0
    k = sp.symbols("k", positive=True)
    factor_residual = sp.simplify(A - k**2 * D + k**2 * D * (sp.eye(m + 1) - k**-2 * D.inv() * A))
    assert factor_residual == sp.zeros(m + 1)

    scaled = {}
    for which in ("L0", "L1"):
        L = endpoint_L(m, which)
        H = exact_H(m, L)
        cH = H.inv() * c
        ellH = H.inv() * ell
        HB = H * B
        assert cH.T * H * A == sp.zeros(1, m + 1)
        assert HB * r == sp.zeros(m + 1, 1)
        assert ellH.T * HB == sp.zeros(1, m + 1)
        assert sp.simplify((ellH.T * r)[0]) != 0
        assert sp.simplify((ellH.T * H * D * r)[0] - (ell.T * D * r)[0]) == 0
        scaled[which] = {
            "L": str(L),
            "left_right_pairing_sign": int(sp.sign(sp.N((ellH.T * r)[0], 40))),
            "transversality_sign": int(sp.sign(sp.N((ellH.T * H * D * r)[0], 40))),
        }

    return {
        "rank_A": A.rank(),
        "rank_A_minus_D": B.rank(),
        "c_dot_rho_nonzero": True,
        "ell_dot_r_sign": int(sp.sign((ell.T * r)[0])),
        "ell_dot_Dr_sign": int(sp.sign((ell.T * D * r)[0])),
        "high_mode_factorization_exact": True,
        "scaled_endpoints": scaled,
    }


def spectral_summary(m: int, H: np.ndarray | None = None) -> dict[str, float | int]:
    A = np.array(exact_A(m), dtype=float)
    D = np.array(exact_D(m), dtype=float)
    if H is None:
        H = np.eye(m + 1)
    mats = [H @ A, H @ (A - D)]
    eig0 = np.linalg.eigvals(mats[0])
    eig1 = np.linalg.eigvals(mats[1])
    nonzero0 = eig0[np.argsort(np.abs(eig0))[1:]]
    nonzero1 = eig1[np.argsort(np.abs(eig1))[1:]]
    max0 = float(np.max(nonzero0.real))
    max1 = float(np.max(nonzero1.real))
    maxhigher = -math.inf
    maxhigher_k = -1
    for k in range(2, 21):
        v = float(np.max(np.linalg.eigvals(H @ (A - (k * k) * D)).real))
        if v > maxhigher:
            maxhigher, maxhigher_k = v, k

    leading = H @ D
    leading_inv_A = np.linalg.solve(leading, H @ A)
    threshold = math.ceil(math.sqrt(2 * np.linalg.norm(leading_inv_A, 2)))
    threshold = max(threshold, 1)
    worst_ratio = 0.0
    for k in (threshold, threshold + 1, 2 * threshold):
        invnorm = np.linalg.norm(np.linalg.inv(H @ (A - (k * k) * D)), 2)
        rhs = 2 * np.linalg.norm(np.linalg.inv(leading), 2) / (k * k)
        worst_ratio = max(worst_ratio, float(invnorm / rhs))
    assert max0 < -1e-9 and max1 < -1e-9 and maxhigher < -1e-9
    assert worst_ratio <= 1 + 1e-9
    return {
        "homogeneous_complement_spectral_bound": max0,
        "first_mode_complement_spectral_bound": max1,
        "higher_mode_max_real_k_2_to_20": maxhigher,
        "higher_mode_argmax_k": maxhigher_k,
        "neumann_bound_threshold_k": threshold,
        "max_inverse_bound_ratio": worst_ratio,
    }


def main() -> None:
    out: dict[str, object] = {
        "method": "standalone definitions; no project imports",
        "logical_scope": "finite/exact checks support but do not prove the infinite-dimensional theorem",
        "exact": {},
        "spectral": {},
    }
    for m in (3, 4, 7):
        out["exact"][str(m)] = exact_checks(m)
    for m in (3, 4, 149):
        unit = spectral_summary(m)
        scaled = {}
        for which in ("L0", "L1"):
            H = np.array(exact_H(m, endpoint_L(m, which)).evalf(40), dtype=float)
            scaled[which] = spectral_summary(m, H)
        out["spectral"][str(m)] = {"unit": unit, "scaled": scaled}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
