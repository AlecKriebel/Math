#!/usr/bin/env python3
"""Strict replay for the two boundary controls and finite color map."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEPENDENCY = (
    HERE.parent
    / "full_list_nonsingleton_terminal"
    / "verify_cyclic_corridor_control.py"
)
SPEC = importlib.util.spec_from_file_location("accepted_control_core", DEPENDENCY)
if SPEC is None or SPEC.loader is None:
    raise AssertionError("could not load frozen accepted verifier")
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def exact_independent_domination(rows: tuple[int, ...]) -> int:
    for size in range(1, len(rows) + 1):
        for state in CORE.masks_of_size(len(rows), size):
            if not CORE.independent(rows, state):
                continue
            maximal = all(
                state >> vertex & 1 or rows[vertex] & state
                for vertex in range(len(rows))
            )
            if maximal:
                return size
    raise AssertionError("no maximal independent set")


def parameters(rows: tuple[int, ...]) -> dict[str, int]:
    return {
        "gamma": CORE.exact_gamma(rows),
        "i": exact_independent_domination(rows),
        "alpha": CORE.exact_alpha(rows),
        "gamma_infinity": CORE.exact_eternal_number(rows),
        "theta": CORE.exact_chromatic(CORE.complement_rows(rows)),
    }


def check_row(
    rows: tuple[int, ...],
    greatest: frozenset[int],
    root: int,
    target: int,
    *,
    u: int,
    v: int,
    t: int,
    q: int,
    r: int,
    w: int,
) -> dict[str, object]:
    ban = CORE.color_ban(rows, root, target, u)
    kernel, ranks, _ = CORE.greatest_kernel(rows, 3, ban)
    state = CORE.vertex_mask
    predecessor = state((v, t, q))
    terminal = state((v, t, r))
    secondary_root = state((u, t, r))
    alternate = state((t, q, r))
    witness_q = state((w, t, q))
    witness_r = state((w, t, r))
    transferred_root = state((u, t, w))

    require(predecessor in greatest, ("predecessor absent", u))
    require(terminal in greatest, ("terminal absent", u))
    require(secondary_root in greatest, ("secondary root absent", u))
    require(witness_q in greatest, ("witness-q state absent", u))
    require(witness_r in greatest, ("witness-r state absent", u))
    require(transferred_root in greatest, ("transfer state absent", u))
    require(ranks[predecessor] == 0, ("predecessor not rank zero", u))
    require(
        r in CORE.deletion_witness_attacks(rows, predecessor, ban, ranks),
        ("terminal attack is not a deletion witness", u),
    )
    require(not CORE.dominates(rows, alternate), ("alternate dominates", u))
    require(CORE.missed_vertices(rows, alternate) == (w,), ("wrong witness", u))
    require(r in CORE.complement_neighbors(rows, target), ("r outside B", u))
    require(q not in CORE.complement_neighbors(rows, target), ("q inside B", u))

    palette_q = CORE.terminal_root_palette(rows, greatest, root, q)
    palette_r = CORE.terminal_root_palette(rows, greatest, root, r)
    palette_w = CORE.terminal_root_palette(rows, greatest, root, w)
    require(u in palette_q, ("primary missing at q", u))
    require({u, v} <= set(palette_r), ("terminal palette", u, palette_r))
    require(v not in palette_q, ("control should use witness transfer", u))
    require(v in palette_w, ("secondary missing at witness", u))

    defenders_from_predecessor = tuple(
        guard
        for guard in CORE.vertices(predecessor)
        if rows[guard] >> w & 1
    )
    defenders_from_secondary = tuple(
        guard
        for guard in CORE.vertices(secondary_root)
        if rows[guard] >> w & 1
    )
    require(defenders_from_predecessor == (v,), ("first move not unique", u))
    require(defenders_from_secondary == (u,), ("second move not unique", u))
    require(
        predecessor ^ (1 << v) ^ (1 << w) == witness_q,
        ("first endpoint", u),
    )
    require(
        secondary_root ^ (1 << u) ^ (1 << w) == witness_r,
        ("second endpoint", u),
    )

    responders_at_u = tuple(
        guard
        for guard in CORE.vertices(witness_q)
        if rows[guard] >> u & 1
    )
    require(set(responders_at_u) == {w, q}, ("transfer responders", u))
    require(
        witness_q ^ (1 << q) ^ (1 << u) == transferred_root,
        ("transfer endpoint", u),
    )

    return {
        "color": u,
        "secondary": v,
        "mover": q,
        "terminal": r,
        "witness": w,
        "restricted_kernel_size": len(kernel),
        "predecessor_rank": ranks[predecessor],
        "palette_q": list(palette_q),
        "palette_r": list(palette_r),
        "palette_w": list(palette_w),
        "missed_by_alternate": list(CORE.missed_vertices(rows, alternate)),
    }


def color_map_audit() -> dict[str, int]:
    maps = []
    for images in itertools.product(range(3), repeat=3):
        if any(images[index] == index for index in range(3)):
            continue
        visited = set()
        cursor = 0
        while cursor not in visited:
            visited.add(cursor)
            cursor = images[cursor]
        cycle_length = 1
        probe = images[cursor]
        while probe != cursor:
            cycle_length += 1
            probe = images[probe]
        maps.append(cycle_length)
    require(len(maps) == 8, "wrong fixed-point-free map count")
    require(maps.count(3) == 2, "wrong 3-cycle count")
    require(maps.count(2) == 6, "wrong 2-cycle count")
    return {
        "fixed_point_free_maps": len(maps),
        "directed_3_cycles": maps.count(3),
        "two_cycle_with_tail": maps.count(2),
    }


def equality_control() -> dict[str, object]:
    rows = CORE.decode_short_graph6("OYifur}UO]}iTij]tpo]v")
    root_vertices = (0, 1, 10)
    root = CORE.vertex_mask(root_vertices)
    target = 6
    greatest, _, _ = CORE.greatest_kernel(rows, 3)
    require(
        CORE.terminal_root_palette(rows, greatest, root, target)
        == root_vertices,
        "target not full",
    )
    kernels = {
        color: len(CORE.greatest_kernel(
            rows, 3, CORE.color_ban(rows, root, target, color)
        )[0])
        for color in root_vertices
    }
    require(kernels == {0: 0, 1: 150, 10: 0}, ("kernel sizes", kernels))

    rows_checked = [
        check_row(
            rows, greatest, root, target,
            u=0, v=1, t=10, q=14, r=11, w=8,
        ),
        check_row(
            rows, greatest, root, target,
            u=10, v=0, t=1, q=12, r=5, w=4,
        ),
    ]

    safe_predecessor = CORE.vertex_mask((0, 3, 10))
    safe_alternate = CORE.vertex_mask((0, 3, 7))
    safe_kernel = CORE.greatest_kernel(
        rows, 3, CORE.color_ban(rows, root, target, 1)
    )[0]
    require(safe_predecessor in safe_kernel, "safe predecessor absent")
    require(safe_alternate in safe_kernel, "safe alternate absent")
    require(CORE.dominates(rows, safe_alternate), "safe alternate nondominating")
    terminal_palettes = {
        vertex: list(CORE.terminal_root_palette(rows, greatest, root, vertex))
        for vertex in (11, 7, 5)
    }
    require(
        terminal_palettes == {
            11: [0, 1],
            7: [1, 10],
            5: [0, 10],
        },
        ("terminal cycle", terminal_palettes),
    )
    return {
        "graph6": "OYifur}UO]}iTij]tpo]v",
        "parameters": parameters(rows),
        "greatest_family_size": len(greatest),
        "restricted_kernel_sizes": kernels,
        "terminal_palettes": terminal_palettes,
        "rank_zero_transfer_rows": rows_checked,
        "safe_color": 1,
        "safe_secondary_alternate": [0, 3, 7],
    }


def gamma_two_control() -> dict[str, object]:
    rows = CORE.decode_short_graph6("IEhbtj{ro")
    root_vertices = (0, 1, 2)
    root = CORE.vertex_mask(root_vertices)
    target = 8
    greatest, _, _ = CORE.greatest_kernel(rows, 3)
    require(
        CORE.terminal_root_palette(rows, greatest, root, target)
        == root_vertices,
        "MMV target not full",
    )
    kernels = {
        color: len(CORE.greatest_kernel(
            rows, 3, CORE.color_ban(rows, root, target, color)
        )[0])
        for color in root_vertices
    }
    require(kernels == {0: 0, 1: 0, 2: 0}, ("MMV kernels", kernels))
    specifications = (
        dict(u=0, v=1, t=2, q=4, r=9, w=3),
        dict(u=1, v=2, t=0, q=3, r=6, w=5),
        dict(u=2, v=0, t=1, q=5, r=7, w=4),
    )
    rows_checked = [
        check_row(rows, greatest, root, target, **specification)
        for specification in specifications
    ]
    dominating_pairs = [
        list(pair)
        for pair in itertools.combinations(range(len(rows)), 2)
        if CORE.dominates(
            rows,
            (1 << pair[0]) | (1 << pair[1]),
        )
    ]
    require(dominating_pairs == [[8, 9]], ("dominating pairs", dominating_pairs))
    require(
        [row["witness"] for row in rows_checked]
        == [rows_checked[1]["mover"], rows_checked[2]["mover"], rows_checked[0]["mover"]],
        "witness-mover cycle failed",
    )
    return {
        "graph6": "IEhbtj{ro",
        "parameters": parameters(rows),
        "greatest_family_size": len(greatest),
        "restricted_kernel_sizes": kernels,
        "rank_zero_transfer_rows": rows_checked,
        "dominating_pairs": dominating_pairs,
    }


def main() -> None:
    result = {
        "schema": "full-list-three-color-coupling-controls-v1",
        "model": (
            "unoccupied attacks; exactly one occupied guard moves along one "
            "G-edge; every retained successor remains in the family"
        ),
        "color_maps": color_map_audit(),
        "equality_control": equality_control(),
        "gamma_two_control": gamma_two_control(),
        "scope": (
            "finite controls and color-map count only; the human theorem is "
            "proved in NOTE.md; no safe-color existence or complete k=3"
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
