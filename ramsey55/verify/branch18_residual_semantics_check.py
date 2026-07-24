#!/usr/bin/env python3
"""Independent exact checker for compact branch-18 residual formulas.

For each supplied order-24 graph6 record this checker:

* builds the production residual formula;
* independently streams and simplifies the audited direct CNF's 1,925,196
  primary Ramsey clauses under the exact root/catalog cube;
* requires clause-for-clause equality after first-occurrence deduplication;
* checks counter acceptance against direct graph degrees on seeded primary
  assignments; and
* exercises every A and B counter immediately below, at, and above its
  degree boundaries.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import sys
from pathlib import Path
from typing import Iterator, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from branch18_residual_cnf import (  # noqa: E402
    A,
    B,
    ORDER,
    PRIMARY_COUNT,
    build_residual,
    decode_graph6_order24,
)
from direct_ramsey_cnf import (  # noqa: E402
    canonical_counter_extension,
    clause_is_satisfied,
)


CHECKER_ID = "ramsey55.branch18_residual_semantics_checker.v1"
EXPECTED_BASE_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
RAMSEY_CLAUSE_COUNT = 2 * math.comb(ORDER, 5)


def independent_edge_map() -> tuple[
    dict[tuple[int, int], int], dict[int, tuple[int, int]]
]:
    by_pair = {
        pair: variable
        for variable, pair in enumerate(
            itertools.combinations(range(ORDER), 2), start=1
        )
    }
    return by_pair, {variable: pair for pair, variable in by_pair.items()}


def independent_unknown_map() -> dict[tuple[int, int], int]:
    pairs = tuple(itertools.combinations(A, 2)) + tuple(
        (left, right) for left in A for right in B
    )
    if len(pairs) != PRIMARY_COUNT:
        raise AssertionError("independent primary count mismatch")
    return {pair: variable for variable, pair in enumerate(pairs, start=1)}


def independent_fixed(
    pair: tuple[int, int], catalog: Sequence[int]
) -> bool | None:
    left, right = pair
    if left == 0:
        return right <= 18
    if left >= 19:
        return not bool(
            (catalog[left - 19] >> (right - 19)) & 1
        )
    return None


def dimacs_clauses(path: Path) -> Iterator[tuple[int, ...]]:
    current: list[int] = []
    with path.open("r", encoding="ascii") as source:
        for line in source:
            fields = line.split()
            if not fields or fields[0] in {"c", "p"}:
                continue
            for field in fields:
                literal = int(field)
                if literal:
                    current.append(literal)
                else:
                    yield tuple(current)
                    current = []
    if current:
        raise ValueError("unterminated DIMACS clause")


def independent_simplification(
    base_cnf: Path, catalog: Sequence[int]
) -> tuple[tuple[int, ...], ...]:
    _by_pair, by_variable = independent_edge_map()
    unknown = independent_unknown_map()
    output: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for index, clause in enumerate(dimacs_clauses(base_cnf)):
        if index == RAMSEY_CLAUSE_COUNT:
            break
        residual: list[int] = []
        satisfied = False
        for literal in clause:
            variable = abs(literal)
            if variable > math.comb(ORDER, 2):
                raise ValueError("auxiliary literal inside primary Ramsey prefix")
            pair = by_variable[variable]
            fixed = independent_fixed(pair, catalog)
            if fixed is None:
                mapped = unknown[pair]
                residual.append(mapped if literal > 0 else -mapped)
                continue
            if fixed == (literal > 0):
                satisfied = True
                break
        if satisfied:
            continue
        rendered = tuple(residual)
        if not rendered:
            raise ValueError("fixed cube falsifies a primary Ramsey clause")
        if rendered not in seen:
            seen.add(rendered)
            output.append(rendered)
    else:
        raise ValueError("base CNF ended before primary Ramsey prefix")
    return tuple(output)


def clause_stream_sha256(clauses: Sequence[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def counter_pair_accepts(counters, primary: Mapping[int, bool]) -> bool:
    assignment = dict(primary)
    for counter in counters:
        assignment.update(canonical_counter_extension(counter, assignment))
    return all(
        clause_is_satisfied(clause, assignment)
        for counter in counters
        for clause in counter.clauses()
    )


def direct_adjacency(instance, primary: Mapping[int, bool]) -> list[int]:
    return instance.primary_adjacency(primary)


def check_record(
    base_cnf: Path,
    graph6: str,
    *,
    seed: int,
    random_assignments: int,
) -> dict[str, object]:
    instance = build_residual(graph6)
    catalog = decode_graph6_order24(graph6)
    independently_simplified = independent_simplification(base_cnf, catalog)
    production = instance.ramsey_clauses
    exact_clause_equality = production == independently_simplified

    pair_to_variable = instance.pair_to_variable()
    generator = random.Random(seed)
    random_ramsey_matches = 0
    random_degree_vector_matches = 0
    for _ in range(random_assignments):
        primary = {
            variable: bool(generator.getrandbits(1))
            for variable in range(1, PRIMARY_COUNT + 1)
        }
        production_ramsey = all(
            clause_is_satisfied(clause, primary) for clause in production
        )
        independent_ramsey = all(
            clause_is_satisfied(clause, primary)
            for clause in independently_simplified
        )
        if production_ramsey == independent_ramsey:
            random_ramsey_matches += 1

        adjacency = direct_adjacency(instance, primary)
        counter_vector = [
            counter_pair_accepts(instance.counters[index : index + 2], primary)
            for index in range(0, len(instance.counters), 2)
        ]
        direct_vector = [
            18 <= adjacency[vertex].bit_count() <= 24
            for vertex in (*A, *B)
        ]
        if counter_vector == direct_vector:
            random_degree_vector_matches += 1

    A_boundary_checks = 0
    for offset, vertex in enumerate(A):
        counters = instance.counters[2 * offset : 2 * offset + 2]
        incident = [
            pair_to_variable[tuple(sorted((vertex, other)))]
            for other in (*A, *B)
            if other != vertex
        ]
        for count in (16, 17, 23, 24):
            primary = {
                variable: index < count
                for index, variable in enumerate(incident)
            }
            if counter_pair_accepts(counters, primary) != (17 <= count <= 23):
                raise AssertionError(f"A boundary failure at {vertex}, {count}")
            A_boundary_checks += 1

    B_boundary_checks = 0
    first_B_counter = 2 * len(A)
    for offset, vertex in enumerate(B):
        q = catalog[offset].bit_count()
        lower = q - 5
        upper = q + 1
        counters = instance.counters[
            first_B_counter + 2 * offset :
            first_B_counter + 2 * offset + 2
        ]
        cross = [pair_to_variable[(left, vertex)] for left in A]
        for count in (lower - 1, lower, upper, upper + 1):
            primary = {
                variable: index < count
                for index, variable in enumerate(cross)
            }
            if counter_pair_accepts(counters, primary) != (
                lower <= count <= upper
            ):
                raise AssertionError(f"B boundary failure at {vertex}, {count}")
            B_boundary_checks += 1

    valid = (
        exact_clause_equality
        and random_ramsey_matches == random_assignments
        and random_degree_vector_matches == random_assignments
        and A_boundary_checks == 72
        and B_boundary_checks == 96
    )
    return {
        "valid": valid,
        "catalog_graph6": graph6,
        "catalog_edge_count": instance.catalog_edge_count,
        "catalog_degree_sequence": list(instance.catalog_degree_sequence),
        "primary_variable_count": instance.primary_variable_count,
        "auxiliary_variable_count": instance.auxiliary_variable_count,
        "variable_count": instance.variable_count,
        "ramsey_clause_count": len(production),
        "degree_clause_count": instance.degree_clause_count,
        "clause_count": instance.clause_count,
        "production_ramsey_sha256": clause_stream_sha256(production),
        "independent_ramsey_sha256": clause_stream_sha256(
            independently_simplified
        ),
        "exact_clause_sequence_equality": exact_clause_equality,
        "random_assignment_count": random_assignments,
        "random_ramsey_matches": random_ramsey_matches,
        "random_degree_vector_matches": random_degree_vector_matches,
        "A_boundary_checks": A_boundary_checks,
        "B_boundary_checks": B_boundary_checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--graph6", action="append", required=True)
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument("--random-assignments", type=int, default=12)
    args = parser.parse_args()
    base_sha = hashlib.sha256(args.base_cnf.read_bytes()).hexdigest()
    records = [
        check_record(
            args.base_cnf,
            graph6,
            seed=args.seed + index,
            random_assignments=args.random_assignments,
        )
        for index, graph6 in enumerate(args.graph6)
    ]
    result = {
        "checker": CHECKER_ID,
        "checker_source_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "valid": base_sha == EXPECTED_BASE_SHA256
        and all(record["valid"] for record in records),
        "base_cnf_sha256": base_sha,
        "records": records,
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
