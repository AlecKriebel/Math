"""Bounded-bit count-to-sample reduction for finite simple graphs.

The production reduction takes two black boxes: a deterministic polynomial-
time perfect-matching witness routine and the claimed unweighted FPRAS. The
exponential exact routines below are deliberately small-instance TEST helpers;
they are not an implementation or certification of that upstream FPRAS.

All probability arithmetic is exact Fraction arithmetic. A draw uses a fixed
number of fair bits; no rejection loop occurs.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product
from typing import Callable

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


@dataclass(frozen=True)
class Graph:
    vertices: tuple[int, ...]
    edges: tuple[Edge, ...]

    @classmethod
    def make(cls, vertices, edges):
        vertices = tuple(sorted(set(vertices)))
        vertex_set = set(vertices)
        canonical = set()
        for u, v in edges:
            if u == v or u not in vertex_set or v not in vertex_set:
                raise ValueError("Graph must be finite, undirected, and simple")
            canonical.add((min(u, v), max(u, v)))
        return cls(vertices, tuple(sorted(canonical)))

    def without(self, u: int, v: int) -> "Graph":
        return Graph(
            tuple(x for x in self.vertices if x != u and x != v),
            tuple((x, y) for x, y in self.edges if x not in (u, v) and y not in (u, v)),
        )

    def neighbors(self, u: int) -> tuple[int, ...]:
        return tuple(sorted(y if x == u else x for x, y in self.edges if u in (x, y)))


@dataclass
class Stats:
    count_calls: int = 0
    witness_calls: int = 0
    decisions: int = 0
    bit_draws: int = 0
    random_bits: int = 0
    witness_fallbacks: int = 0


@dataclass(frozen=True)
class Parameters:
    pairs: int
    call_cap: int
    relative_error: Fraction
    call_failure: Fraction
    bits_per_draw: int


def parameters(vertex_count: int, eta: Fraction) -> Parameters:
    eta = Fraction(eta)
    if not 0 < eta < 1:
        raise ValueError("Require rational 0 < eta < 1")
    if vertex_count < 0 or vertex_count % 2:
        raise ValueError("Require an even nonnegative vertex count")
    pairs = vertex_count // 2
    if not pairs:
        return Parameters(0, 0, Fraction(0), Fraction(0), 0)
    call_cap = pairs * pairs
    relative_error = eta / (4 * pairs)
    call_failure = eta / (4 * call_cap)
    bits = 0
    # Exact integer/rational comparison; no floating-point logarithm.
    while (1 << bits) * eta < 4 * call_cap:
        bits += 1
    return Parameters(pairs, call_cap, relative_error, call_failure, bits)


def rounded_probabilities(weights: tuple[Fraction, ...], bits: int) -> tuple[Fraction, ...]:
    """Floor every cumulative boundary on a common dyadic grid.

    Zero weights stay zero, and the final boundary is exactly 2**bits.
    The result sums to one exactly. It is also the law implemented by drawing
    J in [0, 2**bits) and taking the first boundary strictly exceeding J.
    """
    weights = tuple(Fraction(x) for x in weights)
    if bits < 0 or not weights or any(x < 0 for x in weights):
        raise ValueError("Require nonnegative weights, nonempty list, and bits >= 0")
    total = sum(weights, Fraction(0))
    if not total:
        raise ValueError("All-zero estimates need the witness fallback")
    scale = 1 << bits
    cumulative = Fraction(0)
    previous = 0
    answer = []
    for value in weights:
        cumulative += value
        ratio = scale * cumulative / total
        boundary = ratio.numerator // ratio.denominator
        answer.append(Fraction(boundary - previous, scale))
        previous = boundary
    assert previous == scale
    return tuple(answer)


def sample_perfect_matching(
    graph: Graph,
    eta: Fraction,
    count_oracle: Callable[[Graph, Fraction, Fraction], Fraction],
    witness_oracle: Callable[[Graph], Matching | None],
    draw_bits: Callable[[int], int],
    stats: Stats | None = None,
) -> Matching | None:
    """Return infeasibility exactly, or an eta-TV approximate uniform matching.

    Contract: count_oracle has a uniform worst-case polynomial bit bound and
    returns a nonnegative rational estimate whose relative error exceeds its
    error parameter with probability at most its failure parameter. Its
    randomness must be fresh on each adaptive call. witness_oracle is exact
    deterministic polynomial time, returning a witness or None. draw_bits(b)
    returns a uniform b-bit integer using fresh independent fair bits.
    """
    if stats is None:
        stats = Stats()
    if len(graph.vertices) % 2:
        stats.witness_calls += 1
        if witness_oracle(graph) is not None:
            raise ValueError("Witness oracle violated feasibility contract")
        return None
    par = parameters(len(graph.vertices), eta)
    stats.witness_calls += 1
    current_witness = witness_oracle(graph)
    if current_witness is None:
        return None
    selected: list[Edge] = []
    residual = graph
    while residual.vertices:
        stats.decisions += 1
        u = residual.vertices[0]
        children = []
        for v in residual.neighbors(u):
            child = residual.without(u, v)
            stats.witness_calls += 1
            witness = witness_oracle(child)
            if witness is not None:
                children.append((v, child, witness))
        if not children:
            raise ValueError("Witness oracle violated feasibility contract")
        if len(children) == 1:
            v, residual, current_witness = children[0]
        else:
            estimates = []
            for _, child, _ in children:
                stats.count_calls += 1
                estimate = Fraction(count_oracle(child, par.relative_error, par.call_failure))
                if estimate < 0:
                    raise ValueError("Count oracle must return nonnegative rationals")
                estimates.append(estimate)
            if sum(estimates, Fraction(0)) == 0:
                # A valid matching on every oracle history, including failure.
                stats.witness_fallbacks += 1
                return tuple(sorted((*selected, *current_witness)))
            probabilities = rounded_probabilities(tuple(estimates), par.bits_per_draw)
            integer = draw_bits(par.bits_per_draw)
            scale = 1 << par.bits_per_draw
            if not 0 <= integer < scale:
                raise ValueError("draw_bits returned an invalid integer")
            stats.bit_draws += 1
            stats.random_bits += par.bits_per_draw
            boundary = 0
            chosen = None
            for index, probability in enumerate(probabilities):
                boundary += probability.numerator * (scale // probability.denominator)
                if integer < boundary:
                    chosen = index
                    break
            assert chosen is not None
            v, residual, current_witness = children[chosen]
        selected.append((min(u, v), max(u, v)))
    return tuple(sorted(selected))


@lru_cache(maxsize=None)
def exact_matchings(graph: Graph) -> tuple[Matching, ...]:
    """Exponential reference enumeration: only for small validation instances."""
    if not graph.vertices:
        return ((),)
    if len(graph.vertices) % 2:
        return ()
    u = graph.vertices[0]
    answer = []
    for v in graph.neighbors(u):
        edge = (min(u, v), max(u, v))
        for suffix in exact_matchings(graph.without(u, v)):
            answer.append(tuple(sorted((edge, *suffix))))
    return tuple(answer)


def exact_witness(graph: Graph) -> Matching | None:
    matches = exact_matchings(graph)
    return matches[0] if matches else None


def exact_count_oracle(graph: Graph, _error: Fraction, _failure: Fraction) -> Fraction:
    return Fraction(len(exact_matchings(graph)))


def uniform_law(graph: Graph) -> dict[Matching, Fraction]:
    matches = exact_matchings(graph)
    return {matching: Fraction(1, len(matches)) for matching in matches}


def total_variation(a: dict[Matching, Fraction], b: dict[Matching, Fraction]) -> Fraction:
    return sum((abs(a.get(x, 0) - b.get(x, 0)) for x in a.keys() | b.keys()), Fraction(0)) / 2


def exact_sampler_law(
    graph: Graph,
    eta: Fraction,
    multiplier: Callable[[Graph, int, Fraction], Fraction] | None = None,
    failure_probability: Fraction = Fraction(0),
) -> dict[Matching, Fraction]:
    """Integrate the entire finite-bit sampler law exactly for TEST instances.

    A successful call returns z*multiplier(graph, neighbor, alpha); a failed
    call returns zero. Each call fails independently with the specified
    probability. All 2**k oracle-outcome patterns are summed symbolically;
    all 2**b draw outcomes are integrated by exact cumulative boundaries.
    """
    par = parameters(len(graph.vertices), eta)
    failure_probability = Fraction(failure_probability)
    if not 0 <= failure_probability <= 1:
        raise ValueError("Invalid failure probability")
    if multiplier is None:
        multiplier = lambda _graph, _v, _alpha: Fraction(1)

    @lru_cache(maxsize=None)
    def visit(residual: Graph):
        if not residual.vertices:
            return (((), Fraction(1)),)
        witness = exact_witness(residual)
        if witness is None:
            return ()
        u = residual.vertices[0]
        children = []
        for v in residual.neighbors(u):
            child = residual.without(u, v)
            count = len(exact_matchings(child))
            if count:
                children.append((v, child, count))
        if len(children) == 1:
            v, child, _ = children[0]
            edge = (min(u, v), max(u, v))
            return tuple((tuple(sorted((edge, *suffix))), p) for suffix, p in visit(child))
        successful = tuple(Fraction(z) * multiplier(residual, v, par.relative_error)
                           for v, _, z in children)
        law: dict[Matching, Fraction] = {}
        patterns = product((False, True), repeat=len(children)) if failure_probability else [(False,) * len(children)]
        for failures in patterns:
            num_failures = sum(failures)
            pattern_mass = failure_probability ** num_failures * (1 - failure_probability) ** (len(children) - num_failures)
            if not pattern_mass:
                continue
            estimates = tuple(Fraction(0) if failed else estimate for failed, estimate in zip(failures, successful))
            if not sum(estimates, Fraction(0)):
                law[witness] = law.get(witness, Fraction(0)) + pattern_mass
                continue
            probabilities = rounded_probabilities(estimates, par.bits_per_draw)
            for (v, child, _), branch_mass in zip(children, probabilities):
                if not branch_mass:
                    continue
                edge = (min(u, v), max(u, v))
                for suffix, suffix_mass in visit(child):
                    matching = tuple(sorted((edge, *suffix)))
                    law[matching] = law.get(matching, Fraction(0)) + pattern_mass * branch_mass * suffix_mass
        return tuple(sorted(law.items()))

    return dict(visit(graph))
