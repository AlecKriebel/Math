#!/usr/bin/env python3
"""Independent verifier for the paired-repair gamma-two countercontrol.

The script uses only the explicit complement edge set and the displayed
response-list restriction.  It reconstructs the greatest closed subfamily
subject to that restriction, all exact parameters needed for the control,
the response 2-CNF, and its two distinguished minimal unsatisfiable cores.
It imports no campaign evaluator or SAT/search implementation.
"""

from __future__ import annotations

import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ORDER = 19
S = (0, 1, 2)
EXPECTED_GRAPH6 = "RBn]r]vj]lnZ~^~n~z~^z|~nz~^j~w"
EXPECTED_FAMILY_SIZE = 703
EXPECTED_FAMILY_SHA256 = (
    "c116c4a60299fea35d30bf09bda9b1faa31b39533caac8eb265818cd1347874d"
)
EXPECTED_DELETION_ROUNDS = [51, 37, 63, 29, 10]

H_EDGES = {
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 7),
    (0, 11),
    (1, 2),
    (1, 4),
    (1, 8),
    (1, 9),
    (2, 5),
    (2, 6),
    (2, 10),
    (3, 7),
    (3, 9),
    (3, 15),
    (4, 8),
    (4, 10),
    (4, 16),
    (4, 18),
    (5, 6),
    (5, 11),
    (5, 17),
    (6, 9),
    (6, 12),
    (6, 18),
    (7, 10),
    (7, 13),
    (8, 11),
    (8, 14),
    (12, 15),
    (13, 16),
    (14, 17),
}

EXPECTED_LISTS = {
    3: (1, 2),
    4: (0, 2),
    5: (0, 1),
    6: (0, 1),
    7: (1, 2),
    8: (0, 2),
    9: (0, 2),
    10: (0, 1),
    11: (1, 2),
    12: (1, 2),
    13: (0, 2),
    14: (0, 1),
    15: (1, 2),
    16: (0, 2),
    17: (0, 1),
    18: (1, 2),
}

# Deterministic component ordering gives variables 1,...,7.  Each clause is
# paired with the literal H-edge that supports it.
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
Q_ARM_CORE = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
Q_ARM_CLAUSES = (2, 6)


def pair(u: int, v: int) -> tuple[int, int]:
    if u == v:
        raise ValueError("loop")
    return (u, v) if u < v else (v, u)


ALL_EDGES = set(combinations(range(ORDER), 2))
G_EDGES = ALL_EDGES - H_EDGES


def graph6() -> str:
    bits = [
        int((i, j) in G_EDGES)
        for j in range(1, ORDER)
        for i in range(j)
    ]
    while len(bits) % 6:
        bits.append(0)
    chars = [chr(ORDER + 63)]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def dominates(state: tuple[int, ...]) -> bool:
    occupied = set(state)
    return all(
        vertex in occupied
        or any(pair(vertex, guard) in G_EDGES for guard in state)
        for vertex in range(ORDER)
    )


def independent(state: tuple[int, ...]) -> bool:
    return all(pair(u, v) not in G_EDGES for u, v in combinations(state, 2))


def direct_state(vertex: int, omitted: int) -> tuple[int, int, int]:
    return tuple(sorted((set(S) - {omitted}) | {vertex}))


def restricted_kernel() -> tuple[set[tuple[int, int, int]], list[int]]:
    forbidden = {
        direct_state(vertex, omitted)
        for vertex, allowed in EXPECTED_LISTS.items()
        for omitted in S
        if omitted not in allowed
    }
    family = {
        state
        for state in combinations(range(ORDER), 3)
        if dominates(state) and state not in forbidden
    }
    rounds: list[int] = []
    while True:
        remove: set[tuple[int, int, int]] = set()
        for state in family:
            for attacked in range(ORDER):
                if attacked in state:
                    continue
                if not any(
                    pair(guard, attacked) in G_EDGES
                    and tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    in family
                    for guard in state
                ):
                    remove.add(state)
                    break
        if not remove:
            return family, rounds
        rounds.append(len(remove))
        family -= remove


def family_hash(family: set[tuple[int, int, int]]) -> str:
    payload = "\n".join(
        ",".join(map(str, state)) for state in sorted(family)
    ).encode("ascii")
    return sha256(payload).hexdigest()


