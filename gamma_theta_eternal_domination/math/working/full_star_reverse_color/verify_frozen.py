#!/usr/bin/env python3
"""Deterministically replay the frozen reverse-color candidate artifacts.

This checker shares ``probe_controls.py`` and verifier A, so it is a
candidate replay rather than an independent hostile verification.
"""

from __future__ import annotations

import json
from pathlib import Path

from probe_controls import analyze_graph, scan_orders


HERE = Path(__file__).resolve().parent


def replay_control() -> dict[str, object]:
    result = analyze_graph(r"Ksv`f\knJVis", (1, 2, 3), 0)
    incidence = result["full_incidences"][0]
    summary = {
        "schema": "full-star-reverse-color-control-v1",
        "status": "candidate-replay",
        "graph6_labeled": result["graph6"],
        "parameters": result["parameters"],
        "greatest_family_size": result["greatest_family_size"],
        "root": incidence["root"],
        "target": incidence["target"],
        "physical_link_vertices": incidence["physical_link_vertices"],
        "physical_link_edges": incidence["physical_link_edges"],
        "reverse_colors": incidence["reverse_colors_global"],
        "reverse_states_by_color": {
            str(color): [
                sorted([anchor, *edge])
                for edge in incidence["physical_link_edges"]
            ]
            for color, anchor in enumerate(incidence["root"])
        },
        "anchored_deletion_colorings": (
            incidence["anchored_deletion_coloring_vectors"]
        ),
        "feasible_target_colors": incidence["feasible_target_colors"],
        "color_restricted_kernels": {
            color: {
                "deletion_rounds": report["deletion_rounds"],
                "states": report["kernel_states"],
                "safe": report["safe"],
            }
            for color, report in incidence["restricted_kernel_reports"].items()
        },
        "conclusions": {
            "reverse_color_membership_implies_feasibility": (
                incidence["every_reverse_color_feasible"]
            ),
            "reverse_color_membership_implies_restricted_kernel_survival": all(
                color in incidence["restricted_safe_colors"]
                for color in incidence["reverse_colors_global"]
            ),
            "some_reverse_color_is_feasible_in_this_control": (
                incidence["some_reverse_color_feasible"]
            ),
            "counterexample_to_gamma_theta": (
                result["parameters"]["gamma"]
                == result["parameters"]["gamma_infinity"]
                < result["parameters"]["theta"]
            ),
        },
    }
    expected = json.loads((HERE / "control_result.json").read_text())
    if summary != expected:
        raise AssertionError("control_result.json does not match replay")
    return summary


def replay_order9() -> dict[str, object]:
    scan = scan_orders(9)
    counts = scan["counts"]
    summary = {
        "schema": "full-star-reverse-color-order9-probe-v1",
        "status": "observed-only",
        "generator": "tools/nauty2_9_3/geng -cq",
        "counts": counts,
        "total_connected_unlabeled_graphs": sum(
            row["connected_unlabeled_graphs"] for row in counts.values()
        ),
        "total_gamma_alpha_gamma_infinity_three": sum(
            row["gamma_alpha_gamma_infinity_three"]
            for row in counts.values()
        ),
        "total_full_incidences": sum(
            row["full_incidences"] for row in counts.values()
        ),
        "scope": {
            "complete_generator_stream": True,
            "independent_coverage_audit": False,
            "certificate_claim": False,
            "reverse_color_test_vacuous": True,
        },
    }
    expected = json.loads((HERE / "order9_result.json").read_text())
    if summary != expected:
        raise AssertionError("order9_result.json does not match replay")
    return summary


def main() -> None:
    control = replay_control()
    order9 = replay_order9()
    print(
        json.dumps(
            {
                "schema": "full-star-reverse-color-frozen-replay-v1",
                "control_verified": True,
                "order9_verified": True,
                "control_graph6": control["graph6_labeled"],
                "order9_connected_graphs": (
                    order9["total_connected_unlabeled_graphs"]
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
