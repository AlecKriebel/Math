#!/usr/bin/env python3
"""Build an adversarial, root-invariant input contract for coherent probes.

This is not the full probe computation.  It independently reconstructs every
physical equality anchor from clean closure outputs and defines attachment
sites on *all* edges of the suppressed semi-directed graph.  Thus pendant
arms and reticulation-incoming edges are included, while the two rooted halves
of the artificial-root segment are one certified site.
"""

from __future__ import annotations

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
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
RAW4 = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
RESULT4 = PROJECT / "package/referee/k2p_offline_sweep_portable/results/four_port_release_v4"
THETA2 = PROJECT / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz"
CYCLE = PROJECT / "work/cycle_three_port_closure"
CYCLE_ANCHORS = CYCLE / "artifacts/physical_anchors.json"
CYCLE_FULL = CYCLE / "artifacts/full_completion_ledger.jsonl.gz"
CYCLE_PROMOTION = CYCLE / "promotion/cycle_promotion_certificate.json"
OUTPUT = HERE / "probe_input_contract.json"


class ContractFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ContractFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def import_module(name, path):
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None, f"import:{path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def load_modules():
    atlas = import_module("probe_contract_atlas", ATLAS_PATH)
    common = import_module("cycle_common", CYCLE / "cycle_common.py")
    generator = import_module("probe_contract_cycle_generator", CYCLE / "generate_cycle_closure.py")
    return atlas, common, generator


def graph_payload(graph):
    return {
        "nodes": [
            [repr(node), {key: repr(value) for key, value in sorted(data.items())}]
            for node, data in sorted(graph.nodes(data=True), key=lambda row: repr(row[0]))
        ],
        "edges": [
            [repr(tail), repr(head), {key: repr(value) for key, value in sorted(data.items())}]
            for tail, head, data in sorted(graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1])))
        ],
    }


def labels(graph):
    return tuple(sorted(
        data["label"] for _, data in graph.nodes(data=True)
        if isinstance(data.get("label"), int)
    ))


def insert_on_arc(graph, tail, head, label, namespace):
    require(graph.has_edge(tail, head), f"missing insertion arc:{tail}:{head}")
    result = graph.copy()
    data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = (namespace, "subdivision", label, repr(tail), repr(head))
    leaf = (namespace, "leaf", label, repr(tail), repr(head))
    require(subdivision not in result and leaf not in result, "insertion node collision")
    result.add_node(subdivision, role="tree", label=None, dummy=False, dummy_name=None)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **data)
    result.add_edge(subdivision, head, **data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    require(nx.is_directed_acyclic_graph(result), "insertion cycle")
    expected = {"root": (0, 2), "tree": (1, 2), "retic": (2, 1), "leaf": (1, 0)}
    for node, node_data in result.nodes(data=True):
        require(
            (result.in_degree(node), result.out_degree(node)) == expected[node_data["role"]],
            f"nonbinary insertion:{node}",
        )
    return result


def insert_from_record(graph, record, label, namespace):
    return insert_on_arc(
        graph, ast.literal_eval(record["tail"]), ast.literal_eval(record["head"]), label, namespace
    )


def rooted_core_candidates(graph):
    """The historical fixed-full grammar: core arcs only, in stable order."""
    return [
        {"tail": repr(tail), "head": repr(head), "edge_role": data.get("edge_role")}
        for tail, head, data in sorted(
            graph.edges(data=True), key=lambda item: (repr(item[0]), repr(item[1]))
        )
        if graph.nodes[tail].get("role") != "root"
        and graph.nodes[head].get("role") != "leaf"
    ]


def promote_roles(graph, role_labels):
    result = graph.copy()
    for role, label in role_labels:
        matches = [node for node, data in result.nodes(data=True) if data.get("dummy_name") == role]
        require(len(matches) == 1, f"dummy role multiplicity:{role}:{matches}")
        result.nodes[matches[0]].update(label=label, dummy=False, dummy_name=None)
    return result


def edge_key(left, right):
    return tuple(sorted((repr(left), repr(right))))


def ordinary_triangles(mixed):
    answer = []
    for a, b, c in itertools.combinations(sorted(mixed.nodes(), key=repr), 3):
        if not (mixed.has_edge(a, b) and mixed.has_edge(a, c) and mixed.has_edge(b, c)):
            continue
        edges = frozenset((frozenset((a, b)), frozenset((a, c)), frozenset((b, c))))
        heads = []
        for edge in edges:
            left, right = tuple(edge)
            values = mixed.edges[left, right].get("heads", frozenset())
            require(len(values) <= 1, "two-headed triangle edge")
            if values:
                heads.append(next(iter(values)))
        if len(heads) == 2 and heads[0] == heads[1]:
            answer.append({"edges": edges, "reticulation": heads[0]})
    return answer


def incidence(mixed, triangle=None):
    triangle = frozenset() if triangle is None else triangle
    result = nx.Graph()
    edge_lookup = {}
    for node, data in mixed.nodes(data=True):
        result.add_node(("v", node), kind="vertex", label=data.get("label"), triangle_edge=False)
    for number, (left, right, data) in enumerate(
        sorted(mixed.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1])))
    ):
        edge = frozenset((left, right))
        edge_node = ("e", number)
        edge_lookup[edge_node] = edge
        is_triangle = edge in triangle
        result.add_node(edge_node, kind="edge", label=None, triangle_edge=is_triangle)
        heads = data.get("heads", frozenset())
        result.add_edge(edge_node, ("v", left), head=False if is_triangle else left in heads)
        result.add_edge(edge_node, ("v", right), head=False if is_triangle else right in heads)
    return result, edge_lookup


