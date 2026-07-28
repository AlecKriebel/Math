#!/usr/bin/env python3
"""Measure the shape of unsafe-color attack certificates in the MMV catalog.

The scan is exploratory.  For every full greatest-family incidence in the
fixed published near-miss catalog, it asks whether an unsafe color can be
defeated while the other two root guards remain fixed throughout the
restricted reachability game.
"""

from __future__ import annotations

import csv
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[2]
PROBE = HERE.parent / "full_list_safe_kernel_probe" / "probe.py"
SPEC = importlib.util.spec_from_file_location("safe_probe", PROBE)
assert SPEC is not None and SPEC.loader is not None
safe_probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(safe_probe)


def deletion_ranks(graph, banned):
    active = {
        state
        for state in safe_probe.subsets(len(graph), 3)
        if state not in banned and safe_probe.dominates(graph, state)
    }
    ranks = {}
    round_number = 0
    while True:
        delete = set()
        for state in active:
            for attack in range(len(graph)):
                if attack in state:
                    continue
                if not any(
                    attack in graph[guard]
                    and (state - {guard}) | {attack} in active
                    for guard in state
                ):
                    delete.add(state)
                    break
        if not delete:
            return frozenset(active), ranks
        for state in delete:
            ranks[state] = round_number
        active.difference_update(delete)
        round_number += 1


def successors(graph, state, attack):
    return frozenset(
        (state - {guard}) | {attack}
        for guard in state
        if attack in graph[guard]
        and safe_probe.dominates(
            graph, (state - {guard}) | {attack}
        )
    )


def fixed_pair_win(graph, state, fixed_pair, banned, ranks, memo):
    if state in banned:
        return True
    if state in memo:
        return memo[state]
    if not fixed_pair <= state or state not in ranks:
        memo[state] = False
        return False
    current_rank = ranks[state]
    for attack in range(len(graph)):
        if attack in state:
            continue
        children = successors(graph, state, attack)
        if children and all(
            child in banned
            or (
                child in ranks
                and ranks[child] < current_rank
                and fixed_pair_win(
                    graph, child, fixed_pair, banned, ranks, memo
                )
            )
            for child in children
        ):
            memo[state] = True
            return True
    memo[state] = False
    return False


def deleting_attacks(graph, state, banned, ranks):
    current_rank = ranks[state]
    answers = []
    for attack in range(len(graph)):
        if attack in state:
            continue
        children = successors(graph, state, attack)
        if children and all(
            child in banned
            or (child in ranks and ranks[child] < current_rank)
            for child in children
        ):
            answers.append((attack, children))
    return tuple(answers)


def reachable_rank_zero(graph, start, banned, ranks):
    frontier = [start]
    seen = set()
    terminals = set()
    while frontier:
        state = frontier.pop()
        if state in seen:
            continue
        seen.add(state)
        if ranks[state] == 0:
            terminals.add(state)
            continue
        for _, children in deleting_attacks(
            graph, state, banned, ranks
        ):
            for child in children:
                if child in ranks:
                    frontier.append(child)
    return frozenset(terminals)


def rank_zero_types(graph, state, fixed_pair, banned, ranks):
    kinds = set()
    for attack, children in deleting_attacks(
        graph, state, banned, ranks
    ):
        if not all(child in banned for child in children):
            continue
        if fixed_pair <= state and attack not in fixed_pair:
            kinds.add("corridor")
        elif attack in fixed_pair:
            kinds.add("anchor_restoration")
        else:
            kinds.add("other")
    return frozenset(kinds)


def main():
    with (CAMPAIGN / "instances" / "mmv2022_table9.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    totals = {
        "graphs": 0,
        "full_incidences": 0,
        "unsafe_colors": 0,
        "nonempty_kernel_without_forced_start": 0,
        "fixed_pair_wins": 0,
        "has_corridor_terminal": 0,
        "has_anchor_restoration_terminal": 0,
        "has_only_anchor_restoration_terminals": 0,
    }
    rank_histogram = {}
    failures = []
    for row in rows:
        graph = safe_probe.decode_graph6(row["graph6"])
        if safe_probe.exact_alpha(graph) != 3:
            continue
        family, _ = safe_probe.greatest_safe_family(graph, 3)
        totals["graphs"] += 1
        independent_states = tuple(
            state
            for state in safe_probe.subsets(len(graph), 3)
            if safe_probe.independent(graph, state)
        )
        for root in independent_states:
            for target in range(len(graph)):
                if target in root:
                    continue
                if (
                    safe_probe.response_list(
                        graph, family, root, target
                    )
                    != root
                ):
                    continue
                totals["full_incidences"] += 1
                link = safe_probe.complement_neighbors(graph, target)
                for color in root:
                    banned = frozenset(
                        (root - {color}) | {vertex}
                        for vertex in link
                    )
                    kernel, ranks = deletion_ranks(graph, banned)
                    start = (root - {color}) | {target}
                    if start in kernel:
                        continue
                    totals["unsafe_colors"] += 1
                    if kernel:
                        totals[
                            "nonempty_kernel_without_forced_start"
                        ] += 1
                    rank = ranks[start]
                    rank_histogram[str(rank)] = (
                        rank_histogram.get(str(rank), 0) + 1
                    )
                    fixed_pair = root - {color}
                    works = fixed_pair_win(
                        graph,
                        start,
                        fixed_pair,
                        banned,
                        ranks,
                        {},
                    )
                    if works:
                        totals["fixed_pair_wins"] += 1
                    terminal_kinds = set()
                    for terminal in reachable_rank_zero(
                        graph, start, banned, ranks
                    ):
                        terminal_kinds.update(
                            rank_zero_types(
                                graph,
                                terminal,
                                fixed_pair,
                                banned,
                                ranks,
                            )
                        )
                    if "corridor" in terminal_kinds:
                        totals["has_corridor_terminal"] += 1
                    if "anchor_restoration" in terminal_kinds:
                        totals["has_anchor_restoration_terminal"] += 1
                    if terminal_kinds == {"anchor_restoration"}:
                        totals[
                            "has_only_anchor_restoration_terminals"
                        ] += 1
                    if not works and len(failures) < 20:
                        failures.append(
                            {
                                "catalog_id": row["catalog_id"],
                                "graph6": row["graph6"],
                                "root": sorted(root),
                                "target": target,
                                "color": color,
                                "start_rank": rank,
                                "terminal_kinds": sorted(terminal_kinds),
                            }
                        )
    output = {
        "scope": "exploratory fixed MMV 2022 Table 9 catalog",
        "totals": totals,
        "unsafe_start_rank_histogram": rank_histogram,
        "non_fixed_pair_failures": failures,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
