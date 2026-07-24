#!/usr/bin/env python3
"""Tests for the exact order-43 min/max-degree cover."""

from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from global_minmax_degree_cover import (  # noqa: E402
    BRANCH_DEGREES,
    ORDER,
    additional_degree_units,
    branch_units,
    complement,
    graph_degrees,
    minmax_parameter,
    normalize,
    star_units,
)


def circulant(offsets: set[int]) -> list[int]:
    adjacency = [0] * ORDER
    for left in range(ORDER):
        for offset in offsets:
            right = (left + offset) % ORDER
            if left != right:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return adjacency


class GlobalMinmaxDegreeCoverTests(unittest.TestCase):
    def test_exact_unit_counts_and_disjointness(self) -> None:
        self.assertEqual(tuple(map(len, map(star_units, BRANCH_DEGREES))), (42, 42, 42))
        self.assertEqual(
            tuple(map(len, map(additional_degree_units, BRANCH_DEGREES))),
            (0, 86, 86),
        )
        self.assertEqual(
            tuple(map(len, map(branch_units, BRANCH_DEGREES))),
            (42, 128, 128),
        )
        for degree in BRANCH_DEGREES:
            units = branch_units(degree)
            self.assertEqual(len(set(map(abs, units))), len(units))

    def test_threshold_units_accept_exact_degree_interval(self) -> None:
        # A forward threshold variable t_k is forced true whenever the input
        # count reaches k.  Its negative unit therefore accepts count < k;
        # canonical threshold witnesses prove completeness in the other
        # direction.
        for degree in BRANCH_DEGREES:
            threshold = ORDER - degree
            for observed in range(ORDER):
                base = 18 <= observed <= 24
                narrowed = (
                    True
                    if degree == 18
                    else observed < threshold
                    and (ORDER - 1 - observed) < threshold
                )
                self.assertEqual(
                    base and narrowed,
                    degree <= observed <= ORDER - 1 - degree,
                )

    def test_normalizes_representatives_of_all_three_branches(self) -> None:
        degree18 = circulant(set(range(1, 10)))
        degree20 = circulant(set(range(1, 11)))

        # Remove a matching of 21 edges from a 20-regular graph.  This gives
        # 42 vertices of degree 19 and one of degree 20.
        degree19 = list(degree20)
        vertices = list(range(42))
        random.Random(20260723).shuffle(vertices)
        matching: list[tuple[int, int]] = []
        unused = set(vertices)
        while unused:
            left = min(unused)
            unused.remove(left)
            right = next(
                candidate
                for candidate in sorted(unused)
                if (degree19[left] >> candidate) & 1
            )
            unused.remove(right)
            matching.append((left, right))
        for left, right in matching:
            degree19[left] &= ~(1 << right)
            degree19[right] &= ~(1 << left)

        for expected, graph in ((18, degree18), (19, degree19), (20, degree20)):
            normalized, _complemented, branch = normalize(graph)
            self.assertEqual(branch, expected)
            degrees = graph_degrees(normalized)
            self.assertEqual(degrees[0], expected)
            self.assertTrue(
                all(expected <= value <= ORDER - 1 - expected for value in degrees)
            )
            self.assertEqual(
                [
                    vertex
                    for vertex in range(1, ORDER)
                    if (normalized[0] >> vertex) & 1
                ],
                list(range(1, expected + 1)),
            )

    def test_complement_orientation(self) -> None:
        degree18 = circulant(set(range(1, 10)))
        normalized, complemented, branch = normalize(complement(degree18))
        self.assertTrue(complemented)
        self.assertEqual(branch, 18)
        self.assertEqual(min(graph_degrees(normalized)), 18)

    def test_degree_pair_cover_and_parity(self) -> None:
        parity_pairs: list[tuple[int, int]] = []
        for minimum in range(18, 25):
            for maximum in range(minimum, 25):
                parameter = min(minimum, 42 - maximum)
                if parameter == 21:
                    parity_pairs.append((minimum, maximum))
                else:
                    self.assertIn(parameter, BRANCH_DEGREES)
        self.assertEqual(parity_pairs, [(21, 21)])
        self.assertEqual(43 * 21 % 2, 1)

    def test_minmax_parameter(self) -> None:
        self.assertEqual(minmax_parameter([18] + [24] * 42), 18)
        self.assertEqual(minmax_parameter([19] + [23] * 42), 19)
        self.assertEqual(minmax_parameter([20] + [22] * 42), 20)
        self.assertEqual(minmax_parameter([21] * 43), 21)


if __name__ == "__main__":
    unittest.main()
