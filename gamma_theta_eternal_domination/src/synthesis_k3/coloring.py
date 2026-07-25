"""Independent exact coloring oracle used by the k=3 CEGAR loop."""

from __future__ import annotations

from typing import Iterable


def find_coloring(
    order: int,
    edges: Iterable[tuple[int, int]],
    color_count: int = 3,
) -> tuple[int, ...] | None:
    """Return a proper coloring, or ``None`` after complete DSATUR search."""

    if type(order) is not int or order < 0:
        raise ValueError("order must be a nonnegative integer")
    if type(color_count) is not int or color_count < 1:
        raise ValueError("color_count must be a positive integer")

    adjacency = [0] * order
    for raw_first, raw_second in edges:
        if (
            type(raw_first) is not int
            or type(raw_second) is not int
            or not 0 <= raw_first < order
            or not 0 <= raw_second < order
            or raw_first == raw_second
        ):
            raise ValueError("malformed simple-graph edge")
        first, second = sorted((raw_first, raw_second))
        bit_first = 1 << first
        bit_second = 1 << second
        if adjacency[first] & bit_second:
            raise ValueError("duplicate edge")
        adjacency[first] |= bit_second
        adjacency[second] |= bit_first

    colors = [-1] * order
    degrees = [neighbors.bit_count() for neighbors in adjacency]
    full = (1 << order) - 1

    def search(uncolored: int, maximum_used: int) -> bool:
        if not uncolored:
            return True

        best_vertex = -1
        best_key = (-1, -1, 0)
        cursor = uncolored
        while cursor:
            bit = cursor & -cursor
            cursor ^= bit
            vertex = bit.bit_length() - 1
            neighbor_colors = 0
            neighbors = adjacency[vertex]
            while neighbors:
                neighbor_bit = neighbors & -neighbors
                neighbors ^= neighbor_bit
                color = colors[neighbor_bit.bit_length() - 1]
                if color >= 0:
                    neighbor_colors |= 1 << color
            key = (neighbor_colors.bit_count(), degrees[vertex], -vertex)
            if key > best_key:
                best_key = key
                best_vertex = vertex

        forbidden = 0
        neighbors = adjacency[best_vertex]
        while neighbors:
            bit = neighbors & -neighbors
            neighbors ^= bit
            color = colors[bit.bit_length() - 1]
            if color >= 0:
                forbidden |= 1 << color

        # Existing colors first. At most one new color is tried, which fixes
        # color-label symmetry without excluding a partition.
        largest = min(color_count - 1, maximum_used + 1)
        for color in range(largest + 1):
            if forbidden >> color & 1:
                continue
            if color > maximum_used + 1:
                continue
            colors[best_vertex] = color
            if search(
                uncolored & ~(1 << best_vertex),
                max(maximum_used, color),
            ):
                return True
            colors[best_vertex] = -1
        return False

    if search(full, -1):
        result = tuple(colors)
        verify_coloring(order, adjacency, result, color_count)
        return result
    return None


def verify_coloring(
    order: int,
    adjacency: list[int],
    coloring: tuple[int, ...],
    color_count: int,
) -> None:
    if len(adjacency) != order or len(coloring) != order:
        raise ValueError("coloring dimension mismatch")
    if any(
        type(color) is not int or not 0 <= color < color_count
        for color in coloring
    ):
        raise ValueError("invalid color")
    for first in range(order):
        neighbors = adjacency[first]
        while neighbors:
            bit = neighbors & -neighbors
            neighbors ^= bit
            second = bit.bit_length() - 1
            if first < second and coloring[first] == coloring[second]:
                raise ValueError("coloring is not proper")
