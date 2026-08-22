#!/usr/bin/env python3
"""Independent census of the complete cycle-to-dummy-target restoration tree.

This diagnostic deliberately shares no builder with the adversarial cycle
audit.  It enumerates every raw three-port direction, every dummy-role order,
and every source insertion edge until topology separates or the target becomes
physical.  Fully physical equal-topology leaves are classified by the strict
mixed-graph relation used by the official probe builder.
"""

from __future__ import annotations

import collections
import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
BUILDER = HERE / "build_probe_coherence.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("cycle_independent_probe", BUILDER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def exact_pair_registry_class(atlas, registry, source_graph, target_graph):
    pair = nx.Graph()
    for side, graph in (("S", source_graph), ("T", target_graph)):
        mixed = atlas.sd0_mixed(graph)
        incidence = atlas.mixed_incidence_graph(mixed)
        for node, data in incidence.nodes(data=True):
            pair.add_node(
                (side, node),
                color=(side, data.get("kind"), data.get("label")),
            )
        for left, right, data in incidence.edges(data=True):
            pair.add_edge((side, left), (side, right), color=data.get("head"))
    node_match = lambda left, right: left.get("color") == right.get("color")
    edge_match = lambda left, right: left.get("color") == right.get("color")
    bucket = nx.weisfeiler_lehman_graph_hash(pair, node_attr="color", edge_attr="color", iterations=8)
    for class_id, (other_bucket, representative) in enumerate(registry):
        if bucket == other_bucket and nx.is_isomorphic(
            pair, representative, node_match=node_match, edge_match=edge_match
        ):
            return class_id
    registry.append((bucket, pair))
    return len(registry) - 1


def sparse_public(polynomial):
    return [
        [list(exponent), str(coefficient)]
        for exponent, coefficient in sorted(polynomial.items())
    ]