def direct_lists(
    family: set[tuple[int, int, int]],
) -> dict[int, tuple[int, ...]]:
    return {
        vertex: tuple(
            omitted
            for omitted in S
            if direct_state(vertex, omitted) in family
        )
        for vertex in range(3, ORDER)
    }


def chromatic_number_h() -> tuple[int, list[int]]:
    adjacency = [set() for _ in range(ORDER)]
    for u, v in H_EDGES:
        adjacency[u].add(v)
        adjacency[v].add(u)

    def coloring(colors: int) -> list[int] | None:
        assignment = [-1] * ORDER

        def visit() -> bool:
            uncolored = [v for v in range(ORDER) if assignment[v] < 0]
            if not uncolored:
                return True
            vertex = max(
                uncolored,
                key=lambda v: (
                    len(
                        {
                            assignment[w]
                            for w in adjacency[v]
                            if assignment[w] >= 0
                        }
                    ),
                    len(adjacency[v]),
                    -v,
                ),
            )
            blocked = {
                assignment[w]
                for w in adjacency[vertex]
                if assignment[w] >= 0
            }
            for color in range(colors):
                if color in blocked:
                    continue
                assignment[vertex] = color
                if visit():
                    return True
            assignment[vertex] = -1
            return False

        return assignment if visit() else None

    for colors in range(1, ORDER + 1):
        witness = coloring(colors)
        if witness is not None:
            return colors, witness
    raise AssertionError("unreachable")


def response_formula() -> tuple[
    list[tuple[tuple[int, int], tuple[int, int]]],
    list[tuple[int, tuple[int, ...], dict[int, int]]],
]:
    vertex_type = {
        vertex: next(iter(set(S) - set(allowed)))
        for vertex, allowed in EXPECTED_LISTS.items()
    }
    unseen = set(EXPECTED_LISTS)
    components: list[tuple[int, tuple[int, ...], dict[int, int]]] = []
    info: dict[int, tuple[int, int]] = {}
    for omitted in S:
        remaining = {v for v in unseen if vertex_type[v] == omitted}
        while remaining:
            root = min(remaining)
            remaining.remove(root)
            side = {root: 0}
            queue = deque([root])
            while queue:
                current = queue.popleft()
                for neighbor in sorted(tuple(remaining)):
                    if pair(current, neighbor) in H_EDGES:
                        side[neighbor] = 1 - side[current]
                        remaining.remove(neighbor)
                        queue.append(neighbor)
            index = len(components)
            vertices = tuple(sorted(side))
            components.append((omitted, vertices, side))
            for vertex in vertices:
                info[vertex] = (index, side[vertex])
            unseen -= set(vertices)

    clauses: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for u, v in sorted(H_EDGES):
        if u < 3 or v < 3 or vertex_type[u] == vertex_type[v]:
            continue
        common = next(iter(set(EXPECTED_LISTS[u]) & set(EXPECTED_LISTS[v])))
        iu, pu = info[u]
        iv, pv = info[v]
        bu = pu ^ EXPECTED_LISTS[u].index(common)
        bv = pv ^ EXPECTED_LISTS[v].index(common)
        lu = iu + 1 if bu == 0 else -(iu + 1)
        lv = iv + 1 if bv == 0 else -(iv + 1)
        clauses.append(((lu, lv), (u, v)))
    return clauses, components


def satisfies(
    clauses: list[tuple[tuple[int, int], tuple[int, int]]],
    selected: tuple[int, ...],
    assignment: tuple[int, ...],
) -> bool:
    return all(
        any(
            assignment[abs(literal) - 1]
            if literal > 0
            else not assignment[abs(literal) - 1]
            for literal in clauses[index][0]
        )
        for index in selected
    )


def models(
    clauses: list[tuple[tuple[int, int], tuple[int, int]]],
    selected: tuple[int, ...],
    variable_count: int,
) -> list[tuple[int, ...]]:
    return [
        assignment
        for assignment in product((0, 1), repeat=variable_count)
        if satisfies(clauses, selected, assignment)
    ]


def inclusion_minimal_unsat(
    clauses: list[tuple[tuple[int, int], tuple[int, int]]],
    selected: tuple[int, ...],
    variable_count: int,
) -> bool:
    if models(clauses, selected, variable_count):
        return False
    return all(
        models(
            clauses,
            selected[:index] + selected[index + 1 :],
            variable_count,
        )
        for index in range(len(selected))
    )


