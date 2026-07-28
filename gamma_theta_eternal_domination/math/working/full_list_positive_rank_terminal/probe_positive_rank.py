#!/usr/bin/env python3
"""Exploratory audit of positive-rank C-149 terminal entries.

This is deliberately independent of the campaign search core.  It uses
ordinary integer bit masks and reconstructs the greatest kernels directly
from the one-guard definition.
"""

from __future__ import annotations

import argparse
import csv
from itertools import combinations
import json
from pathlib import Path
import random


CONTROLS = (
    (r"Ksv`f\knJVis", (1, 2, 3), 0),
    ("OQifur}UO]}iTij]tpo}v", (0, 1, 10), 6),
)


def decode_graph6(record: str) -> tuple[int, ...]:
    values = [ord(character) - 63 for character in record]
    order = values[0]
    bits: list[int] = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    rows = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            cursor += 1
    return tuple(rows)


def vertices(mask: int) -> tuple[int, ...]:
    answer = []
    while mask:
        bit = mask & -mask
        answer.append(bit.bit_length() - 1)
        mask ^= bit
    return tuple(answer)


def masks_of_size(order: int, size: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << vertex for vertex in state)
        for state in combinations(range(order), size)
    )


def dominates(rows: tuple[int, ...], state: int) -> bool:
    covered = state
    for guard in vertices(state):
        covered |= rows[guard]
    return covered == (1 << len(rows)) - 1


def greatest_kernel(
    rows: tuple[int, ...],
    size: int,
    banned: frozenset[int] = frozenset(),
) -> tuple[frozenset[int], dict[int, int]]:
    active = {
        state
        for state in masks_of_size(len(rows), size)
        if state not in banned and dominates(rows, state)
    }
    ranks: dict[int, int] = {}
    round_number = 0
    while True:
        doomed = []
        for state in sorted(active):
            for attacked in range(len(rows)):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                if not any(
                    state ^ (1 << guard) ^ attacked_bit in active
                    for guard in vertices(state & rows[attacked])
                ):
                    doomed.append(state)
                    break
        if not doomed:
            return frozenset(active), ranks
        for state in doomed:
            ranks[state] = round_number
        active.difference_update(doomed)
        round_number += 1


def complement_neighbors(rows: tuple[int, ...], target: int) -> int:
    return ((1 << len(rows)) - 1) & ~(rows[target] | (1 << target))


def response_list(
    rows: tuple[int, ...],
    family: frozenset[int],
    root: int,
    target: int,
) -> tuple[int, ...]:
    return tuple(
        color
        for color in vertices(root)
        if rows[color] & (1 << target)
        and root ^ (1 << color) ^ (1 << target) in family
    )


