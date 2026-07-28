#!/usr/bin/env python3
"""Bit-mask clean-room replay of the separated-port lollipop control."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
TARGET = CAMPAIGN / "math" / "working" / "full_list_odd_lollipop_integration" / "NOTE.md"
LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"
GRAPH6 = "HFzvvn{"
ORDER = 9
ANCHORS = (0, 1, 2)
ANCHOR_MASK = sum(1 << v for v in ANCHORS)
FULL = 3
DESIRED = {
    3: (0, 1, 2),
    4: (0, 1),
    5: (0, 1),
    6: (0, 1),
    7: (1, 2),
    8: (1, 2),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(text: str) -> tuple[int, ...]:
    n = ord(text[0]) - 63
    payload: list[int] = []
    for char in text[1:]:
        value = ord(char) - 63
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(payload) != ((needed + 5) // 6) * 6 or any(payload[needed:]):
        raise ValueError("bad graph6 padding")
    rows = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if payload[cursor]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            cursor += 1
    return tuple(rows)


G = decode_graph6(GRAPH6)
ALL = (1 << ORDER) - 1
H = tuple(ALL ^ G[v] ^ (1 << v) for v in range(ORDER))


def masks(size: int):
    for vertices in itertools.combinations(range(ORDER), size):
        yield sum(1 << v for v in vertices)


def dominates(state: int) -> bool:
    covered = state
    for guard in range(ORDER):
        if state & (1 << guard):
            covered |= G[guard]
    return covered == ALL


def independent(state: int) -> bool:
    return all(
        not (G[u] & (1 << v))
        for u, v in itertools.combinations(
            [w for w in range(ORDER) if state & (1 << w)],
            2,
        )
    )


def direct_swap(guard: int, target: int) -> int:
    return (ANCHOR_MASK ^ (1 << guard)) | (1 << target)


def restricted_kernel() -> tuple[frozenset[int], tuple[int, ...], frozenset[int]]:
    banned = frozenset(
        direct_swap(guard, target)
        for target, allowed in DESIRED.items()
        for guard in ANCHORS
        if guard not in allowed
    )
    active = {state for state in masks(3) if state not in banned and dominates(state)}
    rounds: list[int] = []
    while True:
        rejected: set[int] = set()
        for state in active:
            for attack in range(ORDER):
                attack_bit = 1 << attack
                if state & attack_bit:
                    continue
                guards = state & G[attack]
                if not any(
                    ((state ^ (1 << guard)) | attack_bit) in active
                    for guard in range(ORDER)
                    if guards & (1 << guard)
                ):
                    rejected.add(state)
                    break
        if not rejected:
            return frozenset(active), tuple(rounds), banned
        rounds.append(len(rejected))
        active.difference_update(rejected)


def audit_family(family: frozenset[int]) -> int:
    obligations = 0
    for state in family:
        assert dominates(state)
        for attack in range(ORDER):
            attack_bit = 1 << attack
            if state & attack_bit:
                continue
            obligations += 1
            guards = state & G[attack]
            assert any(
                ((state ^ (1 << guard)) | attack_bit) in family
                for guard in range(ORDER)
                if guards & (1 << guard)
            )
    return obligations


def response_lists(family: frozenset[int]) -> dict[int, tuple[int, ...]]:
    return {
        target: tuple(
            guard
            for guard in ANCHORS
            if G[guard] & (1 << target)
            and direct_swap(guard, target) in family
        )
        for target in range(ORDER)
        if target not in ANCHORS
    }


def exact_gamma() -> int:
    return next(size for size in range(1, ORDER + 1) if any(dominates(s) for s in masks(size)))


def exact_alpha() -> int:
    return next(
        size
        for size in range(ORDER, 0, -1)
        if any(independent(s) for s in masks(size))
    )


def greatest_family(size: int) -> frozenset[int]:
    active = {state for state in masks(size) if dominates(state)}
    while True:
        rejected = {
            state
            for state in active
            if any(
                not any(
                    G[attack] & (1 << guard)
                    and ((state ^ (1 << guard)) | (1 << attack)) in active
                    for guard in range(ORDER)
                    if state & (1 << guard)
                )
                for attack in range(ORDER)
                if not state & (1 << attack)
            )
        }
        if not rejected:
            return frozenset(active)
        active.difference_update(rejected)


def exact_eternal() -> int:
    return next(size for size in range(1, ORDER + 1) if greatest_family(size))


def colorable_h(color_count: int) -> bool:
    assigned = [-1] * ORDER

    def search(colored: int) -> bool:
        if colored == ORDER:
            return True
        vertices = [v for v in range(ORDER) if assigned[v] < 0]
        vertex = max(
            vertices,
            key=lambda v: (
                len({assigned[w] for w in range(ORDER) if H[v] & (1 << w) and assigned[w] >= 0}),
                H[v].bit_count(),
                -v,
            ),
        )
        for color in range(color_count):
            if any(
                assigned[w] == color
                for w in range(ORDER)
                if H[vertex] & (1 << w)
            ):
                continue
            assigned[vertex] = color
            if search(colored + 1):
                return True
            assigned[vertex] = -1
        return False

    return search(0)


def exact_theta() -> int:
    return next(k for k in range(1, ORDER + 1) if colorable_h(k))


def compatible_colorings(
    lists: dict[int, tuple[int, ...]],
    *,
    include_full: bool,
    full_color: int | None = None,
) -> tuple[dict[int, int], ...]:
    assigned = {anchor: anchor for anchor in ANCHORS}
    if include_full:
        assert full_color is not None
        assigned[FULL] = full_color
    vertices = [
        v
        for v in range(ORDER)
        if v not in ANCHORS and (not include_full or v != FULL) and v != FULL
    ]
    vertices.sort(key=lambda v: (len(lists[v]), -H[v].bit_count(), v))
    answers: list[dict[int, int]] = []

    def search(index: int) -> None:
        if index == len(vertices):
            answers.append(dict(sorted(assigned.items())))
            return
        vertex = vertices[index]
        for color in lists[vertex]:
            if any(
                H[vertex] & (1 << other) and other_color == color
                for other, other_color in assigned.items()
            ):
                continue
            assigned[vertex] = color
            search(index + 1)
            del assigned[vertex]

    search(0)
    return tuple(answers)


def orientation_formula() -> dict[str, object]:
    assignments = []
    for x_value, y_value in itertools.product((0, 1), repeat=2):
        colors = {
            4: 1 if x_value else 0,
            5: 0 if x_value else 1,
            6: 1 if x_value else 0,
            7: 2 if y_value else 1,
            8: 1 if y_value else 2,
        }
        proper = all(colors[u] != colors[v] for u, v in ((4, 7), (6, 8)))
        assignments.append(
            {
                "X": x_value,
                "Y": y_value,
                "colors": {str(v): c for v, c in colors.items()},
                "base_satisfies": proper,
                "augmentation_unit_X": x_value == 1,
                "augmented_satisfies": proper and x_value == 1,
            }
        )
    base = [[r["X"], r["Y"]] for r in assignments if r["base_satisfies"]]
    augmented = [[r["X"], r["Y"]] for r in assignments if r["augmented_satisfies"]]
    # Truth-table minimality of X & (!X or Y) & (!X or !Y).
    remove_unit_sat = any(
        (not x or y) and (not x or not y)
        for x, y in itertools.product((0, 1), repeat=2)
    )
    remove_first_sat = any(
        x and (not x or not y)
        for x, y in itertools.product((0, 1), repeat=2)
    )
    remove_second_sat = any(
        x and (not x or y)
        for x, y in itertools.product((0, 1), repeat=2)
    )
    return {
        "assignments": assignments,
        "base_satisfying_assignments": base,
        "augmented_satisfying_assignments": augmented,
        "clauses": ["not X or Y", "not X or not Y"],
        "augmentation": "X",
        "inclusion_minimal_unsatisfiable": (
            not augmented
            and remove_unit_sat
            and remove_first_sat
            and remove_second_sat
        ),
    }


def fan_embeddings(lists: dict[int, tuple[int, ...]]) -> list[dict[str, object]]:
    outside = set(range(ORDER)) - set(ANCHORS)
    found: list[dict[str, object]] = []
    for color in ANCHORS:
        for p, q in itertools.permutations(outside, 2):
            if color not in lists[p] or not (H[p] & (1 << q)):
                continue
            remaining = outside - {p, q}
            for vertex_count in range(2, len(remaining) + 1, 2):
                for path in itertools.permutations(remaining, vertex_count):
                    if any(color in lists[v] for v in path):
                        continue
                    if not (H[q] & (1 << path[0]) and H[q] & (1 << path[-1])):
                        continue
                    if all(H[path[i]] & (1 << path[i + 1]) for i in range(len(path) - 1)):
                        found.append(
                            {"color": color, "p": p, "q": q, "path": list(path)}
                        )
    return found


def main() -> int:
    expected_h_edges = {
        (0, 1), (0, 2), (1, 2), (3, 4), (4, 5),
        (5, 6), (6, 8), (7, 8), (4, 7),
    }
    actual_h_edges = {
        (u, v)
        for u in range(ORDER)
        for v in range(u + 1, ORDER)
        if H[u] & (1 << v)
    }
    assert actual_h_edges == expected_h_edges
    family, rounds, banned = restricted_kernel()
    obligations = audit_family(family)
    lists = response_lists(family)
    assert lists == DESIRED
    formula = orientation_formula()
    base_colorings = compatible_colorings(lists, include_full=False)
    augmented_colorings = compatible_colorings(
        lists,
        include_full=True,
        full_color=0,
    )
    fans = fan_embeddings(lists)
    canonical = subprocess.run(
        (str(LABELG), "-q"),
        input=GRAPH6 + "\n",
        text=True,
        capture_output=True,
        check=True,
    )
    assert not canonical.stderr
    family_manifest = "\n".join(
        "".join(str(v) for v in range(ORDER) if state & (1 << v))
        for state in sorted(family)
    ) + "\n"
    result = {
        "schema": "full-list-odd-lollipop-clean-room-replay-v1",
        "status": "PASS",
        "target": {
            "path": str(TARGET.relative_to(CAMPAIGN)),
            "sha256": sha256(TARGET),
        },
        "graph": {
            "labeled_graph6": GRAPH6,
            "canonical_graph6": canonical.stdout.strip(),
            "H_edges": [list(edge) for edge in sorted(actual_h_edges)],
        },
        "parameters": {
            "gamma": exact_gamma(),
            "alpha": exact_alpha(),
            "gamma_infinity": exact_eternal(),
            "theta": exact_theta(),
        },
        "restricted_family": {
            "states": len(family),
            "attack_obligations": obligations,
            "deletion_rounds": list(rounds),
            "banned_direct_swaps": [
                [v for v in range(ORDER) if state & (1 << v)]
                for state in sorted(banned)
            ],
            "state_manifest_sha256": hashlib.sha256(
                family_manifest.encode("ascii")
            ).hexdigest(),
        },
        "response_lists": {
            str(vertex): list(values) for vertex, values in lists.items()
        },
        "semantic_coloring_check": {
            "base_count": len(base_colorings),
            "base_colorings": [
                {str(v): color for v, color in coloring.items()}
                for coloring in base_colorings
            ],
            "augmentation_x_color_0_count": len(augmented_colorings),
        },
        "formula": formula,
        "odd_fan_path_embeddings": fans,
        "scope": {
            "gamma_equals_two_control": True,
            "refutes_automatic_local_implication_only": True,
            "gamma_three_statement_refuted": False,
        },
        "implementation": {
            "bit_mask_graph_and_family": True,
            "target_verify_imported": False,
            "labelg_sha256": sha256(LABELG),
        },
    }
    assert result["graph"]["canonical_graph6"] == "Hvzax|~"
    assert result["parameters"] == {
        "gamma": 2, "alpha": 3, "gamma_infinity": 3, "theta": 3
    }
    assert (len(family), obligations, rounds) == (65, 390, (8, 1, 4))
    assert formula["base_satisfying_assignments"] == [[0, 0], [0, 1]]
    assert not formula["augmented_satisfying_assignments"]
    assert formula["inclusion_minimal_unsatisfiable"]
    assert len(base_colorings) == 2 and not augmented_colorings
    assert not fans
    source = Path(__file__).resolve()
    result["implementation"]["source_sha256_before_result_write"] = sha256(source)
    output = source.with_name("result.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "parameters": result["parameters"],
                "family": result["restricted_family"],
                "base_assignments": formula["base_satisfying_assignments"],
                "fan_embeddings": len(fans),
                "output_sha256": sha256(output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