def exact_relation(atlas, source, target):
    relation = atlas.mixed_relation_exact(source, target)
    require(relation in {"isomorphic", "triangle", "none", None}, f"unknown relation:{relation}")
    if relation in {"none", None}:
        return "none", []
    source_mixed, target_mixed = atlas.sd0_mixed(source), atlas.sd0_mixed(target)
    if relation == "isomorphic":
        triangle_pairs = [(None, None)]
    else:
        triangle_pairs = [
            (left["edges"], right["edges"])
            for left in ordinary_triangles(source_mixed)
            for right in ordinary_triangles(target_mixed)
        ]
    node_match = lambda left, right: (
        left.get("kind") == right.get("kind")
        and left.get("label") == right.get("label")
        and left.get("triangle_edge") == right.get("triangle_edge")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")
    records = {}
    for source_triangle, target_triangle in triangle_pairs:
        source_incidence, source_edges = incidence(source_mixed, source_triangle)
        target_incidence, target_edges = incidence(target_mixed, target_triangle)
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            source_incidence, target_incidence, node_match=node_match, edge_match=edge_match
        )
        for mapping in matcher.isomorphisms_iter():
            vertex_map = {
                node: mapping[("v", node)][1] for node in source_mixed.nodes()
            }
            mixed_edge_map = {
                source_edges[node]: target_edges[mapping[node]] for node in source_edges
            }
            public = {
                "relation": relation,
                "vertex_map": [
                    [repr(source_node), repr(target_node)]
                    for source_node, target_node in sorted(vertex_map.items(), key=lambda row: repr(row[0]))
                ],
                "mixed_edge_map": [
                    [list(edge_key(*tuple(source_edge))), list(edge_key(*tuple(target_edge)))]
                    for source_edge, target_edge in sorted(
                        mixed_edge_map.items(), key=lambda row: edge_key(*tuple(row[0]))
                    )
                ],
                "source_triangle_edges": None if source_triangle is None else sorted(
                    [list(edge_key(*tuple(edge))) for edge in source_triangle]
                ),
                "target_triangle_edges": None if target_triangle is None else sorted(
                    [list(edge_key(*tuple(edge))) for edge in target_triangle]
                ),
            }
            public["transport_sha256"] = sha(public)
            records[public["transport_sha256"]] = {
                "public": public, "vertex_map": vertex_map, "edge_map": mixed_edge_map,
                "source_triangle": source_triangle, "target_triangle": target_triangle,
            }
    return relation, [records[key] for key in sorted(records)]


