#!/usr/bin/env python3
"""Independent audit of the residual hole-5 rim reflection and S6 coverage.

This probe deliberately does not import the synthesis or symmetry-breaker
implementation.  It reconstructs the complete 6,886-variable semantic
allocation, relabeling actions, and signature clauses from combinatorial
definitions, then audits the frozen complete-bank CNF by content hash.

No SAT solver is invoked and no SAT/UNSAT claim is made.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import itertools
import json
from pathlib import Path
import sys
from typing import Iterable, Mapping, Sequence


ORDER = 12
VARIABLE_COUNT = 6_886
BASE_CLAUSE_COUNT = 20_008
BANK_CLAUSE_COUNT = 3_645
FULL_CLAUSE_COUNT = 23_653
FULL_LITERAL_COUNT = 188_959
SIGNATURE_CLAUSE_COUNT = 315
SIGNATURE_LITERAL_COUNT = 3_210
SIGNATURE_STREAM_SIZE = 11_424

EXPECTED_SOURCE_CNF_SHA256 = (
    "76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7"
)
EXPECTED_BANK_SHA256 = (
    "b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00"
)
EXPECTED_MANIFEST_SHA256 = (
    "99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402"
)
EXPECTED_SIGNATURE_STREAM_SHA256 = (
    "ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6"
)

RHO = (1, 0, 4, 3, 2, 5, 6, 7, 8, 9, 10, 11)
CORE_VERTICES = tuple(range(6))
OUTER_VERTICES = tuple(range(6, 12))
ADJACENT_OUTER_TRANSPOSITIONS = (
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (10, 11),
)
POSITIVE_TEMPLATE_EDGES = (
    (0, 1),
    (0, 4),
    (0, 5),
    (1, 2),
    (1, 5),
    (2, 3),
    (3, 4),
)
SCHEMA = "gamma-theta-hole5-rim-reflection-coverage-hostile-audit-v1"


class AuditFailure(ValueError):
    """A deterministic audit assertion failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode("ascii")


def campaign_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ordered_pair(first: int, second: int) -> tuple[int, int]:
    require(first != second, "edge endpoints coincide")
    return (first, second) if first < second else (second, first)


@dataclass(frozen=True)
class ParsedCNF:
    variable_count: int
    clauses: tuple[tuple[int, ...], ...]
    literal_count: int
    header: str
    body: bytes


def parse_dimacs(payload: bytes) -> ParsedCNF:
    require(payload.endswith(b"\n"), "DIMACS payload lacks terminal LF")
    lines = payload.splitlines(keepends=True)
    require(lines and lines[0].endswith(b"\n"), "DIMACS header malformed")
    try:
        header_fields = lines[0].decode("ascii").strip().split()
    except UnicodeDecodeError as error:
        raise AuditFailure("DIMACS header is not ASCII") from error
    require(
        len(header_fields) == 4 and header_fields[:2] == ["p", "cnf"],
        "DIMACS header fields malformed",
    )
    variable_count = int(header_fields[2])
    declared_clauses = int(header_fields[3])
    clauses: list[tuple[int, ...]] = []
    for index, raw_line in enumerate(lines[1:], start=1):
        require(raw_line.endswith(b"\n"), f"DIMACS line {index} lacks LF")
        try:
            fields = tuple(int(field) for field in raw_line.split())
        except ValueError as error:
            raise AuditFailure(f"DIMACS line {index} is not integral") from error
        require(fields and fields[-1] == 0, f"DIMACS line {index} lacks zero")
        clause = fields[:-1]
        require(0 not in clause, f"DIMACS line {index} has an internal zero")
        require(
            all(1 <= abs(literal) <= variable_count for literal in clause),
            f"DIMACS line {index} has an out-of-range literal",
        )
        require(
            len(set(clause)) == len(clause),
            f"DIMACS line {index} repeats a literal",
        )
        require(
            all(-literal not in clause for literal in clause),
            f"DIMACS line {index} is tautological",
        )
        clauses.append(clause)
    require(
        len(clauses) == declared_clauses,
        "DIMACS declared and actual clause counts differ",
    )
    return ParsedCNF(
        variable_count=variable_count,
        clauses=tuple(clauses),
        literal_count=sum(map(len, clauses)),
        header=lines[0].decode("ascii").rstrip("\n"),
        body=b"".join(lines[1:]),
    )


