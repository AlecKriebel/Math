#!/usr/bin/env python3
"""Literal clean-room primitives for the full four-port replay verifier.

This module intentionally does not import the producing replay or the historical
``k3p_atlas_core`` module.  The five rooted cores, completion grammar, switching
Fourier map, topology restrictions, exact algebra, and semi-directed comparison
are implemented below from their mathematical definitions.
"""
from __future__ import annotations

import collections
import hashlib
import itertools
import json
import math
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache

import networkx as nx


class ReplayFailure(RuntimeError):
    pass


def require(condition, code, detail=None):
    if not condition:
        raise ReplayFailure(code if detail is None else f"{code}: {detail!r}")


CORE = {
    "cycle": {"arcs": (("S", "X"), ("S", "X")), "retics": ("X",),
              "sinks": ("X",), "repairs": ((0,), (1,))},
    "theta0": {"arcs": (("S", "U"), ("S", "V"), ("U", "X"),
                           ("V", "X"), ("U", "V")),
               "retics": ("V", "X"), "sinks": ("X",),
               "repairs": ((2, 3), (3, 4))},
    "theta1": {"arcs": (("S", "U"), ("S", "X"), ("V", "X"),
                           ("U", "V"), ("U", "V")),
               "retics": ("V", "X"), "sinks": ("X",),
               "repairs": ((2, 3), (2, 4))},
    "theta2": {"arcs": (("S", "U"), ("S", "V"), ("U", "X0"),
                           ("V", "X0"), ("U", "X1"), ("V", "X1")),
               "retics": ("X0", "X1"), "sinks": ("X0", "X1"),
               "repairs": ((2, 3), (2, 5), (3, 4), (4, 5))},
    "theta3": {"arcs": (("S", "U"), ("S", "X0"), ("V", "X0"),
                           ("U", "X1"), ("V", "X1"), ("U", "V")),
               "retics": ("X0", "X1"), "sinks": ("X0", "X1"),
               "repairs": ((2,), (4,))},
}


@dataclass(frozen=True)
class Completion:
    core_id: str
    incoming_selected: bool
    repair_index: int | None
    sink_mask: int
    words: tuple
    graph: nx.DiGraph
    selected_labels: tuple
    dummy_labels: tuple


@dataclass(frozen=True)
class MapDescriptor:
    k: int
    retic_count: int
    edge_class_count: int
    outputs: tuple
    edge_signatures: tuple


def object_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def descriptor_hash(descriptor):
    return hashlib.sha256(repr(descriptor).encode()).hexdigest()


def graph_hash(graph):
    nodes = [{
        "id": repr(node), "role": data.get("role"), "label": data.get("label"),
        "dummy": bool(data.get("dummy", False)),
        "dummy_name": data.get("dummy_name"),
    } for node, data in graph.nodes(data=True)]
    edges = [{"tail": repr(tail), "head": repr(head),
              "edge_role": data.get("edge_role")}
             for tail, head, data in graph.edges(data=True)]
    nodes.sort(key=lambda row: row["id"])
    edges.sort(key=lambda row: (row["tail"], row["head"], row["edge_role"] or ""))
    return object_hash({"nodes": nodes, "edges": edges})


def weak_compositions(total, bins):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def build_graph(core_id, words, sink_labels, incoming):
    spec = CORE[core_id]
    graph = nx.DiGraph(core_id=core_id)
    for name in {name for arc in spec["arcs"] for name in arc}:
        graph.add_node(("core", name),
                       role="retic" if name in spec["retics"] else "tree",
                       label=None, dummy=False)
    root = ("root",)
    graph.add_node(root, role="root", label=None, dummy=False)
    incoming_leaf = ("leaf", "INCOMING")
    selected = isinstance(incoming, int)
    graph.add_node(incoming_leaf, role="leaf", label=incoming if selected else None,
                   dummy=not selected, dummy_name=None if selected else str(incoming))
    graph.add_edge(root, ("core", "S"), edge_role="incoming_core")
    graph.add_edge(root, incoming_leaf, edge_role="incoming_arm")
    for segment, ((tail, head), word) in enumerate(zip(spec["arcs"], words)):
        previous = ("core", tail)
        for position, label in enumerate(word):
            subdivision = ("sub", segment, position)
            leaf = ("leaf", "seg", segment, position)
            graph.add_node(subdivision, role="tree", label=None, dummy=False)
            selected = isinstance(label, int)
            graph.add_node(leaf, role="leaf", label=label if selected else None,
                           dummy=not selected,
                           dummy_name=None if selected else str(label))
            graph.add_edge(previous, subdivision, edge_role=f"seg{segment}")
            graph.add_edge(subdivision, leaf, edge_role="arm")
            previous = subdivision
        graph.add_edge(previous, ("core", head), edge_role=f"seg{segment}")
    for index, sink in enumerate(spec["sinks"]):
        label = sink_labels[sink]
        selected = isinstance(label, int)
        leaf = ("leaf", "sink", index)
        graph.add_node(leaf, role="leaf", label=label if selected else None,
                       dummy=not selected,
                       dummy_name=None if selected else str(label))
        graph.add_edge(("core", sink), leaf, edge_role="sink_arm")
    require(nx.is_directed_acyclic_graph(graph), "GRAPH_NOT_DAG")
    labels = []
    expected = {"root": (0, 2), "tree": (1, 2),
                "retic": (2, 1), "leaf": (1, 0)}
    for node, data in graph.nodes(data=True):
        require((graph.in_degree(node), graph.out_degree(node)) == expected[data["role"]],
                "GRAPH_DEGREE", (node, data["role"]))
        if isinstance(data.get("label"), int):
            labels.append(data["label"])
        if data["role"] != "leaf":
            require(any(graph.nodes[child]["role"] in {"tree", "leaf"}
                        for child in graph.successors(node)), "TREE_CHILD_FAIL", node)
    require(len(labels) == len(set(labels)), "DUPLICATE_LABEL")
    return graph


