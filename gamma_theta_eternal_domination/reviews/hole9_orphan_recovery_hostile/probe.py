#!/usr/bin/env python3
"""Standalone hostile probe for the hole9 attempt-170 recovery package.

This file deliberately uses only the Python standard library.  In particular,
it does not import any project formula builder, CEGAR runner, recovery
verifier, or proof checker.  It independently:

* replays the 170-cut checkpoint chronology and present-artifact bindings;
* rebuilds the exact hole9 CNF from the mathematical encoding;
* strictly parses the retained CNF and original/addition-only proofs;
* strips only canonical deletion instructions; and
* validates every proof addition by fresh watched-literal unit propagation.

The probe is read-only.  Its JSON result is printed to stdout.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import stat
import time
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/synthesis_k3_runs/hole9"
LIVE_ORPHAN = RUN / "attempts/000170.akmx9xl0"
PACKAGE = ROOT / "certificates/synthesis_k3_hole9_orphan_000170_recovery"
PACKAGED_ORPHAN = PACKAGE / "source/orphan-attempt-000170"
INCIDENT = ROOT / "results/logs/synthesis-k3-hole9-batch-004-checker-incident.json"
INCIDENT_ERRATUM = (
    ROOT
    / "results/logs/synthesis-k3-hole9-batch-004-checker-incident-erratum.json"
)
SOUNDNESS_ERRATUM = (
    ROOT / "results/logs/synthesis-k3-hole9-recovery-soundness-erratum.json"
)

N = 12
VARIABLE_COUNT = 6886
BASE_CLAUSE_COUNT = 20030
FULL_CLAUSE_COUNT = 20200
BASE_LITERAL_COUNT = 114619
FULL_LITERAL_COUNT = 117841
CONFIGURATION_SHA256 = (
    "91b1257afd83f8b574229ebf9a1b8f673bd69b93ca7b72286ba90da6ee38fdd8"
)
RUN_MANIFEST_SHA256 = (
    "73869e60bdefc547a91139ab3bfb0673ee8168acada62485089eb371a9d7c15d"
)
CHECKPOINT_SHA256 = (
    "9cc9cdee08fb1fcd7a8772b09cdf9ba9ced802cb0b31be35ab292244e5f286b7"
)
HISTORY_HEAD_SHA256 = (
    "f174e43a531f4a1fbd857ab334d2ec4f7fa3c9b4c2cd0902eb37d887ccc51c99"
)
BASE_CNF_SHA256 = (
    "cf555f359dc887c89f84e35a40ee649e77ef805b2690ec34e72cc4ef75e5d5c7"
)
FULL_CNF_SHA256 = (
    "2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d"
)
ORIGINAL_PROOF_SHA256 = (
    "3cdd686fb2af82e41ff06aa13901d4706618170eb1dc4e74a870831e7fbde8ef"
)
ADDITION_ONLY_SHA256 = (
    "24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab"
)
CUTS_SHA256 = (
    "a3c7bd3591b71c310cfe0bd5711b8e672b75136f3598bb1505ae11cda3c2193b"
)
GENERATOR_SHA256 = (
    "e492e06a0265f176df9a3e76f15b14a17f9873354dc9b6da4020347e1c95dbb4"
)
CERTIFICATE_SHA256 = (
    "1a2d4f7fd3efe0138bb7a7a7f0975d3c60a7ed4d6f994157c5383f18e4b5806c"
)
PACKAGE_TREE_SHA256 = (
    "dab03e8f53ae975cfa0da32433df9c0838f8c279b9f756be59637017d0cd69b2"
)
RUN_TREE_SHA256 = (
    "bd13c4fdc3629ee02fa510eda09bd503234daf4318a33c562e0ab3427d89fd8b"
)
INCIDENT_SHA256 = (
    "8677b4a80a05c982cc365267933521771ea726766f162d9c487584a46aa3890c"
)
INCIDENT_ERRATUM_SHA256 = (
    "6bfb1cc799977d96fe5058b13c1dd08e8c0cbb8b86c3a58a30c3c9a6233ee135"
)
SOUNDNESS_ERRATUM_SHA256 = (
    "f6135a4121cafaca5275d1f1f707e7c82626d61caec94d908704aaec92400e90"
)
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()

ORPHAN_BINDINGS = {
    "checker.stderr": (0, EMPTY_SHA256),
    "checker.stdout": (
        113,
        "00713579066b184feaa75783404de748da3055bc55d2871c796123a657779590",
    ),
    "cuts.json": (4422, CUTS_SHA256),
    "generator.json": (2536, GENERATOR_SHA256),
    "instance.cnf": (530053, FULL_CNF_SHA256),
    "proof-solver.stderr": (0, EMPTY_SHA256),
    "proof-solver.stdout": (0, EMPTY_SHA256),
    "proof.drat": (512071, ORIGINAL_PROOF_SHA256),
    "proof.result": (
        16,
        "bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162",
    ),
    "solver.result": (
        16,
        "bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162",
    ),
    "solver.stderr": (0, EMPTY_SHA256),
    "solver.stdout": (0, EMPTY_SHA256),
}

RUNTIME_SOURCES = (
    (
        "src/synthesis_k3/__init__.py",
        "fbc5ca4211eb97b498e0eecd692333596bba409c26629623f8d547a48a379e86",
    ),
    (
        "src/synthesis_k3/encoding.py",
        "fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6",
    ),
    (
        "src/synthesis_k3/coloring.py",
        "9791599aaca6b9f7ec5e6fed8cfce41a5c5bec825a350e5e493a0d1aa06d3713",
    ),
    (
        "src/synthesis_k3/generate.py",
        "456029e08a199e3cc8d4aa6070e3209d6884901fc6c3db8486b80862614430e1",
    ),
    (
        "src/synthesis_k3/cegar.py",
        "411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c",
    ),
    (
        "math/synthesis_k3_cegar_design.md",
        "57d82b9dabdc9c8f66950a3f9c483f3cb58e35a11e243a8880c173b5724a09b8",
    ),
    (
        "math/synthesis_k3_cegar_protocol.md",
        "c51db6d865557f4dcc3147772dbaa1c86d3c6c6d3544ab0090f0f89267a9de31",
    ),
)
GENERATOR_SOURCES = tuple(
    row
    for row in RUNTIME_SOURCES
    if row[0]
    in {
        "src/synthesis_k3/__init__.py",
        "src/synthesis_k3/encoding.py",
        "src/synthesis_k3/generate.py",
        "math/synthesis_k3_cegar_design.md",
    }
)

INTEGER = re.compile(r"-?[1-9][0-9]*\Z")
ATTEMPT_NAME = re.compile(r"([0-9]{6})\.[A-Za-z0-9_]+\Z")


class AuditFailure(RuntimeError):
    """A hostile-audit condition failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def reject_constant(value: str) -> object:
    raise AuditFailure(f"non-finite JSON value {value!r}")


def strict_json(payload: bytes, role: str) -> object:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AuditFailure(f"{role}: non-UTF-8 JSON") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise AuditFailure(f"{role}: malformed JSON") from error


def canonical_json(value: object, *, pretty: bool = False) -> bytes:
    arguments: dict[str, object] = {
        "allow_nan": False,
        "sort_keys": True,
    }
    if pretty:
        arguments["indent"] = 2
    else:
        arguments["separators"] = (",", ":")
    return (json.dumps(value, **arguments) + "\n").encode("utf-8")


def source_set_hash(records: Sequence[tuple[str, str]]) -> str:
    return sha256_bytes(
        "".join(f"{name} {digest}\n" for name, digest in records).encode("ascii")
    )


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def regular_single_link(path: Path, role: str) -> Path:
    require(not path.is_symlink(), f"{role}: symlink")
    try:
        info = path.stat()
    except FileNotFoundError as error:
        raise AuditFailure(f"{role}: missing {path}") from error
    require(
        stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
        f"{role}: not a single-link regular file",
    )
    return path.resolve(strict=True)


def exact_binding(path: Path, expected: tuple[int, str], role: str) -> bytes:
    resolved = regular_single_link(path, role)
    payload = resolved.read_bytes()
    size, digest = expected
    require(len(payload) == size, f"{role}: size mismatch")
    require(sha256_bytes(payload) == digest, f"{role}: SHA-256 mismatch")
    return payload


def tree_digest(directory: Path) -> dict[str, object]:
    root = directory.resolve(strict=True)
    digest = hashlib.sha256()
    count = 0
    total = 0
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        information = path.lstat()
        if stat.S_ISDIR(information.st_mode):
            continue
        require(
            stat.S_ISREG(information.st_mode) and information.st_nlink == 1,
            f"tree entry is not a single-link regular file: {path}",
        )
        relative = path.relative_to(root).as_posix().encode("utf-8")
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
        count += 1
        total += len(payload)
    return {
        "sha256": digest.hexdigest(),
        "file_count": count,
        "total_file_bytes": total,
    }


def pair(first: int, second: int) -> tuple[int, int]:
    require(first != second, "loop in edge lookup")
    return (first, second) if first < second else (second, first)