@dataclass(frozen=True)
class Allocation:
    edge: Mapping[tuple[int, int], int]
    witness: Mapping[tuple[int, int, int], int]
    family: Mapping[tuple[int, int, int], int]
    move: Mapping[tuple[tuple[int, int, int], int, int], int]
    role_by_variable: tuple[str, ...]
    label_by_variable: tuple[str, ...]
    role_ranges: Mapping[str, tuple[int, int, int]]


def reconstruct_allocation() -> Allocation:
    """Rebuild the semantic allocation without importing production code."""

    role_by_variable = [""]
    label_by_variable = [""]

    def allocate(role: str, label: str) -> int:
        role_by_variable.append(role)
        label_by_variable.append(label)
        return len(role_by_variable) - 1

    edge: dict[tuple[int, int], int] = {}
    for first, second in itertools.combinations(range(ORDER), 2):
        edge[(first, second)] = allocate("edge", f"e:{first},{second}")

    witness: dict[tuple[int, int, int], int] = {}
    for first, second in itertools.combinations(range(ORDER), 2):
        for third in range(ORDER):
            if third not in (first, second):
                witness[(first, second, third)] = allocate(
                    "witness", f"w:{first},{second}|{third}"
                )

    family: dict[tuple[int, int, int], int] = {}
    triples = tuple(itertools.combinations(range(ORDER), 3))
    for triple in triples:
        family[triple] = allocate(
            "family", "f:" + ",".join(map(str, triple))
        )

    move: dict[tuple[tuple[int, int, int], int, int], int] = {}
    for triple in triples:
        for attacked in range(ORDER):
            if attacked in triple:
                continue
            for guard in triple:
                move[(triple, attacked, guard)] = allocate(
                    "move",
                    "m:"
                    + ",".join(map(str, triple))
                    + f"|{attacked}|{guard}",
                )

    require(
        len(role_by_variable) - 1 == VARIABLE_COUNT,
        "allocation variable count mismatch",
    )
    role_ranges: dict[str, tuple[int, int, int]] = {}
    for role in ("edge", "witness", "family", "move"):
        variables = [
            variable
            for variable, actual in enumerate(role_by_variable)
            if actual == role
        ]
        require(variables, f"empty allocation role {role}")
        role_ranges[role] = (variables[0], variables[-1], len(variables))
    require(
        role_ranges
        == {
            "edge": (1, 66, 66),
            "witness": (67, 726, 660),
            "family": (727, 946, 220),
            "move": (947, 6_886, 5_940),
        },
        "allocation role ranges mismatch",
    )
    return Allocation(
        edge=edge,
        witness=witness,
        family=family,
        move=move,
        role_by_variable=tuple(role_by_variable),
        label_by_variable=tuple(label_by_variable),
        role_ranges=role_ranges,
    )


def allocation_stream_bytes(allocation: Allocation) -> bytes:
    return b"".join(
        (
            f"{variable}\t{allocation.role_by_variable[variable]}"
            f"\t{allocation.label_by_variable[variable]}\n"
        ).encode("ascii")
        for variable in range(1, VARIABLE_COUNT + 1)
    )


