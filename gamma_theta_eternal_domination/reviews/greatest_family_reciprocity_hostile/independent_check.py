#!/usr/bin/env python3
"""Independent hostile checker for the greatest-family reciprocity checkpoint.

This checker imports no campaign evaluator, candidate verifier, search module,
NetworkX, or SAT package.  The graph-specific game kernel is reconstructed by
dependency-queue elimination rather than the candidate's synchronous deletion
loop.  A second compact implementation independently replays the explicitly
delimited 17-bit two-vertex extension census.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
CANDIDATE = CAMPAIGN / "math" / "working" / "greatest_family_reciprocity"
GRAPH6 = "GEjbug"
EXPECTED_EDGES = {
    (0, 3),
    (0, 4),
    (0, 5),
    (0, 7),
    (1, 3),
    (1, 5),
    (1, 6),
    (1, 7),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 6),
    (3, 7),
    (4, 6),
    (5, 7),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_small_graph6(record: str) -> tuple[frozenset[int], ...]:
    """Decode the n<=62 graph6 form from its bitstream."""
    require(bool(record), "empty graph6 record")
    n = ord(record[0]) - 63
    require(0 <= n <= 62, "not a small graph6 record")
    stream: list[int] = []
    for char in record[1:]:
        value = ord(char) - 63
        require(0 <= value < 64, "invalid graph6 character")
        stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    require(len(stream) >= n * (n - 1) // 2, "short graph6 bitstream")
    adjacency = [set() for _ in range(n)]
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if stream[cursor]:
                adjacency[low].add(high)
                adjacency[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in adjacency)


def encode_small_graph6(graph: tuple[frozenset[int], ...]) -> str:
    n = len(graph)
    bits = [
        int(high in graph[low])
        for high in range(1, n)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    chars = [chr(n + 63)]
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def graph_edges(
    graph: tuple[frozenset[int], ...],
) -> set[tuple[int, int]]:
    return {
        (u, v)
        for u in range(len(graph))
        for v in range(u + 1, len(graph))
        if v in graph[u]
    }


def connected(graph: tuple[frozenset[int], ...]) -> bool:
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in graph[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                frontier.append(neighbor)
    return len(reached) == len(graph)


def dominates(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(
        vertex in state or not graph[vertex].isdisjoint(state)
        for vertex in range(len(graph))
    )


def independent(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(v not in graph[u] for u, v in itertools.combinations(state, 2))


def all_subsets(n: int, size: int) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(vertices)
        for vertices in itertools.combinations(range(n), size)
    )


def minimum_cardinality(n: int, predicate) -> int:
    for size in range(n + 1):
        if any(predicate(state) for state in all_subsets(n, size)):
            return size
    raise AssertionError("predicate has no witness")


def clique_partition(
    graph: tuple[frozenset[int], ...], block_limit: int
) -> tuple[tuple[int, ...], ...] | None:
    """Canonical set-partition search, directly in G rather than coloring co-G."""
    blocks: list[list[int]] = []
    n = len(graph)

    def visit(vertex: int) -> bool:
        if vertex == n:
            return True
        for block in blocks:
            if all(member in graph[vertex] for member in block):
                block.append(vertex)
                if visit(vertex + 1):
                    return True
                block.pop()
        if len(blocks) < block_limit:
            blocks.append([vertex])
            if visit(vertex + 1):
                return True
            blocks.pop()
        return False

    if not visit(0):
        return None
    return tuple(tuple(block) for block in blocks)


def greatest_kernel_queue(
    graph: tuple[frozenset[int], ...], size: int
) -> frozenset[frozenset[int]]:
    """Compute the safety kernel by reverse dependency elimination."""
    states = tuple(
        state
        for state in all_subsets(len(graph), size)
        if dominates(graph, state)
    )
    position = {state: index for index, state in enumerate(states)}
    obligations: list[tuple[int, int, tuple[int, ...]]] = []
    reverse_dependencies: list[list[int]] = [[] for _ in states]
    state_obligations: list[list[int]] = [[] for _ in states]

    for state_index, state in enumerate(states):
        for target in range(len(graph)):
            if target in state:
                continue
            successors: list[int] = []
            for guard in state:
                if target not in graph[guard]:
                    continue
                successor = frozenset((state - {guard}) | {target})
                found = position.get(successor)
                if found is not None:
                    successors.append(found)
            obligation_index = len(obligations)
            obligations.append((state_index, target, tuple(successors)))
            state_obligations[state_index].append(obligation_index)
            for successor_index in successors:
                reverse_dependencies[successor_index].append(obligation_index)

    active = [True] * len(states)
    response_counts = [len(record[2]) for record in obligations]
    doomed: list[int] = []
    queued = [False] * len(states)
    for state_index, obligation_indices in enumerate(state_obligations):
        if any(response_counts[item] == 0 for item in obligation_indices):
            doomed.append(state_index)
            queued[state_index] = True

    cursor = 0
    while cursor < len(doomed):
        removed = doomed[cursor]
        cursor += 1
        if not active[removed]:
            continue
        active[removed] = False
        for obligation_index in reverse_dependencies[removed]:
            source = obligations[obligation_index][0]
            response_counts[obligation_index] -= 1
            require(response_counts[obligation_index] >= 0, "negative response count")
            if (
                response_counts[obligation_index] == 0
                and active[source]
                and not queued[source]
            ):
                queued[source] = True
                doomed.append(source)

    return frozenset(
        state for index, state in enumerate(states) if active[index]
    )


def synchronous_waves(
    graph: tuple[frozenset[int], ...], size: int
) -> tuple[int, ...]:
    family = {
        state
        for state in all_subsets(len(graph), size)
        if dominates(graph, state)
    }
    waves: list[int] = []
    while True:
        removed = {
            state
            for state in family
            if any(
                not any(
                    target in graph[guard]
                    and frozenset((state - {guard}) | {target}) in family
                    for guard in state
                )
                for target in range(len(graph))
                if target not in state
            )
        }
        if not removed:
            return tuple(waves)
        family -= removed
        waves.append(len(removed))


def family_digest(family: frozenset[frozenset[int]]) -> str:
    payload = "\n".join(
        ",".join(str(vertex) for vertex in sorted(state))
        for state in sorted(family, key=lambda item: tuple(sorted(item)))
    ) + "\n"
    return sha256_bytes(payload.encode("ascii"))


def response_relations(
    family: frozenset[frozenset[int]],
    first: frozenset[int],
    second: frozenset[int],
) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    left = first - second
    right = second - first
    forward = {
        (u, x)
        for u in left
        for x in right
        if frozenset((first - {u}) | {x}) in family
    }
    reverse = {
        (u, x)
        for u in left
        for x in right
        if frozenset((second - {x}) | {u}) in family
    }
    return forward, reverse


def matching_and_cube_counts(
    family: frozenset[frozenset[int]],
    first: frozenset[int],
    second: frozenset[int],
) -> tuple[int, int]:
    source = tuple(sorted(first - second))
    target = tuple(sorted(second - first))
    mutual_count = 0
    cube_count = 0
    for permutation in itertools.permutations(target):
        mapping = dict(zip(source, permutation))
        mutual = all(
            frozenset((first - {u}) | {mapping[u]}) in family
            and frozenset((second - {mapping[u]}) | {u}) in family
            for u in source
        )
        if mutual:
            mutual_count += 1
        cube = True
        for count in range(len(source) + 1):
            for chosen in itertools.combinations(source, count):
                chosen_set = set(chosen)
                state = frozenset(
                    (first - chosen_set)
                    | {mapping[vertex] for vertex in chosen_set}
                )
                if state not in family:
                    cube = False
        if cube:
            cube_count += 1
    return mutual_count, cube_count


def canonical_hash_without_field(payload: dict[str, object], field: str) -> str:
    reduced = dict(payload)
    reduced.pop(field)
    encoded = json.dumps(
        reduced, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


# Compact, separately coded replay for the delimited extension observation.
TRIPLES10 = tuple(
    sum(1 << vertex for vertex in triple)
    for triple in itertools.combinations(range(10), 3)
)
QUADS10 = tuple(
    sum(1 << vertex for vertex in quad)
    for quad in itertools.combinations(range(10), 4)
)
PAIRS10 = tuple(itertools.combinations(range(10), 2))
ALL10 = (1 << 10) - 1


def bit_independent(adjacency: tuple[int, ...], state: int) -> bool:
    remaining = state
    while remaining:
        vertex_bit = remaining & -remaining
        remaining -= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        if adjacency[vertex] & remaining:
            return False
    return True


def bit_dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    remaining = state
    while remaining:
        vertex_bit = remaining & -remaining
        remaining -= vertex_bit
        covered |= adjacency[vertex_bit.bit_length() - 1]
    return covered == ALL10


def bit_kernel_three(adjacency: tuple[int, ...]) -> frozenset[int]:
    alive = {
        state for state in TRIPLES10 if bit_dominates(adjacency, state)
    }
    while True:
        bad: set[int] = set()
        for state in alive:
            targets = ALL10 & ~state
            while targets:
                target_bit = targets & -targets
                targets -= target_bit
                target = target_bit.bit_length() - 1
                possible = state & adjacency[target]
                answered = False
                while possible:
                    guard_bit = possible & -possible
                    possible -= guard_bit
                    if ((state - guard_bit) | target_bit) in alive:
                        answered = True
                        break
                if not answered:
                    bad.add(state)
                    break
        if not bad:
            return frozenset(alive)
        alive -= bad


def bit_reciprocity_violation(
    adjacency: tuple[int, ...], family: frozenset[int]
) -> bool:
    bases = [
        state for state in family if bit_independent(adjacency, state)
    ]
    for index, first in enumerate(bases):
        for second in bases[index + 1 :]:
            sources = first & ~second
            targets = second & ~first
            scan_source = sources
            while scan_source:
                source_bit = scan_source & -scan_source
                scan_source -= source_bit
                scan_target = targets
                while scan_target:
                    target_bit = scan_target & -scan_target
                    scan_target -= target_bit
                    forward = ((first - source_bit) | target_bit) in family
                    reverse = ((second - target_bit) | source_bit) in family
                    if forward != reverse:
                        return True
    return False


def extension_adjacency(mask: int) -> tuple[int, ...]:
    adjacency = [0] * 10
    for u, v in EXPECTED_EDGES:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    for old in range(8):
        if mask & (1 << old):
            adjacency[8] |= 1 << old
            adjacency[old] |= 1 << 8
        if mask & (1 << (8 + old)):
            adjacency[9] |= 1 << old
            adjacency[old] |= 1 << 9
    if mask & (1 << 16):
        adjacency[8] |= 1 << 9
        adjacency[9] |= 1 << 8
    return tuple(adjacency)


def replay_extension_census() -> dict[str, int]:
    totals = {
        "extension_masks": 0,
        "alpha_equals_three": 0,
        "gamma_equals_three": 0,
        "eternal_equality": 0,
        "independent_state_pairs": 0,
        "reciprocity_violations": 0,
    }
    for mask in range(1 << 17):
        totals["extension_masks"] += 1
        adjacency = extension_adjacency(mask)
        if any(bit_independent(adjacency, quad) for quad in QUADS10):
            continue
        totals["alpha_equals_three"] += 1
        closed = tuple(
            adjacency[vertex] | (1 << vertex) for vertex in range(10)
        )
        if any(
            (closed[u] | closed[v]) == ALL10 for u, v in PAIRS10
        ):
            continue
        totals["gamma_equals_three"] += 1
        family = bit_kernel_three(adjacency)
        if not family:
            continue
        totals["eternal_equality"] += 1
        bases = [
            state for state in family if bit_independent(adjacency, state)
        ]
        totals["independent_state_pairs"] += len(bases) * (len(bases) - 1) // 2
        if bit_reciprocity_violation(adjacency, family):
            totals["reciprocity_violations"] += 1
    return totals


def audit() -> dict[str, object]:
    graph = decode_small_graph6(GRAPH6)
    require(encode_small_graph6(graph) == GRAPH6, "graph6 round-trip failed")
    require(graph_edges(graph) == EXPECTED_EDGES, "edge-list mismatch")
    require(connected(graph), "countermodel graph is unexpectedly disconnected")
    n = len(graph)

    gamma = minimum_cardinality(n, lambda state: dominates(graph, state))
    independent_domination = minimum_cardinality(
        n,
        lambda state: independent(graph, state) and dominates(graph, state),
    )
    alpha = max(
        size
        for size in range(n + 1)
        if any(independent(graph, state) for state in all_subsets(n, size))
    )
    clique_witnesses: dict[int, tuple[tuple[int, ...], ...] | None] = {
        count: clique_partition(graph, count) for count in range(1, n + 1)
    }
    theta = min(count for count, witness in clique_witnesses.items() if witness)

    kernels = {
        size: greatest_kernel_queue(graph, size)
        for size in range(1, n + 1)
    }
    gamma_infinity = min(size for size, family in kernels.items() if family)
    family = kernels[3]
    require(synchronous_waves(graph, 1) == (), "wrong one-kernel waves")
    require(synchronous_waves(graph, 2) == (7,), "wrong two-kernel waves")

    obligations = 0
    retained_moves = 0
    for state in family:
        require(dominates(graph, state), "kernel contains nondominating state")
        for target in range(n):
            if target in state:
                continue
            obligations += 1
            replies = [
                guard
                for guard in state
                if target in graph[guard]
                and frozenset((state - {guard}) | {target}) in family
            ]
            require(bool(replies), "kernel has unanswered attack")
            retained_moves += len(replies)

    candidate_result = json.loads(
        (CANDIDATE / "countermodel_result.json").read_text(encoding="utf-8")
    )
    literal_family = {
        frozenset(state)
        for state in candidate_result["greatest_three_family"]["states"]
    }
    require(literal_family == set(family), "literal 41-state family mismatch")
    require(
        (CANDIDATE / "countermodel_result.json").read_bytes()
        == (CANDIDATE / "verify_countermodel.log").read_bytes(),
        "candidate result and replay log differ",
    )

    parameters = {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
        "theta": theta,
    }
    require(
        parameters
        == {"gamma": 2, "i": 2, "alpha": 3, "gamma_infinity": 3, "theta": 3},
        f"parameter mismatch: {parameters}",
    )
    require(candidate_result["parameters"] == parameters, "result parameter mismatch")
    require(len(family) == 41, "wrong greatest triple-kernel size")
    require(obligations == 205, "wrong attack-obligation count")
    require(retained_moves == 296, "wrong retained-move count")
    require(
        family_digest(family)
        == "59b74f7c52c11f9672407c5c05d6ab9a0131904787742e3715c68e1b39c9eace",
        "wrong family digest",
    )

    first = frozenset({0, 1, 2})
    second = frozenset({3, 4, 5})
    source = 0
    target = 4
    require(independent(graph, first), "S is not independent")
    require(independent(graph, second), "T is not independent")
    require(target in graph[source], "selected exchange is not an edge")
    forward_state = frozenset((first - {source}) | {target})
    reverse_state = frozenset((second - {target}) | {source})
    require(forward_state in family, "forward state is absent")
    require(reverse_state not in family, "reverse state is present")
    require(dominates(graph, reverse_state), "reverse state is not dominating")

    failed_attack = 7
    failures: dict[int, tuple[tuple[int, ...], tuple[int, ...]]] = {}
    for guard in sorted(reverse_state):
        if failed_attack not in graph[guard]:
            continue
        successor = frozenset((reverse_state - {guard}) | {failed_attack})
        missed = tuple(
            vertex
            for vertex in range(n)
            if vertex not in successor and graph[vertex].isdisjoint(successor)
        )
        require(bool(missed), "reverse attack unexpectedly has a dominating reply")
        failures[guard] = (tuple(sorted(successor)), missed)
    require(
        failures
        == {
            0: ((3, 5, 7), (4,)),
            3: ((0, 5, 7), (6,)),
            5: ((0, 3, 7), (2,)),
        },
        f"wrong failed-attack table: {failures}",
    )

    forward_relation, reverse_relation = response_relations(
        family, first, second
    )
    require(
        (source, target) in forward_relation
        and (source, target) not in reverse_relation,
        "selected relation asymmetry missing",
    )
    mutual_matchings, family_cubes = matching_and_cube_counts(
        family, first, second
    )
    require(mutual_matchings > 0, "boundary accidentally refutes mutual matching")
    require(family_cubes > 0, "boundary accidentally refutes rank-three base ordering")

    independent_triples = [
        state for state in all_subsets(n, 3) if independent(graph, state)
    ]
    require(
        all(state in family for state in independent_triples),
        "a maximum independent state is absent from the kernel",
    )
    asymmetric_quadruples = 0
    tested_quadruples = 0
    for first_index, left_state in enumerate(independent_triples):
        for right_state in independent_triples[first_index + 1 :]:
            relation, reverse = response_relations(
                family, left_state, right_state
            )
            tested_quadruples += len(left_state - right_state) * len(
                right_state - left_state
            )
            asymmetric_quadruples += len(relation ^ reverse)
    require(asymmetric_quadruples > 0, "no global PR violation found")

    manifest = json.loads((CANDIDATE / "MANIFEST.json").read_text())
    checked_hashes: dict[str, str] = {}
    for record in manifest["files"]:
        data = (CANDIDATE / record["path"]).read_bytes()
        digest = sha256_bytes(data)
        require(digest == record["sha256"], f"manifest hash mismatch: {record['path']}")
        require(len(data) == record["bytes"], f"manifest byte mismatch: {record['path']}")
        checked_hashes[record["path"]] = digest

    for name in (
        "extension_result.json",
        "random_partition_9.json",
        "random_partition_12.json",
    ):
        payload = json.loads((CANDIDATE / name).read_text())
        require(
            canonical_hash_without_field(payload, "sha256_without_this_field")
            == payload["sha256_without_this_field"],
            f"internal payload hash mismatch: {name}",
        )

    extension_replay = replay_extension_census()
    expected_extension = json.loads(
        (CANDIDATE / "extension_result.json").read_text()
    )
    require(
        extension_replay == expected_extension["totals"],
        f"extension census mismatch: {extension_replay}",
    )
    require(expected_extension["first_violation"] is None, "unexpected stored violation")
    require(
        expected_extension["scope"]["complete_labeled_extension_class"] is True,
        "stored extension scope is not complete",
    )

    random_nine = json.loads((CANDIDATE / "random_partition_9.json").read_text())
    random_twelve = json.loads(
        (CANDIDATE / "random_partition_12.json").read_text()
    )
    random_totals = {
        key: random_nine["totals"][key] + random_twelve["totals"][key]
        for key in random_nine["totals"]
    }
    require(random_totals["equality_graphs"] == 32141, "wrong random equality sum")
    require(
        random_totals["independent_state_pairs"] == 20382718,
        "wrong random pair sum",
    )
    require(
        not random_nine["scope"]["coverage_claim"]
        and not random_twelve["scope"]["coverage_claim"],
        "random evidence incorrectly claims coverage",
    )

    return {
        "schema": "greatest-family-reciprocity-hostile-v1",
        "status": "PASS",
        "graph_specific": {
            "graph6": GRAPH6,
            "graph6_round_trip": True,
            "order": n,
            "size": len(EXPECTED_EDGES),
            "connected": True,
            "parameters": parameters,
            "minimum_clique_partition": [
                list(block) for block in clique_witnesses[theta] or ()
            ],
            "greatest_triple_kernel_size": len(family),
            "greatest_triple_kernel_sha256": family_digest(family),
            "attack_obligations": obligations,
            "legal_retained_moves": retained_moves,
            "maximum_independent_triples": len(independent_triples),
            "tested_pair_exchange_quadruples": tested_quadruples,
            "asymmetric_pair_exchange_quadruples": asymmetric_quadruples,
            "selected_forward_state": sorted(forward_state),
            "selected_reverse_state": sorted(reverse_state),
            "failed_attack": failed_attack,
            "failed_attack_successors": {
                str(guard): {
                    "state": list(successor),
                    "undominated": list(missed),
                }
                for guard, (successor, missed) in failures.items()
            },
            "selected_endpoint_mutual_matchings": mutual_matchings,
            "selected_endpoint_family_base_ordering_cubes": family_cubes,
        },
        "extension_replay": {
            "classification_retained": "OBSERVED",
            "totals": extension_replay,
            "matches_candidate": True,
        },
        "random_evidence_audit": {
            "classification_retained": "EXPLORATORY",
            "recorded_equality_graphs": random_totals["equality_graphs"],
            "recorded_independent_state_pairs": random_totals[
                "independent_state_pairs"
            ],
            "internal_hashes_valid": True,
            "coverage_claims_false": True,
        },
        "sat_evidence_audit": {
            "classification_retained": "EXPLORATORY",
            "proof_logs_present": False,
            "disjoint_endpoint_scope_explicit": True,
            "no_unsat_claim_promoted": True,
        },
        "candidate_manifest": {
            "entries_checked": len(checked_hashes),
            "all_hashes_and_byte_counts_valid": True,
            "candidate_note_sha256": checked_hashes["NOTE.md"],
            "candidate_result_sha256": checked_hashes[
                "countermodel_result.json"
            ],
        },
        "model_guardrails": {
            "unoccupied_attacks_only": True,
            "exactly_one_adjacent_guard_moves": True,
            "every_kernel_state_dominates": True,
            "graph_and_complement_not_confused": True,
            "greatest_family_not_arbitrary_family": True,
        },
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
