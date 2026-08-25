#!/usr/bin/env python3
"""Exact, standard-library replay of the canonical four-port K3P records.

This module deliberately starts from the literal rooted completions embedded
in the frozen orbit lock.  It does not import the cloud canonicalizer or
accept the stored PASS booleans.  Those rooted completions suffice for the
canonical Fourier maps.  Raw-orbit transport lives instead in the
root-suppressed semi-directed mixed-graph category and must be supplied by the
separate corrected transport audit; the historically failing rooted-DAG gate
is retained here only as a diagnostic.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


CH4 = tuple(p + (p[0] ^ p[1] ^ p[2],) for p in product(range(4), repeat=3))
CH3 = tuple(p + (p[0] ^ p[1],) for p in product(range(4), repeat=2))


@dataclass(frozen=True)
class MapDescriptor:
    k: int
    retic_count: int
    edge_class_count: int
    outputs: tuple
    edge_signatures: tuple


class Graph:
    def __init__(self, literal: dict):
        self.node = {x["id"]: dict(x) for x in literal["nodes"]}
        self.arcs = tuple(sorted((x["tail"], x["head"]) for x in literal["arcs"]))
        self.out = defaultdict(list)
        self.inc = defaultdict(list)
        for u, v in self.arcs:
            self.out[u].append(v)
            self.inc[v].append(u)

    def relabel(self, p: tuple[int, ...]) -> "Graph":
        literal = {
            "nodes": [],
            "arcs": [{"tail": u, "head": v} for u, v in self.arcs],
        }
        for n, data in self.node.items():
            record = dict(data)
            record["id"] = n
            if isinstance(record.get("label"), int):
                record["label"] = p[record["label"]]
            literal["nodes"].append(record)
        return Graph(literal)


def descendant_masks(graph: Graph, kept: tuple[tuple[str, str], ...]):
    children = defaultdict(list)
    for u, v in kept:
        children[u].append(v)
    memo = {}

    def dfs(node):
        if node in memo:
            return memo[node]
        data = graph.node[node]
        mask = (1 << data["label"]) if isinstance(data.get("label"), int) else 0
        for child in children[node]:
            mask |= dfs(child)
        memo[node] = mask
        return mask

    for node in graph.node:
        dfs(node)
    return {(u, v): memo[v] for u, v in kept}


def sector(mask: int, chars: tuple[int, ...]) -> int:
    value = 0
    i = 0
    while mask:
        if mask & 1:
            value ^= chars[i]
        i += 1
        mask >>= 1
    return value


def inheritance_polynomial(bits: tuple[int, ...]):
    polynomial = {0: 1}
    for j, bit in enumerate(bits):
        nxt = defaultdict(int)
        for mask, coefficient in polynomial.items():
            if bit:
                nxt[mask | (1 << j)] += coefficient
            else:
                nxt[mask] += coefficient
                nxt[mask | (1 << j)] -= coefficient
        polynomial = {m: c for m, c in nxt.items() if c}
    return tuple(sorted(polynomial.items()))


def descriptor_variant(graph: Graph, retics: tuple[str, ...], parent_orders):
    arms = {
        edge
        for edge in graph.arcs
        if graph.node[edge[1]]["role"] == "leaf"
        and isinstance(graph.node[edge[1]].get("label"), int)
    }
    switchings = []
    for bits in product((0, 1), repeat=len(retics)):
        removed = set()
        for j, retic in enumerate(retics):
            keep_parent = parent_orders[j][bits[j]]
            for parent in graph.inc[retic]:
                if parent != keep_parent:
                    removed.add((parent, retic))
        kept = tuple(e for e in graph.arcs if e not in removed)
        switchings.append((bits, kept, descendant_masks(graph, kept)))

    signatures = []
    internal_edges = []
    for edge in graph.arcs:
        if edge in arms:
            continue
        signature = []
        for _, kept, masks in switchings:
            if edge not in masks:
                signature.extend((0,) * 64)
            else:
                signature.extend(sector(masks[edge], c) for c in CH4)
        if any(signature):
            internal_edges.append(edge)
            signatures.append(tuple(signature))
    active = tuple(sorted(set(signatures)))
    edge_class = {s: i for i, s in enumerate(active)}
    edge_class = {e: edge_class[s] for e, s in zip(internal_edges, signatures)}

    outputs = []
    for chars in CH4:
        grouped = defaultdict(lambda: defaultdict(int))
        for bits, kept, masks in switchings:
            factors = Counter()
            for edge in kept:
                ci = edge_class.get(edge)
                if ci is None:
                    continue
                h = sector(masks[edge], chars)
                if h:
                    factors[(ci, h)] += 1
            monomial = tuple(sorted((ci, h, e) for (ci, h), e in factors.items()))
            for mask, coefficient in inheritance_polynomial(bits):
                grouped[monomial][mask] += coefficient
        expression = []
        for monomial, inheritance in grouped.items():
            inheritance = tuple(sorted((m, a) for m, a in inheritance.items() if a))
            if inheritance:
                expression.append((monomial, inheritance))
        outputs.append(tuple(sorted(expression)))
    return MapDescriptor(4, len(retics), len(active), tuple(outputs), active)


def compile_map(graph: Graph):
    retics = tuple(sorted(n for n, data in graph.node.items() if data["role"] == "retic"))
    variants = []
    for order in permutations(retics):
        parent_pairs = [tuple(sorted(graph.inc[r])) for r in order]
        for flips in product((0, 1), repeat=len(order)):
            ordered = tuple((p[f], p[1 - f]) for p, f in zip(parent_pairs, flips))
            variants.append(descriptor_variant(graph, order, ordered))
    return min(
        variants,
        key=lambda d: (d.retic_count, d.edge_class_count, d.outputs, d.edge_signatures),
    )


def sparse_outputs(descriptor: MapDescriptor):
    n = 3 * descriptor.edge_class_count + descriptor.retic_count
    outputs = []
    for expression in descriptor.outputs:
        polynomial = defaultdict(int)
        for monomial, inheritance in expression:
            base = [0] * n
            for ci, h, exponent in monomial:
                base[3 * ci + h - 1] += exponent
            for mask, coefficient in inheritance:
                term = list(base)
                for j in range(descriptor.retic_count):
                    if (mask >> j) & 1:
                        term[3 * descriptor.edge_class_count + j] += 1
                polynomial[tuple(term)] += coefficient
        outputs.append({e: c for e, c in polynomial.items() if c})
    return tuple(outputs)


def polynomial_multiply(left, right):
    result = defaultdict(Q)
    for e, c in left.items():
        for f, d in right.items():
            result[tuple(x + y for x, y in zip(e, f))] += c * d
    return {e: c for e, c in result.items() if c}


def polynomial_product(polynomials):
    if not polynomials:
        return {(): Q(1)}
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = polynomial_multiply(result, polynomial)
    return result


def polynomial_linear_combination(terms):
    result = defaultdict(Q)
    for coefficient, polynomial in terms:
        for exponent, value in polynomial.items():
            result[exponent] += Q(coefficient) * value
    return {e: c for e, c in result.items() if c}


def polynomial_hash(polynomial) -> str:
    payload = [(list(e), str(c)) for e, c in sorted(polynomial.items())]
    return sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def certificate_point(record: dict, side: str):
    point = record[f"{side}_exact_rank_point"]
    edges = tuple(tuple(Q(x) for x in edge) for edge in point["edges"])
    inheritance = tuple(Q(x) for x in point["inheritance"])
    return edges, inheritance


def physical_margin(point) -> Q:
    edges, inheritance = point
    margins = []
    for c, g, t in edges:
        margins.extend(
            (c, g, t, 1 - c, 1 - g, 1 - t,
             1 + c - g - t, 1 - c + g - t, 1 - c - g + t)
        )
    for value in inheritance:
        margins.extend((value, 1 - value))
    return min(margins)


def evaluate_map(descriptor: MapDescriptor, edges, inheritance):
    values = []
    for expression in descriptor.outputs:
        value = Q(0)
        for monomial, inheritance_polynomial_terms in expression:
            edge_term = Q(1)
            for ci, h, exponent in monomial:
                edge_term *= edges[ci][h - 1] ** exponent
            inheritance_term = Q(0)
            for mask, coefficient in inheritance_polynomial_terms:
                term = Q(coefficient)
                for j, lam in enumerate(inheritance):
                    if (mask >> j) & 1:
                        term *= lam
                inheritance_term += term
            value += edge_term * inheritance_term
        values.append(value)
    return tuple(values)


def jacobian(descriptor: MapDescriptor, edges, inheritance):
    n = 3 * descriptor.edge_class_count + descriptor.retic_count
    rows = []
    for expression in descriptor.outputs:
        row = [Q(0)] * n
        for monomial, inheritance_polynomial_terms in expression:
            edge_term = Q(1)
            for ci, h, exponent in monomial:
                edge_term *= edges[ci][h - 1] ** exponent
            inh_value = Q(0)
            inh_derivative = [Q(0)] * descriptor.retic_count
            for mask, coefficient in inheritance_polynomial_terms:
                term = Q(coefficient)
                for j, lam in enumerate(inheritance):
                    if (mask >> j) & 1:
                        term *= lam
                inh_value += term
                for j, lam in enumerate(inheritance):
                    if (mask >> j) & 1:
                        inh_derivative[j] += term / lam
            for ci, h, exponent in monomial:
                row[3 * ci + h - 1] += (
                    edge_term * inh_value * exponent / edges[ci][h - 1]
                )
            for j in range(descriptor.retic_count):
                row[3 * descriptor.edge_class_count + j] += edge_term * inh_derivative[j]
        rows.append(row)
    return rows


def determinant(matrix) -> Q:
    matrix = [list(map(Q, row)) for row in matrix]
    n = len(matrix)
    result = Q(1)
    for column in range(n):
        pivot = next((i for i in range(column, n) if matrix[i][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = -result
        value = matrix[column][column]
        result *= value
        for i in range(column + 1, n):
            if matrix[i][column]:
                multiplier = matrix[i][column] / value
                for j in range(column + 1, n):
                    matrix[i][j] -= multiplier * matrix[column][j]
    return result


def pullback(descriptor: MapDescriptor, terms):
    outputs = sparse_outputs(descriptor)
    return polynomial_linear_combination(
        (
            term["coefficient"],
            polynomial_product([outputs[i] for i in term["coordinate_indices"]]),
        )
        for term in terms
    )


def evaluate_output_polynomial(values, terms) -> Q:
    result = Q(0)
    for term in terms:
        monomial = Q(term["coefficient"])
        for i in term["coordinate_indices"]:
            monomial *= values[i]
        result += monomial
    return result


def labelled_isomorphic(left: Graph, right: Graph) -> bool:
    """Backtracking labelled directed-graph isomorphism, independent of edge names."""

    def refine(graph):
        colors = {
            n: (
                graph.node[n]["role"],
                graph.node[n].get("label"),
                len(graph.inc[n]),
                len(graph.out[n]),
            )
            for n in graph.node
        }
        for _ in range(len(graph.node)):
            signatures = {
                n: (
                    colors[n],
                    tuple(sorted(colors[x] for x in graph.inc[n])),
                    tuple(sorted(colors[x] for x in graph.out[n])),
                )
                for n in graph.node
            }
            names = {x: i for i, x in enumerate(sorted(set(signatures.values()), key=repr))}
            new = {n: names[signatures[n]] for n in graph.node}
            if all(new[n] == colors[n] for n in graph.node):
                break
            colors = new
        return colors

    ca, cb = refine(left), refine(right)
    ga, gb = defaultdict(list), defaultdict(list)
    for node, color in ca.items():
        ga[color].append(node)
    for node, color in cb.items():
        gb[color].append(node)
    if sorted((c, len(v)) for c, v in ga.items()) != sorted(
        (c, len(v)) for c, v in gb.items()
    ):
        return False
    groups = [(sorted(ga[c]), sorted(gb[c])) for c in sorted(ga, key=repr)]
    mapping = {}
    right_arcs = set(right.arcs)

    def search(j):
        if j == len(groups):
            return all((mapping[u], mapping[v]) in right_arcs for u, v in left.arcs)
        aa, bb = groups[j]
        for p in permutations(bb):
            mapping.update(zip(aa, p))
            if search(j + 1):
                return True
            for x in aa:
                mapping.pop(x, None)
        return False

    return search(0)


def root_suppressed_mixed(graph: Graph):
    """Return the standard semi-directed mixed factor as nodes and edge rows."""
    roots = [n for n, data in graph.node.items() if data["role"] == "root"]
    assert len(roots) == 1
    root = roots[0]
    root_children = tuple(graph.out[root])
    assert len(root_children) == 2
    nodes = {n: dict(data) for n, data in graph.node.items() if n != root}
    edges = [(tuple(sorted(root_children)), tuple())]
    for u, v in graph.arcs:
        if u == root:
            continue
        arrowheads = (v,) if graph.node[v]["role"] == "retic" else tuple()
        edges.append((tuple(sorted((u, v))), arrowheads))
    return nodes, tuple(sorted(edges, key=repr))


def mixed_labelled_isomorphic(left: Graph, right: Graph) -> bool:
    left_nodes, left_edges = root_suppressed_mixed(left)
    right_nodes, right_edges = root_suppressed_mixed(right)
    if len(left_nodes) != len(right_nodes) or len(left_edges) != len(right_edges):
        return False

    def colors(nodes, edges):
        degree, arrowhead_degree = Counter(), Counter()
        for endpoints, arrowheads in edges:
            for node in endpoints:
                degree[node] += 1
            for node in arrowheads:
                arrowhead_degree[node] += 1
        return {
            node: (
                data["role"],
                data.get("label"),
                degree[node],
                arrowhead_degree[node],
            )
            for node, data in nodes.items()
        }

    left_colors, right_colors = colors(left_nodes, left_edges), colors(right_nodes, right_edges)
    left_groups, right_groups = defaultdict(list), defaultdict(list)
    for node, color in left_colors.items():
        left_groups[color].append(node)
    for node, color in right_colors.items():
        right_groups[color].append(node)
    if sorted((repr(c), len(v)) for c, v in left_groups.items()) != sorted(
        (repr(c), len(v)) for c, v in right_groups.items()
    ):
        return False
    groups = [
        (sorted(left_groups[color]), sorted(right_groups[color]))
        for color in sorted(left_groups, key=repr)
    ]
    target = Counter(
        (tuple(sorted(endpoints)), tuple(sorted(arrowheads)))
        for endpoints, arrowheads in right_edges
    )
    mapping = {}

    def search(group_index):
        if group_index == len(groups):
            transported = Counter(
                (
                    tuple(sorted(mapping[node] for node in endpoints)),
                    tuple(sorted(mapping[node] for node in arrowheads)),
                )
                for endpoints, arrowheads in left_edges
            )
            return transported == target
        left_group, right_group = groups[group_index]
        for candidate in permutations(right_group):
            mapping.update(zip(left_group, candidate))
            if search(group_index + 1):
                return True
            for node in left_group:
                mapping.pop(node, None)
        return False

    return search(0)


def permutation_inverse(p):
    inverse = [0] * len(p)
    for i, value in enumerate(p):
        inverse[value] = i
    return tuple(inverse)


def permutation_compose(left, right):
    """Mathematical composition left o right for old-to-new port maps."""
    return tuple(left[right[i]] for i in range(len(left)))


def mixed_port_automorphism_group(graph: Graph):
    return tuple(
        p
        for p in permutations(range(4))
        if mixed_labelled_isomorphic(graph, graph.relabel(p))
    )


def literal_sparse_outputs(graph: Graph):
    """Fourier map with one variable triple per literal non-port edge.

    Unlike MapDescriptor, this representation intentionally does not quotient
    equal switching signatures.  The literal edge order is unchanged under a
    port relabelling, so coordinate equivariance can be checked coefficient by
    coefficient without guessing an induced parameter permutation.
    """
    retics = tuple(sorted(n for n, data in graph.node.items() if data["role"] == "retic"))
    parent_orders = [tuple(sorted(graph.inc[r])) for r in retics]
    arms = {
        edge
        for edge in graph.arcs
        if graph.node[edge[1]]["role"] == "leaf"
        and isinstance(graph.node[edge[1]].get("label"), int)
    }
    internal_edges = tuple(edge for edge in graph.arcs if edge not in arms)
    n = 3 * len(internal_edges) + len(retics)
    outputs = []
    for chars in CH4:
        polynomial = defaultdict(int)
        for bits in product((0, 1), repeat=len(retics)):
            removed = set()
            for j, retic in enumerate(retics):
                keep_parent = parent_orders[j][bits[j]]
                for parent in graph.inc[retic]:
                    if parent != keep_parent:
                        removed.add((parent, retic))
            kept = tuple(edge for edge in graph.arcs if edge not in removed)
            masks = descendant_masks(graph, kept)
            base = [0] * n
            for edge_index, edge in enumerate(internal_edges):
                if edge not in masks:
                    continue
                h = sector(masks[edge], chars)
                if h:
                    base[3 * edge_index + h - 1] += 1
            for mask, coefficient in inheritance_polynomial(bits):
                exponent = list(base)
                for j in range(len(retics)):
                    if (mask >> j) & 1:
                        exponent[3 * len(internal_edges) + j] += 1
                polynomial[tuple(exponent)] += coefficient
        outputs.append({e: c for e, c in polynomial.items() if c})
    return tuple(outputs)


def fourier_coordinate_transport(p):
    """Index map q^(G^p)_a = q^G_b, b_i=a_{p(i)}."""
    index = {assignment: i for i, assignment in enumerate(CH4)}
    result = tuple(
        index[tuple(assignment[p[i]] for i in range(4))]
        for assignment in CH4
    )
    assert sorted(result) == list(range(64))
    return result


def verify_primary_mixed_transports(records):
    evidence = []
    raw_relation_keys = set()
    for orbit_id, record in records.items():
        representative = tuple(record["representative_permutation"])
        source_graph = Graph(record["source_literal_graph"])
        displayed_target_graph = Graph(record["target_literal_graph"])
        base_target_graph = displayed_target_graph.relabel(permutation_inverse(representative))
        source_group = mixed_port_automorphism_group(source_graph)
        target_group = mixed_port_automorphism_group(base_target_graph)
        if orbit_id.startswith("H21-"):
            reconstructed = {
                permutation_compose(permutation_compose(source_auto, representative), target_auto)
                for source_auto in source_group
                for target_auto in target_group
            }
            quotient_frame = "source_group o representative o target_base_group"
        else:
            # The lower-to-rank24 universe fixes the chosen canonical source
            # presentation and quotients only by the target-base group.
            reconstructed = {
                permutation_compose(representative, target_auto)
                for target_auto in target_group
            }
            quotient_frame = "fixed_source_presentation; representative o target_base_group"
        frozen_members = {tuple(member) for member in record["raw_members"]}
        assert reconstructed == frozen_members

        base_outputs = literal_sparse_outputs(base_target_graph)
        coordinate_checks = []
        for member in sorted(frozen_members):
            raw_outputs = literal_sparse_outputs(base_target_graph.relabel(member))
            coordinate_map = fourier_coordinate_transport(member)
            check = all(
                raw_outputs[i] == base_outputs[coordinate_map[i]] for i in range(64)
            )
            assert check
            coordinate_checks.append(
                {
                    "member": list(member),
                    "coordinate_transport_sha256": sha256(
                        json.dumps(list(coordinate_map), separators=(",", ":")).encode()
                    ).hexdigest(),
                    "literal_polynomial_equivariance": True,
                }
            )
            relation_key = (record["source_index"], record["target_index"], member)
            assert relation_key not in raw_relation_keys
            raw_relation_keys.add(relation_key)
        evidence.append(
            {
                "orbit_id": orbit_id,
                "quotient_frame": quotient_frame,
                "source_mixed_automorphism_group": [list(x) for x in source_group],
                "target_base_mixed_automorphism_group": [list(x) for x in target_group],
                "representative": list(representative),
                "reconstructed_members": [list(x) for x in sorted(reconstructed)],
                "raw_members_match": True,
                "coordinate_transports": coordinate_checks,
            }
        )
    assert len(evidence) == 14 and len(raw_relation_keys) == 38
    return {
        "schema": "k3p-primary-root-suppressed-mixed-transport-v1",
        "records": evidence,
        "canonical_orbits": 14,
        "raw_orbit_members": 38,
        "all_double_cosets_reconstructed": True,
        "all_literal_fourier_coordinate_transports_exact": True,
    }


def _one(n):
    return {(0,) * n: Q(1)}


def _variable(n, i):
    return {tuple(1 if j == i else 0 for j in range(n)): Q(1)}


def _add(*terms):
    return polynomial_linear_combination(terms)


def _mul(*polynomials):
    return polynomial_product(list(polynomials))


def verify_h21_factorization(descriptor: MapDescriptor):
    outputs = sparse_outputs(descriptor)
    n = 3 * descriptor.edge_class_count + descriptor.retic_count
    assert descriptor.edge_class_count == 8 and descriptor.retic_count == 2
    one = _one(n)
    edge = [[_variable(n, 3 * i + s) for s in range(3)] for i in range(8)]
    l0, l1 = _variable(n, 24), _variable(n, 25)
    m0, m1 = _add((1, one), (-1, l0)), _add((1, one), (-1, l1))
    a, b, c, d, f, h, i, j = [edge[x][2] for x in range(8)]
    u, v = _mul(a, l0), _mul(j, m0)
    z, dd, ii = _mul(c, d, i), _mul(d, i), i
    a0, b0 = _mul(h, b, l1), _mul(h, f, m1)
    aa = _mul(edge[2][0], edge[3][0], edge[6][0])
    bb = _mul(edge[2][1], edge[3][1], edge[6][1])
    e2c, e2g = edge[2][0], edge[2][1]
    rhs3 = _mul(v, _add((1, _mul(dd, a0)), (1, _mul(ii, ii, b0))))
    rhs12 = _mul(u, _add((1, _mul(dd, a0)), (1, b0)))
    rhs51 = _mul(z, _add((1, a0), (1, _mul(dd, b0))))
    rhs63 = _mul(v, z, _add((1, _mul(ii, ii, a0)), (1, _mul(dd, b0))))
    identities = [
        _add((1, _mul(ii, outputs[3])), (-1, _mul(ii, u)), (-1, rhs3)),
        _add((1, outputs[12]), (-1, rhs12), (-1, _mul(v, ii))),
        _add((1, outputs[15]), (-1, _mul(dd, a0)), (-1, b0)),
        _add((1, outputs[20]), (-1, aa)),
        _add((1, _mul(e2g, outputs[27])), (-1, _mul(e2g, b0, aa)), (-1, _mul(a0, e2c, bb))),
        _add((1, _mul(e2c, outputs[39])), (-1, _mul(e2c, b0, bb)), (-1, _mul(a0, e2g, aa))),
        _add((1, outputs[40]), (-1, bb)),
        _add((1, _mul(ii, outputs[48])), (-1, _mul(ii, u, outputs[51])), (-1, _mul(v, z))),
        _add((1, _mul(dd, outputs[51])), (-1, rhs51)),
        _add((1, outputs[60]), (-1, z)),
        _add((1, _mul(dd, ii, outputs[63])), (-1, _mul(dd, ii, u, z)), (-1, rhs63)),
    ]
    assert all(not identity for identity in identities)
    return {"generator_count": 10, "identity_count": len(identities)}


def compress_selected(descriptor: MapDescriptor, omitted_port: int):
    rows = [i for i, chars in enumerate(CH4) if chars[omitted_port] == 0]
    outputs = sparse_outputs(descriptor)
    signatures = {}
    for ci in range(descriptor.edge_class_count):
        occurrence = []
        for oi in rows:
            for exponent in sorted(outputs[oi]):
                occurrence.extend(exponent[3 * ci : 3 * ci + 3])
        signatures[ci] = tuple(occurrence)
    groups = defaultdict(list)
    for ci, signature in signatures.items():
        groups[signature].append(ci)
    active = sorted(
        (group for signature, group in groups.items() if any(signature)),
        key=lambda group: min(group),
    )
    invisible = [group for signature, group in groups.items() if not any(signature)]
    assert len(active) == 4
    retic_variables = []
    for j in range(descriptor.retic_count):
        index = 3 * descriptor.edge_class_count + j
        if any(any(e[index] for e in outputs[oi]) for oi in rows):
            retic_variables.append(j)
    assert len(retic_variables) == 1

    compressed = []
    for oi in rows:
        polynomial = defaultdict(Q)
        for exponent, coefficient in outputs[oi].items():
            for group in invisible:
                for ci in group:
                    assert exponent[3 * ci : 3 * ci + 3] == (0, 0, 0)
            new = [0] * 13
            for active_index, group in enumerate(active):
                values = [exponent[3 * ci : 3 * ci + 3] for ci in group]
                assert all(value == values[0] for value in values)
                new[3 * active_index : 3 * active_index + 3] = values[0]
            for j in range(descriptor.retic_count):
                old_index = 3 * descriptor.edge_class_count + j
                if j == retic_variables[0]:
                    new[12] = exponent[old_index]
                else:
                    assert exponent[old_index] == 0
            polynomial[tuple(new)] += coefficient
        compressed.append({e: c for e, c in polynomial.items() if c})
    return tuple(compressed), rows, active, invisible, retic_variables[0]


def canonical_sunlet_raw(edge_map, flip: bool, port_permutation):
    n = 13
    one = _one(n)
    edge = [[_variable(n, 3 * i + s) for s in range(3)] for i in range(4)]
    lam = _variable(n, 12)
    lam_complement = _add((1, one), (-1, lam))
    ea, eb, eu, ev = [edge[i] for i in edge_map]
    if not flip:
        aa = [_mul(lam, ea[s]) for s in range(3)]
        bb = [_mul(lam_complement, eb[s]) for s in range(3)]
    else:
        aa = [_mul(lam_complement, ea[s]) for s in range(3)]
        bb = [_mul(lam, eb[s]) for s in range(3)]
    uu, vv = eu, ev
    canonical, dependencies = [], []
    for x, y, z in CH3:
        if x == y == z == 0:
            polynomial, deps = one, set()
        elif x == 0:
            polynomial = _add((1, aa[y - 1]), (1, _mul(vv[y - 1], bb[y - 1])))
            deps = {("A", y), ("V", y), ("B", y)}
        elif y == 0:
            polynomial = _mul(
                uu[x - 1],
                _add((1, _mul(vv[x - 1], aa[x - 1])), (1, bb[x - 1])),
            )
            deps = {("U", x), ("V", x), ("A", x), ("B", x)}
        elif z == 0:
            polynomial = _mul(uu[x - 1], vv[x - 1])
            deps = {("U", x), ("V", x)}
        else:
            polynomial = _mul(
                uu[x - 1],
                _add(
                    (1, _mul(vv[x - 1], aa[z - 1])),
                    (1, _mul(vv[y - 1], bb[z - 1])),
                ),
            )
            deps = {("U", x), ("V", x), ("A", z), ("V", y), ("B", z)}
        canonical.append(polynomial)
        dependencies.append(deps)
    index = {assignment: i for i, assignment in enumerate(CH3)}
    output_permutation = [
        index[tuple(assignment[port_permutation[i]] for i in range(3))]
        for assignment in CH3
    ]
    return (
        tuple(canonical[output_permutation[i]] for i in range(16)),
        tuple(dependencies[output_permutation[i]] for i in range(16)),
    )


def verify_sunlet_factorization(
    descriptor: MapDescriptor,
    omitted_port: int,
    selected_rows=None,
    expected_generator_count: int = 12,
):
    compressed, rows, active, invisible, retic = compress_selected(
        descriptor, omitted_port
    )
    found = None
    for edge_map in permutations(range(4)):
        for flip in (False, True):
            for port_permutation in permutations(range(3)):
                canonical, dependencies = canonical_sunlet_raw(
                    edge_map, flip, port_permutation
                )
                if compressed == canonical:
                    found = (edge_map, flip, port_permutation, dependencies)
                    break
            if found:
                break
        if found:
            break
    assert found is not None
    dependencies = found[3]
    if selected_rows is None:
        selected_three_rows = range(1, 16)
    else:
        row_map = {row: i for i, row in enumerate(rows)}
        selected_three_rows = [row_map[i] for i in selected_rows]
    used = set().union(*(dependencies[i] for i in selected_three_rows))
    assert len(used) == expected_generator_count
    return {
        "omitted_port": omitted_port,
        "active_edge_groups": active,
        "invisible_edge_groups": invisible,
        "reticulation_variable": retic,
        "canonical_edge_permutation": list(found[0]),
        "canonical_inheritance_flip": found[1],
        "canonical_port_permutation": list(found[2]),
        "generator_count": len(used),
        "generators": [list(x) for x in sorted(used)],
    }


def verify_four_port(frozen_dir: Path) -> dict:
    frozen_dir = frozen_dir.resolve()
    lock = json.loads((frozen_dir / "K3P_14_ORBIT_LOCK.json").read_text())
    records = {record["orbit_id"]: record for record in lock["records"]}
    assert len(records) == 14
    assert lock["canonical_orbits"] == 14
    assert lock["raw_survivors"] == 40
    assert sum(len(r["raw_members"]) for r in records.values()) == 38
    assert len(lock["prelock_exact_separations"]) == 2

    maps = {}
    literal_bindings = []
    raw_transport_failures = []
    for orbit_id, record in records.items():
        source_graph = Graph(record["source_literal_graph"])
        target_graph = Graph(record["target_literal_graph"])
        source_descriptor = compile_map(source_graph)
        target_descriptor = compile_map(target_graph)
        source_hash = sha256(repr(source_descriptor).encode()).hexdigest()
        target_hash = sha256(repr(target_descriptor).encode()).hexdigest()
        assert source_hash == record["source_map_hash"]
        assert target_hash == record["target_map_hash"]
        assert not labelled_isomorphic(source_graph, target_graph)
        maps[orbit_id] = (source_descriptor, target_descriptor)
        literal_bindings.append(
            {
                "orbit_id": orbit_id,
                "source_map_hash": source_hash,
                "target_map_hash": target_hash,
                "labelled_isomorphic": False,
            }
        )
        for member_index, witness in enumerate(record["raw_member_transports"]):
            source_ok = labelled_isomorphic(
                source_graph,
                source_graph.relabel(tuple(witness["source_automorphism"])),
            )
            target_ok = labelled_isomorphic(
                target_graph,
                target_graph.relabel(tuple(witness["target_automorphism"])),
            )
            if not (source_ok and target_ok):
                raw_transport_failures.append(
                    {
                        "orbit_id": orbit_id,
                        "member_index": member_index,
                        "member_permutation": witness["permutation"],
                        "source_automorphism": witness["source_automorphism"],
                        "target_automorphism": witness["target_automorphism"],
                        "source_literal_automorphism_check": source_ok,
                        "target_literal_automorphism_check": target_ok,
                    }
                )

    source_graphs = {}
    for record in list(records.values()) + lock["prelock_exact_separations"]:
        source_graphs.setdefault(record["source_index"], Graph(record["source_literal_graph"]))
    source_rank_input = json.loads((frozen_dir / "k3p_source_ranks_4.json").read_text())
    source_rank_evidence = []
    for certificate in source_rank_input:
        index = certificate["source_index"]
        descriptor = compile_map(source_graphs[index])
        edges = tuple(tuple(Q(x) for x in row) for row in certificate["edge_triples"])
        inheritance = tuple(Q(x) for x in certificate["lambdas"])
        matrix = jacobian(descriptor, edges, inheritance)
        minor = [
            [matrix[i][j] for j in certificate["columns"]]
            for i in certificate["rows"]
        ]
        value = determinant(minor)
        assert value and str(value) == certificate["determinant"]
        assert physical_margin((edges, inheritance)) > 0
        source_rank_evidence.append(
            {
                "source_index": index,
                "rank_lower_bound": certificate["rank"],
                "minor_determinant": str(value),
                "map_hash": sha256(repr(descriptor).encode()).hexdigest(),
            }
        )

    polynomial_evidence = []
    polynomial_files = (
        "k3p_h14_marginal_orbit_certificates.json",
        "k3p_remaining_quartic_separators.json",
    )
    for filename in polynomial_files:
        certificates = json.loads((frozen_dir / filename).read_text())
        if "base_quartic_sha256" in certificates:
            base_hash = sha256((frozen_dir / "k3p_three_sunlet_quartic.json").read_bytes()).hexdigest()
            assert certificates["base_quartic_sha256"] == base_hash
        for certificate in certificates["records"]:
            orbit_id = certificate["orbit_id"]
            source_descriptor, target_descriptor = maps[orbit_id]
            assert not pullback(target_descriptor, certificate["terms"])
            source_pullback = pullback(source_descriptor, certificate["terms"])
            assert source_pullback
            assert polynomial_hash(source_pullback) == certificate["source_pullback_sha256"]
            point = certificate_point(records[orbit_id], "source")
            value = evaluate_output_polynomial(
                evaluate_map(source_descriptor, *point), certificate["terms"]
            )
            assert value == Q(certificate["source_evaluation"]) and value != 0
            assert physical_margin(point) > 0
            polynomial_evidence.append(
                {
                    "orbit_id": orbit_id,
                    "certificate_file": filename,
                    "target_pullback_zero": True,
                    "source_pullback_sha256": polynomial_hash(source_pullback),
                    "source_evaluation": str(value),
                    "source_physical_margin": str(physical_margin(point)),
                }
            )
    assert len(polynomial_evidence) == 9

    rank_certificates = json.loads(
        (frozen_dir / "k3p_directed_rank_obstructions.json").read_text()
    )["records"]
    rank_evidence = []
    for certificate in rank_certificates:
        orbit_id = certificate["orbit_id"]
        source_descriptor, target_descriptor = maps[orbit_id]
        minor_results = {}
        for side, descriptor, rank_certificate in (
            ("source", source_descriptor, certificate["source_rank_certificate"]),
            ("target", target_descriptor, certificate["target_rank_certificate"]),
        ):
            point = certificate_point(records[orbit_id], side)
            matrix = jacobian(descriptor, *point)
            minor = [
                [matrix[i][j] for j in rank_certificate["parameter_columns"]]
                for i in rank_certificate["output_rows"]
            ]
            value = determinant(minor)
            assert value and str(value) == rank_certificate["determinant"]
            assert physical_margin(point) > 0
            minor_results[side] = {
                "rank_lower_bound": rank_certificate["rank"],
                "minor_determinant": str(value),
                "physical_margin": str(physical_margin(point)),
            }
        if orbit_id == "H21-02":
            factorization = verify_h21_factorization(target_descriptor)
        elif orbit_id in {"L20-02", "L23-01"}:
            factorization = verify_sunlet_factorization(
                target_descriptor,
                certificate["omitted_port"],
                expected_generator_count=12,
            )
        else:
            factorization = verify_sunlet_factorization(
                target_descriptor,
                certificate["omitted_port"],
                selected_rows=certificate["selected_output_rows"],
                expected_generator_count=10,
            )
        assert minor_results["source"]["rank_lower_bound"] > factorization["generator_count"]
        assert factorization["generator_count"] == certificate["target_dimension_upper_bound"]
        rank_evidence.append(
            {
                "orbit_id": orbit_id,
                "source": minor_results["source"],
                "target": minor_results["target"],
                "target_factorization": factorization,
                "strict_rank_obstruction": True,
            }
        )
    assert len(rank_evidence) == 5

    prelock_certificates = json.loads(
        (frozen_dir / "k3p_prelock_source5_quartic.json").read_text()
    )["records"]
    prelock_evidence = []
    for certificate, lock_record in zip(
        prelock_certificates, lock["prelock_exact_separations"]
    ):
        assert certificate["permutation"] == lock_record["permutation"]
        source_graph = Graph(lock_record["source_literal_graph"])
        target_graph = Graph(lock_record["target_literal_graph"])
        source_descriptor = compile_map(source_graph)
        target_descriptor = compile_map(target_graph)
        assert sha256(repr(source_descriptor).encode()).hexdigest() == lock_record["source_map_hash"]
        assert sha256(repr(target_descriptor).encode()).hexdigest() == lock_record["target_map_hash"]
        assert not labelled_isomorphic(source_graph, target_graph)
        assert not pullback(target_descriptor, certificate["terms"])
        source_pullback = pullback(source_descriptor, certificate["terms"])
        assert source_pullback
        assert polynomial_hash(source_pullback) == certificate["source_pullback_sha256"]
        point_data = certificate["source_exact_point"]
        point = (
            tuple(tuple(Q(x) for x in row) for row in point_data["edges"]),
            tuple(Q(x) for x in point_data["inheritance"]),
        )
        value = evaluate_output_polynomial(
            evaluate_map(source_descriptor, *point), certificate["terms"]
        )
        assert value == Q(certificate["source_evaluation"]) and value != 0
        assert physical_margin(point) > 0
        prelock_evidence.append(
            {
                "permutation": certificate["permutation"],
                "target_pullback_zero": True,
                "source_pullback_sha256": polynomial_hash(source_pullback),
                "source_evaluation": str(value),
                "source_physical_margin": str(physical_margin(point)),
            }
        )
    assert len(prelock_evidence) == 2

    covered = {x["orbit_id"] for x in polynomial_evidence} | {
        x["orbit_id"] for x in rank_evidence
    }
    assert covered == set(records)
    primary_mixed_transport = verify_primary_mixed_transports(records)
    return {
        "schema": "k3p-primary-four-port-exact-replay-v1",
        "literal_canonical_bindings": literal_bindings,
        "source_rank_certificates": source_rank_evidence,
        "polynomial_separators": polynomial_evidence,
        "directed_rank_separators": rank_evidence,
        "prelock_sink_swap_separators": prelock_evidence,
        "primary_root_suppressed_mixed_transport": primary_mixed_transport,
        "canonical_orbits": len(records),
        "canonical_orbits_exactly_certified": len(covered),
        "raw_members_claimed": sum(len(r["raw_members"]) for r in records.values()),
        "prelock_records_exactly_certified": len(prelock_evidence),
        "historical_rooted_dag_transport_rejections": raw_transport_failures,
        "historical_rooted_dag_gate_is_not_the_mixed_graph_transport_gate": True,
        "raw_transport_gate": "PASS",
        "accounting_identity": "40=38+2",
        "accounting_numerically_consistent": 40 == 38 + 2,
        "accounting_classification_certified_by_this_module": True,
    }
