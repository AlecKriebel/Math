#!/usr/bin/env python3
"""Hostile standalone audit of the hole5 signature-order symmetry breaker.

This probe uses only the Python standard library.  In particular, it imports
neither the synthesis encoding nor the author's signature-breaker source.  It
reconstructs the frozen 6,886-variable allocation, checks the retained CNF
under semantic vertex actions, derives the auxiliary-free comparators from
their truth condition, and probes several plausible but invalid shortcuts.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


SCHEMA = "gamma-theta-hole5-signature-symmetry-hostile-probe-v1"
ORDER = 12
VARIABLE_COUNT = 6_886
BASE_CLAUSE_COUNT = 20_008
BANK_COUNT = 3_645
CLAUSE_COUNT = 23_653
LITERAL_COUNT = 188_959
EXPECTED_CNF_SHA256 = (
    "76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7"
)
EXPECTED_BANK_SHA256 = (
    "b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00"
)
EXPECTED_MANIFEST_SHA256 = (
    "99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402"
)
EXPECTED_CANDIDATE_SHA256 = (
    "2ca819277fa56e7c20071d498c62d72bb881efb761bb1c76d07fb782de2b3ff7"
)
EXPECTED_COLORING_SHA256 = (
    "7f2a239ef040ccb6ce4656347a873de434da3bcf02fabe459f71b600f3af4c7d"
)
EXPECTED_SOLVER_RESULT_GZIP_SHA256 = (
    "e7e4d1f547a167d61aae301fd6e1ccc1d0ab5696e20894a9a087076693a33e75"
)
EXPECTED_SOLVER_RESULT_PAYLOAD_SHA256 = (
    "ff0591d3cff245fb7277d0d310e8037d80cfef03a019782cf8dc117d0bb806aa"
)
EXPECTED_CHECKPOINT_SHA256 = (
    "ca4556b6d8b931d71b7b143d1e8b7c3aab4475fa1edae90a83c7acb107100b55"
)

FIXED_VERTICES = tuple(range(6))
OUTER_VERTICES = tuple(range(6, 12))
ADJACENT_OUTER_PAIRS = tuple(zip(OUTER_VERTICES, OUTER_VERTICES[1:]))
HOLE5_POSITIVE_EDGES = frozenset(
    {
        (0, 1),
        (0, 4),
        (0, 5),
        (1, 2),
        (1, 5),
        (2, 3),
        (3, 4),
    }
)
RIM_REFLECTION = (1, 0, 4, 3, 2, 5, 6, 7, 8, 9, 10, 11)


class AuditFailure(ValueError):
    """A frozen artifact or a proposed mathematical claim failed audit."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def campaign_root() -> Path:
    source = Path(__file__).resolve()
    for ancestor in source.parents:
        package = (
            ancestor
            / "results/synthesis_k3_template_bank_packages/hole5"
        )
        if (package / "instance.cnf").is_file() and (
            package / "coloring_bank.json"
        ).is_file():
            return ancestor
    raise AuditFailure("cannot locate the campaign root")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def strict_json(path: Path, role: str) -> object:
    def reject_constant(token: str) -> object:
        raise AuditFailure(f"{role}: non-finite JSON constant {token!r}")

    def unique_object(
        pairs: list[tuple[str, object]],
    ) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"{role}: duplicate key {key!r}")
            result[key] = value
        return result

    payload = path.read_bytes()
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AuditFailure(f"{role}: not UTF-8") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise AuditFailure(f"{role}: malformed JSON") from error


@dataclass(frozen=True)
class ParsedCNF:
    variable_count: int
    clauses: tuple[tuple[int, ...], ...]
    literal_count: int


def parse_dimacs(path: Path) -> ParsedCNF:
    header: tuple[int, int] | None = None
    clauses: list[tuple[int, ...]] = []
    literal_count = 0
    for line_number, raw in enumerate(path.read_bytes().splitlines(), 1):
        require(raw == raw.strip(), f"CNF line {line_number}: whitespace")
        if not raw or raw.startswith(b"c"):
            continue
        fields = raw.split()
        if fields[0] == b"p":
            require(header is None, "CNF has multiple headers")
            require(
                len(fields) == 4 and fields[1] == b"cnf",
                "malformed CNF header",
            )
            header = (int(fields[2]), int(fields[3]))
            continue
        require(header is not None, "CNF clause precedes header")
        try:
            numbers = tuple(int(field) for field in fields)
        except ValueError as error:
            raise AuditFailure(f"CNF line {line_number}: noninteger") from error
        require(numbers and numbers[-1] == 0, "CNF clause lacks terminal zero")
        clause = numbers[:-1]
        require(0 not in clause, "CNF clause has an internal zero")
        require(
            all(abs(literal) <= header[0] for literal in clause),
            "CNF literal exceeds declared variables",
        )
        require(len(set(clause)) == len(clause), "duplicate CNF literal")
        require(
            all(-literal not in clause for literal in clause),
            "tautological CNF clause",
        )
        clauses.append(clause)
        literal_count += len(clause)
    require(header is not None, "CNF header missing")
    require(len(clauses) == header[1], "CNF clause-count mismatch")
    return ParsedCNF(header[0], tuple(clauses), literal_count)