def site_profile(atlas, graph):
    mixed = atlas.sd0_mixed(graph)
    root = next(node for node, data in graph.nodes(data=True) if data.get("role") == "root")
    root_children = tuple(graph.successors(root))
    require(len(root_children) == 2, "root child census")
    direct = {}
    for tail, head, data in graph.edges(data=True):
        if tail == root:
            continue
        direct[frozenset((tail, head))] = (tail, head, data.get("edge_role"))
    sites = []
    half_certificate = None
    for left, right, data in sorted(mixed.edges(data=True), key=lambda row: edge_key(row[0], row[1])):
        edge = frozenset((left, right))
        heads = data.get("heads", frozenset())
        if edge in direct:
            tail, head, role = direct[edge]
            representatives = [[repr(tail), repr(head), role]]
            if graph.nodes[head].get("role") == "leaf" or graph.nodes[tail].get("role") == "leaf":
                site_type = "pendant_arm"
            elif heads:
                site_type = "reticulation_incoming"
            else:
                site_type = "core_unheaded"
        else:
            require(edge == frozenset(root_children), f"unexplained suppressed edge:{edge}")
            representatives = [
                [repr(root), repr(child), graph.edges[root, child].get("edge_role")]
                for child in sorted(root_children, key=repr)
            ]
            site_type = "root_suppressed_segment"
            label = max(labels(graph)) + 1
            children = sorted(root_children, key=lambda node: graph.nodes[node].get("role") != "leaf")
            first = insert_on_arc(graph, root, children[0], label, "root_half_audit_a")
            second = insert_on_arc(graph, root, children[1], label, "root_half_audit_b")
            half_relation = atlas.mixed_relation_exact(first, second)
            require(half_relation == "isomorphic", f"root half inequivalence:{half_relation}")
            half_certificate = {
                "new_label": label,
                "representative_half_arcs": representatives,
                "semi_directed_relation_after_insertion": half_relation,
                "first_graph_sha256": sha(graph_payload(first)),
                "second_graph_sha256": sha(graph_payload(second)),
            }
            half_certificate["certificate_sha256"] = sha(half_certificate)
        row = {
            "site_id": f"E:{sha(list(edge_key(left, right)))}",
            "mixed_endpoints": list(edge_key(left, right)),
            "arrowhead_endpoints": sorted(map(repr, heads)),
            "site_type": site_type,
            "rooted_representatives": representatives,
        }
        sites.append(row)
    k = len(labels(graph))
    r = sum(data.get("role") == "retic" for _, data in graph.nodes(data=True))
    counts = collections.Counter(row["site_type"] for row in sites)
    require(len(sites) == 2 * k + 3 * r - 3, f"mixed edge formula:{k}:{r}:{len(sites)}")
    require(counts["root_suppressed_segment"] == 1, "root segment count")
    require(counts["pendant_arm"] + 1 == k, f"pendant site count:{counts}:{k}")
    require(counts["reticulation_incoming"] == 2 * r, f"retic incoming count:{counts}:{r}")
    require(half_certificate is not None, "missing root-half certificate")
    return {
        "port_count": k, "reticulation_count": r,
        "all_mixed_edge_sites_included": True,
        "site_count": len(sites), "site_type_census": dict(sorted(counts.items())),
        "root_half_equivalence": half_certificate,
        "sites": sites,
        "ordered_site_hash_root": sha([sha(row) for row in sites]),
    }


def profile_edge_lookup(profile):
    return {tuple(row["mixed_endpoints"]): row for row in profile["sites"]}


