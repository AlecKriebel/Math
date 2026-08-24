#!/usr/bin/env python3
"""Independent graph replay of direct equality and ordinary-triangle terminals.

The primitive directed records come from the separate audit engine named on
the command line.  This script implements its own semi-directed conversion,
ordinary-triangle predicate, and incidence-graph isomorphism test.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import networkx as nx


def require(ok, code, detail=None):
    if not ok:
        raise RuntimeError(code if detail is None else f"{code}: {detail}")


def load_primitives(path):
    spec = importlib.util.spec_from_file_location("audit_primitives", path)
    require(spec is not None and spec.loader is not None, "PRIMITIVE_IMPORT")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def semi_directed(graph):
    root = next(node for node, data in graph.nodes(data=True) if data["role"] == "root")
    children = tuple(graph.successors(root)); require(len(children) == 2, "ROOT_CHILDREN")
    mixed = nx.Graph()
    for node, data in graph.nodes(data=True):
        if node != root:
            mixed.add_node(node, label=data.get("label"))
    for tail, head in graph.edges():
        if tail == root:
            continue
        require(not mixed.has_edge(tail, head), "MIXED_PARALLEL")
        mixed.add_edge(tail, head, heads=frozenset((head,)) if graph.nodes[head]["role"] == "retic" else frozenset())
    require(not mixed.has_edge(*children), "ROOT_SUPPRESSION_PARALLEL")
    mixed.add_edge(children[0], children[1],
                   heads=frozenset(child for child in children if graph.nodes[child]["role"] == "retic"))
    return mixed


def selected_graph(graph):
    """Delete dummy boundaries and suppress the resulting unary structure."""
    keep = {data["label"] for _, data in graph.nodes(data=True) if isinstance(data.get("label"), int)}
    result = graph.copy()
    for node, data in list(result.nodes(data=True)):
        if data["role"] == "leaf" and data.get("label") not in keep:
            result.remove_node(node)
    changed = True
    while changed:
        changed = False
        for node, data in list(result.nodes(data=True)):
            if result.out_degree(node) == 0 and not (data["role"] == "leaf" and data.get("label") in keep):
                result.remove_node(node); changed = True; break
        if changed:
            continue
        for node, data in list(result.nodes(data=True)):
            if data["role"] != "leaf" and result.in_degree(node) == 1 and result.out_degree(node) == 1:
                parent = next(result.predecessors(node)); child = next(result.successors(node))
                result.remove_node(node)
                if parent != child and not result.has_edge(parent, child):
                    result.add_edge(parent, child)
                changed = True; break
        if changed:
            continue
        roots = [node for node in result if result.in_degree(node) == 0]
        if len(roots) == 1 and result.nodes[roots[0]]["role"] != "leaf" and result.out_degree(roots[0]) == 1:
            result.remove_node(roots[0]); changed = True
    for node, data in result.nodes(data=True):
        if data.get("label") in keep:
            data["role"] = "leaf"
        elif result.in_degree(node) == 0:
            data["role"] = "root"
        elif result.in_degree(node) == 2:
            data["role"] = "retic"
        else:
            data["role"] = "tree"
    return result


def ordinary_triangles(mixed):
    answer = []
    for vertices in itertools.combinations(mixed.nodes(), 3):
        edges = tuple(frozenset(edge) for edge in itertools.combinations(vertices, 2))
        if not all(mixed.has_edge(*tuple(edge)) for edge in edges):
            continue
        headed = []
        for edge in edges:
            heads = mixed.edges[tuple(edge)].get("heads", frozenset())
            if heads:
                require(len(heads) <= 2, "EDGE_HEAD_COUNT")
                headed.append((edge, heads))
        if len(headed) != 2:
            continue
        common = set(headed[0][1]) & set(headed[1][1])
        if len(common) == 1 and all(len(heads) == 1 for _, heads in headed):
            answer.append(frozenset(edges))
    return tuple(answer)


def incidence(mixed, forgotten=frozenset()):
    graph = nx.Graph()
    for node, data in mixed.nodes(data=True):
        graph.add_node(("v", node), kind="vertex", label=data.get("label"))
    for index, (left, right, data) in enumerate(sorted(mixed.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1])))):
        edge_node = ("e", index); graph.add_node(edge_node, kind="edge", label=None)
        edge = frozenset((left, right)); heads = data.get("heads", frozenset())
        graph.add_edge(edge_node, ("v", left), head=False if edge in forgotten else left in heads)
        graph.add_edge(edge_node, ("v", right), head=False if edge in forgotten else right in heads)
    return graph


def iso(first, second):
    node_match = lambda a, b: a["kind"] == b["kind"] and a["label"] == b["label"]
    edge_match = lambda a, b: a["head"] == b["head"]
    return nx.algorithms.isomorphism.GraphMatcher(first, second, node_match=node_match, edge_match=edge_match).is_isomorphic()


def relation(source, target):
    first = semi_directed(selected_graph(source)); second = semi_directed(selected_graph(target))
    if iso(incidence(first), incidence(second)):
        return "isomorphic", len(ordinary_triangles(first)), len(ordinary_triangles(second))
    first_triangles = ordinary_triangles(first); second_triangles = ordinary_triangles(second)
    for left in first_triangles:
        for right in second_triangles:
            if iso(incidence(first, left), incidence(second, right)):
                return "triangle", len(first_triangles), len(second_triangles)
    return "none", len(first_triangles), len(second_triangles)


def source_support_records(primitives, core_id):
    """Rebuild the repair-tagged primitive sources without the submitted atlas."""
    arcs, _reticulations, sinks, repairs = primitives.CORES[core_id]
    records = []
    for repair in repairs:
        words = [[] for _ in arcs]
        next_label = 1
        for arc_index in repair:
            words[arc_index].append(next_label)
            next_label += 1
        sink_labels = tuple(range(next_label, next_label + len(sinks)))
        records.append((core_id, tuple(tuple(word) for word in words), sink_labels, 0))
    return tuple(records)


def relabel_and_promote_record(record, permutation, promoted_roles=()):
    """Apply a selected-label permutation and then promote named dummy roles."""
    core, words, sink_labels, incoming = record
    promoted = {role: len(permutation) + offset for offset, role in enumerate(promoted_roles)}

    def transform(value):
        if isinstance(value, int):
            return permutation[value]
        return promoted.get(value, value)

    return (
        core,
        tuple(tuple(transform(value) for value in word) for word in words),
        tuple(transform(value) for value in sink_labels),
        transform(incoming),
    )


def insert_source_leaf(graph, insertion_index, label):
    """Subdivide the indexed non-root, non-pendant edge and attach a new leaf."""
    candidates = [
        (tail, head)
        for tail, head in sorted(graph.edges(), key=lambda edge: (repr(edge[0]), repr(edge[1])))
        if graph.nodes[head]["role"] != "leaf" and graph.nodes[tail]["role"] != "root"
    ]
    require(len(candidates) == 3, "CYCLE_SOURCE_INSERTION_CENSUS", len(candidates))
    require(0 <= insertion_index < len(candidates), "CYCLE_SOURCE_INSERTION_INDEX", insertion_index)
    tail, head = candidates[insertion_index]
    result = graph.copy()
    result.remove_edge(tail, head)
    subdivision = ("independent_cycle_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "independent_cycle_restoration", label)
    result.add_node(subdivision, role="tree", label=None)
    result.add_node(leaf, role="leaf", label=label)
    result.add_edge(tail, subdivision)
    result.add_edge(subdivision, head)
    result.add_edge(subdivision, leaf)
    require(nx.is_directed_acyclic_graph(result), "CYCLE_SOURCE_INSERTION_DAG")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--primitive-engine", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(); project = args.project.resolve()
    primitives = load_primitives(args.primitive_engine.resolve())
    registry_path = project / "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz"
    registry = json.load(gzip.open(registry_path, "rt"))
    graph_kinds = {}
    for row in registry["rows"]:
        kind = row["terminal_certificate"]["kind"]
        if kind in ("exact_mixed_graph_isomorphism", "ordinary_triangle_quotient"):
            graph_kinds[row["class_identifier"]] = kind
    ledger_path = project / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz"
    presentations = []
    with gzip.open(ledger_path, "rt") as stream:
        for line in stream:
            row = json.loads(line)
            if row["corrected_category"] != "direct_terminal_presentation":
                continue
            class_id = row["evidence_binding"]["terminal_class_id"]
            if class_id in graph_kinds:
                presentations.append(row)
    source_records = primitives.sources()
    target_records = primitives.targets(4, True) + primitives.targets(4, False)
    permutations = tuple(itertools.permutations(range(4)))
    observed = Counter(); class_presentations = Counter(); rows = []
    for row in presentations:
        class_id = row["evidence_binding"]["terminal_class_id"]
        expected = "isomorphic" if graph_kinds[class_id] == "exact_mixed_graph_isomorphism" else "triangle"
        source = primitives.build_graph(source_records[row["source_index"]])
        target = primitives.relabel(primitives.build_graph(target_records[row["target_index"]]),
                                    permutations[row["permutation_index"]])
        actual, source_triangles, target_triangles = relation(source, target)
        require(actual == expected, "GRAPH_RELATION_MISMATCH", (row["raw_id"], class_id, expected, actual))
        if actual == "triangle":
            require(source_triangles and target_triangles, "ORDINARY_TRIANGLE_ABSENT", row["raw_id"])
        observed[actual] += 1; class_presentations[class_id] += 1
        rows.append({"raw_id": row["raw_id"], "terminal_class_id": class_id, "relation": actual,
                     "source_ordinary_triangles": source_triangles, "target_ordinary_triangles": target_triangles})
    require(len(class_presentations) == len(graph_kinds) == 55, "GRAPH_CLASS_COVERAGE")
    cycle_source_records = source_support_records(primitives, "cycle")
    cycle_target_records = primitives.targets(3, True) + primitives.targets(3, False)
    cycle_permutations = tuple(itertools.permutations(range(3)))
    cycle_path = project / "work/cycle_three_port_closure/promotion/cycle_base_authoritative.jsonl.gz"
    cycle_observed = Counter(); cycle_rows = []
    with gzip.open(cycle_path, "rt") as stream:
        for line in stream:
            row = json.loads(line)
            if row["terminal_kind"] not in ("labelled_isomorphism", "ordinary_triangle_relation"):
                continue
            expected = "isomorphic" if row["terminal_kind"] == "labelled_isomorphism" else "triangle"
            source = primitives.build_graph(cycle_source_records[row["source_index"]])
            target = primitives.relabel(primitives.build_graph(cycle_target_records[row["target_index"]]),
                                        cycle_permutations[row["permutation_index"]])
            actual, source_triangles, target_triangles = relation(source, target)
            require(actual == expected, "CYCLE_GRAPH_RELATION_MISMATCH", (row["raw_id"], expected, actual))
            cycle_observed[actual] += 1
            cycle_rows.append({"raw_id": row["raw_id"], "relation": actual,
                               "source_ordinary_triangles": source_triangles, "target_ordinary_triangles": target_triangles})

    theta2_source_records = source_support_records(primitives, "theta2")
    theta2_target_records = primitives.targets(5, True) + primitives.targets(5, False)
    theta2_permutations = tuple(itertools.permutations(range(5)))
    theta2_path = project / "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz"
    theta2_rows = []
    with gzip.open(theta2_path, "rt") as stream:
        for line in stream:
            if '"corrected_category":"labelled_isomorphism"' not in line:
                continue
            row = json.loads(line)
            source = primitives.build_graph(theta2_source_records[row["source_index"]])
            target = primitives.relabel(primitives.build_graph(theta2_target_records[row["target_index"]]),
                                        theta2_permutations[row["permutation_index"]])
            actual, source_triangles, target_triangles = relation(source, target)
            require(actual == "isomorphic", "THETA2_GRAPH_RELATION_MISMATCH", (row["raw_id"], actual))
            theta2_rows.append({"raw_id": row["raw_id"], "relation": actual,
                                "source_ordinary_triangles": source_triangles,
                                "target_ordinary_triangles": target_triangles})
    require(len(theta2_rows) == 80, "THETA2_ISOMORPHISM_CENSUS", len(theta2_rows))

    cycle_full_path = project / "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz"
    cycle_full_rows = []
    with gzip.open(cycle_full_path, "rt") as stream:
        for line in stream:
            if '"terminal_kind":"labelled_isomorphism"' not in line:
                continue
            row = json.loads(line)
            require(len(row["source_placement_path"]) == 1, "CYCLE_FULL_SOURCE_DEPTH", row["raw_id"])
            source = insert_source_leaf(
                primitives.build_graph(cycle_source_records[row["source_index"]]),
                row["source_placement_path"][0],
                3,
            )
            target_record = relabel_and_promote_record(
                cycle_target_records[row["target_index"]],
                cycle_permutations[row["permutation_index"]],
                tuple(row["dummy_roles_in_label_order"]),
            )
            target = primitives.build_graph(target_record)
            actual, source_triangles, target_triangles = relation(source, target)
            require(actual == "isomorphic", "CYCLE_FULL_GRAPH_RELATION_MISMATCH", (row["raw_id"], actual))
            cycle_full_rows.append({"raw_id": row["raw_id"], "relation": actual,
                                    "source_ordinary_triangles": source_triangles,
                                    "target_ordinary_triangles": target_triangles})
    require(len(cycle_full_rows) == 12, "CYCLE_FULL_ISOMORPHISM_CENSUS", len(cycle_full_rows))

    tested_presentations = len(rows) + len(cycle_rows) + len(theta2_rows) + len(cycle_full_rows)
    result = {
        "schema": "independent-k2p-graph-relation-audit-v3",
        "raw4_class_counts": dict(Counter("isomorphic" if kind == "exact_mixed_graph_isomorphism" else "triangle" for kind in graph_kinds.values())),
        "raw4_presentation_counts": dict(observed), "raw4_classes": len(class_presentations), "raw4_presentations": len(rows),
        "cycle_base_presentation_counts": dict(cycle_observed), "cycle_base_presentations": len(cycle_rows),
        "theta2_isomorphism_presentations": len(theta2_rows),
        "cycle_full_isomorphism_presentations": len(cycle_full_rows),
        "tested_presentations": tested_presentations,
        "all_triangle_tests_restricted_to_ordinary_pattern": True,
        "raw4_rows": rows, "cycle_base_rows": cycle_rows,
        "theta2_rows": theta2_rows, "cycle_full_rows": cycle_full_rows,
        "independence": "fresh incidence-graph isomorphism; only exactly-two-arrows-to-one-common-reticulation triangles may be forgotten",
        "registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
        "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        "theta2_ledger_sha256": hashlib.sha256(theta2_path.read_bytes()).hexdigest(),
        "cycle_full_ledger_sha256": hashlib.sha256(cycle_full_path.read_bytes()).hexdigest(),
        "status": "PASS",
    }
    payload = dict(result); result["payload_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "raw4_classes": result["raw4_classes"],
                      "presentations": result["tested_presentations"],
                      "payload_sha256": result["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
