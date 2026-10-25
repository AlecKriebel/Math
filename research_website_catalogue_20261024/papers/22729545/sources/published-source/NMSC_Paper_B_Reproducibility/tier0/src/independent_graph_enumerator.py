#!/usr/bin/env python3
"""Independent exact cycle/theta orientation and strong-repair enumerator."""
from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import combinations, permutations, product
import json
from pathlib import Path
from typing import Iterable

import networkx as nx

from record_schema import make_record, write_jsonl


def theta_multigraph(lengths: tuple[int, int, int]) -> nx.MultiGraph:
    """Three explicit edge-disjoint u-v paths with stable path-edge IDs."""
    graph = nx.MultiGraph()
    graph.add_nodes_from(("u", "v"))
    for path_index, length in enumerate(lengths):
        previous = "u"
        for edge_index in range(length):
            final = edge_index == length - 1
            current = "v" if final else f"p{path_index}_{edge_index + 1}"
            edge_id = f"p{path_index}:e{edge_index}"
            graph.add_edge(
                previous,
                current,
                key=edge_id,
                edge_id=edge_id,
                path=path_index,
                position=edge_index,
            )
            previous = current
    return graph


def oriented_graph(
    graph: nx.MultiGraph,
    bits: tuple[int, ...],
) -> nx.MultiDiGraph:
    edges = sorted(
        graph.edges(keys=True, data=True),
        key=lambda edge: edge[3]["edge_id"],
    )
    directed = nx.MultiDiGraph()
    directed.add_nodes_from(graph.nodes())
    for (left, right, key, data), bit in zip(edges, bits):
        tail, head = (left, right) if bit == 0 else (right, left)
        directed.add_edge(tail, head, key=key, **data)
    return directed


def assign_roles_if_valid(graph: nx.MultiDiGraph) -> bool:
    if not nx.is_directed_acyclic_graph(graph):
        return False
    sources = [node for node in graph if graph.in_degree(node) == 0]
    if len(sources) != 1:
        return False
    source = sources[0]
    if graph.out_degree(source) != 2:
        return False
    if any(not nx.has_path(graph, source, node) for node in graph):
        return False
    reticulations = [node for node in graph if graph.in_degree(node) == 2]
    if len(reticulations) != 2:
        return False
    for node in graph:
        indegree, outdegree = graph.in_degree(node), graph.out_degree(node)
        if node == source:
            role = "source"
            valid = indegree == 0 and outdegree == 2
        elif node in reticulations:
            role = "retic"
            valid = indegree == 2 and outdegree in (0, 1)
        else:
            role = "tree"
            valid = indegree == 1 and outdegree in (1, 2)
        if not valid:
            return False
        graph.nodes[node]["role"] = role
    return True


def suppress_ordinary_degree_two(graph: nx.MultiDiGraph) -> nx.MultiDiGraph:
    reduced = graph.copy()
    while True:
        candidates = sorted(
            node
            for node, data in reduced.nodes(data=True)
            if data.get("role") == "tree"
            and reduced.in_degree(node) == 1
            and reduced.out_degree(node) == 1
        )
        if not candidates:
            return reduced
        node = candidates[0]
        incoming = next(iter(reduced.in_edges(node, keys=True, data=True)))
        outgoing = next(iter(reduced.out_edges(node, keys=True, data=True)))
        tail, _, in_key, in_data = incoming
        _, head, out_key, out_data = outgoing
        primitive = tuple(in_data.get("primitive_edge_ids", (in_key,))) + tuple(
            out_data.get("primitive_edge_ids", (out_key,))
        )
        reduced.remove_node(node)
        key = "+".join(map(str, primitive))
        reduced.add_edge(
            tail,
            head,
            key=key,
            edge_id=key,
            primitive_edge_ids=primitive,
        )


def _canonical_orders(graph: nx.MultiDiGraph) -> Iterable[tuple[str, ...]]:
    by_role: dict[str, list[str]] = defaultdict(list)
    for node, data in graph.nodes(data=True):
        by_role[str(data.get("role"))].append(node)
    roles = sorted(by_role)
    blocks = [list(permutations(sorted(by_role[role], key=str))) for role in roles]
    for choice in product(*blocks):
        yield tuple(node for block in choice for node in block)


