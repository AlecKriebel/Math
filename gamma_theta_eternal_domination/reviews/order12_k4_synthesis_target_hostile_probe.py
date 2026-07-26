#!/usr/bin/env python3
"""Clean-room audit of the exact order-12, parameter-four parent CNF.

This probe is deliberately standard-library-only.  It imports neither
``synthesis_k4`` nor ``synthesis_k3``.  It independently allocates every
semantic variable, reconstructs every clause, invokes the reviewed generator
only in isolated child processes, and compares the resulting DIMACS bytes.

The output is canonical JSON: temporary paths, timings, process identifiers,
and other run-specific values are excluded.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Mapping, Sequence


SCHEMA = "gamma-theta-order12-k4-hostile-probe-v1"
N = 12
K = 4
VERTICES = tuple(range(N))
ANCHOR = (0, 1, 2, 3)
OUTER = tuple(range(4, N))
Pair = tuple[int, int]
Triple = tuple[int, int, int]
State = tuple[int, int, int, int]
Clause = tuple[int, ...]

REVIEWED_FILES = {
    "math/lemmas/order12_k4_synthesis_target.md": (
        19_489,
        "5421357c5095113ac598afa22fa5a4e3623ef19d3c3a7a348b6c6c9a29945671",
    ),
    "src/synthesis_k4/__init__.py": (
        58,
        "05e51b8d8a86f51f045db00dc10f4042dcf25218448473193b620fc87fe76d3d",
    ),
    "src/synthesis_k4/encoding.py": (
        18_036,
        "193d3e4984cd2fcfa327cc693d518221ba51544bf8ea9e0cbca37c693e34e2e0",
    ),
    "src/synthesis_k4/generate.py": (
        6_757,
        "7f257a47e3a59a226aa1e46bcba42eb3a2cc18e0059a1e906eb93b8960158bcc",
    ),
    "tests/test_synthesis_k4_encoding.py": (
        9_582,
        "b800ac630dbf16dbd88e0c7cdccf7511dd3c8f8c29f508a73a901237d63595b4",
    ),
}

EXPECTED_MODES = {
    "base": {
        "variables": 18_381,
        "clauses": 49_101,
        "literals": 196_290,
        "bytes": 1_008_612,
        "sha256": "df2bb53af5e3fd63bf51846ae85c5d133d5dca58ff6181924a0077deb363df17",
    },
    "bank": {
        "variables": 18_381,
        "clauses": 114_637,
        "literals": 1_179_330,
        "bytes": 3_990_501,
        "sha256": "33f208024840c17b2068f804d9924c31a969d2c5dccf601533b1958a14cc8c42",
    },
    "full": {
        "variables": 18_381,
        "clauses": 114_742,
        "literals": 1_180_016,
        "bytes": 3_992_947,
        "sha256": "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac",
    },
}

EXPECTED_FAMILIES = {
    "no_k5": (792, 7_920),
    "triple_witness_existence": (220, 1_980),
    "triple_witness_implications": (5_940, 11_880),
    "anchored_k4": (6, 6),
    "connected_g_cuts": (2_047, 67_584),
    "selected_state_domination": (3_960, 19_800),
    "family_nonempty": (1, 495),
    "move_edge_and_successor": (31_680, 63_360),
    "attack_response_disjunctions": (3_960, 19_800),
    "h_k4_to_family": (495, 3_465),
    "complete_anchored_four_color_bank": (65_536, 983_040),
    "outer_signature_order": (105, 686),
}

GENERATOR_SOURCE_PATHS = (
    "src/synthesis_k4/__init__.py",
    "src/synthesis_k4/encoding.py",
    "src/synthesis_k4/generate.py",
    "math/lemmas/order12_k4_synthesis_target.md",
)

PERMANENT_INSTANCE_FILES = {
    "instances/order12_k4_connected_parent/instance.cnf": (
        3_992_947,
        "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac",
    ),
    "instances/order12_k4_connected_parent/manifest.json": (
        4_113,
        "621a0878c117dc8b4d6dbd0ba14c8402a8c24e8339d2f85cb23d61ffd74fbb61",
    ),
    "instances/order12_k4_connected_parent/README.md": (
        1_012,
        "7aaf80399e62a9e9ed227a66c63e8cea5190253228f28a13911c682f93207ead",
    ),
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def pair(first: int, second: int) -> Pair:
    if first == second:
        raise AssertionError("loop in clean-room edge map")
    return (first, second) if first < second else (second, first)


class VariableMap:
    """Independent deterministic allocation of the four semantic families."""

    def __init__(self) -> None:
        self.next_variable = 1
        self.edges = self.allocate(combinations(VERTICES, 2))
        self.triples = tuple(combinations(VERTICES, 3))
        self.states = tuple(combinations(VERTICES, 4))
        self.witnesses = self.allocate(
            (triple, witness)
            for triple in self.triples
            for witness in VERTICES
            if witness not in triple
        )
        self.family = self.allocate(self.states)
        self.moves = self.allocate(
            (state, attacked, guard)
            for state in self.states
            for attacked in VERTICES
            if attacked not in state
            for guard in state
        )
        if self.next_variable - 1 != 18_381:
            raise AssertionError("clean-room variable census changed")

    def allocate(self, keys: Iterable[object]) -> dict[object, int]:
        result: dict[object, int] = {}
        for key in keys:
            if key in result:
                raise AssertionError("duplicate semantic variable key")
            result[key] = self.next_variable
            self.next_variable += 1
        return result

    def edge(self, first: int, second: int) -> int:
        return self.edges[pair(first, second)]


def add_family(
    clauses: list[Clause],
    records: list[dict[str, int | str]],
    name: str,
    payload: Iterable[Sequence[int]],
) -> None:
    first = len(clauses)
    literal_first = sum(map(len, clauses))
    for clause_like in payload:
        clause = tuple(int(literal) for literal in clause_like)
        if not clause:
            raise AssertionError(f"empty generated clause in {name}")
        if 0 in clause:
            raise AssertionError(f"internal zero in {name}")
        if len(set(clause)) != len(clause):
            raise AssertionError(f"duplicate literal in {name}")
        if any(-literal in clause for literal in clause):
            raise AssertionError(f"tautology in {name}")
        clauses.append(clause)
    records.append(
        {
            "name": name,
            "first_clause_zero_based": first,
            "clause_count": len(clauses) - first,
            "literal_count": sum(map(len, clauses)) - literal_first,
        }
    )


def reconstruct() -> tuple[
    VariableMap,
    list[Clause],
    list[Clause],
    list[Clause],
    list[dict[str, int | str]],
]:
    variables = VariableMap()
    base: list[Clause] = []
    records: list[dict[str, int | str]] = []

    add_family(
        base,
        records,
        "no_k5",
        (
            tuple(
                -variables.edges[p]
                for p in combinations(five_set, 2)
            )
            for five_set in combinations(VERTICES, 5)
        ),
    )

    add_family(
        base,
        records,
        "triple_witness_existence",
        (
            tuple(
                variables.witnesses[triple, witness]
                for witness in VERTICES
                if witness not in triple
            )
            for triple in variables.triples
        ),
    )

    def witness_implications() -> Iterable[Clause]:
        for triple in variables.triples:
            for witness in VERTICES:
                if witness in triple:
                    continue
                witness_variable = variables.witnesses[triple, witness]
                for vertex in triple:
                    yield (
                        -witness_variable,
                        variables.edge(vertex, witness),
                    )

    add_family(
        base,
        records,
        "triple_witness_implications",
        witness_implications(),
    )

    add_family(
        base,
        records,
        "anchored_k4",
        ((variables.edges[p],) for p in combinations(ANCHOR, 2)),
    )

    def connected_cuts() -> Iterable[Clause]:
        full = (1 << N) - 1
        for mask in range(1, full):
            if not mask & 1:
                continue
            yield tuple(
                -variables.edge(first, second)
                for first in VERTICES
                if mask >> first & 1
                for second in VERTICES
                if not mask >> second & 1
            )

    add_family(
        base,
        records,
        "connected_g_cuts",
        connected_cuts(),
    )

    def domination_clauses() -> Iterable[Clause]:
        for state in variables.states:
            for outside in VERTICES:
                if outside not in state:
                    yield (
                        -variables.family[state],
                        *( -variables.edge(guard, outside) for guard in state),
                    )

    add_family(
        base,
        records,
        "selected_state_domination",
        domination_clauses(),
    )

    add_family(
        base,
        records,
        "family_nonempty",
        (tuple(variables.family.values()),),
    )

    def move_implications() -> Iterable[Clause]:
        for state in variables.states:
            for attacked in VERTICES:
                if attacked in state:
                    continue
                for guard in state:
                    move = variables.moves[state, attacked, guard]
                    successor = tuple(
                        sorted(
                            vertex for vertex in state if vertex != guard
                        )
                        + [attacked]
                    )
                    successor = tuple(sorted(successor))
                    yield (-move, -variables.edge(guard, attacked))
                    yield (-move, variables.family[successor])

    add_family(
        base,
        records,
        "move_edge_and_successor",
        move_implications(),
    )

    def attack_responses() -> Iterable[Clause]:
        for state in variables.states:
            for attacked in VERTICES:
                if attacked not in state:
                    yield (
                        -variables.family[state],
                        *(
                            variables.moves[state, attacked, guard]
                            for guard in state
                        ),
                    )

    add_family(
        base,
        records,
        "attack_response_disjunctions",
        attack_responses(),
    )

    add_family(
        base,
        records,
        "h_k4_to_family",
        (
            (
                *(
                    -variables.edges[p]
                    for p in combinations(state, 2)
                ),
                variables.family[state],
            )
            for state in variables.states
        ),
    )

    bank: list[Clause] = []
    bank_records: list[dict[str, int | str]] = []
    add_family(
        bank,
        bank_records,
        "complete_anchored_four_color_bank",
        (
            tuple(
                variables.edges[first, second]
                for first, second in combinations(VERTICES, 2)
                if coloring[first] == coloring[second]
            )
            for coloring in (
                ANCHOR + outer_colors
                for outer_colors in product(range(K), repeat=len(OUTER))
            )
        ),
    )
    bank_record = dict(bank_records[0])
    bank_record["first_clause_zero_based"] = len(base)
    records.append(bank_record)

    sorter: list[Clause] = []
    sorter_records: list[dict[str, int | str]] = []

    def sorter_clauses() -> Iterable[Clause]:
        for left, right in zip(OUTER[:-1], OUTER[1:]):
            for first_difference in range(K):
                for prefix in product((0, 1), repeat=first_difference):
                    literals: list[int] = []
                    for coordinate, bit in enumerate(prefix):
                        left_edge = variables.edge(
                            ANCHOR[coordinate], left
                        )
                        right_edge = variables.edge(
                            ANCHOR[coordinate], right
                        )
                        if bit == 0:
                            literals.extend((left_edge, right_edge))
                        else:
                            literals.extend((-left_edge, -right_edge))
                    literals.extend(
                        (
                            -variables.edge(
                                ANCHOR[first_difference], left
                            ),
                            variables.edge(
                                ANCHOR[first_difference], right
                            ),
                        )
                    )
                    yield tuple(literals)

    add_family(
        sorter,
        sorter_records,
        "outer_signature_order",
        sorter_clauses(),
    )
    sorter_record = dict(sorter_records[0])
    sorter_record["first_clause_zero_based"] = len(base) + len(bank)
    records.append(sorter_record)

    observed_families = {
        str(record["name"]): (
            int(record["clause_count"]),
            int(record["literal_count"]),
        )
        for record in records
    }
    if observed_families != EXPECTED_FAMILIES:
        raise AssertionError(
            f"clean-room family census differs: {observed_families}"
        )
    return variables, base, bank, sorter, records


def dimacs(variable_count: int, clauses: Sequence[Clause]) -> bytes:
    lines = [f"p cnf {variable_count} {len(clauses)}"]
    lines.extend(
        " ".join(map(str, clause)) + " 0" for clause in clauses
    )
    return ("\n".join(lines) + "\n").encode("ascii")


def parse_dimacs(payload: bytes) -> tuple[int, list[Clause]]:
    try:
        lines = payload.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise AssertionError("DIMACS is not ASCII") from error
    if not lines:
        raise AssertionError("empty DIMACS")
    header = lines[0].split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise AssertionError("bad DIMACS header")
    variables = int(header[2])
    claimed_clauses = int(header[3])
    clauses: list[Clause] = []
    for line in lines[1:]:
        values = tuple(int(field) for field in line.split())
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise AssertionError("bad DIMACS clause terminator")
        clause = values[:-1]
        if not clause:
            raise AssertionError("unexpected empty input clause")
        if len(set(clause)) != len(clause):
            raise AssertionError("duplicate DIMACS literal")
        if any(-literal in clause for literal in clause):
            raise AssertionError("tautological DIMACS clause")
        if any(not 1 <= abs(literal) <= variables for literal in clause):
            raise AssertionError("DIMACS literal outside header range")
        clauses.append(clause)
    if len(clauses) != claimed_clauses:
        raise AssertionError("DIMACS header clause count mismatch")
    return variables, clauses


def source_set_sha256(
    rows: Sequence[tuple[str, int, str]],
) -> str:
    payload = "".join(
        f"{relative} {size} {digest}\n"
        for relative, size, digest in rows
    ).encode("ascii")
    return sha256_bytes(payload)


def audit_sources(campaign: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for relative, (expected_size, expected_hash) in REVIEWED_FILES.items():
        path = campaign / relative
        actual_size = path.stat().st_size
        actual_hash = sha256_file(path)
        if (actual_size, actual_hash) != (expected_size, expected_hash):
            raise AssertionError(
                f"reviewed source changed: {relative}: "
                f"{actual_size}, {actual_hash}"
            )
        records.append(
            {
                "path": relative,
                "bytes": actual_size,
                "sha256": actual_hash,
            }
        )
    return records


def audit_permanent_instance(
    campaign: Path,
    variables: VariableMap,
    full_clauses: Sequence[Clause],
    records: Sequence[Mapping[str, int | str]],
) -> dict[str, object]:
    bound_files: list[dict[str, object]] = []
    for relative, (expected_size, expected_hash) in (
        PERMANENT_INSTANCE_FILES.items()
    ):
        path = campaign / relative
        actual_size = path.stat().st_size
        actual_hash = sha256_file(path)
        if (actual_size, actual_hash) != (expected_size, expected_hash):
            raise AssertionError(
                f"permanent instance artifact changed: {relative}"
            )
        bound_files.append(
            {
                "path": relative,
                "bytes": actual_size,
                "sha256": actual_hash,
            }
        )

    directory = campaign / "instances/order12_k4_connected_parent"
    instance = (directory / "instance.cnf").read_bytes()
    expected = dimacs(variables.next_variable - 1, full_clauses)
    if instance != expected:
        raise AssertionError(
            "permanent full instance differs from clean-room DIMACS"
        )
    manifest = json.loads((directory / "manifest.json").read_bytes())
    audit_manifest(campaign, "full", instance, manifest, records)
    readme = (directory / "README.md").read_text(encoding="utf-8")
    if (
        "NO_MATHEMATICAL_CLAIM" not in readme
        or EXPECTED_MODES["full"]["sha256"] not in readme
        or "no SAT solver has been run" not in readme
    ):
        raise AssertionError("permanent README claim boundary is incomplete")
    parsed_variables, parsed_clauses = parse_dimacs(instance)
    return {
        "bound_files": bound_files,
        "clean_room_byte_equal": True,
        "manifest_valid": True,
        "claim_boundary_present": True,
        "variables": parsed_variables,
        "clauses": len(parsed_clauses),
        "literals": sum(map(len, parsed_clauses)),
    }


def run_generator(
    campaign: Path,
    mode: str,
    output: Path,
    manifest: Path,
) -> tuple[bytes, bytes, dict[str, object]]:
    command = (
        sys.executable,
        "-m",
        "synthesis_k4.generate",
        "--mode",
        mode,
        "--output",
        str(output),
        "--manifest",
        str(manifest),
    )
    environment = {"PYTHONPATH": str(campaign / "src")}
    completed = subprocess.run(
        command,
        cwd=campaign,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"generator {mode} exited {completed.returncode}: "
            f"{completed.stderr!r}"
        )
    if completed.stderr:
        raise AssertionError(f"generator {mode} wrote stderr")
    result = json.loads(completed.stdout)
    manifest_bytes = manifest.read_bytes()
    manifest_object = json.loads(manifest_bytes)
    if result != manifest_object:
        raise AssertionError(f"generator {mode} stdout/manifest mismatch")
    return output.read_bytes(), manifest_bytes, result


def audit_manifest(
    campaign: Path,
    mode: str,
    payload: bytes,
    result: Mapping[str, object],
    records: Sequence[Mapping[str, int | str]],
) -> None:
    expected = EXPECTED_MODES[mode]
    required = {
        "schema": "gamma-theta-order12-k4-parent-cnf-v1",
        "schema_version": 1,
        "claim_status": "NO_MATHEMATICAL_CLAIM",
        "order": 12,
        "parameter": 4,
        "graph_encoded_by_edges": "H=complement(G)",
        "connected_graphs_only": True,
        "mode": mode,
        "complete_anchored_coloring_bank": mode != "base",
        "outer_signature_breaker": mode == "full",
        "variable_count": expected["variables"],
        "clause_count": expected["clauses"],
        "literal_count": expected["literals"],
        "cnf_size_bytes": expected["bytes"],
        "cnf_sha256": expected["sha256"],
    }
    for key, value in required.items():
        if result.get(key) != value:
            raise AssertionError(
                f"manifest {mode} field {key}: "
                f"{result.get(key)!r} != {value!r}"
            )
    if sha256_bytes(payload) != result["cnf_sha256"]:
        raise AssertionError(f"manifest {mode} does not bind CNF")

    expected_names = [
        "no_k5",
        "triple_witness_existence",
        "triple_witness_implications",
        "anchored_k4",
        "connected_g_cuts",
        "selected_state_domination",
        "family_nonempty",
        "move_edge_and_successor",
        "attack_response_disjunctions",
        "h_k4_to_family",
    ]
    if mode != "base":
        expected_names.append("complete_anchored_four_color_bank")
    if mode == "full":
        expected_names.append("outer_signature_order")
    expected_records = [
        record for record in records if record["name"] in expected_names
    ]
    if result.get("clause_families") != expected_records:
        raise AssertionError(f"manifest {mode} clause-family mismatch")

    source_rows: list[tuple[str, int, str]] = []
    raw_sources = result.get("source_manifest")
    if not isinstance(raw_sources, list):
        raise AssertionError("source manifest is not a list")
    for raw, relative in zip(
        raw_sources, GENERATOR_SOURCE_PATHS, strict=True
    ):
        if not isinstance(raw, dict) or raw.get("path") != relative:
            raise AssertionError("source manifest order/path mismatch")
        size = int(raw["size"])
        digest = str(raw["sha256"])
        path = campaign / relative
        if (size, digest) != (path.stat().st_size, sha256_file(path)):
            raise AssertionError("source manifest byte binding mismatch")
        source_rows.append((relative, size, digest))
    if result.get("source_set_sha256") != source_set_sha256(source_rows):
        raise AssertionError("source-set digest mismatch")


def eval_clause(
    clause: Sequence[int],
    assignment: Mapping[int, bool],
) -> bool:
    return any(
        assignment[abs(literal)] == (literal > 0)
        for literal in clause
    )


def audit_bank(
    variables: VariableMap,
    clauses: Sequence[Clause],
) -> dict[str, object]:
    errors: list[int] = []
    length_histogram: Counter[int] = Counter()
    for index, (outer_colors, clause) in enumerate(
        zip(
            product(range(K), repeat=len(OUTER)),
            clauses,
            strict=True,
        )
    ):
        coloring = ANCHOR + outer_colors
        expected = tuple(
            variables.edges[first, second]
            for first, second in combinations(VERTICES, 2)
            if coloring[first] == coloring[second]
        )
        length_histogram[len(clause)] += 1
        if clause != expected or any(literal <= 0 for literal in clause):
            errors.append(index)
            break

        cross_edges = {
            variables.edges[first, second]
            for first, second in combinations(VERTICES, 2)
            if coloring[first] != coloring[second]
        }
        proper_value = any(literal in cross_edges for literal in clause)
        with_conflict = set(cross_edges)
        with_conflict.add(clause[0])
        conflict_value = any(
            literal in with_conflict for literal in clause
        )
        if proper_value or not conflict_value:
            errors.append(index)
            break
    if errors:
        raise AssertionError(f"color-bank semantic error at {errors[0]}")
    return {
        "rows_checked": len(clauses),
        "literal_count": sum(map(len, clauses)),
        "length_histogram": {
            str(length): length_histogram[length]
            for length in sorted(length_histogram)
        },
        "errors": 0,
    }


def audit_sorter(
    variables: VariableMap,
    clauses: Sequence[Clause],
) -> dict[str, int]:
    if len(clauses) != 105:
        raise AssertionError("wrong sorter clause count")
    tested = 0
    for block_index, (left, right) in enumerate(
        zip(OUTER[:-1], OUTER[1:])
    ):
        block = clauses[15 * block_index : 15 * (block_index + 1)]
        for left_bits in product((False, True), repeat=K):
            for right_bits in product((False, True), repeat=K):
                assignment: dict[int, bool] = {}
                for coordinate in range(K):
                    assignment[
                        variables.edge(ANCHOR[coordinate], left)
                    ] = left_bits[coordinate]
                    assignment[
                        variables.edge(ANCHOR[coordinate], right)
                    ] = right_bits[coordinate]
                accepted = all(
                    eval_clause(clause, assignment) for clause in block
                )
                if accepted != (left_bits <= right_bits):
                    raise AssertionError(
                        f"sorter error block {block_index}: "
                        f"{left_bits}, {right_bits}"
                    )
                tested += 1
    return {
        "blocks": 7,
        "signature_pairs_checked": tested,
        "clauses": len(clauses),
        "literals": sum(map(len, clauses)),
        "errors": 0,
    }


def audit_mutations(
    variables: VariableMap,
    full: Sequence[Clause],
    records: Sequence[Mapping[str, int | str]],
) -> dict[str, bool]:
    starts = {
        str(record["name"]): int(record["first_clause_zero_based"])
        for record in records
    }
    state = (0, 1, 2, 3)
    attacked = 4
    guard = 0
    successor = (1, 2, 3, 4)
    move = variables.moves[state, attacked, guard]

    move_start = starts["move_edge_and_successor"]
    response_start = starts["attack_response_disjunctions"]
    domination_start = starts["selected_state_domination"]
    bank_start = starts["complete_anchored_four_color_bank"]

    exact_edge = (-move, -variables.edge(guard, attacked))
    exact_successor = (-move, variables.family[successor])
    if full[move_start] != exact_edge:
        raise AssertionError("representative move-edge clause moved")
    if full[move_start + 1] != exact_successor:
        raise AssertionError("representative successor clause moved")

    results: dict[str, bool] = {}

    edge_fault = (-move, variables.edge(guard, attacked))
    edge_assignment = {
        move: True,
        variables.edge(guard, attacked): True,
    }
    results["move_complement_sign"] = (
        not eval_clause(exact_edge, edge_assignment)
        and eval_clause(edge_fault, edge_assignment)
        and edge_fault != exact_edge
    )

    wrong_successor = (0, 1, 2, 4)
    wrong_clause = (-move, variables.family[wrong_successor])
    wrong_assignment = {
        move: True,
        variables.family[successor]: False,
        variables.family[wrong_successor]: True,
    }
    results["wrong_successor"] = (
        not eval_clause(exact_successor, wrong_assignment)
        and eval_clause(wrong_clause, wrong_assignment)
        and wrong_clause != exact_successor
    )

    jump = (4, 5, 6, 7)
    jump_clause = (-move, variables.family[jump])
    jump_assignment = {
        move: True,
        variables.family[successor]: False,
        variables.family[jump]: True,
    }
    results["multi_guard_jump"] = (
        len(set(state) ^ set(jump)) > 2
        and not eval_clause(exact_successor, jump_assignment)
        and eval_clause(jump_clause, jump_assignment)
    )

    exact_response = (
        -variables.family[state],
        *(
            variables.moves[state, attacked, candidate]
            for candidate in state
        ),
    )
    if full[response_start] != exact_response:
        raise AssertionError("representative response clause moved")
    foreign_state = (1, 2, 3, 4)
    occupied_move = variables.moves[foreign_state, 0, 1]
    occupied_fault = (
        -variables.family[state],
        occupied_move,
        *(exact_response[2:]),
    )
    results["occupied_attack_witness"] = (
        0 in state and occupied_fault != exact_response
    )

    results["missing_successor_clause"] = (
        len(full[: move_start + 1] + full[move_start + 2 :])
        == len(full) - 1
    )

    exact_domination = (
        -variables.family[state],
        *(
            -variables.edge(candidate, attacked)
            for candidate in state
        ),
    )
    if full[domination_start] != exact_domination:
        raise AssertionError("representative domination clause moved")
    domination_fault = (
        -variables.family[state],
        *(
            variables.edge(candidate, attacked)
            for candidate in state
        ),
    )
    domination_assignment = {
        variables.family[state]: True,
        **{
            variables.edge(candidate, attacked): True
            for candidate in state
        },
    }
    results["domination_complement_sign"] = (
        not eval_clause(exact_domination, domination_assignment)
        and eval_clause(domination_fault, domination_assignment)
    )

    exact_row = full[bank_start]
    row_assignment = {literal: False for literal in exact_row}
    color_fault = tuple(-literal for literal in exact_row)
    results["color_bank_complement_sign"] = (
        all(literal > 0 for literal in exact_row)
        and not eval_clause(exact_row, row_assignment)
        and eval_clause(color_fault, row_assignment)
    )

    if not all(results.values()):
        raise AssertionError(f"a targeted mutation survived: {results}")
    return results


def static_small_order_check() -> dict[str, int]:
    """Exhaust the 512 six-vertex graphs containing a fixed K4."""

    order = 6
    vertices = tuple(range(order))
    all_pairs = tuple(combinations(vertices, 2))
    anchor_edges = set(combinations(range(4), 2))
    free_edges = tuple(p for p in all_pairs if p not in anchor_edges)

    def h_edge(mask: int, first: int, second: int) -> bool:
        edge = pair(first, second)
        if edge in anchor_edges:
            return True
        return bool(mask >> free_edges.index(edge) & 1)

    def static_target(mask: int) -> bool:
        no_k5 = all(
            not all(
                h_edge(mask, first, second)
                for first, second in combinations(group, 2)
            )
            for group in combinations(vertices, 5)
        )
        triple_condition = all(
            any(
                witness not in triple
                and all(
                    h_edge(mask, witness, vertex)
                    for vertex in triple
                )
                for witness in vertices
            )
            for triple in combinations(vertices, 3)
        )
        return no_k5 and triple_condition

    def alpha_g(mask: int) -> int:
        best = 0
        for subset in range(1 << order):
            independent = all(
                not (
                    subset >> first & 1
                    and subset >> second & 1
                    and not h_edge(mask, first, second)
                )
                for first, second in all_pairs
            )
            if independent:
                best = max(best, subset.bit_count())
        return best

    def gamma_g(mask: int) -> int:
        for size in range(1, order + 1):
            for state in combinations(vertices, size):
                state_set = set(state)
                if all(
                    outside in state_set
                    or any(
                        not h_edge(mask, guard, outside)
                        for guard in state
                    )
                    for outside in vertices
                ):
                    return size
        raise AssertionError("finite graph has no dominating set")

    accepted = 0
    errors = 0
    for mask in range(1 << len(free_edges)):
        static = static_target(mask)
        exact = alpha_g(mask) == 4 and gamma_g(mask) == 4
        accepted += int(static)
        errors += int(static != exact)
    if errors:
        raise AssertionError("static theorem failed six-vertex check")
    return {
        "order": order,
        "anchored_graphs": 1 << len(free_edges),
        "static_accepts": accepted,
        "errors": errors,
    }


def eternal_value(order: int, edges: set[Pair]) -> int:
    neighborhoods = [set((vertex,)) for vertex in range(order)]
    for first, second in edges:
        neighborhoods[first].add(second)
        neighborhoods[second].add(first)

    for size in range(1, order + 1):
        alive = {
            frozenset(state)
            for state in combinations(range(order), size)
            if all(
                any(guard in neighborhoods[vertex] for guard in state)
                for vertex in range(order)
            )
        }
        while alive:
            rejected: set[frozenset[int]] = set()
            for state in alive:
                for attacked in range(order):
                    if attacked in state:
                        continue
                    if not any(
                        attacked in neighborhoods[guard]
                        and frozenset(
                            (state - {guard}) | {attacked}
                        )
                        in alive
                        for guard in state
                    ):
                        rejected.add(state)
                        break
            if not rejected:
                return size
            alive.difference_update(rejected)
    raise AssertionError("full occupied state must be eternal")


def cycle_check() -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for order in (5, 7, 9, 11):
        cycle = {
            pair(vertex, (vertex + 1) % order)
            for vertex in range(order)
        }
        complete = set(combinations(range(order), 2))
        result[str(order)] = {
            "cycle": eternal_value(order, cycle),
            "anticycle": eternal_value(order, complete - cycle),
        }
    expected = {
        "5": {"cycle": 3, "anticycle": 3},
        "7": {"cycle": 4, "anticycle": 3},
        "9": {"cycle": 5, "anticycle": 3},
        "11": {"cycle": 6, "anticycle": 3},
    }
    if result != expected:
        raise AssertionError(f"cycle values changed: {result}")
    return result


def run_supplied_tests(campaign: Path) -> dict[str, object]:
    completed = subprocess.run(
        (
            sys.executable,
            "-m",
            "unittest",
            "tests/test_synthesis_k4_encoding.py",
        ),
        cwd=campaign,
        env={},
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    transcript = (completed.stdout + completed.stderr).decode(
        "utf-8", errors="replace"
    )
    if completed.returncode != 0:
        raise AssertionError(f"supplied tests failed:\n{transcript}")
    if "Ran 9 tests" not in transcript or not transcript.rstrip().endswith("OK"):
        raise AssertionError(f"unexpected supplied-test transcript:\n{transcript}")
    return {
        "returncode": completed.returncode,
        "tests": 9,
        "ok": True,
    }


def main() -> int:
    campaign = Path(__file__).resolve().parents[1]
    source_records = audit_sources(campaign)
    variables, base, bank, sorter, records = reconstruct()
    mode_clauses = {
        "base": base,
        "bank": base + bank,
        "full": base + bank + sorter,
    }

    modes: dict[str, dict[str, object]] = {}
    with tempfile.TemporaryDirectory(prefix="gamma-k4-hostile-") as raw:
        temporary = Path(raw)
        for mode in ("base", "bank", "full"):
            expected_clauses = mode_clauses[mode]
            expected_payload = dimacs(
                variables.next_variable - 1, expected_clauses
            )
            expected = EXPECTED_MODES[mode]
            if (
                len(expected_payload) != expected["bytes"]
                or sha256_bytes(expected_payload) != expected["sha256"]
            ):
                raise AssertionError(
                    f"clean-room {mode} bytes differ from frozen expectation"
                )

            output = temporary / f"{mode}.cnf"
            manifest = temporary / f"{mode}.json"
            actual_payload, manifest_bytes, result = run_generator(
                campaign, mode, output, manifest
            )
            audit_manifest(
                campaign, mode, actual_payload, result, records
            )
            parsed_variables, parsed_clauses = parse_dimacs(actual_payload)
            if (
                parsed_variables != variables.next_variable - 1
                or parsed_clauses != expected_clauses
                or actual_payload != expected_payload
            ):
                raise AssertionError(
                    f"emitted {mode} formula differs from clean room"
                )

            repeat_payload, repeat_manifest, repeat_result = run_generator(
                campaign, mode, output, manifest
            )
            if (
                repeat_payload != actual_payload
                or repeat_manifest != manifest_bytes
                or repeat_result != result
            ):
                raise AssertionError(f"{mode} replay is nondeterministic")
            modes[mode] = {
                "variables": parsed_variables,
                "clauses": len(parsed_clauses),
                "literals": sum(map(len, parsed_clauses)),
                "bytes": len(actual_payload),
                "sha256": sha256_bytes(actual_payload),
                "clean_room_byte_equal": True,
                "repeat_byte_equal": True,
                "manifest_valid": True,
            }

    if any(
        name == "synthesis_k4"
        or name.startswith("synthesis_k4.")
        or name == "synthesis_k3"
        or name.startswith("synthesis_k3.")
        for name in sys.modules
    ):
        raise AssertionError("forbidden synthesis module imported into probe")

    full = mode_clauses["full"]
    result = {
        "schema": SCHEMA,
        "schema_version": 1,
        "claim_status": "NO_MATHEMATICAL_CLAIM",
        "verdict": "ACCEPT_EXACT_CONSTRUCTOR_IN_NO_CLAIM_MODE",
        "forbidden_synthesis_modules_imported": False,
        "reviewed_files": source_records,
        "variable_families": {
            "edges": len(variables.edges),
            "triple_witnesses": len(variables.witnesses),
            "family_states": len(variables.family),
            "move_witnesses": len(variables.moves),
            "total": variables.next_variable - 1,
        },
        "all_move_attacks_unoccupied": all(
            attacked not in state and guard in state
            for state, attacked, guard in variables.moves
        ),
        "clause_families": records,
        "modes": modes,
        "permanent_instance": audit_permanent_instance(
            campaign, variables, full, records
        ),
        "color_bank": audit_bank(variables, bank),
        "signature_sorter": audit_sorter(variables, sorter),
        "mutation_kills": audit_mutations(variables, full, records),
        "static_small_order_check": static_small_order_check(),
        "cycle_fixed_point_check": cycle_check(),
        "supplied_tests": run_supplied_tests(campaign),
        "solver_invoked": False,
    }
    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
