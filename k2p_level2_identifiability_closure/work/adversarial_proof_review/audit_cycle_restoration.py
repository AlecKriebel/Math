#!/usr/bin/env python3
"""Fail-closed audit of dummy-bearing three-port cycle relations.

The global proof needs more than the already-closed no-dummy three-sunlet
gate: a fixed full containment may restrict to a selected three-port cycle
record whose target completion still contains physical dummy roles.  This
script independently enumerates every such raw direction, asks whether one
chosen first role excludes all possible source insertion edges, and subjects
every fully restored equal-topology child to exact rank/quadratic tests.

It is an adversarial diagnostic, not a promotion certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = (
    PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
)
TOPOLOGY_PATH = HERE / "verify_topology_direction.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def topology_key(topology, graph, labels: int) -> tuple:
    quartets = tuple(
        (quartet, topology.clean_displayed_splits(graph, quartet))
        for quartet in itertools.combinations(range(labels), 4)
    )
    triples = tuple(
        (triple, topology.clean_triple_type(graph, triple))
        for triple in itertools.combinations(range(labels), 3)
    )
    return quartets, triples


def topology_status(source_key: tuple, target_key: tuple) -> str:
    source_quartets, source_triples = source_key
    target_quartets, target_triples = target_key
    if source_quartets != target_quartets:
        return "displayed_quartet_mismatch"
    target_triples = dict(target_triples)
    if any(
        {source_type, target_triples[triple]} == {"tree", "sunlet"}
        for triple, source_type in source_triples
    ):
        return "strict_tree_sunlet"
    return "equal_topology"


def exact_incidence_class(atlas, registry: list, source_graph, target_graph) -> int:
    """Classify an ordered labelled graph pair by exact mixed isomorphism.

    A disjoint-union incidence graph with a side colour makes the test exact
    for the *pair*, rather than separately canonicalizing source and target.
    """
    pieces = []
    for side, graph in (("S", source_graph), ("T", target_graph)):
        mixed = atlas.sd0_mixed(graph)
        incidence = atlas.mixed_incidence_graph(mixed)
        renamed = nx.relabel_nodes(
            incidence, {node: (side, node) for node in incidence}, copy=True
        )
        for _, data in renamed.nodes(data=True):
            data["pair_kind"] = f"{side}|{data.get('kind')}"
        pieces.append(renamed)
    pair = nx.compose(pieces[0], pieces[1])
    node_match = (
        lambda left, right: left.get("pair_kind") == right.get("pair_kind")
        and left.get("label") == right.get("label")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")
    for class_id, representative in enumerate(registry):
        if nx.is_isomorphic(
            pair, representative, node_match=node_match, edge_match=edge_match
        ):
            return class_id
    registry.append(pair)
    return len(registry) - 1


def sparse_hash(atlas, polynomial: dict) -> str:
    rows = [
        [list(exponent), str(coefficient)]
        for exponent, coefficient in sorted(polynomial.items())
    ]
    return hashlib.sha256(canonical_bytes(rows)).hexdigest()


def strict_witness(atlas, descriptor, polynomial: dict) -> dict:
    for salt in range(32):
        edge_pairs, lambdas = atlas.default_exact_point(descriptor, salt)
        point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
        value = 0
        for exponent, coefficient in polynomial.items():
            term = coefficient
            for coordinate, power in zip(point, exponent):
                if power:
                    term *= coordinate**power
            value += term
        if value:
            return {
                "salt": salt,
                "edge_pairs": [[str(s), str(g)] for s, g in edge_pairs],
                "lambdas": [str(value) for value in lambdas],
                "value": str(value),
            }
    raise RuntimeError("no strict witness found for nonzero source pullback")


def exact_algebra_status(atlas, source_graph, target_graph, descriptor_cache) -> dict:
    def descriptor(graph):
        # The exact graph tuple is not hashable, so cache by canonical repr of
        # its nodes/edges only within this small audit.
        key = (
            tuple(sorted((repr(n), tuple(sorted(d.items()))) for n, d in graph.nodes(data=True))),
            tuple(sorted((repr(u), repr(v), tuple(sorted(d.items()))) for u, v, d in graph.edges(data=True))),
        )
        if key not in descriptor_cache:
            descriptor_cache[key] = atlas.model_descriptor_fast2(graph)
        return descriptor_cache[key]

    source = descriptor(source_graph)
    target = descriptor(target_graph)
    source_rank = atlas.rank_certificate(source)["rank"]
    target_rank = atlas.rank_certificate(target)["rank"]
    if source_rank > target_rank:
        return {
            "status": "rank_excluded",
            "source_rank": source_rank,
            "target_rank": target_rank,
        }
    separator = atlas.quadratic_separator_fast(source, target, max_block_size=16)
    if separator is None:
        return {
            "status": "algebra_unresolved",
            "source_rank": source_rank,
            "target_rank": target_rank,
            "descriptor_equal": source == target,
        }
    target_outputs = atlas.output_sparse_polynomials(target)
    target_columns = [
        atlas.sparse_mul(target_outputs[i], target_outputs[j])
        for i, j in separator["coordinate_pairs"]
    ]
    if atlas.sparse_lincomb(target_columns, separator["coefficients"]):
        raise RuntimeError("claimed quadratic is nonzero on target")
    source_pullback = separator["source_pullback"]
    if not source_pullback:
        raise RuntimeError("claimed quadratic is zero on source")
    return {
        "status": "quadratic_excluded",
        "source_rank": source_rank,
        "target_rank": target_rank,
        "weight": list(separator["weight"]),
        "coordinate_pairs": [list(pair) for pair in separator["coordinate_pairs"]],
        "coefficients": list(separator["coefficients"]),
        "source_pullback_sha256": sparse_hash(atlas, source_pullback),
        "strict_D_plus_witness": strict_witness(atlas, source, source_pullback),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    atlas = load_module("cycle_restoration_atlas", ATLAS_PATH)
    topology = load_module("cycle_restoration_topology", TOPOLOGY_PATH)
    sources = atlas.source_supports(core_ids=("cycle",))
    targets = atlas.target_completions(3, True) + atlas.target_completions(3, False)
    permutations = tuple(itertools.permutations(range(3)))
    source_keys = [topology_key(topology, source.graph, 3) for source in sources]
    target_keys = [topology_key(topology, target.graph, 3) for target in targets]

    initial_counts = Counter()
    dummy_roots = []
    no_dummy_terminals = Counter()
    for source_index, source in enumerate(sources):
        for target_index, target in enumerate(targets):
            for permutation in permutations:
                relabelled = atlas.relabel_record(target, permutation)
                mapped_key = topology_key(topology, relabelled.graph, 3)
                status = topology_status(source_keys[source_index], mapped_key)
                if status == "equal_topology":
                    # A terminal relation on the selected restriction does not
                    # restore the physical positions of omitted target roles.
                    # Every equal-topology dummy-bearing presentation remains
                    # a restoration root, regardless of whether its selected
                    # mixed graphs happen to be iso/T related.
                    if target.dummy_labels:
                        status = "equal_topology_nonterminal"
                    else:
                        relation = atlas.mixed_relation_exact(source.graph, relabelled.graph)
                        if relation in {"isomorphic", "triangle"}:
                            status = relation
                        else:
                            status = "equal_topology_nonterminal"
                initial_counts[status] += 1
                if target.dummy_labels and status == "equal_topology_nonterminal":
                    dummy_roots.append(
                        {
                            "source_index": source_index,
                            "target_index": target_index,
                            "permutation": permutation,
                            "roles": tuple(target.dummy_labels),
                        }
                    )
                elif not target.dummy_labels and status in {"isomorphic", "triangle"}:
                    no_dummy_terminals[status] += 1

    if len(dummy_roots) != 5964:
        raise RuntimeError(("dummy-root census", len(dummy_roots), initial_counts))

    source_children = {}
    source_child_keys = {}
    for source_index, source in enumerate(sources):
        for insertion_index, candidate in enumerate(topology.source_insertion_candidates(source.graph)):
            key = (source_index, insertion_index)
            graph = topology.clean_insert_source_leaf(source.graph, candidate, 3)
            source_children[key] = graph
            source_child_keys[key] = topology_key(topology, graph, 4)

    target_children = {}
    target_child_keys = {}
    first_counts = Counter()
    by_remaining = defaultdict(Counter)
    role_profiles = defaultdict(list)
    fully_restored_nonterminals = []
    fully_restored_isomorphisms = 0

    for root_id, root in enumerate(dummy_roots):
        target = targets[root["target_index"]]
        for role in root["roles"]:
            target_key = (root["target_index"], root["permutation"], role)
            if target_key not in target_children:
                graph = topology.clean_promote_target(
                    target, root["permutation"], role, 3
                )
                target_children[target_key] = graph
                target_child_keys[target_key] = topology_key(topology, graph, 4)
            target_graph = target_children[target_key]
            statuses = []
            for insertion_index in range(3):
                source_key = (root["source_index"], insertion_index)
                status = topology_status(
                    source_child_keys[source_key], target_child_keys[target_key]
                )
                remaining = len(root["roles"]) - 1
                if status == "equal_topology" and remaining == 0:
                    relation = atlas.mixed_relation_exact(
                        source_children[source_key], target_graph
                    )
                    if relation in {"isomorphic", "triangle"}:
                        status = relation
                    else:
                        status = "equal_topology_nonterminal"
                        fully_restored_nonterminals.append(
                            {
                                "root_id": root_id,
                                "source_index": root["source_index"],
                                "target_index": root["target_index"],
                                "permutation": root["permutation"],
                                "role": role,
                                "insertion_index": insertion_index,
                                "source_graph": source_children[source_key],
                                "target_graph": target_graph,
                            }
                        )
                elif status == "equal_topology":
                    status = "equal_topology_nonterminal"
                if status == "isomorphic":
                    fully_restored_isomorphisms += 1
                statuses.append(status)
                first_counts[status] += 1
                by_remaining[remaining][status] += 1
            role_profiles[root_id].append((role, tuple(statuses)))

    separated = {"displayed_quartet_mismatch", "strict_tree_sunlet"}
    roots_with_closing_role = 0
    roots_without_closing_role = []
    for root_id, profiles in role_profiles.items():
        closing = [role for role, statuses in profiles if set(statuses) <= separated]
        if closing:
            roots_with_closing_role += 1
        else:
            roots_without_closing_role.append(root_id)

    pair_registry = []
    descriptor_cache = {}
    algebra_by_class = {}
    class_multiplicity = Counter()
    class_examples = {}
    for row in fully_restored_nonterminals:
        class_id = exact_incidence_class(
            atlas, pair_registry, row["source_graph"], row["target_graph"]
        )
        class_multiplicity[class_id] += 1
        class_examples.setdefault(class_id, row)
    for class_id, row in class_examples.items():
        algebra_by_class[class_id] = exact_algebra_status(
            atlas, row["source_graph"], row["target_graph"], descriptor_cache
        )

    algebra_counts = Counter(
        {algebra_by_class[class_id]["status"]: multiplicity
         for class_id, multiplicity in class_multiplicity.items()}
    )
    # Counter(dict-comprehension) loses duplicates of a status; recompute.
    algebra_counts = Counter()
    for class_id, multiplicity in class_multiplicity.items():
        algebra_counts[algebra_by_class[class_id]["status"]] += multiplicity
    algebra_class_counts = Counter(row["status"] for row in algebra_by_class.values())

    public_classes = []
    for class_id in sorted(algebra_by_class):
        example = class_examples[class_id]
        public_classes.append(
            {
                "class_id": class_id,
                "raw_multiplicity": class_multiplicity[class_id],
                "example": {
                    key: (list(value) if isinstance(value, tuple) else value)
                    for key, value in example.items()
                    if key not in {"source_graph", "target_graph"}
                },
                "algebra": algebra_by_class[class_id],
            }
        )

    unresolved = algebra_counts["algebra_unresolved"]
    report = {
        "schema": "k2p-cycle-restoration-adversarial-audit-v1",
        "status": "BLOCKED" if unresolved or roots_without_closing_role else "PASS",
        "initial": {
            "sources": len(sources),
            "targets": len(targets),
            "raw_relations": len(sources) * len(targets) * len(permutations),
            "counts": dict(sorted(initial_counts.items())),
            "no_dummy_terminals": dict(sorted(no_dummy_terminals.items())),
            "dummy_nonterminal_roots": len(dummy_roots),
            "dummy_role_requests": sum(len(row["roles"]) for row in dummy_roots),
        },
        "first_child": {
            "raw_relations": sum(first_counts.values()),
            "counts": dict(sorted(first_counts.items())),
            "by_remaining_roles": {
                str(remaining): dict(sorted(counts.items()))
                for remaining, counts in sorted(by_remaining.items())
            },
            "fully_restored_isomorphisms": fully_restored_isomorphisms,
            "fully_restored_equal_nonterminals": len(fully_restored_nonterminals),
        },
        "smart_first_role": {
            "roots_with_a_role_separating_all_three_insertions": roots_with_closing_role,
            "roots_without_such_a_role": len(roots_without_closing_role),
            "root_ids_without_such_a_role_sha256": hashlib.sha256(
                canonical_bytes(roots_without_closing_role)
            ).hexdigest(),
        },
        "fully_restored_algebra": {
            "exact_ordered_graph_pair_classes": len(pair_registry),
            "raw_counts": dict(sorted(algebra_counts.items())),
            "class_counts": dict(sorted(algebra_class_counts.items())),
            "classes": public_classes,
        },
        "logical_conclusion": (
            "A pointwise quartet-only first-child lemma is false.  Fully restored "
            "equal-topology rows require the exact algebra above; roots without a "
            "closing first role require recursive all-role restoration and coherent "
            "transport before the global theorem can be promoted."
        ),
    }
    report["payload_sha256"] = hashlib.sha256(canonical_bytes(report)).hexdigest()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