def semantic_variable_action(
    permutation: Sequence[int], allocation: Allocation
) -> tuple[int, ...]:
    """Map all variables under an old-vertex to new-vertex relabeling."""

    require(
        tuple(sorted(permutation)) == tuple(range(ORDER)),
        "vertex action is not a permutation",
    )
    action = [0] * (VARIABLE_COUNT + 1)
    for (first, second), variable in allocation.edge.items():
        action[variable] = allocation.edge[
            ordered_pair(permutation[first], permutation[second])
        ]
    for (first, second, third), variable in allocation.witness.items():
        image_pair = ordered_pair(permutation[first], permutation[second])
        action[variable] = allocation.witness[
            (image_pair[0], image_pair[1], permutation[third])
        ]
    for triple, variable in allocation.family.items():
        image = tuple(sorted(permutation[vertex] for vertex in triple))
        action[variable] = allocation.family[image]
    for (triple, attacked, guard), variable in allocation.move.items():
        image_triple = tuple(
            sorted(permutation[vertex] for vertex in triple)
        )
        action[variable] = allocation.move[
            (image_triple, permutation[attacked], permutation[guard])
        ]
    require(
        tuple(sorted(action[1:])) == tuple(range(1, VARIABLE_COUNT + 1)),
        "semantic variable action is not bijective",
    )
    require(
        all(
            allocation.role_by_variable[variable]
            == allocation.role_by_variable[action[variable]]
            for variable in range(1, VARIABLE_COUNT + 1)
        ),
        "semantic variable action changes a role",
    )
    return tuple(action)


def action_stream_bytes(action: Sequence[int]) -> bytes:
    require(len(action) == VARIABLE_COUNT + 1, "action length mismatch")
    return b"".join(
        f"{variable} {action[variable]}\n".encode("ascii")
        for variable in range(1, VARIABLE_COUNT + 1)
    )


def map_clause(
    clause: Sequence[int], action: Sequence[int]
) -> tuple[int, ...]:
    return tuple(
        sorted(
            action[abs(literal)] if literal > 0 else -action[abs(literal)]
            for literal in clause
        )
    )


def clause_counter(
    clauses: Iterable[Sequence[int]],
) -> Counter[tuple[int, ...]]:
    return Counter(tuple(sorted(clause)) for clause in clauses)


def canonical_clause_multiset_bytes(
    clauses: Iterable[Sequence[int]],
) -> bytes:
    normalized = sorted(tuple(sorted(clause)) for clause in clauses)
    return b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in normalized
    )


def covariance_report(
    clauses: Sequence[Sequence[int]], action: Sequence[int]
) -> dict[str, object]:
    original = clause_counter(clauses)
    mapped = Counter(map_clause(clause, action) for clause in clauses)
    missing = original - mapped
    extra = mapped - original
    require(not missing and not extra, "clause multiset is not covariant")
    original_stream = canonical_clause_multiset_bytes(clauses)
    mapped_stream = canonical_clause_multiset_bytes(
        tuple(map_clause(clause, action) for clause in clauses)
    )
    require(original_stream == mapped_stream, "canonical covariance bytes differ")
    return {
        "clause_count": len(clauses),
        "literal_count": sum(map(len, clauses)),
        "multiplicity_preserved": True,
        "canonical_multiset_sha256": sha256_bytes(original_stream),
        "canonical_mapped_multiset_sha256": sha256_bytes(mapped_stream),
        "missing_occurrences": 0,
        "extra_occurrences": 0,
    }


def canonicalize_color_names(row: Sequence[int]) -> tuple[int, ...]:
    require(
        len(row) == ORDER
        and all(type(color) is int and color in (0, 1, 2) for color in row),
        "malformed coloring row",
    )
    names: dict[int, int] = {}
    result: list[int] = []
    for color in row:
        if color not in names:
            names[color] = len(names)
        result.append(names[color])
    return tuple(result)


def load_bank(payload: bytes) -> tuple[tuple[int, ...], ...]:
    try:
        raw = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditFailure("coloring bank is not valid JSON") from error
    require(type(raw) is list, "coloring bank is not a list")
    rows: list[tuple[int, ...]] = []
    for index, value in enumerate(raw):
        require(type(value) is list, f"bank row {index} is not a list")
        row = tuple(value)
        require(
            canonicalize_color_names(row) == row,
            f"bank row {index} is not first-use canonical",
        )
        require(
            all(row[first] != row[second] for first, second in POSITIVE_TEMPLATE_EDGES),
            f"bank row {index} violates a forced positive edge",
        )
        rows.append(row)
    require(len(rows) == BANK_CLAUSE_COUNT, "bank row count mismatch")
    require(rows == sorted(rows), "bank rows are not sorted")
    require(len(set(rows)) == len(rows), "bank rows are not unique")
    return tuple(rows)


