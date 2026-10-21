"""Exact binary-weight perfect-matching reduction and finite reference counters.

No approximation theorem is implemented here.  The exhaustive counters are
exponential reference routines, not the claimed polynomial-time approximation
algorithm.  Python integers and Fraction keep every calculation exact.
"""

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Graph:
    order: int
    edges: tuple[tuple[int, int], ...]

    def __post_init__(self):
        if self.order < 0:
            raise ValueError("negative graph order")
        if len(set(self.edges)) != len(self.edges):
            raise ValueError("parallel edges")
        if any(not (0 <= u < v < self.order) for u, v in self.edges):
            raise ValueError("edges must be sorted, loop-free vertex pairs")


@dataclass(frozen=True)
class DAG:
    order: int
    arcs: tuple[tuple[int, int], ...]
    source: int
    sink: int


@dataclass(frozen=True)
class Gadget:
    weight: int
    dag: DAG
    graph: Graph
    source_terminal: int = 0
    sink_terminal: int = 1


@dataclass
class Expansion:
    graph: Graph
    original_order: int
    denominator: int
    integer_weights: dict[tuple[int, int], int]
    edge_owner: dict[tuple[int, int], tuple[int, int]]

    def project(self, matching: Iterable[tuple[int, int]]):
        """Push a perfect matching forward to its matching of original vertices.

        Checks the certificate, rather than assuming the supplied edges form
        a perfect matching.  The parity lemma guarantees each owner uses zero
        or both endpoints; checking that condition also catches malformed input.
        """
        matching = tuple(tuple(sorted(e)) for e in matching)
        seen = set()
        uses = {}
        for edge in matching:
            if edge not in self.edge_owner:
                raise ValueError("edge outside expansion")
            if any(v in seen for v in edge):
                raise ValueError("matching repeats a vertex")
            seen.update(edge)
            owner = self.edge_owner[edge]
            boundary = {v for v in edge if v < self.original_order}
            uses.setdefault(owner, set()).update(boundary)
        if seen != set(range(self.graph.order)):
            raise ValueError("matching is not perfect")
        answer = []
        for owner, used in uses.items():
            if used and used != set(owner):
                raise ValueError("gadget uses exactly one endpoint")
            if used:
                answer.append(owner)
        return tuple(sorted(answer))


def path_dag(weight: int) -> DAG:
    """Construct the O(log W) acyclic graph with W source-to-sink paths."""
    if not isinstance(weight, int) or weight < 1:
        raise ValueError("weight must be a positive integer")
    arcs = [(0, 1)]
    sink, order = 1, 2
    for bit in bin(weight)[3:]:  # omit the leading one
        a, z = order, order + 1
        arcs.extend(((sink, z), (sink, a), (a, z)))
        if bit == "1":
            arcs.append((0, z))
        sink, order = z, order + 2
    return DAG(order, tuple(arcs), 0, sink)


def dag_path_count(dag: DAG) -> int:
    """Independent dynamic program; vertex numbering is topological."""
    if len(set(dag.arcs)) != len(dag.arcs):
        raise ValueError("parallel arcs")
    if any(not (0 <= i < j < dag.order) for i, j in dag.arcs):
        raise ValueError("numbering is not topological")
    outgoing = [[] for _ in range(dag.order)]
    for i, j in dag.arcs:
        outgoing[i].append(j)
    counts = [0] * dag.order
    counts[dag.source] = 1
    for i in range(dag.order):
        for j in outgoing[i]:
            counts[j] += counts[i]
    return counts[dag.sink]


def integer_gadget(weight: int) -> Gadget:
    dag = path_dag(weight)
    left, right = {dag.source: 0}, {dag.sink: 1}
    edges, next_vertex = [], 2
    for v in range(dag.order):
        if v not in (dag.source, dag.sink):
            left[v], right[v] = next_vertex, next_vertex + 1
            next_vertex += 2
            edges.append((left[v], right[v]))
    for i, j in dag.arcs:
        edges.append(tuple(sorted((left[i], right[j]))))
    return Gadget(weight, dag, Graph(next_vertex, tuple(sorted(edges))))


