#!/usr/bin/env python3
"""Clean-room audit of the supported-pair completion-fan package.

This file deliberately imports no campaign evaluator and no candidate code.
Graphs are immutable neighbor sets and configurations are frozensets.  Eternal
families are reconstructed by literal synchronous greatest-fixed-point
deletion from the one-guard definition.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterable


Graph = tuple[frozenset[int], ...]
State = frozenset[int]
Family = frozenset[State]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(text: str) -> Graph:
    require(text and text[0] != ">", "headers and empty graph6 unsupported")
    order = ord(text[0]) - 63
    require(0 <= order <= 62, ("short graph6 only", order))
    bits: list[int] = []
    for character in text[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, ("bad graph6 character", character))
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    require(len(bits) >= needed, ("short graph6 payload", len(bits), needed))
    neighbors = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                neighbors[low].add(high)
                neighbors[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in neighbors)


def graph_from_code(order: int, code: int) -> Graph:
    neighbors = [set() for _ in range(order)]
    bit = 0
    for high in range(1, order):
        for low in range(high):
            if (code >> bit) & 1:
                neighbors[low].add(high)
                neighbors[high].add(low)
            bit += 1
    return tuple(frozenset(row) for row in neighbors)


def edges(graph: Graph) -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for first in range(len(graph))
        for second in range(first + 1, len(graph))
        if second in graph[first]
    )


def edge_hash(graph: Graph) -> str:
    payload = json.dumps(
        [list(edge) for edge in edges(graph)], separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def configurations(order: int, size: int) -> Iterable[State]:
    return (frozenset(vertices) for vertices in itertools.combinations(range(order), size))


def independent(graph: Graph, state: State) -> bool:
    return all(not (graph[vertex] & (state - {vertex})) for vertex in state)


def dominates(graph: Graph, state: State) -> bool:
    covered = set(state)
    for vertex in state:
        covered.update(graph[vertex])
    return len(covered) == len(graph)


def dominating_states(graph: Graph, size: int) -> Family:
    return frozenset(
        state for state in configurations(len(graph), size) if dominates(graph, state)
    )


def responses(
    graph: Graph, family: Family, source: State, attack: int
) -> tuple[tuple[int, State], ...]:
    require(attack not in source, ("occupied attack", source, attack))
    result = []
    for guard in sorted(source):
        if attack not in graph[guard]:
            continue
        successor = frozenset((source - {guard}) | {attack})
        if successor in family:
            result.append((guard, successor))
    return tuple(result)


def is_eternal(graph: Graph, family: Family) -> bool:
    if not family:
        return False
    if any(not dominates(graph, state) for state in family):
        return False
    for source in family:
        for attack in range(len(graph)):
            if attack not in source and not responses(graph, family, source, attack):
                return False
    return True


def greatest_family(graph: Graph, size: int) -> Family:
    family = dominating_states(graph, size)
    while family:
        survivor = frozenset(
            source
            for source in family
            if all(
                responses(graph, family, source, attack)
                for attack in range(len(graph))
                if attack not in source
            )
        )
        if survivor == family:
            return family
        family = survivor
    return frozenset()


def exact_gamma(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in configurations(len(graph), size)):
            return size
    raise AssertionError("no dominating set")


def exact_i(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(
            independent(graph, state) and dominates(graph, state)
            for state in configurations(len(graph), size)
        ):
            return size
    raise AssertionError("no independent dominating set")


def exact_alpha(graph: Graph) -> int:
    for size in range(len(graph), -1, -1):
        if any(independent(graph, state) for state in configurations(len(graph), size)):
            return size
    raise AssertionError("no independent set")


def exact_eternal(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if greatest_family(graph, size):
            return size
    raise AssertionError("no eternal family")


def complement(graph: Graph) -> Graph:
    vertices = set(range(len(graph)))
    return tuple(
        frozenset(vertices - {vertex} - set(graph[vertex]))
        for vertex in range(len(graph))
    )


def colorable(graph: Graph, colors: int) -> bool:
    order = len(graph)
    assignment = [-1] * order

    def choose_vertex() -> int | None:
        uncolored = [vertex for vertex in range(order) if assignment[vertex] < 0]
        if not uncolored:
            return None
        return max(
            uncolored,
            key=lambda vertex: (
                len(
                    {
                        assignment[neighbor]
                        for neighbor in graph[vertex]
                        if assignment[neighbor] >= 0
                    }
                ),
                len(graph[vertex]),
                -vertex,
            ),
        )

    def search() -> bool:
        vertex = choose_vertex()
        if vertex is None:
            return True
        forbidden = {
            assignment[neighbor]
            for neighbor in graph[vertex]
            if assignment[neighbor] >= 0
        }
        for color in range(colors):
            if color in forbidden:
                continue
            assignment[vertex] = color
            if search():
                return True
            assignment[vertex] = -1
        return False

    return search()


def exact_chromatic(graph: Graph) -> int:
    for colors in range(1, len(graph) + 1):
        if colorable(graph, colors):
            return colors
    raise AssertionError("no coloring")


def parameters(graph: Graph) -> tuple[int, int, int, int, int]:
    return (
        exact_gamma(graph),
        exact_i(graph),
        exact_alpha(graph),
        exact_eternal(graph),
        exact_chromatic(complement(graph)),
    )


def common_missed(graph: Graph, first: int, second: int) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in (first, second)
        and vertex not in graph[first]
        and vertex not in graph[second]
    )


def active(
    graph: Graph, family: Family, source_guard: int, target: int
) -> bool:
    if target not in graph[source_guard]:
        return False
    for source in family:
        if (
            source_guard in source
            and target not in source
            and independent(graph, source)
            and frozenset((source - {source_guard}) | {target}) in family
        ):
            return True
    return False


def full_at(graph: Graph, family: Family, root: State, target: int) -> bool:
    return (
        target not in root
        and all(target in graph[guard] for guard in root)
        and all(frozenset((root - {guard}) | {target}) in family for guard in root)
    )


def check_supported_pair(
    graph: Graph, family: Family, source: State, first: int, second: int
) -> dict[str, int]:
    require({first, second} <= source, ("pair not supported", source, first, second))
    third = next(iter(source - {first, second}))
    witnesses = common_missed(graph, first, second)
    require(witnesses, ("empty fan under gamma three", first, second))
    exchanges = 0
    for witness in witnesses:
        fan = frozenset((first, second, witness))
        require(fan in family, ("fan state omitted", source, first, second, witness))
        if witness == third:
            require(fan == source, ("collision is not source", source, fan))
            continue
        require(witness in graph[third], ("third guard misses attack", source, witness))
        require(
            responses(graph, family, source, witness) == ((third, fan),),
            ("fan response not physically unique", source, witness),
        )
        exchanges += 1
    for left, right in itertools.combinations(witnesses, 2):
        require(right in graph[left], ("fan not clique", first, second, left, right))
    return {"fans": 1, "witnesses": len(witnesses), "unique_exchanges": exchanges}


def check_theorem_three(
    graph: Graph,
    family: Family,
    root: State,
    target: int,
    terminal: int,
    completion: int,
    anchor: int,
) -> dict[str, int]:
    require(independent(graph, root), ("root not independent", root))
    require(root in family, ("root not retained", root))
    require(full_at(graph, family, root, target), ("target not full", root, target))
    require(target not in graph[terminal], ("target-terminal edge", target, terminal))
    require(target not in graph[completion], ("target-completion edge", target, completion))
    require(terminal not in graph[completion], ("terminal-completion edge", terminal, completion))
    branch = frozenset((completion, anchor, terminal))
    require(branch in family, ("branch omitted", branch))

    witnesses = common_missed(graph, completion, anchor)
    trapped = tuple(witness for witness in witnesses if target not in graph[witness] and witness != target)
    cross = frozenset((target, completion, anchor))
    missed = tuple(
        vertex for vertex in range(len(graph)) if not ({vertex} | graph[vertex]) & cross
    )
    require(
        missed == trapped,
        ("cross missed-set identity", root, target, terminal, completion, anchor, missed, trapped),
    )
    require(dominates(graph, cross) == (not trapped), ("cross iff", cross, trapped))

    reverse_sources = 0
    if trapped:
        require(active(graph, family, target, anchor), ("reverse inactive", target, anchor))
        require(active(graph, family, anchor, target), ("full direction inactive", anchor, target))
        for witness in trapped:
            source = frozenset((target, completion, witness))
            fan = frozenset((completion, anchor, witness))
            require(independent(graph, source), ("reverse source not independent", source))
            require(source in family, ("forced independent source omitted", source))
            require(
                (target, fan) in responses(graph, family, source, anchor),
                ("named reverse move absent", source, anchor, fan),
            )
            reverse_sources += 1
    return {
        "instances": 1,
        "trapped_instances": int(bool(trapped)),
        "trapped_witnesses": len(trapped),
        "reverse_sources": reverse_sources,
    }


def merge_counts(total: dict[str, int], update: dict[str, int]) -> None:
    for key, value in update.items():
        total[key] = total.get(key, 0) + value


def audit_family(graph: Graph, family: Family) -> dict[str, int]:
    counts: dict[str, int] = {}
    for source in family:
        for first, second in itertools.combinations(sorted(source), 2):
            merge_counts(
                counts,
                check_supported_pair(graph, family, source, first, second),
            )

    for root in family:
        if not independent(graph, root):
            continue
        for target in range(len(graph)):
            if not full_at(graph, family, root, target):
                continue
            for terminal in range(len(graph)):
                if terminal == target or terminal in graph[target]:
                    continue
                for completion in common_missed(graph, target, terminal):
                    require(
                        frozenset((target, terminal, completion)) in family,
                        ("C010 failure", target, terminal, completion),
                    )
                    for anchor in sorted(root):
                        branch = frozenset((completion, anchor, terminal))
                        if branch in family:
                            merge_counts(
                                counts,
                                check_theorem_three(
                                    graph,
                                    family,
                                    root,
                                    target,
                                    terminal,
                                    completion,
                                    anchor,
                                ),
                            )
    return counts


def audit_fixed_case(
    graph: Graph,
    family: Family,
    *,
    root: tuple[int, int, int],
    target: int,
    terminal: int,
    completion: int,
    anchor: int,
    expected_witnesses: tuple[int, ...],
    expected_trapped: tuple[int, ...],
    cross_dominates: bool,
    cross_retained: bool,
) -> dict[str, object]:
    root_state = frozenset(root)
    require(full_at(graph, family, root_state, target), ("not full", root, target))
    branch = frozenset((completion, anchor, terminal))
    require(branch in family, ("branch absent", branch))
    require(
        independent(graph, frozenset((target, terminal, completion))),
        "completion not independent",
    )
    witnesses = common_missed(graph, completion, anchor)
    trapped = tuple(
        witness
        for witness in witnesses
        if witness != target and witness not in graph[target]
    )
    require(witnesses == expected_witnesses, ("witnesses", witnesses))
    require(trapped == expected_trapped, ("trapped", trapped))
    theorem_counts = check_theorem_three(
        graph,
        family,
        root_state,
        target,
        terminal,
        completion,
        anchor,
    )
    cross = frozenset((target, completion, anchor))
    require(dominates(graph, cross) == cross_dominates, "cross domination")
    require((cross in family) == cross_retained, "cross retention")
    return {
        "root": list(root),
        "target": target,
        "terminal": terminal,
        "completion": completion,
        "anchor": anchor,
        "witnesses": list(witnesses),
        "trapped": list(trapped),
        "cross": sorted(cross),
        "cross_dominates": dominates(graph, cross),
        "cross_retained": cross in family,
        "theorem_counts": theorem_counts,
    }


def fixed_controls() -> dict[str, object]:
    equality_code = "OYifur}UO]}iTij]tpo]v"
    equality = decode_graph6(equality_code)
    equality_family = greatest_family(equality, 3)
    require(parameters(equality) == (3, 3, 3, 3, 3), "equality parameters")
    require(len(equality_family) == 304, "equality family size")
    cases = {
        "nondominating_reciprocal": audit_fixed_case(
            equality,
            equality_family,
            root=(0, 1, 10),
            target=6,
            terminal=5,
            completion=7,
            anchor=1,
            expected_witnesses=(5, 14),
            expected_trapped=(5,),
            cross_dominates=False,
            cross_retained=False,
        ),
        "dominating_retained": audit_fixed_case(
            equality,
            equality_family,
            root=(0, 1, 10),
            target=6,
            terminal=5,
            completion=7,
            anchor=0,
            expected_witnesses=(12,),
            expected_trapped=(),
            cross_dominates=True,
            cross_retained=True,
        ),
        "dominating_omitted": audit_fixed_case(
            equality,
            equality_family,
            root=(1, 13, 14),
            target=12,
            terminal=2,
            completion=7,
            anchor=1,
            expected_witnesses=(5, 14),
            expected_trapped=(),
            cross_dominates=True,
            cross_retained=False,
        ),
    }

    gamma_two_code = "HF~mdfj"
    gamma_two = decode_graph6(gamma_two_code)
    gamma_two_family = greatest_family(gamma_two, 3)
    require(parameters(gamma_two) == (2, 2, 3, 3, 3), "gamma-two parameters")
    require(len(gamma_two_family) == 76, "gamma-two family size")
    gamma_two_branch = frozenset((2, 5, 8))
    require(gamma_two_branch in gamma_two_family, "gamma-two branch absent")
    require(common_missed(gamma_two, 2, 8) == (), "gamma-two pair not dominating")

    return {
        "equality": {
            "graph6": equality_code,
            "edge_list_sha256": edge_hash(equality),
            "parameters": [3, 3, 3, 3, 3],
            "greatest_family_size": len(equality_family),
            "cases": cases,
        },
        "gamma_two": {
            "graph6": gamma_two_code,
            "edge_list_sha256": edge_hash(gamma_two),
            "parameters": [2, 2, 3, 3, 3],
            "greatest_family_size": len(gamma_two_family),
            "retained_branch": sorted(gamma_two_branch),
            "pair": [2, 8],
            "pair_witnesses": [],
        },
    }


def labeled_census() -> dict[str, object]:
    greatest_counts: dict[str, int] = {
        "graphs_examined": 0,
        "applicable_graphs": 0,
        "applicable_families": 0,
    }
    arbitrary_counts: dict[str, int] = {
        "graphs_examined": 0,
        "applicable_graphs": 0,
        "eternal_subfamilies": 0,
    }

    for order in range(1, 7):
        for code in range(1 << (order * (order - 1) // 2)):
            graph = graph_from_code(order, code)
            greatest_counts["graphs_examined"] += 1
            if order <= 5:
                arbitrary_counts["graphs_examined"] += 1
            if order < 3:
                continue
            family = greatest_family(graph, 3)
            if not family:
                continue
            if exact_gamma(graph) != 3 or exact_alpha(graph) != 3:
                continue
            greatest_counts["applicable_graphs"] += 1
            greatest_counts["applicable_families"] += 1
            merge_counts(greatest_counts, audit_family(graph, family))

            if order > 5:
                continue
            arbitrary_counts["applicable_graphs"] += 1
            dominating = tuple(sorted(dominating_states(graph, 3), key=lambda s: tuple(sorted(s))))
            for selection in range(1, 1 << len(dominating)):
                subfamily = frozenset(
                    dominating[index]
                    for index in range(len(dominating))
                    if (selection >> index) & 1
                )
                if not is_eternal(graph, subfamily):
                    continue
                arbitrary_counts["eternal_subfamilies"] += 1
                merge_counts(arbitrary_counts, audit_family(graph, subfamily))

    require(greatest_counts["graphs_examined"] == 33867, greatest_counts)
    require(arbitrary_counts["graphs_examined"] == 1099, arbitrary_counts)
    return {
        "greatest_families_through_order_6": greatest_counts,
        "arbitrary_eternal_subfamilies_through_order_5": arbitrary_counts,
    }


def main() -> None:
    result = {
        "schema": "supported-pair-completion-fan-hostile-clean-room-v1",
        "model": (
            "attacks only at unoccupied vertices; exactly one occupied guard "
            "moves along one graph edge; successor remains in the same family"
        ),
        "fixed_controls": fixed_controls(),
        "labeled_census": labeled_census(),
        "scope": (
            "clean-room regression of the proved local theorems and sharp "
            "controls; no finite exclusion, complete-k3, or conjecture claim"
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
