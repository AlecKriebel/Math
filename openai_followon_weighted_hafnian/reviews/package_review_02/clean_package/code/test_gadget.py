"""Reproduce finite exact checks; run with `python3 code/test_gadget.py`.

This independently counts graph matchings by subset recursion; it does not use
the claimed gadget signature to obtain the observed graph counts.  Tests are
finite supporting evidence and cannot establish an approximation theorem.
"""

from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform
from random import Random
import time

from gadget import (count_perfect_matchings, dag_path_count,
                    enumerate_perfect_matchings, exact_hafnian,
                    expand_rational_matrix, gadget_signature, integer_gadget)


ROOT = Path(__file__).resolve().parents[1]


def matrix_from_edges(n, weights):
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for (i, j), weight in weights.items():
        matrix[i][j] = matrix[j][i] = Fraction(weight)
    return matrix


def check_matrix(matrix, label, detail=True):
    hafnian = exact_hafnian(matrix)
    expansion = expand_rational_matrix(matrix)
    observed = count_perfect_matchings(expansion.graph)
    expected = hafnian * expansion.denominator ** (len(matrix) // 2)
    assert expected.denominator == 1, (label, expected)
    assert observed == expected.numerator, (label, observed, expected)
    if not detail:
        return None
    return {"label": label, "original_order": len(matrix),
            "hafnian": str(hafnian), "denominator": str(expansion.denominator),
            "denominator_bit_length": expansion.denominator.bit_length(),
            "expanded_order": expansion.graph.order,
            "expanded_edges": len(expansion.graph.edges),
            "matching_count": str(observed),
            "scaled_hafnian": str(expected), "verified": True}


def run_checks():
    started = time.monotonic()
    signature_records = []
    for weight in range(1, 65):
        gadget = integer_gadget(weight)
        observed = gadget_signature(weight)
        assert observed == (weight, 1, 0, 0), (weight, observed)
        assert dag_path_count(gadget.dag) == weight
        bits = weight.bit_length()
        assert gadget.graph.order == 4 * bits - 2
        assert len(gadget.graph.edges) <= 6 * bits - 5
        signature_records.append({"weight": weight, "signature": list(observed),
                                  "vertices": gadget.graph.order,
                                  "edges": len(gadget.graph.edges)})

    pairs4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    exhaustive = 0
    for weights in product(range(3), repeat=len(pairs4)):
        check_matrix(matrix_from_edges(4, dict(zip(pairs4, weights))),
                     "exhaustive_K4", False)
        exhaustive += 1

    random = Random(20261006)
    pairs6 = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    for trial in range(40):
        weights = {pair: random.randrange(4) for pair in pairs6}
        check_matrix(matrix_from_edges(6, weights), f"seeded_K6_{trial}", False)

    boundary_cases = [
        ("empty_hafnian", []),
        ("zero_matrix_order_two", matrix_from_edges(2, {})),
        ("zero_matrix_order_four", matrix_from_edges(4, {})),
        ("star_has_no_perfect_matching", matrix_from_edges(
            4, {(0, 1): 2, (0, 2): 3, (0, 3): 1})),
        ("disconnected_positive", matrix_from_edges(
            4, {(0, 1): 2, (2, 3): 3})),
        ("disconnected_two_odd_components", matrix_from_edges(
            6, {(0, 1): 2, (1, 2): 1, (0, 2): 3,
                (3, 4): 2, (4, 5): 1, (3, 5): 3})),
        ("below_one_and_zero_edges", matrix_from_edges(
            4, {(0, 1): Fraction(1, 2), (0, 3): Fraction(2, 3),
                (1, 2): Fraction(3, 4), (1, 3): Fraction(5, 6)})),
        ("rational_complete_order_four", matrix_from_edges(
            4, dict(zip(pairs4, [Fraction(1, 2), Fraction(1, 3),
                                Fraction(1, 2), Fraction(2, 3),
                                Fraction(1, 3), Fraction(3, 2)])))),
        ("extremely_small_positive", matrix_from_edges(
            2, {(0, 1): Fraction(1, 2**512)})),
        ("large_numerator", matrix_from_edges(
            2, {(0, 1): 2**256 + 1})),
        ("large_different_denominators_disconnected", matrix_from_edges(
            4, {(0, 1): Fraction(1, 2**256 + 1),
                (2, 3): Fraction(1, 2**127 + 1)})),
    ]
    diagonal = matrix_from_edges(2, {(0, 1): Fraction(3, 7)})
    diagonal[0][0], diagonal[1][1] = -1000, 999
    boundary_cases.append(("diagonal_irrelevant", diagonal))
    boundaries = [check_matrix(matrix, label) for label, matrix in boundary_cases]

    # Check the *full* pushforward and each fiber, not just their sum.
    projection_weights = dict(zip(pairs4, [2, 3, 1, 2, 1, 1]))
    projection_matrix = matrix_from_edges(4, projection_weights)
    expansion = expand_rational_matrix(projection_matrix)
    fibers = Counter(expansion.project(matching) for matching in
                     enumerate_perfect_matchings(expansion.graph))
    from gadget import Graph
    original_graph = Graph(4, tuple(sorted(projection_weights)))
    fiber_records = []
    for matching in enumerate_perfect_matchings(original_graph):
        matching = tuple(sorted(matching))
        expected = 1
        for edge in matching:
            expected *= projection_weights[edge]
        assert fibers[matching] == expected, (matching, fibers[matching], expected)
        fiber_records.append({"matching": [list(e) for e in matching],
                              "observed_fiber": fibers[matching],
                              "expected_product": expected})
    assert sum(fibers.values()) == exact_hafnian(projection_matrix)
    assert set(fibers) == {tuple(sorted(m)) for m in
                          enumerate_perfect_matchings(original_graph)}

    # Invalid domains must be rejected, rather than silently broadened.
    invalid_cases = [[[0]], [[0, -1], [-1, 0]], [[0, 1], [2, 0]],
                     [[0, 0.5], [0.5, 0]], [[0, 1], [1]]]
    for matrix in invalid_cases:
        try:
            expand_rational_matrix(matrix)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid matrix accepted")
    for weight in (0, -1, Fraction(1, 2)):
        try:
            integer_gadget(weight)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid integer weight accepted")

    return {"status": "all finite exact checks passed",
            "evidence_scope": "Finite checks support the exact reduction only; "
                              "they neither prove it nor certify any upstream FPRAS.",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python_version": platform.python_version(),
            "elapsed_seconds": time.monotonic() - started,
            "source_sha256": {name: sha256((ROOT / "code" / name).read_bytes()).hexdigest()
                              for name in ("gadget.py", "test_gadget.py")},
            "signature_tests": signature_records,
            "exhaustive_integer_K4_tests": {"weight_domain": [0, 1, 2],
                                            "number_of_cases": exhaustive},
            "seeded_integer_K6_tests": {"seed": 20261006, "number_of_cases": 40,
                                        "weight_domain": [0, 1, 2, 3]},
            "boundary_tests": boundaries,
            "projection_fiber_tests": fiber_records,
            "domain_rejection_tests": len(invalid_cases) + 3}


if __name__ == "__main__":
    report = run_checks()
    destination = ROOT / "data" / "gadget_verification.json"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(report["status"])
    print(f"64 signatures; 729 exhaustive K4; 40 seeded K6; "
          f"{len(report['boundary_tests'])} boundary cases; 3 full projection fibers.")
    print(f"Exact reference enumeration took {report['elapsed_seconds']:.3f} seconds.")