def same_color_clause(
    row: Sequence[int], allocation: Allocation
) -> tuple[int, ...]:
    return tuple(
        allocation.edge[(first, second)]
        for first, second in itertools.combinations(range(ORDER), 2)
        if row[first] == row[second]
    )


def transform_coloring(
    row: Sequence[int], permutation: Sequence[int]
) -> tuple[int, ...]:
    image = [-1] * ORDER
    for old_vertex, new_vertex in enumerate(permutation):
        image[new_vertex] = row[old_vertex]
    require(-1 not in image, "coloring transform incomplete")
    return canonicalize_color_names(image)


def signature_variables(
    outer_vertex: int, allocation: Allocation
) -> tuple[int, ...]:
    require(outer_vertex in OUTER_VERTICES, "signature vertex is not outer")
    return tuple(
        allocation.edge[ordered_pair(core, outer_vertex)]
        for core in CORE_VERTICES
    )


def lex_comparator_clauses(
    left_vertex: int, right_vertex: int, allocation: Allocation
) -> tuple[tuple[int, ...], ...]:
    left = signature_variables(left_vertex, allocation)
    right = signature_variables(right_vertex, allocation)
    clauses: list[tuple[int, ...]] = []
    for pivot in range(6):
        for prefix in itertools.product((0, 1), repeat=pivot):
            clause: list[int] = []
            for index, bit in enumerate(prefix):
                clause.extend(
                    (left[index], right[index])
                    if bit == 0
                    else (-left[index], -right[index])
                )
            clause.extend((-left[pivot], right[pivot]))
            clauses.append(tuple(clause))
    return tuple(clauses)


def signature_breaker_clauses(
    allocation: Allocation,
) -> tuple[tuple[int, ...], ...]:
    clauses: list[tuple[int, ...]] = []
    for left, right in ADJACENT_OUTER_TRANSPOSITIONS:
        clauses.extend(lex_comparator_clauses(left, right, allocation))
    result = tuple(clauses)
    require(len(result) == SIGNATURE_CLAUSE_COUNT, "signature clause count")
    require(
        sum(map(len, result)) == SIGNATURE_LITERAL_COUNT,
        "signature literal count",
    )
    return result


def dimacs_clause_stream(
    clauses: Iterable[Sequence[int]],
) -> bytes:
    return b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in clauses
    )


def signature_bits(value: int) -> tuple[int, ...]:
    require(0 <= value < 64, "signature value outside 0..63")
    return tuple((value >> (5 - index)) & 1 for index in range(6))


def comparator_truth_audit(
    left_vertex: int,
    right_vertex: int,
    clauses: Sequence[Sequence[int]],
    allocation: Allocation,
) -> dict[str, int]:
    left_variables = signature_variables(left_vertex, allocation)
    right_variables = signature_variables(right_vertex, allocation)
    checked = 0
    accepted = 0
    for left_value in range(64):
        for right_value in range(64):
            assignment: dict[int, bool] = {}
            for variable, bit in zip(left_variables, signature_bits(left_value)):
                assignment[variable] = bool(bit)
            for variable, bit in zip(
                right_variables, signature_bits(right_value)
            ):
                assignment[variable] = bool(bit)
            actual = all(
                any(
                    assignment[abs(literal)] == (literal > 0)
                    for literal in clause
                )
                for clause in clauses
            )
            expected = left_value <= right_value
            require(actual == expected, "comparator truth-table mismatch")
            checked += 1
            accepted += int(actual)
    require(checked == 4_096 and accepted == 2_080, "comparator counts")
    return {
        "assignments_checked": checked,
        "accepted_assignments": accepted,
        "rejected_assignments": checked - accepted,
    }


def adjacent_outer_permutation(left: int) -> tuple[int, ...]:
    require((left, left + 1) in ADJACENT_OUTER_TRANSPOSITIONS, "bad generator")
    result = list(range(ORDER))
    result[left], result[left + 1] = result[left + 1], result[left]
    return tuple(result)


