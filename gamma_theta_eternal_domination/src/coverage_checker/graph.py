"""Independent small-graph primitives for coverage auditing.

This module deliberately does not import either campaign verifier or any search
module.  It supports only graphs of order at most 12: that keeps malformed
large inputs from turning a coverage check into an accidental resource-heavy
computation.

The graph6 codec accepts the ordinary one-byte order form, with an optional
standard ``>>graph6<<`` header.  Extended order encodings, sparse6/digraph6,
whitespace, extra payload, and nonzero padding are rejected.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator


MAX_ORDER = 12
_GRAPH6_HEADER = b">>graph6<<"


class Graph6Error(ValueError):
    """A graph6 record is malformed or outside this checker's strict scope."""


@dataclass(frozen=True, slots=True)
class Graph:
    """A finite simple graph represented by independent adjacency bit rows."""

    order: int
    neighbors: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.order) is not int or not 0 <= self.order <= MAX_ORDER:
            raise ValueError(f"order must be an integer in [0, {MAX_ORDER}]")
        if type(self.neighbors) is not tuple or len(self.neighbors) != self.order:
            raise ValueError("neighbors must be a tuple with one row per vertex")

        universe = (1 << self.order) - 1
        for vertex, row in enumerate(self.neighbors):
            if type(row) is not int or row < 0 or row & ~universe:
                raise ValueError("adjacency row contains an invalid vertex")
            if row & (1 << vertex):
                raise ValueError("loops are not allowed")

        for first in range(self.order):
            for second in range(first + 1, self.order):
                forward = bool(self.neighbors[first] & (1 << second))
                backward = bool(self.neighbors[second] & (1 << first))
                if forward != backward:
                    raise ValueError("adjacency must be symmetric")

    @property
    def n(self) -> int:
        """Alias for the order, convenient in bounded enumeration code."""

        return self.order

    @property
    def adjacency(self) -> tuple[int, ...]:
        """Read-only compatibility name for the independent bit rows."""

        return self.neighbors

    @property
    def size(self) -> int:
        return sum(row.bit_count() for row in self.neighbors) // 2

    @property
    def degrees(self) -> tuple[int, ...]:
        return tuple(row.bit_count() for row in self.neighbors)

    def has_edge(self, first: int, second: int) -> bool:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < self.order
            or not 0 <= second < self.order
        ):
            raise ValueError("vertex outside graph")
        return bool(self.neighbors[first] & (1 << second))

    def edges(self) -> Iterator[tuple[int, int]]:
        for second in range(1, self.order):
            for first in range(second):
                if self.neighbors[first] & (1 << second):
                    yield first, second

    @classmethod
    def from_edges(
        cls, order: int, edges: Iterable[tuple[int, int]]
    ) -> Graph:
        if type(order) is not int or not 0 <= order <= MAX_ORDER:
            raise ValueError(f"order must be an integer in [0, {MAX_ORDER}]")
        rows = [0] * order
        seen: set[tuple[int, int]] = set()
        try:
            iterator = iter(edges)
        except TypeError as error:
            raise ValueError("edges must be iterable") from error
        for edge in iterator:
            if type(edge) not in (tuple, list) or len(edge) != 2:
                raise ValueError("each edge must have two endpoints")
            first, second = edge
            if (
                type(first) is not int
                or type(second) is not int
                or not 0 <= first < order
                or not 0 <= second < order
            ):
                raise ValueError("edge endpoint outside graph")
            if first == second:
                raise ValueError("loops are not allowed")
            normalized = (
                (first, second) if first < second else (second, first)
            )
            if normalized in seen:
                raise ValueError("duplicate edge")
            seen.add(normalized)
            rows[first] |= 1 << second
            rows[second] |= 1 << first
        return cls(order, tuple(rows))

    @classmethod
    def from_graph6(cls, record: str | bytes) -> Graph:
        return parse_graph6(record)

    def to_graph6(self) -> str:
        return encode_graph6(self)

    def add_extension(self, neighborhood_mask: int) -> Graph:
        """Method form of :func:`add_extension` for streaming audits."""

        return add_extension(self, neighborhood_mask)

    def relabel(self, old_to_new: Iterable[int]) -> Graph:
        """Return the graph under a permutation mapping old labels to new."""

        permutation = tuple(old_to_new)
        if (
            len(permutation) != self.order
            or any(type(vertex) is not int for vertex in permutation)
            or set(permutation) != set(range(self.order))
        ):
            raise ValueError("relabeling must be a permutation of the vertices")

        rows = [0] * self.order
        for first, second in self.edges():
            image_first = permutation[first]
            image_second = permutation[second]
            rows[image_first] |= 1 << image_second
            rows[image_second] |= 1 << image_first
        return Graph(self.order, tuple(rows))


