#!/usr/bin/env python3
"""Independent exact check of the article's ordinary-triangle rank witness.

This script imports no submission modules or stored certificate data.  It
constructs the three-sunlet Fourier map printed in the article, differentiates
it symbolically, and writes a deterministic JSON report.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ZERO, C, G, T = 0, 1, 2, 3
S_SECTOR = {C, T}


def spectrum(char: int, s_value: sp.Expr, g_value: sp.Expr) -> sp.Expr:
    if char == ZERO:
        return sp.Integer(1)
    if char in S_SECTOR:
        return s_value
    if char == G:
        return g_value
    raise ValueError(char)


def sunlet_q(
    pattern: tuple[int, int, int],
    spectra: dict[str, tuple[sp.Expr, sp.Expr]],
    delta: sp.Expr,
) -> sp.Expr:
    x, y, z = pattern
    if x ^ y ^ z:
        return sp.Integer(0)
    a = spectrum(x, *spectra["a"])
    b = spectrum(y, *spectra["b"])
    c = spectrum(z, *spectra["c"])
    f_y = spectrum(y, *spectra["f"])
    f_x = spectrum(x, *spectra["f"])
    d_z = spectrum(z, *spectra["d"])
    e_z = spectrum(z, *spectra["e"])
    return sp.factor(a * b * c * (delta * f_y * d_z + (1 - delta) * f_x * e_z))


def derivative_matrix(
    outputs: list[sp.Expr],
    variables: list[sp.Symbol],
) -> sp.Matrix:
    zero_substitution = {variable: 0 for variable in variables}
    return sp.Matrix(
        [
            [sp.simplify(sp.diff(output, variable).subs(zero_substitution)) for variable in variables]
            for output in outputs
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    half = sp.Rational(1, 2)
    third = sp.Rational(1, 3)
    delta = half

    # Four common logarithmic s/g scales of a,b,c,f.
    ta, tb, tc, tf = sp.symbols("ta tb tc tf")
    common = {
        "a": (half * sp.exp(ta), half * sp.exp(ta)),
        "b": (half * sp.exp(tb), half * sp.exp(tb)),
        "c": (half * sp.exp(tc), half * sp.exp(tc)),
        "d": (half, half),
        "e": (half, half),
        "f": (third * sp.exp(tf), third * sp.exp(tf)),
    }

    x_s = sunlet_q((C, C, ZERO), common, delta)
    y_s = sunlet_q((C, ZERO, C), common, delta)
    z_s = sunlet_q((ZERO, C, C), common, delta)
    w = sunlet_q((G, C, T), common, delta)
    j0 = derivative_matrix(
        [sp.log(x_s), sp.log(y_s), sp.log(z_s), sp.log(w)],
        [ta, tb, tc, tf],
    )

    # Five anisotropies.  The paired coordinates and the e-anisotropy are
    # held fixed, exactly as in the article's displayed slice.
    ua, ub, uc, ud, uf = sp.symbols("ua ub uc ud uf")
    anisotropic = {
        "a": (half, half * sp.exp(ua)),
        "b": (half, half * sp.exp(ub)),
        "c": (half, half * sp.exp(uc)),
        "d": (half, half * sp.exp(ud)),
        "e": (half, half),
        "f": (third, third * sp.exp(uf)),
    }
    xs = sunlet_q((C, C, ZERO), anisotropic, delta)
    xg = sunlet_q((G, G, ZERO), anisotropic, delta)
    ys = sunlet_q((C, ZERO, C), anisotropic, delta)
    yg = sunlet_q((G, ZERO, G), anisotropic, delta)
    zs = sunlet_q((ZERO, C, C), anisotropic, delta)
    zg = sunlet_q((ZERO, G, G), anisotropic, delta)
    u = sunlet_q((C, G, T), anisotropic, delta)
    v = sunlet_q((C, T, G), anisotropic, delta)
    w_anisotropic = sunlet_q((G, C, T), anisotropic, delta)
    j_perp = derivative_matrix(
        [
            sp.log(xg / xs),
            sp.log(yg / ys),
            sp.log(zg / zs),
            sp.log(u / w_anisotropic),
            sp.log(v / w_anisotropic),
        ],
        [ua, ub, uc, ud, uf],
    )

    expected_j0 = sp.Matrix(
        [
            [1, 1, 0, 1],
            [1, 0, 1, sp.Rational(1, 4)],
            [0, 1, 1, sp.Rational(1, 4)],
            [1, 1, 1, 1],
        ]
    )
    expected_j_perp = sp.Matrix(
        [
            [1, 1, 0, 0, 1],
            [1, 0, 1, sp.Rational(3, 4), sp.Rational(1, 4)],
            [0, 1, 1, sp.Rational(1, 4), sp.Rational(1, 4)],
            [-1, 1, 0, 0, 0],
            [-1, 0, 1, sp.Rational(1, 2), sp.Rational(-1, 2)],
        ]
    )

    assert j0 == expected_j0
    assert j_perp == expected_j_perp
    assert j0.det() == sp.Rational(-1, 2)
    assert j_perp.det() == sp.Rational(-1, 4)

    witness = {
        name: (value, value)
        for name, value in {
            "a": half,
            "b": half,
            "c": half,
            "d": half,
            "e": half,
            "f": third,
        }.items()
    }
    pair_patterns = [
        (ZERO, C, C),
        (ZERO, G, G),
        (C, ZERO, C),
        (G, ZERO, G),
        (C, C, ZERO),
        (G, G, ZERO),
    ]
    triple_patterns = [(C, G, T), (C, T, G), (G, C, T)]
    pair_values = [sp.simplify(sunlet_q(pattern, witness, delta)) for pattern in pair_patterns]
    triple_values = [sp.simplify(sunlet_q(pattern, witness, delta)) for pattern in triple_patterns]
    assert pair_values == [sp.Rational(1, 12)] * 6
    assert triple_values == [sp.Rational(1, 48)] * 3
    assert all(g_value > s_value**2 for s_value, g_value in witness.values())

    payload = {
        "schema": "independent-k2p-triangle-germ-v1",
        "imports_submission_code": False,
        "character_order": ["0", "C", "G", "T"],
        "symmetric_pair_coordinates": [str(value) for value in pair_values],
        "symmetric_triple_coordinates": [str(value) for value in triple_values],
        "strict_continuous_time": True,
        "J0": [[str(value) for value in row] for row in j0.tolist()],
        "det_J0": str(j0.det()),
        "J_perp": [[str(value) for value in row] for row in j_perp.tolist()],
        "det_J_perp": str(j_perp.det()),
        "combined_nine_slice_determinant": str(j0.det() * j_perp.det()),
        "rank": j0.rank() + j_perp.rank(),
        "status": "PASS",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("INDEPENDENT_TRIANGLE_GERM_PASS")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
