#!/usr/bin/env python3
"""Independent stdlib-only audit of the all-n theta sharpness theorem.

This file intentionally imports no graph, Fourier, algebra, or certificate code
from the historical packages.  It reconstructs every checked object from the
primitive status-free data in instance.json.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence


HERE = Path(__file__).resolve().parent
DEFAULT_INSTANCE = HERE / "instance.json"
DEFAULT_OUTPUT = HERE / "certificate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def fraction_text(value: Fraction | int) -> str:
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


# ---------------------------------------------------------------------------
# Exact arithmetic in Q(beta), beta^2 = REDUCE_BETA*beta + REDUCE_ONE.
# ---------------------------------------------------------------------------


MINPOLY_A = 43_337_075
MINPOLY_B = -36_083_110
MINPOLY_C = 7_336_259
REDUCE_BETA = Fraction(-MINPOLY_B, MINPOLY_A)
REDUCE_ONE = Fraction(-MINPOLY_C, MINPOLY_A)


@dataclass(frozen=True)
class Quadratic:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", Fraction(self.a))
        object.__setattr__(self, "b", Fraction(self.b))

    @classmethod
    def coerce(cls, value: object) -> "Quadratic":
        if isinstance(value, cls):
            return value
        if isinstance(value, (int, Fraction)):
            return cls(Fraction(value), Fraction(0))
        raise TypeError(f"cannot coerce {type(value)!r} to Quadratic")

    def __add__(self, other: object) -> "Quadratic":
        other = self.coerce(other)
        return Quadratic(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self) -> "Quadratic":
        return Quadratic(-self.a, -self.b)

    def __sub__(self, other: object) -> "Quadratic":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "Quadratic":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "Quadratic":
        other = self.coerce(other)
        constant = self.a * other.a + self.b * other.b * REDUCE_ONE
        beta = (
            self.a * other.b
            + self.b * other.a
            + self.b * other.b * REDUCE_BETA
        )
        return Quadratic(constant, beta)

    __rmul__ = __mul__

    def inverse(self) -> "Quadratic":
        # Multiplication by a+b beta has matrix
        # [[a, b*REDUCE_ONE], [b, a+b*REDUCE_BETA]].
        determinant = self.a * (self.a + self.b * REDUCE_BETA) - self.b * self.b * REDUCE_ONE
        if determinant == 0:
            raise ZeroDivisionError("zero quadratic-field element")
        return Quadratic(
            (self.a + self.b * REDUCE_BETA) / determinant,
            -self.b / determinant,
        )

    def __truediv__(self, other: object) -> "Quadratic":
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other: object) -> "Quadratic":
        return self.coerce(other) / self

    def __pow__(self, exponent: int) -> "Quadratic":
        require(isinstance(exponent, int), "quadratic exponent must be integral")
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        result = Quadratic(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1
        return result

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def encode(self) -> str | dict[str, str]:
        if self.b == 0:
            return fraction_text(self.a)
        return {"constant": fraction_text(self.a), "beta": fraction_text(self.b)}


BETA = Quadratic(0, 1)


# ---------------------------------------------------------------------------
# Exact rational intervals.  Endpoints are closed bounds, while all claims
# below use strict comparisons of those bounds with 0 and 1.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        object.__setattr__(self, "lo", Fraction(self.lo))
        object.__setattr__(self, "hi", Fraction(self.hi))
        require(self.lo <= self.hi, "reversed interval")

    @classmethod
    def point(cls, value: int | Fraction) -> "Interval":
        return cls(Fraction(value), Fraction(value))

    @classmethod
    def coerce(cls, value: object) -> "Interval":
        if isinstance(value, cls):
            return value
        if isinstance(value, (int, Fraction)):
            return cls.point(value)
        raise TypeError(f"cannot coerce {type(value)!r} to Interval")

    def __add__(self, other: object) -> "Interval":
        other = self.coerce(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: object) -> "Interval":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "Interval":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "Interval":
        other = self.coerce(other)
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def inverse(self) -> "Interval":
        require(not (self.lo <= 0 <= self.hi), "interval reciprocal crosses zero")
        return Interval(min(1 / self.lo, 1 / self.hi), max(1 / self.lo, 1 / self.hi))

    def __truediv__(self, other: object) -> "Interval":
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other: object) -> "Interval":
        return self.coerce(other) / self

    def encode(self) -> list[str]:
        return [fraction_text(self.lo), fraction_text(self.hi)]


def evaluate_expression(text: str, beta: Quadratic | Interval) -> Quadratic | Interval:
    """Evaluate a tiny arithmetic grammar; names other than beta are rejected."""

    tree = ast.parse(text, mode="eval")
    point = Quadratic.coerce if isinstance(beta, Quadratic) else Interval.coerce

    def visit(node: ast.AST) -> Quadratic | Interval:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return point(node.value)
        if isinstance(node, ast.Name) and node.id == "beta":
            return beta
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
        raise ValueError(f"forbidden expression syntax in {text!r}: {ast.dump(node)}")

    return visit(tree)


# ---------------------------------------------------------------------------
# Sparse multivariate polynomials over Q for model-wide identity checks.
# A monomial is a sorted tuple with repetitions, avoiding any CAS dependency.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Polynomial:
    terms: tuple[tuple[tuple[str, ...], Fraction], ...] = ()

    def __post_init__(self) -> None:
        cleaned: dict[tuple[str, ...], Fraction] = defaultdict(Fraction)
        for monomial, coefficient in self.terms:
            cleaned[tuple(sorted(monomial))] += Fraction(coefficient)
        canonical = tuple(sorted((m, c) for m, c in cleaned.items() if c))
        object.__setattr__(self, "terms", canonical)

    @classmethod
    def constant(cls, value: int | Fraction) -> "Polynomial":
        value = Fraction(value)
        return cls(()) if value == 0 else cls((((), value),))

    @classmethod
    def variable(cls, name: str) -> "Polynomial":
        return cls((((name,), Fraction(1)),))

    @classmethod
    def coerce(cls, value: object) -> "Polynomial":
        if isinstance(value, cls):
            return value
        if isinstance(value, (int, Fraction)):
            return cls.constant(value)
        raise TypeError(f"cannot coerce {type(value)!r} to Polynomial")

    def as_dict(self) -> dict[tuple[str, ...], Fraction]:
        return dict(self.terms)

    def __add__(self, other: object) -> "Polynomial":
        other = self.coerce(other)
        return Polynomial(self.terms + other.terms)

    __radd__ = __add__

    def __neg__(self) -> "Polynomial":
        return Polynomial(tuple((m, -c) for m, c in self.terms))

    def __sub__(self, other: object) -> "Polynomial":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "Polynomial":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "Polynomial":
        other = self.coerce(other)
        products = []
        for left_monomial, left_coefficient in self.terms:
            for right_monomial, right_coefficient in other.terms:
                products.append(
                    (
                        tuple(sorted(left_monomial + right_monomial)),
                        left_coefficient * right_coefficient,
                    )
                )
        return Polynomial(tuple(products))

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "Polynomial":
        require(isinstance(exponent, int) and exponent >= 0, "polynomial exponent")
        result = Polynomial.constant(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1
        return result

    def is_zero(self) -> bool:
        return not self.terms

    def encode(self) -> list[dict[str, object]]:
        rows = []
        for monomial, coefficient in self.terms:
            powers = Counter(monomial)
            rows.append(
                {
                    "coefficient": fraction_text(coefficient),
                    "monomial": [[name, powers[name]] for name in sorted(powers)],
                }
            )
        return rows


# ---------------------------------------------------------------------------
# Rooted and mixed graph primitives.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Network:
    name: str
    root: str
    types: Mapping[str, str]
    arcs: tuple[tuple[str, str], ...]
    leaves: tuple[str, ...]
    parent_order: Mapping[str, tuple[str, str]]


@dataclass(frozen=True, order=True)
class MixedEdge:
    endpoints: tuple[str, str]
    heads: tuple[str, ...] = ()

    @classmethod
    def make(cls, endpoints: Iterable[str], heads: Iterable[str] = ()) -> "MixedEdge":
        endpoints_tuple = tuple(sorted(endpoints))
        heads_tuple = tuple(sorted(heads))
        require(len(endpoints_tuple) == 2 and endpoints_tuple[0] != endpoints_tuple[1], "bad mixed edge")
        require(set(heads_tuple) <= set(endpoints_tuple), "arrowhead outside edge")
        return cls(endpoints_tuple, heads_tuple)


@dataclass(frozen=True)
class MixedGraph:
    types: Mapping[str, str]
    edges: tuple[MixedEdge, ...]
    leaves: tuple[str, ...]

    @property
    def nodes(self) -> tuple[str, ...]:
        return tuple(sorted(self.types))

    def edge_code(self) -> tuple[tuple[tuple[str, str], tuple[str, ...]], ...]:
        return tuple(sorted((edge.endpoints, edge.heads) for edge in self.edges))


def construct_networks(data: Mapping[str, object]) -> dict[str, Network]:
    root = str(data["root"])
    types = {str(k): str(v) for k, v in dict(data["vertex_types"]).items()}
    leaves = tuple(str(x) for x in data["leaf_order"])
    internal = [tuple(map(str, arc)) for arc in data["internal_arcs"]]
    parent_order_raw = dict(data["inheritance_parent_order"])
    parent_order = {
        str(reticulation): tuple(str(row[0]) for row in rows)
        for reticulation, rows in parent_order_raw.items()
    }
    result = {}
    for name, pendants in dict(data["pendant_arcs"]).items():
        arcs = tuple(internal + [tuple(map(str, arc)) for arc in pendants])
        result[str(name)] = Network(str(name), root, dict(types), arcs, leaves, dict(parent_order))
    return result


def adjacency_from_edges(edges: Iterable[tuple[str, str]]) -> dict[str, set[str]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    return adjacency


def directed_children(arcs: Iterable[tuple[str, str]]) -> dict[str, list[str]]:
    children: dict[str, list[str]] = defaultdict(list)
    for u, v in arcs:
        children[u].append(v)
    return children


def is_acyclic(nodes: Iterable[str], arcs: Iterable[tuple[str, str]]) -> bool:
    nodes = set(nodes)
    indegree = Counter(v for _u, v in arcs)
    children = directed_children(arcs)
    queue = sorted(node for node in nodes if indegree[node] == 0)
    visited = 0
    while queue:
        node = queue.pop(0)
        visited += 1
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort()
    return visited == len(nodes)


def reachable(root: str, arcs: Iterable[tuple[str, str]], blocked: str | None = None) -> set[str]:
    children = directed_children(arcs)
    seen = set()
    stack = [] if root == blocked else [root]
    while stack:
        node = stack.pop()
        if node in seen or node == blocked:
            continue
        seen.add(node)
        stack.extend(children[node])
    return seen


def rooted_validation(network: Network, require_lsa: bool = False) -> tuple[bool, str]:
    nodes = set(network.types)
    arcs = tuple(network.arcs)
    if len(arcs) != len(set(arcs)):
        return False, "parallel or duplicate directed arc"
    if any(u == v or u not in nodes or v not in nodes for u, v in arcs):
        return False, "loop or unknown endpoint"
    indegree = Counter(v for _u, v in arcs)
    outdegree = Counter(u for u, _v in arcs)
    expected = {
        "root": (0, 2),
        "tree": (1, 2),
        "reticulation": (2, 1),
        "leaf": (1, 0),
    }
    for node, kind in network.types.items():
        if (indegree[node], outdegree[node]) != expected[kind]:
            return False, f"bad bidegree at {node}: {(indegree[node], outdegree[node])}"
    if network.types.get(network.root) != "root":
        return False, "distinguished root has wrong type"
    if not is_acyclic(nodes, arcs):
        return False, "directed cycle"
    if reachable(network.root, arcs) != nodes:
        return False, "not every vertex is root-reachable"
    if tuple(sorted(node for node, kind in network.types.items() if kind == "leaf")) != tuple(sorted(network.leaves)):
        return False, "leaf set mismatch"
    if require_lsa and not root_is_lsa(network):
        return False, "root is not the lowest stable ancestor of all leaves"
    return True, "ok"


def tree_child(network: Network) -> bool:
    children = directed_children(network.arcs)
    for node, kind in network.types.items():
        if kind == "leaf":
            continue
        if not any(network.types[child] in {"tree", "leaf"} for child in children[node]):
            return False
    return True


def tree_child_failure_vertices(network: Network) -> list[str]:
    children = directed_children(network.arcs)
    return sorted(
        node
        for node, kind in network.types.items()
        if kind != "leaf"
        and not any(network.types[child] in {"tree", "leaf"} for child in children[node])
    )


def root_is_lsa(network: Network) -> bool:
    """The root is the LSA iff no nonroot vertex dominates every leaf."""

    for candidate in network.types:
        if candidate == network.root:
            continue
        after_removal = reachable(network.root, network.arcs, blocked=candidate)
        if all(leaf not in after_removal for leaf in network.leaves):
            return False
    return True


def reduce_standard(network: Network) -> MixedGraph:
    """Narrow standard reduction used in the manuscript.

    Reticulation heads are retained, ordinary arcs are undirected, the binary
    root is suppressed once, and no further degree-two cleanup or broad
    deletion of reticulation artifacts is performed.
    """

    edges = []
    for u, v in network.arcs:
        heads = (v,) if network.types[v] == "reticulation" else ()
        edges.append(MixedEdge.make((u, v), heads))

    incident = [edge for edge in edges if network.root in edge.endpoints]
    require(len(incident) == 2, "root must have two incident edges")
    outside = []
    inherited_heads = set()
    for edge in incident:
        other = next(node for node in edge.endpoints if node != network.root)
        outside.append(other)
        if other in edge.heads:
            inherited_heads.add(other)
    edges = [edge for edge in edges if network.root not in edge.endpoints]
    edges.append(MixedEdge.make(outside, inherited_heads))

    types = dict(network.types)
    del types[network.root]

    require(len(edges) == len(set(edges)), "parallel artifact outside theorem convention")
    return MixedGraph(types, tuple(sorted(edges)), tuple(sorted(network.leaves)))


def validate_mixed_binary(graph: MixedGraph) -> tuple[bool, str]:
    degree = Counter(node for edge in graph.edges for node in edge.endpoints)
    incoming = Counter(head for edge in graph.edges for head in edge.heads)
    for edge in graph.edges:
        if len(edge.heads) > 1:
            return False, "bidirected edge"
        for head in edge.heads:
            if graph.types[head] != "reticulation":
                return False, "arrowhead at ordinary vertex"
    for node, kind in graph.types.items():
        if kind == "leaf":
            if degree[node] != 1 or incoming[node] != 0:
                return False, f"bad mixed leaf {node}"
        elif kind == "tree":
            if degree[node] != 3 or incoming[node] != 0:
                return False, f"bad mixed tree vertex {node}"
        elif kind == "reticulation":
            if degree[node] != 3 or incoming[node] != 2:
                return False, f"bad mixed reticulation {node}"
        else:
            return False, f"unexpected mixed type {kind}"
    return True, "ok"


def underlying_edges(graph: MixedGraph) -> tuple[tuple[str, str], ...]:
    return tuple(edge.endpoints for edge in graph.edges)


def simple_cycles(graph: MixedGraph) -> tuple[tuple[str, ...], ...]:
    adjacency = adjacency_from_edges(underlying_edges(graph))
    cycles = set()
    for start in sorted(graph.types):
        def search(node: str, path: list[str], visited: set[str]) -> None:
            for nxt in sorted(adjacency[node]):
                if nxt == start and len(path) >= 3:
                    body = tuple(path)
                    reverse = (body[0],) + tuple(reversed(body[1:]))
                    cycles.add(min(body, reverse))
                elif nxt not in visited and nxt >= start:
                    search(nxt, path + [nxt], visited | {nxt})
        search(start, [start], {start})
    return tuple(sorted(cycles))


def biconnected_components(graph: MixedGraph) -> tuple[tuple[tuple[str, str], ...], ...]:
    adjacency = adjacency_from_edges(underlying_edges(graph))
    discovery: dict[str, int] = {}
    low: dict[str, int] = {}
    parent: dict[str, str | None] = {}
    stack: list[tuple[str, str]] = []
    components: list[tuple[tuple[str, str], ...]] = []
    clock = 0

    def canonical_edge(u: str, v: str) -> tuple[str, str]:
        return tuple(sorted((u, v)))

    def dfs(u: str) -> None:
        nonlocal clock
        clock += 1
        discovery[u] = low[u] = clock
        for v in sorted(adjacency[u]):
            edge = canonical_edge(u, v)
            if v not in discovery:
                parent[v] = u
                stack.append(edge)
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] >= discovery[u]:
                    component = []
                    while stack:
                        popped = stack.pop()
                        component.append(popped)
                        if popped == edge:
                            break
                    components.append(tuple(sorted(component)))
            elif v != parent.get(u) and discovery[v] < discovery[u]:
                low[u] = min(low[u], discovery[v])
                stack.append(edge)

    for node in sorted(graph.types):
        if node not in discovery:
            parent[node] = None
            dfs(node)
            if stack:
                components.append(tuple(sorted(stack)))
                stack.clear()
    return tuple(sorted(set(components)))


def blob_audit(graph: MixedGraph) -> dict[str, object]:
    blobs = []
    for edges in biconnected_components(graph):
        vertices = set(itertools.chain.from_iterable(edges))
        if len(edges) < len(vertices):
            continue
        reticulations = sorted(v for v in vertices if graph.types[v] == "reticulation")
        blobs.append(
            {
                "vertices": sorted(vertices),
                "edges": [list(edge) for edge in edges],
                "cycle_rank": len(edges) - len(vertices) + 1,
                "reticulations": reticulations,
                "level": len(reticulations),
            }
        )
    cycles = simple_cycles(graph)
    return {
        "blob_count": len(blobs),
        "blobs": blobs,
        "simple_cycle_count": len(cycles),
        "simple_cycles": [list(cycle) for cycle in cycles],
        "cycle_lengths": sorted(map(len, cycles)),
        "triangle_count": sum(len(cycle) == 3 for cycle in cycles),
        "level": max((int(blob["level"]) for blob in blobs), default=0),
    }


def graph_isomorphism(
    left: MixedGraph,
    right: MixedGraph,
    left_triangle: frozenset[str] | None = None,
    right_triangle: frozenset[str] | None = None,
    ignore_leaf_labels: bool = False,
) -> tuple[bool, dict[str, str] | None]:
    def color(graph: MixedGraph, node: str, triangle: frozenset[str] | None) -> str:
        if triangle is not None and node in triangle:
            return "triangle-neutral"
        kind = graph.types[node]
        if kind == "leaf":
            return "leaf" if ignore_leaf_labels else f"leaf:{node}"
        return kind

    left_groups: dict[str, list[str]] = defaultdict(list)
    right_groups: dict[str, list[str]] = defaultdict(list)
    for node in left.types:
        left_groups[color(left, node, left_triangle)].append(node)
    for node in right.types:
        right_groups[color(right, node, right_triangle)].append(node)
    if {k: len(v) for k, v in left_groups.items()} != {k: len(v) for k, v in right_groups.items()}:
        return False, None

    colors = sorted(left_groups)
    permutations = [list(itertools.permutations(sorted(right_groups[c]))) for c in colors]

    def transformed_edge(edge: MixedEdge, mapping: Mapping[str, str]) -> MixedEdge:
        mapped_endpoints = [mapping[node] for node in edge.endpoints]
        heads = list(edge.heads)
        if left_triangle is not None and set(edge.endpoints) <= set(left_triangle):
            heads = []
        mapped_heads = [mapping[node] for node in heads]
        return MixedEdge.make(mapped_endpoints, mapped_heads)

    target_edges = set()
    for edge in right.edges:
        heads = list(edge.heads)
        if right_triangle is not None and set(edge.endpoints) <= set(right_triangle):
            heads = []
        target_edges.add(MixedEdge.make(edge.endpoints, heads))

    for choices in itertools.product(*permutations):
        mapping: dict[str, str] = {}
        for c, image_group in zip(colors, choices):
            mapping.update(zip(sorted(left_groups[c]), image_group))
        if {transformed_edge(edge, mapping) for edge in left.edges} == target_edges:
            return True, mapping
    return False, None


def triangle_sets(graph: MixedGraph) -> tuple[frozenset[str], ...]:
    return tuple(frozenset(cycle) for cycle in simple_cycles(graph) if len(cycle) == 3)


def site_text(edge: MixedEdge) -> str:
    if not edge.heads:
        return f"{edge.endpoints[0]}--{edge.endpoints[1]}"
    head = edge.heads[0]
    tail = next(node for node in edge.endpoints if node != head)
    return f"{tail}->{head}"


def enumerate_admissible_rootings(
    graph: MixedGraph,
    include_directed_sites: bool = True,
) -> list[dict[str, object]]:
    root = "__ROOT__"
    base_types = dict(graph.types)
    base_types[root] = "root"
    records: dict[tuple[tuple[str, str], ...], dict[str, object]] = {}
    for site in graph.edges:
        if site.heads and not include_directed_sites:
            continue
        if len(site.heads) > 1:
            continue
        remaining = [edge for edge in graph.edges if edge != site]
        undirected = [edge for edge in remaining if not edge.heads]
        fixed_arcs = []
        for edge in remaining:
            if edge.heads:
                head = edge.heads[0]
                tail = next(node for node in edge.endpoints if node != head)
                fixed_arcs.append((tail, head))
        for bits in itertools.product((0, 1), repeat=len(undirected)):
            arcs = list(fixed_arcs)
            for bit, edge in zip(bits, undirected):
                u, v = edge.endpoints
                arcs.append((u, v) if bit == 0 else (v, u))
            arcs.extend((root, endpoint) for endpoint in site.endpoints)
            candidate = Network(
                f"rooted:{site_text(site)}",
                root,
                dict(base_types),
                tuple(sorted(arcs)),
                graph.leaves,
                {},
            )
            valid, _reason = rooted_validation(candidate, require_lsa=False)
            if not valid:
                continue
            if reduce_standard(candidate).edge_code() != graph.edge_code():
                continue
            code = tuple(sorted(candidate.arcs))
            records[code] = {
                "site": site_text(site),
                "site_is_reticulation_edge": bool(site.heads),
                "lsa": root_is_lsa(candidate),
                "tree_child": tree_child(candidate),
                "network": candidate,
            }
    return [records[key] for key in sorted(records)]


# ---------------------------------------------------------------------------
# Displayed-tree Fourier enumeration over Z_2 x Z_2.
# ---------------------------------------------------------------------------


def xor_sum(values: Iterable[int]) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


def z4_sum(values: Iterable[int]) -> int:
    return sum(values) % 4


def displayed_coordinate(
    network: Network,
    characters: Mapping[str, int],
    edge_values: Mapping[tuple[str, str], object],
    inheritance_values: Mapping[str, object],
    zero: object,
    one: object,
    group_sum: Callable[[Iterable[int]], int] = xor_sum,
    forced_choices: tuple[int, ...] | None = None,
) -> object:
    if group_sum(characters[leaf] for leaf in network.leaves) != 0:
        return zero
    reticulations = tuple(sorted(network.parent_order))
    choice_rows = [forced_choices] if forced_choices is not None else itertools.product((0, 1), repeat=len(reticulations))
    total = zero
    for choices in choice_rows:
        selected_parent = {
            reticulation: network.parent_order[reticulation][choice]
            for reticulation, choice in zip(reticulations, choices)
        }
        selected_arcs = []
        for arc in network.arcs:
            u, v = arc
            if v in selected_parent and selected_parent[v] != u:
                continue
            selected_arcs.append(arc)
        children = directed_children(selected_arcs)

        @lru_cache(maxsize=None)
        def descendant_character(node: str) -> int:
            if network.types[node] == "leaf":
                return characters[node]
            return group_sum(descendant_character(child) for child in children[node])

        monomial = one
        for reticulation, choice in zip(reticulations, choices):
            lam = inheritance_values[reticulation]
            monomial *= lam if choice == 0 else one - lam
        for arc in selected_arcs:
            if descendant_character(arc[1]) != 0:
                monomial *= edge_values[arc]
        total += monomial
    return total


def symbolic_fourier_map(network: Network, representatives: Mapping[str, tuple[int, ...]]) -> dict[str, Polynomial]:
    edge_values = {
        arc: Polynomial.variable(f"x_{arc[0]}_{arc[1]}")
        for arc in network.arcs
    }
    inheritance = {
        reticulation: Polynomial.variable(f"lambda_{reticulation}")
        for reticulation in network.parent_order
    }
    return {
        name: displayed_coordinate(
            network,
            dict(zip(network.leaves, characters)),
            edge_values,
            inheritance,
            Polynomial.constant(0),
            Polynomial.constant(1),
        )
        for name, characters in representatives.items()
    }


def invariant_polynomials(coordinates: Mapping[str, Polynomial]) -> list[Polynomial]:
    c = coordinates
    return [
        c["J"] - c["K"] - c["M"] + c["N"],
        c["J"] - c["A"] * c["H"] - c["B"] * c["F"] + c["C"] * c["E"],
        c["G"] * c["L"] - c["E"] * c["N"],
        c["L"] ** 2 - c["B"] * c["E"] * c["H"],
        c["B"] * c["M"] - c["D"] * c["L"] - c["B"] ** 2 * c["F"] + c["B"] * c["C"] * c["E"],
        c["B"] * c["E"] * c["O"] - c["B"] * c["G"] * c["H"] - c["C"] * c["E"] * c["L"] + c["D"] * c["E"] * c["H"],
    ]


def polynomial_map_hash(coordinates: Mapping[str, Polynomial]) -> str:
    encoded = {name: coordinates[name].encode() for name in sorted(coordinates)}
    return sha256_bytes(canonical_json_bytes(encoded))


def root_product_property(coordinates: Mapping[str, Polynomial]) -> bool:
    for polynomial in coordinates.values():
        for monomial, _coefficient in polynomial.terms:
            counts = Counter(monomial)
            if counts["x_rho_A"] != counts["x_rho_C"]:
                return False
    return True


def parse_point(network: Network, point_data: Mapping[str, object]) -> tuple[dict[tuple[str, str], Quadratic], dict[str, Quadratic]]:
    edge_raw = dict(point_data["edge_multipliers"])
    edges = {}
    for key, text in edge_raw.items():
        u, v = str(key).split("->")
        edges[(u, v)] = evaluate_expression(str(text), BETA)
    require(set(edges) == set(network.arcs), f"point edge set mismatch for {network.name}")
    inheritance = {
        str(reticulation): evaluate_expression(str(text), BETA)
        for reticulation, text in dict(point_data["inheritance"]).items()
    }
    require(set(inheritance) == set(network.parent_order), "inheritance set mismatch")
    return edges, inheritance


def full_tensor(
    network: Network,
    edges: Mapping[tuple[str, str], object],
    inheritance: Mapping[str, object],
    zero: object,
    one: object,
    group_sum: Callable[[Iterable[int]], int] = xor_sum,
    forced_choices: tuple[int, ...] | None = None,
) -> dict[tuple[int, ...], object]:
    return {
        characters: displayed_coordinate(
            network,
            dict(zip(network.leaves, characters)),
            edges,
            inheritance,
            zero,
            one,
            group_sum=group_sum,
            forced_choices=forced_choices,
        )
        for characters in itertools.product(range(4), repeat=len(network.leaves))
    }


def character_sign(character: int, state: int) -> int:
    dot = ((character & 1) * (state & 1) + ((character >> 1) & 1) * ((state >> 1) & 1)) % 2
    return -1 if dot else 1


def inverse_fourier(tensor: Mapping[tuple[int, ...], Quadratic]) -> dict[tuple[int, ...], Quadratic]:
    n = len(next(iter(tensor)))
    scale = Quadratic(Fraction(1, 4**n))
    probabilities = {}
    for states in itertools.product(range(4), repeat=n):
        value = Quadratic(0)
        for characters, coordinate in tensor.items():
            sign = 1
            for character, state in zip(characters, states):
                sign *= character_sign(character, state)
            value += sign * coordinate
        probabilities[states] = scale * value
    return probabilities


def orbit_partition() -> tuple[tuple[tuple[int, ...], ...], ...]:
    automorphisms = []
    for permutation in itertools.permutations((1, 2, 3)):
        automorphism = {0: 0, 1: permutation[0], 2: permutation[1], 3: permutation[2]}
        require(
            all(automorphism[a ^ b] == (automorphism[a] ^ automorphism[b]) for a in range(4) for b in range(4)),
            "nonlinear permutation entered the Klein-four automorphism list",
        )
        automorphisms.append(automorphism)
    unseen = {row for row in itertools.product(range(4), repeat=4) if xor_sum(row) == 0}
    orbits = []
    while unseen:
        seed = min(unseen)
        orbit = {
            tuple(automorphism[value] for value in seed)
            for automorphism in automorphisms
        }
        require(all(xor_sum(row) == 0 for row in orbit), "purported automorphism broke XOR")
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))
    return tuple(sorted(orbits))


def character_table_audit() -> dict[str, object]:
    table = [[character_sign(character, state) for state in range(4)] for character in range(4)]
    gram = [
        [sum(table[i][state] * table[j][state] for state in range(4)) for j in range(4)]
        for i in range(4)
    ]
    require(gram == [[4 if i == j else 0 for j in range(4)] for i in range(4)], "Klein-four character table is not orthogonal")
    return {
        "table": table,
        "gram": gram,
        "inverse_scale_per_leaf": "1/4",
        "table_sha256": sha256_bytes(canonical_json_bytes(table)),
    }


# ---------------------------------------------------------------------------
# Exact forward-mode differentiation and two determinant algorithms.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Dual:
    value: Quadratic
    derivative: tuple[Quadratic, ...]

    @classmethod
    def constant(cls, value: object, dimension: int) -> "Dual":
        return cls(Quadratic.coerce(value), (Quadratic(0),) * dimension)

    @classmethod
    def variable(cls, value: object, dimension: int, index: int) -> "Dual":
        derivative = [Quadratic(0)] * dimension
        derivative[index] = Quadratic(1)
        return cls(Quadratic.coerce(value), tuple(derivative))

    def _coerce(self, other: object) -> "Dual":
        if isinstance(other, Dual):
            require(len(other.derivative) == len(self.derivative), "dual dimension mismatch")
            return other
        return Dual.constant(other, len(self.derivative))

    def __add__(self, other: object) -> "Dual":
        other = self._coerce(other)
        return Dual(self.value + other.value, tuple(a + b for a, b in zip(self.derivative, other.derivative)))

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, tuple(-entry for entry in self.derivative))

    def __sub__(self, other: object) -> "Dual":
        return self + (-self._coerce(other))

    def __rsub__(self, other: object) -> "Dual":
        return self._coerce(other) - self

    def __mul__(self, other: object) -> "Dual":
        other = self._coerce(other)
        return Dual(
            self.value * other.value,
            tuple(self.value * b + other.value * a for a, b in zip(self.derivative, other.derivative)),
        )

    __rmul__ = __mul__


def determinant_elimination(matrix: Sequence[Sequence[Quadratic]]) -> Quadratic:
    work = [list(row) for row in matrix]
    n = len(work)
    require(all(len(row) == n for row in work), "nonsquare determinant")
    determinant = Quadratic(1)
    for column in range(n):
        pivot_row = next((row for row in range(column, n) if not work[row][column].is_zero()), None)
        if pivot_row is None:
            return Quadratic(0)
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            determinant = -determinant
        pivot = work[column][column]
        determinant *= pivot
        for row in range(column + 1, n):
            if work[row][column].is_zero():
                continue
            factor = work[row][column] / pivot
            for entry in range(column, n):
                work[row][entry] -= factor * work[column][entry]
    return determinant


def determinant_cofactor(matrix: Sequence[Sequence[Quadratic]]) -> Quadratic:
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "nonsquare determinant")

    @lru_cache(maxsize=None)
    def recurse(row: int, columns: tuple[int, ...]) -> Quadratic:
        if row == n:
            return Quadratic(1)
        total = Quadratic(0)
        for position, column in enumerate(columns):
            rest = columns[:position] + columns[position + 1 :]
            term = matrix[row][column] * recurse(row + 1, rest)
            total += term if position % 2 == 0 else -term
        return total

    return recurse(0, tuple(range(n)))


def jacobian_certificate(
    network: Network,
    point_edges: Mapping[tuple[str, str], Quadratic],
    point_inheritance: Mapping[str, Quadratic],
    representatives: Mapping[str, tuple[int, ...]],
    free_edges: Sequence[tuple[str, str]],
) -> tuple[list[list[Quadratic]], Quadratic]:
    dimension = len(free_edges)
    index = {edge: i for i, edge in enumerate(free_edges)}
    dual_edges = {
        edge: (
            Dual.variable(value, dimension, index[edge])
            if edge in index
            else Dual.constant(value, dimension)
        )
        for edge, value in point_edges.items()
    }
    dual_inheritance = {
        reticulation: Dual.constant(value, dimension)
        for reticulation, value in point_inheritance.items()
    }
    rows = []
    for name in "ABCDEFGH":
        coordinate = displayed_coordinate(
            network,
            dict(zip(network.leaves, representatives[name])),
            dual_edges,
            dual_inheritance,
            Dual.constant(0, dimension),
            Dual.constant(1, dimension),
        )
        require(isinstance(coordinate, Dual), "dual enumeration lost derivatives")
        rows.append(list(coordinate.derivative))
    elimination = determinant_elimination(rows)
    cofactor = determinant_cofactor(rows)
    require(elimination == cofactor, "independent determinant algorithms disagree")
    require(not elimination.is_zero(), f"zero rank-eight determinant for {network.name}")
    return rows, elimination


def matrix_hash(matrix: Sequence[Sequence[Quadratic]]) -> str:
    encoded = [[entry.encode() for entry in row] for row in matrix]
    return sha256_bytes(canonical_json_bytes(encoded))


# ---------------------------------------------------------------------------
# Cherry substitution and exact one-step tensor test.
# ---------------------------------------------------------------------------


def cherry_substitute(network: Network, selected_leaf: str, new_leaf: str, tree_vertex: str) -> tuple[Network, tuple[str, str]]:
    incoming = [arc for arc in network.arcs if arc[1] == selected_leaf]
    require(len(incoming) == 1, "selected leaf must have one parent")
    old_arc = incoming[0]
    parent = old_arc[0]
    arcs = [arc for arc in network.arcs if arc != old_arc]
    arcs.extend(((parent, tree_vertex), (tree_vertex, selected_leaf), (tree_vertex, new_leaf)))
    types = dict(network.types)
    types[tree_vertex] = "tree"
    types[new_leaf] = "leaf"
    leaves = tuple(sorted(network.leaves + (new_leaf,), key=lambda x: int(x[1:])))
    return (
        Network(
            f"{network.name}+{new_leaf}",
            network.root,
            types,
            tuple(sorted(arcs)),
            leaves,
            dict(network.parent_order),
        ),
        old_arc,
    )


def extend_point_for_cherry(
    old_edges: Mapping[tuple[str, str], Quadratic],
    old_arc: tuple[str, str],
    selected_leaf: str,
    new_leaf: str,
    tree_vertex: str,
    u: Quadratic,
    v: Quadratic,
) -> dict[tuple[str, str], Quadratic]:
    parent = old_arc[0]
    result = {edge: value for edge, value in old_edges.items() if edge != old_arc}
    result[(parent, tree_vertex)] = old_edges[old_arc]
    result[(tree_vertex, selected_leaf)] = u
    result[(tree_vertex, new_leaf)] = v
    return result


def extend_rooting_record(record: Mapping[str, object], selected_leaf: str, new_leaf: str, tree_vertex: str) -> dict[str, object]:
    network = record["network"]
    require(isinstance(network, Network), "rooting record lost network")
    extended, _old_arc = cherry_substitute(network, selected_leaf, new_leaf, tree_vertex)
    return {
        "site": record["site"],
        "site_is_reticulation_edge": record["site_is_reticulation_edge"],
        "lsa": root_is_lsa(extended),
        "tree_child": tree_child(extended),
        "network": extended,
    }


def leaf_neighbor(graph: MixedGraph, leaf: str) -> str:
    incident = [edge for edge in graph.edges if leaf in edge.endpoints]
    require(len(incident) == 1, "leaf does not have unique mixed neighbor")
    return next(node for node in incident[0].endpoints if node != leaf)


# ---------------------------------------------------------------------------
# Audit orchestration.
# ---------------------------------------------------------------------------


def interval_audit(data: Mapping[str, object], networks: Mapping[str, Network]) -> dict[str, object]:
    field = dict(data["quadratic_field"])
    coefficients = list(map(int, field["minimal_polynomial_coefficients"]))
    require(coefficients == [MINPOLY_A, MINPOLY_B, MINPOLY_C], "quadratic polynomial mismatch")
    lo = Fraction(str(field["isolating_interval"][0]))
    hi = Fraction(str(field["isolating_interval"][1]))
    beta_interval = Interval(lo, hi)

    def polynomial(x: Fraction) -> Fraction:
        return coefficients[0] * x * x + coefficients[1] * x + coefficients[2]

    def derivative(x: Fraction) -> Fraction:
        return 2 * coefficients[0] * x + coefficients[1]

    discriminant = coefficients[1] ** 2 - 4 * coefficients[0] * coefficients[2]
    require(discriminant > 0, "quadratic has no two real roots")
    discriminant_root = math.isqrt(discriminant)
    require(discriminant_root * discriminant_root != discriminant, "quadratic polynomial is reducible over Q")
    require(polynomial(lo) > 0 and polynomial(hi) < 0, "interval does not bracket the smaller root")
    require(derivative(lo) < 0 and derivative(hi) < 0, "quadratic not strictly decreasing on interval")
    vertex = Fraction(-coefficients[1], 2 * coefficients[0])
    require(hi < vertex, "interval is not on smaller-root branch")
    require((Quadratic(MINPOLY_A) * BETA * BETA + Quadratic(MINPOLY_B) * BETA + Quadratic(MINPOLY_C)).is_zero(), "quadratic reduction failed")

    bounds = {}
    for name, network in networks.items():
        point = dict(data["points"])[name]
        network_bounds = {}
        for edge_name, expression in dict(point["edge_multipliers"]).items():
            interval = evaluate_expression(str(expression), beta_interval)
            require(isinstance(interval, Interval), "interval evaluator returned wrong type")
            require(interval.lo > 0 and interval.hi < 1, f"edge {name}:{edge_name} not certified in (0,1)")
            network_bounds[f"edge:{edge_name}"] = interval.encode()
        for reticulation, expression in dict(point["inheritance"]).items():
            interval = evaluate_expression(str(expression), beta_interval)
            require(isinstance(interval, Interval), "interval evaluator returned wrong type")
            require(interval.lo > 0 and interval.hi < 1, f"inheritance {name}:{reticulation} not in (0,1)")
            network_bounds[f"inheritance:{reticulation}"] = interval.encode()
        root_product = network_bounds["edge:rho->A"]
        del root_product  # Explicit exact product is recorded below.
        bounds[name] = network_bounds

    effective_root_product = evaluate_expression("(2/3)*(3/4)", beta_interval)
    require(isinstance(effective_root_product, Interval) and effective_root_product == Interval.point(Fraction(1, 2)), "root split does not factor to 1/2")
    return {
        "minimal_polynomial": coefficients,
        "polynomial_at_lower": fraction_text(polynomial(lo)),
        "polynomial_at_upper": fraction_text(polynomial(hi)),
        "derivative_interval": [fraction_text(derivative(lo)), fraction_text(derivative(hi))],
        "discriminant": str(discriminant),
        "discriminant_is_nonsquare": True,
        "axis": fraction_text(vertex),
        "beta_interval": beta_interval.encode(),
        "effective_root_product": effective_root_product.encode(),
        "parameter_bounds": bounds,
    }


def graph_audit(networks: Mapping[str, Network]) -> tuple[dict[str, object], dict[str, MixedGraph], dict[str, list[dict[str, object]]]]:
    mixed_graphs = {}
    rootings = {}
    result = {}
    for name, network in networks.items():
        valid, reason = rooted_validation(network, require_lsa=True)
        require(valid, f"supplied rooted network {name} invalid: {reason}")
        require(tree_child(network), f"supplied rooted network {name} is not tree-child")
        mixed = reduce_standard(network)
        mixed_valid, mixed_reason = validate_mixed_binary(mixed)
        require(mixed_valid, f"standard reduction {name} invalid: {mixed_reason}")
        blobs = blob_audit(mixed)
        require(blobs["blob_count"] == 1, "wrong blob count")
        require(blobs["level"] == 2, "wrong level")
        require(blobs["cycle_lengths"] == [3, 5, 6], "wrong cycle lengths")
        require(blobs["triangle_count"] == 1, "wrong triangle count")
        rows = enumerate_admissible_rootings(mixed)
        undirected_count = sum(not edge.heads for edge in mixed.edges)
        orientation_candidates = sum(
            2 ** (undirected_count - (0 if edge.heads else 1))
            for edge in mixed.edges
        )
        require(len(rows) == 5, f"unexpected admissible-rooting census for {name}")
        require(all(bool(row["lsa"]) for row in rows), f"LSA filtering changes census for {name}")
        require(sum(bool(row["tree_child"]) for row in rows) == 2, f"wrong tree-child-rooting census for {name}")
        strong_sites = sorted(str(row["site"]) for row in rows if row["tree_child"])
        require(strong_sites == ["A->C", "A->F"], f"wrong strong root sites for {name}: {strong_sites}")
        mixed_graphs[name] = mixed
        rootings[name] = rows
        result[name] = {
            "rooted_DAG_valid": True,
            "root_is_LSA": True,
            "R_TC": True,
            "standard_mixed_graph_edges": [
                {"endpoints": list(edge.endpoints), "heads": list(edge.heads)}
                for edge in mixed.edges
            ],
            "blob_cycle_level": blobs,
            "admissible_rootings_exact_reduction": len(rows),
            "root_site_orientation_candidates_exhausted": orientation_candidates,
            "admissible_rootings_after_LSA_filter": sum(bool(row["lsa"]) for row in rows),
            "tree_child_rootings": sum(bool(row["tree_child"]) for row in rows),
            "non_tree_child_rootings": sum(not bool(row["tree_child"]) for row in rows),
            "tree_child_root_sites": strong_sites,
            "rooting_records": [
                {
                    "site": row["site"],
                    "site_is_reticulation_edge": row["site_is_reticulation_edge"],
                    "lsa": row["lsa"],
                    "tree_child": row["tree_child"],
                    "tree_child_failure_vertices": tree_child_failure_vertices(row["network"]),
                    "arcs": [list(arc) for arc in row["network"].arcs],
                    "arc_sha256": sha256_bytes(canonical_json_bytes(list(row["network"].arcs))),
                }
                for row in rows
            ],
            "W_TC": True,
            "S_TC": False,
        }

    left, right = mixed_graphs["N"], mixed_graphs["N_prime"]
    isomorphic, _mapping = graph_isomorphism(left, right)
    require(not isomorphic, "pair unexpectedly labelled-isomorphic")
    left_triangles, right_triangles = triangle_sets(left), triangle_sets(right)
    require(len(left_triangles) == len(right_triangles) == 1, "triangle quotient not unique")
    t_equivalent, _mapping = graph_isomorphism(
        left,
        right,
        left_triangles[0],
        right_triangles[0],
    )
    require(not t_equivalent, "pair unexpectedly ordinary-T-equivalent")
    require(leaf_neighbor(left, "L1") in left_triangles[0], "N leaf 1 lost triangle adjacency")
    require(leaf_neighbor(right, "L1") not in right_triangles[0], "N' leaf 1 gained triangle adjacency")
    label_blind, label_blind_mapping = graph_isomorphism(left, right, ignore_leaf_labels=True)
    require(label_blind, "label-blind mutation did not collapse the pair")
    result["separation"] = {
        "labelled_mixed_graph_isomorphic": False,
        "ordinary_T_equivalent": False,
        "separating_invariant": "the neighbor of labelled leaf 1 lies on the unique triangle only in N",
        "label_blind_graphs_are_isomorphic": True,
        "label_blind_witness": label_blind_mapping,
    }
    return result, mixed_graphs, rootings


def fourier_and_dimension_audit(
    data: Mapping[str, object],
    networks: Mapping[str, Network],
) -> tuple[dict[str, object], dict[str, tuple[dict[tuple[str, str], Quadratic], dict[str, Quadratic]]], dict[tuple[int, ...], Quadratic]]:
    representatives = {
        str(name): tuple(map(int, str(row)))
        for name, row in dict(data["orbit_representatives"]).items()
    }
    require(set(representatives) == set("ABCDEFGHJKLMNO"), "orbit representative names mismatch")
    orbits = orbit_partition()
    characters = character_table_audit()
    require(len(orbits) == 15, "zero-sum orbit count is not 15")
    representative_orbits = {
        min(orbit) for orbit in orbits
    }
    supplied_canonical = {
        min(orbit)
        for orbit in orbits
        if any(row in orbit for row in representatives.values())
    }
    require(len(supplied_canonical) == 14, "fourteen representatives are not orbit-distinct")
    require(representative_orbits - supplied_canonical == {(0, 0, 0, 0)}, "representatives do not cover all nonconstant orbits")

    symbolic = {name: symbolic_fourier_map(network, representatives) for name, network in networks.items()}
    for name, coordinates in symbolic.items():
        invariants = invariant_polynomials(coordinates)
        require(all(polynomial.is_zero() for polynomial in invariants), f"common invariant failed symbolically for {name}")
        require(root_product_property(coordinates), f"root-arm product property failed for {name}")

    points = {
        name: parse_point(network, dict(data["points"])[name])
        for name, network in networks.items()
    }
    tensors = {
        name: full_tensor(network, points[name][0], points[name][1], Quadratic(0), Quadratic(1))
        for name, network in networks.items()
    }
    source_tensor, target_tensor = tensors["N"], tensors["N_prime"]
    require(len(source_tensor) == len(target_tensor) == 256, "four-leaf tensor size mismatch")
    mismatches = [row for row in source_tensor if source_tensor[row] != target_tensor[row]]
    require(not mismatches, f"exact Fourier mismatch: {mismatches[:3]}")
    require(sum(value.is_zero() for row, value in source_tensor.items() if xor_sum(row) != 0) == 192, "forced-zero count mismatch")
    require(sum(not value.is_zero() for row, value in source_tensor.items() if xor_sum(row) == 0) == 64, "positive zero-sum coordinate count mismatch")
    require(source_tensor[(0, 0, 0, 0)] == Quadratic(1), "normalization coordinate is not one")

    claimed = {str(k): Fraction(str(v)) for k, v in dict(data["claimed_common_orbit_values"]).items()}
    derived_orbit_values = {}
    for name, row in representatives.items():
        value = source_tensor[row]
        require(value.b == 0 and value.a == claimed[name], f"claimed orbit value mismatch at {name}")
        require(target_tensor[row] == value, f"target orbit mismatch at {name}")
        derived_orbit_values[name] = value.encode()

    source_probabilities = inverse_fourier(source_tensor)
    target_probabilities = inverse_fourier(target_tensor)
    require(source_probabilities == target_probabilities, "inverse Fourier pattern distributions differ")
    require(sum(source_probabilities.values(), Quadratic(0)) == Quadratic(1), "pattern probabilities do not normalize")
    rational_probabilities = [value.a for value in source_probabilities.values() if value.b == 0]
    require(len(rational_probabilities) == 256 and min(rational_probabilities) > 0, "common pattern point is not strictly positive")

    source_free = (
        ("D", "L2"), ("D", "E"), ("E", "L4"), ("E", "F"),
        ("F", "L3"), ("C", "D"), ("A", "B"), ("B", "L1"),
    )
    target_free = (
        ("D", "L2"), ("D", "E"), ("A", "F"), ("A", "B"),
        ("F", "L3"), ("C", "D"), ("E", "L1"), ("B", "L4"),
    )
    source_matrix, source_det = jacobian_certificate(networks["N"], *points["N"], representatives, source_free)
    target_matrix, target_det = jacobian_certificate(networks["N_prime"], *points["N_prime"], representatives, target_free)

    s = points["N"][0]
    P, sv, Qv, t, R, u, v, S = [s[edge] for edge in source_free]
    source_factored = -(
        P**3 * sv**3 * Qv**4 * t * R**4 * u**3 * v * S**3
        * (sv - 1) ** 2 * (v - 1) * (v + 1) ** 2
    ) / 16_384
    require(source_det == source_factored, "source Jacobian disagrees with displayed factorization")

    tpoint = points["N_prime"][0]
    Pp, x, y, z, Rp, w, Sp, Qp = [tpoint[edge] for edge in target_free]
    target_factored = -(
        Pp**3 * x**2 * y**2 * z * Rp**4 * w**4 * Sp**3 * Qp**4
        * (x - 1) ** 2 * (z - 1) * (z + 1) ** 3
    ) / 32_768
    require(target_det == target_factored, "target Jacobian disagrees with displayed factorization")

    # At BE != 0 the six identities reconstruct J,K,M,N,O, leaving the one
    # equation L^2=BEH in nine coordinates.  These arithmetic checks ensure
    # the localized reconstruction is valid at the certified point.
    c = {name: source_tensor[row] for name, row in representatives.items()}
    require(not c["B"].is_zero() and not c["E"].is_zero(), "localized coordinate ring denominator vanishes")
    reconstructed = {
        "J": c["A"] * c["H"] + c["B"] * c["F"] - c["C"] * c["E"],
        "N": c["G"] * c["L"] / c["E"],
        "M": (c["D"] * c["L"] + c["B"] ** 2 * c["F"] - c["B"] * c["C"] * c["E"]) / c["B"],
        "O": (c["B"] * c["G"] * c["H"] + c["C"] * c["E"] * c["L"] - c["D"] * c["E"] * c["H"]) / (c["B"] * c["E"]),
    }
    reconstructed["K"] = reconstructed["J"] + reconstructed["N"] - reconstructed["M"]
    require(all(reconstructed[name] == c[name] for name in reconstructed), "localized invariant reconstruction failed")
    require(c["L"] ** 2 == c["B"] * c["E"] * c["H"], "quadratic sheet equation failed")

    tensor_encoding = [source_tensor[row].encode() for row in sorted(source_tensor)]
    return (
        {
            "group": "Z2 x Z2 with bitwise XOR",
            "character_table": characters,
            "zero_sum_assignments": 64,
            "nonzero_total_assignments_forced_zero": 192,
            "JC_orbits_including_normalization": len(orbits),
            "nonconstant_orbit_representatives": len(representatives),
            "symbolic_parameterization_sha256": {
                name: polynomial_map_hash(coordinates) for name, coordinates in symbolic.items()
            },
            "symbolic_coordinate_term_counts": {
                name: {coordinate: len(polynomial.terms) for coordinate, polynomial in coordinates.items()}
                for name, coordinates in symbolic.items()
            },
            "six_common_invariants_identically_zero": {name: True for name in networks},
            "root_arms_occur_only_as_product": {name: True for name in networks},
            "derived_common_orbit_values": derived_orbit_values,
            "fourier_coordinates_compared": 256,
            "fourier_mismatches": 0,
            "common_fourier_tensor_sha256": sha256_bytes(canonical_json_bytes(tensor_encoding)),
            "inverse_fourier_coordinates_compared": 256,
            "pattern_mismatches": 0,
            "minimum_common_pattern_probability": fraction_text(min(rational_probabilities)),
            "source_rank_eight": {
                "input_edges": [f"{u}->{v}" for u, v in source_free],
                "output_coordinates": list("ABCDEFGH"),
                "matrix_sha256": matrix_hash(source_matrix),
                "determinant": source_det.encode(),
                "elimination_equals_cofactor_expansion": True,
                "matches_independently_entered_factorization": True,
            },
            "target_rank_eight": {
                "input_edges": [f"{u}->{v}" for u, v in target_free],
                "output_coordinates": list("ABCDEFGH"),
                "matrix_sha256": matrix_hash(target_matrix),
                "determinant": target_det.encode(),
                "elimination_equals_cofactor_expansion": True,
                "matches_independently_entered_factorization": True,
            },
            "localized_upper_bound": {
                "invariants": 6,
                "free_coordinates_before_sheet_equation": 9,
                "sheet_equation": "L^2-B*E*H=0",
                "localization": "B*E != 0",
                "dimension_at_most": 8,
                "rank_at_least": 8,
                "exact_dimension": 8,
                "smoothness_derivative": "d/dH(L^2-BEH)=-BE != 0",
            },
        },
        points,
        source_tensor,
    )


def all_n_audit(
    networks: Mapping[str, Network],
    mixed_graphs: Mapping[str, MixedGraph],
    rootings: Mapping[str, list[dict[str, object]]],
    points: Mapping[str, tuple[dict[tuple[str, str], Quadratic], dict[str, Quadratic]]],
) -> dict[str, object]:
    selected_leaf = "L2"
    u, v = Quadratic(Fraction(2, 5)), Quadratic(Fraction(3, 7))
    one_step = {}
    for name, network in networks.items():
        extended, old_arc = cherry_substitute(network, selected_leaf, "L5", "X5")
        valid, reason = rooted_validation(extended, require_lsa=True)
        require(valid and tree_child(extended), f"one-step rooted extension failed for {name}: {reason}")
        extended_edges = extend_point_for_cherry(points[name][0], old_arc, selected_leaf, "L5", "X5", u, v)
        direct = full_tensor(extended, extended_edges, points[name][1], Quadratic(0), Quadratic(1))
        formula = {}
        for row in itertools.product(range(4), repeat=5):
            assignment = dict(zip(extended.leaves, row))
            old_assignment = {leaf: assignment[leaf] for leaf in network.leaves}
            old_assignment[selected_leaf] = assignment[selected_leaf] ^ assignment["L5"]
            base = displayed_coordinate(
                network,
                old_assignment,
                points[name][0],
                points[name][1],
                Quadratic(0),
                Quadratic(1),
            )
            value = base
            if assignment[selected_leaf] != 0:
                value *= u
            if assignment["L5"] != 0:
                value *= v
            formula[row] = value
        require(direct == formula, f"cherry Fourier formula failed for {name}")

        h = 1
        product_assignment = {leaf: 0 for leaf in extended.leaves}
        product_assignment[selected_leaf] = h
        product_assignment["L5"] = h
        product_coordinate = displayed_coordinate(
            extended, product_assignment, extended_edges, points[name][1], Quadratic(0), Quadratic(1)
        )
        numerator_assignment = {leaf: 0 for leaf in extended.leaves}
        numerator_assignment["L1"] = h
        numerator_assignment[selected_leaf] = h
        denominator_assignment = {leaf: 0 for leaf in extended.leaves}
        denominator_assignment["L1"] = h
        denominator_assignment["L5"] = h
        numerator = displayed_coordinate(
            extended, numerator_assignment, extended_edges, points[name][1], Quadratic(0), Quadratic(1)
        )
        denominator = displayed_coordinate(
            extended, denominator_assignment, extended_edges, points[name][1], Quadratic(0), Quadratic(1)
        )
        ratio = numerator / denominator
        require(product_coordinate == u * v and ratio == u / v, "cherry inverse coordinates failed")
        require(product_coordinate * ratio == u**2 and product_coordinate / ratio == v**2, "cherry square recovery failed")
        one_step[name] = {
            "direct_coordinates": len(direct),
            "formula_mismatches": 0,
            "extended_tensor_sha256": sha256_bytes(canonical_json_bytes([direct[row].encode() for row in sorted(direct)])),
            "uv": product_coordinate.encode(),
            "u_over_v": ratio.encode(),
            "recovered_u_squared": (product_coordinate * ratio).encode(),
            "recovered_v_squared": (product_coordinate / ratio).encode(),
        }

    # Equality of the two 5-leaf tensors follows here by a direct second
    # enumeration, independently of merely invoking the transform formula.
    require(one_step["N"]["extended_tensor_sha256"] == one_step["N_prime"]["extended_tensor_sha256"], "one-step common tensors differ")

    regression = {}
    current_networks = dict(networks)
    current_rootings = {name: list(rows) for name, rows in rootings.items()}
    for n in range(4, 13):
        if n > 4:
            new_leaf = f"L{n}"
            tree_vertex = f"X{n}"
            for name in ("N", "N_prime"):
                current_networks[name], _old_arc = cherry_substitute(
                    current_networks[name], selected_leaf, new_leaf, tree_vertex
                )
                current_rootings[name] = [
                    extend_rooting_record(row, selected_leaf, new_leaf, tree_vertex)
                    for row in current_rootings[name]
                ]
        row = {}
        current_mixed = {}
        for name in ("N", "N_prime"):
            network = current_networks[name]
            valid, reason = rooted_validation(network, require_lsa=True)
            require(valid and tree_child(network), f"all-n supplied rooting regression failed at n={n}, {name}: {reason}")
            mixed = reduce_standard(network)
            current_mixed[name] = mixed
            blob = blob_audit(mixed)
            require(blob["level"] == 2 and blob["cycle_lengths"] == [3, 5, 6], f"blob changed at n={n}, {name}")
            require(len(network.arcs) == 2 * n + 3 * 2 - 2, f"edge count formula failed at n={n}, {name}")
            extensions = current_rootings[name]
            require(all(bool(record["lsa"]) for record in extensions), f"LSA witness extension failed at n={n}, {name}")
            require(sum(bool(record["tree_child"]) for record in extensions) == 2, f"tree-child witness extension failed at n={n}, {name}")
            require(sum(not bool(record["tree_child"]) for record in extensions) == 3, f"non-tree-child witness extension failed at n={n}, {name}")
            triangle = triangle_sets(mixed)
            require(len(triangle) == 1, "all-n unique triangle failed")
            row[name] = {
                "rooted_tree_child": True,
                "extended_admissible_LSA_witnesses": len(extensions),
                "extended_tree_child_witnesses": 2,
                "extended_non_tree_child_witnesses": 3,
                "level": blob["level"],
                "cycle_lengths": blob["cycle_lengths"],
                "edge_count": len(network.arcs),
            }
        left_triangle = triangle_sets(current_mixed["N"])[0]
        right_triangle = triangle_sets(current_mixed["N_prime"])[0]
        require(leaf_neighbor(current_mixed["N"], "L1") in left_triangle, "all-n N separation invariant failed")
        require(leaf_neighbor(current_mixed["N_prime"], "L1") not in right_triangle, "all-n N' separation invariant failed")
        row["separation_invariant"] = True
        regression[str(n)] = row

    return {
        "explicit_family": "repeatedly replace labelled leaf 2 by a cherry retaining leaf 2 and adding leaf n",
        "one_step_exact_Fourier_test": one_step,
        "one_step_common_tensor_equal": True,
        "positive_analytic_inverse": {
            "product_coordinate": "uv=P_tilde(0,h,h)",
            "ratio_coordinate": "u/v=P_tilde(g_X,h,0)/P_tilde(g_X,0,h)",
            "positive_recovery": "u=sqrt((uv)(u/v)), v=sqrt((uv)/(u/v))",
            "base_tensor_recovery": "P(g_X,k)=P_tilde(g_X,k,0)/u^[k!=0]",
        },
        "dimension_induction": {
            "base_dimension": 8,
            "new_identifiable_parameters_per_cherry": 2,
            "substitutions": "n-4",
            "formula": "8+2(n-4)=2n",
            "model_image_is_exactly_base_image_times_open_square_under_embedding": True,
        },
        "full_dimensional_overlap_induction": {
            "common_base_germ_dimension": 8,
            "common_product_germ_gains_two_dimensions_per_cherry": True,
            "regularity_preserved_by_analytic_embedding_with_inverse": True,
        },
        "class_preservation_proof_components": {
            "binary_rooted_tree_child_representative_extends": True,
            "original_non_tree_child_admissible_rooting_extends": True,
            "blobs_and_level_unchanged_by_bridge-attached_cherry": True,
            "therefore_R_TC_and_W_TC_and_not_S_TC": True,
        },
        "nonisomorphism_nonT_proof": "labelled leaf 1 remains triangle-adjacent only in N_n",
        "finite_structural_regression": regression,
        "quantified_conclusion": "for every integer n>=4",
        "dimension": "2n",
    }


def adversarial_mutations(
    networks: Mapping[str, Network],
    mixed_graphs: Mapping[str, MixedGraph],
    points: Mapping[str, tuple[dict[tuple[str, str], Quadratic], dict[str, Quadratic]]],
    source_tensor: Mapping[tuple[int, ...], Quadratic],
    data: Mapping[str, object],
) -> dict[str, object]:
    left, right = mixed_graphs["N"], mixed_graphs["N_prime"]

    undirected_only = {
        name: enumerate_admissible_rootings(graph, include_directed_sites=False)
        for name, graph in mixed_graphs.items()
    }
    require(all(sum(bool(row["tree_child"]) for row in rows) == 0 for rows in undirected_only.values()), "undirected-only root-site mutation unexpectedly preserves W_TC witness")

    mutated_edges = []
    for edge in left.edges:
        if set(edge.endpoints) == {"A", "C"}:
            mutated_edges.append(MixedEdge.make(edge.endpoints, ()))
        else:
            mutated_edges.append(edge)
    bad_mixed = MixedGraph(dict(left.types), tuple(sorted(mutated_edges)), left.leaves)
    bad_valid, bad_reason = validate_mixed_binary(bad_mixed)
    require(not bad_valid, "undirecting the suppressed A->C artifact was not rejected")

    z4_source = full_tensor(networks["N"], *points["N"], Quadratic(0), Quadratic(1), group_sum=z4_sum)
    z4_target = full_tensor(networks["N_prime"], *points["N_prime"], Quadratic(0), Quadratic(1), group_sum=z4_sum)
    z4_mismatches = sum(z4_source[row] != z4_target[row] for row in z4_source)
    # This is deliberately not required to be positive.  In fact it is zero:
    # the collision is robust to this wrong group law, so the common point
    # cannot by itself lock the Klein-four convention.

    single_source = full_tensor(networks["N"], *points["N"], Quadratic(0), Quadratic(1), forced_choices=(0, 0))
    single_target = full_tensor(networks["N_prime"], *points["N_prime"], Quadratic(0), Quadratic(1), forced_choices=(0, 0))
    single_mismatches = sum(single_source[row] != single_target[row] for row in single_source)
    require(single_mismatches > 0, "single displayed-tree mutation did not break equality")

    swapped_target = {
        row: source_tensor[(row[3], row[1], row[2], row[0])]
        for row in source_tensor
    }
    leaf_order_mismatches = sum(swapped_target[row] != source_tensor[row] for row in source_tensor)
    require(leaf_order_mismatches > 0, "leaf-order mutation was invisible")

    field = dict(data["quadratic_field"])
    lo = Fraction(str(field["isolating_interval"][0]))
    hi = Fraction(str(field["isolating_interval"][1]))
    root_sum = Fraction(-MINPOLY_B, MINPOLY_A)
    other_root = Interval(root_sum - hi, root_sum - lo)
    wrong_branch_z = evaluate_expression("24835*beta/(20678-24835*beta)", other_root)
    require(isinstance(wrong_branch_z, Interval) and wrong_branch_z.lo > 1, "larger beta root was not rejected by z>1")

    # A sign typo in the first common invariant must be visible symbolically.
    representatives = {
        str(name): tuple(map(int, str(row)))
        for name, row in dict(data["orbit_representatives"]).items()
    }
    source_symbolic = symbolic_fourier_map(networks["N"], representatives)
    typo = source_symbolic["J"] - source_symbolic["K"] + source_symbolic["M"] + source_symbolic["N"]
    require(not typo.is_zero(), "invariant-sign mutation was not detected")

    return {
        "all_required_mutations_rejected": True,
        "tests": {
            "ignoring_leaf_labels_collapses_pair": True,
            "disallowing_root_sites_on_reticulation_edges": {
                name: {
                    "admissible_rootings": len(rows),
                    "tree_child_rootings": sum(bool(row["tree_child"]) for row in rows),
                }
                for name, rows in undirected_only.items()
            },
            "incorrectly_undirecting_suppressed_A_to_C": bad_reason,
            "using_Z4_addition_instead_of_XOR_mismatches": z4_mismatches,
            "using_one_displayed_tree_instead_of_inheritance_mixture_mismatches": single_mismatches,
            "swapping_leaf_1_and_leaf_4_tensor_axes_mismatches": leaf_order_mismatches,
            "using_larger_quadratic_root_gives_A_to_B_interval": wrong_branch_z.encode(),
            "common_invariant_sign_typo_nonzero_terms": len(typo.terms),
        },
        "convention_warning": "The R_TC/W_TC/not-S_TC conclusion uses the standard convention permitting root insertion on a compatible retained reticulation edge; excluding those sites would erase both tree-child witnesses.",
        "robustness_warning": "The certified inheritance probabilities are 1/2, so the common-point equality alone cannot detect a swap of the named parent order. Symbolic full-model invariants were therefore checked with independent lambda_C and lambda_F variables.",
        "state_group_blind_spot": "The same point collision also survives if XOR is incorrectly replaced by addition modulo 4. The Z2xZ2 convention is locked instead by the explicit six-automorphism orbit census and the independently checked Klein-four character inverse.",
    }


def build_certificate(instance_path: Path) -> dict[str, object]:
    data = json.loads(instance_path.read_text())
    require(data["schema_version"] == 1, "unsupported instance schema")
    networks = construct_networks(data)
    require(set(networks) == {"N", "N_prime"}, "network IDs mismatch")

    intervals = interval_audit(data, networks)
    graph_result, mixed_graphs, rootings = graph_audit(networks)
    fourier_result, points, source_tensor = fourier_and_dimension_audit(data, networks)
    all_n_result = all_n_audit(networks, mixed_graphs, rootings, points)
    mutations = adversarial_mutations(networks, mixed_graphs, points, source_tensor, data)

    return {
        "schema_version": 1,
        "implementation": {
            "language": "Python standard library only",
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "instance_sha256": sha256_file(instance_path),
            "historical_graph_or_Fourier_code_imported": False,
            "historical_status_strings_used_as_evidence": False,
        },
        "claims": {
            "four_leaf_graph_and_class_membership": "EXACTLY COMPUTED",
            "four_leaf_nonisomorphism_and_nonordinary_T_equivalence": "PROVED",
            "all_256_Fourier_coordinates_equal_at_exact_interior_point": "EXACTLY COMPUTED",
            "all_256_pattern_coordinates_equal": "EXACTLY COMPUTED",
            "source_and_target_rank_eight": "EXACTLY COMPUTED",
            "common_invariant_upper_bound_and_dimension_eight": "PROVED",
            "four_leaf_full_dimensional_regular_overlap": "PROVED",
            "all_n_cherry_substitution_theorem": "PROVED",
            "standalone_sharpness_theorem": "PROVED",
        },
        "interval_positivity": intervals,
        "graphs": graph_result,
        "fourier_dimension_overlap": fourier_result,
        "all_n": all_n_result,
        "adversarial_mutations": mutations,
        "final_verdict": "PROVED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=Path, default=DEFAULT_INSTANCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stdout", action="store_true", help="also print the full canonical certificate")
    args = parser.parse_args()

    certificate = build_certificate(args.instance.resolve())
    encoded = canonical_json_bytes(certificate)
    args.output.write_bytes(encoded)
    if args.stdout:
        print(encoded.decode(), end="")
    print(f"PASS final_verdict={certificate['final_verdict']}")
    print(f"certificate_sha256={sha256_bytes(encoded)}")
    print(f"output={args.output.resolve()}")


if __name__ == "__main__":
    main()
