#!/usr/bin/env python3
"""Clean-room replay for the positive-rank full-list terminal review.

This file deliberately imports no campaign module and uses frozenset
configurations rather than the candidate's packed-integer transition core.
"""

from __future__ import annotations

from itertools import combinations
import json


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    data = [ord(character) - 63 for character in record]
    if not data or not 0 <= data[0] <= 62:
        raise ValueError("only short graph6 records are supported")
    order = data[0]
    stream = []
    for value in data[1:]:
        stream.extend(bool(value & (1 << shift)) for shift in range(5, -1, -1))
    adjacency = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if stream[cursor]:
                adjacency[low].add(high)
                adjacency[high].add(low)
            cursor += 1
    return tuple(frozenset(neighbors) for neighbors in adjacency)


def all_states(order: int, size: int) -> tuple[frozenset[int], ...]:
    return tuple(frozenset(state) for state in combinations(range(order), size))


def dominates(
    adjacency: tuple[frozenset[int], ...],
    state: frozenset[int],
) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(adjacency[guard])
    return len(covered) == len(adjacency)


def legal_successors(
    adjacency: tuple[frozenset[int], ...],
    state: frozenset[int],
    attacked: int,
) -> tuple[frozenset[int], ...]:
    if attacked in state:
        raise AssertionError("attacks must be unoccupied")
    return tuple(
        frozenset((state - {guard}) | {attacked})
        for guard in sorted(state)
        if attacked in adjacency[guard]
    )