def canonical_coloring(raw: object) -> tuple[int, ...]:
    require(
        isinstance(raw, list)
        and len(raw) == N
        and all(type(color) is int and color in (0, 1, 2) for color in raw),
        "malformed coloring",
    )
    relabel: dict[int, int] = {}
    normalized: list[int] = []
    for color in raw:
        if color not in relabel:
            relabel[color] = len(relabel)
        normalized.append(relabel[color])
    result = tuple(normalized)
    require(tuple(raw) == result, "coloring is not first-use canonical")
    return result


def build_formula(
    colorings: Sequence[Sequence[int]],
) -> tuple[int, tuple[tuple[int, ...], ...], dict[tuple[int, int], int]]:
    """Rebuild the encoding directly from the published mathematical clauses."""

    variable_count = 0
    clauses: list[tuple[int, ...]] = []

    def new_variable() -> int:
        nonlocal variable_count
        variable_count += 1
        return variable_count

    def add_clause(values: Iterable[int]) -> None:
        clause = tuple(int(value) for value in values)
        require(all(value != 0 for value in clause), "zero inside built clause")
        require(
            all(abs(value) <= variable_count for value in clause),
            "built clause uses unallocated variable",
        )
        require(len(set(clause)) == len(clause), "duplicate in built clause")
        require(
            not any(-value in clause for value in clause),
            "tautological built clause",
        )
        clauses.append(clause)

    vertices = tuple(range(N))
    triples = tuple(combinations(vertices, 3))
    edge_variables = {
        edge_pair: new_variable() for edge_pair in combinations(vertices, 2)
    }
    witness_variables = {
        (first, second, witness): new_variable()
        for first, second in combinations(vertices, 2)
        for witness in vertices
        if witness not in (first, second)
    }
    family_variables = {
        triple: new_variable()
        for triple in triples
    }
    move_variables = {
        (triple, attacked, guard): new_variable()
        for triple in triples
        for attacked in vertices
        if attacked not in triple
        for guard in triple
    }

    def edge(first: int, second: int) -> int:
        return edge_variables[pair(first, second)]

    # No four vertices form an H-clique.
    for four_set in combinations(vertices, 4):
        add_clause(
            -edge(first, second)
            for first, second in combinations(four_set, 2)
        )

    # Every pair has a certified external common H-neighbor.
    for first, second in combinations(vertices, 2):
        witnesses = tuple(
            vertex for vertex in vertices if vertex not in (first, second)
        )
        add_clause(
            witness_variables[(first, second, witness)]
            for witness in witnesses
        )
        for witness in witnesses:
            variable = witness_variables[(first, second, witness)]
            add_clause((-variable, edge(first, witness)))
            add_clause((-variable, edge(second, witness)))

    # Induced C9, no external hub, and fixed common neighbor 9 for rim edge 01.
    rim = tuple(range(9))
    rim_edges = {
        pair(vertex, (vertex + 1) % 9)
        for vertex in rim
    }
    for first, second in combinations(rim, 2):
        variable = edge(first, second)
        add_clause((variable if (first, second) in rim_edges else -variable,))
    for outside in range(9, N):
        add_clause(-edge(outside, rim_vertex) for rim_vertex in rim)
    add_clause((edge(0, 9),))
    add_clause((edge(1, 9),))

    # Every proper cut represented by the side containing 0 has a G-edge.
    full_mask = (1 << N) - 1
    for mask in range(1, full_mask):
        if not mask & 1:
            continue
        add_clause(
            -edge(first, second)
            for first in vertices
            if mask >> first & 1
            for second in vertices
            if not (mask >> second & 1)
        )

    # Every selected guard-family triple dominates in G.
    for triple in triples:
        family = family_variables[triple]
        for outside in vertices:
            if outside in triple:
                continue
            add_clause(
                (
                    -family,
                    -edge(outside, triple[0]),
                    -edge(outside, triple[1]),
                    -edge(outside, triple[2]),
                )
            )

    # Nonempty family and a legal one-guard response to every outside attack.
    add_clause(family_variables.values())
    for triple in triples:
        family = family_variables[triple]
        for attacked in vertices:
            if attacked in triple:
                continue
            responses: list[int] = []
            for guard in triple:
                move = move_variables[(triple, attacked, guard)]
                successor = tuple(
                    sorted((set(triple) - {guard}) | {attacked})
                )
                responses.append(move)
                add_clause((-move, -edge(guard, attacked)))
                add_clause((-move, family_variables[successor]))
            add_clause((-family, *responses))

    # Every H-triangle is selected.
    for triple in triples:
        add_clause(
            (
                -edge(triple[0], triple[1]),
                -edge(triple[0], triple[2]),
                -edge(triple[1], triple[2]),
                family_variables[triple],
            )
        )

    seen: set[tuple[int, ...]] = set()
    for raw in colorings:
        coloring = canonical_coloring(list(raw))
        require(coloring not in seen, "duplicate coloring partition")
        seen.add(coloring)
        add_clause(
            edge(first, second)
            for first, second in combinations(vertices, 2)
            if coloring[first] == coloring[second]
        )

    return variable_count, tuple(clauses), edge_variables


def clause_line(clause: Sequence[int]) -> bytes:
    if clause:
        return (" ".join(map(str, clause)) + " 0\n").encode("ascii")
    return b"0\n"


def dimacs_bytes(variable_count: int, clauses: Sequence[Sequence[int]]) -> bytes:
    header = f"p cnf {variable_count} {len(clauses)}\n".encode("ascii")
    return header + b"".join(clause_line(clause) for clause in clauses)


def parse_cnf(payload: bytes) -> tuple[int, tuple[tuple[int, ...], ...]]:
    require(payload != b"" and payload.endswith(b"\n"), "CNF framing")
    require(b"\r" not in payload and b"\x00" not in payload, "CNF control byte")
    try:
        payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditFailure("CNF is not ASCII") from error
    lines = payload.splitlines(keepends=True)
    require(bool(lines), "CNF has no header")
    header = re.fullmatch(rb"p cnf ([1-9][0-9]*) ([1-9][0-9]*)\n", lines[0])
    require(header is not None, "noncanonical CNF header")
    variable_count = int(header.group(1))
    declared_clause_count = int(header.group(2))
    clauses: list[tuple[int, ...]] = []
    for number, line in enumerate(lines[1:], 2):
        require(line.endswith(b"\n"), f"CNF line {number}: no LF")
        try:
            text = line[:-1].decode("ascii")
        except UnicodeDecodeError as error:
            raise AuditFailure(f"CNF line {number}: non-ASCII") from error
        tokens = text.split(" ")
        require(
            len(tokens) >= 2 and tokens[-1] == "0" and "" not in tokens,
            f"CNF line {number}: malformed terminator/spacing",
        )
        require(
            all(INTEGER.fullmatch(token) for token in tokens[:-1]),
            f"CNF line {number}: malformed literal",
        )
        clause = tuple(int(token) for token in tokens[:-1])
        require(bool(clause), f"CNF line {number}: empty source clause")
        require(
            all(abs(literal) <= variable_count for literal in clause),
            f"CNF line {number}: variable out of range",
        )
        require(
            len(set(clause)) == len(clause),
            f"CNF line {number}: duplicate literal",
        )
        require(
            not any(-literal in clause for literal in clause),
            f"CNF line {number}: tautology",
        )
        clauses.append(clause)
    require(
        len(clauses) == declared_clause_count,
        "CNF declared/actual clause counts differ",
    )
    return variable_count, tuple(clauses)


def parse_clause_instruction(
    line: bytes,
    *,
    deletion: bool,
    number: int,
) -> tuple[int, ...]:
    prefix = b"d " if deletion else b""
    require(
        line.startswith(prefix) and line.endswith(b"\n") and b"\r" not in line,
        f"proof line {number}: framing",
    )
    body = line[len(prefix):-1]
    try:
        text = body.decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditFailure(f"proof line {number}: non-ASCII") from error
    tokens = text.split(" ")
    require(
        bool(tokens) and tokens[-1] == "0" and "" not in tokens,
        f"proof line {number}: malformed zero termination/spacing",
    )
    require(
        all(INTEGER.fullmatch(token) for token in tokens[:-1]),
        f"proof line {number}: malformed literal token",
    )
    clause = tuple(int(token) for token in tokens[:-1])
    require(
        all(abs(literal) <= 2_147_483_647 for literal in clause),
        f"proof line {number}: integer overflow",
    )
    require(
        len(set(clause)) == len(clause),
        f"proof line {number}: repeated literal",
    )
    require(
        not any(-literal in clause for literal in clause),
        f"proof line {number}: tautology",
    )
    require(not deletion or bool(clause), f"proof line {number}: empty deletion")
    canonical = prefix + clause_line(clause)
    require(line == canonical, f"proof line {number}: noncanonical bytes")
    return clause


