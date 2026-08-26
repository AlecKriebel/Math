#!/usr/bin/env python3
"""Fail-closed independent replay of the physical probe input contract.

This verifier deliberately does not import ``build_probe_input_contract``.  It
reconstructs every labelled source/target graph from the upstream locators,
replays the four-port omitted-role recursion, checks exact mixed-graph
relations and transports, and independently enumerates every suppressed
semi-directed edge available for a physical probe insertion.
"""

from __future__ import annotations

import argparse
import ast
import collections
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CONTRACT = HERE / "probe_input_contract.json"
REPORT = HERE / "probe_input_independent_verification.json"
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
RAW4 = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
RESULT4 = PROJECT / "package/referee/k2p_offline_sweep_portable/results/four_port_release_v4"
THETA2 = PROJECT / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz"
CYCLE = PROJECT / "work/cycle_three_port_closure"
CYCLE_ANCHORS = CYCLE / "artifacts/physical_anchors.json"
CYCLE_FULL = CYCLE / "artifacts/full_completion_ledger.jsonl.gz"
CYCLE_PROMOTION = CYCLE / "promotion/cycle_promotion_certificate.json"


class VerificationFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_digest(path):
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"module:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def graph_digest(graph):
    payload = {
        "nodes": [
            [repr(node), {key: repr(value) for key, value in sorted(data.items())}]
            for node, data in sorted(graph.nodes(data=True), key=lambda item: repr(item[0]))
        ],
        "edges": [
            [repr(tail), repr(head), {key: repr(value) for key, value in sorted(data.items())}]
            for tail, head, data in sorted(
                graph.edges(data=True), key=lambda item: (repr(item[0]), repr(item[1]))
            )
        ],
    }
    return digest(payload)


def labelled_ports(graph):
    return tuple(sorted(
        data["label"] for _, data in graph.nodes(data=True)
        if isinstance(data.get("label"), int)
    ))


def insert_arc(graph, record, label, namespace):
    tail, head = ast.literal_eval(record["tail"]), ast.literal_eval(record["head"])
    require(graph.has_edge(tail, head), f"insertion arc:{tail}:{head}")
    result = graph.copy()
    attrs = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = (namespace, "subdivision", label, repr(tail), repr(head))
    leaf = (namespace, "leaf", label, repr(tail), repr(head))
    require(subdivision not in result and leaf not in result, "insertion collision")
    result.add_node(subdivision, role="tree", label=None, dummy=False, dummy_name=None)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **attrs)
    result.add_edge(subdivision, head, **attrs)
    result.add_edge(subdivision, leaf, edge_role="arm")
    require(nx.is_directed_acyclic_graph(result), "inserted cycle")
    return result


def promote(graph, assignments):
    result = graph.copy()
    for role, label in assignments:
        nodes = [node for node, data in result.nodes(data=True) if data.get("dummy_name") == role]
        require(len(nodes) == 1, f"dummy role:{role}:{nodes}")
        result.nodes[nodes[0]].update(label=label, dummy=False, dummy_name=None)
    return result


def rooted_candidates(graph):
    return [
        {"tail": repr(tail), "head": repr(head), "edge_role": data.get("edge_role")}
        for tail, head, data in sorted(
            graph.edges(data=True), key=lambda item: (repr(item[0]), repr(item[1]))
        )
        if graph.nodes[tail].get("role") != "root"
        and graph.nodes[head].get("role") != "leaf"
    ]


def edge_tuple(left, right):
    return tuple(sorted((repr(left), repr(right))))


def triangle_sets(mixed):
    rows = []
    for nodes in itertools.combinations(sorted(mixed.nodes(), key=repr), 3):
        if not all(mixed.has_edge(*pair) for pair in itertools.combinations(nodes, 2)):
            continue
        edges = frozenset(frozenset(pair) for pair in itertools.combinations(nodes, 2))
        arrowheads = []
        for edge in edges:
            left, right = tuple(edge)
            heads = mixed.edges[left, right].get("heads", frozenset())
            require(len(heads) <= 1, "two-headed triangle edge")
            arrowheads.extend(heads)
        if len(arrowheads) == 2 and arrowheads[0] == arrowheads[1]:
            rows.append(edges)
    return rows