def sources():
    answer = []
    for core_id in ("theta0", "theta1", "theta3"):
        spec = CORE[core_id]
        for repair_index, repair in enumerate(spec["repairs"]):
            words = [[] for _ in spec["arcs"]]
            next_label = 1
            for segment in repair:
                words[segment].append(next_label)
                next_label += 1
            sink_labels = {}
            for sink in spec["sinks"]:
                sink_labels[sink] = next_label
                next_label += 1
            graph = build_graph(core_id, tuple(map(tuple, words)), sink_labels, 0)
            answer.append(Completion(core_id, True, repair_index,
                                     (1 << len(spec["sinks"])) - 1,
                                     tuple(map(tuple, words)), graph,
                                     tuple(range(next_label)), ()))
    return tuple(answer)


def targets(selected_total, incoming_selected):
    answer = []
    for core_id, spec in CORE.items():
        outgoing = selected_total - int(incoming_selected)
        for sink_mask in range(1 << len(spec["sinks"])):
            ordinary = outgoing - sink_mask.bit_count()
            if ordinary < 0:
                continue
            for counts in weak_compositions(ordinary, len(spec["arcs"])):
                labels = iter(range(1 if incoming_selected else 0, selected_total))
                selected_words = tuple(tuple(next(labels) for _ in range(count))
                                       for count in counts)
                repair_options = ((None, ()),) if core_id == "cycle" else tuple(enumerate(spec["repairs"]))
                for repair_index, repair in repair_options:
                    words = [list(word) for word in selected_words]
                    dummies = []
                    for segment in repair:
                        if not words[segment]:
                            dummy = f"D_REPAIR_{repair_index}_{segment}"
                            words[segment].append(dummy)
                            dummies.append(dummy)
                    used = [label for word in selected_words for label in word]
                    next_label = max(used) + 1 if used else (1 if incoming_selected else 0)
                    sink_labels = {}
                    for index, sink in enumerate(spec["sinks"]):
                        if (sink_mask >> index) & 1:
                            sink_labels[sink] = next_label
                            next_label += 1
                        else:
                            dummy = f"D_SINK_{index}"
                            sink_labels[sink] = dummy
                            dummies.append(dummy)
                    incoming = 0 if incoming_selected else "INCOMING"
                    if not incoming_selected:
                        dummies.append("INCOMING")
                    graph = build_graph(core_id, tuple(map(tuple, words)), sink_labels, incoming)
                    selected = tuple(sorted(data["label"] for _, data in graph.nodes(data=True)
                                            if isinstance(data.get("label"), int)))
                    require(selected == tuple(range(selected_total)), "TARGET_LABEL_CENSUS")
                    answer.append(Completion(core_id, incoming_selected, repair_index,
                                             sink_mask, tuple(map(tuple, words)), graph,
                                             selected, tuple(sorted(dummies))))
    return tuple(answer)


def relabel(record, permutation):
    graph = record.graph.copy()
    for _, data in graph.nodes(data=True):
        if isinstance(data.get("label"), int):
            data["label"] = permutation[data["label"]]
    return Completion(record.core_id, record.incoming_selected, record.repair_index,
                      record.sink_mask, record.words, graph, tuple(sorted(permutation)),
                      record.dummy_labels)


def restrict_rooted(graph, labels):
    result = graph.copy()
    for node, data in list(result.nodes(data=True)):
        if data["role"] == "leaf" and data.get("label") not in labels:
            result.remove_node(node)
    changed = True
    while changed:
        changed = False
        for node, data in list(result.nodes(data=True)):
            if result.out_degree(node) == 0 and not (data["role"] == "leaf" and data.get("label") in labels):
                result.remove_node(node)
                changed = True
                break
        if changed:
            continue
        for node, data in list(result.nodes(data=True)):
            if data["role"] != "leaf" and result.in_degree(node) == result.out_degree(node) == 1:
                parent = next(result.predecessors(node))
                child = next(result.successors(node))
                result.remove_node(node)
                if parent != child and not result.has_edge(parent, child):
                    result.add_edge(parent, child, edge_role="suppressed")
                changed = True
                break
        if changed:
            continue
        roots = [node for node in result if result.in_degree(node) == 0]
        if len(roots) == 1 and result.nodes[roots[0]]["role"] != "leaf" and result.out_degree(roots[0]) == 1:
            result.remove_node(roots[0])
            changed = True
    for node, data in result.nodes(data=True):
        if data.get("label") in labels:
            data["role"] = "leaf"
        elif result.in_degree(node) == 0:
            data["role"] = "root"
        elif result.in_degree(node) == 2:
            data["role"] = "retic"
        else:
            data["role"] = "tree"
    return result