def shortest_implication_path(
    clauses: list[tuple[tuple[int, int], tuple[int, int]]],
    selected: tuple[int, ...],
    source: int,
    target: int,
    variable_count: int,
) -> list[tuple[int, int, int]] | None:
    adjacency = {
        literal: []
        for variable in range(1, variable_count + 1)
        for literal in (variable, -variable)
    }
    for index in selected:
        left, right = clauses[index][0]
        adjacency[-left].append((right, index))
        adjacency[-right].append((left, index))
    queue = deque([source])
    predecessor: dict[int, int | None] = {source: None}
    via: dict[int, int] = {}
    while queue:
        current = queue.popleft()
        if current == target:
            break
        for neighbor, clause_index in adjacency[current]:
            if neighbor in predecessor:
                continue
            predecessor[neighbor] = current
            via[neighbor] = clause_index
            queue.append(neighbor)
    if target not in predecessor:
        return None
    path: list[tuple[int, int, int]] = []
    current = target
    while predecessor[current] is not None:
        prior = predecessor[current]
        assert prior is not None
        path.append((prior, current, via[current]))
        current = prior
    path.reverse()
    return path


def exact_parameters(
    family: set[tuple[int, int, int]],
) -> tuple[dict[str, int], list[int]]:
    gamma = next(
        size
        for size in range(1, 4)
        if any(dominates(state) for state in combinations(range(ORDER), size))
    )
    independent_dominating_sizes = [
        size
        for size in range(1, 4)
        for state in combinations(range(ORDER), size)
        if independent(state) and dominates(state)
    ]
    if not independent(S):
        raise AssertionError("anchor state is not independent")
    if any(independent(state) for state in combinations(range(ORDER), 4)):
        raise AssertionError("unexpected independent four-set")
    theta, coloring = chromatic_number_h()
    parameters = {
        "gamma": gamma,
        "i": min(independent_dominating_sizes),
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": theta,
    }
    if not family:
        raise AssertionError("empty eternal triple-family")
    return parameters, coloring


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    if graph6() != EXPECTED_GRAPH6:
        raise AssertionError("graph6 mismatch")

    family, rounds = restricted_kernel()
    if len(family) != EXPECTED_FAMILY_SIZE:
        raise AssertionError("restricted-family size mismatch")
    if rounds != EXPECTED_DELETION_ROUNDS:
        raise AssertionError("deletion-round mismatch")
    if family_hash(family) != EXPECTED_FAMILY_SHA256:
        raise AssertionError("restricted-family hash mismatch")
    if direct_lists(family) != EXPECTED_LISTS:
        raise AssertionError("direct response-list mismatch")

    obligations = 0
    for state in family:
        if not dominates(state):
            raise AssertionError("retained state does not dominate")
        for attacked in range(ORDER):
            if attacked in state:
                continue
            obligations += 1
            if not any(
                pair(guard, attacked) in G_EDGES
                and tuple(sorted((set(state) - {guard}) | {attacked}))
                in family
                for guard in state
            ):
                raise AssertionError("failed one-guard obligation")

    parameters, theta_coloring = exact_parameters(family)
    expected_parameters = {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if parameters != expected_parameters:
        raise AssertionError("parameter mismatch")

    clauses, components = response_formula()
    if clauses != EXPECTED_CLAUSES:
        raise AssertionError("response formula mismatch")
    variable_count = len(components)
    full = tuple(range(len(clauses)))
    if models(clauses, full, variable_count):
        raise AssertionError("response formula unexpectedly satisfiable")

    if not inclusion_minimal_unsat(
        clauses, OLD_CORE, variable_count
    ):
        raise AssertionError("old core is not inclusion-minimal UNSAT")
    if not inclusion_minimal_unsat(
        clauses, Q_ARM_CORE, variable_count
    ):
        raise AssertionError("q-arm core is not inclusion-minimal UNSAT")

    minimum_cores: list[tuple[int, ...]] = []
    for size in range(1, len(clauses) + 1):
        for selected in combinations(range(len(clauses)), size):
            if not models(clauses, selected, variable_count):
                minimum_cores.append(selected)
        if minimum_cores:
            break
    if minimum_cores != [OLD_CORE]:
        raise AssertionError("minimum-core classification mismatch")

    minimum_q_arm_cores: list[tuple[int, ...]] = []
    for size in range(1, len(clauses) + 1):
        for selected in combinations(range(len(clauses)), size):
            if not all(index in selected for index in Q_ARM_CLAUSES):
                continue
            if not inclusion_minimal_unsat(
                clauses, selected, variable_count
            ):
                continue
            minimum_q_arm_cores.append(selected)
        if minimum_q_arm_cores:
            break
    if minimum_q_arm_cores != [Q_ARM_CORE]:
        raise AssertionError("q-arm-core classification mismatch")

    left_arm = set(clauses[Q_ARM_CLAUSES[0]][0])
    right_arm = set(clauses[Q_ARM_CLAUSES[1]][0])
    resolvent = tuple(
        sorted(
            (left_arm - {-3}) | (right_arm - {3}),
            key=lambda literal: abs(literal),
        )
    )
    if set(resolvent) != set(clauses[10][0]):
        raise AssertionError("almost-cap resolvent mismatch")

    old_forward = shortest_implication_path(
        clauses, OLD_CORE, 4, -4, variable_count
    )
    old_reverse = shortest_implication_path(
        clauses, OLD_CORE, -4, 4, variable_count
    )
    new_forward = shortest_implication_path(
        clauses, Q_ARM_CORE, 4, -4, variable_count
    )
    new_reverse = shortest_implication_path(
        clauses, Q_ARM_CORE, -4, 4, variable_count
    )
    path_lengths = {
        "old_forward": len(old_forward or ()),
        "old_reverse": len(old_reverse or ()),
        "q_arm_forward": len(new_forward or ()),
        "q_arm_reverse": len(new_reverse or ()),
    }
    if path_lengths != {
        "old_forward": 4,
        "old_reverse": 5,
        "q_arm_forward": 5,
        "q_arm_reverse": 5,
    }:
        raise AssertionError("shortest contradiction-path mismatch")

    common_4_6 = [
        vertex
        for vertex in range(ORDER)
        if vertex not in (4, 6)
        and pair(4, vertex) in H_EDGES
        and pair(6, vertex) in H_EDGES
    ]
    if common_4_6 != [18]:
        raise AssertionError("critical-pair witness mismatch")
    if pair(0, 18) in H_EDGES:
        raise AssertionError("almost-cap is not dynamic at anchor 0")

    dominating_pairs = [
        state
        for state in combinations(range(ORDER), 2)
        if dominates(state)
    ]
    result = {
        "schema": "paired-repair-implication-countercontrol-v1",
        "classification": (
            "exact gamma-two countercontrol; not a gamma-theta "
            "counterexample"
        ),
        "graph6": EXPECTED_GRAPH6,
        "order": ORDER,
        "size": len(G_EDGES),
        "parameters": parameters,
        "theta_coloring_of_H": theta_coloring,
        "restricted_family": {
            "size": len(family),
            "sha256": family_hash(family),
            "deletion_round_sizes": rounds,
            "one_guard_obligations": obligations,
        },
        "response_lists": {
            str(vertex): list(allowed)
            for vertex, allowed in EXPECTED_LISTS.items()
        },
        "response_formula": {
            "variable_count": variable_count,
            "clause_count": len(clauses),
            "minimum_unsat_core": list(OLD_CORE),
            "minimum_unsat_core_size": len(OLD_CORE),
            "minimum_q_arm_core": list(Q_ARM_CORE),
            "minimum_q_arm_core_size": len(Q_ARM_CORE),
            "q_arm_clause_indices": list(Q_ARM_CLAUSES),
            "q_arm_resolvent": list(resolvent),
            "duplicated_original_clause_index": 10,
            "shortest_path_lengths": path_lengths,
        },
        "critical_pair": {
            "vertices": [4, 6],
            "unique_common_H_neighbor": 18,
            "witness_list": list(EXPECTED_LISTS[18]),
            "omitted_anchor": 0,
            "anchor_witness_edge_in_G": True,
        },
        "dominating_pair_count": len(dominating_pairs),
        "one_dominating_pair": list(dominating_pairs[0]),
        "claim_boundary": [
            "gamma is 2, not 3",
            "the selected family is a restricted eternal family, not the greatest triple-family",
            "the control refutes only a descent using the selected critical-pair witness and local closure",
            "it does not refute a proof using the full global no-dominating-pair hypothesis",
        ],
    }

    if args.check is not None:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("frozen result mismatch")

    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS")


if __name__ == "__main__":
    main()
