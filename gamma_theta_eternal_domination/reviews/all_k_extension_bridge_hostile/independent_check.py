#!/usr/bin/env python3
"""Clean-room verifier for the all-k extension-bridge positive control.

This checker imports no candidate verifier, search code, graph library, or
campaign evaluator.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
CANDIDATE = CAMPAIGN / "math/working/all_k_extension_bridge"
GRAPH6 = r"Ksv`f\knJVis"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def bits(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def mask_of(items) -> int:
    mask = 0
    for item in items:
        bit = 1 << int(item)
        assert not (mask & bit)
        mask |= bit
    return mask


def decode_graph6(record: str) -> tuple[int, list[int]]:
    raw = record.encode("ascii")
    assert raw and raw[0] != 126
    n = raw[0] - 63
    stream = []
    for char in raw[1:]:
        value = char - 63
        assert 0 <= value < 64
        stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = [(u, v) for v in range(1, n) for u in range(v)]
    assert len(stream) >= len(pairs)
    assert not any(stream[len(pairs) :])
    adjacency = [0] * n
    for present, (u, v) in zip(stream, pairs):
        if present:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return n, adjacency


def adjacent(adjacency: list[int], u: int, v: int) -> bool:
    return bool(adjacency[u] & (1 << v))


def independent(adjacency: list[int], state: int) -> bool:
    return all(not (adjacency[u] & state) for u in bits(state))


def dominates(adjacency: list[int], state: int) -> bool:
    covered = state
    for guard in bits(state):
        covered |= adjacency[guard]
    return covered == (1 << len(adjacency)) - 1


def successor(state: int, mover: int, attacked: int) -> int:
    return (state ^ (1 << mover)) | (1 << attacked)


def induced(adjacency: list[int], retained: list[int]) -> list[int]:
    old_to_new = {old: new for new, old in enumerate(retained)}
    out = [0] * len(retained)
    for old_u in retained:
        for old_v in bits(adjacency[old_u]):
            if old_v in old_to_new:
                out[old_to_new[old_u]] |= 1 << old_to_new[old_v]
    return out


def complement(adjacency: list[int]) -> list[int]:
    full = (1 << len(adjacency)) - 1
    return [full ^ (1 << u) ^ adjacency[u] for u in range(len(adjacency))]


def greatest_kernel(adjacency: list[int], k: int) -> tuple[set[int], int]:
    n = len(adjacency)
    alive = {
        mask_of(state)
        for state in combinations(range(n), k)
        if dominates(adjacency, mask_of(state))
    }
    rounds = 0
    while True:
        remove = set()
        for state in alive:
            for attacked in range(n):
                if state & (1 << attacked):
                    continue
                if not any(
                    adjacent(adjacency, mover, attacked)
                    and successor(state, mover, attacked) in alive
                    for mover in bits(state)
                ):
                    remove.add(state)
                    break
        if not remove:
            return alive, rounds
        alive.difference_update(remove)
        rounds += 1


def static_parameters(adjacency: list[int]) -> tuple[int, int, int]:
    all_states = range(1 << len(adjacency))
    gamma = min(
        state.bit_count() for state in all_states if dominates(adjacency, state)
    )
    independent_domination = min(
        state.bit_count()
        for state in range(1 << len(adjacency))
        if independent(adjacency, state) and dominates(adjacency, state)
    )
    alpha = max(
        state.bit_count()
        for state in range(1 << len(adjacency))
        if independent(adjacency, state)
    )
    return gamma, independent_domination, alpha


def proper_colorings(adjacency: list[int], color_count: int):
    n = len(adjacency)
    for coloring in product(range(color_count), repeat=n):
        if all(
            coloring[u] != coloring[v]
            for u in range(n)
            for v in range(u + 1, n)
            if adjacent(adjacency, u, v)
        ):
            yield coloring


def family_obligations(adjacency: list[int], family: set[int]) -> tuple[int, int]:
    obligations = 0
    legal = 0
    for state in family:
        for attacked in range(len(adjacency)):
            if state & (1 << attacked):
                continue
            obligations += 1
            responses = [
                successor(state, mover, attacked)
                for mover in bits(state)
                if adjacent(adjacency, mover, attacked)
                and successor(state, mover, attacked) in family
            ]
            assert responses
            legal += len(responses)
    return obligations, legal


def main() -> None:
    manifest = json.loads((CANDIDATE / "MANIFEST.json").read_text())
    for name, expected in manifest["files_sha256"].items():
        assert digest(CANDIDATE / name) == expected
    assert (
        digest(CANDIDATE / "MANIFEST.json")
        == "c99b154ed344c7efd076e5115e6d64eed9e9d8eeff6d28810889b405cb39874f"
    )
    n, graph = decode_graph6(GRAPH6)
    assert n == 12
    target = 0
    root = mask_of((1, 2, 3))
    deletion_vertices = [v for v in range(n) if v != target]
    deletion = induced(graph, deletion_vertices)
    h_graph = complement(graph)
    h_deletion = complement(deletion)

    full_gamma, full_i, full_alpha = static_parameters(graph)
    del_gamma, del_i, del_alpha = static_parameters(deletion)
    full_kernels = [greatest_kernel(graph, k) for k in (1, 2, 3)]
    del_kernels = [greatest_kernel(deletion, k) for k in (1, 2, 3)]
    assert (full_gamma, full_i, full_alpha) == (3, 3, 3)
    assert (del_gamma, del_i, del_alpha) == (2, 2, 3)
    assert [len(kernel) for kernel, _ in full_kernels[:2]] == [0, 0]
    assert [len(kernel) for kernel, _ in del_kernels[:2]] == [0, 0]
    family = full_kernels[2][0]
    deletion_family = del_kernels[2][0]
    assert len(family) == 127
    assert deletion_family
    full_obligations, full_legal = family_obligations(graph, family)
    del_obligations, del_legal = family_obligations(deletion, deletion_family)

    assert independent(graph, root)
    assert root in family
    root_responses = [
        guard
        for guard in bits(root)
        if adjacent(graph, guard, target)
        and successor(root, guard, target) in family
    ]
    assert root_responses == [1, 2, 3]

    facets = [
        mask_of(state)
        for state in combinations(deletion_vertices, 3)
        if independent(graph, mask_of(state))
    ]
    facet_support = set().union(*(set(bits(state)) for state in facets))
    assert facet_support == set(deletion_vertices)
    active_status: dict[int, bool] = {}
    active_incidences = 0
    for state in facets:
        assert state in family
        for guard in bits(state):
            status = (
                adjacent(graph, guard, target)
                and successor(state, guard, target) in family
            )
            if guard in active_status:
                assert active_status[guard] == status
            else:
                active_status[guard] = status
            active_incidences += 1
    active = {vertex for vertex, status in active_status.items() if status}
    inactive = set(deletion_vertices) - active
    assert active == {1, 2, 3, 4, 5, 7, 9}
    assert inactive == {6, 8, 10, 11}
    complement_neighbors = {
        vertex
        for vertex in deletion_vertices
        if adjacent(h_graph, target, vertex)
    }
    assert inactive == complement_neighbors

    colorings = list(proper_colorings(h_deletion, 3))
    assert len(colorings) == 12
    old_to_new = {old: new for new, old in enumerate(deletion_vertices)}
    split = {2: 0, 3: 0}
    missing = {0: 0, 1: 0, 2: 0}
    extendible = 0
    serialized_colorings = []
    for coloring in colorings:
        inactive_colors = {
            coloring[old_to_new[vertex]] for vertex in inactive
        }
        split[len(inactive_colors)] += 1
        absent = set(range(3)) - inactive_colors
        for color in absent:
            missing[color] += 1
            # Assigning this color to x must extend the deletion coloring.
            assert all(
                coloring[old_to_new[neighbor]] != color
                for neighbor in complement_neighbors
            )
        if absent:
            extendible += 1
        serialized_colorings.append("".join(map(str, coloring)))
    assert split == {2: 6, 3: 6}
    assert missing == {0: 2, 1: 2, 2: 2}
    assert extendible == 6

    # Alpha=3 gives theta>=3; the enumerated deletion colorings and any
    # successful extension give theta<=3 for deletion and full graph.
    assert colorings
    assert extendible

    result = {
        "verdict": "PASS",
        "candidate_note_sha256": digest(CANDIDATE / "NOTE.md"),
        "manifest_sha256": digest(CANDIDATE / "MANIFEST.json"),
        "control_sha256": digest(CANDIDATE / "positive_control.json"),
        "control": {
            "graph6": GRAPH6,
            "order": n,
            "size": sum(row.bit_count() for row in graph) // 2,
            "full_parameters": {
                "gamma": full_gamma,
                "i": full_i,
                "alpha": full_alpha,
                "gamma_infinity": 3,
                "theta": 3,
            },
            "deletion_parameters": {
                "gamma": del_gamma,
                "i": del_i,
                "alpha": del_alpha,
                "gamma_infinity": 3,
                "theta": 3,
            },
            "full_kernel_sizes_k1_to_k3": [
                len(kernel) for kernel, _ in full_kernels
            ],
            "full_kernel_rounds_k1_to_k3": [
                rounds for _, rounds in full_kernels
            ],
            "deletion_kernel_sizes_k1_to_k3": [
                len(kernel) for kernel, _ in del_kernels
            ],
            "deletion_kernel_rounds_k1_to_k3": [
                rounds for _, rounds in del_kernels
            ],
            "full_family_obligations": full_obligations,
            "full_family_legal_responses": full_legal,
            "deletion_family_obligations": del_obligations,
            "deletion_family_legal_responses": del_legal,
            "root_responses": root_responses,
            "facet_count": len(facets),
            "facet_support_size": len(facet_support),
            "active_incidences": active_incidences,
            "active_set": sorted(active),
            "inactive_set": sorted(inactive),
            "deletion_colorings": len(colorings),
            "inactive_color_split": {str(k): v for k, v in split.items()},
            "missing_color_counts": {str(k): v for k, v in missing.items()},
            "extendible_colorings": extendible,
            "colorings_sha256": sha256(
                "\n".join(sorted(serialized_colorings)).encode("ascii")
            ).hexdigest(),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
