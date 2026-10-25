#!/usr/bin/env python3
"""Derive every model-independent non-four physical equality anchor.

This producer starts from the literal primitive graph grammar exposed by the
active K3P atlas, but it uses only graph construction, restriction, topology
signatures, exact semi-directed mixed-graph relations, and fixed-full
restoration.  It never compiles or evaluates a K2P polynomial, rank, sign, or
model descriptor, and it does not read the frozen 176-anchor contract, theta2
closure, or cycle anchor list.
"""

from __future__ import annotations

import argparse
import ast
import collections
import hashlib
import importlib.util
import itertools
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ATLAS_PATH = PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py"
DEFAULT_OUTPUT = HERE / "artifacts/NON_FOUR_ANCHOR_UNIVERSE.json"


class UniverseFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise UniverseFailure(code if detail is None else f"{code}: {detail}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def graph_payload(graph) -> dict[str, Any]:
    """The public probe-contract graph serialization, reproduced literally."""
    return {
        "nodes": [
            [repr(node), {key: repr(value) for key, value in sorted(data.items())}]
            for node, data in sorted(graph.nodes(data=True), key=lambda row: repr(row[0]))
        ],
        "edges": [
            [
                repr(tail),
                repr(head),
                {key: repr(value) for key, value in sorted(data.items())},
            ]
            for tail, head, data in sorted(
                graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
            )
        ],
    }


class StreamDigest:
    def __init__(self) -> None:
        self._digest = hashlib.sha256()
        self.count = 0

    def add(self, value: Any) -> None:
        self._digest.update(canonical_bytes(value))
        self._digest.update(b"\n")
        self.count += 1

    def public(self) -> dict[str, Any]:
        return {"rows": self.count, "sha256": self._digest.hexdigest()}


def load_atlas():
    name = f"k3p_non_four_producer_atlas_{sha_file(ATLAS_PATH)[:12]}"
    spec = importlib.util.spec_from_file_location(name, ATLAS_PATH)
    require(spec is not None and spec.loader is not None, "ATLAS_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def labels_of(graph) -> tuple[int, ...]:
    return tuple(
        sorted(
            data["label"]
            for _, data in graph.nodes(data=True)
            if isinstance(data.get("label"), int)
        )
    )


def topology_mismatch(source_signature, target_permuted_signature) -> str | None:
    """Return a graph-invariant mismatch kind, never a model-specific sign claim."""
    _labels, source_quartets, source_triples = source_signature
    target_quartets, target_triples = target_permuted_signature
    require(
        tuple(quartet for quartet, _ in source_quartets)
        == tuple(quartet for quartet, _ in target_quartets),
        "TOPOLOGY_QUARTET_INDEX",
    )
    for (_quartet, source_splits), (_other, target_splits) in zip(
        source_quartets, target_quartets
    ):
        if source_splits != target_splits:
            return "displayed_quartet_mismatch"
    source_types = dict(source_triples)
    target_types = dict(target_triples)
    require(set(source_types) == set(target_types), "TOPOLOGY_TRIPLE_INDEX")
    for triple in sorted(source_types):
        if {source_types[triple], target_types[triple]} == {"tree", "sunlet"}:
            return "three_leaf_type_mismatch"
    return None


def topology_mismatch_graphs(atlas, source, target) -> str | None:
    source_signature = atlas.topology_signature(source)
    target_signature = atlas.topology_signature(target)
    require(source_signature[0] == target_signature[0], "TOPOLOGY_LABEL_SET")
    return topology_mismatch(
        source_signature, (target_signature[1], target_signature[2])
    )


def source_insertion_candidates(graph) -> list[dict[str, Any]]:
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


def _insert(
    graph, candidate, label: int, subdivision, leaf, atlas, *, dummy_name_field: bool
):
    tail = ast.literal_eval(str(candidate["tail"]))
    head = ast.literal_eval(str(candidate["head"]))
    require(graph.has_edge(tail, head), "INSERTION_EDGE", candidate)
    result = graph.copy()
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    require(subdivision not in result and leaf not in result, "INSERTION_COLLISION")
    subdivision_data = {"role": "tree", "label": None, "dummy": False}
    if dummy_name_field:
        subdivision_data["dummy_name"] = None
    result.add_node(subdivision, **subdivision_data)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    atlas.validate_graph(result)
    return result


def insert_cycle_native(atlas, graph, candidate, label: int):
    tail = ast.literal_eval(str(candidate["tail"]))
    head = ast.literal_eval(str(candidate["head"]))
    return _insert(
        graph,
        candidate,
        label,
        ("cycle_restoration_subdivision", label, repr(tail), repr(head)),
        ("leaf", "cycle_restoration", label),
        atlas,
        dummy_name_field=False,
    )


def insert_theta_native(atlas, graph, candidate, label: int):
    tail = ast.literal_eval(str(candidate["tail"]))
    head = ast.literal_eval(str(candidate["head"]))
    return _insert(
        graph,
        candidate,
        label,
        ("theta2_restoration_subdivision", label, repr(tail), repr(head)),
        ("leaf", "theta2_restoration", label),
        atlas,
        dummy_name_field=False,
    )


def insert_contract(atlas, graph, candidate, label: int, namespace: str):
    tail = ast.literal_eval(str(candidate["tail"]))
    head = ast.literal_eval(str(candidate["head"]))
    return _insert(
        graph,
        candidate,
        label,
        (namespace, "subdivision", label, repr(tail), repr(head)),
        (namespace, "leaf", label, repr(tail), repr(head)),
        atlas,
        dummy_name_field=True,
    )


def promote_roles(atlas, graph, roles: tuple[tuple[str, int], ...]):
    result = graph.copy()
    for role, label in roles:
        matches = [
            node
            for node, data in result.nodes(data=True)
            if data.get("dummy_name") == role
        ]
        require(len(matches) == 1, "PROMOTION_ROLE", (role, matches))
        result.nodes[matches[0]].update(label=label, dummy=False, dummy_name=None)
    atlas.validate_graph(result)
    return result


def assert_physical_pair(source, target, port_count: int) -> None:
    require(labels_of(source) == tuple(range(port_count)), "SOURCE_LABELS")
    require(labels_of(target) == tuple(range(port_count)), "TARGET_LABELS")
    require(
        not [data for _, data in source.nodes(data=True) if data.get("dummy")],
        "SOURCE_DUMMY",
    )
    require(
        not [data for _, data in target.nodes(data=True) if data.get("dummy")],
        "TARGET_DUMMY",
    )


def make_anchor(
    origin: str,
    port_count: int,
    relation: str,
    source,
    target,
    structural_locator: dict[str, Any],
) -> dict[str, Any]:
    require(relation in {"isomorphic", "triangle"}, "ANCHOR_RELATION", relation)
    assert_physical_pair(source, target, port_count)
    body = {
        "origin": origin,
        "port_count": port_count,
        "relation": relation,
        "source_graph_sha256": sha_object(graph_payload(source)),
        "target_graph_sha256": sha_object(graph_payload(target)),
        "structural_locator": structural_locator,
    }
    return {"anchor_key": sha_object(body), **body}


def tree_graph(atlas):
    graph = atlas.nx.DiGraph(name="three_port_tree")
    for node, role, label in (
        ("r", "root", None),
        ("v", "tree", None),
        ("L0", "leaf", 0),
        ("L1", "leaf", 1),
        ("L2", "leaf", 2),
    ):
        graph.add_node(node, role=role, label=label, dummy=False, dummy_name=None)
    graph.add_edges_from(
        (
            ("r", "L0", {"edge_role": "incoming_arm"}),
            ("r", "v", {"edge_role": "incoming_core"}),
            ("v", "L1", {"edge_role": "arm"}),
            ("v", "L2", {"edge_role": "arm"}),
        )
    )
    atlas.validate_graph(graph)
    return graph


def cycle_configurations(atlas, sources):
    configurations = {}
    for source_index, source in enumerate(sources):
        states = [
            {
                "placement_path": [],
                "insertions": [],
                "graph": source.graph,
                "signature": atlas.topology_signature(source.graph),
            }
        ]
        for depth in range(1, 5):
            label = 2 + depth
            children = []
            for parent in states:
                candidates = source_insertion_candidates(parent["graph"])
                require(
                    len(candidates) == 2 + depth,
                    "CYCLE_INSERTION_CANDIDATES",
                    (source_index, depth, len(candidates)),
                )
                for insertion_index, candidate in enumerate(candidates):
                    graph = insert_cycle_native(
                        atlas, parent["graph"], candidate, label
                    )
                    children.append(
                        {
                            "placement_path": parent["placement_path"]
                            + [insertion_index],
                            "insertions": parent["insertions"] + [candidate],
                            "graph": graph,
                            "signature": atlas.topology_signature(graph),
                        }
                    )
            states = children
            configurations[(source_index, depth)] = states
    expected = {1: 3, 2: 12, 3: 60, 4: 360}
    for source_index in range(2):
        for depth, count in expected.items():
            require(
                len(configurations[(source_index, depth)]) == count,
                "CYCLE_CONFIGURATION_CENSUS",
            )
    return configurations


def generate_cycle(atlas):
    sources = tuple(atlas.source_supports(("cycle",)))
    targets = tuple(
        atlas.target_completions(3, True)
        + atlas.target_completions(3, False)
    )
    permutations = tuple(itertools.permutations(range(3)))
    require((len(sources), len(targets), len(permutations)) == (2, 1120, 6), "CYCLE_PRIMITIVES")
    source_signatures = tuple(atlas.topology_signature(row.graph) for row in sources)
    target_signatures = tuple(
        atlas.topology_signature(atlas.selected_graph_from_completion(row))
        for row in targets
    )
    base_digest = StreamDigest()
    base_counts = collections.Counter()
    parent_relations = collections.Counter()
    root_multiplicity = collections.Counter()
    roots = []
    anchors = []
    raw_id = 0
    for source_index, source in enumerate(sources):
        for target_index, target in enumerate(targets):
            for permutation_index, permutation in enumerate(permutations):
                mismatch = topology_mismatch(
                    source_signatures[source_index],
                    atlas.permute_signature(target_signatures[target_index], permutation),
                )
                if mismatch is not None:
                    category = mismatch
                    relation = "none"
                    dummy_roles: tuple[str, ...] = ()
                else:
                    record = atlas.relabel_record(target, permutation)
                    selected_target = atlas.selected_graph_from_completion(record)
                    relation = atlas.mixed_relation_exact(source.graph, selected_target)
                    require(relation in {"isomorphic", "triangle", "none"},
                            "CYCLE_PARENT_RELATION", (raw_id, relation))
                    parent_relations[relation] += 1
                    dummy_roles = tuple(sorted(record.dummy_labels))
                    if dummy_roles:
                        category = "restoration_root"
                        roots.append(
                            {
                                "base_raw_id": raw_id,
                                "source_index": source_index,
                                "target_index": target_index,
                                "permutation_index": permutation_index,
                                "port_permutation": list(permutation),
                                "dummy_roles": dummy_roles,
                                "record": record,
                                "parent_relation": relation,
                            }
                        )
                        root_multiplicity[len(dummy_roles)] += 1
                    else:
                        require(
                            relation in {"isomorphic", "triangle"},
                            "CYCLE_NO_DUMMY_RELATION",
                            (raw_id, relation),
                        )
                        category = relation
                        anchors.append(
                            make_anchor(
                                "cycle_physical_k3",
                                3,
                                relation,
                                source.graph,
                                record.graph,
                                {
                                    "source_index": source_index,
                                    "target_index": target_index,
                                    "permutation_index": permutation_index,
                                    "port_permutation": list(permutation),
                                    "base_raw_id": raw_id,
                                },
                            )
                        )
                base_counts[category] += 1
                base_digest.add(
                    {
                        "raw_id": raw_id,
                        "category": category,
                        "relation": relation,
                        "dummy_count": len(dummy_roles),
                    }
                )
                raw_id += 1
    require(
        base_counts
        == collections.Counter(
            {
                "three_leaf_type_mismatch": 7452,
                "restoration_root": 5964,
                "isomorphic": 8,
                "triangle": 16,
            }
        ),
        "CYCLE_BASE_COUNTS",
        dict(base_counts),
    )
    require(
        root_multiplicity == collections.Counter({1: 324, 2: 1896, 3: 2784, 4: 960}),
        "CYCLE_ROOT_MULTIPLICITY",
        dict(root_multiplicity),
    )
    configurations = cycle_configurations(atlas, sources)
    full_digest = StreamDigest()
    full_counts = collections.Counter()
    full_raw_id = 0
    for root in roots:
        roles = root["dummy_roles"]
        depth = len(roles)
        target_graph = promote_roles(
            atlas,
            root["record"].graph,
            tuple((role, 3 + offset) for offset, role in enumerate(roles)),
        )
        target_signature = atlas.topology_signature(target_graph)
        for configuration in configurations[(root["source_index"], depth)]:
            mismatch = topology_mismatch(
                configuration["signature"],
                (target_signature[1], target_signature[2]),
            )
            if mismatch is not None:
                category = mismatch
                relation = "none"
            else:
                relation = atlas.mixed_relation_exact(
                    configuration["graph"], target_graph
                )
                require(
                    relation in {"isomorphic", "none"},
                    "CYCLE_FULL_RELATION",
                    (full_raw_id, relation),
                )
                category = relation
                if relation == "isomorphic":
                    anchors.append(
                        make_anchor(
                            "cycle_restored_physical_k4",
                            3 + depth,
                            relation,
                            configuration["graph"],
                            target_graph,
                            {
                                "source_index": root["source_index"],
                                "target_index": root["target_index"],
                                "permutation_index": root["permutation_index"],
                                "port_permutation": root["port_permutation"],
                                "base_raw_id": root["base_raw_id"],
                                "dummy_roles_in_label_order": list(roles),
                                "source_placement_path": configuration[
                                    "placement_path"
                                ],
                                "full_raw_id": full_raw_id,
                            },
                        )
                    )
            full_counts[category] += 1
            full_digest.add(
                {
                    "full_raw_id": full_raw_id,
                    "base_raw_id": root["base_raw_id"],
                    "source_placement_path": configuration["placement_path"],
                    "category": category,
                    "relation": relation,
                }
            )
            full_raw_id += 1
    require(
        full_counts
        == collections.Counter(
            {
                "displayed_quartet_mismatch": 535920,
                "three_leaf_type_mismatch": 300,
                "none": 132,
                "isomorphic": 12,
            }
        ),
        "CYCLE_FULL_COUNTS",
        dict(full_counts),
    )
    require(len(anchors) == 36, "CYCLE_ANCHOR_COUNT", len(anchors))
    return anchors, {
        "sources": len(sources),
        "targets": len(targets),
        "selected_incoming_targets": 289,
        "marginalized_incoming_targets": 831,
        "permutations": len(permutations),
        "base_raw": raw_id,
        "base_counts": dict(sorted(base_counts.items())),
        "parent_relations": dict(sorted(parent_relations.items())),
        "dummy_root_multiplicity": {
            str(key): value for key, value in sorted(root_multiplicity.items())
        },
        "restoration_raw": full_raw_id,
        "restoration_counts": dict(sorted(full_counts.items())),
        "base_enumeration": base_digest.public(),
        "restoration_enumeration": full_digest.public(),
    }


def generate_theta2(atlas):
    sources = tuple(atlas.source_supports(("theta2",)))
    selected_targets = tuple(atlas.target_completions(5, True))
    marginalized_targets = tuple(atlas.target_completions(5, False))
    targets = selected_targets + marginalized_targets
    permutations = tuple(itertools.permutations(range(5)))
    require(
        (len(sources), len(selected_targets), len(marginalized_targets), len(permutations))
        == (4, 1983, 4155, 120),
        "THETA2_PRIMITIVES",
    )
    source_signatures = tuple(atlas.topology_signature(row.graph) for row in sources)
    target_signatures = tuple(
        atlas.topology_signature(atlas.selected_graph_from_completion(row))
        for row in targets
    )
    base_digest = StreamDigest()
    base_counts = collections.Counter()
    per_source = collections.defaultdict(collections.Counter)
    roots = []
    anchors = []
    raw_per_source = len(targets) * len(permutations)
    for source_index, source in enumerate(sources):
        for target_index, target in enumerate(targets):
            for permutation_index, permutation in enumerate(permutations):
                raw_id = (
                    source_index * raw_per_source
                    + target_index * len(permutations)
                    + permutation_index
                )
                mismatch = topology_mismatch(
                    source_signatures[source_index],
                    atlas.permute_signature(target_signatures[target_index], permutation),
                )
                dummy_count = 0
                if mismatch is not None:
                    category = mismatch
                    relation = "none"
                else:
                    record = atlas.relabel_record(target, permutation)
                    selected_target = atlas.selected_graph_from_completion(record)
                    relation = atlas.mixed_relation_exact(source.graph, selected_target)
                    require(
                        relation in {"isomorphic", "none"},
                        "THETA2_BASE_RELATION",
                        (raw_id, relation),
                    )
                    # A marginalized target incoming role is not a physical
                    # equality boundary presentation.  Its selected mixed
                    # graph can become abstractly isomorphic after deleting
                    # that role, but it is not an equality anchor and is not
                    # a theta2 fixed-full repair obligation.  This is port
                    # metadata, not a model-specific rank exclusion.
                    if relation == "isomorphic" and not record.incoming_selected:
                        category = "incoming_boundary_mismatch"
                    elif relation == "isomorphic":
                        roles = tuple(sorted(record.dummy_labels))
                        dummy_count = len(roles)
                        root = {
                            "base_raw_id": raw_id,
                            "source_index": source_index,
                            "target_index": target_index,
                            "permutation_index": permutation_index,
                            "port_permutation": list(permutation),
                            "dummy_roles": roles,
                            "record": record,
                        }
                        if roles:
                            roots.append(root)
                        else:
                            anchors.append(
                                make_anchor(
                                    "theta2_physical_k5",
                                    5,
                                    "isomorphic",
                                    source.graph,
                                    record.graph,
                                    {
                                        "source_index": source_index,
                                        "target_index": target_index,
                                        "permutation_index": permutation_index,
                                        "port_permutation": list(permutation),
                                        "base_raw_id": raw_id,
                                    },
                                )
                            )
                        category = relation
                    else:
                        category = relation
                base_counts[category] += 1
                per_source[source_index][category] += 1
                base_digest.add(
                    {
                        "raw_id": raw_id,
                        "category": category,
                        "relation": relation,
                        "dummy_count": dummy_count,
                    }
                )
    expected_source = collections.Counter(
        {
            "displayed_quartet_mismatch": 735648,
            "three_leaf_type_mismatch": 632,
            "incoming_boundary_mismatch": 44,
            "none": 216,
            "isomorphic": 20,
        }
    )
    for source_index in range(4):
        require(
            per_source[source_index] == expected_source,
            "THETA2_SOURCE_COUNTS",
            (source_index, dict(per_source[source_index])),
        )
    require(len(anchors) == 24 and len(roots) == 56, "THETA2_BASE_ANCHORS_ROOTS")
    root_multiplicity = collections.Counter(len(row["dummy_roles"]) for row in roots)
    require(
        root_multiplicity == collections.Counter({1: 40, 2: 16}),
        "THETA2_ROOT_MULTIPLICITY",
        dict(root_multiplicity),
    )

    first_digest = StreamDigest()
    first_counts = collections.Counter()
    first_by_remaining = collections.Counter()
    continuations = []
    for root in roots:
        source = sources[root["source_index"]].graph
        candidates = source_insertion_candidates(source)
        require(len(candidates) == 8, "THETA2_FIRST_CANDIDATES")
        for restored_role in root["dummy_roles"]:
            target_full = promote_roles(
                atlas, root["record"].graph, ((restored_role, 5),)
            )
            selected_target = atlas.restrict_rooted(target_full, set(range(6)))
            remaining_roles = tuple(
                role for role in root["dummy_roles"] if role != restored_role
            )
            for insertion_index, candidate in enumerate(candidates):
                source_six = insert_theta_native(atlas, source, candidate, 5)
                mismatch = topology_mismatch_graphs(
                    atlas, source_six, selected_target
                )
                if mismatch is not None:
                    category = mismatch
                    relation = "none"
                else:
                    relation = atlas.mixed_relation_exact(source_six, selected_target)
                    require(
                        relation in {"isomorphic", "none"},
                        "THETA2_FIRST_RELATION",
                        (root["base_raw_id"], restored_role, insertion_index, relation),
                    )
                    category = relation
                first_counts[category] += 1
                first_by_remaining[(len(remaining_roles), category)] += 1
                first_digest.add(
                    {
                        "base_raw_id": root["base_raw_id"],
                        "restored_role": restored_role,
                        "source_insertion_index": insertion_index,
                        "remaining_roles": list(remaining_roles),
                        "category": category,
                        "relation": relation,
                    }
                )
                if relation != "isomorphic":
                    continue
                state = {
                    **root,
                    "first_restored_role": restored_role,
                    "first_source_insertion_index": insertion_index,
                    "first_source_insertion": candidate,
                    "source_six": source_six,
                    "target_six_full": target_full,
                    "remaining_roles": remaining_roles,
                }
                if remaining_roles:
                    continuations.append(state)
                else:
                    contract_source = insert_contract(
                        atlas, source, candidate, 5, "theta2_k6"
                    )
                    anchors.append(
                        make_anchor(
                            "theta2_physical_k6",
                            6,
                            "isomorphic",
                            contract_source,
                            target_full,
                            {
                                "source_index": root["source_index"],
                                "target_index": root["target_index"],
                                "permutation_index": root["permutation_index"],
                                "port_permutation": root["port_permutation"],
                                "base_raw_id": root["base_raw_id"],
                                "restored_role": restored_role,
                                "source_insertion_index": insertion_index,
                                "source_insertion": candidate,
                            },
                        )
                    )
    require(
        first_counts
        == collections.Counter(
            {"displayed_quartet_mismatch": 504, "isomorphic": 72}
        ),
        "THETA2_FIRST_COUNTS",
        dict(first_counts),
    )
    require(
        first_by_remaining
        == collections.Counter(
            {
                (0, "displayed_quartet_mismatch"): 280,
                (0, "isomorphic"): 40,
                (1, "displayed_quartet_mismatch"): 224,
                (1, "isomorphic"): 32,
            }
        ),
        "THETA2_FIRST_REMAINING_COUNTS",
        dict(first_by_remaining),
    )
    require(len(continuations) == 32, "THETA2_CONTINUATIONS")

    second_digest = StreamDigest()
    second_counts = collections.Counter()
    for state in continuations:
        require(len(state["remaining_roles"]) == 1, "THETA2_SECOND_ROLE_COUNT")
        restored_role = state["remaining_roles"][0]
        candidates = source_insertion_candidates(state["source_six"])
        require(len(candidates) == 9, "THETA2_SECOND_CANDIDATES")
        target_full = promote_roles(
            atlas, state["target_six_full"], ((restored_role, 6),)
        )
        selected_target = atlas.restrict_rooted(target_full, set(range(7)))
        for insertion_index, candidate in enumerate(candidates):
            source_seven = insert_theta_native(
                atlas, state["source_six"], candidate, 6
            )
            mismatch = topology_mismatch_graphs(atlas, source_seven, selected_target)
            if mismatch is not None:
                category = mismatch
                relation = "none"
            else:
                relation = atlas.mixed_relation_exact(source_seven, selected_target)
                require(
                    relation in {"isomorphic", "none"},
                    "THETA2_SECOND_RELATION",
                    (state["base_raw_id"], restored_role, insertion_index, relation),
                )
                category = relation
            second_counts[category] += 1
            second_digest.add(
                {
                    "base_raw_id": state["base_raw_id"],
                    "first_restored_role": state["first_restored_role"],
                    "first_source_insertion_index": state[
                        "first_source_insertion_index"
                    ],
                    "restored_role": restored_role,
                    "source_insertion_index": insertion_index,
                    "category": category,
                    "relation": relation,
                }
            )
            if relation != "isomorphic":
                continue
            source_base = sources[state["source_index"]].graph
            contract_source = insert_contract(
                atlas,
                source_base,
                state["first_source_insertion"],
                5,
                "theta2_k7_first",
            )
            contract_source = insert_contract(
                atlas,
                contract_source,
                candidate,
                6,
                "theta2_k7_second",
            )
            anchors.append(
                make_anchor(
                    "theta2_physical_k7",
                    7,
                    "isomorphic",
                    contract_source,
                    target_full,
                    {
                        "source_index": state["source_index"],
                        "target_index": state["target_index"],
                        "permutation_index": state["permutation_index"],
                        "port_permutation": state["port_permutation"],
                        "base_raw_id": state["base_raw_id"],
                        "first_restored_role": state["first_restored_role"],
                        "first_source_insertion_index": state[
                            "first_source_insertion_index"
                        ],
                        "first_source_insertion": state["first_source_insertion"],
                        "restored_role": restored_role,
                        "source_insertion_index": insertion_index,
                        "source_insertion": candidate,
                    },
                )
            )
    require(
        second_counts
        == collections.Counter(
            {"displayed_quartet_mismatch": 256, "isomorphic": 32}
        ),
        "THETA2_SECOND_COUNTS",
        dict(second_counts),
    )
    by_origin = collections.Counter(row["origin"] for row in anchors)
    require(
        by_origin
        == collections.Counter(
            {
                "theta2_physical_k5": 24,
                "theta2_physical_k6": 40,
                "theta2_physical_k7": 32,
            }
        ),
        "THETA2_ANCHOR_COUNTS",
        dict(by_origin),
    )
    return anchors, {
        "sources": len(sources),
        "selected_incoming_targets": len(selected_targets),
        "marginalized_incoming_targets": len(marginalized_targets),
        "targets": len(targets),
        "permutations": len(permutations),
        "raw_per_source": raw_per_source,
        "base_raw": raw_per_source * len(sources),
        "base_counts": dict(sorted(base_counts.items())),
        "per_source_counts": {
            str(source_index): dict(sorted(per_source[source_index].items()))
            for source_index in range(4)
        },
        "dummy_root_multiplicity": {
            str(key): value for key, value in sorted(root_multiplicity.items())
        },
        "first_layer_role_requests": sum(len(row["dummy_roles"]) for row in roots),
        "six_port_children": first_digest.count,
        "six_port_counts": dict(sorted(first_counts.items())),
        "six_port_counts_by_remaining_roles": {
            f"{remaining}:{category}": value
            for (remaining, category), value in sorted(first_by_remaining.items())
        },
        "six_port_isomorphic_continuations": len(continuations),
        "seven_port_children": second_digest.count,
        "seven_port_counts": dict(sorted(second_counts.items())),
        "base_enumeration": base_digest.public(),
        "six_port_enumeration": first_digest.public(),
        "seven_port_enumeration": second_digest.public(),
    }


def census(anchors):
    by_origin = collections.Counter(row["origin"] for row in anchors)
    by_relation = collections.Counter(row["relation"] for row in anchors)
    by_port_count = collections.Counter(row["port_count"] for row in anchors)
    return {
        "total": len(anchors),
        "by_origin": dict(sorted(by_origin.items())),
        "by_relation": dict(sorted(by_relation.items())),
        "by_port_count": {
            str(key): value for key, value in sorted(by_port_count.items())
        },
    }


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    content = json.dumps(value, sort_keys=True, indent=2) + "\n"
    with temporary.open("w") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def main(argv: list[str] | None = None) -> int:
    if not __debug__:
        raise UniverseFailure("OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    started = time.monotonic()
    atlas = load_atlas()
    tree = tree_graph(atlas)
    tree_anchor = make_anchor(
        "tree_physical_k3", 3, "isomorphic", tree, tree, {}
    )
    cycle_anchors, cycle_counts = generate_cycle(atlas)
    theta2_anchors, theta2_counts = generate_theta2(atlas)
    anchors = sorted(
        [tree_anchor, *cycle_anchors, *theta2_anchors],
        key=lambda row: (row["origin"], canonical_bytes(row["structural_locator"])),
    )
    require(len({row["anchor_key"] for row in anchors}) == len(anchors), "ANCHOR_KEY_UNIQUENESS")
    derived_census = census(anchors)
    require(
        derived_census
        == {
            "total": 133,
            "by_origin": {
                "cycle_physical_k3": 24,
                "cycle_restored_physical_k4": 12,
                "theta2_physical_k5": 24,
                "theta2_physical_k6": 40,
                "theta2_physical_k7": 32,
                "tree_physical_k3": 1,
            },
            "by_relation": {"isomorphic": 117, "triangle": 16},
            "by_port_count": {"3": 25, "4": 12, "5": 24, "6": 40, "7": 32},
        },
        "NON_FOUR_CENSUS",
        derived_census,
    )
    report = {
        "schema": "k3p-model-independent-non-four-anchor-universe-v1",
        "status": "PASS",
        "claim_boundary": {
            "derived": (
                "The complete designated tree, cycle, and theta2 anchor-seed "
                "universe under the primitive completion grammar and its "
                "incoming-selected theta2 fixed-full-parent convention."
            ),
            "conditional_convention": (
                "A theta2 target whose incoming boundary is marginalized is "
                "not a fixed-full anchor parent, even when deleting that role "
                "makes its selected mixed graph abstractly isomorphic. Such "
                "incoming/root-movement presentations belong to the later "
                "probe boundary, not this bounded seed list."
            ),
            "excluded_marginalized_incoming_parents": theta2_counts[
                "base_counts"
            ]["incoming_boundary_mismatch"],
            "separate_descendant_obligation": (
                "The no-import verifier must independently enumerate every "
                "fully physical restoration of these 176 parents and map "
                "each graph-isomorphic path to an existing seed plus a "
                "transported downstream one-port attachment."
            ),
            "not_claimed": (
                "This producer alone does not assert that every fully restored "
                "descendant of a marginalized-incoming abstract isomorphism "
                "is absent."
            ),
            "methods": [
                "literal directed graph construction",
                "rooted restriction and deterministic relabelling",
                "displayed-quartet and three-leaf graph-type prefilters",
                "exact labelled semi-directed mixed-graph isomorphism",
                "ordinary-triangle quotient",
                "exhaustive fixed-full source insertion and target promotion",
            ],
            "forbidden_and_unused": [
                "K2P polynomial compilation",
                "K2P rank certificates",
                "K2P sign certificates",
                "frozen 176-anchor contract as an enumeration input",
                "frozen theta2 closure as an enumeration input",
                "frozen cycle physical-anchor list as an enumeration input",
            ],
        },
        "bindings": {
            "producer_sha256": sha_file(Path(__file__).resolve()),
            "k3p_atlas_sha256": sha_file(ATLAS_PATH),
        },
        "primitive_counts": {
            "target_completion_formula": (
                "sum_H r_H sum_{j=0}^{q_H} binom(q_H,j) "
                "binom(k-epsilon-j+m_H-1,m_H-1)"
            ),
            "cycle": cycle_counts,
            "theta2": theta2_counts,
            "tree": {"sources": 1, "physical_anchors": 1},
        },
        "stage_counts": {
            "cycle_base_presentations": cycle_counts["base_raw"],
            "cycle_restoration_presentations": cycle_counts["restoration_raw"],
            "theta2_base_presentations": theta2_counts["base_raw"],
            "theta2_six_port_children": theta2_counts["six_port_children"],
            "theta2_seven_port_children": theta2_counts["seven_port_children"],
        },
        "census": derived_census,
        "anchors": anchors,
        "ordered_anchor_key_sha256": sha_object(
            sorted(row["anchor_key"] for row in anchors)
        ),
    }
    report["payload_sha256"] = sha_object(
        {
            key: value
            for key, value in report.items()
            if key not in {"payload_sha256", "operational"}
        }
    )
    atomic_json(args.output.resolve(), report)
    elapsed = time.monotonic() - started
    print(
        "K3P_NON_FOUR_ANCHOR_UNIVERSE_PASS "
        f"anchors={len(anchors)} runtime_seconds={elapsed:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
