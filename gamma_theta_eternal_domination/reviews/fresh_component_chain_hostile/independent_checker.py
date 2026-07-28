#!/usr/bin/env python3
"""Clean-room audit of the two fresh-component-chain controls.

This checker imports no campaign evaluator and no candidate executable.
It reconstructs both graphs, all five parameters, the relevant eternal
families, every literal one-guard obligation, response lists, frozen
components, and the claimed side-incidence controls.
"""

from __future__ import annotations

import hashlib
import itertools
import json


def pair(a: int, b: int) -> tuple[int, int]:
    if a == b:
        raise ValueError("simple graphs have no loops")
    return (a, b) if a < b else (b, a)


class ExactGraph:
    def __init__(self, graph6: str):
        values = [ord(char) - 63 for char in graph6]
        if not values or not 0 <= values[0] <= 62:
            raise ValueError("only short graph6 records are supported")
        self.graph6 = graph6
        self.n = values[0]
        payload = [
            (value >> shift) & 1
            for value in values[1:]
            for shift in range(5, -1, -1)
        ]
        needed = self.n * (self.n - 1) // 2
        if len(payload) < needed:
            raise ValueError("truncated graph6 record")
        cursor = 0
        edges: set[tuple[int, int]] = set()
        for high in range(1, self.n):
            for low in range(high):
                if payload[cursor]:
                    edges.add((low, high))
                cursor += 1
        self.g_edges = frozenset(edges)
        self.h_edges = frozenset(
            pair(a, b)
            for a, b in itertools.combinations(range(self.n), 2)
            if pair(a, b) not in self.g_edges
        )

    def adjacent(self, a: int, b: int) -> bool:
        return a != b and pair(a, b) in self.g_edges

    def h_adjacent(self, a: int, b: int) -> bool:
        return a != b and pair(a, b) in self.h_edges

    def connected(self) -> bool:
        reached = {0}
        frontier = [0]
        for vertex in frontier:
            for other in range(self.n):
                if other not in reached and self.adjacent(vertex, other):
                    reached.add(other)
                    frontier.append(other)
        return len(reached) == self.n

    def dominates(self, state: frozenset[int]) -> bool:
        return all(
            vertex in state
            or any(self.adjacent(vertex, guard) for guard in state)
            for vertex in range(self.n)
        )

    def independent(self, state: frozenset[int]) -> bool:
        return all(
            not self.adjacent(a, b)
            for a, b in itertools.combinations(state, 2)
        )

    def subsets(self, size: int):
        return (
            frozenset(choice)
            for choice in itertools.combinations(range(self.n), size)
        )

    def minimum_witness(self, predicate) -> tuple[int, tuple[int, ...]]:
        for size in range(1, self.n + 1):
            for state in self.subsets(size):
                if predicate(state):
                    return size, tuple(sorted(state))
        raise AssertionError("finite subset search exhausted")

    def maximum_independent(self) -> tuple[int, tuple[int, ...]]:
        for size in range(self.n, 0, -1):
            for state in self.subsets(size):
                if self.independent(state):
                    return size, tuple(sorted(state))
        raise AssertionError("finite subset search exhausted")

    def minimum_clique_partition(self) -> tuple[int, list[list[int]]]:
        """Color the complement by a fresh saturation-first search."""

        h_neighbors = {
            vertex: {
                other
                for other in range(self.n)
                if self.h_adjacent(vertex, other)
            }
            for vertex in range(self.n)
        }

        def coloring_with(limit: int) -> dict[int, int] | None:
            colors: dict[int, int] = {}

            def search() -> bool:
                if len(colors) == self.n:
                    return True
                uncolored = set(range(self.n)) - colors.keys()
                vertex = max(
                    uncolored,
                    key=lambda x: (
                        len(
                            {
                                colors[y]
                                for y in h_neighbors[x]
                                if y in colors
                            }
                        ),
                        len(h_neighbors[x]),
                        -x,
                    ),
                )
                blocked = {
                    colors[y] for y in h_neighbors[vertex] if y in colors
                }
                for color in range(limit):
                    if color in blocked:
                        continue
                    colors[vertex] = color
                    if search():
                        return True
                    del colors[vertex]
                return False

            return dict(colors) if search() else None

        for count in range(1, self.n + 1):
            coloring = coloring_with(count)
            if coloring is not None:
                classes = [
                    sorted(vertex for vertex, color in coloring.items()
                           if color == chosen)
                    for chosen in range(count)
                ]
                return count, classes
        raise AssertionError("finite coloring search exhausted")

    def kernel(
        self,
        guards: int,
        permitted: set[frozenset[int]] | None = None,
    ) -> tuple[set[frozenset[int]], list[int]]:
        family = {
            state
            for state in self.subsets(guards)
            if self.dominates(state)
            and (permitted is None or state in permitted)
        }
        round_sizes: list[int] = []
        while True:
            doomed: set[frozenset[int]] = set()
            for state in family:
                for attack in set(range(self.n)) - state:
                    if not any(
                        self.adjacent(guard, attack)
                        and (state - {guard}) | {attack} in family
                        for guard in state
                    ):
                        doomed.add(state)
                        break
            if not doomed:
                return family, round_sizes
            round_sizes.append(len(doomed))
            family -= doomed

    def eternal_number(
        self,
    ) -> tuple[int, dict[int, int], set[frozenset[int]]]:
        sizes: dict[int, int] = {}
        for guards in range(1, self.n + 1):
            family, _ = self.kernel(guards)
            sizes[guards] = len(family)
            if family:
                return guards, sizes, family
        raise AssertionError("all-vertex state must be eternal")

    def parameters(self) -> tuple[dict[str, int], dict[str, object]]:
        gamma, gamma_witness = self.minimum_witness(self.dominates)
        independent_domination, i_witness = self.minimum_witness(
            lambda state: self.independent(state) and self.dominates(state)
        )
        alpha, alpha_witness = self.maximum_independent()
        gamma_infinity, kernel_sizes, _ = self.eternal_number()
        theta, partition = self.minimum_clique_partition()
        return (
            {
                "gamma": gamma,
                "i": independent_domination,
                "alpha": alpha,
                "gamma_infinity": gamma_infinity,
                "theta": theta,
            },
            {
                "dominating": list(gamma_witness),
                "maximal_independent": list(i_witness),
                "maximum_independent": list(alpha_witness),
                "clique_partition": partition,
                "kernel_sizes_through_first_nonempty": {
                    str(k): value for k, value in kernel_sizes.items()
                },
            },
        )

    def family_audit(
        self, family: set[frozenset[int]]
    ) -> tuple[int, int, str]:
        lines: list[str] = []
        obligations = 0
        retained_moves = 0
        for state in sorted(family, key=lambda item: tuple(sorted(item))):
            assert self.dominates(state)
            for attack in sorted(set(range(self.n)) - state):
                responders = []
                for guard in sorted(state):
                    successor = (state - {guard}) | {attack}
                    if self.adjacent(guard, attack) and successor in family:
                        responders.append(guard)
                assert responders
                obligations += 1
                retained_moves += len(responders)
                lines.append(
                    f"{''.join(map(str, sorted(state)))}:{attack}:"
                    f"{','.join(map(str, responders))}"
                )
        digest = hashlib.sha256(
            ("\n".join(lines) + "\n").encode("ascii")
        ).hexdigest()
        return obligations, retained_moves, digest

    def components(
        self, vertices: set[int]
    ) -> list[tuple[list[int], list[int], list[int]]]:
        unseen = set(vertices)
        result = []
        while unseen:
            start = min(unseen)
            queue = [start]
            color = {start: 0}
            unseen.remove(start)
            for current in queue:
                for other in sorted(vertices):
                    if not self.h_adjacent(current, other):
                        continue
                    if other not in color:
                        color[other] = 1 - color[current]
                        unseen.remove(other)
                        queue.append(other)
                    else:
                        assert color[other] != color[current]
            members = sorted(color)
            result.append(
                (
                    members,
                    sorted(x for x in members if color[x] == 0),
                    sorted(x for x in members if color[x] == 1),
                )
            )
        return sorted(result)


