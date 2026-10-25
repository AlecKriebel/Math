#!/usr/bin/env python3
"""Derive lowest-reticulation anchor certificates from enumerated repairs."""
from __future__ import annotations

import argparse
from pathlib import Path

import networkx as nx

from independent_graph_enumerator import graph_from_payload, graph_payload
from record_schema import load_records, make_record, validate_record, write_jsonl


LEAF_ROLES = {"port_leaf", "sink_leaf"}


def lowest_reticulations(graph: nx.MultiDiGraph) -> list[str]:
    reticulations = sorted(
        node
        for node, data in graph.nodes(data=True)
        if data.get("role") == "retic"
    )
    return [
        node
        for node in reticulations
        if not any(
            node != other and nx.has_path(graph, node, other)
            for other in reticulations
        )
    ]


def parent_relation(
    graph: nx.MultiDiGraph,
    left: str,
    right: str,
    deleted: str,
) -> str:
    residual = graph.copy()
    residual.remove_node(deleted)
    if nx.has_path(residual, left, right):
        return "left-ancestor-right"
    if nx.has_path(residual, right, left):
        return "right-ancestor-left"
    return "incomparable"


def _edge_ids(edges: list[tuple[str, str, str, dict]]) -> list[str]:
    return sorted(str(data.get("edge_id", key)) for _, _, key, data in edges)


def parent_anchor(
    graph: nx.MultiDiGraph,
    parent: str,
    reticulation: str,
) -> dict:
    """Return graph-visible ordinary incidences anchoring one parent tail."""
    incoming = _edge_ids(list(graph.in_edges(parent, keys=True, data=True)))
    outgoing_ordinary = [
        (tail, head, key, data)
        for tail, head, key, data in graph.out_edges(parent, keys=True, data=True)
        if head != reticulation and graph.nodes[head].get("role") != "retic"
    ]
    ordinary_ids = _edge_ids(outgoing_ordinary)
    leaf_paths = []
    residual = graph.copy()
    residual.remove_node(reticulation)
    for leaf, data in sorted(residual.nodes(data=True), key=lambda item: str(item[0])):
        if data.get("role") not in LEAF_ROLES:
            continue
        if parent in residual and nx.has_path(residual, parent, leaf):
            leaf_paths.append(nx.shortest_path(residual, parent, leaf))
    boundary = "source-boundary" if graph.nodes[parent].get("role") == "source" else None
    witness_count = len(incoming) + len(ordinary_ids) + (boundary is not None)
    return {
        "parent": parent,
        "parent_role": graph.nodes[parent].get("role"),
        "incoming_anchor_edges": incoming,
        "ordinary_exit_edges": ordinary_ids,
        "sample_leaf_paths_after_deletion": leaf_paths,
        "boundary_anchor": boundary,
        "incidence_witness_count": witness_count,
    }


def derive_anchor_records(core_records: list[dict]) -> list[dict]:
    output = []
    for core_record in core_records:
        validate_record(core_record, "independent_graph_enumerator")
        core_code = core_record["exact_witness"]["core_code"]
        for repair in core_record["exact_witness"]["repairs"]:
            graph = graph_from_payload(repair["graph"])
            for lowest in lowest_reticulations(graph):
                parents = sorted(set(graph.predecessors(lowest)), key=str)
                children = sorted(set(graph.successors(lowest)), key=str)
                anchors = [parent_anchor(graph, parent, lowest) for parent in parents]
                failures = []
                if len(parents) != 2:
                    failures.append(f"expected two distinct parents, found {len(parents)}")
                if len(children) != 1 or graph.nodes[children[0]].get("role") != "sink_leaf":
                    failures.append("lowest reticulation lacks one explicit sampled child")
                if any(anchor["incidence_witness_count"] < 2 for anchor in anchors):
                    failures.append("a parent tail lacks the two ordinary incidences required by strong-tail")
                if not any(anchor["sample_leaf_paths_after_deletion"] for anchor in anchors):
                    failures.append("no sampled side anchor survives deletion")
                status = "BLOCKING" if failures else "PASS"
                case_input = {
                    "core_code": core_code,
                    "repair_edge_ids": repair["edge_ids"],
                    "expansion_code": repair["expansion_code"],
                    "lowest_reticulation": lowest,
                }
                relation = (
                    parent_relation(graph, parents[0], parents[1], lowest)
                    if len(parents) == 2
                    else "undefined"
                )
                output.append(
                    make_record(
                        job="anchor_verifier",
                        case_input=case_input,
                        status=status,
                        graph=graph_payload(graph),
                        exact_witness={
                            "core_code": core_code,
                            "repair_edge_ids": repair["edge_ids"],
                            "expansion_code": repair["expansion_code"],
                            "lowest_reticulation": lowest,
                            "parents": parents,
                            "parent_relation_after_deletion": relation,
                            "sampled_children": children,
                            "parent_anchors": anchors,
                            "failures": failures,
                        },
                        declared_quotient_orbit={
                            "core_code": core_code,
                            "expansion_code": repair["expansion_code"],
                        },
                        notes=(
                            "Anchor incidences and sampled paths were recomputed from the "
                            "independently enumerated repaired multigraph."
                        ),
                    )
                )
    if not output:
        raise ValueError("no anchor records were derived")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cores", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    records = derive_anchor_records(load_records(args.cores))
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(output, records)
    blocking = [record for record in records if record["status"] != "PASS"]
    if blocking:
        print(f"ANCHOR_VERIFIER_BLOCKING count={len(blocking)}")
        raise SystemExit(1)
    print(f"ANCHOR_VERIFIER_OK records={len(records)} nonempty_anchors={len(records)}")


if __name__ == "__main__":
    main()