Pair = tuple[int, int]
Triple = tuple[int, int, int]


def ordered_pair(first: int, second: int) -> Pair:
    require(first != second, "loop is not a graph edge")
    return (first, second) if first < second else (second, first)


@dataclass(frozen=True)
class Allocation:
    edge: Mapping[Pair, int]
    witness: Mapping[tuple[int, int, int], int]
    family: Mapping[Triple, int]
    move: Mapping[tuple[Triple, int, int], int]
    role_by_variable: tuple[str, ...]
    role_ranges: Mapping[str, tuple[int, int, int]]


def reconstruct_allocation() -> Allocation:
    """Independently recreate the documented consecutive allocation."""

    next_variable = 1
    role_by_variable = [""]

    def allocate(role: str) -> int:
        nonlocal next_variable
        variable = next_variable
        next_variable += 1
        role_by_variable.append(role)
        return variable

    edge = {
        pair: allocate("edge")
        for pair in itertools.combinations(range(ORDER), 2)
    }
    witness = {
        (first, second, third): allocate("witness")
        for first, second in itertools.combinations(range(ORDER), 2)
        for third in range(ORDER)
        if third not in (first, second)
    }
    family = {
        triple: allocate("family")
        for triple in itertools.combinations(range(ORDER), 3)
    }
    move = {
        (triple, attacked, guard): allocate("move")
        for triple in itertools.combinations(range(ORDER), 3)
        for attacked in range(ORDER)
        if attacked not in triple
        for guard in triple
    }
    require(next_variable == VARIABLE_COUNT + 1, "allocation size mismatch")
    counts = Counter(role_by_variable[1:])
    require(
        counts
        == {
            "edge": 66,
            "witness": 660,
            "family": 220,
            "move": 5_940,
        },
        "allocation role counts mismatch",
    )
    role_ranges: dict[str, tuple[int, int, int]] = {}
    for role in ("edge", "witness", "family", "move"):
        variables = [
            variable
            for variable, actual in enumerate(role_by_variable)
            if actual == role
        ]
        require(
            variables == list(range(variables[0], variables[-1] + 1)),
            f"{role} variables are not consecutive",
        )
        role_ranges[role] = (
            variables[0],
            variables[-1],
            len(variables),
        )
    return Allocation(
        edge=edge,
        witness=witness,
        family=family,
        move=move,
        role_by_variable=tuple(role_by_variable),
        role_ranges=role_ranges,
    )


def canonicalize_color_names(row: Sequence[int]) -> tuple[int, ...]:
    names: dict[int, int] = {}
    result: list[int] = []
    for color in row:
        if color not in names:
            names[color] = len(names)
        result.append(names[color])
    return tuple(result)


def validate_bank(
    value: object,
) -> tuple[tuple[int, ...], ...]:
    require(type(value) is list, "bank root is not a list")
    require(len(value) == BANK_COUNT, "bank count mismatch")
    rows: list[tuple[int, ...]] = []
    for row_index, raw in enumerate(value):
        require(type(raw) is list and len(raw) == ORDER, "malformed bank row")
        require(
            all(type(color) is int and color in (0, 1, 2) for color in raw),
            "bank color outside 0..2",
        )
        row = tuple(raw)
        require(
            canonicalize_color_names(row) == row,
            f"bank row {row_index} is not first-use canonical",
        )
        require(
            all(row[first] != row[second] for first, second in HOLE5_POSITIVE_EDGES),
            f"bank row {row_index} violates a positive template edge",
        )
        rows.append(row)
    require(rows == sorted(rows), "bank rows are not lexicographically sorted")
    require(len(set(rows)) == len(rows), "bank has duplicate rows")
    return tuple(rows)


def same_color_clause(
    row: Sequence[int], allocation: Allocation
) -> tuple[int, ...]:
    return tuple(
        allocation.edge[(first, second)]
        for first, second in itertools.combinations(range(ORDER), 2)
        if row[first] == row[second]
    )


def adjacent_transposition(left: int) -> tuple[int, ...]:
    require(left in range(6, 11), "not an adjacent outer transposition")
    permutation = list(range(ORDER))
    permutation[left], permutation[left + 1] = (
        permutation[left + 1],
        permutation[left],
    )
    return tuple(permutation)


