#!/usr/bin/env python3
"""Probe full-star reverse colors and anchored deletion colorings.

This is discovery code, not an independent verifier.  It recomputes the
greatest eternal triple-family, the physical link, the globally transported
reverse colors, and every proper three-coloring of the deletion complement
with the root triangle fixed.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha,
    domination_number,
    eternal_domination_number,
    eternal_fixed_point,
    independent_domination_number,
    theta,
)


def vertices(bits: int, order: int) -> list[int]:
    return [vertex for vertex in range(order) if bits >> vertex & 1]


def triples(order: int) -> Iterable[tuple[tuple[int, int, int], int]]:
    for values in itertools.combinations(range(order), 3):
        yield values, sum(1 << value for value in values)


def alpha_exactly_three(
    graph: BitGraph,
) -> tuple[bool, list[tuple[tuple[int, int, int], int]]]:
    """Return alpha=3 and all independent triples."""

    complement = graph.complement()
    for values in itertools.combinations(range(graph.n), 4):
        if all(
            complement.adj[u] >> v & 1
            for u, v in itertools.combinations(values, 2)
        ):
            return False, []
    independent = [
        (values, state)
        for values, state in triples(graph.n)
        if graph.is_independent(state)
    ]
    return bool(independent), independent


def gamma_at_least_three(graph: BitGraph) -> bool:
    complement = graph.complement()
    return all(
        complement.adj[u] & complement.adj[v]
        for u, v in itertools.combinations(range(graph.n), 2)
    )


def anchored_deletion_colorings(
    complement: BitGraph,
    target: int,
    root: tuple[int, int, int],
) -> list[tuple[int, ...]]:
    """Enumerate H-target proper 3-colorings with root colors 0,1,2."""

    colors = [-1] * complement.n
    colors[target] = -2
    for color, anchor in enumerate(root):
        colors[anchor] = color
    order = [
        vertex
        for vertex in range(complement.n)
        if vertex != target and colors[vertex] == -1
    ]
    order.sort(
        key=lambda vertex: (
            -(complement.adj[vertex] & ~(1 << target)).bit_count(),
            vertex,
        )
    )
    answers: list[tuple[int, ...]] = []

    def search(position: int) -> None:
        if position == len(order):
            answers.append(tuple(colors))
            return
        vertex = order[position]
        forbidden = {
            colors[neighbor]
            for neighbor in vertices(
                complement.adj[vertex] & ~(1 << target), complement.n
            )
            if colors[neighbor] >= 0
        }
        for color in range(3):
            if color in forbidden:
                continue
            colors[vertex] = color
            search(position + 1)
        colors[vertex] = -1

    search(0)
    return answers


def restricted_kernel(
    graph: BitGraph,
    size: int,
    banned: set[int],
) -> tuple[set[int], list[int]]:
    active = {
        state
        for _values, state in (
            (
                values,
                sum(1 << value for value in values),
            )
            for values in itertools.combinations(range(graph.n), size)
        )
        if state not in banned and graph.is_dominating(state)
    }
    rounds: list[int] = []
    while True:
        delete: set[int] = set()
        for state in active:
            for attack in range(graph.n):
                attack_bit = 1 << attack
                if state & attack_bit:
                    continue
                if not any(
                    graph.adj[guard] & attack_bit
                    and (state ^ (1 << guard) ^ attack_bit) in active
                    for guard in vertices(state, graph.n)
                ):
                    delete.add(state)
                    break
        if not delete:
            return active, rounds
        rounds.append(len(delete))
        active.difference_update(delete)


def analyze_incidence(
    graph: BitGraph,
    family: set[int],
    root: tuple[int, int, int],
    target: int,
) -> dict[str, object] | None:
    root_mask = sum(1 << vertex for vertex in root)
    target_bit = 1 << target
    if not all(
        root_mask ^ (1 << anchor) ^ target_bit in family
        for anchor in root
    ):
        return None

    complement = graph.complement()
    physical = complement.adj[target]
    physical_vertices = vertices(physical, graph.n)
    link_edges = [
        (u, v)
        for u, v in itertools.combinations(physical_vertices, 2)
        if complement.adj[u] >> v & 1
    ]
    if not link_edges:
        return None

    edge_reverse: dict[str, list[int]] = {}
    for u, v in link_edges:
        edge_reverse[f"{u}-{v}"] = [
            color
            for color, anchor in enumerate(root)
            if (1 << anchor) | (1 << u) | (1 << v) in family
        ]
    reverse_sets = {tuple(values) for values in edge_reverse.values()}
    palettes = {
        vertex: {
            color
            for color, anchor in enumerate(root)
            if target_bit | (1 << anchor) | (1 << vertex) in family
        }
        for vertex in physical_vertices
    }
    exact_rows_verified = True
    hall_covers_all_guards = True
    for u, v in link_edges:
        state = target_bit | (1 << u) | (1 << v)
        union: set[int] = set()
        for color, anchor in enumerate(root):
            actual = {
                guard
                for guard in (target, u, v)
                if graph.adj[guard] >> anchor & 1
                and (state ^ (1 << guard) ^ (1 << anchor)) in family
            }
            expected = set()
            if color in edge_reverse[f"{u}-{v}"]:
                expected.add(target)
            if color in palettes[v]:
                expected.add(u)
            if color in palettes[u]:
                expected.add(v)
            exact_rows_verified &= actual == expected
            union.update(actual)
        hall_covers_all_guards &= union == {target, u, v}

    colorings = anchored_deletion_colorings(complement, target, root)
    avoiding: dict[str, int] = {}
    for color in range(3):
        avoiding[str(color)] = sum(
            all(coloring[vertex] != color for vertex in physical_vertices)
            for coloring in colorings
        )

    reverse = sorted(next(iter(reverse_sets))) if len(reverse_sets) == 1 else []
    safe_colors = []
    restricted_reports: dict[str, object] = {}
    for color, anchor in enumerate(root):
        banned = {
            root_mask ^ (1 << anchor) ^ (1 << vertex)
            for vertex in physical_vertices
        }
        restricted, rounds = restricted_kernel(graph, 3, banned)
        selected = root_mask ^ (1 << anchor) ^ target_bit
        safe = root_mask in restricted and selected in restricted
        if safe:
            safe_colors.append(color)
        restricted_reports[str(color)] = {
            "banned_states": len(banned),
            "kernel_states": len(restricted),
            "deletion_rounds": rounds,
            "root_survives": root_mask in restricted,
            "selected_target_state_survives": selected in restricted,
            "safe": safe,
        }
    return {
        "root": list(root),
        "target": target,
        "family_size": len(family),
        "physical_link_vertices": physical_vertices,
        "physical_link_edges": [list(edge) for edge in link_edges],
        "reverse_colors_by_edge": edge_reverse,
        "reverse_colors_global": reverse,
        "reverse_edge_independent": len(reverse_sets) == 1,
        "exact_response_rows_verified": exact_rows_verified,
        "hall_covers_all_three_guard_roles": hall_covers_all_guards,
        "anchored_deletion_colorings": len(colorings),
        "anchored_deletion_coloring_vectors": [
            [
                None if value == -2 else value
                for value in coloring
            ]
            for coloring in colorings
        ],
        "colorings_avoiding_color_on_physical_link": avoiding,
        "feasible_target_colors": [
            color for color in range(3) if avoiding[str(color)]
        ],
        "every_reverse_color_feasible": all(avoiding[str(color)] for color in reverse),
        "some_reverse_color_feasible": any(avoiding[str(color)] for color in reverse),
        "restricted_safe_colors": safe_colors,
        "restricted_kernel_reports": restricted_reports,
    }


def analyze_graph(
    record: str,
    selected_root: tuple[int, int, int] | None = None,
    selected_target: int | None = None,
    include_parameters: bool = True,
    require_gamma_three: bool = True,
) -> dict[str, object]:
    graph = BitGraph.from_graph6(record)
    alpha_three, independent = alpha_exactly_three(graph)
    static = alpha_three and (
        gamma_at_least_three(graph) if require_gamma_three else True
    )
    family = set(eternal_fixed_point(graph, 3).family) if static else set()
    incidences = []
    if static and family:
        for root, root_mask in independent:
            if selected_root is not None and root != selected_root:
                continue
            if root_mask not in family:
                raise AssertionError("maximum independent triple absent")
            for target in range(graph.n):
                if selected_target is not None and target != selected_target:
                    continue
                if root_mask >> target & 1:
                    continue
                result = analyze_incidence(graph, family, root, target)
                if result is not None:
                    incidences.append(result)
    result: dict[str, object] = {
        "graph6": record,
        "order": graph.n,
        "static_gamma_alpha_three": static,
        "alpha_exactly_three": alpha_three,
        "greatest_family_exists_at_three": bool(family),
        "greatest_family_size": len(family),
        "full_incidences": incidences,
    }
    if include_parameters:
        result["parameters"] = {
            "gamma": domination_number(graph),
            "i": independent_domination_number(graph),
            "alpha": alpha(graph),
            "gamma_infinity": eternal_domination_number(graph),
            "theta": theta(graph),
        }
    return result


def scan_orders(max_order: int) -> dict[str, object]:
    geng = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
    counts: dict[str, object] = {}
    countermodels = []
    records = []
    for order in range(1, max_order + 1):
        process = subprocess.Popen(
            [str(geng), "-cq", str(order)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        assert process.stdout is not None
        tested = equality = full = 0
        for line in process.stdout:
            record = line.strip()
            if not record:
                continue
            tested += 1
            result = analyze_graph(record, include_parameters=False)
            if (
                result["static_gamma_alpha_three"]
                and result["greatest_family_exists_at_three"]
            ):
                equality += 1
            incidences = result["full_incidences"]
            full += len(incidences)
            if incidences:
                records.append(result)
            for incidence in incidences:
                if not incidence["every_reverse_color_feasible"]:
                    countermodels.append(
                        {
                            "graph6": record,
                            "order": order,
                            "incidence": incidence,
                        }
                    )
        return_code = process.wait()
        if return_code:
            raise RuntimeError(f"geng failed with code {return_code}")
        counts[str(order)] = {
            "connected_unlabeled_graphs": tested,
            "gamma_alpha_gamma_infinity_three": equality,
            "full_incidences": full,
        }
    return {
        "counts": counts,
        "graphs_with_full_incidences": records,
        "countermodels_to_every_reverse_color": countermodels,
    }


def scan_toggles(
    record: str,
    root: tuple[int, int, int],
    target: int,
    radius: int,
) -> dict[str, object]:
    base = BitGraph.from_graph6(record)
    pairs = list(itertools.combinations(range(base.n), 2))
    tested = equality = full = 0
    pattern_counts: dict[str, int] = {}
    representatives: dict[str, object] = {}
    for edit_count in range(radius + 1):
        for edits in itertools.combinations(pairs, edit_count):
            tested += 1
            adjacency = list(base.adj)
            for u, v in edits:
                adjacency[u] ^= 1 << v
                adjacency[v] ^= 1 << u
            graph = BitGraph(base.n, tuple(adjacency))
            generated = graph.to_graph6()
            result = analyze_graph(
                generated,
                root,
                target,
                include_parameters=False,
            )
            if (
                result["static_gamma_alpha_three"]
                and result["greatest_family_exists_at_three"]
            ):
                equality += 1
            incidences = result["full_incidences"]
            if not incidences:
                continue
            full += 1
            incidence = incidences[0]
            pattern = json.dumps(
                {
                    "reverse": incidence["reverse_colors_global"],
                    "safe": incidence["restricted_safe_colors"],
                    "feasible": incidence["feasible_target_colors"],
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            representatives.setdefault(
                pattern,
                {
                    "graph6": generated,
                    "edits": [list(edge) for edge in edits],
                    "incidence": incidence,
                },
            )
    return {
        "base_graph6": record,
        "root": list(root),
        "target": target,
        "toggle_radius": radius,
        "labeled_graphs_tested": tested,
        "equality_graphs": equality,
        "full_incidences": full,
        "pattern_counts": pattern_counts,
        "representatives": representatives,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph6",
        action="append",
        default=[],
        help="labeled graph6 control to analyze",
    )
    parser.add_argument(
        "--root",
        help="optional comma-separated ordered root triple",
    )
    parser.add_argument("--target", type=int)
    parser.add_argument("--scan-through", type=int, default=0)
    parser.add_argument("--toggle-base")
    parser.add_argument("--toggle-radius", type=int, default=0)
    parser.add_argument("--allow-gamma-two", action="store_true")
    arguments = parser.parse_args()

    selected_root = (
        tuple(int(value) for value in arguments.root.split(","))
        if arguments.root
        else None
    )
    if selected_root is not None and len(selected_root) != 3:
        raise SystemExit("--root requires three comma-separated vertices")
    controls = [
        analyze_graph(
            record,
            selected_root,
            arguments.target,
            require_gamma_three=not arguments.allow_gamma_two,
        )
        for record in arguments.graph6
    ]
    scan = scan_orders(arguments.scan_through) if arguments.scan_through else None
    toggles = None
    if arguments.toggle_base:
        if selected_root is None or arguments.target is None:
            raise SystemExit("--toggle-base requires --root and --target")
        toggles = scan_toggles(
            arguments.toggle_base,
            selected_root,
            arguments.target,
            arguments.toggle_radius,
        )
    print(
        json.dumps(
            {
                "schema": "full-star-reverse-color-probe-v1",
                "status": "DISCOVERY_ONLY",
                "controls": controls,
                "scan": scan,
                "toggle_scan": toggles,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
