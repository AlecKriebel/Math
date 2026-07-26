#!/usr/bin/env python3
"""Clean-room hostile audit for the two order-13, parameter-three notes.

This program uses only the Python standard library.  It does not import the
campaign search code, either eternal-domination evaluator, or either CNF
constructor.  Its finite checks support (but do not replace) the written
all-orders arguments reviewed in REVIEW.md.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence


ROOT = Path(__file__).resolve().parents[2]
SYNTHESIS_NOTE = ROOT / "math/lemmas/order13_k3_synthesis_target.md"
HOLE_NOTE = ROOT / "math/lemmas/order13_k3_hole11_exclusion.md"

FROZEN_NOTES = {
    "math/lemmas/order13_k3_synthesis_target.md": {
        "sha256": "02c661edf61db8f4b4a5769972e726ce8c1c693e418c1b97b2293e68765e0f44",
        "bytes": 26112,
    },
    "math/lemmas/order13_k3_hole11_exclusion.md": {
        "sha256": "ee492ff314ac2df5f9e1e80982c9bd455dcbce30106d54083d0cd7a930627408",
        "bytes": 16303,
    },
}

LOCAL_PRIMARY_SOURCES = (
    "literature/sources/km2015_src/gamma_theta_Revised_July_11.tex",
    "literature/sources/km2016_src/ProtectionSurvey_KlostermeyerMynhardt_Mar5_2015.tex",
    "literature/sources/mmv2022_src/EternalDomination.tex",
    "literature/sources/taletskii2024_src/GammaThetav2.tex",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_binding(relative: str) -> dict[str, object]:
    data = (ROOT / relative).read_bytes()
    return {"path": relative, "bytes": len(data), "sha256": sha256(data)}


def verify_frozen_notes() -> list[dict[str, object]]:
    result = []
    for relative, expected in FROZEN_NOTES.items():
        actual = file_binding(relative)
        if actual["sha256"] != expected["sha256"] or actual["bytes"] != expected["bytes"]:
            raise AssertionError({"frozen_note_changed": relative, "actual": actual})
        result.append(actual)
    return result


# ---------------------------------------------------------------------------
# Small graph kernel.  A graph is a tuple of open-neighborhood bit masks.


Graph = tuple[int, ...]


def empty_graph(n: int) -> list[int]:
    return [0] * n


def add_edge(adjacency: list[int], u: int, v: int) -> None:
    if u == v:
        raise AssertionError("loops are forbidden")
    adjacency[u] |= 1 << v
    adjacency[v] |= 1 << u


def has_edge(graph: Graph, u: int, v: int) -> bool:
    return bool(graph[u] & (1 << v))


def complement(graph: Graph) -> Graph:
    n = len(graph)
    universe = (1 << n) - 1
    return tuple((universe ^ (1 << v) ^ graph[v]) for v in range(n))


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(i for i in range(mask.bit_length()) if mask & (1 << i))


def subset_mask(values: Iterable[int]) -> int:
    result = 0
    for value in values:
        result |= 1 << value
    return result


def dominates(graph: Graph, state: int) -> bool:
    covered = state
    pending = state
    while pending:
        bit = pending & -pending
        pending ^= bit
        covered |= graph[bit.bit_length() - 1]
    return covered == (1 << len(graph)) - 1


def independent(graph: Graph, state: int) -> bool:
    pending = state
    while pending:
        bit = pending & -pending
        pending ^= bit
        if graph[bit.bit_length() - 1] & pending:
            return False
    return True


def legal_successors(graph: Graph, state: int, attack: int) -> tuple[int, ...]:
    if state & (1 << attack):
        raise AssertionError("occupied attack")
    successors = []
    pending = state
    while pending:
        guard_bit = pending & -pending
        pending ^= guard_bit
        guard = guard_bit.bit_length() - 1
        if not has_edge(graph, guard, attack):
            continue
        successor = (state ^ guard_bit) | (1 << attack)
        if dominates(graph, successor):
            successors.append(successor)
    return tuple(sorted(successors))


def all_k_subsets(n: int, k: int) -> Iterator[int]:
    for values in itertools.combinations(range(n), k):
        yield subset_mask(values)


def minimum_domination(graph: Graph, maximum: int) -> int | None:
    for size in range(1, maximum + 1):
        if any(dominates(graph, state) for state in all_k_subsets(len(graph), size)):
            return size
    return None


def maximum_independence_at_most_four(graph: Graph) -> int:
    n = len(graph)
    found = 0
    for size in range(1, 5):
        if any(independent(graph, state) for state in all_k_subsets(n, size)):
            found = size
        else:
            return found
    return 4


def independent_domination_at_most_three(graph: Graph) -> int | None:
    n = len(graph)
    for size in range(1, 4):
        for state in all_k_subsets(n, size):
            if independent(graph, state) and dominates(graph, state):
                return size
    return None


def k_colorable(graph: Graph, k: int) -> bool:
    """Exact deterministic DSATUR decision."""
    n = len(graph)
    colors = [-1] * n
    degrees = [graph[v].bit_count() for v in range(n)]

    def search(colored: int) -> bool:
        if colored == n:
            return True
        candidates = []
        for v in range(n):
            if colors[v] >= 0:
                continue
            used = {
                colors[u]
                for u in range(n)
                if colors[u] >= 0 and has_edge(graph, u, v)
            }
            candidates.append((len(used), degrees[v], -v, v, used))
        _, _, _, vertex, forbidden = max(candidates)
        for color in range(k):
            if color in forbidden:
                continue
            colors[vertex] = color
            if search(colored + 1):
                return True
            colors[vertex] = -1
        return False

    return search(0)


def chromatic_number_at_most_four(graph: Graph) -> int | None:
    for k in range(1, 5):
        if k_colorable(graph, k):
            return k
    return None


def eternal_fixed_point(graph: Graph, k: int) -> tuple[set[int], list[int]]:
    """Greatest fixed point on dominating k-configurations, from definition."""
    alive = {
        state
        for state in all_k_subsets(len(graph), k)
        if dominates(graph, state)
    }
    deleted_by_round = []
    while True:
        doomed = set()
        for state in alive:
            for attack in range(len(graph)):
                if state & (1 << attack):
                    continue
                answered = False
                pending = state
                while pending:
                    guard_bit = pending & -pending
                    pending ^= guard_bit
                    guard = guard_bit.bit_length() - 1
                    if not has_edge(graph, guard, attack):
                        continue
                    successor = (state ^ guard_bit) | (1 << attack)
                    if successor in alive:
                        answered = True
                        break
                if not answered:
                    doomed.add(state)
                    break
        if not doomed:
            return alive, deleted_by_round
        alive.difference_update(doomed)
        deleted_by_round.append(len(doomed))


# ---------------------------------------------------------------------------
# Complement dictionary and CNF local semantics.


def graph_from_edge_mask(n: int, mask: int) -> Graph:
    adjacency = empty_graph(n)
    bit_index = 0
    for v in range(1, n):
        for u in range(v):
            if mask & (1 << bit_index):
                add_edge(adjacency, u, v)
            bit_index += 1
    return tuple(adjacency)


def pair_common_neighbor_audit() -> dict[str, int]:
    n = 6
    graph_count = 1 << math.comb(n, 2)
    pair_checks = 0
    for mask in range(graph_count):
        h_graph = graph_from_edge_mask(n, mask)
        g_graph = complement(h_graph)
        for a, b in itertools.combinations(range(n), 2):
            pair = (1 << a) | (1 << b)
            fails_to_dominate = not dominates(g_graph, pair)
            common = any(
                x not in (a, b)
                and has_edge(h_graph, a, x)
                and has_edge(h_graph, b, x)
                for x in range(n)
            )
            if fails_to_dominate != common:
                raise AssertionError(("pair dictionary", mask, a, b))
            pair_checks += 1
    return {"n": n, "graphs": graph_count, "pair_checks": pair_checks}


def connected(graph: Graph) -> bool:
    n = len(graph)
    seen = 1
    frontier = 1
    while frontier:
        next_frontier = 0
        pending = frontier
        while pending:
            bit = pending & -pending
            pending ^= bit
            next_frontier |= graph[bit.bit_length() - 1]
        next_frontier &= ~seen
        seen |= next_frontier
        frontier = next_frontier
    return seen == (1 << n) - 1


def complement_cut_clauses_hold(h_graph: Graph) -> bool:
    n = len(h_graph)
    full = (1 << n) - 1
    for choice in range(1 << (n - 1)):
        state = 1
        for offset in range(n - 1):
            if choice & (1 << offset):
                state |= 1 << (offset + 1)
        if state == full:
            continue
        outside = full ^ state
        crossing_g_edge = False
        for u in vertices(state):
            for v in vertices(outside):
                if not has_edge(h_graph, u, v):
                    crossing_g_edge = True
                    break
            if crossing_g_edge:
                break
        if not crossing_g_edge:
            return False
    return True


def cut_sign_audit() -> dict[str, int]:
    n = 5
    graph_count = 1 << math.comb(n, 2)
    for mask in range(graph_count):
        h_graph = graph_from_edge_mask(n, mask)
        if complement_cut_clauses_hold(h_graph) != connected(complement(h_graph)):
            raise AssertionError(("cut complement sign", mask))
    return {
        "n": n,
        "H_graphs": graph_count,
        "cuts_per_graph": (1 << (n - 1)) - 1,
    }


def cnf_gadget_truth_tables() -> dict[str, int]:
    # no-K4 clause: six H-edge literals, with at least one required false.
    no_k4_cases = 0
    for edge_mask in range(1 << 6):
        clause = any(not bool(edge_mask & (1 << bit)) for bit in range(6))
        if clause != (edge_mask != (1 << 6) - 1):
            raise AssertionError("no-K4 truth table")
        no_k4_cases += 1

    # One pair, three eligible common-neighbor candidates.  Existentially
    # quantify the three witness variables exactly as (4.2)--(4.3).
    witness_cases = 0
    for edge_mask in range(1 << 6):
        left = [bool(edge_mask & (1 << i)) for i in range(3)]
        right = [bool(edge_mask & (1 << (3 + i))) for i in range(3)]
        cnf_exists = False
        for witness_mask in range(1 << 3):
            witnesses = [bool(witness_mask & (1 << i)) for i in range(3)]
            if not any(witnesses):
                continue
            if all(
                (not witnesses[i]) or (left[i] and right[i])
                for i in range(3)
            ):
                cnf_exists = True
                break
        semantic = any(left[i] and right[i] for i in range(3))
        if cnf_exists != semantic:
            raise AssertionError("pair witness gadget")
        witness_cases += 1

    domination_cases = 0
    for f_selected in (False, True):
        for h_edges_mask in range(1 << 3):
            h_edges = [bool(h_edges_mask & (1 << i)) for i in range(3)]
            clause = (not f_selected) or any(not value for value in h_edges)
            semantic = (not f_selected) or not all(h_edges)
            if clause != semantic:
                raise AssertionError("domination complement sign")
            domination_cases += 1

    # Existentially quantify alternative response variables.  A true response
    # represents one guard, one G-edge, and one selected successor.
    response_cases = 0
    for f_source in (False, True):
        for h_edge_mask in range(1 << 3):
            h_edges = [bool(h_edge_mask & (1 << i)) for i in range(3)]
            for successor_mask in range(1 << 3):
                selected_successors = [
                    bool(successor_mask & (1 << i)) for i in range(3)
                ]
                cnf_exists = False
                for move_mask in range(1 << 3):
                    moves = [bool(move_mask & (1 << i)) for i in range(3)]
                    existence = (not f_source) or any(moves)
                    implications = all(
                        (not moves[i])
                        or ((not h_edges[i]) and selected_successors[i])
                        for i in range(3)
                    )
                    if existence and implications:
                        cnf_exists = True
                        break
                semantic = (not f_source) or any(
                    (not h_edges[i]) and selected_successors[i]
                    for i in range(3)
                )
                if cnf_exists != semantic:
                    raise AssertionError("one-guard response gadget")
                response_cases += 1

    triangle_cases = 0
    for edge_mask in range(1 << 3):
        for f_selected in (False, True):
            h_edges = [bool(edge_mask & (1 << i)) for i in range(3)]
            clause = any(not value for value in h_edges) or f_selected
            semantic = (not all(h_edges)) or f_selected
            if clause != semantic:
                raise AssertionError("triangle-to-family gadget")
            triangle_cases += 1

    return {
        "no_K4_cases": no_k4_cases,
        "pair_witness_edge_cases": witness_cases,
        "selected_state_domination_cases": domination_cases,
        "one_guard_response_primary_cases": response_cases,
        "triangle_to_family_cases": triangle_cases,
    }


# ---------------------------------------------------------------------------
# Odd-hole coverage, template arithmetic, and complete coloring banks.


def spgt_coverage_arithmetic() -> dict[str, object]:
    antiholes = []
    for order in range(5, 14, 2):
        q = (order - 1) // 2
        if q <= 3:
            antiholes.append(
                {
                    "order": order,
                    "clique_number": q,
                    "disposition": (
                        "self-complementary C5"
                        if order == 5
                        else "C7 antihole excluded by accepted C-017"
                    ),
                }
            )
    if [item["order"] for item in antiholes] != [5, 7]:
        raise AssertionError("SPGT antihole arithmetic")
    odd_holes_with_two_outsiders = [
        order for order in range(5, 14, 2) if order <= 13 - 2
    ]
    if odd_holes_with_two_outsiders != [5, 7, 9, 11]:
        raise AssertionError("odd-hole length cover")
    odd_holes_with_three_outsiders = [
        order for order in range(5, 14, 2) if order <= 13 - 3
    ]
    if odd_holes_with_three_outsiders != [5, 7, 9]:
        raise AssertionError("strengthened odd-hole length cover")
    return {
        "odd_antiholes_compatible_with_omega_at_most_3": antiholes,
        "order13_hub_free_holes_after_two_outside_argument":
            odd_holes_with_two_outsiders,
        "order13_hub_free_holes_after_near_spanning_theorem":
            odd_holes_with_three_outsiders,
    }


def canonical_color_row(row: Sequence[int]) -> tuple[int, ...]:
    rename: dict[int, int] = {}
    result = []
    for color in row:
        if color not in rename:
            rename[color] = len(rename)
        result.append(rename[color])
    return tuple(result)


def proper_cycle_rows(length: int) -> Iterator[tuple[int, ...]]:
    row = [-1] * length

    def extend(index: int) -> Iterator[tuple[int, ...]]:
        if index == length:
            if row[-1] != row[0]:
                yield tuple(row)
            return
        for color in range(3):
            if index > 0 and row[index - 1] == color:
                continue
            if index == length - 1 and row[0] == color:
                continue
            row[index] = color
            yield from extend(index + 1)
            row[index] = -1

    yield from extend(0)


def enumerate_coloring_bank(length: int) -> tuple[tuple[int, ...], ...]:
    z = length
    free = tuple(range(length + 1, 13))
    bank = set()
    for rim in proper_cycle_rows(length):
        z_color = ({0, 1, 2} - {rim[0], rim[1]}).pop()
        for tail in itertools.product(range(3), repeat=len(free)):
            row = list(rim) + [z_color] + list(tail)
            canonical = canonical_color_row(row)
            if len(set(canonical)) != 3:
                raise AssertionError("forced triangle did not use three colors")
            bank.add(canonical)
    return tuple(sorted(bank))


def bank_and_census_audit() -> dict[str, object]:
    expected_bank = {5: 10935, 7: 5103, 9: 2295, 11: 1023}
    expected_base = {5: 29791, 7: 29800, 9: 29813, 11: 29830}
    branches = []
    for length in (5, 7, 9, 11):
        bank = enumerate_coloring_bank(length)
        formula_count = ((2**length - 2) * 3 ** (12 - length)) // 6
        if len(bank) != formula_count or len(bank) != expected_bank[length]:
            raise AssertionError(("coloring bank count", length, len(bank)))
        for row in bank:
            if row[0] == row[1] or row[0] == row[length] or row[1] == row[length]:
                raise AssertionError(("forced triangle coloring", length, row))
            if any(row[i] == row[(i + 1) % length] for i in range(length)):
                raise AssertionError(("rim coloring", length, row))
            if canonical_color_row(row) != row:
                raise AssertionError(("noncanonical row", length, row))
        encoded = json.dumps(bank, separators=(",", ":")).encode("ascii")

        category_counts = {
            "no_K4": math.comb(13, 4),
            "pair_witnesses": math.comb(13, 2) * (1 + 2 * 11),
            "template": math.comb(length, 2) + 15 - length,
            "G_connected_cuts": 2**12 - 1,
            "selected_state_domination": math.comb(13, 3) * 10,
            "family_nonempty": 1,
            "response_existence": math.comb(13, 3) * 10,
            "move_implications": 2 * math.comb(13, 3) * 10 * 3,
            "triangle_to_family": math.comb(13, 3),
        }
        base = sum(category_counts.values())
        if base != expected_base[length]:
            raise AssertionError(("base clause count", length, base))
        branches.append(
            {
                "length": length,
                "variables": (
                    math.comb(13, 2)
                    + math.comb(13, 2) * 11
                    + math.comb(13, 3)
                    + math.comb(13, 3) * 10 * 3
                ),
                "category_counts": category_counts,
                "base_clauses": base,
                "bank_rows": len(bank),
                "bank_row_stream_sha256": sha256(encoded),
                "full_clauses": base + len(bank),
                "raw_labeled_rows": 6 * len(bank),
            }
        )
    if any(branch["variables"] != 9802 for branch in branches):
        raise AssertionError("variable census")
    return {"branches": branches}


# ---------------------------------------------------------------------------
# Complete classification of the two outside-vertex patterns.


def cyclic_distance(length: int, a: int, b: int) -> int:
    delta = (a - b) % length
    return min(delta, length - delta)


def transform_set(
    length: int,
    values: frozenset[int],
    shift: int,
    reflection: int,
) -> frozenset[int]:
    return frozenset((reflection * value + shift) % length for value in values)


def pattern_orbit_key(
    length: int,
    first: frozenset[int],
    second: frozenset[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    images = []
    for reflection in (-1, 1):
        for shift in range(length):
            a = tuple(sorted(transform_set(length, first, shift, reflection)))
            b = tuple(sorted(transform_set(length, second, shift, reflection)))
            images.append((a, b))
            images.append((b, a))
    return min(images)


def classified_pairs(
    length: int,
    required_distance: int = 2,
) -> tuple[
    tuple[frozenset[int], frozenset[int]],
    ...,
]:
    # Once either nonempty side is fixed, the other lies in a two-element
    # distance-two sphere.  Thus any valid side has size at most two.
    candidates = [
        frozenset(values)
        for size in (1, 2)
        for values in itertools.combinations(range(length), size)
    ]
    result = []
    for first in candidates:
        for second in candidates:
            if first & second:
                continue
            if all(
                cyclic_distance(length, a, b) == required_distance
                for a in first
                for b in second
            ):
                result.append((first, second))
    return tuple(result)


def pattern_classification_audit() -> dict[str, object]:
    lengths = list(range(5, 52, 2))
    rows = []
    for length in lengths:
        pairs = classified_pairs(length)
        orbits = {pattern_orbit_key(length, first, second) for first, second in pairs}
        targets = {
            pattern_orbit_key(length, frozenset({0}), frozenset({2})),
            pattern_orbit_key(
                length,
                frozenset({0}),
                frozenset({2, length - 2}),
            ),
        }
        if orbits != targets or len(pairs) != 4 * length:
            raise AssertionError(("pattern classification", length, len(pairs), orbits))
        rows.append(
            {
                "length": length,
                "ordered_pairs": len(pairs),
                "orbits_under_dihedral_times_swap": len(orbits),
            }
        )
    row_stream = json.dumps(rows, separators=(",", ":"), sort_keys=True).encode("ascii")
    return {
        "odd_lengths_checked": {
            "first": lengths[0],
            "last": lengths[-1],
            "step": 2,
            "count": len(lengths),
        },
        "row_count": len(rows),
        "row_stream_sha256": sha256(row_stream),
        "per_length_result": "4*l ordered pairs and exactly 2 D_(2l)-times-swap orbits",
        "all_orders_argument": (
            "Because Y is nonempty, choosing j in Y gives "
            "X subset {j-2,j+2}; symmetrically each side has size at most two. "
            "The written normalization at X containing 0 then exhausts these "
            "two-element spheres for every odd length at least five."
        ),
    }


# ---------------------------------------------------------------------------
# The exact two canonical graphs, all attack trees, and family parameters.


def canonical_h(
    length: int,
    pattern: int,
    *,
    xy_h_edge: bool = False,
    extra_y_misses: frozenset[int] = frozenset(),
) -> Graph:
    if length < 5 or length % 2 == 0 or pattern not in (1, 2):
        raise AssertionError((length, pattern))
    x = length
    y = length + 1
    adjacency = empty_graph(length + 2)
    for rim in range(length):
        add_edge(adjacency, rim, (rim + 1) % length)
    for rim in range(length):
        if rim != 0:
            add_edge(adjacency, x, rim)
    misses = {2}
    if pattern == 2:
        misses.add(length - 2)
    misses.update(value % length for value in extra_y_misses)
    for rim in range(length):
        if rim not in misses:
            add_edge(adjacency, y, rim)
    if xy_h_edge:
        add_edge(adjacency, x, y)
    return tuple(adjacency)


def state_tuple(state: int) -> tuple[int, ...]:
    return vertices(state)


def assert_state(
    graph: Graph,
    values: Sequence[int],
    *,
    is_independent: bool | None = None,
    is_dominating: bool | None = None,
) -> int:
    state = subset_mask(values)
    if is_independent is not None and independent(graph, state) != is_independent:
        raise AssertionError(("independence", values))
    if is_dominating is not None and dominates(graph, state) != is_dominating:
        raise AssertionError(("domination", values))
    return state


def expect_successors(
    graph: Graph,
    state_values: Sequence[int],
    attack: int,
    expected_values: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    state = subset_mask(state_values)
    actual = tuple(state_tuple(value) for value in legal_successors(graph, state, attack))
    expected = tuple(sorted(tuple(sorted(value)) for value in expected_values))
    if actual != expected:
        raise AssertionError(
            {
                "state": tuple(state_values),
                "attack": attack,
                "actual": actual,
                "expected": expected,
            }
        )
    return actual


def small_attack_tree_audit() -> list[dict[str, object]]:
    results = []

    # The genuine l=5, Pattern II exception when xy is an H-edge.
    h_graph = canonical_h(5, 2, xy_h_edge=True)
    g_graph = complement(h_graph)
    x, y = 5, 6
    assert_state(g_graph, (1, 2, x), is_independent=True, is_dominating=True)
    expect_successors(g_graph, (1, 2, x), 4, ())
    results.append(
        {
            "case": "l5_pattern2_xy_H_edge",
            "root": [1, 2, x],
            "attack": 4,
            "dominating_successors": [],
        }
    )

    cases = [
        {
            "case": "l5_pattern1_xy_G_edge",
            "length": 5,
            "pattern": 1,
            "root": (0, 1, 6),
            "first_attack": 3,
            "first_successors": ((1, 3, 6),),
            "leaves": (((1, 3, 6), 2),),
        },
        {
            "case": "l5_pattern2_xy_G_edge",
            "length": 5,
            "pattern": 2,
            "root": (0, 1, 6),
            "first_attack": 3,
            "first_successors": ((1, 3, 6), (0, 1, 3)),
            "leaves": (((1, 3, 6), 2), ((0, 1, 3), 2)),
        },
        {
            "case": "l7_pattern1_xy_G_edge",
            "length": 7,
            "pattern": 1,
            "root": (0, 1, 8),
            "first_attack": 3,
            "first_successors": ((1, 3, 8), (0, 3, 8)),
            "leaves": (((1, 3, 8), 2), ((0, 3, 8), 5)),
        },
        {
            "case": "l7_pattern2_xy_G_edge",
            "length": 7,
            "pattern": 2,
            "root": (1, 2, 7),
            "first_attack": 6,
            "first_successors": ((2, 6, 7), (1, 6, 7)),
            "leaves": (((2, 6, 7), 4), ((1, 6, 7), 0)),
        },
    ]
    for case in cases:
        length = int(case["length"])
        h_graph = canonical_h(length, int(case["pattern"]), xy_h_edge=False)
        g_graph = complement(h_graph)
        root = tuple(case["root"])
        assert_state(g_graph, root, is_independent=True, is_dominating=True)
        first = expect_successors(
            g_graph,
            root,
            int(case["first_attack"]),
            tuple(case["first_successors"]),
        )
        leaves = []
        for state_values, attack in case["leaves"]:
            expect_successors(g_graph, state_values, attack, ())
            leaves.append({"state": list(state_values), "attack": attack, "successors": []})
        results.append(
            {
                "case": case["case"],
                "root": list(root),
                "root_independent_and_dominating": True,
                "first_attack": case["first_attack"],
                "first_dominating_successors": [list(value) for value in first],
                "terminal_attacks": leaves,
            }
        )
    return results


def uniform_attack_audit() -> dict[str, object]:
    checked_lengths = list(range(9, 202, 2))
    transition_count = 0
    for length in checked_lengths:
        x = length
        for pattern in (1, 2):
            g_graph = complement(canonical_h(length, pattern))
            root = (4, 5, x)
            assert_state(g_graph, root, is_independent=True, is_dominating=True)
            expect_successors(
                g_graph,
                root,
                0,
                ((0, 4, x), (0, 5, x)),
            )
            transition_count += 1
            expect_successors(g_graph, (0, 4, x), 2, ())
            transition_count += 1
            for j in range(5, length - 4, 2):
                expect_successors(
                    g_graph,
                    (0, j, x),
                    j + 2,
                    ((0, j + 2, x),),
                )
                transition_count += 1
            expect_successors(g_graph, (0, length - 4, x), length - 2, ())
            transition_count += 1
    return {
        "odd_lengths_checked": {
            "first": checked_lengths[0],
            "last": checked_lengths[-1],
            "step": 2,
            "count": len(checked_lengths),
        },
        "patterns_per_length": 2,
        "named_attack_transitions_checked": transition_count,
        "symbolic_range_audit": {
            "induction_indices": "odd 5 <= j < l-4",
            "largest_induction_source": "l-6",
            "largest_induction_attack": "l-4",
            "terminal_state": "S_(l-4)",
            "terminal_attack": "r_(l-2)",
            "l9_induction": "empty",
            "why_finite_range_is_not_the_proof": (
                "All witnesses use only consecutive rim triples "
                "(j,j+1,j+2) and the four terminal residues "
                "(l-4,l-3,l-2,l-1).  For odd l>=9 the displayed range keeps "
                "these residues distinct from 0 and from x,y; the written "
                "argument therefore applies uniformly, while this range is "
                "only an indexing regression."
            ),
        },
    }


def graph6(graph: Graph, *, wrong_order: bool = False) -> str:
    n = len(graph)
    if not 0 <= n <= 62:
        raise AssertionError("short graph6 only")
    bits = []
    if wrong_order:
        pairs = ((u, v) for u in range(n - 1) for v in range(u + 1, n))
    else:
        pairs = ((u, v) for v in range(1, n) for u in range(v))
    for u, v in pairs:
        bits.append(1 if has_edge(graph, u, v) else 0)
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(n + 63) + "".join(payload)


def family_parameter_audit() -> dict[str, object]:
    static_lengths = list(range(5, 42, 2))
    exact_eternal_lengths = list(range(5, 16, 2))
    static_rows = []
    eternal_rows = []
    for length in static_lengths:
        for pattern in (1, 2):
            h_graph = canonical_h(length, pattern)
            g_graph = complement(h_graph)
            gamma = minimum_domination(g_graph, 3)
            independence = maximum_independence_at_most_four(g_graph)
            independent_domination = independent_domination_at_most_three(g_graph)
            theta = chromatic_number_at_most_four(h_graph)
            pair_condition = all(
                any(
                    x not in (a, b)
                    and has_edge(h_graph, a, x)
                    and has_edge(h_graph, b, x)
                    for x in range(length + 2)
                )
                for a, b in itertools.combinations(range(length + 2), 2)
            )
            if (
                gamma,
                independent_domination,
                independence,
                theta,
                pair_condition,
            ) != (3, 3, 3, 4, True):
                raise AssertionError(
                    (
                        "family static parameters",
                        length,
                        pattern,
                        gamma,
                        independent_domination,
                        independence,
                        theta,
                        pair_condition,
                    )
                )
            static_rows.append(
                {
                    "length": length,
                    "family": pattern,
                    "order": length + 2,
                    "gamma": gamma,
                    "i": independent_domination,
                    "alpha": independence,
                    "theta": theta,
                    "every_H_pair_has_external_common_neighbor": pair_condition,
                }
            )

            if length in exact_eternal_lengths:
                alive3, rounds3 = eternal_fixed_point(g_graph, 3)
                alive4, rounds4 = eternal_fixed_point(g_graph, 4)
                if alive3 or not alive4:
                    raise AssertionError(
                        ("family eternal parameters", length, pattern, len(alive3), len(alive4))
                    )
                eternal_rows.append(
                    {
                        "length": length,
                        "family": pattern,
                        "gamma_infinity": 4,
                        "k3_final_family_size": len(alive3),
                        "k3_deletion_rounds": rounds3,
                        "k4_final_family_size": len(alive4),
                        "k4_deletion_rounds": rounds4,
                    }
                )

    strings = []
    expected = {
        1: "LUzvvz}~r~O?G@",
        2: "LUzvvz}~r~O?GD",
    }
    for pattern in (1, 2):
        value = graph6(complement(canonical_h(11, pattern)))
        if value != expected[pattern]:
            raise AssertionError(("Graph6", pattern, value))
        strings.append({"family": pattern, "length": 11, "Graph6": value})

    static_stream = json.dumps(
        static_rows, separators=(",", ":"), sort_keys=True
    ).encode("ascii")
    return {
        "static_exact_lengths": static_lengths,
        "static_row_count": len(static_rows),
        "static_row_stream_sha256": sha256(static_stream),
        "static_result_each_family": {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "theta": 4,
            "every_H_pair_has_external_common_neighbor": True,
        },
        "greatest_fixed_point_exact_lengths": exact_eternal_lengths,
        "eternal_rows": eternal_rows,
        "Graph6_order13": strings,
        "all_orders_parameter_proof_audit": [
            "pair/common-neighbor check proves gamma at least 3",
            "no K4 and an H-triangle prove alpha exactly 3",
            "a maximum independent triple dominates, proving gamma at most 3 and i=3",
            "the alternating-path argument forbids an H 3-coloring for every odd l>=5",
            "a 3-colored rim plus one shared outsider color proves theta at most 4",
            "Theorem 1 gives gamma-infinity at least 4 and clique cover gives at most 4",
        ],
    }


# ---------------------------------------------------------------------------
# Fail-closed mutations and local-source conflict scan.


def expect_rejection(name: str, action: Callable[[], None]) -> dict[str, object]:
    try:
        action()
    except AssertionError as exc:
        return {"mutation": name, "rejected": True, "reason": str(exc)[:240]}
    raise AssertionError({"mutation_was_not_rejected": name})


def mutation_audit() -> list[dict[str, object]]:
    mutations = []

    def wrong_pair_sign() -> None:
        h_graph = graph_from_edge_mask(4, 0)
        g_graph = complement(h_graph)
        pair = subset_mask((0, 1))
        actual = not dominates(g_graph, pair)
        wrong = any(
            x not in (0, 1)
            and has_edge(g_graph, 0, x)
            and has_edge(g_graph, 1, x)
            for x in range(4)
        )
        if actual != wrong:
            raise AssertionError("G-common-neighbor mutation disagrees")

    mutations.append(expect_rejection("pair_dictionary_uses_G_not_H", wrong_pair_sign))

    def wrong_cut_sign() -> None:
        h_graph = graph_from_edge_mask(5, 0)
        if complement_cut_clauses_hold(h_graph) != connected(h_graph):
            raise AssertionError("cut mutation checks H-connectedness")

    mutations.append(expect_rejection("cut_literal_sign_reversed", wrong_cut_sign))

    def occupied_attack() -> None:
        graph = complement(canonical_h(5, 1))
        legal_successors(graph, subset_mask((0, 1, 6)), 0)

    mutations.append(expect_rejection("occupied_attack_added", occupied_attack))

    def multi_guard_successor() -> None:
        source = subset_mask((0, 1, 2))
        attacked = 4
        mutant = subset_mask((2, 3, 4))
        removed = source & ~mutant
        inserted = mutant & ~source
        if removed.bit_count() != 1 or inserted != 1 << attacked:
            raise AssertionError("successor is not D-u+r for one guard")

    mutations.append(expect_rejection("all_guards_successor", multi_guard_successor))

    def omit_second_pattern() -> None:
        length = 11
        observed = {
            pattern_orbit_key(length, first, second)
            for first, second in classified_pairs(length)
        }
        incomplete = {
            pattern_orbit_key(length, frozenset({0}), frozenset({2}))
        }
        if observed != incomplete:
            raise AssertionError("Pattern II was omitted")

    mutations.append(expect_rejection("omit_pattern_II", omit_second_pattern))

    def wrong_cross_distance() -> None:
        length = 11
        observed = {
            pattern_orbit_key(length, first, second)
            for first, second in classified_pairs(length, required_distance=1)
        }
        targets = {
            pattern_orbit_key(length, frozenset({0}), frozenset({2})),
            pattern_orbit_key(length, frozenset({0}), frozenset({2, 9})),
        }
        if observed != targets:
            raise AssertionError("distance-one mutation changes the orbit set")

    mutations.append(expect_rejection("cross_distance_two_changed_to_one", wrong_cross_distance))

    def remove_small_tree_branch() -> None:
        graph = complement(canonical_h(5, 2))
        actual = legal_successors(graph, subset_mask((0, 1, 6)), 3)
        incomplete = (subset_mask((1, 3, 6)),)
        if actual != incomplete:
            raise AssertionError("second l=5 Pattern-II branch is necessary")

    mutations.append(expect_rejection("drop_l5_patternII_Q_branch", remove_small_tree_branch))

    def uniform_bound_at_seven() -> None:
        graph = complement(canonical_h(7, 1))
        expect_successors(graph, (4, 5, 7), 0, ((0, 4, 7), (0, 5, 7)))

    mutations.append(expect_rejection("uniform_l_at_least_9_changed_to_7", uniform_bound_at_seven))

    def mutate_family_y_miss_zero() -> None:
        h_graph = canonical_h(9, 1, extra_y_misses=frozenset({0}))
        if chromatic_number_at_most_four(h_graph) != 4:
            raise AssertionError("adding y-r0 miss destroys the theta=4 conclusion")

    mutations.append(expect_rejection("family_y_also_misses_r0", mutate_family_y_miss_zero))

    def mutate_family_xy_edge() -> None:
        g_graph = complement(canonical_h(9, 1, xy_h_edge=True))
        if maximum_independence_at_most_four(g_graph) != 3:
            raise AssertionError("xy H-edge creates an independent four-set in G")

    mutations.append(expect_rejection("family_xy_changed_to_H_edge", mutate_family_xy_edge))

    def coloring_count_off_by_one() -> None:
        length = 7
        actual = len(enumerate_coloring_bank(length))
        mutant_expected = ((2**length - 2) * 3 ** (13 - length)) // 6
        if actual != mutant_expected:
            raise AssertionError("outside-vertex exponent must be 12-l, not 13-l")

    mutations.append(expect_rejection("color_bank_exponent_12_minus_l_changed", coloring_count_off_by_one))

    def wrong_graph6_order() -> None:
        graph = complement(canonical_h(11, 1))
        mutant = graph6(graph, wrong_order=True)
        if mutant != "LUzvvz}~r~O?G@":
            raise AssertionError("row-major Graph6 order changes the string")

    mutations.append(expect_rejection("Graph6_bit_order_transposed", wrong_graph6_order))

    if not all(item["rejected"] for item in mutations):
        raise AssertionError("mutation suite did not fail closed")
    return mutations


def local_literature_conflict_scan() -> dict[str, object]:
    needles = (
        "LUzvvz}~r~O?G@",
        "LUzvvz}~r~O?GD",
        "near-spanning odd-hole",
        "near spanning odd hole",
        "hub-free induced cycle",
        "at least three vertices outside",
    )
    sources = []
    total_hits = {needle: 0 for needle in needles}
    for relative in LOCAL_PRIMARY_SOURCES:
        binding = file_binding(relative)
        text = (ROOT / relative).read_text(encoding="utf-8", errors="replace").lower()
        hits = {}
        for needle in needles:
            count = text.count(needle.lower())
            hits[needle] = count
            total_hits[needle] += count
        binding["exact_string_hits"] = hits
        sources.append(binding)
    if any(total_hits.values()):
        raise AssertionError({"unexpected_exact_local_source_match": total_hits})
    return {
        "scope": "only the four locally retained primary-source TeX files",
        "sources": sources,
        "exact_string_hits_across_sources": total_hits,
        "conclusion_boundary": (
            "No exact local match or conflict was found.  This is not a "
            "novelty search and supports no priority or novelty claim."
        ),
    }


def run() -> dict[str, object]:
    frozen_notes = verify_frozen_notes()
    pair_dictionary = pair_common_neighbor_audit()
    cut_sign = cut_sign_audit()
    gadgets = cnf_gadget_truth_tables()
    spgt = spgt_coverage_arithmetic()
    banks = bank_and_census_audit()
    patterns = pattern_classification_audit()
    small_trees = small_attack_tree_audit()
    uniform = uniform_attack_audit()
    families = family_parameter_audit()
    mutations = mutation_audit()
    literature = local_literature_conflict_scan()

    source_data = Path(__file__).read_bytes()
    return {
        "schema": "gamma-theta-order13-k3-math-hostile-audit-v1",
        "schema_version": 1,
        "verdict": "ACCEPT_MATHEMATICS_WITH_NONMATHEMATICAL_WORDING_GAPS",
        "claim_boundary": {
            "accepted": [
                "the abstract four-template CNF semantics and iff theorem, relative to its listed accepted inputs",
                "the reduction to three live templates once the near-spanning-hole theorem is accepted",
                "the near-spanning odd-hole obstruction for every odd l>=5",
                "the order-13 C11 exclusion as a strict corollary",
                "the exact parameter theorem for both infinite canonical families",
            ],
            "not_accepted_here": [
                "novelty or publication priority",
                "the truth of the listed campaign inputs C-014, C-017, C-050, SPGT, or the general parameter chain",
                "any SAT/UNSAT result or certificate",
                "the current mutable production runner",
                "any order-13 exclusion for hole5, hole7, or hole9",
                "the k=4 or k=5 order-13 slices",
            ],
        },
        "frozen_theorem_files": frozen_notes,
        "manual_quantifier_and_sign_audit": {
            "SPGT_cover": (
                "omega(H)=3 reduces odd antiholes to orders 5 and 7; C5 is "
                "an odd hole and accepted C-017 removes the C7 antihole"
            ),
            "hub_free": (
                "accepted C-014 removes a vertex complete in H to the selected "
                "odd-hole rim; no stronger assumption is used"
            ),
            "relabeling": (
                "the rim, a rim edge, one guaranteed external common H-neighbor, "
                "and all remaining vertices are relabeled together; no graph "
                "automorphism or independent anchor is assumed"
            ),
            "one_guard_quantifiers": (
                "for every selected D and every r outside D there exists one "
                "u in D with ur in G and D-u+r selected; multiple true move "
                "variables remain alternative existential witnesses"
            ),
            "complement_signs": (
                "e=1 means H-edge; domination, guard movement, and G-cut "
                "crossing therefore use negative e literals"
            ),
            "family_exactness": (
                "the all-orders proof gives gamma=i=alpha=3 and "
                "gamma-infinity=theta=4; finite checks are regression only"
            ),
        },
        "pair_common_neighbor_dictionary": pair_dictionary,
        "connected_cut_complement_sign": cut_sign,
        "CNF_local_truth_tables": gadgets,
        "SPGT_and_order_arithmetic": spgt,
        "coloring_banks_and_clause_census": banks,
        "two_outside_vertex_pattern_classification": patterns,
        "small_attack_trees": small_trees,
        "uniform_attack": uniform,
        "canonical_family_parameters": families,
        "fail_closed_mutations": mutations,
        "local_primary_source_conflict_scan": literature,
        "wording_gaps": [
            {
                "severity": "documentation-only",
                "file": "math/lemmas/order13_k3_synthesis_target.md",
                "lines": "729-732",
                "issue": (
                    "The heading 'No implementation theorem yet' is stale: "
                    "a separately frozen A/B constructor acceptance now exists. "
                    "The sentence does not enter any mathematical inference."
                ),
            },
            {
                "severity": "documentation-only",
                "file": "math/lemmas/order13_k3_hole11_exclusion.md",
                "lines": "503-505",
                "issue": (
                    "The statement that two exact evaluators reproduced the "
                    "order-13 parameters gives no artifact paths or hashes in "
                    "this note.  Theorem 4 is nevertheless proved without that "
                    "regression statement, and this audit independently "
                    "reproduces it."
                ),
            },
            {
                "severity": "status-only",
                "file": "both notes",
                "lines": "synthesis 14-16; hole note 11-14",
                "issue": (
                    "Both pre-audit status paragraphs still say the companion "
                    "proof should receive adversarial review.  This artifact "
                    "supplies that review for the frozen bytes."
                ),
            },
        ],
        "source": {
            "path": "reviews/order13_k3_math_hostile/audit.py",
            "bytes": len(source_data),
            "sha256": sha256(source_data),
            "runtime_dependencies": "Python standard library only",
            "campaign_modules_imported": [],
        },
    }


def main() -> int:
    print(json.dumps(run(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