def selected_graph(record):
    return restrict_rooted(record.graph, set(record.selected_labels))


def switchings(graph):
    retics = [node for node, data in graph.nodes(data=True)
              if data["role"] == "retic" and graph.in_degree(node) == 2]
    incoming = [tuple(graph.in_edges(node)) for node in retics]
    for chosen in itertools.product(*incoming):
        result = graph.copy()
        keep = set(chosen)
        for pair in incoming:
            for edge in pair:
                if edge not in keep:
                    result.remove_edge(*edge)
        yield result


def unrooted_restriction(graph, labels):
    rooted = restrict_rooted(graph, labels)
    result = nx.Graph()
    result.add_nodes_from((node, dict(data)) for node, data in rooted.nodes(data=True))
    result.add_edges_from(rooted.edges())
    changed = True
    while changed:
        changed = False
        for node, data in list(result.nodes(data=True)):
            if data.get("label") not in labels and result.degree(node) <= 1:
                result.remove_node(node); changed = True; break
            if data.get("label") not in labels and result.degree(node) == 2:
                first, second = tuple(result.neighbors(node))
                result.remove_node(node)
                if first != second:
                    result.add_edge(first, second)
                changed = True; break
    return result


def quartet_splits(graph, quartet):
    labels = set(quartet)
    result = set()
    for switching in switchings(graph):
        tree = unrooted_restriction(switching, labels)
        split = None
        for edge in list(tree.edges()):
            tree.remove_edge(*edge)
            components = list(nx.connected_components(tree))
            tree.add_edge(*edge)
            if len(components) != 2:
                continue
            sides = [frozenset(tree.nodes[node].get("label") for node in component
                               if tree.nodes[node].get("label") in labels)
                     for component in components]
            if sorted(map(len, sides)) == [2, 2]:
                split = tuple(sorted((tuple(sorted(sides[0])), tuple(sorted(sides[1])))))
                break
        result.add(split if split is not None else ("star",))
    return frozenset(result)


def triple_type(graph, triple):
    restricted = restrict_rooted(graph, set(triple))
    count = sum(data["role"] == "retic" and restricted.in_degree(node) == 2
                for node, data in restricted.nodes(data=True))
    return "tree" if count == 0 else ("sunlet" if count == 1 else f"r{count}")


def topology_signature(graph):
    labels = tuple(sorted(data["label"] for _, data in graph.nodes(data=True)
                          if isinstance(data.get("label"), int)))
    quartets = tuple((q, quartet_splits(graph, q))
                     for q in itertools.combinations(labels, 4))
    triples = tuple((t, triple_type(graph, t))
                    for t in itertools.combinations(labels, 3))
    return labels, quartets, triples


def permute_signature(signature, permutation):
    _, quartets, triples = signature
    remap = lambda values: tuple(sorted(permutation[value] for value in values))
    mapped_quartets = []
    for quartet, splits in quartets:
        mapped = []
        for split in splits:
            mapped.append(split if split == ("star",) else
                          tuple(sorted((remap(split[0]), remap(split[1])))))
        mapped_quartets.append((remap(quartet), frozenset(mapped)))
    mapped_triples = [(remap(triple), kind) for triple, kind in triples]
    return tuple(sorted(mapped_quartets)), tuple(sorted(mapped_triples))


def immediate_compatible(source_signature, target_signature):
    _, source_quartets, source_triples = source_signature
    target_quartets, target_triples = target_signature
    if tuple(source_quartets) != tuple(target_quartets):
        return False, "quartet"
    source_types, target_types = dict(source_triples), dict(target_triples)
    for triple in source_types:
        if {source_types[triple], target_types[triple]} == {"tree", "sunlet"}:
            return False, "tree_sunlet"
    return True, None


@lru_cache(maxsize=None)
def assignments(k):
    answer = []
    for prefix in itertools.product(range(4), repeat=k - 1):
        final = 0
        for value in prefix:
            final ^= value
        answer.append(prefix + (final,))
    return tuple(answer)


def descendant_masks(graph, kept):
    children = {node: [] for node in graph}
    for tail, head in kept:
        children[tail].append(head)
    order = list(nx.topological_sort(nx.edge_subgraph(graph, kept).copy()))
    masks = {}
    for node in reversed(order):
        label = graph.nodes[node].get("label")
        value = (1 << label) if isinstance(label, int) else 0
        for child in children[node]:
            value |= masks[child]
        masks[node] = value
    return {(tail, head): masks[head] for tail, head in kept}


def sector(mask, characters):
    result, index = 0, 0
    while mask:
        if mask & 1:
            result ^= characters[index]
        mask >>= 1
        index += 1
    return result


