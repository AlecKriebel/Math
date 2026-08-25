#!/usr/bin/env python3
"""Independent clean-room verifier for the H21-01 transport and all 14 orbits.

This file uses only the Python standard library and the immutable, flattened
input bundle.  It does not import the primary atlas, graph canonicalizer,
switching/Fourier compiler, orbit reducer, polynomial selector, or rank
selector.  Graph presentations, semi-directed automorphisms, double cosets,
Fourier coordinate transport, map descriptors, polynomial pullbacks, and exact
rank minors are reconstructed here.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import permutations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
if not __debug__ or sys.flags.optimize:
    raise RuntimeError(
        "certification verifier refuses optimized Python; rerun without -O or PYTHONOPTIMIZE"
    )


class CertificationError(RuntimeError):
    """A deterministic, non-optimizable certification-gate failure."""


def require(condition, message, *details):
    if not condition:
        suffix = "" if not details else f": {details!r}"
        raise CertificationError(f"{message}{suffix}")


ARTIFACTS = Path(os.environ.get(
    "K3P_CLEANROOM_ARTIFACTS",
    HERE.parent / "input_frozen" / "k3p_cloud_artifacts",
)).resolve()
EXPECTED_INPUT_SHA256 = {
    "K3P_14_ORBIT_LOCK.json":
        "61d88a67b487ebbee1cae881def23fdce770d4fa0cac0d6b86be02e7368438a3",
    "k3p_prelock_source5_quartic.json":
        "5e7bf1599f2a28858b2dbce3993baf6adea9e27cef9ffa8d23503200742d0a5e",
    "k3p_h14_marginal_orbit_certificates.json":
        "41c3c9756536a28b9fc24250c62491e10322e66c0bd4c4b692e939aade2395c0",
    "k3p_remaining_quartic_separators.json":
        "8ee39cd08a01f9e9dd385e41bbab4814f7e0859f143aceda4e8831ddba053f61",
    "k3p_directed_rank_obstructions.json":
        "fa0ac74cde903edc422a90b5e490bd639b2e2b4c758d9d3ec10a794f1a044f42",
}


def load_bound_json(filename):
    path = ARTIFACTS / filename
    payload = path.read_bytes()
    observed = hashlib.sha256(payload).hexdigest()
    expected = EXPECTED_INPUT_SHA256.get(filename)
    require(expected is not None, "unregistered active input", filename)
    require(observed == expected, "active input hash mismatch",
            filename, observed, expected)
    return json.loads(payload)


LOCK = load_bound_json("K3P_14_ORBIT_LOCK.json")
RECORDS = {record["orbit_id"]: record for record in LOCK["records"]}

CH4 = tuple(prefix + (prefix[0] ^ prefix[1] ^ prefix[2],)
            for prefix in product(range(4), repeat=3))
CH4_INDEX = {chars: index for index, chars in enumerate(CH4)}
CH3 = tuple(prefix + (prefix[0] ^ prefix[1],)
            for prefix in product(range(4), repeat=2))
LETTER = "0CGT"
IDENTITY = (0, 1, 2, 3)


# Ordered exactly by the mathematical core census, not loaded from the primary
# compiler.  Segment indices are positions in each arcs tuple.
CORES = {
    "cycle": {
        "arcs": (("S", "X"), ("S", "X")),
        "retics": ("X",),
        "sinks": ("X",),
        "repairs": ((0,), (1,)),
    },
    "theta0": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X"),
                 ("V", "X"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (3, 4)),
    },
    "theta1": {
        "arcs": (("S", "U"), ("S", "X"), ("V", "X"),
                 ("U", "V"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (2, 4)),
    },
    "theta2": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X0"),
                 ("V", "X0"), ("U", "X1"), ("V", "X1")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
    },
    "theta3": {
        "arcs": (("S", "U"), ("S", "X0"), ("V", "X0"),
                 ("U", "X1"), ("V", "X1"), ("U", "V")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2,), (4,)),
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_hash(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(payload)


def compose(left, right):
    """Permutation composition left o right, with arrays mapping old to new."""
    return tuple(left[right[index]] for index in range(4))


def inverse(perm):
    result = [None] * len(perm)
    for old, new in enumerate(perm):
        result[new] = old
    return tuple(result)


@dataclass(frozen=True)
class ConstructionRecord:
    core_id: str
    incoming_selected: bool
    repair_index: int | None
    selected_sink_mask: int
    words: tuple
    graph: "Graph"


class Graph:
    """Small rooted directed graph with construction edge roles."""

    def __init__(self, nodes=None, arcs=None, edge_roles=None):
        self.node = {} if nodes is None else {node: dict(data)
                                              for node, data in nodes.items()}
        self.arcs = tuple(sorted(set(() if arcs is None else arcs), key=repr))
        self.edge_role = {} if edge_roles is None else dict(edge_roles)
        self.out = defaultdict(list)
        self.inc = defaultdict(list)
        for tail, head in self.arcs:
            self.out[tail].append(head)
            self.inc[head].append(tail)
        for node in self.node:
            self.out[node].sort(key=repr)
            self.inc[node].sort(key=repr)

    @classmethod
    def from_literal(cls, literal):
        nodes = {}
        for entry in literal["nodes"]:
            node = ast.literal_eval(entry["id"])
            data = dict(entry)
            data.pop("id")
            nodes[node] = data
        arcs = []
        roles = {}
        for entry in literal["arcs"]:
            edge = (ast.literal_eval(entry["tail"]), ast.literal_eval(entry["head"]))
            arcs.append(edge)
            roles[edge] = entry.get("edge_role")
        return cls(nodes, arcs, roles)

    def relabel(self, perm):
        nodes = {node: dict(data) for node, data in self.node.items()}
        for data in nodes.values():
            if isinstance(data.get("label"), int):
                data["label"] = perm[data["label"]]
        return Graph(nodes, self.arcs, self.edge_role)

    def literal(self):
        nodes = []
        for node in sorted(self.node, key=repr):
            data = self.node[node]
            nodes.append({
                "dummy": bool(data.get("dummy", False)),
                "dummy_name": data.get("dummy_name"),
                "id": repr(node),
                "label": data.get("label"),
                "role": data["role"],
            })
        arcs = []
        for edge in sorted(self.arcs, key=lambda item: (repr(item[0]), repr(item[1]))):
            tail, head = edge
            arcs.append({
                "edge_role": self.edge_role.get(edge),
                "head": repr(head),
                "tail": repr(tail),
            })
        return {"arcs": arcs, "nodes": nodes}


def _node(role, label=None, dummy=False, dummy_name=None):
    return {
        "role": role,
        "label": label,
        "dummy": dummy,
        "dummy_name": dummy_name,
    }


def build_graph(core_id, words, sink_labels, incoming_label):
    spec = CORES[core_id]
    nodes = {}
    edges = []
    roles = {}

    for name in {name for edge in spec["arcs"] for name in edge}:
        role = "retic" if name in spec["retics"] else "tree"
        nodes[("core", name)] = _node(role)

    root = ("root",)
    incoming_leaf = ("leaf", "INCOMING")
    nodes[root] = _node("root")
    selected = isinstance(incoming_label, int)
    nodes[incoming_leaf] = _node(
        "leaf",
        incoming_label if selected else None,
        not selected,
        None if selected else str(incoming_label),
    )

    def add(tail, head, role):
        edge = (tail, head)
        if edge in roles:
            raise AssertionError(("unexpected parallel presentation edge", edge))
        edges.append(edge)
        roles[edge] = role

    add(root, ("core", "S"), "incoming_core")
    add(root, incoming_leaf, "incoming_arm")
    for segment, (((tail, head), word)) in enumerate(zip(spec["arcs"], words)):
        previous = ("core", tail)
        for position, label in enumerate(word):
            subdivision = ("sub", segment, position)
            leaf = ("leaf", "seg", segment, position)
            nodes[subdivision] = _node("tree")
            selected = isinstance(label, int)
            nodes[leaf] = _node(
                "leaf", label if selected else None, not selected,
                None if selected else str(label),
            )
            add(previous, subdivision, f"seg{segment}")
            add(subdivision, leaf, "arm")
            previous = subdivision
        add(previous, ("core", head), f"seg{segment}")
    for sink_index, sink in enumerate(spec["sinks"]):
        label = sink_labels[sink]
        selected = isinstance(label, int)
        leaf = ("leaf", "sink", sink_index)
        nodes[leaf] = _node(
            "leaf", label if selected else None, not selected,
            None if selected else str(label),
        )
        add(("core", sink), leaf, "sink_arm")

    graph = Graph(nodes, edges, roles)
    validate_rooted_graph(graph)
    return graph


def validate_rooted_graph(graph):
    roots = [node for node, data in graph.node.items() if data["role"] == "root"]
    require(len(roots) == 1, "rooted graph must have exactly one root", roots)
    labels = []
    for node, data in graph.node.items():
        degree = (len(graph.inc[node]), len(graph.out[node]))
        expected = {
            "root": (0, 2),
            "tree": (1, 2),
            "retic": (2, 1),
            "leaf": (1, 0),
        }[data["role"]]
        require(degree == expected, "rooted graph degree/role mismatch",
                node, degree, expected)
        if isinstance(data.get("label"), int):
            labels.append(data["label"])
    require(len(labels) == len(set(labels)), "duplicate selected leaf label", labels)

    state = {}

    def visit(node):
        if state.get(node) == 1:
            raise AssertionError("directed cycle")
        if state.get(node) == 2:
            return
        state[node] = 1
        for child in graph.out[node]:
            visit(child)
        state[node] = 2

    for node in graph.node:
        visit(node)


def weak_compositions(total, bins):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def source_supports():
    records = []
    for core_id in ("theta0", "theta1", "theta3"):
        spec = CORES[core_id]
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
            graph = build_graph(core_id, tuple(tuple(word) for word in words),
                                sink_labels, 0)
            records.append(ConstructionRecord(
                core_id, True, repair_index,
                (1 << len(spec["sinks"])) - 1,
                tuple(tuple(word) for word in words), graph,
            ))
    return records


def target_completions(selected_total, incoming_selected):
    records = []
    for core_id, spec in CORES.items():
        outgoing_total = selected_total - 1 if incoming_selected else selected_total
        sink_count = len(spec["sinks"])
        for sink_mask in range(1 << sink_count):
            selected_sinks = sum((sink_mask >> index) & 1
                                 for index in range(sink_count))
            ordinary = outgoing_total - selected_sinks
            if ordinary < 0:
                continue
            for counts in weak_compositions(ordinary, len(spec["arcs"])):
                labels = iter(range(1 if incoming_selected else 0, selected_total))
                selected_words = tuple(
                    tuple(next(labels) for _ in range(count)) for count in counts
                )
                repair_options = (((None, ()),) if core_id == "cycle" else
                                  tuple(enumerate(spec["repairs"])))
                for repair_index, repair in repair_options:
                    words = [list(word) for word in selected_words]
                    for segment in repair:
                        if not words[segment]:
                            words[segment].append(
                                f"D_REPAIR_{repair_index}_{segment}"
                            )
                    used = [label for word in selected_words for label in word]
                    next_label = ((max(used) + 1) if used else
                                  (1 if incoming_selected else 0))
                    sink_labels = {}
                    for sink_index, sink in enumerate(spec["sinks"]):
                        if (sink_mask >> sink_index) & 1:
                            sink_labels[sink] = next_label
                            next_label += 1
                        else:
                            sink_labels[sink] = f"D_SINK_{sink_index}"
                    incoming = 0 if incoming_selected else "INCOMING"
                    graph = build_graph(
                        core_id, tuple(tuple(word) for word in words),
                        sink_labels, incoming,
                    )
                    selected = sorted(
                        data["label"] for data in graph.node.values()
                        if isinstance(data.get("label"), int)
                    )
                    require(selected == list(range(selected_total)),
                            "completion selected-label census mismatch",
                            core_id, selected, selected_total)
                    records.append(ConstructionRecord(
                        core_id, incoming_selected, repair_index, sink_mask,
                        tuple(tuple(word) for word in words), graph,
                    ))
    return records


SOURCES = source_supports()
TARGETS = target_completions(4, True) + target_completions(4, False)


def descendant_masks(graph, kept_edges):
    children = defaultdict(list)
    for tail, head in kept_edges:
        children[tail].append(head)
    memo = {}

    def descend(node):
        if node in memo:
            return memo[node]
        label = graph.node[node].get("label")
        mask = (1 << label) if isinstance(label, int) else 0
        for child in children[node]:
            mask |= descend(child)
        memo[node] = mask
        return mask

    for node in graph.node:
        descend(node)
    return {edge: memo[edge[1]] for edge in kept_edges}


def sector(mask, chars):
    answer = 0
    index = 0
    while mask:
        if mask & 1:
            answer ^= chars[index]
        index += 1
        mask >>= 1
    return answer


def inheritance_weight(bits):
    poly = {0: 1}
    for index, bit in enumerate(bits):
        updated = defaultdict(int)
        for mask, coefficient in poly.items():
            if bit:
                updated[mask | (1 << index)] += coefficient
            else:
                updated[mask] += coefficient
                updated[mask | (1 << index)] -= coefficient
        poly = {mask: coefficient for mask, coefficient in updated.items()
                if coefficient}
    return tuple(sorted(poly.items()))


@dataclass(frozen=True)
class MapDescriptor:
    k: int
    retic_count: int
    edge_class_count: int
    outputs: tuple
    edge_signatures: tuple


def descriptor_variant(graph, reticulation_order, parent_orders):
    selected_arms = {
        edge for edge in graph.arcs
        if graph.node[edge[1]]["role"] == "leaf"
        and isinstance(graph.node[edge[1]].get("label"), int)
    }
    switches = []
    for bits in product((0, 1), repeat=len(reticulation_order)):
        removed = set()
        for index, reticulation in enumerate(reticulation_order):
            kept_parent = parent_orders[index][bits[index]]
            for parent in graph.inc[reticulation]:
                if parent != kept_parent:
                    removed.add((parent, reticulation))
        kept = tuple(edge for edge in graph.arcs if edge not in removed)
        switches.append((bits, kept, descendant_masks(graph, kept)))

    signatures = []
    internal_edges = []
    for edge in graph.arcs:
        if edge in selected_arms:
            continue
        signature = []
        for _, _, masks in switches:
            if edge not in masks:
                signature.extend((0,) * len(CH4))
            else:
                signature.extend(sector(masks[edge], chars) for chars in CH4)
        if any(signature):
            internal_edges.append(edge)
            signatures.append(tuple(signature))

    active = tuple(sorted(set(signatures)))
    signature_class = {signature: index for index, signature in enumerate(active)}
    edge_class = {edge: signature_class[signature]
                  for edge, signature in zip(internal_edges, signatures)}

    outputs = []
    for chars in CH4:
        grouped = defaultdict(lambda: defaultdict(int))
        for bits, kept, masks in switches:
            factors = Counter()
            for edge in kept:
                class_index = edge_class.get(edge)
                if class_index is None:
                    continue
                character = sector(masks[edge], chars)
                if character:
                    factors[(class_index, character)] += 1
            monomial = tuple(sorted(
                (class_index, character, exponent)
                for (class_index, character), exponent in factors.items()
            ))
            for mask, coefficient in inheritance_weight(bits):
                grouped[monomial][mask] += coefficient
        expression = []
        for monomial, poly in grouped.items():
            nonzero = tuple(sorted((mask, coefficient)
                                   for mask, coefficient in poly.items()
                                   if coefficient))
            if nonzero:
                expression.append((monomial, nonzero))
        outputs.append(tuple(sorted(expression)))
    return MapDescriptor(4, len(reticulation_order), len(active),
                         tuple(outputs), active)


def compile_map(graph):
    reticulations = tuple(sorted(
        (node for node, data in graph.node.items() if data["role"] == "retic"),
        key=repr,
    ))
    variants = []
    for order in permutations(reticulations):
        parents = [tuple(sorted(graph.inc[reticulation], key=repr))
                   for reticulation in order]
        for flips in product((0, 1), repeat=len(order)):
            parent_orders = tuple((pair[flip], pair[1 - flip])
                                  for pair, flip in zip(parents, flips))
            variants.append(descriptor_variant(graph, order, parent_orders))
    return min(variants, key=lambda descriptor: (
        descriptor.retic_count,
        descriptor.edge_class_count,
        descriptor.outputs,
        descriptor.edge_signatures,
    ))


def physical_fourier_map(graph):
    """Uncollapsed map keyed by physical edges, for coordinate transport checks."""
    reticulations = tuple(sorted(
        (node for node, data in graph.node.items() if data["role"] == "retic"),
        key=repr,
    ))
    parents = tuple(tuple(sorted(graph.inc[node], key=repr))
                    for node in reticulations)
    selected_arms = {
        edge for edge in graph.arcs
        if graph.node[edge[1]]["role"] == "leaf"
        and isinstance(graph.node[edge[1]].get("label"), int)
    }
    switches = []
    for bits in product((0, 1), repeat=len(reticulations)):
        removed = set()
        for index, reticulation in enumerate(reticulations):
            kept_parent = parents[index][bits[index]]
            for parent in graph.inc[reticulation]:
                if parent != kept_parent:
                    removed.add((parent, reticulation))
        kept = tuple(edge for edge in graph.arcs if edge not in removed)
        switches.append((bits, kept, descendant_masks(graph, kept)))

    outputs = []
    for chars in CH4:
        grouped = defaultdict(lambda: defaultdict(int))
        for bits, kept, masks in switches:
            factors = Counter()
            for edge in kept:
                if edge in selected_arms:
                    continue
                character = sector(masks[edge], chars)
                if character:
                    factors[(repr(edge), character)] += 1
            monomial = tuple(sorted(
                (edge, character, exponent)
                for (edge, character), exponent in factors.items()
            ))
            for mask, coefficient in inheritance_weight(bits):
                grouped[monomial][mask] += coefficient
        expression = []
        for monomial, poly in grouped.items():
            nonzero = tuple(sorted((mask, coefficient)
                                   for mask, coefficient in poly.items()
                                   if coefficient))
            if nonzero:
                expression.append((monomial, nonzero))
        outputs.append(tuple(sorted(expression)))
    return tuple(outputs)


def coordinate_transport(perm):
    """For G^perm at new assignment a, return the base-G assignment index."""
    return tuple(CH4_INDEX[tuple(chars[perm[old]] for old in range(4))]
                 for chars in CH4)


def verify_fourier_transport(base_graph, relabelled_graph, perm):
    base = physical_fourier_map(base_graph)
    transported = physical_fourier_map(relabelled_graph)
    coordinate_map = coordinate_transport(perm)
    require(all(transported[index] == base[coordinate_map[index]]
                for index in range(len(CH4))),
            "physical-edge Fourier coordinate transport mismatch", perm)
    return coordinate_map


@dataclass(frozen=True)
class MixedGraph:
    labels: dict
    edges: dict

    def relabel(self, perm):
        labels = dict(self.labels)
        for node, label in labels.items():
            if isinstance(label, int):
                labels[node] = perm[label]
        return MixedGraph(labels, self.edges)


def root_suppressed_mixed(graph):
    roots = [node for node, data in graph.node.items()
             if data["role"] == "root"]
    require(len(roots) == 1, "root suppression requires exactly one root", roots)
    root = roots[0]
    children = tuple(graph.out[root])
    require(len(children) == 2, "root suppression requires two root children",
            children)
    labels = {node: data.get("label") for node, data in graph.node.items()
              if node != root}
    edges = {}
    for tail, head in graph.arcs:
        if tail == root:
            continue
        key = frozenset((tail, head))
        require(len(key) == 2 and key not in edges,
                "invalid or duplicate mixed edge during root suppression",
                tail, head)
        heads = frozenset((head,)) if graph.node[head]["role"] == "retic" else frozenset()
        edges[key] = heads
    first, second = children
    key = frozenset((first, second))
    require(len(key) == 2 and key not in edges,
            "invalid suppressed-root edge", children)
    root_heads = frozenset(
        node for node in children if graph.node[node]["role"] == "retic"
    )
    edges[key] = root_heads
    return MixedGraph(labels, edges)


def mixed_adjacency(graph):
    adjacency = defaultdict(dict)
    for endpoints, heads in graph.edges.items():
        first, second = tuple(endpoints)
        adjacency[first][second] = (first in heads, second in heads)
        adjacency[second][first] = (second in heads, first in heads)
    return adjacency


def mixed_isomorphism(first, second):
    if len(first.labels) != len(second.labels) or len(first.edges) != len(second.edges):
        return None
    first_adj = mixed_adjacency(first)
    second_adj = mixed_adjacency(second)

    def invariant(graph, adjacency, node):
        return (
            graph.labels[node],
            len(adjacency[node]),
            sum(flags[0] for flags in adjacency[node].values()),
            tuple(sorted(
                ((flags[0], flags[1], graph.labels[neighbor])
                 for neighbor, flags in adjacency[node].items()),
                key=repr,
            )),
        )

    first_invariants = {node: invariant(first, first_adj, node)
                        for node in first.labels}
    second_invariants = {node: invariant(second, second_adj, node)
                         for node in second.labels}
    candidates = {
        node: tuple(other for other in second.labels
                    if second_invariants[other] == first_invariants[node])
        for node in first.labels
    }
    if any(not values for values in candidates.values()):
        return None

    mapping = {}
    used = set()

    def compatible(node, other):
        for old, image in mapping.items():
            first_edge = old in first_adj[node]
            second_edge = image in second_adj[other]
            if first_edge != second_edge:
                return False
            if first_edge:
                a_flags = first_adj[node][old]
                b_flags = second_adj[other][image]
                if a_flags != b_flags:
                    return False
        return True

    def search():
        if len(mapping) == len(first.labels):
            return dict(mapping)
        remaining = [node for node in first.labels if node not in mapping]
        node = min(remaining,
                   key=lambda item: sum(candidate not in used
                                        for candidate in candidates[item]))
        for other in candidates[node]:
            if other in used or not compatible(node, other):
                continue
            mapping[node] = other
            used.add(other)
            result = search()
            if result is not None:
                return result
            used.remove(other)
            del mapping[node]
        return None

    return search()


def directed_isomorphism(first, second):
    """Rooted-presentation isomorphism used only to expose the old category error."""
    if len(first.node) != len(second.node) or len(first.arcs) != len(second.arcs):
        return None
    candidates = {}
    for node, data in first.node.items():
        signature = (data["role"], data.get("label"),
                     len(first.inc[node]), len(first.out[node]))
        candidates[node] = tuple(
            other for other, other_data in second.node.items()
            if signature == (other_data["role"], other_data.get("label"),
                             len(second.inc[other]), len(second.out[other]))
        )
        if not candidates[node]:
            return None
    first_edges = set(first.arcs)
    second_edges = set(second.arcs)
    mapping = {}
    used = set()

    def compatible(node, other):
        for old, image in mapping.items():
            if ((node, old) in first_edges) != ((other, image) in second_edges):
                return False
            if ((old, node) in first_edges) != ((image, other) in second_edges):
                return False
        return True

    def search():
        if len(mapping) == len(first.node):
            return dict(mapping)
        remaining = [node for node in first.node if node not in mapping]
        node = min(remaining,
                   key=lambda item: sum(candidate not in used
                                        for candidate in candidates[item]))
        for other in candidates[node]:
            if other in used or not compatible(node, other):
                continue
            mapping[node] = other
            used.add(other)
            result = search()
            if result is not None:
                return result
            used.remove(other)
            del mapping[node]
        return None

    return search()


def mixed_automorphism_group(rooted_graph):
    base = root_suppressed_mixed(rooted_graph)
    group = []
    for perm in permutations(range(4)):
        if mixed_isomorphism(base, base.relabel(perm)) is not None:
            group.append(tuple(perm))
    group = tuple(sorted(group))
    require(IDENTITY in group, "mixed automorphism group lacks identity", group)
    require(all(compose(first, second) in group
                for first in group for second in group),
            "mixed automorphism candidates are not composition-closed", group)
    return group


def graph_binding(record, side, graph):
    literal = graph.literal()
    require(literal == record[f"{side}_literal_graph"],
            "literal graph binding mismatch", record.get("orbit_id"), side)
    require(canonical_json_hash(literal) == record[f"{side}_graph_hash"],
            "literal graph hash mismatch", record.get("orbit_id"), side)
    descriptor = compile_map(graph)
    require(sha256_bytes(repr(descriptor).encode()) == record[f"{side}_map_hash"],
            "map descriptor hash mismatch", record.get("orbit_id"), side)
    return descriptor


def double_coset(source_group, representative, target_group):
    return tuple(sorted({
        compose(source_auto, compose(representative, target_auto))
        for source_auto in source_group for target_auto in target_group
    }))


def reconstruct_record(record):
    representative = tuple(record["representative_permutation"])
    source_record = SOURCES[record["source_index"]]
    target_record = TARGETS[record["target_index"]]
    source_graph = source_record.graph
    target_base = target_record.graph
    target_displayed = target_base.relabel(representative)

    require(tuple(record["port_permutation"]) == representative,
            "port_permutation is not bound to representative_permutation",
            record["orbit_id"])
    require(source_record.core_id == record["source_core"],
            "source core mismatch", record["orbit_id"])
    require(source_record.repair_index == record["source_repair"],
            "source repair mismatch", record["orbit_id"])
    require(source_record.incoming_selected, "source incoming arm is not selected",
            record["orbit_id"])
    require(target_record.core_id == record["target_core"],
            "target core mismatch", record["orbit_id"])
    require(target_record.repair_index == record["target_repair"],
            "target repair mismatch", record["orbit_id"])
    require(target_record.incoming_selected, "target incoming arm is not selected",
            record["orbit_id"])
    require(record["source_incoming_role"] == "selected-port-0",
            "source incoming-role metadata mismatch", record["orbit_id"])
    require(record["target_incoming_role"] ==
            f"selected-port-{representative[0]}",
            "target incoming-role metadata mismatch", record["orbit_id"])
    source_descriptor = graph_binding(record, "source", source_graph)
    target_descriptor = graph_binding(record, "target", target_displayed)

    source_geometric_group = mixed_automorphism_group(source_graph)
    target_group = mixed_automorphism_group(target_base)
    frozen_source_group = tuple(sorted(
        tuple(auto) for auto in
        LOCK["source_automorphism_groups"][str(record["source_index"])]
    ))
    require(source_geometric_group == frozen_source_group,
            "source automorphism-group mismatch", record["orbit_id"])
    target_group_key = (
        "target_automorphism_group_theta0_repair1"
        if target_record.core_id == "theta0"
        else "target_automorphism_group_theta3_repair1"
    )
    frozen_target_group = tuple(sorted(tuple(auto) for auto in LOCK[target_group_key]))
    require(target_group == frozen_target_group,
            "target base automorphism-group mismatch", record["orbit_id"])
    displayed_target_group = mixed_automorphism_group(target_displayed)
    expected_displayed = tuple(sorted(
        compose(representative, compose(auto, inverse(representative)))
        for auto in target_group
    ))
    require(displayed_target_group == expected_displayed,
            "displayed target group is not the representative conjugate",
            record["orbit_id"])

    # The frozen relation census has two explicit frames.  H21 compares
    # relabellings of one complete factor; inverse-relation reduction permits
    # its source and target base groups to act on the two sides.  The lower-to-
    # rank24 census fixes its already-selected canonical source support and
    # reduces only the target completion.  This is a census convention, not a
    # claim that every lower source has a trivial geometric automorphism group.
    if record["family"] == "rank21_nonautomorphic_relabelling":
        source_action_group = source_geometric_group
    elif record["family"] == "lower_to_rank24":
        source_action_group = (IDENTITY,)
    else:
        raise CertificationError(
            f"unknown relation-census frame: {record['family']!r}"
        )

    orbit = double_coset(source_action_group, representative, target_group)
    recorded_members = tuple(sorted(tuple(member) for member in record["raw_members"]))
    require(orbit == recorded_members, "double-coset membership mismatch",
            record["orbit_id"], orbit, recorded_members)

    witnesses = set()
    for witness in record["raw_member_transports"]:
        source_auto = tuple(witness["source_automorphism"])
        target_auto = tuple(witness["target_automorphism"])
        member = tuple(witness["permutation"])
        require(source_auto in source_action_group,
                "witness source automorphism outside action group",
                record["orbit_id"], source_auto)
        require(target_auto in target_group,
                "witness target automorphism outside base target group",
                record["orbit_id"], target_auto)
        require(member == compose(source_auto,
                                  compose(representative, target_auto)),
                "raw-member witness equation mismatch", record["orbit_id"], member)
        witnesses.add(member)
    require(witnesses == set(orbit), "raw-member witnesses do not cover orbit",
            record["orbit_id"], witnesses, orbit)

    for member in orbit:
        verify_fourier_transport(
            target_base, target_base.relabel(member), member
        )

    coordinate_map = verify_fourier_transport(
        target_base, target_displayed, representative
    )
    require(mixed_isomorphism(root_suppressed_mixed(source_graph),
                              root_suppressed_mixed(target_displayed)) is None,
            "locked relation is mixed-graph isomorphic", record["orbit_id"])
    return {
        "source_descriptor": source_descriptor,
        "target_descriptor": target_descriptor,
        "source_group": source_action_group,
        "source_geometric_group": source_geometric_group,
        "target_group": target_group,
        "displayed_target_group": displayed_target_group,
        "double_coset": orbit,
        "coordinate_map": coordinate_map,
        "source_graph": source_graph,
        "target_base": target_base,
        "target_displayed": target_displayed,
    }


def sparse_outputs(descriptor):
    variable_count = 3 * descriptor.edge_class_count + descriptor.retic_count
    outputs = []
    for expression in descriptor.outputs:
        poly = defaultdict(int)
        for monomial, inheritance in expression:
            base = [0] * variable_count
            for class_index, character, exponent in monomial:
                base[3 * class_index + character - 1] += exponent
            for mask, coefficient in inheritance:
                powers = list(base)
                for index in range(descriptor.retic_count):
                    if (mask >> index) & 1:
                        powers[3 * descriptor.edge_class_count + index] += 1
                poly[tuple(powers)] += coefficient
        outputs.append({powers: coefficient for powers, coefficient in poly.items()
                        if coefficient})
    return tuple(outputs)


def polynomial_multiply(first, second):
    answer = defaultdict(Q)
    for first_power, first_coefficient in first.items():
        for second_power, second_coefficient in second.items():
            power = tuple(a + b for a, b in zip(first_power, second_power))
            answer[power] += first_coefficient * second_coefficient
    return {power: coefficient for power, coefficient in answer.items()
            if coefficient}


def polynomial_product(polys):
    if not polys:
        return {(): Q(1)}
    answer = polys[0]
    for poly in polys[1:]:
        answer = polynomial_multiply(answer, poly)
    return answer


def polynomial_linear_combination(terms):
    answer = defaultdict(Q)
    for scalar, poly in terms:
        for power, coefficient in poly.items():
            answer[power] += Q(scalar) * coefficient
    return {power: coefficient for power, coefficient in answer.items()
            if coefficient}


def pullback(descriptor, terms):
    outputs = sparse_outputs(descriptor)
    return polynomial_linear_combination(
        (term["coefficient"],
         polynomial_product([outputs[index]
                             for index in term["coordinate_indices"]]))
        for term in terms
    )


def polynomial_hash(poly):
    serial = [(list(power), str(coefficient))
              for power, coefficient in sorted(poly.items())]
    return sha256_bytes(json.dumps(serial, separators=(",", ":")).encode())


def _one(variable_count):
    return {(0,) * variable_count: Q(1)}


def _variable(variable_count, index):
    return {
        tuple(1 if column == index else 0
              for column in range(variable_count)): Q(1)
    }


def _add(*terms):
    return polynomial_linear_combination(terms)


def _mul(*polynomials):
    return polynomial_product(list(polynomials))


def verify_h21_target_upper_bound(descriptor, certificate):
    """Reconstruct the ten rational generators of the H21 projection.

    The eleven selected target coordinates are explicitly expressed through
    ten rational generators on the dense open set e2C*e2G*D*I != 0.  Every
    displayed identity is checked as an exact sparse-polynomial identity in
    the independently compiled target parameters.
    """
    require(descriptor.edge_class_count == 8 and descriptor.retic_count == 2,
            "H21 target descriptor has unexpected parameter census",
            descriptor.edge_class_count, descriptor.retic_count)
    expected_rows = (3, 12, 15, 20, 27, 39, 40, 48, 51, 60, 63)
    require(tuple(certificate["selected_output_rows"]) == expected_rows,
            "H21 rational factorization selected-observable set mismatch")
    require(tuple(certificate["selected_output_labels"]) == tuple(
        "".join(LETTER[value] for value in CH4[index]) for index in expected_rows
    ), "H21 selected-observable labels mismatch")

    outputs = sparse_outputs(descriptor)
    variable_count = 3 * descriptor.edge_class_count + descriptor.retic_count
    one = _one(variable_count)
    edge = [[_variable(variable_count, 3 * index + sector_index)
             for sector_index in range(3)] for index in range(8)]
    lambda0 = _variable(variable_count, 24)
    lambda1 = _variable(variable_count, 25)
    mu0 = _add((1, one), (-1, lambda0))
    mu1 = _add((1, one), (-1, lambda1))

    # These definitions are reconstructed from the target parameterization;
    # none is read from the rank certificate.
    a, b, c, d, f, h, i, j = [edge[index][2] for index in range(8)]
    e2c, e2g = edge[2][0], edge[2][1]
    generators = {
        "U": _mul(a, lambda0),
        "V": _mul(j, mu0),
        "Z": _mul(c, d, i),
        "D": _mul(d, i),
        "I": i,
        "A0": _mul(h, b, lambda1),
        "B0": _mul(h, f, mu1),
        "A": _mul(edge[2][0], edge[3][0], edge[6][0]),
        "B": _mul(edge[2][1], edge[3][1], edge[6][1]),
        # rho is the rational generator e2C/e2G; its numerator and
        # denominator are retained separately for exact cross-multiplication.
        "rho": (e2c, e2g),
    }
    expected_generator_names = (
        "U", "V", "Z", "D", "I", "A0", "B0", "A", "B", "rho"
    )
    require(tuple(generators) == expected_generator_names,
            "internal H21 generator census mismatch")
    require(tuple(certificate["rational_generators"]) == expected_generator_names,
            "frozen H21 rational-generator names mismatch")
    require(tuple(certificate["saturation_factors"]) ==
            ("e2C", "e2G", "D", "I"),
            "H21 saturation-factor list mismatch")
    require(certificate["factorization_reference"] ==
            "H21_TEN_GENERATOR_FORMULAS",
            "H21 factorization-reference mismatch")

    u, v, z = generators["U"], generators["V"], generators["Z"]
    dd, ii = generators["D"], generators["I"]
    a0, b0 = generators["A0"], generators["B0"]
    aa, bb = generators["A"], generators["B"]
    rhs3 = _mul(v, _add((1, _mul(dd, a0)), (1, _mul(ii, ii, b0))))
    rhs12 = _mul(u, _add((1, _mul(dd, a0)), (1, b0)))
    rhs51 = _mul(z, _add((1, a0), (1, _mul(dd, b0))))
    rhs63 = _mul(v, z, _add((1, _mul(ii, ii, a0)),
                            (1, _mul(dd, b0))))
    identities = (
        _add((1, _mul(ii, outputs[3])), (-1, _mul(ii, u)), (-1, rhs3)),
        _add((1, outputs[12]), (-1, rhs12), (-1, _mul(v, ii))),
        _add((1, outputs[15]), (-1, _mul(dd, a0)), (-1, b0)),
        _add((1, outputs[20]), (-1, aa)),
        _add((1, _mul(e2g, outputs[27])), (-1, _mul(e2g, b0, aa)),
             (-1, _mul(a0, e2c, bb))),
        _add((1, _mul(e2c, outputs[39])), (-1, _mul(e2c, b0, bb)),
             (-1, _mul(a0, e2g, aa))),
        _add((1, outputs[40]), (-1, bb)),
        _add((1, _mul(ii, outputs[48])),
             (-1, _mul(ii, u, outputs[51])), (-1, _mul(v, z))),
        _add((1, _mul(dd, outputs[51])), (-1, rhs51)),
        _add((1, outputs[60]), (-1, z)),
        _add((1, _mul(dd, ii, outputs[63])),
             (-1, _mul(dd, ii, u, z)), (-1, rhs63)),
    )
    require(all(not identity for identity in identities),
            "H21 rational-generator identity failed")
    return {
        "mechanism": "ten-rational-generator-cross-multiplication",
        "generator_count": len(generators),
        "generators": list(generators),
        "selected_output_rows": list(expected_rows),
        "identity_count": len(identities),
        "saturation_factors": list(certificate["saturation_factors"]),
    }


def compress_sunlet_projection(descriptor, omitted_port):
    require(0 <= omitted_port < 4, "invalid omitted port", omitted_port)
    rows = [index for index, chars in enumerate(CH4)
            if chars[omitted_port] == 0]
    outputs = sparse_outputs(descriptor)
    signatures = {}
    for class_index in range(descriptor.edge_class_count):
        occurrence = []
        for output_index in rows:
            for exponent in sorted(outputs[output_index]):
                occurrence.extend(
                    exponent[3 * class_index:3 * class_index + 3]
                )
        signatures[class_index] = tuple(occurrence)
    groups = defaultdict(list)
    for class_index, signature in signatures.items():
        groups[signature].append(class_index)
    active = sorted(
        (group for signature, group in groups.items() if any(signature)),
        key=lambda group: min(group),
    )
    invisible = [group for signature, group in groups.items()
                 if not any(signature)]
    require(len(active) == 4,
            "sunlet marginal does not reconstruct four active edge classes",
            omitted_port, active)
    retic_variables = []
    for index in range(descriptor.retic_count):
        column = 3 * descriptor.edge_class_count + index
        if any(any(exponent[column] for exponent in outputs[output_index])
               for output_index in rows):
            retic_variables.append(index)
    require(len(retic_variables) == 1,
            "sunlet marginal does not reconstruct one inheritance variable",
            omitted_port, retic_variables)

    compressed = []
    for output_index in rows:
        polynomial = defaultdict(Q)
        for exponent, coefficient in outputs[output_index].items():
            for group in invisible:
                for class_index in group:
                    require(exponent[3 * class_index:3 * class_index + 3] ==
                            (0, 0, 0),
                            "invisible sunlet edge class remains active",
                            output_index, class_index)
            new_exponent = [0] * 13
            for active_index, group in enumerate(active):
                values = [exponent[3 * class_index:3 * class_index + 3]
                          for class_index in group]
                require(all(value == values[0] for value in values),
                        "collapsed sunlet edge signatures disagree",
                        output_index, group)
                new_exponent[3 * active_index:3 * active_index + 3] = values[0]
            for index in range(descriptor.retic_count):
                old_column = 3 * descriptor.edge_class_count + index
                if index == retic_variables[0]:
                    new_exponent[12] = exponent[old_column]
                else:
                    require(exponent[old_column] == 0,
                            "invisible sunlet inheritance variable remains active",
                            output_index, index)
            polynomial[tuple(new_exponent)] += coefficient
        compressed.append({exponent: coefficient
                           for exponent, coefficient in polynomial.items()
                           if coefficient})
    return tuple(compressed), rows, active, invisible, retic_variables[0]


def canonical_sunlet_map(edge_map, inheritance_flip, port_permutation):
    """Construct an ordinary three-sunlet through its 12 generators."""
    variable_count = 13
    one = _one(variable_count)
    edge = [[_variable(variable_count, 3 * index + sector_index)
             for sector_index in range(3)] for index in range(4)]
    inheritance = _variable(variable_count, 12)
    complement = _add((1, one), (-1, inheritance))
    edge_a, edge_b, edge_u, edge_v = [edge[index] for index in edge_map]
    if not inheritance_flip:
        aa = [_mul(inheritance, edge_a[index]) for index in range(3)]
        bb = [_mul(complement, edge_b[index]) for index in range(3)]
    else:
        aa = [_mul(complement, edge_a[index]) for index in range(3)]
        bb = [_mul(inheritance, edge_b[index]) for index in range(3)]
    uu, vv = edge_u, edge_v
    canonical = []
    dependencies = []
    for x_value, y_value, z_value in CH3:
        if x_value == y_value == z_value == 0:
            polynomial, deps = one, set()
        elif x_value == 0:
            polynomial = _add(
                (1, aa[y_value - 1]),
                (1, _mul(vv[y_value - 1], bb[y_value - 1])),
            )
            deps = {("A", y_value), ("V", y_value), ("B", y_value)}
        elif y_value == 0:
            polynomial = _mul(
                uu[x_value - 1],
                _add((1, _mul(vv[x_value - 1], aa[x_value - 1])),
                     (1, bb[x_value - 1])),
            )
            deps = {("U", x_value), ("V", x_value),
                    ("A", x_value), ("B", x_value)}
        elif z_value == 0:
            polynomial = _mul(uu[x_value - 1], vv[x_value - 1])
            deps = {("U", x_value), ("V", x_value)}
        else:
            polynomial = _mul(
                uu[x_value - 1],
                _add((1, _mul(vv[x_value - 1], aa[z_value - 1])),
                     (1, _mul(vv[y_value - 1], bb[z_value - 1]))),
            )
            deps = {("U", x_value), ("V", x_value), ("A", z_value),
                    ("V", y_value), ("B", z_value)}
        canonical.append(polynomial)
        dependencies.append(deps)
    index = {assignment: position for position, assignment in enumerate(CH3)}
    output_permutation = [
        index[tuple(assignment[port_permutation[position]]
                    for position in range(3))]
        for assignment in CH3
    ]
    return (
        tuple(canonical[output_permutation[position]] for position in range(16)),
        tuple(dependencies[output_permutation[position]]
              for position in range(16)),
    )


def verify_sunlet_target_upper_bound(descriptor, certificate):
    compressed, marginal_rows, active, invisible, reticulation = (
        compress_sunlet_projection(descriptor, certificate["omitted_port"])
    )
    found = None
    for edge_map in permutations(range(4)):
        for inheritance_flip in (False, True):
            for port_permutation in permutations(range(3)):
                canonical, dependencies = canonical_sunlet_map(
                    edge_map, inheritance_flip, port_permutation
                )
                if compressed == canonical:
                    found = (edge_map, inheritance_flip,
                             port_permutation, dependencies)
                    break
            if found is not None:
                break
        if found is not None:
            break
    require(found is not None,
            "target marginal did not match any ordinary-sunlet parameterization",
            certificate["orbit_id"])

    selected_rows = tuple(certificate["selected_output_rows"])
    require(len(selected_rows) == len(set(selected_rows)),
            "duplicate selected observable", certificate["orbit_id"])
    require(all(row in marginal_rows and row != 0 for row in selected_rows),
            "selected observable lies outside nonconstant sunlet marginal",
            certificate["orbit_id"], selected_rows)
    require(tuple(certificate["selected_output_labels"]) == tuple(
        "".join(LETTER[value] for value in CH4[index]) for index in selected_rows
    ), "sunlet selected-observable labels mismatch", certificate["orbit_id"])
    row_map = {row: index for index, row in enumerate(marginal_rows)}
    selected_three_rows = [row_map[row] for row in selected_rows]
    used = set().union(*(found[3][index] for index in selected_three_rows))
    all_generators = tuple(
        (prefix, character)
        for character in range(1, 4)
        for prefix in ("A", "B", "U", "V")
    )
    generator_names = tuple(
        f"{prefix}_{LETTER[character]}"
        for prefix, character in all_generators if (prefix, character) in used
    )
    absent_names = tuple(
        f"{prefix}_{LETTER[character]}"
        for prefix, character in all_generators if (prefix, character) not in used
    )
    require(tuple(certificate["rational_generators"]) == generator_names,
            "sunlet rational-generator names mismatch",
            certificate["orbit_id"], generator_names)
    require(tuple(certificate.get("absent_generators", ())) == absent_names,
            "sunlet absent-generator names mismatch",
            certificate["orbit_id"], absent_names)
    require(certificate["factorization_reference"] ==
            "SUNLET_TWELVE_GENERATOR_FORMULAS",
            "sunlet factorization-reference mismatch", certificate["orbit_id"])
    return {
        "mechanism": "ordinary-sunlet-generator-compression",
        "generator_count": len(used),
        "generators": list(generator_names),
        "absent_generators": list(absent_names),
        "selected_output_rows": list(selected_rows),
        "omitted_port": certificate["omitted_port"],
        "active_edge_groups": active,
        "invisible_edge_groups": invisible,
        "reticulation_variable": reticulation,
        "canonical_edge_permutation": list(found[0]),
        "canonical_inheritance_flip": found[1],
        "canonical_port_permutation": list(found[2]),
    }


def exact_point(record, side):
    point = record[f"{side}_exact_rank_point"]
    edges = tuple(tuple(Q(value) for value in row) for row in point["edges"])
    inheritance = tuple(Q(value) for value in point["inheritance"])
    return edges, inheritance


def physical_margin(point):
    edges, inheritance = point
    margins = []
    for c_value, g_value, t_value in edges:
        margins.extend((
            c_value, g_value, t_value,
            1 - c_value, 1 - g_value, 1 - t_value,
            1 + c_value - g_value - t_value,
            1 - c_value + g_value - t_value,
            1 - c_value - g_value + t_value,
        ))
    for value in inheritance:
        margins.extend((value, 1 - value))
    return min(margins)


def evaluate_map(descriptor, edge_values, inheritance_values):
    outputs = []
    for expression in descriptor.outputs:
        answer = Q(0)
        for monomial, inheritance in expression:
            monomial_value = Q(1)
            for class_index, character, exponent in monomial:
                monomial_value *= edge_values[class_index][character - 1] ** exponent
            inheritance_value = Q(0)
            for mask, coefficient in inheritance:
                term = Q(coefficient)
                for index, value in enumerate(inheritance_values):
                    if (mask >> index) & 1:
                        term *= value
                inheritance_value += term
            answer += monomial_value * inheritance_value
        outputs.append(answer)
    return tuple(outputs)


def evaluate_coordinate_polynomial(q_values, terms):
    answer = Q(0)
    for term in terms:
        monomial = Q(term["coefficient"])
        for index in term["coordinate_indices"]:
            monomial *= q_values[index]
        answer += monomial
    return answer


def jacobian(descriptor, edge_values, inheritance_values):
    parameter_count = 3 * descriptor.edge_class_count + descriptor.retic_count
    rows = []
    for expression in descriptor.outputs:
        row = [Q(0)] * parameter_count
        for monomial, inheritance in expression:
            monomial_value = Q(1)
            for class_index, character, exponent in monomial:
                monomial_value *= edge_values[class_index][character - 1] ** exponent
            inheritance_value = Q(0)
            inheritance_derivative = [Q(0)] * descriptor.retic_count
            for mask, coefficient in inheritance:
                term = Q(coefficient)
                for index, value in enumerate(inheritance_values):
                    if (mask >> index) & 1:
                        term *= value
                inheritance_value += term
                for index, value in enumerate(inheritance_values):
                    if (mask >> index) & 1:
                        inheritance_derivative[index] += term / value
            for class_index, character, exponent in monomial:
                column = 3 * class_index + character - 1
                row[column] += (monomial_value * inheritance_value * exponent /
                                edge_values[class_index][character - 1])
            for index, value in enumerate(inheritance_derivative):
                row[3 * descriptor.edge_class_count + index] += monomial_value * value
        rows.append(row)
    return rows


def determinant(matrix):
    work = [list(map(Q, row)) for row in matrix]
    size = len(work)
    answer = Q(1)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            scale = work[row][column] / pivot_value
            for index in range(column + 1, size):
                work[row][index] -= scale * work[column][index]
    return answer


def verify_rank_minor(record, certificate, side, descriptor):
    cert = certificate[f"{side}_rank_certificate"]
    selected_rows = tuple(certificate["selected_output_rows"])
    rows = tuple(cert["output_rows"])
    columns = tuple(cert["parameter_columns"])
    claimed_rank = cert["rank"]
    require(isinstance(claimed_rank, int) and claimed_rank > 0,
            "rank claim is not a positive integer", certificate["orbit_id"], side)
    require(len(rows) == len(set(rows)) and len(columns) == len(set(columns)),
            "rank minor has duplicate rows or columns",
            certificate["orbit_id"], side)
    require(claimed_rank == len(rows) == len(columns),
            "rank claim is not bound to square minor size",
            certificate["orbit_id"], side, claimed_rank, len(rows), len(columns))
    require(all(row in selected_rows for row in rows),
            "rank minor row lies outside selected observable set",
            certificate["orbit_id"], side, rows, selected_rows)
    require(tuple(cert["output_labels"]) == tuple(
        "".join(LETTER[value] for value in CH4[index]) for index in rows
    ), "rank-minor output labels mismatch", certificate["orbit_id"], side)
    parameter_count = 3 * descriptor.edge_class_count + descriptor.retic_count
    require(all(0 <= row < len(CH4) for row in rows),
            "rank-minor output row out of range", certificate["orbit_id"], side)
    require(all(0 <= column < parameter_count for column in columns),
            "rank-minor parameter column out of range",
            certificate["orbit_id"], side, parameter_count)
    point = exact_point(record, side)
    margin = physical_margin(point)
    require(margin > 0, "rank point is outside strict principal domain",
            certificate["orbit_id"], side, margin)
    require(str(margin) == certificate[f"{side}_physical_min_margin"],
            "stored physical margin mismatch", certificate["orbit_id"], side)
    matrix = jacobian(descriptor, *point)
    minor = [[matrix[row][column] for column in columns] for row in rows]
    value = determinant(minor)
    require(value != 0, "certified Jacobian minor vanishes",
            certificate["orbit_id"], side)
    require(str(value) == cert["determinant"],
            "certified Jacobian determinant mismatch",
            certificate["orbit_id"], side, str(value), cert["determinant"])
    return {
        "rank": claimed_rank,
        "minor_size": len(rows),
        "output_rows": list(rows),
        "parameter_columns": list(columns),
        "determinant": str(value),
        "physical_margin": str(margin),
    }


def verify_rank_obstruction_certificate(certificate, reconstructions):
    orbit_id = certificate["orbit_id"]
    require(orbit_id in reconstructions and orbit_id in RECORDS,
            "rank certificate names an unknown orbit", orbit_id)
    record = RECORDS[orbit_id]
    reconstruction = reconstructions[orbit_id]
    require(certificate["source_map_hash"] == record["source_map_hash"],
            "rank certificate source-map binding mismatch", orbit_id)
    require(certificate["target_map_hash"] == record["target_map_hash"],
            "rank certificate target-map binding mismatch", orbit_id)
    source_minor = verify_rank_minor(
        record, certificate, "source", reconstruction["source_descriptor"]
    )
    target_minor = verify_rank_minor(
        record, certificate, "target", reconstruction["target_descriptor"]
    )
    if certificate["obstruction_type"] == "rational-projection-factorization":
        require(orbit_id == "H21-02",
                "H21 factorization attached to wrong orbit", orbit_id)
        upper_bound = verify_h21_target_upper_bound(
            reconstruction["target_descriptor"], certificate
        )
    elif certificate["obstruction_type"] in {
            "ordinary-sunlet-absorption-rank",
            "ordinary-sunlet-selected-ten-generator-rank"}:
        upper_bound = verify_sunlet_target_upper_bound(
            reconstruction["target_descriptor"], certificate
        )
    else:
        raise CertificationError(
            f"unknown target upper-bound mechanism: {certificate['obstruction_type']!r}"
        )
    generator_count = upper_bound["generator_count"]
    require(certificate["target_dimension_upper_bound"] == generator_count,
            "claimed target upper bound differs from reconstructed generator count",
            orbit_id, certificate["target_dimension_upper_bound"], generator_count)
    require(target_minor["rank"] == generator_count,
            "target minor rank differs from reconstructed upper bound",
            orbit_id, target_minor["rank"], generator_count)
    require(source_minor["rank"] > generator_count,
            "source minor does not exceed reconstructed target upper bound",
            orbit_id, source_minor["rank"], generator_count)
    return {
        "orbit_id": orbit_id,
        "source_minor": source_minor,
        "target_minor": target_minor,
        "target_upper_bound": upper_bound,
        "strict_rank_obstruction": True,
    }


def verify_certificate_replay(reconstructions):
    prelock_certificates = load_bound_json(
        "k3p_prelock_source5_quartic.json"
    )["records"]
    require(len(prelock_certificates) ==
            len(LOCK["prelock_exact_separations"]) == 2,
            "prelock sink-swap certificate census mismatch")
    for certificate, lock_record in zip(
            prelock_certificates, LOCK["prelock_exact_separations"]):
        perm = tuple(certificate["permutation"])
        require(perm == tuple(lock_record["permutation"]),
                "prelock permutation mismatch", perm)
        source_graph = SOURCES[lock_record["source_index"]].graph
        target_graph = TARGETS[lock_record["target_index"]].graph.relabel(perm)
        source_descriptor = graph_binding(lock_record, "source", source_graph)
        target_descriptor = graph_binding(lock_record, "target", target_graph)
        require(mixed_isomorphism(root_suppressed_mixed(source_graph),
                                  root_suppressed_mixed(target_graph)) is None,
                "prelock relation is mixed-graph isomorphic", perm)
        require(not pullback(target_descriptor, certificate["terms"]),
                "prelock target polynomial pullback is nonzero", perm)
        source_pullback = pullback(source_descriptor, certificate["terms"])
        require(polynomial_hash(source_pullback) ==
                certificate["source_pullback_sha256"],
                "prelock source pullback hash mismatch", perm)
        point = certificate["source_exact_point"]
        exact = (tuple(tuple(Q(value) for value in row) for row in point["edges"]),
                 tuple(Q(value) for value in point["inheritance"]))
        q_values = evaluate_map(source_descriptor, *exact)
        evaluation = evaluate_coordinate_polynomial(q_values, certificate["terms"])
        require(evaluation == Q(certificate["source_evaluation"]) and
                evaluation != 0, "prelock source evaluation mismatch", perm)
        require(physical_margin(exact) > 0,
                "prelock source point is outside strict principal domain", perm)

    polynomial_files = (
        "k3p_h14_marginal_orbit_certificates.json",
        "k3p_remaining_quartic_separators.json",
    )
    covered = set()
    for filename in polynomial_files:
        certificates = load_bound_json(filename)["records"]
        for certificate in certificates:
            orbit_id = certificate["orbit_id"]
            require(orbit_id not in covered,
                    "orbit has more than one separation certificate", orbit_id)
            covered.add(orbit_id)
            record = RECORDS[orbit_id]
            reconstruction = reconstructions[orbit_id]
            source_descriptor = reconstruction["source_descriptor"]
            target_descriptor = reconstruction["target_descriptor"]
            require(not pullback(target_descriptor, certificate["terms"]),
                    "target polynomial pullback is nonzero", orbit_id)
            source_pullback = pullback(source_descriptor, certificate["terms"])
            require(polynomial_hash(source_pullback) ==
                    certificate["source_pullback_sha256"],
                    "source polynomial pullback hash mismatch", orbit_id)
            point = exact_point(record, "source")
            require(physical_margin(point) > 0,
                    "polynomial witness point outside strict principal domain",
                    orbit_id)
            q_values = evaluate_map(source_descriptor, *point)
            evaluation = evaluate_coordinate_polynomial(q_values, certificate["terms"])
            require(evaluation == Q(certificate["source_evaluation"]) and
                    evaluation != 0,
                    "source polynomial evaluation mismatch", orbit_id)

    rank_certificates = load_bound_json(
        "k3p_directed_rank_obstructions.json"
    )["records"]
    rank_evidence = []
    for certificate in rank_certificates:
        orbit_id = certificate["orbit_id"]
        require(orbit_id not in covered,
                "orbit has more than one separation certificate", orbit_id)
        covered.add(orbit_id)
        rank_evidence.append(
            verify_rank_obstruction_certificate(certificate, reconstructions)
        )
    require(len(rank_evidence) == 5,
            "directed-rank certificate census mismatch", len(rank_evidence))
    require(covered == set(RECORDS),
            "separation certificates do not cover exactly fourteen orbits",
            covered, set(RECORDS))
    return rank_evidence


def h21_diagnostics(reconstruction):
    record = RECORDS["H21-01"]
    source_graph = reconstruction["source_graph"]
    target_displayed = reconstruction["target_displayed"]
    base_auto = (2, 1, 0, 3)
    representative = tuple(record["representative_permutation"])
    displayed_auto = compose(representative,
                             compose(base_auto, inverse(representative)))

    require(directed_isomorphism(source_graph,
                                 source_graph.relabel(base_auto)) is None,
            "historical rooted category unexpectedly accepts H21 symmetry")
    require(mixed_isomorphism(root_suppressed_mixed(source_graph),
                              root_suppressed_mixed(
                                  source_graph.relabel(base_auto))) is not None,
            "correct mixed category rejects H21 symmetry")
    require(base_auto not in reconstruction["displayed_target_group"],
            "base target automorphism incorrectly used in displayed frame")
    require(displayed_auto in reconstruction["displayed_target_group"],
            "conjugated target automorphism missing from displayed frame")

    source_mixed = root_suppressed_mixed(source_graph)
    target_mixed = root_suppressed_mixed(target_displayed)

    def edge_rows(mixed):
        rows = []
        for endpoints, heads in sorted(mixed.edges.items(), key=lambda item: repr(item[0])):
            vertices = tuple(sorted((repr(node) for node in endpoints)))
            rows.append({
                "endpoints": vertices,
                "arrowheads": tuple(sorted(repr(node) for node in heads)),
            })
        return rows

    coordinate_map = reconstruction["coordinate_map"]
    return {
        "orbit_id": "H21-01",
        "representative": representative,
        "source_base_automorphism_group": reconstruction["source_group"],
        "target_base_automorphism_group": reconstruction["target_group"],
        "target_displayed_automorphism_group": reconstruction["displayed_target_group"],
        "base_to_displayed_target_conjugate": displayed_auto,
        "double_coset": reconstruction["double_coset"],
        "coordinate_transport": coordinate_map,
        "coordinate_transport_named": tuple(
            ("".join(LETTER[value] for value in CH4[index]),
             "".join(LETTER[value] for value in CH4[coordinate_map[index]]))
            for index in range(len(CH4))
        ),
        "source_mixed_edges": edge_rows(source_mixed),
        "target_displayed_mixed_edges": edge_rows(target_mixed),
        "historical_rooted_check_rejects_source_02_swap": True,
        "correct_mixed_check_accepts_source_02_swap": True,
    }


def verify_all(run_certificates=True):
    require(run_certificates is True,
            "full verifier cannot skip algebraic certificates")
    require(len(SOURCES) == 6, "source support census mismatch", len(SOURCES))
    require(len(target_completions(4, True)) == 831,
            "selected-incoming target completion census mismatch")
    require(len(target_completions(4, False)) == 1983,
            "dummy-incoming target completion census mismatch")
    require(len(TARGETS) == 2814, "combined target completion census mismatch")
    require(len(RECORDS) == 14, "canonical orbit census mismatch", len(RECORDS))
    require(sum(len(record["raw_members"]) for record in RECORDS.values()) == 38,
            "raw orbit-member census mismatch")
    require(len(LOCK["prelock_exact_separations"]) == 2,
            "prelock separation census mismatch")

    reconstructions = {}
    for orbit_id, record in RECORDS.items():
        reconstructions[orbit_id] = reconstruct_record(record)
        print("PASS", orbit_id, "graph/map binding, mixed groups, double coset, Fourier transport")

    # The 22 H21 raw nonisomorphic relations are six complete double cosets.
    h21 = reconstructions["H21-01"]
    h_group = h21["source_group"]
    remaining = set(permutations(range(4)))
    all_cosets = []
    while remaining:
        representative = min(remaining)
        coset = set(double_coset(h_group, representative, h_group))
        all_cosets.append(tuple(sorted(coset)))
        remaining -= coset
    recorded_h21 = {
        tuple(sorted(tuple(member) for member in record["raw_members"]))
        for orbit_id, record in RECORDS.items() if orbit_id.startswith("H21-")
    }
    omitted = set(all_cosets) - recorded_h21
    require(len(all_cosets) == 7 and len(recorded_h21) == 6 and
            len(omitted) == 1,
            "H21 double-coset partition census mismatch")
    require(omitted == {tuple(sorted(h_group))},
            "omitted H21 coset is not exactly the isomorphic class", omitted)

    diagnostics = h21_diagnostics(h21)
    if run_certificates:
        rank_evidence = verify_certificate_replay(reconstructions)
        diagnostics["rank_upper_bounds"] = rank_evidence
        print("PASS two sink-swap and fourteen exact separation certificate replays")
        print("PASS five independently reconstructed directed-rank upper bounds")
    print("CLEANROOM_K3P_H21_TRANSPORT_AND_FOURTEEN_ORBITS_PASS")
    return diagnostics


if __name__ == "__main__":
    verify_all(run_certificates=True)
