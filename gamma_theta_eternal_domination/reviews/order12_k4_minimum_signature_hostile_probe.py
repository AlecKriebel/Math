#!/usr/bin/env python3
"""Independent exhaustive probe for the order-12 k=4 minimum-signature lemma."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CNF_PATH = ROOT / "instances/order12_k4_connected_parent/instance.cnf"
NOTE_PATH = ROOT / "math/lemmas/order12_k4_minimum_signature.md"
EXPECTED_CNF_SHA256 = (
    "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac"
)
EXPECTED_VARIABLE_COUNT = 18_381
EXPECTED_CLAUSE_COUNT = 114_742
ANCHOR_CLAUSE_START = 6_952
CONNECTED_CLAUSE_START = 6_958
SORTER_CLAUSE_START = 114_637


def parse_dimacs(payload: bytes) -> tuple[int, list[tuple[int, ...]]]:
    lines = payload.decode("ascii").splitlines()
    header = lines[0].split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise AssertionError("malformed DIMACS header")
    variable_count, declared_clause_count = map(int, header[2:])
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        tokens = tuple(map(int, line.split()))
        if not tokens or tokens[-1] != 0 or 0 in tokens[:-1]:
            raise AssertionError("malformed DIMACS clause")
        clauses.append(tokens[:-1])
    if len(clauses) != declared_clause_count:
        raise AssertionError("DIMACS clause count differs")
    return variable_count, clauses


def edge_variables() -> dict[tuple[int, int], int]:
    return {
        pair: index
        for index, pair in enumerate(combinations(range(12), 2), start=1)
    }


def clause_satisfied(
    clause: tuple[int, ...], assignment: dict[int, bool]
) -> bool:
    return any(
        assignment[abs(literal)] == (literal > 0) for literal in clause
    )


def main() -> None:
    payload = CNF_PATH.read_bytes()
    if sha256(payload).hexdigest() != EXPECTED_CNF_SHA256:
        raise AssertionError("frozen parent hash differs")
    variable_count, clauses = parse_dimacs(payload)
    if (
        variable_count != EXPECTED_VARIABLE_COUNT
        or len(clauses) != EXPECTED_CLAUSE_COUNT
    ):
        raise AssertionError("frozen parent census differs")

    edge = edge_variables()
    cube_variables = tuple(edge[(anchor, 4)] for anchor in range(4))
    if cube_variables != (4, 14, 23, 31):
        raise AssertionError("cube-variable direction or allocation differs")

    expected_anchor_units = tuple(
        (edge[pair],) for pair in combinations(range(4), 2)
    )
    observed_anchor_units = tuple(
        clauses[ANCHOR_CLAUSE_START:CONNECTED_CLAUSE_START]
    )
    if observed_anchor_units != expected_anchor_units:
        raise AssertionError("anchored H-clique units differ")

    singleton_zero_cut = tuple(-edge[(0, vertex)] for vertex in range(1, 12))
    if clauses[CONNECTED_CLAUSE_START] != singleton_zero_cut:
        raise AssertionError("the connected-G singleton cut for vertex 0 differs")

    sorter = clauses[SORTER_CLAUSE_START:]
    if len(sorter) != 105:
        raise AssertionError("outer-signature sorter clause count differs")
    comparator_truth_rows = 0
    for offset, (left, right) in enumerate(zip(range(4, 11), range(5, 12))):
        comparator = sorter[15 * offset : 15 * (offset + 1)]
        allowed_variables = {
            edge[(anchor, vertex)]
            for anchor in range(4)
            for vertex in (left, right)
        }
        if any(
            abs(literal) not in allowed_variables
            for clause in comparator
            for literal in clause
        ):
            raise AssertionError("sorter comparator escapes its two signatures")
        for left_bits in product((0, 1), repeat=4):
            for right_bits in product((0, 1), repeat=4):
                assignment = {
                    edge[(anchor, left)]: bool(left_bits[anchor])
                    for anchor in range(4)
                }
                assignment.update(
                    {
                        edge[(anchor, right)]: bool(right_bits[anchor])
                        for anchor in range(4)
                    }
                )
                observed = all(
                    clause_satisfied(clause, assignment)
                    for clause in comparator
                )
                expected = left_bits <= right_bits
                if observed != expected:
                    raise AssertionError(
                        "sorter truth table differs from nondecreasing lex order"
                    )
                comparator_truth_rows += 1

    sequence_count = 0
    singleton_cut_compatible_count = 0
    excluded_all_first_bit_one_count = 0
    for signatures in combinations_with_replacement(range(16), 8):
        sequence_count += 1
        singleton_cut_compatible = any(signature < 8 for signature in signatures)
        if singleton_cut_compatible:
            singleton_cut_compatible_count += 1
            if signatures[0] >= 8:
                raise AssertionError(
                    "connected singleton cut permits a first-one minimum"
                )
        else:
            excluded_all_first_bit_one_count += 1
            if signatures[0] < 8:
                raise AssertionError("signature classification is inconsistent")

    surviving_cubes = [
        "".join(map(str, bits))
        for bits in product((0, 1), repeat=4)
        if bits[0] == 0
    ]
    if surviving_cubes != [
        "0000",
        "0001",
        "0010",
        "0011",
        "0100",
        "0101",
        "0110",
        "0111",
    ]:
        raise AssertionError("eight-cube list differs")

    report = {
        "schema": "gamma-theta-order12-k4-minimum-signature-hostile-probe-v1",
        "status": "PASS_EXACT_LOGICAL_REDUCTION_ONLY",
        "claim_boundary": (
            "This verifies the minimum-signature implication and eight-cube "
            "list only; it is not an aggregate UNSAT or mathematical-slice claim."
        ),
        "parent_cnf_sha256": EXPECTED_CNF_SHA256,
        "note_sha256": sha256(NOTE_PATH.read_bytes()).hexdigest(),
        "cube_variables": list(cube_variables),
        "comparator_count": 7,
        "comparator_truth_rows_checked": comparator_truth_rows,
        "nondecreasing_signature_sequences_checked": sequence_count,
        "singleton_cut_compatible_sequences": singleton_cut_compatible_count,
        "all_first_bit_one_sequences_excluded": (
            excluded_all_first_bit_one_count
        ),
        "surviving_cube_ids": surviving_cubes,
    }
    print(json.dumps(report, allow_nan=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
