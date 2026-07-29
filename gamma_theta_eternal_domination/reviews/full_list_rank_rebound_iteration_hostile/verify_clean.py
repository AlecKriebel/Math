#!/usr/bin/env python3
"""Clean-room audit of the full-list rank-rebound iteration.

This file intentionally imports no campaign or candidate Python module.
Graphs are integer neighborhood masks and guard configurations are integer
bitmasks.  Besides replaying the 13-vertex control, it exhausts:

* every graph through order four, every k <= 3, every eternal family, and
  every nonempty ban when checking the tight-shell lemma;
* a deterministic bounded collection of anchored rank-one instances through
  order six; and
* every graph through order six for the static target-fan split and its
  collision-safe reciprocal exchanges.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
CANDIDATE = CAMPAIGN / "math" / "working" / "full_list_rank_rebound_iteration"

PINNED = {
    "NOTE.md": "378633621b759c31d1b747b0f1a7bd657f17d8b60da9b8356488640e8fbb8f19",
    "RESEARCH_LOG.md": "d5dc301d3a086cc3a185fe63ba2075c6eeec912868fe66a876341c2fe3e87f6f",
    "verify_boundary.py": "49b3caa552e4562744fe8592fdaf8b604a9f811b107c645969b6917dc3d9682e",
    "verify_strict.sh": "1c45c5d9ed4bc03b92f87daebd5badeb4a95cb5ca36297990cdd17c58e31ffbc",
    "expected_result.json": "e74547cbbc38651f874f10124a1bb09b95db901a37cf8ff02e057f27b7722650",
}

GRAPH6 = "LEhbtnm~D]xln{"
S = (0, 5, 6)
X = 8
U, V, T = 6, 0, 5
Q, R, W, Y = 2, 10, 3, 1
D, E = 11, 12


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def bits(mask: int):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def masks_of_size(n: int, k: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << vertex for vertex in chosen)
        for chosen in itertools.combinations(range(n), k)
    )


def graph_from_edge_code(n: int, code: int) -> tuple[int, ...]:
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if (code >> cursor) & 1:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def decode_graph6(record: str) -> tuple[int, ...]:
    require(record and 0 <= ord(record[0]) - 63 <= 62, "short graph6")
    n = ord(record[0]) - 63
    payload = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "graph6 character")
        for shift in range(5, -1, -1):
            payload.append((value >> shift) & 1)
    needed = n * (n - 1) // 2
    require(len(payload) == ((needed + 5) // 6) * 6, "graph6 length")
    require(not any(payload[needed:]), "graph6 padding")
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if payload[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def edge_list(graph: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (low, high)
        for high in range(1, len(graph))
        for low in range(high)
        if graph[high] & (1 << low)
    )


def dominates(graph: tuple[int, ...], guards: int) -> bool:
    covered = guards
    for guard in bits(guards):
        covered |= graph[guard]
    return covered == (1 << len(graph)) - 1


def independent(graph: tuple[int, ...], chosen: int) -> bool:
    return all(not (graph[vertex] & chosen) for vertex in bits(chosen))


def physical_successors(
    graph: tuple[int, ...], guards: int, attacked: int
) -> tuple[int, ...]:
    require(not (guards & (1 << attacked)), ("occupied attack", guards, attacked))
    return tuple(
        (guards ^ (1 << guard)) | (1 << attacked)
        for guard in bits(guards)
        if graph[guard] & (1 << attacked)
    )


def greatest_kernel(
    graph: tuple[int, ...], k: int, banned: frozenset[int] = frozenset()
) -> tuple[frozenset[int], dict[int, int], tuple[int, ...]]:
    active = {
        guards
        for guards in masks_of_size(len(graph), k)
        if guards not in banned and dominates(graph, guards)
    }
    ranks: dict[int, int] = {}
    rounds: list[int] = []
    rank = 0
    while True:
        deleted = set()
        for guards in active:
            for attacked in range(len(graph)):
                if guards & (1 << attacked):
                    continue
                if not any(
                    endpoint in active
                    for endpoint in physical_successors(graph, guards, attacked)
                ):
                    deleted.add(guards)
                    break
        if not deleted:
            return frozenset(active), ranks, tuple(rounds)
        for guards in deleted:
            ranks[guards] = rank
        rounds.append(len(deleted))
        active.difference_update(deleted)
        rank += 1


def is_eternal_family(
    graph: tuple[int, ...], family: frozenset[int]
) -> bool:
    if not family or any(not dominates(graph, state) for state in family):
        return False
    for state in family:
        for attacked in range(len(graph)):
            if state & (1 << attacked):
                continue
            if not any(
                endpoint in family
                for endpoint in physical_successors(graph, state, attacked)
            ):
                return False
    return True


def deletion_witnesses(
    graph: tuple[int, ...],
    state: int,
    banned: frozenset[int],
    kernel: frozenset[int],
    ranks: dict[int, int],
) -> tuple[int, ...]:
    rank = ranks[state]
    result = []
    for attacked in range(len(graph)):
        if state & (1 << attacked):
            continue
        endpoints = [
            endpoint
            for endpoint in physical_successors(graph, state, attacked)
            if endpoint not in banned and dominates(graph, endpoint)
        ]
        if all(
            endpoint not in kernel
            and endpoint in ranks
            and ranks[endpoint] < rank
            for endpoint in endpoints
        ):
            result.append(attacked)
    return tuple(result)


def johnson_distance(state: int, banned: frozenset[int], k: int) -> int:
    return min(k - (state & target).bit_count() for target in banned)


def exact_gamma(graph: tuple[int, ...]) -> int:
    for k in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in masks_of_size(len(graph), k)):
            return k
    raise AssertionError("gamma")


def exact_i(graph: tuple[int, ...]) -> int:
    for k in range(1, len(graph) + 1):
        if any(
            dominates(graph, state) and independent(graph, state)
            for state in masks_of_size(len(graph), k)
        ):
            return k
    raise AssertionError("i")


def exact_alpha(graph: tuple[int, ...]) -> int:
    for k in range(len(graph), 0, -1):
        if any(independent(graph, state) for state in masks_of_size(len(graph), k)):
            return k
    return 0


def exact_eternal(graph: tuple[int, ...]) -> int:
    for k in range(1, len(graph) + 1):
        kernel, _, _ = greatest_kernel(graph, k)
        if kernel:
            return k
    raise AssertionError("eternal")


def colorable_complement(graph: tuple[int, ...], color_count: int) -> bool:
    n = len(graph)
    universe = (1 << n) - 1
    opposite = tuple(universe ^ (1 << vertex) ^ graph[vertex] for vertex in range(n))
    colors = [-1] * n

    def visit(colored: int) -> bool:
        if colored == n:
            return True
        uncolored = [vertex for vertex in range(n) if colors[vertex] < 0]
        vertex = max(
            uncolored,
            key=lambda item: (
                len(
                    {
                        colors[neighbor]
                        for neighbor in bits(opposite[item])
                        if colors[neighbor] >= 0
                    }
                ),
                opposite[item].bit_count(),
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in bits(opposite[vertex])
            if colors[neighbor] >= 0
        }
        for color in range(color_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            if visit(colored + 1):
                return True
            colors[vertex] = -1
        return False

    return visit(0)


def exact_theta(graph: tuple[int, ...]) -> int:
    for count in range(1, len(graph) + 1):
        if colorable_complement(graph, count):
            return count
    raise AssertionError("theta")


def complement_neighbors(graph: tuple[int, ...], vertex: int) -> int:
    return ((1 << len(graph)) - 1) ^ (1 << vertex) ^ graph[vertex]


def color_ban(
    graph: tuple[int, ...], root: tuple[int, int, int], target: int, color: int
) -> frozenset[int]:
    fixed = sum(1 << vertex for vertex in root if vertex != color)
    return frozenset(
        fixed | (1 << terminal)
        for terminal in bits(complement_neighbors(graph, target))
    )


def common_missed(graph: tuple[int, ...], first: int, second: int) -> int:
    covered = (
        (1 << first)
        | (1 << second)
        | graph[first]
        | graph[second]
    )
    return ((1 << len(graph)) - 1) ^ covered


def state(*vertices: int) -> int:
    return sum(1 << vertex for vertex in vertices)


def state_list(mask: int) -> list[int]:
    return list(bits(mask))


def audit_tight_shell() -> dict[str, int]:
    graphs = 0
    eternal_families = 0
    ban_instances = 0
    tight_states = 0
    witness_attacks = 0
    retained_responses = 0
    for n in range(1, 5):
        for edge_code in range(1 << (n * (n - 1) // 2)):
            graph = graph_from_edge_code(n, edge_code)
            graphs += 1
            for k in range(1, min(3, n) + 1):
                all_states = masks_of_size(n, k)
                dominating = tuple(s for s in all_states if dominates(graph, s))
                for family_code in range(1, 1 << len(dominating)):
                    family = frozenset(
                        dominating[index]
                        for index in range(len(dominating))
                        if family_code & (1 << index)
                    )
                    if not is_eternal_family(graph, family):
                        continue
                    eternal_families += 1
                    for ban_code in range(1, 1 << len(all_states)):
                        banned = frozenset(
                            all_states[index]
                            for index in range(len(all_states))
                            if ban_code & (1 << index)
                        )
                        ban_instances += 1
                        kernel, ranks, _ = greatest_kernel(graph, k, banned)
                        for retained in family:
                            if retained not in ranks:
                                continue
                            distance = johnson_distance(retained, banned, k)
                            rank = ranks[retained]
                            require(
                                rank >= distance - 1,
                                ("rank floor", n, edge_code, k, retained, banned),
                            )
                            if distance < 2 or rank != distance - 1:
                                continue
                            tight_states += 1
                            for attacked in deletion_witnesses(
                                graph, retained, banned, kernel, ranks
                            ):
                                witness_attacks += 1
                                responses = [
                                    endpoint
                                    for endpoint in physical_successors(
                                        graph, retained, attacked
                                    )
                                    if endpoint in family
                                ]
                                require(responses, "eternal response missing")
                                for endpoint in responses:
                                    retained_responses += 1
                                    require(
                                        endpoint in ranks
                                        and ranks[endpoint] == distance - 2,
                                        (
                                            "tight rank",
                                            n,
                                            edge_code,
                                            k,
                                            retained,
                                            attacked,
                                            endpoint,
                                        ),
                                    )
                                    require(
                                        johnson_distance(endpoint, banned, k)
                                        == distance - 1,
                                        (
                                            "tight distance",
                                            n,
                                            edge_code,
                                            k,
                                            retained,
                                            attacked,
                                            endpoint,
                                        ),
                                    )
    return {
        "graphs": graphs,
        "eternal_families": eternal_families,
        "ban_instances": ban_instances,
        "tight_states": tight_states,
        "deletion_witness_attacks": witness_attacks,
        "retained_responses": retained_responses,
    }


def audit_anchor_exit() -> dict[str, int]:
    graphs = 0
    anchored_bans = 0
    rank_one_states = 0
    witness_attacks = 0
    retained_responses = 0
    for n in range(3, 7):
        edge_count = n * (n - 1) // 2
        codes = range(1 << edge_count)
        if n == 6:
            # A deterministic 1/16 slice of the labeled graph universe.
            codes = range(7, 1 << edge_count, 16)
        for edge_code in codes:
            graph = graph_from_edge_code(n, edge_code)
            greatest, _, _ = greatest_kernel(graph, 3)
            if not greatest:
                continue
            graphs += 1
            for target in range(n):
                neighbors = list(bits(graph[target]))
                for first_index in range(len(neighbors)):
                    for second_index in range(first_index + 1, len(neighbors)):
                        first = neighbors[first_index]
                        second = neighbors[second_index]
                        region = complement_neighbors(graph, target)
                        if not region:
                            continue
                        anchor_mask = (1 << first) | (1 << second)
                        banned = frozenset(
                            anchor_mask | (1 << b) for b in bits(region)
                        )
                        anchored_bans += 1
                        kernel, ranks, _ = greatest_kernel(graph, 3, banned)
                        for retained in greatest:
                            if retained & anchor_mask or ranks.get(retained) != 1:
                                continue
                            if johnson_distance(retained, banned, 3) != 2:
                                continue
                            rank_one_states += 1
                            for attacked in deletion_witnesses(
                                graph, retained, banned, kernel, ranks
                            ):
                                witness_attacks += 1
                                require(
                                    anchor_mask & (1 << attacked),
                                    (
                                        "nonanchor rank-one witness",
                                        n,
                                        edge_code,
                                        target,
                                        first,
                                        second,
                                        retained,
                                        attacked,
                                    ),
                                )
                                for endpoint in physical_successors(
                                    graph, retained, attacked
                                ):
                                    if endpoint not in greatest:
                                        continue
                                    retained_responses += 1
                                    require(
                                        ranks.get(endpoint) == 0
                                        and johnson_distance(endpoint, banned, 3) == 1,
                                        (
                                            "anchor endpoint",
                                            n,
                                            edge_code,
                                            retained,
                                            attacked,
                                            endpoint,
                                        ),
                                    )
    return {
        "graphs_with_eternal_triples": graphs,
        "anchored_bans": anchored_bans,
        "rank_one_states": rank_one_states,
        "deletion_witness_attacks": witness_attacks,
        "retained_responses": retained_responses,
        "order6_graph_code_slice": "code == 7 (mod 16)",
    }


def audit_target_fans() -> dict[str, int]:
    graphs = 0
    ordered_pair_targets = 0
    trapped_fan_cases = 0
    alpha_at_most_three_cases = 0
    reciprocal_exchange_pairs = 0
    collision_d_equals_auxiliary = 0
    for n in range(1, 7):
        for edge_code in range(1 << (n * (n - 1) // 2)):
            graph = graph_from_edge_code(n, edge_code)
            graphs += 1
            alpha_at_most_three = not any(
                independent(graph, chosen) for chosen in masks_of_size(n, 4)
            ) if n >= 4 else True
            for target in range(n):
                ban_region = complement_neighbors(graph, target)
                for first in range(n):
                    if first == target or not (graph[target] & (1 << first)):
                        continue
                    for second in range(n):
                        if second in (target, first):
                            continue
                        if graph[first] & (1 << second):
                            continue
                        if graph[target] & (1 << second):
                            continue
                        ordered_pair_targets += 1
                        fan = common_missed(graph, first, second)
                        triple = state(target, first, second)
                        require(
                            (
                                dominates(graph, triple)
                                == (not bool(fan & ban_region))
                            ),
                            (
                                "fan dominance",
                                n,
                                edge_code,
                                target,
                                first,
                                second,
                            ),
                        )
                        trapped = fan & ban_region
                        if not trapped:
                            continue
                        trapped_fan_cases += 1
                        if not alpha_at_most_three:
                            continue
                        alpha_at_most_three_cases += 1
                        fan_vertices = list(bits(fan))
                        require(
                            all(
                                graph[left] & (1 << right)
                                for left_index, left in enumerate(fan_vertices)
                                for right in fan_vertices[left_index + 1 :]
                            ),
                            ("fan not clique", n, edge_code, first, second),
                        )
                        for completion in bits(trapped):
                            left_state = state(first, second, completion)
                            right_state = state(target, second, completion)
                            require(
                                independent(graph, left_state)
                                and independent(graph, right_state),
                                ("hinge independence", n, edge_code),
                            )
                            require(
                                physical_successors(graph, left_state, target)
                                == (right_state,),
                                (
                                    "forward hinge",
                                    n,
                                    edge_code,
                                    target,
                                    first,
                                    second,
                                    completion,
                                ),
                            )
                            require(
                                physical_successors(graph, right_state, first)
                                == (left_state,),
                                (
                                    "reverse hinge",
                                    n,
                                    edge_code,
                                    target,
                                    first,
                                    second,
                                    completion,
                                ),
                            )
                            reciprocal_exchange_pairs += 1
                            if completion == second:
                                collision_d_equals_auxiliary += 1
    return {
        "graphs": graphs,
        "ordered_pair_targets": ordered_pair_targets,
        "trapped_fan_cases": trapped_fan_cases,
        "alpha_at_most_three_cases": alpha_at_most_three_cases,
        "reciprocal_exchange_pairs": reciprocal_exchange_pairs,
        "collision_d_equals_auxiliary": collision_d_equals_auxiliary,
    }


def audit_control() -> dict[str, object]:
    graph = decode_graph6(GRAPH6)
    n = len(graph)
    greatest, _, unrestricted_rounds = greatest_kernel(graph, 3)
    root = state(*S)
    require(independent(graph, root) and root in greatest, "root")
    require(all(graph[color] & (1 << X) for color in S), "target edges")
    require(
        all(
            state(*(set(S) - {color}), X) in greatest
            for color in S
        ),
        "target not full",
    )

    source = state(V, T, Q)
    escape = state(V, T, Y)
    first_completion = state(Q, W, D)
    second_completion = state(R, Y, E)
    first_cross = state(X, Q, W)
    second_cross = state(X, R, Y)
    second_source = state(V, R, Y)

    first_fan = common_missed(graph, Q, W)
    second_fan = common_missed(graph, R, Y)
    require(first_fan == 1 << D, ("first fan", first_fan))
    require(second_fan == 1 << E, ("second fan", second_fan))
    require(graph[T] & (1 << D), "first fan support")
    require(graph[V] & (1 << E), "second fan support")
    require(
        physical_successors(graph, state(W, T, Q), D)
        == (first_completion,),
        "first exchange",
    )
    require(
        physical_successors(graph, second_source, E)
        == (second_completion,),
        "second exchange",
    )

    restricted = {}
    all_source_data = {
        0: (0, (27, 49, 74, 46), 1, 2, 3, 2),
        5: (0, (20, 30, 53, 74, 20), 3, 2, 3, 4),
        6: (0, (20, 53, 90, 34), 0, 0, 2, 2),
    }
    source_ban = frozenset()
    source_ranks: dict[int, int] = {}
    source_kernel = frozenset()
    for color in S:
        banned = color_ban(graph, S, X, color)
        kernel, ranks, rounds = greatest_kernel(graph, 3, banned)
        actual = (
            len(kernel),
            rounds,
            ranks.get(source),
            ranks.get(escape),
            ranks.get(first_completion),
            ranks.get(second_completion),
        )
        require(actual == all_source_data[color], ("restricted", color, actual))
        restricted[str(color)] = {
            "kernel_size": len(kernel),
            "round_sizes": list(rounds),
            "source_rank": ranks.get(source),
            "escape_rank": ranks.get(escape),
            "first_completion_rank": ranks.get(first_completion),
            "second_completion_rank": ranks.get(second_completion),
        }
        if color == U:
            source_ban, source_kernel, source_ranks = banned, kernel, ranks

    require(dominates(graph, first_cross) and first_cross in greatest, "first cross")
    require(dominates(graph, second_cross) and second_cross in greatest, "second cross")
    require(source_ranks[first_cross] == 3, "first cross rank")
    require(source_ranks[second_cross] == 2, "second cross rank")

    witnesses = deletion_witnesses(
        graph, second_completion, source_ban, source_kernel, source_ranks
    )
    require(witnesses == (V, W, T), ("second witnesses", witnesses))
    responses = tuple(
        endpoint
        for endpoint in physical_successors(graph, second_completion, W)
        if endpoint in greatest
    )
    require(
        set(responses) == {state(W, R, E), state(Y, W, R)},
        ("nonanchor responses", responses),
    )
    require(all(source_ranks[endpoint] == 1 for endpoint in responses), "rank one")

    edges = edge_list(graph)
    serialized_edges = "".join(f"{a}-{b}\n" for a, b in edges).encode("ascii")
    parameters = {
        "gamma": exact_gamma(graph),
        "i": exact_i(graph),
        "alpha": exact_alpha(graph),
        "gamma_infinity": exact_eternal(graph),
        "theta": exact_theta(graph),
    }
    require(
        parameters
        == {
            "gamma": 2,
            "i": 2,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 4,
        },
        parameters,
    )
    return {
        "graph6": GRAPH6,
        "graph6_sha256": hashlib.sha256(GRAPH6.encode("ascii")).hexdigest(),
        "edge_list_sha256": hashlib.sha256(serialized_edges).hexdigest(),
        "order": n,
        "size": len(edges),
        "parameters": parameters,
        "greatest_family_size": len(greatest),
        "unrestricted_round_sizes": list(unrestricted_rounds),
        "restricted": restricted,
        "completion_fans": {
            "first": state_list(first_fan),
            "second": state_list(second_fan),
        },
        "crosses": {
            "first": {
                "state": state_list(first_cross),
                "rank": source_ranks[first_cross],
            },
            "second": {
                "state": state_list(second_cross),
                "rank": source_ranks[second_cross],
            },
        },
        "second_completion": {
            "state": state_list(second_completion),
            "rank": source_ranks[second_completion],
            "deletion_witnesses": list(witnesses),
            "nonanchor_witness": W,
            "nonanchor_responses": [
                {
                    "state": state_list(endpoint),
                    "rank": source_ranks[endpoint],
                }
                for endpoint in sorted(responses)
            ],
        },
        "scope": "gamma-two sharpness control only",
    }


def main() -> None:
    for relative, expected in PINNED.items():
        actual = hashlib.sha256((CANDIDATE / relative).read_bytes()).hexdigest()
        require(actual == expected, ("candidate hash", relative, actual))

    result = {
        "schema": "full-list-rank-rebound-hostile-clean-v1",
        "candidate_commit": "42629d71",
        "candidate_hashes": PINNED,
        "tight_shell_audit": audit_tight_shell(),
        "anchor_exit_audit": audit_anchor_exit(),
        "target_fan_audit": audit_target_fans(),
        "exact_control": audit_control(),
        "verdict": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
