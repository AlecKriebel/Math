#!/usr/bin/env python3
"""Exact independent-routing marginals and two-atom rate recovery."""
from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
from pathlib import Path

import sympy as sp

from record_schema import make_record, write_json_record


def weights(m: int, gamma: Fraction) -> dict[tuple[int, ...], Fraction]:
    return {
        bits: gamma ** sum(bits) * (1 - gamma) ** (m - sum(bits))
        for bits in itertools.product((0, 1), repeat=m)
    }


def marginal(
    full: dict[tuple[int, ...], Fraction],
    selected: tuple[int, ...],
) -> dict[tuple[int, ...], Fraction]:
    output: dict[tuple[int, ...], Fraction] = {}
    for bits, weight in full.items():
        key = tuple(bits[index] for index in selected)
        output[key] = output.get(key, Fraction(0)) + weight
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=4)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.max_m < 1:
        raise SystemExit("max-m must be positive")
    gamma = Fraction(3, 7)
    routing_records = []
    failures = []
    for m in range(1, args.max_m + 1):
        full = weights(m, gamma)
        checks = {
            "assignment_count": len(full) == 2**m,
            "mass_one": sum(full.values()) == 1,
            "tested_marginals": True,
        }
        marginal_checks = []
        for size in range(1, min(3, m) + 1):
            selected = tuple(range(size))
            ok = marginal(full, selected) == weights(size, gamma)
            marginal_checks.append({"selected": list(selected), "exact_identity": ok})
            checks["tested_marginals"] &= ok
        if not all(checks.values()):
            failures.append(m)
        routing_records.append(
            {
                "m": m,
                "assignment_count": len(full),
                "checks": checks,
                "marginal_checks": marginal_checks,
            }
        )

    moment_gamma = sp.Rational(2, 7)
    rate1, rate2 = sp.Rational(2), sp.Rational(5)
    moments = [
        sp.simplify(moment_gamma**2 * rate1**k + (1 - moment_gamma) ** 2 * rate2**k)
        for k in range(1, 5)
    ]
    recurrence_matrix = sp.Matrix(
        [[moments[1], -moments[0]], [moments[2], -moments[1]]]
    )
    recurrence_rhs = sp.Matrix([moments[2], moments[3]])
    recurrence = recurrence_matrix.LUsolve(recurrence_rhs)
    z = sp.symbols("z")
    roots = sp.solve(z**2 - recurrence[0] * z + recurrence[1], z)
    pair_ok = set(roots) == {rate1, rate2}
    equal_rate_coefficient = sp.simplify(
        1
        - (moment_gamma**2 + (1 - moment_gamma) ** 2)
        - 2 * moment_gamma * (1 - moment_gamma)
    ) == 0
    checks = {
        "all_routing_marginals": not failures,
        "two_atom_rates_recovered": pair_ok,
        "equal_rate_confluent_coefficient": equal_rate_coefficient,
    }
    record = make_record(
        job="routing_tomography",
        case_input={"max_m": args.max_m, "routing_gamma": "3/7"},
        status="PASS" if all(checks.values()) else "BLOCKING",
        system={
            "independent_routing_gamma": "3/7",
            "two_atom_fixture": {"gamma": "2/7", "rates": ["2", "5"]},
        },
        exact_witness={
            "checks": checks,
            "routing_records": routing_records,
            "failed_m": failures,
            "two_atom_moments": [str(value) for value in moments],
            "recovered_rates": [str(value) for value in roots],
            "equal_rate_coefficient_check": equal_rate_coefficient,
        },
        declared_quotient_orbit={"routing": "independent Bernoulli lineage routing"},
        notes="Every marginal is summed exactly with Fraction arithmetic; rate recovery is symbolic.",
    )
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_json_record(output, record)
    if record["status"] != "PASS":
        print("ROUTING_TOMOGRAPHY_BLOCKING")
        raise SystemExit(1)
    print(f"ROUTING_TOMOGRAPHY_OK m=1..{args.max_m} pair_recovery=PASS")


if __name__ == "__main__":
    main()
