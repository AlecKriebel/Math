#!/usr/bin/env python3
"""Exact Kingman-germ separator and old rank-one false-positive fixture."""
from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path

import networkx as nx
import sympy as sp

from record_schema import make_record, write_json_record


def fixture() -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for node, role, time in (
        ("root", "root", Fraction(5)),
        ("S", "tree", Fraction(4)),
        ("p", "tree", Fraction(3)),
        ("h", "retic", Fraction(1)),
        ("A", "leaf", Fraction(0)),
        ("z", "leaf", Fraction(0)),
        ("w", "leaf", Fraction(0)),
    ):
        graph.add_node(node, role=role, time=time)
    for index, (tail, head) in enumerate(
        (
            ("root", "S"),
            ("root", "w"),
            ("S", "p"),
            ("S", "h"),
            ("p", "h"),
            ("p", "z"),
            ("h", "A"),
        )
    ):
        graph.add_edge(tail, head, key=f"a{index}", edge_id=f"a{index}")
    return graph


def rooted_binary_and_temporal(graph: nx.MultiDiGraph) -> bool:
    for node, data in graph.nodes(data=True):
        role = data["role"]
        degree = (graph.in_degree(node), graph.out_degree(node))
        expected = {
            "root": (0, 2),
            "tree": (1, 2),
            "retic": (2, 1),
            "leaf": (1, 0),
        }[role]
        if degree != expected:
            return False
    return all(
        graph.nodes[tail]["time"] > graph.nodes[head]["time"]
        for tail, head, _ in graph.edges(keys=True)
    )


def tree_child(graph: nx.MultiDiGraph) -> bool:
    for node, data in graph.nodes(data=True):
        if data["role"] == "leaf":
            continue
        children = [head for _, head, _ in graph.out_edges(node, keys=True)]
        if not any(graph.nodes[head]["role"] in {"tree", "leaf"} for head in children):
            return False
    return True


def strong_tail(graph: nx.MultiDiGraph) -> bool:
    for reticulation, data in graph.nodes(data=True):
        if data["role"] != "retic":
            continue
        for parent in set(graph.predecessors(reticulation)):
            ordinary = graph.in_degree(parent) + sum(
                1
                for _, head, _ in graph.out_edges(parent, keys=True)
                if graph.nodes[head]["role"] != "retic"
            )
            if ordinary < 2:
                return False
    return True


