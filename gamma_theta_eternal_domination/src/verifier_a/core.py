"""Exact bitset algorithms for the one-guard-moves model.

This module intentionally uses only the Python standard library.  Its eternal
domination core is a greatest-fixed-point deletion algorithm on bit-encoded
dominating configurations.  Verifier B uses different graph/configuration
representations and must not import this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from typing import Iterable, Iterator


def _vertex_of(bit: int) -> int:
    """Return the index of a nonzero singleton bit."""

    return bit.bit_length() - 1


def _masks_of_size(n: int, k: int) -> Iterator[int]:
    for vertices in combinations(range(n), k):
        mask = 0
        for vertex in vertices:
            mask |= 1 << vertex
        yield mask


@dataclass(frozen=True, slots=True)
class BitGraph:
    """A finite simple graph with open neighborhoods stored as integer masks."""

    n: int
    adj: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.n < 0 or len(self.adj) != self.n:
            raise ValueError("adjacency length must equal a nonnegative order")
        full = (1 << self.n) - 1
        for vertex, neighborhood in enumerate(self.adj):
            if neighborhood < 0 or neighborhood & ~full:
                raise ValueError("adjacency contains an out-of-range vertex")
            if neighborhood & (1 << vertex):
                raise ValueError("loops are not allowed")
        for u in range(self.n):
            for v in range(u + 1, self.n):
                if bool(self.adj[u] & (1 << v)) != bool(
                    self.adj[v] & (1 << u)
                ):
                    raise ValueError("adjacency must be symmetric")

    @property
    def full(self) -> int:
        return (1 << self.n) - 1

    @property
    def closed(self) -> tuple[int, ...]:
        return tuple(self.adj[v] | (1 << v) for v in range(self.n))

    @property
    def size(self) -> int:
        return sum(mask.bit_count() for mask in self.adj) // 2

    @classmethod
    def from_edges(
        cls, n: int, edges: Iterable[tuple[int, int]]
    ) -> "BitGraph":
        adjacency = [0] * n
        for u, v in edges:
            if not (0 <= u < n and 0 <= v < n):
                raise ValueError("edge endpoint out of range")
            if u == v:
                raise ValueError("loops are not allowed")
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
        return cls(n, tuple(adjacency))

    @classmethod
    def complete(cls, n: int) -> "BitGraph":
        full = (1 << n) - 1
        return cls(n, tuple(full ^ (1 << v) for v in range(n)))

    @classmethod
    def edgeless(cls, n: int) -> "BitGraph":
        return cls(n, (0,) * n)

    @classmethod
    def path(cls, n: int) -> "BitGraph":
        return cls.from_edges(n, ((v, v + 1) for v in range(n - 1)))

    @classmethod
    def cycle(cls, n: int) -> "BitGraph":
        if n < 3:
            raise ValueError("a simple cycle has order at least 3")
        return cls.from_edges(
            n, ((v, (v + 1) % n) for v in range(n))
        )

    @classmethod
    def from_graph6(cls, text: str | bytes) -> "BitGraph":
        """Decode one graph6 record, including the standard optional header."""

        if isinstance(text, str):
            raw = text.strip().encode("ascii")
        else:
            raw = text.strip()
        header = b">>graph6<<"
        if raw.startswith(header):
            raw = raw[len(header) :]
        if not raw:
            raise ValueError("empty graph6 record")
        values = [byte - 63 for byte in raw]
        if any(value < 0 or value > 63 for value in values):
            raise ValueError("invalid graph6 character")

        if values[0] < 63:
            n = values[0]
            offset = 1
        elif len(values) >= 4 and values[1] < 63:
            n = (values[1] << 12) | (values[2] << 6) | values[3]
            if n < 63:
                raise ValueError("noncanonical graph6 18-bit order")
            offset = 4
        elif len(values) >= 8 and values[1] == 63:
            n = 0
            for value in values[2:8]:
                n = (n << 6) | value
            if n < 258_048:
                raise ValueError("noncanonical graph6 36-bit order")
            offset = 8
        else:
            raise ValueError("truncated graph6 order")

        needed = n * (n - 1) // 2
        payload = values[offset:]
        expected_payload_length = (needed + 5) // 6
        if len(payload) != expected_payload_length:
            raise ValueError("wrong graph6 edge-data length")
        bits: list[int] = []
        for value in payload:
            bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
        if any(bits[needed:]):
            raise ValueError("nonzero graph6 padding")

        adjacency = [0] * n
        position = 0
        for v in range(1, n):
            for u in range(v):
                if bits[position]:
                    adjacency[u] |= 1 << v
                    adjacency[v] |= 1 << u
                position += 1
        return cls(n, tuple(adjacency))

    def to_graph6(self) -> str:
        if self.n <= 62:
            prefix = [self.n]
        elif self.n <= 258047:
            prefix = [
                63,
                (self.n >> 12) & 63,
                (self.n >> 6) & 63,
                self.n & 63,
            ]
        elif self.n <= (1 << 36) - 1:
            prefix = [63, 63]
            prefix.extend(
                (self.n >> shift) & 63 for shift in range(30, -1, -6)
            )
        else:
            raise ValueError("graph too large for graph6")

        bits: list[int] = []
        for v in range(1, self.n):
            for u in range(v):
                bits.append(int(bool(self.adj[u] & (1 << v))))
        while len(bits) % 6:
            bits.append(0)
        values = list(prefix)
        for start in range(0, len(bits), 6):
            value = 0
            for bit in bits[start : start + 6]:
                value = (value << 1) | bit
            values.append(value)
        return bytes(value + 63 for value in values).decode("ascii")

    def is_dominating(self, mask: int) -> bool:
        if mask < 0 or mask & ~self.full:
            return False
        covered = 0
        remaining = mask
        closed = self.closed
        while remaining:
            bit = remaining & -remaining
            covered |= closed[_vertex_of(bit)]
            if covered == self.full:
                return True
            remaining ^= bit
        return covered == self.full

    def is_independent(self, mask: int) -> bool:
        if mask < 0 or mask & ~self.full:
            return False
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            vertex = _vertex_of(bit)
            remaining ^= bit
            if self.adj[vertex] & remaining:
                return False
        return True

    def complement(self) -> "BitGraph":
        return BitGraph(
            self.n,
            tuple(self.full ^ (1 << v) ^ self.adj[v] for v in range(self.n)),
        )


def dominating_masks(graph: BitGraph, k: int) -> tuple[int, ...]:
    if not 0 <= k <= graph.n:
        return ()
    return tuple(
        mask for mask in _masks_of_size(graph.n, k) if graph.is_dominating(mask)
    )


def domination_number(graph: BitGraph) -> int:
    for k in range(graph.n + 1):
        if any(graph.is_dominating(mask) for mask in _masks_of_size(graph.n, k)):
            return k
    raise AssertionError("the full vertex set must dominate")


def alpha(graph: BitGraph) -> int:
    for k in range(graph.n, -1, -1):
        if any(graph.is_independent(mask) for mask in _masks_of_size(graph.n, k)):
            return k
    raise AssertionError("the empty set must be independent")


def independent_domination_number(graph: BitGraph) -> int:
    """Minimum cardinality of a maximal independent set."""

    for k in range(graph.n + 1):
        for mask in _masks_of_size(graph.n, k):
            if graph.is_independent(mask) and graph.is_dominating(mask):
                return k
    raise AssertionError("a maximal independent set always exists")


@dataclass(frozen=True, slots=True)
class CliqueCoverResult:
    value: int
    parts: tuple[int, ...]


def clique_cover(graph: BitGraph) -> CliqueCoverResult:
    """Exact clique-partition number by exhaustive subset dynamic programming."""

    clique = [False] * (1 << graph.n)
    clique[0] = True
    for mask in range(1, 1 << graph.n):
        bit = mask & -mask
        vertex = _vertex_of(bit)
        rest = mask ^ bit
        clique[mask] = clique[rest] and not (rest & ~graph.adj[vertex])

    choice: dict[int, int] = {}

    @lru_cache(maxsize=None)
    def solve(mask: int) -> int:
        if not mask:
            return 0
        pivot = mask & -mask
        best = graph.n + 1
        best_part = pivot
        part = mask
        while part:
            if part & pivot and clique[part]:
                candidate = 1 + solve(mask ^ part)
                if candidate < best:
                    best = candidate
                    best_part = part
            part = (part - 1) & mask
        choice[mask] = best_part
        return best

    value = solve(graph.full)
    parts: list[int] = []
    remaining = graph.full
    while remaining:
        part = choice[remaining]
        parts.append(part)
        remaining ^= part
    return CliqueCoverResult(value, tuple(parts))


def theta(graph: BitGraph) -> int:
    return clique_cover(graph).value


@dataclass(frozen=True, slots=True)
class EternalResult:
    """Greatest closed family and one selected legal response per attack."""

    k: int
    family: tuple[int, ...]
    responses: dict[tuple[int, int], tuple[int, int]]
    rounds: int

    @property
    def exists(self) -> bool:
        return bool(self.family)


def eternal_fixed_point(graph: BitGraph, k: int) -> EternalResult:
    """Return the greatest eternal family among dominating k-configurations.

    Each configuration and each family of configurations is encoded as a
    bitset.  Starting from all dominating k-configurations, a configuration is
    deleted whenever one of its unoccupied attacked vertices has no legal
    one-edge, one-guard response remaining in the current family.  Monotonicity
    makes the terminal set the greatest fixed point.
    """

    configurations = dominating_masks(graph, k)
    if not configurations:
        return EternalResult(k, (), {}, 0)
    index = {mask: position for position, mask in enumerate(configurations)}

    attacks: list[tuple[tuple[int, int], ...]] = []
    for configuration in configurations:
        per_attack: list[tuple[int, int]] = []
        unoccupied = graph.full ^ configuration
        while unoccupied:
            attacked_bit = unoccupied & -unoccupied
            attacked = _vertex_of(attacked_bit)
            candidates = 0
            movable = configuration & graph.adj[attacked]
            while movable:
                guard_bit = movable & -movable
                successor = configuration ^ guard_bit ^ attacked_bit
                successor_index = index.get(successor)
                if successor_index is not None:
                    candidates |= 1 << successor_index
                movable ^= guard_bit
            per_attack.append((attacked, candidates))
            unoccupied ^= attacked_bit
        attacks.append(tuple(per_attack))

    active = (1 << len(configurations)) - 1
    rounds = 0
    while True:
        rounds += 1
        before = active
        scanning = before
        while scanning:
            bit = scanning & -scanning
            position = _vertex_of(bit)
            if any(not (candidate_set & active) for _, candidate_set in attacks[position]):
                active ^= bit
            scanning ^= bit
        if active == before:
            break

    family = tuple(
        configurations[position]
        for position in range(len(configurations))
        if active & (1 << position)
    )
    responses: dict[tuple[int, int], tuple[int, int]] = {}
    if family:
        for position, configuration in enumerate(configurations):
            if not (active & (1 << position)):
                continue
            for attacked, candidate_set in attacks[position]:
                legal = candidate_set & active
                if not legal:
                    raise AssertionError("terminal family is not closed")
                successor_position = _vertex_of(legal & -legal)
                successor = configurations[successor_position]
                removed = configuration & ~successor
                if removed.bit_count() != 1:
                    raise AssertionError("response did not move exactly one guard")
                guard = _vertex_of(removed)
                responses[(configuration, attacked)] = (guard, successor)
    return EternalResult(k, family, responses, rounds)


def eternal_domination_number(graph: BitGraph) -> int:
    lower = domination_number(graph)
    for k in range(lower, graph.n + 1):
        if eternal_fixed_point(graph, k).exists:
            return k
    raise AssertionError("placing a guard on every vertex is eternal")


def verify_eternal_result(graph: BitGraph, result: EternalResult) -> bool:
    """Check an explicit family/response certificate without fixed-point logic."""

    if not isinstance(result, EternalResult):
        return False
    if type(result.k) is not int or not 0 <= result.k <= graph.n:
        return False
    if not result.family or not isinstance(result.responses, dict):
        return False
    try:
        family = set(result.family)
    except TypeError:
        return False
    if not family:
        return False
    for configuration in family:
        if (
            type(configuration) is not int
            or configuration < 0
            or configuration & ~graph.full
        ):
            return False

    expected_response_keys: set[tuple[int, int]] = set()
    for configuration in family:
        if configuration.bit_count() != result.k:
            return False
        if not graph.is_dominating(configuration):
            return False
        unoccupied = graph.full ^ configuration
        while unoccupied:
            attacked_bit = unoccupied & -unoccupied
            attacked = _vertex_of(attacked_bit)
            response_key = (configuration, attacked)
            expected_response_keys.add(response_key)
            response = result.responses.get(response_key)
            if response is None:
                return False
            if not isinstance(response, tuple) or len(response) != 2:
                return False
            guard, successor = response
            if (
                type(guard) is not int
                or not 0 <= guard < graph.n
                or type(successor) is not int
                or successor < 0
                or successor & ~graph.full
            ):
                return False
            guard_bit = 1 << guard
            if not (configuration & guard_bit):
                return False
            if not (graph.adj[attacked] & guard_bit):
                return False
            if successor != (configuration ^ guard_bit ^ attacked_bit):
                return False
            if successor not in family or not graph.is_dominating(successor):
                return False
            unoccupied ^= attacked_bit
    return set(result.responses) == expected_response_keys