def audit_control(
    graph6: str,
    root_vertices: tuple[int, int, int],
    target: int,
) -> list[dict[str, object]]:
    rows = decode_graph6(graph6)
    root = sum(1 << vertex for vertex in root_vertices)
    greatest = greatest_kernel(rows, 3)[0]
    if response_list(rows, greatest, root, target) != root_vertices:
        raise AssertionError("target is not full at the named root")
    records = []
    for color in root_vertices:
        base = root ^ (1 << color)
        link = complement_neighbors(rows, target)
        banned = frozenset(
            base | (1 << vertex) for vertex in vertices(link)
        )
        kernel, ranks = greatest_kernel(rows, 3, banned)
        if kernel:
            continue
        for predecessor in sorted(greatest - banned):
            height = ranks[predecessor]
            for attacked in range(len(rows)):
                attacked_bit = 1 << attacked
                if predecessor & attacked_bit:
                    continue
                allowed_dominating = []
                for guard in vertices(predecessor & rows[attacked]):
                    successor = predecessor ^ (1 << guard) ^ attacked_bit
                    if successor in banned or not dominates(rows, successor):
                        continue
                    allowed_dominating.append(successor)
                if not all(
                    successor in ranks and ranks[successor] < height
                    for successor in allowed_dominating
                ):
                    continue
                for mover in vertices(predecessor & rows[attacked]):
                    successor = predecessor ^ (1 << mover) ^ attacked_bit
                    if successor not in greatest & banned:
                        continue
                    terminal_vertex_mask = successor & ~base
                    if terminal_vertex_mask.bit_count() != 1:
                        continue
                    terminal_vertex = terminal_vertex_mask.bit_length() - 1
                    palette = response_list(
                        rows, greatest, root, terminal_vertex
                    )
                    if len(palette) < 2:
                        continue
                    if attacked == terminal_vertex:
                        gate = (
                            "direct_root"
                            if predecessor == root and mover == color
                            else "nonroot_corridor"
                        )
                        alternates = []
                        for secondary in palette:
                            if secondary == color:
                                continue
                            alternate = (
                                predecessor
                                ^ (1 << secondary)
                                ^ (1 << terminal_vertex)
                            )
                            alternates.append(
                                {
                                    "guard": secondary,
                                    "state": vertices(alternate),
                                    "dominates": dominates(rows, alternate),
                                    "rank": ranks.get(alternate),
                                    "retained": alternate in greatest,
                                    "banned": alternate in banned,
                                }
                            )
                    elif base & attacked_bit:
                        gate = "anchor_restoration"
                        alternates = []
                        if rows[terminal_vertex] & attacked_bit:
                            alternate = (
                                predecessor
                                ^ (1 << terminal_vertex)
                                ^ attacked_bit
                            )
                            alternates.append(
                                {
                                    "guard": terminal_vertex,
                                    "state": vertices(alternate),
                                    "dominates": dominates(rows, alternate),
                                    "rank": ranks.get(alternate),
                                    "retained": alternate in greatest,
                                    "banned": alternate in banned,
                                }
                            )
                    else:
                        continue
                    records.append(
                        {
                            "graph6": graph6,
                            "root": root_vertices,
                            "target": target,
                            "color": color,
                            "predecessor": vertices(predecessor),
                            "rank": height,
                            "attack": attacked,
                            "mover": mover,
                            "terminal": vertices(successor),
                            "terminal_vertex": terminal_vertex,
                            "palette": palette,
                            "attacked_anchor_in_palette": (
                                attacked in palette
                                if gate == "anchor_restoration"
                                else None
                            ),
                            "gate": gate,
                            "predecessor_induced_edges": tuple(
                                (first, second)
                                for first, second in combinations(
                                    vertices(predecessor), 2
                                )
                                if rows[first] & (1 << second)
                            ),
                            "alternates": alternates,
                        }
                    )
    return records


def has_dominating_pair(rows: tuple[int, ...]) -> bool:
    return any(
        dominates(rows, (1 << first) | (1 << second))
        for first, second in combinations(range(len(rows)), 2)
    )


def independent(rows: tuple[int, ...], state: int) -> bool:
    return all(
        not rows[first] & (1 << second)
        for first, second in combinations(vertices(state), 2)
    )


def exact_parameters(rows: tuple[int, ...]) -> dict[str, int]:
    order = len(rows)
    gamma = next(
        size
        for size in range(order + 1)
        if any(
            dominates(rows, state)
            for state in masks_of_size(order, size)
        )
    )
    alpha = next(
        size
        for size in range(order, -1, -1)
        if any(
            independent(rows, state)
            for state in masks_of_size(order, size)
        )
    )
    gamma_infinity = next(
        size
        for size in range(1, order + 1)
        if greatest_kernel(rows, size)[0]
    )
    cliques = []
    for size in range(1, order + 1):
        for state in masks_of_size(order, size):
            if all(
                rows[first] & (1 << second)
                for first, second in combinations(vertices(state), 2)
            ):
                cliques.append(state)
    cover = {0: 0}
    for remaining in range(1, 1 << order):
        pivot = remaining & -remaining
        cover[remaining] = min(
            1 + cover[remaining ^ clique]
            for clique in cliques
            if clique & pivot and clique & remaining == clique
        )
    return {
        "gamma": gamma,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
        "theta": cover[(1 << order) - 1],
    }


