#!/usr/bin/env python3
"""Adversarial theorem-logic mutations for the promotion referee.

The fixtures are deliberately tiny.  They test the logical validators used by
the proof without rerunning any local atlas or importing primary code.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from audit_promotion import AuditFailure, LANDMARK, transport_extends


def reject(condition: bool, label: str) -> None:
    if not condition:
        raise AuditFailure(label)


def validate_gapless(indices: list[int], count: int) -> None:
    reject(indices == list(range(count)), "path inventory is not a bijection")


def validate_q_partition(words: list[int], shapes: list[tuple[int, int]]) -> None:
    reject(sum(r * c for r, c in shapes) == len(words), "conditional q stream is truncated")


def validate_class_coherence(base: str, children: list[str]) -> None:
    allowed = "ordinary_T" if base == "ordinary_T" else "labelled_isomorphism"
    reject(all(child == allowed for child in children), "probe changed the fixed anchor class")


def validate_pointwise_rigidity(transport_count: int) -> None:
    reject(transport_count == 1, "fixed labelled anchor has a nontrivial pointwise automorphism")


def validate_one_port_locations(locations: dict[str, str]) -> None:
    reject(len(set(locations.values())) == len(locations),
           "one-port probes merged two distinct anchor intervals")


def validate_total_order(labels: tuple[str, ...], comparisons: dict[tuple[str, str], int]) -> None:
    directed = {label: set() for label in labels}
    indegree = {label: 0 for label in labels}
    for i, left in enumerate(labels):
        for right in labels[i + 1:]:
            sign = comparisons[(left, right)]
            before, after = (left, right) if sign < 0 else (right, left)
            directed[before].add(after)
            indegree[after] += 1
    queue = sorted(label for label in labels if indegree[label] == 0)
    visited = []
    while queue:
        current = queue.pop(0)
        visited.append(current)
        for nxt in sorted(directed[current]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
                queue.sort()
    reject(len(visited) == len(labels), "pair probes contain a directed cycle")


def validate_product_partition(classes: list[set[str]], values: dict[str, float]) -> None:
    seen: set[str] = set()
    for block in classes:
        reject(bool(block), "empty effective product class")
        reject(seen.isdisjoint(block), "physical edge occurs in two effective product classes")
        seen |= block
    reject(all(0.0 < values[edge] < 1.0 for edge in seen), "parameter left the open JC domain")


def validate_dummy_grammar(incoming_selected: bool, dummy: set[str], restored: set[str], remaining: set[str]) -> None:
    reject(("INCOMING" in dummy) == (not incoming_selected), "incoming dummy bit is wrong")
    reject(restored <= dummy, "restored role was not a declared dummy role")
    reject(remaining == dummy - restored, "dummy restoration is not a partition")
    reject(all(
        role == "INCOMING" or role.startswith("D_SINK_") or role.startswith("D_REPAIR_")
        for role in dummy
    ), "unknown weak-target role")


def validate_separator_direction(source_zero: bool, target_zero: bool, source_nonzero: bool, direction: str) -> None:
    if direction == "source_le_target":
        reject(target_zero and source_nonzero, "separator does not exclude source-to-target containment")
    else:
        reject(source_zero and not target_zero, "separator does not exclude target-to-source containment")


def baseline_transport() -> tuple[dict[str, Any], dict[str, Any]]:
    parent = {
        "vertex_transport": [[0, 10], [1, 11], [2, 12]],
        "port_transport": [["A", "A"], ["B", "B"]],
        "reticulation_transport_outside_redirected_triangle": [[2, 12]],
    }
    child = {
        "vertex_transport": [[0, 10], [1, 11], [2, 12], [3, 13], [4, 14]],
        "port_transport": [["A", "A"], ["B", "B"], ["p", "p"]],
        "reticulation_transport_outside_redirected_triangle": [[2, 12]],
    }
    return parent, child


def run_mutations() -> list[dict[str, str]]:
    tests: list[tuple[str, Callable[[], None]]] = []

    tests.append(("delete_path", lambda: validate_gapless([0, 1, 3], 4)))
    tests.append(("duplicate_path", lambda: validate_gapless([0, 1, 1, 2], 4)))
    tests.append(("truncate_q_block", lambda: validate_q_partition([0] * 11, [(3, 4)])))

    def corrupt_vertex() -> None:
        parent, child = baseline_transport()
        child["vertex_transport"][1][1] = 99
        transport_extends(parent, child, "mutated")

    tests.append(("corrupt_child_transport", corrupt_vertex))

    def cross_anchor() -> None:
        parent, child = baseline_transport()
        child["vertex_transport"][0][1], child["vertex_transport"][1][1] = (
            child["vertex_transport"][1][1], child["vertex_transport"][0][1]
        )
        transport_extends(parent, child, "cross-anchor")

    tests.append(("cross_anchor_identification", cross_anchor))
    tests.append(("probe_dependent_T_choice", lambda: validate_class_coherence("ordinary_T", ["ordinary_T", "labelled_isomorphism"])))
    tests.append(("nontrivial_anchor_automorphism", lambda: validate_pointwise_rigidity(2)))
    tests.append(("merged_one_port_intervals", lambda: validate_one_port_locations(
        {"left-empty-segment": "same", "right-empty-segment": "same"}
    )))

    def corrupt_t_sink() -> None:
        parent, child = baseline_transport()
        child["reticulation_transport_outside_redirected_triangle"] = [[2, 99]]
        transport_extends(parent, child, "T-sink")

    tests.append(("T_sink_transport_change", corrupt_t_sink))

    cyclic = {("p", "q"): -1, ("p", "r"): 1, ("q", "r"): -1}
    tests.append(("cyclic_pair_orders", lambda: validate_total_order(("p", "q", "r"), cyclic)))
    tests.append(("overlapping_product_classes", lambda: validate_product_partition(
        [{"e0", "e1"}, {"e1", "e2"}], {"e0": .5, "e1": .6, "e2": .7}
    )))
    tests.append(("boundary_product_parameter", lambda: validate_product_partition(
        [{"e0", "e1"}], {"e0": 0.0, "e1": .6}
    )))
    tests.append(("missing_incoming_dummy", lambda: validate_dummy_grammar(
        False, {"D_REPAIR_0_1"}, set(), {"D_REPAIR_0_1"}
    )))
    tests.append(("missing_sink_or_repair_partition", lambda: validate_dummy_grammar(
        True, {"D_SINK_0", "D_REPAIR_0_1"}, {"D_SINK_0"}, set()
    )))
    tests.append(("reverse_separator_direction", lambda: validate_separator_direction(
        source_zero=False, target_zero=True, source_nonzero=True, direction="target_le_source"
    )))

    def false_bound() -> None:
        certificate = json.loads((LANDMARK / "reviews/arbitrary_subdivision_promotion_referee/certificates/promotion_audit_certificate.json").read_text())
        reject(certificate["aggregate"]["exact_attained_probe_tensor_port_bound"] <= 9,
               "claimed bound 9 omits certified ten-port records")

    tests.append(("understate_tensor_port_bound", false_bound))

    results = []
    for name, operation in tests:
        try:
            operation()
        except (AuditFailure, KeyError, ValueError) as exc:
            results.append({"mutation": name, "status": "REJECTED", "reason": str(exc)})
        else:
            raise RuntimeError(f"mutation survived: {name}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = run_mutations()
    certificate = {
        "schema": "arbitrary-subdivision-promotion-mutations-v1",
        "status": "VERIFIED",
        "mutations_attempted": len(results),
        "mutations_rejected": len(results),
        "results": results,
    }
    rendered = json.dumps(certificate, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
