#!/usr/bin/env python3
"""Exact audit of the first nonlocal paired-forest exchange unit.

All calculations use ``Fraction`` arithmetic.  Enumeration is restricted to
the complete-K3 cycle mate and the weighted-P3 one/two-pivot obstruction.
The script verifies exact identities and refuted strengthenings, not PAPT.
"""

from __future__ import annotations

import itertools
import sys
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
CROSS_RULE = HERE.parent / "r2_cross_rule_sum"
sys.path.insert(0, str(CROSS_RULE))

from verify_cross_rule_tree_reduction import (  # noqa: E402
    conditional_tree_root_weights,
    db_generator,
    tree_cofactors,
    unbatched_generators,
)


def event_db(weights):
    generator = db_generator(weights)
    return [
        [value / F((row + 1).bit_count()) for value in line]
        for row, line in enumerate(generator)
    ]


def tree_root(edges, size):
    """Return the root of a directed in-tree, or ``None``."""

    sources = {source for source, _ in edges}
    roots = set(range(size)) - sources
    if len(edges) != size - 1 or len(roots) != 1:
        return None
    root = next(iter(roots))
    parent = dict(edges)
    if len(parent) != size - 1:
        return None
    for source in range(size):
        if source == root:
            continue
        seen = set()
        vertex = source
        while vertex != root:
            if vertex in seen or vertex not in parent:
                return None
            seen.add(vertex)
            vertex = parent[vertex]
    return root


def tree_weight(generator, edges):
    root = tree_root(edges, len(generator))
    if root is None:
        return F(0)
    answer = F(1)
    for source, target in edges:
        answer *= generator[source][target]
    return answer


def enumerate_trees(generator):
    size = len(generator)
    answer = []
    for root in range(size):
        vertices = [vertex for vertex in range(size) if vertex != root]
        choices = [
            [
                target
                for target in range(size)
                if target != source and generator[source][target]
            ]
            for source in vertices
        ]
        for targets in itertools.product(*choices):
            edges = frozenset(zip(vertices, targets))
            if tree_root(edges, size) != root:
                continue
            answer.append((root, edges, tree_weight(generator, edges)))
    return answer


def pivot_neighbours(generator, edges):
    """All arborescences differing in at most one directed edge."""

    size = len(generator)
    answer = {edges}
    for removed in edges:
        base = set(edges) - {removed}
        for source in range(size):
            for target in range(size):
                if source == target or not generator[source][target]:
                    continue
                candidate = frozenset(base | {(source, target)})
                if tree_root(candidate, size) is not None:
                    answer.add(candidate)
    return answer


def completion_class(trees, forest):
    return [tree for tree in trees if forest <= tree[1]]


def audit_complete_cycle_mate():
    complete = ((0, 1, 1), (1, 0, 1), (1, 1, 0))
    left, _ = unbatched_generators(complete)
    event = event_db(complete)

    # One reversible L skeleton has the complete conditional mean.  The same
    # is true for every supported skeleton, but one exact representative is
    # enough to audit the paired cancellation.
    left_skeleton_masks = ((1, 2), (1, 3), (1, 4), (1, 5), (2, 6), (3, 7))
    left_skeleton = tuple((a - 1, b - 1) for a, b in left_skeleton_masks)
    left_roots = conditional_tree_root_weights(left, left_skeleton)
    assert len(set(left_roots)) == 1
    left_mean = sum(
        ((root + 1).bit_count() * weight for root, weight in enumerate(left_roots)),
        F(0),
    ) / sum(left_roots, F(0))
    assert left_mean == F(12, 7)

    bad = frozenset(
        (a - 1, b - 1)
        for a, b in ((2, 1), (3, 1), (4, 1), (5, 1), (1, 6))
    )
    good = (bad - {(0, 5)}) | {(5, 2)}
    assert tree_root(bad, 6) == 5
    assert tree_root(good, 6) == 0
    assert tree_weight(event, bad) == tree_weight(event, good) == F(1, 972)
    assert bad in pivot_neighbours(event, good)
    assert good in pivot_neighbours(event, bad)

    b, d = F(12, 7), F(4, 3)
    assert b * d / 2 - left_mean == F(-4, 7)
    assert b * d - left_mean == F(4, 7)