def peel(
    adjacency: tuple[frozenset[int], ...],
    size: int,
    banned: frozenset[frozenset[int]] = frozenset(),
) -> tuple[
    frozenset[frozenset[int]],
    dict[frozenset[int], int],
    tuple[int, ...],
]:
    active = {
        state
        for state in all_states(len(adjacency), size)
        if state not in banned and dominates(adjacency, state)
    }
    ranks: dict[frozenset[int], int] = {}
    rounds = []
    rank = 0
    while True:
        doomed = set()
        for state in active:
            for attacked in range(len(adjacency)):
                if attacked in state:
                    continue
                if not any(
                    successor in active
                    for successor in legal_successors(
                        adjacency, state, attacked
                    )
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return frozenset(active), ranks, tuple(rounds)
        rounds.append(len(doomed))
        for state in doomed:
            ranks[state] = rank
        active.difference_update(doomed)
        rank += 1


def independent(
    adjacency: tuple[frozenset[int], ...],
    state: frozenset[int],
) -> bool:
    return all(second not in adjacency[first] for first, second in combinations(state, 2))


def gamma(adjacency: tuple[frozenset[int], ...]) -> int:
    return next(
        size
        for size in range(len(adjacency) + 1)
        if any(dominates(adjacency, state) for state in all_states(len(adjacency), size))
    )


def alpha(adjacency: tuple[frozenset[int], ...]) -> int:
    return next(
        size
        for size in range(len(adjacency), -1, -1)
        if any(independent(adjacency, state) for state in all_states(len(adjacency), size))
    )


def gamma_infinity(adjacency: tuple[frozenset[int], ...]) -> int:
    return next(
        size
        for size in range(1, len(adjacency) + 1)
        if peel(adjacency, size)[0]
    )


def complement(
    adjacency: tuple[frozenset[int], ...],
) -> tuple[frozenset[int], ...]:
    vertices = frozenset(range(len(adjacency)))
    return tuple(
        vertices - {vertex} - adjacency[vertex]
        for vertex in range(len(adjacency))
    )


def coloring(
    adjacency: tuple[frozenset[int], ...],
    number_of_colors: int,
) -> tuple[int, ...] | None:
    order = len(adjacency)
    assigned = [-1] * order

    def extend(used: int) -> bool:
        if all(color >= 0 for color in assigned):
            return True
        uncolored = [vertex for vertex in range(order) if assigned[vertex] < 0]
        vertex = max(
            uncolored,
            key=lambda item: (
                len(
                    {
                        assigned[neighbor]
                        for neighbor in adjacency[item]
                        if assigned[neighbor] >= 0
                    }
                ),
                len(adjacency[item]),
                -item,
            ),
        )
        forbidden = {
            assigned[neighbor]
            for neighbor in adjacency[vertex]
            if assigned[neighbor] >= 0
        }
        upper = min(number_of_colors, used + 1)
        for color in range(upper):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if extend(max(used, color + 1)):
                return True
            assigned[vertex] = -1
        return False

    if extend(0):
        return tuple(assigned)
    return None


def theta(
    adjacency: tuple[frozenset[int], ...],
) -> tuple[int, tuple[int, ...]]:
    other = complement(adjacency)
    for number_of_colors in range(1, len(adjacency) + 1):
        witness = coloring(other, number_of_colors)
        if witness is not None:
            return number_of_colors, witness
    raise AssertionError("every finite graph is colorable")


def parameters(
    adjacency: tuple[frozenset[int], ...],
) -> tuple[dict[str, int], tuple[int, ...]]:
    clique_cover, color_witness = theta(adjacency)
    return (
        {
            "gamma": gamma(adjacency),
            "alpha": alpha(adjacency),
            "gamma_infinity": gamma_infinity(adjacency),
            "theta": clique_cover,
        },
        color_witness,
    )


def link(
    adjacency: tuple[frozenset[int], ...],
    target: int,
) -> frozenset[int]:
    return frozenset(range(len(adjacency))) - {target} - adjacency[target]


def palette(
    adjacency: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
    root: frozenset[int],
    target: int,
) -> frozenset[int]:
    return frozenset(
        color
        for color in root
        if target in adjacency[color]
        and frozenset((root - {color}) | {target}) in family
    )


def is_deletion_witness(
    adjacency: tuple[frozenset[int], ...],
    ranks: dict[frozenset[int], int],
    kernel: frozenset[frozenset[int]],
    state: frozenset[int],
    attacked: int,
) -> bool:
    height = ranks[state]
    for successor in legal_successors(adjacency, state, attacked):
        if not dominates(adjacency, successor):
            continue
        if successor in kernel or ranks.get(successor, -1) >= height:
            return False
    return True


def terminal_entries(
    adjacency: tuple[frozenset[int], ...],
    root: frozenset[int],
    target: int,
    color: int,
) -> tuple[
    list[dict[str, object]],
    frozenset[frozenset[int]],
    dict[frozenset[int], int],
    tuple[int, ...],
]:
    greatest, _, _ = peel(adjacency, 3)
    physical_link = link(adjacency, target)
    base = root - {color}
    banned = frozenset(frozenset(base | {vertex}) for vertex in physical_link)
    kernel, ranks, rounds = peel(adjacency, 3, banned)
    if kernel:
        return [], kernel, ranks, rounds

    entries = []
    for state in sorted(greatest - banned, key=lambda item: tuple(sorted(item))):
        height = ranks[state]
        for attacked in range(len(adjacency)):
            if attacked in state or not is_deletion_witness(
                adjacency, ranks, kernel, state, attacked
            ):
                continue
            successors = legal_successors(adjacency, state, attacked)
            for mover in sorted(state):
                if attacked not in adjacency[mover]:
                    continue
                successor = frozenset((state - {mover}) | {attacked})
                if successor not in greatest or successor not in banned:
                    continue
                outside = successor - base
                assert len(outside) == 1
                terminal = next(iter(outside))
                terminal_palette = palette(
                    adjacency, greatest, root, terminal
                )
                assert color in terminal_palette
                assert terminal in physical_link

                if attacked == terminal:
                    gate = "direct_root" if state == root else "nonroot_corridor"
                    corridor_mover = mover
                    assert state == frozenset(base | {corridor_mover})
                    if gate == "direct_root":
                        assert corridor_mover == color
                    else:
                        assert corridor_mover not in root | physical_link | {target}
                        quartet = {target, color, corridor_mover, terminal}
                        assert len(quartet) == 4
                        missing = {
                            frozenset(pair)
                            for pair in combinations(quartet, 2)
                            if pair[1] not in adjacency[pair[0]]
                        }
                        assert missing == {frozenset({target, terminal})}

                    for secondary in terminal_palette - {color}:
                        alternate = frozenset(
                            (state - {secondary}) | {terminal}
                        )
                        assert terminal in adjacency[secondary]
                        assert alternate not in banned
                        if gate == "direct_root":
                            assert alternate in greatest
                            assert dominates(adjacency, alternate)
                            assert ranks[alternate] < height
                        elif dominates(adjacency, alternate):
                            assert ranks[alternate] < height
                        else:
                            missed = {
                                vertex
                                for vertex in range(len(adjacency))
                                if vertex not in alternate
                                and not (adjacency[vertex] & alternate)
                            }
                            assert missed
                            for witness in missed:
                                assert witness in adjacency[secondary]
                                assert witness not in root | {
                                    target,
                                    corridor_mover,
                                    terminal,
                                }

                    if terminal_palette == root:
                        secondary_colors = sorted(root - {color})
                        missed_sets = []
                        for secondary in secondary_colors:
                            alternate = frozenset(
                                (state - {secondary}) | {terminal}
                            )
                            if not dominates(adjacency, alternate):
                                missed_sets.append(
                                    {
                                        vertex
                                        for vertex in range(len(adjacency))
                                        if vertex not in alternate
                                        and not (adjacency[vertex] & alternate)
                                    }
                                )
                        if len(missed_sets) == 2:
                            assert missed_sets[0].isdisjoint(missed_sets[1])

                    if height > 0:
                        anchor_alternates = [
                            frozenset((state - {anchor}) | {terminal})
                            for anchor in base
                            if terminal in adjacency[anchor]
                            and frozenset((state - {anchor}) | {terminal})
                            not in banned
                            and dominates(
                                adjacency,
                                frozenset((state - {anchor}) | {terminal}),
                            )
                        ]
                        assert anchor_alternates
                        assert all(ranks[item] < height for item in anchor_alternates)

                elif attacked in base:
                    gate = "anchor_restoration"
                    anchor = attacked
                    other_anchor = next(iter(base - {anchor}))
                    assert state == frozenset({other_anchor, terminal, mover})
                    if height > 0:
                        restored = frozenset((state - {terminal}) | {anchor})
                        assert anchor in adjacency[terminal]
                        assert dominates(adjacency, restored)
                        assert restored not in banned
                        assert ranks[restored] < height
                    elif (
                        anchor in adjacency[terminal]
                        and mover not in physical_link
                    ):
                        restored = frozenset((state - {terminal}) | {anchor})
                        if not dominates(adjacency, restored):
                            missed = {
                                vertex
                                for vertex in range(len(adjacency))
                                if vertex not in restored
                                and not (adjacency[vertex] & restored)
                            }
                            assert missed
                            for witness in missed:
                                assert witness in adjacency[terminal]
                                assert witness not in {
                                    anchor,
                                    other_anchor,
                                    mover,
                                    terminal,
                                    target,
                                }
                else:
                    raise AssertionError("C-149 terminal gate is not exhaustive")

                entries.append(
                    {
                        "state": tuple(sorted(state)),
                        "rank": height,
                        "attack": attacked,
                        "mover": mover,
                        "successor": tuple(sorted(successor)),
                        "terminal": terminal,
                        "palette": tuple(sorted(terminal_palette)),
                        "gate": gate,
                    }
                )

    assert entries
    minimum = min(entry["rank"] for entry in entries)
    for entry in entries:
        if entry["rank"] != minimum:
            continue
        state = frozenset(entry["state"])
        terminal = int(entry["terminal"])
        terminal_palette = frozenset(entry["palette"])
        if entry["gate"] == "direct_root":
            assert terminal_palette == {color}
        elif entry["gate"] == "nonroot_corridor":
            for secondary in terminal_palette - {color}:
                alternate = frozenset((state - {secondary}) | {terminal})
                if dominates(adjacency, alternate):
                    assert alternate not in greatest
            if entry["rank"] > 0:
                compulsory = [
                    frozenset((state - {anchor}) | {terminal})
                    for anchor in base
                    if terminal in adjacency[anchor]
                    and dominates(
                        adjacency,
                        frozenset((state - {anchor}) | {terminal}),
                    )
                    and frozenset((state - {anchor}) | {terminal})
                    not in banned
                ]
                assert compulsory
                assert all(item not in greatest for item in compulsory)
        elif entry["rank"] > 0:
            anchor = int(entry["attack"])
            restored = frozenset((state - {terminal}) | {anchor})
            assert restored not in greatest

    return entries, kernel, ranks, rounds


def check_named_controls() -> dict[str, object]:
    specifications = (
        {
            "name": "equality_anchor_rank_drop",
            "graph6": r"Ksv`f\knJVis",
            "parameters": {
                "gamma": 3,
                "alpha": 3,
                "gamma_infinity": 3,
                "theta": 3,
            },
            "root": {1, 2, 3},
            "target": 0,
            "color": 1,
            "named": {
                "state": (3, 5, 8),
                "rank": 1,
                "attack": 2,
                "mover": 5,
                "successor": (2, 3, 8),
                "terminal": 8,
                "palette": (1, 2),
                "gate": "anchor_restoration",
            },
            "alternate": {2, 3, 5},
            "alternate_rank": 0,
            "alternate_retained": True,
        },
        {
            "name": "gamma2_nonretained_corridor_alternate",
            "graph6": "JEhbtj{rvf?",
            "parameters": {
                "gamma": 2,
                "alpha": 3,
                "gamma_infinity": 3,
                "theta": 4,
            },
            "root": {4, 5, 10},
            "target": 8,
            "color": 4,
            "named": {
                "state": (0, 5, 10),
                "rank": 2,
                "attack": 9,
                "mover": 0,
                "successor": (5, 9, 10),
                "terminal": 9,
                "palette": (4, 5),
                "gate": "nonroot_corridor",
            },
            "alternate": {0, 9, 10},
            "alternate_rank": 1,
            "alternate_retained": False,
        },
        {
            "name": "gamma2_missing_palette_not_missing_edge",
            "graph6": "JEhbtj{ruv?",
            "parameters": {
                "gamma": 2,
                "alpha": 3,
                "gamma_infinity": 3,
                "theta": 4,
            },
            "root": {1, 4, 7},
            "target": 9,
            "color": 1,
            "named": {
                "state": (6, 7, 10),
                "rank": 1,
                "attack": 4,
                "mover": 6,
                "successor": (4, 7, 10),
                "terminal": 10,
                "palette": (1, 7),
                "gate": "anchor_restoration",
            },
            "alternate": {4, 6, 7},
            "alternate_rank": 0,
            "alternate_retained": True,
        },
    )

    result: dict[str, object] = {
        "schema": "full-list-positive-rank-hostile-replay-v1",
        "model": (
            "unoccupied attacks; exactly one occupied guard moves along "
            "one G-edge; synchronous greatest-fixed-point deletion"
        ),
        "controls": {},
    }
    controls = result["controls"]
    assert isinstance(controls, dict)

    for specification in specifications:
        adjacency = decode_graph6(str(specification["graph6"]))
        exact, color_witness = parameters(adjacency)
        assert exact == specification["parameters"]
        root = frozenset(specification["root"])
        target = int(specification["target"])
        color = int(specification["color"])
        greatest, _, unrestricted_rounds = peel(adjacency, 3)
        assert independent(adjacency, root)
        assert palette(adjacency, greatest, root, target) == root
        entries, kernel, ranks, restricted_rounds = terminal_entries(
            adjacency, root, target, color
        )
        assert not kernel
        matches = [entry for entry in entries if entry == specification["named"]]
        assert len(matches) == 1

        alternate = frozenset(specification["alternate"])
        assert dominates(adjacency, alternate)
        assert ranks[alternate] == specification["alternate_rank"]
        assert (alternate in greatest) is specification["alternate_retained"]

        if specification["name"] == "gamma2_missing_palette_not_missing_edge":
            terminal = int(specification["named"]["terminal"])
            attacked = int(specification["named"]["attack"])
            assert attacked not in palette(adjacency, greatest, root, terminal)
            assert attacked in adjacency[terminal]

        controls[specification["name"]] = {
            "graph6": specification["graph6"],
            "order": len(adjacency),
            "size": sum(len(row) for row in adjacency) // 2,
            "parameters": exact,
            "complement_coloring": color_witness,
            "unrestricted_kernel_size": len(greatest),
            "unrestricted_deletion_rounds": unrestricted_rounds,
            "restricted_deletion_rounds": restricted_rounds,
            "terminal_entry_count": len(entries),
            "minimum_terminal_rank": min(entry["rank"] for entry in entries),
            "named_entry": matches[0],
            "alternate": tuple(sorted(alternate)),
            "alternate_rank": ranks[alternate],
            "alternate_retained": alternate in greatest,
        }
    return result


def main() -> None:
    print(
        json.dumps(
            check_named_controls(),
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