def canonical_code(graph: nx.MultiDiGraph) -> str:
    """Exact role-preserving canonical code, including edge multiplicities."""
    best = None
    for order in _canonical_orders(graph):
        roles = tuple(str(graph.nodes[node].get("role")) for node in order)
        adjacency = tuple(
            graph.number_of_edges(tail, head)
            for tail in order
            for head in order
        )
        candidate = (roles, adjacency)
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise ValueError("cannot canonicalize an empty graph")
    return json.dumps(best, separators=(",", ":"))


def canonical_relabel(graph: nx.MultiDiGraph) -> nx.MultiDiGraph:
    best = None
    best_order = None
    for order in _canonical_orders(graph):
        roles = tuple(str(graph.nodes[node].get("role")) for node in order)
        adjacency = tuple(
            graph.number_of_edges(tail, head)
            for tail in order
            for head in order
        )
        candidate = (roles, adjacency)
        if best is None or candidate < best:
            best, best_order = candidate, order
    if best_order is None:
        raise ValueError("cannot canonicalize an empty graph")
    mapping = {node: f"v{index}" for index, node in enumerate(best_order)}
    relabelled = nx.MultiDiGraph()
    for node in best_order:
        relabelled.add_node(mapping[node], role=graph.nodes[node]["role"])
    raw_edges = sorted(
        graph.edges(keys=True, data=True),
        key=lambda edge: (mapping[edge[0]], mapping[edge[1]], str(edge[2])),
    )
    for index, (tail, head, _, data) in enumerate(raw_edges):
        edge_id = f"e{index}"
        relabelled.add_edge(
            mapping[tail],
            mapping[head],
            key=edge_id,
            edge_id=edge_id,
            primitive_edge_ids=tuple(data.get("primitive_edge_ids", (data.get("edge_id"),))),
        )
    return relabelled


def role_isomorphic(left: nx.MultiDiGraph, right: nx.MultiDiGraph) -> bool:
    matcher = nx.algorithms.isomorphism.MultiDiGraphMatcher(
        left,
        right,
        node_match=nx.algorithms.isomorphism.categorical_node_match("role", None),
    )
    return matcher.is_isomorphic()


def graph_payload(graph: nx.MultiDiGraph) -> dict:
    return {
        "nodes": [
            {"id": str(node), "role": graph.nodes[node].get("role")}
            for node in sorted(graph, key=str)
        ],
        "edges": [
            {
                "id": str(data.get("edge_id", key)),
                "tail": str(tail),
                "head": str(head),
            }
            for tail, head, key, data in sorted(
                graph.edges(keys=True, data=True),
                key=lambda edge: str(edge[3].get("edge_id", edge[2])),
            )
        ],
    }


def graph_from_payload(payload: dict) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for node in payload["nodes"]:
        graph.add_node(node["id"], role=node["role"])
    for edge in payload["edges"]:
        graph.add_edge(
            edge["tail"],
            edge["head"],
            key=edge["id"],
            edge_id=edge["id"],
        )
    return graph


def cycle_core() -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    graph.add_node("v0", role="source")
    graph.add_node("v1", role="retic")
    graph.add_edge("v0", "v1", key="e0", edge_id="e0")
    graph.add_edge("v0", "v1", key="e1", edge_id="e1")
    return graph


