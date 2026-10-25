#!/usr/bin/env python3
"""Exact actual-row Hankel certificate for a retained nonbridge."""
from __future__ import annotations

import argparse
from pathlib import Path

import sympy as sp

from record_schema import make_record, write_json_record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    gamma, lam, distance, delta, u1, u2, u = sp.symbols(
        "gamma lambda D delta u1 u2 u", positive=True
    )
    a = lambda x: gamma * (1 - gamma) * lam * sp.exp(-lam * x)
    c = lambda x: gamma**2 * lam * sp.exp(-lam * distance - 2 * lam * x)
    e_delta = sp.exp(-lam * delta)
    row = lambda x: sp.Matrix([[c(x) * (1 - e_delta), a(x) + c(x) * e_delta]])
    determinant = sp.factor(sp.Matrix.vstack(row(u1), row(u2)).det())
    expected = sp.factor(
        (1 - e_delta)
        * gamma**3
        * (1 - gamma)
        * lam**2
        * sp.exp(-lam * distance)
        * (
            sp.exp(-2 * lam * u1 - lam * u2)
            - sp.exp(-2 * lam * u2 - lam * u1)
        )
    )
    wronskian = sp.factor(
        row(u)[0] * sp.diff(row(u)[1], u)
        - row(u)[1] * sp.diff(row(u)[0], u)
    )
    checks = {
        "actual_minor_matches_closed_form": sp.simplify(determinant - expected) == 0,
        "wronskian_nonzero": wronskian != 0,
    }
    record = make_record(
        job="observable_hankel_rows",
        case_input={
            "endpoint": "t=h+D",
            "partition": ["xz", "y"],
            "suffixes": ["merge-next-delta", "survive-next-delta"],
            "assumptions": "gamma in (0,1); lambda,D,delta,u1,u2 positive; u1 != u2",
        },
        status="PASS" if all(checks.values()) else "BLOCKING",
        system={
            "row_formula": str(row(u)),
            "same_cut_endpoint": "t=h+D",
            "same_cut_partition": ["xz", "y"],
        },
        exact_witness={
            "checks": checks,
            "determinant": str(determinant),
            "expected_determinant": str(expected),
            "wronskian": str(wronskian),
        },
        declared_quotient_orbit={"interface": "retained-nonbridge actual marked rows"},
        notes="Both rows are observable events at one fixed cut; no latent row is used.",
    )
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_json_record(output, record)
    if record["status"] != "PASS":
        print("OBSERVABLE_HANKEL_ROWS_BLOCKING")
        raise SystemExit(1)
    print("OBSERVABLE_HANKEL_ROWS_OK actual_minor=PASS")


if __name__ == "__main__":
    main()
