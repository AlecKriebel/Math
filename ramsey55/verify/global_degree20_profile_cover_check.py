#!/usr/bin/env python3
"""Independent checker for the exact degree-20 multiplicity cover."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Generator, Iterable, Sequence


CHECKER_ID = "ramsey55.global_degree20_profile_cover_checker.v1"
SCHEMA = "ramsey55.global_degree20_profile_cover.v1"
ORDER = 43
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
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


def independent_profiles() -> tuple[tuple[int, int, int], ...]:
    result: list[tuple[int, int, int]] = []
    # Enumerate all 990 nonnegative triples summing to 43 independently, then
    # apply parity and the complement orientation.
    for count20 in range(ORDER + 1):
        for count21 in range(ORDER - count20 + 1):
            count22 = ORDER - count20 - count21
            if count21 % 2 == 0 and count20 > count22:
                result.append((count20, count21, count22))
    return tuple(sorted(result, key=lambda profile: (profile[1], profile[2])))


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
    for degree, multiplicity in zip((20, 21, 22), profile):
        for _ in range(multiplicity):
            result.extend(
                independent_exact_degree_units(vertex, degree, finals)
            )
            vertex += 1
    if vertex != ORDER:
        raise AssertionError("profile does not cover vertices")
    return tuple(result)


def independent_selector_clauses() -> tuple[tuple[int, ...], ...]:
    profiles = independent_profiles()
    finals, variable_count = counter_finals()
    if variable_count != BASE_VARIABLE_COUNT:
        raise AssertionError("independent counter layout mismatch")
    selectors = tuple(
        range(BASE_VARIABLE_COUNT + 1, BASE_VARIABLE_COUNT + 1 + len(profiles))
    )
    clauses: list[tuple[int, ...]] = [selectors]
    for selector, profile in zip(selectors, profiles):
        clauses.extend(
            (-selector, literal)
            for literal in independent_profile_units(profile, finals)
        )
    return tuple(clauses)


def complement_orbit_audit() -> dict[str, int | bool]:
    """Exhaust all arithmetically admissible multiplicity triples."""

    admissible = [
        (a, b, ORDER - a - b)
        for a in range(ORDER + 1)
        for b in range(ORDER - a + 1)
        if b % 2 == 0
    ]
    canonical = set(independent_profiles())
    covered: set[tuple[int, int, int]] = set()
    fixed = 0
    for profile in admissible:
        swapped = (profile[2], profile[1], profile[0])
        if profile == swapped:
            fixed += 1
            continue
        representative = profile if profile[0] > profile[2] else swapped
        if representative not in canonical:
            return {
                "valid": False,
                "admissible_count": len(admissible),
                "fixed_count": fixed,
                "covered_count": len(covered),
            }
        covered.add(profile)
    return {
        "valid": fixed == 0 and len(covered) == len(admissible),
        "admissible_count": len(admissible),
        "fixed_count": fixed,
        "covered_count": len(covered),
        "canonical_count": len(canonical),
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


def check_plan(
    plan_path: Path, base_cnf: Path, base_metadata: Path
) -> dict[str, object]:
    plan_bytes = plan_path.read_bytes()
    plan = json.loads(plan_bytes)
    errors: list[str] = []
    for key, expected in (
        ("schema", SCHEMA),
        ("order", ORDER),
        ("degree_values", [20, 21, 22]),
        ("base_cnf_sha256", BASE_CNF_SHA256),
        ("base_metadata_sha256", BASE_METADATA_SHA256),
        ("base_variable_count", BASE_VARIABLE_COUNT),
        ("base_clause_count", BASE_CLAUSE_COUNT),
        ("profile_count", 253),
    ):
        if plan.get(key) != expected:
            errors.append(f"plan field mismatch: {key}")
    if sha256_file(base_cnf) != BASE_CNF_SHA256:
        errors.append("base CNF file hash mismatch")
    if sha256_file(base_metadata) != BASE_METADATA_SHA256:
        errors.append("base metadata file hash mismatch")

    profiles = independent_profiles()
    finals, final_variable = counter_finals()
    if final_variable != BASE_VARIABLE_COUNT:
        errors.append("counter allocation variable count mismatch")
    expected_profile_hash = hashlib.sha256(
        "".join(f"{a} {b} {c}\n" for a, b, c in profiles).encode("ascii")
    ).hexdigest()
    if plan.get("profile_stream_sha256") != expected_profile_hash:
        errors.append("profile stream hash mismatch")

    records = plan.get("profiles")
    if not isinstance(records, list) or len(records) != len(profiles):
        errors.append("profile record count mismatch")
        records = []
    record_errors = 0
    for index, (profile, record) in enumerate(zip(profiles, records)):
        units = independent_profile_units(profile, finals)
        a, b, c = profile
        expected = {
            "profile_index": index,
            "profile_id": f"n20_{a:02d}_n21_{b:02d}_n22_{c:02d}",
            "multiplicities": [a, b, c],
            "edge_count": (20 * a + 21 * b + 22 * c) // 2,
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

    additions = independent_selector_clauses()
    union = plan.get("selector_union")
    expected_union = {
        "selector_variable_first": BASE_VARIABLE_COUNT + 1,
        "selector_variable_count": len(profiles),
        "variable_count": BASE_VARIABLE_COUNT + len(profiles),
        "selector_at_least_one_clause_count": 1,
        "selector_implication_clause_count": 2 * ORDER * len(profiles),
        "appended_clause_count": len(additions),
        "appended_clause_stream_sha256": clause_hash(additions),
        "clause_count": BASE_CLAUSE_COUNT + len(additions),
    }
    if not isinstance(union, dict):
        errors.append("selector union missing")
        union = {}
    for key, value in expected_union.items():
        if union.get(key) != value:
            errors.append(f"selector union field mismatch: {key}")

    orbit_audit = complement_orbit_audit()
    if not orbit_audit["valid"]:
        errors.append("complement orbit audit failed")
    return {
        "checker": CHECKER_ID,
        "checker_source_sha256": sha256_file(Path(__file__)),
        "valid": not errors,
        "errors": errors,
        "plan_sha256": hashlib.sha256(plan_bytes).hexdigest(),
        "independent_profile_count": len(profiles),
        "independent_counter_variable_count": final_variable,
        "profile_record_errors": record_errors,
        "complement_orbit_audit": orbit_audit,
        "expected_appended_clause_count": len(additions),
        "expected_appended_clause_stream_sha256": clause_hash(additions),
        "claim_limit": (
            "This checks the exact degree-profile cover and union clauses; "
            "it does not establish SAT or UNSAT."
        ),
    }


def check_materialized(
    *,
    base_cnf: Path,
    union_cnf: Path,
    metadata_path: Path,
) -> dict[str, object]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    expected_additions = independent_selector_clauses()
    base_stream = dimacs_stream(base_cnf)
    union_stream = dimacs_stream(union_cnf)
    base_summary = None
    union_summary = None
    mismatch_count = 0
    copied = 0
    while base_summary is None:
        expected, base_summary = next_clause(base_stream)
        if base_summary is not None:
            break
        actual, union_summary = next_clause(union_stream)
        if union_summary is not None:
            mismatch_count += 1
            break
        copied += 1
        mismatch_count += expected != actual

    observed_additions: list[tuple[int, ...]] = []
    if union_summary is None:
        while True:
            clause, union_summary = next_clause(union_stream)
            if union_summary is not None:
                break
            assert clause is not None
            observed_additions.append(clause)
    assert base_summary is not None
    assert union_summary is not None

    union_sha = sha256_file(union_cnf)
    expected_variables = BASE_VARIABLE_COUNT + len(independent_profiles())
    expected_clauses = BASE_CLAUSE_COUNT + len(expected_additions)
    checks = {
        "base_hash": sha256_file(base_cnf) == BASE_CNF_SHA256,
        "base_header": base_summary
        == {
            "variable_count": BASE_VARIABLE_COUNT,
            "declared_clause_count": BASE_CLAUSE_COUNT,
            "actual_clause_count": BASE_CLAUSE_COUNT,
        },
        "base_prefix_exact": (
            copied == BASE_CLAUSE_COUNT and mismatch_count == 0
        ),
        "appended_sequence_exact": (
            tuple(observed_additions) == expected_additions
        ),
        "union_header": union_summary
        == {
            "variable_count": expected_variables,
            "declared_clause_count": expected_clauses,
            "actual_clause_count": expected_clauses,
        },
        "metadata_hash": metadata.get("cnf_sha256") == union_sha,
        "metadata_bytes": metadata.get("cnf_bytes")
        == union_cnf.stat().st_size,
        "metadata_counts": (
            metadata.get("variable_count") == expected_variables
            and metadata.get("clause_count") == expected_clauses
            and metadata.get("appended_clause_count")
            == len(expected_additions)
        ),
        "metadata_append_hash": (
            metadata.get("appended_clause_stream_sha256")
            == clause_hash(expected_additions)
        ),
    }
    return {
        "valid": all(checks.values()),
        "checks": checks,
        "union_cnf_sha256": union_sha,
        "union_cnf_bytes": union_cnf.stat().st_size,
        "metadata_sha256": sha256_file(metadata_path),
        "copied_base_clause_count": copied,
        "base_prefix_mismatch_count": mismatch_count,
        "observed_appended_clause_count": len(observed_additions),
        "expected_appended_clause_count": len(expected_additions),
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
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
