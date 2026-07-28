#!/usr/bin/env python3
"""Clean-room audit for the singleton-buffer candidate.

This file imports no campaign or candidate module.  Graph states are integer
bit masks, and the one-guard greatest fixed point is reconstructed directly
from the definition.
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
CANDIDATE = CAMPAIGN / "math" / "working" / "singleton_list_endgame"

EXPECTED_SOURCE_HASHES = {
    "NOTE.md": "4f6244214e125a31d4237a7e8f59e20266c15374be4d54c2e23bfbb061e313c5",
    "RESEARCH_LOG.md": "0a45cd338672f9f3c9cd7da0aa397c539d6454ddceff29bf0ca3660e0542503b",
    "controls.json": "108bedac6c157a70a2d21200afa4740faac64f501906ec845e098a8f141b22a9",
    "search_sealed_cap.py": "f4b1b70c09f1fc8f46b1ec65cdf4afca01f30d2825df116d9d357c2f9f20a719",
    "verify.py": "b9f0078167e0d1ee040edbf00fd8e32837a438c5919d0776a10297a84047bf11",
}

EXPECTED_DEPENDENCY_HASHES = {
    "math/working/k3_projection_gluing.md":
        "fc7f817aa611751b9bedbb9ddebd5830d81f02719f2d8aafe914db34f4c64907",
    "math/working/k3_twosat_bicycle/NOTE.md":
        "8a934a8194913633821223b070a013dda8e0cd8c0d6870616b32a882e8b2fd59",
    "math/working/k3_long_bicycle_connectors/NOTE.md":
        "d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10",
    "math/working/dynamic_connector_edge_caps/NOTE.md":
        "185e29a4b8e231aa5e90126f7fd16be32c696cd3f99e46c00f90cb61f27548e7",
    "math/working/physicalized_twosat_endgame/NOTE.md":
        "3a357c3c7ece9a0cf33f7b555cae21e629a19b9e2d86e6ebe6f5798b4f08e7df",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def bits(mask: int) -> list[int]:
    out: list[int] = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out


def mask_of(vertices: tuple[int, ...] | list[int]) -> int:
    out = 0
    for vertex in vertices:
        out |= 1 << vertex
    return out


def graph6_masks(record: str) -> tuple[int, tuple[int, ...]]:
    data = record.encode("ascii")
    assert data and 63 <= data[0] <= 125
    n = data[0] - 63
    stream: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        assert 0 <= value < 64
        stream.extend((value >> shift) & 1 for shift in (5, 4, 3, 2, 1, 0))
    assert len(stream) >= n * (n - 1) // 2
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if stream[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return n, tuple(adjacency)


def graph_size(adjacency: tuple[int, ...]) -> int:
    return sum(mask.bit_count() for mask in adjacency) // 2


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    n = len(adjacency)
    universe = (1 << n) - 1
    return tuple(
        universe & ~(1 << vertex) & ~adjacency[vertex]
        for vertex in range(n)
    )


def connected(adjacency: tuple[int, ...]) -> bool:
    reached = 1
    frontier = 1
    while frontier:
        merged = 0
        for vertex in bits(frontier):
            merged |= adjacency[vertex]
        frontier = merged & ~reached
        reached |= frontier
    return reached == (1 << len(adjacency)) - 1


def dominates(state: int, adjacency: tuple[int, ...]) -> bool:
    covered = state
    for guard in bits(state):
        covered |= adjacency[guard]
    return covered == (1 << len(adjacency)) - 1


def independent(state: int, adjacency: tuple[int, ...]) -> bool:
    return all(not (adjacency[vertex] & state) for vertex in bits(state))


def subsets(n: int, cardinality: int):
    for vertices in combinations(range(n), cardinality):
        yield mask_of(list(vertices))


def domination_number(adjacency: tuple[int, ...]) -> int:
    n = len(adjacency)
    for cardinality in range(1, n + 1):
        if any(dominates(state, adjacency) for state in subsets(n, cardinality)):
            return cardinality
    raise AssertionError


def independence_number(adjacency: tuple[int, ...]) -> int:
    n = len(adjacency)
    for cardinality in range(n, 0, -1):
        if any(independent(state, adjacency) for state in subsets(n, cardinality)):
            return cardinality
    raise AssertionError


def independent_domination_number(adjacency: tuple[int, ...]) -> int:
    n = len(adjacency)
    for cardinality in range(1, n + 1):
        for state in subsets(n, cardinality):
            if independent(state, adjacency) and dominates(state, adjacency):
                return cardinality
    raise AssertionError


def k_colorable(adjacency: tuple[int, ...], k: int) -> tuple[bool, tuple[int, ...]]:
    n = len(adjacency)
    colors = [-1] * n

    def search(colored: int) -> bool:
        if colored == n:
            return True
        remaining = [v for v in range(n) if colors[v] < 0]
        vertex = max(
            remaining,
            key=lambda v: (
                len({colors[w] for w in bits(adjacency[v]) if colors[w] >= 0}),
                (adjacency[v] & sum(1 << x for x in remaining)).bit_count(),
                -v,
            ),
        )
        forbidden = {colors[w] for w in bits(adjacency[vertex]) if colors[w] >= 0}
        used = set(colors) - {-1}
        for color in range(k):
            if color in forbidden:
                continue
            # Canonical color introduction.
            if color not in used and color > len(used):
                continue
            colors[vertex] = color
            if search(colored + 1):
                return True
            colors[vertex] = -1
        return False

    success = search(0)
    return success, tuple(colors) if success else ()


def chromatic_number(adjacency: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    for k in range(1, len(adjacency) + 1):
        success, coloring = k_colorable(adjacency, k)
        if success:
            return k, coloring
    raise AssertionError


def greatest_eternal_triples(adjacency: tuple[int, ...]) -> tuple[set[int], list[int]]:
    n = len(adjacency)
    family = {
        state for state in subsets(n, 3)
        if dominates(state, adjacency)
    }
    deleted_per_round: list[int] = []
    while True:
        doomed: set[int] = set()
        for state in family:
            for attacked in range(n):
                attack_bit = 1 << attacked
                if state & attack_bit:
                    continue
                possible = False
                for guard in bits(state):
                    if not (adjacency[guard] & attack_bit):
                        continue
                    successor = (state ^ (1 << guard)) | attack_bit
                    if successor in family:
                        possible = True
                        break
                if not possible:
                    doomed.add(state)
                    break
        if not doomed:
            return family, deleted_per_round
        family.difference_update(doomed)
        deleted_per_round.append(len(doomed))


def family_audit(
    family: set[int],
    adjacency: tuple[int, ...],
) -> tuple[int, str]:
    n = len(adjacency)
    obligations = 0
    response_lines: list[str] = []
    for state in sorted(family):
        assert state.bit_count() == 3 and dominates(state, adjacency)
        for attacked in range(n):
            attack_bit = 1 << attacked
            if state & attack_bit:
                continue
            obligations += 1
            responders: list[int] = []
            for guard in bits(state):
                if adjacency[guard] & attack_bit:
                    successor = (state ^ (1 << guard)) | attack_bit
                    if successor in family:
                        responders.append(guard)
            assert responders
            response_lines.append(
                f"{','.join(map(str, bits(state)))}:{attacked}:"
                f"{','.join(map(str, responders))}"
            )
    response_hash = sha256(("\n".join(response_lines) + "\n").encode()).hexdigest()
    return obligations, response_hash


def response_lists(reference: int, family: set[int], n: int) -> dict[int, tuple[int, ...]]:
    result: dict[int, tuple[int, ...]] = {}
    for vertex in range(n):
        if reference & (1 << vertex):
            continue
        responders = []
        for anchor in bits(reference):
            successor = (reference ^ (1 << anchor)) | (1 << vertex)
            if successor in family:
                responders.append(anchor)
        result[vertex] = tuple(responders)
    return result


def audit_reference_lists(
    reference: int,
    lists: dict[int, tuple[int, ...]],
    family: set[int],
    adjacency: tuple[int, ...],
) -> None:
    assert reference in family
    assert independent(reference, adjacency)
    for vertex, response in lists.items():
        assert response
        for anchor in response:
            # This directly audits that a recorded response can be made by
            # the named guard along one actual G-edge.
            assert adjacency[anchor] & (1 << vertex)
            assert (reference ^ (1 << anchor)) | (1 << vertex) in family


def list_coloring_count(
    reference: int,
    lists: dict[int, tuple[int, ...]],
    h_adjacency: tuple[int, ...],
) -> int:
    assigned = {anchor: anchor for anchor in bits(reference)}
    outside = sorted(lists, key=lambda x: (len(lists[x]), x))
    count = 0

    def search(position: int) -> None:
        nonlocal count
        if position == len(outside):
            count += 1
            return
        vertex = outside[position]
        forbidden = {
            color for other, color in assigned.items()
            if h_adjacency[vertex] & (1 << other)
        }
        for color in lists[vertex]:
            if color in forbidden:
                continue
            assigned[vertex] = color
            search(position + 1)
            del assigned[vertex]

    search(0)
    return count


def projection_component(
    omitted: int,
    start: int,
    reference: int,
    lists: dict[int, tuple[int, ...]],
    h_adjacency: tuple[int, ...],
) -> tuple[tuple[int, ...], dict[int, int]]:
    allowed = (reference & ~(1 << omitted))
    for vertex, response in lists.items():
        if omitted not in response:
            allowed |= 1 << vertex
    parity = {start: 0}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for other in bits(h_adjacency[vertex] & allowed):
            if other not in parity:
                parity[other] = parity[vertex] ^ 1
                queue.append(other)
            else:
                assert parity[other] != parity[vertex]
    return tuple(sorted(parity)), parity


def exact_parameters(
    adjacency: tuple[int, ...],
    eternal_family: set[int],
) -> tuple[dict[str, int], tuple[int, ...]]:
    h_adjacency = complement(adjacency)
    theta, coloring = chromatic_number(h_adjacency)
    alpha = independence_number(adjacency)
    assert eternal_family and alpha == 3
    return {
        "gamma": domination_number(adjacency),
        "i": independent_domination_number(adjacency),
        "alpha": alpha,
        "gamma_infinity": 3,
        "theta": theta,
    }, coloring


def audit_six_vertex_control() -> dict[str, object]:
    record = "EEv?"
    n, adjacency = graph6_masks(record)
    assert n == 6 and graph_size(adjacency) == 7
    h_adjacency = complement(adjacency)
    chosen = {
        mask_of(list(state))
        for state in (
            (0, 1, 2), (0, 2, 3), (0, 2, 4), (0, 2, 5),
            (1, 2, 3), (1, 2, 4), (2, 3, 5), (2, 4, 5),
        )
    }
    obligations, response_hash = family_audit(chosen, adjacency)
    assert obligations == 24
    reference = mask_of([0, 1, 2])
    lists = response_lists(reference, chosen, n)
    audit_reference_lists(reference, lists, chosen, adjacency)
    assert lists == {3: (0, 1), 4: (0, 1), 5: (1,)}
    parameters, coloring = exact_parameters(adjacency, chosen)
    assert parameters == {
        "gamma": 3, "i": 3, "alpha": 3,
        "gamma_infinity": 3, "theta": 3,
    }
    positive_zero = {v for v, response in lists.items() if 0 in response}
    sealed = {
        v for v in positive_zero
        if not any(h_adjacency[v] & (1 << w) for w in positive_zero - {v})
    }
    assert sealed == {3, 4}
    for z in sealed:
        assert h_adjacency[z] & (1 << 5)
        assert h_adjacency[2] & (1 << 5)
        # Sharp branch: the omitted anchor is itself a common H-neighbor
        # of {1,z}; there is no singleton-{2} outside witness.
        assert h_adjacency[1] & (1 << 2)
        assert h_adjacency[z] & (1 << 2)
    assert list_coloring_count(reference, lists, h_adjacency) == 1
    edge_rows = [
        f"{u}-{v}" for u in range(n) for v in range(u + 1, n)
        if adjacency[u] & (1 << v)
    ]
    return {
        "graph6": record,
        "order": n,
        "size": graph_size(adjacency),
        "connected": connected(adjacency),
        "edge_sha256": sha256(("\n".join(edge_rows) + "\n").encode()).hexdigest(),
        "parameters": parameters,
        "family_size": len(chosen),
        "attack_obligations": obligations,
        "response_certificate_sha256": response_hash,
        "lists": {str(v): list(value) for v, value in lists.items()},
        "sealed": sorted(sealed),
        "singleton_buffer": 5,
        "list_coloring_count": 1,
        "h_coloring": list(coloring),
    }


def audit_thirteen_vertex_control() -> dict[str, object]:
    record = "LFzJbZYhdrDZdM"
    n, adjacency = graph6_masks(record)
    assert n == 13 and graph_size(adjacency) == 43 and connected(adjacency)
    h_adjacency = complement(adjacency)
    family, deletion_rounds = greatest_eternal_triples(adjacency)
    assert len(family) == 142
    obligations, response_hash = family_audit(family, adjacency)
    assert obligations == 1420
    reference = mask_of([0, 1, 2])
    lists = response_lists(reference, family, n)
    audit_reference_lists(reference, lists, family, adjacency)
    assert lists == {
        3: (0, 1), 4: (1, 2), 5: (0, 1), 6: (1, 2),
        7: (1, 2), 8: (0, 1), 9: (0, 2), 10: (0, 2),
        11: (2,), 12: (0,),
    }
    parameters, coloring = exact_parameters(adjacency, family)
    assert parameters == {
        "gamma": 3, "i": 3, "alpha": 3,
        "gamma_infinity": 3, "theta": 3,
    }
    dynamic: dict[int, int] = {}
    anchors = {0, 1, 2}
    for vertex, response in lists.items():
        if len(response) == 2:
            omitted = next(iter(anchors - set(response)))
            if adjacency[vertex] & (1 << omitted):
                dynamic[vertex] = omitted
    assert dynamic == {3: 2, 4: 0}

    expected_paths = {3: (3, 5, 8), 4: (4, 6, 7)}
    expected_caps = {3: 11, 4: 12}
    component_rows: dict[str, object] = {}
    cap_rows: dict[str, object] = {}
    singleton_vertices = {v for v, response in lists.items() if len(response) == 1}
    for port, omitted in dynamic.items():
        path = expected_paths[port]
        component, parity = projection_component(
            omitted, port, reference, lists, h_adjacency
        )
        assert component == tuple(path)
        assert not (set(component) & singleton_vertices)
        assert not (set(component) & anchors)
        assert parity[path[0]] == parity[path[2]]
        assert all(
            h_adjacency[path[index]] & (1 << path[index + 1])
            for index in (0, 1)
        )
        assert not (h_adjacency[path[0]] & (1 << path[2]))
        assert h_adjacency[omitted] & (1 << path[2])
        assert lists[path[2]] == lists[port]

        cap = expected_caps[port]
        assert lists[cap] == (omitted,)
        assert h_adjacency[cap] & (1 << path[0])
        assert h_adjacency[cap] & (1 << path[1])
        positive = {v for v, response in lists.items() if omitted in response}
        assert not any(
            h_adjacency[cap] & (1 << other)
            for other in positive - {cap}
        )
        component_rows[str(port)] = {
            "omitted": omitted,
            "component": list(component),
            "same_side_endpoints": True,
        }
        cap_rows[str(port)] = {
            "cap": cap,
            "list": list(lists[cap]),
            "sealed": True,
            "first_edge": list(path[:2]),
        }

    assert list_coloring_count(reference, lists, h_adjacency) == 2
    family_lines = [
        ",".join(map(str, bits(state))) for state in sorted(family)
    ]
    edge_rows = [
        f"{u}-{v}" for u in range(n) for v in range(u + 1, n)
        if adjacency[u] & (1 << v)
    ]
    return {
        "graph6": record,
        "order": n,
        "size": graph_size(adjacency),
        "connected": True,
        "edge_sha256": sha256(("\n".join(edge_rows) + "\n").encode()).hexdigest(),
        "parameters": parameters,
        "greatest_family_size": len(family),
        "greatest_family_sha256":
            sha256(("\n".join(family_lines) + "\n").encode()).hexdigest(),
        "simultaneous_deletion_rounds": deletion_rounds,
        "attack_obligations": obligations,
        "response_certificate_sha256": response_hash,
        "lists": {str(v): list(value) for v, value in lists.items()},
        "dynamic_ports": dynamic,
        "free_components": component_rows,
        "sealed_singleton_caps": cap_rows,
        "list_coloring_count": 2,
        "h_coloring": list(coloring),
    }


def audit_clause_inventory() -> dict[str, int]:
    colors = frozenset({0, 1, 2})
    proper_lists = [
        frozenset(choice)
        for size in (1, 2)
        for choice in combinations(colors, size)
    ]
    counts = {"same_projection": 0, "disjoint": 0, "cross_clause": 0}
    for first_index, first in enumerate(proper_lists):
        for second in proper_lists[first_index:]:
            omitted_first = colors - first
            omitted_second = colors - second
            if omitted_first & omitted_second:
                counts["same_projection"] += 1
            elif not (first & second):
                assert sorted((len(first), len(second))) == [1, 2]
                counts["disjoint"] += 1
            else:
                assert len(first) == len(second) == 2
                assert len(first & second) == 1
                counts["cross_clause"] += 1
    assert sum(counts.values()) == 21
    return counts


def audit_local_list_forcing() -> dict[str, list[list[int]]]:
    colors = {0, 1, 2}
    nonempty = [
        set(choice)
        for size in (1, 2, 3)
        for choice in combinations(colors, size)
    ]
    p_options = [choice for choice in nonempty if 0 not in choice and 2 not in choice]
    q_options = [choice for choice in nonempty if 0 not in choice and 1 not in choice]
    assert p_options == [{1}]
    assert q_options == [{2}]
    return {
        "p_after_excluding_i_k": [sorted(choice) for choice in p_options],
        "q_after_excluding_i_j": [sorted(choice) for choice in q_options],
    }


def audit_hashes() -> dict[str, object]:
    actual_source = {
        name: digest(CANDIDATE / name)
        for name in EXPECTED_SOURCE_HASHES
    }
    assert actual_source == EXPECTED_SOURCE_HASHES
    manifest = json.loads((CANDIDATE / "MANIFEST.json").read_text())
    assert manifest["files"] == EXPECTED_SOURCE_HASHES
    actual_dependencies = {
        name: digest(CAMPAIGN / name)
        for name in EXPECTED_DEPENDENCY_HASHES
    }
    assert actual_dependencies == EXPECTED_DEPENDENCY_HASHES
    return {
        "source": actual_source,
        "manifest_sha256": digest(CANDIDATE / "MANIFEST.json"),
        "dependencies": actual_dependencies,
    }


def main() -> None:
    result = {
        "schema": "singleton-buffer-hostile-independent-v1",
        "status": "PASS",
        "hashes": audit_hashes(),
        "clause_inventory": audit_clause_inventory(),
        "local_list_forcing": audit_local_list_forcing(),
        "sealed_control": audit_six_vertex_control(),
        "dynamic_control": audit_thirteen_vertex_control(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