def parse_proof(payload: bytes) -> dict[str, object]:
    require(payload != b"" and payload.endswith(b"\n"), "proof framing")
    require(b"\r" not in payload and b"\x00" not in payload, "proof control byte")
    try:
        payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditFailure("proof is not ASCII") from error
    lines = payload.splitlines(keepends=True)
    additions: list[tuple[int, ...]] = []
    addition_lines: list[int] = []
    stripped: list[bytes] = []
    deletion_count = 0
    comment_count = 0
    empty_count = 0
    maximum_variable = 0
    maximum_clause_size = 0
    maximum_addition_clause_size = 0
    for number, line in enumerate(lines, 1):
        require(line not in (b"", b"\n"), f"blank proof line {number}")
        if line.startswith(b"c "):
            require(
                all(byte == 9 or 32 <= byte <= 126 for byte in line[:-1]),
                f"proof comment {number}: control byte",
            )
            comment_count += 1
            stripped.append(line)
            continue
        deletion = line.startswith(b"d ")
        clause = parse_clause_instruction(
            line,
            deletion=deletion,
            number=number,
        )
        maximum_clause_size = max(maximum_clause_size, len(clause))
        maximum_variable = max(
            maximum_variable,
            max((abs(literal) for literal in clause), default=0),
        )
        if deletion:
            deletion_count += 1
            continue
        additions.append(clause)
        addition_lines.append(number)
        stripped.append(line)
        maximum_addition_clause_size = max(
            maximum_addition_clause_size,
            len(clause),
        )
        if not clause:
            empty_count += 1
            require(
                number == len(lines),
                f"proof line {number}: nonfinal empty addition",
            )
    require(
        empty_count == 1 and additions and additions[-1] == (),
        "proof does not end in exactly one empty addition",
    )
    return {
        "line_count": len(lines),
        "addition_count": len(additions),
        "deletion_count": deletion_count,
        "comment_count": comment_count,
        "empty_count": empty_count,
        "maximum_variable": maximum_variable,
        "maximum_clause_size": maximum_clause_size,
        "maximum_addition_clause_size": maximum_addition_clause_size,
        "additions": tuple(additions),
        "addition_lines": tuple(addition_lines),
        "stripped": b"".join(stripped),
    }


class RUPChecker:
    """Fresh forward RUP checker with mutable two-watched-literal state."""

    def __init__(
        self,
        variable_count: int,
        clauses: Sequence[Sequence[int]],
    ) -> None:
        self.variable_count = variable_count
        self.clauses: list[tuple[int, ...]] = []
        self.watch_positions: list[tuple[int, int] | None] = []
        self.watch_lists: dict[int, list[int]] = defaultdict(list)
        self.units: list[int] = []
        self.has_empty_clause = False
        self.assignment = [0] * (variable_count + 1)
        self.check_count = 0
        self.clause_visits = 0
        self.enqueues = 0
        self.maximum_trail = 0
        for clause in clauses:
            self.add_clause(tuple(clause))

    def add_clause(self, clause: tuple[int, ...]) -> None:
        require(
            all(0 < abs(literal) <= self.variable_count for literal in clause),
            "RUP clause variable outside formula range",
        )
        require(len(set(clause)) == len(clause), "RUP clause duplicate")
        require(
            not any(-literal in clause for literal in clause),
            "RUP tautology",
        )
        clause_id = len(self.clauses)
        self.clauses.append(clause)
        if not clause:
            self.watch_positions.append(None)
            self.has_empty_clause = True
        elif len(clause) == 1:
            self.watch_positions.append(None)
            self.units.append(clause[0])
        else:
            self.watch_positions.append((0, 1))
            self.watch_lists[clause[0]].append(clause_id)
            self.watch_lists[clause[1]].append(clause_id)

    def _literal_value(self, literal: int) -> int:
        assigned = self.assignment[abs(literal)]
        return assigned if literal > 0 else -assigned

    def check_rup(self, candidate: tuple[int, ...]) -> bool:
        require(not self.has_empty_clause, "proof continues after empty clause")
        require(
            all(0 < abs(literal) <= self.variable_count for literal in candidate),
            "candidate variable outside formula range",
        )
        self.check_count += 1
        trail: list[int] = []

        def enqueue(literal: int) -> bool:
            variable = abs(literal)
            desired = 1 if literal > 0 else -1
            current = self.assignment[variable]
            if current == 0:
                self.assignment[variable] = desired
                trail.append(literal)
                self.enqueues += 1
                return True
            return current == desired

        conflict = False
        try:
            for literal in candidate:
                if not enqueue(-literal):
                    conflict = True
                    break
            if not conflict:
                for literal in self.units:
                    if not enqueue(literal):
                        conflict = True
                        break
            head = 0
            while not conflict and head < len(trail):
                true_literal = trail[head]
                head += 1
                false_literal = -true_literal
                watched = self.watch_lists.get(false_literal)
                if not watched:
                    continue
                position = 0
                while position < len(watched):
                    clause_id = watched[position]
                    clause = self.clauses[clause_id]
                    watch_pair = self.watch_positions[clause_id]
                    require(watch_pair is not None, "invalid watcher state")
                    first_position, second_position = watch_pair
                    if clause[first_position] == false_literal:
                        false_slot = 0
                        other_position = second_position
                    elif clause[second_position] == false_literal:
                        false_slot = 1
                        other_position = first_position
                    else:
                        raise AuditFailure("stale watched-literal entry")
                    self.clause_visits += 1
                    other_literal = clause[other_position]
                    if self._literal_value(other_literal) == 1:
                        position += 1
                        continue

                    replacement_position: int | None = None
                    for candidate_position, candidate_literal in enumerate(clause):
                        if candidate_position in (first_position, second_position):
                            continue
                        if self._literal_value(candidate_literal) != -1:
                            replacement_position = candidate_position
                            break
                    if replacement_position is not None:
                        replacement_literal = clause[replacement_position]
                        if false_slot == 0:
                            self.watch_positions[clause_id] = (
                                replacement_position,
                                second_position,
                            )
                        else:
                            self.watch_positions[clause_id] = (
                                first_position,
                                replacement_position,
                            )
                        watched[position] = watched[-1]
                        watched.pop()
                        self.watch_lists[replacement_literal].append(clause_id)
                        continue

                    other_value = self._literal_value(other_literal)
                    if other_value == -1 or not enqueue(other_literal):
                        conflict = True
                        break
                    position += 1
            self.maximum_trail = max(self.maximum_trail, len(trail))
            return conflict
        finally:
            for literal in trail:
                self.assignment[abs(literal)] = 0


def cut_prefix_hashes(cuts: Sequence[dict[str, object]]) -> tuple[str, ...]:
    hashes: list[str] = []
    rows: list[object] = []
    hashes.append(sha256_bytes(canonical_json(rows)))
    for cut in cuts:
        rows.append(cut["coloring"])
        hashes.append(sha256_bytes(canonical_json(rows)))
    return tuple(hashes)


def history_initial() -> str:
    return sha256_bytes(
        canonical_json(
            {
                "domain": "gamma-theta-k3-cegar-history-v1",
                "configuration_sha256": CONFIGURATION_SHA256,
                "run_manifest_sha256": RUN_MANIFEST_SHA256,
            }
        )
    )


def history_step(
    before: str,
    reference: dict[str, object],
    cut: dict[str, object],
) -> str:
    return sha256_bytes(
        canonical_json(
            {
                "domain": "gamma-theta-k3-cegar-history-v1",
                "before_sha256": before,
                "attempt_reference": reference,
                "cut_record": cut,
                "status": "running",
                "terminal": None,
            }
        )
    )


def checkpoint_digest(
    *,
    attempt_count: int,
    cut_count: int,
    cuts_payload_sha256: str,
    history_chain_sha256: str,
) -> str:
    return sha256_bytes(
        canonical_json(
            {
                "domain": "gamma-theta-k3-cegar-checkpoint-state-v1",
                "schema": "gamma-theta-k3-cegar-checkpoint-v2",
                "schema_version": 2,
                "configuration_sha256": CONFIGURATION_SHA256,
                "run_manifest_path": str((RUN / "run_manifest.json").resolve()),
                "run_manifest_sha256": RUN_MANIFEST_SHA256,
                "status": "running",
                "attempt_count": attempt_count,
                "cut_count": cut_count,
                "cuts_payload_sha256": cuts_payload_sha256,
                "history_chain_sha256": history_chain_sha256,
                "terminal": None,
            }
        )
    )


def validate_recorded_file(
    record: object,
    *,
    role: str,
) -> Path:
    require(
        isinstance(record, dict)
        and set(record) == {"path", "sha256", "size_bytes"},
        f"{role}: malformed binding",
    )
    raw_path = record["path"]
    require(type(raw_path) is str, f"{role}: path is not text")
    path = Path(raw_path)
    require(path.is_absolute(), f"{role}: path is not absolute")
    resolved = regular_single_link(path, role)
    require(within(resolved, RUN.resolve()), f"{role}: path escapes run")
    require(
        type(record["size_bytes"]) is int
        and record["size_bytes"] == resolved.stat().st_size,
        f"{role}: recorded size mismatch",
    )
    require(
        type(record["sha256"]) is str
        and record["sha256"] == sha256_file(resolved),
        f"{role}: recorded hash mismatch",
    )
    return resolved