def _ascii_record(record: str | bytes) -> bytes:
    if isinstance(record, str):
        try:
            raw = record.encode("ascii")
        except UnicodeEncodeError as error:
            raise Graph6Error("graph6 record must be ASCII") from error
    elif isinstance(record, bytes):
        raw = record
    else:
        raise Graph6Error("graph6 record must be str or bytes")
    if raw.startswith(_GRAPH6_HEADER):
        raw = raw[len(_GRAPH6_HEADER) :]
    if not raw:
        raise Graph6Error("empty graph6 record")
    return raw


def parse_graph6(record: str | bytes) -> Graph:
    """Parse a strict ordinary graph6 record of order at most 12."""

    raw = _ascii_record(record)
    if raw[0] == 126:
        raise Graph6Error("extended graph6 order encodings are not supported")
    if not 63 <= raw[0] <= 125:
        raise Graph6Error("invalid graph6 order character")
    order = raw[0] - 63
    if order > MAX_ORDER:
        raise Graph6Error(f"graph6 order exceeds the limit of {MAX_ORDER}")

    edge_bit_count = order * (order - 1) // 2
    payload_length = (edge_bit_count + 5) // 6
    if len(raw) != 1 + payload_length:
        raise Graph6Error("wrong graph6 payload length")
    payload = raw[1:]
    if any(not 63 <= byte <= 126 for byte in payload):
        raise Graph6Error("invalid graph6 payload character")

    padding = payload_length * 6 - edge_bit_count
    if padding and payload and (payload[-1] - 63) & ((1 << padding) - 1):
        raise Graph6Error("nonzero graph6 padding")

    rows = [0] * order
    position = 0
    for second in range(1, order):
        for first in range(second):
            value = payload[position // 6] - 63
            present = (value >> (5 - position % 6)) & 1
            if present:
                rows[first] |= 1 << second
                rows[second] |= 1 << first
            position += 1
    return Graph(order, tuple(rows))


def encode_graph6(graph: Graph) -> str:
    """Encode a bounded graph in canonical ordinary graph6 syntax."""

    if not isinstance(graph, Graph):
        raise ValueError("expected a coverage_checker Graph")

    bits: list[int] = []
    for second in range(1, graph.order):
        for first in range(second):
            bits.append(int(bool(graph.neighbors[first] & (1 << second))))
    while len(bits) % 6:
        bits.append(0)

    output = bytearray((graph.order + 63,))
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        output.append(value + 63)
    return output.decode("ascii")


def add_extension(graph: Graph, neighborhood_mask: int) -> Graph:
    """Add one vertex with a specified nonempty neighborhood in ``graph``."""

    if not isinstance(graph, Graph):
        raise ValueError("expected a coverage_checker Graph")
    if graph.order >= MAX_ORDER:
        raise ValueError(f"extension would exceed order {MAX_ORDER}")
    universe = (1 << graph.order) - 1
    if (
        type(neighborhood_mask) is not int
        or neighborhood_mask <= 0
        or neighborhood_mask & ~universe
    ):
        raise ValueError("extension neighborhood must be a nonempty vertex mask")

    new_vertex = graph.order
    rows = list(graph.neighbors)
    for vertex in range(graph.order):
        if neighborhood_mask & (1 << vertex):
            rows[vertex] |= 1 << new_vertex
    rows.append(neighborhood_mask)
    return Graph(graph.order + 1, tuple(rows))


def _component_orders(graph: Graph) -> tuple[int, ...]:
    unseen = (1 << graph.order) - 1
    orders: list[int] = []
    while unseen:
        seed = unseen & -unseen
        unseen ^= seed
        frontier = seed
        size = 0
        while frontier:
            vertex_bit = frontier & -frontier
            frontier ^= vertex_bit
            vertex = vertex_bit.bit_length() - 1
            size += 1
            additions = graph.neighbors[vertex] & unseen
            unseen ^= additions
            frontier |= additions
        orders.append(size)
    return tuple(sorted(orders))


def _distance_profile(graph: Graph, root: int) -> tuple[int, ...]:
    reached = 1 << root
    frontier = reached
    layer_sizes: list[int] = []
    while frontier:
        next_frontier = 0
        remaining = frontier
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            vertex = bit.bit_length() - 1
            next_frontier |= graph.neighbors[vertex]
        next_frontier &= ~reached
        if not next_frontier:
            break
        layer_sizes.append(next_frontier.bit_count())
        reached |= next_frontier
        frontier = next_frontier
    layer_sizes.append(graph.order - reached.bit_count())
    return tuple(layer_sizes)


def _base_vertex_invariants(graph: Graph) -> tuple[tuple[object, ...], ...]:
    degrees = graph.degrees
    invariants: list[tuple[object, ...]] = []
    for vertex, row in enumerate(graph.neighbors):
        neighbor_degrees = tuple(
            sorted(
                degrees[other]
                for other in range(graph.order)
                if row & (1 << other)
            )
        )
        twice_triangles = 0
        remaining = row
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            neighbor = bit.bit_length() - 1
            twice_triangles += (graph.neighbors[neighbor] & row).bit_count()
        invariants.append(
            (
                degrees[vertex],
                twice_triangles // 2,
                neighbor_degrees,
                _distance_profile(graph, vertex),
            )
        )
    return tuple(invariants)


def _joint_color_refinement(
    left: Graph,
    right: Graph,
    left_invariants: tuple[tuple[object, ...], ...],
    right_invariants: tuple[tuple[object, ...], ...],
    pairs: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    left_fixed = {vertex: index for index, (vertex, _) in enumerate(pairs)}
    right_fixed = {vertex: index for index, (_, vertex) in enumerate(pairs)}

    left_labels = tuple(
        (1, left_fixed[vertex], left_invariants[vertex])
        if vertex in left_fixed
        else (0, left_invariants[vertex])
        for vertex in range(left.order)
    )
    right_labels = tuple(
        (1, right_fixed[vertex], right_invariants[vertex])
        if vertex in right_fixed
        else (0, right_invariants[vertex])
        for vertex in range(right.order)
    )
    palette = {
        label: color
        for color, label in enumerate(sorted(set(left_labels + right_labels)))
    }
    left_colors = tuple(palette[label] for label in left_labels)
    right_colors = tuple(palette[label] for label in right_labels)

    while True:
        if sorted(left_colors) != sorted(right_colors):
            return None
        color_count = max(left_colors + right_colors, default=-1) + 1

        def signatures(graph: Graph, colors: tuple[int, ...]) -> tuple[
            tuple[int, tuple[int, ...]], ...
        ]:
            result: list[tuple[int, tuple[int, ...]]] = []
            for vertex, row in enumerate(graph.neighbors):
                counts = [0] * color_count
                remaining = row
                while remaining:
                    bit = remaining & -remaining
                    remaining ^= bit
                    counts[colors[bit.bit_length() - 1]] += 1
                result.append((colors[vertex], tuple(counts)))
            return tuple(result)

        left_signatures = signatures(left, left_colors)
        right_signatures = signatures(right, right_colors)
        signature_palette = {
            signature: color
            for color, signature in enumerate(
                sorted(set(left_signatures + right_signatures))
            )
        }
        new_left = tuple(
            signature_palette[signature] for signature in left_signatures
        )
        new_right = tuple(
            signature_palette[signature] for signature in right_signatures
        )
        if new_left == left_colors and new_right == right_colors:
            return left_colors, right_colors
        left_colors, right_colors = new_left, new_right


def _mapping_is_valid(
    left: Graph, right: Graph, mapping: tuple[int, ...]
) -> bool:
    if len(mapping) != left.order or set(mapping) != set(range(right.order)):
        return False
    for vertex, row in enumerate(left.neighbors):
        mapped_row = 0
        remaining = row
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            mapped_row |= 1 << mapping[bit.bit_length() - 1]
        if mapped_row != right.neighbors[mapping[vertex]]:
            return False
    return True


def find_isomorphism(left: Graph, right: Graph) -> tuple[int, ...] | None:
    """Return an exact old-left-to-right vertex map, or ``None``.

    The search uses joint color refinement and individualization.  There is no
    heuristic cutoff: a ``None`` result is an exhaustive nonisomorphism result
    for the bounded inputs.
    """

    if not isinstance(left, Graph) or not isinstance(right, Graph):
        raise ValueError("isomorphism inputs must be coverage_checker Graphs")
    if left.order != right.order or left.size != right.size:
        return None
    if sorted(left.degrees) != sorted(right.degrees):
        return None
    if _component_orders(left) != _component_orders(right):
        return None
    if left == right:
        return tuple(range(left.order))

    left_invariants = _base_vertex_invariants(left)
    right_invariants = _base_vertex_invariants(right)
    if sorted(left_invariants) != sorted(right_invariants):
        return None

    def search(
        pairs: tuple[tuple[int, int], ...],
    ) -> tuple[int, ...] | None:
        refined = _joint_color_refinement(
            left, right, left_invariants, right_invariants, pairs
        )
        if refined is None:
            return None
        left_colors, right_colors = refined

        left_cells: dict[int, list[int]] = {}
        right_cells: dict[int, list[int]] = {}
        for vertex, color in enumerate(left_colors):
            left_cells.setdefault(color, []).append(vertex)
        for vertex, color in enumerate(right_colors):
            right_cells.setdefault(color, []).append(vertex)
        if {
            color: len(cell) for color, cell in left_cells.items()
        } != {color: len(cell) for color, cell in right_cells.items()}:
            return None

        nonsingleton_colors = [
            color for color, cell in left_cells.items() if len(cell) > 1
        ]
        if not nonsingleton_colors:
            right_by_color = {
                color: cell[0] for color, cell in right_cells.items()
            }
            mapping = tuple(right_by_color[color] for color in left_colors)
            return mapping if _mapping_is_valid(left, right, mapping) else None

        branch_color = min(
            nonsingleton_colors,
            key=lambda color: (len(left_cells[color]), color),
        )
        left_vertex = left_cells[branch_color][0]
        for right_vertex in right_cells[branch_color]:
            consistent = True
            for paired_left, paired_right in pairs:
                left_edge = bool(
                    left.neighbors[left_vertex] & (1 << paired_left)
                )
                right_edge = bool(
                    right.neighbors[right_vertex] & (1 << paired_right)
                )
                if left_edge != right_edge:
                    consistent = False
                    break
            if not consistent:
                continue
            result = search(pairs + ((left_vertex, right_vertex),))
            if result is not None:
                return result
        return None

    return search(())


def are_isomorphic(left: Graph, right: Graph) -> bool:
    """Return whether two bounded graphs are exactly isomorphic."""

    return find_isomorphism(left, right) is not None


is_isomorphic = are_isomorphic
graphs_are_isomorphic = are_isomorphic


__all__ = [
    "MAX_ORDER",
    "Graph",
    "Graph6Error",
    "add_extension",
    "are_isomorphic",
    "encode_graph6",
    "find_isomorphism",
    "graphs_are_isomorphic",
    "is_isomorphic",
    "parse_graph6",
]
