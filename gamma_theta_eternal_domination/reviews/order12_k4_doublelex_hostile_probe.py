#!/usr/bin/env python3
"""Independent hostile probe for the proposed order-12 k=4 DoubleLex gate.

The suffix is reconstructed without calling ``search.k4_doublelex``.  The
accepted pre-sort formula is then checked for covariance under generators of
S_8 x S_4 using an independently allocated semantic-variable action.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from search import k4_doublelex  # noqa: E402
from synthesis_k4.encoding import build_k4_encoding  # noqa: E402


EXPECTED = {
    "math/lemmas/order12_k4_doublelex.md": (
        "d5be9b6373d7aa7c49dec32c18c6202698b35fe05a1f58b2b97dcc98d9114a76"
    ),
    "src/search/k4_doublelex.py": (
        "e5aeb23eb3938631c62a29df45a880839fa9c8384121e0ec310d9740936baba1"
    ),
    "tests/test_k4_doublelex.py": (
        "36282f747f971cf5a57c90e1b645fbe2cd76ab51c3413b7b2268547144322469"
    ),
    "instances/order12_k4_connected_parent/instance.cnf": (
        "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac"
    ),
}
EXPECTED_SUFFIX_SHA256 = (
    "328eeeaadc688bbce63fd3ffd952f86a4eb9209e6d0abf5542979fe54ebdbbe0"
)
EXPECTED_OUTPUT_SHA256 = (
    "14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7"
)

N = 12
VERTICES = tuple(range(N))
ANCHOR = tuple(range(4))
OUTER = tuple(range(4, 12))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def edge(first: int, second: int) -> int:
    """Independent closed form for combinations(range(12), 2) numbering."""

    if first > second:
        first, second = second, first
    if not 0 <= first < second < N:
        raise ValueError("bad edge")
    return 1 + first * (2 * N - first - 1) // 2 + second - first - 1


def independent_comparator(
    left_anchor: int, right_anchor: int
) -> tuple[tuple[int, ...], ...]:
    clauses: list[tuple[int, ...]] = []
    for first_difference in range(8):
        for prefix in product((0, 1), repeat=first_difference):
            clause: list[int] = []
            for coordinate, bit in enumerate(prefix):
                left = edge(left_anchor, OUTER[coordinate])
                right = edge(right_anchor, OUTER[coordinate])
                clause.extend((left, right) if bit == 0 else (-left, -right))
            clause.extend(
                (
                    -edge(left_anchor, OUTER[first_difference]),
                    edge(right_anchor, OUTER[first_difference]),
                )
            )
            clauses.append(tuple(clause))
    return tuple(clauses)


def independent_suffix() -> tuple[tuple[int, ...], ...]:
    return tuple(
        clause
        for left, right in zip(ANCHOR[:-1], ANCHOR[1:], strict=True)
        for clause in independent_comparator(left, right)
    )


def dimacs_suffix(clauses: tuple[tuple[int, ...], ...]) -> bytes:
    return b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in clauses
    )


def exhaustive_comparator_check(
    clauses: tuple[tuple[int, ...], ...]
) -> int:
    left_variables = tuple(edge(0, vertex) for vertex in OUTER)
    right_variables = tuple(edge(1, vertex) for vertex in OUTER)
    checked = 0
    for assignment in product((False, True), repeat=16):
        values = dict(
            zip(left_variables + right_variables, assignment, strict=True)
        )
        observed = all(
            any(values[abs(literal)] == (literal > 0) for literal in clause)
            for clause in clauses
        )
        expected = assignment[:8] <= assignment[8:]
        if observed != expected:
            raise AssertionError(f"comparator counterexample: {assignment}")
        checked += 1
    return checked


def semantic_maps() -> tuple[
    dict[tuple[int, int], int],
    dict[tuple[tuple[int, int, int], int], int],
    dict[tuple[int, int, int, int], int],
    dict[tuple[tuple[int, int, int, int], int, int], int],
]:
    cursor = 1
    edges = {
        pair: variable
        for variable, pair in enumerate(
            combinations(VERTICES, 2), start=cursor
        )
    }
    cursor += len(edges)
    triples = tuple(combinations(VERTICES, 3))
    witnesses = {
        record: variable
        for variable, record in enumerate(
            (
                (triple, witness)
                for triple in triples
                for witness in VERTICES
                if witness not in triple
            ),
            start=cursor,
        )
    }
    cursor += len(witnesses)
    states = tuple(combinations(VERTICES, 4))
    families = {
        state: variable
        for variable, state in enumerate(states, start=cursor)
    }
    cursor += len(families)
    moves = {
        record: variable
        for variable, record in enumerate(
            (
                (state, attacked, guard)
                for state in states
                for attacked in VERTICES
                if attacked not in state
                for guard in state
            ),
            start=cursor,
        )
    }
    cursor += len(moves)
    if cursor - 1 != 18_381:
        raise AssertionError("independent variable census differs")
    return edges, witnesses, families, moves


def covariance_check(parent: bytes) -> dict[str, object]:
    edges, witnesses, families, moves = semantic_maps()
    reverse: dict[int, tuple[str, object]] = {}
    for kind, mapping in (
        ("edge", edges),
        ("witness", witnesses),
        ("family", families),
        ("move", moves),
    ):
        for key, variable in mapping.items():
            if variable in reverse:
                raise AssertionError("variable families overlap")
            reverse[variable] = (kind, key)

    encoding = build_k4_encoding(
        include_coloring_bank=True,
        include_signature_breaker=False,
    )
    if (
        encoding.edge_variables != edges
        or encoding.witness_variables != witnesses
        or encoding.family_variables != families
        or encoding.move_variables != moves
    ):
        raise AssertionError("semantic allocation differs from accepted encoder")
    if (
        encoding.cnf.variable_count != 18_381
        or len(encoding.cnf.clauses) != 114_637
        or encoding.cnf.literal_count != 1_179_330
    ):
        raise AssertionError("F0 census differs")

    lines = parent.decode("ascii").splitlines()[1:]
    prefix = [
        tuple(map(int, line.split()[:-1]))
        for line in lines[: len(encoding.cnf.clauses)]
    ]
    if prefix != encoding.cnf.clauses:
        raise AssertionError("accepted parent is not exact F0 followed by R")
    base = Counter(tuple(sorted(clause)) for clause in encoding.cnf.clauses)

    def variable_action(permutation: tuple[int, ...]) -> dict[int, int]:
        action: dict[int, int] = {}
        for variable, (kind, key) in reverse.items():
            if kind == "edge":
                first, second = key
                target = edges[
                    tuple(sorted((permutation[first], permutation[second])))
                ]
            elif kind == "witness":
                triple, witness = key
                target = witnesses[
                    (
                        tuple(sorted(permutation[v] for v in triple)),
                        permutation[witness],
                    )
                ]
            elif kind == "family":
                target = families[
                    tuple(sorted(permutation[v] for v in key))
                ]
            else:
                state, attacked, guard = key
                target = moves[
                    (
                        tuple(sorted(permutation[v] for v in state)),
                        permutation[attacked],
                        permutation[guard],
                    )
                ]
            action[variable] = target
        return action

    generators = (
        ((0, 1), (1, 2), (2, 3))
        + tuple((vertex, vertex + 1) for vertex in range(4, 11))
    )
    checked: list[list[int]] = []
    for first, second in generators:
        permutation = list(VERTICES)
        permutation[first], permutation[second] = (
            permutation[second],
            permutation[first],
        )
        action = variable_action(tuple(permutation))
        image = Counter(
            tuple(
                sorted(
                    (1 if literal > 0 else -1) * action[abs(literal)]
                    for literal in clause
                )
            )
            for clause in encoding.cnf.clauses
        )
        if image != base:
            raise AssertionError(
                f"F0 covariance failed for swap {first},{second}"
            )
        checked.append([first, second])
    return {
        "f0_clause_count": len(encoding.cnf.clauses),
        "f0_literal_count": encoding.cnf.literal_count,
        "semantic_variable_count": len(reverse),
        "generator_count": len(checked),
        "generators": checked,
    }


def small_orbit_check() -> int:
    """Exhaust all 3x3 matrices as a regression for the least-image proof."""

    row_permutations = tuple(permutations(range(3)))
    column_permutations = tuple(permutations(range(3)))
    checked = 0
    for bits in product((0, 1), repeat=9):
        matrix = tuple(tuple(bits[3 * row : 3 * row + 3]) for row in range(3))
        images = []
        for rows in row_permutations:
            for columns in column_permutations:
                image = tuple(
                    tuple(matrix[row][column] for column in columns)
                    for row in rows
                )
                images.append(image)
        least = min(images)
        rows_ok = all(least[row] <= least[row + 1] for row in range(2))
        columns = tuple(
            tuple(least[row][column] for row in range(3))
            for column in range(3)
        )
        columns_ok = all(
            columns[column] <= columns[column + 1] for column in range(2)
        )
        if not rows_ok or not columns_ok:
            raise AssertionError(f"least-image regression failed: {matrix}")
        checked += 1
    return checked


def main() -> int:
    for relative, expected in EXPECTED.items():
        observed = digest(ROOT / relative)
        if observed != expected:
            raise AssertionError(f"hash differs for {relative}: {observed}")

    parent = (ROOT / "instances/order12_k4_connected_parent/instance.cnf").read_bytes()
    clauses = independent_suffix()
    if len(clauses) != 765 or sum(map(len, clauses)) != 10_758:
        raise AssertionError("independent suffix census differs")
    suffix = dimacs_suffix(clauses)
    if sha256(suffix).hexdigest() != EXPECTED_SUFFIX_SHA256:
        raise AssertionError("independent suffix hash differs")
    if clauses != k4_doublelex.doublelex_suffix():
        raise AssertionError("implementation suffix differs")

    _, body = parent.split(b"\n", 1)
    output = b"p cnf 18381 115507\n" + body + suffix
    if (
        len(output) != 4_030_657
        or sha256(output).hexdigest() != EXPECTED_OUTPUT_SHA256
        or output != k4_doublelex.build_doublelex_payload(parent)
    ):
        raise AssertionError("independent strengthened payload differs")

    result = {
        "status": "PASS",
        "reviewed_hashes": EXPECTED,
        "parent_size_bytes": len(parent),
        "suffix_clause_count": len(clauses),
        "suffix_literal_count": sum(map(len, clauses)),
        "suffix_size_bytes": len(suffix),
        "suffix_sha256": sha256(suffix).hexdigest(),
        "output_size_bytes": len(output),
        "output_sha256": sha256(output).hexdigest(),
        "comparator_truth_assignments": exhaustive_comparator_check(
            clauses[:255]
        ),
        "covariance": covariance_check(parent),
        "small_orbit_matrices": small_orbit_check(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
