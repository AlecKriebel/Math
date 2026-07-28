#!/usr/bin/env python3
"""Independent finite checks for the hostile Y_k equality-gates audit.

This checker does not prove the human clean-branch lemmas.  It pins their
sources, checks the elementary finite counting/cycle assertions, and
reconstructs the symbolic nonindependent-carrier control used to refute
the overclaimed dirty-carrier inference.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]

PINNED = {
    "math/working/yk_equality_gates/NOTE.md":
        "9c874711a469eca96d790b9680c975f143bede945ee6624ebc9fc860b9f3a785",
    "math/working/yk_equality_gates/RESEARCH_LOG.md":
        "1af30ae0237f40ca8988e297632d1b509d460ae2ad65a0bde1e39023fbac17a3",
    "math/working/yk_equality_gates/MANIFEST.json":
        "3f44e5aae91b014d884d88e54ad98110ecda6beb3f6a8a42a4fc85262b5649ea",
    "math/working/all_k_yk_dynamic/NOTE.md":
        "98a56786a8db1f78c4f6328871b1926795928997389f441e4637e6e3d801d6e0",
    "math/working/dynamic_gluing_y3/NOTE.md":
        "ff559cb949c5427bc33e75a43deba38a8284e78c380a01bb97488a82a59798f9",
    "math/working/forced_c5_contradiction/NOTE.md":
        "0c6a3de00f8e4daa53f4602c437ed51a22da911cfdff3f42445550b07e3430bb",
    "math/working/k3_mixed_witness_followup.md":
        "079c3ee0e880eb211f7e7460193e9c4c8212d70350965e668eb462f4f0a4db04",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pins() -> None:
    for relative, expected in PINNED.items():
        actual = sha256(CAMPAIGN / relative)
        assert actual == expected, (relative, expected, actual)

    manifest_path = CAMPAIGN / "math/working/yk_equality_gates/MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["status"] == "revised-after-hostile-review"
    for artifact in manifest["artifacts"]:
        actual = sha256(manifest_path.parent / artifact["path"])
        assert actual == artifact["sha256"], artifact


def has_directed_cycle(vertices: tuple[int, ...], arcs: set[tuple[int, int]]) -> bool:
    color = {v: 0 for v in vertices}

    def visit(v: int) -> bool:
        color[v] = 1
        for _, w in (arc for arc in arcs if arc[0] == v):
            if color[w] == 1:
                return True
            if color[w] == 0 and visit(w):
                return True
        color[v] = 2
        return False

    return any(color[v] == 0 and visit(v) for v in vertices)


def check_cycle_and_counts() -> dict[str, object]:
    cycle_instances = {}
    for size in range(1, 5):
        vertices = tuple(range(size))
        possible = tuple((u, v) for u in vertices for v in vertices if u != v)
        positive_outdegree_instances = 0
        for mask in range(1 << len(possible)):
            arcs = {possible[j] for j in range(len(possible)) if mask & (1 << j)}
            if not all(any(u == v for u, _ in arcs) for v in vertices):
                continue
            positive_outdegree_instances += 1
            assert size >= 2
            assert has_directed_cycle(vertices, arcs)
        cycle_instances[size] = positive_outdegree_instances

    for k in range(5, 51):
        assert 12 + 2 * (k - 3) + 2 + 1 == 2 * k + 9
        assert 12 + 2 * (k - 3) + 2 + 2 == 2 * k + 10

    return {
        "positive_outdegree_digraphs_checked": cycle_instances,
        "count_identities_checked_for_k": [5, 50],
    }


def check_symbolic_carrier() -> dict[str, object]:
    # Vertices: Z=(z0,z1), C=(p,b,c), X=(x0,x1,x2,x3).
    z = (0, 1)
    carrier = (2, 3, 4)
    path = (5, 6, 7, 8)
    vertices = tuple(range(9))
    installed = frozenset(z + carrier)

    edges = {
        (1, 2),                              # z1-p
        (2, 5), (2, 6),                     # p-x0,p-x1
        (3, 6), (3, 7), (3, 8),             # b-x1,b-x2,b-x3
        (4, 5), (4, 6), (4, 7), (4, 8),     # c-x0,c-x1,c-x2,c-x3
        (5, 7), (5, 8), (6, 8),             # complement-P4 chords in G
    }

    def adjacent(u: int, v: int) -> bool:
        return tuple(sorted((u, v))) in edges

    assert all(not adjacent(u, v) for u, v in itertools.combinations(z, 2))
    assert all(not adjacent(u, v) for u, v in itertools.combinations(carrier, 2))
    assert all(not adjacent(u, v) for u in z for v in path)
    assert [adjacent(path[j], path[j + 1]) for j in range(3)] == [False] * 3
    assert all(
        adjacent(u, v)
        for u, v in ((path[0], path[2]), (path[0], path[3]), (path[1], path[3]))
    )
    assert adjacent(1, 2)
    assert any(adjacent(u, v) for u in z for v in carrier)

    # Abstract original colors: d0,d1,a,b,c = 0,1,2,3,4.
    assigned_lists = {
        0: frozenset({0}),
        1: frozenset({1}),
        2: frozenset({2}),
        5: frozenset({0, 1, 2}),
        6: frozenset({0, 1, 2, 4}),
        7: frozenset({0, 1, 3, 4}),
        8: frozenset({0, 1, 3}),
    }
    all_colors = frozenset(range(5))

    def dominates(state: frozenset[int]) -> bool:
        return all(
            v in state or any(adjacent(v, u) for u in state)
            for v in vertices
        )

    def satisfies_restoration(state: frozenset[int]) -> bool:
        # Original b,c are represented by vertices 3,4.  The three other
        # original positions are absent from this symbolic residual universe.
        occupied_original = {v for v in (3, 4) if v in state}
        missing = all_colors - occupied_original
        covered: set[int] = set()
        for v in state:
            covered.update(assigned_lists.get(v, ()))
        return missing <= covered

    forbidden = frozenset((installed - {4}) | {6})  # U-c+x1
    active = {
        state
        for choice in itertools.combinations(vertices, 5)
        if (state := frozenset(choice)) != forbidden
        and dominates(state)
        and satisfies_restoration(state)
    }
    initial_count = len(active)
    deletion_rounds = []
    while True:
        deleted = set()
        for state in active:
            for attack in vertices:
                if attack in state:
                    continue
                if not any(
                    adjacent(guard, attack)
                    and frozenset((state - {guard}) | {attack}) in active
                    for guard in state
                ):
                    deleted.add(state)
                    break
        if not deleted:
            break
        deletion_rounds.append(len(deleted))
        active -= deleted

    assert initial_count == 39
    assert deletion_rounds == [5]
    assert len(active) == 34
    assert installed in active
    assert forbidden not in active
    assert all(dominates(state) for state in active)
    assert all(satisfies_restoration(state) for state in active)

    obligations = 0
    for state in active:
        for attack in vertices:
            if attack in state:
                continue
            obligations += 1
            responses = [
                guard
                for guard in state
                if adjacent(guard, attack)
                and frozenset((state - {guard}) | {attack}) in active
            ]
            assert responses
    assert obligations == 136

    response_lists = {
        attack: [
            guard
            for guard in carrier
            if adjacent(guard, attack)
            and frozenset((installed - {guard}) | {attack}) in active
        ]
        for attack in path
    }
    assert response_lists == {5: [2], 6: [2], 7: [3, 4], 8: [3]}

    intended_caps = {5: {2}, 6: {2, 4}, 7: {3, 4}, 8: {3}}
    assert all(set(response_lists[x]) <= intended_caps[x] for x in path)
    assert all(
        adjacent(role, attack)
        for attack, cap in intended_caps.items()
        for role in cap
    )
    assert 4 not in response_lists[6]

    return {
        "vertices": 9,
        "edges": len(edges),
        "initial_admissible_states": initial_count,
        "deletion_rounds": deletion_rounds,
        "eternal_family_states": len(active),
        "one_guard_obligations": obligations,
        "response_lists_at_U": {
            "x0": ["p"],
            "x1": ["p"],
            "x2": ["b", "c"],
            "x3": ["b"],
        },
        "missing_intended_role": "c at x1",
        "scope": "symbolic proof-method falsifier, not a full original Y_k realization",
    }


def main() -> None:
    check_pins()
    result = {
        "status": "PASS",
        "pinned_artifacts": len(PINNED),
        "clean_branch_corollaries": check_cycle_and_counts(),
        "nonindependent_carrier_control": check_symbolic_carrier(),
        "global_frontier": "OPEN",
        "k3": "OPEN",
        "GL(k)": "OPEN",
        "universal_gamma_theta_conjecture": "OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
