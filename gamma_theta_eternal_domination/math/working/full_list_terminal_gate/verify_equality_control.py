#!/usr/bin/env python3
"""Independent replay of the C-142 equality control at the C-149 gate.

This checker imports no campaign transition, parameter, or coloring code.
Configurations are integer masks and all fixed points are recomputed
directly from the one-guard game definition.
"""

from __future__ import annotations

import itertools
import json


GRAPH6 = r"Ksv`f\knJVis"
ROOT_VERTICES = (1, 2, 3)
TARGET = 0


def decode_short_graph6(record: str) -> tuple[int, ...]:
    order = ord(record[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 records are supported")
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    if len(bits) != ((needed + 5) // 6) * 6 or any(bits[needed:]):
        raise ValueError("noncanonical graph6 padding")
    rows = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            cursor += 1
    return tuple(rows)


def masks_of_size(order: int, size: int):
    for vertices in itertools.combinations(range(order), size):
        yield sum(1 << vertex for vertex in vertices)


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(mask.bit_length()) if mask >> index & 1)


def dominates(rows: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in vertices(state):
        covered |= rows[vertex]
    return covered == (1 << len(rows)) - 1


def independent(rows: tuple[int, ...], state: int) -> bool:
    return all(rows[vertex] & (state ^ (1 << vertex)) == 0 for vertex in vertices(state))


def legal_successors(
    rows: tuple[int, ...],
    state: int,
    attacked: int,
) -> tuple[int, ...]:
    attacked_bit = 1 << attacked
    if state & attacked_bit:
        return ()
    return tuple(
        state ^ (1 << guard) ^ attacked_bit
        for guard in vertices(state & rows[attacked])
    )


def greatest_kernel(
    rows: tuple[int, ...],
    size: int,
    banned: frozenset[int] = frozenset(),
) -> tuple[frozenset[int], dict[int, int], tuple[int, ...]]:
    active = {
        state
        for state in masks_of_size(len(rows), size)
        if state not in banned and dominates(rows, state)
    }
    ranks: dict[int, int] = {}
    rounds: list[int] = []
    round_number = 0
    while True:
        deleted = set()
        for state in active:
            for attacked in range(len(rows)):
                if state >> attacked & 1:
                    continue
                if not any(
                    successor in active
                    for successor in legal_successors(rows, state, attacked)
                ):
                    deleted.add(state)
                    break
        if not deleted:
            return frozenset(active), ranks, tuple(rounds)
        for state in deleted:
            ranks[state] = round_number
        rounds.append(len(deleted))
        active.difference_update(deleted)
        round_number += 1


def exact_gamma(rows: tuple[int, ...]) -> int:
    for size in range(1, len(rows) + 1):
        if any(dominates(rows, state) for state in masks_of_size(len(rows), size)):
            return size
    raise AssertionError("no dominating set")


def exact_alpha(rows: tuple[int, ...]) -> int:
    for size in range(len(rows), 0, -1):
        if any(independent(rows, state) for state in masks_of_size(len(rows), size)):
            return size
    return 0


def complement_rows(rows: tuple[int, ...]) -> tuple[int, ...]:
    universe = (1 << len(rows)) - 1
    return tuple(universe ^ (1 << vertex) ^ rows[vertex] for vertex in range(len(rows)))


def colorable(rows: tuple[int, ...], color_count: int) -> bool:
    colors = [-1] * len(rows)

    def search(colored: int) -> bool:
        if colored == len(rows):
            return True
        candidates = [vertex for vertex, color in enumerate(colors) if color < 0]
        vertex = max(
            candidates,
            key=lambda item: (
                len(
                    {
                        colors[neighbor]
                        for neighbor in vertices(rows[item])
                        if colors[neighbor] >= 0
                    }
                ),
                rows[item].bit_count(),
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in vertices(rows[vertex])
            if colors[neighbor] >= 0
        }
        for color in range(color_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            if search(colored + 1):
                return True
            colors[vertex] = -1
        return False

    return search(0)


def exact_chromatic(rows: tuple[int, ...]) -> int:
    for color_count in range(1, len(rows) + 1):
        if colorable(rows, color_count):
            return color_count
    raise AssertionError("no coloring")


def response_palette(
    rows: tuple[int, ...],
    family: frozenset[int],
    root: int,
    target: int,
) -> tuple[int, ...]:
    return tuple(
        guard
        for guard in vertices(root)
        if rows[guard] >> target & 1
        and root ^ (1 << guard) ^ (1 << target) in family
    )


def complement_neighbors(rows: tuple[int, ...], vertex: int) -> tuple[int, ...]:
    return tuple(
        other
        for other in range(len(rows))
        if other != vertex and not (rows[vertex] >> other & 1)
    )


def ban_for(
    rows: tuple[int, ...],
    root: int,
    target: int,
    color: int,
) -> frozenset[int]:
    base = root ^ (1 << color)
    return frozenset(
        base | (1 << neighbor)
        for neighbor in complement_neighbors(rows, target)
    )


def deletion_witness_attacks(
    rows: tuple[int, ...],
    state: int,
    banned: frozenset[int],
    ranks: dict[int, int],
) -> tuple[int, ...]:
    result = []
    current_rank = ranks[state]
    for attacked in range(len(rows)):
        if state >> attacked & 1:
            continue
        allowed = tuple(
            successor
            for successor in legal_successors(rows, state, attacked)
            if successor not in banned and dominates(rows, successor)
        )
        if all(
            successor in ranks and ranks[successor] < current_rank
            for successor in allowed
        ):
            result.append(attacked)
    return tuple(result)


def gate_record(
    rows: tuple[int, ...],
    greatest: frozenset[int],
    root: int,
    target: int,
    color: int,
    predecessor: int,
    attacked: int,
    successor: int,
) -> dict[str, object]:
    base = root ^ (1 << color)
    extra = successor & ~base
    removed = predecessor & ~successor
    if extra.bit_count() != 1 or removed.bit_count() != 1:
        raise AssertionError("terminal transition is not a one-guard move")
    b = extra.bit_length() - 1
    mover = removed.bit_length() - 1
    if attacked == b:
        gate = "direct_root_corridor" if mover == color else "nonroot_corridor"
        if mover in complement_neighbors(rows, target):
            raise AssertionError("corridor mover lies in the physical link")
        if mover != color:
            quartet = (target, color, mover, b)
            missing = tuple(
                tuple(sorted((first, second)))
                for first, second in itertools.combinations(quartet, 2)
                if not (rows[first] >> second & 1)
            )
            if missing != (tuple(sorted((target, b))),):
                raise AssertionError(("corridor is not the forced diamond", quartet, missing))
    elif base >> attacked & 1:
        gate = "anchor_restoration"
    else:
        raise AssertionError("unclassified terminal gate")
    return {
        "predecessor": list(vertices(predecessor)),
        "attack": attacked,
        "mover": mover,
        "successor": list(vertices(successor)),
        "gate": gate,
        "terminal_vertex": b,
        "terminal_palette": list(response_palette(rows, greatest, root, b)),
    }


def reachable_terminal_entries(
    rows: tuple[int, ...],
    greatest: frozenset[int],
    root: int,
    target: int,
    color: int,
    banned: frozenset[int],
    ranks: dict[int, int],
) -> tuple[tuple[int, ...], tuple[dict[str, object], ...]]:
    start = (root ^ (1 << color)) | (1 << target)
    frontier = [start]
    seen = set()
    entries: dict[tuple[int, int, int], dict[str, object]] = {}
    while frontier:
        state = frontier.pop()
        if state in seen:
            continue
        seen.add(state)
        for attacked in deletion_witness_attacks(rows, state, banned, ranks):
            for successor in legal_successors(rows, state, attacked):
                if successor not in greatest:
                    continue
                if successor in banned:
                    key = (state, attacked, successor)
                    entries[key] = gate_record(
                        rows,
                        greatest,
                        root,
                        target,
                        color,
                        state,
                        attacked,
                        successor,
                    )
                else:
                    if successor not in ranks or ranks[successor] >= ranks[state]:
                        raise AssertionError("retained descent failed to lower rank")
                    frontier.append(successor)
    ordered_states = tuple(sorted(seen))
    ordered_entries = tuple(entries[key] for key in sorted(entries))
    return ordered_states, ordered_entries


def main() -> None:
    rows = decode_short_graph6(GRAPH6)
    root = sum(1 << vertex for vertex in ROOT_VERTICES)
    greatest, _, unrestricted_rounds = greatest_kernel(rows, 3)
    eternal = next(
        size
        for size in range(1, len(rows) + 1)
        if greatest_kernel(rows, size)[0]
    )
    result: dict[str, object] = {
        "scope": (
            "exact finite sharpness control only; it does not decide whether "
            "all three equality kernels can be empty"
        ),
        "graph6": GRAPH6,
        "order": len(rows),
        "size": sum(row.bit_count() for row in rows) // 2,
        "parameters": {
            "gamma": exact_gamma(rows),
            "alpha": exact_alpha(rows),
            "gamma_infinity": eternal,
            "theta": exact_chromatic(complement_rows(rows)),
        },
        "greatest_family_states": len(greatest),
        "greatest_family_deletion_rounds": list(unrestricted_rounds),
        "root": list(ROOT_VERTICES),
        "target": TARGET,
        "target_palette": list(response_palette(rows, greatest, root, TARGET)),
        "colors": {},
    }
    color_records: dict[str, object] = {}
    for color in ROOT_VERTICES:
        banned = ban_for(rows, root, TARGET, color)
        kernel, ranks, rounds = greatest_kernel(rows, 3, banned)
        start = (root ^ (1 << color)) | (1 << TARGET)
        record: dict[str, object] = {
            "kernel_states": len(kernel),
            "deletion_rounds": list(rounds),
            "selected_start_survives": start in kernel,
        }
        if not kernel:
            reachable, entries = reachable_terminal_entries(
                rows,
                greatest,
                root,
                TARGET,
                color,
                banned,
                ranks,
            )
            record.update(
                {
                    "selected_start_rank": ranks[start],
                    "reachable_descent_states": [
                        {"state": list(vertices(state)), "rank": ranks[state]}
                        for state in reachable
                    ],
                    "reachable_terminal_entries": list(entries),
                    "only_nonroot_corridor_entries": bool(entries)
                    and all(entry["gate"] == "nonroot_corridor" for entry in entries),
                    "all_terminal_palettes_nonsingleton": bool(entries)
                    and all(len(entry["terminal_palette"]) >= 2 for entry in entries),
                }
            )
        color_records[str(color)] = record
    result["colors"] = color_records

    expected_parameters = {
        "gamma": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if result["parameters"] != expected_parameters:
        raise AssertionError(result["parameters"])
    if len(greatest) != 127 or unrestricted_rounds:
        raise AssertionError("wrong unrestricted greatest family")
    if result["target_palette"] != [1, 2, 3]:
        raise AssertionError("target is not full")
    for color in ("1", "2"):
        record = color_records[color]
        if record["kernel_states"] != 0:
            raise AssertionError("expected annihilated color")
        if not record["only_nonroot_corridor_entries"]:
            raise AssertionError("unexpected reachable gate")
        if not record["all_terminal_palettes_nonsingleton"]:
            raise AssertionError("unexpected singleton terminal")
    if color_records["3"]["kernel_states"] != 64:
        raise AssertionError("wrong surviving color kernel")

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
