#!/usr/bin/env python3
"""Exhibit the root-sensitive false topology oracle in the revoked probe deck."""

from __future__ import annotations

import collections
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
BUILDER = PROJECT / "work/probe_coherence_closure/build_probe_coherence.py"
PROBE = PROJECT / "work/probe_coherence_closure/probe_certificate.json"
REVOKED_PROBE = PROJECT / "work/probe_coherence_closure/counterexamples/root_sensitive_bad_certificate.json"
OUTPUT = HERE / "revoked_probe_truth_certificate.json"


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def public_topology_key(builder, value):
    labels, quartets, triples = value
    return {
        "labels": list(labels),
        "quartets": [
            [list(quartet), builder.serialize_split_set(splits)]
            for quartet, splits in quartets
        ],
        "triples": [[list(triple), kind] for triple, kind in triples],
    }


def load_builder():
    spec = importlib.util.spec_from_file_location("revoked_probe_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("builder import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def mixed_incidence(atlas, graph):
    mixed = atlas.sd0_mixed(graph)
    result = nx.Graph()
    for node, data in mixed.nodes(data=True):
        result.add_node(("v", node), color=("vertex", data.get("label")))
    for number, (left, right, data) in enumerate(
        sorted(mixed.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1])))
    ):
        edge_node = ("e", number)
        result.add_node(edge_node, color=("edge", None))
        heads = data.get("heads", frozenset())
        result.add_edge(edge_node, ("v", left), color=left in heads)
        result.add_edge(edge_node, ("v", right), color=right in heads)
    return result


def main():
    builder = load_builder()
    atlas = builder.load_atlas()
    probe_path = PROBE if PROBE.exists() else REVOKED_PROBE
    probe = json.loads(probe_path.read_text())
    probe_payload = probe["payload_sha256"]
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    anchors, _ = builder.four_port_anchors(atlas, sources, targets)
    if len(anchors) != 39:
        raise RuntimeError(f"reviewed anchor census:{len(anchors)}")

    topology_counts = collections.Counter()
    exact_by_claim = collections.Counter()
    false_rows = []
    children = []
    for anchor in anchors:
        label = anchor["labels"]
        source_children = [
            builder.insert_leaf(atlas, anchor["source_graph"], candidate, label)
            for candidate in builder.internal_candidates(anchor["source_graph"])
        ]
        target_children = [
            builder.insert_leaf(atlas, anchor["target_graph"], candidate, label)
            for candidate in builder.internal_candidates(anchor["target_graph"])
        ]
        source_keys = [builder.topology_key(graph) for graph in source_children]
        target_keys = [builder.topology_key(graph) for graph in target_children]
        children.extend(
            (anchor["anchor_id"], "source", index, graph, source_keys[index])
            for index, graph in enumerate(source_children)
        )
        children.extend(
            (anchor["anchor_id"], "target", index, graph, target_keys[index])
            for index, graph in enumerate(target_children)
        )
        for source_index, source_graph in enumerate(source_children):
            for target_index, target_graph in enumerate(target_children):
                topology = builder.topology_compare(
                    source_keys[source_index], target_keys[target_index]
                )
                if topology is None:
                    continue
                claimed = topology["status"]
                topology_counts[claimed] += 1
                exact_status, witnesses = builder.exact_relation(
                    atlas, source_graph, target_graph
                )
                exact_by_claim[(claimed, exact_status)] += 1
                if exact_status == "none":
                    continue
                false_rows.append(
                    {
                        "anchor_id": anchor["anchor_id"],
                        "origin": anchor["origin"],
                        "source_insertion_index": source_index,
                        "target_insertion_index": target_index,
                        "claimed_topology": topology,
                        "exact_relation": exact_status,
                        "exact_transport_multiplicity": len(witnesses),
                        "exact_transport_sha256": [row["transport_sha256"] for row in witnesses],
                        "source_graph_sha256": sha(builder.graph_payload(source_graph)),
                        "target_graph_sha256": sha(builder.graph_payload(target_graph)),
                    }
                )

    # Independently group every rooted child by exact labelled semi-directed
    # incidence isomorphism and require its deck to be constant on a class.
    representatives = []
    representative_keys = []
    representative_metadata = []
    buckets = collections.defaultdict(list)
    conflicts = []
    node_match = lambda left, right: left.get("color") == right.get("color")
    edge_match = lambda left, right: left.get("color") == right.get("color")
    for anchor_id, side, index, graph, topology_key in children:
        incidence = mixed_incidence(atlas, graph)
        bucket = nx.weisfeiler_lehman_graph_hash(
            incidence, node_attr="color", edge_attr="color", iterations=8
        )
        class_id = None
        for candidate in buckets[bucket]:
            if nx.is_isomorphic(
                incidence,
                representatives[candidate],
                node_match=node_match,
                edge_match=edge_match,
            ):
                class_id = candidate
                break
        if class_id is None:
            class_id = len(representatives)
            representatives.append(incidence)
            representative_keys.append(topology_key)
            representative_metadata.append([anchor_id, side, index])
            buckets[bucket].append(class_id)
        elif representative_keys[class_id] != topology_key:
            conflicts.append(
                {
                    "mixed_class_id": class_id,
                    "representative": representative_metadata[class_id],
                    "conflicting_row": [anchor_id, side, index],
                    "representative_topology_sha256": sha(
                        public_topology_key(builder, representative_keys[class_id])
                    ),
                    "conflicting_topology_sha256": sha(
                        public_topology_key(builder, topology_key)
                    ),
                }
            )

    if topology_counts != collections.Counter(
        {"displayed_quartet_mismatch": 1820, "strict_tree_sunlet": 115}
    ):
        raise RuntimeError(f"reviewed topology census drift:{topology_counts}")
    if exact_by_claim != collections.Counter(
        {
            ("displayed_quartet_mismatch", "none"): 1820,
            ("strict_tree_sunlet", "none"): 39,
            ("strict_tree_sunlet", "isomorphic"): 36,
            ("strict_tree_sunlet", "triangle"): 40,
        }
    ):
        raise RuntimeError(f"exact truth census drift:{exact_by_claim}")
    if len(false_rows) != 76 or len(conflicts) != 76:
        raise RuntimeError(f"false/conflict census:{len(false_rows)}/{len(conflicts)}")

    report = {
        "schema": "k2p-revoked-probe-topology-truth-v1",
        "status": "BLOCKED_FALSE_TOPOLOGY_ORACLE",
        "revoked_probe_payload_sha256": probe_payload,
        "reviewed_raw_anchors": len(anchors),
        "reviewed_child_graphs": len(children),
        "claimed_topology_counts": dict(sorted(topology_counts.items())),
        "exact_full_relation_census_by_claim": {
            f"{claim}:{truth}": count
            for (claim, truth), count in sorted(exact_by_claim.items())
        },
        "false_topology_oracle_count": len(false_rows),
        "false_topology_oracle_by_exact_relation": dict(
            sorted(collections.Counter(row["exact_relation"] for row in false_rows).items())
        ),
        "mixed_isomorphism_classes": len(representatives),
        "mixed_isomorphic_topology_key_conflicts": len(conflicts),
        "false_rows": false_rows,
        "mixed_key_conflicts": conflicts,
        "conclusion": (
            "A claimed pointwise tree--sunlet separation cannot coexist with an "
            "exact labelled semi-directed isomorphism or ordinary-triangle relation. "
            "The rooted clean-restriction oracle is therefore revoked."
        ),
    }
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: report[key] for key in (
        "status", "false_topology_oracle_count",
        "mixed_isomorphic_topology_key_conflicts", "payload_sha256"
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
