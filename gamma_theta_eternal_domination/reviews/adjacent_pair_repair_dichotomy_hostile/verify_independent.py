#!/usr/bin/env python3
"""Clean-room audit of the adjacent-pair repair dichotomy.

This verifier intentionally does not import the candidate checker or any
campaign evaluator.  Graphs are represented by Python neighbor sets and
guard configurations by frozensets, whereas the candidate uses integer
bitsets.  Eternal closure is evaluated literally from the one-guard
definition with attacks only at unoccupied vertices.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


def check(condition: bool, label: object) -> None:
    if not condition:
        raise AssertionError(label)


def graph_from_index(order: int, index: int) -> tuple[frozenset[int], ...]:
    neighbors = [set() for _ in range(order)]
    edge_slots = tuple(itertools.combinations(range(order), 2))
    for place, (left, right) in enumerate(edge_slots):
        if (index >> place) & 1:
            neighbors[left].add(right)
            neighbors[right].add(left)
    return tuple(frozenset(row) for row in neighbors)


def decode_short_graph6(text: str) -> tuple[frozenset[int], ...]:
    check(text and text[0] != "~", "extended graph6 is outside review scope")
    order = ord(text[0]) - 63
    check(0 <= order <= 62, "invalid graph6 order")
    payload: list[int] = []
    for character in text[1:]:
        value = ord(character) - 63
        check(0 <= value < 64, ("bad graph6 character", character))
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    check(len(payload) == 6 * ((required + 5) // 6), "wrong graph6 length")
    check(not any(payload[required:]), "nonzero graph6 padding")
    neighbors = [set() for _ in range(order)]
    cursor = 0
    for later in range(1, order):
        for earlier in range(later):
            if payload[cursor]:
                neighbors[earlier].add(later)
                neighbors[later].add(earlier)
            cursor += 1
    return tuple(frozenset(row) for row in neighbors)


def states(order: int, size: int) -> tuple[frozenset[int], ...]:
    return tuple(frozenset(choice) for choice in itertools.combinations(range(order), size))


def is_independent(
    graph: tuple[frozenset[int], ...], configuration: frozenset[int]
) -> bool:
    return all(not (graph[vertex] & (configuration - {vertex})) for vertex in configuration)


def dominates(
    graph: tuple[frozenset[int], ...], configuration: frozenset[int]
) -> bool:
    covered = set(configuration)
    for vertex in configuration:
        covered.update(graph[vertex])
    return len(covered) == len(graph)


def physical_responses(
    graph: tuple[frozenset[int], ...],
    configuration: frozenset[int],
    attacked: int,
) -> tuple[tuple[int, frozenset[int]], ...]:
    check(attacked not in configuration, ("occupied attack", configuration, attacked))
    return tuple(
        (guard, frozenset((configuration - {guard}) | {attacked}))
        for guard in sorted(configuration)
        if attacked in graph[guard]
    )


def is_eternal(
    graph: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
) -> bool:
    if not family or any(not dominates(graph, configuration) for configuration in family):
        return False
    for configuration in family:
        for attacked in range(len(graph)):
            if attacked in configuration:
                continue
            if not any(
                successor in family
                for _, successor in physical_responses(graph, configuration, attacked)
            ):
                return False
    return True


def literal_kernel(
    graph: tuple[frozenset[int], ...], guard_count: int
) -> frozenset[frozenset[int]]:
    surviving = {
        configuration
        for configuration in states(len(graph), guard_count)
        if dominates(graph, configuration)
    }
    while True:
        snapshot = frozenset(surviving)
        rejected = {
            configuration
            for configuration in snapshot
            if any(
                attacked not in configuration
                and not any(
                    successor in snapshot
                    for _, successor in physical_responses(
                        graph, configuration, attacked
                    )
                )
                for attacked in range(len(graph))
            )
        }
        if not rejected:
            return snapshot
        surviving.difference_update(rejected)


def has_exact_gamma_alpha_three(graph: tuple[frozenset[int], ...]) -> bool:
    order = len(graph)
    if order < 3:
        return False
    if any(dominates(graph, configuration) for configuration in states(order, 1)):
        return False
    if any(dominates(graph, configuration) for configuration in states(order, 2)):
        return False
    if not any(dominates(graph, configuration) for configuration in states(order, 3)):
        return False
    if not any(is_independent(graph, configuration) for configuration in states(order, 3)):
        return False
    return order < 4 or not any(
        is_independent(graph, configuration) for configuration in states(order, 4)
    )


def common_nonneighbors(
    graph: tuple[frozenset[int], ...], left: int, right: int
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in (left, right)
        and vertex not in graph[left]
        and vertex not in graph[right]
    )


def active_orientation(
    graph: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
    source: int,
    target: int,
) -> bool:
    for configuration in family:
        if (
            source in configuration
            and target not in configuration
            and is_independent(graph, configuration)
            and target in graph[source]
            and frozenset((configuration - {source}) | {target}) in family
        ):
            return True
    return False


def audit_omitted_orientation_from_definition(
    graph: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
    source: int,
    target: int,
    witness: int,
) -> int:
    """Reconstruct Lemma 3.1, including all occupancy/collision checks."""

    central = frozenset((source, target, witness))
    check(central not in family, ("central state unexpectedly retained", central))
    check(target in graph[source], "oriented pair is not an edge")
    check(witness not in graph[source], "witness hits source")
    check(witness not in graph[target], "witness hits target")

    completions = common_nonneighbors(graph, source, witness)
    check(completions, ("pair unexpectedly dominates", source, witness))
    constructions = 0
    for completion in completions:
        check(completion not in (source, witness), "missed vertex collision")
        check(
            completion != target,
            "attacked endpoint cannot be a completion because it hits source",
        )
        independent_state = frozenset((source, witness, completion))
        check(len(independent_state) == 3, "completion is not a triple")
        check(is_independent(graph, independent_state), "completion is not independent")
        check(
            independent_state in family,
            "maximum independent triple is absent from eternal family",
        )

        physical = physical_responses(graph, independent_state, target)
        eligible = {guard for guard, _ in physical}
        check(source in eligible, "source endpoint is graph-ineligible")
        check(witness not in eligible, "common nonneighbor became eligible")
        if completion in eligible:
            completion_successor = next(
                successor for guard, successor in physical if guard == completion
            )
            check(
                completion_successor == central,
                "completion guard does not reach the central state",
            )
            check(
                completion_successor not in family,
                "omitted central successor became retained",
            )
        source_successor = next(
            successor for guard, successor in physical if guard == source
        )
        check(
            source_successor in family,
            "closure did not force the source-endpoint response",
        )
        retained = [
            guard for guard, successor in physical if successor in family
        ]
        check(
            retained == [source],
            ("source response is not uniquely retained", retained),
        )
        constructions += 1
    return constructions


def audit_family(
    graph: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
) -> tuple[Counter, int, int, int]:
    check(has_exact_gamma_alpha_three(graph), "static assumptions fail")
    check(is_eternal(graph, family), "family is not one-guard eternal")

    # The proof uses the forced-state lemma for arbitrary eternal
    # subfamilies.  Verify it explicitly before invoking it below.
    independent_triples = {
        configuration
        for configuration in states(len(graph), 3)
        if is_independent(graph, configuration)
    }
    check(independent_triples <= family, "forced independent triple missing")

    branch_counts = Counter()
    orientation_constructions = 0
    nonedge_pair_fans = 0
    nonedge_exchange_obligations = 0
    for left in range(len(graph)):
        for right in range(left + 1, len(graph)):
            if right not in graph[left]:
                # Immediate all-pairs corollary, audited separately from
                # the candidate edge dichotomy.  Gamma three makes this
                # common-nonneighbor set nonempty.  Every central state
                # is independent, hence forced into the family.
                witnesses = common_nonneighbors(graph, left, right)
                check(
                    witnesses,
                    ("gamma-three nonedge lacks common nonneighbor", left, right),
                )
                for witness in witnesses:
                    central = frozenset((left, right, witness))
                    check(len(central) == 3, "nonedge central state collision")
                    check(is_independent(graph, central), "nonedge center not independent")
                    check(central in family, "nonedge independent center not retained")
                    for attacked in witnesses:
                        if witness == attacked:
                            continue
                        check(
                            attacked in graph[witness],
                            "alpha three failed to clique the nonedge witness set",
                        )
                        responses = physical_responses(graph, central, attacked)
                        check(
                            [guard for guard, _ in responses] == [witness],
                            "nonedge central exchange not physically unique",
                        )
                        check(
                            responses[0][1]
                            == frozenset((left, right, attacked)),
                            "wrong nonedge exchange endpoint",
                        )
                        check(
                            responses[0][1] in family,
                            "nonedge exchange endpoint not retained",
                        )
                        nonedge_exchange_obligations += 1
                nonedge_pair_fans += 1
                continue
            witnesses = common_nonneighbors(graph, left, right)
            check(witnesses, ("gamma-three edge lacks common nonneighbor", left, right))
            centers = {
                witness: frozenset((left, right, witness)) in family
                for witness in witnesses
            }
            if any(centers.values()):
                check(all(centers.values()), ("mixed central fan", left, right))
                for witness in witnesses:
                    for attacked in witnesses:
                        if witness == attacked:
                            continue
                        check(attacked in graph[witness], "central fan is not a clique")
                        source_state = frozenset((left, right, witness))
                        responses = physical_responses(graph, source_state, attacked)
                        check(
                            [guard for guard, _ in responses] == [witness],
                            ("central exchange not physically unique", responses),
                        )
                        check(
                            responses[0][1] == frozenset((left, right, attacked)),
                            "wrong central exchange endpoint",
                        )
                        check(responses[0][1] in family, "central target not retained")
                if active_orientation(graph, family, left, right) and active_orientation(
                    graph, family, right, left
                ):
                    branch_counts["retained_fan_reciprocal"] += 1
                else:
                    branch_counts["retained_fan_nonreciprocal"] += 1
            else:
                check(not any(centers.values()), "omitted fan is not uniform")
                for witness in witnesses:
                    orientation_constructions += audit_omitted_orientation_from_definition(
                        graph, family, left, right, witness
                    )
                    orientation_constructions += audit_omitted_orientation_from_definition(
                        graph, family, right, left, witness
                    )
                check(
                    active_orientation(graph, family, left, right),
                    "omitted fan lacks forward activity",
                )
                check(
                    active_orientation(graph, family, right, left),
                    "omitted fan lacks reverse activity",
                )
                branch_counts["omitted_fan_reciprocal"] += 1
    return (
        branch_counts,
        orientation_constructions,
        nonedge_pair_fans,
        nonedge_exchange_obligations,
    )


def minimum_cardinality(order: int, predicate) -> int:
    for size in range(1, order + 1):
        if any(predicate(configuration) for configuration in states(order, size)):
            return size
    raise AssertionError("finite minimum not found")


def independence_number(graph: tuple[frozenset[int], ...]) -> int:
    for size in range(len(graph), 0, -1):
        if any(is_independent(graph, configuration) for configuration in states(len(graph), size)):
            return size
    return 0


def clique_partition_number(graph: tuple[frozenset[int], ...]) -> int:
    order = len(graph)

    def colorable(part_count: int) -> bool:
        parts: list[list[int]] = [[] for _ in range(part_count)]

        def extend(vertex: int, used: int) -> bool:
            if vertex == order:
                return True
            for part_index in range(min(used + 1, part_count)):
                if all(member in graph[vertex] for member in parts[part_index]):
                    parts[part_index].append(vertex)
                    if extend(vertex + 1, max(used, part_index + 1)):
                        return True
                    parts[part_index].pop()
            return False

        return extend(0, 0)

    for count in range(1, order + 1):
        if colorable(count):
            return count
    raise AssertionError("singleton partition was rejected")


def parameter_vector(graph: tuple[frozenset[int], ...]) -> list[int]:
    order = len(graph)
    gamma = minimum_cardinality(order, lambda configuration: dominates(graph, configuration))
    independent_domination = minimum_cardinality(
        order,
        lambda configuration: is_independent(graph, configuration)
        and dominates(graph, configuration),
    )
    alpha = independence_number(graph)
    eternal_number = next(
        count for count in range(1, order + 1) if literal_kernel(graph, count)
    )
    theta = clique_partition_number(graph)
    return [gamma, independent_domination, alpha, eternal_number, theta]


def is_connected(graph: tuple[frozenset[int], ...]) -> bool:
    if not graph:
        return False
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in graph[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    return len(reached) == len(graph)


def edge_list(graph: tuple[frozenset[int], ...]) -> list[list[int]]:
    return [
        [left, right]
        for left in range(len(graph))
        for right in range(left + 1, len(graph))
        if right in graph[left]
    ]


def control(record: str) -> dict:
    graph = decode_short_graph6(record)
    family = literal_kernel(graph, 3)
    (
        branch_counts,
        constructions,
        nonedge_pair_fans,
        nonedge_exchange_obligations,
    ) = audit_family(graph, family)
    return {
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": len(graph),
        "size": len(edge_list(graph)),
        "edge_list": edge_list(graph),
        "connected": is_connected(graph),
        "parameters": parameter_vector(graph),
        "greatest_triple_family_size": len(family),
        "branch_counts": dict(sorted(branch_counts.items())),
        "omitted_orientation_constructions": constructions,
        "all_pairs_corollary": {
            "nonedge_pair_fans": nonedge_pair_fans,
            "nonedge_exchange_obligations": nonedge_exchange_obligations,
        },
    }


def main() -> None:
    greatest_graphs = 0
    greatest_branches = Counter()
    greatest_constructions = 0
    greatest_nonedge_fans = 0
    greatest_nonedge_exchanges = 0
    labeled_graphs = 0
    for order in range(1, 7):
        edge_count = order * (order - 1) // 2
        for graph_index in range(1 << edge_count):
            labeled_graphs += 1
            graph = graph_from_index(order, graph_index)
            if not has_exact_gamma_alpha_three(graph):
                continue
            family = literal_kernel(graph, 3)
            if not family:
                continue
            (
                branches,
                constructions,
                nonedge_fans,
                nonedge_exchanges,
            ) = audit_family(graph, family)
            greatest_graphs += 1
            greatest_branches.update(branches)
            greatest_constructions += constructions
            greatest_nonedge_fans += nonedge_fans
            greatest_nonedge_exchanges += nonedge_exchanges

    arbitrary_graphs = 0
    arbitrary_families = 0
    arbitrary_branches = Counter()
    arbitrary_constructions = 0
    arbitrary_nonedge_fans = 0
    arbitrary_nonedge_exchanges = 0
    for order in range(3, 6):
        edge_count = order * (order - 1) // 2
        triples = states(order, 3)
        for graph_index in range(1 << edge_count):
            graph = graph_from_index(order, graph_index)
            if not has_exact_gamma_alpha_three(graph):
                continue
            dominating = tuple(
                configuration
                for configuration in triples
                if dominates(graph, configuration)
            )
            has_family = False
            for selector in range(1, 1 << len(dominating)):
                family = frozenset(
                    dominating[position]
                    for position in range(len(dominating))
                    if (selector >> position) & 1
                )
                if not is_eternal(graph, family):
                    continue
                (
                    branches,
                    constructions,
                    nonedge_fans,
                    nonedge_exchanges,
                ) = audit_family(graph, family)
                has_family = True
                arbitrary_families += 1
                arbitrary_branches.update(branches)
                arbitrary_constructions += constructions
                arbitrary_nonedge_fans += nonedge_fans
                arbitrary_nonedge_exchanges += nonedge_exchanges
            arbitrary_graphs += int(has_family)

    controls = {
        "connected_two_branch_control": control("EpQ?"),
        "retained_fan_reciprocal_control": control("D]?"),
    }
    check(
        controls["connected_two_branch_control"]["edge_list"]
        == [[0, 1], [0, 2], [0, 5], [1, 4], [2, 3]],
        "connected control edge list mismatch",
    )
    check(
        controls["connected_two_branch_control"]["parameters"] == [3, 3, 3, 3, 3],
        "connected control parameter mismatch",
    )
    check(
        controls["connected_two_branch_control"]["branch_counts"].get(
            "retained_fan_nonreciprocal", 0
        )
        > 0
        and controls["connected_two_branch_control"]["branch_counts"].get(
            "omitted_fan_reciprocal", 0
        )
        > 0,
        "connected control does not realize both principal branches",
    )
    check(
        controls["retained_fan_reciprocal_control"]["parameters"]
        == [3, 3, 3, 3, 3],
        "reciprocal-fan control parameter mismatch",
    )
    check(
        controls["retained_fan_reciprocal_control"]["branch_counts"].get(
            "retained_fan_reciprocal", 0
        )
        > 0,
        "retained reciprocal branch is absent",
    )

    result = {
        "schema": "adjacent-pair-repair-dichotomy-hostile-review-v1",
        "verdict": "UNCONDITIONAL_PASS",
        "model": "one guard moves along one edge; attacks only at unoccupied vertices",
        "greatest_family_census_through_order_6": {
            "labeled_graphs_examined": labeled_graphs,
            "applicable_graphs": greatest_graphs,
            "applicable_families": greatest_graphs,
            "edge_obligations": dict(sorted(greatest_branches.items())),
            "omitted_orientation_constructions": greatest_constructions,
            "all_pairs_corollary": {
                "nonedge_pair_fans": greatest_nonedge_fans,
                "nonedge_exchange_obligations": greatest_nonedge_exchanges,
            },
        },
        "arbitrary_eternal_subfamily_census_through_order_5": {
            "applicable_graphs": arbitrary_graphs,
            "applicable_families": arbitrary_families,
            "edge_obligations": dict(sorted(arbitrary_branches.items())),
            "omitted_orientation_constructions": arbitrary_constructions,
            "all_pairs_corollary": {
                "nonedge_pair_fans": arbitrary_nonedge_fans,
                "nonedge_exchange_obligations": arbitrary_nonedge_exchanges,
            },
        },
        "controls": controls,
        "scope": (
            "The theorem and sharp controls pass. The discovery-only order-26 "
            "UNSAT observation is excluded; this does not eliminate QQ1, prove "
            "complete k=3, or resolve gamma-theta."
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
