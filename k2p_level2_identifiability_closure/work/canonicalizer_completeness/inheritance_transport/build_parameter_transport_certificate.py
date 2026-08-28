#!/usr/bin/env python3
"""Build graph-derived K2P parameter-transport certificates.

This layer is deliberately derived from, and separate from, the frozen graph
and restoration ledgers.  It binds the missing passage from a labelled mixed-
graph transport to paired K2P edge products and to the identity/complement
action on ordered inheritance parameters.  Ordinary-triangle parameters are
marked as local-section parameters rather than being assigned a spurious
affine transport.
"""

from __future__ import annotations

import argparse
import ast
import collections
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import decode_json_document  # noqa: E402

PROBE_AUDIT = PROJECT / "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py"
PROBE_PACKAGE = PROJECT / "work/probe_coherence_corrected"
PROBE_CONTRACT = PROJECT / "work/adversarial_proof_review/probe_input_contract.json"
PROBE_RECONSTRUCTOR = PROJECT / "work/adversarial_proof_review/verify_probe_input_contract.py"
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
CYCLE_COMMON = PROJECT / "work/cycle_three_port_closure/cycle_common.py"
CYCLE_GENERATOR = PROJECT / "work/cycle_three_port_closure/generate_cycle_closure.py"
RESTORATION_GENERATOR = PROJECT / "work/restoration_forest/enumerate_five_port.py"
RESTORATION_CERTIFICATE = PROJECT / "work/restoration_sign_reclassification/corrected_restoration_forest.json"

RELATION_LEDGER = "probe_relation_parameter_transports.jsonl.gz"
RESTRICTION_LEDGER = "probe_restriction_parameter_transports.jsonl.gz"
RESTORATION_LEDGER = "restoration_restriction_parameter_transports.jsonl.gz"
CERTIFICATE = "parameter_transport_certificate.json"


class Failure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def import_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"import:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def edge_key(left: Any, right: Any) -> tuple[str, str]:
    return tuple(sorted((repr(left), repr(right))))


def arc_payload(arc: tuple[Any, Any]) -> list[str]:
    return [repr(arc[0]), repr(arc[1])]


def graph_root(graph) -> Any:
    roots = [
        node for node, data in graph.nodes(data=True)
        if data.get("role") == "root" or graph.in_degree(node) == 0
    ]
    require(len(roots) == 1, f"root multiplicity:{len(roots)}")
    return roots[0]


def graph_reticulations(graph) -> tuple[Any, ...]:
    return tuple(sorted(
        (
            node for node, data in graph.nodes(data=True)
            if data.get("role") == "retic" and graph.in_degree(node) == 2
        ),
        key=repr,
    ))


def physical_edge_groups(atlas, graph) -> dict[tuple[str, str], tuple[tuple[Any, Any], ...]]:
    """Lift each root-suppressed mixed edge to its rooted serial factors."""
    mixed = atlas.sd0_mixed(graph)
    root = graph_root(graph)
    root_children = tuple(graph.successors(root))
    require(len(root_children) == 2, "binary root")
    root_edge = edge_key(*root_children)
    result: dict[tuple[str, str], tuple[tuple[Any, Any], ...]] = {}
    for left, right in mixed.edges():
        key = edge_key(left, right)
        if key == root_edge:
            factors = tuple(sorted(((root, root_children[0]), (root, root_children[1])), key=repr))
        elif graph.has_edge(left, right):
            factors = ((left, right),)
        elif graph.has_edge(right, left):
            factors = ((right, left),)
        else:
            raise Failure(f"mixed edge has no rooted lift:{key}")
        result[key] = factors
    return result


def physical_parent_incidence(graph, reticulation: Any, parent: Any) -> tuple[tuple[str, str], bool]:
    """Return the mixed incoming incidence, including a suppressed root arc."""
    root = graph_root(graph)
    if parent != root:
        return edge_key(parent, reticulation), False
    children = tuple(graph.successors(root))
    require(len(children) == 2 and reticulation in children, "root-reticulation incidence")
    other = children[0] if children[1] == reticulation else children[1]
    return edge_key(other, reticulation), True