def validate_run_manifest(payload: bytes) -> dict[str, object]:
    require(sha256_bytes(payload) == RUN_MANIFEST_SHA256, "run manifest hash")
    manifest = strict_json(payload, "run manifest")
    require(isinstance(manifest, dict), "run manifest is not an object")
    require(
        manifest.get("schema") == "gamma-theta-k3-cegar-run-v2"
        and manifest.get("schema_version") == 2,
        "run manifest schema",
    )
    configuration = manifest.get("configuration")
    require(isinstance(configuration, dict), "run configuration")
    require(
        sha256_bytes(canonical_json(configuration))
        == manifest.get("configuration_sha256")
        == CONFIGURATION_SHA256,
        "configuration digest",
    )
    require(
        configuration.get("template") == "hole9"
        and Path(str(configuration.get("run_directory"))).resolve()
        == RUN.resolve(),
        "run manifest target",
    )
    expected_sources = [[path, digest] for path, digest in RUNTIME_SOURCES]
    require(
        configuration.get("runtime_source_manifest") == expected_sources,
        "runtime source manifest",
    )
    for relative, digest in RUNTIME_SOURCES:
        require(sha256_file(ROOT / relative) == digest, f"runtime source {relative}")
    require(
        configuration.get("runtime_source_set_sha256")
        == source_set_hash(RUNTIME_SOURCES)
        == "8c4e811bc4250c3e2b0b7edeb8afd07f7509ebda3cbae3db1b3ca82c07b35299",
        "runtime source-set digest",
    )
    tools = (
        (
            "cadical",
            "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6",
            "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e",
        ),
        (
            "drat_trim",
            "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
            "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108",
        ),
    )
    for role, binary_digest, archive_digest in tools:
        binding = configuration.get(role)
        require(isinstance(binding, dict), f"{role}: binding")
        require(
            binding.get("sha256") == binary_digest
            and sha256_file(Path(str(binding.get("path")))) == binary_digest,
            f"{role}: binary digest",
        )
        require(
            binding.get("source_archive_sha256") == archive_digest
            and sha256_file(Path(str(binding.get("source_archive_path"))))
            == archive_digest,
            f"{role}: archive digest",
        )
    return manifest


def validate_checkpoint_and_attempts(
    checkpoint_payload: bytes,
    base_clauses: tuple[tuple[int, ...], ...],
    edge_variables: dict[tuple[int, int], int],
) -> dict[str, object]:
    require(sha256_bytes(checkpoint_payload) == CHECKPOINT_SHA256, "checkpoint hash")
    checkpoint = strict_json(checkpoint_payload, "checkpoint")
    require(isinstance(checkpoint, dict), "checkpoint is not an object")
    require(
        checkpoint.get("schema") == "gamma-theta-k3-cegar-checkpoint-v2"
        and checkpoint.get("schema_version") == 2
        and checkpoint.get("configuration_sha256") == CONFIGURATION_SHA256
        and checkpoint.get("run_manifest_sha256") == RUN_MANIFEST_SHA256
        and checkpoint.get("run_manifest_path")
        == str((RUN / "run_manifest.json").resolve())
        and checkpoint.get("status") == "running"
        and checkpoint.get("terminal") is None,
        "checkpoint provenance/status",
    )
    attempts = checkpoint.get("attempts")
    cuts = checkpoint.get("cuts")
    require(
        isinstance(attempts, list)
        and isinstance(cuts, list)
        and len(attempts) == len(cuts) == 170,
        "checkpoint is not a 170-attempt/170-cut prefix",
    )
    require(
        all(isinstance(item, dict) for item in attempts)
        and all(isinstance(item, dict) for item in cuts),
        "checkpoint ledger record type",
    )
    attempt_records = [dict(item) for item in attempts]
    cut_records = [dict(item) for item in cuts]
    prefixes = cut_prefix_hashes(cut_records)
    require(
        prefixes[-1] == checkpoint.get("cuts_payload_sha256") == CUTS_SHA256,
        "cut payload digest",
    )

    base_body = b"".join(clause_line(clause) for clause in base_clauses)
    cut_lines: list[bytes] = []
    colorings: list[tuple[int, ...]] = []
    seen_colorings: set[tuple[int, ...]] = set()
    manifests: list[dict[str, object]] = []
    artifact_checks = 0

    # First validate every cut and source-attempt reference.
    for index, (reference, cut) in enumerate(zip(attempt_records, cut_records)):
        require(
            set(reference)
            == {
                "index",
                "manifest_path",
                "manifest_sha256",
                "outcome",
                "checkpoint_before_sha256",
                "history_chain_before_sha256",
            },
            f"attempt reference {index}: schema",
        )
        require(
            reference["index"] == index
            and reference["outcome"] == "coloring_cut_committed",
            f"attempt reference {index}: index/outcome",
        )
        manifest_path = Path(str(reference["manifest_path"]))
        require(
            manifest_path.is_absolute()
            and manifest_path.name == "attempt.json"
            and within(manifest_path.resolve(), RUN.resolve()),
            f"attempt reference {index}: path",
        )
        match = ATTEMPT_NAME.fullmatch(manifest_path.parent.name)
        require(
            match is not None and int(match.group(1)) == index,
            f"attempt reference {index}: directory index",
        )
        manifest_bytes = regular_single_link(
            manifest_path,
            f"attempt {index} manifest",
        ).read_bytes()
        require(
            sha256_bytes(manifest_bytes) == reference["manifest_sha256"],
            f"attempt {index}: manifest digest",
        )
        manifest = strict_json(manifest_bytes, f"attempt {index} manifest")
        require(isinstance(manifest, dict), f"attempt {index}: manifest type")
        manifest = dict(manifest)
        manifests.append(manifest)
        require(
            manifest.get("schema") == "gamma-theta-k3-cegar-attempt-v2"
            and manifest.get("schema_version") == 2
            and manifest.get("attempt_index") == index
            and manifest.get("outcome") == "coloring_cut_committed"
            and manifest.get("configuration_sha256") == CONFIGURATION_SHA256
            and manifest.get("run_manifest_sha256") == RUN_MANIFEST_SHA256
            and manifest.get("checkpoint_before_sha256")
            == reference["checkpoint_before_sha256"]
            and manifest.get("history_chain_before_sha256")
            == reference["history_chain_before_sha256"]
            and manifest.get("cut_count_before") == index,
            f"attempt {index}: provenance",
        )
        require(
            set(cut)
            == {
                "index",
                "coloring",
                "coloring_sha256",
                "clause",
                "clause_sha256",
                "source_attempt_index",
                "source_attempt_manifest_path",
                "source_attempt_manifest_sha256",
            },
            f"cut {index}: schema",
        )
        require(
            cut["index"] == index
            and cut["source_attempt_index"] == index
            and cut["source_attempt_manifest_path"] == reference["manifest_path"]
            and cut["source_attempt_manifest_sha256"]
            == reference["manifest_sha256"],
            f"cut {index}: source binding",
        )
        coloring = canonical_coloring(cut["coloring"])
        require(coloring not in seen_colorings, f"cut {index}: duplicate coloring")
        seen_colorings.add(coloring)
        colorings.append(coloring)
        clause = tuple(
            edge_variables[(first, second)]
            for first, second in combinations(range(N), 2)
            if coloring[first] == coloring[second]
        )
        require(
            isinstance(cut["clause"], list)
            and tuple(cut["clause"]) == clause,
            f"cut {index}: wrong same-color clause",
        )
        require(
            cut["coloring_sha256"]
            == sha256_bytes(canonical_json(list(coloring))),
            f"cut {index}: coloring hash",
        )
        cut_clause_bytes = (
            " ".join(map(str, clause)) + "\n"
        ).encode("ascii")
        require(
            cut["clause_sha256"] == sha256_bytes(cut_clause_bytes),
            f"cut {index}: clause hash",
        )
        cut_lines.append(clause_line(clause))
        committed = {
            key: cut[key]
            for key in (
                "index",
                "coloring",
                "coloring_sha256",
                "clause",
                "clause_sha256",
            )
        }
        require(
            manifest.get("committed_cut") == committed,
            f"attempt {index}: committed cut mismatch",
        )

    # Then validate every present, compressed, and reconstructible artifact.
    cut_body = b""
    for index, manifest in enumerate(manifests):
        direct = manifest.get("artifacts")
        require(isinstance(direct, dict), f"attempt {index}: direct artifacts")
        direct_paths: dict[str, Path] = {}
        for role, record in direct.items():
            require(type(role) is str, f"attempt {index}: direct role")
            direct_paths[role] = validate_recorded_file(
                record,
                role=f"attempt {index} {role}",
            )
            artifact_checks += 1

        compressed = manifest.get("compressed_artifacts")
        require(
            isinstance(compressed, dict),
            f"attempt {index}: compressed artifact ledger",
        )
        for role, record in compressed.items():
            require(
                type(role) is str
                and isinstance(record, dict)
                and set(record)
                == {
                    "format",
                    "raw_path",
                    "raw_sha256",
                    "raw_size_bytes",
                    "gzip_path",
                    "gzip_sha256",
                    "gzip_size_bytes",
                },
                f"attempt {index}: compressed {role} schema",
            )
            require(record["format"] == "gzip", "compression format")
            gzip_path = Path(str(record["gzip_path"]))
            resolved = regular_single_link(
                gzip_path,
                f"attempt {index} compressed {role}",
            )
            require(within(resolved, RUN.resolve()), "compressed path escape")
            compressed_payload = resolved.read_bytes()
            require(
                len(compressed_payload) == record["gzip_size_bytes"]
                and sha256_bytes(compressed_payload) == record["gzip_sha256"],
                f"attempt {index}: compressed {role} binding",
            )
            try:
                raw_payload = gzip.decompress(compressed_payload)
            except (gzip.BadGzipFile, EOFError) as error:
                raise AuditFailure(
                    f"attempt {index}: malformed compressed {role}"
                ) from error
            require(
                len(raw_payload) == record["raw_size_bytes"]
                and sha256_bytes(raw_payload) == record["raw_sha256"],
                f"attempt {index}: raw {role} binding",
            )
            raw_path = Path(str(record["raw_path"]))
            require(
                raw_path.is_absolute()
                and within(raw_path, RUN.resolve())
                and not raw_path.exists(),
                f"attempt {index}: raw {role} path",
            )
            artifact_checks += 2

        reconstructed = manifest.get("reconstructible_artifacts")
        require(
            isinstance(reconstructed, dict)
            and set(reconstructed) == {"cnf", "cuts_input"},
            f"attempt {index}: reconstruction ledger",
        )
        expected_prefix_hash = prefixes[index]
        prefix_rows = [list(coloring) for coloring in colorings[:index]]
        expected_cuts = canonical_json(prefix_rows)
        expected_cnf = (
            f"p cnf {VARIABLE_COUNT} {BASE_CLAUSE_COUNT + index}\n".encode(
                "ascii"
            )
            + base_body
            + cut_body
        )
        expected_payloads = {
            "cnf": expected_cnf,
            "cuts_input": expected_cuts,
        }
        for role, record in reconstructed.items():
            require(
                isinstance(record, dict)
                and record.get("cut_count") == index
                and record.get("cut_prefix_sha256") == expected_prefix_hash,
                f"attempt {index}: {role} prefix binding",
            )
            raw_path = Path(str(record.get("raw_path")))
            require(
                raw_path.is_absolute()
                and within(raw_path, RUN.resolve())
                and not raw_path.exists(),
                f"attempt {index}: {role} absent raw path",
            )
            expected_payload = expected_payloads[role]
            require(
                record.get("raw_size_bytes") == len(expected_payload)
                and record.get("raw_sha256") == sha256_bytes(expected_payload),
                f"attempt {index}: {role} exact reconstruction binding",
            )
        generator_path = direct_paths.get("generator_manifest")
        require(
            generator_path is not None,
            f"attempt {index}: generator manifest absent",
        )
        generator = strict_json(
            generator_path.read_bytes(),
            f"attempt {index} generator",
        )
        require(isinstance(generator, dict), "generator manifest type")
        require(
            generator.get("cnf_sha256")
            == reconstructed["cnf"].get("raw_sha256")
            and generator.get("colorings_sha256")
            == reconstructed["cuts_input"].get("raw_sha256")
            and generator.get("coloring_cut_count") == index,
            f"attempt {index}: generator/reconstruction mismatch",
        )
        artifact_checks += 4
        cut_body += cut_lines[index]

    require(artifact_checks == 2210, "present artifact check count")

    # Independently replay predecessor and history-chain chronology.
    history = history_initial()
    predecessor = checkpoint_digest(
        attempt_count=0,
        cut_count=0,
        cuts_payload_sha256=prefixes[0],
        history_chain_sha256=history,
    )
    for index, (reference, cut, manifest) in enumerate(
        zip(attempt_records, cut_records, manifests)
    ):
        require(
            reference["history_chain_before_sha256"] == history
            and manifest["history_chain_before_sha256"] == history
            and reference["checkpoint_before_sha256"] == predecessor
            and manifest["checkpoint_before_sha256"] == predecessor,
            f"chronology predecessor {index}",
        )
        history = history_step(history, reference, cut)
        predecessor = checkpoint_digest(
            attempt_count=index + 1,
            cut_count=index + 1,
            cuts_payload_sha256=prefixes[index + 1],
            history_chain_sha256=history,
        )
    require(
        history == checkpoint.get("history_chain_sha256") == HISTORY_HEAD_SHA256,
        "history chain head",
    )

    # Exactly 170 referenced attempt directories plus the unreferenced 000170.
    actual_directories = sorted(
        path.resolve()
        for path in (RUN / "attempts").iterdir()
        if path.is_dir()
    )
    require(len(actual_directories) == 171, "unexpected attempt directory count")
    referenced_directories = {
        Path(str(reference["manifest_path"])).parent.resolve()
        for reference in attempt_records
    }
    require(
        LIVE_ORPHAN.resolve() not in referenced_directories,
        "orphan unexpectedly checkpoint-referenced",
    )
    require(
        set(actual_directories) - referenced_directories == {LIVE_ORPHAN.resolve()},
        "attempt directory set is not 170 referenced plus exact orphan",
    )
    require(
        not (LIVE_ORPHAN / "attempt.json").exists(),
        "orphan attempt manifest unexpectedly exists",
    )
    require(
        not any(
            path.name in {"unsat.verified.json", "candidate.freeze.json"}
            for path in RUN.iterdir()
        ),
        "terminal marker unexpectedly exists",
    )
    return {
        "checkpoint": checkpoint,
        "cuts": cut_records,
        "colorings": tuple(colorings),
        "present_artifact_hash_checks": artifact_checks,
        "history_chain_sha256": history,
        "referenced_attempt_count": len(referenced_directories),
        "orphan_unreferenced": True,
    }


