#!/usr/bin/env python3
"""Exact fixed-full restoration of dummy-bearing theta2 isomorphism anchors."""

from __future__ import annotations

import ast
import collections
import itertools

from theta2_common import (
    exact_isomorphism_mapping,
    fail,
    record_metadata,
    sha_object,
    topology_decision,
    witness_id,
)


BRIDGE_MARGINAL_PROOF_SHA256 = "0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc"
BRIDGE_MARGINAL_CERTIFICATE_SHA256 = "9231a7b78c13e54b745eba68926276a6551c6c3512d6a85746baba6613c1aacf"
BRIDGE_MARGINAL_REPLAYER_SHA256 = "da9c56d0057b90ccf63588c4a8ce90ca4fd3ab8764013f2c44ffc66411079431"


def source_insertion_candidates(graph):
    rows = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        rows.append(
            {
                "tail": repr(tail),
                "head": repr(head),
                "edge_role": data.get("edge_role"),
            }
        )
    return rows


def insert_source_leaf(atlas, graph, candidate, label: int):
    result = graph.copy()
    tail = ast.literal_eval(candidate["tail"])
    head = ast.literal_eval(candidate["head"])
    if not result.has_edge(tail, head):
        fail("THETA2_RESTORATION_INSERTION_EDGE_MISSING", candidate)
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = ("theta2_restoration_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "theta2_restoration", label)
    if subdivision in result or leaf in result:
        fail("THETA2_RESTORATION_NODE_COLLISION", (subdivision, leaf))
    result.add_node(subdivision, role="tree", label=None, dummy=False)
    result.add_node(
        leaf, role="leaf", label=label, dummy=False, dummy_name=None
    )
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    atlas.validate_graph(result)
    return result


def promote_target_role(graph, role: str, label: int):
    result = graph.copy()
    nodes = [
        node
        for node, data in result.nodes(data=True)
        if data.get("dummy_name") == role
    ]
    if len(nodes) != 1:
        fail("THETA2_RESTORATION_TARGET_ROLE_FAIL", (role, nodes))
    node = nodes[0]
    result.nodes[node]["label"] = label
    result.nodes[node]["dummy"] = False
    result.nodes[node]["dummy_name"] = None
    return result


def exact_graph_matcher(atlas, left, right):
    node_match = (
        lambda x, y: x.get("kind") == y.get("kind")
        and x.get("label") == y.get("label")
    )
    edge_match = lambda x, y: x.get("head") == y.get("head")
    return atlas.nx.algorithms.isomorphism.GraphMatcher(
        left, right, node_match=node_match, edge_match=edge_match
    ).is_isomorphic()


class MixedGraphRegistry:
    """WL-bucketed registry whose membership test is exact isomorphism."""

    def __init__(self, atlas):
        self.atlas = atlas
        self.buckets = collections.defaultdict(list)
        self.representatives = []

    def add(self, graph):
        incidence = self.atlas.mixed_incidence_graph(self.atlas.sd0_mixed(graph))
        colored = incidence.copy()
        for _, data in colored.nodes(data=True):
            data["wl_color"] = f"{data.get('kind')}|{data.get('label')!r}"
        for _, _, data in colored.edges(data=True):
            data["wl_head"] = "1" if data.get("head") else "0"
        bucket = self.atlas.nx.weisfeiler_lehman_graph_hash(
            colored,
            node_attr="wl_color",
            edge_attr="wl_head",
            iterations=8,
        )
        for class_id in self.buckets[bucket]:
            if exact_graph_matcher(
                self.atlas, self.representatives[class_id], incidence
            ):
                return class_id
        class_id = len(self.representatives)
        self.representatives.append(incidence)
        self.buckets[bucket].append(class_id)
        return class_id


def classify_child(
    atlas,
    source_graph,
    selected_target_graph,
    topology_witnesses,
):
    source_signature = atlas.topology_signature(source_graph)
    target_signature = atlas.topology_signature(selected_target_graph)
    if source_signature[0] != target_signature[0]:
        fail(
            "THETA2_RESTORATION_LABEL_SET_FAIL",
            (source_signature[0], target_signature[0]),
        )
    content = topology_decision(
        source_signature, (target_signature[1], target_signature[2])
    )
    if content is not None:
        identifier = witness_id(content)
        previous = topology_witnesses.setdefault(identifier, content)
        if previous != content:
            fail("THETA2_RESTORATION_WITNESS_HASH_COLLISION", identifier)
        category = (
            "quartet_pointwise_excluded"
            if content["reason"] == "displayed_quartet_mismatch"
            else "tree_sunlet_pointwise_excluded"
        )
        return {
            "category": category,
            "certificate_id": identifier,
        }
    relation = atlas.mixed_relation_exact(source_graph, selected_target_graph)
    if relation != "isomorphic":
        fail("THETA2_RESTORATION_UNRESOLVED_CHILD", relation)
    mapping = exact_isomorphism_mapping(
        atlas, source_graph, selected_target_graph
    )
    if mapping is None:
        fail("THETA2_RESTORATION_ISOMORPHISM_MAPPING_FAIL")
    content = {
        "relation": "exact_labelled_semi_directed_isomorphism",
        "mixed_vertex_mapping_source_to_target": mapping,
    }
    identifier = f"RI:{sha_object(content)}"
    return {
        "category": "isomorphic",
        "certificate_id": identifier,
        "isomorphism_certificate": content,
    }


def _register_relation(
    row,
    source_graph,
    target_graph,
    source_registry,
    target_registry,
    pair_counts,
    pair_categories,
):
    source_class = source_registry.add(source_graph)
    target_class = target_registry.add(target_graph)
    row["source_mixed_graph_class"] = source_class
    row["target_mixed_graph_class"] = target_class
    pair = (source_class, target_class)
    pair_counts[pair] += 1
    pair_categories[pair].add(row["category"])


def generate_restoration_payload(
    atlas,
    sources,
    targets,
    permutations,
    class_rows,
    compiler_sha256,
    canonicalizer_sha256,
):
    """Return the complete 6/7-port fixed-full restoration certificate."""
    topology_witnesses = {}
    isomorphism_certificates = {}
    source_registry = MixedGraphRegistry(atlas)
    target_registry = MixedGraphRegistry(atlas)
    pair_counts = collections.Counter()
    pair_categories = collections.defaultdict(set)
    roots = []
    no_dummy_anchors = []
    root_multiplicity = collections.Counter()

    for class_row in class_rows:
        if class_row["category"] != "isomorphic":
            continue
        source_index = class_row["source_index"]
        for member in class_row["raw_members"]:
            target_index = member["target_index"]
            permutation_index = member["permutation_index"]
            record = atlas.relabel_record(
                targets[target_index], permutations[permutation_index]
            )
            roles = tuple(sorted(record.dummy_labels))
            anchor = {
                "source_index": source_index,
                "source_repair_index": sources[source_index].repair_index,
                "class_id": class_row["class_id"],
                "target_index": target_index,
                "permutation_index": permutation_index,
                "port_permutation": list(permutations[permutation_index]),
                "base_raw_id": member["raw_id"],
                "base_certificate_id": class_row["certificate_id"],
                "dummy_roles": list(roles),
                "target_record": record_metadata(record),
            }
            root_multiplicity[len(roles)] += 1
            if not roles:
                anchor_id = f"A:{sha_object(anchor)}"
                anchor["anchor_id"] = anchor_id
                no_dummy_anchors.append(anchor)
            else:
                candidates = source_insertion_candidates(
                    sources[source_index].graph
                )
                if len(candidates) != 8:
                    fail(
                        "THETA2_RESTORATION_BASE_CANDIDATE_CENSUS_FAIL",
                        (source_index, len(candidates)),
                    )
                anchor["source_first_insertion_candidates"] = candidates
                anchor_id = f"A:{sha_object(anchor)}"
                anchor["anchor_id"] = anchor_id
                roots.append((anchor, record))

    if root_multiplicity != collections.Counter({0: 24, 1: 40, 2: 16}):
        fail("THETA2_RESTORATION_ROOT_MULTIPLICITY_FAIL", dict(root_multiplicity))

    first_rows = []
    continuations = []
    first_counts = collections.Counter()
    first_by_remaining = collections.Counter()
    for anchor, record in roots:
        source_index = anchor["source_index"]
        source_graph = sources[source_index].graph
        roles = tuple(anchor["dummy_roles"])
        for restored_role in roles:
            target_full = promote_target_role(record.graph, restored_role, 5)
            selected_target = atlas.restrict_rooted(target_full, set(range(6)))
            remaining_roles = tuple(role for role in roles if role != restored_role)
            for insertion_index, candidate in enumerate(
                anchor["source_first_insertion_candidates"]
            ):
                restored_source = insert_source_leaf(
                    atlas, source_graph, candidate, 5
                )
                result = classify_child(
                    atlas,
                    restored_source,
                    selected_target,
                    topology_witnesses,
                )
                row = {
                    "layer": 1,
                    "port_count": 6,
                    "anchor_id": anchor["anchor_id"],
                    "base_raw_id": anchor["base_raw_id"],
                    "source_index": source_index,
                    "base_class_id": anchor["class_id"],
                    "restored_role": restored_role,
                    "restored_label": 5,
                    "remaining_roles": list(remaining_roles),
                    "source_insertion_index": insertion_index,
                    "source_insertion": candidate,
                    "target_index": anchor["target_index"],
                    "permutation_index": anchor["permutation_index"],
                    "category": result["category"],
                    "certificate_id": result["certificate_id"],
                }
                path_content = {
                    key: row[key]
                    for key in (
                        "layer",
                        "anchor_id",
                        "restored_role",
                        "source_insertion_index",
                    )
                }
                row["path_id"] = f"P6:{sha_object(path_content)}"
                if result["category"] == "isomorphic":
                    certificate = {
                        **result["isomorphism_certificate"],
                        "path_id": row["path_id"],
                        "remaining_roles": list(remaining_roles),
                    }
                    certificate_id = f"RI:{sha_object(certificate)}"
                    row["certificate_id"] = certificate_id
                    isomorphism_certificates[certificate_id] = certificate
                _register_relation(
                    row,
                    restored_source,
                    selected_target,
                    source_registry,
                    target_registry,
                    pair_counts,
                    pair_categories,
                )
                first_rows.append(row)
                first_counts[row["category"]] += 1
                first_by_remaining[(len(remaining_roles), row["category"])] += 1
                if row["category"] == "isomorphic" and remaining_roles:
                    continuations.append(
                        (
                            row,
                            restored_source,
                            target_full,
                            remaining_roles[0],
                        )
                    )

    expected_first = collections.Counter(
        {"quartet_pointwise_excluded": 504, "isomorphic": 72}
    )
    expected_first_by_remaining = collections.Counter(
        {
            (0, "quartet_pointwise_excluded"): 280,
            (0, "isomorphic"): 40,
            (1, "quartet_pointwise_excluded"): 224,
            (1, "isomorphic"): 32,
        }
    )
    if first_counts != expected_first or first_by_remaining != expected_first_by_remaining:
        fail(
            "THETA2_RESTORATION_FIRST_LAYER_CENSUS_FAIL",
            (dict(first_counts), dict(first_by_remaining)),
        )
    if len(continuations) != 32:
        fail("THETA2_RESTORATION_CONTINUATION_CENSUS_FAIL", len(continuations))

    second_rows = []
    second_counts = collections.Counter()
    for parent_row, source_six, target_six_full, restored_role in continuations:
        candidates = source_insertion_candidates(source_six)
        if len(candidates) != 9:
            fail(
                "THETA2_RESTORATION_SECOND_CANDIDATE_CENSUS_FAIL",
                (parent_row["path_id"], len(candidates)),
            )
        target_full = promote_target_role(target_six_full, restored_role, 6)
        selected_target = atlas.restrict_rooted(target_full, set(range(7)))
        for insertion_index, candidate in enumerate(candidates):
            restored_source = insert_source_leaf(
                atlas, source_six, candidate, 6
            )
            result = classify_child(
                atlas,
                restored_source,
                selected_target,
                topology_witnesses,
            )
            row = {
                "layer": 2,
                "port_count": 7,
                "anchor_id": parent_row["anchor_id"],
                "base_raw_id": parent_row["base_raw_id"],
                "source_index": parent_row["source_index"],
                "base_class_id": parent_row["base_class_id"],
                "parent_path_id": parent_row["path_id"],
                "first_restored_role": parent_row["restored_role"],
                "first_source_insertion_index": parent_row[
                    "source_insertion_index"
                ],
                "restored_role": restored_role,
                "restored_label": 6,
                "remaining_roles": [],
                "source_insertion_index": insertion_index,
                "source_insertion": candidate,
                "target_index": parent_row["target_index"],
                "permutation_index": parent_row["permutation_index"],
                "category": result["category"],
                "certificate_id": result["certificate_id"],
            }
            path_content = {
                key: row[key]
                for key in (
                    "layer",
                    "parent_path_id",
                    "restored_role",
                    "source_insertion_index",
                )
            }
            row["path_id"] = f"P7:{sha_object(path_content)}"
            if result["category"] == "isomorphic":
                certificate = {
                    **result["isomorphism_certificate"],
                    "path_id": row["path_id"],
                    "remaining_roles": [],
                }
                certificate_id = f"RI:{sha_object(certificate)}"
                row["certificate_id"] = certificate_id
                isomorphism_certificates[certificate_id] = certificate
            _register_relation(
                row,
                restored_source,
                selected_target,
                source_registry,
                target_registry,
                pair_counts,
                pair_categories,
            )
            second_rows.append(row)
            second_counts[row["category"]] += 1

    expected_second = collections.Counter(
        {"quartet_pointwise_excluded": 256, "isomorphic": 32}
    )
    if second_counts != expected_second:
        fail(
            "THETA2_RESTORATION_SECOND_LAYER_CENSUS_FAIL",
            dict(second_counts),
        )
    if any(len(categories) != 1 for categories in pair_categories.values()):
        fail("THETA2_RESTORATION_RELATION_CLASS_STATUS_DRIFT")

    physical_isomorphic_terminals = [
        row
        for row in first_rows + second_rows
        if row["category"] == "isomorphic" and not row["remaining_roles"]
    ]
    if len(physical_isomorphic_terminals) != 72:
        fail(
            "THETA2_RESTORATION_PHYSICAL_TERMINAL_CENSUS_FAIL",
            len(physical_isomorphic_terminals),
        )

    return {
        "schema": "k2p-theta2-fixed-full-restoration-closure-v1",
        "claim_scope": {
            "proved": "Every one- or two-dummy theta2 isomorphism anchor is discharged along every actual fixed-full 6/7-port restoration path by a pointwise quartet separator or an exact full labelled semi-directed isomorphism.",
            "logic": "Fix a full relation first; marginalize that same relation to its actual restored label. Source marginal openness selects one enumerated child. No target marginal openness and no lifting of an abstract selected relation is used.",
        },
        "bindings": {
            "compiler_sha256": compiler_sha256,
            "canonicalizer_sha256": canonicalizer_sha256,
            "base_class_rows_sha256": sha_object(class_rows),
            "paired_marginal_open_image_proof_sha256": BRIDGE_MARGINAL_PROOF_SHA256,
            "paired_marginal_certificate_sha256": BRIDGE_MARGINAL_CERTIFICATE_SHA256,
            "paired_marginal_replayer_sha256": BRIDGE_MARGINAL_REPLAYER_SHA256,
        },
        "census": {
            "base_isomorphic_raw_anchors": 80,
            "no_dummy_physical_anchors": 24,
            "dummy_restoration_roots": 56,
            "one_dummy_roots": 40,
            "two_dummy_roots": 16,
            "first_layer_role_requests": 72,
            "first_insertion_candidates_per_request": 8,
            "six_port_children": 576,
            "six_port_categories": dict(sorted(first_counts.items())),
            "six_port_categories_by_remaining_roles": {
                f"{remaining}:{category}": count
                for (remaining, category), count in sorted(
                    first_by_remaining.items()
                )
            },
            "six_port_isomorphic_continuations": 32,
            "second_insertion_candidates_per_continuation": 9,
            "seven_port_children": 288,
            "seven_port_categories": dict(sorted(second_counts.items())),
            "physical_isomorphic_restoration_terminals": 72,
            "unresolved_paths": 0,
            "exact_source_mixed_graph_classes": len(
                source_registry.representatives
            ),
            "exact_target_mixed_graph_classes": len(
                target_registry.representatives
            ),
            "exact_directed_relation_classes": len(pair_counts),
        },
        "no_dummy_anchors": no_dummy_anchors,
        "restoration_roots": [anchor for anchor, _record in roots],
        "topology_witnesses": {
            key: topology_witnesses[key] for key in sorted(topology_witnesses)
        },
        "isomorphism_certificates": {
            key: isomorphism_certificates[key]
            for key in sorted(isomorphism_certificates)
        },
        "six_port_rows": first_rows,
        "seven_port_rows": second_rows,
        "physical_isomorphic_terminal_path_ids": [
            row["path_id"] for row in physical_isomorphic_terminals
        ],
        "relation_class_presentation_counts": {
            f"{left}:{right}": count
            for (left, right), count in sorted(pair_counts.items())
        },
        "relation_class_categories": {
            f"{left}:{right}": sorted(pair_categories[(left, right)])
            for left, right in sorted(pair_categories)
        },
    }