def relation_parameter_row(
    atlas,
    graph_sha,
    source,
    target,
    transport: dict[str, Any],
    transport_id: str,
    occurrence_id: str,
    occurrence_kind: str,
) -> dict[str, Any]:
    """Derive the paired-edge and inheritance action of one graph transport."""
    vertex_map = dict(transport["vertex_map"])
    mixed_edge_map = {
        tuple(source_edge): tuple(target_edge)
        for source_edge, target_edge in transport["mixed_edge_map"]
    }
    source_groups = physical_edge_groups(atlas, source)
    target_groups = physical_edge_groups(atlas, target)
    require(set(mixed_edge_map) == set(source_groups), f"relation source edge coverage:{occurrence_id}")
    require(set(mixed_edge_map.values()) == set(target_groups), f"relation target edge coverage:{occurrence_id}")

    source_triangle = {
        tuple(edge) for edge in (transport.get("source_triangle_edges") or [])
    }
    target_triangle = {
        tuple(edge) for edge in (transport.get("target_triangle_edges") or [])
    }
    edge_actions = []
    for source_edge in sorted(source_groups):
        target_edge = mixed_edge_map[source_edge]
        triangle_local = source_edge in source_triangle or target_edge in target_triangle
        edge_actions.append({
            "mode": "ordinary_triangle_local_section" if triangle_local else "paired_K2P_product",
            "source_physical_edge": list(source_edge),
            "target_physical_edge": list(target_edge),
            "source_rooted_factors": [arc_payload(arc) for arc in source_groups[source_edge]],
            "target_rooted_factors": [arc_payload(arc) for arc in target_groups[target_edge]],
            "s_action": "local_section" if triangle_local else "match_products",
            "g_action": "local_section" if triangle_local else "match_products",
        })

    ordinary = transport.get("ordinary_triangle_arrowhead_witness") or {}
    source_common = ordinary.get("source_common_reticulation")
    target_common = ordinary.get("target_common_reticulation")
    target_nodes = {repr(node): node for node in target.nodes()}
    inheritance_actions = []
    affine_target_reticulations: set[str] = set()
    for source_reticulation in graph_reticulations(source):
        source_name = repr(source_reticulation)
        if source_name == source_common:
            require(transport["relation"] == "triangle", f"triangle-local mode outside triangle:{occurrence_id}")
            inheritance_actions.append({
                "mode": "ordinary_triangle_local_section",
                "source_reticulation": source_common,
                "target_reticulation": target_common,
                "section_certificate": "rank_nine_ordinary_triangle_common_germ",
            })
            continue
        require(source_name in vertex_map, f"missing reticulation vertex map:{occurrence_id}:{source_name}")
        target_name = vertex_map[source_name]
        require(target_name in target_nodes, f"missing target reticulation node:{occurrence_id}:{target_name}")
        target_reticulation = target_nodes[target_name]
        require(
            target.nodes[target_reticulation].get("role") == "retic"
            and target.in_degree(target_reticulation) == 2,
            f"nontriangle reticulation mapped to nonreticulation:{occurrence_id}:{source_name}",
        )
        source_parents = tuple(sorted(source.predecessors(source_reticulation), key=repr))
        target_parents = tuple(sorted(target.predecessors(target_reticulation), key=repr))
        source_incidences = [physical_parent_incidence(source, source_reticulation, parent) for parent in source_parents]
        target_incidences = [physical_parent_incidence(target, target_reticulation, parent) for parent in target_parents]
        target_lookup = {incidence: index for index, (incidence, _) in enumerate(target_incidences)}
        mapped = [mixed_edge_map.get(incidence) for incidence, _ in source_incidences]
        require(all(item in target_lookup for item in mapped), f"incoming incidence map:{occurrence_id}:{source_name}")
        permutation = tuple(target_lookup[item] for item in mapped)
        require(permutation in {(0, 1), (1, 0)}, f"parent permutation:{occurrence_id}:{source_name}:{permutation}")
        flip = permutation == (1, 0)
        inheritance_actions.append({
            "mode": "affine_parent_transport",
            "source_reticulation": source_name,
            "target_reticulation": target_name,
            "source_ordered_parents": [repr(parent) for parent in source_parents],
            "target_ordered_parents": [repr(parent) for parent in target_parents],
            "source_ordered_incoming_physical_edges": [list(item[0]) for item in source_incidences],
            "target_ordered_incoming_physical_edges": [list(item[0]) for item in target_incidences],
            "source_parent_index_to_target_parent_index": list(permutation),
            "source_lambda_parent_index": 1,
            "target_lambda_parent_index": 1,
            "target_lambda_from_source": "one_minus_lambda" if flip else "lambda",
            "parent_order_reversed": flip,
            "root_suppressed_incoming_incidence": any(item[1] for item in source_incidences + target_incidences),
        })
        affine_target_reticulations.add(target_name)

    expected_target_affine = {
        repr(node) for node in graph_reticulations(target) if repr(node) != target_common
    }
    require(
        affine_target_reticulations == expected_target_affine,
        f"target affine reticulation coverage:{occurrence_id}",
    )
    payload = {
        "schema": "k2p_graph_derived_relation_parameter_transport_v1",
        "occurrence_id": occurrence_id,
        "occurrence_kind": occurrence_kind,
        "relation": transport["relation"],
        "transport_id": transport_id,
        "source_graph_sha256": graph_sha(source),
        "target_graph_sha256": graph_sha(target),
        "edge_actions": edge_actions,
        "inheritance_actions": inheritance_actions,
        "triangle_local_parameters_are_not_affine_parent_flips": True,
    }
    return payload