def anchor_record(atlas, anchor_id, origin, source, target, locator):
    status, transports = exact_relation(atlas, source, target)
    require(status in {"isomorphic", "triangle"}, f"anchor not equality:{anchor_id}:{status}")
    require(len(transports) == 1, f"anchor transport multiplicity:{anchor_id}:{len(transports)}")
    transport = transports[0]
    source_profile, target_profile = site_profile(atlas, source), site_profile(atlas, target)
    require(source_profile["site_count"] == target_profile["site_count"], f"site count mismatch:{anchor_id}")
    source_lookup, target_lookup = profile_edge_lookup(source_profile), profile_edge_lookup(target_profile)
    site_transport = []
    for source_edge, target_edge in transport["edge_map"].items():
        source_key, target_key = edge_key(*tuple(source_edge)), edge_key(*tuple(target_edge))
        require(source_key in source_lookup and target_key in target_lookup, f"transport site omission:{anchor_id}")
        site_transport.append({
            "source_site_id": source_lookup[source_key]["site_id"],
            "target_site_id": target_lookup[target_key]["site_id"],
            "source_site_type": source_lookup[source_key]["site_type"],
            "target_site_type": target_lookup[target_key]["site_type"],
        })
    site_transport.sort(key=lambda row: (row["source_site_id"], row["target_site_id"]))
    require(len(site_transport) == source_profile["site_count"], f"site transport coverage:{anchor_id}")
    require(len({row["source_site_id"] for row in site_transport}) == len(site_transport), "source site transport collision")
    require(len({row["target_site_id"] for row in site_transport}) == len(site_transport), "target site transport collision")
    record = {
        "anchor_id": anchor_id, "origin": origin, "relation": status,
        "labels": list(labels(source)), "source_graph_sha256": sha(graph_payload(source)),
        "target_graph_sha256": sha(graph_payload(target)), "locator": locator,
        "source_candidate_profile": source_profile,
        "target_candidate_profile": target_profile,
        "parent_transport": transport["public"],
        "site_transport": site_transport,
        "site_transport_sha256": sha(site_transport),
    }
    record["anchor_row_sha256"] = sha(record)
    return record


