#!/usr/bin/env python3
"""Independent fusion-graph cross-check of the H_n(3,6) arithmetic.

Unlike hecke_multiplicity_spectrum.py, this verifier does not enumerate
Young diagrams or add boxes.  It uses an explicit ten-vertex SU(3)_3 fusion
graph for tensoring with the two-dimensional generating object.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction


# Vertices are SU(3)_3 highest weights (a,b), a+b <= 3.
# The adjacency lists are written explicitly rather than generated from
# partition arithmetic.
FUSION_BY_X = {
    (0, 0): ((1, 0),),
    (1, 0): ((2, 0), (0, 1)),
    (0, 1): ((1, 1), (0, 0)),
    (2, 0): ((3, 0), (1, 1)),
    (1, 1): ((2, 1), (0, 2), (1, 0)),
    (0, 2): ((1, 2), (0, 1)),
    (3, 0): ((2, 1),),
    (2, 1): ((1, 2), (2, 0)),
    (1, 2): ((0, 3), (1, 1)),
    (0, 3): ((0, 2),),
}

DIMENSION = {
    (0, 0): 1,
    (1, 0): 2,
    (0, 1): 2,
    (2, 0): 2,
    (1, 1): 3,
    (0, 2): 2,
    (3, 0): 1,
    (2, 1): 2,
    (1, 2): 2,
    (0, 3): 1,
}


def next_paths(paths: dict[tuple[int, int], int]) -> dict[tuple[int, int], int]:
    following: dict[tuple[int, int], int] = defaultdict(int)
    for vertex, count in paths.items():
        for successor in FUSION_BY_X[vertex]:
            following[successor] += count
    return dict(following)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-strand", type=int, default=60)
    parser.add_argument("--test-d-through", type=int, default=100)
    args = parser.parse_args()

    for vertex, successors in FUSION_BY_X.items():
        assert sum(DIMENSION[x] for x in successors) == 2 * DIMENSION[vertex]
    print("[ok] explicit ten-vertex fusion matrix has PF eigenvector D and eigenvalue 2")

    paths = {(0, 0): 1}
    active_dimensions: dict[int, set[int]] = {}
    for strand in range(args.max_strand + 1):
        active_dimensions[strand] = {
            DIMENSION[vertex] for vertex in paths
        }
        categorical_dimension = sum(
            count * DIMENSION[vertex]
            for vertex, count in paths.items()
        )
        assert categorical_dimension == 2**strand

        central_trace = sum(
            Fraction(count * DIMENSION[vertex], 2**strand)
            for vertex, count in paths.items()
        )
        assert central_trace == 1

        for local_dimension in (2, 4, 6):
            represented_dimension = sum(
                count
                * Fraction(
                    DIMENSION[vertex] * local_dimension**strand,
                    2**strand,
                )
                for vertex, count in paths.items()
            )
            assert represented_dimension == local_dimension**strand

        if strand <= 9:
            display = ", ".join(
                f"{vertex}:{count}"
                for vertex, count in sorted(paths.items())
            )
            print(f"n={strand}: {display}")

        paths = next_paths(paths)

    survivors = []
    for local_dimension in range(1, args.test_d_through + 1):
        integral = True
        for strand in range(2, args.max_strand + 1):
            for quantum_dimension in active_dimensions[strand]:
                multiplicity = Fraction(
                    quantum_dimension * local_dimension**strand,
                    2**strand,
                )
                if multiplicity.denominator != 1:
                    integral = False
                    break
            if not integral:
                break
        if integral:
            survivors.append(local_dimension)

    assert survivors == list(range(2, args.test_d_through + 1, 2))
    print(
        f"[ok] levels 0..{args.max_strand}: categorical and represented "
        "dimensions close exactly"
    )
    print(
        "[ok] multiplicity integrality through d="
        f"{args.test_d_through} holds exactly for even d"
    )


if __name__ == "__main__":
    main()