def graph_input(graph: nx.MultiDiGraph) -> dict:
    return {
        "nodes": [
            {
                "id": node,
                "role": data["role"],
                "time": [data["time"].numerator, data["time"].denominator],
            }
            for node, data in sorted(graph.nodes(data=True))
        ],
        "edges": [
            {"id": key, "tail": tail, "head": head}
            for tail, head, key in sorted(graph.edges(keys=True))
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    u, v, lam, energy = sp.symbols("u v lambda E", positive=True)
    kingman = sp.exp(-lam * u)
    kingman_defect = sp.simplify(
        kingman.subs(u, u + v) - kingman * kingman.subs(u, v)
    )
    kingman_curvature = sp.simplify(
        kingman * sp.diff(kingman, u, 2) - sp.diff(kingman, u) ** 2
    )

    routed = sp.Rational(1, 2) + sp.Rational(1, 2) * sp.exp(-lam * u)
    routed_defect = sp.factor(
        routed.subs(u, u + v) - routed * routed.subs(u, v)
    )
    expected_defect = sp.Rational(1, 4) * (
        1 - sp.exp(-lam * u)
    ) * (1 - sp.exp(-lam * v))
    routed_curvature = sp.factor(
        routed * sp.diff(routed, u, 2) - sp.diff(routed, u) ** 2
    )
    expected_curvature = sp.Rational(1, 4) * lam**2 * sp.exp(-lam * u)
    routed_germ = sp.simplify(sp.diff(routed_defect, v).subs(v, 0))
    expected_germ = sp.Rational(1, 4) * lam * (1 - sp.exp(-lam * u))

    one_block = sp.Matrix(
        [
            [sp.Rational(1, 2), sp.Rational(1, 2)],
            [energy / 4, energy / 4],
        ]
    )
    two_block = sp.Matrix([[energy / 4, sp.Rational(1, 4), sp.Rational(1, 4), energy / 4]])

    gamma, distance, delta, u1, u2 = sp.symbols(
        "gamma D delta u1 u2", positive=True
    )
    a = lambda x: gamma * (1 - gamma) * lam * sp.exp(-lam * x)
    c = lambda x: gamma**2 * lam * sp.exp(-lam * distance - 2 * lam * x)
    e_delta = sp.exp(-lam * delta)
    fixed_cut = sp.Matrix(
        [
            [c(x) * (1 - e_delta), a(x) + c(x) * e_delta]
            for x in (u1, u2)
        ]
    )
    fixed_cut_det = sp.factor(fixed_cut.det())

    graph = fixture()
    simple = nx.Graph(graph)
    graph_bridges = {frozenset(edge) for edge in nx.bridges(simple)}
    retic_arm_is_bridge = frozenset(("p", "h")) in graph_bridges
    checks = {
        "kingman_semigroup": kingman_defect == 0,
        "kingman_constant_log_hazard": kingman_curvature == 0,
        "routing_defect_formula": sp.simplify(routed_defect - expected_defect) == 0,
        "routing_curvature_formula": sp.simplify(routed_curvature - expected_curvature) == 0,
        "routing_local_germ_formula": sp.simplify(routed_germ - expected_germ) == 0,
        "routing_germ_nonzero": routed_germ != 0,
        "old_one_block_rank_one": one_block.rank() == 1,
        "old_two_block_rank_one": two_block.rank() == 1,
        "fixture_rooted_binary_temporal": rooted_binary_and_temporal(graph),
        "fixture_tree_child": tree_child(graph),
        "fixture_strong_tail": strong_tail(graph),
        "strict_port_precedes_reticulation": graph.nodes["p"]["time"] > graph.nodes["h"]["time"],
        "retic_arm_is_not_graph_bridge": not retic_arm_is_bridge,
        "fixed_cut_actual_minor_nonzero": fixed_cut_det != 0,
    }
    status = "PASS" if all(checks.values()) else "BLOCKING"
    witness = {
        "checks": checks,
        "kingman_germ": {
            "survival": str(kingman),
            "semigroup_defect": str(kingman_defect),
            "log_hazard_numerator": str(kingman_curvature),
        },
        "equal_arm_routing_germ": {
            "survival": str(routed),
            "semigroup_defect": str(routed_defect),
            "expected_semigroup_defect": str(sp.factor(expected_defect)),
            "local_v_derivative_at_zero": str(routed_germ),
            "log_hazard_numerator": str(routed_curvature),
        },
        "rank_one_false_positive": {
            "gamma": "1/2",
            "one_block_rows": str(one_block),
            "one_block_rank": one_block.rank(),
            "two_block_rows": str(two_block),
            "two_block_rank": two_block.rank(),
            "retic_arm": ["p", "h"],
            "retic_arm_is_graph_bridge": retic_arm_is_bridge,
        },
        "actual_fixed_cut_minor": str(fixed_cut_det),
    }
    record = make_record(
        job="one_port_separator",
        case_input={
            "fixture": graph_input(graph),
            "gamma": "1/2",
            "symbol_assumptions": "u,v,lambda,E,D,delta,u1,u2 positive",
        },
        status=status,
        graph=graph_input(graph),
        exact_witness=witness,
        declared_quotient_orbit={"fixture": "strict-STC repaired-cycle nonbridge"},
        notes=(
            "Rank one alone is an exact false positive on this valid nonbridge; "
            "the local Kingman semigroup/log-hazard germ separates it."
        ),
    )
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_json_record(output, record)
    if status != "PASS":
        print("ONE_PORT_SEPARATOR_BLOCKING")
        raise SystemExit(1)
    print("ONE_PORT_SEPARATOR_OK kingman_germ=PASS rank_one_false_positive=PASS")


if __name__ == "__main__":
    main()
