#!/usr/bin/env python3
"""Strict exact replay for the terminal-completion boundary controls."""

from __future__ import annotations

import hashlib
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
SPEC = importlib.util.spec_from_file_location("accepted_c157_core", DEPENDENCY)
if SPEC is None or SPEC.loader is None:
    raise AssertionError("could not load accepted C-157 verifier core")
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def graph6_encode(rows: tuple[int, ...]) -> str:
    order = len(rows)
    require(order <= 62, "short graph6 only")
    bits = [
        (rows[low] >> high) & 1
        for high in range(1, order)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = "".join(
        chr(
            63
            + sum(
                bits[offset + bit] << (5 - bit)
                for bit in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )
    return chr(63 + order) + payload


def graph_hash(rows: tuple[int, ...]) -> str:
    edges = [
        [first, second]
        for first in range(len(rows))
        for second in range(first + 1, len(rows))
        if rows[first] >> second & 1
    ]
    payload = json.dumps(edges, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def exact_independent_domination(rows: tuple[int, ...]) -> int:
    for size in range(1, len(rows) + 1):
        for state in CORE.masks_of_size(len(rows), size):
            if not CORE.independent(rows, state):
                continue
            if all(
                state >> vertex & 1 or rows[vertex] & state
                for vertex in range(len(rows))
            ):
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


def dominating_pairs(rows: tuple[int, ...]) -> list[list[int]]:
    return [
        list(pair)
        for pair in itertools.combinations(range(len(rows)), 2)
        if CORE.dominates(rows, CORE.vertex_mask(pair))
    ]


def completion_set(
    rows: tuple[int, ...],
    target: int,
    terminal: int,
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(rows))
        if vertex not in (target, terminal)
        and not (rows[target] >> vertex & 1)
        and not (rows[terminal] >> vertex & 1)
    )


def retained_moves(
    rows: tuple[int, ...],
    greatest: frozenset[int],
    state: int,
    attacked: int,
) -> tuple[tuple[int, int], ...]:
    result = []
    for guard in CORE.vertices(state):
        if not (rows[guard] >> attacked & 1):
            continue
        successor = state ^ (1 << guard) ^ (1 << attacked)
        if successor in greatest:
            result.append((guard, successor))
    return tuple(result)


def row_audit(
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
    expected_completions: tuple[int, ...],
) -> dict[str, object]:
    state = CORE.vertex_mask
    predecessor = state((v, t, q))
    terminal = state((v, t, r))
    secondary_root = state((u, t, r))
    alternate = state((t, q, r))
    witness_q = state((w, t, q))
    witness_r = state((w, t, r))
    transferred_root = state((u, t, w))

    ban = CORE.color_ban(rows, root, target, u)
    kernel, ranks, _ = CORE.greatest_kernel(rows, 3, ban)
    require(predecessor in greatest, ("predecessor absent", u))
    require(terminal in greatest, ("terminal absent", u))
    require(secondary_root in greatest, ("secondary root absent", u))
    require(witness_q in greatest, ("witness-q absent", u))
    require(witness_r in greatest, ("witness-r absent", u))
    require(transferred_root in greatest, ("transfer absent", u))
    require(ranks[predecessor] == 0, ("predecessor rank", u))
    require(
        r in CORE.deletion_witness_attacks(rows, predecessor, ban, ranks),
        ("wrong deletion witness", u),
    )
    require(not CORE.dominates(rows, alternate), ("alternate dominates", u))
    require(
        CORE.missed_vertices(rows, alternate) == (w,),
        ("wrong missed witness", u),
    )
    require(rows[u] >> w & 1, ("u-w edge missing", u))
    require(rows[v] >> w & 1, ("v-w edge missing", u))
    for missed in (t, q, r):
        require(not (rows[missed] >> w & 1), ("witness nonedge", u, missed))

    completions = completion_set(rows, target, r)
    require(completions == expected_completions, ("completion set", u, completions))
    completion_rows = []
    for d in completions:
        independent_completion = state((target, r, d))
        first_branch = state((d, t, r))
        second_branch = state((v, d, r))

        require(
            CORE.independent(rows, independent_completion),
            ("completion not independent", u, d),
        )
        require(
            independent_completion in greatest,
            ("independent completion absent", u, d),
        )

        moves = retained_moves(rows, greatest, terminal, d)
        expected_moves = []
        if first_branch in greatest and rows[v] >> d & 1:
            expected_moves.append((v, first_branch))
        if second_branch in greatest and rows[t] >> d & 1:
            expected_moves.append((t, second_branch))
        require(
            moves == tuple(sorted(expected_moves)),
            ("completion moves", u, d, moves),
        )
        require(moves, ("empty completion split", u, d))
        require(
            all(guard in (v, t) for guard, _ in moves),
            ("terminal moved", u, d),
        )

        first_survives = first_branch in greatest
        second_survives = second_branch in greatest
        if first_survives:
            require(
                d == w or rows[d] >> w & 1,
                ("closed witness incidence", u, d),
            )
            responders = tuple(
                guard
                for guard in CORE.vertices(first_branch)
                if rows[guard] >> target & 1
            )
            require(responders == (t,), ("first return not unique", u, d))
            require(
                first_branch ^ (1 << t) ^ (1 << target)
                == independent_completion,
                ("first return endpoint", u, d),
            )
            require(
                retained_moves(
                    rows, greatest, first_branch, target
                ) == ((t, independent_completion),),
                ("first retained return", u, d),
            )

        completion_rows.append(
            {
                "d": d,
                "first_branch_retained": first_survives,
                "second_branch_retained": second_survives,
                "closed_hit_on_witness": (
                    d == w or bool(rows[d] >> w & 1)
                ),
                "source_rank_first_branch": ranks.get(first_branch),
                "source_rank_independent_completion": ranks.get(
                    independent_completion
                ),
                "unique_return_guard": t if first_survives else None,
            }
        )

    return {
        "u": u,
        "v": v,
        "t": t,
        "q": q,
        "r": r,
        "w": w,
        "restricted_kernel_size": len(kernel),
        "predecessor_rank": ranks[predecessor],
        "terminal_palette": list(
            CORE.terminal_root_palette(rows, greatest, root, r)
        ),
        "completion_rows": completion_rows,
    }


def equality_control() -> dict[str, object]:
    graph6 = "OYifur}UO]}iTij]tpo]v"
    rows = CORE.decode_short_graph6(graph6)
    require(graph6_encode(rows) == graph6, "equality graph6 round trip")
    root_vertices = (0, 1, 10)
    root = CORE.vertex_mask(root_vertices)
    target = 6
    greatest, _, _ = CORE.greatest_kernel(rows, 3)
    require(
        CORE.terminal_root_palette(rows, greatest, root, target)
        == root_vertices,
        "equality target not full",
    )
    kernels = {
        color: len(
            CORE.greatest_kernel(
                rows,
                3,
                CORE.color_ban(rows, root, target, color),
            )[0]
        )
        for color in root_vertices
    }
    require(kernels == {0: 0, 1: 150, 10: 0}, ("equality kernels", kernels))

    checked = [
        row_audit(
            rows,
            greatest,
            root,
            target,
            u=0,
            v=1,
            t=10,
            q=14,
            r=11,
            w=8,
            expected_completions=(13,),
        ),
        row_audit(
            rows,
            greatest,
            root,
            target,
            u=10,
            v=0,
            t=1,
            q=12,
            r=5,
            w=4,
            expected_completions=(7, 9),
        ),
    ]
    for row in checked:
        for completion in row["completion_rows"]:
            require(
                completion["source_rank_first_branch"] == 0,
                ("expected rank-zero branch", row["u"], completion["d"]),
            )
            require(
                completion["source_rank_independent_completion"] == 3,
                ("expected rank-three completion", row["u"], completion["d"]),
            )
            require(
                completion["first_branch_retained"]
                and completion["second_branch_retained"],
                ("both equality branches should survive", row["u"]),
            )
    require(not dominating_pairs(rows), "equality graph has dominating pair")
    return {
        "graph6": graph6,
        "edge_list_sha256": graph_hash(rows),
        "parameters": parameters(rows),
        "greatest_family_size": len(greatest),
        "restricted_kernel_sizes": kernels,
        "rows": checked,
        "dominating_pairs": [],
    }


def gamma_two_all_completed_control() -> dict[str, object]:
    graph6 = "JEhbtj{rvu?"
    rows = CORE.decode_short_graph6(graph6)
    require(graph6_encode(rows) == graph6, "gamma-two graph6 round trip")
    base = CORE.decode_short_graph6("IEhbtj{ro")
    require(
        tuple(row & ((1 << 10) - 1) for row in rows[:10]) == base,
        "not the claimed MMV-001 extension",
    )
    require(
        tuple(CORE.vertices(rows[10])) == (0, 1, 2, 3, 4, 6, 7),
        "wrong extension neighborhood",
    )
    root_vertices = (0, 1, 2)
    root = CORE.vertex_mask(root_vertices)
    target = 8
    greatest, _, _ = CORE.greatest_kernel(rows, 3)
    require(
        CORE.terminal_root_palette(rows, greatest, root, target)
        == root_vertices,
        "gamma-two target not full",
    )
    kernels = {
        color: len(
            CORE.greatest_kernel(
                rows,
                3,
                CORE.color_ban(rows, root, target, color),
            )[0]
        )
        for color in root_vertices
    }
    require(kernels == {0: 0, 1: 0, 2: 0}, ("gamma-two kernels", kernels))
    specifications = (
        dict(
            u=0,
            v=1,
            t=2,
            q=4,
            r=9,
            w=3,
            expected_completions=(10,),
        ),
        dict(
            u=1,
            v=2,
            t=0,
            q=3,
            r=6,
            w=5,
            expected_completions=(7,),
        ),
        dict(
            u=2,
            v=0,
            t=1,
            q=5,
            r=7,
            w=4,
            expected_completions=(6,),
        ),
    )
    checked = [
        row_audit(rows, greatest, root, target, **specification)
        for specification in specifications
    ]
    for row in checked:
        completion = row["completion_rows"][0]
        require(
            completion["first_branch_retained"]
            and completion["second_branch_retained"],
            ("both gamma-two branches", row["u"]),
        )
        require(
            completion["source_rank_first_branch"] == 0,
            ("gamma-two branch rank", row["u"]),
        )
        require(
            completion["source_rank_independent_completion"] == 3,
            ("gamma-two completion rank", row["u"]),
        )
    pairs = dominating_pairs(rows)
    require(pairs == [[1, 10], [5, 10]], ("gamma-two pairs", pairs))
    return {
        "graph6": graph6,
        "edge_list_sha256": graph_hash(rows),
        "new_vertex_neighbors": list(CORE.vertices(rows[10])),
        "parameters": parameters(rows),
        "greatest_family_size": len(greatest),
        "restricted_kernel_sizes": kernels,
        "rows": checked,
        "dominating_pairs": pairs,
    }


def gamma_two_full_terminal_control() -> dict[str, object]:
    graph6 = "HF~mdfj"
    rows = CORE.decode_short_graph6(graph6)
    require(graph6_encode(rows) == graph6, "full-terminal graph6 round trip")
    root_vertices = (0, 1, 2)
    root = CORE.vertex_mask(root_vertices)
    target = 3
    greatest, _, _ = CORE.greatest_kernel(rows, 3)
    require(
        CORE.terminal_root_palette(rows, greatest, root, target)
        == root_vertices,
        "full-terminal target not full",
    )
    require(
        CORE.terminal_root_palette(rows, greatest, root, 5)
        == root_vertices,
        "terminal palette not full",
    )
    kernels = {
        color: len(
            CORE.greatest_kernel(
                rows,
                3,
                CORE.color_ban(rows, root, target, color),
            )[0]
        )
        for color in root_vertices
    }
    require(kernels == {0: 68, 1: 65, 2: 65}, ("full-terminal kernels", kernels))
    first = row_audit(
        rows,
        greatest,
        root,
        target,
        u=0,
        v=1,
        t=2,
        q=4,
        r=5,
        w=6,
        expected_completions=(8,),
    )
    second = row_audit(
        rows,
        greatest,
        root,
        target,
        u=0,
        v=2,
        t=1,
        q=4,
        r=5,
        w=7,
        expected_completions=(8,),
    )
    require(first["w"] != second["w"], "witnesses collide")
    first_completion = first["completion_rows"][0]
    second_completion = second["completion_rows"][0]
    require(
        first_completion["first_branch_retained"]
        and second_completion["first_branch_retained"],
        "symmetric branches do not both survive",
    )
    require(rows[8] >> 6 & 1 and rows[8] >> 7 & 1, "overlap hits missing")
    return {
        "graph6": graph6,
        "edge_list_sha256": graph_hash(rows),
        "parameters": parameters(rows),
        "greatest_family_size": len(greatest),
        "restricted_kernel_sizes": kernels,
        "terminal_palette": list(
            CORE.terminal_root_palette(rows, greatest, root, 5)
        ),
        "first_secondary_row": first,
        "second_secondary_row": second,
        "dominating_pairs": dominating_pairs(rows),
    }


def main() -> None:
    result = {
        "schema": "full-list-terminal-completion-controls-v1",
        "model": (
            "unoccupied attacks; exactly one occupied guard moves along one "
            "G-edge; every retained successor remains in the family"
        ),
        "equality_rank_reversal": equality_control(),
        "gamma_two_all_completed": gamma_two_all_completed_control(),
        "gamma_two_full_terminal": gamma_two_full_terminal_control(),
        "scope": (
            "exact finite controls for the human theorem in NOTE.md; no "
            "safe-color theorem, complete k=3 result, or conjecture resolution"
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
