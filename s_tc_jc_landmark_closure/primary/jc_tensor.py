"""Exact primary JC Fourier tensors and polynomial pullbacks."""

from __future__ import annotations

import ast
from collections import defaultdict
from functools import lru_cache
from itertools import permutations, product
import math
from pathlib import Path
from typing import Iterable, Sequence

from graph_model import RootedGraph, descendant_masks, displayed_switchings


Poly = dict[tuple[int, ...], int]
Descriptor = tuple[int, tuple[tuple[int, ...], ...]]


def poly_add(a: Poly, b: Poly, scale: int = 1) -> Poly:
    out = dict(a)
    for monomial, coefficient in b.items():
        value = out.get(monomial, 0) + scale * coefficient
        if value:
            out[monomial] = value
        else:
            out.pop(monomial, None)
    return out


def poly_mul(a: Poly, b: Poly) -> Poly:
    if not a or not b:
        return {}
    out: dict[tuple[int, ...], int] = defaultdict(int)
    for ma, ca in a.items():
        for mb, cb in b.items():
            out[tuple(x + y for x, y in zip(ma, mb))] += ca * cb
    return {m: c for m, c in out.items() if c}


def poly_const(value: int, variables: int) -> Poly:
    return {} if not value else {(0,) * variables: value}


def primitive(poly: Poly) -> tuple[tuple[tuple[int, ...], int], ...]:
    if not poly:
        return ()
    content = 0
    for value in poly.values():
        content = math.gcd(content, abs(value))
    reduced = {m: c // content for m, c in poly.items()}
    first = min(reduced)
    if reduced[first] < 0:
        reduced = {m: -c for m, c in reduced.items()}
    return tuple(sorted(reduced.items()))


@lru_cache(maxsize=1)
def jc_representatives() -> tuple[tuple[int, int, int, int], ...]:
    colour_maps = [(0, *row) for row in permutations((1, 2, 3))]

    def canon(row: tuple[int, ...]) -> tuple[int, ...]:
        return min(tuple(mapping[value] for value in row) for mapping in colour_maps)

    answer = sorted({
        canon(row)
        for row in product(range(4), repeat=4)
        if row[0] ^ row[1] ^ row[2] ^ row[3] == 0
    })
    if len(answer) != 15:
        raise AssertionError(len(answer))
    return tuple(answer)


def raw_descriptor(graph: RootedGraph, ordered_labels: Sequence[str]) -> Descriptor:
    indegree, _ = graph.degrees()
    retics = tuple(sorted(v for v in graph.vertices if indegree[v] == 2))
    displays = tuple(product((0, 1), repeat=len(retics)))
    signatures = [[0] * len(displays) for _ in graph.arcs]
    for display_index, (_choices, active) in enumerate(displayed_switchings(graph)):
        masks = descendant_masks(graph, active, ordered_labels)
        for edge_id, mask in zip(active, masks):
            signatures[edge_id][display_index] = mask
    return len(retics), tuple(sorted(tuple(row) for row in signatures if any(row)))


def canonicalize_rows(retics: int, signatures: Iterable[Sequence[int]]) -> Descriptor:
    # Edges with the same complete displayed-tree mask signature are
    # observationally visible only through the product of their positive JC
    # multipliers.  Zip each such class to one effective variable.
    signatures = tuple(sorted(set(tuple(row) for row in signatures if any(row))))
    if not retics:
        return 0, signatures
    displays = tuple(product((0, 1), repeat=retics))
    display_index = {bits: index for index, bits in enumerate(displays)}
    candidates: list[Descriptor] = []
    for permutation in permutations(range(retics)):
        for flips in product((0, 1), repeat=retics):
            moved = []
            for signature in signatures:
                row = [0] * len(displays)
                for old_index, old_bits in enumerate(displays):
                    new_bits = tuple(old_bits[permutation[j]] ^ flips[j] for j in range(retics))
                    row[display_index[new_bits]] = signature[old_index]
                moved.append(tuple(row))
            candidates.append((retics, tuple(sorted(set(moved)))))
    return min(candidates)


def canonical_descriptor(graph: RootedGraph, ordered_labels: Sequence[str]) -> Descriptor:
    retics, signatures = raw_descriptor(graph, ordered_labels)
    return canonicalize_rows(retics, signatures)


def ordered_quartet_deck(
    graph: RootedGraph,
    outgoing_labels: Sequence[str],
    incoming_label: str,
) -> dict[tuple[int, int, int], Descriptor]:
    """All ordered triples of outgoing ports, with incoming fixed in slot 3."""
    outgoing = tuple(outgoing_labels)
    retics, signatures = raw_descriptor(graph, (*outgoing, incoming_label))
    n = len(outgoing)
    answer = {}
    for triple in permutations(range(n), 3):
        rows = []
        for signature in signatures:
            moved = []
            for mask in signature:
                new_mask = 0
                for new_index, old_index in enumerate(triple):
                    if mask & (1 << old_index):
                        new_mask |= 1 << new_index
                if mask & (1 << n):
                    new_mask |= 1 << 3
                moved.append(new_mask)
            rows.append(tuple(moved))
        answer[triple] = canonicalize_rows(retics, rows)
    return answer


def all_port_quartet_deck(
    graph: RootedGraph,
    outgoing_labels: Sequence[str],
    incoming_label: str,
) -> dict[tuple[int, int, int, int], Descriptor]:
    """Every ordered four-port restriction of the complete boundary tensor.

    The earlier closure compiler considered only quartets containing the
    distinguished incoming boundary.  That is not sufficient for a directed
    containment atlas: a weak target can hide a reticulation from all such
    restrictions while an all-outgoing quartet detects it.  Keys are ordered
    tuples of positions in ``(*outgoing_labels, incoming_label)``.
    """
    labels = (*tuple(outgoing_labels), incoming_label)
    retics, signatures = raw_descriptor(graph, labels)
    answer = {}
    for ordered in permutations(range(len(labels)), 4):
        rows = []
        for signature in signatures:
            moved = []
            for mask in signature:
                new_mask = 0
                for new_index, old_index in enumerate(ordered):
                    if mask & (1 << old_index):
                        new_mask |= 1 << new_index
                moved.append(new_mask)
            rows.append(tuple(moved))
        answer[ordered] = canonicalize_rows(retics, rows)
    return answer


@lru_cache(maxsize=None)
def coordinate_polynomials(descriptor: Descriptor) -> tuple[Poly, ...]:
    retics, signatures = descriptor
    displays = tuple(product((0, 1), repeat=retics))
    variables = len(signatures) + retics
    coordinates = []
    for assignment in jc_representatives():
        total: Poly = {}
        for display_index, choices in enumerate(displays):
            exponent = [0] * variables
            for variable, signature in enumerate(signatures):
                mask = signature[display_index]
                state = 0
                for leaf_index, character in enumerate(assignment):
                    if mask & (1 << leaf_index):
                        state ^= character
                if state:
                    exponent[variable] = 1
            term: Poly = {tuple(exponent): 1}
            for retic_index, choice in enumerate(choices):
                variable = len(signatures) + retic_index
                row = [0] * variables
                row[variable] = 1
                factor = {tuple(row): 1} if choice == 0 else {
                    (0,) * variables: 1,
                    tuple(row): -1,
                }
                term = poly_mul(term, factor)
            total = poly_add(total, term)
        coordinates.append(total)
    return tuple(coordinates)


def pullback(descriptor: Descriptor, invariant: Sequence[tuple[Sequence[int], int]]) -> Poly:
    coordinates = coordinate_polynomials(descriptor)
    variables = len(descriptor[1]) + descriptor[0]
    cache: dict[tuple[int, ...], Poly] = {(): poly_const(1, variables)}

    def monomial(indices: tuple[int, ...]) -> Poly:
        if indices not in cache:
            cache[indices] = poly_mul(monomial(indices[:-1]), coordinates[indices[-1]])
        return cache[indices]

    answer: Poly = {}
    for indices, coefficient in invariant:
        answer = poly_add(answer, monomial(tuple(indices)), int(coefficient))
    return answer


def trinet_F_pullback(descriptor: Descriptor) -> Poly:
    """Pull back ``abc-t^2`` on a three-port marginal.

    The descriptor is built from exactly three ordered labels.  We embed the
    assignments into four positions with a zero fourth character, so the
    relevant coordinates in ``jc_representatives`` are
    ``(1,1,0,0)``, ``(1,0,1,0)``, ``(0,1,1,0)``, and ``(1,2,3,0)``.
    """
    representatives = jc_representatives()
    indexes = {
        assignment: representatives.index(assignment)
        for assignment in ((1, 1, 0, 0), (1, 0, 1, 0), (0, 1, 1, 0), (1, 2, 3, 0))
    }
    coordinates = coordinate_polynomials(descriptor)
    a = coordinates[indexes[(1, 1, 0, 0)]]
    b = coordinates[indexes[(1, 0, 1, 0)]]
    c = coordinates[indexes[(0, 1, 1, 0)]]
    t = coordinates[indexes[(1, 2, 3, 0)]]
    return poly_add(poly_mul(poly_mul(a, b), c), poly_mul(t, t), scale=-1)


def parse_literal(path: Path, name: str):
    module = ast.parse(path.read_text())
    for node in module.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return ast.literal_eval(node.value)
    raise KeyError(name)


def invariant_orbit(templates: Iterable[Sequence[tuple[Sequence[int], int]]]):
    reps = jc_representatives()
    rep_index = {row: index for index, row in enumerate(reps)}
    colour_maps = [(0, *row) for row in permutations((1, 2, 3))]

    def canon(row: tuple[int, ...]):
        return min(tuple(mapping[value] for value in row) for mapping in colour_maps)

    orbit = set()
    for template in templates:
        for leaf_permutation in permutations(range(4)):
            terms: dict[tuple[int, ...], int] = defaultdict(int)
            for indices, coefficient in template:
                moved = []
                for coordinate in indices:
                    assignment = reps[coordinate]
                    transported = tuple(assignment[leaf_permutation[i]] for i in range(4))
                    moved.append(rep_index[canon(transported)])
                terms[tuple(sorted(moved))] += int(coefficient)
            normalized = tuple(sorted((m, c) for m, c in terms.items() if c))
            if normalized and normalized[0][1] < 0:
                normalized = tuple((m, -c) for m, c in normalized)
            orbit.add(normalized)
    return tuple(sorted(orbit))
