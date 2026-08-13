#!/usr/bin/env python3
"""Primitive displayed-tree JC Fourier engine written for this audit."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from clean_graph import MixedGraph, Rooting, edge_key


def jc_orbit_representatives(n: int) -> Tuple[Tuple[int, ...], ...]:
    """Represent zero-total JC character orbits under Aut(Z2 x Z2)."""

    autos = tuple(permutations((1, 2, 3)))

    def transform(g: Tuple[int, ...], perm: Tuple[int, int, int]) -> Tuple[int, ...]:
        table = (0,) + perm
        return tuple(table[x] for x in g)

    reps = set()
    for prefix in product(range(4), repeat=n - 1):
        total = 0
        for x in prefix:
            total ^= x
        g = tuple(prefix) + (total,)
        reps.add(min(transform(g, p) for p in autos))
    return tuple(sorted(reps))


@dataclass(frozen=True)
class Switching:
    choices: Tuple[int, ...]
    descendant_masks: Tuple[int, ...]  # zero for an arc deleted in this switching


@dataclass(frozen=True)
class JCModel:
    n: int
    reticulations: Tuple[int, ...]
    arcs: Tuple[Tuple[int, int], ...]
    incoming_arcs: Tuple[Tuple[int, int], ...]  # indices, two per retic
    switchings: Tuple[Switching, ...]
    coordinates: Tuple[Tuple[int, ...], ...]

    @property
    def edge_parameter_count(self) -> int:
        return len(self.arcs)

    @property
    def parameter_count(self) -> int:
        return len(self.arcs) + len(self.reticulations)


def _descendant_mask(n: int, head: int, kept_arcs: Sequence[Tuple[int, int]]) -> int:
    out: Dict[int, List[int]] = {}
    for u, v in kept_arcs:
        out.setdefault(u, []).append(v)
    seen = {head}
    stack = [head]
    while stack:
        u = stack.pop()
        for v in out.get(u, ()):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    mask = 0
    for leaf in range(n):
        if leaf in seen:
            mask |= 1 << leaf
    return mask


def build_model(graph: MixedGraph, rooting: Rooting) -> JCModel:
    arcs = tuple(sorted(rooting.arcs))
    arc_index = {a: i for i, a in enumerate(arcs)}
    retics = tuple(sorted(graph.reticulations))
    incoming = []
    for r in retics:
        inds = tuple(sorted(arc_index[a] for a in arcs if a[1] == r))
        if len(inds) != 2:
            raise ValueError((r, inds))
        incoming.append(inds)

    switchings = []
    for choices in product((0, 1), repeat=len(retics)):
        deleted = {incoming[j][1 - bit] for j, bit in enumerate(choices)}
        kept = tuple(a for i, a in enumerate(arcs) if i not in deleted)
        masks = []
        for i, (_, head) in enumerate(arcs):
            masks.append(0 if i in deleted else _descendant_mask(graph.n, head, kept))
        switchings.append(Switching(tuple(choices), tuple(masks)))
    coordinates = tuple(g for g in jc_orbit_representatives(graph.n) if any(g))
    return JCModel(graph.n, retics, arcs, tuple(incoming), tuple(switchings), coordinates)


def _subset_xor(g: Sequence[int], mask: int) -> int:
    answer = 0
    i = 0
    while mask:
        if mask & 1:
            answer ^= g[i]
        mask >>= 1
        i += 1
    return answer


def evaluate(model: JCModel, parameters: Sequence[float]) -> List[float]:
    ecount = model.edge_parameter_count
    if len(parameters) != model.parameter_count:
        raise ValueError("wrong parameter count")
    x = parameters[:ecount]
    lambdas = parameters[ecount:]
    values = []
    for g in model.coordinates:
        total = 0.0
        for switching in model.switchings:
            weight = 1.0
            for bit, lam in zip(switching.choices, lambdas):
                weight *= lam if bit == 0 else (1.0 - lam)
            monomial = 1.0
            for xe, mask in zip(x, switching.descendant_masks):
                if mask and _subset_xor(g, mask):
                    monomial *= xe
            total += weight * monomial
        values.append(total)
    return values


def evaluate_and_jacobian(model: JCModel, parameters: Sequence[float]) -> Tuple[List[float], List[List[float]]]:
    ecount = model.edge_parameter_count
    rcount = len(model.reticulations)
    x = parameters[:ecount]
    lambdas = parameters[ecount:]
    values = []
    jacobian = []
    for g in model.coordinates:
        value = 0.0
        row = [0.0] * (ecount + rcount)
        for switching in model.switchings:
            factors = [lam if bit == 0 else 1.0 - lam for bit, lam in zip(switching.choices, lambdas)]
            weight = 1.0
            for factor in factors:
                weight *= factor
            active = [bool(mask and _subset_xor(g, mask)) for mask in switching.descendant_masks]
            mono = 1.0
            for xe, flag in zip(x, active):
                if flag:
                    mono *= xe
            term = weight * mono
            value += term
            for j, flag in enumerate(active):
                if flag:
                    row[j] += term / x[j]
            for j, bit in enumerate(switching.choices):
                derivative = 1.0 if bit == 0 else -1.0
                other = 1.0
                for k, factor in enumerate(factors):
                    if k != j:
                        other *= factor
                row[ecount + j] += derivative * other * mono
        values.append(value)
        jacobian.append(row)
    return values, jacobian


def evaluate_fraction(model: JCModel, parameters: Sequence[Fraction]) -> Tuple[Fraction, ...]:
    ecount = model.edge_parameter_count
    x = parameters[:ecount]
    lambdas = parameters[ecount:]
    values = []
    for g in model.coordinates:
        total = Fraction(0)
        for switching in model.switchings:
            weight = Fraction(1)
            for bit, lam in zip(switching.choices, lambdas):
                weight *= lam if bit == 0 else 1 - lam
            monomial = Fraction(1)
            for xe, mask in zip(x, switching.descendant_masks):
                if mask and _subset_xor(g, mask):
                    monomial *= xe
            total += weight * monomial
        values.append(total)
    return tuple(values)


def evaluate_mod_prime(model: JCModel, parameters: Sequence[int], prime: int) -> Tuple[List[int], List[List[int]]]:
    """Exact finite-field value and Jacobian for screening/rank witnesses."""

    ecount = model.edge_parameter_count
    rcount = len(model.reticulations)
    x = [z % prime for z in parameters[:ecount]]
    lambdas = [z % prime for z in parameters[ecount:]]
    values: List[int] = []
    jac: List[List[int]] = []
    for g in model.coordinates:
        value = 0
        row = [0] * (ecount + rcount)
        for switching in model.switchings:
            factors = [(lam if bit == 0 else 1 - lam) % prime for bit, lam in zip(switching.choices, lambdas)]
            weight = 1
            for factor in factors:
                weight = weight * factor % prime
            active = [bool(mask and _subset_xor(g, mask)) for mask in switching.descendant_masks]
            mono = 1
            for xe, flag in zip(x, active):
                if flag:
                    mono = mono * xe % prime
            term = weight * mono % prime
            value = (value + term) % prime
            for j, flag in enumerate(active):
                if flag:
                    row[j] = (row[j] + term * pow(x[j], prime - 2, prime)) % prime
            for j, bit in enumerate(switching.choices):
                other = 1
                for k, factor in enumerate(factors):
                    if k != j:
                        other = other * factor % prime
                sign = 1 if bit == 0 else prime - 1
                row[ecount + j] = (row[ecount + j] + sign * other * mono) % prime
        values.append(value)
        jac.append(row)
    return values, jac


def rank_mod_prime(matrix: Sequence[Sequence[int]], prime: int) -> int:
    if not matrix:
        return 0
    a = [[x % prime for x in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], prime - 2, prime)
        a[rank] = [x * inv % prime for x in a[rank]]
        for i in range(rows):
            if i != rank and a[i][col]:
                factor = a[i][col]
                a[i] = [(x - factor * y) % prime for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def model_record(model: JCModel) -> dict:
    return {
        "n": model.n,
        "reticulations": list(model.reticulations),
        "arcs": [list(a) for a in model.arcs],
        "incoming_arc_indices": [list(x) for x in model.incoming_arcs],
        "coordinates": [list(g) for g in model.coordinates],
        "switchings": [
            {"choices": list(s.choices), "descendant_masks": list(s.descendant_masks)}
            for s in model.switchings
        ],
    }


def effective_unrooted_signature(graph: MixedGraph, rooting: Rooting) -> Tuple[tuple, ...]:
    """Normalize a rooted map to one effective multiplier per mixed edge.

    The two arcs introduced at the root map back to ``rooting.root_edge``.
    Trivial all-leaf root splits are discarded.  The output records the
    selected incoming mixed edge at every reticulation and the displayed-tree
    split carried by every mixed edge.  It is therefore independent of root
    multiplier factorization.
    """

    model = build_model(graph, rooting)
    all_mask = (1 << graph.n) - 1
    mixed_edges = tuple(sorted(graph.edges))

    def mixed_edge_for_arc(arc: Tuple[int, int]) -> Tuple[int, int]:
        if arc[0] == rooting.root:
            return rooting.root_edge
        return edge_key(*arc)

    records = []
    for switching in model.switchings:
        selected = []
        for j, _ in enumerate(model.reticulations):
            kept_index = model.incoming_arcs[j][switching.choices[j]]
            selected.append(mixed_edge_for_arc(model.arcs[kept_index]))
        masks_by_edge: Dict[Tuple[int, int], set[int]] = {e: set() for e in mixed_edges}
        for arc, mask in zip(model.arcs, switching.descendant_masks):
            canonical_mask = min(mask, all_mask ^ mask)
            if canonical_mask:
                masks_by_edge[mixed_edge_for_arc(arc)].add(canonical_mask)
        normalized_masks = []
        for e in mixed_edges:
            masks = masks_by_edge[e]
            if len(masks) > 1:
                raise AssertionError((rooting.root_edge, e, masks))
            normalized_masks.append(next(iter(masks), 0))
        records.append((tuple(selected), tuple(normalized_masks)))
    return tuple(sorted(records))
