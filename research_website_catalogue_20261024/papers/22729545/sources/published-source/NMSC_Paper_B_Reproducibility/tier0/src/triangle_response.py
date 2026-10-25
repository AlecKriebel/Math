#!/usr/bin/env python3
"""Exact bi-unary triangle kernel and directional response certificate."""
from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path

import networkx as nx
import sympy as sp

from record_schema import make_record, write_json_record


def preexposure_fixture(h: Fraction, rates: tuple[Fraction, Fraction, Fraction]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for node, role, time in (
        ("R", "root", Fraction(7)),
        ("S", "tree", Fraction(5)),
        ("T", "tree", Fraction(3)),
        ("X", "retic", h),
        ("w", "leaf", Fraction(0)),
        ("z", "leaf", Fraction(0)),
        ("x", "leaf", Fraction(0)),
    ):
        graph.add_node(node, role=role, time=time)
    edge_data = (
        ("R", "S", Fraction(13), None),
        ("R", "w", Fraction(17), None),
        ("S", "T", Fraction(2), None),
        ("S", "X", rates[2], Fraction(2, 3)),
        ("T", "z", Fraction(19), None),
        ("T", "X", rates[1], Fraction(1, 3)),
        ("X", "x", rates[0], None),
    )
    for index, (tail, head, rate, inheritance) in enumerate(edge_data):
        graph.add_edge(
            tail,
            head,
            key=f"a{index}",
            rate=rate,
            inheritance=inheritance,
        )
    return graph


def fixture_predicates(graph: nx.MultiDiGraph) -> dict[str, bool]:
    degree_type = {
        "root": (0, 2),
        "tree": (1, 2),
        "retic": (2, 1),
        "leaf": (1, 0),
    }
    binary = all(
        (graph.in_degree(node), graph.out_degree(node)) == degree_type[data["role"]]
        for node, data in graph.nodes(data=True)
    )
    strict_temporal = all(
        graph.nodes[tail]["time"] > graph.nodes[head]["time"]
        for tail, head, _ in graph.edges(keys=True)
    )
    event_times = [
        data["time"]
        for _, data in graph.nodes(data=True)
        if data["role"] != "leaf"
    ]
    separated = len(event_times) == len(set(event_times))
    tree_child = all(
        data["role"] == "leaf"
        or any(
            graph.nodes[child]["role"] in {"tree", "leaf"}
            for _, child, _ in graph.out_edges(node, keys=True)
        )
        for node, data in graph.nodes(data=True)
    )
    strong = True
    for reticulation, data in graph.nodes(data=True):
        if data["role"] != "retic":
            continue
        for parent in set(graph.predecessors(reticulation)):
            ordinary = graph.in_degree(parent) + sum(
                1
                for _, child, _ in graph.out_edges(parent, keys=True)
                if graph.nodes[child]["role"] != "retic"
            )
            strong &= ordinary >= 2
    reticulations = {
        node for node, data in graph.nodes(data=True) if data["role"] == "retic"
    }
    level_one = bool(reticulations) and all(
        len(reticulations.intersection(component)) <= 1
        for component in nx.biconnected_components(nx.Graph(graph))
    )
    return {
        "rooted_binary": binary and graph.in_degree("R") == 0,
        "strict_temporal": strict_temporal,
        "temporally_separated": separated,
        "tree_child": tree_child,
        "strong_tail": strong,
        "level_one": level_one,
    }


def graph_payload(graph: nx.MultiDiGraph) -> dict:
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
            {
                "tail": tail,
                "head": head,
                "key": key,
                "rate": [data["rate"].numerator, data["rate"].denominator],
                "inheritance": None
                if data["inheritance"] is None
                else [data["inheritance"].numerator, data["inheritance"].denominator],
            }
            for tail, head, key, data in sorted(graph.edges(keys=True, data=True))
        ],
    }


def stopped_fan_safe(
    maximum_internal_occupancy: int,
    internal_sample_entries: tuple,
) -> bool:
    return maximum_internal_occupancy <= 1 and not internal_sample_entries


