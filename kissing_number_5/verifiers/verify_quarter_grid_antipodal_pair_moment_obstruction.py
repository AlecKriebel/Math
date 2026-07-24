#!/usr/bin/env python3
"""Verify the exact quarter-grid obstruction for 14--16 antipodal pairs.

The verifier expands the affine identity coefficient by coefficient over
the rationals.  It then reconstructs every branch constant and compares the
resulting energy upper bound with the rank-five lower bound.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = (
    ROOT
    / "certificates"
    / "quarter_grid_antipodal_pair_moment_obstruction.json"
)


class VerificationError(ValueError):
    """Raised when an exact certificate check fails."""


def check(condition: bool, message: str) -> None:
    """Proof-critical check that remains active under ``python -O``."""

    if not condition:
        raise VerificationError(message)


def gegenbauer_5(t: Q, maximum_degree: int) -> list[Q]:
    """Normalized dimension-five Gegenbauer values, with P_k(1)=1."""

    values = [Q(1)]
    if maximum_degree:
        values.append(t)
    for degree in range(2, maximum_degree + 1):
        values.append(
            (
                (2 * degree + 1) * t * values[-1]
                - (degree - 1) * values[-2]
            )
            / (degree + 2)
        )
    return values


def add_scaled(
    constant: Q,
    coefficients: list[Q],
    scale: Q,
    other_constant: Q,
    other_coefficients: list[Q],
) -> tuple[Q, list[Q]]:
    return (
        constant + scale * other_constant,
        [
            value + scale * other
            for value, other in zip(
                coefficients, other_coefficients, strict=True
            )
        ],
    )


def branch_affine_data(
    antipode_pairs: int,
) -> tuple[int, int, int, dict[int, tuple[Q, list[Q]]]]:
    """Return n,C,B and M_1,M_3,M_4 in the nine count variables."""

    n = 41 - 2 * antipode_pairs
    core_pairs = math.comb(n, 2)
    background_pairs = 820 - antipode_pairs - core_pairs
    core_nodes = [Q(value, 4) for value in range(-3, 3)]
    polynomials = {
        node: gegenbauer_5(node, 4) for node in core_nodes
    }
    moments: dict[int, tuple[Q, list[Q]]] = {}
    for degree in (1, 3):
        moments[degree] = (
            Q(n),
            [2 * polynomials[node][degree] for node in core_nodes]
            + [Q(0), Q(0), Q(0)],
        )
    p4_half = gegenbauer_5(Q(1, 2), 4)[4]
    p4_quarter = gegenbauer_5(Q(1, 4), 4)[4]
    p4_zero = gegenbauer_5(Q(0), 4)[4]
    moments[4] = (
        Q(41 + 2 * antipode_pairs),
        [2 * polynomials[node][4] for node in core_nodes]
        + [4 * p4_half, 4 * p4_quarter, 2 * p4_zero],
    )
    return n, core_pairs, background_pairs, moments


def verify(certificate_path: Path = DEFAULT_CERTIFICATE) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    check(
        certificate["schema"]
        == "kissing5.quarter_grid_antipodal_pair_moment_obstruction.v1",
        "unexpected certificate schema",
    )
    check(certificate["cardinality"] == 41, "cardinality must be 41")
    check(certificate["grid_denominator"] == 4, "grid must be quarter")
    check(certificate["rank_bound"] == 5, "rank bound must be five")
    check(
        certificate["core_numerators"] == list(range(-3, 3)),
        "core node list is wrong",
    )
    check(
        certificate["background_variables"] == ["b_2", "b_1", "b_0"],
        "background variable order is wrong",
    )
    check(
        certificate["gegenbauer_degrees"] == [1, 3, 4],
        "harmonic degree list is wrong",
    )
    expected_multipliers = {
        "M_1": 363,
        "M_3": 960,
        "M_4": 1024,
        "core_pair_count_equality": -319,
        "background_pair_count_equality": -256,
        "off_antipode_energy_R": 140,
    }
    check(
        certificate["multipliers"] == expected_multipliers,
        "identity multiplier changed",
    )
    variable_names = [
        "c_-3",
        "c_-2",
        "c_-1",
        "c_0",
        "c_1",
        "c_2",
        "b_2",
        "b_1",
        "b_0",
    ]
    expected_coefficients = [
        Q(0),
        Q(-126),
        Q(0),
        Q(-63),
        Q(-252),
        Q(0),
        Q(0),
        Q(-126),
        Q(0),
    ]
    check(
        certificate["identity_variable_coefficients"]
        == dict(zip(variable_names, map(int, expected_coefficients))),
        "recorded identity coefficient changed",
    )

    rank_lower = Q(11808, 5)
    check(
        Q(certificate["rank_energy_lower_bound_Q"]) == rank_lower,
        "rank energy lower bound is wrong",
    )
    branch_results = []
    branches = certificate["excluded_antipode_pair_branches"]
    check(
        [branch["r"] for branch in branches] == [14, 15, 16],
        "branch list must be exactly 14,15,16",
    )
    for branch in branches:
        antipode_pairs = int(branch["r"])
        n, core_pairs, background_pairs, moments = branch_affine_data(
            antipode_pairs
        )
        constant = Q(0)
        coefficients = [Q(0) for _ in variable_names]
        for degree, multiplier in ((1, 363), (3, 960), (4, 1024)):
            constant, coefficients = add_scaled(
                constant,
                coefficients,
                Q(multiplier),
                *moments[degree],
            )

        # -319(sum c-C)
        constant += Q(319 * core_pairs)
        for index in range(6):
            coefficients[index] -= 319
        # -256(2b2+2b1+b0-B)
        constant += Q(256 * background_pairs)
        coefficients[6] -= 512
        coefficients[7] -= 512
        coefficients[8] -= 256
        # +140 R, where
        # R=sum m^2 c_m+8b2+2b1.
        for index, numerator in enumerate(range(-3, 3)):
            coefficients[index] += 140 * numerator * numerator
        coefficients[6] += 1120
        coefficients[7] += 280

        check(
            coefficients == expected_coefficients,
            f"symbolic identity failed in branch r={antipode_pairs}",
        )
        expected_constant = (
            1323 * n
            + 1024 * (41 + 2 * antipode_pairs)
            + 319 * core_pairs
            + 256 * background_pairs
        )
        check(
            constant == expected_constant,
            f"closed constant formula failed in branch r={antipode_pairs}",
        )
        energy_upper = Q(16 * antipode_pairs) + constant / 140
        rank_gap = rank_lower - energy_upper
        check(
            n == branch["unpaired_points_n"],
            f"unpaired count mismatch in branch r={antipode_pairs}",
        )
        check(
            core_pairs == branch["core_pairs_C"],
            f"core pair count mismatch in branch r={antipode_pairs}",
        )
        check(
            background_pairs == branch["background_pairs_B"],
            f"background count mismatch in branch r={antipode_pairs}",
        )
        check(
            constant == branch["identity_constant_K"],
            f"recorded identity constant mismatch in branch r={antipode_pairs}",
        )
        check(
            energy_upper == Q(branch["energy_upper_bound_Q"]),
            f"energy upper bound mismatch in branch r={antipode_pairs}",
        )
        check(
            rank_gap == Q(branch["rank_gap"]) > 0,
            f"rank gap is not strictly positive in branch r={antipode_pairs}",
        )
        branch_results.append(
            {
                "r": antipode_pairs,
                "energy_upper_bound_Q": str(energy_upper),
                "rank_gap": str(rank_gap),
            }
        )
    return {
        "branches_verified": branch_results,
        "identity_coefficients": list(map(str, expected_coefficients)),
        "rank_energy_lower_bound_Q": str(rank_lower),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate", nargs="?", type=Path, default=DEFAULT_CERTIFICATE
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
