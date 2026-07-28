#!/usr/bin/env python3
"""Replay the finite controls for the cumulative safe-kernel reduction.

The transition routines are the ordinary-frozenset implementation from the
independent safe-kernel probe.  This script is evidence for the stated
controls only; the theorems in NOTE.md are proved mathematically.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE = HERE.parent / "full_list_safe_kernel_probe" / "probe.py"
SPEC = importlib.util.spec_from_file_location("safe_probe", PROBE)
assert SPEC is not None and SPEC.loader is not None
safe_probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(safe_probe)


def proper_on_full_core(graph, assignment):
    return all(
        assignment[x] != assignment[y] or y in graph[x]
        for x, y in itertools.combinations(assignment, 2)
    )


def cumulative_profile(record, root_vertices):
    graph = safe_probe.decode_graph6(record)
    root = frozenset(root_vertices)
    greatest, _ = safe_probe.greatest_safe_family(graph, 3)
    full_core = tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in root
        and safe_probe.response_list(
            graph, greatest, root, vertex
        )
        == root
    )
    profiles = []
    for colors in itertools.product(sorted(root), repeat=len(full_core)):
        assignment = dict(zip(full_core, colors))
        if not proper_on_full_core(graph, assignment):
            continue
        banned = set()
        for target, color in assignment.items():
            banned.update(
                (root - {color}) | {vertex}
                for vertex in safe_probe.complement_neighbors(
                    graph, target
                )
            )
        kernel, _ = safe_probe.greatest_safe_family(
            graph, 3, banned=frozenset(banned)
        )
        coloring_count = 0
        if kernel:
            lists = {
                vertex: (
                    frozenset({assignment[vertex]})
                    if vertex in assignment
                    else safe_probe.response_list(
                        graph, kernel, root, vertex
                    )
                )
                for vertex in range(len(graph))
                if vertex not in root
            }
            coloring_count = len(
                safe_probe.compatible_anchored_colorings(
                    graph, root, lists, limit=10000
                )
            )
        profiles.append(
            {
                "assignment": {
                    str(vertex): color
                    for vertex, color in sorted(assignment.items())
                },
                "kernel_states": len(kernel),
                "compatible_colorings": coloring_count,
            }
        )
    return {
        "graph6": record,
        "parameters": safe_probe.exact_parameters(graph),
        "root": sorted(root),
        "full_core": list(full_core),
        "proper_assignment_profiles": profiles,
    }


def individual_profile(record, root_vertices, target, color):
    graph = safe_probe.decode_graph6(record)
    root = frozenset(root_vertices)
    banned = frozenset(
        (root - {color}) | {vertex}
        for vertex in safe_probe.complement_neighbors(graph, target)
    )
    kernel, _ = safe_probe.greatest_safe_family(
        graph, 3, banned=banned
    )
    successor = (root - {color}) | {target}
    lists = {
        vertex: (
            frozenset({color})
            if vertex == target
            else safe_probe.response_list(graph, kernel, root, vertex)
        )
        for vertex in range(len(graph))
        if vertex not in root
    }
    colorings = (
        safe_probe.compatible_anchored_colorings(
            graph, root, lists, limit=10000
        )
        if kernel
        else ()
    )
    return {
        "graph6": record,
        "root": sorted(root),
        "target": target,
        "color": color,
        "kernel_states": len(kernel),
        "forced_successor_survives": successor in kernel,
        "compatible_colorings_with_target_fixed": len(colorings),
    }


def main():
    result = {
        "scope": (
            "finite controls only; no exhaustive theorem and no "
            "gamma-theta resolution"
        ),
        "equality_control": cumulative_profile(
            r"Ksv`f\knJVis", (1, 2, 3)
        ),
        "mmv001_all_empty": cumulative_profile(
            "IEhbtj{ro", (0, 1, 2)
        ),
        "mmv021_joint_core": cumulative_profile(
            "JEhbtj{rv~?", (0, 1, 2)
        ),
        "mmv021_individual_safe_target": individual_profile(
            "JEhbtj{rv~?", (0, 1, 2), 10, 2
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