def restrict_with_provenance(atlas, graph, keep_labels: set[int]):
    """Independently mirror restrict_rooted while retaining contracted arcs."""
    restricted = graph.copy()
    provenance = {(tail, head): {(tail, head)} for tail, head in restricted.edges()}

    def remove_node(node: Any) -> None:
        for edge in list(restricted.in_edges(node)) + list(restricted.out_edges(node)):
            provenance.pop(edge, None)
        restricted.remove_node(node)

    for node, data in list(restricted.nodes(data=True)):
        if data.get("role") == "leaf" and data.get("label") not in keep_labels:
            remove_node(node)
    changed = True
    while changed:
        changed = False
        for node, data in list(restricted.nodes(data=True)):
            if restricted.out_degree(node) == 0 and not (
                data.get("role") == "leaf" and data.get("label") in keep_labels
            ):
                remove_node(node)
                changed = True
                break
        if changed:
            continue
        for node, data in list(restricted.nodes(data=True)):
            if (
                data.get("role") != "leaf"
                and restricted.in_degree(node) == 1
                and restricted.out_degree(node) == 1
            ):
                parent = next(restricted.predecessors(node))
                child = next(restricted.successors(node))
                combined = provenance[(parent, node)] | provenance[(node, child)]
                remove_node(node)
                if parent != child and not restricted.has_edge(parent, child):
                    restricted.add_edge(parent, child, edge_role="suppressed")
                    provenance[(parent, child)] = combined
                changed = True
                break
        if changed:
            continue
        roots = [node for node in restricted if restricted.in_degree(node) == 0]
        if (
            len(roots) == 1
            and restricted.nodes[roots[0]].get("role") != "leaf"
            and restricted.out_degree(roots[0]) == 1
        ):
            remove_node(roots[0])
            changed = True
    for node, data in restricted.nodes(data=True):
        if data.get("label") in keep_labels:
            data["role"] = "leaf"
        elif restricted.in_degree(node) == 0:
            data["role"] = "root"
        elif restricted.in_degree(node) == 2:
            data["role"] = "retic"
        else:
            data["role"] = "tree"
    reference = atlas.restrict_rooted(graph, keep_labels)
    require(set(restricted.nodes()) == set(reference.nodes()), "restriction node replay")
    require(set(restricted.edges()) == set(reference.edges()), "restriction edge replay")
    require(
        all(restricted.nodes[node].get("role") == reference.nodes[node].get("role") for node in restricted),
        "restriction role replay",
    )
    return restricted, provenance