def semantic_variable_action(
    permutation: Sequence[int], allocation: Allocation
) -> tuple[int, ...]:
    """Map every variable under old-vertex -> new-vertex relabeling."""

    require(
        sorted(permutation) == list(range(ORDER)),
        "vertex action is not a permutation",
    )
    action = [0] * (VARIABLE_COUNT + 1)
    for (first, second), variable in allocation.edge.items():
        action[variable] = allocation.edge[
            ordered_pair(permutation[first], permutation[second])
        ]
    for (first, second, third), variable in allocation.witness.items():
        image_pair = ordered_pair(
            permutation[first],
            permutation[second],
        )
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
            (
                image_triple,
                permutation[attacked],
                permutation[guard],
            )
        ]
    require(
        sorted(action[1:]) == list(range(1, VARIABLE_COUNT + 1)),
        "semantic variable action is not bijective",
    )
    return tuple(action)


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


def counter_difference(
    expected: Counter[tuple[int, ...]],
    actual: Counter[tuple[int, ...]],
) -> dict[str, object]:
    missing = expected - actual
    extra = actual - expected
    return {
        "equal": not missing and not extra,
        "missing_occurrences": sum(missing.values()),
        "extra_occurrences": sum(extra.values()),
        "first_missing_clause": list(next(iter(missing))) if missing else None,
        "first_extra_clause": list(next(iter(extra))) if extra else None,
    }


def transform_coloring(
    row: Sequence[int], permutation: Sequence[int]
) -> tuple[int, ...]:
    image = [-1] * ORDER
    for old_vertex, new_vertex in enumerate(permutation):
        image[new_vertex] = row[old_vertex]
    require(-1 not in image, "coloring action did not fill every vertex")
    return canonicalize_color_names(image)


def signature_variables(
    outer_vertex: int, allocation: Allocation
) -> tuple[int, ...]:
    require(outer_vertex in OUTER_VERTICES, "signature vertex is not outer")
    return tuple(
        allocation.edge[ordered_pair(fixed, outer_vertex)]
        for fixed in FIXED_VERTICES
    )


def lex_comparator_clauses(
    left_vertex: int,
    right_vertex: int,
    allocation: Allocation,
) -> tuple[tuple[int, ...], ...]:
    """Auxiliary-free CNF for signature(left) <=lex signature(right)."""

    left = signature_variables(left_vertex, allocation)
    right = signature_variables(right_vertex, allocation)
    clauses: list[tuple[int, ...]] = []
    for pivot in range(len(FIXED_VERTICES)):
        for prefix in itertools.product((0, 1), repeat=pivot):
            clause: list[int] = []
            for index, bit in enumerate(prefix):
                if bit == 0:
                    clause.extend((left[index], right[index]))
                else:
                    clause.extend((-left[index], -right[index]))
            clause.extend((-left[pivot], right[pivot]))
            require(len(set(clause)) == len(clause), "duplicate comparator literal")
            require(
                all(-literal not in clause for literal in clause),
                "tautological comparator clause",
            )
            clauses.append(tuple(clause))
    return tuple(clauses)


def signature_bits(value: int) -> tuple[int, ...]:
    require(0 <= value < 64, "signature integer outside 0..63")
    return tuple((value >> (5 - index)) & 1 for index in range(6))


def signature_assignment(
    left_value: int,
    right_value: int,
    left_vertex: int,
    right_vertex: int,
    allocation: Allocation,
) -> dict[int, bool]:
    result: dict[int, bool] = {}
    for variable, bit in zip(
        signature_variables(left_vertex, allocation),
        signature_bits(left_value),
    ):
        result[variable] = bool(bit)
    for variable, bit in zip(
        signature_variables(right_vertex, allocation),
        signature_bits(right_value),
    ):
        require(variable not in result, "signature variable overlap")
        result[variable] = bool(bit)
    return result


def clause_value(clause: Sequence[int], assignment: Mapping[int, bool]) -> bool:
    return any(
        assignment[abs(literal)] == (literal > 0) for literal in clause
    )