def inheritance_polynomial(bits):
    poly = {0: 1}
    for index, bit in enumerate(bits):
        updated = collections.defaultdict(int)
        for mask, coefficient in poly.items():
            if bit:
                updated[mask | (1 << index)] += coefficient
            else:
                updated[mask] += coefficient
                updated[mask | (1 << index)] -= coefficient
        poly = {mask: value for mask, value in updated.items() if value}
    return tuple(sorted(poly.items()))


def compile_descriptor(graph):
    chars = assignments(sum(isinstance(data.get("label"), int)
                            for _, data in graph.nodes(data=True)))
    retics = tuple(sorted((node for node, data in graph.nodes(data=True)
                           if data["role"] == "retic"), key=repr))
    parents = tuple(tuple(sorted(graph.predecessors(node), key=repr)) for node in retics)
    edges = tuple(graph.edges())
    arms = {(tail, head) for tail, head in edges
            if graph.nodes[head]["role"] == "leaf"
            and isinstance(graph.nodes[head].get("label"), int)}
    base = []
    for bits in itertools.product((0, 1), repeat=len(retics)):
        removed = set()
        for index, node in enumerate(retics):
            kept_parent = parents[index][bits[index]]
            removed.update((parent, node) for parent in parents[index] if parent != kept_parent)
        kept = tuple(edge for edge in edges if edge not in removed)
        masks = descendant_masks(graph, kept)
        edge_sectors = {edge: tuple(sector(masks[edge], row) for row in chars)
                        for edge in kept if edge not in arms}
        base.append((bits, kept, edge_sectors))
    actions = [(order, flips) for order in itertools.permutations(range(len(retics)))
               for flips in itertools.product((0, 1), repeat=len(retics))] if retics else [((), ())]
    variants = []
    for order, flips in actions:
        ordered = []
        for new_bits in itertools.product((0, 1), repeat=len(retics)):
            old_bits = [0] * len(retics)
            for index in range(len(retics)):
                old_bits[order[index]] = new_bits[index] ^ flips[index]
            offset = 0
            for bit in old_bits:
                offset = (offset << 1) | bit
            ordered.append((new_bits, base[offset]))
        signatures, internal = [], []
        for edge in edges:
            if edge in arms:
                continue
            signature = []
            for _, (_, _, edge_sectors) in ordered:
                signature.extend(edge_sectors.get(edge, (0,) * len(chars)))
            if any(signature):
                internal.append(edge)
                signatures.append(tuple(signature))
        active = tuple(sorted(set(signatures)))
        class_index = {signature: index for index, signature in enumerate(active)}
        edge_class = {edge: class_index[signature]
                      for edge, signature in zip(internal, signatures)}
        outputs = []
        for coordinate in range(len(chars)):
            grouped = collections.defaultdict(lambda: collections.defaultdict(int))
            for new_bits, (_, kept, edge_sectors) in ordered:
                factors = collections.Counter()
                for edge in kept:
                    index = edge_class.get(edge)
                    if index is None:
                        continue
                    character = edge_sectors.get(edge, (0,) * len(chars))[coordinate]
                    if character:
                        factors[(index, character)] += 1
                monomial = tuple(sorted((index, character, exponent)
                                        for (index, character), exponent in factors.items()))
                for mask, coefficient in inheritance_polynomial(new_bits):
                    grouped[monomial][mask] += coefficient
            outputs.append(tuple(sorted((monomial, tuple(sorted((mask, value)
                                                                  for mask, value in poly.items() if value)))
                                        for monomial, poly in grouped.items()
                                        if any(poly.values()))))
        variants.append(MapDescriptor(len(chars).bit_length() // 2, len(retics), len(active),
                                      tuple(outputs), active))
    # k above is corrected explicitly; bit-length expression is not an authority.
    k = sum(isinstance(data.get("label"), int) for _, data in graph.nodes(data=True))
    best = min(variants, key=lambda row: (row.retic_count, row.edge_class_count,
                                          row.outputs, row.edge_signatures))
    return MapDescriptor(k, best.retic_count, best.edge_class_count,
                         best.outputs, best.edge_signatures)


def sparse_outputs(descriptor):
    parameter_count = 3 * descriptor.edge_class_count + descriptor.retic_count
    answer = []
    for expression in descriptor.outputs:
        poly = collections.defaultdict(int)
        for monomial, inheritance in expression:
            base = [0] * parameter_count
            for edge, character, exponent in monomial:
                base[3 * edge + character - 1] += exponent
            for mask, coefficient in inheritance:
                powers = list(base)
                for index in range(descriptor.retic_count):
                    if (mask >> index) & 1:
                        powers[3 * descriptor.edge_class_count + index] += 1
                poly[tuple(powers)] += coefficient
        answer.append({powers: value for powers, value in poly.items() if value})
    return tuple(answer)


def polynomial_multiply(first, second):
    answer = collections.defaultdict(Q)
    for first_power, first_value in first.items():
        for second_power, second_value in second.items():
            answer[tuple(a + b for a, b in zip(first_power, second_power))] += first_value * second_value
    return {power: value for power, value in answer.items() if value}


