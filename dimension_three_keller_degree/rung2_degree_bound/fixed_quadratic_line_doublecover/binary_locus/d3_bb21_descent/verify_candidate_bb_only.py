#!/usr/bin/env python3
"""Run only the BB21 portions of the concurrently edited primary module."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)


def main() -> None:
    source = Path(__file__).resolve().parent.parent / "d3_construction_search" / "verify_ansatz_obstructions.py"
    spec = importlib.util.spec_from_file_location("d3_candidate_primary", source)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load candidate primary module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    h = module.p * module.q
    R = module.p**2 * module.q
    P = module.sp.expand(h * module.p**2)
    Q = module.sp.expand(h * module.q**2)
    alpha = module.jac2(Q, R)
    beta = -module.jac2(P, R)
    gamma = module.jac2(P, Q)
    module.verify_r2_kernel_zero(alpha, beta, "BB_HOSTILE")
    module.verify_expected_basis(
        alpha,
        beta,
        gamma,
        1,
        ((module.sp.Rational(8, 5) * module.p, 0, 1),),
    )
    module.verify_expected_basis(
        alpha,
        beta,
        gamma,
        2,
        (
            (-module.sp.Rational(1, 5) * module.p**2, module.q**2, 0),
            (module.sp.Rational(8, 5) * module.p**2, 0, module.p),
            (module.sp.Rational(8, 5) * module.p * module.q, 0, module.q),
        ),
    )
    module.verify_origin_structure("BB", h, None)
    module.verify_bb_full_parameterization(None)
    print("D3_BB21_CANDIDATE_PRIMARY_ONLY_PASS")


if __name__ == "__main__":
    main()
