#!/usr/bin/env python3
"""Independent exact spot checks of representative four-port obstructions.

The polynomial checks read literal rooted graphs from the frozen orbit lock.
The quotient check separately reads the exhaustive replay's flat final-residue
registry and compares its independently reconstructed partition with the
derived quotient.  The switching compiler, sparse polynomial algebra,
Jacobian evaluator, graph-automorphism search, and factorization checks are
local; no package producer, verifier, atlas module, or stored separator/rank
certificate is imported.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
from itertools import permutations, product
import json
from pathlib import Path
import random

import networkx as nx


if not __debug__:
    raise RuntimeError("run without -O so fail-closed assertions remain active")


CH4 = tuple(prefix + (prefix[0] ^ prefix[1] ^ prefix[2],) for prefix in product(range(4), repeat=3))
CH3 = tuple(prefix + (prefix[0] ^ prefix[1],) for prefix in product(range(4), repeat=2))


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def locate_proof_root(package_root):
    for candidate in (package_root / "proof_package", package_root):
        if (candidate / "input_frozen/k3p_cloud_artifacts/K3P_14_ORBIT_LOCK.json").is_file():
            return candidate
    raise FileNotFoundError("could not locate proof_package beneath --package-root")


def compose(left, right):
    """Return left after right for permutations stored as image tuples."""
    return tuple(left[right[index]] for index in range(4))


def literal_mixed_incidence_graph(literal, label_permutation=None):
    """Root-suppress a literal DAG and encode mixed-edge arrowheads by incidence."""

    label_permutation = label_permutation or tuple(range(4))
    nodes = {}
    for row in literal["nodes"]:
        assert row["id"] not in nodes
        label = row.get("label")
        if isinstance(label, int):
            label = label_permutation[label]
        nodes[row["id"]] = {"role": row["role"], "label": label}

    arcs = tuple((row["tail"], row["head"]) for row in literal["arcs"])
    assert len(arcs) == len(set(arcs))
    assert all(tail in nodes and head in nodes and tail != head for tail, head in arcs)
    roots = [node for node, data in nodes.items() if data["role"] == "root"]
    assert len(roots) == 1
    root = roots[0]
    children = tuple(head for tail, head in arcs if tail == root)
    assert len(children) == 2 and len(set(children)) == 2

    mixed_edges = {}
    for tail, head in arcs:
        if tail == root:
            continue
        endpoints = frozenset((tail, head))
        assert len(endpoints) == 2 and endpoints not in mixed_edges
        mixed_edges[endpoints] = (
            frozenset((head,)) if nodes[head]["role"] == "retic" else frozenset()
        )
    suppressed_root_edge = frozenset(children)
    assert suppressed_root_edge not in mixed_edges
    mixed_edges[suppressed_root_edge] = frozenset(
        child for child in children if nodes[child]["role"] == "retic"
    )

    incidence = nx.Graph()
    for node, data in nodes.items():
        if node != root:
            incidence.add_node(("vertex", node), kind="vertex", label=data["label"])
    for index, (endpoints, heads) in enumerate(
        sorted(mixed_edges.items(), key=lambda row: tuple(sorted(map(repr, row[0]))))
    ):
        edge_node = ("edge", index)
        incidence.add_node(edge_node, kind="edge", label=None)
        for endpoint in endpoints:
            incidence.add_edge(edge_node, ("vertex", endpoint), head=endpoint in heads)
    return incidence


def inverse_permutation(permutation):
    return tuple(permutation.index(index) for index in range(4))


def literal_port_automorphisms(literal, normalizer=None):
    """Compute port relabellings induced by mixed-graph automorphisms."""
    normalizer = normalizer or tuple(range(4))
    identity = literal_mixed_incidence_graph(literal, normalizer)

    def node_match(left, right):
        return left["kind"] == right["kind"] and left["label"] == right["label"]

    def edge_match(left, right):
        return left["head"] == right["head"]

    result = []
    for permutation in permutations(range(4)):
        relabelled = literal_mixed_incidence_graph(
            literal, compose(permutation, normalizer)
        )
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            identity,
            relabelled,
            node_match=node_match,
            edge_match=edge_match,
        )
        if matcher.is_isomorphic():
            result.append(tuple(permutation))
    assert tuple(range(4)) in result
    result = tuple(sorted(result))
    assert all(compose(left, right) in result for left in result for right in result)
    return result


def residue_quotient(proof_root, lock):
    """Recompute the 38-record double-coset quotient from flat residue rows."""
    registry_path = (
        proof_root
        / "four_port_atlas/full_universe_replay/artifacts/eligible_class_registry.json.gz"
    )
    with gzip.open(registry_path, "rt", encoding="utf-8") as handle:
        registry = json.load(handle)
    residue = []
    for record in registry["records"]:
        for member in record["members"]:
            if member["category"] == "post_quadratic_residue":
                item = dict(member)
                item["class_id"] = record["class_id"]
                item["source_index"] = record["source_index"]
                item["source_rank"] = record["source_rank"]
                item["target_rank"] = record["target_rank"]
                residue.append(item)
    assert len(residue) == 40
    assert len({item["class_id"] for item in residue}) == 40
    lexicographic = list(permutations(range(4)))
    assert all(
        tuple(item["port_permutation"]) == lexicographic[item["permutation_index"]]
        for item in residue
    )
    assert all(
        item["selected_graph_sha256"] == item["target_graph_sha256"]
        and not item["target_has_dummy_completion"]
        for item in residue
    )

    ordinary = [item for item in residue if item["source_index"] != 5]
    sink_swaps = [item for item in residue if item["source_index"] == 5]
    assert len(ordinary) == 38 and len(sink_swaps) == 2
    assert {tuple(item["port_permutation"]) for item in sink_swaps} == {
        (0, 1, 3, 2), (1, 0, 2, 3)
    }
    assert all(item["source_rank"] == item["target_rank"] == 24 for item in sink_swaps)

    literal_by_source = {}
    literal_by_target = {}
    for record in lock["records"]:
        literal_by_source.setdefault(record["source_index"], record["source_literal_graph"])
        literal_by_target.setdefault(
            record["target_index"],
            (
                record["target_literal_graph"],
                inverse_permutation(tuple(record["representative_permutation"])),
            ),
        )
    assert set(item["source_index"] for item in ordinary) == {0, 1, 2, 3, 4}
    assert set(item["target_index"] for item in ordinary) == {80, 822}
    source_geometric_groups = {
        index: literal_port_automorphisms(literal_by_source[index])
        for index in sorted({item["source_index"] for item in ordinary})
    }
    target_groups = {
        index: literal_port_automorphisms(*literal_by_target[index])
        for index in sorted({item["target_index"] for item in ordinary})
    }
    pair_members = defaultdict(set)
    for item in ordinary:
        pair_members[(item["source_index"], item["target_index"])].add(
            tuple(item["port_permutation"])
        )
    assert sorted(map(len, pair_members.values())) == [4, 4, 4, 4, 22]
    h_pair = next(pair for pair, members in pair_members.items() if len(members) == 22)
    identity = tuple(range(4))
    source_action_groups = {
        index: source_geometric_groups[index] if index == h_pair[0] else (identity,)
        for index in source_geometric_groups
    }
    assert len(source_geometric_groups[h_pair[0]]) == 2
    assert all(group == (identity,) for index, group in source_action_groups.items() if index != h_pair[0])
    assert {index: len(group) for index, group in target_groups.items()} == {80: 2, 822: 2}

    # Every target literal in the lock is already in its representative's
    # displayed label frame.  Recover the base frame, then independently check
    # that the directly computed displayed group is the conjugate pi G pi^-1.
    displayed_frame_checks = 0
    for record in lock["records"]:
        target_index = record["target_index"]
        if target_index not in target_groups:
            continue
        representative = tuple(record["representative_permutation"])
        normalizer = inverse_permutation(representative)
        recovered_base = literal_port_automorphisms(
            record["target_literal_graph"], normalizer
        )
        assert recovered_base == target_groups[target_index]
        displayed = literal_port_automorphisms(record["target_literal_graph"])
        expected_displayed = tuple(sorted(
            compose(representative, compose(automorphism, normalizer))
            for automorphism in recovered_base
        ))
        assert displayed == expected_displayed
        displayed_frame_checks += 1

    remaining = {
        (item["source_index"], item["target_index"], tuple(item["port_permutation"]))
        for item in ordinary
    }
    assert len(remaining) == 38
    quotient = []
    while remaining:
        seed = min(remaining)
        source_index, target_index, permutation = seed
        double_coset = {
            (
                source_index,
                target_index,
                compose(source_auto, compose(permutation, target_auto)),
            )
            for source_auto in source_action_groups[source_index]
            for target_auto in target_groups[target_index]
        }
        orbit = remaining & double_coset
        assert orbit and double_coset.issubset(remaining | orbit)
        quotient.append(tuple(sorted(item[2] for item in orbit)))
        remaining -= orbit
    quotient = tuple(sorted(quotient))
    assert len(quotient) == 14
    assert sorted(map(len, quotient)) == [2] * 9 + [4] * 5

    derived_path = (
        proof_root
        / "four_port_atlas/full_universe_replay/artifacts/DERIVED_RESIDUE_QUOTIENT.json"
    )
    derived = json.loads(derived_path.read_text(encoding="utf-8"))
    stored_partition = tuple(sorted(
        tuple(sorted(tuple(permutation) for permutation in orbit["raw_members"]))
        for orbit in derived["orbits"]
    ))
    assert quotient == stored_partition
    assert derived["post_quadratic_raw_records"] == 40
    assert derived["raw_records_in_fourteen_orbits"] == 38
    assert derived["separate_sink_swap_records"] == 2
    assert derived["canonical_orbits"] == 14
    return {
        "flat_residue_records": len(residue),
        "ordinary_records": len(ordinary),
        "separate_sink_swaps": len(sink_swaps),
        "source_mixed_geometric_automorphism_groups_recomputed": {
            str(index): [list(permutation) for permutation in group]
            for index, group in source_geometric_groups.items()
        },
        "source_relation_census_action_groups": {
            str(index): [list(permutation) for permutation in group]
            for index, group in source_action_groups.items()
        },
        "target_base_mixed_automorphism_groups_recomputed": {
            str(index): [list(permutation) for permutation in group]
            for index, group in target_groups.items()
        },
        "target_displayed_frame_conjugations_checked": displayed_frame_checks,
        "double_coset_orbits_recomputed": len(quotient),
        "orbit_size_multiset": sorted(map(len, quotient)),
        "partition_matches_derived_quotient": True,
        "sink_swap_permutations": sorted(item["port_permutation"] for item in sink_swaps),
        "boundary": (
            "The flat 40-row post-quadratic residue is read from the exhaustive replay registry. "
            "Its 38+2 split, root-suppressed arrowhead-preserving mixed-graph automorphism groups, "
            "displayed-frame conjugations, and fourteen-orbit double-coset quotient are independently "
            "recomputed; the preceding 405,216-to-40 filtering is not."
        ),
    }


@dataclass(frozen=True)
class Descriptor:
    edge_count: int
    retic_count: int
    outputs: tuple
    signatures: tuple


class Graph:
    def __init__(self, literal):
        self.nodes = {row["id"]: row for row in literal["nodes"]}
        self.arcs = tuple(sorted((row["tail"], row["head"]) for row in literal["arcs"]))
        self.incoming = defaultdict(list)
        for tail, head in self.arcs:
            self.incoming[head].append(tail)


def descendants(graph, kept):
    children = defaultdict(list)
    for tail, head in kept:
        children[tail].append(head)
    memo = {}

    def visit(node):
        if node in memo:
            return memo[node]
        label = graph.nodes[node].get("label")
        mask = (1 << label) if isinstance(label, int) else 0
        for child in children[node]:
            mask |= visit(child)
        memo[node] = mask
        return mask

    for node in graph.nodes:
        visit(node)
    return {edge: memo[edge[1]] for edge in kept}


def sector(mask, chars):
    value = 0
    index = 0
    while mask:
        if mask & 1:
            value ^= chars[index]
        index += 1
        mask >>= 1
    return value


def inheritance_expansion(bits):
    result = {0: 1}
    for index, selected_second_parent in enumerate(bits):
        nxt = defaultdict(int)
        for mask, coefficient in result.items():
            if selected_second_parent:
                nxt[mask | (1 << index)] += coefficient
            else:
                nxt[mask] += coefficient
                nxt[mask | (1 << index)] -= coefficient
        result = {mask: coefficient for mask, coefficient in nxt.items() if coefficient}
    return tuple(sorted(result.items()))


def compile_variant(graph, reticulations, parent_orders):
    selected_arms = {
        edge for edge in graph.arcs
        if graph.nodes[edge[1]]["role"] == "leaf"
        and isinstance(graph.nodes[edge[1]].get("label"), int)
    }
    switchings = []
    for bits in product((0, 1), repeat=len(reticulations)):
        removed = set()
        for index, reticulation in enumerate(reticulations):
            keep = parent_orders[index][bits[index]]
            removed.update(
                (parent, reticulation)
                for parent in graph.incoming[reticulation]
                if parent != keep
            )
        kept = tuple(edge for edge in graph.arcs if edge not in removed)
        switchings.append((bits, kept, descendants(graph, kept)))

    raw_signatures = []
    internal = []
    for edge in graph.arcs:
        if edge in selected_arms:
            continue
        signature = []
        for _, kept, masks in switchings:
            signature.extend(
                (sector(masks[edge], chars) if edge in kept else 0)
                for chars in CH4
            )
        if any(signature):
            internal.append(edge)
            raw_signatures.append(tuple(signature))
    assert len(raw_signatures) == len(set(raw_signatures)), (
        "duplicate literal switching signatures require product-coordinate collapse",
        tuple(signature for signature, count in Counter(raw_signatures).items() if count > 1),
    )
    signatures = tuple(sorted(set(raw_signatures)))
    edge_class = {edge: signatures.index(signature) for edge, signature in zip(internal, raw_signatures)}

    width = 3 * len(signatures) + len(reticulations)
    outputs = []
    for chars in CH4:
        polynomial = defaultdict(Q)
        for bits, kept, masks in switchings:
            exponent = [0] * width
            for edge in kept:
                if edge not in edge_class:
                    continue
                value = sector(masks[edge], chars)
                if value:
                    exponent[3 * edge_class[edge] + value - 1] += 1
            for mask, coefficient in inheritance_expansion(bits):
                term = exponent.copy()
                for index in range(len(reticulations)):
                    if (mask >> index) & 1:
                        term[3 * len(signatures) + index] += 1
                polynomial[tuple(term)] += coefficient
        outputs.append(tuple(sorted((term, coefficient) for term, coefficient in polynomial.items() if coefficient)))
    return Descriptor(len(signatures), len(reticulations), tuple(outputs), signatures)


def all_parameter_conventions(literal):
    graph = Graph(literal)
    reticulation_set = tuple(sorted(
        node for node, data in graph.nodes.items() if data["role"] == "retic"
    ))
    for reticulations in permutations(reticulation_set):
        pairs = [tuple(sorted(graph.incoming[node])) for node in reticulations]
        for flips in product((0, 1), repeat=len(reticulations)):
            parent_orders = tuple((pair[flip], pair[1-flip]) for pair, flip in zip(pairs, flips))
            yield compile_variant(graph, reticulations, parent_orders)


def compile_graph(literal):
    return min(
        all_parameter_conventions(literal),
        key=lambda descriptor: (
            descriptor.retic_count,
            descriptor.edge_count,
            descriptor.outputs,
            descriptor.signatures,
        ),
    )


def poly_dict(output):
    return dict(output)


def add(*terms):
    result = defaultdict(Q)
    for scalar, polynomial in terms:
        for exponent, coefficient in polynomial.items():
            result[exponent] += Q(scalar) * coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def mul(*polynomials):
    if not polynomials:
        return {(): Q(1)}
    result = polynomials[0]
    for right in polynomials[1:]:
        nxt = defaultdict(Q)
        for left_exp, left_coefficient in result.items():
            for right_exp, right_coefficient in right.items():
                nxt[tuple(a+b for a, b in zip(left_exp, right_exp))] += left_coefficient * right_coefficient
        result = {exponent: coefficient for exponent, coefficient in nxt.items() if coefficient}
    return result


def variable(width, index):
    return {tuple(int(position == index) for position in range(width)): Q(1)}


def one(width):
    return {(0,) * width: Q(1)}


def quartic_pullback(descriptor, terms):
    outputs = [poly_dict(output) for output in descriptor.outputs]
    return add(*[
        (coefficient, mul(*(outputs[index] for index in indices)))
        for coefficient, indices in terms
    ])


def evaluate(polynomial, point):
    total = Q(0)
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def jacobian_at(descriptor, rows, point):
    matrix = []
    for output_index in rows:
        row = []
        for parameter_index in range(len(point)):
            value = Q(0)
            for exponent, coefficient in descriptor.outputs[output_index]:
                if exponent[parameter_index] == 0:
                    continue
                term = coefficient * exponent[parameter_index]
                for index, power in enumerate(exponent):
                    adjusted = power - int(index == parameter_index)
                    if adjusted:
                        term *= point[index] ** adjusted
                value += term
            row.append(value)
        matrix.append(row)
    return matrix


def rref_rank_and_pivots(matrix):
    work = [list(row) for row in matrix]
    rows, columns = len(work), len(work[0])
    pivots = []
    pivot_row = 0
    for column in range(columns):
        selected = next((index for index in range(pivot_row, rows) if work[index][column]), None)
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [value/pivot for value in work[pivot_row]]
        for index in range(rows):
            if index != pivot_row and work[index][column]:
                factor = work[index][column]
                work[index] = [left-factor*right for left, right in zip(work[index], work[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row, pivots


def determinant(matrix):
    work = [list(row) for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot_row = next((index for index in range(column, len(work)) if work[index][column]), None)
        if pivot_row is None:
            return Q(0)
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            answer = -answer
        pivot = work[column][column]
        answer *= pivot
        for index in range(column + 1, len(work)):
            if work[index][column]:
                factor = work[index][column] / pivot
                for right in range(column + 1, len(work)):
                    work[index][right] -= factor * work[column][right]
    return answer


def independent_minor(matrix):
    rank, columns = rref_rank_and_pivots(matrix)
    narrowed = [[row[index] for index in columns[:rank]] for row in matrix]
    _, rows = rref_rank_and_pivots([list(row) for row in zip(*narrowed)])
    rows = rows[:rank]
    square = [[matrix[row][column] for column in columns[:rank]] for row in rows]
    value = determinant(square)
    assert value != 0
    return rank, rows, columns[:rank], value


def ct_margin(triple):
    c, g, t = triple
    return min(
        c, g, t, 1-c, 1-g, 1-t,
        1+c-g-t, 1-c+g-t, 1-c-g+t,
        c-g*t, g-c*t, t-c*g,
    )


def own_point(descriptor, seed):
    rng = random.Random(seed)
    point, margins = [], []
    for _ in range(descriptor.edge_count):
        while True:
            denominator = rng.choice((17, 19, 23, 29, 31))
            triple = tuple(Q(rng.randint(4, denominator-4), denominator) for _ in range(3))
            margin = ct_margin(triple)
            if margin > 0:
                point.extend(triple)
                margins.append(margin)
                break
    for _ in range(descriptor.retic_count):
        denominator = rng.choice((11, 13, 17))
        value = Q(rng.randint(2, denominator-2), denominator)
        point.append(value)
        margins.append(min(value, 1-value))
    return point, min(margins)


QHA = (
    (1, (0,24,44,52)), (-1, (0,28,36,56)), (-1, (4,24,32,60)), (1, (4,28,40,48)),
    (1, (8,16,36,60)), (-1, (8,20,44,48)), (-1, (12,16,40,52)), (1, (12,20,32,56)),
)
Q20 = (
    (1, (0,10,35,61)), (-1, (0,11,34,61)), (1, (0,14,41,51)), (-1, (0,15,41,50)),
    (-1, (1,10,35,60)), (1, (1,11,34,60)), (-1, (1,14,40,51)), (1, (1,15,40,50)),
)
Q23 = (
    (1, (0,8,45,53)), (1, (0,9,37,60)), (-1, (0,12,37,57)), (-1, (0,13,40,53)),
    (-1, (5,8,45,48)), (-1, (5,9,32,60)), (1, (5,12,32,57)), (1, (5,13,40,48)),
)


def verify_h21_factorization(descriptor):
    width = 3*descriptor.edge_count + descriptor.retic_count
    assert (descriptor.edge_count, descriptor.retic_count) == (8, 2)
    outputs = [poly_dict(output) for output in descriptor.outputs]
    edges = [[variable(width, 3*edge+sector_index) for sector_index in range(3)] for edge in range(8)]
    lambda0, lambda1 = variable(width, 24), variable(width, 25)
    complement0 = add((1, one(width)), (-1, lambda0))
    complement1 = add((1, one(width)), (-1, lambda1))
    a, b, c, d, f, h, i, j = [edges[index][2] for index in range(8)]
    U, V, Z, D, I0 = mul(a, lambda0), mul(j, complement0), mul(c, d, i), mul(d, i), i
    A0, B0 = mul(h, b, lambda1), mul(h, f, complement1)
    A = mul(edges[2][0], edges[3][0], edges[6][0])
    B = mul(edges[2][1], edges[3][1], edges[6][1])
    e2c, e2g = edges[2][0], edges[2][1]
    rhs3 = mul(V, add((1, mul(D, A0)), (1, mul(I0, I0, B0))))
    rhs12 = mul(U, add((1, mul(D, A0)), (1, B0)))
    rhs51 = mul(Z, add((1, A0), (1, mul(D, B0))))
    rhs63 = mul(V, Z, add((1, mul(I0, I0, A0)), (1, mul(D, B0))))
    identities = (
        add((1, mul(I0, outputs[3])), (-1, mul(I0, U)), (-1, rhs3)),
        add((1, outputs[12]), (-1, rhs12), (-1, mul(V, I0))),
        add((1, outputs[15]), (-1, mul(D, A0)), (-1, B0)),
        add((1, outputs[20]), (-1, A)),
        add((1, mul(e2g, outputs[27])), (-1, mul(e2g, B0, A)), (-1, mul(A0, e2c, B))),
        add((1, mul(e2c, outputs[39])), (-1, mul(e2c, B0, B)), (-1, mul(A0, e2g, A))),
        add((1, outputs[40]), (-1, B)),
        add((1, mul(I0, outputs[48])), (-1, mul(I0, U, outputs[51])), (-1, mul(V, Z))),
        add((1, mul(D, outputs[51])), (-1, rhs51)),
        add((1, outputs[60]), (-1, Z)),
        add((1, mul(D, I0, outputs[63])), (-1, mul(D, I0, U, Z)), (-1, rhs63)),
    )
    assert all(not identity for identity in identities)
    return {
        "exact_identity_count": len(identities),
        "rational_generators": ["U", "V", "Z", "D", "I", "A0", "B0", "A", "B", "rho=e2C/e2G"],
        "saturation_divisors": ["e2C", "e2G", "D=d*i", "I=i"],
        "divisors_nonzero_on_strict_Dplus": True,
        "target_directional_rank_upper_bound": 10,
    }


def compress_for_omitted_port(descriptor, omitted):
    rows = [index for index, chars in enumerate(CH4) if chars[omitted] == 0]
    occurrences = {}
    for edge_class in range(descriptor.edge_count):
        signature = []
        for output_index in rows:
            for exponent, _ in descriptor.outputs[output_index]:
                signature.extend(exponent[3*edge_class:3*edge_class+3])
        occurrences[edge_class] = tuple(signature)
    grouped = defaultdict(list)
    for edge_class, signature in occurrences.items():
        grouped[signature].append(edge_class)
    active = sorted((group for signature, group in grouped.items() if any(signature)), key=min)
    invisible = [group for signature, group in grouped.items() if not any(signature)]
    assert len(active) == 4
    reticulations = [
        index for index in range(descriptor.retic_count)
        if any(
            any(exponent[3*descriptor.edge_count+index] for exponent, _ in descriptor.outputs[output_index])
            for output_index in rows
        )
    ]
    assert len(reticulations) == 1
    compressed = []
    for output_index in rows:
        polynomial = defaultdict(Q)
        for exponent, coefficient in descriptor.outputs[output_index]:
            new = [0] * 13
            for active_index, group in enumerate(active):
                values = [exponent[3*edge_class:3*edge_class+3] for edge_class in group]
                assert all(value == values[0] for value in values)
                new[3*active_index:3*active_index+3] = values[0]
            new[12] = exponent[3*descriptor.edge_count+reticulations[0]]
            polynomial[tuple(new)] += coefficient
        compressed.append({exponent: coefficient for exponent, coefficient in polynomial.items() if coefficient})
    return compressed, rows, active, invisible, reticulations[0]


def canonical_sunlet(edge_map, flip, port_permutation):
    width = 13
    edges = [[variable(width, 3*edge+sector_index) for sector_index in range(3)] for edge in range(4)]
    inheritance = variable(width, 12)
    complement = add((1, one(width)), (-1, inheritance))
    ea, eb, U, V = [edges[index] for index in edge_map]
    A = [mul(complement if flip else inheritance, ea[index]) for index in range(3)]
    B = [mul(inheritance if flip else complement, eb[index]) for index in range(3)]
    outputs, dependencies = [], []
    for x, y, z in CH3:
        if x == y == z == 0:
            polynomial, dependency = one(width), set()
        elif x == 0:
            polynomial = add((1, A[y-1]), (1, mul(V[y-1], B[y-1])))
            dependency = {("A", y), ("V", y), ("B", y)}
        elif y == 0:
            polynomial = mul(U[x-1], add((1, mul(V[x-1], A[x-1])), (1, B[x-1])))
            dependency = {("U", x), ("V", x), ("A", x), ("B", x)}
        elif z == 0:
            polynomial = mul(U[x-1], V[x-1])
            dependency = {("U", x), ("V", x)}
        else:
            polynomial = mul(U[x-1], add((1, mul(V[x-1], A[z-1])), (1, mul(V[y-1], B[z-1]))))
            dependency = {("U", x), ("V", x), ("A", z), ("V", y), ("B", z)}
        outputs.append(polynomial)
        dependencies.append(dependency)
    index = {chars: position for position, chars in enumerate(CH3)}
    transport = [index[tuple(chars[port_permutation[position]] for position in range(3))] for chars in CH3]
    return [outputs[position] for position in transport], [dependencies[position] for position in transport]


def verify_sunlet_upper(descriptor, omitted, selected_rows):
    compressed, rows, active, invisible, reticulation = compress_for_omitted_port(descriptor, omitted)
    found = None
    for edge_map in permutations(range(4)):
        for flip in (False, True):
            for port_permutation in permutations(range(3)):
                candidate, dependencies = canonical_sunlet(edge_map, flip, port_permutation)
                if compressed == candidate:
                    found = (edge_map, flip, port_permutation, dependencies)
                    break
            if found:
                break
        if found:
            break
    assert found is not None
    row_index = {row: index for index, row in enumerate(rows)}
    used = set().union(*(found[3][row_index[row]] for row in selected_rows))
    return {
        "omitted_port": omitted,
        "generator_count": len(used),
        "generators": sorted(map(str, used)),
        "active_edge_groups": active,
        "invisible_edge_groups": invisible,
        "inheritance_index": reticulation,
    }


def main():
    args = arguments()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    proof_root = locate_proof_root(args.package_root)
    lock_path = proof_root / "input_frozen/k3p_cloud_artifacts/K3P_14_ORBIT_LOCK.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    records = {record["orbit_id"]: record for record in lock["records"]}
    assert len(records) == len(lock["records"])
    quotient_check = residue_quotient(proof_root, lock)

    descriptors = {}
    for orbit_id in {"H21-01", "H21-02", "L20-01", "L20-02", "L21a-02", "L23-02"}:
        record = records[orbit_id]
        descriptors[(orbit_id, "source")] = compile_graph(record["source_literal_graph"])
        descriptors[(orbit_id, "target")] = compile_graph(record["target_literal_graph"])

    separators = []
    for seed, (orbit_id, body) in enumerate((("H21-01", QHA), ("L20-01", Q20), ("L23-02", Q23)), 27001):
        source_pullback = quartic_pullback(descriptors[(orbit_id, "source")], body)
        target_pullback = quartic_pullback(descriptors[(orbit_id, "target")], body)
        assert source_pullback and not target_pullback
        point, margin = own_point(descriptors[(orbit_id, "source")], seed)
        value = evaluate(source_pullback, point)
        assert value != 0
        separators.append({
            "orbit": orbit_id,
            "source_pullback_term_count": len(source_pullback),
            "target_pullback_term_count": len(target_pullback),
            "fresh_strict_ct_margin": str(margin),
            "fresh_source_value": str(value),
        })

    rank_rows = {
        "H21-02": [3,12,15,20,27,39,40,48,51,60,63],
        "L20-02": [5,10,15,17,20,27,30,34,39,40,45,51,54,57,60],
        "L21a-02": [5,15,17,20,27,39,40,45,51,57,60],
    }
    rank_results = []
    for seed, orbit_id in enumerate(rank_rows, 28001):
        rows = rank_rows[orbit_id]
        item = {"orbit": orbit_id, "selected_outputs": rows}
        for side in ("source", "target"):
            descriptor = descriptors[(orbit_id, side)]
            point, margin = own_point(descriptor, seed + (0 if side == "source" else 100))
            matrix = jacobian_at(descriptor, rows, point)
            rank, pivot_rows, pivot_columns, value = independent_minor(matrix)
            item[side] = {
                "fresh_sample_rank": rank,
                "pivot_rows_within_selected_order": pivot_rows,
                "pivot_columns": pivot_columns,
                "pivot_determinant": str(value),
                "strict_ct_margin": str(margin),
            }
        rank_results.append(item)
    assert rank_results[0]["source"]["fresh_sample_rank"] == 11
    assert rank_results[0]["target"]["fresh_sample_rank"] == 10
    assert rank_results[1]["source"]["fresh_sample_rank"] >= 14
    assert rank_results[1]["target"]["fresh_sample_rank"] <= 12
    assert rank_results[2]["source"]["fresh_sample_rank"] == 11
    assert rank_results[2]["target"]["fresh_sample_rank"] == 10

    h21 = None
    for candidate in all_parameter_conventions(records["H21-02"]["target_literal_graph"]):
        try:
            h21 = verify_h21_factorization(candidate)
            break
        except AssertionError:
            continue
    assert h21 is not None
    sunlet20 = verify_sunlet_upper(descriptors[("L20-02", "target")], 3, rank_rows["L20-02"])
    sunlet21 = verify_sunlet_upper(descriptors[("L21a-02", "target")], 3, rank_rows["L21a-02"])
    assert sunlet20["generator_count"] == 12
    assert sunlet21["generator_count"] == 10

    result = {
        "independent_final_residue_quotient": quotient_check,
        "literal_lock_accounting": {
            "canonical_records": len(lock["records"]),
            "raw_member_sum": sum(len(record["raw_members"]) for record in lock["records"]),
            "unique_orbit_ids": len(records),
            "prelock_exact_separations": len(lock["prelock_exact_separations"]),
        },
        "fresh_quartic_pullbacks": separators,
        "fresh_directional_rank_samples": rank_results,
        "H21_exact_rational_saturation_factorization": h21,
        "sunlet_target_factorizations": {"L20-02": sunlet20, "L21a-02": sunlet21},
        "independence_boundary": (
            "The script independently requotients the stored flat 40-row final residue as 38 records in "
            "fourteen literal-graph double cosets plus two sink swaps, and checks three quartic and three "
            "directional-rank representatives.  It does not repeat the 405,216-to-40 filtering.  Sample ranks "
            "provide lower bounds only; exact H21/sunlet factorizations provide the stated target upper bounds."
        ),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (args.output_dir / "four_port_witnesses.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