def four_port_anchors(atlas):
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    terminal_keys = set()
    manifest_hashes = {}
    for path in sorted(RESULT4.glob("source_*/residual_manifest.json")):
        manifest_hashes[str(path.relative_to(PROJECT))] = sha_file(path)
        manifest = json.loads(path.read_text())
        source_index = manifest["source_index"]
        for record in manifest["records"]:
            if record["status"] in {"isomorphic", "triangle"}:
                terminal_keys.add((source_index, record["canonical_class_id"]))
    require(len(terminal_keys) == 55, "four terminal class census")
    members = []
    with gzip.open(RAW4, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if (row["source_index"], row.get("class_id")) in terminal_keys:
                members.append(row)
    require(len(members) == 80, "four terminal member census")
    anchors = []
    direct_count = 0
    restoration_requests = 0
    exact_none_children = 0
    equality_continuations = 0
    equality_states_by_depth = collections.Counter()
    for row in members:
        source = sources[row["source_index"]].graph
        record = atlas.relabel_record(targets[row["target_index"]], tuple(row["port_permutation"]))
        if not record.dummy_labels:
            anchors.append(anchor_record(
                atlas, f"four:raw{row['raw_id']}", "four_port_direct_physical",
                source, record.graph,
                {"raw_id": row["raw_id"], "source_index": row["source_index"],
                 "target_index": row["target_index"], "permutation_index": row["permutation_index"]},
            ))
            direct_count += 1
            continue
        initial_status, initial_transports = exact_relation(
            atlas, source, atlas.selected_graph_from_completion(record)
        )
        require(initial_status in {"isomorphic", "triangle"} and len(initial_transports) == 1,
                "four omitted parent relation")
        states = [
            {
                "source": source,
                "target_full": record.graph,
                "remaining": tuple(sorted(record.dummy_labels)),
                "path": [],
                "transport": initial_transports[0],
            }
        ]
        while states:
            state = states.pop(0)
            depth = len(state["path"])
            equality_states_by_depth[depth] += 1
            core_candidates = rooted_core_candidates(state["source"])
            expected = 7 + depth
            require(len(core_candidates) == expected, f"four restoration core candidates:{depth}")
            new_label = 4 + depth
            for role in state["remaining"]:
                promoted_full = promote_roles(state["target_full"], ((role, new_label),))
                remaining = tuple(value for value in state["remaining"] if value != role)
                selected_target = atlas.restrict_rooted(
                    promoted_full, set(range(new_label + 1))
                )
                for insertion_index, candidate in enumerate(core_candidates):
                    restoration_requests += 1
                    child = insert_from_record(
                        state["source"], candidate, new_label,
                        f"four_anchor_restore_{row['raw_id']}_{depth}_{insertion_index}",
                    )
                    relation = atlas.mixed_relation_exact(child, selected_target)
                    if relation not in {"isomorphic", "triangle"}:
                        exact_none_children += 1
                        continue
                    child_status, child_transports = exact_relation(atlas, child, selected_target)
                    require(child_status == relation and len(child_transports) == 1,
                            "four continuation transport")
                    path = state["path"] + [{
                        "restored_role": role,
                        "source_insertion_index": insertion_index,
                        "source_insertion": candidate,
                        "label": new_label,
                    }]
                    if remaining:
                        equality_continuations += 1
                        states.append({
                            "source": child, "target_full": promoted_full,
                            "remaining": remaining, "path": path,
                            "transport": child_transports[0],
                        })
                    else:
                        require(not [
                            data for _, data in promoted_full.nodes(data=True) if data.get("dummy")
                        ], "four physical anchor retains dummy")
                        anchors.append(anchor_record(
                            atlas,
                            f"four-restored:raw{row['raw_id']}:{sha(path)}",
                            f"four_port_restored_physical_k{new_label + 1}",
                            child, promoted_full,
                            {"raw_id": row["raw_id"], "source_index": row["source_index"],
                             "target_index": row["target_index"],
                             "permutation_index": row["permutation_index"],
                             "restoration_path": path},
                        ))
    restored_count = len(anchors) - direct_count
    require(restoration_requests >= 532 and exact_none_children + equality_continuations + restored_count == restoration_requests,
            "four restoration accounting")
    return anchors, {
        "terminal_classes": len(terminal_keys), "terminal_member_roots": len(members),
        "direct_physical": direct_count, "restoration_children_exact_tested": restoration_requests,
        "restoration_children_exact_none": exact_none_children,
        "equality_continuations": equality_continuations,
        "equality_states_by_depth": {str(key): value for key, value in sorted(equality_states_by_depth.items())},
        "restored_physical_equalities": restored_count,
        "manifest_hashes": manifest_hashes,
    }


def theta2_anchors(atlas):
    with gzip.open(THETA2, "rt") as handle:
        closure = json.load(handle)
    sources = atlas.source_supports(("theta2",))
    targets = atlas.target_completions(5, True) + atlas.target_completions(5, False)
    roots = {row["base_raw_id"]: row for row in closure["restoration_roots"]}
    six_by_path = {row["path_id"]: row for row in closure["six_port_rows"]}
    anchors = []
    for row in closure["no_dummy_anchors"]:
        source = sources[row["source_index"]].graph
        target = atlas.relabel_record(
            targets[row["target_index"]], tuple(row["port_permutation"])
        ).graph
        anchors.append(anchor_record(
            atlas, f"theta2:k5:{row['anchor_id']}", "theta2_physical_k5", source, target,
            {"base_raw_id": row["base_raw_id"], "upstream_anchor_id": row["anchor_id"]},
        ))
    for row in closure["six_port_rows"]:
        if row["category"] != "isomorphic" or row["remaining_roles"]:
            continue
        root = roots[row["base_raw_id"]]
        source = insert_from_record(
            sources[row["source_index"]].graph, row["source_insertion"], 5, "theta2_k6"
        )
        target_record = atlas.relabel_record(
            targets[row["target_index"]], tuple(root["port_permutation"])
        )
        target = promote_roles(target_record.graph, ((row["restored_role"], 5),))
        require(not [data for _, data in target.nodes(data=True) if data.get("dummy")], "theta2 k6 dummy")
        anchors.append(anchor_record(
            atlas, f"theta2:k6:{row['path_id']}", "theta2_physical_k6", source, target,
            {"base_raw_id": row["base_raw_id"], "path_id": row["path_id"],
             "upstream_anchor_id": row["anchor_id"], "certificate_id": row["certificate_id"]},
        ))
    for row in closure["seven_port_rows"]:
        if row["category"] != "isomorphic":
            continue
        parent = six_by_path[row["parent_path_id"]]
        root = roots[row["base_raw_id"]]
        source = insert_from_record(
            sources[row["source_index"]].graph, parent["source_insertion"], 5, "theta2_k7_first"
        )
        source = insert_from_record(source, row["source_insertion"], 6, "theta2_k7_second")
        target_record = atlas.relabel_record(
            targets[row["target_index"]], tuple(root["port_permutation"])
        )
        target = promote_roles(target_record.graph, (
            (row["first_restored_role"], 5), (row["restored_role"], 6)
        ))
        require(not [data for _, data in target.nodes(data=True) if data.get("dummy")], "theta2 k7 dummy")
        anchors.append(anchor_record(
            atlas, f"theta2:k7:{row['path_id']}", "theta2_physical_k7", source, target,
            {"base_raw_id": row["base_raw_id"], "path_id": row["path_id"],
             "parent_path_id": row["parent_path_id"], "upstream_anchor_id": row["anchor_id"],
             "certificate_id": row["certificate_id"]},
        ))
    by_origin = collections.Counter(row["origin"] for row in anchors)
    require(by_origin == {
        "theta2_physical_k5": 24, "theta2_physical_k6": 40, "theta2_physical_k7": 32
    }, f"theta2 anchor census:{by_origin}")
    upstream_ids_by_origin = {
        origin: len({
            row["locator"]["upstream_anchor_id"] for row in anchors if row["origin"] == origin
        }) for origin in sorted(by_origin)
    }
    return anchors, {
        "physical_anchor_census": dict(sorted(by_origin.items())),
        "unique_upstream_anchor_ids_by_origin": upstream_ids_by_origin,
        "note": "k7 has 32 restoration-path records and 16 upstream topology-anchor IDs",
        "clean_closure_census": closure["census"],
    }


def cycle_anchors(atlas, common, generator):
    package = json.loads(CYCLE_ANCHORS.read_text())
    sources = tuple(atlas.source_supports(("cycle",)))
    targets = tuple(atlas.target_completions(3, True) + atlas.target_completions(3, False))
    permutations = tuple(itertools.permutations(range(3)))
    configurations = generator.build_source_configurations(atlas, sources)
    configuration_index = {
        (source_index, depth, tuple(row["placement_path"])): row["graph"]
        for (source_index, depth), rows in configurations.items() for row in rows
    }
    anchors = []
    for row in package["anchors"]:
        if row["origin"] == "base_no_dummy":
            source = sources[row["source_index"]].graph
            target = atlas.relabel_record(
                targets[row["target_index"]], tuple(row["port_permutation"])
            ).graph
            origin = "cycle_physical_k3"
        else:
            depth = len(row["dummy_roles_in_label_order"])
            source = configuration_index[
                (row["source_index"], depth, tuple(row["source_placement_path"]))
            ]
            target = common.relabel_and_promote_all(
                atlas, targets[row["target_index"]], permutations[row["permutation_index"]],
                tuple(row["dummy_roles_in_label_order"]),
            )
            origin = f"cycle_restored_physical_k{row['port_count']}"
        anchor = anchor_record(
            atlas, f"cycle:{row['anchor_id']}", origin, source, target,
            {key: value for key, value in row.items() if key not in {"origin", "relation"}},
        )
        require(anchor["relation"] == row["relation"], f"cycle relation drift:{row['anchor_id']}")
        anchors.append(anchor)
    by_origin = collections.Counter(row["origin"] for row in anchors)
    require(by_origin == {"cycle_physical_k3": 24, "cycle_restored_physical_k4": 12},
            f"cycle anchor census:{by_origin}")
    return anchors, {"physical_anchor_census": dict(sorted(by_origin.items()))}


def tree_anchor(atlas):
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
    return [anchor_record(atlas, "tree:k3:identity", "tree_physical_k3", graph, graph, {})]


def main():
    atlas, common, generator = load_modules()
    four, four_report = four_port_anchors(atlas)
    theta2, theta2_report = theta2_anchors(atlas)
    cycle, cycle_report = cycle_anchors(atlas, common, generator)
    tree = tree_anchor(atlas)
    anchors = four + theta2 + cycle + tree
    by_origin = collections.Counter(row["origin"] for row in anchors)
    by_relation = collections.Counter(row["relation"] for row in anchors)
    by_port = collections.Counter(row["source_candidate_profile"]["port_count"] for row in anchors)
    candidate_counts = collections.Counter()
    type_counts = collections.Counter()
    first_probe_pairs = 0
    for row in anchors:
        source = row["source_candidate_profile"]
        target = row["target_candidate_profile"]
        candidate_counts["source"] += source["site_count"]
        candidate_counts["target"] += target["site_count"]
        first_probe_pairs += source["site_count"] * target["site_count"]
        type_counts.update({f"source:{key}": value for key, value in source["site_type_census"].items()})
        type_counts.update({f"target:{key}": value for key, value in target["site_type_census"].items()})
    require(len(anchors) == 176, f"total anchor census:{len(anchors)}")
    require(all(row["source_candidate_profile"]["all_mixed_edge_sites_included"] for row in anchors),
            "source site omission")
    require(all(row["target_candidate_profile"]["all_mixed_edge_sites_included"] for row in anchors),
            "target site omission")
    report = {
        "schema": "k2p-root-invariant-probe-input-contract-v2",
        "status": "PASS",
        "claim_boundary": (
            "This certifies the complete physical equality-anchor and attachment-site input universe. "
            "It does not classify the ensuing one-/two-port cross-products."
        ),
        "inputs": {
            "atlas_sha256": sha_file(ATLAS_PATH), "raw4_ledger_sha256": sha_file(RAW4),
            "theta2_fixed_full_closure_sha256": sha_file(THETA2),
            "cycle_physical_anchors_sha256": sha_file(CYCLE_ANCHORS),
            "cycle_full_ledger_sha256": sha_file(CYCLE_FULL),
            "cycle_promotion_certificate_sha256": sha_file(CYCLE_PROMOTION),
            "cycle_common_sha256": sha_file(CYCLE / "cycle_common.py"),
            "cycle_generator_sha256": sha_file(CYCLE / "generate_cycle_closure.py"),
        },
        "anchor_census": {
            "physical_equality_anchor_records": len(anchors),
            "unique_anchor_record_ids": len({row["anchor_id"] for row in anchors}),
            "by_origin": dict(sorted(by_origin.items())),
            "by_relation": dict(sorted(by_relation.items())),
            "by_port_count": {str(key): value for key, value in sorted(by_port.items())},
            "four_port": four_report, "theta2": theta2_report,
            "cycle": cycle_report, "tree": {"physical_anchor_census": 1},
        },
        "candidate_census": {
            "all_suppressed_semi_directed_edges_included": True,
            "source_sites": candidate_counts["source"], "target_sites": candidate_counts["target"],
            "first_probe_source_target_pairs": first_probe_pairs,
            "site_types": dict(sorted(type_counts.items())),
            "reticulation_incoming_edges_included": True,
            "pendant_arm_edges_included": True,
            "artificial_root_two_halves_quotiented": True,
            "per_graph_formula": "site_count = 2*k + 3*r - 3",
        },
        "root_movement_contract": {
            "canonical_object": "suppressed semi-directed mixed edge",
            "root_segment_rule": (
                "the two arcs leaving the artificial root represent one mixed edge; "
                "subdivision on either half is exactly semi-directed-isomorphic"
            ),
            "every_anchor_half_equivalences_certified": len(anchors) * 2,
            "parent_transport_maps_every_source_site_bijectively_to_a_target_site": True,
            "labelled_boundary_transport_compatible": True,
        },
        "required_probe_classifier_order": [
            "exact_labelled_isomorphism_or_ordinary_triangle_relation",
            "displayed_quartet_set_strict_separator",
            "direct_full_map_Ti_search_over_every_triple_and_orientation",
            "certified_multihomogeneous_algebra_fallback_or_unresolved",
        ],
        "forbidden_probe_shortcuts": [
            "rooted_restriction_type_as_proof", "triple_type_gate_before_full_map_Ti_search",
            "dropping_root-tail_arcs_without_half-quotient", "dropping_pendant_arms",
            "dropping_reticulation-incoming_arcs", "accepting_transport_not_restricting_parent",
        ],
        "anchors": anchors,
        "ordered_anchor_row_hashes": [row["anchor_row_sha256"] for row in anchors],
        "ordered_anchor_hash_root": sha([row["anchor_row_sha256"] for row in anchors]),
        "unresolved_anchor_inputs": 0,
        "incoherent_site_transports": 0,
    }
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"], "anchors": len(anchors),
        "source_sites": candidate_counts["source"], "target_sites": candidate_counts["target"],
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ContractFailure, KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PROBE_INPUT_CONTRACT_FAIL:{exc}") from exc
