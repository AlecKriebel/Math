#!/usr/bin/env python3
"""Proof-first exploration of the missing coherent one-/two-port forest.

This is intentionally not a promotion certificate.  It asks whether exact
displayed-set/tree-sunlet separations plus labelled mixed-graph terminals
already classify every A+p and A+p+q row above the currently visible direct
and repaired anchors.  Exact transport restriction is left as a separate
gate and is reported as such.
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


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RAW_LEDGER = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
THETA2_LEDGER = (
    PROJECT
    / "work/theta2_five_port_closure/artifacts/raw_directional_ledger.jsonl.gz"
)
TOPOLOGY_AUDIT = HERE / "verify_topology_direction.py"
PROBE_AUDIT = HERE / "verify_probe_coverage.py"


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


def classify(grammar, source_graph, target_graph, source_key, target_key) -> str:
    source_quartets, source_triples = source_key
    target_quartets, target_triples = target_key
    if source_quartets != target_quartets:
        return "displayed_quartet_mismatch"
    source_triples = dict(source_triples)
    target_triples = dict(target_triples)
    if any(
        {source_triples[triple], target_triples[triple]} == {"tree", "sunlet"}
        for triple in source_triples
    ):
        return "strict_tree_sunlet"
    relation = grammar.mixed_relation_exact(source_graph, target_graph)
    # The atlas uses the literal string ``"none"`` for an equal-deck
    # relation that is neither a labelled isomorphism nor an ordinary
    # triangle relation.  Treating that nonempty string as a terminal would
    # silently promote precisely the cases this audit is meant to detect.
    return (
        relation
        if relation in {"isomorphic", "triangle"}
        else "equal_deck_nonterminal"
    )


def transport_records(grammar, source_graph, target_graph, status: str) -> list[dict]:
    """Enumerate exact labelled vertex transports for an iso/T terminal."""
    source_mixed = grammar.sd0_mixed(source_graph)
    target_mixed = grammar.sd0_mixed(target_graph)
    if status == "isomorphic":
        triangle_pairs = [(None, None)]
    elif status == "triangle":
        triangle_pairs = [
            (source_triangle, target_triangle)
            for source_triangle in grammar._mixed_triangle_edges(source_mixed)
            for target_triangle in grammar._mixed_triangle_edges(target_mixed)
        ]
    else:
        raise RuntimeError(("transport requested for nonterminal", status))
    node_match = (
        lambda left, right: left.get("kind") == right.get("kind")
        and left.get("label") == right.get("label")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")
    records = {}
    for source_triangle, target_triangle in triangle_pairs:
        source_incidence = grammar.mixed_incidence_graph(source_mixed, source_triangle)
        target_incidence = grammar.mixed_incidence_graph(target_mixed, target_triangle)
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            source_incidence,
            target_incidence,
            node_match=node_match,
            edge_match=edge_match,
        )
        for mapping in matcher.isomorphisms_iter():
            vertex_map = {
                node: mapping[("v", node)][1] for node in source_mixed.nodes()
            }
            public_map = tuple(
                sorted(
                    ((repr(left), repr(right)) for left, right in vertex_map.items()),
                    key=lambda pair: pair[0],
                )
            )
            public_source_triangle = None
            public_target_triangle = None
            if source_triangle is not None:
                public_source_triangle = tuple(
                    sorted(tuple(sorted(map(repr, edge))) for edge in source_triangle)
                )
                public_target_triangle = tuple(
                    sorted(tuple(sorted(map(repr, edge))) for edge in target_triangle)
                )
            key = (public_map, public_source_triangle, public_target_triangle)
            records[key] = {
                "vertex_map": vertex_map,
                "source_triangle": (
                    None if source_triangle is None else frozenset(source_triangle)
                ),
                "target_triangle": (
                    None if target_triangle is None else frozenset(target_triangle)
                ),
                "public": {
                    "vertex_map": [list(pair) for pair in public_map],
                    "source_triangle": public_source_triangle,
                    "target_triangle": public_target_triangle,
                },
            }
    return [records[key] for key in sorted(records, key=repr)]


def compatible_transport(grammar, parent: dict, child: dict) -> bool:
    parent_transport = parent["transport"]
    child_transport = child["transport"]
    source_nodes = set(grammar.sd0_mixed(parent["source_graph"]).nodes())
    if any(
        child_transport["vertex_map"].get(node)
        != parent_transport["vertex_map"][node]
        for node in source_nodes
    ):
        return False
    if child["status"] == "triangle":
        if parent["status"] != "triangle":
            return False
        if child_transport["source_triangle"] != parent_transport["source_triangle"]:
            return False
        if child_transport["target_triangle"] != parent_transport["target_triangle"]:
            return False
    return True


def direct_anchors(grammar, sources, targets) -> list[dict]:
    anchors = []
    with gzip.open(RAW_LEDGER, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("status") not in {"isomorphic", "triangle"}:
                continue
            if targets[row["target_index"]].dummy_labels:
                continue
            target_graph = grammar.relabel_record(
                targets[row["target_index"]], tuple(row["port_permutation"])
            ).graph
            source_graph = sources[row["source_index"]].graph
            relation = grammar.mixed_relation_exact(source_graph, target_graph)
            if relation != row["status"]:
                raise RuntimeError(("direct anchor status drift", row, relation))
            transports = transport_records(grammar, source_graph, target_graph, relation)
            if len(transports) != 1:
                raise RuntimeError(("nonunique direct anchor transport", row, len(transports)))
            anchors.append(
                {
                    "anchor_id": f"direct:raw{row['raw_id']}",
                    "origin": "direct_no_dummy",
                    "base_status": relation,
                    "status": relation,
                    "transport": transports[0],
                    "labels": 4,
                    "source_graph": source_graph,
                    "target_graph": target_graph,
                }
            )
    if len(anchors) != 26:
        raise RuntimeError(("direct anchor count", len(anchors)))
    return anchors


def repaired_anchors(topology, probe_audit, grammar, sources, targets) -> list[dict]:
    roots, _ = probe_audit.terminal_inventory(targets)
    anchors = []
    for root in roots:
        for role in root["roles"]:
            target_graph = topology.clean_promote_target(
                targets[root["target_index"]], root["permutation"], role
            )
            target_key = topology_key(topology, target_graph, 5)
            for insertion_index, candidate in enumerate(root["candidates"]):
                source_graph = topology.clean_insert_source_leaf(
                    sources[root["source_index"]].graph, candidate, 4
                )
                source_key = topology_key(topology, source_graph, 5)
                relation = classify(
                    grammar, source_graph, target_graph, source_key, target_key
                )
                if relation not in {"isomorphic", "triangle"}:
                    continue
                transports = transport_records(
                    grammar, source_graph, target_graph, relation
                )
                if len(transports) != 1:
                    raise RuntimeError(
                        ("nonunique repaired anchor transport", len(transports))
                    )
                anchors.append(
                    {
                        "anchor_id": (
                            f"repaired:s{root['source_index']}:c{root['canonical_class_id']}:"
                            f"t{root['target_index']}:p{''.join(map(str, root['permutation']))}:"
                            f"{role}:i{insertion_index}"
                        ),
                        "origin": "omitted_terminal_first_child",
                        "base_status": relation,
                        "status": relation,
                        "transport": transports[0],
                        "labels": 5,
                        "source_graph": source_graph,
                        "target_graph": target_graph,
                    }
                )
    if len(anchors) != 13:
        raise RuntimeError(("repaired anchor count", len(anchors)))
    if any(anchor["base_status"] != "isomorphic" for anchor in anchors):
        raise RuntimeError("nonisomorphic repaired anchor")
    return anchors


def theta2_anchors(grammar) -> list[dict]:
    sources = grammar.source_supports(core_ids=("theta2",))
    targets = grammar.target_completions(5, True) + grammar.target_completions(5, False)
    anchors = []
    with gzip.open(THETA2_LEDGER, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("category") != "isomorphic":
                continue
            if targets[row["target_index"]].dummy_labels:
                raise RuntimeError(("theta2 iso terminal retained a dummy", row))
            source_graph = sources[row["source_index"]].graph
            target_graph = grammar.relabel_record(
                targets[row["target_index"]], tuple(row["port_permutation"])
            ).graph
            relation = grammar.mixed_relation_exact(source_graph, target_graph)
            if relation != "isomorphic":
                raise RuntimeError(("theta2 anchor status drift", row, relation))
            transports = transport_records(grammar, source_graph, target_graph, relation)
            if len(transports) != 1:
                raise RuntimeError(("theta2 anchor transport multiplicity", len(transports)))
            anchors.append(
                {
                    "anchor_id": f"theta2:raw{row['raw_id']}",
                    "origin": "theta2_direct",
                    "base_status": relation,
                    "status": relation,
                    "transport": transports[0],
                    "labels": 5,
                    "source_graph": source_graph,
                    "target_graph": target_graph,
                }
            )
    if len(anchors) != 80:
        raise RuntimeError(("theta2 anchor count", len(anchors)))
    return anchors


def cycle_anchors(grammar) -> list[dict]:
    """Expand the separately closed three-sunlet T class to raw transports."""
    sources = grammar.source_supports(core_ids=("cycle",))
    targets = grammar.target_completions(3, True) + grammar.target_completions(3, False)
    anchors = []
    for source_index, source in enumerate(sources):
        for target_index, target in enumerate(targets):
            if target.core_id != "cycle" or target.dummy_labels:
                continue
            for permutation in itertools.permutations(range(3)):
                source_graph = source.graph
                target_graph = grammar.relabel_record(target, permutation).graph
                relation = grammar.mixed_relation_exact(source_graph, target_graph)
                if relation not in {"isomorphic", "triangle"}:
                    raise RuntimeError(("cycle anchor relation drift", relation))
                transports = transport_records(
                    grammar, source_graph, target_graph, relation
                )
                if len(transports) != 1:
                    raise RuntimeError(("cycle anchor transport multiplicity", len(transports)))
                anchors.append(
                    {
                        "anchor_id": (
                            f"cycle:s{source_index}:t{target_index}:"
                            f"p{''.join(map(str, permutation))}"
                        ),
                        "origin": "cycle_three_port",
                        "base_status": relation,
                        "status": relation,
                        "transport": transports[0],
                        "labels": 3,
                        "source_graph": source_graph,
                        "target_graph": target_graph,
                    }
                )
    if len(anchors) != 24:
        raise RuntimeError(("cycle anchor count", len(anchors)))
    return anchors


def add_one_port(topology, grammar, anchor: dict) -> tuple[Counter, list[dict], Counter]:
    label = anchor["labels"]
    source_children = []
    target_children = []
    for index, candidate in enumerate(
        topology.source_insertion_candidates(anchor["source_graph"])
    ):
        graph = topology.clean_insert_source_leaf(anchor["source_graph"], candidate, label)
        source_children.append((index, graph, topology_key(topology, graph, label + 1)))
    for index, candidate in enumerate(
        topology.source_insertion_candidates(anchor["target_graph"])
    ):
        graph = topology.clean_insert_source_leaf(anchor["target_graph"], candidate, label)
        target_children.append((index, graph, topology_key(topology, graph, label + 1)))

    counts = Counter()
    transport_counts = Counter()
    survivors = []
    for source_index, source_graph, source_key in source_children:
        for target_index, target_graph, target_key in target_children:
            status = classify(grammar, source_graph, target_graph, source_key, target_key)
            counts[status] += 1
            if status in {"isomorphic", "triangle"}:
                transports = transport_records(
                    grammar, source_graph, target_graph, status
                )
                transport_counts[f"multiplicity_{len(transports)}"] += 1
                if len(transports) != 1:
                    raise RuntimeError(("one-port transport multiplicity", len(transports)))
                child = {
                        "parent_anchor_id": anchor["anchor_id"],
                        "parent_status": anchor["base_status"],
                        "source_insertion_index": source_index,
                        "target_insertion_index": target_index,
                        "status": status,
                        "transport": transports[0],
                        "labels": label + 1,
                        "source_graph": source_graph,
                        "target_graph": target_graph,
                    }
                if not compatible_transport(grammar, anchor, child):
                    raise RuntimeError(("one-port orphan transport", child))
                transport_counts["compatible"] += 1
                survivors.append(child)
    return counts, survivors, transport_counts


def add_second_port(topology, grammar, parent: dict) -> tuple[Counter, Counter, list[str]]:
    label = parent["labels"]
    source_children = []
    target_children = []
    for index, candidate in enumerate(
        topology.source_insertion_candidates(parent["source_graph"])
    ):
        graph = topology.clean_insert_source_leaf(parent["source_graph"], candidate, label)
        source_children.append((index, graph, topology_key(topology, graph, label + 1)))
    for index, candidate in enumerate(
        topology.source_insertion_candidates(parent["target_graph"])
    ):
        graph = topology.clean_insert_source_leaf(parent["target_graph"], candidate, label)
        target_children.append((index, graph, topology_key(topology, graph, label + 1)))
    counts = Counter()
    transport_counts = Counter()
    terminal_hashes = []
    for source_index, source_graph, source_key in source_children:
        for target_index, target_graph, target_key in target_children:
            status = classify(grammar, source_graph, target_graph, source_key, target_key)
            counts[status] += 1
            if status not in {"isomorphic", "triangle"}:
                continue
            transports = transport_records(grammar, source_graph, target_graph, status)
            transport_counts[f"multiplicity_{len(transports)}"] += 1
            if len(transports) != 1:
                raise RuntimeError(("two-port transport multiplicity", len(transports)))
            child = {
                "status": status,
                "transport": transports[0],
                "source_graph": source_graph,
                "target_graph": target_graph,
            }
            if not compatible_transport(grammar, parent, child):
                raise RuntimeError(("two-port orphan transport", parent, child))
            transport_counts["compatible"] += 1
            terminal_row = {
                "parent_anchor_id": parent["parent_anchor_id"],
                "parent_source_insertion_index": parent["source_insertion_index"],
                "parent_target_insertion_index": parent["target_insertion_index"],
                "parent_status": parent["status"],
                "source_insertion_index": source_index,
                "target_insertion_index": target_index,
                "status": status,
                "transport": transports[0]["public"],
            }
            terminal_hashes.append(
                hashlib.sha256(canonical_bytes(terminal_row)).hexdigest()
            )
    return counts, transport_counts, terminal_hashes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    topology = load_module("probe_forest_topology", TOPOLOGY_AUDIT)
    probe_audit = load_module("probe_forest_inventory", PROBE_AUDIT)
    grammar = topology.load_graph_grammar()
    sources = grammar.source_supports()
    targets = grammar.target_completions(4, True) + grammar.target_completions(4, False)
    anchors = direct_anchors(grammar, sources, targets)
    anchors += repaired_anchors(topology, probe_audit, grammar, sources, targets)
    anchors += theta2_anchors(grammar)
    anchors += cycle_anchors(grammar)

    one_counts = Counter()
    one_survivors = []
    one_by_origin = Counter()
    one_transport_counts = Counter()
    one_terminal_hashes = []
    for anchor in anchors:
        counts, survivors, transport_counts = add_one_port(
            topology, grammar, anchor
        )
        one_counts.update(counts)
        one_survivors.extend(survivors)
        one_transport_counts.update(transport_counts)
        for child in survivors:
            terminal_row = {
                "parent_anchor_id": child["parent_anchor_id"],
                "parent_status": child["parent_status"],
                "source_insertion_index": child["source_insertion_index"],
                "target_insertion_index": child["target_insertion_index"],
                "status": child["status"],
                "transport": child["transport"]["public"],
            }
            one_terminal_hashes.append(
                hashlib.sha256(canonical_bytes(terminal_row)).hexdigest()
            )
        for status, count in counts.items():
            one_by_origin[(anchor["origin"], status)] += count

    two_counts = Counter()
    two_transport_counts = Counter()
    two_terminal_hashes = []
    for parent in one_survivors:
        counts, transport_counts, terminal_hashes = add_second_port(
            topology, grammar, parent
        )
        two_counts.update(counts)
        two_transport_counts.update(transport_counts)
        two_terminal_hashes.extend(terminal_hashes)

    nonterminal = one_counts["equal_deck_nonterminal"] + two_counts["equal_deck_nonterminal"]
    report: dict[str, object] = {
        "schema": "k2p-proof-first-probe-exploration-v1",
        "status": (
            "STRUCTURAL_TRANSPORT_PASS_MUTATIONS_UNCHECKED"
            if nonterminal == 0
            else "ALGEBRA_NEEDED"
        ),
        "scope": (
            "all direct no-dummy raw equality presentations and the 13 repaired five-port "
            "anchors; topology and exact mixed-graph status only"
        ),
        "anchors": {
            "direct_raw": sum(anchor["origin"] == "direct_no_dummy" for anchor in anchors),
            "repaired_raw": sum(
                anchor["origin"] == "omitted_terminal_first_child" for anchor in anchors
            ),
            "theta2_raw": sum(anchor["origin"] == "theta2_direct" for anchor in anchors),
            "cycle_raw": sum(
                anchor["origin"] == "cycle_three_port" for anchor in anchors
            ),
            "total": len(anchors),
            "by_base_status": dict(sorted(Counter(a["base_status"] for a in anchors).items())),
        },
        "one_port": {
            "raw_relations": sum(one_counts.values()),
            "counts": dict(sorted(one_counts.items())),
            "terminal_survivors": len(one_survivors),
            "transport_counts": dict(sorted(one_transport_counts.items())),
            "ordered_terminal_hash_root": hashlib.sha256(
                canonical_bytes(one_terminal_hashes)
            ).hexdigest(),
            "by_origin_and_status": {
                f"{origin}:{status}": count
                for (origin, status), count in sorted(one_by_origin.items())
            },
        },
        "two_port": {
            "parent_relations": len(one_survivors),
            "raw_relations": sum(two_counts.values()),
            "counts": dict(sorted(two_counts.items())),
            "transport_counts": dict(sorted(two_transport_counts.items())),
            "ordered_terminal_hash_root": hashlib.sha256(
                canonical_bytes(two_terminal_hashes)
            ).hexdigest(),
        },
        "remaining_gate": (
            "independently replay these graph-derived rows, publish explicit mutation tests "
            "for wrong parent/order/triangle choices, and bind the package into the theorem gate"
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