def validate_orphan_and_package() -> dict[str, object]:
    certificate_payload = exact_binding(
        PACKAGE / "certificate.json",
        (11639, CERTIFICATE_SHA256),
        "certificate",
    )
    certificate = strict_json(certificate_payload, "certificate")
    require(isinstance(certificate, dict), "certificate type")
    require(
        certificate.get("schema")
        == "gamma-theta-hole9-recovered-certificate-v1"
        and certificate.get("status") == "verified_pending_hostile_review",
        "certificate schema/status",
    )
    records = certificate.get("package_artifacts")
    require(isinstance(records, list), "package artifact ledger")
    recorded_paths: set[str] = set()
    for record in records:
        require(
            isinstance(record, dict)
            and set(record) == {"path", "sha256", "size_bytes"}
            and type(record["path"]) is str,
            "package artifact record",
        )
        relative = record["path"]
        require(relative not in recorded_paths, "duplicate package artifact")
        recorded_paths.add(relative)
        path = regular_single_link(PACKAGE / relative, f"package {relative}")
        require(within(path, PACKAGE.resolve()), "package path escape")
        require(
            path.stat().st_size == record["size_bytes"]
            and sha256_file(path) == record["sha256"],
            f"package artifact mismatch: {relative}",
        )
    actual_paths = {
        path.relative_to(PACKAGE).as_posix()
        for path in PACKAGE.rglob("*")
        if path.is_file()
    }
    require(
        actual_paths == recorded_paths | {"certificate.json"},
        "package omitted/extra file",
    )

    live_run_manifest = exact_binding(
        RUN / "run_manifest.json",
        (4442, RUN_MANIFEST_SHA256),
        "live run manifest",
    )
    live_checkpoint = exact_binding(
        RUN / "checkpoint.json",
        (253000, CHECKPOINT_SHA256),
        "live checkpoint",
    )
    require(
        (PACKAGE / "source/run_manifest.json").read_bytes() == live_run_manifest,
        "packaged run manifest differs from live source",
    )
    require(
        (PACKAGE / "source/checkpoint.json").read_bytes() == live_checkpoint,
        "packaged checkpoint differs from live source",
    )
    for name, binding in ORPHAN_BINDINGS.items():
        live_payload = exact_binding(LIVE_ORPHAN / name, binding, f"live {name}")
        packaged_payload = exact_binding(
            PACKAGED_ORPHAN / name,
            binding,
            f"packaged {name}",
        )
        require(live_payload == packaged_payload, f"source/package {name} mismatch")
    require(
        (LIVE_ORPHAN / "solver.result").read_bytes() == b"s UNSATISFIABLE\n"
        and (LIVE_ORPHAN / "proof.result").read_bytes() == b"s UNSATISFIABLE\n",
        "exact duplicate UNSAT result bytes",
    )
    require(
        b"s VERIFIED" not in (LIVE_ORPHAN / "checker.stdout").read_bytes()
        and (LIVE_ORPHAN / "checker.stderr").read_bytes() == b"",
        "failed source checker transcript masquerades as success",
    )

    incident_payload = exact_binding(
        INCIDENT,
        (4993, INCIDENT_SHA256),
        "ART-115 incident",
    )
    incident = strict_json(incident_payload, "ART-115 incident")
    require(isinstance(incident, dict), "incident type")
    recorded_cut_digest = (
        incident.get("unreferenced_attempt", {})
        .get("artifacts", {})
        .get("cuts.json", {})
        .get("sha256")
    )
    incident_defects: list[dict[str, object]] = []
    if recorded_cut_digest != CUTS_SHA256:
        incident_defects.append(
            {
                "severity": "correction_required",
                "artifact": "results/logs/synthesis-k3-hole9-batch-004-checker-incident.json",
                "field": "unreferenced_attempt.artifacts.cuts.json.sha256",
                "recorded": recorded_cut_digest,
                "actual": CUTS_SHA256,
                "recorded_length": (
                    len(recorded_cut_digest)
                    if isinstance(recorded_cut_digest, str)
                    else None
                ),
                "finding": "ART-115 omits the final hexadecimal digit `b`",
            }
        )

    # Require the non-destructive erratum to bind and supersede that typo.
    incident_erratum_payload = exact_binding(
        INCIDENT_ERRATUM,
        (2652, INCIDENT_ERRATUM_SHA256),
        "ART-115 erratum",
    )
    incident_erratum = strict_json(incident_erratum_payload, "ART-115 erratum")
    require(isinstance(incident_erratum, dict), "incident erratum type")
    require(
        incident_erratum.get("schema")
        == "gamma-theta-k3-cegar-checker-incident-erratum-v1"
        and incident_erratum.get("status") == "ERRATUM",
        "incident erratum schema/status",
    )
    superseded = incident_erratum.get("superseded_artifact")
    error = incident_erratum.get("error")
    require(
        isinstance(superseded, dict)
        and superseded.get("artifact_id") == "ART-115"
        and superseded.get("path") == INCIDENT.relative_to(ROOT).as_posix()
        and superseded.get("sha256") == INCIDENT_SHA256,
        "incident erratum superseded binding",
    )
    require(
        isinstance(error, dict)
        and error.get("json_pointer")
        == "/unreferenced_attempt/artifacts/cuts.json/sha256"
        and error.get("recorded_value") == recorded_cut_digest
        and error.get("recorded_length") == len(str(recorded_cut_digest))
        and error.get("correct_value") == CUTS_SHA256
        and error.get("correct_length") == len(CUTS_SHA256) == 64,
        "incident erratum exact correction",
    )
    independent_bindings = incident_erratum.get("independent_bindings")
    require(
        isinstance(independent_bindings, list)
        and len(independent_bindings) == 4,
        "incident erratum independent bindings",
    )
    by_role = {
        row.get("role"): row
        for row in independent_bindings
        if isinstance(row, dict)
    }
    live_cut_binding = by_role.get("live orphan cuts")
    checkpoint_binding = by_role.get("atomic checkpoint cuts_payload_sha256")
    generator_binding = by_role.get("orphan generator colorings_sha256")
    package_cut_binding = by_role.get("sealed recovery-package cuts")
    require(
        isinstance(live_cut_binding, dict)
        and live_cut_binding.get("size_bytes") == 4422
        and live_cut_binding.get("sha256") == CUTS_SHA256
        and sha256_file(ROOT / str(live_cut_binding.get("path")))
        == CUTS_SHA256,
        "incident erratum live-cut binding",
    )
    packaged_checkpoint = strict_json(
        (PACKAGE / "source/checkpoint.json").read_bytes(),
        "packaged checkpoint for erratum",
    )
    packaged_generator = strict_json(
        (PACKAGED_ORPHAN / "generator.json").read_bytes(),
        "packaged generator for erratum",
    )
    require(
        isinstance(checkpoint_binding, dict)
        and checkpoint_binding.get("container_sha256") == CHECKPOINT_SHA256
        and checkpoint_binding.get("sha256") == CUTS_SHA256
        and isinstance(packaged_checkpoint, dict)
        and packaged_checkpoint.get("cuts_payload_sha256") == CUTS_SHA256,
        "incident erratum checkpoint binding",
    )
    require(
        isinstance(generator_binding, dict)
        and generator_binding.get("container_sha256") == GENERATOR_SHA256
        and generator_binding.get("sha256") == CUTS_SHA256
        and isinstance(packaged_generator, dict)
        and packaged_generator.get("colorings_sha256") == CUTS_SHA256,
        "incident erratum generator binding",
    )
    require(
        isinstance(package_cut_binding, dict)
        and package_cut_binding.get("package_tree_sha256")
        == PACKAGE_TREE_SHA256
        and package_cut_binding.get("sha256") == CUTS_SHA256
        and sha256_file(PACKAGED_ORPHAN / "cuts.json") == CUTS_SHA256,
        "incident erratum package-cut binding",
    )

    # Require the second erratum to correct the one imprecise source sentence.
    soundness_erratum_payload = exact_binding(
        SOUNDNESS_ERRATUM,
        (2702, SOUNDNESS_ERRATUM_SHA256),
        "soundness-note erratum",
    )
    soundness_erratum = strict_json(
        soundness_erratum_payload,
        "soundness-note erratum",
    )
    require(isinstance(soundness_erratum, dict), "soundness erratum type")
    require(
        soundness_erratum.get("schema")
        == "gamma-theta-hole9-recovery-soundness-erratum-v1"
        and soundness_erratum.get("status") == "ERRATUM",
        "soundness erratum schema/status",
    )
    affected = soundness_erratum.get("affected_artifacts")
    require(
        isinstance(affected, list) and len(affected) == 2,
        "soundness erratum affected artifacts",
    )
    affected_by_role = {
        row.get("role"): row
        for row in affected
        if isinstance(row, dict)
    }
    source_note_binding = affected_by_role.get("source soundness note")
    package_note_binding = affected_by_role.get("sealed package copy")
    note_digest = (
        "3c341560cb46e8a10ad0eb89ea8aa0e7e4131ea8c6d1dbaf7f1634282a2fa4bc"
    )
    require(
        isinstance(source_note_binding, dict)
        and source_note_binding.get("sha256") == note_digest
        and sha256_file(ROOT / str(source_note_binding.get("path"))) == note_digest,
        "soundness erratum source-note binding",
    )
    require(
        isinstance(package_note_binding, dict)
        and package_note_binding.get("sha256") == note_digest
        and package_note_binding.get("package_tree_sha256")
        == PACKAGE_TREE_SHA256
        and package_note_binding.get("certificate_sha256") == CERTIFICATE_SHA256
        and sha256_file(PACKAGE / "SOUNDNESS.md") == note_digest,
        "soundness erratum package-note binding",
    )
    wording_error = soundness_erratum.get("error")
    original_sentence = "The production runner generated the exact 170-cut CNF twice."
    corrected_sentence = (
        "The production runner generated the exact 170-cut CNF once and ran "
        "CaDiCaL twice against that same CNF path."
    )
    require(
        isinstance(wording_error, dict)
        and wording_error.get("section") == "The source incident"
        and wording_error.get("original_sentence") == original_sentence
        and wording_error.get("corrected_sentence") == corrected_sentence
        and original_sentence
        in (PACKAGE / "SOUNDNESS.md").read_text(encoding="utf-8"),
        "soundness erratum exact prose correction",
    )
    soundness_evidence = soundness_erratum.get("evidence")
    require(
        isinstance(soundness_evidence, dict)
        and soundness_evidence.get("generator_artifact_count") == 1
        and soundness_evidence.get("generator_sha256") == GENERATOR_SHA256
        and soundness_evidence.get("cnf_sha256") == FULL_CNF_SHA256,
        "soundness erratum generator/CNF evidence",
    )
    solver_passes = soundness_evidence.get("solver_passes")
    require(
        isinstance(solver_passes, list)
        and len(solver_passes) == 2,
        "soundness erratum solver passes",
    )
    result_paths = {
        ROOT / str(row.get("result_path"))
        for row in solver_passes
        if isinstance(row, dict)
        and row.get("parsed_status") == "UNSAT"
        and row.get("result_sha256") == ORPHAN_BINDINGS["solver.result"][1]
    }
    require(
        result_paths == {
            LIVE_ORPHAN / "solver.result",
            LIVE_ORPHAN / "proof.result",
        }
        and all(path.read_bytes() == b"s UNSATISFIABLE\n" for path in result_paths),
        "soundness erratum exact two solver results",
    )
    return {
        "certificate": certificate,
        "live_run_manifest": live_run_manifest,
        "live_checkpoint": live_checkpoint,
        "incident_defects": incident_defects,
        "errata": {
            "incident_erratum_sha256": INCIDENT_ERRATUM_SHA256,
            "soundness_erratum_sha256": SOUNDNESS_ERRATUM_SHA256,
            "both_validated": True,
        },
        "package_artifact_count": len(records),
    }