def incidence_graph(mixed, erased_triangle=None):
    erased_triangle = frozenset() if erased_triangle is None else erased_triangle
    result, lookup = nx.Graph(), {}
    for node, data in mixed.nodes(data=True):
        result.add_node(("vertex", node), kind="vertex", label=data.get("label"), erased=False)
    for index, (left, right, data) in enumerate(sorted(
        mixed.edges(data=True), key=lambda item: (repr(item[0]), repr(item[1]))
    )):
        edge_node = ("edge", index)
        edge = frozenset((left, right))
        lookup[edge_node] = edge
        erased = edge in erased_triangle
        result.add_node(edge_node, kind="edge", label=None, erased=erased)
        heads = data.get("heads", frozenset())
        result.add_edge(edge_node, ("vertex", left), head=False if erased else left in heads)
        result.add_edge(edge_node, ("vertex", right), head=False if erased else right in heads)
    return result, lookup


def exact_transports(atlas, source, target, relation):
    source_mixed, target_mixed = atlas.sd0_mixed(source), atlas.sd0_mixed(target)
    pairs = [(None, None)] if relation == "isomorphic" else list(itertools.product(
        triangle_sets(source_mixed), triangle_sets(target_mixed)
    ))
    node_match = lambda left, right: (
        left.get("kind") == right.get("kind")
        and left.get("label") == right.get("label")
        and left.get("erased") == right.get("erased")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")
    transports = {}
    for source_triangle, target_triangle in pairs:
        left_graph, left_edges = incidence_graph(source_mixed, source_triangle)
        right_graph, right_edges = incidence_graph(target_mixed, target_triangle)
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            left_graph, right_graph, node_match=node_match, edge_match=edge_match
        )
        for mapping in matcher.isomorphisms_iter():
            vertex_map = {
                node: mapping[("vertex", node)][1] for node in source_mixed.nodes()
            }
            edge_map = {left_edges[node]: right_edges[mapping[node]] for node in left_edges}
            public = {
                "relation": relation,
                "vertex_map": [[repr(left), repr(right)] for left, right in sorted(
                    vertex_map.items(), key=lambda item: repr(item[0])
                )],
                "mixed_edge_map": [
                    [list(edge_tuple(*tuple(left))), list(edge_tuple(*tuple(right)))]
                    for left, right in sorted(edge_map.items(), key=lambda item: edge_tuple(*tuple(item[0])))
                ],
                "source_triangle_edges": None if source_triangle is None else sorted(
                    [list(edge_tuple(*tuple(edge))) for edge in source_triangle]
                ),
                "target_triangle_edges": None if target_triangle is None else sorted(
                    [list(edge_tuple(*tuple(edge))) for edge in target_triangle]
                ),
            }
            public["transport_sha256"] = digest(public)
            transports[public["transport_sha256"]] = public
    return [transports[key] for key in sorted(transports)]


def root_half_graph(graph, child, label, namespace):
    root = next(node for node, data in graph.nodes(data=True) if data.get("role") == "root")
    return insert_arc(graph, {
        "tail": repr(root), "head": repr(child), "edge_role": graph.edges[root, child].get("edge_role")
    }, label, namespace)


def independently_enumerate_sites(atlas, graph):
    mixed = atlas.sd0_mixed(graph)
    root = next(node for node, data in graph.nodes(data=True) if data.get("role") == "root")
    root_children = tuple(graph.successors(root))
    require(len(root_children) == 2, "root degree")
    directed_lookup = {
        frozenset((tail, head)): (tail, head, data.get("edge_role"))
        for tail, head, data in graph.edges(data=True) if tail != root
    }
    rows = []
    root_edge = frozenset(root_children)
    for left, right, data in sorted(mixed.edges(data=True), key=lambda item: edge_tuple(item[0], item[1])):
        edge = frozenset((left, right))
        heads = data.get("heads", frozenset())
        if edge == root_edge and edge not in directed_lookup:
            site_type = "root_suppressed_segment"
            representatives = [
                [repr(root), repr(child), graph.edges[root, child].get("edge_role")]
                for child in sorted(root_children, key=repr)
            ]
        else:
            require(edge in directed_lookup, f"unexplained mixed edge:{edge}")
            tail, head, role = directed_lookup[edge]
            representatives = [[repr(tail), repr(head), role]]
            if graph.nodes[tail].get("role") == "leaf" or graph.nodes[head].get("role") == "leaf":
                site_type = "pendant_arm"
            elif heads:
                site_type = "reticulation_incoming"
            else:
                site_type = "core_unheaded"
        rows.append({
            "site_id": f"E:{digest(list(edge_tuple(left, right)))}",
            "mixed_endpoints": list(edge_tuple(left, right)),
            "arrowhead_endpoints": sorted(map(repr, heads)),
            "site_type": site_type,
            "rooted_representatives": representatives,
        })
    return rows


