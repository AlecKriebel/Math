#!/usr/bin/env python3
"""Independent checker for the order-43 min/max-degree cover artifact.

This checker does not import the production cover or direct-CNF generator.
It reconstructs the edge map, sequential-counter allocation, branch units,
cover cases, and threshold semantics independently.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Sequence


CHECKER_ID = "ramsey55.global_minmax_degree_cover_checker.v1"
SCHEMA = "ramsey55.global_minmax_degree_cover.v1"
ORDER = 43
LOWER = 18
UPPER = 24
BRANCHES = (18, 19, 20)
BASE_CNF_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
BASE_METADATA_SHA256 = (
    "88906686b2554cf1b5b9051eae4a200b878944278ed91682b78d9f40d43cf70c"
)


def units_sha256(units: Sequence[int]) -> str:
    value = "".join(f"{literal} 0\n" for literal in units).encode("ascii")
    return hashlib.sha256(value).hexdigest()


def independent_edge_map() -> dict[tuple[int, int], int]:
    return {
        pair: variable
        for variable, pair in enumerate(
            itertools.combinations(range(ORDER), 2), start=1
        )
    }


def allocate_final_thresholds(
    next_variable: int, input_count: int, bound: int
) -> tuple[tuple[int, ...], int]:
    width = bound + 1
    rows: list[tuple[int, ...]] = []
    for prefix in range(1, input_count + 1):
        row_width = min(prefix, width)
        rows.append(tuple(range(next_variable, next_variable + row_width)))
        next_variable += row_width
    return rows[-1], next_variable


def independent_counter_finals() -> tuple[list[tuple[int, ...]], int]:
    next_variable = math.comb(ORDER, 2) + 1
    finals: list[tuple[int, ...]] = []
    for _vertex in range(ORDER):
        edge_final, next_variable = allocate_final_thresholds(
            next_variable, ORDER - 1, UPPER
        )
        finals.append(edge_final)
        nonedge_final, next_variable = allocate_final_thresholds(
            next_variable, ORDER - 1, ORDER - 1 - LOWER
        )
        finals.append(nonedge_final)
    return finals, next_variable - 1


def expected_units(degree: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    edge_map = independent_edge_map()
    star = tuple(
        (
            edge_map[(0, other)]
            if other <= degree
            else -edge_map[(0, other)]
        )
        for other in range(1, ORDER)
    )
    strict: tuple[int, ...] = ()
    if degree > LOWER:
        finals, _ = independent_counter_finals()
        threshold = ORDER - degree
        strict = tuple(
            -finals[2 * vertex + kind][threshold - 1]
            for vertex in range(ORDER)
            for kind in (0, 1)
        )
    return star, strict


def threshold_semantics_valid(degree: int) -> bool:
    """Check every possible primary degree against the assumed thresholds."""

    threshold = ORDER - degree
    for observed_degree in range(ORDER):
        base_accepts = LOWER <= observed_degree <= UPPER
        if degree == LOWER:
            assumptions_accept = True
        else:
            edge_threshold_false = observed_degree < threshold
            nonedges = ORDER - 1 - observed_degree
            nonedge_threshold_false = nonedges < threshold
            assumptions_accept = edge_threshold_false and nonedge_threshold_false
        expected = degree <= observed_degree <= ORDER - 1 - degree
        if (base_accepts and assumptions_accept) != expected:
            return False
    return True


def cover_table() -> list[dict[str, int | str]]:
    rows: list[dict[str, int | str]] = []
    for minimum in range(LOWER, UPPER + 1):
        for maximum in range(minimum, UPPER + 1):
            parameter = min(minimum, ORDER - 1 - maximum)
            if parameter == 21:
                outcome = "HANDSHAKE_PARITY"
            elif parameter in BRANCHES:
                outcome = f"BRANCH_{parameter}"
            else:
                outcome = "INVALID"
            rows.append(
                {
                    "minimum": minimum,
                    "maximum": maximum,
                    "parameter": parameter,
                    "outcome": outcome,
                }
            )
    return rows


def check(plan_path: Path, base_cnf: Path, base_metadata: Path) -> dict[str, object]:
    plan_bytes = plan_path.read_bytes()
    plan = json.loads(plan_bytes)
    errors: list[str] = []

    if plan.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if plan.get("order") != ORDER:
        errors.append("order mismatch")
    if plan.get("base_cnf_sha256") != BASE_CNF_SHA256:
        errors.append("plan base CNF hash mismatch")
    if plan.get("base_metadata_sha256") != BASE_METADATA_SHA256:
        errors.append("plan base metadata hash mismatch")

    actual_cnf_sha = hashlib.sha256(base_cnf.read_bytes()).hexdigest()
    actual_metadata_sha = hashlib.sha256(base_metadata.read_bytes()).hexdigest()
    if actual_cnf_sha != BASE_CNF_SHA256:
        errors.append("actual base CNF hash mismatch")
    if actual_metadata_sha != BASE_METADATA_SHA256:
        errors.append("actual base metadata hash mismatch")

    finals, expected_variable_count = independent_counter_finals()
    if expected_variable_count != 65_403:
        errors.append("independent counter variable count mismatch")
    if len(finals) != 86 or any(len(row) != 25 for row in finals):
        errors.append("independent counter layout mismatch")

    records = plan.get("branches")
    if not isinstance(records, list) or len(records) != len(BRANCHES):
        errors.append("branch record count mismatch")
        records = []
    semantic_results: dict[str, bool] = {}
    for degree, record in zip(BRANCHES, records):
        if not isinstance(record, dict) or record.get("degree") != degree:
            errors.append(f"branch {degree} identity mismatch")
            continue
        star, strict = expected_units(degree)
        all_units = star + strict
        expected = {
            "degree_interval": [degree, ORDER - 1 - degree],
            "star_unit_count": len(star),
            "additional_degree_unit_count": len(strict),
            "total_assumption_count": len(all_units),
            "star_units_sha256": units_sha256(star),
            "additional_degree_units_sha256": units_sha256(strict),
            "all_units_sha256": units_sha256(all_units),
        }
        for key, value in expected.items():
            if record.get(key) != value:
                errors.append(f"branch {degree} field mismatch: {key}")
        semantic_results[str(degree)] = threshold_semantics_valid(degree)
        if not semantic_results[str(degree)]:
            errors.append(f"branch {degree} threshold semantics fail")

    parity = plan.get("parity_elimination")
    if not isinstance(parity, dict):
        errors.append("missing parity record")
    else:
        if parity.get("parameter") != 21:
            errors.append("parity parameter mismatch")
        if parity.get("forced_degree_sequence") != [21] * ORDER:
            errors.append("parity degree sequence mismatch")
        if parity.get("degree_sum") != 903 or 903 % 2 != 1:
            errors.append("parity sum mismatch")

    table = cover_table()
    if any(row["outcome"] == "INVALID" for row in table):
        errors.append("minimum/maximum cover is not exhaustive")
    parity_rows = [row for row in table if row["parameter"] == 21]
    if parity_rows != [
        {
            "minimum": 21,
            "maximum": 21,
            "parameter": 21,
            "outcome": "HANDSHAKE_PARITY",
        }
    ]:
        errors.append("parity is not the unique uncovered degree pair")

    catalog = plan.get("optional_degree18_catalog_split")
    if not isinstance(catalog, dict):
        errors.append("missing catalog split record")
    else:
        expected_catalog = {
            "catalog_sha256": (
                "83ca4028f206b2fa4315ef219b8c2c57c"
                "7835209673dd8183d8fb4353bd4fdd0"
            ),
            "catalog_record_count": 352_366,
            "fixed_star_primary_variables": 42,
            "fixed_antineighborhood_primary_variables": 276,
            "remaining_primary_variables_per_catalog_cube": 585,
        }
        for key, value in expected_catalog.items():
            if catalog.get(key) != value:
                errors.append(f"catalog split field mismatch: {key}")

    return {
        "checker": CHECKER_ID,
        "checker_source_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "valid": not errors,
        "errors": errors,
        "plan_sha256": hashlib.sha256(plan_bytes).hexdigest(),
        "base_cnf_sha256": actual_cnf_sha,
        "base_metadata_sha256": actual_metadata_sha,
        "independent_variable_count": expected_variable_count,
        "independent_counter_final_row_count": len(finals),
        "cover_degree_pair_count": len(table),
        "cover_table": table,
        "threshold_semantics": semantic_results,
        "parity_case_count": len(parity_rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--base-metadata", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.plan, args.base_cnf, args.base_metadata)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
