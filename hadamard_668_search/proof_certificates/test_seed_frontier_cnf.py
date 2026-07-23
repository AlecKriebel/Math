#!/usr/bin/env python3
"""Small exhaustive regressions for the proof CNF's derived constraints."""

from __future__ import annotations

import itertools
import unittest

try:
    from .export_seed_frontier_cnf import (
        CNF,
        EXCHANGEABLE_QUAD_COMPARISONS,
        EXCHANGEABLE_QUAD_PARTITION,
        _add_four_bit_mask_order,
    )
except ImportError:
    from export_seed_frontier_cnf import (
        CNF,
        EXCHANGEABLE_QUAD_COMPARISONS,
        EXCHANGEABLE_QUAD_PARTITION,
        _add_four_bit_mask_order,
    )

from verify_variable_q_seed_radius import SEED


class DirectionBudgetTests(unittest.TestCase):
    def test_wrong_direction_identity_exhaustively(self) -> None:
        for length in range(1, 7):
            for seed in itertools.product((-1, 1), repeat=length):
                before = sum(seed)
                for mask in range(1 << length):
                    flipped = tuple(bool(mask >> index & 1) for index in range(length))
                    after = sum(
                        -value if flip else value
                        for value, flip in zip(seed, flipped, strict=True)
                    )
                    delta = (after - before) // 2
                    plus_flips = sum(
                        flip and value == 1
                        for value, flip in zip(seed, flipped, strict=True)
                    )
                    minus_flips = sum(
                        flip and value == -1
                        for value, flip in zip(seed, flipped, strict=True)
                    )
                    wrong = plus_flips if delta >= 0 else minus_flips
                    self.assertEqual(
                        sum(flipped), abs(delta) + 2 * wrong
                    )
                    if delta >= 0:
                        self.assertEqual(minus_flips, delta + wrong)
                    else:
                        self.assertEqual(plus_flips, -delta + wrong)


class PairDistanceTests(unittest.TestCase):
    def test_quad_dp_lower_bounds_match_brute_force(self) -> None:
        from verify_variable_q_seed_quad_radius import (
            quad_preserving_distances,
        )

        first = (1, -1, 1, 1)
        second = (-1, 1, 1, -1)
        radius = 8
        dynamic = quad_preserving_distances(first, second, radius)
        brute: dict[tuple[int, int, int, int], int] = {}
        # Two endpoint quads, each containing two entries from each sequence.
        quad_cells = (
            ((0, 0), (0, 3), (1, 0), (1, 3)),
            ((0, 1), (0, 2), (1, 1), (1, 2)),
        )
        sequence_pair = (first, second)
        for mask in range(1 << 8):
            if any(
                sum(bool(mask >> (quad * 4 + cell) & 1) for cell in range(4))
                % 2
                for quad in range(2)
            ):
                continue
            delta = [0, 0, 0, 0]
            cost = 0
            for quad, cells in enumerate(quad_cells):
                for cell, (sequence_index, coordinate) in enumerate(cells):
                    if not (mask >> (quad * 4 + cell) & 1):
                        continue
                    cost += 1
                    coordinate_class = 2 * sequence_index + coordinate % 2
                    delta[coordinate_class] -= sequence_pair[sequence_index][
                        coordinate
                    ]
            key = tuple(delta)
            brute[key] = min(cost, brute.get(key, cost))
        self.assertEqual(dynamic, brute)


class OrbitOrderTests(unittest.TestCase):
    def test_four_bit_order_clauses_are_exact(self) -> None:
        cnf = CNF()
        earlier = tuple(cnf.new_var(f"earlier_{index}") for index in range(4))
        later = tuple(cnf.new_var(f"later_{index}") for index in range(4))
        cnf.start_section("test")
        _add_four_bit_mask_order(cnf, earlier, later)
        self.assertEqual(len(cnf.clauses), 120)
        for earlier_mask in range(16):
            for later_mask in range(16):
                assignment = {
                    variable: bool(earlier_mask >> bit & 1)
                    for bit, variable in enumerate(earlier)
                }
                assignment.update(
                    {
                        variable: bool(later_mask >> bit & 1)
                        for bit, variable in enumerate(later)
                    }
                )
                satisfied = all(
                    any(
                        assignment[abs(literal)] == (literal > 0)
                        for literal in clause
                    )
                    for clause in cnf.clauses
                )
                self.assertEqual(
                    satisfied,
                    earlier_mask <= later_mask,
                    (earlier_mask, later_mask),
                )