def audit_path_pivot_radius_and_packets():
    path = ((0, 1, 2), (1, 0, 0), (2, 0, 0))
    left, _ = unbatched_generators(path)
    event = event_db(path)
    b, d = F(12, 7), F(4, 3)

    left_bad = frozenset(
        (a - 1, c - 1)
        for a, c in ((1, 2), (2, 3), (3, 6), (4, 1), (5, 6), (7, 3))
    )
    event_bad = frozenset(
        (a - 1, c - 1)
        for a, c in ((1, 6), (2, 1), (3, 6), (4, 1), (5, 6))
    )
    assert tree_root(left_bad, 7) == 5
    assert tree_root(event_bad, 6) == 5
    assert tree_weight(left, left_bad) == F(4, 27)
    assert tree_weight(event, event_bad) == F(3, 100)
    bad_cost = b * d / 2 - 2
    assert bad_cost == F(-6, 7)
    assert bad_cost * tree_weight(left, left_bad) * tree_weight(
        event, event_bad
    ) == F(-2, 525)

    left_neighbours = pivot_neighbours(left, left_bad)
    event_neighbours = pivot_neighbours(event, event_bad)
    left_ranks = {
        (tree_root(edges, 7) + 1).bit_count() for edges in left_neighbours
    }
    event_ranks = {
        (tree_root(edges, 6) + 1).bit_count() for edges in event_neighbours
    }
    assert left_ranks == {2, 3}
    assert event_ranks == {2}
    assert all(
        b * d / (tree_root(d_tree, 6) + 1).bit_count()
        - (tree_root(l_tree, 7) + 1).bit_count()
        < 0
        for l_tree in left_neighbours
        for d_tree in event_neighbours
    )

    middle = (event_bad - {(4, 5)}) | {(5, 4)}
    good = (middle - {(0, 5)}) | {(4, 0)}
    assert tree_root(middle, 6) == 4
    assert tree_root(good, 6) == 0
    assert middle in pivot_neighbours(event, event_bad)
    assert good in pivot_neighbours(event, middle)
    assert good not in pivot_neighbours(event, event_bad)
    assert tree_weight(event, middle) == F(3, 50)
    assert tree_weight(event, good) == F(1, 10)
    good_cost = b * d - 2
    assert good_cost == F(2, 7)
    good_mass = good_cost * tree_weight(left, left_bad) * tree_weight(event, good)
    assert good_mass == F(4, 945)
    assert good_mass / F(2, 525) == F(10, 9)

    left_trees = enumerate_trees(left)
    event_trees = enumerate_trees(event)
    assert len(left_trees) == 1176
    assert len(event_trees) == 57

    # Matrix-tree cofactors agree with direct arborescence enumeration.
    assert [
        sum((weight for root, _, weight in left_trees if root == state), F(0))
        for state in range(7)
    ] == tree_cofactors(left)
    assert [
        sum((weight for root, _, weight in event_trees if root == state), F(0))
        for state in range(6)
    ] == tree_cofactors(event)

    # The exact two-deletion identity: every N-state tree extends precisely
    # C(N-1,2) distinct three-component subforests.
    for trees, size in ((left_trees, 7), (event_trees, 6)):
        extension_count = defaultdict(int)
        for _, edges, _ in trees:
            for removed in itertools.combinations(edges, 2):
                extension_count[edges - frozenset(removed)] += 1
        left_side = sum(
            (
                sum(
                    weight
                    for _, edges, weight in trees
                    if forest <= edges
                )
                for forest in extension_count
            ),
            F(0),
        )
        right_side = F((size - 1) * (size - 2), 2) * sum(
            (weight for _, _, weight in trees), F(0)
        )
        assert left_side == right_side

    left_forest = left_bad - {(1, 2), (2, 5)}
    event_forest = event_bad - {(0, 5), (4, 5)}
    left_extensions = completion_class(left_trees, left_forest)
    event_extensions = completion_class(event_trees, event_forest)
    assert len(left_extensions) == 7
    assert len(event_extensions) == 6

    left_by_rank = {
        rank: sum(
            (
                weight
                for root, _, weight in left_extensions
                if (root + 1).bit_count() == rank
            ),
            F(0),
        )
        for rank in (1, 2, 3)
    }
    event_by_rank = {
        rank: sum(
            (
                weight
                for root, _, weight in event_extensions
                if (root + 1).bit_count() == rank
            ),
            F(0),
        )
        for rank in (1, 2)
    }
    assert left_by_rank == {1: F(80, 81), 2: F(32, 81), 3: F(0)}
    assert event_by_rank == {1: F(3, 20), 2: F(9, 50)}

    z_left = sum(left_by_rank.values(), F(0))
    y_left = sum((F(rank) * value for rank, value in left_by_rank.items()), F(0))
    theta = sum(event_by_rank.values(), F(0))
    phi = sum((value / rank for rank, value in event_by_rank.items()), F(0))
    assert (z_left, y_left, theta, phi) == (
        F(112, 81),
        F(16, 9),
        F(33, 100),
        F(6, 25),
    )
    assert b * d * z_left * phi - y_left * theta == F(116, 675)

    # Packetwise positivity is false even at the same D forest.
    negative_left_forest = left_bad - {(6, 2), (4, 5)}
    negative_left_extensions = completion_class(left_trees, negative_left_forest)
    negative_packet = sum(
        (
            left_weight
            * event_weight
            * (
                b * d / (event_root + 1).bit_count()
                - (left_root + 1).bit_count()
            )
            for left_root, _, left_weight in negative_left_extensions
            for event_root, _, event_weight in event_extensions
        ),
        F(0),
    )
    assert negative_packet == F(-362, 525)


def main():
    audit_complete_cycle_mate()
    audit_path_pivot_radius_and_packets()
    print("PASS: complete-K3 bad star has an exact weight-preserving cycle mate")
    print("REFUTED: one fundamental-cycle pivot in each paired tree on weighted P3")
    print("PASS: closest positive witness is a sharp two-pivot D exchange (ratio 10/9)")
    print("PASS: exact two-deletion identity and positive 42-atom completion packet")
    print("REFUTED: pointwise sign of three-component completion packets")
    print("OPEN: nonduplicating exchange between three-component forest pairs")


if __name__ == "__main__":
    main()
