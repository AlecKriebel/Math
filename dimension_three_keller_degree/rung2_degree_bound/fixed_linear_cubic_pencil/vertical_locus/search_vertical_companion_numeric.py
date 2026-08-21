#!/usr/bin/env python3
"""Targeted numerical construction search on the triple-vertical companion.

This is discovery code, not a proof.  It searches the exact E7 normal form

    H4 = (z^4, z*q, 0),
    H3 = (4*z*W/3 + q, V, z^3),
    H2 = (A, B, W),
    L  = I,

for one fixed primitive cubic representative q, with general quadratic
A,B,W and general cubic V having no z^3 term.  A
numerical zero of the coefficient residual is only a candidate: it must be
rationally reconstructed and checked exactly before it has mathematical
value.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import least_squares


def build_system(general_linear: bool, q_shape: str):
    x, y, z = sp.symbols("x y z")
    variables = (x, y, z)
    quadratic_monomials = (x**2, x * y, y**2, x * z, y * z, z**2)
    cubic_monomials_no_z3 = (
        x**3,
        x**2 * y,
        x * y**2,
        y**3,
        x**2 * z,
        x * y * z,
        y**2 * z,
        x * z**2,
        y * z**2,
    )

    a_coeffs = sp.symbols("A0:6")
    b_coeffs = sp.symbols("B0:6")
    w_coeffs = sp.symbols("W0:6")
    v_coeffs = sp.symbols("V0:9")
    lower_parameters = a_coeffs + b_coeffs + w_coeffs + v_coeffs

    A = sum(c * m for c, m in zip(a_coeffs, quadratic_monomials))
    B = sum(c * m for c, m in zip(b_coeffs, quadratic_monomials))
    W = sum(c * m for c, m in zip(w_coeffs, quadratic_monomials))
    V = sum(c * m for c, m in zip(v_coeffs, cubic_monomials_no_z3))

    q_shapes = {
        "squarefree": x * y * (x - y),
        "double": x**2 * y + y**2 * z,
        "triple_y2z": x**3 + y**2 * z,
        "triple_xyz": x**3 + x * y * z,
        "triple_yz2": x**3 + y * z**2,
    }
    q = q_shapes[q_shape]
    H2 = sp.Matrix((A, B, W))
    H3 = sp.Matrix((sp.Rational(4, 3) * z * W + q, V, z**3))
    H4 = sp.Matrix((z**4, z * q, 0))
    if general_linear:
        linear_coeffs = sp.symbols("L0:9")
        linear_part = sp.Matrix(3, 3, linear_coeffs)
        parameters = lower_parameters + linear_coeffs
    else:
        linear_part = sp.eye(3)
        parameters = lower_parameters
    determinant = sp.expand(
        (linear_part + H2.jacobian(variables) + H3.jacobian(variables)
         + H4.jacobian(variables)).det()
    )
    residual_poly = sp.Poly(determinant - 1, x, y, z)
    monomials = residual_poly.monoms()
    residuals = sp.Matrix(residual_poly.coeffs())
    jacobian = residuals.jacobian(parameters)

    residual_fun = sp.lambdify((parameters,), residuals, modules="numpy")
    jacobian_fun = sp.lambdify((parameters,), jacobian, modules="numpy")
    names = tuple(str(p) for p in parameters)
    return names, monomials, residual_fun, jacobian_fun


def witness_start(names: tuple[str, ...]) -> np.ndarray:
    """The exact E8--E5 survivor from the working note."""
    start = np.zeros(len(names), dtype=float)
    start[names.index("B3")] = 1.0  # B=xz
    start[names.index("W5")] = 1.0  # W=z^2
    if "L0" in names:
        start[names.index("L0")] = 1.0
        start[names.index("L4")] = 1.0
        start[names.index("L8")] = 1.0
    return start


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=24)
    parser.add_argument("--max-nfev", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument("--scale", type=float, default=0.35)
    parser.add_argument("--general-linear", action="store_true")
    parser.add_argument(
        "--q-shape",
        choices=(
            "squarefree",
            "double",
            "triple_y2z",
            "triple_xyz",
            "triple_yz2",
        ),
        default="squarefree",
    )
    parser.add_argument(
        "--bound",
        type=float,
        help="Optional symmetric box bound on every search parameter.",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    names, monomials, residual_fun_raw, jacobian_fun_raw = build_system(
        args.general_linear, args.q_shape
    )

    def residual_fun(values):
        return np.asarray(residual_fun_raw(tuple(values)), dtype=float).reshape(-1)

    def jacobian_fun(values):
        return np.asarray(jacobian_fun_raw(tuple(values)), dtype=float)

    rng = np.random.default_rng(args.seed)
    base = witness_start(names)
    starts = [base, np.zeros_like(base)]
    starts.extend(base + args.scale * rng.normal(size=base.shape)
                  for _ in range(max(0, args.starts - 2)))

    best = None
    for index, start in enumerate(starts):
        options = {}
        if args.bound is not None:
            options["bounds"] = (-args.bound, args.bound)
            start = np.clip(start, -0.99 * args.bound, 0.99 * args.bound)
        result = least_squares(
            residual_fun,
            start,
            jac=jacobian_fun,
            method="trf",
            x_scale="jac",
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
            **options,
        )
        norm_inf = float(np.linalg.norm(result.fun, ord=np.inf))
        norm_two = float(np.linalg.norm(result.fun))
        record = {
            "start": index,
            "success": bool(result.success),
            "status": int(result.status),
            "nfev": int(result.nfev),
            "cost": float(result.cost),
            "residual_inf": norm_inf,
            "residual_two": norm_two,
            "parameters": {name: float(value)
                           for name, value in zip(names, result.x)},
        }
        if best is None or norm_inf < best["residual_inf"]:
            best = record
        print(
            f"start={index:02d} nfev={result.nfev:4d} "
            f"||r||_inf={norm_inf:.6e} ||r||_2={norm_two:.6e}",
            flush=True,
        )

    assert best is not None
    payload = {
        "scope": (
            f"fixed q-shape={args.q_shape}, vertical companion, a=1, "
            + ("general L with det(L)=1" if args.general_linear else "L=I")
        ),
        "proof_status": "numerical discovery evidence only",
        "parameter_count": len(names),
        "residual_coefficient_count": len(monomials),
        "best": best,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if args.output is not None:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
