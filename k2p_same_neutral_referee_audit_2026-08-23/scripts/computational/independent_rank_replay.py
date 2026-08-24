#!/usr/bin/env python3
"""Replay one load-bearing raw4 rank comparison through an independent map engine.

This file contains its own general-k Fourier/Jacobian implementation and does
not import the atlas or primary rank verifier.  Primitive source/target graphs
are rebuilt from literal edge lists and raw ID 97 is reconstructed directly.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path

import networkx as nx


CORES = {
    "cycle": ((("S", "X"), ("S", "X")), ("X",), ("X",), ((0,), (1,))),
    "theta0": ((("S", "U"), ("S", "V"), ("U", "X"), ("V", "X"), ("U", "V")), ("V", "X"), ("X",), ((2, 3), (3, 4))),
    "theta1": ((("S", "U"), ("S", "X"), ("V", "X"), ("U", "V"), ("U", "V")), ("V", "X"), ("X",), ((2, 3), (2, 4))),
    "theta2": ((("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1")), ("X0", "X1"), ("X0", "X1"), ((2, 3), (2, 5), (3, 4), (4, 5))),
    "theta3": ((("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V")), ("X0", "X1"), ("X0", "X1"), ((2,), (4,))),
}


def require(ok, code, detail=None):
    if not ok:
        raise RuntimeError(code if detail is None else f"{code}: {detail}")


def orbit_coordinates(k):
    answer = set()
    for prefix in itertools.product(range(4), repeat=k - 1):
        last = 0
        for value in prefix:
            last ^= value
        chars = prefix + (last,)
        swapped = tuple(3 if x == 1 else (1 if x == 3 else x) for x in chars)
        answer.add(min(chars, swapped))
    return tuple(sorted(answer))


def sector(mask, chars):
    value = 0
    for label, character in enumerate(chars):
        if mask & (1 << label):
            value ^= character
    return 0 if value == 0 else (2 if value == 2 else 1)


def inheritance_polynomial(bits):
    polynomial = {0: 1}
    for index, bit in enumerate(bits):
        updated = defaultdict(int)
        for mask, coefficient in polynomial.items():
            if bit:
                updated[mask | (1 << index)] += coefficient
            else:
                updated[mask] += coefficient
                updated[mask | (1 << index)] -= coefficient
        polynomial = {mask: coefficient for mask, coefficient in updated.items() if coefficient}
    return tuple(sorted(polynomial.items()))


def descendant_masks(graph, kept):
    tree = nx.DiGraph()
    tree.add_nodes_from(graph.nodes())
    tree.add_edges_from(kept)
    masks = {}
    for node in reversed(tuple(nx.topological_sort(tree))):
        label = graph.nodes[node].get("label")
        value = (1 << label) if isinstance(label, int) else 0
        for child in tree.successors(node):
            value |= masks[child]
        masks[node] = value
    return {(tail, head): masks[head] for tail, head in kept}


@dataclass(frozen=True)
class IndependentMap:
    retic_order: tuple
    parent_orders: tuple
    edge_signatures: tuple
    outputs: tuple

    @property
    def edge_class_count(self):
        return len(self.edge_signatures)


def formal_variant(graph, retic_order, parent_orders):
    coords = orbit_coordinates(len([1 for _, d in graph.nodes(data=True) if isinstance(d.get("label"), int)]))
    all_edges = tuple(graph.edges())
    arms = {(u, v) for u, v in all_edges if graph.nodes[v]["role"] == "leaf" and isinstance(graph.nodes[v].get("label"), int)}
    switches = []
    for bits in itertools.product((0, 1), repeat=len(retic_order)):
        removed = set()
        for index, reticulation in enumerate(retic_order):
            kept_parent = parent_orders[index][bits[index]]
            for parent in graph.predecessors(reticulation):
                if parent != kept_parent:
                    removed.add((parent, reticulation))
        kept = tuple(edge for edge in all_edges if edge not in removed)
        switches.append((bits, kept, descendant_masks(graph, kept)))
    signatures = {}
    for edge in all_edges:
        if edge in arms:
            continue
        signature = []
        for _, kept, masks in switches:
            signature.extend((0,) * len(coords) if edge not in kept else (sector(masks[edge], chars) for chars in coords))
        if any(signature):
            signatures[edge] = tuple(signature)
    active = tuple(sorted(set(signatures.values())))
    edge_class = {edge: active.index(signature) for edge, signature in signatures.items()}
    outputs = []
    for chars in coords:
        grouped = defaultdict(lambda: defaultdict(int))
        for bits, kept, masks in switches:
            exponents = Counter()
            for edge in kept:
                if edge not in edge_class:
                    continue
                sec = sector(masks[edge], chars)
                if sec:
                    exponents[(edge_class[edge], sec)] += 1
            monomial = tuple(sorted((index, sec, exponent) for (index, sec), exponent in exponents.items()))
            for mask, coefficient in inheritance_polynomial(bits):
                grouped[monomial][mask] += coefficient
        expression = []
        for monomial, polynomial in grouped.items():
            clean = tuple(sorted((mask, coefficient) for mask, coefficient in polynomial.items() if coefficient))
            if clean:
                expression.append((monomial, clean))
        outputs.append(tuple(sorted(expression)))
    return IndependentMap(tuple(retic_order), tuple(parent_orders), active, tuple(outputs))


def canonical_formal_map(graph):
    retics = tuple(sorted((node for node, data in graph.nodes(data=True) if data["role"] == "retic"), key=repr))
    variants = []
    for order in itertools.permutations(retics):
        parents = tuple(tuple(sorted(graph.predecessors(retic), key=repr)) for retic in order)
        for flips in itertools.product((0, 1), repeat=len(order)):
            parent_orders = tuple((pair[flip], pair[1 - flip]) for pair, flip in zip(parents, flips))
            variants.append(formal_variant(graph, order, parent_orders))
    return min(variants, key=lambda model: (len(model.retic_order), model.edge_class_count, model.outputs, model.edge_signatures))


def evaluate_polynomial(polynomial, lambdas):
    total = F(0)
    for mask, coefficient in polynomial:
        term = F(coefficient)
        for index, value in enumerate(lambdas):
            if mask & (1 << index):
                term *= value
        total += term
    return total


def jacobian(model, edge_pairs, lambdas):
    width = 2 * model.edge_class_count + len(lambdas)
    matrix = []
    for expression in model.outputs:
        row = [F(0) for _ in range(width)]
        for monomial, polynomial in expression:
            edge_value = F(1); powers = {}
            for class_index, sec, exponent in monomial:
                column = 2 * class_index + sec - 1
                powers[column] = exponent
                edge_value *= edge_pairs[class_index][sec - 1] ** exponent
            poly_value = evaluate_polynomial(polynomial, lambdas)
            for column, exponent in powers.items():
                row[column] += edge_value * poly_value * exponent / edge_pairs[column // 2][column % 2]
            for lambda_index, inheritance in enumerate(lambdas):
                derivative = F(0)
                for mask, coefficient in polynomial:
                    if mask & (1 << lambda_index):
                        term = F(coefficient)
                        for index, value in enumerate(lambdas):
                            if mask & (1 << index):
                                term *= value
                        derivative += term / inheritance
                row[2 * model.edge_class_count + lambda_index] += edge_value * derivative
        matrix.append(row)
    return matrix


def rank_pivots(matrix):
    work = [row[:] for row in matrix]; row_ids = list(range(len(work)))
    rows = []; columns = []; rank = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(rank, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        row_ids[rank], row_ids[pivot] = row_ids[pivot], row_ids[rank]
        value = work[rank][column]
        work[rank] = [x / value for x in work[rank]]
        for i in range(len(work)):
            if i != rank and work[i][column]:
                factor = work[i][column]
                work[i] = [a - factor * b for a, b in zip(work[i], work[rank])]
        rows.append(row_ids[rank]); columns.append(column); rank += 1
        if rank == len(work):
            break
    return rank, tuple(rows), tuple(columns)


def determinant(matrix):
    work = [list(row) for row in matrix]; answer = F(1)
    for column in range(len(work)):
        pivot = next((i for i in range(column, len(work)) if work[i][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]; answer = -answer
        value = work[column][column]; answer *= value
        for i in range(column + 1, len(work)):
            if work[i][column]:
                factor = work[i][column] / value
                for j in range(column + 1, len(work)):
                    work[i][j] -= factor * work[column][j]
    return answer


def weak_compositions(total, bins):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def targets(k, incoming_selected):
    rows = []
    for core, (arcs, retics, sinks, repairs) in CORES.items():
        outgoing = k - 1 if incoming_selected else k
        for mask in range(1 << len(sinks)):
            ordinary = outgoing - mask.bit_count()
            if ordinary < 0:
                continue
            for counts in weak_compositions(ordinary, len(arcs)):
                start = 1 if incoming_selected else 0
                labels = iter(range(start, k))
                selected_words = tuple(tuple(next(labels) for _ in range(count)) for count in counts)
                repair_rows = ((None, ()),) if core == "cycle" else tuple(enumerate(repairs))
                for repair_index, repair in repair_rows:
                    words = [list(word) for word in selected_words]
                    for arc_index in repair:
                        if not words[arc_index]:
                            words[arc_index].append(f"D_REPAIR_{repair_index}_{arc_index}")
                    used = [x for word in selected_words for x in word]
                    next_label = max(used, default=start - 1) + 1
                    sink_labels = []
                    for sink_index in range(len(sinks)):
                        if mask & (1 << sink_index):
                            sink_labels.append(next_label); next_label += 1
                        else:
                            sink_labels.append(f"D_SINK_{sink_index}")
                    rows.append((core, tuple(tuple(word) for word in words), tuple(sink_labels), 0 if incoming_selected else "INCOMING"))
    return rows


def sources():
    rows = []
    for core in ("theta0", "theta1", "theta3"):
        arcs, retics, sinks, repairs = CORES[core]
        for repair in repairs:
            words = [[] for _ in arcs]
            next_label = 1
            for arc_index in repair:
                words[arc_index].append(next_label); next_label += 1
            rows.append((core, tuple(tuple(word) for word in words), tuple(range(next_label, next_label + len(sinks))), 0))
    return rows


def build_graph(record):
    core, words, sink_labels, incoming_label = record
    arcs, retics, sinks, _ = CORES[core]
    graph = nx.DiGraph(name=core)
    for node in {x for edge in arcs for x in edge}:
        graph.add_node(("core", node), role="retic" if node in retics else "tree", label=None)
    graph.add_node(("root",), role="root", label=None)
    graph.add_node(("leaf", "INCOMING"), role="leaf", label=incoming_label if isinstance(incoming_label, int) else None)
    graph.add_edge(("root",), ("core", "S"))
    graph.add_edge(("root",), ("leaf", "INCOMING"))
    for arc_index, ((tail, head), word) in enumerate(zip(arcs, words)):
        prior = ("core", tail)
        for word_index, label in enumerate(word):
            subdivision = ("sub", arc_index, word_index)
            leaf = ("leaf", "seg", arc_index, word_index)
            graph.add_node(subdivision, role="tree", label=None)
            graph.add_node(leaf, role="leaf", label=label if isinstance(label, int) else None)
            graph.add_edge(prior, subdivision); graph.add_edge(subdivision, leaf)
            prior = subdivision
        graph.add_edge(prior, ("core", head))
    for sink_index, (sink, label) in enumerate(zip(sinks, sink_labels)):
        leaf = ("leaf", "sink", sink_index)
        graph.add_node(leaf, role="leaf", label=label if isinstance(label, int) else None)
        graph.add_edge(("core", sink), leaf)
    require(nx.is_directed_acyclic_graph(graph), "GRAPH_CYCLE")
    for node, data in graph.nodes(data=True):
        expected = {"root": (0, 2), "tree": (1, 2), "retic": (2, 1), "leaf": (1, 0)}[data["role"]]
        require((graph.in_degree(node), graph.out_degree(node)) == expected, "GRAPH_DEGREE", node)
    return graph


def relabel(graph, permutation):
    result = graph.copy()
    for _, data in result.nodes(data=True):
        if isinstance(data.get("label"), int):
            data["label"] = permutation[data["label"]]
    return result


def descriptor_digest(model) -> str:
    payload = {
        "k": 4, "retic_count": len(model.retic_order),
        "edge_class_count": model.edge_class_count,
        "outputs": model.outputs, "edge_signatures": model.edge_signatures,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def point(model):
    edges = tuple((F(2 * i + 3, 8 * i + 16), F(3 * i + 5, 10 * i + 21)) for i in range(model.edge_class_count))
    lambdas = tuple(F(j + 2, j + 5) for j in range(len(model.retic_order)))
    require(all(0 < s < 1 and 0 < g < 1 and g > 2 * s - 1 for s, g in edges), "POINT_DOMAIN")
    return edges, lambdas


def replay(model, certificate):
    edges, lambdas = point(model)
    jac = jacobian(model, edges, lambdas)
    rows = tuple(certificate["pivot_rows"]); columns = tuple(certificate["pivot_columns"])
    minor_determinant = determinant([[jac[r][c] for c in columns] for r in rows])
    rank, own_rows, own_columns = rank_pivots(jac)
    return {
        "rank": rank, "stored_rank": certificate["rank"],
        "stored_minor_rows": list(rows), "stored_minor_columns": list(columns),
        "independent_stored_minor_determinant": str(minor_determinant),
        "stored_minor_determinant": certificate["minor_determinant"],
        "own_pivot_rows": list(own_rows), "own_pivot_columns": list(own_columns),
        "domain_checked_exactly": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    source_graph = build_graph(sources()[0])
    target_records = targets(4, True) + targets(4, False)
    require(len(target_records) == 2814, "TARGET_COUNT")
    permutation = tuple(itertools.permutations(range(4)))[1]
    target_graph = relabel(build_graph(target_records[4]), permutation)
    source_model = canonical_formal_map(source_graph)
    target_model = canonical_formal_map(target_graph)
    source_hash = descriptor_digest(source_model)
    target_hash = descriptor_digest(target_model)
    expected_source = "ffa19a908a552bb362e0c840df91c95a7db974f700f8ebc7fcce4ac2e5f55cd0"
    expected_target = "3085ce46031358d1cd879afdc62343b79dc0e00916df48421d73d5c105821dee"
    require(source_hash == expected_source, "SOURCE_DESCRIPTOR_HASH", source_hash)
    require(target_hash == expected_target, "TARGET_DESCRIPTOR_HASH", target_hash)
    lower_path = project / "work/raw_ledger_audit/artifacts/rank_lower_certificates.json.gz"
    lower = json.load(gzip.open(lower_path, "rt"))
    by_hash = {row["descriptor_sha256"]: row for row in lower["descriptors"]}
    source = replay(source_model, by_hash[source_hash])
    target = replay(target_model, by_hash[target_hash])
    require(source["rank"] == 13 and target["rank"] == 10, "RANK_COMPARISON", (source["rank"], target["rank"]))
    require(source["independent_stored_minor_determinant"] == source["stored_minor_determinant"], "SOURCE_DETERMINANT")
    require(target["independent_stored_minor_determinant"] == target["stored_minor_determinant"], "TARGET_DETERMINANT")
    result = {
        "schema": "independent-raw4-rank-replay-v1", "raw_id": 97,
        "raw_id_reconstruction": "((source_index=0)*2814+target_index=4)*24+permutation_index=1=97",
        "source_descriptor_sha256": source_hash, "target_descriptor_sha256": target_hash,
        "source": source, "target": target,
        "engine_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "lower_certificate_file_sha256": hashlib.sha256(lower_path.read_bytes()).hexdigest(),
        "independence": "literal graph reconstruction and separately implemented four-switch Fourier/Jacobian engine; no atlas/classifier/rank verifier import",
        "status": "PASS",
    }
    payload = dict(result)
    result["payload_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "payload_sha256": result["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
