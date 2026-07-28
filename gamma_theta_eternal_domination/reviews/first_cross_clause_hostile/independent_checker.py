#!/usr/bin/env python3
"""Clean-room audit of the two first-cross-clause controls.

This checker imports no campaign module and does not execute the candidate
verifier.  Graphs are represented by ordinary frozensets, configurations by
frozensets, clique cover by a direct set-partition recursion, and the eternal
game by an explicitly colored configuration digraph followed by greatest
fixed-point deletion.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations
from pathlib import Path
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "math/working/first_cross_clause_attack"

CANDIDATE_MANIFEST_SHA256 = (
    "2e157de3ce02eda7eee2cff65d2af064eb7b9103a6f2b3d16772ede44d4e86b0"
)

DEPENDENCIES = {
    "math/working/singleton_fixed_certificates/NOTE.md":
        "25e775574caa48c719e3cf2949fe0ae29c23082b308f2f2002cb1ac2287fa95b",
    "math/working/free_unit_chain_attack/NOTE.md":
        "3dbccd2aa69cfc45b1c5e518e05165594e27f06b1741fcd1ec7a2b8b0d02fb39",
    "math/working/dynamic_gluing_y3/NOTE.md":
        "ff559cb949c5427bc33e75a43deba38a8284e78c380a01bb97488a82a59798f9",
}

# This is witness data, not imported candidate logic.
FDZRO_FAMILY = frozenset(
    frozenset(state)
    for state in (
        (0, 1, 2),
        (1, 2, 3),
        (0, 1, 4),
        (1, 2, 4),
        (1, 3, 4),
        (0, 1, 5),
        (0, 2, 5),
        (1, 3, 5),
        (2, 3, 5),
        (0, 4, 5),
        (1, 4, 5),
        (2, 4, 5),
        (3, 4, 5),
        (0, 2, 6),
        (2, 3, 6),
        (0, 4, 6),
        (2, 4, 6),
        (3, 4, 6),
        (0, 5, 6),
        (3, 5, 6),
        (4, 5, 6),
    )
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> tuple[frozenset[int], frozenset[frozenset[int]]]:
    """Decode a short graph6 record directly from the published bit order."""
    words = [ord(char) - 63 for char in record]
    assert words and 0 <= words[0] <= 62
    order = words[0]
    stream = [
        (word >> shift) & 1
        for word in words[1:]
        for shift in range(5, -1, -1)
    ]
    required = order * (order - 1) // 2
    assert len(stream) >= required
    edges: set[frozenset[int]] = set()
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if stream[cursor]:
                edges.add(frozenset((low, high)))
            cursor += 1
    return frozenset(range(order)), frozenset(edges)


def encode_graph6(
    vertices: frozenset[int], edges: frozenset[frozenset[int]]
) -> str:
    assert vertices == frozenset(range(len(vertices)))
    bits = []
    for high in range(1, len(vertices)):
        for low in range(high):
            bits.append(int(frozenset((low, high)) in edges))
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start:start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(len(vertices) + 63) + "".join(payload)


def adjacent(edges: frozenset[frozenset[int]], left: int, right: int) -> bool:
    return left != right and frozenset((left, right)) in edges


def subsets(vertices: frozenset[int], size: int):
    for choice in combinations(sorted(vertices), size):
        yield frozenset(choice)


def dominates(
    state: frozenset[int],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> bool:
    return all(
        target in state
        or any(adjacent(edges, guard, target) for guard in state)
        for target in vertices
    )


def independent(
    state: frozenset[int], edges: frozenset[frozenset[int]]
) -> bool:
    return all(
        not adjacent(edges, left, right)
        for left, right in combinations(sorted(state), 2)
    )


def maximal_independent(
    state: frozenset[int],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> bool:
    return independent(state, edges) and all(
        any(adjacent(edges, outside, inside) for inside in state)
        for outside in vertices - state
    )


def minimum_size(vertices: frozenset[int], predicate) -> int:
    for size in range(1, len(vertices) + 1):
        if any(predicate(state) for state in subsets(vertices, size)):
            return size
    raise AssertionError("minimum search failed")


def clique_partition_number(
    vertices: frozenset[int], edges: frozenset[frozenset[int]]
) -> tuple[int, tuple[tuple[int, ...], ...]]:
    """Complete canonical partition recursion, not a coloring routine."""
    ordered = sorted(vertices)
    best = len(vertices) + 1
    witness: tuple[tuple[int, ...], ...] | None = None
    blocks: list[list[int]] = []

    def visit(position: int) -> None:
        nonlocal best, witness
        if len(blocks) >= best:
            return
        if position == len(ordered):
            best = len(blocks)
            witness = tuple(tuple(block) for block in blocks)
            return
        vertex = ordered[position]
        for block in blocks:
            if all(adjacent(edges, vertex, member) for member in block):
                block.append(vertex)
                visit(position + 1)
                block.pop()
        blocks.append([vertex])
        visit(position + 1)
        blocks.pop()

    visit(0)
    assert witness is not None
    return best, witness


def legal_successors(
    state: frozenset[int],
    attacked: int,
    edges: frozenset[frozenset[int]],
) -> tuple[tuple[int, frozenset[int]], ...]:
    assert attacked not in state
    return tuple(
        (
            guard,
            frozenset((state - {guard}) | {attacked}),
        )
        for guard in sorted(state)
        if adjacent(edges, guard, attacked)
    )


def colored_configuration_digraph(
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
    size: int,
) -> tuple[
    frozenset[frozenset[int]],
    dict[tuple[frozenset[int], int], tuple[frozenset[int], ...]],
]:
    states = frozenset(
        state
        for state in subsets(vertices, size)
        if dominates(state, vertices, edges)
    )
    arcs = {}
    for state in states:
        for attacked in sorted(vertices - state):
            arcs[(state, attacked)] = tuple(
                successor
                for _, successor in legal_successors(state, attacked, edges)
                if successor in states
            )
    return states, arcs


def greatest_eternal_family(
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
    size: int,
) -> tuple[frozenset[frozenset[int]], tuple[int, ...]]:
    states, arcs = colored_configuration_digraph(vertices, edges, size)
    current = states
    stages = [len(current)]
    while True:
        kept = frozenset(
            state
            for state in current
            if all(
                any(successor in current for successor in arcs[(state, attacked)])
                for attacked in vertices - state
            )
        )
        if kept == current:
            return current, tuple(stages)
        current = kept
        stages.append(len(current))


def family_obligations(
    family: frozenset[frozenset[int]],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> tuple[int, str]:
    assert family
    rows = []
    for state in sorted(family, key=lambda item: tuple(sorted(item))):
        assert dominates(state, vertices, edges)
        for attacked in sorted(vertices - state):
            answers = []
            for guard, successor in legal_successors(state, attacked, edges):
                if successor in family:
                    assert dominates(successor, vertices, edges)
                    answers.append(guard)
            assert answers
            rows.append([sorted(state), attacked, answers])
    encoding = json.dumps(rows, separators=(",", ":"), sort_keys=True).encode()
    return len(rows), hashlib.sha256(encoding).hexdigest()


def graph_parameters(
    vertices: frozenset[int], edges: frozenset[frozenset[int]]
) -> tuple[dict[str, int], tuple[tuple[int, ...], ...]]:
    gamma = minimum_size(
        vertices, lambda state: dominates(state, vertices, edges)
    )
    independent_sets = [
        state
        for size in range(1, len(vertices) + 1)
        for state in subsets(vertices, size)
        if independent(state, edges)
    ]
    independence = max(map(len, independent_sets))
    independent_domination = min(
        len(state)
        for state in independent_sets
        if maximal_independent(state, vertices, edges)
    )
    eternal = next(
        size
        for size in range(1, len(vertices) + 1)
        if greatest_eternal_family(vertices, edges, size)[0]
    )
    theta, partition = clique_partition_number(vertices, edges)
    return {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": independence,
        "gamma_infinity": eternal,
        "theta": theta,
    }, partition


def response_lists(
    reference: frozenset[int],
    family: frozenset[frozenset[int]],
    vertices: frozenset[int],
) -> dict[int, tuple[int, ...]]:
    answer = {}
    for outside in sorted(vertices - reference):
        answer[outside] = tuple(
            removed
            for removed in sorted(reference)
            if frozenset((reference - {removed}) | {outside}) in family
        )
        assert answer[outside]
    return answer


def static_response_lists(
    reference: frozenset[int],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> dict[int, tuple[int, ...]]:
    answer = {}
    for outside in sorted(vertices - reference):
        answer[outside] = tuple(
            removed
            for removed in sorted(reference)
            if adjacent(edges, removed, outside)
            and dominates(
                frozenset((reference - {removed}) | {outside}),
                vertices,
                edges,
            )
        )
    return answer


def complement_neighbors(
    vertex: int,
    universe: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> frozenset[int]:
    return frozenset(
        other
        for other in universe
        if other != vertex and not adjacent(edges, vertex, other)
    )


def complement_components(
    universe: frozenset[int], edges: frozenset[frozenset[int]]
) -> tuple[tuple[int, ...], ...]:
    unseen = set(universe)
    answer = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = deque((root,))
        component = {root}
        while queue:
            left = queue.popleft()
            for right in sorted(
                complement_neighbors(left, universe, edges) & unseen
            ):
                unseen.remove(right)
                component.add(right)
                queue.append(right)
        answer.append(tuple(sorted(component)))
    return tuple(sorted(answer))


def frozen_components(
    frozen: int,
    reference: frozenset[int],
    lists: dict[int, tuple[int, ...]],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> tuple[tuple[int, ...], ...]:
    universe = frozenset(
        set(reference - {frozen})
        | {
            outside
            for outside in vertices - reference
            if frozen not in lists[outside]
        }
    )
    return complement_components(universe, edges)


def audit_fdzro() -> dict[str, object]:
    record = "FDzro"
    vertices, edges = decode_graph6(record)
    assert encode_graph6(vertices, edges) == record
    parameters, partition = graph_parameters(vertices, edges)
    assert parameters == {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    assert len(FDZRO_FAMILY) == 21
    obligations, obligation_hash = family_obligations(
        FDZRO_FAMILY, vertices, edges
    )
    assert obligations == 84

    greatest, stages = greatest_eternal_family(vertices, edges, 3)
    assert len(greatest) == 33
    assert FDZRO_FAMILY < greatest

    reference = frozenset((0, 1, 2))
    lists = response_lists(reference, FDZRO_FAMILY, vertices)
    assert lists == {
        3: (0,),
        4: (0, 2),
        5: (1, 2),
        6: (1,),
    }
    static_lists = static_response_lists(reference, vertices, edges)
    assert all(set(lists[x]) <= set(static_lists[x]) for x in lists)

    induced = (3, 4, 5, 6)
    complement_path_edges = {
        frozenset((3, 4)),
        frozenset((4, 5)),
        frozenset((5, 6)),
    }
    actual_complement_edges = {
        frozenset(pair)
        for pair in combinations(induced, 2)
        if not adjacent(edges, *pair)
    }
    assert actual_complement_edges == complement_path_edges

    frozen_1 = frozen_components(1, reference, lists, vertices, edges)
    frozen_0 = frozen_components(0, reference, lists, vertices, edges)
    assert (3, 4) in frozen_1
    assert (5, 6) in frozen_0

    defect_left = tuple(
        sorted(
            complement_neighbors(2, vertices, edges)
            & complement_neighbors(3, vertices, edges)
        )
    )
    defect_right = tuple(
        sorted(
            complement_neighbors(2, vertices, edges)
            & complement_neighbors(6, vertices, edges)
        )
    )
    assert defect_left == (1,)
    assert defect_right == (0,)

    return {
        "graph6": record,
        "edges": [sorted(edge) for edge in sorted(edges, key=lambda e: tuple(sorted(e)))],
        "parameters": parameters,
        "clique_partition": [list(block) for block in partition],
        "specified_family_states": len(FDZRO_FAMILY),
        "specified_family_obligations": obligations,
        "specified_obligation_sha256": obligation_hash,
        "greatest_family_states": len(greatest),
        "greatest_family_stages": list(stages),
        "family_response_lists": {
            str(vertex): list(values) for vertex, values in lists.items()
        },
        "static_response_lists": {
            str(vertex): list(values) for vertex, values in static_lists.items()
        },
        "free_components": {
            "frozen_1": [list(component) for component in frozen_1],
            "frozen_0": [list(component) for component in frozen_0],
        },
        "induced_complement_path": list(induced),
        "anchor_only_defect_ridges": [list(defect_left), list(defect_right)],
    }


def audit_fczbg() -> dict[str, object]:
    record = "FCZbg"
    vertices, edges = decode_graph6(record)
    assert encode_graph6(vertices, edges) == record
    parameters, partition = graph_parameters(vertices, edges)
    assert parameters == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    family, stages = greatest_eternal_family(vertices, edges, 3)
    assert len(family) == 18
    obligations, obligation_hash = family_obligations(family, vertices, edges)
    assert obligations == 72

    reference = frozenset((3, 4, 5))
    lists = response_lists(reference, family, vertices)
    assert lists == {
        0: (3,),
        1: (4, 5),
        2: (4, 5),
        6: (5,),
    }
    left = tuple(
        sorted(
            complement_neighbors(4, vertices, edges)
            & complement_neighbors(0, vertices, edges)
        )
    )
    right = tuple(
        sorted(
            complement_neighbors(4, vertices, edges)
            & complement_neighbors(6, vertices, edges)
        )
    )
    assert left == (6,)
    assert right == (0,)
    exchange = frozenset((0, 4, 6))
    assert exchange in family

    # Directly check both one-guard exchange obligations.
    assert (
        3,
        frozenset((0, 4, 6)),
    ) in legal_successors(frozenset((3, 4, 6)), 0, edges)
    assert (
        5,
        frozenset((0, 4, 6)),
    ) in legal_successors(frozenset((0, 4, 5)), 6, edges)

    return {
        "graph6": record,
        "edges": [sorted(edge) for edge in sorted(edges, key=lambda e: tuple(sorted(e)))],
        "parameters": parameters,
        "clique_partition": [list(block) for block in partition],
        "greatest_family_states": len(family),
        "greatest_family_stages": list(stages),
        "unoccupied_attack_obligations": obligations,
        "obligation_sha256": obligation_hash,
        "family_response_lists": {
            str(vertex): list(values) for vertex, values in lists.items()
        },
        "defect_ridges_at_shared_anchor_4": {
            "pin_0": list(left),
            "pin_6": list(right),
        },
        "retained_exchange_state": sorted(exchange),
    }


def audit_hashes() -> dict[str, object]:
    manifest_path = CANDIDATE / "MANIFEST.json"
    assert sha256(manifest_path) == CANDIDATE_MANIFEST_SHA256
    manifest = json.loads(manifest_path.read_text())
    checked = {}
    for relative, expected in manifest["files"].items():
        path = ROOT / relative
        actual = sha256(path)
        assert actual == expected, (relative, expected, actual)
        checked[relative] = actual
    dependency_checked = {}
    for relative, expected in DEPENDENCIES.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, (relative, expected, actual)
        dependency_checked[relative] = actual
    return {
        "candidate_manifest_sha256": CANDIDATE_MANIFEST_SHA256,
        "candidate_files": checked,
        "accepted_dependency_notes": dependency_checked,
    }


def main() -> None:
    result = {
        "schema": "first-cross-clause-hostile-clean-room-v1",
        "verdict": "PASS_STRICT_SCOPE",
        "model": (
            "attacks only at unoccupied vertices; exactly one adjacent guard "
            "moves; every retained successor dominates"
        ),
        "candidate_hash_audit": audit_hashes(),
        "fdzro_literal_control": audit_fdzro(),
        "fczbg_equality_ridge_control": audit_fczbg(),
        "scope": {
            "four_parity_types": "PROVED_GIVEN_C124",
            "component_intersection_singleton_shared_color":
                "PROVED_GIVEN_NONEMPTY_PROPER_LISTS",
            "shared_anchor_complete_to_support_components":
                "PROVED_FROM_FREE_COMPONENT_SEPARATION",
            "odd_singleton_defect_ridge": "PROVED",
            "odd_odd_ridges_disjoint": "PROVED_GIVEN_C120_C124",
            "literal_p4_c121_identification":
                "ONLY_WITH_INDUCEDNESS_AND_EXACT_STATIC_LISTS",
            "even_arms": "OPEN",
            "anchor_only_ridges_under_equality": "OPEN",
            "all_first_cross_clauses": "OPEN",
            "complete_k3": "OPEN",
            "universal_conjecture": "OPEN",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