def restriction_parameter_row(
    atlas,
    graph_sha,
    child,
    parent,
    keep_labels: set[int],
    occurrence_id: str,
    occurrence_kind: str,
    restriction_id: str | None = None,
) -> dict[str, Any]:
    restricted, provenance = restrict_with_provenance(atlas, child, keep_labels)
    require(
        atlas.sd0_mixed(restricted).number_of_nodes() == atlas.sd0_mixed(parent).number_of_nodes(),
        f"restriction mixed node count:{occurrence_id}",
    )
    # Restoration restrictions have exact node names. Probe restrictions are
    # independently checked by their frozen mixed-graph hashes below.
    parent_groups = physical_edge_groups(atlas, parent)
    child_arcs = set(child.edges())
    used_child_arcs: set[tuple[Any, Any]] = set()
    edge_actions = []
    for physical_edge in sorted(parent_groups):
        parent_factors = parent_groups[physical_edge]
        child_factors: set[tuple[Any, Any]] = set()
        for parent_arc in parent_factors:
            require(parent_arc in provenance, f"missing parent arc provenance:{occurrence_id}:{parent_arc}")
            child_factors.update(provenance[parent_arc])
        require(child_factors <= child_arcs, f"unknown child factor:{occurrence_id}")
        used_child_arcs.update(child_factors)
        edge_actions.append({
            "mode": "paired_serial_product",
            "parent_physical_edge": list(physical_edge),
            "parent_rooted_factors": [arc_payload(arc) for arc in parent_factors],
            "child_rooted_factors": [arc_payload(arc) for arc in sorted(child_factors, key=repr)],
            "parent_s_from_child": "product",
            "parent_g_from_child": "product",
            "root_suppressed_parent_edge": len(parent_factors) == 2,
        })

    child_root = graph_root(child)
    parent_root = graph_root(parent)
    mapped_child_reticulations: set[Any] = set()
    inheritance_actions = []
    for parent_reticulation in graph_reticulations(parent):
        require(parent_reticulation in child, f"parent reticulation absent in child:{occurrence_id}")
        require(
            child.nodes[parent_reticulation].get("role") == "retic"
            and child.in_degree(parent_reticulation) == 2,
            f"parent reticulation not binary in child:{occurrence_id}:{parent_reticulation}",
        )
        parent_parents = tuple(sorted(parent.predecessors(parent_reticulation), key=repr))
        child_parents = tuple(sorted(child.predecessors(parent_reticulation), key=repr))
        permutation = []
        for child_parent in child_parents:
            child_arc = (child_parent, parent_reticulation)
            matches = [
                index for index, parent_parent in enumerate(parent_parents)
                if child_arc in provenance[(parent_parent, parent_reticulation)]
            ]
            require(len(matches) == 1, f"restriction parent incidence uniqueness:{occurrence_id}")
            permutation.append(matches[0])
        require(tuple(permutation) in {(0, 1), (1, 0)}, f"restriction parent permutation:{occurrence_id}")
        flip = tuple(permutation) == (1, 0)
        inheritance_actions.append({
            "mode": "affine_parent_transport",
            "child_reticulation": repr(parent_reticulation),
            "parent_reticulation": repr(parent_reticulation),
            "child_ordered_parents": [repr(node) for node in child_parents],
            "parent_ordered_parents": [repr(node) for node in parent_parents],
            "child_parent_index_to_parent_parent_index": permutation,
            "child_lambda_parent_index": 1,
            "parent_lambda_parent_index": 1,
            "parent_lambda_from_child": "one_minus_lambda" if flip else "lambda",
            "parent_order_reversed": flip,
            "root_suppressed_incoming_incidence": (
                child_root in child_parents or parent_root in parent_parents
            ),
        })
        mapped_child_reticulations.add(parent_reticulation)

    forgotten_reticulations = [
        repr(node) for node in graph_reticulations(child)
        if node not in mapped_child_reticulations
    ]
    payload = {
        "schema": "k2p_graph_derived_restriction_parameter_transport_v1",
        "occurrence_id": occurrence_id,
        "occurrence_kind": occurrence_kind,
        "restriction_id": restriction_id,
        "removed_labels": sorted(
            data.get("label") for _, data in child.nodes(data=True)
            if isinstance(data.get("label"), int) and data.get("label") not in keep_labels
        ),
        "kept_labels": sorted(keep_labels),
        "child_graph_sha256": graph_sha(child),
        "parent_graph_sha256": graph_sha(parent),
        "restricted_child_graph_sha256": graph_sha(restricted),
        "edge_actions": edge_actions,
        "inheritance_actions": inheritance_actions,
        "forgotten_child_rooted_arcs": [
            arc_payload(arc) for arc in sorted(child_arcs - used_child_arcs, key=repr)
        ],
        "forgotten_reticulations": forgotten_reticulations,
    }
    return payload


class LedgerWriter:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.open("wb")
        self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.rows = 0
        self.root = sha([])
        self.counts = collections.Counter()

    def add(self, payload: dict[str, Any], count_keys: Iterable[str] = ()) -> None:
        row = dict(payload)
        row_sha = sha(row)
        wrapped = {"row": row, "row_sha256": row_sha}
        self.stream.write(canonical_bytes(wrapped) + b"\n")
        self.root = sha({"previous": self.root, "row_sha256": row_sha})
        self.rows += 1
        for key in count_keys:
            self.counts[key] += 1

    def close(self) -> dict[str, Any]:
        self.stream.close()
        self.raw.close()
        return {
            "path": self.path.name,
            "rows": self.rows,
            "ordered_hash_root": self.root,
            "sha256": sha_file(self.path),
            "bytes": self.path.stat().st_size,
            "counts": dict(sorted(self.counts.items())),
        }


def action_count_keys(row: dict[str, Any]) -> list[str]:
    keys = [f"occurrence:{row['occurrence_kind']}"]
    for action in row["inheritance_actions"]:
        if action["mode"] == "ordinary_triangle_local_section":
            keys.append("inheritance:triangle_local_section")
        elif action.get("parent_order_reversed"):
            keys.append("inheritance:complement")
        else:
            keys.append("inheritance:identity")
        if action.get("root_suppressed_incoming_incidence"):
            keys.append("inheritance:root_suppressed_incoming")
    return keys


def mixed_hash(probe, atlas, graph) -> str:
    return probe.mixed_graph_sha(atlas, graph)


