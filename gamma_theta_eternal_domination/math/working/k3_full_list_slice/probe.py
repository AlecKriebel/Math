#!/usr/bin/env python3
"""Independent bounded falsifier for the k=3 full-response-list slice.

This program deliberately imports no campaign evaluator.  It uses:

* ordinary Python integer bitsets for graph predicates;
* a literal greatest-fixed-point implementation of the one-guard game;
* the pinned nauty ``geng`` only as an unlabeled graph source; and
* direct ordinary-set checks for the displayed proper-family controls.

The exhaustive graph scan asks a sharply bounded two-stage question:

    Does a connected graph through ``--max-order`` with gamma=alpha=3
    admit an independent triple S and a vertex x whose *static* response
    list at S is all of S, and, if so, does that list remain full in the
    greatest eternal three-family?

Family-response lists are subsets of static lists.  Hence a zero answer
at the greatest-family stage also covers every eternal family, including
every proper subfamily.  This is not a counterexample exclusion and not a
proof for unbounded order.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import resource
import subprocess
import time
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[2]
DEFAULT_GENG = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
DEFAULT_LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"
DEFAULT_OUTPUT = HERE / "probe_result.json"
DEFAULT_LOG = HERE / "RESEARCH_LOG.md"


def decode_graph6(record: str) -> tuple[int, ...]:
    """Decode canonical short graph6 into open-neighborhood bitsets."""

    raw = record.strip().encode("ascii")
    if not raw or not 63 <= raw[0] <= 125:
        raise ValueError(f"unsupported graph6 header: {record!r}")
    order = raw[0] - 63
    if order > 62:
        raise ValueError("bounded probe accepts short graph6 only")
    bit_count = order * (order - 1) // 2
    payload_length = (bit_count + 5) // 6
    if len(raw) != payload_length + 1:
        raise ValueError(f"noncanonical graph6 payload: {record!r}")
    bits: list[int] = []
    for byte in raw[1:]:
        six = byte - 63
        bits.extend((six >> shift) & 1 for shift in range(5, -1, -1))
    if any(bits[bit_count:]):
        raise ValueError(f"nonzero graph6 padding: {record!r}")
    adjacency = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def vertices(mask: int) -> Iterable[int]:
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def subset_mask(group: Iterable[int]) -> int:
    answer = 0
    for vertex in group:
        answer |= 1 << vertex
    return answer


def closed_masks(graph: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(row | (1 << vertex) for vertex, row in enumerate(graph))


def dominates(closed: tuple[int, ...], state: int, all_vertices: int) -> bool:
    covered = 0
    for vertex in vertices(state):
        covered |= closed[vertex]
    return covered == all_vertices


def independent(graph: tuple[int, ...], state: int) -> bool:
    return all(not (graph[vertex] & state) for vertex in vertices(state))


def masks_of_size(order: int, size: int) -> Iterable[int]:
    for group in itertools.combinations(range(order), size):
        yield subset_mask(group)


def alpha_at_most_three(graph: tuple[int, ...]) -> bool:
    order = len(graph)
    return not any(independent(graph, state) for state in masks_of_size(order, 4))


def gamma_at_least_three(
    closed: tuple[int, ...], all_vertices: int
) -> bool:
    order = len(closed)
    return not any(
        closed[first] | closed[second] == all_vertices
        for first in range(order)
        for second in range(first + 1, order)
    ) and not any(row == all_vertices for row in closed)


def static_full_pairs(
    graph: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    """Return (independent-triple mask, full target) pairs."""

    order = len(graph)
    all_vertices = (1 << order) - 1
    closed = closed_masks(graph)
    answer: list[tuple[int, int]] = []
    for state in masks_of_size(order, 3):
        if not independent(graph, state):
            continue
        anchors = tuple(vertices(state))
        for target in range(order):
            if state & (1 << target):
                continue
            if graph[target] & state != state:
                continue
            if all(
                dominates(
                    closed,
                    (state & ~(1 << guard)) | (1 << target),
                    all_vertices,
                )
                for guard in anchors
            ):
                answer.append((state, target))
    return tuple(answer)


def greatest_family(graph: tuple[int, ...], size: int) -> frozenset[int]:
    """Literal greatest fixed point in the one-guard-moves model."""

    order = len(graph)
    all_vertices = (1 << order) - 1
    closed = closed_masks(graph)
    family = frozenset(
        state
        for state in masks_of_size(order, size)
        if dominates(closed, state, all_vertices)
    )
    while True:
        retained: set[int] = set()
        for state in family:
            valid = True
            for attack in vertices(all_vertices & ~state):
                if not any(
                    ((state & ~(1 << guard)) | (1 << attack)) in family
                    for guard in vertices(state & graph[attack])
                ):
                    valid = False
                    break
            if valid:
                retained.add(state)
        next_family = frozenset(retained)
        if next_family == family:
            return family
        family = next_family


def family_response_list(
    graph: tuple[int, ...],
    family: frozenset[int],
    state: int,
    target: int,
) -> tuple[int, ...]:
    return tuple(
        guard
        for guard in vertices(state & graph[target])
        if ((state & ~(1 << guard)) | (1 << target)) in family
    )


def literal_family_check(
    graph: tuple[int, ...], family: frozenset[int]
) -> dict[str, object]:
    order = len(graph)
    all_vertices = (1 << order) - 1
    closed = closed_masks(graph)
    obligations = 0
    for state in family:
        if not dominates(closed, state, all_vertices):
            raise AssertionError(f"nondominating state {state}")
        for attack in vertices(all_vertices & ~state):
            obligations += 1
            successors = [
                (guard, (state & ~(1 << guard)) | (1 << attack))
                for guard in vertices(state & graph[attack])
                if ((state & ~(1 << guard)) | (1 << attack)) in family
            ]
            if not successors:
                raise AssertionError(
                    f"unanswered attack state={state} attack={attack}"
                )
    return {"states": len(family), "attack_obligations": obligations}


def graph_parameters(graph: tuple[int, ...]) -> dict[str, int]:
    order = len(graph)
    all_vertices = (1 << order) - 1
    closed = closed_masks(graph)
    gamma = next(
        size
        for size in range(1, order + 1)
        if any(
            dominates(closed, state, all_vertices)
            for state in masks_of_size(order, size)
        )
    )
    alpha = next(
        size
        for size in range(order, 0, -1)
        if any(independent(graph, state) for state in masks_of_size(order, size))
    )
    eternal = next(
        size
        for size in range(1, order + 1)
        if greatest_family(graph, size)
    )
    return {"gamma": gamma, "alpha": alpha, "gamma_infinity": eternal}


def stream_scan(geng: Path, maximum_order: int) -> dict[str, object]:
    order_rows: list[dict[str, object]] = []
    first_static: dict[str, object] | None = None
    first_equality_static: dict[str, object] | None = None
    first_family: dict[str, object] | None = None

    for order in range(1, maximum_order + 1):
        process = subprocess.Popen(
            (str(geng), "-cq", str(order)),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert process.stdout is not None
        stream_hash = hashlib.sha256()
        connected = 0
        raw_static_pairs = 0
        gamma_alpha_graphs = 0
        gamma_alpha_pairs = 0
        eternal_graphs_among_candidates = 0
        equality_static_pairs_in_eternal_graphs = 0
        equality_static_pair_family_list_size_histogram = {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
        }
        family_full_pairs = 0

        for line in process.stdout:
            record = line.strip()
            if not record:
                continue
            connected += 1
            stream_hash.update(record.encode("ascii") + b"\n")
            graph = decode_graph6(record)
            pairs = static_full_pairs(graph)
            raw_static_pairs += len(pairs)
            if not pairs:
                continue
            all_vertices = (1 << order) - 1
            closed = closed_masks(graph)
            if not alpha_at_most_three(graph):
                continue
            if not gamma_at_least_three(closed, all_vertices):
                continue
            # The displayed independent triple proves alpha >= 3 and,
            # under alpha <= 3, dominates.  The pair test proves gamma >= 3.
            gamma_alpha_graphs += 1
            gamma_alpha_pairs += len(pairs)
            if first_static is None:
                state, target = pairs[0]
                first_static = {
                    "graph6": record,
                    "order": order,
                    "reference": list(vertices(state)),
                    "target": target,
                }
            family = greatest_family(graph, 3)
            if not family:
                continue
            eternal_graphs_among_candidates += 1
            equality_static_pairs_in_eternal_graphs += len(pairs)
            if first_equality_static is None:
                first_equality_static = {
                    "graph6": record,
                    "order": order,
                    "greatest_family_size": len(family),
                    "static_full_pairs": [
                        {
                            "reference": list(vertices(state)),
                            "target": target,
                            "greatest_family_response_list": list(
                                family_response_list(
                                    graph, family, state, target
                                )
                            ),
                        }
                        for state, target in pairs
                    ],
                }
            for state, target in pairs:
                family_list = family_response_list(graph, family, state, target)
                equality_static_pair_family_list_size_histogram[
                    str(len(family_list))
                ] += 1
                if family_list == tuple(vertices(state)):
                    family_full_pairs += 1
                    if first_family is None:
                        first_family = {
                            "graph6": record,
                            "order": order,
                            "reference": list(vertices(state)),
                            "target": target,
                            "greatest_family_size": len(family),
                        }

        stderr = process.stderr.read() if process.stderr is not None else ""
        return_code = process.wait()
        if return_code:
            raise RuntimeError(
                f"geng failed at order {order}: return={return_code}, {stderr!r}"
            )
        if stderr:
            raise RuntimeError(f"unexpected geng stderr at order {order}: {stderr!r}")
        order_rows.append(
            {
                "order": order,
                "connected_graphs": connected,
                "graph6_stream_sha256": stream_hash.hexdigest(),
                "raw_static_full_pairs": raw_static_pairs,
                "gamma_alpha_three_graphs_with_static_full_pair": gamma_alpha_graphs,
                "gamma_alpha_three_static_full_pairs": gamma_alpha_pairs,
                "eternal_three_graphs_among_those_candidates": (
                    eternal_graphs_among_candidates
                ),
                "equality_static_pairs_in_eternal_graphs": (
                    equality_static_pairs_in_eternal_graphs
                ),
                "equality_static_pair_family_list_size_histogram": (
                    equality_static_pair_family_list_size_histogram
                ),
                "greatest_family_full_pairs": family_full_pairs,
                "complete": True,
            }
        )

    return {
        "orders": order_rows,
        "totals": {
            key: sum(int(row[key]) for row in order_rows)
            for key in (
                "connected_graphs",
                "raw_static_full_pairs",
                "gamma_alpha_three_graphs_with_static_full_pair",
                "gamma_alpha_three_static_full_pairs",
                "eternal_three_graphs_among_those_candidates",
                "equality_static_pairs_in_eternal_graphs",
                "greatest_family_full_pairs",
            )
        },
        "equality_static_pair_family_list_size_histogram": {
            str(size): sum(
                int(row["equality_static_pair_family_list_size_histogram"][str(size)])
                for row in order_rows
            )
            for size in range(4)
        },
        "first_gamma_alpha_three_static_full_pair": first_static,
        "first_eternal_equality_static_full_pair": first_equality_static,
        "first_equality_family_full_pair": first_family,
    }


def proper_family_control() -> dict[str, object]:
    """Verify a proper FDzro family whose displayed reference has full lists."""

    graph = decode_graph6("FDzro")
    triples = (
        (0, 1, 2),
        (0, 1, 4),
        (0, 2, 4),
        (0, 2, 6),
        (0, 4, 6),
        (1, 2, 3),
        (1, 2, 4),
        (1, 2, 5),
        (1, 3, 4),
        (1, 4, 5),
        (2, 3, 4),
        (2, 3, 6),
        (2, 4, 5),
        (2, 4, 6),
        (2, 5, 6),
        (3, 4, 6),
        (4, 5, 6),
    )
    family = frozenset(subset_mask(state) for state in triples)
    greatest = greatest_family(graph, 3)
    check = literal_family_check(graph, family)
    reference = subset_mask((0, 1, 2))
    lists = {
        str(target): list(family_response_list(graph, family, reference, target))
        for target in range(3, 7)
    }
    return {
        "graph6": "FDzro",
        "parameters": graph_parameters(graph),
        "proper_family": check,
        "greatest_family_size": len(greatest),
        "strict_proper_subfamily": family < greatest,
        "reference": [0, 1, 2],
        "family_response_lists": lists,
        "full_targets": [
            target
            for target in range(3, 7)
            if tuple(lists[str(target)]) == (0, 1, 2)
        ],
        "states": [list(state) for state in triples],
        "scope": (
            "REFUTED CONTROL ONLY: full lists occur in a proper eternal "
            "family after dropping gamma=3; this graph has gamma=2."
        ),
    }


def equality_static_control() -> dict[str, object]:
    """Separate static fullness from family fullness in an equality graph."""

    graph = decode_graph6("HCQebjw")
    family = greatest_family(graph, 3)
    reference = subset_mask((0, 1, 2))
    target = 8
    closed = closed_masks(graph)
    all_vertices = (1 << len(graph)) - 1
    static_swaps = {
        str(guard): dominates(
            closed,
            (reference & ~(1 << guard)) | (1 << target),
            all_vertices,
        )
        for guard in vertices(reference)
    }
    family_list = list(
        family_response_list(graph, family, reference, target)
    )
    link = [
        vertex
        for vertex in range(len(graph))
        if vertex != target and not (graph[target] & (1 << vertex))
    ]
    parts = ((0, 3, 6), (1, 4, 8), (2, 5, 7))
    if not all(
        all(graph[first] & (1 << second) for first, second in itertools.combinations(part, 2))
        for part in parts
    ):
        raise AssertionError("displayed HCQebjw clique partition failed")
    spokes: dict[str, object] = {}
    for anchor in vertices(reference):
        spoke = [
            vertex
            for vertex in link
            if not (graph[anchor] & (1 << vertex))
        ]
        spokes[str(anchor)] = {
            "vertices": spoke,
            "states_in_greatest_family": {
                str(vertex): (
                    subset_mask((target, anchor, vertex)) in family
                )
                for vertex in spoke
            },
        }
    return {
        "graph6": "HCQebjw",
        "parameters": graph_parameters(graph),
        "greatest_family_size": len(family),
        "reference": [0, 1, 2],
        "target": target,
        "all_three_static_swaps_dominate": static_swaps,
        "greatest_family_response_list": family_list,
        "target_link_in_H": {
            "vertices": link,
            "edges": [
                [first, second]
                for first, second in itertools.combinations(link, 2)
                if not (graph[first] & (1 << second))
            ],
        },
        "anchor_spokes": spokes,
        "checked_three_clique_partition": [list(part) for part in parts],
        "status": (
            "REFUTED: even gamma=alpha=gamma_infinity=3 and static fullness "
            "do not force family fullness. The greatest family retains only "
            "guard 1 as a response to target 8."
        ),
    }


def equality_family_full_control() -> dict[str, object]:
    """Verify the order-12 equality graph with a genuine full family list."""

    labeled_graph6 = "Ksv`f\\knJVis"
    expected_canonical_graph6 = "K{eYptMJynEn"
    canonical_process = subprocess.run(
        (str(DEFAULT_LABELG), "-q"),
        input=labeled_graph6 + "\n",
        text=True,
        capture_output=True,
        check=True,
    )
    canonical_graph6 = canonical_process.stdout.strip()
    if canonical_process.stderr or canonical_graph6 != expected_canonical_graph6:
        raise AssertionError(
            "pinned labelg canonicalization mismatch: "
            f"stdout={canonical_graph6!r}, stderr={canonical_process.stderr!r}"
        )
    graph = decode_graph6(labeled_graph6)
    family = greatest_family(graph, 3)
    family_check = literal_family_check(graph, family)
    reference_tuple = (1, 2, 3)
    reference = subset_mask(reference_tuple)
    target = 0
    response_lists = {
        str(vertex): list(
            family_response_list(graph, family, reference, vertex)
        )
        for vertex in range(len(graph))
        if not (reference & (1 << vertex))
    }
    full_targets = [
        vertex
        for vertex in range(len(graph))
        if not (reference & (1 << vertex))
        and tuple(response_lists[str(vertex)]) == reference_tuple
    ]

    compatible_colorings: list[dict[int, int]] = []
    outside = [
        vertex
        for vertex in range(len(graph))
        if not (reference & (1 << vertex))
    ]
    for values in itertools.product(
        *(response_lists[str(vertex)] for vertex in outside)
    ):
        coloring = dict(zip(reference_tuple, reference_tuple))
        coloring.update(dict(zip(outside, values)))
        if all(
            coloring[first] != coloring[second]
            for first, second in itertools.combinations(range(len(graph)), 2)
            if not (graph[first] & (1 << second))
        ):
            compatible_colorings.append(coloring)

    partition = ((1, 5, 8, 11), (2, 6, 7, 10), (0, 3, 4, 9))
    if not all(
        all(
            graph[first] & (1 << second)
            for first, second in itertools.combinations(part, 2)
        )
        for part in partition
    ):
        raise AssertionError("displayed order-12 clique partition failed")

    link = [
        vertex
        for vertex in range(len(graph))
        if vertex != target and not (graph[target] & (1 << vertex))
    ]
    spokes: dict[str, object] = {}
    for anchor in reference_tuple:
        spoke = [
            vertex
            for vertex in link
            if not (graph[anchor] & (1 << vertex))
        ]
        spoke_rows: list[dict[str, object]] = []
        for spoke_vertex in spoke:
            witnesses = [
                vertex
                for vertex in range(len(graph))
                if vertex not in (anchor, spoke_vertex)
                and not (graph[anchor] & (1 << vertex))
                and not (graph[spoke_vertex] & (1 << vertex))
            ]
            spoke_rows.append(
                {
                    "vertex": spoke_vertex,
                    "forced_spoke_state_in_family": (
                        subset_mask((target, anchor, spoke_vertex)) in family
                    ),
                    "external_witness_clique": witnesses,
                    "all_witnesses_adjacent_to_full_target": all(
                        graph[target] & (1 << witness)
                        for witness in witnesses
                    ),
                    "all_independent_witness_states_in_family": all(
                        subset_mask((anchor, spoke_vertex, witness)) in family
                        for witness in witnesses
                    ),
                }
            )
        spokes[str(anchor)] = spoke_rows

    return {
        "labeled_graph6": labeled_graph6,
        "canonical_graph6": canonical_graph6,
        "canonical_graph6_checked_by_pinned_labelg": True,
        "parameters": graph_parameters(graph),
        "dominating_triples": sum(
            1
            for state in masks_of_size(len(graph), 3)
            if dominates(
                closed_masks(graph),
                state,
                (1 << len(graph)) - 1,
            )
        ),
        "greatest_family": family_check,
        "greatest_family_equals_all_dominating_triples": (
            family_check["states"]
            == sum(
                1
                for state in masks_of_size(len(graph), 3)
                if dominates(
                    closed_masks(graph),
                    state,
                    (1 << len(graph)) - 1,
                )
            )
        ),
        "reference": list(reference_tuple),
        "family_response_lists": response_lists,
        "full_targets": full_targets,
        "compatible_anchored_coloring_count": len(compatible_colorings),
        "compatible_full_target_color_histogram": {
            str(color): sum(
                coloring[target] == color
                for coloring in compatible_colorings
            )
            for color in reference_tuple
        },
        "compatible_colorings": [
            {str(vertex): coloring[vertex] for vertex in range(len(graph))}
            for coloring in compatible_colorings
        ],
        "checked_three_clique_partition": [list(part) for part in partition],
        "target_link_in_H": {
            "vertices": link,
            "edges": [
                [first, second]
                for first, second in itertools.combinations(link, 2)
                if not (graph[first] & (1 << second))
            ],
        },
        "anchor_spokes_and_witnesses": spokes,
        "status": (
            "POSITIVE EQUALITY CONTROL: genuine full family lists do occur. "
            "This graph has theta=3 via the checked partition and a unique "
            "family-compatible anchored coloring, with target 0 colored 3."
        ),
    }


def abstract_full_column_control() -> dict[str, object]:
    """Check a rank-three exchange system with a full first target column."""

    states = frozenset(
        {
            (0, 0),
            (1, 1),
            (1, 2),
            (2, 1),
            (2, 4),
            (3, 3),
            (3, 5),
            (3, 6),
            (4, 1),
            (5, 5),
            (6, 3),
            (7, 7),
        }
    )

    def axioms_hold() -> bool:
        for removed, inserted in states:
            for target in range(3):
                if inserted & (1 << target):
                    continue
                if not any(
                    not (removed & (1 << source))
                    and (
                        removed | (1 << source),
                        inserted | (1 << target),
                    )
                    in states
                    for source in range(3)
                ):
                    return False
            for source in range(3):
                if not (removed & (1 << source)):
                    continue
                if not any(
                    inserted & (1 << target)
                    and (
                        removed & ~(1 << source),
                        inserted & ~(1 << target),
                    )
                    in states
                    for target in range(3)
                ):
                    return False
        return True

    base_orderings: list[list[int]] = []
    for permutation in itertools.permutations(range(3)):
        if all(
            (
                removed,
                sum(
                    1 << permutation[source]
                    for source in range(3)
                    if removed & (1 << source)
                ),
            )
            in states
            for removed in range(8)
        ):
            base_orderings.append(list(permutation))
    return {
        "rank": 3,
        "states": [list(pair) for pair in sorted(states)],
        "exchange_axioms_hold": axioms_hold(),
        "first_target_column_full": all((1 << source, 1) in states for source in range(3)),
        "base_orderings": base_orderings,
        "status": (
            "REFUTED: a full first-level response column does not force "
            "base-orderability of the abstract exchange system."
        ),
    }


def marked_link_control() -> dict[str, object]:
    """Check the smallest bipartite marked-link obstruction."""

    # Link K_1,3: center 0 and leaves 1,2,3.  Leaf j is adjacent in H
    # to anchor color j-1; the center has no anchor mark.
    link_edges = {(0, 1), (0, 2), (0, 3)}
    marks = {1: 0, 2: 1, 3: 2}
    extensions: dict[str, list[dict[str, int]]] = {}
    for x_color in range(3):
        remaining = tuple(color for color in range(3) if color != x_color)
        valid: list[dict[str, int]] = []
        for flip in (0, 1):
            coloring = {
                vertex: remaining[(0 if vertex == 0 else 1) ^ flip]
                for vertex in range(4)
            }
            if all(coloring[vertex] != mark for vertex, mark in marks.items()):
                valid.append({str(vertex): color for vertex, color in coloring.items()})
        extensions[str(x_color)] = valid

    # Eight-vertex graph realizing exactly this local H pattern:
    # S=012, x=3, link center=4, marked leaves=5,6,7.
    h_edges = {
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (4, 5),
        (4, 6),
        (4, 7),
        (0, 5),
        (1, 6),
        (2, 7),
    }
    graph_rows = [0] * 8
    for first, second in itertools.combinations(range(8), 2):
        if (first, second) not in h_edges:
            graph_rows[first] |= 1 << second
            graph_rows[second] |= 1 << first
    graph = tuple(graph_rows)
    return {
        "link": {
            "vertices": [0, 1, 2, 3],
            "edges": [list(edge) for edge in sorted(link_edges)],
            "anchor_marks": {str(vertex): mark for vertex, mark in marks.items()},
            "extensions_by_full_vertex_color": extensions,
        },
        "realizing_graph": {
            "order": 8,
            "parameters": graph_parameters(graph),
            "greatest_eternal_three_family_size": len(greatest_family(graph, 3)),
            "dominating_pairs": [
                [first, second]
                for first, second in itertools.combinations(range(8), 2)
                if dominates(
                    closed_masks(graph),
                    (1 << first) | (1 << second),
                    (1 << 8) - 1,
                )
            ],
        },
        "status": (
            "REFUTED ABSTRACT/LOW-GAMMA CONTROL: bipartite link geometry and "
            "one anchor mark per link vertex do not alone guarantee a local "
            "anchored extension. The realizing graph has gamma=2 and no "
            "eternal three-family, so the equality-specific statement stays open."
        ),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, default=9)
    parser.add_argument("--geng", type=Path, default=DEFAULT_GENG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1 <= args.max_order <= 9:
        raise SystemExit("this laptop-bounded probe requires 1 <= max-order <= 9")
    started = time.monotonic()
    scan = stream_scan(args.geng.resolve(), args.max_order)
    payload: dict[str, object] = {
        "schema": "k3-full-list-slice-probe-v1",
        "status": "COMPLETE",
        "scope": {
            "orders": [1, args.max_order],
            "connected_unlabeled_graphs": True,
            "graph_source": str(args.geng.resolve()),
            "search_predicate": (
                "gamma=alpha=3 with an independent reference triple having "
                "a static full-response target, followed by exact greatest-"
                "eternal-family testing of every surviving candidate"
            ),
            "family_quantifier_note": (
                "Any proper-family response list is contained in the "
                "greatest-family response list, which is contained in the "
                "static list. Therefore the zero greatest-family-full count "
                "through the stated order covers arbitrary proper eternal "
                "families there."
            ),
            "order14_used": False,
        },
        "scan": scan,
        "controls": {
            "proper_eternal_family_full_list": proper_family_control(),
            "equality_static_but_not_family_full": equality_static_control(),
            "equality_genuine_family_full": equality_family_full_control(),
            "abstract_full_column": abstract_full_column_control(),
            "marked_bipartite_link": marked_link_control(),
        },
        "claim_boundary": {
            "PROVED_BY_WRITTEN_ARGUMENT": [
                "family-response lists are subsets of static response lists",
                "family-response lists in any subfamily are subsets of the greatest-family lists",
            ],
            "CERTIFIED_FINITE": [
                (
                    "the pinned connected-unlabeled graph stream was exhausted "
                    f"through order {args.max_order} for the stated static predicate"
                ),
                "the displayed FDzro proper family passes every literal obligation",
                "the displayed abstract exchange system passes both exchange axioms and has no base ordering",
            ],
            "OPEN": [
                "whether every equality graph with a full family-response list has a compatible anchored coloring",
                "whether an inclusion-minimal eternal family can always avoid full lists",
                "whether the full-list link geometry plus gamma=3 and full closure forces an anchored extension",
            ],
            "universal_conjecture_resolved": False,
            "finite_counterexample_frontier_raised": False,
        },
        "source": {
            "script": str(Path(__file__).resolve().relative_to(CAMPAIGN)),
            "script_sha256_before_result_write": sha256(Path(__file__).resolve()),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "geng_sha256": sha256(args.geng.resolve()),
            "labelg_sha256": sha256(DEFAULT_LABELG),
        },
    }
    write_json(args.output.resolve(), payload)
    elapsed = time.monotonic() - started
    maximum_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if platform.system() != "Darwin":
        maximum_rss *= 1024
    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.log.write_text(
        "# Full-list-slice probe execution log\n\n"
        f"- status: COMPLETE\n"
        f"- maximum order: {args.max_order}\n"
        f"- connected graphs: {scan['totals']['connected_graphs']}\n"
        f"- elapsed seconds: {elapsed:.6f}\n"
        f"- maximum resident bytes: {maximum_rss}\n"
        f"- result: `{args.output.resolve()}`\n",
        encoding="utf-8",
    )
    print(json.dumps(scan["totals"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
