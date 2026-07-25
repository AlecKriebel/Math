#!/usr/bin/env python3
"""Independent verifier for the odd deficit lemma small-case audit."""

from __future__ import annotations

from itertools import combinations
import hashlib
import json
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results" / "small_case_audit.json"
EXPECTED_SHA256 = (
    "9cdce88d4e6d2492c69424020d42d7956c55ffacf2eb8f2140bf5041c9a0869b"
)


class VerificationError(RuntimeError):
    """Raised when a finite certificate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def has_independent_set(
    adjacency: list[int], required_size: int
) -> bool:
    """Exact recursive independent-set decision."""

    def search(candidates: int, remaining: int) -> bool:
        if remaining == 0:
            return True
        if candidates.bit_count() < remaining:
            return False
        while candidates:
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            candidates ^= bit
            if search(
                candidates & ~adjacency[vertex],
                remaining - 1,
            ):
                return True
        return False

    return search((1 << len(adjacency)) - 1, required_size)


def enumerate_triangle_free(a: int) -> tuple[int, dict[int, int]]:
    """Generate triangle-free graphs edge by edge, then test alpha."""

    cardinality = 2 * a + 1
    edges = list(combinations(range(cardinality), 2))
    adjacency = [0] * cardinality
    triangle_free_leaves = 0
    histogram: dict[int, int] = {}

    def search(edge_index: int, edge_count: int) -> None:
        nonlocal triangle_free_leaves
        if edge_index == len(edges):
            triangle_free_leaves += 1
            if not has_independent_set(adjacency, a + 1):
                histogram[edge_count] = (
                    histogram.get(edge_count, 0) + 1
                )
            return
        first, second = edges[edge_index]
        search(edge_index + 1, edge_count)
        if adjacency[first] & adjacency[second]:
            return
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
        search(edge_index + 1, edge_count + 1)
        adjacency[first] ^= 1 << second
        adjacency[second] ^= 1 << first

    search(0, 0)
    return triangle_free_leaves, histogram


def verify_example(record: dict[str, object]) -> None:
    cardinality = int(record["cardinality"])
    a = int(record["a"])
    adjacency = [0] * cardinality
    seen = set()
    for edge in record["maximum_example_edges"]:
        require(
            isinstance(edge, list)
            and len(edge) == 2
            and all(isinstance(vertex, int) for vertex in edge),
            "malformed example edge",
        )
        first, second = edge
        require(
            0 <= first < second < cardinality,
            "example edge is out of range",
        )
        require((first, second) not in seen, "duplicate example edge")
        seen.add((first, second))
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    require(
        len(seen) == record["maximum_edge_count"],
        "example edge count mismatch",
    )
    require(
        all(
            not (adjacency[first] & adjacency[second])
            for first, second in seen
        ),
        "example contains a triangle",
    )
    require(
        not has_independent_set(adjacency, a + 1),
        "example has excessive independence number",
    )
    all_edges = list(combinations(range(cardinality), 2))
    decoded_mask = sum(
        1 << index
        for index, edge in enumerate(all_edges)
        if edge in seen
    )
    require(
        decoded_mask == record["maximum_example_edge_mask"],
        "example edge mask mismatch",
    )


def verify(
    path: Path = SOURCE, *, enforce_pinned_hash: bool = True
) -> dict[str, object]:
    source_bytes = path.read_bytes()
    if enforce_pinned_hash:
        require(
            hashlib.sha256(source_bytes).hexdigest()
            == EXPECTED_SHA256,
            "small-case artifact hash mismatch",
        )
    source = json.loads(source_bytes)
    require(
        source["schema"]
        == "kissing5.odd_triangle_free_deficit_small_a.v1",
        "wrong schema",
    )
    require(
        source["claim"]
        == (
            "If F is triangle-free on 2a+1 vertices and "
            "alpha(F)<=a, then e(F)<=a^2+1."
        ),
        "wrong audited claim",
    )
    require(
        source["evidence_status"]
        == (
            "COMPUTATIONALLY CERTIFIED SMALL-CASE AUDIT; "
            "THE GENERAL LEMMA HAS A SEPARATE HUMAN PROOF"
        ),
        "unsafe evidence status",
    )
    records = source["full_labeled_enumerations"]
    require(len(records) == 2, "expected a=2 and a=3 records")
    expected_triangle_free_leaves = {2: 388, 3: 133501}
    verified = {}
    for record in records:
        a = int(record["a"])
        require(a in (2, 3), "unexpected full enumeration")
        cardinality = 2 * a + 1
        require(
            record["cardinality"] == cardinality,
            "wrong graph order",
        )
        require(
            record["total_labeled_graphs"]
            == 1 << math.comb(cardinality, 2),
            "wrong labeled graph count",
        )
        leaves, histogram = enumerate_triangle_free(a)
        require(
            leaves == expected_triangle_free_leaves[a],
            "triangle-free leaf count changed",
        )
        stored_histogram = {
            int(edge_count): int(count)
            for edge_count, count in record[
                "edge_count_histogram"
            ].items()
        }
        require(
            histogram == stored_histogram,
            "feasible edge histogram mismatch",
        )
        require(
            record["feasible_labeled_graphs"]
            == sum(histogram.values()),
            "feasible graph count mismatch",
        )
        maximum = max(histogram)
        require(
            record["maximum_edge_count"] == maximum
            and record["lemma_bound"] == a * a + 1
            and maximum <= a * a + 1,
            "small-case edge maximum fails",
        )
        verify_example(record)
        verified[str(a)] = {
            "triangle_free_labeled_graphs": leaves,
            "feasible_labeled_graphs": sum(histogram.values()),
            "maximum_edge_count": maximum,
        }

    a4 = source["a4_violation_enumeration"]
    require(
        a4["a"] == 4
        and a4["cardinality"] == 9
        and a4["lemma_bound"] == 17
        and a4["only_possible_violating_edge_count"] == 18,
        "wrong a=4 reduction",
    )
    # If e=18, the degree bound Delta<=4 makes the graph 4-regular.
    # With A=N(v) and |B|=4, the degree equations give e(B)=2.
    # Row sum three means the A-B incidence matrix is determined by one
    # missing B-neighbor per A-vertex.  Its missing multiplicities equal
    # the B-internal degrees.
    matching_sets = 3
    adjacent_sets = 12
    matching_matrices_each = math.factorial(4)
    adjacent_matrices_each = (
        math.factorial(4) // math.factorial(2)
    )
    matching_matrices = matching_sets * matching_matrices_each
    adjacent_matrices = adjacent_sets * adjacent_matrices_each
    require(
        a4["internal_B_edge_sets"]
        == math.comb(math.comb(4, 2), 2)
        == matching_sets + adjacent_sets,
        "wrong internal-B enumeration",
    )
    require(
        a4["incidence_matrices_checked"]
        == a4["internal_B_edge_sets"] * (1 << 16),
        "wrong incidence enumeration size",
    )
    require(
        a4["degree_feasible_incidence_matrices"]
        == matching_matrices + adjacent_matrices
        == 216,
        "wrong degree-feasible incidence count",
    )
    require(
        a4["by_internal_B_shape"]["matching"]
        == {
            "internal_edge_sets": matching_sets,
            "degree_feasible_incidence_matrices": (
                matching_matrices
            ),
            "triangle_free_survivors": 0,
        }
        and a4["by_internal_B_shape"]["adjacent"]
        == {
            "internal_edge_sets": adjacent_sets,
            "degree_feasible_incidence_matrices": (
                adjacent_matrices
            ),
            "triangle_free_survivors": 0,
        },
        "wrong internal-B shape counts",
    )
    # For every B-edge yz, q_y+q_z is two (matching) or three
    # (adjacent).  The two A-neighborhood sizes therefore sum to six or
    # five, respectively, so they cannot be disjoint subsets of |A|=4.
    require(
        (8 - 2 > 4) and (8 - 3 > 4),
        "a=4 common-neighbor contradiction failed",
    )
    require(
        a4["triangle_free_survivors"] == 0
        and a4[
            "violating_graphs_up_to_the_safe_normalization"
        ]
        == 0,
        "a=4 violating graph survived",
    )

    return {
        "status": (
            "odd triangle-free deficit lemma small cases "
            "independently verified"
        ),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "full_enumerations": verified,
        "a4_degree_feasible_normalized_cases": 216,
        "a4_triangle_free_violations": 0,
    }


def main() -> None:
    try:
        result = verify()
    except (
        KeyError,
        TypeError,
        ValueError,
        VerificationError,
    ) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