def build_port_repair(
    core: nx.MultiDiGraph,
    repair: tuple[str, ...],
) -> nx.MultiDiGraph:
    repaired = nx.MultiDiGraph()
    repaired.add_nodes_from((node, dict(data)) for node, data in core.nodes(data=True))
    repair_set = set(repair)
    for tail, head, key, data in core.edges(keys=True, data=True):
        edge_id = str(data.get("edge_id", key))
        if edge_id not in repair_set:
            repaired.add_edge(tail, head, key=edge_id, edge_id=edge_id)
            continue
        port = f"port:{edge_id}"
        leaf = f"port-leaf:{edge_id}"
        repaired.add_node(port, role="tree")
        repaired.add_node(leaf, role="port_leaf")
        repaired.add_edge(tail, port, key=f"{edge_id}:a", edge_id=f"{edge_id}:a")
        repaired.add_edge(port, head, key=f"{edge_id}:b", edge_id=f"{edge_id}:b")
        repaired.add_edge(port, leaf, key=f"{edge_id}:leaf", edge_id=f"{edge_id}:leaf")
    for node, data in list(core.nodes(data=True)):
        if data.get("role") == "retic" and core.out_degree(node) == 0:
            leaf = f"sink-leaf:{node}"
            repaired.add_node(leaf, role="sink_leaf")
            repaired.add_edge(node, leaf, key=f"{node}:child", edge_id=f"{node}:child")
    return repaired


def rooted_tree_child(graph: nx.MultiDiGraph) -> bool:
    for node, data in graph.nodes(data=True):
        role = data.get("role")
        if role in {"port_leaf", "sink_leaf"}:
            if (graph.in_degree(node), graph.out_degree(node)) != (1, 0):
                return False
            continue
        if role not in {"source", "tree", "retic"}:
            return False
        children = [head for _, head, _ in graph.out_edges(node, keys=True)]
        if not children:
            return False
        if not any(graph.nodes[child].get("role") not in {"retic"} for child in children):
            return False
        if role == "source" and (graph.in_degree(node), graph.out_degree(node)) != (0, 2):
            return False
        if role == "tree" and (graph.in_degree(node), graph.out_degree(node)) != (1, 2):
            return False
        if role == "retic" and (graph.in_degree(node), graph.out_degree(node)) != (2, 1):
            return False
    return True


def strong_tail(graph: nx.MultiDiGraph) -> bool:
    for retic, data in graph.nodes(data=True):
        if data.get("role") != "retic":
            continue
        for tail in set(graph.predecessors(retic)):
            ordinary = graph.in_degree(tail)
            ordinary += sum(
                1
                for _, head, _ in graph.out_edges(tail, keys=True)
                if graph.nodes[head].get("role") != "retic"
            )
            if graph.nodes[tail].get("role") == "source":
                ordinary += 1
            if ordinary < 2:
                return False
    return True


def enumerate_minimal_repairs(core: nx.MultiDiGraph) -> tuple[tuple[str, ...], ...]:
    edge_ids = tuple(
        sorted(str(data.get("edge_id", key)) for _, _, key, data in core.edges(keys=True, data=True))
    )
    minimal: list[tuple[str, ...]] = []
    for size in range(len(edge_ids) + 1):
        for repair in combinations(edge_ids, size):
            graph = build_port_repair(core, repair)
            if not (rooted_tree_child(graph) and strong_tail(graph)):
                continue
            if any(set(old).issubset(repair) for old in minimal):
                continue
            minimal.append(repair)
    return tuple(minimal)


def enumerate_theta_orbits(max_path: int) -> tuple[dict[str, nx.MultiDiGraph], dict[str, list[dict]]]:
    representatives: dict[str, nx.MultiDiGraph] = {}
    sources: dict[str, list[dict]] = defaultdict(list)
    for lengths in product(range(1, max_path + 1), repeat=3):
        primitive = theta_multigraph(lengths)
        edge_count = primitive.number_of_edges()
        edge_ids = [
            str(data["edge_id"])
            for _, _, _, data in sorted(
                primitive.edges(keys=True, data=True),
                key=lambda edge: edge[3]["edge_id"],
            )
        ]
        for bits in product((0, 1), repeat=edge_count):
            directed = oriented_graph(primitive, bits)
            if not assign_roles_if_valid(directed):
                continue
            reduced = suppress_ordinary_degree_two(directed)
            code = canonical_code(reduced)
            if code not in representatives:
                representatives[code] = canonical_relabel(reduced)
            elif not role_isomorphic(representatives[code], reduced):
                raise AssertionError("canonical-code collision between nonisomorphic multidigraphs")
            sources[code].append(
                {
                    "lengths": list(lengths),
                    "edge_ids": edge_ids,
                    "orientation_bits": list(bits),
                }
            )
    representative_list = list(representatives.values())
    for left, right in combinations(representative_list, 2):
        if role_isomorphic(left, right):
            raise AssertionError("two canonical codes represent the same role-preserving orbit")
    return representatives, sources