def tree_graph():
    graph = nx.DiGraph(name="three_port_tree")
    for node, role, label in (
        ("r", "root", None), ("v", "tree", None),
        ("L0", "leaf", 0), ("L1", "leaf", 1), ("L2", "leaf", 2),
    ):
        graph.add_node(node, role=role, label=label, dummy=False, dummy_name=None)
    graph.add_edges_from((
        ("r", "L0", {"edge_role": "incoming_arm"}),
        ("r", "v", {"edge_role": "incoming_core"}),
        ("v", "L1", {"edge_role": "arm"}),
        ("v", "L2", {"edge_role": "arm"}),
    ))
    return graph


def prepare_upstream(atlas, common, cycle_generator):
    four_sources = atlas.source_supports()
    four_targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    raw_by_id = {}
    with gzip.open(RAW4, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            raw_by_id[row["raw_id"]] = row
    with gzip.open(THETA2, "rt") as handle:
        theta = json.load(handle)
    theta_sources = atlas.source_supports(("theta2",))
    theta_targets = atlas.target_completions(5, True) + atlas.target_completions(5, False)
    theta_no_dummy = {row["anchor_id"]: row for row in theta["no_dummy_anchors"]}
    theta_roots = {row["base_raw_id"]: row for row in theta["restoration_roots"]}
    theta_six = {row["path_id"]: row for row in theta["six_port_rows"]}
    theta_seven = {row["path_id"]: row for row in theta["seven_port_rows"]}
    cycle_package = json.loads(CYCLE_ANCHORS.read_text())
    cycle_rows = {row["anchor_id"]: row for row in cycle_package["anchors"]}
    cycle_sources = tuple(atlas.source_supports(("cycle",)))
    cycle_targets = tuple(atlas.target_completions(3, True) + atlas.target_completions(3, False))
    cycle_permutations = tuple(itertools.permutations(range(3)))
    configurations = cycle_generator.build_source_configurations(atlas, cycle_sources)
    configuration_index = {
        (source_index, depth, tuple(row["placement_path"])): row["graph"]
        for (source_index, depth), rows in configurations.items() for row in rows
    }
    return {
        "four_sources": four_sources, "four_targets": four_targets, "raw_by_id": raw_by_id,
        "theta": theta, "theta_sources": theta_sources, "theta_targets": theta_targets,
        "theta_no_dummy": theta_no_dummy, "theta_roots": theta_roots,
        "theta_six": theta_six, "theta_seven": theta_seven,
        "cycle_rows": cycle_rows, "cycle_sources": cycle_sources,
        "cycle_targets": cycle_targets, "cycle_permutations": cycle_permutations,
        "cycle_configuration_index": configuration_index, "common": common,
    }


def reconstruct_anchor(atlas, upstream, anchor):
    origin, locator = anchor["origin"], anchor["locator"]
    if origin.startswith("four_port"):
        raw = upstream["raw_by_id"][locator["raw_id"]]
        require(raw["source_index"] == locator["source_index"], "four source locator")
        require(raw["target_index"] == locator["target_index"], "four target locator")
        source = upstream["four_sources"][raw["source_index"]].graph
        record = atlas.relabel_record(
            upstream["four_targets"][raw["target_index"]], tuple(raw["port_permutation"])
        )
        target = record.graph
        for depth, step in enumerate(locator.get("restoration_path", [])):
            require(step["label"] == 4 + depth, "four restored label order")
            source = insert_arc(
                source, step["source_insertion"], step["label"],
                f"four_anchor_restore_{locator['raw_id']}_{depth}_{step['source_insertion_index']}",
            )
            target = promote(target, ((step["restored_role"], step["label"]),))
        return source, target
    if origin == "theta2_physical_k5":
        row = upstream["theta_no_dummy"][locator["upstream_anchor_id"]]
        return (
            upstream["theta_sources"][row["source_index"]].graph,
            atlas.relabel_record(
                upstream["theta_targets"][row["target_index"]], tuple(row["port_permutation"])
            ).graph,
        )
    if origin == "theta2_physical_k6":
        row = upstream["theta_six"][locator["path_id"]]
        root = upstream["theta_roots"][row["base_raw_id"]]
        source = insert_arc(
            upstream["theta_sources"][row["source_index"]].graph,
            row["source_insertion"], 5, "theta2_k6",
        )
        target = atlas.relabel_record(
            upstream["theta_targets"][row["target_index"]], tuple(root["port_permutation"])
        ).graph
        return source, promote(target, ((row["restored_role"], 5),))
    if origin == "theta2_physical_k7":
        row = upstream["theta_seven"][locator["path_id"]]
        parent = upstream["theta_six"][row["parent_path_id"]]
        root = upstream["theta_roots"][row["base_raw_id"]]
        source = insert_arc(
            upstream["theta_sources"][row["source_index"]].graph,
            parent["source_insertion"], 5, "theta2_k7_first",
        )
        source = insert_arc(source, row["source_insertion"], 6, "theta2_k7_second")
        target = atlas.relabel_record(
            upstream["theta_targets"][row["target_index"]], tuple(root["port_permutation"])
        ).graph
        return source, promote(target, (
            (row["first_restored_role"], 5), (row["restored_role"], 6)
        ))
    if origin.startswith("cycle_"):
        row = upstream["cycle_rows"][locator["anchor_id"]]
        if row["origin"] == "base_no_dummy":
            source = upstream["cycle_sources"][row["source_index"]].graph
            target = atlas.relabel_record(
                upstream["cycle_targets"][row["target_index"]], tuple(row["port_permutation"])
            ).graph
        else:
            depth = len(row["dummy_roles_in_label_order"])
            source = upstream["cycle_configuration_index"][
                (row["source_index"], depth, tuple(row["source_placement_path"]))
            ]
            target = upstream["common"].relabel_and_promote_all(
                atlas, upstream["cycle_targets"][row["target_index"]],
                upstream["cycle_permutations"][row["permutation_index"]],
                tuple(row["dummy_roles_in_label_order"]),
            )
        return source, target
    require(origin == "tree_physical_k3", f"unknown origin:{origin}")
    graph = tree_graph()
    return graph, graph


def expected_four_anchor_ids(atlas, upstream):
    terminal_keys = set()
    manifest_hashes = {}
    for path in sorted(RESULT4.glob("source_*/residual_manifest.json")):
        manifest_hashes[str(path.relative_to(PROJECT))] = file_digest(path)
        manifest = json.loads(path.read_text())
        for row in manifest["records"]:
            if row["status"] in {"isomorphic", "triangle"}:
                terminal_keys.add((manifest["source_index"], row["canonical_class_id"]))
    members = [
        row for row in upstream["raw_by_id"].values()
        if (row["source_index"], row.get("class_id")) in terminal_keys
    ]
    require(len(terminal_keys) == 55 and len(members) == 80, "four terminal census")
    ids, tested, none_count, continuations = set(), 0, 0, 0
    physical_restored = 0
    for raw in sorted(members, key=lambda row: row["raw_id"]):
        source = upstream["four_sources"][raw["source_index"]].graph
        record = atlas.relabel_record(
            upstream["four_targets"][raw["target_index"]], tuple(raw["port_permutation"])
        )
        if not record.dummy_labels:
            ids.add(f"four:raw{raw['raw_id']}")
            continue
        states = [(source, record.graph, tuple(sorted(record.dummy_labels)), [])]
        while states:
            parent_source, parent_target, remaining, path = states.pop(0)
            for role in remaining:
                new_label = 4 + len(path)
                promoted = promote(parent_target, ((role, new_label),))
                selected = atlas.restrict_rooted(promoted, set(range(new_label + 1)))
                for insertion_index, candidate in enumerate(rooted_candidates(parent_source)):
                    tested += 1
                    child = insert_arc(
                        parent_source, candidate, new_label,
                        f"verify_four_complete_{raw['raw_id']}_{len(path)}_{insertion_index}",
                    )
                    relation = atlas.mixed_relation_exact(child, selected)
                    if relation not in {"isomorphic", "triangle"}:
                        none_count += 1
                        continue
                    child_path = path + [{
                        "restored_role": role, "source_insertion_index": insertion_index,
                        "source_insertion": candidate, "label": new_label,
                    }]
                    remaining_child = tuple(value for value in remaining if value != role)
                    if remaining_child:
                        continuations += 1
                        states.append((child, promoted, remaining_child, child_path))
                    else:
                        physical_restored += 1
                        ids.add(f"four-restored:raw{raw['raw_id']}:{digest(child_path)}")
    require((tested, none_count, continuations, physical_restored) == (564, 543, 4, 17),
            f"four recursion:{tested}:{none_count}:{continuations}:{physical_restored}")
    return ids, manifest_hashes


def expected_nonfour_anchor_ids(upstream):
    ids = set()
    theta = upstream["theta"]
    ids.update(f"theta2:k5:{row['anchor_id']}" for row in theta["no_dummy_anchors"])
    ids.update(
        f"theta2:k6:{row['path_id']}" for row in theta["six_port_rows"]
        if row["category"] == "isomorphic" and not row["remaining_roles"]
    )
    ids.update(
        f"theta2:k7:{row['path_id']}" for row in theta["seven_port_rows"]
        if row["category"] == "isomorphic"
    )
    ids.update(f"cycle:{anchor_id}" for anchor_id in upstream["cycle_rows"])
    ids.add("tree:k3:identity")
    return ids


def verify_profile(atlas, graph, profile, side, anchor_id):
    sites = independently_enumerate_sites(atlas, graph)
    require(profile["sites"] == sites, f"site enumeration:{anchor_id}:{side}")
    require(profile["site_count"] == len(sites), f"site count:{anchor_id}:{side}")
    require(profile["ordered_site_hash_root"] == digest([digest(row) for row in sites]),
            f"site hash root:{anchor_id}:{side}")
    k = len(labelled_ports(graph))
    r = sum(data.get("role") == "retic" for _, data in graph.nodes(data=True))
    require(len(sites) == 2 * k + 3 * r - 3, f"edge formula:{anchor_id}:{side}")
    types = collections.Counter(row["site_type"] for row in sites)
    require(profile["site_type_census"] == dict(sorted(types.items())),
            f"site types:{anchor_id}:{side}")
    require(types["root_suppressed_segment"] == 1, f"root site:{anchor_id}:{side}")
    require(types["pendant_arm"] == k - 1, f"pendant sites:{anchor_id}:{side}")
    require(types["reticulation_incoming"] == 2 * r, f"retic sites:{anchor_id}:{side}")
    root = next(node for node, data in graph.nodes(data=True) if data.get("role") == "root")
    children = sorted(graph.successors(root), key=lambda node: graph.nodes[node].get("role") != "leaf")
    label = max(labelled_ports(graph)) + 1
    first = root_half_graph(graph, children[0], label, f"verify_half_{side}_a")
    second = root_half_graph(graph, children[1], label, f"verify_half_{side}_b")
    require(atlas.mixed_relation_exact(first, second) == "isomorphic",
            f"root half relation:{anchor_id}:{side}")
    half = profile["root_half_equivalence"]
    require(half["semi_directed_relation_after_insertion"] == "isomorphic",
            f"root half reported:{anchor_id}:{side}")
    require(half["new_label"] == label, f"root half label:{anchor_id}:{side}")
    require(half["certificate_sha256"] == digest({
        key: value for key, value in half.items() if key != "certificate_sha256"
    }), f"root half hash:{anchor_id}:{side}")
    # Namespace names differ between builder and verifier, so graph digests are
    # validated through the exact relation and all public structural fields;
    # the stored two digests remain payload-bound provenance.
    return sites


def main():
    if not __debug__:
        raise SystemExit("PROBE_INPUT_VERIFY_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()
    contract = json.loads(args.contract.read_text())
    require(contract["schema"] == "k2p-root-invariant-probe-input-contract-v2", "schema")
    require(contract["status"] == "PASS", "status")
    payload = {key: value for key, value in contract.items() if key != "payload_sha256"}
    require(contract["payload_sha256"] == digest(payload), "payload hash")
    expected_inputs = {
        "atlas_sha256": file_digest(ATLAS_PATH),
        "raw4_ledger_sha256": file_digest(RAW4),
        "theta2_fixed_full_closure_sha256": file_digest(THETA2),
        "cycle_physical_anchors_sha256": file_digest(CYCLE_ANCHORS),
        "cycle_full_ledger_sha256": file_digest(CYCLE_FULL),
        "cycle_promotion_certificate_sha256": file_digest(CYCLE_PROMOTION),
        "cycle_common_sha256": file_digest(CYCLE / "cycle_common.py"),
        "cycle_generator_sha256": file_digest(CYCLE / "generate_cycle_closure.py"),
    }
    require(contract["inputs"] == expected_inputs, "input bindings")
    atlas = load_module("probe_verify_atlas", ATLAS_PATH)
    common = load_module("cycle_common", CYCLE / "cycle_common.py")
    cycle_generator = load_module("probe_verify_cycle_generator", CYCLE / "generate_cycle_closure.py")
    upstream = prepare_upstream(atlas, common, cycle_generator)
    expected_ids, manifest_hashes = expected_four_anchor_ids(atlas, upstream)
    expected_ids |= expected_nonfour_anchor_ids(upstream)
    anchors = contract["anchors"]
    require(len(anchors) == 176, f"anchor count:{len(anchors)}")
    require({row["anchor_id"] for row in anchors} == expected_ids, "anchor completeness")
    require(len(expected_ids) == len(anchors), "duplicate anchor ids")
    require(contract["ordered_anchor_row_hashes"] == [row["anchor_row_sha256"] for row in anchors],
            "ordered row hashes")
    require(contract["ordered_anchor_hash_root"] == digest(contract["ordered_anchor_row_hashes"]),
            "anchor hash root")
    relation_counts, origin_counts, port_counts = collections.Counter(), collections.Counter(), collections.Counter()
    site_counts, site_types = collections.Counter(), collections.Counter()
    four_regression = set()
    for anchor in anchors:
        anchor_id = anchor["anchor_id"]
        require(anchor["anchor_row_sha256"] == digest({
            key: value for key, value in anchor.items() if key != "anchor_row_sha256"
        }), f"anchor row hash:{anchor_id}")
        source, target = reconstruct_anchor(atlas, upstream, anchor)
        require(graph_digest(source) == anchor["source_graph_sha256"], f"source graph:{anchor_id}")
        require(graph_digest(target) == anchor["target_graph_sha256"], f"target graph:{anchor_id}")
        require(list(labelled_ports(source)) == anchor["labels"] == list(labelled_ports(target)),
                f"labels:{anchor_id}")
        relation = atlas.mixed_relation_exact(source, target)
        require(relation == anchor["relation"] and relation in {"isomorphic", "triangle"},
                f"exact relation:{anchor_id}:{relation}")
        transports = exact_transports(atlas, source, target, relation)
        require(len(transports) == 1, f"transport uniqueness:{anchor_id}:{len(transports)}")
        require(transports[0] == anchor["parent_transport"], f"parent transport:{anchor_id}")
        source_sites = verify_profile(
            atlas, source, anchor["source_candidate_profile"], "source", anchor_id
        )
        target_sites = verify_profile(
            atlas, target, anchor["target_candidate_profile"], "target", anchor_id
        )
        source_site_ids = {row["site_id"] for row in source_sites}
        target_site_ids = {row["site_id"] for row in target_sites}
        transport = anchor["site_transport"]
        require(anchor["site_transport_sha256"] == digest(transport), f"site transport hash:{anchor_id}")
        require({row["source_site_id"] for row in transport} == source_site_ids,
                f"source transport coverage:{anchor_id}")
        require({row["target_site_id"] for row in transport} == target_site_ids,
                f"target transport coverage:{anchor_id}")
        require(len(transport) == len(source_site_ids) == len(target_site_ids),
                f"transport bijection:{anchor_id}")
        relation_counts[relation] += 1
        origin_counts[anchor["origin"]] += 1
        port_counts[len(anchor["labels"])] += 1
        site_counts["source"] += len(source_sites)
        site_counts["target"] += len(target_sites)
        site_types.update({f"source:{key}": value for key, value in collections.Counter(
            row["site_type"] for row in source_sites
        ).items()})
        site_types.update({f"target:{key}": value for key, value in collections.Counter(
            row["site_type"] for row in target_sites
        ).items()})
        if anchor["locator"].get("raw_id") in {67161, 67167, 67401, 67407}:
            four_regression.add(anchor["locator"]["raw_id"])
            require(anchor["origin"] == "four_port_restored_physical_k5", "regression origin")
            require(anchor["relation"] == "triangle", "regression relation")
    expected_origin = {
        "four_port_direct_physical": 26, "four_port_restored_physical_k5": 17,
        "theta2_physical_k5": 24, "theta2_physical_k6": 40, "theta2_physical_k7": 32,
        "cycle_physical_k3": 24, "cycle_restored_physical_k4": 12,
        "tree_physical_k3": 1,
    }
    require(dict(origin_counts) == expected_origin, f"origin census:{origin_counts}")
    require(relation_counts == {"isomorphic": 143, "triangle": 33}, f"relations:{relation_counts}")
    require(port_counts == {3: 25, 4: 38, 5: 41, 6: 40, 7: 32}, f"ports:{port_counts}")
    require(site_counts == {"source": 2206, "target": 2206}, f"sites:{site_counts}")
    require(sum(
        row["source_candidate_profile"]["site_count"]
        * row["target_candidate_profile"]["site_count"] for row in anchors
    ) == 29964, "first probe pair census")
    require(four_regression == {67161, 67167, 67401, 67407}, "four-row regression binding")
    require(contract["anchor_census"]["four_port"]["manifest_hashes"] == manifest_hashes,
            "four manifest bindings")
    require(contract["unresolved_anchor_inputs"] == 0, "unresolved anchors")
    require(contract["incoherent_site_transports"] == 0, "incoherent transports")
    report = {
        "schema": "k2p-probe-input-independent-replay-v1",
        "status": "PASS",
        "contract_sha256": file_digest(args.contract),
        "contract_payload_sha256": contract["payload_sha256"],
        "anchors_reconstructed": len(anchors),
        "exact_relations_replayed": len(anchors),
        "unique_parent_transports_replayed": len(anchors),
        "root_half_equivalences_replayed": 2 * len(anchors),
        "source_sites_reenumerated": site_counts["source"],
        "target_sites_reenumerated": site_counts["target"],
        "first_probe_source_target_pairs": 29964,
        "origin_census": dict(sorted(origin_counts.items())),
        "relation_census": dict(sorted(relation_counts.items())),
        "port_census": {str(key): value for key, value in sorted(port_counts.items())},
        "site_type_census": dict(sorted(site_types.items())),
        "four_terminal_classes": 55,
        "four_terminal_member_roots": 80,
        "four_omitted_role_children_replayed": 564,
        "four_exact_none_children": 543,
        "four_equality_continuations": 4,
        "four_restored_physical_equalities": 17,
        "new_triangle_regression_raw_ids": sorted(four_regression),
        "missing_anchors": 0,
        "extra_anchors": 0,
        "unresolved": 0,
    }
    report["payload_sha256"] = digest(report)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS", "anchors": len(anchors), "sites_per_side": site_counts["source"],
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (VerificationFailure, KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PROBE_INPUT_VERIFY_FAIL:{exc}") from exc
