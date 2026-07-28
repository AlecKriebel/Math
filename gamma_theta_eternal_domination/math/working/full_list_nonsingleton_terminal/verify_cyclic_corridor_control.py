#!/usr/bin/env python3
"""Clean replay of the cyclic nonsingleton-corridor equality control.

This verifier imports no campaign graph, parameter, transition, or kernel
code.  Graphs and configurations are integer bit masks, and every quantity
used by the candidate note is recomputed directly from the one-guard game.

The certified graph realizes three simultaneous cyclic doubleton corridor
rows.  Two are genuine final rows of decreasing-rank traces for annihilated
restricted kernels.  The third restricted kernel survives because its
secondary root-color response is a dominating state in that kernel.
Consequently this is a boundary control for rank-free/static elimination,
not an example with all three restricted kernels empty.
"""

from __future__ import annotations

import itertools
import json


GRAPH6 = "OQifur}UO]}iTij]tpo}v"
ROOT_VERTICES = (0, 1, 10)
TARGET = 6

# color: (approach attack / corridor mover, terminal attack / vertex,
#         predecessor, terminal state, secondary root color,
#         secondary-response state)
ROW_SPECS = {
    0: {
        "mover": 14,
        "terminal_vertex": 11,
        "predecessor": (1, 10, 14),
        "terminal": (1, 10, 11),
        "secondary_color": 1,
        "secondary_response": (10, 11, 14),
        "missed_vertex": 8,
    },
    1: {
        "mover": 3,
        "terminal_vertex": 7,
        "predecessor": (0, 3, 10),
        "terminal": (0, 7, 10),
        "secondary_color": 10,
        "secondary_response": (0, 3, 7),
        "missed_vertex": None,
    },
    10: {
        "mover": 12,
        "terminal_vertex": 5,
        "predecessor": (0, 1, 12),
        "terminal": (0, 1, 5),
        "secondary_color": 0,
        "secondary_response": (1, 5, 12),
        "missed_vertex": 4,
    },
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def decode_short_graph6(record: str) -> tuple[int, ...]:
    """Decode a canonical graph6 record with a one-byte order header."""

    require(bool(record), "empty graph6 record")
    order = ord(record[0]) - 63
    require(0 <= order <= 62, "only short graph6 records are supported")
    payload_bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 payload character")
        payload_bits.extend(
            (value >> shift) & 1
            for shift in range(5, -1, -1)
        )
    needed = order * (order - 1) // 2
    padded = ((needed + 5) // 6) * 6
    require(len(payload_bits) == padded, "noncanonical graph6 payload length")
    require(not any(payload_bits[needed:]), "nonzero graph6 padding")

    rows = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if payload_bits[cursor]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            cursor += 1
    require(
        all(not (row >> vertex & 1) for vertex, row in enumerate(rows)),
        "decoded loop",
    )
    require(
        all(
            (rows[first] >> second & 1) == (rows[second] >> first & 1)
            for first in range(order)
            for second in range(order)
        ),
        "decoded adjacency is not symmetric",
    )
    return tuple(rows)


def vertex_mask(items: tuple[int, ...]) -> int:
    require(len(items) == len(set(items)), ("repeated vertex", items))
    return sum(1 << vertex for vertex in items)


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(mask.bit_length())
        if mask >> vertex & 1
    )


def masks_of_size(order: int, size: int):
    for items in itertools.combinations(range(order), size):
        yield vertex_mask(items)


def covered_mask(rows: tuple[int, ...], state: int) -> int:
    covered = state
    for vertex in vertices(state):
        covered |= rows[vertex]
    return covered


def dominates(rows: tuple[int, ...], state: int) -> bool:
    return covered_mask(rows, state) == (1 << len(rows)) - 1


def missed_vertices(rows: tuple[int, ...], state: int) -> tuple[int, ...]:
    return vertices(((1 << len(rows)) - 1) ^ covered_mask(rows, state))


def independent(rows: tuple[int, ...], state: int) -> bool:
    return all(
        not rows[vertex] & (state ^ (1 << vertex))
        for vertex in vertices(state)
    )


def successor_moves(
    rows: tuple[int, ...],
    state: int,
    attacked: int,
) -> tuple[tuple[int, int], ...]:
    """Return (moving guard, one-swap successor) for every legal edge move."""

    require(not (state >> attacked & 1), ("occupied attack", vertices(state), attacked))
    return tuple(
        (
            guard,
            state ^ (1 << guard) ^ (1 << attacked),
        )
        for guard in vertices(state & rows[attacked])
    )


def greatest_kernel(
    rows: tuple[int, ...],
    size: int,
    banned: frozenset[int] = frozenset(),
) -> tuple[frozenset[int], dict[int, int], tuple[int, ...]]:
    """Synchronous greatest-fixed-point peeling for the one-guard game."""

    active = {
        state
        for state in masks_of_size(len(rows), size)
        if state not in banned and dominates(rows, state)
    }
    ranks: dict[int, int] = {}
    round_sizes: list[int] = []
    rank = 0
    while True:
        deleted: set[int] = set()
        for state in active:
            for attacked in range(len(rows)):
                if state >> attacked & 1:
                    continue
                if not any(
                    successor in active
                    for _, successor in successor_moves(rows, state, attacked)
                ):
                    deleted.add(state)
                    break
        if not deleted:
            return frozenset(active), ranks, tuple(round_sizes)
        for state in deleted:
            ranks[state] = rank
        round_sizes.append(len(deleted))
        active.difference_update(deleted)
        rank += 1


def deletion_witness_attacks(
    rows: tuple[int, ...],
    state: int,
    banned: frozenset[int],
    ranks: dict[int, int],
) -> tuple[int, ...]:
    """Attacks witnessing synchronous deletion at the state's rank."""

    require(state in ranks, ("state has no deletion rank", vertices(state)))
    current_rank = ranks[state]
    witnesses: list[int] = []
    for attacked in range(len(rows)):
        if state >> attacked & 1:
            continue
        allowed = tuple(
            successor
            for _, successor in successor_moves(rows, state, attacked)
            if successor not in banned and dominates(rows, successor)
        )
        if all(
            successor in ranks and ranks[successor] < current_rank
            for successor in allowed
        ):
            witnesses.append(attacked)
    return tuple(witnesses)


def exact_gamma(rows: tuple[int, ...]) -> int:
    for size in range(1, len(rows) + 1):
        if any(
            dominates(rows, state)
            for state in masks_of_size(len(rows), size)
        ):
            return size
    raise AssertionError("graph has no dominating set")


def exact_alpha(rows: tuple[int, ...]) -> int:
    for size in range(len(rows), 0, -1):
        if any(
            independent(rows, state)
            for state in masks_of_size(len(rows), size)
        ):
            return size
    return 0


def complement_rows(rows: tuple[int, ...]) -> tuple[int, ...]:
    universe = (1 << len(rows)) - 1
    return tuple(
        universe ^ (1 << vertex) ^ rows[vertex]
        for vertex in range(len(rows))
    )


def colorable(rows: tuple[int, ...], color_count: int) -> bool:
    """Exact DSATUR-style backtracking, sufficient for this order-16 graph."""

    colors = [-1] * len(rows)

    def search(colored_count: int) -> bool:
        if colored_count == len(rows):
            return True
        uncolored = [
            vertex
            for vertex, color in enumerate(colors)
            if color < 0
        ]
        vertex = max(
            uncolored,
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
            if search(colored_count + 1):
                return True
            colors[vertex] = -1
        return False

    return search(0)


def exact_chromatic(rows: tuple[int, ...]) -> int:
    for color_count in range(1, len(rows) + 1):
        if colorable(rows, color_count):
            return color_count
    raise AssertionError("graph has no coloring")


def exact_eternal_number(rows: tuple[int, ...]) -> int:
    for size in range(1, len(rows) + 1):
        kernel, _, _ = greatest_kernel(rows, size)
        if kernel:
            return size
    raise AssertionError("graph has no eternal family")


def complement_neighbors(
    rows: tuple[int, ...],
    vertex: int,
) -> tuple[int, ...]:
    return tuple(
        other
        for other in range(len(rows))
        if other != vertex and not (rows[vertex] >> other & 1)
    )


def terminal_root_palette(
    rows: tuple[int, ...],
    greatest: frozenset[int],
    root: int,
    terminal_vertex: int,
) -> tuple[int, ...]:
    """Q(z)=L_S^{F*}(z), not the physical-link palette of C-139."""

    return tuple(
        color
        for color in vertices(root)
        if rows[color] >> terminal_vertex & 1
        and root ^ (1 << color) ^ (1 << terminal_vertex) in greatest
    )


def color_ban(
    rows: tuple[int, ...],
    root: int,
    target: int,
    color: int,
) -> frozenset[int]:
    base = root ^ (1 << color)
    return frozenset(
        base | (1 << terminal)
        for terminal in complement_neighbors(rows, target)
    )


def induced_complement_edges(
    rows: tuple[int, ...],
    subset: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for first, second in itertools.combinations(subset, 2)
        if not (rows[first] >> second & 1)
    )


def move_records(
    rows: tuple[int, ...],
    greatest: frozenset[int],
    kernel: frozenset[int],
    banned: frozenset[int],
    state: int,
    attacked: int,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for guard, successor in successor_moves(rows, state, attacked):
        records.append(
            {
                "mover": guard,
                "successor": list(vertices(successor)),
                "dominates": dominates(rows, successor),
                "missed_vertices": list(missed_vertices(rows, successor)),
                "in_unrestricted_greatest_family": successor in greatest,
                "in_color_ban": successor in banned,
                "in_restricted_kernel": successor in kernel,
            }
        )
    return records


def main() -> None:
    rows = decode_short_graph6(GRAPH6)
    order = len(rows)
    root = vertex_mask(ROOT_VERTICES)
    require(independent(rows, root), "root is not independent")
    require(not (root >> TARGET & 1), "target is occupied by the root")

    greatest, _, unrestricted_rounds = greatest_kernel(rows, 3)
    parameters = {
        "gamma": exact_gamma(rows),
        "alpha": exact_alpha(rows),
        "gamma_infinity": exact_eternal_number(rows),
        "theta": exact_chromatic(complement_rows(rows)),
    }
    require(
        parameters
        == {
            "gamma": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        ("wrong equality parameters", parameters),
    )
    require(len(greatest) == 304, ("wrong greatest-family size", len(greatest)))
    require(not unrestricted_rounds, ("unexpected unrestricted peeling", unrestricted_rounds))
    require(root in greatest, "root is not in the greatest eternal family")

    target_palette = terminal_root_palette(rows, greatest, root, TARGET)
    require(target_palette == ROOT_VERTICES, ("target is not full", target_palette))

    physical_link = complement_neighbors(rows, TARGET)
    physical_link_edges = induced_complement_edges(rows, physical_link)
    require(
        physical_link == (5, 7, 9, 11, 13),
        ("wrong physical link", physical_link),
    )
    require(
        physical_link_edges == ((5, 7), (5, 9), (11, 13)),
        ("wrong induced physical-link edges", physical_link_edges),
    )

    expected_palettes = {
        5: (0, 10),
        7: (1, 10),
        9: (1, 10),
        11: (0, 1),
        13: (0, 10),
    }
    actual_palettes = {
        terminal: terminal_root_palette(rows, greatest, root, terminal)
        for terminal in physical_link
    }
    require(
        actual_palettes == expected_palettes,
        ("wrong terminal root palettes", actual_palettes),
    )

    expected_kernels = {
        0: {
            "kernel_size": 0,
            "rounds": (26, 81, 132, 62),
            "start_rank": 1,
        },
        1: {
            "kernel_size": 150,
            "rounds": (28, 74, 49),
            "start_rank": None,
        },
        10: {
            "kernel_size": 0,
            "rounds": (29, 81, 128, 62),
            "start_rank": 1,
        },
    }

    kernels: dict[int, frozenset[int]] = {}
    bans: dict[int, frozenset[int]] = {}
    rank_maps: dict[int, dict[int, int]] = {}
    kernel_records: dict[str, object] = {}
    for color in ROOT_VERTICES:
        banned = color_ban(rows, root, TARGET, color)
        kernel, ranks, rounds = greatest_kernel(rows, 3, banned)
        start = (root ^ (1 << color)) | (1 << TARGET)
        expected = expected_kernels[color]
        require(
            len(kernel) == expected["kernel_size"],
            ("wrong restricted-kernel size", color, len(kernel)),
        )
        require(
            rounds == expected["rounds"],
            ("wrong restricted peeling", color, rounds),
        )
        require(
            ranks.get(start) == expected["start_rank"],
            ("wrong selected-start rank", color, ranks.get(start)),
        )
        require(
            (start in kernel) == (color == 1),
            ("wrong selected-start survival", color),
        )
        kernels[color] = kernel
        bans[color] = banned
        rank_maps[color] = ranks
        kernel_records[str(color)] = {
            "kernel_states": len(kernel),
            "deletion_rounds": list(rounds),
            "selected_start": list(vertices(start)),
            "selected_start_survives": start in kernel,
            "selected_start_rank": ranks.get(start),
        }

    # Full occupancy/collision audit for the named cyclic control.
    movers = tuple(int(ROW_SPECS[color]["mover"]) for color in ROOT_VERTICES)
    terminals = tuple(
        int(ROW_SPECS[color]["terminal_vertex"])
        for color in ROOT_VERTICES
    )
    rank_zero_missed = tuple(
        int(ROW_SPECS[color]["missed_vertex"])
        for color in (0, 10)
    )
    require(len(set(movers)) == 3, ("mover collision", movers))
    require(len(set(terminals)) == 3, ("terminal collision", terminals))
    require(
        not set(movers) & set(terminals),
        ("mover-terminal collision", movers, terminals),
    )
    require(
        not (set(movers) | set(terminals))
        & (set(ROOT_VERTICES) | {TARGET}),
        "root/target collision with a mover or terminal",
    )
    require(len(set(rank_zero_missed)) == 2, ("missed-witness collision", rank_zero_missed))
    require(
        not set(rank_zero_missed)
        & (set(ROOT_VERTICES) | {TARGET} | set(movers) | set(terminals)),
        "rank-zero missed witness collides with a named occupied vertex",
    )
    require(
        len(
            set(ROOT_VERTICES)
            | {TARGET}
            | set(movers)
            | set(terminals)
            | set(rank_zero_missed)
        )
        == 12,
        "the twelve named vertices are not pairwise distinct",
    )

    row_records: list[dict[str, object]] = []
    secondary_cycle: dict[int, int] = {}
    for color in ROOT_VERTICES:
        spec = ROW_SPECS[color]
        mover = int(spec["mover"])
        terminal_vertex = int(spec["terminal_vertex"])
        secondary_color = int(spec["secondary_color"])
        predecessor = vertex_mask(tuple(spec["predecessor"]))
        terminal = vertex_mask(tuple(spec["terminal"]))
        secondary_response = vertex_mask(tuple(spec["secondary_response"]))
        base = root ^ (1 << color)
        start = base | (1 << TARGET)
        banned = bans[color]
        kernel = kernels[color]
        ranks = rank_maps[color]

        require(
            predecessor == base | (1 << mover),
            ("wrong corridor predecessor occupancy", color),
        )
        require(
            terminal == base | (1 << terminal_vertex),
            ("wrong terminal occupancy", color),
        )
        require(mover not in physical_link, ("mover lies in physical link", color, mover))
        require(terminal_vertex in physical_link, ("terminal outside physical link", color))
        require(predecessor in greatest, ("predecessor not retained", color))
        require(terminal in greatest, ("terminal not retained", color))
        require(terminal in banned, ("terminal not in color ban", color))
        require(predecessor not in banned, ("predecessor lies in color ban", color))

        # The selected start reaches the named predecessor by moving the
        # target guard to the named corridor mover.
        approach_moves = successor_moves(rows, start, mover)
        require(
            (TARGET, predecessor) in approach_moves,
            ("missing selected-start approach", color, approach_moves),
        )

        terminal_moves = successor_moves(rows, predecessor, terminal_vertex)
        require(
            (mover, terminal) in terminal_moves,
            ("missing corridor terminal move", color, terminal_moves),
        )
        require(
            (secondary_color, secondary_response) in terminal_moves,
            ("missing secondary-color response", color, terminal_moves),
        )

        quartet = (TARGET, color, mover, terminal_vertex)
        require(len(set(quartet)) == 4, ("diamond collision", color, quartet))
        missing_quartet_edges = tuple(
            pair
            for pair in itertools.combinations(quartet, 2)
            if not (rows[pair[0]] >> pair[1] & 1)
        )
        require(
            missing_quartet_edges == ((TARGET, terminal_vertex),),
            ("corridor quartet is not the forced diamond", color, missing_quartet_edges),
        )

        palette = terminal_root_palette(rows, greatest, root, terminal_vertex)
        require(
            palette == tuple(sorted((color, secondary_color))),
            ("wrong cyclic doubleton palette", color, palette),
        )
        secondary_cycle[color] = secondary_color

        if color in (0, 10):
            require(not kernel, ("expected annihilated color", color))
            require(ranks[start] == 1, ("wrong approach-source rank", color))
            require(ranks[predecessor] == 0, ("wrong predecessor rank", color))
            require(
                mover in deletion_witness_attacks(rows, start, banned, ranks),
                ("approach is not a decreasing-rank witness", color),
            )
            require(
                deletion_witness_attacks(rows, predecessor, banned, ranks)
                == (terminal_vertex,),
                ("wrong final deletion-witness attack", color),
            )
            greatest_terminal_successors = tuple(
                successor
                for _, successor in terminal_moves
                if successor in greatest
            )
            require(
                greatest_terminal_successors == (terminal,),
                ("rank-zero row has another retained successor", color),
            )
            missed = missed_vertices(rows, secondary_response)
            require(
                missed == (int(spec["missed_vertex"]),),
                ("wrong private missed witness", color, missed),
            )
            require(
                rows[secondary_color] >> missed[0] & 1,
                ("private witness is not dominated by its secondary color", color),
            )
            require(
                secondary_response not in banned,
                ("secondary response unexpectedly banned", color),
            )
            require(
                not dominates(rows, secondary_response),
                ("secondary response unexpectedly dominates", color),
            )
            row_status = "rank_zero_annihilation_terminal"
        else:
            require(start in kernel, "safe selected start does not survive")
            require(predecessor in kernel, "safe predecessor does not survive")
            require(secondary_response in kernel, "secondary response is not safe")
            require(terminal not in kernel, "banned terminal entered safe kernel")
            greatest_terminal_successors = tuple(
                successor
                for _, successor in terminal_moves
                if successor in greatest
            )
            require(
                greatest_terminal_successors == (terminal, secondary_response),
                ("safe row has wrong retained responses", greatest_terminal_successors),
            )
            require(
                not missed_vertices(rows, secondary_response),
                "safe secondary response does not dominate",
            )
            row_status = "surviving_kernel_row"

        row_records.append(
            {
                "color": color,
                "status": row_status,
                "selected_start": list(vertices(start)),
                "approach_attack": mover,
                "predecessor": list(vertices(predecessor)),
                "predecessor_rank": ranks.get(predecessor),
                "terminal_attack": terminal_vertex,
                "corridor_mover": mover,
                "terminal": list(vertices(terminal)),
                "terminal_palette_Q": list(palette),
                "secondary_color": secondary_color,
                "secondary_response": list(vertices(secondary_response)),
                "secondary_response_missed_vertices": list(
                    missed_vertices(rows, secondary_response)
                ),
                "terminal_attack_moves": move_records(
                    rows,
                    greatest,
                    kernel,
                    banned,
                    predecessor,
                    terminal_vertex,
                ),
                "diamond": {
                    "vertices": list(quartet),
                    "unique_missing_edge": [TARGET, terminal_vertex],
                },
            }
        )

    require(
        secondary_cycle == {0: 1, 1: 10, 10: 0},
        ("secondary palettes are not cyclic", secondary_cycle),
    )

    result = {
        "schema": "full-list-nonsingleton-cyclic-corridor-control-v1",
        "scope": (
            "exact equality boundary for rank-free/static corridor elimination; "
            "only colors 0 and 10 have empty restricted kernels"
        ),
        "graph6": GRAPH6,
        "order": order,
        "size": sum(row.bit_count() for row in rows) // 2,
        "parameters": parameters,
        "greatest_eternal_triple_family_states": len(greatest),
        "greatest_family_deletion_rounds": list(unrestricted_rounds),
        "root": list(ROOT_VERTICES),
        "root_in_greatest_family": root in greatest,
        "target": TARGET,
        "target_palette_Q": list(target_palette),
        "physical_link_B": list(physical_link),
        "physical_link_H_edges": [list(edge) for edge in physical_link_edges],
        "terminal_root_palettes_Q": {
            str(vertex): list(palette)
            for vertex, palette in actual_palettes.items()
        },
        "restricted_kernels": kernel_records,
        "collision_audit": {
            "root_target_movers_terminals_rank_zero_witnesses_pairwise_distinct": True,
            "movers": list(movers),
            "terminals": list(terminals),
            "rank_zero_private_missed_witnesses": list(rank_zero_missed),
            "named_distinct_vertex_count": 12,
        },
        "cyclic_corridor_rows": row_records,
        "certified_boundary": {
            "genuine_rank_decreasing_terminal_colors": [0, 10],
            "surviving_color": 1,
            "surviving_kernel_states": len(kernels[1]),
            "reason_static_elimination_fails": (
                "the secondary color-10 response to the color-1 row is "
                "dominating and belongs to the restricted kernel"
            ),
            "all_three_restricted_kernels_empty": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
