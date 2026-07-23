"""Independent exhaustive 4x4 tests for alternating eight-cycle generation."""

from __future__ import annotations

import itertools
import unittest


SIZE = 4
CELLS = tuple(range(SIZE * SIZE))
ROW_CYCLES = ((0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3))


def cell(row: int, column: int) -> int:
    return SIZE * row + column


def connected(support: frozenset[int]) -> bool:
    neighbors = [set() for _ in range(2 * SIZE)]
    for entry in support:
        row, column = divmod(entry, SIZE)
        neighbors[row].add(SIZE + column)
        neighbors[SIZE + column].add(row)
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in neighbors[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    return len(reached) == 2 * SIZE


def brute_supports() -> set[frozenset[int]]:
    result: set[frozenset[int]] = set()
    for raw in itertools.combinations(CELLS, 2 * SIZE):
        support = frozenset(raw)
        if any(sum(cell(row, column) in support for column in range(SIZE)) != 2
               for row in range(SIZE)):
            continue
        if any(sum(cell(row, column) in support for row in range(SIZE)) != 2
               for column in range(SIZE)):
            continue
        if connected(support):
            result.add(support)
    return result


def canonical_descriptors() -> list[
    tuple[frozenset[int], int, int, tuple[int, ...]]
]:
    result = []
    for rows in ROW_CYCLES:
        for columns in itertools.permutations(range(SIZE)):
            positive = 0
            negative = 0
            vertex_pairs = []
            support = set()
            for edge in range(SIZE):
                next_edge = (edge + 1) % SIZE
                first = cell(rows[edge], columns[edge])
                second = cell(rows[next_edge], columns[edge])
                support.update((first, second))
                positive |= 1 << first
                negative |= 1 << second
            immutable = frozenset(support)
            for row in range(SIZE):
                vertex_pairs.append(sum(
                    1 << cell(row, column)
                    for column in range(SIZE)
                    if cell(row, column) in immutable
                ))
            for column in range(SIZE):
                vertex_pairs.append(sum(
                    1 << cell(row, column)
                    for row in range(SIZE)
                    if cell(row, column) in immutable
                ))
            result.append(
                (immutable, positive, negative, tuple(vertex_pairs))
            )
    return result


class EightCycleEnumerationTests(unittest.TestCase):
    def test_canonical_supports_equal_all_connected_two_regular_supports(
        self,
    ) -> None:
        descriptors = canonical_descriptors()
        canonical = [descriptor[0] for descriptor in descriptors]
        self.assertEqual(len(canonical), 72)
        self.assertEqual(len(set(canonical)), 72)
        self.assertEqual(set(canonical), brute_supports())

    def test_sign_orientation_buckets_are_exhaustive_for_all_signings(
        self,
    ) -> None:
        for support, positive, negative, vertex_pairs in canonical_descriptors():
            support_mask = sum(1 << entry for entry in support)
            for signing in range(1 << (SIZE * SIZE)):
                projected = signing & support_mask
                bucket_orientations = int(projected == positive) + int(
                    projected == negative
                )
                alternating = all(
                    signing & pair not in (0, pair) for pair in vertex_pairs
                )
                self.assertEqual(bucket_orientations, int(alternating))


if __name__ == "__main__":
    unittest.main()