def encode_graph6(rows: tuple[int, ...]) -> str:
    order = len(rows)
    bits = [
        int(bool(rows[low] & (1 << high)))
        for high in range(1, order)
        for low in range(high)
    ]
    while len(bits) % 6:
        bits.append(0)
    return chr(order + 63) + "".join(
        chr(
            63
            + sum(
                bits[offset + shift] << (5 - shift)
                for shift in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )


def random_three_clique_graph(
    rng: random.Random,
    class_size: int,
    cross_probability: float,
) -> tuple[tuple[int, ...], tuple[int, int, int], int]:
    order = 3 * class_size
    classes = tuple(
        tuple(range(color * class_size, (color + 1) * class_size))
        for color in range(3)
    )
    root = tuple(color_class[0] for color_class in classes)
    target = classes[0][1]
    rows = [0] * order

    def add_edge(first: int, second: int) -> None:
        rows[first] |= 1 << second
        rows[second] |= 1 << first

    for color_class in classes:
        for first, second in combinations(color_class, 2):
            add_edge(first, second)
    for first_color, second_color in combinations(range(3), 2):
        for first in classes[first_color]:
            for second in classes[second_color]:
                if rng.random() < cross_probability:
                    add_edge(first, second)
    # Keep the named root independent while making the target graph-adjacent
    # to all root anchors.
    for first, second in combinations(root, 2):
        rows[first] &= ~(1 << second)
        rows[second] &= ~(1 << first)
    for anchor in root:
        if anchor != target:
            add_edge(anchor, target)
    return tuple(rows), root, target


def search_controls(
    trials: int,
    seed: int,
    class_size: int,
    cross_probability: float,
) -> None:
    rng = random.Random(seed)
    full_count = 0
    annihilated_count = 0
    positive_count = 0
    for trial in range(trials):
        rows, root_vertices, target = random_three_clique_graph(
            rng, class_size, cross_probability
        )
        if has_dominating_pair(rows):
            continue
        root = sum(1 << vertex for vertex in root_vertices)
        greatest = greatest_kernel(rows, 3)[0]
        if response_list(rows, greatest, root, target) != root_vertices:
            continue
        full_count += 1
        graph6 = encode_graph6(rows)
        records = audit_control(graph6, root_vertices, target)
        if records:
            annihilated_count += 1
        for record in records:
            if record["rank"] <= 0:
                continue
            positive_count += 1
            alternates = record["alternates"]
            if (
                record["gate"] == "nonroot_corridor"
                and any(
                    alternate["dominates"] and not alternate["retained"]
                    for alternate in alternates
                )
            ) or (
                record["gate"] == "anchor_restoration"
                and (
                    not alternates
                    or any(
                        alternate["dominates"] and not alternate["retained"]
                        for alternate in alternates
                    )
                )
            ):
                print(
                    {
                        "trial": trial,
                        "graph6": graph6,
                        "root": root_vertices,
                        "target": target,
                        "record": record,
                    }
                )
                return
    print(
        {
            "trials": trials,
            "seed": seed,
            "full": full_count,
            "with_annihilated_color": annihilated_count,
            "positive_entries": positive_count,
            "countercontrol_found": False,
        }
    )


def scan_mmv_catalog() -> None:
    campaign = Path(__file__).resolve().parents[3]
    with (campaign / "instances/mmv2022_table9.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        graph_records = tuple(csv.DictReader(stream))
    counts = {
        "graphs": 0,
        "full_incidences": 0,
        "annihilated_incidences": 0,
        "positive_entries": 0,
    }
    examples: dict[str, dict[str, object]] = {}
    for graph_record in graph_records:
        graph6 = graph_record["graph6"]
        rows = decode_graph6(graph6)
        greatest = greatest_kernel(rows, 3)[0]
        counts["graphs"] += 1
        for root_vertices in combinations(range(len(rows)), 3):
            root = sum(1 << vertex for vertex in root_vertices)
            if any(
                rows[first] & (1 << second)
                for first, second in combinations(root_vertices, 2)
            ):
                continue
            for target in range(len(rows)):
                if root & (1 << target):
                    continue
                if response_list(
                    rows, greatest, root, target
                ) != root_vertices:
                    continue
                counts["full_incidences"] += 1
                records = audit_control(graph6, root_vertices, target)
                if records:
                    counts["annihilated_incidences"] += 1
                for record in records:
                    if record["rank"] <= 0:
                        continue
                    counts["positive_entries"] += 1
                    alternates = record["alternates"]
                    categories = []
                    if record["gate"] == "direct_root":
                        categories.append("direct_root")
                    elif record["gate"] == "nonroot_corridor":
                        if any(
                            not alternate["dominates"]
                            for alternate in alternates
                        ):
                            categories.append("corridor_nondominating")
                        if any(
                            alternate["dominates"] and alternate["retained"]
                            for alternate in alternates
                        ):
                            categories.append("corridor_retained_lower")
                        if any(
                            alternate["dominates"]
                            and not alternate["retained"]
                            for alternate in alternates
                        ):
                            categories.append("corridor_nonretained_lower")
                    elif record["gate"] == "anchor_restoration":
                        if not alternates:
                            categories.append("anchor_no_graph_alternate")
                        if any(
                            not alternate["dominates"]
                            for alternate in alternates
                        ):
                            categories.append("anchor_nondominating")
                        if any(
                            alternate["dominates"] and alternate["retained"]
                            for alternate in alternates
                        ):
                            categories.append("anchor_retained_lower")
                        if any(
                            alternate["dominates"]
                            and not alternate["retained"]
                            for alternate in alternates
                        ):
                            categories.append("anchor_nonretained_lower")
                        if any(
                            alternate["banned"] for alternate in alternates
                        ):
                            categories.append("anchor_alternate_banned")
                    for category in categories:
                        examples.setdefault(
                            category,
                            {
                                "catalog_row": graph_record,
                                "record": record,
                            },
                        )
    print({"counts": counts, "first_examples": examples})


def add_true_twin(
    rows: tuple[int, ...],
    source: int,
) -> tuple[int, ...]:
    order = len(rows)
    extended = list(rows) + [0]
    for neighbor in vertices(rows[source]):
        extended[neighbor] |= 1 << order
        extended[order] |= 1 << neighbor
    extended[source] |= 1 << order
    extended[order] |= 1 << source
    return tuple(extended)


def scan_true_twin_extensions() -> None:
    examples = []
    for graph6, root_vertices, target in CONTROLS:
        base_rows = decode_graph6(graph6)
        for source in range(len(base_rows)):
            rows = add_true_twin(base_rows, source)
            extended_graph6 = encode_graph6(rows)
            records = audit_control(
                extended_graph6, root_vertices, target
            )
            for record in records:
                if record["rank"] <= 0:
                    continue
                for alternate in record["alternates"]:
                    if (
                        record["gate"] == "nonroot_corridor"
                        and alternate["dominates"]
                        and not alternate["retained"]
                    ):
                        examples.append(
                            {
                                "base": graph6,
                                "twin_source": source,
                                "extended_graph6": extended_graph6,
                                "record": record,
                            }
                        )
                        print(examples[0])
                        return
    print({"true_twin_extensions": sum(len(decode_graph6(g)) for g, _, _ in CONTROLS),
           "corridor_nonretained_lower_found": False})


def find_record(
    graph6: str,
    root: tuple[int, int, int],
    target: int,
    *,
    color: int,
    predecessor: tuple[int, int, int],
    attack: int,
    mover: int,
) -> dict[str, object]:
    matches = [
        record
        for record in audit_control(graph6, root, target)
        if record["color"] == color
        and record["predecessor"] == predecessor
        and record["attack"] == attack
        and record["mover"] == mover
    ]
    if len(matches) != 1:
        raise AssertionError(("named terminal record not unique", matches))
    return matches[0]


def verify_named_controls() -> None:
    equality_graph = r"Ksv`f\knJVis"
    equality_parameters = exact_parameters(decode_graph6(equality_graph))
    if equality_parameters != {
        "gamma": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }:
        raise AssertionError(equality_parameters)
    equality_record = find_record(
        equality_graph,
        (1, 2, 3),
        0,
        color=1,
        predecessor=(3, 5, 8),
        attack=2,
        mover=5,
    )
    if not (
        equality_record["rank"] == 1
        and equality_record["gate"] == "anchor_restoration"
        and equality_record["terminal"] == (2, 3, 8)
        and equality_record["palette"] == (1, 2)
        and equality_record["alternates"] == [
            {
                "guard": 8,
                "state": (2, 3, 5),
                "dominates": True,
                "rank": 0,
                "retained": True,
                "banned": False,
            }
        ]
    ):
        raise AssertionError(equality_record)

    nonretained_graph = "JEhbtj{rvf?"
    nonretained_parameters = exact_parameters(
        decode_graph6(nonretained_graph)
    )
    if nonretained_parameters != {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 4,
    }:
        raise AssertionError(nonretained_parameters)
    nonretained_record = find_record(
        nonretained_graph,
        (4, 5, 10),
        8,
        color=4,
        predecessor=(0, 5, 10),
        attack=9,
        mover=0,
    )
    if not (
        nonretained_record["rank"] == 2
        and nonretained_record["gate"] == "nonroot_corridor"
        and nonretained_record["terminal"] == (5, 9, 10)
        and nonretained_record["palette"] == (4, 5)
        and nonretained_record["alternates"] == [
            {
                "guard": 5,
                "state": (0, 9, 10),
                "dominates": True,
                "rank": 1,
                "retained": False,
                "banned": False,
            }
        ]
    ):
        raise AssertionError(nonretained_record)

    irrelevant_graph = "JEhbtj{ruv?"
    irrelevant_parameters = exact_parameters(decode_graph6(irrelevant_graph))
    if irrelevant_parameters != {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 4,
    }:
        raise AssertionError(irrelevant_parameters)
    irrelevant_record = find_record(
        irrelevant_graph,
        (1, 4, 7),
        9,
        color=1,
        predecessor=(6, 7, 10),
        attack=4,
        mover=6,
    )
    if not (
        irrelevant_record["rank"] == 1
        and irrelevant_record["gate"] == "anchor_restoration"
        and irrelevant_record["terminal"] == (4, 7, 10)
        and irrelevant_record["palette"] == (1, 7)
        and irrelevant_record["attacked_anchor_in_palette"] is False
        and irrelevant_record["alternates"] == [
            {
                "guard": 10,
                "state": (4, 6, 7),
                "dominates": True,
                "rank": 0,
                "retained": True,
                "banned": False,
            }
        ]
    ):
        raise AssertionError(irrelevant_record)

    print(
        json.dumps(
            {
                "schema": "full-list-positive-rank-controls-v1",
                "model": (
                    "unoccupied attacks; exactly one occupied guard moves "
                    "along one G-edge"
                ),
                "equality_anchor_rank_drop": {
                    "graph6": equality_graph,
                    "parameters": equality_parameters,
                    "record": equality_record,
                },
                "gamma2_nonretained_corridor_alternate": {
                    "graph6": nonretained_graph,
                    "parameters": nonretained_parameters,
                    "record": nonretained_record,
                },
                "gamma2_missing_palette_not_missing_edge": {
                    "graph6": irrelevant_graph,
                    "parameters": irrelevant_parameters,
                    "record": irrelevant_record,
                },
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--class-size", type=int, default=4)
    parser.add_argument("--cross-probability", type=float, default=0.22)
    parser.add_argument("--catalog", action="store_true")
    parser.add_argument("--twins", action="store_true")
    parser.add_argument("--verify-controls", action="store_true")
    arguments = parser.parse_args()
    if arguments.verify_controls:
        verify_named_controls()
        return
    if arguments.twins:
        scan_true_twin_extensions()
        return
    if arguments.catalog:
        scan_mmv_catalog()
        return
    if arguments.search:
        search_controls(
            arguments.search,
            arguments.seed,
            arguments.class_size,
            arguments.cross_probability,
        )
        return
    for control in CONTROLS:
        for record in audit_control(*control):
            if record["rank"] > 0:
                print(record)


if __name__ == "__main__":
    main()