def enumerate_records(max_path: int) -> list[dict]:
    theta_representatives, theta_sources = enumerate_theta_orbits(max_path)
    if len(theta_representatives) != 4:
        raise AssertionError(
            f"expected four theta core orbits through path length {max_path}, "
            f"found {len(theta_representatives)}"
        )
    core_entries = [
        (
            "cycle",
            cycle_core(),
            [{"lengths": [1, 1], "edge_ids": ["e0", "e1"], "orientation_bits": [0, 0]}],
        )
    ]
    core_entries.extend(
        ("theta", theta_representatives[code], theta_sources[code])
        for code in sorted(theta_representatives)
    )
    records = []
    total_raw_repairs = 0
    for family, core, primitive_sources in core_entries:
        repairs = enumerate_minimal_repairs(core)
        repair_payloads = []
        orbit_codes = set()
        for repair in repairs:
            expanded = build_port_repair(core, repair)
            if not rooted_tree_child(expanded):
                raise AssertionError("enumerated repair lost rooted tree-childness")
            if not strong_tail(expanded):
                raise AssertionError("enumerated repair lost the strong-tail property")
            expansion_code = canonical_code(expanded)
            orbit_codes.add(expansion_code)
            repair_payloads.append(
                {
                    "edge_ids": list(repair),
                    "expansion_code": expansion_code,
                    "graph": graph_payload(expanded),
                }
            )
        total_raw_repairs += len(repairs)
        core_code = canonical_code(core)
        case_input = {
            "family": family,
            "core_code": core_code,
            "max_path": max_path,
            "primitive_source_count": len(primitive_sources),
        }
        records.append(
            make_record(
                job="independent_graph_enumerator",
                case_input=case_input,
                status="PASS",
                graph=graph_payload(core),
                exact_witness={
                    "core_code": core_code,
                    "primitive_source_count": len(primitive_sources),
                    "primitive_sources": primitive_sources,
                    "raw_minimal_repair_count": len(repairs),
                    "repair_orbit_count": len(orbit_codes),
                    "repairs": repair_payloads,
                    "rooted_tree_child_and_strong_tail": all(
                        rooted_tree_child(build_port_repair(core, repair))
                        and strong_tail(build_port_repair(core, repair))
                        for repair in repairs
                    ),
                },
                declared_quotient_orbit={"family": family, "core_code": core_code},
                notes="Derived from explicit path-edge orientations and both graph-domain predicates.",
                extra={"family": family, "core_code": core_code},
            )
        )
    if sum(record["family"] == "cycle" for record in records) != 1:
        raise AssertionError("expected one cycle core orbit")
    if sum(record["family"] == "theta" for record in records) != 4:
        raise AssertionError("expected four theta core orbits")
    if len(records) != 5:
        raise AssertionError(f"expected five total core orbits, found {len(records)}")
    if total_raw_repairs != 12:
        raise AssertionError(f"expected 12 raw minimum repairs, found {total_raw_repairs}")
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-path", type=int, default=3)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.max_path != 3:
        raise SystemExit("this bounded verifier requires max-path exactly 3")
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    records = enumerate_records(args.max_path)
    write_jsonl(output, records)
    raw_repairs = sum(
        record["exact_witness"]["raw_minimal_repair_count"] for record in records
    )
    orbit_repairs = sum(
        record["exact_witness"]["repair_orbit_count"] for record in records
    )
    print(
        "INDEPENDENT_ENUMERATOR_OK "
        f"core_orbits={len(records)} raw_repairs={raw_repairs} "
        f"repair_orbits={orbit_repairs}"
    )


if __name__ == "__main__":
    main()