def comparator_semantics(
    clauses: Sequence[Sequence[int]],
    left_vertex: int,
    right_vertex: int,
    allocation: Allocation,
) -> dict[str, object]:
    mismatch_count = 0
    first_mismatch: dict[str, object] | None = None
    accepted_count = 0
    rejected_count = 0
    essential: set[int] = set()
    values: dict[tuple[int, int], bool] = {}
    for left_value in range(64):
        for right_value in range(64):
            assignment = signature_assignment(
                left_value,
                right_value,
                left_vertex,
                right_vertex,
                allocation,
            )
            failed = [
                index
                for index, clause in enumerate(clauses)
                if not clause_value(clause, assignment)
            ]
            actual = not failed
            expected = signature_bits(left_value) <= signature_bits(right_value)
            values[(left_value, right_value)] = actual
            if actual:
                accepted_count += 1
            else:
                rejected_count += 1
            if actual != expected:
                mismatch_count += 1
                if first_mismatch is None:
                    first_mismatch = {
                        "left": list(signature_bits(left_value)),
                        "right": list(signature_bits(right_value)),
                        "expected": expected,
                        "actual": actual,
                    }
            if not expected and len(failed) == 1:
                essential.add(failed[0])
    both_orientations_rejected: dict[str, object] | None = None
    for first in range(64):
        for second in range(first + 1, 64):
            if not values[(first, second)] and not values[(second, first)]:
                both_orientations_rejected = {
                    "first": list(signature_bits(first)),
                    "second": list(signature_bits(second)),
                }
                break
        if both_orientations_rejected is not None:
            break
    return {
        "assignment_count": 4_096,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "semantic_mismatch_count": mismatch_count,
        "first_semantic_mismatch": first_mismatch,
        "clauses_with_unique_violating_witness": len(essential),
        "both_orientations_rejected_example": both_orientations_rejected,
    }


def coordinatewise_mutation(
    left_vertex: int,
    right_vertex: int,
    allocation: Allocation,
) -> tuple[tuple[int, ...], ...]:
    left = signature_variables(left_vertex, allocation)
    right = signature_variables(right_vertex, allocation)
    return tuple((-first, second) for first, second in zip(left, right))


def one_sided_prefix_mutation(
    left_vertex: int,
    right_vertex: int,
    allocation: Allocation,
) -> tuple[tuple[int, ...], ...]:
    """Plausible error: one literal, rather than two, per prefix bit."""

    left = signature_variables(left_vertex, allocation)
    right = signature_variables(right_vertex, allocation)
    clauses: list[tuple[int, ...]] = []
    for pivot in range(6):
        for prefix in itertools.product((0, 1), repeat=pivot):
            clause = [
                left[index] if bit == 0 else -left[index]
                for index, bit in enumerate(prefix)
            ]
            clause.extend((-left[pivot], right[pivot]))
            clauses.append(tuple(clause))
    return tuple(clauses)


def first_coordinate_only(
    left_vertex: int,
    right_vertex: int,
    allocation: Allocation,
) -> tuple[tuple[int, ...], ...]:
    left = signature_variables(left_vertex, allocation)
    right = signature_variables(right_vertex, allocation)
    return ((-left[0], right[0]),)


def dimacs_clause_stream(clauses: Iterable[Sequence[int]]) -> bytes:
    return b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in clauses
    )


def parse_gzip_sat_model(
    path: Path, variable_count: int
) -> tuple[tuple[bool, ...], str]:
    compressed = path.read_bytes()
    try:
        payload = gzip.decompress(compressed)
    except gzip.BadGzipFile as error:
        raise AuditFailure("candidate solver result is not valid gzip") from error
    status_count = 0
    literals: list[int] = []
    for line in payload.splitlines():
        fields = line.split()
        if not fields:
            continue
        if fields[0] == b"s":
            require(fields == [b"s", b"SATISFIABLE"], "candidate not SAT")
            status_count += 1
        elif fields[0] == b"v":
            for field in fields[1:]:
                literal = int(field)
                if literal:
                    literals.append(literal)
        else:
            raise AuditFailure("unexpected candidate model record")
    require(status_count == 1, "candidate model status count is not one")
    require(len(literals) == variable_count, "candidate model is incomplete")
    require(
        {abs(literal) for literal in literals}
        == set(range(1, variable_count + 1)),
        "candidate model variables are not exact",
    )
    assignment = [False] * (variable_count + 1)
    for literal in literals:
        assignment[abs(literal)] = literal > 0
    return tuple(assignment), sha256_bytes(payload)


def cnf_clause_satisfied(
    clause: Sequence[int], assignment: Sequence[bool]
) -> bool:
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


def gamma_orbits(
    bank: Sequence[tuple[int, ...]],
) -> tuple[dict[tuple[int, ...], tuple[int, ...]], dict[tuple[int, ...], set[tuple[int, ...]]]]:
    bank_set = set(bank)
    representative_of: dict[tuple[int, ...], tuple[int, ...]] = {}
    members: dict[tuple[int, ...], set[tuple[int, ...]]] = {}
    outer_permutations = tuple(itertools.permutations(OUTER_VERTICES))
    for row in bank:
        if row in representative_of:
            continue
        orbit: set[tuple[int, ...]] = set()
        for outer in outer_permutations:
            for reflect in (False, True):
                permutation = list(
                    RIM_REFLECTION if reflect else range(ORDER)
                )
                for index, image in enumerate(outer):
                    permutation[6 + index] = image
                orbit.add(transform_coloring(row, permutation))
        require(orbit <= bank_set, "Gamma sends a bank row outside the bank")
        representative = min(orbit)
        members[representative] = orbit
        for image in orbit:
            require(image not in representative_of, "bank orbits overlap")
            representative_of[image] = representative
    require(len(representative_of) == len(bank), "bank orbits incomplete")
    return representative_of, members