def build(output_dir: Path) -> dict[str, Any]:
    require(__debug__, "optimized Python is forbidden")
    output_dir.mkdir(parents=True, exist_ok=True)
    probe = import_path("parameter_transport_probe_audit", PROBE_AUDIT)
    primitive = probe.import_path("parameter_transport_probe_reconstructor", PROBE_RECONSTRUCTOR)
    atlas = primitive.load_module("parameter_transport_atlas", ATLAS_PATH)
    common = primitive.load_module("cycle_common", CYCLE_COMMON)
    cycle_generator = primitive.load_module("parameter_transport_cycle_generator", CYCLE_GENERATOR)
    upstream = primitive.prepare_upstream(atlas, common, cycle_generator)
    contract = decode_json_document(
        PROBE_CONTRACT.read_bytes(),
        label=PROBE_CONTRACT.name,
        require_object=True,
    )

    transports: dict[str, dict[str, Any]] = {}
    for _, wrapped in probe.iter_jsonl(PROBE_PACKAGE / "exact_transport_ledger.jsonl.gz"):
        transports[wrapped["record_id"]] = wrapped["record"]
    require(len(transports) == 67_741, "exact transport input census")
    restrictions: dict[str, dict[str, Any]] = {}
    restriction_index: dict[tuple[str, str, int], str] = {}
    for _, wrapped in probe.iter_jsonl(PROBE_PACKAGE / "parent_restriction_ledger.jsonl.gz"):
        record_id, record = wrapped["record_id"], wrapped["record"]
        restrictions[record_id] = record
        key = (
            record["parent_mixed_graph_sha256"],
            record["restricted_mixed_graph_sha256"],
            record["removed_label"],
        )
        previous = restriction_index.setdefault(key, record_id)
        require(previous == record_id, f"restriction index collision:{key}")
    require(len(restrictions) == 4_379, "restriction input census")

    relation_writer = LedgerWriter(output_dir / RELATION_LEDGER)
    restriction_writer = LedgerWriter(output_dir / RESTRICTION_LEDGER)
    restoration_writer = LedgerWriter(output_dir / RESTORATION_LEDGER)
    used_transports: set[str] = set()
    used_restrictions: set[str] = set()

    def emit_relation(source, target, transport_id: str, occurrence_id: str, kind: str) -> dict[str, Any]:
        require(transport_id in transports, f"transport reference:{occurrence_id}")
        row = relation_parameter_row(
            atlas, probe.graph_sha, source, target, transports[transport_id],
            transport_id, occurrence_id, kind,
        )
        relation_writer.add(row, action_count_keys(row))
        used_transports.add(transport_id)
        return row

    def restriction_id_for(child, parent, removed_label: int) -> str:
        restricted = atlas.restrict_rooted(child, set(probe.labels_of(parent)))
        key = (mixed_hash(probe, atlas, parent), mixed_hash(probe, atlas, restricted), removed_label)
        require(key in restriction_index, f"restriction lookup:{key}")
        return restriction_index[key]

    def emit_probe_restriction(child, parent, removed_label: int, occurrence_id: str, kind: str) -> str:
        record_id = restriction_id_for(child, parent, removed_label)
        row = restriction_parameter_row(
            atlas, probe.graph_sha, child, parent, set(probe.labels_of(parent)),
            occurrence_id, kind, record_id,
        )
        record = restrictions[record_id]
        restricted = atlas.restrict_rooted(child, set(probe.labels_of(parent)))
        require(record["parent_mixed_graph_sha256"] == mixed_hash(probe, atlas, parent), f"parent hash:{occurrence_id}")
        require(record["restricted_mixed_graph_sha256"] == mixed_hash(probe, atlas, restricted), f"restricted hash:{occurrence_id}")
        restriction_writer.add(row, action_count_keys(row))
        used_restrictions.add(record_id)
        return record_id

    anchors: dict[str, dict[str, Any]] = {}
    for contract_anchor in contract["anchors"]:
        anchor_id = contract_anchor["anchor_id"]
        source, target = primitive.reconstruct_anchor(atlas, upstream, contract_anchor)
        transport_id = contract_anchor["parent_transport"]["transport_sha256"]
        emit_relation(source, target, transport_id, f"anchor:{anchor_id}", "probe_anchor")
        anchors[anchor_id] = {
            "source": source,
            "target": target,
            "source_profile": contract_anchor["source_candidate_profile"],
            "target_profile": contract_anchor["target_candidate_profile"],
            "labels": tuple(contract_anchor["labels"]),
        }

    one_parents: dict[str, dict[str, Any]] = {}
    one_path = PROBE_PACKAGE / "one_port_ledger.jsonl.gz"
    current_anchor = None
    source_children: list[dict[str, Any]] = []
    target_children: list[dict[str, Any]] = []
    for row_number, row in probe.iter_jsonl(one_path):
        anchor_id = row["parent_anchor_id"]
        anchor = anchors[anchor_id]
        if anchor_id != current_anchor:
            label = row["inserted_label"]
            source_children = []
            for index, site in enumerate(anchor["source_profile"]["sites"]):
                child = probe.insert_at_site(
                    primitive, anchor["source"], site, label,
                    (f"P1:{anchor_id}", "source", index),
                )
                restriction_id = emit_probe_restriction(
                    child, anchor["source"], label,
                    f"one:{anchor_id}:source:{index}", "probe_one_port_restriction",
                )
                source_children.append({"graph": child, "restriction_id": restriction_id})
            target_children = []
            for index, site in enumerate(anchor["target_profile"]["sites"]):
                child = probe.insert_at_site(
                    primitive, anchor["target"], site, label,
                    (f"P1:{anchor_id}", "target", index),
                )
                restriction_id = emit_probe_restriction(
                    child, anchor["target"], label,
                    f"one:{anchor_id}:target:{index}", "probe_one_port_restriction",
                )
                target_children.append({"graph": child, "restriction_id": restriction_id})
            current_anchor = anchor_id
        source_child = source_children[row["source_site_index"]]
        target_child = target_children[row["target_site_index"]]
        require(row["source_parent_restriction_id"] == source_child["restriction_id"], f"one source restriction:{row_number}")
        require(row["target_parent_restriction_id"] == target_child["restriction_id"], f"one target restriction:{row_number}")
        if row["status"] in {"isomorphic", "triangle"}:
            emit_relation(
                source_child["graph"], target_child["graph"], row["transport_id"],
                f"one:{row_number}", "probe_one_port_equality",
            )
            parent_id = f"P1:{anchor_id}:{row['source_site_index']}:{row['target_site_index']}"
            one_parents[parent_id] = {
                "source": source_child["graph"],
                "target": target_child["graph"],
                "base_anchor_id": anchor_id,
                "first_label": row["inserted_label"],
            }
    require(len(one_parents) == 2_107, "one-port equality parent census")

    for _, inventory in probe.iter_jsonl(PROBE_PACKAGE / "two_port_parent_inventory.jsonl.gz"):
        parent = one_parents[inventory["one_port_parent_id"]]
        parent["source_profile"] = inventory["source_candidate_profile"]
        parent["target_profile"] = inventory["target_candidate_profile"]

    current_parent = None
    source_children = []
    target_children = []
    for row_number, row in probe.iter_jsonl(PROBE_PACKAGE / "two_port_ledger.jsonl.gz"):
        parent_id = row["one_port_parent_id"]
        parent = one_parents[parent_id]
        if parent_id != current_parent:
            label = row["second_label"]
            source_children = []
            for index, site in enumerate(parent["source_profile"]["sites"]):
                child = probe.insert_at_site(
                    primitive, parent["source"], site, label,
                    (f"P2:{parent_id}", "source", index),
                )
                restriction_id = emit_probe_restriction(
                    child, parent["source"], label,
                    f"two:{parent_id}:source:{index}", "probe_two_port_restriction",
                )
                source_children.append({"graph": child, "restriction_id": restriction_id})
            target_children = []
            for index, site in enumerate(parent["target_profile"]["sites"]):
                child = probe.insert_at_site(
                    primitive, parent["target"], site, label,
                    (f"P2:{parent_id}", "target", index),
                )
                restriction_id = emit_probe_restriction(
                    child, parent["target"], label,
                    f"two:{parent_id}:target:{index}", "probe_two_port_restriction",
                )
                target_children.append({"graph": child, "restriction_id": restriction_id})
            current_parent = parent_id
        source_child = source_children[row["second_source_site_index"]]
        target_child = target_children[row["second_target_site_index"]]
        require(row["source_parent_restriction_id"] == source_child["restriction_id"], f"two source restriction:{row_number}")
        require(row["target_parent_restriction_id"] == target_child["restriction_id"], f"two target restriction:{row_number}")
        if row["status"] not in {"isomorphic", "triangle"}:
            continue
        emit_relation(
            source_child["graph"], target_child["graph"], row["transport_id"],
            f"two:{row_number}", "probe_two_port_equality",
        )
        reverse = row["reverse_order_certificate"]
        base = anchors[parent["base_anchor_id"]]
        keep = set(base["labels"]) | {row["second_label"]}
        reverse_source = atlas.restrict_rooted(source_child["graph"], keep)
        reverse_target = atlas.restrict_rooted(target_child["graph"], keep)
        reverse_source = probe.relabel_leaf(reverse_source, row["second_label"], parent["first_label"])
        reverse_target = probe.relabel_leaf(reverse_target, row["second_label"], parent["first_label"])
        emit_relation(
            reverse_source, reverse_target, reverse["reverse_parent_transport_id"],
            f"reverse:{row_number}", "probe_reverse_one_port_marginal",
        )

    require(len(used_transports) == len(transports) == 67_741, "complete exact transport use")
    require(len(used_restrictions) == len(restrictions) == 4_379, "complete restriction-record use")

    # Restoration restrictions: first source/target classes, then every side of
    # each second restoration edge.  These are rebuilt from primitive roots.
    restoration = import_path("parameter_transport_restoration", RESTORATION_GENERATOR)
    restoration_atlas = restoration.load_atlas()
    sources = restoration_atlas.source_supports()
    targets = (
        restoration_atlas.target_completions(4, True)
        + restoration_atlas.target_completions(4, False)
    )
    roots, _, canonical_parent_count = restoration.reconstruct_roots(restoration_atlas, sources, targets)
    require(canonical_parent_count == 997 and len(roots) == 2_540, "restoration parent census")
    root_by_id = {row["root_id"]: row for row in roots}
    first_source_seen: set[tuple[int, int]] = set()
    first_target_seen: set[tuple[int, tuple[int, ...], str]] = set()
    first_source_graphs: dict[tuple[int, int], Any] = {}
    first_target_graphs: dict[tuple[int, tuple[int, ...], str], tuple[Any, Any]] = {}
    for root in roots:
        for index, insertion in enumerate(root["source_insertion_edge_candidates"]):
            key = (root["source_index"], index)
            if key not in first_source_seen:
                first_source_seen.add(key)
                parent = sources[key[0]].graph
                child = restoration.insert_source_leaf(restoration_atlas, parent, insertion, 4)
                first_source_graphs[key] = child
                row = restriction_parameter_row(
                    restoration_atlas, probe.graph_sha, child, parent, set(range(4)),
                    f"restoration:first:source:{key[0]}:{key[1]}",
                    "restoration_first_source_restriction", None,
                )
                restoration_writer.add(row, action_count_keys(row))
        for role in root["dummy_roles"]:
            key = (root["target_index"], tuple(root["port_match"]), role)
            if key not in first_target_seen:
                first_target_seen.add(key)
                _, child = restoration.promoted_target(
                    restoration_atlas, targets, key[0], key[1], key[2], 4
                )
                parent = restoration_atlas.selected_graph_from_completion(
                    restoration_atlas.relabel_record(targets[key[0]], key[1])
                )
                first_target_graphs[key] = (child, parent)
                row = restriction_parameter_row(
                    restoration_atlas, probe.graph_sha, child, parent, set(range(4)),
                    f"restoration:first:target:{key[0]}:{sha(list(key[1]))}:{key[2]}",
                    "restoration_first_target_restriction", None,
                )
                restoration_writer.add(row, action_count_keys(row))
    require(len(first_source_seen) == 42, "restoration first source class census")
    require(len(first_target_seen) == 4_986, "restoration first target class census")

    corrected = decode_json_document(
        RESTORATION_CERTIFICATE.read_bytes(),
        label=RESTORATION_CERTIFICATE.name,
        require_object=True,
    )
    continuations = [row for row in corrected["first_coverage"] if row["status"] == "continuation"]
    require(len(continuations) == 32, "restoration continuation census")
    second_rows = corrected["second_coverage"]
    second_ordinal = 0
    for continuation in continuations:
        root = root_by_id[continuation["root_id"]]
        first_source = first_source_graphs[(root["source_index"], continuation["source_insertion_index"])]
        first_role = continuation["restored_role"]
        remaining_role = continuation["remaining_roles"][0]
        first_target_full, first_target = restoration.promoted_target(
            restoration_atlas, targets, root["target_index"], tuple(root["port_match"]), first_role, 4
        )
        second_target_full = first_target_full.copy()
        nodes = [
            node for node, data in second_target_full.nodes(data=True)
            if data.get("dummy_name") == remaining_role
        ]
        require(len(nodes) == 1, "second target promoted role")
        second_target_full.nodes[nodes[0]]["label"] = 5
        second_target_full.nodes[nodes[0]]["dummy"] = False
        second_target_full.nodes[nodes[0]]["dummy_name"] = None
        second_target = restoration_atlas.restrict_rooted(second_target_full, set(range(6)))
        candidates = restoration.source_insertion_candidates(first_source)
        require(len(candidates) == 8, "second source candidate census")
        for second_index, candidate in enumerate(candidates):
            bound = second_rows[second_ordinal]
            require(bound["parent_first_coverage_index"] == continuation["ordinal"], "second parent ordinal")
            second_source = restoration.insert_source_leaf(
                restoration_atlas, first_source, candidate, 5
            )
            source_row = restriction_parameter_row(
                restoration_atlas, probe.graph_sha, second_source, first_source, set(range(5)),
                f"restoration:second:{second_ordinal}:source",
                "restoration_second_source_restriction", None,
            )
            target_row = restriction_parameter_row(
                restoration_atlas, probe.graph_sha, second_target, first_target, set(range(5)),
                f"restoration:second:{second_ordinal}:target",
                "restoration_second_target_restriction", None,
            )
            restoration_writer.add(source_row, action_count_keys(source_row))
            restoration_writer.add(target_row, action_count_keys(target_row))
            second_ordinal += 1
    require(second_ordinal == len(second_rows) == 256, "second restoration edge census")

    ledgers = {
        "probe_relations": relation_writer.close(),
        "probe_restrictions": restriction_writer.close(),
        "restoration_restrictions": restoration_writer.close(),
    }
    source_paths = [
        Path(__file__).resolve(),
        HERE / "verify_parameter_transport_certificate.py",
        HERE / "run_parameter_transport_mutations.py",
        PROBE_AUDIT,
        PROBE_CONTRACT,
        PROBE_RECONSTRUCTOR,
        ATLAS_PATH,
        CYCLE_COMMON,
        CYCLE_GENERATOR,
        PROBE_PACKAGE / "exact_transport_ledger.jsonl.gz",
        PROBE_PACKAGE / "parent_restriction_ledger.jsonl.gz",
        PROBE_PACKAGE / "one_port_ledger.jsonl.gz",
        PROBE_PACKAGE / "two_port_parent_inventory.jsonl.gz",
        PROBE_PACKAGE / "two_port_ledger.jsonl.gz",
        RESTORATION_GENERATOR,
        RESTORATION_CERTIFICATE,
    ]
    certificate = {
        "schema": "k2p_graph_derived_parameter_transport_certificate_v1",
        "status": "PASS",
        "scope": (
            "all 67,741 probe equality/reverse graph transports, every concrete probe "
            "parent restriction occurrence binding all 4,379 frozen restriction records, "
            "and every first/second restoration restriction"
        ),
        "commands": {
            "producer": ".venv/bin/python -B work/canonicalizer_completeness/inheritance_transport/build_parameter_transport_certificate.py",
            "structural_replay": ".venv/bin/python -B work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py --structural-only",
            "full_replay": ".venv/bin/python -B work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py",
            "mutations": ".venv/bin/python -B work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py --output /tmp/k2p-parameter-transport-mutations.json",
        },
        "parameter_convention": {
            "reticulation_order": "increasing repr(node)",
            "parent_order": "increasing repr(parent)",
            "inheritance_parameter": "lambda is the probability of parent index 1; parent index 0 has probability 1-lambda",
            "K2P_character_order": ["0", "C", "G", "T"],
            "K2P_edge_pair": ["s for C/T", "g for G"],
            "root_suppression": "the two rooted root arcs are paired serial factors of the one suppressed mixed edge",
            "ordinary_triangle": "the common reticulation and triangle edges use the rank-nine local section, never an affine parent flip",
        },
        "inputs": {
            path.relative_to(PROJECT).as_posix(): {
                "sha256": sha_file(path), "bytes": path.stat().st_size
            }
            for path in source_paths
        },
        "ledgers": ledgers,
        "closure": {
            "all_exact_transport_records_used": len(used_transports),
            "all_frozen_parent_restriction_records_used": len(used_restrictions),
            "restoration_canonical_parents": canonical_parent_count,
            "restoration_member_roots": len(roots),
            "restoration_first_source_classes": len(first_source_seen),
            "restoration_first_target_classes": len(first_target_seen),
            "restoration_second_edges": second_ordinal,
            "unresolved_parameter_transports": 0,
        },
    }
    certificate["payload_sha256"] = sha(certificate)
    (output_dir / CERTIFICATE).write_bytes(canonical_bytes(certificate) + b"\n")
    return certificate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    certificate = build(args.output_dir.resolve())
    print(
        "PARAMETER_TRANSPORT_BUILD_PASS "
        + json.dumps({
            "payload_sha256": certificate["payload_sha256"],
            "relation_rows": certificate["ledgers"]["probe_relations"]["rows"],
            "probe_restriction_rows": certificate["ledgers"]["probe_restrictions"]["rows"],
            "restoration_rows": certificate["ledgers"]["restoration_restrictions"]["rows"],
        }, sort_keys=True)
    )


if __name__ == "__main__":
    main()