def state_hash(family: set[frozenset[int]]) -> str:
    payload = "".join(
        " ".join(map(str, sorted(state))) + "\n"
        for state in sorted(family, key=lambda item: tuple(sorted(item)))
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def response_lists(
    graph: ExactGraph,
    family: set[frozenset[int]],
    reference: frozenset[int],
) -> dict[int, frozenset[int]]:
    outside = set(range(graph.n)) - reference
    return {
        target: frozenset(
            anchor
            for anchor in reference
            if graph.adjacent(anchor, target)
            and (reference - {anchor}) | {target} in family
        )
        for target in outside
    }


def frozen_components(
    graph: ExactGraph,
    reference: frozenset[int],
    lists: dict[int, frozenset[int]],
    anchor: int,
):
    vertices = (set(reference) - {anchor}) | {
        target for target, values in lists.items() if anchor not in values
    }
    return graph.components(vertices)


def list_coloring_count(
    graph: ExactGraph,
    reference: frozenset[int],
    lists: dict[int, frozenset[int]],
) -> int:
    fixed = {anchor: anchor for anchor in reference}
    outside = sorted(lists)
    count = 0

    def search(index: int) -> None:
        nonlocal count
        if index == len(outside):
            count += 1
            return
        vertex = outside[index]
        for color in sorted(lists[vertex]):
            if any(
                graph.h_adjacent(vertex, other)
                and fixed[other] == color
                for other in fixed
            ):
                continue
            fixed[vertex] = color
            search(index + 1)
            del fixed[vertex]

    search(0)
    return count


def exposed_mates(
    graph: ExactGraph,
    lists: dict[int, frozenset[int]],
    anchor: int,
    source: int,
) -> list[int]:
    return sorted(
        vertex
        for vertex, values in lists.items()
        if vertex != source
        and anchor in values
        and graph.h_adjacent(vertex, source)
    )


def audit_equality_control() -> dict[str, object]:
    graph = ExactGraph("HEhbtjK")
    assert graph.n == 9
    assert graph.connected()
    reference = frozenset({0, 1, 2})
    assert graph.independent(reference)

    family, rounds = graph.kernel(3)
    assert len(family) == 48
    obligations, moves, obligation_hash = graph.family_audit(family)
    assert obligations == 288
    lists = response_lists(graph, family, reference)
    expected = {
        3: frozenset({0, 1}),
        4: frozenset({0, 2}),
        5: frozenset({1, 2}),
        6: frozenset({1, 2}),
        7: frozenset({0, 2}),
        8: frozenset({0, 1}),
    }
    assert lists == expected

    parameters, witnesses = graph.parameters()
    assert parameters == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    frozen_zero = frozen_components(graph, reference, lists, 0)
    frozen_two = frozen_components(graph, reference, lists, 2)
    assert frozen_zero == [([1, 2], [1], [2]), ([5, 6], [5], [6])]
    assert frozen_two == [([0, 1], [0], [1]), ([3, 8], [3], [8])]

    assert lists[3] == lists[8] == frozenset({0, 1})
    assert graph.h_adjacent(3, 8)
    assert graph.h_adjacent(3, 5) and not graph.h_adjacent(3, 6)
    assert graph.h_adjacent(8, 6) and not graph.h_adjacent(8, 5)
    exposed = {
        3: exposed_mates(graph, lists, 0, 3),
        8: exposed_mates(graph, lists, 0, 8),
    }
    assert exposed == {3: [4, 8], 8: [3, 7]}
    compatible_colorings = list_coloring_count(graph, reference, lists)
    assert compatible_colorings > 0

    return {
        "graph6": graph.graph6,
        "connected": True,
        "order": graph.n,
        "size": len(graph.g_edges),
        "parameters": parameters,
        "parameter_witnesses": witnesses,
        "greatest_triple_family_size": len(family),
        "greatest_triple_family_sha256": state_hash(family),
        "kernel_deletion_rounds": rounds,
        "attack_obligations": obligations,
        "retained_response_moves": moves,
        "obligation_sha256": obligation_hash,
        "response_lists": {
            str(vertex): sorted(values)
            for vertex, values in sorted(lists.items())
        },
        "frozen_0_components_with_bipartitions": frozen_zero,
        "frozen_2_components_with_bipartitions": frozen_two,
        "target_component": [5, 6],
        "source_component": [3, 8],
        "opposite_target_side_incidence": [[3, 5], [8, 6]],
        "exposed_positive_mates": {
            str(source): values for source, values in exposed.items()
        },
        "compatible_response_list_colorings": compatible_colorings,
        "scope_check": (
            "sources 3 and 8 see opposite target sides but are adjacent "
            "in the complement, so every proper response coloring gives "
            "them opposite colors; this is not a same-color return"
        ),
    }


def audit_gamma_two_boundary() -> dict[str, object]:
    graph = ExactGraph("HFzvvn{")
    assert graph.n == 9
    assert graph.connected()
    explicit_h = {
        pair(*edge)
        for edge in (
            (0, 1),
            (0, 2),
            (1, 2),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 8),
            (7, 8),
            (4, 7),
        )
    }
    assert graph.h_edges == explicit_h
    reference = frozenset({0, 1, 2})
    assert graph.independent(reference)
    expected = {
        3: frozenset({0}),
        4: frozenset({0, 1}),
        5: frozenset({0}),
        6: frozenset({0, 1}),
        7: frozenset({1, 2}),
        8: frozenset({1, 2}),
    }
    banned = {
        (reference - {anchor}) | {target}
        for target, values in expected.items()
        for anchor in reference
        if anchor not in values
    }
    permitted = {
        state
        for state in graph.subsets(3)
        if state not in banned
    }
    family, rounds = graph.kernel(3, permitted=permitted)
    assert len(family) == 52
    assert rounds == [15, 4, 4]
    assert family <= graph.kernel(3)[0]
    obligations, moves, obligation_hash = graph.family_audit(family)
    assert obligations == 312
    lists = response_lists(graph, family, reference)
    assert lists == expected
    parameters, witnesses = graph.parameters()
    assert parameters == {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }

    frozen_two = frozen_components(graph, reference, lists, 2)
    frozen_zero = frozen_components(graph, reference, lists, 0)
    assert frozen_two == [
        ([0, 1], [0], [1]),
        ([3, 4, 5, 6], [3, 5], [4, 6]),
    ]
    assert frozen_zero == [([1, 2], [1], [2]), ([7, 8], [7], [8])]
    assert graph.h_adjacent(4, 7) and graph.h_adjacent(6, 8)
    assert not graph.h_adjacent(4, 8)
    assert not graph.h_adjacent(6, 7)
    assert not graph.h_adjacent(4, 6)
    assert expected[4] == expected[6] == frozenset({0, 1})
    exposed = {
        4: exposed_mates(graph, lists, 0, 4),
        6: exposed_mates(graph, lists, 0, 6),
    }
    assert exposed == {4: [3, 5], 6: [5]}
    compatible_colorings = list_coloring_count(graph, reference, lists)
    assert compatible_colorings == 0

    dominating_pairs = [
        sorted(state)
        for state in graph.subsets(2)
        if graph.dominates(state)
    ]
    assert len(dominating_pairs) == 26
    _, _, unrestricted_triples = graph.eternal_number()

    return {
        "graph6": graph.graph6,
        "connected": True,
        "order": graph.n,
        "size": len(graph.g_edges),
        "parameters": parameters,
        "parameter_witnesses": witnesses,
        "restricted_triple_family_size": len(family),
        "restricted_triple_family_sha256": state_hash(family),
        "unrestricted_greatest_triple_family_size": len(
            unrestricted_triples
        ),
        "restricted_kernel_deletion_rounds": rounds,
        "attack_obligations": obligations,
        "retained_response_moves": moves,
        "obligation_sha256": obligation_hash,
        "response_lists": {
            str(vertex): sorted(values)
            for vertex, values in sorted(lists.items())
        },
        "frozen_2_components_with_bipartitions": frozen_two,
        "frozen_0_components_with_bipartitions": frozen_zero,
        "source_ports_same_side": [4, 6],
        "target_component_opposite_sides": [7, 8],
        "cross_clause_edges": [[4, 7], [6, 8]],
        "exposed_positive_mates": {
            str(source): values for source, values in exposed.items()
        },
        "compatible_response_list_colorings": compatible_colorings,
        "dominating_pair_count": len(dominating_pairs),
        "dominating_pairs": dominating_pairs,
        "scope_check": (
            "the separated same-color return is exact, but gamma=2 and "
            "26 dominating pairs prevent it from refuting a gamma=3 "
            "synchronization theorem"
        ),
    }


def main() -> None:
    result = {
        "schema": "fresh-component-chain-hostile-clean-room-v1",
        "status": "PASS",
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one G-edge",
            "retention": "successor belongs to the same family",
        },
        "equality_control": audit_equality_control(),
        "gamma_two_boundary": audit_gamma_two_boundary(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