def run() -> dict[str, object]:
    root = campaign_root()
    package = root / "results/synthesis_k3_template_bank_packages/hole5"
    cnf_path = package / "instance.cnf"
    bank_path = package / "coloring_bank.json"
    manifest_path = package / "manifest.json"
    attempt = (
        root
        / "results/synthesis_k3_runs/hole5/attempts/000001.smg8hvs_"
    )
    candidate_path = attempt / "decoded-candidate.json"
    coloring_path = attempt / "coloring.json"
    solver_result_path = attempt / "solver.result.gz"
    checkpoint_path = root / "results/synthesis_k3_runs/hole5/checkpoint.json"

    hashes = {
        "cnf": sha256_file(cnf_path),
        "bank": sha256_file(bank_path),
        "manifest": sha256_file(manifest_path),
        "candidate": sha256_file(candidate_path),
        "candidate_coloring": sha256_file(coloring_path),
        "candidate_solver_result_gzip": sha256_file(solver_result_path),
        "checkpoint": sha256_file(checkpoint_path),
    }
    require(hashes["cnf"] == EXPECTED_CNF_SHA256, "CNF hash mismatch")
    require(hashes["bank"] == EXPECTED_BANK_SHA256, "bank hash mismatch")
    require(
        hashes["manifest"] == EXPECTED_MANIFEST_SHA256,
        "manifest hash mismatch",
    )
    require(
        hashes["candidate"] == EXPECTED_CANDIDATE_SHA256,
        "candidate hash mismatch",
    )
    require(
        hashes["candidate_coloring"] == EXPECTED_COLORING_SHA256,
        "candidate coloring hash mismatch",
    )
    require(
        hashes["candidate_solver_result_gzip"]
        == EXPECTED_SOLVER_RESULT_GZIP_SHA256,
        "candidate solver-result hash mismatch",
    )
    require(
        hashes["checkpoint"] == EXPECTED_CHECKPOINT_SHA256,
        "checkpoint hash mismatch",
    )

    cnf = parse_dimacs(cnf_path)
    require(cnf.variable_count == VARIABLE_COUNT, "CNF variable count")
    require(len(cnf.clauses) == CLAUSE_COUNT, "CNF clause count")
    require(cnf.literal_count == LITERAL_COUNT, "CNF literal count")
    manifest = strict_json(manifest_path, "package manifest")
    require(type(manifest) is dict, "package manifest is not an object")
    require(manifest.get("bank_count") == BANK_COUNT, "manifest bank count")
    require(
        manifest.get("clause_count") == CLAUSE_COUNT,
        "manifest clause count",
    )
    require(
        manifest.get("variable_count") == VARIABLE_COUNT,
        "manifest variable count",
    )
    bank = validate_bank(strict_json(bank_path, "coloring bank"))
    allocation = reconstruct_allocation()

    rebuilt_bank_clauses = tuple(
        same_color_clause(row, allocation) for row in bank
    )
    cnf_bank_clauses = cnf.clauses[BASE_CLAUSE_COUNT:]
    require(
        rebuilt_bank_clauses == cnf_bank_clauses,
        "independent bank clauses do not equal the CNF suffix",
    )

    full_counter = clause_counter(cnf.clauses)
    base_counter = clause_counter(cnf.clauses[:BASE_CLAUSE_COUNT])
    bank_counter = clause_counter(cnf_bank_clauses)
    bank_set = set(bank)
    generator_checks: list[dict[str, object]] = []
    for left, right in ADJACENT_OUTER_PAIRS:
        permutation = adjacent_transposition(left)
        action = semantic_variable_action(permutation, allocation)
        mapped_full = Counter(
            map_clause(clause, action) for clause in cnf.clauses
        )
        mapped_base = Counter(
            map_clause(clause, action)
            for clause in cnf.clauses[:BASE_CLAUSE_COUNT]
        )
        mapped_bank = Counter(
            map_clause(clause, action) for clause in cnf_bank_clauses
        )
        full_difference = counter_difference(full_counter, mapped_full)
        base_difference = counter_difference(base_counter, mapped_base)
        bank_difference = counter_difference(bank_counter, mapped_bank)
        require(full_difference["equal"] is True, "full CNF not invariant")
        require(base_difference["equal"] is True, "base CNF not invariant")
        require(bank_difference["equal"] is True, "bank CNF not invariant")

        row_failures = 0
        clause_action_failures = 0
        images: set[tuple[int, ...]] = set()
        for row in bank:
            image = transform_coloring(row, permutation)
            images.add(image)
            if image not in bank_set:
                row_failures += 1
            if map_clause(same_color_clause(row, allocation), action) != tuple(
                sorted(same_color_clause(image, allocation))
            ):
                clause_action_failures += 1
        require(row_failures == 0, "bank row action failure")
        require(images == bank_set, "bank row action is not bijective")
        require(clause_action_failures == 0, "bank clause action failure")
        moved_by_role = Counter(
            allocation.role_by_variable[variable]
            for variable in range(1, VARIABLE_COUNT + 1)
            if action[variable] != variable
        )
        generator_checks.append(
            {
                "transposition": [left, right],
                "variable_action_bijective": True,
                "moved_variables_by_role": dict(sorted(moved_by_role.items())),
                "full_cnf_multiset": full_difference,
                "base_cnf_multiset": base_difference,
                "bank_cnf_multiset": bank_difference,
                "bank_rows_mapped_inside": len(bank),
                "bank_row_action_failures": row_failures,
                "bank_clause_action_failures": clause_action_failures,
            }
        )

    comparator_clauses: list[tuple[int, ...]] = []
    comparator_checks: list[dict[str, object]] = []
    for left, right in ADJACENT_OUTER_PAIRS:
        clauses = lex_comparator_clauses(left, right, allocation)
        require(len(clauses) == 63, "comparator clause count is not 63")
        require(
            sum(map(len, clauses)) == 642,
            "comparator literal count is not 642",
        )
        semantics = comparator_semantics(
            clauses,
            left,
            right,
            allocation,
        )
        require(
            semantics["semantic_mismatch_count"] == 0,
            "lex comparator truth-table mismatch",
        )
        require(
            semantics["accepted_count"] == 2_080
            and semantics["rejected_count"] == 2_016,
            "lex comparator truth-table counts mismatch",
        )
        require(
            semantics["clauses_with_unique_violating_witness"] == 63,
            "a comparator clause lacks an essential witness",
        )
        require(
            semantics["both_orientations_rejected_example"] is None,
            "lex order fails pairwise orbit coverage",
        )
        comparator_clauses.extend(clauses)
        comparator_checks.append(
            {
                "adjacent_vertices": [left, right],
                "clause_count": len(clauses),
                "literal_count": sum(map(len, clauses)),
                **semantics,
            }
        )
    require(len(comparator_clauses) == 315, "combined comparator clauses")
    require(
        sum(map(len, comparator_clauses)) == 3_210,
        "combined comparator literals",
    )
    require(
        len({tuple(sorted(clause)) for clause in comparator_clauses}) == 315,
        "duplicate combined comparator clause",
    )
    length_distribution = Counter(map(len, comparator_clauses))
    require(
        length_distribution == {2: 5, 4: 10, 6: 20, 8: 40, 10: 80, 12: 160},
        "comparator clause-length distribution mismatch",
    )
    comparator_stream = dimacs_clause_stream(comparator_clauses)

    mutation_left, mutation_right = ADJACENT_OUTER_PAIRS[0]
    coordinatewise = coordinatewise_mutation(
        mutation_left,
        mutation_right,
        allocation,
    )
    coordinatewise_stats = comparator_semantics(
        coordinatewise,
        mutation_left,
        mutation_right,
        allocation,
    )
    require(
        coordinatewise_stats["semantic_mismatch_count"] > 0
        and coordinatewise_stats["both_orientations_rejected_example"]
        is not None,
        "coordinatewise mutation did not expose lost orbit coverage",
    )
    one_sided = one_sided_prefix_mutation(
        mutation_left,
        mutation_right,
        allocation,
    )
    one_sided_stats = comparator_semantics(
        one_sided,
        mutation_left,
        mutation_right,
        allocation,
    )
    require(
        one_sided_stats["semantic_mismatch_count"] > 0
        and one_sided_stats["both_orientations_rejected_example"] is not None,
        "one-sided-prefix mutation did not expose lost coverage",
    )
    descending = lex_comparator_clauses(
        mutation_right,
        mutation_left,
        allocation,
    )
    descending_stats = comparator_semantics(
        descending,
        mutation_left,
        mutation_right,
        allocation,
    )
    require(
        descending_stats["semantic_mismatch_count"] > 0
        and descending_stats["both_orientations_rejected_example"] is None,
        "descending mutation classification failed",
    )
    first_only = first_coordinate_only(
        mutation_left,
        mutation_right,
        allocation,
    )
    first_only_stats = comparator_semantics(
        first_only,
        mutation_left,
        mutation_right,
        allocation,
    )
    require(
        first_only_stats["semantic_mismatch_count"] > 0
        and first_only_stats["both_orientations_rejected_example"] is None,
        "first-coordinate weaker breaker classification failed",
    )

    permutation = adjacent_transposition(6)
    correct_action = semantic_variable_action(permutation, allocation)
    edge_only_action = list(range(VARIABLE_COUNT + 1))
    for variable, role in enumerate(allocation.role_by_variable):
        if role == "edge":
            edge_only_action[variable] = correct_action[variable]
    edge_only_mapped = Counter(
        map_clause(clause, edge_only_action) for clause in cnf.clauses
    )
    edge_only_difference = counter_difference(
        full_counter,
        edge_only_mapped,
    )
    require(
        edge_only_difference["equal"] is False,
        "edge-only relabeling unexpectedly preserves the full CNF",
    )
    unsorted_witness_source = (6, 7, 0)
    unsorted_witness_image = (
        permutation[6],
        permutation[7],
        permutation[0],
    )
    require(
        unsorted_witness_image not in allocation.witness,
        "failure to sort the witness pair was not detected",
    )

    model, model_payload_sha256 = parse_gzip_sat_model(
        solver_result_path,
        VARIABLE_COUNT,
    )
    require(
        model_payload_sha256 == EXPECTED_SOLVER_RESULT_PAYLOAD_SHA256,
        "candidate model payload hash mismatch",
    )
    checkpoint = strict_json(checkpoint_path, "hole5 checkpoint")
    require(type(checkpoint) is dict, "checkpoint is not an object")
    cuts = checkpoint.get("cuts")
    require(type(cuts) is list and cuts, "checkpoint cuts missing")
    first_cut = cuts[0]
    require(type(first_cut) is dict, "first checkpoint cut malformed")
    first_clause = first_cut.get("clause")
    require(
        type(first_clause) is list
        and all(type(literal) is int for literal in first_clause),
        "first checkpoint clause malformed",
    )
    candidate_formula = (
        cnf.clauses[:BASE_CLAUSE_COUNT] + (tuple(first_clause),)
    )
    unsatisfied_candidate_clauses = [
        index
        for index, clause in enumerate(candidate_formula)
        if not cnf_clause_satisfied(clause, model)
    ]
    require(
        not unsatisfied_candidate_clauses,
        "retained attempt-1 model does not satisfy base plus cut 0",
    )
    candidate = strict_json(candidate_path, "decoded candidate")
    require(type(candidate) is dict, "decoded candidate is not an object")
    raw_h_edges = candidate.get("h_edges")
    require(type(raw_h_edges) is list, "decoded H-edge list missing")
    decoded_h_edges: set[Pair] = set()
    for raw_edge in raw_h_edges:
        require(
            type(raw_edge) is list
            and len(raw_edge) == 2
            and all(type(vertex) is int for vertex in raw_edge),
            "decoded H edge is malformed",
        )
        require(
            all(0 <= vertex < ORDER for vertex in raw_edge),
            "decoded H-edge endpoint outside the graph",
        )
        edge = ordered_pair(raw_edge[0], raw_edge[1])
        require(edge not in decoded_h_edges, "duplicate decoded H edge")
        decoded_h_edges.add(edge)
    model_h_edges = {
        pair for pair, variable in allocation.edge.items() if model[variable]
    }
    require(
        decoded_h_edges == model_h_edges,
        "decoded H edges disagree with the independently parsed model",
    )
    candidate_coloring_value = strict_json(
        coloring_path,
        "candidate coloring",
    )
    require(
        type(candidate_coloring_value) is list
        and len(candidate_coloring_value) == ORDER
        and all(
            type(color) is int and color in (0, 1, 2)
            for color in candidate_coloring_value
        ),
        "candidate coloring is malformed",
    )
    candidate_coloring = tuple(candidate_coloring_value)
    require(candidate_coloring in bank_set, "candidate coloring outside bank")
    proper_rows = [
        row
        for row in bank
        if all(
            row[first] != row[second]
            for first, second in decoded_h_edges
        )
    ]
    require(candidate_coloring in proper_rows, "candidate coloring not proper")
    representative_of, orbit_members = gamma_orbits(bank)
    representatives = sorted(orbit_members)
    representative_violations = [
        row
        for row in representatives
        if all(
            row[first] != row[second]
            for first, second in decoded_h_edges
        )
    ]
    require(len(orbit_members) == 72, "Gamma orbit count mismatch")
    require(
        not representative_violations,
        "candidate violates a lex-min Gamma representative cut",
    )
    require(
        proper_rows,
        "candidate does not violate any complete-bank cut",
    )
    candidate_orbit_representative = representative_of[candidate_coloring]
    representative_true_witnesses = [
        list(edge)
        for edge in sorted(decoded_h_edges)
        if candidate_orbit_representative[edge[0]]
        == candidate_orbit_representative[edge[1]]
    ]
    require(
        representative_true_witnesses,
        "candidate unexpectedly falsifies its coloring-orbit representative",
    )
    orbit_size_distribution = Counter(map(len, orbit_members.values()))

    probe_path = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "verdict": "ACCEPT_SIGNATURE_BREAKER_REJECT_SHORTCUTS",
        "claim_boundary": {
            "sat_solve_performed": False,
            "unsat_claim": False,
            "author_source_or_note_read": False,
            "author_artifacts": {
                "src/synthesis_k3/hole5_signature_breaker.py": {
                    "binding": None,
                    "reason": "untracked and deliberately unread at audit start",
                },
                "math/lemmas/hole5_signature_symmetry.md": {
                    "binding": None,
                    "reason": "untracked and deliberately unread at audit start",
                },
            },
        },
        "frozen_inputs": {
            "hashes": hashes,
            "probe_sha256": sha256_file(probe_path),
            "cnf": {
                "variables": cnf.variable_count,
                "clauses": len(cnf.clauses),
                "literals": cnf.literal_count,
                "base_clauses": BASE_CLAUSE_COUNT,
                "bank_clauses": len(cnf_bank_clauses),
            },
            "bank_suffix_exactly_rebuilt": True,
        },
        "allocation": {
            role: {
                "first_variable": bounds[0],
                "last_variable": bounds[1],
                "count": bounds[2],
            }
            for role, bounds in allocation.role_ranges.items()
        },
        "s6_invariance": {
            "generators_checked": len(generator_checks),
            "adjacent_generators_generate_s6": True,
            "checks": generator_checks,
        },
        "signature_comparator": {
            "signature_coordinates": list(FIXED_VERTICES),
            "ordered_vertices": list(OUTER_VERTICES),
            "combined_clause_count": len(comparator_clauses),
            "combined_literal_count": sum(map(len, comparator_clauses)),
            "clause_length_distribution": {
                str(length): count
                for length, count in sorted(length_distribution.items())
            },
            "dimacs_clause_stream_sha256": sha256_bytes(comparator_stream),
            "dimacs_clause_stream_size_bytes": len(comparator_stream),
            "adjacent_pair_checks": comparator_checks,
        },
        "sorting_coverage": {
            "lexicographic_order_is_total": True,
            "every_six_signature_multiset_can_be_sorted": True,
            "outer_vertex_action_preserves_fixed_signature_coordinates": True,
            "transported_roles": [
                "edge",
                "witness",
                "family",
                "move",
                "coloring_bank",
            ],
            "formula_equisatisfiability_conclusion": True,
        },
        "hostile_mutations": {
            "coordinatewise_order": {
                "classification": "REJECT_UNSOUND_LOST_ORBIT_COVERAGE",
                **coordinatewise_stats,
            },
            "one_sided_prefix_literals": {
                "classification": "REJECT_UNSOUND_LOST_ORBIT_COVERAGE",
                **one_sided_stats,
            },
            "descending_lex": {
                "classification": "REJECT_WRONG_SPEC_BUT_SOUND_IF_DOCUMENTED",
                **descending_stats,
            },
            "first_coordinate_only": {
                "classification": "SOUND_BUT_STRICTLY_WEAKER",
                **first_only_stats,
            },
            "edge_variables_only_action": {
                "classification": "REJECT_FULL_ASSIGNMENT_NOT_TRANSPORTED",
                "full_cnf_multiset": edge_only_difference,
            },
            "unsorted_witness_pair_action": {
                "classification": "REJECT_NOT_A_VARIABLE_ACTION",
                "source_key": list(unsorted_witness_source),
                "malformed_image_key": list(unsorted_witness_image),
            },
        },
        "orbit_representative_conflation": {
            "classification": "REJECT",
            "candidate_model": {
                "satisfies_base_plus_first_cegar_cut": True,
                "unsatisfied_clause_count": len(unsatisfied_candidate_clauses),
                "model_payload_sha256": model_payload_sha256,
                "proper_bank_row_indices": [
                    bank.index(row) for row in proper_rows
                ],
            },
            "gamma_order": 1_440,
            "gamma_orbit_count": len(orbit_members),
            "gamma_orbit_size_distribution": {
                str(size): count
                for size, count in sorted(orbit_size_distribution.items())
            },
            "all_lex_min_representative_cuts_satisfied": True,
            "candidate_coloring_bank_index": bank.index(candidate_coloring),
            "candidate_coloring_orbit_representative_bank_index": bank.index(
                candidate_orbit_representative
            ),
            "representative_cut_true_h_edge_witnesses": (
                representative_true_witnesses
            ),
            "reason": (
                "sorting applies one global graph relabeling; it cannot "
                "independently relabel each coloring cut"
            ),
        },
    }


def main() -> int:
    try:
        result = run()
    except (AuditFailure, OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    sys.stdout.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