def evaluate_sparse(polynomial, point):
    total = 0
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def algebra_certificate(pc, atlas, source_graph, target_graph):
    source = atlas.model_descriptor_fast2(source_graph)
    target = atlas.model_descriptor_fast2(target_graph)
    source_rank = atlas.rank_certificate(source)["rank"]
    target_rank = atlas.rank_certificate(target)["rank"]
    if source_rank > target_rank:
        return {"status": "rank_excluded", "source_rank": source_rank, "target_rank": target_rank}
    separator = atlas.quadratic_separator_fast(source, target, max_block_size=16)
    if separator is None:
        return {
            "status": "unresolved", "source_rank": source_rank,
            "target_rank": target_rank, "descriptor_equal": source == target,
        }
    target_outputs = atlas.output_sparse_polynomials(target)
    target_columns = [
        atlas.sparse_mul(target_outputs[left], target_outputs[right])
        for left, right in separator["coordinate_pairs"]
    ]
    if atlas.sparse_lincomb(target_columns, separator["coefficients"]):
        raise RuntimeError("cycle target separator does not vanish")
    source_pullback = separator["source_pullback"]
    if not source_pullback:
        raise RuntimeError("cycle source separator vanishes")
    witness = None
    for salt in range(32):
        edge_pairs, lambdas = atlas.default_exact_point(source, salt)
        point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
        value = evaluate_sparse(source_pullback, point)
        if value:
            witness = {
                "salt": salt,
                "edge_pairs": [[str(s), str(g)] for s, g in edge_pairs],
                "lambdas": [str(value) for value in lambdas],
                "source_value": str(value),
            }
            break
    if witness is None:
        raise RuntimeError("cycle separator lacks exact witness")
    public_pullback = sparse_public(source_pullback)
    return {
        "status": "quadratic_excluded",
        "source_rank": source_rank,
        "target_rank": target_rank,
        "weight": list(separator["weight"]),
        "coordinate_pairs": [list(pair) for pair in separator["coordinate_pairs"]],
        "coefficients": [str(value) for value in separator["coefficients"]],
        "source_pullback_sha256": pc.sha(public_pullback),
        "source_pullback_terms": len(public_pullback),
        "strict_witness": witness,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    pc = load_builder()
    atlas = pc.load_atlas()
    sources = atlas.source_supports(("cycle",))
    targets = atlas.target_completions(3, True) + atlas.target_completions(3, False)
    permutations = tuple(itertools.permutations(range(3)))

    source_states = {}
    target_states = {}

    def source_state(key):
        if key in source_states:
            return source_states[key]
        source_index, path = key
        if not path:
            graph = sources[source_index].graph
        else:
            parent = source_state((source_index, path[:-1]))[0]
            candidates = pc.internal_candidates(parent)
            graph = pc.insert_leaf(atlas, parent, candidates[path[-1]], 2 + len(path))
        value = graph, pc.topology_key(graph)
        source_states[key] = value
        return value

    def target_state(key):
        if key in target_states:
            return target_states[key]
        target_index, permutation_index, roles = key
        record = atlas.relabel_record(targets[target_index], permutations[permutation_index])
        full = record.graph
        for offset, role in enumerate(roles):
            full = pc.promote_graph_role(full, role, 3 + offset)
        selected = pc.selected_from_full_graph(full)
        value = full, selected, pc.topology_key(selected)
        target_states[key] = value
        return value

    roots = []
    initial = collections.Counter()
    no_dummy = []
    for source_index, source in enumerate(sources):
        source_key = source_state((source_index, ()))[1]
        for target_index, target in enumerate(targets):
            for permutation_index, permutation in enumerate(permutations):
                record = atlas.relabel_record(target, permutation)
                selected = atlas.selected_graph_from_completion(record)
                topology = pc.topology_compare(source_key, pc.topology_key(selected))
                if topology is not None:
                    initial[topology["status"]] += 1
                    continue
                roles = tuple(sorted(record.dummy_labels))
                if roles:
                    root_id = len(roots)
                    roots.append({
                        "root_id": root_id,
                        "source_index": source_index,
                        "target_index": target_index,
                        "permutation_index": permutation_index,
                        "roles": roles,
                    })
                    initial["dummy_equal_topology"] += 1
                    continue
                status, witnesses = pc.exact_relation(atlas, source.graph, record.graph)
                if status not in {"isomorphic", "triangle"}:
                    raise RuntimeError(("no-dummy three-port nonterminal", source_index, target_index, permutation_index))
                if len(witnesses) != 1:
                    raise RuntimeError(("no-dummy three-port transport", len(witnesses)))
                initial[status] += 1
                no_dummy.append((source_index, target_index, permutation_index, status))

    if initial != collections.Counter({
        "strict_tree_sunlet": 7452,
        "dummy_equal_topology": 5964,
        "triangle": 16,
        "isomorphic": 8,
    }):
        raise RuntimeError(("initial census", initial))

    states = [
        (row["root_id"], (row["source_index"], ()),
         (row["target_index"], row["permutation_index"], ()), row["roles"])
        for row in roots
    ]
    depth_reports = []
    exact_leaves = []
    nonterminal_leaves = []
    running = hashlib.sha256()
    for depth in range(1, 5):
        counts = collections.Counter()
        next_states = []
        for root_id, source_key, target_key, remaining in states:
            source_graph = source_state(source_key)[0]
            source_candidates = pc.internal_candidates(source_graph)
            for role in remaining:
                child_target_key = (target_key[0], target_key[1], target_key[2] + (role,))
                _, target_graph, target_topology = target_state(child_target_key)
                child_remaining = tuple(value for value in remaining if value != role)
                for insertion_index in range(len(source_candidates)):
                    child_source_key = (source_key[0], source_key[1] + (insertion_index,))
                    child_source, source_topology = source_state(child_source_key)
                    topology = pc.topology_compare(source_topology, target_topology)
                    if topology is not None:
                        status = topology["status"]
                    elif child_remaining:
                        status = "equal_topology_continuation"
                        next_states.append((root_id, child_source_key, child_target_key, child_remaining))
                    else:
                        try:
                            status, witnesses = pc.exact_relation(atlas, child_source, target_graph)
                        except ValueError:
                            status, witnesses = "none", []
                        if status in {"isomorphic", "triangle"}:
                            if len(witnesses) != 1:
                                raise RuntimeError(("cycle restored transport", len(witnesses)))
                            exact_leaves.append((root_id, child_source_key, child_target_key, status, witnesses[0]))
                        else:
                            status = "physical_equal_topology_nonterminal"
                            nonterminal_leaves.append((root_id, child_source_key, child_target_key))
                    counts[status] += 1
                    row = [root_id, list(source_key[1]), list(target_key[2]), role, insertion_index, status]
                    running.update(pc.canonical_bytes(row))
        depth_reports.append({
            "depth": depth,
            "parents": len(states),
            "raw_children": sum(counts.values()),
            "counts": dict(sorted(counts.items())),
            "continuations": len(next_states),
        })
        print(json.dumps(depth_reports[-1], sort_keys=True), flush=True)
        states = next_states
        if not states:
            break

    pair_registry = []
    pair_examples = {}
    pair_multiplicity = collections.Counter()
    for root_id, source_key, target_key in nonterminal_leaves:
        source_graph = source_state(source_key)[0]
        target_graph = target_state(target_key)[1]
        class_id = exact_pair_registry_class(
            atlas, pair_registry, source_graph, target_graph
        )
        pair_multiplicity[class_id] += 1
        pair_examples.setdefault(class_id, (root_id, source_key, target_key))
    algebra_classes = []
    for class_id in sorted(pair_examples):
        root_id, source_key, target_key = pair_examples[class_id]
        certificate = algebra_certificate(
            pc, atlas, source_state(source_key)[0], target_state(target_key)[1]
        )
        algebra_classes.append({
            "class_id": class_id,
            "raw_multiplicity": pair_multiplicity[class_id],
            "example": {
                "root_id": root_id,
                "source_state": [source_key[0], list(source_key[1])],
                "target_state": [target_key[0], target_key[1], list(target_key[2])],
            },
            "certificate": certificate,
        })

    report = {
        "initial": dict(sorted(initial.items())),
        "roots": len(roots),
        "dummy_profile": dict(sorted(collections.Counter(len(row["roles"]) for row in roots).items())),
        "no_dummy_exact": dict(sorted(collections.Counter(row[3] for row in no_dummy).items())),
        "depths": depth_reports,
        "exact_physical_leaves": dict(sorted(collections.Counter(row[3] for row in exact_leaves).items())),
        "physical_equal_topology_nonterminal": len(nonterminal_leaves),
        "physical_nonterminal_pair_classes": len(pair_registry),
        "physical_nonterminal_algebra_counts": dict(sorted(collections.Counter(
            row["certificate"]["status"] for row in algebra_classes
        ).items())),
        "physical_nonterminal_algebra_classes": algebra_classes,
        "ordered_edge_stream_sha256": running.hexdigest(),
        "source_state_cache": len(source_states),
        "target_state_cache": len(target_states),
    }
    report["payload_sha256"] = pc.sha(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
