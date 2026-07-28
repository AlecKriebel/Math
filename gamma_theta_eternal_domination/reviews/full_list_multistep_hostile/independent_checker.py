#!/usr/bin/env python3
"""Clean-room audit of the full-list two-attack spoke theorem.

The graph/game core below is independent of the candidate implementation.
Graphs are represented by integer adjacency masks and configurations by
integer masks.  No campaign evaluator is imported.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "math/working/full_list_multistep_bridge"
CANDIDATE_MANIFEST_SHA = (
    "fc35e58e2d96f9a7dc96d359fa601dc6083932ca8d899256db629e57869fb705"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(text: str) -> tuple[int, ...]:
    """Decode a canonical short-form graph6 record into adjacency masks."""

    payload = text.encode("ascii")
    assert payload and payload[0] != 126
    n = payload[0] - 63
    need = n * (n - 1) // 2
    assert len(payload) == 1 + (need + 5) // 6
    stream = []
    for byte in payload[1:]:
        value = byte - 63
        assert 0 <= value <= 63
        stream.extend((value >> shift) & 1 for shift in (5, 4, 3, 2, 1, 0))
    assert not any(stream[need:])
    rows = [0] * n
    cursor = 0
    for upper in range(1, n):
        for lower in range(upper):
            if stream[cursor]:
                rows[upper] |= 1 << lower
                rows[lower] |= 1 << upper
            cursor += 1
    return tuple(rows)


def complement(graph: tuple[int, ...]) -> tuple[int, ...]:
    all_vertices = (1 << len(graph)) - 1
    return tuple(
        all_vertices & ~(graph[vertex] | (1 << vertex))
        for vertex in range(len(graph))
    )


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def masks_of_size(n: int, size: int):
    for selection in itertools.combinations(range(n), size):
        mask = 0
        for vertex in selection:
            mask |= 1 << vertex
        yield mask


def dominates(graph: tuple[int, ...], state: int) -> bool:
    covered = state
    for guard in vertices(state):
        covered |= graph[guard]
    return covered == (1 << len(graph)) - 1


def independent(graph: tuple[int, ...], state: int) -> bool:
    return all(not (graph[v] & (state ^ (1 << v))) for v in vertices(state))


def domination_number(graph: tuple[int, ...]) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in masks_of_size(len(graph), size)):
            return size
    raise AssertionError


def independence_number(graph: tuple[int, ...]) -> int:
    for size in range(len(graph), 0, -1):
        if any(independent(graph, state) for state in masks_of_size(len(graph), size)):
            return size
    return 0


def independent_domination_number(graph: tuple[int, ...]) -> int:
    for size in range(1, len(graph) + 1):
        if any(
            independent(graph, state) and dominates(graph, state)
            for state in masks_of_size(len(graph), size)
        ):
            return size
    raise AssertionError


def colorable(graph: tuple[int, ...], colors: int) -> bool:
    n = len(graph)
    assigned = [-1] * n
    degrees = [row.bit_count() for row in graph]

    def search(done: int) -> bool:
        if done == n:
            return True
        choices = []
        for vertex in range(n):
            if assigned[vertex] >= 0:
                continue
            forbidden = {
                assigned[other]
                for other in vertices(graph[vertex])
                if assigned[other] >= 0
            }
            choices.append((len(forbidden), degrees[vertex], vertex, forbidden))
        _, _, vertex, forbidden = max(choices)
        for color in range(colors):
            if color not in forbidden:
                assigned[vertex] = color
                if search(done + 1):
                    return True
                assigned[vertex] = -1
        return False

    return search(0)


def chromatic_number(graph: tuple[int, ...]) -> int:
    for colors in range(1, len(graph) + 1):
        if colorable(graph, colors):
            return colors
    raise AssertionError


def kernel(
    graph: tuple[int, ...], size: int
) -> tuple[set[int], dict[int, int], list[int], int]:
    family = {
        state
        for state in masks_of_size(len(graph), size)
        if dominates(graph, state)
    }
    initial = len(family)
    ranks: dict[int, int] = {}
    waves: list[int] = []
    round_number = 0
    while True:
        remove = []
        for state in family:
            for attack in range(len(graph)):
                attack_bit = 1 << attack
                if state & attack_bit:
                    continue
                responders = [
                    guard
                    for guard in vertices(state)
                    if graph[guard] & attack_bit
                    and ((state ^ (1 << guard)) | attack_bit) in family
                ]
                if not responders:
                    remove.append(state)
                    break
        if not remove:
            return family, ranks, waves, initial
        round_number += 1
        waves.append(len(remove))
        for state in remove:
            family.remove(state)
            ranks[state] = round_number


def legal_dominating_moves(
    graph: tuple[int, ...], state: int, attack: int
) -> list[tuple[int, int]]:
    assert not (state & (1 << attack))
    answer = []
    for guard in vertices(state):
        if graph[guard] & (1 << attack):
            successor = (state ^ (1 << guard)) | (1 << attack)
            if dominates(graph, successor):
                answer.append((guard, successor))
    return answer


def induced_delete(graph: tuple[int, ...], deleted: int) -> tuple[int, ...]:
    keep = [v for v in range(len(graph)) if v != deleted]
    index = {old: new for new, old in enumerate(keep)}
    rows = []
    for old in keep:
        row = 0
        for neighbor in vertices(graph[old]):
            if neighbor in index:
                row |= 1 << index[neighbor]
        rows.append(row)
    return tuple(rows)


def components(graph: tuple[int, ...], subset: int) -> list[list[int]]:
    unseen = subset
    answer = []
    while unseen:
        first_bit = unseen & -unseen
        first = first_bit.bit_length() - 1
        unseen ^= first_bit
        queue = deque([first])
        found = [first]
        while queue:
            vertex = queue.popleft()
            available = graph[vertex] & unseen
            for other in list(vertices(available)):
                unseen ^= 1 << other
                queue.append(other)
                found.append(other)
        answer.append(sorted(found))
    return sorted(answer)


def abstract_truth_table() -> list[dict[str, object]]:
    """Exhaust all anchor-incidence/palette patterns under the three attacks."""

    records = []
    for h_incidence in range(8):
        first_states_dominate = h_incidence.bit_count() <= 1
        for palette in range(8):
            closes = first_states_dominate
            if closes:
                for removed in range(3):
                    remaining = 0b111 ^ (1 << removed)
                    response = False
                    for mover in vertices(remaining):
                        if h_incidence & (1 << mover):
                            continue
                        stationary = remaining ^ (1 << mover)
                        anchor = stationary.bit_length() - 1
                        if palette & (1 << anchor):
                            response = True
                    if not response:
                        closes = False
                        break
            predicted = (
                h_incidence.bit_count() <= 1
                and palette.bit_count() >= 2
                and (h_incidence & ~palette) == 0
            )
            assert closes == predicted
            records.append(
                {
                    "H_anchor_incidence": list(vertices(h_incidence)),
                    "retained_palette": list(vertices(palette)),
                    "all_three_second_attacks_close": closes,
                }
            )
    return records


def analyze(
    name: str,
    graph6: str,
    target: int,
    root_vertices: tuple[int, int, int],
) -> dict[str, object]:
    graph = decode_graph6(graph6)
    h = complement(graph)
    n = len(graph)
    root = sum(1 << v for v in root_vertices)
    assert independent(graph, root)
    assert not (root & (1 << target))
    assert all(graph[s] & (1 << target) for s in root_vertices)
    successors = {
        removed: (root ^ (1 << removed)) | (1 << target)
        for removed in root_vertices
    }
    assert all(dominates(graph, state) for state in successors.values())

    b_mask = h[target]
    assert not (b_mask & root)
    spokes = {
        anchor: b_mask & h[anchor]
        for anchor in root_vertices
    }
    assert all(
        sum(bool(spokes[a] & (1 << b)) for a in root_vertices) <= 1
        for b in vertices(b_mask)
    )

    q_palettes = {}
    failures = []
    for b in vertices(b_mask):
        q = 0
        for anchor in root_vertices:
            state = (1 << target) | (1 << anchor) | (1 << b)
            if dominates(graph, state):
                q |= 1 << anchor
            equivalence_rhs = not (h[b] & spokes[anchor])
            assert dominates(graph, state) == equivalence_rhs
        q_palettes[b] = q
        for removed, state in successors.items():
            moves = legal_dominating_moves(graph, state, b)
            if not moves:
                failures.append((removed, b, tuple(vertices(state))))

    family, ranks, waves, initial = kernel(graph, 3)
    retained = {}
    for b in vertices(b_mask):
        retained[b] = sum(
            1 << anchor
            for anchor in root_vertices
            if ((1 << target) | (1 << anchor) | (1 << b)) in family
        )
    if root in family:
        assert all(successor in family for successor in successors.values())
        assert not failures
        for b in vertices(b_mask):
            own = sum(
                1 << anchor
                for anchor in root_vertices
                if spokes[anchor] & (1 << b)
            )
            assert retained[b].bit_count() >= 2
            assert not (own & ~retained[b])
            assert not (retained[b] & ~q_palettes[b])
            for anchor in vertices(retained[b]):
                assert not (h[b] & spokes[anchor])

    component_rows = []
    for component in components(h, b_mask):
        component_mask = sum(1 << v for v in component)
        signature = [
            anchor
            for anchor in root_vertices
            if spokes[anchor] & component_mask
        ]
        component_rows.append({"vertices": component, "signature": signature})

    target_params = (
        domination_number(graph),
        independent_domination_number(graph),
        independence_number(graph),
        next(size for size in range(1, n + 1) if kernel(graph, size)[0]),
        chromatic_number(h),
    )
    deletion_graph = induced_delete(graph, target)
    deletion_h = complement(deletion_graph)
    deletion_params = (
        domination_number(deletion_graph),
        independent_domination_number(deletion_graph),
        independence_number(deletion_graph),
        next(
            size
            for size in range(1, n)
            if kernel(deletion_graph, size)[0]
        ),
        chromatic_number(deletion_h),
    )
    return {
        "name": name,
        "graph6": graph6,
        "order": n,
        "root": list(root_vertices),
        "target": target,
        "B": list(vertices(b_mask)),
        "spokes": {
            str(anchor): list(vertices(spokes[anchor]))
            for anchor in root_vertices
        },
        "Q": {
            str(vertex): list(vertices(q_palettes[vertex]))
            for vertex in vertices(b_mask)
        },
        "P": {
            str(vertex): list(vertices(retained[vertex]))
            for vertex in vertices(b_mask)
        },
        "H_B_edges": [
            [u, v]
            for u, v in itertools.combinations(vertices(b_mask), 2)
            if h[u] & (1 << v)
        ],
        "components": component_rows,
        "second_attack_failures": sorted([
            {
                "first_removed": removed,
                "attack": attack,
                "state": list(state),
            }
            for removed, attack, state in failures
        ], key=lambda row: (row["first_removed"], row["attack"])),
        "kernel": {
            "initial": initial,
            "size": len(family),
            "waves": waves,
            "root_rank": ranks.get(root),
            "root_retained": root in family,
        },
        "target_parameters_gamma_i_alpha_gamma_inf_theta": target_params,
        "deletion_parameters_gamma_i_alpha_gamma_inf_theta": deletion_params,
    }


def main() -> None:
    manifest_path = CANDIDATE / "MANIFEST.json"
    assert sha256(manifest_path) == CANDIDATE_MANIFEST_SHA
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    hash_rows = {}
    for group in ("rigorous_files", "observed_discovery_files"):
        for row in manifest[group]:
            path = ROOT / row["path"]
            actual = sha256(path)
            assert actual == row["sha256"]
            hash_rows[row["path"]] = actual

    controls = [
        analyze("C123", "IxU[ISrXW", 9, (1, 5, 8)),
        analyze("C128", "KxU[ISrR}NP^", 11, (0, 4, 8)),
        analyze("equality", r"Ksv`f\knJVis", 0, (1, 2, 3)),
    ]
    by_name = {row["name"]: row for row in controls}

    c123 = by_name["C123"]
    assert c123["B"] == [0, 3, 4, 6]
    assert c123["spokes"] == {"1": [3, 6], "5": [], "8": [0, 4]}
    assert [3, 6] in c123["H_B_edges"] and [0, 4] in c123["H_B_edges"]
    assert c123["kernel"]["waves"] == [36, 22]
    assert c123["kernel"]["root_rank"] == 2

    c128 = by_name["C128"]
    assert c128["B"] == [1, 2, 3, 5]
    assert c128["spokes"] == {"0": [3], "4": [2], "8": [1, 5]}
    assert c128["Q"]["1"] == [4] and c128["Q"]["5"] == [0]
    assert c128["second_attack_failures"] == [
        {"first_removed": 0, "attack": 1, "state": [4, 8, 11]},
        {"first_removed": 0, "attack": 5, "state": [4, 8, 11]},
        {"first_removed": 4, "attack": 1, "state": [0, 8, 11]},
        {"first_removed": 4, "attack": 5, "state": [0, 8, 11]},
    ]
    assert c128["kernel"]["waves"] == [47, 56, 3]
    assert c128["kernel"]["root_rank"] == 3

    equality = by_name["equality"]
    assert equality["B"] == [6, 8, 10, 11]
    assert equality["spokes"] == {"1": [6], "2": [11], "3": [8, 10]}
    assert equality["P"] == {
        "6": [1, 2],
        "8": [2, 3],
        "10": [1, 3],
        "11": [1, 2],
    }
    assert equality["components"] == [
        {"vertices": [6, 8], "signature": [1, 3]},
        {"vertices": [10, 11], "signature": [2, 3]},
    ]
    assert equality["kernel"] == {
        "initial": 127,
        "size": 127,
        "waves": [],
        "root_rank": None,
        "root_retained": True,
    }
    assert equality["target_parameters_gamma_i_alpha_gamma_inf_theta"] == (
        3,
        3,
        3,
        3,
        3,
    )
    assert equality["deletion_parameters_gamma_i_alpha_gamma_inf_theta"][0] == 2

    truth_table = abstract_truth_table()
    result = {
        "schema": "full-list-multistep-hostile-result-v1",
        "verdict": "PASS",
        "candidate_manifest_sha256": CANDIDATE_MANIFEST_SHA,
        "all_candidate_hashes_match": True,
        "candidate_file_hashes": hash_rows,
        "abstract_patterns_checked": len(truth_table),
        "abstract_patterns": truth_table,
        "controls": controls,
        "scope": {
            "proved": [
                "two-attack retained-palette theorem",
                "spoke independence",
                "conditional two-spoke component/bipartition theorem",
                "C123 and C128 fail the two-attack condition",
                "named equality control satisfies the theorem",
            ],
            "open": [
                "anchorless physical inactive vertices",
                "dynamically inactive residual R_x minus B",
                "component palette synchronization",
                "complete k=3 theorem",
                "universal gamma-theta conjecture",
            ],
        },
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output = Path(__file__).with_name("result.json")
    output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
