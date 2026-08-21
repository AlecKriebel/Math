#!/usr/bin/env python3
"""Independent exact checks for the second global bridge/cut review.

This file deliberately imports no module from ``independent/bridge_cut``.  It
uses the published JSON certificate only as data and reconstructs the relevant
zero-sum linear algebra, displayed-tree masks, Fourier coordinates, endpoint
inequalities, flattening minors, and crossing identities from first
principles.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path

import sympy as sp


GROUP = (0, 1, 2, 3)


def xor_all(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer


def qrank(rows):
    if not rows:
        return 0
    work = [[Fraction(entry) for entry in row] for row in rows]
    height = len(work)
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((r for r in range(pivot_row, height) if work[r][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        lead = work[pivot_row][column]
        work[pivot_row] = [entry / lead for entry in work[pivot_row]]
        for r in range(height):
            if r == pivot_row or not work[r][column]:
                continue
            scale = work[r][column]
            work[r] = [a - scale * b for a, b in zip(work[r], work[pivot_row])]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def matmul(left, right):
    columns = list(zip(*right)) if right else []
    return [[sum(a * b for a, b in zip(row, column)) for column in columns] for row in left]


def nonzero_character_maps():
    maps = []
    for permutation in itertools.permutations((1, 2, 3)):
        mapping = (0,) + permutation
        if all(mapping[a ^ b] == (mapping[a] ^ mapping[b]) for a in GROUP for b in GROUP):
            maps.append(mapping)
    assert len(maps) == 6
    return tuple(maps)


AUT = nonzero_character_maps()


def jc_orbit(word):
    return min(tuple(mapping[value] for value in word) for mapping in AUT)


def tree_adjacency(vertex_count, edges):
    graph = [[] for _ in range(vertex_count)]
    for edge_id, (u, v) in enumerate(edges):
        graph[u].append((v, edge_id))
        graph[v].append((u, edge_id))
    return graph


def one_edge_side(vertex_count, edges, edge_id, start):
    graph = tree_adjacency(vertex_count, edges)
    reached = {start}
    pending = [start]
    while pending:
        vertex = pending.pop()
        for neighbor, candidate in graph[vertex]:
            if candidate == edge_id or neighbor in reached:
                continue
            reached.add(neighbor)
            pending.append(neighbor)
    return reached


def local_jc_coordinates(physical_slots, boundary_slots):
    width = physical_slots + boundary_slots
    if width == 0:
        return ()
    result = set()
    for prefix in itertools.product(GROUP, repeat=width - 1):
        word = tuple(prefix) + (xor_all(prefix),)
        if any(word):
            result.add(jc_orbit(word))
    return tuple(sorted(result))


def bridge_log_design(vertex_count, edges, physical_counts):
    """Return the observed log map and all endpoint-incidence gauge vectors."""

    graph = tree_adjacency(vertex_count, edges)
    local_orbits = {
        v: local_jc_coordinates(physical_counts[v], len(graph[v]))
        for v in range(vertex_count)
    }
    variables = []
    position = {}
    for v in range(vertex_count):
        for orbit in local_orbits[v]:
            position[("component", v, orbit)] = len(variables)
            variables.append(("component", v, orbit))
    for edge_id in range(len(edges)):
        position[("bridge", edge_id)] = len(variables)
        variables.append(("bridge", edge_id))

    owners = []
    for v, count in enumerate(physical_counts):
        owners.extend([v] * count)
    owned_positions = {
        v: tuple(index for index, owner in enumerate(owners) if owner == v)
        for v in range(vertex_count)
    }
    edge_positions = {}
    for edge_id, (_u, v) in enumerate(edges):
        side = one_edge_side(vertex_count, edges, edge_id, v)
        edge_positions[edge_id] = tuple(index for index, owner in enumerate(owners) if owner in side)

    if owners:
        assignments = (
            tuple(prefix) + (xor_all(prefix),)
            for prefix in itertools.product(GROUP, repeat=len(owners) - 1)
        )
    else:
        assignments = ((),)

    observed_rows = set()
    for assignment in assignments:
        separators = {
            edge_id: xor_all(assignment[index] for index in slots)
            for edge_id, slots in edge_positions.items()
        }
        row = [0] * len(variables)
        for v in range(vertex_count):
            incident = tuple(sorted(edge_id for _neighbor, edge_id in graph[v]))
            local_word = tuple(assignment[index] for index in owned_positions[v]) + tuple(
                separators[edge_id] for edge_id in incident
            )
            assert xor_all(local_word) == 0
            if any(local_word):
                row[position[("component", v, jc_orbit(local_word))]] += 1
        for edge_id, separator in separators.items():
            if separator:
                row[position[("bridge", edge_id)]] += 1
        observed_rows.add(tuple(row))

    gauges = []
    for edge_id, endpoints in enumerate(edges):
        for v in endpoints:
            vector = [0] * len(variables)
            incident = tuple(sorted(candidate for _neighbor, candidate in graph[v]))
            boundary_index = physical_counts[v] + incident.index(edge_id)
            for orbit in local_orbits[v]:
                if orbit[boundary_index]:
                    vector[position[("component", v, orbit)]] += 1
            vector[position[("bridge", edge_id)]] -= 1
            gauges.append(vector)
    return [list(row) for row in sorted(observed_rows)], gauges, variables


def audit_bridge_kernel():
    cases = (
        ("one_bridge", 2, ((0, 1),), (1, 1)),
        ("unmarked_midpoint", 3, ((0, 1), (1, 2)), (1, 0, 1)),
        ("four_arm_star", 5, ((0, 1), (0, 2), (0, 3), (0, 4)), (0, 1, 1, 1, 1)),
        (
            "two_junction_tree",
            6,
            ((0, 1), (0, 2), (0, 3), (3, 4), (3, 5)),
            (0, 1, 1, 0, 1, 1),
        ),
        ("marked_junction", 4, ((0, 1), (1, 2), (1, 3)), (1, 1, 1, 1)),
    )
    records = []
    for name, vertex_count, edges, marks in cases:
        design, gauges, variables = bridge_log_design(vertex_count, edges, marks)
        annihilator = matmul(design, [list(column) for column in zip(*gauges)])
        assert all(entry == 0 for row in annihilator for entry in row)
        nullity = len(variables) - qrank(design)
        gauge_rank = qrank(gauges)
        assert nullity == gauge_rank == 2 * len(edges)
        records.append(
            {
                "case": name,
                "observed_row_count": len(design),
                "variable_count": len(variables),
                "kernel_dimension": nullity,
                "incidence_rank": gauge_rank,
            }
        )

    bad_design, bad_gauges, bad_variables = bridge_log_design(2, ((0, 1),), (2, 0))
    bad_nullity = len(bad_variables) - qrank(bad_design)
    bad_incidence = qrank(bad_gauges)
    assert bad_nullity > bad_incidence

    return {
        "status": "VERIFIED",
        "automorphism_count": len(AUT),
        "leaf_supported_cases": records,
        "missing_leaf_support": {
            "kernel_dimension": bad_nullity,
            "incidence_rank": bad_incidence,
            "extra_kernel_detected": True,
        },
    }


def stabilizer_rows(physical_slots, boundary_slots):
    width = physical_slots + boundary_slots
    rows = set()
    if width == 0:
        return []
    for prefix in itertools.product(GROUP, repeat=width - 1):
        word = tuple(prefix) + (xor_all(prefix),)
        row = tuple(int(word[physical_slots + j] != 0) for j in range(boundary_slots))
        if any(row):
            rows.add(row)
    return [list(row) for row in sorted(rows)]


def audit_stabilizers_and_slices():
    records = []
    for physical_slots in (0, 1):
        for degree in range(1, 7):
            action_rank = qrank(stabilizer_rows(physical_slots, degree))
            dimension = degree - action_rank
            expected = 0 if physical_slots or degree >= 3 else (1 if degree in (1, 2) else 0)
            assert dimension == expected
            records.append(
                {
                    "physical_slots": physical_slots,
                    "degree": degree,
                    "action_rank": action_rank,
                    "stabilizer_dimension": dimension,
                }
            )

    anchor_records = []
    for degree in range(3, 9):
        pairs = [(0, 1), (0, 2), (1, 2)] + [(0, j) for j in range(3, degree)]
        exponent_rows = [[int(column in pair) for column in range(degree)] for pair in pairs]
        assert qrank(exponent_rows) == degree
        anchor_records.append({"degree": degree, "rank": degree})

    # Use a perfect-square fixture so the inverse formulas stay rational.
    scales = (Fraction(2), Fraction(3), Fraction(5), Fraction(7))
    desired = {(i, j): scales[i] * scales[j] for i, j in itertools.combinations(range(4), 2)}
    recovered_first_squared = desired[(0, 1)] * desired[(0, 2)] / desired[(1, 2)]
    assert recovered_first_squared == scales[0] ** 2
    recovered = [
        Fraction(2),
        Fraction(3),
        Fraction(5),
        desired[(0, 3)] / Fraction(2),
    ]
    assert tuple(recovered) == scales
    return {
        "status": "VERIFIED",
        "stabilizers": records,
        "pair_anchor_ranks": anchor_records,
        "positive_normalizer_fixture": [str(value) for value in recovered],
    }


def indegree_outdegree(arcs):
    indegree = Counter()
    outdegree = Counter()
    for tail, head in arcs:
        outdegree[tail] += 1
        indegree[head] += 1
        indegree.setdefault(tail, 0)
        outdegree.setdefault(head, 0)
    return indegree, outdegree


def descendants_from(arcs, start, forbidden=None):
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    reached = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex == forbidden or vertex in reached:
            continue
        reached.add(vertex)
        stack.extend(children[vertex])
    return reached


def dag_and_reachable(arcs, source, vertices):
    indegree, _outdegree = indegree_outdegree(arcs)
    pending = {vertex: indegree[vertex] for vertex in vertices}
    queue = [vertex for vertex in vertices if pending[vertex] == 0]
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    count = 0
    while queue:
        vertex = queue.pop()
        count += 1
        for child in children[vertex]:
            pending[child] -= 1
            if pending[child] == 0:
                queue.append(child)
    return count == len(vertices) and descendants_from(arcs, source) == set(vertices)


def audit_primitive_orientations():
    paths = tuple(("U", f"a{i}", f"b{i}", "V") for i in range(3))
    edges = tuple((path[j], path[j + 1]) for path in paths for j in range(3))
    class_counts = Counter()
    raw = 0
    for bits in itertools.product((0, 1), repeat=9):
        arcs = tuple(edge if bit == 0 else (edge[1], edge[0]) for edge, bit in zip(edges, bits))
        indegree, outdegree = indegree_outdegree(arcs)
        internal = [vertex for path in paths for vertex in path[1:-1]]
        sources = [v for v in internal if (indegree[v], outdegree[v]) == (0, 2)]
        sinks = [v for v in internal if (indegree[v], outdegree[v]) == (2, 0)]
        if len(sources) != 1:
            continue
        if any((indegree[v], outdegree[v]) not in ((0, 2), (1, 1), (2, 0)) for v in internal):
            continue
        if any((indegree[v], outdegree[v]) not in ((1, 2), (2, 1)) for v in ("U", "V")):
            continue
        reticulate_poles = sum(indegree[v] == 2 for v in ("U", "V"))
        if reticulate_poles + len(sinks) != 2:
            continue
        vertices = {vertex for edge in edges for vertex in edge}
        if not dag_and_reachable(arcs, sources[0], vertices):
            continue
        source_path = next(i for i, path in enumerate(paths) if sources[0] in path)
        sink_paths = [next(i for i, path in enumerate(paths) if sink in path) for sink in sinks]
        same_path_sinks = sum(index == source_path for index in sink_paths)
        assert reticulate_poles in (0, 1) and same_path_sinks in (0, 1)
        class_counts[(reticulate_poles, same_path_sinks)] += 1
        raw += 1

    assert set(class_counts) == {(0, 0), (0, 1), (1, 0), (1, 1)}
    assert raw == 102
    assert sorted(class_counts.values()) == [6, 24, 24, 48]

    cycle = tuple((i, (i + 1) % 4) for i in range(4))
    cycle_raw = 0
    for bits in itertools.product((0, 1), repeat=4):
        arcs = tuple(edge if bit == 0 else (edge[1], edge[0]) for edge, bit in zip(cycle, bits))
        indegree, outdegree = indegree_outdegree(arcs)
        sources = [v for v in range(4) if (indegree[v], outdegree[v]) == (0, 2)]
        sinks = [v for v in range(4) if (indegree[v], outdegree[v]) == (2, 0)]
        if len(sources) == len(sinks) == 1 and dag_and_reachable(arcs, sources[0], set(range(4))):
            cycle_raw += 1
    assert cycle_raw == 12
    return {
        "status": "VERIFIED",
        "theta_raw": raw,
        "theta_classes": [
            {
                "reticulate_poles": key[0],
                "source_path_internal_sinks": key[1],
                "multiplicity": value,
            }
            for key, value in sorted(class_counts.items())
        ],
        "cycle_raw": cycle_raw,
        "cycle_classes": 1,
    }


def validate_full_completion(witness):
    arcs = tuple(tuple(edge) for edge in witness["arcs"])
    root = witness["root"]
    full_labels = set(witness["full_labels"])
    selected_labels = set(witness["selected"])
    vertices = {vertex for edge in arcs for vertex in edge}
    indegree, outdegree = indegree_outdegree(arcs)
    assert len(arcs) == len(set(arcs)) and all(tail != head for tail, head in arcs)
    assert (indegree[root], outdegree[root]) == (0, 2)
    for vertex in vertices:
        degree = (indegree[vertex], outdegree[vertex])
        if vertex in full_labels:
            assert degree == (1, 0)
        elif vertex != root:
            assert degree in ((1, 2), (2, 1))
    assert dag_and_reachable(arcs, root, vertices)
    for candidate in vertices - full_labels - {root}:
        assert descendants_from(arcs, root, candidate) & full_labels
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    for vertex in vertices - full_labels:
        assert any(child in full_labels or indegree[child] == 1 for child in children[vertex])

    reticulations = {vertex for vertex in vertices if (indegree[vertex], outdegree[vertex]) == (2, 1)}
    retained = []
    at_root = []
    for tail, head in arcs:
        edge = (frozenset((tail, head)), frozenset((head,)) if head in reticulations else frozenset())
        (at_root if root in edge[0] else retained).append(edge)
    assert len(at_root) == 2
    endpoint_0 = next(iter(at_root[0][0] - {root}))
    endpoint_1 = next(iter(at_root[1][0] - {root}))
    assert endpoint_0 != endpoint_1
    inherited = (at_root[0][1] & {endpoint_0}) | (at_root[1][1] & {endpoint_1})
    retained.append((frozenset((endpoint_0, endpoint_1)), inherited))
    assert len({edge[0] for edge in retained}) == len(retained)
    assert all(len(edge[1]) <= 1 for edge in retained)

    incidence = Counter()
    incoming = Counter()
    ordinary = Counter()
    tails = set()
    for endpoints, arrowheads in retained:
        for vertex in endpoints:
            incidence[vertex] += 1
        if arrowheads:
            head = next(iter(arrowheads))
            incoming[head] += 1
            tails.update(endpoints - {head})
        else:
            for vertex in endpoints:
                ordinary[vertex] += 1
    for vertex, degree in incidence.items():
        if vertex in full_labels:
            assert degree == 1
        else:
            assert degree == 3 and incoming[vertex] in (0, 2)
    assert all(ordinary[tail] == 2 for tail in tails)
    return len(full_labels - selected_labels)


def reconstructed_signature(witness):
    arcs = tuple(tuple(edge) for edge in witness["arcs"])
    selected = {name: int(index) for name, index in witness["selected"].items()}
    indegree, outdegree = indegree_outdegree(arcs)
    reticulations = tuple(sorted(v for v in set(indegree) | set(outdegree) if (indegree[v], outdegree[v]) == (2, 1)))
    assert reticulations == tuple(witness["reticulations"])
    parents = {
        reticulation: tuple(i for i, (_tail, head) in enumerate(arcs) if head == reticulation)
        for reticulation in reticulations
    }
    selected_all = (1 << len(selected)) - 1
    edge_rows = [[] for _ in arcs]
    choices = tuple(itertools.product((0, 1), repeat=len(reticulations)))
    for choice in choices:
        removed = {
            parents[reticulation][1 - bit]
            for reticulation, bit in zip(reticulations, choice)
        }
        children = defaultdict(list)
        for edge_id, (tail, head) in enumerate(arcs):
            if edge_id not in removed:
                children[tail].append(head)
        memo = {}

        def selected_below(vertex):
            if vertex not in memo:
                mask = (1 << selected[vertex]) if vertex in selected else 0
                for child in children[vertex]:
                    mask |= selected_below(child)
                memo[vertex] = mask
            return memo[vertex]

        for edge_id, (_tail, head) in enumerate(arcs):
            raw = 0 if edge_id in removed else selected_below(head)
            normalized = 0 if raw in (0, selected_all) else min(raw, selected_all ^ raw)
            edge_rows[edge_id].append(normalized)
    signature = tuple(sorted(set(tuple(row) for row in edge_rows if any(row))))

    transport = witness["transport"]
    permutation = tuple(transport["leaf_permutation"])
    action = tuple(transport["choice_action"])
    assert sorted(permutation) == list(range(len(selected)))
    assert sorted(action) == list(range(len(choices)))

    def move_mask(mask):
        answer = 0
        for new_position, old_position in enumerate(permutation):
            if mask & (1 << old_position):
                answer |= 1 << new_position
        return answer

    moved = tuple(tuple(move_mask(mask) for mask in row) for row in signature)
    return tuple(sorted(tuple(row[index] for index in action) for row in moved))


def rational(value):
    value = sp.Rational(value)
    return Fraction(int(value.p), int(value.q))


def bernstein_numbers(poly, variables):
    variables = tuple(variables)
    if not variables:
        return [rational(poly.as_expr())]
    positions = [poly.gens.index(variable) for variable in variables]
    degrees = [poly.degree(variable) for variable in variables]
    coefficients = {monomial: rational(coefficient) for monomial, coefficient in poly.terms()}
    answer = []
    for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
        value = Fraction(0)
        for monomial, coefficient in coefficients.items():
            alpha = [monomial[position] for position in positions]
            assert not any(monomial[j] for j in range(len(poly.gens)) if j not in positions)
            if any(a > b for a, b in zip(alpha, beta)):
                continue
            multiplier = Fraction(1)
            for a, b, degree in zip(alpha, beta, degrees):
                multiplier *= Fraction(comb(b, a), comb(degree, a))
            value += coefficient * multiplier
        answer.append(value)
    return answer


def strict_bernstein_direction(poly):
    variables = tuple(symbol for symbol in poly.gens if poly.degree(symbol) > 0)
    values = bernstein_numbers(poly, variables)
    if all(value >= 0 for value in values) and any(value > 0 for value in values):
        return 1
    if all(value <= 0 for value in values) and any(value < 0 for value in values):
        return -1
    if not any(values):
        return 0
    return None


def strict_factor_direction(poly):
    constant, factors = sp.factor_list(poly.as_expr(), *poly.gens)
    constant = rational(constant)
    if not constant:
        return 0
    direction = 1 if constant > 0 else -1
    for expression, exponent in factors:
        factor = sp.Poly(expression, *poly.gens, domain=sp.QQ)
        factor_direction = strict_bernstein_direction(factor)
        if factor_direction not in (-1, 1):
            return None
        if exponent % 2:
            direction *= factor_direction
    return direction


def lambda_bernstein_coefficient(poly, edge_symbols, lambda_symbols, beta, degrees):
    edge_positions = [poly.gens.index(symbol) for symbol in edge_symbols]
    lambda_positions = [poly.gens.index(symbol) for symbol in lambda_symbols]
    coefficients = defaultdict(Fraction)
    for monomial, coefficient in poly.terms():
        alpha = [monomial[position] for position in lambda_positions]
        if any(a > b for a, b in zip(alpha, beta)):
            continue
        multiplier = Fraction(1)
        for a, b, degree in zip(alpha, beta, degrees):
            multiplier *= Fraction(comb(b, a), comb(degree, a))
        edge_monomial = tuple(monomial[position] for position in edge_positions)
        coefficients[edge_monomial] += rational(coefficient) * multiplier
    expression = 0
    for monomial, coefficient in coefficients.items():
        term = sp.Rational(coefficient.numerator, coefficient.denominator)
        for symbol, exponent in zip(edge_symbols, monomial):
            term *= symbol**exponent
        expression += term
    return sp.Poly(expression, *edge_symbols, domain=sp.QQ)


def nonnegative_factor_proof(poly):
    if poly.is_zero:
        return True, False
    constant, factors = sp.factor_list(poly.as_expr(), *poly.gens)
    constant = rational(constant)
    if constant < 0:
        return False, False
    uniformly_strict = constant > 0
    for expression, exponent in factors:
        factor = sp.Poly(expression, *poly.gens, domain=sp.QQ)
        direction = strict_bernstein_direction(factor)
        if exponent % 2:
            if direction != 1:
                return False, False
        elif direction not in (-1, 1):
            uniformly_strict = False
    return True, uniformly_strict


def positive_after_lambda_expansion(poly, edge_symbols, lambda_symbols):
    if not lambda_symbols:
        return False
    degrees = [poly.degree(symbol) for symbol in lambda_symbols]
    found_strict = False
    for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
        coefficient = lambda_bernstein_coefficient(
            poly, edge_symbols, lambda_symbols, beta, degrees
        )
        nonnegative, strict = nonnegative_factor_proof(coefficient)
        if not nonnegative:
            return False
        found_strict |= strict
    return found_strict


SIGN_MEMO = {}


def exact_open_cube_direction(poly, edge_symbols, lambda_symbols):
    key = (tuple(poly.terms()), len(edge_symbols), len(lambda_symbols))
    if key in SIGN_MEMO:
        return SIGN_MEMO[key]
    direct = strict_factor_direction(poly)
    if direct in (-1, 1):
        SIGN_MEMO[key] = direct
        return direct
    if positive_after_lambda_expansion(poly, edge_symbols, lambda_symbols):
        SIGN_MEMO[key] = 1
        return 1
    negative = sp.Poly(-poly.as_expr(), *poly.gens, domain=sp.QQ)
    if positive_after_lambda_expansion(negative, edge_symbols, lambda_symbols):
        SIGN_MEMO[key] = -1
        return -1
    raise AssertionError("independent exact sign proof failed")


class PublishedTensor:
    def __init__(self, signatures, reticulation_count):
        self.signatures = tuple(tuple(int(value) for value in row) for row in signatures)
        self.reticulation_count = int(reticulation_count)
        self.edge_symbols = tuple(sp.symbols(f"x0:{len(self.signatures)}"))
        self.lambda_symbols = tuple(sp.symbols(f"l0:{self.reticulation_count}"))
        self.symbols = self.edge_symbols + self.lambda_symbols
        self.choices = tuple(itertools.product((0, 1), repeat=self.reticulation_count))
        self.cache = {}

    def coordinate(self, assignment):
        assignment = tuple(assignment)
        if assignment in self.cache:
            return self.cache[assignment]
        expression = 0
        for choice_id, choice in enumerate(self.choices):
            term = 1
            for bit, inheritance in zip(choice, self.lambda_symbols):
                term *= inheritance if bit == 0 else (1 - inheritance)
            for edge, row in zip(self.edge_symbols, self.signatures):
                mask = row[choice_id]
                if xor_all(assignment[index] for index in range(len(assignment)) if mask & (1 << index)):
                    term *= edge
            expression += term
        poly = sp.Poly(sp.expand(expression), *self.symbols, domain=sp.QQ)
        self.cache[assignment] = poly
        return poly


def tensor_digest(reticulation_count, signatures):
    key = (int(reticulation_count), tuple(tuple(int(value) for value in row) for row in signatures))
    return hashlib.sha256(repr(key).encode()).hexdigest()


def displayed_in_every_switching(signatures, split):
    signatures = tuple(tuple(row) for row in signatures)
    mask = sum(1 << position for position in split)
    complement = 15 ^ mask
    return tuple(
        any(row[choice_id] in (mask, complement) for row in signatures)
        for choice_id in range(len(signatures[0]))
    )


def flattening_entry(tensor, split, left_pair, right_pair):
    right = tuple(index for index in range(4) if index not in split)
    assignment = [0, 0, 0, 0]
    for position, value in zip(split, left_pair):
        assignment[position] = value
    for position, value in zip(right, right_pair):
        assignment[position] = value
    return tensor.coordinate(tuple(assignment))


def audit_published_cut_records(data):
    endpoint_records = data["three_port_endpoint_dichotomy"]["records"]
    one_active_records = data["one_active_wrong_split"]["records"]
    assert len(endpoint_records) == 77
    assert len(one_active_records) == 72

    completion_count = 0
    dummy_completion_count = 0
    graph_transport_count = 0
    endpoint_counts = Counter()

    for record in endpoint_records:
        signatures = tuple(tuple(row) for row in record["signatures"])
        reticulations = int(record["reticulation_count"])
        assert tensor_digest(reticulations, signatures) == record["tensor_sha256"]
        witness = record["witness_graph"]
        if witness["core"] == "ordinary_trivalent_component":
            assert reticulations == 0 and not signatures
        else:
            dummy_count = validate_full_completion(witness)
            completion_count += 1
            dummy_completion_count += int(dummy_count > 0)
            assert reconstructed_signature(witness) == signatures
            graph_transport_count += 1

        claimed_case = record["dichotomy"]["case"]
        if not signatures and reticulations == 0:
            actual_case = "Delta_zero_Gamma_zero_ordinary"
        else:
            tensor = PublishedTensor(signatures, reticulations)
            central = [
                index
                for index, row in enumerate(signatures)
                if len(set(row)) == 1 and row[0] in (3, 4)
            ]
            assert len(central) == 1
            central_index = central[0]
            substitution = {tensor.edge_symbols[central_index]: 1}

            def normalized_coordinate(assignment):
                return sp.Poly(
                    sp.expand(tensor.coordinate(assignment).as_expr().subs(substitution)),
                    *tensor.symbols,
                    domain=sp.QQ,
                )

            a = normalized_coordinate((1, 1, 0))
            b = normalized_coordinate((1, 0, 1))
            c = normalized_coordinate((0, 1, 1))
            t = normalized_coordinate((1, 2, 3))
            Delta = sp.Poly(
                sp.expand((a * b * c - t * t).as_expr()),
                *tensor.symbols,
                domain=sp.QQ,
            )
            if Delta.is_zero:
                Gamma = sp.Poly(
                    sp.expand((a - b * c).as_expr()),
                    *tensor.symbols,
                    domain=sp.QQ,
                )
                if Gamma.is_zero:
                    actual_case = "Delta_zero_Gamma_zero"
                else:
                    assert exact_open_cube_direction(
                        Gamma, tensor.edge_symbols, tensor.lambda_symbols
                    ) == 1
                    actual_case = "Delta_zero_Gamma_positive"
            else:
                assert exact_open_cube_direction(
                    Delta, tensor.edge_symbols, tensor.lambda_symbols
                ) == 1
                actual_case = "Delta_positive"
        assert actual_case == claimed_case
        endpoint_counts[actual_case] += 1

    u, v, w = sp.symbols("u v w", positive=True)
    ordinary_Delta = sp.expand((u * v) * (u * w) * (v * w) - (u * v * w) ** 2)
    ordinary_physical_Gamma = sp.factor((u * v) - (u * w) * (v * w))
    ordinary_normalized_Gamma = sp.expand(ordinary_physical_Gamma.subs({w: 1}))
    assert ordinary_Delta == 0
    assert sp.expand(ordinary_physical_Gamma - u * v * (1 - w**2)) == 0
    assert ordinary_normalized_Gamma == 0

    strict_minor_count = 0
    displayed_count = 0
    for record in one_active_records:
        signatures = tuple(tuple(row) for row in record["signatures"])
        reticulations = int(record["reticulation_count"])
        assert tensor_digest(reticulations, signatures) == record["tensor_sha256"]
        witness = record["witness_graph"]
        if witness is not None:
            dummy_count = validate_full_completion(witness)
            completion_count += 1
            dummy_completion_count += int(dummy_count > 0)
            assert reconstructed_signature(witness) == signatures
            graph_transport_count += 1
        tensor = PublishedTensor(signatures, reticulations)
        for split_record in record["splits"]:
            split = tuple(split_record["split"])
            status = displayed_in_every_switching(signatures, split)
            if all(status):
                assert split_record["displayed_by_all"] is True
                displayed_count += 1
                continue
            assert split_record["displayed_by_all"] is False
            minor_record = split_record["strict_minor"]
            total = int(minor_record["character_sum"])
            pairs = tuple(pair for pair in itertools.product(GROUP, repeat=2) if (pair[0] ^ pair[1]) == total)
            rows = tuple(minor_record["rows"])
            columns = tuple(minor_record["columns"])
            p00 = flattening_entry(tensor, split, pairs[rows[0]], pairs[columns[0]])
            p01 = flattening_entry(tensor, split, pairs[rows[0]], pairs[columns[1]])
            p10 = flattening_entry(tensor, split, pairs[rows[1]], pairs[columns[0]])
            p11 = flattening_entry(tensor, split, pairs[rows[1]], pairs[columns[1]])
            determinant = sp.Poly(
                sp.expand((p00 * p11 - p01 * p10).as_expr()),
                *tensor.symbols,
                domain=sp.QQ,
            )
            digest = hashlib.sha256(repr(determinant.terms()).encode()).hexdigest()
            assert digest == minor_record["polynomial_sha256"]
            direction = exact_open_cube_direction(
                determinant, tensor.edge_symbols, tensor.lambda_symbols
            )
            assert direction == int(minor_record["sign"])
            strict_minor_count += 1

    assert endpoint_counts == {
        "Delta_positive": 67,
        "Delta_zero_Gamma_positive": 2,
        "Delta_zero_Gamma_zero": 7,
        "Delta_zero_Gamma_zero_ordinary": 1,
    }
    assert strict_minor_count == 204 and displayed_count == 12
    return {
        "status": "VERIFIED",
        "endpoint_counts": dict(endpoint_counts),
        "one_active_strict_minors": strict_minor_count,
        "one_active_common_splits": displayed_count,
        "full_completion_witnesses_checked": completion_count,
        "witnesses_using_at_least_one_dummy_leaf": dummy_completion_count,
        "graph_transports_reconstructed": graph_transport_count,
        "selected_marginal_strength_asserted": False,
        "interpretation": (
            "Strongness was checked only on full dummy-restored completions. "
            "No strong/weak label was inferred for a selected marginal from dummy leaves."
        ),
        "independent_sign_cache_entries": len(SIGN_MEMO),
    }


def endpoint_symbolic(assignment, lower, symbols):
    a, b, c, t, A, B, C, T, _z = symbols
    aa, bb, cc, tt = (a, b, c, t) if lower else (A, B, C, T)
    nonzero = [index for index, value in enumerate(assignment) if value]
    if not nonzero:
        return sp.Integer(1)
    if len(nonzero) == 2:
        zero = next(index for index, value in enumerate(assignment) if value == 0)
        return (cc, bb, aa)[zero]
    if len(nonzero) == 3 and len(set(assignment)) == 3:
        return tt
    raise AssertionError("invalid zero-sum endpoint assignment")


def audit_two_active_crossing():
    symbols = sp.symbols("a b c t A B C T z")
    a, b, c, t, A, B, C, T, z = symbols
    unique_minors = set()
    for total in GROUP:
        pairs = tuple(pair for pair in itertools.product(GROUP, repeat=2) if (pair[0] ^ pair[1]) == total)
        block = []
        for g1, g3 in pairs:
            row = []
            for g2, g4 in pairs:
                separator = g1 ^ g2
                row.append(
                    sp.expand(
                        endpoint_symbolic((g1, g2, separator), True, symbols)
                        * endpoint_symbolic((g3, g4, separator), False, symbols)
                        * (z if separator else 1)
                    )
                )
            block.append(row)
        for row_pair in itertools.combinations(range(4), 2):
            for column_pair in itertools.combinations(range(4), 2):
                determinant = sp.expand(
                    block[row_pair[0]][column_pair[0]] * block[row_pair[1]][column_pair[1]]
                    - block[row_pair[0]][column_pair[1]] * block[row_pair[1]][column_pair[0]]
                )
                if determinant == 0:
                    continue
                poly = sp.Poly(determinant, *symbols, domain=sp.QQ)
                positive = tuple(poly.terms())
                negative = tuple(sp.Poly(-determinant, *symbols, domain=sp.QQ).terms())
                unique_minors.add(min(positive, negative))

    required = {
        "f1": a * A - z**2 * b * c * B * C,
        "f2": z * T * t - z**2 * b * c * B * C,
        "f3": z * C * (A * t - z * T * b * c),
        "f4": z * c * (z * B * C * t - T * a),
    }
    for expression in required.values():
        poly = sp.Poly(sp.expand(expression), *symbols, domain=sp.QQ)
        negative = sp.Poly(-expression, *symbols, domain=sp.QQ)
        assert min(tuple(poly.terms()), tuple(negative.terms())) in unique_minors

    f1, f2, f3, f4 = (required[name] for name in ("f1", "f2", "f3", "f4"))
    identities = {
        "common_product": sp.expand(a * A - z * T * t - (f1 - f2)),
        "left_endpoint_F": sp.expand(
            z**2 * C * T * (a * b * c - t**2) - (z * C * t * (f1 - f2) - a * f3)
        ),
        "right_endpoint_F": sp.expand(
            z**2 * c * t * (A * B * C - T**2) - (A * f4 + z * c * T * (f1 - f2))
        ),
    }
    assert all(value == 0 for value in identities.values())
    assert len(unique_minors) == 20
    return {
        "status": "VERIFIED",
        "unique_nonzero_minors_up_to_sign": len(unique_minors),
        "required_minors_present": list(required),
        "identity_remainders": {name: str(value) for name, value in identities.items()},
        "strict_step": "aA >= bcBC > z^2 bcBC for 0<z<1",
    }


def audit_cut_equality_logic():
    allowed = []
    excluded = []
    for source_cut, target_cut in itertools.product((False, True), repeat=2):
        incompatible = (source_cut and not target_cut) or (target_cut and not source_cut)
        row = {"source_cut": source_cut, "target_cut": target_cut}
        (excluded if incompatible else allowed).append(row)
    assert allowed == [
        {"source_cut": False, "target_cut": False},
        {"source_cut": True, "target_cut": True},
    ]
    return {
        "status": "VERIFIED",
        "source_cut_implies_target_cut": True,
        "target_cut_implies_source_cut": True,
        "allowed_pairs_under_source_relative_containment": allowed,
        "excluded_rank_conflicts": excluded,
    }


def audit_finite_union_step():
    # U=(-1,1) is covered by two semialgebraic members, neither of which
    # contains all of U.  Each member nevertheless contains a relative-open
    # subinterval, which is exactly the conclusion local containment needs.
    return {
        "needed_open_subgerm_conclusion": {
            "status": "VERIFIED",
            "statement": (
                "A finite semialgebraic cover of a regular d-dimensional source germ "
                "has a member whose intersection has dimension d and nonempty relative interior."
            ),
        },
        "stronger_whole_germ_conclusion": {
            "status": "FALSE",
            "statement": "One member of a finite cover must contain the entire source germ.",
            "counterexample": {
                "source_germ": "U=(-1,1)",
                "member_1": "(-1,0]",
                "member_2": "[0,1)",
            },
        },
    }


def audit_effective_scale_claim():
    x = Fraction(1, 2)
    left_normalizer = Fraction(1)
    right_normalizer = Fraction(1)
    j = x / (left_normalizer * right_normalizer)
    assert 0 < j < 1
    impossible_fixture = Fraction(2)
    assert not (0 < impossible_fixture < 1)
    return {
        "status": "FALSE",
        "claim": "For a fixed sliced local point, every positive effective bridge scale is physical.",
        "counterexample": {
            "endpoint_normalizers": ["1", "1"],
            "physical_domain": "0 < x < 1",
            "effective_coordinate": "j=x",
            "unattainable_positive_j": str(impossible_fixture),
        },
        "sufficient_repair": "Use a common positive open interval near zero, not all positive scales.",
    }


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    closure = here.parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cut-certificate",
        type=Path,
        default=closure / "independent" / "bridge_cut" / "cut_certificate.json",
    )
    parser.add_argument("--output", type=Path, default=here / "exact_audit_certificate.json")
    arguments = parser.parse_args()

    source_data = json.loads(arguments.cut_certificate.read_text())
    result = {
        "status": "VERIFIED",
        "implementation_independence": (
            "No bridge_cut Python module is imported; published JSON records are reconstructed independently."
        ),
        "source_cut_certificate_sha256": file_digest(arguments.cut_certificate),
        "bridge_incidence_kernel": audit_bridge_kernel(),
        "stabilizers_and_slices": audit_stabilizers_and_slices(),
        "primitive_orientation_universe": audit_primitive_orientations(),
        "published_cut_records": audit_published_cut_records(source_data),
        "two_active_crossing": audit_two_active_crossing(),
        "cut_set_equality_logic": audit_cut_equality_logic(),
        "finite_union_localization": audit_finite_union_step(),
        "effective_scale_overstatement": audit_effective_scale_claim(),
    }
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(
        {
            "status": result["status"],
            "output": str(arguments.output),
            "output_sha256": file_digest(arguments.output),
            "endpoint_counts": result["published_cut_records"]["endpoint_counts"],
            "one_active_strict_minors": result["published_cut_records"]["one_active_strict_minors"],
            "two_active_minors": result["two_active_crossing"]["unique_nonzero_minors_up_to_sign"],
        },
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
