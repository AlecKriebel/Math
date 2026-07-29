#!/usr/bin/env python3
"""Explore C-170 branch spokes in the frozen exact boundary controls.

This is a discovery script.  It imports the already reviewed bit-mask core,
reconstructs the literal greatest family, and reports every common-
nonneighbor spoke of each retained completion branch.  No output from this
script is a certificate or finite exclusion.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE_PATH = (
    HERE.parent
    / "full_list_nonsingleton_terminal"
    / "verify_cyclic_corridor_control.py"
)
SPEC = importlib.util.spec_from_file_location("accepted_c157_core", CORE_PATH)
if SPEC is None or SPEC.loader is None:
    raise AssertionError("could not load accepted C-157 verifier core")
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


def mask(vertices: tuple[int, ...]) -> int:
    return CORE.vertex_mask(vertices)


def common_missed(
    rows: tuple[int, ...],
    first: int,
    second: int,
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(rows))
        if vertex not in (first, second)
        and not (rows[first] >> vertex & 1)
        and not (rows[second] >> vertex & 1)
    )


def retained_moves(
    rows: tuple[int, ...],
    family: frozenset[int],
    state: int,
    attack: int,
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    moves = []
    for guard in CORE.vertices(state):
        if not (rows[guard] >> attack & 1):
            continue
        successor = state ^ (1 << guard) ^ (1 << attack)
        if successor in family:
            moves.append((guard, CORE.vertices(successor)))
    return tuple(moves)


def parameters(rows: tuple[int, ...]) -> tuple[int, int, int, int]:
    return (
        CORE.exact_gamma(rows),
        CORE.exact_alpha(rows),
        CORE.exact_eternal_number(rows),
        CORE.exact_chromatic(CORE.complement_rows(rows)),
    )


def audit_row(
    *,
    graph6: str,
    root_vertices: tuple[int, int, int],
    target: int,
    u: int,
    v: int,
    t: int,
    q: int,
    r: int,
    witness: int,
) -> dict[str, object]:
    rows = CORE.decode_short_graph6(graph6)
    family, _, _ = CORE.greatest_kernel(rows, 3)
    root = mask(root_vertices)
    terminal = mask((v, t, r))
    completions = common_missed(rows, target, r)
    records = []

    for d in completions:
        first = mask((d, t, r))
        if first not in family:
            continue
        spokes = []
        for e in common_missed(rows, d, t):
            spoke = mask((d, t, e))
            independent_start = mask((target, r, d))
            independent_end = mask((target, e, d))
            reverse = mask((target, d, t))
            spokes.append(
                {
                    "e": e,
                    "r_e_edge": bool(rows[r] >> e & 1),
                    "spoke_retained": spoke in family,
                    "unique_spoke_move": retained_moves(
                        rows, family, first, e
                    ),
                    "e_misses_target": not bool(rows[e] >> target & 1),
                    "independent_start": CORE.independent(
                        rows, independent_start
                    ),
                    "independent_end": CORE.independent(rows, independent_end),
                    "independent_end_retained": independent_end in family,
                    "reverse_retained": reverse in family,
                    "r_responds_to_t_at_start": any(
                        guard == r
                        for guard, _ in retained_moves(
                            rows, family, independent_start, t
                        )
                    ),
                    "e_responds_to_t_at_end": any(
                        guard == e
                        for guard, _ in retained_moves(
                            rows, family, independent_end, t
                        )
                    )
                    if CORE.independent(rows, independent_end)
                    else None,
                    "witness_e_edge": bool(rows[witness] >> e & 1),
                    "t_d_edge": bool(rows[t] >> d & 1),
                }
            )
        records.append(
            {
                "d": d,
                "d_equals_witness": d == witness,
                "d_witness_edge": bool(rows[d] >> witness & 1),
                "spokes": spokes,
            }
        )

    return {
        "graph6": graph6,
        "parameters_gamma_alpha_gamma_infinity_theta": parameters(rows),
        "root": root_vertices,
        "target": target,
        "source": u,
        "secondary": v,
        "third": t,
        "mover": q,
        "terminal": r,
        "witness": witness,
        "terminal_palette": CORE.terminal_root_palette(
            rows, family, root, r
        ),
        "completion_records": records,
    }


def search_completion_branches(graph6: str) -> list[dict[str, object]]:
    """Find retained branches over a full target and an independent completion."""
    rows = CORE.decode_short_graph6(graph6)
    if parameters(rows)[:3] != (3, 3, 3):
        return []
    family, _, _ = CORE.greatest_kernel(rows, 3)
    records = []
    order = len(rows)
    for root in CORE.masks_of_size(order, 3):
        if not CORE.independent(rows, root):
            continue
        root_vertices = CORE.vertices(root)
        for target in range(order):
            if root >> target & 1:
                continue
            if (
                CORE.terminal_root_palette(rows, family, root, target)
                != root_vertices
            ):
                continue
            B = frozenset(CORE.complement_neighbors(rows, target))
            for terminal in B:
                for d in common_missed(rows, target, terminal):
                    independent_completion = mask((target, terminal, d))
                    if independent_completion not in family:
                        continue
                    for fixed_anchor in root_vertices:
                        branch = mask((d, fixed_anchor, terminal))
                        if branch not in family:
                            continue
                        witnesses = common_missed(rows, d, fixed_anchor)
                        trapped = tuple(e for e in witnesses if e in B)
                        cross = mask((target, d, fixed_anchor))
                        records.append(
                            {
                                "root": root_vertices,
                                "target": target,
                                "terminal": terminal,
                                "terminal_palette": (
                                    CORE.terminal_root_palette(
                                        rows, family, root, terminal
                                    )
                                ),
                                "completion": d,
                                "fixed_anchor": fixed_anchor,
                                "witnesses": witnesses,
                                "trapped_witnesses": trapped,
                                "cross_dominates": CORE.dominates(rows, cross),
                                "cross_retained": cross in family,
                            }
                        )
    return records


def main() -> None:
    rows = [
        # Equality rank-reversal rows from accepted C-170.
        {
            "graph6": "OYifur}UO]}iTij]tpo]v",
            "root_vertices": (0, 1, 10),
            "target": 6,
            "u": 0,
            "v": 1,
            "t": 10,
            "q": 14,
            "r": 11,
            "witness": 8,
        },
        {
            "graph6": "OYifur}UO]}iTij]tpo]v",
            "root_vertices": (0, 1, 10),
            "target": 6,
            "u": 10,
            "v": 0,
            "t": 1,
            "q": 12,
            "r": 5,
            "witness": 4,
        },
        # Full-terminal overlap control: both secondary rows.
        {
            "graph6": "HF~mdfj",
            "root_vertices": (0, 1, 2),
            "target": 3,
            "u": 0,
            "v": 1,
            "t": 2,
            "q": 4,
            "r": 5,
            "witness": 6,
        },
        {
            "graph6": "HF~mdfj",
            "root_vertices": (0, 1, 2),
            "target": 3,
            "u": 0,
            "v": 2,
            "t": 1,
            "q": 4,
            "r": 5,
            "witness": 7,
        },
        # C-171 trapped-witness control and its opposite secondary row.
        {
            "graph6": "JEhbtnm~D]_",
            "root_vertices": (0, 5, 6),
            "target": 8,
            "u": 6,
            "v": 0,
            "t": 5,
            "q": 2,
            "r": 10,
            "witness": 3,
        },
        {
            "graph6": "JEhbtnm~D]_",
            "root_vertices": (0, 5, 6),
            "target": 8,
            "u": 6,
            "v": 5,
            "t": 0,
            "q": 2,
            "r": 10,
            "witness": 1,
        },
    ]
    equality_graphs = (
        "Ksv`f\\knJVis",
        "OYifur}UO]}iTij]tpo]v",
        "OQifur}UO]}iTij]tpo}v",
        "FCpbO",
        "EpQ?",
        "D]?",
    )
    result = {
        "schema": "completion-coupling-control-scan-v1",
        "status": "OBSERVED",
        "rows": [audit_row(**row) for row in rows],
        "equality_completion_branches": {
            graph6: search_completion_branches(graph6)
            for graph6 in equality_graphs
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