def sorting_permutation(values: Sequence[int]) -> tuple[int, ...]:
    """Return old-vertex -> new-vertex action sorting six signatures."""

    require(
        len(values) == 6
        and all(type(value) is int and 0 <= value < 64 for value in values),
        "malformed signature list",
    )
    old_vertices = sorted(
        OUTER_VERTICES,
        key=lambda vertex: (values[vertex - 6], vertex),
    )
    permutation = list(range(ORDER))
    for new_vertex, old_vertex in zip(OUTER_VERTICES, old_vertices):
        permutation[old_vertex] = new_vertex
    return tuple(permutation)


def image_signature_values(
    values: Sequence[int], permutation: Sequence[int]
) -> tuple[int, ...]:
    image = [-1] * 6
    for old_vertex in OUTER_VERTICES:
        new_vertex = permutation[old_vertex]
        image[new_vertex - 6] = values[old_vertex - 6]
    require(-1 not in image, "signature image incomplete")
    return tuple(image)


def run() -> dict[str, object]:
    root = campaign_root()
    package = root / "results/synthesis_k3_template_bank_packages/hole5"
    cnf_path = package / "instance.cnf"
    bank_path = package / "coloring_bank.json"
    manifest_path = package / "manifest.json"

    source_payload = cnf_path.read_bytes()
    bank_payload = bank_path.read_bytes()
    manifest_payload = manifest_path.read_bytes()
    frozen_hashes = {
        "source_cnf": sha256_bytes(source_payload),
        "coloring_bank": sha256_bytes(bank_payload),
        "manifest": sha256_bytes(manifest_payload),
    }
    require(
        frozen_hashes
        == {
            "source_cnf": EXPECTED_SOURCE_CNF_SHA256,
            "coloring_bank": EXPECTED_BANK_SHA256,
            "manifest": EXPECTED_MANIFEST_SHA256,
        },
        "frozen input hash mismatch",
    )

    source = parse_dimacs(source_payload)
    require(source.variable_count == VARIABLE_COUNT, "source variable count")
    require(len(source.clauses) == FULL_CLAUSE_COUNT, "source clause count")
    require(source.literal_count == FULL_LITERAL_COUNT, "source literal count")
    require(source.header == "p cnf 6886 23653", "source header mismatch")

    manifest = json.loads(manifest_payload.decode("utf-8"))
    require(type(manifest) is dict, "manifest is not an object")
    require(
        (
            manifest.get("variable_count"),
            manifest.get("clause_count"),
            manifest.get("literal_count"),
            manifest.get("bank_count"),
        )
        == (
            VARIABLE_COUNT,
            FULL_CLAUSE_COUNT,
            FULL_LITERAL_COUNT,
            BANK_CLAUSE_COUNT,
        ),
        "manifest counts mismatch",
    )
    layout = manifest.get("clause_layout")
    require(type(layout) is dict, "manifest clause layout missing")
    require(
        (
            layout.get("base_clause_count"),
            layout.get("bank_clause_first_index_zero_based"),
            layout.get("bank_clause_end_index_exclusive"),
        )
        == (BASE_CLAUSE_COUNT, BASE_CLAUSE_COUNT, FULL_CLAUSE_COUNT),
        "manifest clause boundaries mismatch",
    )

    allocation = reconstruct_allocation()
    allocation_stream = allocation_stream_bytes(allocation)
    bank = load_bank(bank_payload)
    base_clauses = source.clauses[:BASE_CLAUSE_COUNT]
    bank_clauses = source.clauses[BASE_CLAUSE_COUNT:]
    rebuilt_bank_clauses = tuple(
        same_color_clause(row, allocation) for row in bank
    )
    require(
        bank_clauses == rebuilt_bank_clauses,
        "bank CNF suffix is not the independent row reconstruction",
    )

    rho_action = semantic_variable_action(RHO, allocation)
    require(
        all(
            rho_action[rho_action[variable]] == variable
            for variable in range(1, VARIABLE_COUNT + 1)
        ),
        "rho variable action is not involutive",
    )
    rho_action_stream = action_stream_bytes(rho_action)
    moved_by_role = Counter(
        allocation.role_by_variable[variable]
        for variable in range(1, VARIABLE_COUNT + 1)
        if rho_action[variable] != variable
    )
    fixed_by_role = Counter(
        allocation.role_by_variable[variable]
        for variable in range(1, VARIABLE_COUNT + 1)
        if rho_action[variable] == variable
    )

    base_covariance = covariance_report(base_clauses, rho_action)
    bank_covariance = covariance_report(bank_clauses, rho_action)
    full_covariance = covariance_report(source.clauses, rho_action)

    bank_set = set(bank)
    bank_images: set[tuple[int, ...]] = set()
    bank_clause_action_failures = 0
    for row in bank:
        image = transform_coloring(row, RHO)
        require(image in bank_set, "rho sends a bank row outside the bank")
        bank_images.add(image)
        if map_clause(
            same_color_clause(row, allocation), rho_action
        ) != tuple(sorted(same_color_clause(image, allocation))):
            bank_clause_action_failures += 1
    require(bank_images == bank_set, "rho bank action is not bijective")
    require(
        bank_clause_action_failures == 0,
        "rho bank row/clause action mismatch",
    )

    e05 = allocation.edge[(0, 5)]
    e15 = allocation.edge[(1, 5)]
    e25 = allocation.edge[(2, 5)]
    e35 = allocation.edge[(3, 5)]
    e45 = allocation.edge[(4, 5)]
    require(
        (e05, e15, e25, e35, e45) == (5, 15, 24, 32, 39),
        "named edge variable IDs mismatch",
    )
    require(
        (
            rho_action[e05],
            rho_action[e15],
            rho_action[e25],
            rho_action[e35],
            rho_action[e45],
        )
        == (e15, e05, e45, e35, e25),
        "rho named-edge action mismatch",
    )

    base_counter = clause_counter(base_clauses)
    required_source_clauses = {
        "unit_e05": (e05,),
        "unit_e15": (e15,),
        "no_hub_vertex_5": (-e05, -e15, -e25, -e35, -e45),
    }
    for role, clause in required_source_clauses.items():
        require(
            base_counter[tuple(sorted(clause))] == 1,
            f"required source clause {role} is not unique",
        )

    signature_clauses = signature_breaker_clauses(allocation)
    signature_stream = dimacs_clause_stream(signature_clauses)
    require(
        len(signature_stream) == SIGNATURE_STREAM_SIZE,
        "signature stream size mismatch",
    )
    require(
        sha256_bytes(signature_stream) == EXPECTED_SIGNATURE_STREAM_SHA256,
        "signature stream hash mismatch",
    )
    comparator_reports = []
    offset = 0
    for left, right in ADJACENT_OUTER_TRANSPOSITIONS:
        clauses = signature_clauses[offset : offset + 63]
        offset += 63
        comparator_reports.append(
            {
                "vertices": [left, right],
                **comparator_truth_audit(
                    left, right, clauses, allocation
                ),
            }
        )
    require(offset == SIGNATURE_CLAUSE_COUNT, "signature partition mismatch")

    t_clause = (-e25, e45)
    t_stream = dimacs_clause_stream((t_clause,))
    require(t_clause == (-24, 39), "T clause is not (-24,39)")
    require(t_stream == b"-24 39 0\n", "T DIMACS stream mismatch")

    outer_generator_reports: list[dict[str, object]] = []
    for left, right in ADJACENT_OUTER_TRANSPOSITIONS:
        permutation = adjacent_outer_permutation(left)
        action = semantic_variable_action(permutation, allocation)
        require(
            action[e25] == e25 and action[e45] == e45,
            "outer generator does not preserve T variables",
        )
        generator_covariance = covariance_report(source.clauses, action)
        outer_generator_reports.append(
            {
                "transposition": [left, right],
                "t_clause_fixed_literal_by_literal": tuple(
                    map_clause(t_clause, action)
                )
                == tuple(sorted(t_clause)),
                "full_cnf_covariance": generator_covariance,
            }
        )
    require(
        all(
            report["t_clause_fixed_literal_by_literal"] is True
            for report in outer_generator_reports
        ),
        "an S6 generator changes T",
    )

    sorting_cases_checked = 0
    for values in itertools.product(range(4), repeat=6):
        permutation = sorting_permutation(values)
        image_values = image_signature_values(values, permutation)
        require(
            image_values == tuple(sorted(values)),
            "constructive outer sorting failed",
        )
        sorting_cases_checked += 1
    require(sorting_cases_checked == 4_096, "sorting audit case count")

    cube_records: list[dict[str, object]] = []
    representatives: list[str] = []
    for x, y, z in itertools.product((0, 1), repeat=3):
        pattern = f"{x}{y}{z}"
        template_allowed = not (x == y == z == 1)
        t_allowed = (not x) or bool(z)
        rho_image = f"{z}{y}{x}"
        retained = template_allowed and t_allowed
        if retained:
            representatives.append(pattern)
        cube_records.append(
            {
                "pattern_e25_e35_e45": pattern,
                "rho_image": rho_image,
                "template_allowed_after_units_and_no_hub": template_allowed,
                "satisfies_T_e25_le_e45": t_allowed,
                "retained": retained,
            }
        )
    require(
        representatives == ["000", "001", "010", "011", "101"],
        "cube representative list mismatch",
    )
    require(
        all(
            record["satisfies_T_e25_le_e45"]
            or next(
                other
                for other in cube_records
                if other["pattern_e25_e35_e45"] == record["rho_image"]
            )["satisfies_T_e25_le_e45"]
            for record in cube_records
        ),
        "rho does not send every T failure to a T success",
    )

    derived_header = b"p cnf 6886 23969\n"
    derived_body = source.body + signature_stream + t_stream
    derived_payload = derived_header + derived_body
    derived = parse_dimacs(derived_payload)
    require(
        (
            derived.variable_count,
            len(derived.clauses),
            derived.literal_count,
        )
        == (6_886, 23_969, 192_171),
        "F-and-S-and-T derived counts mismatch",
    )
    require(
        derived.body[: len(source.body)] == source.body,
        "source body is not the exact derived prefix",
    )
    require(
        derived.body[
            len(source.body) : len(source.body) + len(signature_stream)
        ]
        == signature_stream,
        "signature stream is not the exact middle segment",
    )
    require(derived.body.endswith(t_stream), "T is not the exact suffix")

    probe_path = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "verdict": "ACCEPT_RIM_REFLECTION_AND_COMBINED_COVERAGE",
        "claim_boundary": {
            "audit_scope": (
                "formula-covariance-symmetry-coverage-and-byte-construction"
            ),
            "sat_solver_run": False,
            "hole5_sat_claim": False,
            "hole5_unsat_claim": False,
        },
        "frozen_inputs": {
            "hashes": frozen_hashes,
            "source": {
                "variables": source.variable_count,
                "clauses": len(source.clauses),
                "literals": source.literal_count,
                "header": source.header,
                "size_bytes": len(source_payload),
                "body_size_bytes": len(source.body),
                "body_sha256": sha256_bytes(source.body),
            },
            "bank_rows": len(bank),
            "bank_suffix_exactly_rebuilt": True,
        },
        "independent_allocation": {
            "variables_reconstructed": VARIABLE_COUNT,
            "role_ranges": {
                role: {
                    "first_variable": bounds[0],
                    "last_variable": bounds[1],
                    "count": bounds[2],
                }
                for role, bounds in allocation.role_ranges.items()
            },
            "allocation_stream_size_bytes": len(allocation_stream),
            "allocation_stream_sha256": sha256_bytes(allocation_stream),
        },
        "rho": {
            "vertex_action_old_to_new": list(RHO),
            "cycle_notation": "(0 1)(2 4)",
            "fixes_vertices": [3, 5, 6, 7, 8, 9, 10, 11],
            "full_variable_action": {
                "variables_mapped": VARIABLE_COUNT,
                "bijective": True,
                "involutive": True,
                "role_preserving": True,
                "action_stream_size_bytes": len(rho_action_stream),
                "action_stream_sha256": sha256_bytes(rho_action_stream),
                "moved_variables_by_role": dict(sorted(moved_by_role.items())),
                "fixed_variables_by_role": dict(sorted(fixed_by_role.items())),
            },
            "named_edge_action": {
                "e05": {"variable": e05, "image": rho_action[e05]},
                "e15": {"variable": e15, "image": rho_action[e15]},
                "e25": {"variable": e25, "image": rho_action[e25]},
                "e35": {"variable": e35, "image": rho_action[e35]},
                "e45": {"variable": e45, "image": rho_action[e45]},
            },
            "cnf_covariance": {
                "base": base_covariance,
                "bank": bank_covariance,
                "full": full_covariance,
                "semantics": (
                    "exact normalized clause multiset with multiplicity"
                ),
            },
            "bank_action": {
                "rows_mapped_inside": len(bank),
                "row_image_set_equals_bank": True,
                "row_clause_action_failures": bank_clause_action_failures,
            },
        },
        "combined_coverage": {
            "statement": "F is satisfiable iff F-and-S-and-T is satisfiable",
            "construction": (
                "if T fails apply rho; then apply an S6 permutation sorting "
                "the outer signatures"
            ),
            "rho_swaps_T_variables": [e25, e45],
            "rho_fixes_middle_cube_variable": e35,
            "every_T_failure_maps_to_T_success": True,
            "outer_S6_fixes_core_vertices": list(CORE_VERTICES),
            "outer_S6_preserves_T": True,
            "outer_generator_reports": outer_generator_reports,
            "sorting_witness": {
                "algorithm": (
                    "stable-sort old outer vertices by six-bit signature "
                    "and map them to positions 6 through 11"
                ),
                "generic_reason": (
                    "the image signature at each target position is the "
                    "signature selected for that position"
                ),
                "finite_sanity_cases_checked_over_alphabet_0_to_3": (
                    sorting_cases_checked
                ),
            },
            "signature_breaker": {
                "clauses": len(signature_clauses),
                "literals": sum(map(len, signature_clauses)),
                "size_bytes": len(signature_stream),
                "sha256": sha256_bytes(signature_stream),
                "comparator_truth_reports": comparator_reports,
            },
            "T": {
                "meaning": "e25 <= e45",
                "clause": list(t_clause),
                "stream_ascii": t_stream.decode("ascii").rstrip("\n"),
                "size_bytes": len(t_stream),
                "sha256": sha256_bytes(t_stream),
            },
        },
        "cube_reduction": {
            "coordinate_order": ["e25", "e35", "e45"],
            "variable_ids": [e25, e35, e45],
            "source_units": {
                "e05": e05,
                "e15": e15,
            },
            "source_no_hub_clause_vertex_5": list(
                required_source_clauses["no_hub_vertex_5"]
            ),
            "source_clauses_unique": True,
            "all_cube_records": cube_records,
            "retained_representatives": representatives,
            "retained_count": len(representatives),
            "excluded_by_T": ["100", "110"],
            "excluded_by_units_and_no_hub": ["111"],
        },
        "derived_F_and_S_and_T": {
            "variables": derived.variable_count,
            "clauses": len(derived.clauses),
            "literals": derived.literal_count,
            "header": derived.header,
            "size_bytes": len(derived_payload),
            "sha256": sha256_bytes(derived_payload),
            "body_size_bytes": len(derived_body),
            "body_sha256": sha256_bytes(derived_body),
            "layout": {
                "source_body_exact_prefix": True,
                "source_clauses": FULL_CLAUSE_COUNT,
                "source_body_size_bytes": len(source.body),
                "signature_exact_middle": True,
                "signature_clauses": SIGNATURE_CLAUSE_COUNT,
                "signature_stream_size_bytes": len(signature_stream),
                "T_exact_suffix": True,
                "T_clauses": 1,
                "T_stream_size_bytes": len(t_stream),
            },
            "appended": {
                "clauses": SIGNATURE_CLAUSE_COUNT + 1,
                "literals": SIGNATURE_LITERAL_COUNT + 2,
                "size_bytes": len(signature_stream) + len(t_stream),
            },
        },
        "probe": {
            "path": "reviews/hole5_rim_reflection_coverage_hostile_probe.py",
            "sha256": sha256_bytes(probe_path.read_bytes()),
        },
    }


def main() -> int:
    try:
        result = run()
    except (AuditFailure, OSError, ValueError, TypeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonical_json_bytes(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
