#!/usr/bin/env python3
"""Independent checker for selector-union order-5 cover CNFs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import subprocess
import sys
import time
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from automorphism_orbit_cnf_check import (  # noqa: E402
    independently_build,
    read_dimacs,
)


CHECKER_ID = "ramsey55_order5_selector_union_independent_checker_v1"
ORDER = 43
PRIME = 5
CYCLES = 8
FIXED = (40, 41, 42)
HARD_COUNTS = (1,) * 8
BASE_VARIABLES = 183
BASE_CLAUSES = 384_108


class CheckError(RuntimeError):
    """The cover, formula, or proof chain failed verification."""


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def edge_variable_from_orbits(
    orbits: Sequence[Sequence[tuple[int, int]]],
) -> dict[tuple[int, int], int]:
    return {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }


def membership_counts(
    subsets: tuple[frozenset[int], frozenset[int], frozenset[int]],
) -> tuple[int, ...]:
    counts = [0] * 8
    for cycle in range(CYCLES):
        mask = sum(
            (cycle in subset) << coordinate
            for coordinate, subset in enumerate(subsets)
        )
        counts[mask] += 1
    return tuple(counts)


def permute_coordinates(
    counts: tuple[int, ...], coordinate_order: tuple[int, int, int]
) -> tuple[int, ...]:
    transformed = [0] * 8
    for old_mask, count in enumerate(counts):
        new_mask = sum(
            ((old_mask >> coordinate_order[new_coordinate]) & 1)
            << new_coordinate
            for new_coordinate in range(3)
        )
        transformed[new_mask] = count
    return tuple(transformed)


def independent_type_schedule(
    include_hard: bool,
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    first = frozenset(range(4))
    four_subsets = tuple(
        frozenset(subset) for subset in itertools.combinations(range(8), 4)
    )
    result: list[tuple[str, tuple[int, ...]]] = []
    groups = {
        "edgeless": tuple(itertools.permutations(range(3))),
        "one_edge": ((0, 1, 2), (1, 0, 2)),
    }
    for fixed_pattern in ("edgeless", "one_edge"):
        group = groups[fixed_pattern]
        representatives = {
            min(
                permute_coordinates(
                    membership_counts((first, second, third)), order
                )
                for order in group
            )
            for second in four_subsets
            for third in four_subsets
        }
        for counts in sorted(representatives):
            if (
                include_hard
                or fixed_pattern != "one_edge"
                or counts != HARD_COUNTS
            ):
                result.append((fixed_pattern, counts))
    return tuple(result)


def subsets_from_counts(
    counts: tuple[int, ...],
) -> tuple[frozenset[int], frozenset[int], frozenset[int]]:
    masks = [
        mask
        for wanted_first_bit in (1, 0)
        for mask, count in enumerate(counts)
        if bool(mask & 1) == bool(wanted_first_bit)
        for _ in range(count)
    ]
    subsets = tuple(
        frozenset(
            cycle for cycle, mask in enumerate(masks) if (mask >> axis) & 1
        )
        for axis in range(3)
    )
    if (
        len(masks) != 8
        or tuple(map(len, subsets)) != (4, 4, 4)
        or subsets[0] != frozenset(range(4))
        or membership_counts(subsets) != counts
    ):
        raise CheckError("failed to realize a membership-count representative")
    return subsets  # type: ignore[return-value]


def independent_assumptions(
    fixed_pattern: str,
    counts: tuple[int, ...],
    edge_variable: Mapping[tuple[int, int], int],
) -> tuple[int, ...]:
    subsets = subsets_from_counts(counts)
    assignments: dict[int, bool] = {
        edge_variable[(40, 41)]: fixed_pattern == "one_edge",
        edge_variable[(40, 42)]: False,
        edge_variable[(41, 42)]: False,
    }
    for axis, fixed_vertex in enumerate(FIXED):
        for cycle in range(CYCLES):
            assignments[edge_variable[(5 * cycle, fixed_vertex)]] = (
                cycle in subsets[axis]
            )
    if len(assignments) != 27:
        raise CheckError("ordinary type does not assign 27 variables")
    return tuple(
        variable if value else -variable
        for variable, value in sorted(assignments.items())
    )


def normalized_fixed_graph_cover() -> dict[str, object]:
    edges = ((0, 1), (0, 2), (1, 2))
    targets = {(False, False, False), (True, False, False)}
    records = []
    for bits in itertools.product((False, True), repeat=3):
        normalized = False
        for complement in (False, True):
            values = {
                edge: bits[index] ^ complement
                for index, edge in enumerate(edges)
            }
            for permutation in itertools.permutations(range(3)):
                transformed = tuple(
                    values[tuple(sorted((permutation[left], permutation[right])))]
                    for left, right in edges
                )
                if transformed in targets:
                    normalized = True
                    break
            if normalized:
                break
        records.append({"fixed_graph_bits": list(bits), "covered": normalized})
    return {
        "labeled_fixed_graph_count": 8,
        "normalized_patterns": ["edgeless", "one_edge"],
        "records": records,
        "valid": all(record["covered"] for record in records),
    }


def degree_normalization() -> dict[str, object]:
    possibilities = {
        fixed_degree: [
            moved_cycles
            for moved_cycles in range(9)
            if 18 <= 5 * moved_cycles + fixed_degree <= 24
        ]
        for fixed_degree in range(3)
    }
    return {
        "degree_interval": [18, 24],
        "possibilities": {
            str(fixed_degree): values
            for fixed_degree, values in possibilities.items()
        },
        "valid": all(values == [4] for values in possibilities.values()),
    }


def independent_orientations() -> tuple[tuple[bool, ...], ...]:
    subsets = subsets_from_counts(HARD_COUNTS)
    masks = tuple(
        sum(
            (cycle in subset) << axis
            for axis, subset in enumerate(subsets)
        )
        for cycle in range(8)
    )
    cycle_of_mask = {mask: cycle for cycle, mask in enumerate(masks)}

    def endpoint_swap(bits: tuple[bool, ...]) -> tuple[bool, ...]:
        result = [False] * 8
        for old_cycle, mask in enumerate(masks):
            swapped_mask = (
                (mask & ~3)
                | ((mask & 1) << 1)
                | ((mask & 2) >> 1)
            )
            result[cycle_of_mask[swapped_mask]] = bits[old_cycle]
        return tuple(result)

    representatives = set()
    covered = set()
    for bits in itertools.product((False, True), repeat=8):
        swapped = endpoint_swap(bits)
        orbit = {
            bits,
            swapped,
            tuple(not value for value in bits),
            tuple(not value for value in swapped),
        }
        representatives.add(min(orbit))
        covered.update(orbit)
    result = tuple(sorted(representatives))
    if len(result) != 80 or len(covered) != 256:
        raise CheckError("internal-orientation quotient is incomplete")
    return result


def independent_internal_assumptions(
    orientation: Sequence[bool],
    edge_variable: Mapping[tuple[int, int], int],
) -> tuple[int, ...]:
    literals: list[int] = []
    for cycle, second_distance in enumerate(orientation):
        base = 5 * cycle
        first = edge_variable[(base, base + 1)]
        second = edge_variable[(base, base + 2)]
        literals.extend(
            (
                -first if second_distance else first,
                second if second_distance else -second,
            )
        )
    if len(literals) != 16 or len(set(map(abs, literals))) != 16:
        raise CheckError("internal orientation does not assign 16 variables")
    return tuple(literals)


def shift_literal(literal: int, offset: int) -> int:
    return (abs(literal) + offset) * (1 if literal > 0 else -1)


def expected_ordinary_formula(
    metadata: Mapping[str, object],
) -> tuple[tuple[int, ...], ...]:
    _, orbits, base_clauses = independently_build(5, 8)
    edge_variable = edge_variable_from_orbits(orbits)
    schedule = independent_type_schedule(include_hard=False)
    if len(schedule) != 58:
        raise CheckError("ordinary schedule is not exactly 58 types")
    leaves = metadata.get("leaves")
    if not isinstance(leaves, list) or len(leaves) != 58:
        raise CheckError("metadata leaf schedule is not exactly 58 records")
    offset = 58
    expected: list[tuple[int, ...]] = [
        tuple(shift_literal(literal, offset) for literal in clause)
        for clause in base_clauses
    ]
    selectors = []
    for index, ((fixed_pattern, counts), leaf) in enumerate(
        zip(schedule, leaves, strict=True)
    ):
        if not isinstance(leaf, dict):
            raise CheckError("malformed metadata leaf")
        selector = index + 1
        assumptions = independent_assumptions(
            fixed_pattern, counts, edge_variable
        )
        if (
            leaf.get("kind") != "type"
            or leaf.get("index") != index
            or leaf.get("fixed_pattern") != fixed_pattern
            or leaf.get("membership_counts") != list(counts)
            or leaf.get("internal_orientation") is not None
            or leaf.get("assumptions") != list(assumptions)
            or leaf.get("selector_variable") != selector
        ):
            raise CheckError(f"metadata leaf {index} is not independently exact")
        selectors.append(selector)
        expected.extend(
            (-selector, shift_literal(literal, offset))
            for literal in assumptions
        )
    expected.extend(
        (-first, -second)
        for first, second in itertools.combinations(selectors, 2)
    )
    expected.append(tuple(selectors))
    return tuple(expected)


def expected_orientation_formula(
    metadata: Mapping[str, object],
    *,
    independent_orbits: Sequence[Sequence[tuple[int, int]]] | None = None,
    independent_base_clauses: Sequence[Sequence[int]] | None = None,
) -> tuple[tuple[int, ...], ...]:
    if independent_orbits is None or independent_base_clauses is None:
        _, built_orbits, built_base_clauses = independently_build(5, 8)
        orbits = built_orbits
        base_clauses = built_base_clauses
    else:
        orbits = independent_orbits
        base_clauses = independent_base_clauses
    edge_variable = edge_variable_from_orbits(orbits)
    orientations = independent_orientations()
    batch_start = metadata.get("batch_start")
    batch_count = metadata.get("batch_count")
    if type(batch_start) is not int or type(batch_count) is not int:
        raise CheckError("orientation batch bounds are malformed")
    chosen = orientations[batch_start : batch_start + batch_count]
    if len(chosen) != batch_count or not chosen:
        raise CheckError("orientation batch bounds are outside the schedule")
    leaves = metadata.get("leaves")
    if not isinstance(leaves, list) or len(leaves) != len(chosen):
        raise CheckError("metadata orientation schedule has the wrong size")

    offset = len(chosen)
    expected: list[tuple[int, ...]] = [
        tuple(shift_literal(literal, offset) for literal in clause)
        for clause in base_clauses
    ]
    fixed = independent_assumptions(
        "one_edge", HARD_COUNTS, edge_variable
    )
    selectors = []
    for local_index, (orientation, leaf) in enumerate(
        zip(chosen, leaves, strict=True)
    ):
        if not isinstance(leaf, dict):
            raise CheckError("malformed orientation metadata leaf")
        global_index = batch_start + local_index
        selector = local_index + 1
        assumptions = (
            *fixed,
            *independent_internal_assumptions(
                orientation, edge_variable
            ),
        )
        if (
            leaf.get("kind") != "orientation"
            or leaf.get("index") != global_index
            or leaf.get("fixed_pattern") != "one_edge"
            or leaf.get("membership_counts") != [1] * 8
            or leaf.get("internal_orientation")
            != [int(value) for value in orientation]
            or leaf.get("assumptions") != list(assumptions)
            or leaf.get("selector_variable") != selector
        ):
            raise CheckError(
                f"orientation metadata leaf {global_index} is not exact"
            )
        selectors.append(selector)
        expected.extend(
            (-selector, shift_literal(literal, offset))
            for literal in assumptions
        )
    expected.extend(
        (-first, -second)
        for first, second in itertools.combinations(selectors, 2)
    )
    expected.append(tuple(selectors))
    return tuple(expected)


def says_verified(output: str) -> bool:
    return any(
        "VERIFIED" in line and "NOT VERIFIED" not in line
        for line in output.splitlines()
    )


def run_proof_check(
    cnf: Path,
    proof: Path,
    lrat: Path,
    drat_trim: Path,
    lrat_check: Path,
) -> dict[str, object]:
    started = time.monotonic()
    drat = subprocess.run(
        (str(drat_trim), str(cnf), str(proof)),
        text=True,
        capture_output=True,
        check=False,
    )
    drat_output = drat.stdout + drat.stderr
    checked = subprocess.run(
        (str(lrat_check), str(cnf), str(lrat)),
        text=True,
        capture_output=True,
        check=False,
    )
    lrat_output = checked.stdout + checked.stderr
    return {
        "drat_trim_valid": drat.returncode == 0
        and says_verified(drat_output),
        "drat_trim_returncode": drat.returncode,
        "drat_trim_output": drat_output,
        "lrat_check_valid": checked.returncode == 0
        and says_verified(lrat_output),
        "lrat_check_returncode": checked.returncode,
        "lrat_check_output": lrat_output,
        "proof_check_runtime_seconds": time.monotonic() - started,
    }


def check(
    cnf: Path,
    metadata_path: Path,
    proof: Path | None = None,
    lrat: Path | None = None,
    worker_path: Path | None = None,
    drat_trim: Path | None = None,
    lrat_check: Path | None = None,
) -> dict[str, object]:
    started = time.monotonic()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    portion = metadata.get("portion")
    if portion == "ordinary":
        expected = expected_ordinary_formula(metadata)
        selector_count = 58
    elif portion == "orientations":
        expected = expected_orientation_formula(metadata)
        selector_count = int(metadata["batch_count"])
    else:
        raise CheckError("checker accepts ordinary or orientation batches only")
    variables, declared, actual = read_dimacs(cnf)
    first_mismatch = None
    for index, pair in enumerate(
        itertools.zip_longest(expected, actual), start=1
    ):
        if pair[0] != pair[1]:
            first_mismatch = {
                "clause_index": index,
                "expected": list(pair[0]) if pair[0] is not None else None,
                "actual": list(pair[1]) if pair[1] is not None else None,
            }
            break

    fixed_graph = normalized_fixed_graph_cover()
    degree = degree_normalization()
    full_schedule = independent_type_schedule(include_hard=True)
    ordinary_schedule = independent_type_schedule(include_hard=False)
    orientation_count = len(independent_orientations())
    cnf_hash = sha256_file(cnf)
    common_metadata_valid = (
        metadata.get("cycle_type") == "5^8 1^3"
        and metadata.get("selectors_first") is True
        and metadata.get("base_variable_offset") == selector_count
        and metadata.get("base_variable_count") == BASE_VARIABLES
        and metadata.get("base_clause_count") == BASE_CLAUSES
        and metadata.get("selector_variable_count") == selector_count
        and metadata.get("variable_count") == BASE_VARIABLES + selector_count
        and metadata.get("clause_count") == len(expected)
        and metadata.get("ordinary_type_leaf_count") == 58
        and metadata.get("hard_orientation_leaf_count") == 80
        and metadata.get("total_leaf_count") == selector_count
        and metadata.get("omitted_hard_type")
        == {
            "fixed_pattern": "one_edge",
            "membership_counts": [1] * 8,
        }
        and metadata.get("cnf_sha256") == cnf_hash
        and metadata.get("cnf_bytes") == cnf.stat().st_size
    )
    metadata_valid = common_metadata_valid and (
        (
            portion == "ordinary"
            and selector_count == 58
            and metadata.get("batch_start") == 0
        )
        or (
            portion == "orientations"
            and type(metadata.get("batch_start")) is int
            and 0 <= int(metadata["batch_start"]) < 80
            and int(metadata["batch_start"]) + selector_count <= 80
        )
    )
    structural_valid = (
        variables == BASE_VARIABLES + selector_count
        and declared == len(expected)
        and actual == expected
        and metadata_valid
        and fixed_graph["valid"] is True
        and degree["valid"] is True
        and len(full_schedule) == 59
        and len(ordinary_schedule) == 58
        and ("one_edge", HARD_COUNTS) in full_schedule
        and ("one_edge", HARD_COUNTS) not in ordinary_schedule
        and orientation_count == 80
    )

    proof_result: dict[str, object] = {
        "proof_requested": proof is not None or lrat is not None,
        "proof_valid": None,
    }
    if proof is not None or lrat is not None:
        if (
            proof is None
            or lrat is None
            or worker_path is None
            or drat_trim is None
            or lrat_check is None
        ):
            raise CheckError("complete proof-check arguments are required")
        worker = json.loads(worker_path.read_text(encoding="utf-8"))
        checks = run_proof_check(
            cnf, proof, lrat, drat_trim, lrat_check
        )
        worker_valid = (
            worker.get("status") == "UNSAT"
            and worker.get("solver") == "MapleChrono"
            and worker.get("cnf_sha256") == cnf_hash
            and worker.get("variable_count") == variables
            and worker.get("clause_count") == declared
            and worker.get("proof_sha256") == sha256_file(proof)
            and worker.get("proof_bytes") == proof.stat().st_size
        )
        proof_valid = (
            structural_valid
            and worker_valid
            and checks["drat_trim_valid"] is True
            and checks["lrat_check_valid"] is True
        )
        proof_result = {
            "proof_requested": True,
            "proof_valid": proof_valid,
            "worker_valid": worker_valid,
            "worker_sha256": sha256_file(worker_path),
            "proof_sha256": sha256_file(proof),
            "proof_bytes": proof.stat().st_size,
            "lrat_sha256": sha256_file(lrat),
            "lrat_bytes": lrat.stat().st_size,
            **checks,
        }

    valid = structural_valid and (
        proof_result["proof_valid"] is not False
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "structural_valid": structural_valid,
        "metadata_valid": metadata_valid,
        "cnf_sha256": cnf_hash,
        "cnf_bytes": cnf.stat().st_size,
        "expected_variable_count": BASE_VARIABLES + selector_count,
        "actual_variable_count": variables,
        "expected_clause_count": len(expected),
        "actual_clause_count": len(actual),
        "first_mismatch": first_mismatch,
        "fixed_graph_cover": fixed_graph,
        "degree_normalization": degree,
        "complete_structural_type_count": len(full_schedule),
        "certified_ordinary_type_count": (
            len(ordinary_schedule) if portion == "ordinary" else 0
        ),
        "certified_orientation_start": (
            metadata.get("batch_start") if portion == "orientations" else None
        ),
        "certified_orientation_count": (
            selector_count if portion == "orientations" else 0
        ),
        "omitted_hard_type": (
            "one_edge; counts=(1,1,1,1,1,1,1,1)"
            if portion == "ordinary"
            else None
        ),
        "hard_type_orientation_representative_count": orientation_count,
        "full_cycle_type_covered": False,
        "claim_boundary": (
            (
                "This formula covers exactly the 58 ordinary normalized "
                "types. The one-edge all-ones type remains outside this "
                "proof and needs its separate exact 80-orientation "
                "certificate cover."
            )
            if portion == "ordinary"
            else (
                "This formula covers exactly the recorded internal-"
                "orientation batch of the one-edge all-ones type; all other "
                "orientation representatives and the ordinary types are "
                "outside this formula."
            )
        ),
        **proof_result,
        "runtime_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--lrat", type=Path)
    parser.add_argument("--worker", type=Path)
    parser.add_argument(
        "--drat-trim",
        type=Path,
        default=Path("/tmp/ramsey55-drat-trim.x3nb3p/src/drat-trim"),
    )
    parser.add_argument(
        "--lrat-check",
        type=Path,
        default=Path("/tmp/ramsey55-drat-trim.x3nb3p/src/lrat-check"),
    )
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = check(
        args.cnf,
        args.metadata,
        args.proof,
        args.lrat,
        args.worker,
        args.drat_trim,
        args.lrat_check,
    )
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