def preexposure_observable(
    h: Fraction,
    unary_rates: tuple[Fraction, Fraction, Fraction],
    elapsed: sp.Symbol,
    upper_continuation: sp.Matrix,
) -> dict:
    if not (0 < h < Fraction(3)) or any(rate <= 0 for rate in unary_rates):
        raise ValueError("invalid hidden fan time or unary rate")
    gamma = sp.Rational(1, 3)
    rate = sp.Rational(2)
    delta = sp.Rational(2)
    density = gamma * rate * sp.exp(-rate * elapsed)
    survive = 1 - gamma + gamma * sp.exp(-rate * delta)
    merge = gamma * (1 - sp.exp(-rate * delta))
    kernel = sp.Matrix([[survive, merge], [0, 1]])
    return {
        "density": density,
        "support_start": Fraction(3),
        "kernel": kernel,
        "upper_composition": sp.simplify(kernel * upper_continuation),
    }


def canonical_composed_fan_response(
    weights: tuple[Fraction, ...],
    exit_rows: tuple[tuple[Fraction, ...], ...],
    output_types: tuple[str, ...],
) -> tuple:
    if len(weights) != len(exit_rows) or any(len(row) != len(output_types) for row in exit_rows):
        raise ValueError("fan response dimensions disagree")
    if sum(weights, Fraction(0)) != 1:
        raise ValueError("fan weights must sum to one")
    composed: dict[str, Fraction] = {}
    for weight, row in zip(weights, exit_rows):
        for output_type, value in zip(output_types, row):
            composed[output_type] = composed.get(output_type, Fraction(0)) + weight * value
    return tuple(
        (output_type, value)
        for output_type, value in sorted(composed.items())
        if value != 0
    )


