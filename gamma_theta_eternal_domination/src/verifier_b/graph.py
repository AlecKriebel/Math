"""Small, immutable simple graphs for verifier B.

The representation is intentionally ordinary: vertex ``v`` has neighborhood
``adjacency[v]``, a ``frozenset`` of integer vertex labels.  No packed integer
or bit-vector representation is used in this verifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence


_GRAPH6_HEADER = ">>graph6<<"


@dataclass(frozen=True, slots=True)
class Graph:
    """A finite simple undirected graph on vertices ``0, ..., order - 1``."""

    adjacency: tuple[frozenset[int], ...]

    def __post_init__(self) -> None:
        normalized = tuple(frozenset(neighbors) for neighbors in self.adjacency)
        object.__setattr__(self, "adjacency", normalized)

        order = len(normalized)
        for vertex, neighbors in enumerate(normalized):
            if vertex in neighbors:
                raise ValueError(f"loop at vertex {vertex}")
            for neighbor in neighbors:
                if not isinstance(neighbor, int):
                    raise TypeError("vertex labels must be integers")
                if neighbor < 0 or neighbor >= order:
                    raise ValueError(
                        f"neighbor {neighbor} of {vertex} is outside 0..{order - 1}"
                    )
                if vertex not in normalized[neighbor]:
                    raise ValueError(
                        f"adjacency is not symmetric at edge {vertex}-{neighbor}"
                    )

    @classmethod
    def from_edges(
        cls, order: int, edges: Iterable[tuple[int, int]]
    ) -> "Graph":
        """Construct a graph of the given order from an iterable of edges."""

        if not isinstance(order, int):
            raise TypeError("order must be an integer")
        if order < 0:
            raise ValueError("order must be nonnegative")

        neighborhoods: list[set[int]] = [set() for _ in range(order)]
        for first, second in edges:
            if not isinstance(first, int) or not isinstance(second, int):
                raise TypeError("edge endpoints must be integers")
            if first < 0 or first >= order or second < 0 or second >= order:
                raise ValueError(f"edge endpoint outside 0..{order - 1}")
            if first == second:
                raise ValueError(f"loop at vertex {first}")
            neighborhoods[first].add(second)
            neighborhoods[second].add(first)
        return cls(tuple(frozenset(neighbors) for neighbors in neighborhoods))

    @classmethod
    def from_graph6(cls, encoded: str | bytes) -> "Graph":
        """Decode one graph6 record.

        The size formats from the graph6 specification are accepted.  The
        intended campaign range is order at most 12, but supporting all size
        headers makes malformed input easier to diagnose.
        """

        if isinstance(encoded, bytes):
            try:
                record = encoded.decode("ascii")
            except UnicodeDecodeError as error:
                raise ValueError("graph6 data must be ASCII") from error
        elif isinstance(encoded, str):
            record = encoded
        else:
            raise TypeError("graph6 record must be str or bytes")

        record = record.strip()
        if record.startswith(_GRAPH6_HEADER):
            record = record[len(_GRAPH6_HEADER) :]
        if not record:
            raise ValueError("empty graph6 record")

        values = _graph6_values(record)
        order, payload_start = _decode_order(values)
        edge_slots = order * (order - 1) // 2
        expected_payload_length = (edge_slots + 5) // 6
        payload = values[payload_start:]
        if len(payload) != expected_payload_length:
            raise ValueError(
                "wrong graph6 payload length: "
                f"expected {expected_payload_length}, got {len(payload)}"
            )

        bits: list[int] = []
        for value in payload:
            bits.extend(_six_bits(value))
        if any(bits[edge_slots:]):
            raise ValueError("nonzero graph6 padding bits")

        edges: list[tuple[int, int]] = []
        position = 0
        for higher_vertex in range(1, order):
            for lower_vertex in range(higher_vertex):
                if bits[position] == 1:
                    edges.append((lower_vertex, higher_vertex))
                position += 1
        return cls.from_edges(order, edges)

    @property
    def order(self) -> int:
        return len(self.adjacency)

    @property
    def vertices(self) -> range:
        return range(self.order)

    @property
    def size(self) -> int:
        return sum(len(neighbors) for neighbors in self.adjacency) // 2

    def degree(self, vertex: int) -> int:
        self._check_vertex(vertex)
        return len(self.adjacency[vertex])

    def neighbors(self, vertex: int) -> frozenset[int]:
        self._check_vertex(vertex)
        return self.adjacency[vertex]

    def closed_neighbors(self, vertex: int) -> frozenset[int]:
        self._check_vertex(vertex)
        return self.adjacency[vertex] | frozenset((vertex,))

    def has_edge(self, first: int, second: int) -> bool:
        self._check_vertex(first)
        self._check_vertex(second)
        return second in self.adjacency[first]

    def edges(self) -> Iterator[tuple[int, int]]:
        for first in self.vertices:
            for second in sorted(self.adjacency[first]):
                if first < second:
                    yield (first, second)

    def complement(self) -> "Graph":
        all_vertices = set(self.vertices)
        complemented: list[frozenset[int]] = []
        for vertex in self.vertices:
            complemented.append(
                frozenset(all_vertices - {vertex} - set(self.adjacency[vertex]))
            )
        return Graph(tuple(complemented))

    def to_graph6(self, header: bool = False) -> str:
        """Encode the graph as one graph6 record without a trailing newline."""

        values = _encode_order(self.order)
        bits: list[int] = []
        for higher_vertex in range(1, self.order):
            for lower_vertex in range(higher_vertex):
                bits.append(
                    1 if higher_vertex in self.adjacency[lower_vertex] else 0
                )
        while len(bits) % 6 != 0:
            bits.append(0)
        for start in range(0, len(bits), 6):
            value = 0
            for bit in bits[start : start + 6]:
                value = 2 * value + bit
            values.append(value)
        body = "".join(chr(value + 63) for value in values)
        return (_GRAPH6_HEADER if header else "") + body

    def _check_vertex(self, vertex: int) -> None:
        if not isinstance(vertex, int):
            raise TypeError("vertex must be an integer")
        if vertex < 0 or vertex >= self.order:
            raise ValueError(f"vertex {vertex} is outside 0..{self.order - 1}")


def _graph6_values(record: str) -> list[int]:
    values: list[int] = []
    for character in record:
        code = ord(character)
        if code < 63 or code > 126:
            raise ValueError(f"invalid graph6 character {character!r}")
        values.append(code - 63)
    return values


def _decode_base64_digits(digits: Sequence[int]) -> int:
    value = 0
    for digit in digits:
        value = 64 * value + digit
    return value


def _decode_order(values: Sequence[int]) -> tuple[int, int]:
    if not values:
        raise ValueError("missing graph6 order")
    if values[0] < 63:
        return values[0], 1
    if len(values) < 2:
        raise ValueError("truncated graph6 order")
    if values[1] < 63:
        if len(values) < 4:
            raise ValueError("truncated graph6 18-bit order")
        order = _decode_base64_digits(values[1:4])
        if order < 63:
            raise ValueError("noncanonical graph6 18-bit order")
        return order, 4
    if len(values) < 8:
        raise ValueError("truncated graph6 36-bit order")
    order = _decode_base64_digits(values[2:8])
    if order < 258_048:
        raise ValueError("noncanonical graph6 36-bit order")
    return order, 8


def _encode_order(order: int) -> list[int]:
    if order < 0:
        raise ValueError("order must be nonnegative")
    if order <= 62:
        return [order]
    if order <= 258_047:
        return [63] + _fixed_base64_digits(order, 3)
    if order <= 68_719_476_735:
        return [63, 63] + _fixed_base64_digits(order, 6)
    raise ValueError("graph6 cannot encode this order")


def _fixed_base64_digits(value: int, width: int) -> list[int]:
    digits = [0] * width
    remaining = value
    for position in range(width - 1, -1, -1):
        remaining, digit = divmod(remaining, 64)
        digits[position] = digit
    if remaining != 0:
        raise ValueError("value does not fit in requested graph6 width")
    return digits


def _six_bits(value: int) -> list[int]:
    return [(value // (2**power)) % 2 for power in range(5, -1, -1)]


def complete_graph(order: int) -> Graph:
    return Graph.from_edges(
        order,
        (
            (first, second)
            for first in range(order)
            for second in range(first + 1, order)
        ),
    )


def edgeless_graph(order: int) -> Graph:
    return Graph.from_edges(order, ())


def path_graph(order: int) -> Graph:
    if order < 0:
        raise ValueError("order must be nonnegative")
    return Graph.from_edges(order, ((vertex, vertex + 1) for vertex in range(order - 1)))


def cycle_graph(order: int) -> Graph:
    if order < 3:
        raise ValueError("a simple cycle needs at least three vertices")
    edges = [(vertex, vertex + 1) for vertex in range(order - 1)]
    edges.append((order - 1, 0))
    return Graph.from_edges(order, edges)