def validate_generator(
    generator_payload: bytes,
    colorings: Sequence[Sequence[int]],
) -> None:
    require(sha256_bytes(generator_payload) == GENERATOR_SHA256, "generator hash")
    generator = strict_json(generator_payload, "orphan generator")
    require(isinstance(generator, dict), "generator type")
    stream = hashlib.sha256()
    for coloring in colorings:
        stream.update((" ".join(map(str, coloring)) + "\n").encode("ascii"))
    require(
        generator.get("schema") == "gamma-theta-k3-cnf-v2"
        and generator.get("schema_version") == 2
        and generator.get("template") == "hole9"
        and generator.get("order") == N
        and generator.get("variable_count") == VARIABLE_COUNT
        and generator.get("clause_count") == FULL_CLAUSE_COUNT
        and generator.get("literal_count") == FULL_LITERAL_COUNT
        and generator.get("coloring_cut_count") == 170
        and generator.get("colorings_sha256") == CUTS_SHA256
        and generator.get("cnf_sha256") == FULL_CNF_SHA256
        and generator.get("coloring_cut_stream_sha256") == stream.hexdigest(),
        "generator dimensions/input/output bindings",
    )
    require(
        generator.get("generator_source_manifest")
        == [[path, digest] for path, digest in GENERATOR_SOURCES]
        and generator.get("generator_source_set_sha256")
        == source_set_hash(GENERATOR_SOURCES)
        == "e48f1b430cfa5d1421bb8e7c856d70db8fc634b27d6cbd51d7d22e11f16d30bd",
        "generator source-set binding",
    )


