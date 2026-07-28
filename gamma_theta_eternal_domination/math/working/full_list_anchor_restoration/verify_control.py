#!/usr/bin/env python3
"""Independent exact verifier for the rank-zero restoration control.

The implementation deliberately uses ordinary frozensets and reconstructs
every game kernel from the one-guard definition.  It imports no campaign
search or verifier core.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json


GRAPH6 = "OYifur}UO]}iTij]tpo]v"
ROOT = frozenset((0, 1, 10))
TARGET = 6
COLOR = 0
SHARED = 1
ATTACKED = 10
TERMINAL = 5
MOVER = 7


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    """Decode the short graph6 format used by the 16-vertex control."""

    values = [ord(character) - 63 for character in record]
    order = values[0]
    if not 0 <= order < 63:
        raise AssertionError("only short graph6 records are supported")
    bits: list[int] = []
    for value in values[1:]:
        if not 0 <= value < 64:
            raise AssertionError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    neighborhoods = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                neighborhoods[low].add(high)
                neighborhoods[high].add(low)
            cursor += 1
    return tuple(frozenset(neighbors) for neighbors in neighborhoods)


def all_sets(order: int, size: int) -> tuple[frozenset[int], ...]:
    return tuple(frozenset(choice) for choice in combinations(range(order), size))


def dominates(
    neighborhoods: tuple[frozenset[int], ...],
    state: frozenset[int],
) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(neighborhoods[guard])
    return len(covered) == len(neighborhoods)


def independent(
    neighborhoods: tuple[frozenset[int], ...],
    state: frozenset[int],
) -> bool:
    return all(second not in neighborhoods[first] for first, second in combinations(state, 2))


def legal_successors(
    neighborhoods: tuple[frozenset[int], ...],
    state: frozenset[int],
    attacked: int,
) -> tuple[frozenset[int], ...]:
    if attacked in state:
        raise AssertionError("attacks must be unoccupied")
    return tuple(
        state - {guard} | {attacked}
        for guard in sorted(state)
        if attacked in neighborhoods[guard]
    )


def greatest_kernel(
    neighborhoods: tuple[frozenset[int], ...],
    size: int,
    banned: frozenset[frozenset[int]] = frozenset(),
) -> tuple[frozenset[frozenset[int]], dict[frozenset[int], int]]:
    """Synchronous greatest-fixed-point deletion with exact deletion ranks."""

    active = {
        state
        for state in all_sets(len(neighborhoods), size)
        if state not in banned and dominates(neighborhoods, state)
    }
    ranks: dict[frozenset[int], int] = {}
    round_number = 0
    while True:
        doomed = set()
        for state in active:
            for attacked in range(len(neighborhoods)):
                if attacked in state:
                    continue
                if not any(
                    successor in active
                    for successor in legal_successors(
                        neighborhoods, state, attacked
                    )
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return frozenset(active), ranks
        for state in doomed:
            ranks[state] = round_number
        active.difference_update(doomed)
        round_number += 1


def response_palette(
    neighborhoods: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
    root: frozenset[int],
    vertex: int,
) -> tuple[int, ...]:
    return tuple(
        color
        for color in sorted(root)
        if vertex in neighborhoods[color]
        and root - {color} | {vertex} in family
    )


def exact_parameters(
    neighborhoods: tuple[frozenset[int], ...],
) -> tuple[dict[str, int], tuple[frozenset[int], ...], frozenset[frozenset[int]]]:
    order = len(neighborhoods)
    subsets_by_size = tuple(all_sets(order, size) for size in range(order + 1))

    gamma = next(
        size
        for size, subsets in enumerate(subsets_by_size)
        if any(dominates(neighborhoods, state) for state in subsets)
    )
    alpha = next(
        size
        for size in range(order, -1, -1)
        if any(independent(neighborhoods, state) for state in subsets_by_size[size])
    )
    independent_domination = next(
        size
        for size, subsets in enumerate(subsets_by_size)
        if any(
            independent(neighborhoods, state)
            and dominates(neighborhoods, state)
            for state in subsets
        )
    )

    kernels = []
    for size in range(1, 4):
        kernel, _ = greatest_kernel(neighborhoods, size)
        kernels.append(kernel)
    if kernels[0] or kernels[1] or not kernels[2]:
        raise AssertionError("the exact eternal parameter is not three")

    clique_masks = []
    for mask in range(1, 1 << order):
        state = frozenset(vertex for vertex in range(order) if mask >> vertex & 1)
        if all(second in neighborhoods[first] for first, second in combinations(state, 2)):
            clique_masks.append(mask)
    cliques_by_pivot: dict[int, tuple[int, ...]] = {}
    for pivot in range(order):
        pivot_bit = 1 << pivot
        cliques_by_pivot[pivot] = tuple(
            clique for clique in clique_masks if clique & pivot_bit
        )

    choice: dict[int, int] = {}

    @lru_cache(maxsize=None)
    def cover(remaining: int) -> int:
        if remaining == 0:
            return 0
        pivot_bit = remaining & -remaining
        pivot = pivot_bit.bit_length() - 1
        candidates = (
            clique
            for clique in cliques_by_pivot[pivot]
            if clique & remaining == clique
        )
        best_value = order + 1
        best_clique = 0
        for clique in candidates:
            value = 1 + cover(remaining ^ clique)
            if value < best_value:
                best_value = value
                best_clique = clique
        choice[remaining] = best_clique
        return best_value

    full_mask = (1 << order) - 1
    theta = cover(full_mask)
    partition = []
    remaining = full_mask
    while remaining:
        clique = choice[remaining]
        partition.append(
            frozenset(vertex for vertex in range(order) if clique >> vertex & 1)
        )
        remaining ^= clique

    parameters = {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": 3,
        "theta": theta,
    }
    return parameters, tuple(partition), kernels[2]


def edge_list(
    neighborhoods: tuple[frozenset[int], ...],
) -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for first in range(len(neighborhoods))
        for second in sorted(neighborhoods[first])
        if first < second
    )


def verify() -> dict[str, object]:
    neighborhoods = decode_graph6(GRAPH6)
    order = len(neighborhoods)
    if any(
        vertex in neighborhoods[vertex]
        or any(vertex not in neighborhoods[neighbor] for neighbor in neighborhoods[vertex])
        for vertex in range(order)
    ):
        raise AssertionError("decoded graph is not finite, simple, and undirected")

    parameters, clique_partition, family = exact_parameters(neighborhoods)
    expected_parameters = {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if parameters != expected_parameters:
        raise AssertionError(parameters)
    if not independent(neighborhoods, ROOT) or ROOT not in family:
        raise AssertionError("the reference triple is not retained independent")
    if response_palette(neighborhoods, family, ROOT, TARGET) != (0, 1, 10):
        raise AssertionError("the named target is not full")

    complement_link = frozenset(
        vertex
        for vertex in range(order)
        if vertex != TARGET and vertex not in neighborhoods[TARGET]
    )
    if complement_link != frozenset((5, 7, 9, 11, 13)):
        raise AssertionError(complement_link)
    ban = frozenset(
        ROOT - {COLOR} | {vertex} for vertex in complement_link
    )
    restricted_kernel, ranks = greatest_kernel(
        neighborhoods, 3, banned=ban
    )
    if restricted_kernel:
        raise AssertionError("the selected restricted kernel survived")

    terminal_ban_state = frozenset((1, 5, 10))
    omitted_alternate = frozenset((1, 7, 10))
    if terminal_ban_state not in family or terminal_ban_state not in ban:
        raise AssertionError("the selected terminal state is not retained and banned")
    if (
        not dominates(neighborhoods, omitted_alternate)
        or omitted_alternate in family
        or omitted_alternate not in ban
    ):
        raise AssertionError("the common alternate does not have the claimed status")

    attacked_secondary_predecessor = frozenset((1, 5, 7))
    shared_secondary_predecessor = frozenset((5, 7, 10))
    if ranks.get(attacked_secondary_predecessor) != 0:
        raise AssertionError("the attacked-secondary predecessor is not rank zero")
    if ranks.get(shared_secondary_predecessor) != 0:
        raise AssertionError("the shared-secondary predecessor is not rank zero")
    if attacked_secondary_predecessor not in family:
        raise AssertionError("first predecessor is not retained")
    if shared_secondary_predecessor not in family:
        raise AssertionError("second predecessor is not retained")

    # First row: q=7 answers attack a=10; r=5 is the legal alternate.
    first_selected = attacked_secondary_predecessor - {MOVER} | {ATTACKED}
    first_alternate = attacked_secondary_predecessor - {TERMINAL} | {ATTACKED}
    if (
        ATTACKED not in neighborhoods[MOVER]
        or ATTACKED not in neighborhoods[TERMINAL]
        or first_selected != terminal_ban_state
        or first_alternate != omitted_alternate
    ):
        raise AssertionError("first one-guard row is incorrect")
    if response_palette(neighborhoods, family, ROOT, TERMINAL) != (0, 10):
        raise AssertionError("terminal palette is not exactly {0,10}")

    # Second row: the same q=7 answers attack a=1; r=5 cannot move.
    second_selected = shared_secondary_predecessor - {MOVER} | {SHARED}
    if (
        SHARED not in neighborhoods[MOVER]
        or SHARED in neighborhoods[TERMINAL]
        or second_selected != terminal_ban_state
    ):
        raise AssertionError("second one-guard row is incorrect")
    if response_palette(neighborhoods, family, ROOT, MOVER) != (1, 10):
        raise AssertionError("restoration did not force the attacked color at q")

    # A rank-zero witness attack has no dominating unbanned successor.
    for predecessor, attacked in (
        (attacked_secondary_predecessor, ATTACKED),
        (shared_secondary_predecessor, SHARED),
    ):
        for successor in legal_successors(neighborhoods, predecessor, attacked):
            if dominates(neighborhoods, successor) and successor not in ban:
                raise AssertionError(
                    ("rank-zero row has a dominating unbanned successor", predecessor, successor)
                )

    obligations = 0
    for state in family:
        if not dominates(neighborhoods, state):
            raise AssertionError("greatest-family state fails domination")
        for attacked in range(order):
            if attacked in state:
                continue
            obligations += 1
            if not any(
                successor in family
                for successor in legal_successors(
                    neighborhoods, state, attacked
                )
            ):
                raise AssertionError(("unanswered family attack", state, attacked))

    per_color_kernel_sizes = {}
    for color in sorted(ROOT):
        color_ban = frozenset(
            ROOT - {color} | {vertex} for vertex in complement_link
        )
        color_kernel, _ = greatest_kernel(
            neighborhoods, 3, banned=color_ban
        )
        per_color_kernel_sizes[str(color)] = len(color_kernel)
    if per_color_kernel_sizes != {"0": 0, "1": 150, "10": 0}:
        raise AssertionError(per_color_kernel_sizes)

    edges = edge_list(neighborhoods)
    result = {
        "schema": "full-list-anchor-restoration-control-v1",
        "graph": {
            "graph6": GRAPH6,
            "graph6_ascii_sha256": sha256(GRAPH6.encode("ascii")).hexdigest(),
            "order": order,
            "size": len(edges),
            "edges": edges,
            "connected": _connected(neighborhoods),
        },
        "parameters": parameters,
        "theta_clique_partition": tuple(
            tuple(sorted(clique)) for clique in clique_partition
        ),
        "greatest_eternal_triple_family": {
            "states": len(family),
            "unoccupied_attack_obligations": obligations,
        },
        "full_list_setup": {
            "root": tuple(sorted(ROOT)),
            "target": TARGET,
            "target_palette": response_palette(
                neighborhoods, family, ROOT, TARGET
            ),
            "complement_link": tuple(sorted(complement_link)),
            "banned_color": COLOR,
            "restricted_kernel_states": len(restricted_kernel),
            "restricted_rank_counts": {
                str(rank): sum(value == rank for value in ranks.values())
                for rank in sorted(set(ranks.values()))
            },
            "all_color_kernel_sizes": per_color_kernel_sizes,
        },
        "attacked_secondary_row": {
            "predecessor": tuple(sorted(attacked_secondary_predecessor)),
            "rank": ranks[attacked_secondary_predecessor],
            "attack": ATTACKED,
            "selected_mover": MOVER,
            "selected_successor": tuple(sorted(first_selected)),
            "alternate_mover": TERMINAL,
            "alternate_successor": tuple(sorted(first_alternate)),
            "terminal_palette": response_palette(
                neighborhoods, family, ROOT, TERMINAL
            ),
            "alternate_dominates": dominates(
                neighborhoods, omitted_alternate
            ),
            "alternate_retained": omitted_alternate in family,
            "alternate_banned": omitted_alternate in ban,
        },
        "shared_secondary_row": {
            "predecessor": tuple(sorted(shared_secondary_predecessor)),
            "rank": ranks[shared_secondary_predecessor],
            "attack": SHARED,
            "selected_mover": MOVER,
            "selected_successor": tuple(sorted(second_selected)),
            "terminal_mover_edge": SHARED in neighborhoods[TERMINAL],
            "terminal_palette": response_palette(
                neighborhoods, family, ROOT, TERMINAL
            ),
            "mover_palette": response_palette(
                neighborhoods, family, ROOT, MOVER
            ),
            "common_alternate": tuple(sorted(omitted_alternate)),
            "common_alternate_dominates": dominates(
                neighborhoods, omitted_alternate
            ),
            "common_alternate_retained": omitted_alternate in family,
        },
    }
    if not result["graph"]["connected"]:
        raise AssertionError("the control graph is disconnected")
    return result


def _connected(
    neighborhoods: tuple[frozenset[int], ...],
) -> bool:
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in neighborhoods[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                frontier.append(neighbor)
    return len(reached) == len(neighborhoods)


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