def count_perfect_matchings(graph: Graph, removed: Iterable[int] = ()) -> int:
    """Exact subset enumeration with memoization; exponential worst-case time.

    The recurrence chooses a minimum-degree vertex and pairs it with each
    remaining neighbor.  Disconnected components are counted separately.
    """
    removed = set(removed)
    if any(not (0 <= v < graph.order) for v in removed):
        raise ValueError("invalid removed vertex")
    adjacency = [0] * graph.order
    for u, v in graph.edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    initial = ((1 << graph.order) - 1)
    for v in removed:
        initial &= ~(1 << v)

    @lru_cache(None)
    def count(mask):
        if not mask:
            return 1
        if mask.bit_count() % 2:
            return 0
        candidates = mask
        minimum_degree, chosen, neighbors = graph.order + 1, None, None
        while candidates:
            low = candidates & -candidates
            v = low.bit_length() - 1
            candidates ^= low
            available = adjacency[v] & mask
            degree = available.bit_count()
            if degree == 0:
                return 0
            if degree < minimum_degree:
                minimum_degree, chosen, neighbors = degree, v, available
                if degree == 1:
                    break
        # Split connected components before branching.  This reduces runtime
        # for boundary checks but is only an optimization of exact enumeration.
        component, frontier = 0, 1 << chosen
        while frontier:
            component |= frontier
            expanded = 0
            scan = frontier
            while scan:
                low = scan & -scan
                scan ^= low
                expanded |= adjacency[low.bit_length() - 1]
            frontier = expanded & mask & ~component
        if component != mask:
            return count(component) * count(mask ^ component)
        total = 0
        while neighbors:
            low = neighbors & -neighbors
            neighbors ^= low
            total += count(mask ^ (1 << chosen) ^ low)
        return total

    return count(initial)


def enumerate_perfect_matchings(graph: Graph):
    """Yield each matching exactly once; only for genuinely small checks."""
    adjacency = [set() for _ in range(graph.order)]
    for u, v in graph.edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    def visit(remaining):
        if not remaining:
            yield ()
            return
        u = min(remaining)
        for v in sorted(adjacency[u] & remaining):
            edge = tuple(sorted((u, v)))
            for rest in visit(remaining - {u, v}):
                yield (edge,) + rest

    yield from visit(set(range(graph.order)))


def normalized_matrix(matrix: Sequence[Sequence[Fraction | int]]):
    """Validate exact rational off-diagonal entries; ignore every diagonal."""
    n = len(matrix)
    if n % 2:
        raise ValueError("hafnian matrix order must be even")
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix must be square")
    result = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            value = matrix[i][j]
            if not isinstance(value, (int, Fraction)):
                raise ValueError("use integers or exact Fraction entries")
            result[i][j] = Fraction(value)
            if result[i][j] < 0:
                raise ValueError("off-diagonal entries must be nonnegative")
    if any(result[i][j] != result[j][i] for i in range(n) for j in range(i)):
        raise ValueError("matrix must have symmetric off-diagonal entries")
    return result


def exact_hafnian(matrix: Sequence[Sequence[Fraction | int]]) -> Fraction:
    """Exact original matching recurrence; exponential worst-case time."""
    matrix = normalized_matrix(matrix)

    @lru_cache(None)
    def count(vertices):
        if not vertices:
            return Fraction(1)
        i, others = vertices[0], vertices[1:]
        return sum((matrix[i][j] * count(tuple(v for v in others if v != j))
                    for j in others), Fraction(0))

    return count(tuple(range(len(matrix))))


def expand_rational_matrix(matrix: Sequence[Sequence[Fraction | int]]) -> Expansion:
    matrix = normalized_matrix(matrix)
    n = len(matrix)
    support = {(i, j): matrix[i][j] for i in range(n)
               for j in range(i + 1, n) if matrix[i][j] > 0}
    denominator = 1
    for value in support.values():
        denominator *= value.denominator
    integer_weights = {e: value.numerator * (denominator // value.denominator)
                       for e, value in support.items()}
    edges, edge_owner, next_vertex = [], {}, n
    for (u, v), weight in integer_weights.items():
        gadget = integer_gadget(weight)
        names = {0: u, 1: v}
        for local in range(2, gadget.graph.order):
            names[local] = next_vertex
            next_vertex += 1
        for i, j in gadget.graph.edges:
            edge = tuple(sorted((names[i], names[j])))
            if edge in edge_owner:
                raise AssertionError("unexpected edge collision")
            edges.append(edge)
            edge_owner[edge] = (u, v)
    return Expansion(Graph(next_vertex, tuple(sorted(edges))), n,
                     denominator, integer_weights, edge_owner)


def gadget_signature(weight: int):
    gadget = integer_gadget(weight)
    return tuple(count_perfect_matchings(gadget.graph, removed) for removed in
                 ((), (0, 1), (0,), (1,)))