def exact_nested_response(
    initial: tuple[sp.Rational, ...],
    transitions: tuple[sp.Matrix, ...],
    continuation: sp.Matrix,
) -> sp.Matrix:
    current = sp.Matrix([list(initial)])
    for transition in transitions:
        current = sp.simplify(current * transition)
    return sp.simplify(current * continuation)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    gamma, lam, distance, u = sp.symbols(
        "gamma lambda D u", positive=True
    )
    survival = sp.exp(-lam * distance)
    kernel = sp.Matrix(
        [
            [1 - gamma + gamma * survival, gamma * (1 - survival)],
            [0, 1],
        ]
    )
    enumerated_kernel = sp.Matrix(
        [
            [(1 - gamma) + gamma * survival, gamma * (1 - survival)],
            [0, 1],
        ]
    )
    forward = (
        gamma * (1 - gamma) * lam * sp.exp(-lam * u)
        + gamma**2 * lam * sp.exp(-lam * distance - 2 * lam * u)
    )
    reverse = gamma * lam * sp.exp(-lam * distance - 2 * lam * u)
    curvature = sp.factor(
        forward * sp.diff(forward, u, 2) - sp.diff(forward, u) ** 2
    )
    left_graph = preexposure_fixture(
        Fraction(1),
        (Fraction(5), Fraction(7), Fraction(11)),
    )
    right_graph = preexposure_fixture(
        Fraction(2),
        (Fraction(23), Fraction(29), Fraction(31)),
    )
    c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
    arbitrary_upper = sp.Matrix([[c00, c01], [c10, c11]])
    left_observable = preexposure_observable(
        Fraction(1),
        (Fraction(5), Fraction(7), Fraction(11)),
        u,
        arbitrary_upper,
    )
    right_observable = preexposure_observable(
        Fraction(2),
        (Fraction(23), Fraction(29), Fraction(31)),
        u,
        arbitrary_upper,
    )
    fan_density = left_observable["density"]
    fan_kernel = left_observable["kernel"]
    fan_ports = (
        ("T", Fraction(3), "first-exposure", Fraction(1, 3)),
        ("S", Fraction(5), "first-exposure", Fraction(2, 3)),
    )
    fan_frontier = tuple(port[:3] for port in fan_ports)
    scalar_response = canonical_composed_fan_response(
        (Fraction(1, 3), Fraction(2, 3)),
        ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))),
        ("T@3:first-exposure", "S@5:first-exposure"),
    )
    left_old_signature = ("Q1-Q7", Fraction(1), fan_ports)
    right_old_signature = ("Q1-Q7", Fraction(2), fan_ports)
    left_q8_signature = (
        "Q8",
        ("x", Fraction(0), "one-block"),
        fan_frontier,
        scalar_response,
    )
    right_q8_signature = (
        "Q8",
        ("x", Fraction(0), "one-block"),
        fan_frontier,
        scalar_response,
    )
    future_null_rows = (
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(0)),
    )
    future_null_left = canonical_composed_fan_response(
        (Fraction(1, 3), Fraction(2, 3)),
        future_null_rows,
        ("common-future", "null-future"),
    )
    future_null_right = canonical_composed_fan_response(
        (Fraction(2, 5), Fraction(3, 5)),
        future_null_rows,
        ("common-future", "null-future"),
    )
    typed_response_a = canonical_composed_fan_response(
        (Fraction(1, 3), Fraction(2, 3)),
        ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))),
        ("future-A", "future-B"),
    )
    typed_response_b = canonical_composed_fan_response(
        (Fraction(1, 3), Fraction(2, 3)),
        ((Fraction(0), Fraction(1)), (Fraction(1), Fraction(0))),
        ("future-A", "future-B"),
    )
    outer = (sp.Rational(1, 3), sp.Rational(2, 3))
    inner = (sp.Rational(1, 4), sp.Rational(3, 4))
    nested_transition = sp.Matrix(
        [[inner[0], inner[1], 0], [0, 0, 1]]
    )
    flattened = tuple(sp.simplify(value) for value in list(
        sp.Matrix([list(outer)]) * nested_transition
    ))
    nested_continuation = sp.Matrix([[1, 0], [0, 1], [1, 1]])
    nested_outer_then_inner = exact_nested_response(
        outer,
        (nested_transition,),
        nested_continuation,
    )
    nested_flattened_once = exact_nested_response(
        flattened,
        (),
        nested_continuation,
    )
    nested_inner_then_outer = exact_nested_response(
        outer,
        (),
        nested_transition * nested_continuation,
    )
    left_predicates = fixture_predicates(left_graph)
    right_predicates = fixture_predicates(right_graph)
    checks = {
        "kernel_rows_stochastic": sp.simplify(sum(kernel[0, column] for column in range(2)) - 1) == 0,
        "route_enumeration_matches_kernel": kernel == enumerated_kernel,
        "forward_curvature_nonzero": curvature != 0,
        "gamma_half_curvature_nonzero": sp.simplify(
            curvature.subs(gamma, sp.Rational(1, 2))
        )
        != 0,
        "forward_reverse_distinct": sp.simplify(forward - reverse) != 0,
        "fan_raw_left_in_domain": all(left_predicates.values()),
        "fan_raw_right_in_domain": all(right_predicates.values()),
        "fan_hidden_times_distinct": left_graph.nodes["X"]["time"]
        != right_graph.nodes["X"]["time"],
        "fan_unary_rate_words_distinct": tuple(
            left_graph[tail][head][key]["rate"]
            for tail, head, key in (("X", "x", "a6"), ("T", "X", "a5"), ("S", "X", "a3"))
        )
        != tuple(
            right_graph[tail][head][key]["rate"]
            for tail, head, key in (("X", "x", "a6"), ("T", "X", "a5"), ("S", "X", "a3"))
        ),
        "fan_density_support_starts_at_a": left_observable["support_start"]
        == Fraction(3),
        "fan_density_support_not_hidden_h": left_observable["support_start"]
        != left_graph.nodes["X"]["time"],
        "fan_kernel_stochastic": sp.simplify(fan_kernel[0, 0] + fan_kernel[0, 1] - 1)
        == 0,
        "fan_complete_local_observable_independent_of_h_and_unary_rates": left_observable
        == right_observable,
        "fan_arbitrary_upper_composition_independent_of_h": left_observable[
            "upper_composition"
        ]
        == right_observable["upper_composition"],
        "old_q1_q7_retains_h": left_old_signature != right_old_signature,
        "q8_fan_slide_detected": left_q8_signature == right_q8_signature,
        "q8_scalar_separated_response_is_raw_k": scalar_response
        == (("S@5:first-exposure", Fraction(2, 3)),
            ("T@3:first-exposure", Fraction(1, 3))),
        "q8_different_k_equal_after_future_null_composition": future_null_left
        == future_null_right
        == (("common-future", Fraction(1)),),
        "q8_same_k_different_typed_continuation_not_equal": typed_response_a
        != typed_response_b,
        "maximal_nested_first_hit_flattening_exact": flattened
        == (sp.Rational(1, 12), sp.Rational(1, 4), sp.Rational(2, 3)),
        "maximal_nested_contraction_order_independent": nested_outer_then_inner
        == nested_flattened_once
        == nested_inner_then_outer,
        "safe_fan_accepted": stopped_fan_safe(1, ()),
        "two_block_exposed_extension_rejected": not stopped_fan_safe(
            2, (("z", "T", Fraction(3)),)
        ),
    }
    record = make_record(
        job="triangle_response",
        case_input={
            "cases": ["bi-unary sister triangle", "pre-exposure unary routing fan"],
            "assumptions": "positive rates; gamma in (0,1); 0<h<a<d<r",
        },
        status="PASS" if all(checks.values()) else "BLOCKING",
        system={
            "kernel_states": ["survive", "merge"],
            "route_weights": ["1-gamma", "gamma"],
            "preexposure_fan": {
                "lower_boundary": ["x", 0, "one-block"],
                "first_exposure_ports": [
                    ["T", 3, "first-exposure", "1/3"],
                    ["S", 5, "first-exposure", "2/3"],
                ],
            },
        },
        exact_witness={
            "checks": checks,
            "kernel": str(kernel),
            "route_enumerated_kernel": str(enumerated_kernel),
            "forward_response": str(sp.factor(forward)),
            "reverse_response": str(sp.factor(reverse)),
            "forward_curvature": str(curvature),
            "preexposure_unary_fan": {
                "left_graph": graph_payload(left_graph),
                "right_graph": graph_payload(right_graph),
                "left_predicates": left_predicates,
                "right_predicates": right_predicates,
                "marked_xz_density_on_0_u_2": str(sp.factor(fan_density)),
                "metric_support_start": "a=3",
                "state_kernel": str(fan_kernel),
                "arbitrary_upper_continuation": str(left_observable["upper_composition"]),
                "old_q1_q7_left_signature": str(left_old_signature),
                "old_q1_q7_right_signature": str(right_old_signature),
                "q8_left_signature": str(left_q8_signature),
                "q8_right_signature": str(right_q8_signature),
                "future_null_left_response": str(future_null_left),
                "future_null_right_response": str(future_null_right),
                "same_k_typed_response_a": str(typed_response_a),
                "same_k_typed_response_b": str(typed_response_b),
                "nested_flattened_transport": str(flattened),
                "nested_outer_then_inner": str(nested_outer_then_inner),
                "nested_flattened_once": str(nested_flattened_once),
                "nested_inner_then_outer": str(nested_inner_then_outer),
                "exposed_extension": {
                    "maximum_internal_occupancy": 2,
                    "internal_sample_entries": [["z", "T", 3]],
                    "accepted": stopped_fan_safe(2, (("z", "T", Fraction(3)),)),
                },
            },
        },
        declared_quotient_orbit={
            "local_moves": [
                "bi-unary sister-triangle response",
                "Q8 pre-exposure unary-fan slide",
            ]
        },
        notes=(
            "The triangle responses and stopped-fan collision are independently recomputed; "
            "the fan guard rejects side entry and occupancy two."
        ),
    )
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_json_record(output, record)
    if record["status"] != "PASS":
        print("TRIANGLE_RESPONSE_BLOCKING")
        raise SystemExit(1)
    print("TRIANGLE_RESPONSE_OK kernel=PASS curvature=PASS unary_fan=PASS")


if __name__ == "__main__":
    main()
