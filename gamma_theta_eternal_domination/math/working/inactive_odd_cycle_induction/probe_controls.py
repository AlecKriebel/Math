#!/usr/bin/env python3
"""Check the proposed path-parity invariant in exact equality controls."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[3]
C4_PATH = CAMPAIGN / "math/working/inactive_odd_cycle_attack/verify_c4_control.py"
SPEC = importlib.util.spec_from_file_location("c4_control", C4_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import C4 control verifier")
C4 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C4)
G6_PATH = CAMPAIGN / "math/working/all_k_extension_bridge/verify_positive_control.py"
G6_SPEC = importlib.util.spec_from_file_location("g6_control", G6_PATH)
if G6_SPEC is None or G6_SPEC.loader is None:
    raise RuntimeError("cannot import graph6 control verifier")
G6 = importlib.util.module_from_spec(G6_SPEC)
G6_SPEC.loader.exec_module(G6)


def state_mask(state: set[int]) -> int:
    return sum(1 << vertex for vertex in state)


def induced_paths(
    adjacency: tuple[int, ...],
    allowed: set[int],
) -> list[tuple[int, ...]]:
    answer: list[tuple[int, ...]] = []

    def extend(path: tuple[int, ...]) -> None:
        if len(path) >= 3:
            answer.append(path)
        last = path[-1]
        for following in allowed:
            if following in path or not (adjacency[last] >> following & 1):
                continue
            if any(adjacency[following] >> earlier & 1 for earlier in path[:-1]):
                continue
            extend(path + (following,))

    for start in sorted(allowed):
        extend((start,))
    return answer


def main() -> None:
    controls = [
        ("accepted exact C4 equality control", C4.complement(C4.graph(16, C4.H_EDGES))),
        ("order-nine equality control HCQebjw", G6.decode_graph6("HCQebjw")),
        ("order-five equality control FCZbg", G6.decode_graph6("FCZbg")),
    ]
    control_rows = []
    rows = []
    for control_name, g in controls:
        if G6.parameter_record(g) != {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        }:
            continue
        h = C4.complement(g)
        family = C4.greatest_family(g, 3)
        target_rows = []
        for target in range(len(g)):
            retained = tuple(vertex for vertex in range(len(g)) if vertex != target)
            deletion = G6.induced(g, retained)
            if C4.domination_number(deletion) < 3:
                continue
            triangles = tuple(
                frozenset(state)
                for state in itertools.combinations(retained, 3)
                if all(
                    h[first] >> second & 1
                    for first, second in itertools.combinations(state, 2)
                )
            )
            containing_by_vertex = {
                vertex: [state for state in triangles if vertex in state]
                for vertex in retained
            }
            if any(not containing for containing in containing_by_vertex.values()):
                continue
            inactive: set[int] = set()
            for vertex, containing in containing_by_vertex.items():
                statuses = {
                    bool(g[vertex] >> target & 1)
                    and state_mask((set(state) - {vertex}) | {target}) in family
                    for state in containing
                }
                if len(statuses) != 1:
                    raise AssertionError("vertex-star propagation failed")
                if statuses == {False}:
                    inactive.add(vertex)
            paths = induced_paths(h, inactive)
            target_rows.append(
                {
                    "target": target,
                    "inactive_set": sorted(inactive),
                    "induced_path_count": len(paths),
                }
            )
            for path in paths:
                edges = len(path) - 1
                endpoint_state = state_mask({path[0], path[-1], target})
                actual = endpoint_state in family
                expected = edges % 2 == 1
                if actual != expected:
                    rows.append(
                        {
                            "control": control_name,
                            "target": target,
                            "path": path,
                            "path_edges": edges,
                            "expected_endpoint_membership": expected,
                            "actual_endpoint_membership": actual,
                        }
                    )
        control_rows.append(
            {
                "control": control_name,
                "eligible_targets": target_rows,
            }
        )
    print(
        json.dumps(
            {
                "classification": "OBSERVED",
                "controls": control_rows,
                "path_parity_failures": rows,
                "schema": "inactive-path-parity-control-probe-v1",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