def run_mutations(
    base_clauses: tuple[tuple[int, ...], ...],
    original_proof: bytes,
    addition_only: bytes,
    additions: tuple[tuple[int, ...], ...],
) -> list[dict[str, object]]:
    outcomes: list[dict[str, object]] = []

    def expected_rejection(name: str, operation: object) -> None:
        try:
            operation()  # type: ignore[operator]
        except AuditFailure as error:
            outcomes.append(
                {
                    "mutation": name,
                    "status": "rejected_as_expected",
                    "reason": str(error),
                }
            )
            return
        raise AuditFailure(f"mutation unexpectedly accepted: {name}")

    # A valid but wrong CNF with the implication (-w_01,2 or e_02) removed.
    target_clause = (-67, 2)
    require(target_clause in base_clauses, "mutation target CNF clause absent")
    target_index = base_clauses.index(target_clause)
    wrong_cnf_clauses = (
        base_clauses[:target_index] + base_clauses[target_index + 1:]
    )
    wrong_cnf_payload = dimacs_bytes(VARIABLE_COUNT, wrong_cnf_clauses)
    parsed_variables, parsed_wrong_cnf = parse_cnf(wrong_cnf_payload)
    require(parsed_variables == VARIABLE_COUNT, "wrong CNF parse")
    require(
        sha256_bytes(wrong_cnf_payload) != BASE_CNF_SHA256,
        "wrong CNF hash collision",
    )
    wrong_cnf_checker = RUPChecker(VARIABLE_COUNT, parsed_wrong_cnf)
    require(additions[0] == (-67,), "unexpected first proof addition")
    require(
        not wrong_cnf_checker.check_rup(additions[0]),
        "wrong CNF did not break the first RUP step",
    )
    outcomes.append(
        {
            "mutation": "wrong_cnf_drop_clause_-67_or_2",
            "status": "rejected_as_expected",
            "reason": "first proof addition -67 is no longer RUP",
            "dropped_zero_based_clause_index": target_index,
        }
    )

    # A syntactically valid wrong first proof addition.
    wrong_addition_checker = RUPChecker(VARIABLE_COUNT, base_clauses)
    require(
        not wrong_addition_checker.check_rup((-66,)),
        "wrong unit addition -66 unexpectedly RUP",
    )
    outcomes.append(
        {
            "mutation": "wrong_first_addition_-66",
            "status": "rejected_as_expected",
            "reason": "fresh unit propagation finds no conflict",
        }
    )

    wrong_original = original_proof.replace(b"-67 0\n", b"-66 0\n", 1)
    wrong_parsed = parse_proof(wrong_original)
    require(
        sha256_bytes(wrong_original) != ORIGINAL_PROOF_SHA256
        and wrong_parsed["stripped"] != addition_only,
        "wrong proof binding mutation ineffective",
    )
    outcomes.append(
        {
            "mutation": "wrong_original_proof_byte_valid_syntax",
            "status": "rejected_as_expected",
            "reason": "original/stripped SHA-256 bindings change and first RUP fails",
        }
    )

    wrong_addition_only = addition_only.replace(b"-67 0\n", b"-66 0\n", 1)
    parse_proof(wrong_addition_only)
    require(
        sha256_bytes(wrong_addition_only) != ADDITION_ONLY_SHA256,
        "wrong addition-only proof hash collision",
    )
    outcomes.append(
        {
            "mutation": "wrong_stored_addition_only_proof",
            "status": "rejected_as_expected",
            "reason": "stored proof SHA-256 changes and first RUP fails",
        }
    )

    lines = original_proof.splitlines(keepends=True)
    require(lines[-1] == b"0\n", "unexpected original proof terminus")
    expected_rejection(
        "missing_final_empty_clause",
        lambda: parse_proof(b"".join(lines[:-1])),
    )
    expected_rejection(
        "instruction_after_empty_clause",
        lambda: parse_proof(original_proof + b"1 0\n"),
    )
    malformed_deletions = {
        "malformed_deletion_missing_zero": b"1 0\nd 2\n0\n",
        "malformed_deletion_duplicate": b"1 0\nd 2 2 0\n0\n",
        "malformed_deletion_empty": b"1 0\nd 0\n0\n",
        "malformed_deletion_extra_zero": b"1 0\nd 2 0 0\n0\n",
        "malformed_deletion_double_space": b"1 0\nd  2 0\n0\n",
    }
    for name, payload in malformed_deletions.items():
        expected_rejection(name, lambda payload=payload: parse_proof(payload))
    return outcomes


