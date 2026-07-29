#!/usr/bin/env python3
"""Exact replay of the supported-pair-fan boundary controls."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
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


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def state(vertices: tuple[int, ...]) -> int:
    return CORE.vertex_mask(vertices)


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
            + sum(bits[offset + bit] << (5 - bit) for bit in range(6))
        )
        for offset in range(0, len(bits), 6)
    )
    return chr(63 + order) + payload


def exact_i(rows: tuple[int, ...]) -> int:
    for size in range(1, len(rows) + 1):
        for candidate in CORE.masks_of_size(len(rows), size):
            if CORE.independent(rows, candidate) and CORE.dominates(
                rows, candidate
            ):
                return size
    raise AssertionError("independent domination number absent")


def parameters(rows: tuple[int, ...]) -> tuple[int, int, int, int, int]:
    return (
        CORE.exact_gamma(rows),
        exact_i(rows),
        CORE.exact_alpha(rows),
        CORE.exact_eternal_number(rows),
        CORE.exact_chromatic(CORE.complement_rows(rows)),
    )


def edge_hash(rows: tuple[int, ...]) -> str:
    edges = [
        [first, second]
        for first in range(len(rows))
        for second in range(first + 1, len(rows))
        if rows[first] >> second & 1
    ]
    return hashlib.sha256(
        json.dumps(edges, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def common_missed(
    rows: tuple[int, ...], first: int, second: int
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
    source: int,
    attack: int,
) -> tuple[tuple[int, int], ...]:
    result = []
    for guard in CORE.vertices(source):
        if not (rows[guard] >> attack & 1):
            continue
        successor = source ^ (1 << guard) ^ (1 << attack)
        if successor in family:
            result.append((guard, successor))
    return tuple(result)


def active(
    rows: tuple[int, ...],
    family: frozenset[int],
    source_guard: int,
    target: int,
) -> bool:
    if not (rows[source_guard] >> target & 1):
        return False
    for source in CORE.masks_of_size(len(rows), 3):
        if (
            source not in family
            or not CORE.independent(rows, source)
            or not (source >> source_guard & 1)
            or source >> target & 1
        ):
            continue
        successor = source ^ (1 << source_guard) ^ (1 << target)
        if successor in family:
            return True
    return False


def audit_case(
    rows: tuple[int, ...],
    family: frozenset[int],
    *,
    root_vertices: tuple[int, int, int],
    target: int,
    terminal: int,
    completion: int,
    fixed_anchor: int,
    expected_witnesses: tuple[int, ...],
    expected_trapped: tuple[int, ...],
    expected_cross_dominates: bool,
    expected_cross_retained: bool,
) -> dict[str, object]:
    root = state(root_vertices)
    require(CORE.independent(rows, root), "root not independent")
    require(root in family, "root absent")
    require(
        CORE.terminal_root_palette(rows, family, root, target)
        == root_vertices,
        "target not full",
    )

    B = frozenset(CORE.complement_neighbors(rows, target))
    require(terminal in B, "terminal not in B")
    require(completion in B, "completion does not miss target")
    require(
        not (rows[terminal] >> completion & 1),
        "completion does not miss terminal",
    )

    independent_completion = state((target, terminal, completion))
    branch = state((completion, fixed_anchor, terminal))
    cross = state((target, completion, fixed_anchor))
    require(
        CORE.independent(rows, independent_completion),
        "completion triple not independent",
    )
    require(independent_completion in family, "completion triple absent")
    require(branch in family, "branch absent")

    witnesses = common_missed(rows, completion, fixed_anchor)
    trapped = tuple(vertex for vertex in witnesses if vertex in B)
    require(witnesses == expected_witnesses, ("witnesses", witnesses))
    require(trapped == expected_trapped, ("trapped", trapped))

    fan_states = []
    unique_moves = []
    for witness in witnesses:
        fan = state((completion, fixed_anchor, witness))
        require(fan in family, ("fan state absent", witness))
        fan_states.append(CORE.vertices(fan))
        if witness == terminal:
            require(fan == branch, "terminal collision is not branch")
            continue
        require(
            rows[terminal] >> witness & 1,
            ("terminal does not hit fan witness", witness),
        )
        moves = retained_moves(rows, family, branch, witness)
        require(
            moves == ((terminal, fan),),
            ("fan move not unique", witness, moves),
        )
        unique_moves.append(
            {
                "attack": witness,
                "guard": terminal,
                "successor": CORE.vertices(fan),
            }
        )

    for first, second in itertools.combinations(witnesses, 2):
        require(rows[first] >> second & 1, "witness fan not a clique")

    cross_dominates = CORE.dominates(rows, cross)
    require(
        cross_dominates == expected_cross_dominates,
        ("cross domination", cross_dominates),
    )
    require(
        (cross in family) == expected_cross_retained,
        ("cross retention", cross in family),
    )
    require(
        cross_dominates == (not trapped),
        "domination/trapped equivalence failed",
    )

    reciprocal = None
    independent_reverse_sources = []
    if trapped:
        require(active(rows, family, target, fixed_anchor), "x->t inactive")
        require(active(rows, family, fixed_anchor, target), "t->x inactive")
        reciprocal = True
        for witness in trapped:
            reverse_source = state((target, completion, witness))
            fan = state((completion, fixed_anchor, witness))
            require(
                CORE.independent(rows, reverse_source),
                ("reverse source not independent", witness),
            )
            require(reverse_source in family, "independent source absent")
            require(
                (
                    target,
                    fan,
                )
                in retained_moves(
                    rows, family, reverse_source, fixed_anchor
                ),
                ("named reverse response absent", witness),
            )
            independent_reverse_sources.append(CORE.vertices(reverse_source))

    return {
        "root": list(root_vertices),
        "target": target,
        "terminal": terminal,
        "completion": completion,
        "fixed_anchor": fixed_anchor,
        "pair_witnesses": list(witnesses),
        "trapped_witnesses": list(trapped),
        "fan_states": [list(vertices) for vertices in fan_states],
        "unique_fan_moves": unique_moves,
        "cross_state": list(CORE.vertices(cross)),
        "cross_dominates": cross_dominates,
        "cross_retained": cross in family,
        "reciprocal_target_anchor": reciprocal,
        "independent_reverse_sources": [
            list(vertices) for vertices in independent_reverse_sources
        ],
    }


def equality_control() -> dict[str, object]:
    graph6 = "OYifur}UO]}iTij]tpo]v"
    rows = CORE.decode_short_graph6(graph6)
    require(graph6_encode(rows) == graph6, "equality graph6 round trip")
    family, _, _ = CORE.greatest_kernel(rows, 3)
    require(parameters(rows) == (3, 3, 3, 3, 3), "equality parameters")
    require(len(family) == 304, "equality family size")

    cases = {
        "nondominating_reciprocal": audit_case(
            rows,
            family,
            root_vertices=(0, 1, 10),
            target=6,
            terminal=5,
            completion=7,
            fixed_anchor=1,
            expected_witnesses=(5, 14),
            expected_trapped=(5,),
            expected_cross_dominates=False,
            expected_cross_retained=False,
        ),
        "dominating_retained": audit_case(
            rows,
            family,
            root_vertices=(0, 1, 10),
            target=6,
            terminal=5,
            completion=7,
            fixed_anchor=0,
            expected_witnesses=(12,),
            expected_trapped=(),
            expected_cross_dominates=True,
            expected_cross_retained=True,
        ),
        "dominating_omitted": audit_case(
            rows,
            family,
            root_vertices=(1, 13, 14),
            target=12,
            terminal=2,
            completion=7,
            fixed_anchor=1,
            expected_witnesses=(5, 14),
            expected_trapped=(),
            expected_cross_dominates=True,
            expected_cross_retained=False,
        ),
    }
    return {
        "graph6": graph6,
        "edge_list_sha256": edge_hash(rows),
        "parameters": {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "greatest_family_size": len(family),
        "cases": cases,
    }


def gamma_two_control() -> dict[str, object]:
    graph6 = "HF~mdfj"
    rows = CORE.decode_short_graph6(graph6)
    require(graph6_encode(rows) == graph6, "gamma-two graph6 round trip")
    family, _, _ = CORE.greatest_kernel(rows, 3)
    require(parameters(rows) == (2, 2, 3, 3, 3), "gamma-two parameters")
    branch_vertices = (2, 5, 8)
    branch = state(branch_vertices)
    require(branch in family, "gamma-two branch absent")
    witnesses = common_missed(rows, 2, 8)
    require(witnesses == (), ("gamma-two pair not dominating", witnesses))
    return {
        "graph6": graph6,
        "edge_list_sha256": edge_hash(rows),
        "parameters": {
            "gamma": 2,
            "i": 2,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "greatest_family_size": len(family),
        "retained_branch": list(branch_vertices),
        "pair": [2, 8],
        "pair_witnesses": [],
    }


def main() -> None:
    result = {
        "schema": "supported-pair-completion-fan-controls-v1",
        "model": (
            "unoccupied attacks; exactly one occupied guard moves along one "
            "G-edge; every retained successor remains in the family"
        ),
        "equality": equality_control(),
        "gamma_two_boundary": gamma_two_control(),
        "scope": (
            "exact controls for the candidate human theorem; no safe-color, "
            "complete-k3, finite-exclusion, or conjecture-resolution claim"
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
