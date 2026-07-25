"""Strict bounded graph primitives for the independent edge-toggle audit.

Only ordinary graph6 records of order at most twelve are accepted.  The
isomorphism routine is an exact deterministic backtracker with joint
one-dimensional color refinement; it does not call nauty or either campaign
verifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator


MAX_ORDER = 12


class Graph6Error(ValueError):
    """Raised when a graph6 record is malformed or outside the bounded scope."""


@dataclass(frozen=True, slots=True)
class Graph:
    order: int
    rows: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.order) is not int or not 0 <= self.order <= MAX_ORDER:
            raise ValueError(f"order must be an integer in [0,{MAX_ORDER}]")
        if type(self.rows) is not tuple or len(self.rows) != self.order:
            raise ValueError("one integer adjacency row is required per vertex")
        universe = (1 << self.order) - 1
        for vertex, row in enumerate(self.rows):
            if type(row) is not int or row < 0 or row & ~universe:
                raise ValueError("invalid adjacency row")
            if row & (1 << vertex):
                raise ValueError("loops are forbidden")
        for first in range(self.order):
            for second in range(first + 1, self.order):
                if bool(self.rows[first] & (1 << second)) != bool(
                    self.rows[second] & (1 << first)
                ):
                    raise ValueError("adjacency is not symmetric")

    @property
    def size(self) -> int:
        return sum(row.bit_count() for row in self.rows) // 2

    @property
    def degrees(self) -> tuple[int, ...]:
        return tuple(row.bit_count() for row in self.rows)

    def has_edge(self, first: int, second: int) -> bool:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < self.order
            or not 0 <= second < self.order
        ):
            raise ValueError("vertex outside graph")
        return bool(self.rows[first] & (1 << second))

    def edges(self) -> Iterator[tuple[int, int]]:
        for second in range(1, self.order):
            for first in range(second):
                if self.rows[first] & (1 << second):
                    yield first, second

    def toggled(self, first: int, second: int) -> Graph:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < second < self.order
        ):
            raise ValueError("toggle pair must satisfy 0 <= first < second < n")
        rows = list(self.rows)
        rows[first] ^= 1 << second
        rows[second] ^= 1 << first
        return Graph(self.order, tuple(rows))

    def is_connected(self) -> bool:
        if self.order == 0:
            return False
        reached = 1
        frontier = 1
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            vertex = bit.bit_length() - 1
            additions = self.rows[vertex] & ~reached
            reached |= additions
            frontier |= additions
        return reached == (1 << self.order) - 1

    def relabeled(self, old_to_new: Iterable[int]) -> Graph:
        permutation = tuple(old_to_new)
        if (
            len(permutation) != self.order
            or any(type(value) is not int for value in permutation)
            or set(permutation) != set(range(self.order))
        ):
            raise ValueError("relabeling is not a permutation")
        rows = [0] * self.order
        for first, second in self.edges():
            image_first = permutation[first]
            image_second = permutation[second]
            rows[image_first] |= 1 << image_second
            rows[image_second] |= 1 << image_first
        return Graph(self.order, tuple(rows))

    @classmethod
    def from_edges(
        cls, order: int, edges: Iterable[tuple[int, int]]
    ) -> Graph:
        if type(order) is not int or not 0 <= order <= MAX_ORDER:
            raise ValueError("invalid graph order")
        rows = [0] * order
        seen: set[tuple[int, int]] = set()
        for edge in edges:
            if type(edge) not in (tuple, list) or len(edge) != 2:
                raise ValueError("each edge must have two endpoints")
            first, second = edge
            if (
                type(first) is not int
                or type(second) is not int
                or not 0 <= first < order
                or not 0 <= second < order
                or first == second
            ):
                raise ValueError("invalid edge")
            pair = (first, second) if first < second else (second, first)
            if pair in seen:
                raise ValueError("duplicate edge")
            seen.add(pair)
            rows[first] |= 1 << second
            rows[second] |= 1 << first
        return cls(order, tuple(rows))

    @classmethod
    def from_graph6(cls, record: str | bytes) -> Graph:
        if isinstance(record, str):
            try:
                raw = record.encode("ascii")
            except UnicodeEncodeError as error:
                raise Graph6Error("graph6 must be ASCII") from error
        elif isinstance(record, bytes):
            raw = record
        else:
            raise Graph6Error("graph6 must be text or bytes")
        if raw.startswith(b">>graph6<<"):
            raw = raw[10:]
        if not raw:
            raise Graph6Error("empty graph6 record")
        if raw[0] == 126:
            raise Graph6Error("extended graph6 order is outside this scope")
        if not 63 <= raw[0] <= 125:
            raise Graph6Error("invalid graph6 order byte")
        order = raw[0] - 63
        if order > MAX_ORDER:
            raise Graph6Error("graph6 order exceeds twelve")
        edge_bits = order * (order - 1) // 2
        payload_length = (edge_bits + 5) // 6
        if len(raw) != payload_length + 1:
            raise Graph6Error("wrong graph6 payload length")
        payload = raw[1:]
        if any(not 63 <= value <= 126 for value in payload):
            raise Graph6Error("invalid graph6 payload byte")
        padding = payload_length * 6 - edge_bits
        if padding and payload and ((payload[-1] - 63) & ((1 << padding) - 1)):
            raise Graph6Error("nonzero graph6 padding")
        rows = [0] * order
        position = 0
        for second in range(1, order):
            for first in range(second):
                value = payload[position // 6] - 63
                if value & (1 << (5 - position % 6)):
                    rows[first] |= 1 << second
                    rows[second] |= 1 << first
                position += 1
        return cls(order, tuple(rows))

    def to_graph6(self) -> str:
        bits: list[int] = []
        for second in range(1, self.order):
            for first in range(second):
                bits.append(int(bool(self.rows[first] & (1 << second))))
        while len(bits) % 6:
            bits.append(0)
        encoded = bytearray((self.order + 63,))
        for start in range(0, len(bits), 6):
            value = 0
            for bit in bits[start : start + 6]:
                value = (value << 1) | bit
            encoded.append(value + 63)
        return encoded.decode("ascii")


def _distance_profile(graph: Graph, root: int) -> tuple[int, ...]:
    reached = 1 << root
    frontier = reached
    layers: list[int] = []
    while frontier:
        neighbors = 0
        remaining = frontier
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            neighbors |= graph.rows[bit.bit_length() - 1]
        frontier = neighbors & ~reached
        if not frontier:
            break
        layers.append(frontier.bit_count())
        reached |= frontier
    layers.append(graph.order - reached.bit_count())
    return tuple(layers)


def _initial_signatures(graph: Graph) -> tuple[tuple[object, ...], ...]:
    degrees = graph.degrees
    signatures: list[tuple[object, ...]] = []
    for vertex, row in enumerate(graph.rows):
        twice_triangles = 0
        neighbor_degrees: list[int] = []
        remaining = row
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            neighbor = bit.bit_length() - 1
            neighbor_degrees.append(degrees[neighbor])
            twice_triangles += (row & graph.rows[neighbor]).bit_count()
        signatures.append(
            (
                degrees[vertex],
                twice_triangles // 2,
                tuple(sorted(neighbor_degrees)),
                _distance_profile(graph, vertex),
            )
        )
    return tuple(signatures)


def _joint_refinement(
    left: Graph, right: Graph
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    signatures = _initial_signatures(left) + _initial_signatures(right)
    palette = {
        signature: color
        for color, signature in enumerate(sorted(set(signatures)))
    }
    left_colors = tuple(
        palette[value] for value in _initial_signatures(left)
    )
    right_colors = tuple(
        palette[value] for value in _initial_signatures(right)
    )
    while True:
        if sorted(left_colors) != sorted(right_colors):
            return None
        labels: list[tuple[object, ...]] = []
        for graph, colors in (
            (left, left_colors),
            (right, right_colors),
        ):
            for vertex, row in enumerate(graph.rows):
                labels.append(
                    (
                        colors[vertex],
                        tuple(
                            sorted(
                                colors[other]
                                for other in range(graph.order)
                                if row & (1 << other)
                            )
                        ),
                    )
                )
        next_palette = {
            label: color
            for color, label in enumerate(sorted(set(labels)))
        }
        split = left.order
        next_left = tuple(next_palette[label] for label in labels[:split])
        next_right = tuple(next_palette[label] for label in labels[split:])
        if next_left == left_colors and next_right == right_colors:
            return left_colors, right_colors
        left_colors, right_colors = next_left, next_right


def verify_isomorphism(
    left: Graph, right: Graph, old_to_new: Iterable[int]
) -> bool:
    mapping = tuple(old_to_new)
    if (
        left.order != right.order
        or len(mapping) != left.order
        or any(type(value) is not int for value in mapping)
        or set(mapping) != set(range(left.order))
    ):
        return False
    for first in range(left.order):
        for second in range(first + 1, left.order):
            if left.has_edge(first, second) != right.has_edge(
                mapping[first], mapping[second]
            ):
                return False
    return True


def find_isomorphism(left: Graph, right: Graph) -> tuple[int, ...] | None:
    """Return an exact old-left-to-new-right isomorphism, if one exists."""

    if (
        left.order != right.order
        or left.size != right.size
        or sorted(left.degrees) != sorted(right.degrees)
    ):
        return None
    refined = _joint_refinement(left, right)
    if refined is None:
        return None
    left_colors, right_colors = refined
    order = left.order
    mapping = [-1] * order
    used = [False] * order

    def compatible(first: int, image: int) -> bool:
        if left_colors[first] != right_colors[image]:
            return False
        for assigned, assigned_image in enumerate(mapping):
            if assigned_image < 0:
                continue
            if left.has_edge(first, assigned) != right.has_edge(
                image, assigned_image
            ):
                return False
        return True

    def search(remaining: int) -> bool:
        if remaining == 0:
            return True
        chosen = -1
        candidates: tuple[int, ...] = ()
        for first in range(order):
            if mapping[first] >= 0:
                continue
            available = tuple(
                image
                for image in range(order)
                if not used[image] and compatible(first, image)
            )
            if not available:
                return False
            if chosen < 0 or len(available) < len(candidates):
                chosen = first
                candidates = available
                if len(candidates) == 1:
                    break
        for image in candidates:
            mapping[chosen] = image
            used[image] = True
            feasible = True
            for first in range(order):
                if mapping[first] >= 0:
                    continue
                if not any(
                    not used[target] and compatible(first, target)
                    for target in range(order)
                ):
                    feasible = False
                    break
            if feasible and search(remaining - 1):
                return True
            used[image] = False
            mapping[chosen] = -1
        return False

    if not search(order):
        return None
    result = tuple(mapping)
    if not verify_isomorphism(left, right, result):
        raise AssertionError("internal isomorphism witness verification failed")
    return result