def audit() -> dict[str, object]:
    started = time.perf_counter()
    run_tree_before = tree_digest(RUN)
    package_tree_before = tree_digest(PACKAGE)
    require(
        run_tree_before
        == {
            "sha256": RUN_TREE_SHA256,
            "file_count": 1205,
            "total_file_bytes": 6946580,
        },
        "live run tree binding",
    )
    require(
        package_tree_before
        == {
            "sha256": PACKAGE_TREE_SHA256,
            "file_count": 23,
            "total_file_bytes": 1486583,
        },
        "package tree binding",
    )

    package_evidence = validate_orphan_and_package()
    validate_run_manifest(package_evidence["live_run_manifest"])

    base_variable_count, base_clauses, edge_variables = build_formula(())
    base_payload = dimacs_bytes(base_variable_count, base_clauses)
    require(
        base_variable_count == VARIABLE_COUNT
        and len(base_clauses) == BASE_CLAUSE_COUNT
        and sum(map(len, base_clauses)) == BASE_LITERAL_COUNT
        and sha256_bytes(base_payload) == BASE_CNF_SHA256,
        "independent base formula dimensions/hash",
    )
    chronology = validate_checkpoint_and_attempts(
        package_evidence["live_checkpoint"],
        base_clauses,
        edge_variables,
    )
    colorings = chronology["colorings"]
    require(isinstance(colorings, tuple), "internal coloring ledger")

    full_variable_count, full_clauses, full_edges = build_formula(colorings)
    require(full_edges == edge_variables, "edge allocation instability")
    reconstructed_cnf = dimacs_bytes(full_variable_count, full_clauses)
    source_cnf = (PACKAGED_ORPHAN / "instance.cnf").read_bytes()
    parsed_variable_count, parsed_clauses = parse_cnf(source_cnf)
    require(
        full_variable_count == parsed_variable_count == VARIABLE_COUNT
        and len(full_clauses) == len(parsed_clauses) == FULL_CLAUSE_COUNT
        and sum(map(len, full_clauses)) == FULL_LITERAL_COUNT
        and full_clauses == parsed_clauses
        and reconstructed_cnf == source_cnf
        and sha256_bytes(reconstructed_cnf) == FULL_CNF_SHA256,
        "exact full CNF reconstruction/parse",
    )
    cuts_payload = (PACKAGED_ORPHAN / "cuts.json").read_bytes()
    require(
        cuts_payload == canonical_json([list(coloring) for coloring in colorings])
        and sha256_bytes(cuts_payload) == CUTS_SHA256,
        "exact orphan cuts payload",
    )
    validate_generator(
        (PACKAGED_ORPHAN / "generator.json").read_bytes(),
        colorings,
    )

    original_proof = (PACKAGED_ORPHAN / "proof.drat").read_bytes()
    addition_only = (PACKAGE / "proof/addition-only.rup.drat").read_bytes()
    original_stats = parse_proof(original_proof)
    stripped_stats = parse_proof(addition_only)
    require(
        original_stats["line_count"] == 16388
        and original_stats["addition_count"] == 4705
        and original_stats["deletion_count"] == 11683
        and original_stats["comment_count"] == 0
        and original_stats["empty_count"] == 1
        and original_stats["maximum_variable"] == VARIABLE_COUNT
        and original_stats["maximum_clause_size"] == 220,
        "original proof exact statistics",
    )
    require(
        stripped_stats["line_count"] == 4705
        and stripped_stats["addition_count"] == 4705
        and stripped_stats["deletion_count"] == 0
        and stripped_stats["comment_count"] == 0
        and stripped_stats["empty_count"] == 1
        and stripped_stats["maximum_variable"] == VARIABLE_COUNT
        and stripped_stats["maximum_clause_size"] == 218,
        "addition-only proof exact statistics",
    )
    require(
        original_stats["stripped"] == addition_only
        and stripped_stats["stripped"] == addition_only
        and original_stats["additions"] == stripped_stats["additions"]
        and len(addition_only) == 65906
        and sha256_bytes(addition_only) == ADDITION_ONLY_SHA256,
        "deterministic strict deletion stripping",
    )

    additions = stripped_stats["additions"]
    addition_lines = stripped_stats["addition_lines"]
    require(
        isinstance(additions, tuple) and isinstance(addition_lines, tuple),
        "internal proof representation",
    )
    replay_started = time.perf_counter()
    checker = RUPChecker(VARIABLE_COUNT, parsed_clauses)
    for addition_index, clause in enumerate(additions):
        require(
            checker.check_rup(clause),
            (
                f"non-RUP addition {addition_index + 1}/4705 "
                f"(proof line {addition_lines[addition_index]})"
            ),
        )
        checker.add_clause(clause)
    replay_seconds = time.perf_counter() - replay_started
    require(
        checker.check_count == 4705
        and checker.has_empty_clause
        and additions[-1] == (),
        "RUP replay did not validate and install all additions",
    )

    # Cross-check every decisive numerical/logical claim made by the outer
    # certificate against the independently computed values above.
    certificate = package_evidence["certificate"]
    require(isinstance(certificate, dict), "internal certificate object")
    reconstruction_claim = certificate.get("independent_reconstruction")
    transformation_claim = certificate.get("proof_transformation")
    source_claim = certificate.get("source")
    validation_claim = certificate.get("validation")
    require(
        isinstance(reconstruction_claim, dict)
        and reconstruction_claim.get("variable_count") == VARIABLE_COUNT
        and reconstruction_claim.get("base_clause_count") == BASE_CLAUSE_COUNT
        and reconstruction_claim.get("cut_clause_count") == 170
        and reconstruction_claim.get("total_clause_count") == FULL_CLAUSE_COUNT
        and reconstruction_claim.get("base_literal_count") == BASE_LITERAL_COUNT
        and reconstruction_claim.get("literal_count") == FULL_LITERAL_COUNT
        and reconstruction_claim.get("present_attempt_artifact_hash_checks")
        == 2210
        and reconstruction_claim.get("cnf_byte_equality") is True
        and reconstruction_claim.get("checkpoint_history_chain_replayed") is True,
        "certificate reconstruction claims",
    )
    require(
        isinstance(transformation_claim, dict)
        and transformation_claim.get("original_sha256")
        == ORIGINAL_PROOF_SHA256
        and transformation_claim.get("original_size_bytes") == 512071
        and transformation_claim.get("original_line_count") == 16388
        and transformation_claim.get("addition_count") == 4705
        and transformation_claim.get("deletion_count") == 11683
        and transformation_claim.get("comment_count") == 0
        and transformation_claim.get("empty_addition_count") == 1
        and transformation_claim.get("maximum_variable") == VARIABLE_COUNT
        and transformation_claim.get("maximum_clause_size") == 220
        and transformation_claim.get("stripped_sha256")
        == ADDITION_ONLY_SHA256
        and transformation_claim.get("stripped_size_bytes") == 65906
        and transformation_claim.get("stripped_line_count") == 4705
        and transformation_claim.get("addition_only_reparse_deletion_count") == 0,
        "certificate proof-transformation claims",
    )
    require(
        isinstance(source_claim, dict)
        and source_claim.get("checkpoint_sha256") == CHECKPOINT_SHA256
        and source_claim.get("run_manifest_sha256") == RUN_MANIFEST_SHA256
        and source_claim.get("original_cnf_sha256") == FULL_CNF_SHA256
        and source_claim.get("original_proof_sha256") == ORIGINAL_PROOF_SHA256
        and source_claim.get("orphan_directory_name") == "000170.akmx9xl0"
        and source_claim.get("orphan_was_checkpoint_referenced") is False
        and source_claim.get("checkpoint_status") == "running"
        and source_claim.get("checkpoint_terminal") is None,
        "certificate source claims",
    )
    for tree_role in ("run_tree_before", "run_tree_after"):
        tree_claim = source_claim.get(tree_role)
        require(
            isinstance(tree_claim, dict)
            and tree_claim.get("sha256") == run_tree_before["sha256"]
            and tree_claim.get("file_count") == run_tree_before["file_count"]
            and tree_claim.get("total_file_bytes")
            == run_tree_before["total_file_bytes"],
            f"certificate {tree_role} claim",
        )
    require(
        isinstance(validation_claim, dict)
        and all(value is True for value in validation_claim.values())
        and validation_claim.get("package_pending_hostile_review") is True
        and validation_claim.get("addition_only_proof_rup_verified") is True
        and validation_claim.get("cut_ledger_and_chronology") is True
        and validation_claim.get("formula_exactly_reconstructed") is True,
        "certificate validation claims",
    )
    for checker_role, expected_flags, semantics in (
        (
            "primary_checker",
            ["-I", "-f", "-W", "-U", "-t", "60"],
            "forward addition-only RUP",
        ),
        (
            "redundant_original_checker",
            ["-I", "-f", "-p", "-W", "-U", "-t", "60"],
            "forward plain-mode RUP; deletions ignored",
        ),
    ):
        checker_claim = certificate.get(checker_role)
        require(
            isinstance(checker_claim, dict)
            and checker_claim.get("required_flags") == expected_flags
            and checker_claim.get("semantics") == semantics
            and checker_claim.get("exact_verified_line_count") == 1
            and checker_claim.get("warning_count") == 0
            and isinstance(checker_claim.get("record"), dict)
            and checker_claim["record"].get("exit_code") == 0
            and checker_claim["record"].get("timed_out") is False
            and checker_claim["record"].get("memory_limit_exceeded") is False,
            f"certificate {checker_role} claim",
        )

    mutation_results = run_mutations(
        base_clauses,
        original_proof,
        addition_only,
        additions,
    )
    run_tree_after = tree_digest(RUN)
    package_tree_after = tree_digest(PACKAGE)
    require(run_tree_after == run_tree_before, "probe changed live run tree")
    require(package_tree_after == package_tree_before, "probe changed package tree")
    total_seconds = time.perf_counter() - started
    incident_defects = package_evidence["incident_defects"]
    require(isinstance(incident_defects, list), "internal incident findings")

    return {
        "schema": "hole9-orphan-recovery-hostile-probe-v1",
        "status": "accepted_with_validated_errata",
        "standalone_import_boundary": (
            "Python standard library only; no project module imported"
        ),
        "hashes": {
            "run_manifest_sha256": RUN_MANIFEST_SHA256,
            "checkpoint_sha256": CHECKPOINT_SHA256,
            "cuts_sha256": CUTS_SHA256,
            "cnf_sha256": FULL_CNF_SHA256,
            "original_proof_sha256": ORIGINAL_PROOF_SHA256,
            "addition_only_proof_sha256": ADDITION_ONLY_SHA256,
            "certificate_sha256": CERTIFICATE_SHA256,
            "incident_sha256": INCIDENT_SHA256,
            "incident_erratum_sha256": INCIDENT_ERRATUM_SHA256,
            "soundness_erratum_sha256": SOUNDNESS_ERRATUM_SHA256,
            "run_tree_sha256": RUN_TREE_SHA256,
            "package_tree_sha256": PACKAGE_TREE_SHA256,
        },
        "chronology": {
            "committed_attempt_count": chronology["referenced_attempt_count"],
            "committed_cut_count": len(chronology["cuts"]),
            "present_artifact_hash_checks": chronology[
                "present_artifact_hash_checks"
            ],
            "history_chain_sha256": chronology["history_chain_sha256"],
            "orphan_unreferenced": chronology["orphan_unreferenced"],
        },
        "formula": {
            "variable_count": VARIABLE_COUNT,
            "base_clause_count": BASE_CLAUSE_COUNT,
            "cut_clause_count": 170,
            "total_clause_count": FULL_CLAUSE_COUNT,
            "base_literal_count": BASE_LITERAL_COUNT,
            "total_literal_count": FULL_LITERAL_COUNT,
            "byte_identical_reconstruction": True,
        },
        "proof": {
            "original_line_count": original_stats["line_count"],
            "addition_count": original_stats["addition_count"],
            "deletion_count": original_stats["deletion_count"],
            "comment_count": original_stats["comment_count"],
            "empty_addition_count": original_stats["empty_count"],
            "all_additions_rup": True,
            "final_addition_empty": True,
            "watched_clause_visits": checker.clause_visits,
            "assignment_enqueues": checker.enqueues,
            "maximum_trail": checker.maximum_trail,
        },
        "mutations": mutation_results,
        "corrected_findings": incident_defects,
        "errata": package_evidence["errata"],
        "timing_seconds": {
            "rup_replay": replay_seconds,
            "total": total_seconds,
        },
        "read_only_tree_check": {
            "run_before": run_tree_before,
            "run_after": run_tree_after,
            "package_before": package_tree_before,
            "package_after": package_tree_after,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--compact",
        action="store_true",
        help="emit compact rather than indented JSON",
    )
    arguments = parser.parse_args()
    try:
        result = audit()
    except AuditFailure as error:
        print(
            json.dumps(
                {
                    "schema": "hole9-orphan-recovery-hostile-probe-v1",
                    "status": "failed",
                    "error": str(error),
                },
                sort_keys=True,
            )
        )
        return 1
    print(
        json.dumps(
            result,
            sort_keys=True,
            indent=None if arguments.compact else 2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
