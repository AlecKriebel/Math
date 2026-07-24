#!/usr/bin/env python3
"""Independent checker for the exact minmax-degree-19 profile cover.

This module does not import the production profile-cover implementation or
the direct-CNF generator.  It reconstructs the profile census, complement
orbits, counter allocation, exact-degree units, selector clauses, and
materialized union stream independently.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
from pathlib import Path
from typing import Generator, Iterable, Iterator, Sequence


CHECKER_ID = "ramsey55.global_degree19_profile_cover_checker.v1"
SCHEMA = "ramsey55.global_degree19_profile_cover.v1"
ORDER = 43
DEGREES = (19, 20, 21, 22, 23)
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
EXPECTED_PROFILE_COUNT = 44_275
EXPECTED_ADMISSIBLE_COUNT = 88_550
BASE_CNF_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
BASE_METADATA_SHA256 = (
    "88906686b2554cf1b5b9051eae4a200b878944278ed91682b78d9f40d43cf70c"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def clause_hash(clauses: Iterable[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def all_exact_branch_profiles() -> Iterator[tuple[int, int, int, int, int]]:
    """Enumerate profiles by four independent coordinates."""

    for count19 in range(ORDER + 1):
        for count20 in range(ORDER - count19 + 1):
            for count21 in range(ORDER - count19 - count20 + 1):
                for count22 in range(
                    ORDER - count19 - count20 - count21 + 1
                ):
                    count23 = (
                        ORDER - count19 - count20 - count21 - count22
                    )
                    profile = (
                        count19,
                        count20,
                        count21,
                        count22,
                        count23,
                    )
                    if count19 + count23 == 0:
                        continue
                    if (count19 + count21 + count23) % 2:
                        continue
                    yield profile


def complement_profile(
    profile: Sequence[int],
) -> tuple[int, int, int, int, int]:
    if len(profile) != 5:
        raise ValueError("profile must have five multiplicities")
    return (profile[4], profile[3], profile[2], profile[1], profile[0])


def independent_profiles() -> tuple[tuple[int, int, int, int, int], ...]:
    canonical = [
        profile
        for profile in all_exact_branch_profiles()
        if (profile[0], profile[1]) > (profile[4], profile[3])
    ]
    return tuple(sorted(canonical))


def complement_orbit_audit() -> dict[str, int | bool]:
    admissible = tuple(all_exact_branch_profiles())
    canonical = frozenset(independent_profiles())
    covered: set[tuple[int, int, int, int, int]] = set()
    fixed_count = 0
    invalid_representatives = 0
    for profile in admissible:
        swapped = complement_profile(profile)
        if swapped == profile:
            fixed_count += 1
            continue
        representative = (
            profile
            if (profile[0], profile[1]) > (profile[4], profile[3])
            else swapped
        )
        if representative not in canonical:
            invalid_representatives += 1
        covered.add(profile)
    return {
        "valid": (
            len(admissible) == EXPECTED_ADMISSIBLE_COUNT
            and fixed_count == 0
            and invalid_representatives == 0
            and len(covered) == len(admissible)
            and len(canonical) == EXPECTED_PROFILE_COUNT
        ),
        "admissible_count": len(admissible),
        "fixed_count": fixed_count,
        "invalid_representative_count": invalid_representatives,
        "covered_count": len(covered),
        "canonical_count": len(canonical),
    }


def allocate_final(
    first: int, input_count: int = 42, width: int = 25
) -> tuple[tuple[int, ...], int]:
    final: tuple[int, ...] = ()
    for prefix_length in range(1, input_count + 1):
        row_width = min(prefix_length, width)
        final = tuple(range(first, first + row_width))
        first += row_width
    return final, first


def counter_finals() -> tuple[tuple[tuple[int, ...], ...], int]:
    next_variable = math.comb(ORDER, 2) + 1
    finals: list[tuple[int, ...]] = []
    for _vertex in range(ORDER):
        edge_final, next_variable = allocate_final(next_variable)
        nonedge_final, next_variable = allocate_final(next_variable)
        finals.extend((edge_final, nonedge_final))
    return tuple(finals), next_variable - 1


def independent_exact_degree_units(
    vertex: int,
    degree: int,
    finals: Sequence[Sequence[int]],
) -> tuple[int, int]:
    edge = finals[2 * vertex]
    nonedge = finals[2 * vertex + 1]
    return (-edge[degree], -nonedge[ORDER - 1 - degree])


def independent_profile_units(
    profile: Sequence[int], finals: Sequence[Sequence[int]]
) -> tuple[int, ...]:
    result: list[int] = []
    vertex = 0
    for degree, multiplicity in zip(DEGREES, profile):
        for _ in range(multiplicity):
            result.extend(
                independent_exact_degree_units(vertex, degree, finals)
            )
            vertex += 1
    if vertex != ORDER:
        raise AssertionError("profile does not cover all vertices")
    return tuple(result)


def independent_selector_clauses() -> Iterator[tuple[int, ...]]:
    canonical = independent_profiles()
    finals, variable_count = counter_finals()
    if variable_count != BASE_VARIABLE_COUNT:
        raise AssertionError("independent counter layout mismatch")
    selectors = tuple(
        range(BASE_VARIABLE_COUNT + 1, BASE_VARIABLE_COUNT + 1 + len(canonical))
    )
    yield selectors
    for selector, profile in zip(selectors, canonical):
        for literal in independent_profile_units(profile, finals):
            yield (-selector, literal)


def profile_stream_hash(
    profiles: Iterable[tuple[int, int, int, int, int]]
) -> str:
    digest = hashlib.sha256()
    for profile in profiles:
        digest.update((" ".join(map(str, profile)) + "\n").encode("ascii"))
    return digest.hexdigest()


def threshold_semantics() -> dict[str, bool]:
    results: dict[str, bool] = {}
    for requested in DEGREES:
        valid = True
        for observed in range(ORDER):
            edge_false = observed < requested + 1
            nonedge_count = ORDER - 1 - observed
            nonedge_false = nonedge_count < ORDER - requested
            if (edge_false and nonedge_false) != (observed == requested):
                valid = False
                break
        results[str(requested)] = valid
    return results


def check_plan(
    plan_path: Path, base_cnf: Path, base_metadata: Path
) -> dict[str, object]:
    plan_bytes = plan_path.read_bytes()
    plan = json.loads(plan_bytes)
    errors: list[str] = []
    expected_top = {
        "schema": SCHEMA,
        "order": ORDER,
        "degree_values": list(DEGREES),
        "base_cnf_sha256": BASE_CNF_SHA256,
        "base_metadata_sha256": BASE_METADATA_SHA256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "admissible_profile_count_before_complement": EXPECTED_ADMISSIBLE_COUNT,
        "complement_fixed_profile_count": 0,
        "profile_count": EXPECTED_PROFILE_COUNT,
    }
    for key, expected in expected_top.items():
        if plan.get(key) != expected:
            errors.append(f"plan field mismatch: {key}")
    if sha256_file(base_cnf) != BASE_CNF_SHA256:
        errors.append("base CNF file hash mismatch")
    if sha256_file(base_metadata) != BASE_METADATA_SHA256:
        errors.append("base metadata file hash mismatch")

    canonical = independent_profiles()
    orbit_audit = complement_orbit_audit()
    if not orbit_audit["valid"]:
        errors.append("complement orbit audit failed")
    expected_profile_hash = profile_stream_hash(canonical)
    if plan.get("profile_stream_sha256") != expected_profile_hash:
        errors.append("profile stream hash mismatch")

    finals, final_variable = counter_finals()
    if final_variable != BASE_VARIABLE_COUNT:
        errors.append("counter allocation variable count mismatch")
    records = plan.get("profiles")
    if not isinstance(records, list) or len(records) != len(canonical):
        errors.append("profile record count mismatch")
        records = []
    record_errors = 0
    for index, (profile, record) in enumerate(zip(canonical, records)):
        units = independent_profile_units(profile, finals)
        degree_sum = sum(
            degree * count for degree, count in zip(DEGREES, profile)
        )
        expected = {
            "profile_index": index,
            "profile_id": "_".join(
                f"n{degree}_{count:02d}"
                for degree, count in zip(DEGREES, profile)
            ),
            "multiplicities": list(profile),
            "edge_count": degree_sum // 2,
            "assumption_count": 2 * ORDER,
            "assumptions_sha256": clause_hash(
                (literal,) for literal in units
            ),
        }
        if not isinstance(record, dict) or any(
            record.get(key) != value for key, value in expected.items()
        ):
            record_errors += 1
    if record_errors:
        errors.append(f"{record_errors} profile records malformed")

    expected_appended_count = 1 + 2 * ORDER * len(canonical)
    expected_appended_hash = clause_hash(independent_selector_clauses())
    expected_union = {
        "selector_variable_first": BASE_VARIABLE_COUNT + 1,
        "selector_variable_count": len(canonical),
        "variable_count": BASE_VARIABLE_COUNT + len(canonical),
        "selector_at_least_one_clause_count": 1,
        "selector_implication_clause_count": 2 * ORDER * len(canonical),
        "appended_clause_count": expected_appended_count,
        "appended_clause_stream_sha256": expected_appended_hash,
        "clause_count": BASE_CLAUSE_COUNT + expected_appended_count,
    }
    union = plan.get("selector_union")
    if not isinstance(union, dict):
        errors.append("selector union missing")
        union = {}
    for key, value in expected_union.items():
        if union.get(key) != value:
            errors.append(f"selector union field mismatch: {key}")

    semantics = threshold_semantics()
    if not all(semantics.values()):
        errors.append("false-threshold exact-degree semantics failed")
    return {
        "checker": CHECKER_ID,
        "checker_source_sha256": sha256_file(Path(__file__)),
        "valid": not errors,
        "errors": errors,
        "plan_sha256": hashlib.sha256(plan_bytes).hexdigest(),
        "independent_profile_count": len(canonical),
        "independent_counter_variable_count": final_variable,
        "profile_record_errors": record_errors,
        "complement_orbit_audit": orbit_audit,
        "threshold_semantics": semantics,
        "expected_appended_clause_count": expected_appended_count,
        "expected_appended_clause_stream_sha256": expected_appended_hash,
        "claim_limit": (
            "This checks the exact profile cover and selector-union clauses. "
            "It establishes neither SAT nor UNSAT."
        ),
    }


def dimacs_stream(
    path: Path,
) -> Generator[tuple[int, ...], None, dict[str, int]]:
    variables: int | None = None
    declared: int | None = None
    actual = 0
    pending: list[int] = []
    with path.open("r", encoding="ascii") as source:
        for line_number, line in enumerate(source, start=1):
            fields = line.split()
            if not fields or fields[0] == "c":
                continue
            if fields[0] == "p":
                if (
                    variables is not None
                    or len(fields) != 4
                    or fields[1] != "cnf"
                ):
                    raise ValueError(f"malformed header at line {line_number}")
                variables = int(fields[2])
                declared = int(fields[3])
                continue
            if variables is None:
                raise ValueError("clause before header")
            for field in fields:
                literal = int(field)
                if literal:
                    if abs(literal) > variables:
                        raise ValueError("literal outside declared range")
                    pending.append(literal)
                else:
                    if not pending:
                        raise ValueError("unexpected empty clause")
                    actual += 1
                    yield tuple(pending)
                    pending = []
    if pending:
        raise ValueError("unterminated final clause")
    if variables is None or declared is None:
        raise ValueError("missing header")
    return {
        "variable_count": variables,
        "declared_clause_count": declared,
        "actual_clause_count": actual,
    }


def next_clause(
    stream: Generator[tuple[int, ...], None, dict[str, int]],
) -> tuple[tuple[int, ...] | None, dict[str, int] | None]:
    try:
        return next(stream), None
    except StopIteration as stopped:
        return None, stopped.value


def check_materialized(
    *,
    base_cnf: Path,
    union_cnf: Path,
    metadata_path: Path,
) -> dict[str, object]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    base_stream = dimacs_stream(base_cnf)
    union_stream = dimacs_stream(union_cnf)
    copied = 0
    prefix_mismatches = 0
    base_summary = None
    union_summary = None
    while base_summary is None:
        expected, base_summary = next_clause(base_stream)
        if base_summary is not None:
            break
        actual, union_summary = next_clause(union_stream)
        if union_summary is not None:
            prefix_mismatches += 1
            break
        copied += 1
        prefix_mismatches += expected != actual

    appended_count = 0
    appended_mismatches = 0
    observed_appended_hash = hashlib.sha256()
    if union_summary is None:
        for expected in independent_selector_clauses():
            actual, union_summary = next_clause(union_stream)
            if union_summary is not None:
                appended_mismatches += 1
                break
            assert actual is not None
            appended_count += 1
            observed_appended_hash.update(
                (" ".join(map(str, actual)) + " 0\n").encode("ascii")
            )
            appended_mismatches += actual != expected
    if union_summary is None:
        extra, union_summary = next_clause(union_stream)
        if extra is not None:
            appended_mismatches += 1
            while extra is not None:
                appended_count += 1
                extra, union_summary = next_clause(union_stream)
    assert base_summary is not None
    assert union_summary is not None

    expected_profile_count = EXPECTED_PROFILE_COUNT
    expected_variables = BASE_VARIABLE_COUNT + expected_profile_count
    expected_appended_count = 1 + 2 * ORDER * expected_profile_count
    expected_clauses = BASE_CLAUSE_COUNT + expected_appended_count
    expected_append_hash = clause_hash(independent_selector_clauses())
    union_sha = sha256_file(union_cnf)
    checks = {
        "base_hash": sha256_file(base_cnf) == BASE_CNF_SHA256,
        "base_header": base_summary
        == {
            "variable_count": BASE_VARIABLE_COUNT,
            "declared_clause_count": BASE_CLAUSE_COUNT,
            "actual_clause_count": BASE_CLAUSE_COUNT,
        },
        "base_prefix_exact": (
            copied == BASE_CLAUSE_COUNT and prefix_mismatches == 0
        ),
        "appended_sequence_exact": (
            appended_count == expected_appended_count
            and appended_mismatches == 0
        ),
        "appended_hash": (
            observed_appended_hash.hexdigest() == expected_append_hash
        ),
        "union_header": union_summary
        == {
            "variable_count": expected_variables,
            "declared_clause_count": expected_clauses,
            "actual_clause_count": expected_clauses,
        },
        "metadata_hash": metadata.get("cnf_sha256") == union_sha,
        "metadata_bytes": metadata.get("cnf_bytes") == union_cnf.stat().st_size,
        "metadata_counts": (
            metadata.get("profile_count") == expected_profile_count
            and metadata.get("variable_count") == expected_variables
            and metadata.get("clause_count") == expected_clauses
            and metadata.get("appended_clause_count")
            == expected_appended_count
        ),
        "metadata_append_hash": (
            metadata.get("appended_clause_stream_sha256")
            == expected_append_hash
        ),
    }
    return {
        "valid": all(checks.values()),
        "checks": checks,
        "union_cnf_sha256": union_sha,
        "union_cnf_bytes": union_cnf.stat().st_size,
        "metadata_sha256": sha256_file(metadata_path),
        "copied_base_clause_count": copied,
        "base_prefix_mismatch_count": prefix_mismatches,
        "observed_appended_clause_count": appended_count,
        "expected_appended_clause_count": expected_appended_count,
        "appended_clause_mismatch_count": appended_mismatches,
        "observed_appended_clause_stream_sha256": (
            observed_appended_hash.hexdigest()
        ),
        "expected_appended_clause_stream_sha256": expected_append_hash,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--base-metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--union-cnf", type=Path)
    parser.add_argument("--union-metadata", type=Path)
    args = parser.parse_args()
    result = check_plan(args.plan, args.base_cnf, args.base_metadata)
    if (args.union_cnf is None) != (args.union_metadata is None):
        parser.error("--union-cnf and --union-metadata must be supplied together")
    if args.union_cnf is not None:
        materialized = check_materialized(
            base_cnf=args.base_cnf,
            union_cnf=args.union_cnf,
            metadata_path=args.union_metadata,
        )
        result["materialized_union"] = materialized
        if not materialized["valid"]:
            result["valid"] = False
            result["errors"].append("materialized union check failed")
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite {args.output}")
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
