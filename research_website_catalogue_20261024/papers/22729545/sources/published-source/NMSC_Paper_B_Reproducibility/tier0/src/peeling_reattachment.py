#!/usr/bin/env python3
"""Delete and exactly reattach lowest reticulations using graph-derived tags."""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import networkx as nx

from anchor_verifier import lowest_reticulations
from independent_graph_enumerator import (
    canonical_code,
    graph_from_payload,
    graph_payload,
)
from record_schema import load_records, make_record, validate_record, write_jsonl


def _relation(graph: nx.MultiDiGraph, parents: list[str], deleted: str) -> str:
    residual = graph.copy()
    residual.remove_node(deleted)
    if len(parents) != 2:
        return "undefined"
    if nx.has_path(residual, parents[0], parents[1]) or nx.has_path(
        residual, parents[1], parents[0]
    ):
        return "comparable"
    return "incomparable"


def tagged_deletion(
    graph: nx.MultiDiGraph,
    reticulation: str,
) -> tuple[nx.MultiDiGraph, dict]:
    parents = sorted(set(graph.predecessors(reticulation)), key=str)
    children = sorted(set(graph.successors(reticulation)), key=str)
    if len(parents) != 2:
        raise ValueError("tagged deletion requires two distinct parents")
    if len(children) != 1 or graph.nodes[children[0]].get("role") != "sink_leaf":
        raise ValueError("tagged deletion requires one sampled sink child")

    residual = graph.copy()
    child = children[0]
    residual.nodes[child]["role"] = "selected_child"
    for index, parent in enumerate(parents):
        old_role = str(residual.nodes[parent].get("role"))
        residual.nodes[parent]["role"] = f"{old_role}|selected_parent"
        marker = f"reattach-parent-marker:{reticulation}:{index}"
        edge_id = f"reattach-parent-marker-edge:{reticulation}:{index}"
        residual.add_node(marker, role="parent_marker")
        residual.add_edge(parent, marker, key=edge_id, edge_id=edge_id)
    residual.remove_node(reticulation)
    metadata = {
        "parents": parents,
        "selected_child": child,
        "parent_relation": _relation(graph, parents, reticulation),
    }
    return residual, metadata


def reattach_from_tags(residual: nx.MultiDiGraph) -> nx.MultiDiGraph:
    rebuilt = residual.copy()
    parents = sorted(
        node
        for node, data in rebuilt.nodes(data=True)
        if str(data.get("role")).endswith("|selected_parent")
    )
    children = [
        node
        for node, data in rebuilt.nodes(data=True)
        if data.get("role") == "selected_child"
    ]
    markers = [
        node
        for node, data in rebuilt.nodes(data=True)
        if data.get("role") == "parent_marker"
    ]
    if len(parents) != 2 or len(children) != 1 or len(markers) != 2:
        raise ValueError("tagged residual has invalid parent/child marker multiplicity")
    for marker in markers:
        rebuilt.remove_node(marker)
    for parent in parents:
        role = str(rebuilt.nodes[parent]["role"])
        rebuilt.nodes[parent]["role"] = role.removesuffix("|selected_parent")
    child = children[0]
    rebuilt.nodes[child]["role"] = "sink_leaf"
    reticulation = "reattached:selected-reticulation"
    rebuilt.add_node(reticulation, role="retic")
    for index, parent in enumerate(parents):
        edge_id = f"reattached:parent:{index}"
        rebuilt.add_edge(parent, reticulation, key=edge_id, edge_id=edge_id)
    rebuilt.add_edge(
        reticulation,
        child,
        key="reattached:child",
        edge_id="reattached:child",
    )
    return rebuilt


def derive_reattachment_records(core_records: list[dict]) -> list[dict]:
    cases = []
    for core_record in core_records:
        validate_record(core_record, "independent_graph_enumerator")
        core_code = core_record["exact_witness"]["core_code"]
        for repair in core_record["exact_witness"]["repairs"]:
            graph = graph_from_payload(repair["graph"])
            for lowest in lowest_reticulations(graph):
                residual, metadata = tagged_deletion(graph, lowest)
                residual_code = canonical_code(residual)
                rebuilt = reattach_from_tags(residual)
                rebuilt_code = canonical_code(rebuilt)
                cases.append(
                    {
                        "core_code": core_code,
                        "repair": repair,
                        "graph": graph,
                        "lowest": lowest,
                        "residual": residual,
                        "residual_code": residual_code,
                        "rebuilt_code": rebuilt_code,
                        "metadata": metadata,
                    }
                )

    if not cases:
        raise ValueError("no lowest-reticulation reattachment cases were derived")
    collision_targets: dict[tuple[str, str], set[str]] = defaultdict(set)
    for case in cases:
        key = (case["residual_code"], case["metadata"]["parent_relation"])
        collision_targets[key].add(case["repair"]["expansion_code"])

    records = []
    for case in cases:
        key = (case["residual_code"], case["metadata"]["parent_relation"])
        target_codes = sorted(collision_targets[key])
        failures = []
        if case["rebuilt_code"] != case["repair"]["expansion_code"]:
            failures.append("tagged residual did not reconstruct the input expansion orbit")
        if len(target_codes) != 1:
            failures.append("one tagged residual signature reconstructs multiple expansion orbits")
        status = "BLOCKING" if failures else "PASS"
        case_input = {
            "core_code": case["core_code"],
            "repair_edge_ids": case["repair"]["edge_ids"],
            "expansion_code": case["repair"]["expansion_code"],
            "lowest_reticulation": case["lowest"],
        }
        records.append(
            make_record(
                job="peeling_reattachment",
                case_input=case_input,
                status=status,
                graph=graph_payload(case["graph"]),
                exact_witness={
                    "core_code": case["core_code"],
                    "repair_edge_ids": case["repair"]["edge_ids"],
                    "expansion_code": case["repair"]["expansion_code"],
                    "lowest_reticulation": case["lowest"],
                    "parents": case["metadata"]["parents"],
                    "selected_child": case["metadata"]["selected_child"],
                    "parent_relation": case["metadata"]["parent_relation"],
                    "tagged_residual_code": case["residual_code"],
                    "tagged_residual_graph": graph_payload(case["residual"]),
                    "reconstructed_expansion_code": case["rebuilt_code"],
                    "signature_target_codes": target_codes,
                    "failures": failures,
                },
                declared_quotient_orbit={
                    "core_code": case["core_code"],
                    "expansion_code": case["repair"]["expansion_code"],
                },
                notes=(
                    "The residual, parent tags, child tag, and reconstruction were "
                    "derived from the enumerated primitive repair, not the proof catalog."
                ),
            )
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cores", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    records = derive_reattachment_records(load_records(args.cores))
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(output, records)
    blocking = [record for record in records if record["status"] != "PASS"]
    if blocking:
        print(f"PEELING_REATTACHMENT_BLOCKING count={len(blocking)}")
        raise SystemExit(1)
    print(f"PEELING_REATTACHMENT_OK records={len(records)} derived_signatures={len(records)}")


if __name__ == "__main__":
    main()
