#!/usr/bin/env python3
"""Clean-room audit of the paired-repair implication countercontrol.

The graph is decoded from the frozen graph6 record.  This checker does not
import the campaign evaluator, the source verifier, or any search artifact.
It independently rebuilds the restricted fixed point, direct response lists,
response formula, minimal cores, marked implication paths, and gate geometry.
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
SOURCE = CAMPAIGN / "math/working/paired_repair_implication"
GRAPH6 = "RBn]r]vj]lnZ~^~n~z~^z|~nz~^j~w"
N = 19
ANCHOR = (0, 1, 2)
ALL_VERTICES = (1 << N) - 1

EXPECTED_H_EDGES = {
    (0, 1), (0, 2), (0, 3), (0, 7), (0, 11),
    (1, 2), (1, 4), (1, 8), (1, 9),
    (2, 5), (2, 6), (2, 10),
    (3, 7), (3, 9), (3, 15),
    (4, 8), (4, 10), (4, 16), (4, 18),
    (5, 6), (5, 11), (5, 17),
    (6, 9), (6, 12), (6, 18),
    (7, 10), (7, 13),
    (8, 11), (8, 14),
    (12, 15), (13, 16), (14, 17),
}

EXPECTED_LISTS = {
    3: (1, 2), 4: (0, 2), 5: (0, 1), 6: (0, 1),
    7: (1, 2), 8: (0, 2), 9: (0, 2), 10: (0, 1),
    11: (1, 2), 12: (1, 2), 13: (0, 2), 14: (0, 1),
    15: (1, 2), 16: (0, 2), 17: (0, 1), 18: (1, 2),
}

EXPECTED_COMPONENTS = [
    (0, (3, 7, 12, 15)),
    (0, (11,)),
    (0, (18,)),
    (1, (4, 8, 13, 16)),
    (1, (9,)),
    (2, (5, 6, 14, 17)),
    (2, (10,)),
]

EXPECTED_CLAUSES = [
    ((-1, -5), (3, 9)),
    ((4, 7), (4, 10)),
    ((-4, -3), (4, 18)),
    ((-6, 2), (5, 11)),
    ((-6, 5), (6, 9)),
    ((6, 1), (6, 12)),
    ((6, 3), (6, 18)),
    ((-1, -7), (7, 10)),
    ((1, -4), (7, 13)),
    ((4, -2), (8, 11)),
    ((-4, 6), (8, 14)),
]

OLD_CORE = (0, 1, 3, 4, 5, 7, 8, 9, 10)
ARM_CORE = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
ARM_INDICES = (2, 6)


def edge(u: int, v: int) -> tuple[int, int]:
    assert u != v
    return (u, v) if u < v else (v, u)


def mask(vertices: tuple[int, ...]) -> int:
    value = 0
    for vertex in vertices:
        value |= 1 << vertex
    return value


def vertices(state: int) -> tuple[int, ...]:
    return tuple(v for v in range(N) if state >> v & 1)


def decode_graph6(record: str) -> set[tuple[int, int]]:
    raw = record.encode("ascii")
    assert raw[0] != 126, "only the one-byte order form is expected"
    order = raw[0] - 63
    assert order == N
    bits: list[int] = []
    for byte in raw[1:]:
        assert 63 <= byte <= 126
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    assert len(bits) >= needed and not any(bits[needed:])
    result: set[tuple[int, int]] = set()
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                result.add((left, right))
            cursor += 1
    return result


G_EDGES = decode_graph6(GRAPH6)
ALL_EDGES = set(combinations(range(N), 2))
H_EDGES = ALL_EDGES - G_EDGES
G_ADJ = [0] * N
H_ADJ = [0] * N
for u, v in G_EDGES:
    G_ADJ[u] |= 1 << v
    G_ADJ[v] |= 1 << u
for u, v in H_EDGES:
    H_ADJ[u] |= 1 << v
    H_ADJ[v] |= 1 << u
G_CLOSED = [G_ADJ[v] | 1 << v for v in range(N)]


def dominates(state: int) -> bool:
    reached = 0
    pending = state
    while pending:
        bit = pending & -pending
        pending ^= bit
        reached |= G_CLOSED[bit.bit_length() - 1]
    return reached == ALL_VERTICES


def independent_g(state: int) -> bool:
    pending = state
    while pending:
        bit = pending & -pending
        pending ^= bit
        vertex = bit.bit_length() - 1
        if G_ADJ[vertex] & pending:
            return False
    return True


def direct_state(attacked: int, moved_guard: int) -> int:
    return (mask(ANCHOR) ^ (1 << moved_guard)) | (1 << attacked)


def successors(state: int, attacked: int) -> tuple[int, ...]:
    answer: list[int] = []
    for guard in vertices(state):
        if G_ADJ[guard] >> attacked & 1:
            answer.append((state ^ (1 << guard)) | (1 << attacked))
    return tuple(answer)


def greatest_kernel(
    initial: set[int],
) -> tuple[set[int], list[int]]:
    family = set(initial)
    round_sizes: list[int] = []
    while True:
        doomed: set[int] = set()
        for state in family:
            for attacked in range(N):
                if state >> attacked & 1:
                    continue
                if not any(
                    successor in family
                    for successor in successors(state, attacked)
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return family, round_sizes
        round_sizes.append(len(doomed))
        family.difference_update(doomed)


def family_digest(family: set[int]) -> str:
    lines = [
        ",".join(str(v) for v in vertices(state))
        for state in sorted(family, key=vertices)
    ]
    return sha256("\n".join(lines).encode("ascii")).hexdigest()


def bipartite_components() -> tuple[
    list[tuple[int, tuple[int, ...], dict[int, int]]],
    dict[int, tuple[int, int]],
]:
    missing = {
        vertex: next(iter(set(ANCHOR) - set(EXPECTED_LISTS[vertex])))
        for vertex in EXPECTED_LISTS
    }
    components: list[tuple[int, tuple[int, ...], dict[int, int]]] = []
    location: dict[int, tuple[int, int]] = {}
    for omitted in ANCHOR:
        unseen = {v for v in EXPECTED_LISTS if missing[v] == omitted}
        while unseen:
            root = min(unseen)
            unseen.remove(root)
            side = {root: 0}
            queue = deque([root])
            while queue:
                current = queue.popleft()
                for neighbor in range(3, N):
                    if neighbor == current:
                        continue
                    if missing.get(neighbor) != omitted:
                        continue
                    if edge(current, neighbor) not in H_EDGES:
                        continue
                    if neighbor in side:
                        assert side[neighbor] != side[current]
                    else:
                        side[neighbor] = 1 - side[current]
                        unseen.remove(neighbor)
                        queue.append(neighbor)
            component_index = len(components)
            component_vertices = tuple(sorted(side))
            components.append((omitted, component_vertices, side))
            for vertex, parity in side.items():
                location[vertex] = (component_index, parity)
    return components, location


def build_formula() -> tuple[
    list[tuple[tuple[int, int], tuple[int, int]]],
    list[tuple[int, tuple[int, ...], dict[int, int]]],
]:
    components, location = bipartite_components()
    missing = {
        vertex: next(iter(set(ANCHOR) - set(EXPECTED_LISTS[vertex])))
        for vertex in EXPECTED_LISTS
    }
    clauses: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for u, v in sorted(H_EDGES):
        if u in ANCHOR or v in ANCHOR or missing[u] == missing[v]:
            continue
        common = set(EXPECTED_LISTS[u]) & set(EXPECTED_LISTS[v])
        assert len(common) == 1
        common_color = next(iter(common))
        literals: list[int] = []
        for endpoint in (u, v):
            variable, parity = location[endpoint]
            color_position = EXPECTED_LISTS[endpoint].index(common_color)
            forbidden_value = parity ^ color_position
            # This literal is true precisely when the endpoint does not take
            # the one color common to the two lists.
            literals.append(
                variable + 1 if forbidden_value == 0 else -(variable + 1)
            )
        clauses.append((tuple(literals), (u, v)))
    return clauses, components


def clause_true(clause: tuple[int, int], assignment: tuple[int, ...]) -> bool:
    for literal in clause:
        value = bool(assignment[abs(literal) - 1])
        if (literal > 0 and value) or (literal < 0 and not value):
            return True
    return False


def formula_models(
    clauses: list[tuple[tuple[int, int], tuple[int, int]]],
    indices: tuple[int, ...],
    variable_count: int,
) -> list[tuple[int, ...]]:
    return [
        assignment
        for assignment in product((0, 1), repeat=variable_count)
        if all(clause_true(clauses[i][0], assignment) for i in indices)
    ]


def minimal_unsat(
    clauses: list[tuple[tuple[int, int], tuple[int, int]]],
    indices: tuple[int, ...],
    variable_count: int,
) -> bool:
    if formula_models(clauses, indices, variable_count):
        return False
    return all(
        formula_models(
            clauses,
            indices[:position] + indices[position + 1:],
            variable_count,
        )
        for position in range(len(indices))
    )


def implication_path(
    clauses: list[tuple[tuple[int, int], tuple[int, int]]],
    indices: tuple[int, ...],
    source: int,
    target: int,
    variable_count: int,
) -> tuple[tuple[int, int, int], ...] | None:
    adjacency = {
        literal: []
        for variable in range(1, variable_count + 1)
        for literal in (variable, -variable)
    }
    for clause_index in indices:
        left, right = clauses[clause_index][0]
        adjacency[-left].append((right, clause_index))
        adjacency[-right].append((left, clause_index))
    queue = deque([source])
    previous: dict[int, tuple[int, int] | None] = {source: None}
    while queue:
        literal = queue.popleft()
        if literal == target:
            break
        for following, clause_index in adjacency[literal]:
            if following not in previous:
                previous[following] = (literal, clause_index)
                queue.append(following)
    if target not in previous:
        return None
    reverse: list[tuple[int, int, int]] = []
    current = target
    while previous[current] is not None:
        prior, via = previous[current]  # type: ignore[misc]
        reverse.append((prior, current, via))
        current = prior
    return tuple(reversed(reverse))


def color_from_assignment(
    vertex: int,
    assignment: tuple[int, ...],
    location: dict[int, tuple[int, int]],
) -> int:
    variable, parity = location[vertex]
    position = parity ^ assignment[variable]
    return EXPECTED_LISTS[vertex][position]


def all_obligations(family: set[int]) -> int:
    obligations = 0
    for state in family:
        assert dominates(state)
        for attacked in range(N):
            if state >> attacked & 1:
                continue
            obligations += 1
            assert any(
                successor in family
                for successor in successors(state, attacked)
            )
    return obligations


def gate_audit(
    clauses: list[tuple[tuple[int, int], tuple[int, int]]],
    location: dict[int, tuple[int, int]],
) -> dict[str, object]:
    rows = [
        # left, right, cap, original-right, midpoint, cap-anchor
        (6, 3, 9, 12, 15, 1),
        (7, 4, 10, 13, 16, 2),
        (8, 5, 11, 14, 17, 0),
    ]
    gate_clause_sets = [
        (0, 4, 5),
        (1, 7, 8),
        (3, 9, 10),
    ]
    local_equalities: list[bool] = []
    for row, selected in zip(rows, gate_clause_sets):
        left, right, cap, original, midpoint, cap_anchor = row
        for h_edge in (
            edge(left, cap),
            edge(right, cap),
            edge(left, original),
            edge(original, midpoint),
            edge(midpoint, right),
            edge(cap_anchor, cap),
        ):
            assert h_edge in H_EDGES
        assert edge(left, right) in G_EDGES
        # The original-right and right ports are same-type, same-side
        # representatives joined by an even physicalization path.
        assert location[original] == location[right]

        endpoint_variable_left, endpoint_side_left = location[left]
        endpoint_variable_right, endpoint_side_right = location[right]
        type_left = next(
            iter(set(ANCHOR) - set(EXPECTED_LISTS[left]))
        )
        type_right = next(
            iter(set(ANCHOR) - set(EXPECTED_LISTS[right]))
        )
        # In the cyclic (0,1,2) chirality convention, types 0 and 2 use
        # the reverse of sorted list order, while type 1 uses sorted order.
        orientation_left = int(type_left in (0, 2))
        orientation_right = int(type_right in (0, 2))
        permitted: set[tuple[int, int]] = set()
        for assignment in product((0, 1), repeat=7):
            if all(clause_true(clauses[i][0], assignment) for i in selected):
                # The orientation bit converts component coordinates to
                # the cyclic chirality convention.
                local_left = (
                    assignment[endpoint_variable_left]
                    ^ endpoint_side_left
                    ^ orientation_left
                )
                local_right = (
                    assignment[endpoint_variable_right]
                    ^ endpoint_side_right
                    ^ orientation_right
                )
                permitted.add((local_left, local_right))
        assert permitted == {(0, 0), (1, 1)}
        local_equalities.append(True)

    connectors = ((3, 7), (4, 8), (5, 6))
    connector_flips: list[bool] = []
    for u, v in connectors:
        assert edge(u, v) in H_EDGES
        component_u, side_u = location[u]
        component_v, side_v = location[v]
        assert component_u == component_v and side_u != side_v
        connector_flips.append(True)

    return {
        "gate_clause_sets": [list(item) for item in gate_clause_sets],
        "all_three_gates_preserve_local_chirality": all(local_equalities),
        "all_three_connectors_reverse_local_chirality": all(connector_flips),
        "odd_connector_count": len(connectors),
    }


def main() -> None:
    assert len(G_EDGES) == 139
    assert H_EDGES == EXPECTED_H_EDGES

    result = json.loads((SOURCE / "result.json").read_text(encoding="utf-8"))
    assert result["graph6"] == GRAPH6
    assert result["order"] == N and result["size"] == len(G_EDGES)

    dominating_singletons = [
        mask((v,)) for v in range(N) if dominates(mask((v,)))
    ]
    dominating_pairs = [
        mask(pair_vertices)
        for pair_vertices in combinations(range(N), 2)
        if dominates(mask(pair_vertices))
    ]
    assert not dominating_singletons
    assert len(dominating_pairs) == 93
    assert vertices(dominating_pairs[0]) == (0, 11)

    independent_four_sets = [
        item
        for item in combinations(range(N), 4)
        if independent_g(mask(item))
    ]
    assert independent_g(mask(ANCHOR))
    assert not independent_four_sets
    independent_dominating_pairs = [
        state for state in dominating_pairs if independent_g(state)
    ]
    assert independent_dominating_pairs
    assert result["parameters"] == {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }

    all_dominating_pairs = set(dominating_pairs)
    pair_kernel, pair_rounds = greatest_kernel(all_dominating_pairs)
    assert not pair_kernel

    forbidden = {
        direct_state(vertex, moved_guard)
        for vertex, allowed in EXPECTED_LISTS.items()
        for moved_guard in ANCHOR
        if moved_guard not in allowed
    }
    assert len(forbidden) == 16
    all_dominating_triples = {
        mask(item)
        for item in combinations(range(N), 3)
        if dominates(mask(item))
    }
    family, deletion_rounds = greatest_kernel(
        all_dominating_triples - forbidden
    )
    assert deletion_rounds == [51, 37, 63, 29, 10]
    assert len(family) == 703
    assert family_digest(family) == (
        "c116c4a60299fea35d30bf09bda9b1faa31b39533caac8eb265818cd1347874d"
    )
    obligations = all_obligations(family)
    assert obligations == 11248

    rebuilt_lists = {
        vertex: tuple(
            moved_guard
            for moved_guard in ANCHOR
            if direct_state(vertex, moved_guard) in family
        )
        for vertex in range(3, N)
    }
    assert rebuilt_lists == EXPECTED_LISTS
    assert result["restricted_family"] == {
        "deletion_round_sizes": deletion_rounds,
        "one_guard_obligations": obligations,
        "sha256": family_digest(family),
        "size": len(family),
    }
    assert {
        int(vertex): tuple(allowed)
        for vertex, allowed in result["response_lists"].items()
    } == rebuilt_lists

    # theta(H)=3: the anchor is an H-triangle, and the frozen coloring is
    # checked edge by edge.
    theta_coloring = result["theta_coloring_of_H"]
    assert len(theta_coloring) == N
    assert len(set(theta_coloring)) == 3
    assert all(theta_coloring[u] != theta_coloring[v] for u, v in H_EDGES)
    assert all(edge(u, v) in H_EDGES for u, v in combinations(ANCHOR, 2))

    clauses, components = build_formula()
    location = {
        vertex: (component_index, side[vertex])
        for component_index, (_, component_vertices, side)
        in enumerate(components)
        for vertex in component_vertices
    }
    assert [
        (omitted, component_vertices)
        for omitted, component_vertices, _ in components
    ] == EXPECTED_COMPONENTS
    assert clauses == EXPECTED_CLAUSES
    variable_count = len(components)
    assert variable_count == 7

    # Independent semantic check: each Boolean assignment colors every
    # same-type H edge properly by construction; the CNF is true iff all
    # cross-type H edges are also properly colored.
    full_indices = tuple(range(len(clauses)))
    for assignment in product((0, 1), repeat=variable_count):
        colors = {
            vertex: color_from_assignment(vertex, assignment, location)
            for vertex in range(3, N)
        }
        proper_cross = all(
            colors[u] != colors[v]
            for u, v in H_EDGES
            if u >= 3
            and v >= 3
            and set(EXPECTED_LISTS[u]) != set(EXPECTED_LISTS[v])
        )
        formula_true = all(
            clause_true(clause, assignment) for clause, _ in clauses
        )
        assert proper_cross == formula_true
    assert not formula_models(clauses, full_indices, variable_count)

    unsat_by_size: dict[int, list[tuple[int, ...]]] = {}
    for selected_size in range(1, len(clauses) + 1):
        unsat = [
            chosen
            for chosen in combinations(range(len(clauses)), selected_size)
            if not formula_models(clauses, chosen, variable_count)
        ]
        if unsat:
            unsat_by_size[selected_size] = unsat
            break
    assert unsat_by_size == {9: [OLD_CORE]}
    assert minimal_unsat(clauses, OLD_CORE, variable_count)
    assert minimal_unsat(clauses, ARM_CORE, variable_count)

    arm_minimal_cores: list[tuple[int, ...]] = []
    arm_minimum_size = None
    for selected_size in range(2, len(clauses) + 1):
        for chosen in combinations(range(len(clauses)), selected_size):
            if not set(ARM_INDICES).issubset(chosen):
                continue
            if minimal_unsat(clauses, chosen, variable_count):
                arm_minimal_cores.append(chosen)
        if arm_minimal_cores:
            arm_minimum_size = selected_size
            break
    assert arm_minimum_size == 10
    assert arm_minimal_cores == [ARM_CORE]
    assert all(len(clauses[index][0]) == 2 for index in ARM_CORE)

    left_arm = set(clauses[2][0])
    right_arm = set(clauses[6][0])
    assert 3 in right_arm and -3 in left_arm
    resolvent = (left_arm - {-3}) | (right_arm - {3})
    assert resolvent == set(clauses[10][0]) == {-4, 6}

    opposite_route = tuple(index for index in OLD_CORE if index != 10)
    for source, target in ((4, -6), (6, -4), (-4, 6), (-6, 4)):
        assert implication_path(
            clauses,
            opposite_route,
            source,
            target,
            variable_count,
        ) is not None
    # The route consequences are (-4 or -6) and (4 or 6).  Resolving
    # each with the arm resolvent (-4 or 6) yields the logical units -4
    # and 6, although neither is a syntactic unit in the selected core.
    assert ({-4, 6} - {6}) | ({-4, -6} - {-6}) == {-4}
    assert ({-4, 6} - {-4}) | ({4, 6} - {4}) == {6}

    old_forward = implication_path(
        clauses, OLD_CORE, 4, -4, variable_count
    )
    old_reverse = implication_path(
        clauses, OLD_CORE, -4, 4, variable_count
    )
    arm_forward = implication_path(
        clauses, ARM_CORE, 4, -4, variable_count
    )
    arm_reverse = implication_path(
        clauses, ARM_CORE, -4, 4, variable_count
    )
    assert old_forward is not None and old_reverse is not None
    assert arm_forward is not None and arm_reverse is not None
    assert [len(path) for path in (
        old_forward, old_reverse, arm_forward, arm_reverse
    )] == [4, 5, 5, 5]
    assert tuple((u, v) for u, v, _ in old_forward) == (
        (4, 1), (1, -5), (-5, -6), (-6, -4)
    )
    displayed_arm_forward = (
        (4, 1, 8),
        (1, -5, 0),
        (-5, -6, 4),
        (-6, 3, 6),
        (3, -4, 2),
    )
    assert all(
        clause_index in ARM_CORE
        and (
            (clauses[clause_index][0][0] == -u
             and clauses[clause_index][0][1] == v)
            or
            (clauses[clause_index][0][1] == -u
             and clauses[clause_index][0][0] == v)
        )
        for u, v, clause_index in displayed_arm_forward
    )
    assert tuple((u, v) for u, v, _ in old_reverse) == tuple(
        (u, v) for u, v, _ in arm_reverse
    ) == (
        (-4, 7), (7, -1), (-1, 6), (6, 2), (2, 4)
    )
    assert result["response_formula"] == {
        "clause_count": 11,
        "duplicated_original_clause_index": 10,
        "minimum_q_arm_core": list(ARM_CORE),
        "minimum_q_arm_core_size": 10,
        "minimum_unsat_core": list(OLD_CORE),
        "minimum_unsat_core_size": 9,
        "q_arm_clause_indices": list(ARM_INDICES),
        "q_arm_resolvent": [-4, 6],
        "shortest_path_lengths": {
            "old_forward": 4,
            "old_reverse": 5,
            "q_arm_forward": 5,
            "q_arm_reverse": 5,
        },
        "variable_count": 7,
    }

    gate_result = gate_audit(clauses, location)

    common_4_6 = tuple(
        v for v in range(N)
        if v not in (4, 6)
        and edge(4, v) in H_EDGES
        and edge(6, v) in H_EDGES
    )
    assert common_4_6 == (18,)
    assert edge(4, 18) in H_EDGES and edge(6, 18) in H_EDGES
    assert edge(0, 18) in G_EDGES
    assert EXPECTED_LISTS[18] == (1, 2)
    assert result["critical_pair"] == {
        "anchor_witness_edge_in_G": True,
        "omitted_anchor": 0,
        "unique_common_H_neighbor": 18,
        "vertices": [4, 6],
        "witness_list": [1, 2],
    }
    assert result["dominating_pair_count"] == 93
    assert result["one_dominating_pair"] == [0, 11]

    source_hashes = {
        filename: sha256((SOURCE / filename).read_bytes()).hexdigest()
        for filename in ("NOTE.md", "verify.py", "result.json")
    }
    evidence = {
        "verdict": "PASS",
        "source_sha256": source_hashes,
        "graph": {
            "graph6": GRAPH6,
            "order": N,
            "size": len(G_EDGES),
            "complement_size": len(H_EDGES),
            "graph6_decodes_to_displayed_complement": True,
        },
        "parameters": {
            "gamma": 2,
            "i": 2,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
            "dominating_pair_count": len(dominating_pairs),
            "independent_dominating_pair_count": len(
                independent_dominating_pairs
            ),
            "two_guard_greatest_kernel_size": len(pair_kernel),
            "two_guard_deletion_round_sizes": pair_rounds,
        },
        "restricted_family": {
            "initial_dominating_triples": len(all_dominating_triples),
            "forbidden_direct_states": len(forbidden),
            "deletion_round_sizes": deletion_rounds,
            "size": len(family),
            "sha256": family_digest(family),
            "obligations": obligations,
            "all_direct_lists_exact_two_lists": all(
                len(value) == 2 for value in rebuilt_lists.values()
            ),
        },
        "response_formula": {
            "variables": variable_count,
            "clauses": len(clauses),
            "full_formula_unsat": True,
            "unique_minimum_unsat_core": list(OLD_CORE),
            "unique_minimum_unsat_core_size": 9,
            "unique_smallest_minimal_core_with_arms": list(ARM_CORE),
            "unique_smallest_minimal_core_with_arms_size": 10,
            "arm_indices": list(ARM_INDICES),
            "arm_resolvent": sorted(resolvent),
            "duplicated_clause": list(clauses[10][0]),
            "shortest_marked_lengths": {
                "old_forward": len(old_forward),
                "old_reverse": len(old_reverse),
                "arm_forward": len(arm_forward),
                "arm_reverse": len(arm_reverse),
            },
            "both_cores_binary_and_unit_free": True,
            "opposite_route_implies_both_inequality_clauses": True,
            "derived_endpoint_units": [-4, 6],
            "derived_units_are_not_syntactic_unit_clauses": True,
        },
        "gate_geometry": gate_result,
        "critical_pair": {
            "vertices": [4, 6],
            "unique_common_H_neighbor": 18,
            "witness_exact_list": list(EXPECTED_LISTS[18]),
            "omitted_anchor_edge_is_in_G": True,
        },
        "scope": {
            "gamma_is_two_not_three": True,
            "family_is_restricted_not_claimed_greatest_unrestricted": True,
            "countercontrol_does_not_refute_gamma_three_descent": True,
            "universal_conjecture_not_claimed_resolved": True,
        },
    }
    (HERE / "evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    print("PASS")


if __name__ == "__main__":
    main()