class GlobalOrbitGroupingTests(unittest.TestCase):
    """Audit the declared global grouping without its modulo-12 key."""

    ROOT_PATTERNS = {
        3: ((1, 0, -1), (0, 1, -1)),
        4: ((1, 0, -1, 0), (0, 1, 0, -1)),
        6: ((1, 0, -1, -1, 0, 1), (0, 1, 1, 0, -1, -1)),
    }
    EVEN_MASKS = tuple(mask for mask in range(16) if mask.bit_count() % 2 == 0)

    @staticmethod
    def _physical_quads():
        result = []
        for first_index, second_index in ((0, 1), (2, 3)):
            length = len(SEED[first_index])
            for left in range(length // 2):
                right = length - 1 - left
                result.append(
                    (
                        (first_index, left),
                        (first_index, right),
                        (second_index, left),
                        (second_index, right),
                    )
                )
        return tuple(result)

    @classmethod
    def _observable_contribution(cls, quad, mask):
        distance = mask.bit_count()
        class_margin_delta = [0] * 8
        # For every sequence/parity class, retain separate counts of flips
        # from seed +1 and seed -1.  These determine every target-dependent
        # wrong-direction count used by the exporter.
        direction_counts = [0] * 16
        pair_distance = [0, 0]
        root_deltas = {
            (modulus, sequence_index, form): 0
            for modulus in (3, 4, 6)
            for sequence_index in range(4)
            for form in (0, 1)
        }
        for cell, (sequence_index, coordinate) in enumerate(quad):
            if not (mask >> cell & 1):
                continue
            seed_value = SEED[sequence_index][coordinate]
            class_index = 2 * sequence_index + coordinate % 2
            class_margin_delta[class_index] -= 2 * seed_value
            sign_slot = 0 if seed_value == 1 else 1
            direction_counts[2 * class_index + sign_slot] += 1
            pair_distance[0 if sequence_index < 2 else 1] += 1
            for modulus, patterns in cls.ROOT_PATTERNS.items():
                for form, pattern in enumerate(patterns):
                    root_deltas[(modulus, sequence_index, form)] += (
                        -2 * seed_value * pattern[coordinate % modulus]
                    )
        ordered_roots = tuple(
            root_deltas[(modulus, sequence_index, form)]
            for modulus in (3, 4, 6)
            for sequence_index in range(4)
            for form in (0, 1)
        )
        return (
            distance,
            *class_margin_delta,
            *direction_counts,
            *pair_distance,
            *ordered_roots,
        )

    @staticmethod
    def _components_from_comparisons(quads):
        parent = {quad: quad for quad in quads}

        def find(quad):
            while parent[quad] != quad:
                parent[quad] = parent[parent[quad]]
                quad = parent[quad]
            return quad

        def union(left, right):
            left_root = find(left)
            right_root = find(right)
            if left_root == right_root:
                raise AssertionError("declared comparison graph contains a cycle")
            parent[right_root] = left_root

        for earlier, later in EXCHANGEABLE_QUAD_COMPARISONS:
            if earlier not in parent or later not in parent:
                raise AssertionError("declared comparison contains a foreign quad")
            union(earlier, later)
        groups = {}
        for quad in quads:
            groups.setdefault(find(quad), set()).add(quad)
        return {frozenset(group) for group in groups.values()}

    def test_declared_orbits_match_complete_root_observables(self) -> None:
        quads = self._physical_quads()
        self.assertEqual(len(quads), 83)
        self.assertEqual(len(set(quads)), 83)

        independently_grouped = {}
        for quad in quads:
            signature = tuple(
                self._observable_contribution(quad, mask)
                for mask in self.EVEN_MASKS
            )
            independently_grouped.setdefault(signature, set()).add(quad)
        independent_partition = {
            frozenset(group) for group in independently_grouped.values()
        }

        declared_partition = {
            frozenset(orbit) for orbit in EXCHANGEABLE_QUAD_PARTITION
        }
        self.assertEqual(
            sum(map(len, declared_partition)),
            83,
            "declared orbit partition omits or duplicates endpoint quads",
        )
        self.assertEqual(declared_partition, independent_partition)

        comparison_partition = self._components_from_comparisons(quads)
        self.assertEqual(comparison_partition, declared_partition)
        self.assertEqual(
            len(EXCHANGEABLE_QUAD_COMPARISONS),
            sum(len(orbit) - 1 for orbit in declared_partition),
        )

        for orbit in declared_partition:
            for mask in self.EVEN_MASKS:
                contributions = {
                    self._observable_contribution(quad, mask)
                    for quad in orbit
                }
                self.assertEqual(
                    len(contributions),
                    1,
                    f"mask {mask} changes root observables inside an orbit",
                )


if __name__ == "__main__":
    unittest.main()
