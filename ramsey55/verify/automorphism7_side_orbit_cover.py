#!/usr/bin/env python3
"""Independently audit the one-side orbit cover for the order-7 branch.

This checker deliberately rebuilds the 30-variable side formula and all
relabeling actions instead of importing the constructive pilot.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path

from pysat.solvers import Cadical195


ORDER = 43
PRIME = 7
SIDE_ORDER = 21
SIDE_VARIABLES = 30


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_lines(lines: list[str]) -> str:
    return hashlib.sha256(("\n".join(lines) + "\n").encode("ascii")).hexdigest()


def parse_dimacs(path: Path) -> tuple[int, tuple[tuple[int, ...], ...]]:
    variable_count = clause_count = None
    clauses: list[tuple[int, ...]] = []
    for line_number, raw in enumerate(
        path.read_text(encoding="ascii").splitlines(), start=1
    ):
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            fields = line.split()
            if (
                len(fields) != 4
                or fields[:2] != ["p", "cnf"]
                or variable_count is not None
            ):
                raise ValueError(f"invalid header on line {line_number}")
            variable_count, clause_count = map(int, fields[2:])
            continue
        if variable_count is None:
            raise ValueError("clause before header")
        fields = [int(field) for field in line.split()]
        if not fields or fields[-1] != 0 or 0 in fields[:-1]:
            raise ValueError(f"invalid clause on line {line_number}")
        clause = tuple(fields[:-1])
        if any(abs(literal) > variable_count for literal in clause):
            raise ValueError(f"literal outside header range on line {line_number}")
        clauses.append(clause)
    if variable_count is None or clause_count != len(clauses):
        raise ValueError("DIMACS header count mismatch")
    return variable_count, tuple(clauses)


def side_edge_orbits() -> tuple[
    tuple[tuple[tuple[int, int], ...], ...],
    dict[tuple[int, int], int],
]:
    rotate = tuple(
        block * PRIME + (offset + 1) % PRIME
        for block in range(3)
        for offset in range(PRIME)
    )
    unseen = set(itertools.combinations(range(SIDE_ORDER), 2))
    orbits: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        edge = min(unseen)
        orbit: set[tuple[int, int]] = set()
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((rotate[edge[0]], rotate[edge[1]])))
        unseen.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))
    orbits.sort(key=lambda orbit: orbit[0])
    table = {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }
    if len(orbits) != SIDE_VARIABLES or len(table) != math.comb(SIDE_ORDER, 2):
        raise AssertionError("unexpected side edge-orbit partition")
    return tuple(orbits), table


def side_formula(
    edge_variable: dict[tuple[int, int], int],
) -> tuple[tuple[int, ...], ...]:
    clique_signatures = {
        tuple(
            sorted(
                {
                    edge_variable[edge]
                    for edge in itertools.combinations(vertices, 2)
                }
            )
        )
        for vertices in itertools.combinations(range(SIDE_ORDER), 4)
    }
    independent_signatures = {
        tuple(
            sorted(
                {
                    edge_variable[edge]
                    for edge in itertools.combinations(vertices, 2)
                }
            )
        )
        for vertices in itertools.combinations(range(SIDE_ORDER), 5)
    }
    if len(clique_signatures) != 843 or len(independent_signatures) != 2775:
        raise AssertionError("unexpected side signature count")
    return tuple(
        [tuple(-variable for variable in signature) for signature in sorted(clique_signatures)]
        + list(sorted(independent_signatures))
    )


def edge_variable_permutation(
    edge_orbits: tuple[tuple[tuple[int, int], ...], ...],
    edge_variable: dict[tuple[int, int], int],
    block_permutation: tuple[int, int, int],
    shifts: tuple[int, int, int],
    multiplier: int = 1,
) -> tuple[int, ...]:
    image: list[int] = []
    for orbit in edge_orbits:
        left, right = orbit[0]
        left_block, left_offset = divmod(left, PRIME)
        right_block, right_offset = divmod(right, PRIME)
        new_left = (
            block_permutation[left_block] * PRIME
            + (multiplier * left_offset + shifts[left_block]) % PRIME
        )
        new_right = (
            block_permutation[right_block] * PRIME
            + (multiplier * right_offset + shifts[right_block]) % PRIME
        )
        image.append(edge_variable[tuple(sorted((new_left, new_right)))] - 1)
    if sorted(image) != list(range(SIDE_VARIABLES)):
        raise AssertionError("side action is not a variable permutation")
    return tuple(image)


def transform_bits(bits: int, permutation: tuple[int, ...]) -> int:
    transformed = 0
    while bits:
        lowest = bits & -bits
        old_index = lowest.bit_length() - 1
        transformed |= 1 << permutation[old_index]
        bits -= lowest
    return transformed


def enumerate_models(clauses: tuple[tuple[int, ...], ...]) -> set[int]:
    models: set[int] = set()
    with Cadical195(bootstrap_with=clauses) as solver:
        while solver.solve():
            truth = {abs(literal): literal > 0 for literal in solver.get_model()}
            model = sum(
                1 << (variable - 1)
                for variable in range(1, SIDE_VARIABLES + 1)
                if truth[variable]
            )
            if model in models:
                raise AssertionError("duplicate side model")
            models.add(model)
            solver.add_clause(
                [
                    -variable if truth[variable] else variable
                    for variable in range(1, SIDE_VARIABLES + 1)
                ]
            )
    return models


def global_edge_table(metadata: dict[str, object]) -> dict[tuple[int, int], int]:
    records = metadata.get("edge_orbits")
    if not isinstance(records, list):
        raise ValueError("metadata has no edge-orbit list")
    table: dict[tuple[int, int], int] = {}
    for record in records:
        if not isinstance(record, dict) or type(record.get("variable")) is not int:
            raise ValueError("malformed edge-orbit record")
        variable = int(record["variable"])
        edges = record.get("edges")
        if not isinstance(edges, list):
            raise ValueError("malformed edge list")
        for raw_edge in edges:
            if (
                not isinstance(raw_edge, list)
                or len(raw_edge) != 2
                or any(type(vertex) is not int for vertex in raw_edge)
            ):
                raise ValueError("malformed edge")
            edge = tuple(raw_edge)
            if not 0 <= edge[0] < edge[1] < ORDER or edge in table:
                raise ValueError("invalid or duplicate edge")
            table[edge] = variable
    multiplicities = Counter(table.values())
    if (
        len(table) != math.comb(ORDER, 2)
        or set(multiplicities) != set(range(1, 130))
        or set(multiplicities.values()) != {PRIME}
    ):
        raise ValueError("unexpected global edge-orbit partition")
    return table


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()

    edge_orbits, edge_variable = side_edge_orbits()
    clauses = side_formula(edge_variable)
    clause_set = {tuple(sorted(clause)) for clause in clauses}
    if len(clause_set) != len(clauses):
        raise AssertionError("duplicate side clause")

    shift_permutations = {
        edge_variable_permutation(
            edge_orbits, edge_variable, block_permutation, (0, shift_1, shift_2)
        )
        for block_permutation in itertools.permutations(range(3))
        for shift_1 in range(PRIME)
        for shift_2 in range(PRIME)
    }
    multiplier_permutations = tuple(
        edge_variable_permutation(
            edge_orbits, edge_variable, (0, 1, 2), (0, 0, 0), multiplier
        )
        for multiplier in range(1, PRIME)
    )
    if len(shift_permutations) != 294 or len(set(multiplier_permutations)) != 6:
        raise AssertionError("unexpected side action size")
    for permutation in [*shift_permutations, *multiplier_permutations]:
        mapped = {
            tuple(
                sorted(
                    (
                        permutation[abs(literal) - 1] + 1
                        if literal > 0
                        else -(permutation[abs(literal) - 1] + 1)
                    )
                    for literal in clause
                )
            )
            for clause in clauses
        }
        if mapped != clause_set:
            raise AssertionError("side action does not preserve the side formula")

    models = enumerate_models(clauses)
    side_class: dict[int, int] = {}
    representatives: list[int] = []
    shift_orbit_sizes: list[int] = []
    for model in sorted(models):
        if model in side_class:
            continue
        orbit = {
            transform_bits(model, permutation)
            for permutation in shift_permutations
        }
        if not orbit <= models or orbit & side_class.keys():
            raise AssertionError("side shift/permutation orbit coverage failed")
        class_index = len(representatives)
        for image in orbit:
            side_class[image] = class_index
        representatives.append(min(orbit))
        shift_orbit_sizes.append(len(orbit))
    if set(side_class) != models:
        raise AssertionError("side shift/permutation classes are incomplete")

    multiplier_actions: list[tuple[int, ...]] = []
    for permutation in multiplier_permutations:
        action = tuple(
            side_class[transform_bits(model, permutation)]
            for model in representatives
        )
        if sorted(action) != list(range(len(representatives))):
            raise AssertionError("multiplier does not permute side classes")
        multiplier_actions.append(action)
    seen_classes: set[int] = set()
    quotient_representatives: list[int] = []
    multiplier_orbit_sizes: list[int] = []
    for class_index in range(len(representatives)):
        if class_index in seen_classes:
            continue
        orbit = {action[class_index] for action in multiplier_actions}
        seen_classes.update(orbit)
        quotient_representatives.append(min(orbit))
        multiplier_orbit_sizes.append(len(orbit))
    if seen_classes != set(range(len(representatives))):
        raise AssertionError("multiplier class coverage failed")

    variable_count, global_clauses = parse_dimacs(args.cnf)
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict) or variable_count != 129:
        raise ValueError("unexpected global formula")
    global_table = global_edge_table(metadata)
    global_clause_set = {tuple(sorted(clause)) for clause in global_clauses}
    if len(global_clause_set) != len(global_clauses):
        raise AssertionError("duplicate global clause")
    global_invariance: list[dict[str, object]] = []
    for multiplier in range(1, PRIME):
        variable_map: dict[int, int] = {}
        for (left, right), variable in global_table.items():
            def image(vertex: int) -> int:
                if vertex == ORDER - 1:
                    return vertex
                block, offset = divmod(vertex, PRIME)
                return block * PRIME + multiplier * offset % PRIME

            new_variable = global_table[tuple(sorted((image(left), image(right))))]
            if variable in variable_map and variable_map[variable] != new_variable:
                raise AssertionError("global action is not well-defined on edge orbits")
            variable_map[variable] = new_variable
        if (
            set(variable_map) != set(range(1, variable_count + 1))
            or set(variable_map.values()) != set(range(1, variable_count + 1))
        ):
            raise AssertionError("global action is not a variable bijection")
        mapped_clauses = {
            tuple(
                sorted(
                    (
                        variable_map[abs(literal)]
                        if literal > 0
                        else -variable_map[abs(literal)]
                    )
                    for literal in clause
                )
            )
            for clause in global_clauses
        }
        invariant = mapped_clauses == global_clause_set
        global_invariance.append(
            {
                "multiplier": multiplier,
                "variable_bijection": True,
                "mapped_clause_count": len(mapped_clauses),
                "missing_clause_count": len(mapped_clauses - global_clause_set),
                "extra_clause_count": len(global_clause_set - mapped_clauses),
                "cnf_invariant": invariant,
            }
        )
        if not invariant:
            raise AssertionError("global multiplier does not preserve the CNF")

    result = {
        "audit": "order43_automorphism7_one_side_orbit_cover_v1",
        "evidence_label": "EXACT FINITE ENUMERATION AND CLAUSE-SET AUDIT",
        "claim_boundary": (
            "This verifies a symmetry-complete 122-cube cover of the "
            "automorphism-7 branch after fixed-vertex degree normalization. "
            "It does not determine cube satisfiability and is not an "
            "UNSAT certificate for any cube or for the global formula."
        ),
        "cnf": {
            "path": str(args.cnf.resolve()),
            "sha256": sha256_file(args.cnf),
            "variable_count": variable_count,
            "clause_count": len(global_clauses),
        },
        "metadata": {
            "path": str(args.metadata.resolve()),
            "sha256": sha256_file(args.metadata),
        },
        "side_formula": {
            "variable_count": SIDE_VARIABLES,
            "clause_count": len(clauses),
            "sha256": sha256_lines(
                [" ".join(map(str, clause)) for clause in clauses]
            ),
            "model_count": len(models),
        },
        "shift_and_block_action": {
            "distinct_variable_permutation_count": len(shift_permutations),
            "orbit_count": len(representatives),
            "orbit_size_histogram": dict(sorted(Counter(shift_orbit_sizes).items())),
            "covered_model_count": len(side_class),
        },
        "common_multiplier_action": {
            "distinct_action_count": len(set(multiplier_actions)),
            "quotient_orbit_count": len(quotient_representatives),
            "orbit_size_histogram": dict(
                sorted(Counter(multiplier_orbit_sizes).items())
            ),
            "covered_shift_block_class_count": len(seen_classes),
            "global_cnf_invariance": global_invariance,
        },
        "coverage_valid": (
            len(models) == 191394
            and len(representatives) == 664
            and len(quotient_representatives) == 122
            and all(record["cnf_invariant"] for record in global_invariance)
        ),
        "runtime_seconds": time.monotonic() - started,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["coverage_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