def polynomial_product(polynomials):
    if not polynomials:
        return {(): Q(1)}
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = polynomial_multiply(result, polynomial)
    return result


def polynomial_combination(polynomials, coefficients):
    answer = collections.defaultdict(Q)
    for polynomial, scalar in zip(polynomials, coefficients):
        for power, value in polynomial.items():
            answer[power] += Q(scalar) * value
    return {power: value for power, value in answer.items() if value}


def polynomial_hash(polynomial):
    rows = [[list(power), str(value)] for power, value in sorted(polynomial.items())]
    return object_hash(rows)


@lru_cache(maxsize=None)
def coordinate_weights(k):
    return tuple(tuple(int(character == selected)
                       for character in row for selected in (1, 2, 3))
                 for row in assignments(k))


@lru_cache(maxsize=None)
def quadratic_blocks(k):
    weights = coordinate_weights(k)
    blocks = collections.defaultdict(list)
    for first, second in itertools.combinations_with_replacement(range(len(weights)), 2):
        weight = tuple(a + b for a, b in zip(weights[first], weights[second]))
        blocks[weight].append((first, second))
    return tuple((weight, tuple(block)) for weight, block in sorted(blocks.items()))


def primitive_integer_vector(vector):
    denominator = 1
    for value in vector:
        denominator = math.lcm(denominator, Q(value).denominator)
    integers = [int(Q(value) * denominator) for value in vector]
    divisor = 0
    for value in integers:
        divisor = math.gcd(divisor, abs(value))
    if divisor:
        integers = [value // divisor for value in integers]
    if next((value for value in integers if value), 1) < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def kernel_sparse_columns(columns):
    count = len(columns)
    if count == 0:
        return ()
    by_row = collections.defaultdict(lambda: [Q(0)] * count)
    for column, polynomial in enumerate(columns):
        for power, value in polynomial.items():
            by_row[power][column] = Q(value)
    basis, pivots = [], []
    for candidate in by_row.values():
        row = list(candidate)
        for basis_row, pivot in zip(basis, pivots):
            if row[pivot]:
                factor = row[pivot]
                row = [value - factor * base for value, base in zip(row, basis_row)]
        pivot = next((index for index, value in enumerate(row) if value), None)
        if pivot is None:
            continue
        scale = row[pivot]
        row = [value / scale for value in row]
        for index, basis_row in enumerate(basis):
            if basis_row[pivot]:
                factor = basis_row[pivot]
                basis[index] = [value - factor * base for value, base in zip(basis_row, row)]
        place = sum(old < pivot for old in pivots)
        pivots.insert(place, pivot)
        basis.insert(place, row)
        if len(basis) == count:
            break
    free = [index for index in range(count) if index not in pivots]
    result = []
    for free_index in free:
        vector = [Q(0)] * count
        vector[free_index] = Q(1)
        for row, pivot in reversed(tuple(zip(basis, pivots))):
            vector[pivot] = -sum(row[index] * vector[index] for index in free)
        result.append(primitive_integer_vector(vector))
    return tuple(result)


def quadratic_separator(source, target, maximum_block=4):
    source_outputs, target_outputs = sparse_outputs(source), sparse_outputs(target)
    source_products, target_products = {}, {}
    for weight, block in sorted(quadratic_blocks(source.k), key=lambda item: (len(item[1]), item[0])):
        if not 2 <= len(block) <= maximum_block:
            continue
        for pair in block:
            source_products.setdefault(pair, polynomial_multiply(source_outputs[pair[0]], source_outputs[pair[1]]))
            target_products.setdefault(pair, polynomial_multiply(target_outputs[pair[0]], target_outputs[pair[1]]))
        target_columns = [target_products[pair] for pair in block]
        source_columns = [source_products[pair] for pair in block]
        for coefficients in kernel_sparse_columns(target_columns):
            source_pullback = polynomial_combination(source_columns, coefficients)
            if source_pullback:
                require(not polynomial_combination(target_columns, coefficients), "QUADRATIC_TARGET_NONZERO")
                return {"degree": 2, "weight": list(weight),
                        "coordinate_pairs": [list(pair) for pair in block],
                        "coefficients": list(coefficients),
                        "source_nonzero_terms": len(source_pullback),
                        "source_pullback_sha256": polynomial_hash(source_pullback)}
    return None


def exact_point(descriptor, salt=0):
    edges = []
    for index in range(descriptor.edge_class_count):
        c = Q(3 * index + 5 + salt, 12 * index + 23 + 4 * salt)
        g = Q(5 * index + 7 + salt, 18 * index + 29 + 3 * salt)
        t = Q(7 * index + 9 + salt, 22 * index + 35 + 2 * salt)
        require(min(c, g, t, c - g*t, g - c*t, t - c*g,
                    1 + c-g-t, 1-c+g-t, 1-c-g+t) > 0, "POINT_NOT_STRICT")
        edges.append((c, g, t))
    inheritance = tuple(Q(index + 2 + salt, index + 5 + 2 * salt)
                        for index in range(descriptor.retic_count))
    require(all(0 < value < 1 for value in inheritance), "INHERITANCE_NOT_STRICT")
    return tuple(edges), inheritance


def evaluate(descriptor, edges, inheritance):
    result = []
    for expression in descriptor.outputs:
        value = Q(0)
        for monomial, poly in expression:
            edge_value = Q(1)
            for edge, character, exponent in monomial:
                edge_value *= edges[edge][character - 1] ** exponent
            inheritance_value = Q(0)
            for mask, coefficient in poly:
                term = Q(coefficient)
                for index, variable in enumerate(inheritance):
                    if (mask >> index) & 1:
                        term *= variable
                inheritance_value += term
            value += edge_value * inheritance_value
        result.append(value)
    return tuple(result)


def jacobian(descriptor, edges, inheritance):
    parameter_count = 3 * descriptor.edge_class_count + descriptor.retic_count
    result = []
    for expression in descriptor.outputs:
        row = [Q(0)] * parameter_count
        for monomial, poly in expression:
            edge_value = Q(1)
            for edge, character, exponent in monomial:
                edge_value *= edges[edge][character - 1] ** exponent
            inheritance_value = Q(0)
            inheritance_derivative = [Q(0)] * descriptor.retic_count
            for mask, coefficient in poly:
                term = Q(coefficient)
                for index, variable in enumerate(inheritance):
                    if (mask >> index) & 1:
                        term *= variable
                inheritance_value += term
                for index, variable in enumerate(inheritance):
                    if (mask >> index) & 1:
                        inheritance_derivative[index] += term / variable
            for edge, character, exponent in monomial:
                column = 3 * edge + character - 1
                row[column] += edge_value * inheritance_value * exponent / edges[edge][character - 1]
            for index, derivative in enumerate(inheritance_derivative):
                row[3 * descriptor.edge_class_count + index] += edge_value * derivative
        result.append(row)
    return result


def rank_pivots(matrix):
    work = [list(map(Q, row)) for row in matrix]
    row_ids = list(range(len(work)))
    rank, rows, columns = 0, [], []
    for column in range(len(work[0]) if work else 0):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        row_ids[rank], row_ids[pivot] = row_ids[pivot], row_ids[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                factor = work[row][column]
                work[row] = [value - factor * base for value, base in zip(work[row], work[rank])]
        rows.append(row_ids[rank]); columns.append(column); rank += 1
        if rank == len(work):
            break
    return rank, tuple(rows), tuple(columns)


def determinant(matrix):
    work = [list(map(Q, row)) for row in matrix]
    result = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        scale = work[column][column]
        result *= scale
        for row in range(column + 1, len(work)):
            factor = work[row][column] / scale
            for index in range(column + 1, len(work)):
                work[row][index] -= factor * work[column][index]
    return result


def rank_certificate(descriptor, salt=0):
    edges, inheritance = exact_point(descriptor, salt)
    matrix = jacobian(descriptor, edges, inheritance)
    rank, rows, columns = rank_pivots(matrix)
    det = determinant([[matrix[row][column] for column in columns] for row in rows])
    require(det != 0, "RANK_MINOR_ZERO")
    return {"rank": rank, "rows": list(rows), "columns": list(columns),
            "determinant": str(det),
            "edge_triples": [[str(value) for value in triple] for triple in edges],
            "inheritance": [str(value) for value in inheritance]}


def lcm(left, right):
    return abs(left // math.gcd(left, right) * right) if left and right else 0


def syzygy_rank_upper(descriptor, include_evaluation_witness=False):
    """Coefficientwise solve for polynomial fields and evaluate their kernel span.

    If A is the coefficient matrix for J_f V=0 and E evaluates coefficient
    vectors at a strict point, then E(ker A) has dimension
    rank([A;E])-rank(A).  A nonzero minor witnessing this rank persists on a
    Zariski-open set, so p-dim(E(ker A)) is a genuine generic rank upper.
    """
    from sympy import ZZ
    from sympy.polys.matrices import DomainMatrix

    outputs = sparse_outputs(descriptor)
    edge_variables = 3 * descriptor.edge_class_count
    retics = descriptor.retic_count
    parameter_count = edge_variables + retics
    labels = [("edge", parameter, mask)
              for parameter in range(edge_variables) for mask in range(1 << retics)]
    labels += [("inheritance", parameter, mask)
               for parameter in range(retics) for mask in range(1 << retics)
               if not ((mask >> parameter) & 1)]
    column = {label: index for index, label in enumerate(labels)}
    equations = collections.defaultdict(lambda: collections.defaultdict(int))
    for output_index, polynomial in enumerate(outputs):
        for powers, coefficient in polynomial.items():
            for parameter in range(edge_variables):
                if not powers[parameter]:
                    continue
                for mask in range(1 << retics):
                    shifted = list(powers)
                    for index in range(retics):
                        if (mask >> index) & 1:
                            shifted[edge_variables + index] += 1
                    equations[(output_index, tuple(shifted))][column[("edge", parameter, mask)]] += coefficient * powers[parameter]
            for parameter in range(retics):
                position = edge_variables + parameter
                if not powers[position]:
                    continue
                for mask in range(1 << retics):
                    if (mask >> parameter) & 1:
                        continue
                    shifted = list(powers)
                    for index in range(retics):
                        if (mask >> index) & 1:
                            shifted[edge_variables + index] += 1
                    equations[(output_index, tuple(shifted))][column[("inheritance", parameter, mask)]] += coefficient * powers[position]
                    shifted[position] += 1
                    equations[(output_index, tuple(shifted))][column[("inheritance", parameter, mask)]] -= coefficient * powers[position]
    coefficient_system = []
    for key in sorted(equations):
        row = [equations[key].get(index, 0) for index in range(len(labels))]
        if any(row):
            coefficient_system.append(row)
    edges, inheritance = exact_point(descriptor)
    edge_values = tuple(value for triple in edges for value in triple)
    evaluation = []
    for parameter in range(parameter_count):
        rational = []
        for kind, index, mask in labels:
            monomial = Q(1)
            for retic, value in enumerate(inheritance):
                if (mask >> retic) & 1:
                    monomial *= value
            entry = Q(0)
            if kind == "edge" and parameter == index:
                entry = edge_values[index] * monomial
            if kind == "inheritance" and parameter == edge_variables + index:
                entry = inheritance[index] * (1 - inheritance[index]) * monomial
            rational.append(entry)
        denominator = 1
        for value in rational:
            denominator = lcm(denominator, value.denominator)
        evaluation.append([int(value * denominator) for value in rational])
    integer_rank = lambda rows: (0 if not rows else int(DomainMatrix.from_list(rows, ZZ).rank()))
    coefficient_matrix = DomainMatrix.from_list(coefficient_system, ZZ)
    coefficient_rank = int(coefficient_matrix.rank()) if coefficient_system else 0
    stacked_rank = integer_rank(coefficient_system + evaluation)
    independent = stacked_rank - coefficient_rank
    require(0 <= independent <= parameter_count, "SYZYGY_DIMENSION")
    result = {
        "mechanism": "coefficientwise_multilinear_polynomial_vector_fields",
        "parameter_count": parameter_count,
        "unknown_coefficient_count": len(labels),
        "coefficient_equation_count": len(coefficient_system),
        "coefficient_system_rank": coefficient_rank,
        "stacked_system_rank": stacked_rank,
        "independent_kernel_fields": independent,
        "certified_rank_upper": parameter_count - independent,
    }
    if include_evaluation_witness:
        # DomainMatrix.nullspace returns one exact integer kernel vector per
        # row.  Evaluating those rows gives a p-by-k matrix for E|ker(A).
        kernel_rows = ([list(map(int, row)) for row in
                        coefficient_matrix.nullspace().to_Matrix().tolist()]
                       if coefficient_system else
                       [[int(index == column) for column in range(len(labels))]
                        for index in range(len(labels))])
        image = [[sum(evaluation_row[column] * kernel_row[column]
                      for column in range(len(labels)))
                  for kernel_row in kernel_rows]
                 for evaluation_row in evaluation]
        image_rank, minor_rows, minor_columns = rank_pivots(image)
        require(image_rank == independent, "SYZYGY_EVALUATION_IMAGE_RANK",
                (image_rank, independent))
        minor = [[image[row][column] for column in minor_columns]
                 for row in minor_rows]
        minor_determinant = determinant(minor) if image_rank else Q(1)
        require(minor_determinant != 0, "SYZYGY_EVALUATION_MINOR_ZERO")
        result.update({
            "evaluation_kernel_basis_count": len(kernel_rows),
            "evaluation_image_minor_rows": list(minor_rows),
            "evaluation_image_minor_columns": list(minor_columns),
            "evaluation_image_minor_determinant": str(minor_determinant),
        })
    return result


def root_suppressed(graph):
    result = graph.copy()
    roots = [node for node, data in result.nodes(data=True)
             if data["role"] == "root" or result.in_degree(node) == 0]
    require(len(roots) == 1, "MIXED_ROOT_CENSUS")
    root = roots[0]
    children = tuple(result.successors(root))
    require(len(children) == 2, "MIXED_ROOT_DEGREE")
    mixed = nx.Graph()
    for node, data in result.nodes(data=True):
        if node != root:
            mixed.add_node(node, role=data.get("role"), label=data.get("label"))
    for tail, head in result.edges():
        if tail != root:
            heads = frozenset({head}) if result.nodes[head]["role"] == "retic" else frozenset()
            require(not mixed.has_edge(tail, head), "MIXED_PARALLEL")
            mixed.add_edge(tail, head, heads=heads)
    first, second = children
    require(first != second and not mixed.has_edge(first, second), "ROOT_SUPPRESSION_NOT_SIMPLE")
    mixed.add_edge(first, second,
                   heads=frozenset(node for node in children if result.nodes[node]["role"] == "retic"))
    return mixed


def incidence_graph(mixed, forgotten=()):
    forgotten = {frozenset(edge) for edge in forgotten}
    result = nx.Graph()
    for vertex, data in mixed.nodes(data=True):
        result.add_node(("v", vertex), kind="vertex", label=data.get("label"))
    for index, (first, second, data) in enumerate(mixed.edges(data=True)):
        edge_node = ("e", index)
        result.add_node(edge_node, kind="edge", label=None)
        heads = data.get("heads", frozenset())
        forget = frozenset((first, second)) in forgotten
        result.add_edge(edge_node, ("v", first), head=False if forget else first in heads)
        result.add_edge(edge_node, ("v", second), head=False if forget else second in heads)
    return result


def incidence_isomorphic(first, second):
    node_match = lambda a, b: a.get("kind") == b.get("kind") and a.get("label") == b.get("label")
    edge_match = lambda a, b: a.get("head") == b.get("head")
    return nx.algorithms.isomorphism.GraphMatcher(first, second,
                                                  node_match=node_match,
                                                  edge_match=edge_match).is_isomorphic()


def triangles(mixed):
    result = []
    for clique in nx.enumerate_all_cliques(mixed):
        if len(clique) == 3:
            result.append({frozenset((clique[0], clique[1])),
                           frozenset((clique[0], clique[2])),
                           frozenset((clique[1], clique[2]))})
        elif len(clique) > 3:
            break
    return result


def mixed_relation(source, target):
    try:
        first, second = root_suppressed(source), root_suppressed(target)
    except ReplayFailure:
        return "none"
    if incidence_isomorphic(incidence_graph(first), incidence_graph(second)):
        return "isomorphic"
    for first_triangle in triangles(first):
        for second_triangle in triangles(second):
            if incidence_isomorphic(incidence_graph(first, first_triangle),
                                    incidence_graph(second, second_triangle)):
                return "triangle"
    return "none"


def mixed_automorphisms(record, permutations):
    base = root_suppressed(record.graph)
    result = []
    for permutation in permutations:
        candidate = root_suppressed(relabel(record, permutation).graph)
        if incidence_isomorphic(incidence_graph(base), incidence_graph(candidate)):
            result.append(tuple(permutation))
    return tuple(sorted(result))


def compose(left, right):
    return tuple(left[right[index]] for index in range(4))


H14 = (
    (+1, ((0, 0, 0), (1, 2, 3), (2, 3, 1), (3, 1, 2))),
    (-1, ((0, 0, 0), (1, 3, 2), (2, 1, 3), (3, 2, 1))),
    (-1, ((0, 1, 1), (1, 2, 3), (2, 0, 2), (3, 3, 0))),
    (+1, ((0, 1, 1), (1, 3, 2), (2, 2, 0), (3, 0, 3))),
    (+1, ((0, 2, 2), (1, 0, 1), (2, 1, 3), (3, 3, 0))),
    (-1, ((0, 2, 2), (1, 1, 0), (2, 3, 1), (3, 0, 3))),
    (-1, ((0, 3, 3), (1, 0, 1), (2, 2, 0), (3, 1, 2))),
    (+1, ((0, 3, 3), (1, 1, 0), (2, 0, 2), (3, 2, 1))),
)


def h14_terms(omitted, port_order, character_permutation):
    coordinate = {row: index for index, row in enumerate(assignments(4))}
    remap = {0: 0, **dict(zip((1, 2, 3), character_permutation))}
    rows = []
    for coefficient, triples in H14:
        indices, labels = [], []
        for triple in triples:
            assignment = [0, 0, 0, 0]
            for local, global_port in enumerate(port_order):
                assignment[global_port] = remap[triple[local]]
            assignment = tuple(assignment)
            indices.append(coordinate[assignment])
            labels.append("0CGT"[assignment[0]] + "0CGT"[assignment[1]] +
                          "0CGT"[assignment[2]] + "0CGT"[assignment[3]])
        rows.append({"coefficient": coefficient, "coordinate_indices": indices,
                     "coordinate_labels": labels})
    return rows


def quartic_pullback(descriptor, terms):
    outputs = sparse_outputs(descriptor)
    products = [polynomial_product([outputs[index] for index in term["coordinate_indices"]])
                for term in terms]
    return polynomial_combination(products, [term["coefficient"] for term in terms])


def h14_separator(source, target, source_index):
    for omitted in range(4):
        retained = tuple(port for port in range(4) if port != omitted)
        for port_order in itertools.permutations(retained):
            for character_permutation in itertools.permutations((1, 2, 3)):
                terms = h14_terms(omitted, port_order, character_permutation)
                if quartic_pullback(target, terms):
                    continue
                source_pullback = quartic_pullback(source, terms)
                if not source_pullback:
                    continue
                edges, inheritance = exact_point(source, source_index)
                outputs = evaluate(source, edges, inheritance)
                value = sum(Q(term["coefficient"]) * math.prod(outputs[index]
                            for index in term["coordinate_indices"]) for term in terms)
                require(value != 0, "H14_SOURCE_EVALUATION_ZERO")
                return {"degree": 4, "base_identity": "normalized_three_leaf_H14_quartic",
                        "omitted_port": omitted, "retained_port_order": list(port_order),
                        "character_permutation": list(character_permutation), "terms": terms,
                        "target_pullback_term_count": 0,
                        "source_pullback_term_count": len(source_pullback),
                        "source_pullback_sha256": polynomial_hash(source_pullback),
                        "source_evaluation": str(value)}
    return None
