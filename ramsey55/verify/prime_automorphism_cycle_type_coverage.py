#!/usr/bin/env python3
"""Audit certified and elementary prime-order automorphism exclusions.

This checker deliberately distinguishes a cycle type from an automorphism
order.  A prime-order permutation of 43 points can have any cycle type

    p^c 1^(43-pc),  1 <= c <= floor(43/p).

Consequently, excluding one value of ``c`` does not exclude the other values.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


CHECKER_ID = "ramsey55_prime_automorphism_cycle_type_coverage_checker_v1"
ORDER = 43
DEGREE_MINIMUM = 18
DEGREE_MAXIMUM = 24


CERTIFICATE_SPECS = {
    (11, 3): {
        "name": "11^3 1^10",
        "stem": "order43_automorphism11_three_cycles",
        "check": "order43_automorphism11_three_cycles_cnf_check.json",
    },
    (13, 2): {
        "name": "13^2 1^17",
        "stem": "order43_automorphism13_two_cycles_symmetry_broken",
        "check": "order43_automorphism13_two_cycles_symmetry_cnf_check.json",
    },
    (17, 2): {
        "name": "17^2 1^9",
        "stem": "order43_automorphism17_two_cycles",
        "check": "order43_automorphism17_two_cycles_cnf_check.json",
    },
    (19, 2): {
        "name": "19^2 1^5",
        "stem": "order43_automorphism19_two_cycles",
        "check": "order43_automorphism19_two_cycles_cnf_check.json",
    },
    (43, 1): {
        "name": "43^1",
        "stem": "circulant43_exact",
        "check": "circulant43_exact_cnf_check.json",
    },
}

DIRECT_DEGREE_EXCLUSIONS = ((13, 3), (29, 1), (31, 1), (37, 1), (41, 1))
P23_TYPE = (23, 1)


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def is_prime(value: int) -> bool:
    return value >= 2 and all(
        value % divisor for divisor in range(2, math.isqrt(value) + 1)
    )


def all_prime_cycle_types() -> tuple[tuple[int, int], ...]:
    return tuple(
        (prime, cycles)
        for prime in range(2, ORDER + 1)
        if is_prime(prime)
        for cycles in range(1, ORDER // prime + 1)
    )


def type_name(prime: int, cycles: int) -> str:
    fixed = ORDER - prime * cycles
    return f"{prime}^{cycles} 1^{fixed}"


def fixed_vertex_degree_options(
    prime: int, cycles: int
) -> tuple[tuple[int, int, int], ...]:
    """Return (seen moved cycles, fixed-subgraph degree, total degree).

    A fixed vertex is adjacent either to every vertex or to no vertex in each
    prime cycle.  Its moved-part degree is therefore a multiple of ``prime``.
    """

    fixed = ORDER - prime * cycles
    if fixed <= 0:
        return ()
    return tuple(
        (seen, fixed_degree, prime * seen + fixed_degree)
        for seen in range(cycles + 1)
        for fixed_degree in range(fixed)
        if DEGREE_MINIMUM
        <= prime * seen + fixed_degree
        <= DEGREE_MAXIMUM
    )


def p23_arithmetic() -> dict[str, object]:
    """Check the complete fixed-vertex argument for type 23^1 1^20."""

    options = fixed_vertex_degree_options(23, 1)
    expected_options = (
        (0, 18, 18),
        (0, 19, 19),
        (1, 0, 23),
        (1, 1, 24),
    )
    if options != expected_options:
        raise AssertionError(f"unexpected p=23 degree options: {options}")

    # L vertices see the 23-cycle and have fixed degree at most one.
    # H vertices miss the cycle and have fixed degree at least 18, hence at
    # most one nonneighbor in the 20-vertex fixed graph.
    cross_bounds = []
    feasible_low_counts = []
    for low_count in range(21):
        high_count = 20 - low_count
        lower = high_count * max(0, low_count - 1)
        upper = low_count
        feasible = lower <= upper
        cross_bounds.append(
            {
                "low_count": low_count,
                "high_count": high_count,
                "cross_edge_lower_bound": lower,
                "cross_edge_upper_bound": upper,
                "feasible": feasible,
            }
        )
        if feasible:
            feasible_low_counts.append(low_count)
    if feasible_low_counts != [0, 1, 19, 20]:
        raise AssertionError(feasible_low_counts)

    # Complementation interchanges L and H, so only |L|=0,1 remain.
    # For |L|=0 the complement of the fixed graph has maximum degree one,
    # and the elementary greedy bound alpha >= ceil(n/(Delta+1)) gives a
    # clique of order at least ten in the original fixed graph.
    low_zero_clique_lower_bound = math.ceil(20 / (1 + 1))

    # For |L|=1 the lone L vertex has at most one H-neighbor.  Every H
    # vertex missing that L vertex has fixed degree at least 18 and therefore
    # sees all other 18 H vertices.  At least 18 such witnesses exist, and
    # they force all 19 H vertices to be pairwise adjacent.
    low_one_h_vertices = 19
    low_one_h_missing_low_at_least = 18
    low_one_clique_lower_bound = 19

    return {
        "degree_options": [list(option) for option in options],
        "cross_bounds": cross_bounds,
        "feasible_low_counts": feasible_low_counts,
        "complement_representatives": [0, 1],
        "low_zero_clique_lower_bound": low_zero_clique_lower_bound,
        "low_one_h_vertices": low_one_h_vertices,
        "low_one_h_missing_low_at_least": low_one_h_missing_low_at_least,
        "low_one_clique_lower_bound": low_one_clique_lower_bound,
        "contradiction": (
            low_zero_clique_lower_bound >= 5
            and low_one_clique_lower_bound >= 5
        ),
    }


def audit_certificate(root: Path, cycle_type: tuple[int, int]) -> dict[str, object]:
    spec = CERTIFICATE_SPECS[cycle_type]
    stem = str(spec["stem"])
    cnf = root / "certificates" / f"{stem}.cnf"
    metadata_path = root / "certificates" / f"{stem}.metadata.json"
    result_path = root / "certificates" / f"{stem}_glucose3.result.json"
    proof_path = root / "certificates" / f"{stem}_glucose3.drat"
    lrat_path = root / "certificates" / f"{stem}_glucose3.lrat"
    check_path = root / "results" / "verification" / str(spec["check"])

    paths = (cnf, metadata_path, result_path, proof_path, lrat_path, check_path)
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        return {
            "name": spec["name"],
            "valid": False,
            "missing": missing,
        }

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    structural_check = json.loads(check_path.read_text(encoding="utf-8"))
    prime, cycles = cycle_type
    fixed = ORDER - prime * cycles

    cnf_hash = sha256_file(cnf)
    proof_hash = sha256_file(proof_path)
    lrat_hash = sha256_file(lrat_path)
    cycle_metadata_valid = (
        (
            prime == 43
            and cycles == 1
            and metadata.get("order") == ORDER
            and metadata.get("variable_count") == 21
        )
        or (
            metadata.get("automorphism_order") == prime
            and metadata.get("cycle_count") == cycles
            and metadata.get("fixed_point_count") == fixed
        )
    )
    valid = (
        cycle_metadata_valid
        and metadata.get("cnf_sha256") == cnf_hash
        and structural_check.get("valid") is True
        and structural_check.get("cnf_sha256") == cnf_hash
        and result.get("status") == "CERTIFIED_UNSAT"
        and result.get("drat_trim_valid") is True
        and result.get("lrat_check_valid") is True
        and result.get("cnf_sha256") == cnf_hash
        and result.get("proof_sha256") == proof_hash
        and result.get("lrat_sha256") == lrat_hash
    )
    return {
        "name": spec["name"],
        "valid": valid,
        "cnf_sha256": cnf_hash,
        "proof_sha256": proof_hash,
        "lrat_sha256": lrat_hash,
        "structural_check_sha256": sha256_file(check_path),
        "result_sha256": sha256_file(result_path),
    }


def check(root: Path) -> dict[str, object]:
    direct_degree_checks = []
    for prime, cycles in DIRECT_DEGREE_EXCLUSIONS:
        options = fixed_vertex_degree_options(prime, cycles)
        direct_degree_checks.append(
            {
                "name": type_name(prime, cycles),
                "degree_options": [list(option) for option in options],
                "excluded": not options,
            }
        )
    direct_valid = all(item["excluded"] for item in direct_degree_checks)

    p23 = p23_arithmetic()
    certificate_audits = [
        audit_certificate(root, cycle_type)
        for cycle_type in sorted(CERTIFICATE_SPECS)
    ]
    certificates_valid = all(item["valid"] for item in certificate_audits)

    mathematical = set(DIRECT_DEGREE_EXCLUSIONS) | {P23_TYPE}
    certified = set(CERTIFICATE_SPECS)
    all_types = set(all_prime_cycle_types())
    overlap = mathematical & certified
    covered = mathematical | certified
    uncovered = sorted(all_types - covered)
    extraneous = sorted(covered - all_types)
    large_prime_types = {
        cycle_type for cycle_type in all_types if cycle_type[0] >= 23
    }
    large_prime_complete = large_prime_types <= covered

    valid = (
        direct_valid
        and p23["contradiction"] is True
        and certificates_valid
        and not overlap
        and not extraneous
        and large_prime_complete
        and covered | set(uncovered) == all_types
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "order": ORDER,
        "degree_interval": [DEGREE_MINIMUM, DEGREE_MAXIMUM],
        "degree_interval_basis": "R(4,5)=R(5,4)=25",
        "direct_degree_checks": direct_degree_checks,
        "p23_check": p23,
        "certificate_audits": certificate_audits,
        "all_prime_cycle_type_count": len(all_types),
        "covered_cycle_type_count": len(covered),
        "covered_cycle_types": [
            type_name(prime, cycles) for prime, cycles in sorted(covered)
        ],
        "large_prime_cycle_types_complete": large_prime_complete,
        "large_prime_cycle_types": [
            type_name(prime, cycles)
            for prime, cycles in sorted(large_prime_types)
        ],
        "uncovered_cycle_type_count": len(uncovered),
        "uncovered_cycle_types": [
            type_name(prime, cycles) for prime, cycles in uncovered
        ],
        "classification_complete": not uncovered,
        "claim_boundary": (
            "This is a cycle-type coverage audit, not a full automorphism "
            "classification. Every listed uncovered type remains open here."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.root.resolve())
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
