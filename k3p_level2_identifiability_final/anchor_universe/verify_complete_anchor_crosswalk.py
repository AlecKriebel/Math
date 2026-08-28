#!/usr/bin/env python3
"""Cross-bind the derived 133 non-four anchors to four-port and contract rows.

The frozen theta/cycle artifacts and 176-row contract enter only here, after
the non-four producer and no-import verifier have fixed their universe.  They
serve as opaque legacy-locator dictionaries and a regression target, never as
an enumeration premise.
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
import os
import sys
import time
from pathlib import Path
from typing import Any

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DEFAULT_PRODUCER = HERE / "artifacts/NON_FOUR_ANCHOR_UNIVERSE.json"
DEFAULT_VERIFIER = HERE / "INDEPENDENT_NON_FOUR_VERIFICATION.json"
DEFAULT_ROOT_MOVEMENT_RECONCILIATION = (
    HERE / "MARGINALIZED_THETA_ONE_PORT_RECONCILIATION.json"
)
DEFAULT_OUTPUT = HERE / "COMPLETE_ANCHOR_UNIVERSE_CROSSWALK.json"
CONTRACT = (
    PROJECT
    / "input_frozen/model_independent_topology_package/anchor_inputs/probe_input_contract.json"
)
THETA = (
    PROJECT
    / "input_frozen/model_independent_topology_package/anchor_inputs/fixed_full_restoration_closure.json.gz"
)
CYCLE = (
    PROJECT
    / "input_frozen/model_independent_topology_package/cycle/physical_anchors.json"
)
FOUR_SUMMARY = (
    PROJECT
    / "four_port_atlas/full_universe_replay/artifacts/FULL_FOUR_PORT_REPLAY.json"
)
FOUR_VERIFICATION = (
    PROJECT
    / "four_port_atlas/full_universe_replay/INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json"
)
FOUR_GRAPH_CORE = (
    PROJECT
    / "four_port_atlas/full_universe_replay/independent_replay_core.py"
)
FOUR_RAW_LEDGER = (
    PROJECT
    / "four_port_atlas/full_universe_replay/artifacts/full_directional_ledger.jsonl.gz"
)
ONE_PORT_MANIFEST = PROJECT / "probes/ONE_PORT_PROBE_MANIFEST.json"
ONE_PORT_LEDGER = PROJECT / "probes/one_port_ledger.jsonl.gz"
TWO_PORT_MANIFEST = PROJECT / "probes/TWO_PORT_PROBE_MANIFEST.json"
TWO_PORT_PARENT_INVENTORY = (
    PROJECT / "probes/two_port_parent_inventory.jsonl.gz"
)
TWO_PORT_LEDGER = PROJECT / "probes/two_port_ledger.jsonl.gz"


class CrosswalkFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise CrosswalkFailure(code if detail is None else f"{code}: {detail}")


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


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CrosswalkFailure(f"JSON_READ:{path}:{exc}") from exc


def load_gzip_json(path: Path):
    try:
        with gzip.open(path, "rt") as handle:
            return json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CrosswalkFailure(f"GZIP_JSON_READ:{path}:{exc}") from exc


def iter_gzip_jsonl(path: Path):
    try:
        with gzip.open(path, "rt") as handle:
            for number, line in enumerate(handle, start=1):
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as exc:
                    raise CrosswalkFailure(
                        f"GZIP_JSONL_ROW:{path}:{number}:{exc}"
                    ) from exc
    except (OSError, UnicodeError) as exc:
        raise CrosswalkFailure(f"GZIP_JSONL_READ:{path}:{exc}") from exc


def import_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "IMPORT_SPEC", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def graph_payload(graph) -> dict[str, Any]:
    return {
        "nodes": [
            [
                repr(node),
                {key: repr(value) for key, value in sorted(data.items())},
            ]
            for node, data in sorted(
                graph.nodes(data=True), key=lambda row: repr(row[0])
            )
        ],
        "edges": [
            [
                repr(tail),
                repr(head),
                {key: repr(value) for key, value in sorted(data.items())},
            ]
            for tail, head, data in sorted(
                graph.edges(data=True),
                key=lambda row: (repr(row[0]), repr(row[1])),
            )
        ],
    }


def graph_sha256(graph) -> str:
    return sha_object(graph_payload(graph))


def insert_on_arc(graph, record, label: int, namespace):
    tail = ast.literal_eval(record["tail"])
    head = ast.literal_eval(record["head"])
    require(graph.has_edge(tail, head), "FOUR_INSERTION_ARC", record)
    result = graph.copy()
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = (
        namespace,
        "subdivision",
        label,
        repr(tail),
        repr(head),
    )
    leaf = (namespace, "leaf", label, repr(tail), repr(head))
    require(
        subdivision not in result and leaf not in result,
        "FOUR_INSERTION_COLLISION",
    )
    result.add_node(
        subdivision,
        role="tree",
        label=None,
        dummy=False,
        dummy_name=None,
    )
    result.add_node(
        leaf,
        role="leaf",
        label=label,
        dummy=False,
        dummy_name=None,
    )
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    require(nx.is_directed_acyclic_graph(result), "FOUR_INSERTION_CYCLE")
    expected = {
        "root": (0, 2),
        "tree": (1, 2),
        "retic": (2, 1),
        "leaf": (1, 0),
    }
    for node, data in result.nodes(data=True):
        require(
            (result.in_degree(node), result.out_degree(node))
            == expected[data["role"]],
            "FOUR_INSERTION_NONBINARY",
            node,
        )
    return result


def promote_dummy_role(graph, role: str, label: int):
    result = graph.copy()
    matches = [
        node
        for node, data in result.nodes(data=True)
        if data.get("dummy_name") == role
    ]
    require(len(matches) == 1, "FOUR_DUMMY_ROLE", [role, matches])
    result.nodes[matches[0]].update(
        label=label, dummy=False, dummy_name=None
    )
    return result


def rooted_core_candidates(graph) -> list[dict[str, Any]]:
    """Fixed-full restoration grammar: nonroot arcs not ending at a leaf."""
    return [
        {
            "tail": repr(tail),
            "head": repr(head),
            "edge_role": data.get("edge_role"),
        }
        for tail, head, data in sorted(
            graph.edges(data=True),
            key=lambda row: (repr(row[0]), repr(row[1])),
        )
        if graph.nodes[tail].get("role") != "root"
        and graph.nodes[head].get("role") != "leaf"
    ]


def profile_candidate(site: dict[str, Any]) -> dict[str, Any]:
    representative = site["rooted_representatives"][0]
    return {
        "tail": representative[0],
        "head": representative[1],
        "edge_role": representative[2],
    }


def exact_incidence_maps(core, source, target) -> list[dict[Any, Any]]:
    """All labelled arrowhead-preserving mixed-graph vertex maps."""
    try:
        source_mixed = core.root_suppressed(source)
        target_mixed = core.root_suppressed(target)
    except core.ReplayFailure:
        return []
    source_incidence = core.incidence_graph(source_mixed)
    target_incidence = core.incidence_graph(target_mixed)
    node_match = lambda left, right: (
        left.get("kind") == right.get("kind")
        and left.get("label") == right.get("label")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        source_incidence,
        target_incidence,
        node_match=node_match,
        edge_match=edge_match,
    )
    maps = []
    for mapping in matcher.isomorphisms_iter():
        maps.append(
            {
                node: mapping[("v", node)][1]
                for node in source_mixed.nodes()
            }
        )
    maps.sort(
        key=lambda mapping: canonical_bytes(
            [
                [repr(left), repr(right)]
                for left, right in sorted(
                    mapping.items(), key=lambda row: repr(row[0])
                )
            ]
        )
    )
    return maps


def mapped_site_index(
    profile: dict[str, Any],
    vertex_map: dict[Any, Any],
    candidate: dict[str, Any],
) -> int:
    tail = ast.literal_eval(candidate["tail"])
    head = ast.literal_eval(candidate["head"])
    endpoints = sorted((repr(vertex_map[tail]), repr(vertex_map[head])))
    matches = [
        index
        for index, site in enumerate(profile["sites"])
        if site["mixed_endpoints"] == endpoints
    ]
    require(len(matches) == 1, "FOUR_SITE_TRANSPORT", [endpoints, matches])
    return matches[0]


def target_child_match(
    core,
    actual_parent,
    actual_child,
    canonical_parent,
    profile: dict[str, Any],
    parent_vertex_map: dict[Any, Any],
    label: int,
    namespace: str,
):
    """Find the unique canonical site compatible with the parent transport."""
    matches = []
    for site_index, site in enumerate(profile["sites"]):
        canonical_child = insert_on_arc(
            canonical_parent,
            profile_candidate(site),
            label,
            (namespace, "target", site_index),
        )
        compatible_maps = []
        for child_map in exact_incidence_maps(
            core, actual_child, canonical_child
        ):
            if all(
                node not in child_map
                or image not in canonical_child
                or child_map[node] == image
                for node, image in parent_vertex_map.items()
            ):
                compatible_maps.append(child_map)
        if compatible_maps:
            matches.append(
                (site_index, canonical_child, compatible_maps[0])
            )
    require(
        len(matches) == 1,
        "FOUR_TARGET_SITE_TRANSPORT",
        [label, [row[0] for row in matches]],
    )
    return matches[0]


def validate_producer(producer: dict[str, Any]) -> None:
    require(
        producer.get("schema") == "k3p-model-independent-non-four-anchor-universe-v1",
        "PRODUCER_SCHEMA",
    )
    require(producer.get("status") == "PASS", "PRODUCER_STATUS")
    expected = sha_object(
        {
            key: value
            for key, value in producer.items()
            if key not in {"payload_sha256", "operational"}
        }
    )
    require(producer.get("payload_sha256") == expected, "PRODUCER_PAYLOAD")
    require(producer.get("census", {}).get("total") == 133, "PRODUCER_CENSUS")


def cycle_locator(row: dict[str, Any]) -> dict[str, Any]:
    if row["origin"] == "base_no_dummy":
        keys = (
            "source_index",
            "target_index",
            "permutation_index",
            "port_permutation",
            "base_raw_id",
        )
    else:
        keys = (
            "source_index",
            "target_index",
            "permutation_index",
            "port_permutation",
            "base_raw_id",
            "dummy_roles_in_label_order",
            "source_placement_path",
            "full_raw_id",
        )
    return {key: row[key] for key in keys}


def theta_locator(
    origin: str,
    contract_locator: dict[str, Any],
    no_dummy: dict[str, dict[str, Any]],
    roots: dict[int, dict[str, Any]],
    six: dict[str, dict[str, Any]],
    seven: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if origin == "theta2_physical_k5":
        row = no_dummy[contract_locator["upstream_anchor_id"]]
        return {
            key: row[key]
            for key in (
                "source_index",
                "target_index",
                "permutation_index",
                "port_permutation",
                "base_raw_id",
            )
        }
    if origin == "theta2_physical_k6":
        row = six[contract_locator["path_id"]]
        root = roots[row["base_raw_id"]]
        return {
            "source_index": row["source_index"],
            "target_index": row["target_index"],
            "permutation_index": row["permutation_index"],
            "port_permutation": root["port_permutation"],
            "base_raw_id": row["base_raw_id"],
            "restored_role": row["restored_role"],
            "source_insertion_index": row["source_insertion_index"],
            "source_insertion": row["source_insertion"],
        }
    require(origin == "theta2_physical_k7", "THETA_ORIGIN", origin)
    row = seven[contract_locator["path_id"]]
    parent = six[row["parent_path_id"]]
    root = roots[row["base_raw_id"]]
    return {
        "source_index": row["source_index"],
        "target_index": row["target_index"],
        "permutation_index": row["permutation_index"],
        "port_permutation": root["port_permutation"],
        "base_raw_id": row["base_raw_id"],
        "first_restored_role": row["first_restored_role"],
        "first_source_insertion_index": row["first_source_insertion_index"],
        "first_source_insertion": parent["source_insertion"],
        "restored_role": row["restored_role"],
        "source_insertion_index": row["source_insertion_index"],
        "source_insertion": row["source_insertion"],
    }


def reconstruct_restored_four_contract_graphs(
    core,
    sources,
    targets,
    permutations,
    row: dict[str, Any],
):
    locator = row["locator"]
    source = sources[locator["source_index"]].graph
    target_record = core.relabel(
        targets[locator["target_index"]],
        permutations[locator["permutation_index"]],
    )
    target_full = target_record.graph
    for depth, step in enumerate(locator["restoration_path"]):
        source = insert_on_arc(
            source,
            step["source_insertion"],
            step["label"],
            (
                f"four_anchor_restore_{locator['raw_id']}_"
                f"{depth}_{step['source_insertion_index']}"
            ),
        )
        target_full = promote_dummy_role(
            target_full, step["restored_role"], step["label"]
        )
    require(
        not [
            node
            for node, data in target_full.nodes(data=True)
            if data.get("dummy")
        ],
        "FOUR_RESTORED_CONTRACT_DUMMY",
        row["anchor_id"],
    )
    return source, target_full


def pair_exact_maps(core, source_pair, target_pair):
    source_maps = exact_incidence_maps(
        core, source_pair[0], target_pair[0]
    )
    if not source_maps:
        return []
    target_maps = exact_incidence_maps(
        core, source_pair[1], target_pair[1]
    )
    if not target_maps:
        return []
    return source_maps, target_maps


def verify_four_port_descendant_completeness(
    contract: dict[str, Any],
    four_summary: dict[str, Any],
    raw_ledger_path: Path,
    one_port_ledger_path: Path,
    two_port_parent_path: Path,
    two_port_ledger_path: Path,
) -> dict[str, Any]:
    """Derive every graph-equality parent and bind every restoration child.

    Only the literal graph grammar and exact mixed-graph routines in the
    independent full-replay core are invoked.  No Fourier map, rank, sign,
    separator, or other model-algebra routine is called.
    """
    core = import_path("k3p_anchor_four_graph_core", FOUR_GRAPH_CORE)
    require(
        four_summary.get("artifacts", {})
        .get("full_directional_ledger.jsonl.gz", {})
        .get("sha256")
        == sha_file(raw_ledger_path),
        "FOUR_RAW_LEDGER_BINDING",
    )
    one_manifest = load_json(ONE_PORT_MANIFEST)
    two_manifest = load_json(TWO_PORT_MANIFEST)
    require(one_manifest.get("status") == "PASS", "ONE_PORT_MANIFEST_STATUS")
    require(two_manifest.get("status") == "PASS", "TWO_PORT_MANIFEST_STATUS")
    require(
        one_manifest.get("ledger_sha256") == sha_file(one_port_ledger_path),
        "ONE_PORT_LEDGER_BINDING",
    )
    require(
        two_manifest.get("parent_inventory_sha256")
        == sha_file(two_port_parent_path),
        "TWO_PORT_PARENT_BINDING",
    )
    require(
        two_manifest.get("ledger_sha256") == sha_file(two_port_ledger_path),
        "TWO_PORT_LEDGER_BINDING",
    )

    sources = core.sources()
    targets = core.targets(4, True) + core.targets(4, False)
    permutations = tuple(itertools.permutations(range(4)))
    require(len(sources) == 6, "FOUR_LITERAL_SOURCE_COUNT")
    require(len(targets) == 2_814, "FOUR_LITERAL_TARGET_COUNT")
    require(len(permutations) == 24, "FOUR_LITERAL_PERMUTATION_COUNT")

    direct_rows = [
        row
        for row in contract["anchors"]
        if row["origin"] == "four_port_direct_physical"
    ]
    restored_rows = [
        row
        for row in contract["anchors"]
        if row["origin"] == "four_port_restored_physical_k5"
    ]
    require(len(direct_rows) == 26, "FOUR_DIRECT_CONTRACT_COUNT")
    require(len(restored_rows) == 17, "FOUR_RESTORED_CONTRACT_COUNT")

    direct_seeds = []
    for row in direct_rows:
        locator = row["locator"]
        source = sources[locator["source_index"]].graph
        target = core.selected_graph(
            core.relabel(
                targets[locator["target_index"]],
                permutations[locator["permutation_index"]],
            )
        )
        require(
            graph_sha256(source) == row["source_graph_sha256"],
            "FOUR_DIRECT_SOURCE_GRAPH",
            row["anchor_id"],
        )
        require(
            graph_sha256(target) == row["target_graph_sha256"],
            "FOUR_DIRECT_TARGET_GRAPH",
            row["anchor_id"],
        )
        require(
            core.mixed_relation(source, target) == row["relation"],
            "FOUR_DIRECT_RELATION",
            row["anchor_id"],
        )
        direct_seeds.append((row, source, target))

    restored_contract_pairs = []
    for row in restored_rows:
        source, target = reconstruct_restored_four_contract_graphs(
            core, sources, targets, permutations, row
        )
        require(
            graph_sha256(source) == row["source_graph_sha256"],
            "FOUR_RESTORED_SOURCE_GRAPH",
            row["anchor_id"],
        )
        require(
            graph_sha256(target) == row["target_graph_sha256"],
            "FOUR_RESTORED_TARGET_GRAPH",
            row["anchor_id"],
        )
        require(
            core.mixed_relation(source, target) == row["relation"],
            "FOUR_RESTORED_RELATION",
            row["anchor_id"],
        )
        restored_contract_pairs.append((row, source, target))

    raw_equalities = []
    for row in iter_gzip_jsonl(raw_ledger_path):
        if row.get("graph_relation") in {"isomorphic", "triangle"}:
            raw_equalities.append(row)
    require(len(raw_equalities) == 144, "FOUR_RAW_EQUALITY_COUNT")
    require(
        collections.Counter(row["graph_relation"] for row in raw_equalities)
        == {"isomorphic": 30, "triangle": 114},
        "FOUR_RAW_EQUALITY_RELATIONS",
    )
    map_class_counts = collections.Counter()
    for relation in ("isomorphic", "triangle"):
        map_class_counts[relation] = len(
            {
                (row["source_index"], row["class_id"])
                for row in raw_equalities
                if row["graph_relation"] == relation
            }
        )
    require(
        map_class_counts == {"isomorphic": 24, "triangle": 69},
        "FOUR_ACTIVE_MAP_CLASS_COUNTS",
        map_class_counts,
    )

    one_port_rows = {}
    for row in iter_gzip_jsonl(one_port_ledger_path):
        parent_id = row.get("parent_anchor_id", "")
        if parent_id.startswith("four:"):
            key = (
                parent_id,
                row["source_site_index"],
                row["target_site_index"],
            )
            require(key not in one_port_rows, "ONE_PORT_KEY_COLLISION", key)
            one_port_rows[key] = row
    parent_inventory = {}
    for row in iter_gzip_jsonl(two_port_parent_path):
        key = row["one_port_parent_id"]
        require(
            key not in parent_inventory,
            "TWO_PORT_PARENT_COLLISION",
            key,
        )
        parent_inventory[key] = row
    require(
        len(parent_inventory) == two_manifest.get("parents") == 2_107,
        "TWO_PORT_PARENT_COUNT",
    )

    parent_mapping_rows = []
    first_mapping_rows = []
    terminal_records = []
    continuation_records = []
    dummy_multiplicity = collections.Counter()
    parent_hit_multiplicity = collections.Counter()
    for raw in raw_equalities:
        source = sources[raw["source_index"]].graph
        target_record = core.relabel(
            targets[raw["target_index"]], tuple(raw["port_permutation"])
        )
        target_full = target_record.graph
        target = core.selected_graph(target_record)
        relation = core.mixed_relation(source, target)
        require(
            relation == raw["graph_relation"],
            "FOUR_RAW_RELATION_REPLAY",
            raw["raw_id"],
        )
        dummy_roles = tuple(sorted(target_record.dummy_labels))
        dummy_multiplicity[len(dummy_roles)] += 1
        seed_matches = []
        for seed_row, seed_source, seed_target in direct_seeds:
            source_maps = exact_incidence_maps(core, source, seed_source)
            if not source_maps:
                continue
            target_maps = exact_incidence_maps(core, target, seed_target)
            if target_maps:
                seed_matches.append(
                    (
                        seed_row,
                        seed_source,
                        seed_target,
                        source_maps[0],
                        target_maps[0],
                    )
                )
        require(seed_matches, "FOUR_PARENT_UNMATCHED", raw["raw_id"])
        parent_hit_multiplicity[len(seed_matches)] += 1
        (
            seed_row,
            seed_source,
            seed_target,
            source_vertex_map,
            target_vertex_map,
        ) = seed_matches[0]
        parent_mapping_rows.append(
            {
                "raw_id": raw["raw_id"],
                "relation": relation,
                "dummy_role_count": len(dummy_roles),
                "canonical_direct_seed_id": seed_row["anchor_id"],
                "direct_contract_seed_hits": len(seed_matches),
                "source_transport_sha256": sha_object(
                    [
                        [repr(left), repr(right)]
                        for left, right in sorted(
                            source_vertex_map.items(),
                            key=lambda item: repr(item[0]),
                        )
                    ]
                ),
                "target_transport_sha256": sha_object(
                    [
                        [repr(left), repr(right)]
                        for left, right in sorted(
                            target_vertex_map.items(),
                            key=lambda item: repr(item[0]),
                        )
                    ]
                ),
            }
        )
        for role in dummy_roles:
            promoted_full = promote_dummy_role(target_full, role, 4)
            target_child = core.restrict_rooted(
                promoted_full, set(range(5))
            )
            remaining = tuple(value for value in dummy_roles if value != role)
            (
                target_site_index,
                canonical_target_child,
                _,
            ) = target_child_match(
                core,
                target,
                target_child,
                seed_target,
                seed_row["target_candidate_profile"],
                target_vertex_map,
                4,
                f"P1:{seed_row['anchor_id']}",
            )
            candidates = rooted_core_candidates(source)
            require(len(candidates) == 7, "FOUR_FIRST_CANDIDATE_COUNT")
            for candidate_index, candidate in enumerate(candidates):
                source_child = insert_on_arc(
                    source,
                    candidate,
                    4,
                    f"four_complete_{raw['raw_id']}_{role}_{candidate_index}",
                )
                source_site_index = mapped_site_index(
                    seed_row["source_candidate_profile"],
                    source_vertex_map,
                    candidate,
                )
                key = (
                    seed_row["anchor_id"],
                    source_site_index,
                    target_site_index,
                )
                require(key in one_port_rows, "FOUR_ONE_PORT_UNMATCHED", key)
                ledger_row = one_port_rows[key]
                child_relation = core.mixed_relation(
                    source_child, target_child
                )
                if child_relation in {"isomorphic", "triangle"}:
                    require(
                        ledger_row["status"] == child_relation,
                        "FOUR_ONE_PORT_EQUALITY_STATUS",
                        key,
                    )
                else:
                    require(
                        ledger_row["status"]
                        in {
                            "displayed_quartet_mismatch",
                            "k3p_tree_sunlet_sos",
                        },
                        "FOUR_ONE_PORT_NONE_STATUS",
                        key,
                    )
                one_port_parent_id = (
                    f"P1:{seed_row['anchor_id']}:"
                    f"{source_site_index}:{target_site_index}"
                )
                mapping_row = {
                    "raw_id": raw["raw_id"],
                    "role": role,
                    "candidate": candidate_index,
                    "seed": seed_row["anchor_id"],
                    "si": source_site_index,
                    "ti": target_site_index,
                    "relation": child_relation,
                    "ledger_status": ledger_row["status"],
                    "p1": one_port_parent_id,
                    "remaining": len(remaining),
                }
                first_mapping_rows.append(mapping_row)
                if child_relation in {"isomorphic", "triangle"}:
                    record = {
                        "raw_id": raw["raw_id"],
                        "source": source_child,
                        "target": target_child,
                        "target_full": promoted_full,
                        "remaining": remaining,
                        "one_port_parent_id": one_port_parent_id,
                        "canonical_source": insert_on_arc(
                            seed_source,
                            profile_candidate(
                                seed_row["source_candidate_profile"]["sites"][
                                    source_site_index
                                ]
                            ),
                            4,
                            (
                                f"P1:{seed_row['anchor_id']}",
                                "source",
                                source_site_index,
                            ),
                        ),
                        "canonical_target": canonical_target_child,
                        "mapping_row": mapping_row,
                    }
                    if remaining:
                        continuation_records.append(record)
                    else:
                        terminal_records.append(record)

    require(
        dummy_multiplicity == {0: 30, 1: 60, 2: 42, 3: 12},
        "FOUR_DUMMY_MULTIPLICITY",
        dummy_multiplicity,
    )
    require(
        parent_hit_multiplicity == {2: 44, 3: 12, 4: 88},
        "FOUR_PARENT_HIT_MULTIPLICITY",
        parent_hit_multiplicity,
    )
    require(
        len({row["canonical_direct_seed_id"] for row in parent_mapping_rows})
        == 9,
        "FOUR_PARENT_PAIR_CLASS_COUNT",
    )
    require(len(first_mapping_rows) == 1_260, "FOUR_FIRST_REQUEST_COUNT")
    first_relation_counts = collections.Counter(
        row["relation"] for row in first_mapping_rows
    )
    first_status_counts = collections.Counter(
        row["ledger_status"] for row in first_mapping_rows
    )
    require(
        first_relation_counts
        == {"isomorphic": 15, "triangle": 24, "none": 1_221},
        "FOUR_FIRST_RELATION_COUNTS",
        first_relation_counts,
    )
    require(
        first_status_counts
        == {
            "isomorphic": 15,
            "triangle": 24,
            "displayed_quartet_mismatch": 1_080,
            "k3p_tree_sunlet_sos": 141,
        },
        "FOUR_FIRST_STATUS_COUNTS",
        first_status_counts,
    )
    require(
        len({row["p1"] for row in first_mapping_rows}) == 161,
        "FOUR_FIRST_UNIQUE_P1_COUNT",
    )
    require(len(terminal_records) == 27, "FOUR_PHYSICAL_TERMINAL_COUNT")
    require(len(continuation_records) == 12, "FOUR_CONTINUATION_COUNT")
    require(
        collections.Counter(
            row["mapping_row"]["relation"] for row in terminal_records
        )
        == {"isomorphic": 15, "triangle": 12},
        "FOUR_TERMINAL_RELATION_COUNTS",
    )

    restored_pair_representatives = []
    for row, source, target in restored_contract_pairs:
        if not any(
            pair_exact_maps(
                core,
                (source, target),
                (representative[1], representative[2]),
            )
            for representative in restored_pair_representatives
        ):
            restored_pair_representatives.append((row, source, target))
    require(
        len(restored_pair_representatives) == 11,
        "FOUR_RESTORED_CONTRACT_PAIR_CLASSES",
    )
    terminal_crosswalk = []
    extra_terminal_records = []
    for record in terminal_records:
        contract_hits = [
            row["anchor_id"]
            for row, source, target in restored_contract_pairs
            if pair_exact_maps(
                core,
                (record["source"], record["target"]),
                (source, target),
            )
        ]
        terminal_row = {
            **record["mapping_row"],
            "restored_contract_pair_hits": contract_hits,
        }
        terminal_crosswalk.append(terminal_row)
        if not contract_hits:
            extra_terminal_records.append(record)
    require(
        len(terminal_records) - len(extra_terminal_records) == 19,
        "FOUR_TERMINALS_IN_CONTRACT_CLASSES",
    )
    require(len(extra_terminal_records) == 8, "FOUR_EXTRA_TERMINALS")
    require(
        {row["raw_id"] for row in extra_terminal_records}
        == {
            202225,
            202231,
            202465,
            202471,
            269761,
            269767,
            270001,
            270007,
        },
        "FOUR_EXTRA_TERMINAL_IDS",
    )
    extra_pair_representatives = []
    for record in extra_terminal_records:
        if not any(
            pair_exact_maps(
                core,
                (record["source"], record["target"]),
                (representative["source"], representative["target"]),
            )
            for representative in extra_pair_representatives
        ):
            extra_pair_representatives.append(record)
    require(
        len(extra_pair_representatives) == 4,
        "FOUR_EXTRA_TERMINAL_PAIR_CLASSES",
    )
    terminal_pair_representatives = []
    for record in terminal_records:
        if not any(
            pair_exact_maps(
                core,
                (record["source"], record["target"]),
                (representative["source"], representative["target"]),
            )
            for representative in terminal_pair_representatives
        ):
            terminal_pair_representatives.append(record)
    require(
        len(terminal_pair_representatives) == 15,
        "FOUR_TERMINAL_PAIR_CLASS_COUNT",
    )

    second_mapping_rows = []
    requested_two_port_keys = []
    for continuation in continuation_records:
        parent_id = continuation["one_port_parent_id"]
        require(
            parent_id in parent_inventory,
            "FOUR_CONTINUATION_PARENT_UNMATCHED",
            parent_id,
        )
        inventory = parent_inventory[parent_id]
        require(
            graph_sha256(continuation["canonical_source"])
            == inventory["source_graph_sha256"],
            "FOUR_CONTINUATION_SOURCE_GRAPH",
            parent_id,
        )
        require(
            graph_sha256(continuation["canonical_target"])
            == inventory["target_graph_sha256"],
            "FOUR_CONTINUATION_TARGET_GRAPH",
            parent_id,
        )
        source_maps = exact_incidence_maps(
            core,
            continuation["source"],
            continuation["canonical_source"],
        )
        target_maps = exact_incidence_maps(
            core,
            continuation["target"],
            continuation["canonical_target"],
        )
        require(source_maps and target_maps, "FOUR_CONTINUATION_TRANSPORT")
        source_vertex_map = source_maps[0]
        target_vertex_map = target_maps[0]
        require(
            len(continuation["remaining"]) == 1,
            "FOUR_CONTINUATION_REMAINING_ROLE",
        )
        role = continuation["remaining"][0]
        physical_target = promote_dummy_role(
            continuation["target_full"], role, 5
        )
        physical_target = core.restrict_rooted(
            physical_target, set(range(6))
        )
        (
            target_site_index,
            _,
            _,
        ) = target_child_match(
            core,
            continuation["target"],
            physical_target,
            continuation["canonical_target"],
            inventory["target_candidate_profile"],
            target_vertex_map,
            5,
            f"P2:{parent_id}",
        )
        candidates = rooted_core_candidates(continuation["source"])
        require(len(candidates) == 8, "FOUR_SECOND_CANDIDATE_COUNT")
        for candidate_index, candidate in enumerate(candidates):
            physical_source = insert_on_arc(
                continuation["source"],
                candidate,
                5,
                f"four_complete_second_{continuation['raw_id']}_"
                f"{candidate_index}",
            )
            source_site_index = mapped_site_index(
                inventory["source_candidate_profile"],
                source_vertex_map,
                candidate,
            )
            relation = core.mixed_relation(physical_source, physical_target)
            key = (parent_id, source_site_index, target_site_index)
            requested_two_port_keys.append(key)
            second_mapping_rows.append(
                {
                    "raw_id": continuation["raw_id"],
                    "p1": parent_id,
                    "candidate": candidate_index,
                    "si": source_site_index,
                    "ti": target_site_index,
                    "relation": relation,
                }
            )
    require(len(second_mapping_rows) == 96, "FOUR_SECOND_REQUEST_COUNT")
    require(
        len(set(requested_two_port_keys)) == 64,
        "FOUR_SECOND_UNIQUE_KEY_COUNT",
    )
    require(
        collections.Counter(row["relation"] for row in second_mapping_rows)
        == {"none": 96},
        "FOUR_SECOND_RELATION_COUNTS",
    )
    selected_two_port_rows = {}
    requested_key_set = set(requested_two_port_keys)
    for row in iter_gzip_jsonl(two_port_ledger_path):
        key = (
            row.get("one_port_parent_id"),
            row.get("second_source_site_index"),
            row.get("second_target_site_index"),
        )
        if key in requested_key_set:
            require(
                key not in selected_two_port_rows,
                "FOUR_TWO_PORT_KEY_COLLISION",
                key,
            )
            selected_two_port_rows[key] = row
    require(
        len(selected_two_port_rows) == 64,
        "FOUR_TWO_PORT_UNMATCHED",
    )
    for row, key in zip(second_mapping_rows, requested_two_port_keys):
        ledger_status = selected_two_port_rows[key]["status"]
        require(
            ledger_status
            in {"displayed_quartet_mismatch", "k3p_tree_sunlet_sos"},
            "FOUR_TWO_PORT_NONE_STATUS",
            key,
        )
        row["ledger_status"] = ledger_status
    second_status_counts = collections.Counter(
        row["ledger_status"] for row in second_mapping_rows
    )
    require(
        second_status_counts
        == {
            "displayed_quartet_mismatch": 84,
            "k3p_tree_sunlet_sos": 12,
        },
        "FOUR_SECOND_STATUS_COUNTS",
        second_status_counts,
    )

    omitted_terminal_descendants = sorted(
        [
            {
                "raw_id": record["raw_id"],
                "one_port_parent_id": record["one_port_parent_id"],
                "relation": record["mapping_row"]["relation"],
            }
            for record in extra_terminal_records
        ],
        key=lambda row: row["raw_id"],
    )
    require(
        collections.Counter(
            row["one_port_parent_id"]
            for row in omitted_terminal_descendants
        )
        == {
            "P1:four:raw154873:0:0": 2,
            "P1:four:raw154873:5:6": 2,
            "P1:four:raw154873:1:1": 2,
            "P1:four:raw154873:8:8": 2,
        },
        "FOUR_OMITTED_TERMINAL_DESCENDANTS",
    )
    continuation_crosswalk = [
        {
            "raw_id": record["raw_id"],
            "one_port_parent_id": record["one_port_parent_id"],
            "remaining_role": record["remaining"][0],
        }
        for record in continuation_records
    ]

    return {
        "method": {
            "parent_quotient": (
                "exact labelled arrowhead-preserving isomorphism on each "
                "member of the ordered source/target graph pair"
            ),
            "restoration_grammar": (
                "promote each target dummy role and insert the same new "
                "label on every nonroot source arc not ending at a leaf"
            ),
            "site_transport": (
                "unique mixed-edge image compatible with the exact parent "
                "vertex transport"
            ),
            "algebra_used": False,
        },
        "counts": {
            "raw_equality_parents": 144,
            "raw_isomorphic_parents": 30,
            "raw_triangle_parents": 114,
            "active_map_classes": 93,
            "active_isomorphic_map_classes": 24,
            "active_triangle_map_classes": 69,
            "raw_parent_pair_classes": 9,
            "direct_contract_rows": 26,
            "dummy_parent_roots": 114,
            "dummy_multiplicity": {
                str(key): value
                for key, value in sorted(dummy_multiplicity.items())
            },
            "first_restoration_requests": 1_260,
            "first_unique_one_port_rows": 161,
            "first_isomorphic": 15,
            "first_triangle": 24,
            "first_none": 1_221,
            "physical_k5_equality_terminals": 27,
            "physical_k5_terminal_pair_classes": 15,
            "terminal_isomorphic": 15,
            "terminal_triangle": 12,
            "restored_contract_rows": 17,
            "restored_contract_pair_classes": 11,
            "terminal_presentations_in_contract_pair_classes": 19,
            "additional_terminal_presentations": 8,
            "additional_terminal_pair_classes": 4,
            "equality_continuations": 12,
            "second_restoration_requests": 96,
            "second_unique_two_port_rows": 64,
            "second_none": 96,
            "mapped": 1_356,
            "unmatched": 0,
        },
        "ledger_status_counts": {
            "first": dict(sorted(first_status_counts.items())),
            "second": dict(sorted(second_status_counts.items())),
        },
        "bindings": {
            "parent_mapping_rows_sha256": sha_object(parent_mapping_rows),
            "first_mapping_rows_sha256": sha_object(first_mapping_rows),
            "terminal_crosswalk_sha256": sha_object(terminal_crosswalk),
            "second_mapping_rows_sha256": sha_object(second_mapping_rows),
            "omitted_terminal_descendants_sha256": sha_object(
                omitted_terminal_descendants
            ),
            "continuation_crosswalk_sha256": sha_object(
                continuation_crosswalk
            ),
        },
        "additional_terminal_descendants": omitted_terminal_descendants,
        "continuation_crosswalk": continuation_crosswalk,
        "continuation_parent_ids": sorted(
            {
                record["one_port_parent_id"]
                for record in continuation_records
            }
        ),
    }


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    with temporary.open("w") as handle:
        handle.write(json.dumps(value, sort_keys=True, indent=2) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def main(argv: list[str] | None = None) -> int:
    if not __debug__:
        raise CrosswalkFailure("OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer", type=Path, default=DEFAULT_PRODUCER)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument(
        "--root-movement-reconciliation",
        type=Path,
        default=DEFAULT_ROOT_MOVEMENT_RECONCILIATION,
    )
    parser.add_argument(
        "--four-raw-ledger", type=Path, default=FOUR_RAW_LEDGER
    )
    parser.add_argument(
        "--one-port-ledger", type=Path, default=ONE_PORT_LEDGER
    )
    parser.add_argument(
        "--two-port-parent-inventory",
        type=Path,
        default=TWO_PORT_PARENT_INVENTORY,
    )
    parser.add_argument(
        "--two-port-ledger", type=Path, default=TWO_PORT_LEDGER
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    started = time.monotonic()
    producer_path = args.producer.resolve()
    verifier_path = args.verifier.resolve()
    reconciliation_path = args.root_movement_reconciliation.resolve()
    four_raw_ledger_path = args.four_raw_ledger.resolve()
    one_port_ledger_path = args.one_port_ledger.resolve()
    two_port_parent_path = args.two_port_parent_inventory.resolve()
    two_port_ledger_path = args.two_port_ledger.resolve()
    producer = load_json(producer_path)
    verifier = load_json(verifier_path)
    reconciliation = load_json(reconciliation_path)
    validate_producer(producer)
    require(verifier.get("status") == "PASS", "VERIFIER_STATUS")
    require(
        verifier.get("payload_sha256")
        == sha_object(
            {
                key: value
                for key, value in verifier.items()
                if key not in {"payload_sha256", "operational"}
            }
        ),
        "VERIFIER_PAYLOAD",
    )
    verified_count = (
        verifier.get("counts", {}).get("anchors")
        or verifier.get("census", {}).get("total")
        or verifier.get("anchors_verified")
        or verifier.get("comparisons", {}).get("semantic_rows")
    )
    require(verified_count == 133, "VERIFIER_ANCHOR_COUNT", verified_count)
    verified_artifact = verifier.get("artifact", {})
    require(
        verified_artifact.get("sha256") == sha_file(producer_path)
        and verified_artifact.get("payload_sha256") == producer["payload_sha256"],
        "VERIFIER_PRODUCER_BINDING",
    )
    root_movement = verifier.get(
        "marginalized_incoming_root_movement_certificate", {}
    )
    require(
        root_movement.get("incoming_boundary_mismatch_parents") == 176,
        "MARGINALIZED_PARENT_COUNT",
    )
    require(root_movement.get("mapped") == 424, "ROOT_MOVEMENT_MAPPED")
    require(root_movement.get("unmatched") == 0, "ROOT_MOVEMENT_UNMATCHED")
    require(
        root_movement.get("terminal_paths_by_restoration_depth")
        == {"1": 56, "2": 176, "3": 192},
        "ROOT_MOVEMENT_DEPTH_COUNTS",
    )
    require(
        reconciliation.get("schema")
        == "k3p-marginalized-theta-one-port-reconciliation-v1",
        "ROOT_MOVEMENT_RECONCILIATION_SCHEMA",
    )
    require(
        reconciliation.get("status") == "PASS",
        "ROOT_MOVEMENT_RECONCILIATION_STATUS",
    )
    require(
        reconciliation.get("payload_sha256")
        == sha_object(
            {
                key: value
                for key, value in reconciliation.items()
                if key != "payload_sha256"
            }
        ),
        "ROOT_MOVEMENT_RECONCILIATION_PAYLOAD",
    )
    reconciliation_census = reconciliation.get("reconciliation_census", {})
    reconciliation_bindings = reconciliation.get("bindings", {})
    reconciliation_paths = reconciliation.get("path_crosswalk")
    reconciliation_sites = reconciliation.get("one_port_site_pairs")
    require(
        isinstance(reconciliation_paths, list)
        and len(reconciliation_paths) == 424
        and reconciliation_bindings.get("path_crosswalk_sha256")
        == sha_object(reconciliation_paths),
        "ROOT_MOVEMENT_RECONCILIATION_PATH_BINDING",
    )
    require(
        isinstance(reconciliation_sites, list)
        and len(reconciliation_sites) == 66
        and reconciliation_bindings.get("one_port_site_pair_rows_sha256")
        == sha_object(reconciliation_sites),
        "ROOT_MOVEMENT_RECONCILIATION_SITE_BINDING",
    )
    require(
        reconciliation_census.get("fully_restored_exact_paths") == 424
        and reconciliation_census.get("canonical_theta_seed_pair_classes") == 15
        and reconciliation_census.get("existing_isomorphic_one_port_rows") == 66
        and reconciliation_census.get("canonical_one_port_relation_classes") == 66
        and reconciliation_census.get("mapped") == 424
        and reconciliation_census.get("unmatched") == 0,
        "ROOT_MOVEMENT_RECONCILIATION_CENSUS",
    )
    require(
        reconciliation_bindings.get(
            "clean_room_mapping_rows_sha256"
        )
        == root_movement.get("mapping_rows_sha256"),
        "ROOT_MOVEMENT_RECONCILIATION_MAPPING_BINDING",
    )
    reconciliation_inputs = reconciliation.get("inputs", {})
    require(
        reconciliation_inputs.get("non_four_anchor_artifact", {}).get(
            "sha256"
        )
        == sha_file(producer_path),
        "ROOT_MOVEMENT_RECONCILIATION_PRODUCER_BINDING",
    )
    require(
        reconciliation_inputs.get("clean_room_core", {}).get("sha256")
        == verifier.get("independence_boundary", {}).get("core_sha256"),
        "ROOT_MOVEMENT_RECONCILIATION_CORE_BINDING",
    )
    require(
        reconciliation_inputs.get("frozen_structural_probe_contract", {}).get(
            "sha256"
        )
        == sha_file(CONTRACT),
        "ROOT_MOVEMENT_RECONCILIATION_CONTRACT_BINDING",
    )

    contract = load_json(CONTRACT)
    theta = load_gzip_json(THETA)
    cycle_rows = load_json(CYCLE)["anchors"]
    cycle_by_id = {row["anchor_id"]: row for row in cycle_rows}
    no_dummy = {row["anchor_id"]: row for row in theta["no_dummy_anchors"]}
    roots = {row["base_raw_id"]: row for row in theta["restoration_roots"]}
    six = {row["path_id"]: row for row in theta["six_port_rows"]}
    seven = {row["path_id"]: row for row in theta["seven_port_rows"]}

    producer_index = {
        (row["origin"], canonical_bytes(row["structural_locator"])): row
        for row in producer["anchors"]
    }
    require(len(producer_index) == 133, "PRODUCER_LOCATOR_UNIQUENESS")
    matched_keys = set()
    contract_ids = []
    non_four_contract_rows = []
    four_contract_rows = []
    for contract_row in contract["anchors"]:
        origin = contract_row["origin"]
        if origin.startswith("four_port"):
            four_contract_rows.append(contract_row)
            continue
        locator = contract_row["locator"]
        if origin == "tree_physical_k3":
            structural = {}
        elif origin.startswith("cycle"):
            structural = cycle_locator(cycle_by_id[locator["anchor_id"]])
        else:
            structural = theta_locator(
                origin, locator, no_dummy, roots, six, seven
            )
        key = (origin, canonical_bytes(structural))
        require(key in producer_index, "CONTRACT_LOCATOR_NOT_DERIVED", contract_row["anchor_id"])
        derived = producer_index[key]
        require(
            derived["relation"] == contract_row["relation"],
            "CONTRACT_RELATION",
            contract_row["anchor_id"],
        )
        require(
            derived["port_count"] == len(contract_row["labels"]),
            "CONTRACT_PORT_COUNT",
            contract_row["anchor_id"],
        )
        require(
            derived["source_graph_sha256"] == contract_row["source_graph_sha256"],
            "CONTRACT_SOURCE_GRAPH",
            contract_row["anchor_id"],
        )
        require(
            derived["target_graph_sha256"] == contract_row["target_graph_sha256"],
            "CONTRACT_TARGET_GRAPH",
            contract_row["anchor_id"],
        )
        matched_keys.add(derived["anchor_key"])
        contract_ids.append(contract_row["anchor_id"])
        non_four_contract_rows.append(contract_row)
    require(len(non_four_contract_rows) == 133, "CONTRACT_NON_FOUR_COUNT")
    require(
        matched_keys == {row["anchor_key"] for row in producer["anchors"]},
        "CONTRACT_NON_FOUR_EXACT_SET",
    )

    four_summary = load_json(FOUR_SUMMARY)
    four_verification = load_json(FOUR_VERIFICATION)
    require(four_verification.get("status") == "PASS", "FOUR_VERIFIER_STATUS")
    require(
        four_verification.get("counts", {}).get("probe_four_port_anchors") == 43,
        "FOUR_ANCHOR_COUNT",
    )
    require(
        four_verification.get("verified_summary_payload_sha256")
        == four_summary.get("payload_sha256_without_hash"),
        "FOUR_SUMMARY_BINDING",
    )
    require(len(four_contract_rows) == 43, "CONTRACT_FOUR_COUNT")
    four_origins = collections.Counter(row["origin"] for row in four_contract_rows)
    four_relations = collections.Counter(row["relation"] for row in four_contract_rows)
    require(
        four_origins
        == collections.Counter(
            {"four_port_direct_physical": 26, "four_port_restored_physical_k5": 17}
        ),
        "FOUR_ORIGINS",
    )
    require(
        four_relations == collections.Counter({"isomorphic": 26, "triangle": 17}),
        "FOUR_RELATIONS",
    )
    four_descendant_completeness = verify_four_port_descendant_completeness(
        contract,
        four_summary,
        four_raw_ledger_path,
        one_port_ledger_path,
        two_port_parent_path,
        two_port_ledger_path,
    )

    all_rows = contract["anchors"]
    by_origin = collections.Counter(row["origin"] for row in all_rows)
    by_relation = collections.Counter(row["relation"] for row in all_rows)
    by_port = collections.Counter(len(row["labels"]) for row in all_rows)
    require(len(all_rows) == len({row["anchor_id"] for row in all_rows}) == 176, "FULL_COUNT")
    require(by_relation == {"isomorphic": 143, "triangle": 33}, "FULL_RELATIONS")
    require(by_port == {3: 25, 4: 38, 5: 41, 6: 40, 7: 32}, "FULL_PORTS")

    report = {
        "schema": "k3p-complete-anchor-universe-crosswalk-v1",
        "status": "PASS",
        "claim_boundary": {
            "non_four_enumeration_input": "active graph-only producer plus separate no-import verifier",
            "four_port_enumeration_input": "literal graph-only replay of all 144 raw equality parents and all 1,356 fixed-full restoration requests, crosswalked through the 26 direct seeds into existing one-/two-port ledgers; the 43 contract rows remain designated serialization rows",
            "contract_role": "regression target for the derived 133 non-four rows; designated four-port serialization of 26 direct generators plus 17 physical descendants, not an exhaustive presentation quotient",
            "legacy_theta_cycle_role": "opaque locator expansion only after the derived 133-row set is fixed",
            "marginalized_incoming_role": (
                "the independent verifier maps every one of 424 fully physical "
                "restoration paths from 176 excluded parents to a canonical "
                "theta seed plus one transported downstream port; zero unmatched"
            ),
            "k2p_algebra_active": False,
        },
        "bindings": {
            "crosswalk_verifier_sha256": sha_file(Path(__file__).resolve()),
            "producer_sha256": sha_file(producer_path),
            "producer_payload_sha256": producer["payload_sha256"],
            "independent_verifier_sha256": sha_file(verifier_path),
            "root_movement_reconciliation_sha256": sha_file(
                reconciliation_path
            ),
            "root_movement_reconciliation_payload_sha256": reconciliation[
                "payload_sha256"
            ],
            "contract_sha256": sha_file(CONTRACT),
            "theta_locator_dictionary_sha256": sha_file(THETA),
            "cycle_locator_dictionary_sha256": sha_file(CYCLE),
            "four_summary_sha256": sha_file(FOUR_SUMMARY),
            "four_independent_verification_sha256": sha_file(FOUR_VERIFICATION),
            "four_graph_core_sha256": sha_file(FOUR_GRAPH_CORE),
            "four_raw_ledger_sha256": sha_file(four_raw_ledger_path),
            "one_port_manifest_sha256": sha_file(ONE_PORT_MANIFEST),
            "one_port_ledger_sha256": sha_file(one_port_ledger_path),
            "two_port_manifest_sha256": sha_file(TWO_PORT_MANIFEST),
            "two_port_parent_inventory_sha256": sha_file(
                two_port_parent_path
            ),
            "two_port_ledger_sha256": sha_file(two_port_ledger_path),
        },
        "counts": {
            "non_four_derived_and_crosswalked": 133,
            "four_port_active_and_crosswalked": 43,
            "complete": 176,
            "excluded_marginalized_incoming_parents": 176,
            "excluded_paths_root_movement_mapped": 424,
            "excluded_paths_root_movement_unmatched": 0,
            "excluded_paths_existing_one_port_rows": 66,
            "excluded_paths_existing_one_port_relation_classes": 66,
            "by_origin": dict(sorted(by_origin.items())),
            "by_relation": dict(sorted(by_relation.items())),
            "by_port_count": {
                str(key): value for key, value in sorted(by_port.items())
            },
        },
        "ordered_non_four_contract_id_sha256": sha_object(contract_ids),
        "ordered_complete_contract_row_hash_sha256": sha_object(
            contract["ordered_anchor_row_hashes"]
        ),
        "four_port_descendant_completeness": four_descendant_completeness,
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
        "K3P_COMPLETE_ANCHOR_UNIVERSE_CROSSWALK_PASS "
        f"anchors=176 runtime_seconds={elapsed:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
