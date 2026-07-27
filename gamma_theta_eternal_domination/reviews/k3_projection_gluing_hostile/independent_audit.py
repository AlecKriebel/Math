#!/usr/bin/env python3
"""Independent hostile replay for the k=3 projection-gluing note.

This checker deliberately does not import the generating probe.  Graphs are
represented by adjacency sets, the eternal kernel is computed by a
support-dependency queue, and the finite scans enumerate raw labelled masks
directly.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "math/working/k3_projection_gluing.md"
PROBE = ROOT / "math/working/k3_projection_gluing_evidence/probe.py"


def graph6(record):
    raw = [ord(char) - 63 for char in record]
    n = raw[0]
    bits = []
    for value in raw[1:]:
        bits += [(value >> shift) & 1 for shift in range(5, -1, -1)]
    graph = [set() for _ in range(n)]
    position = 0
    for right in range(1, n):
        for left in range(right):
            if bits[position]:
                graph[left].add(right)
                graph[right].add(left)
            position += 1
    return graph


def edge_set(graph):
    return {
        (left, right)
        for left in range(len(graph))
        for right in graph[left]
        if left < right
    }


def complement(graph):
    n = len(graph)
    return [
        {v for v in range(n) if v != u and v not in graph[u]}
        for u in range(n)
    ]


def dominates(graph, state):
    covered = set(state)
    for guard in state:
        covered.update(graph[guard])
    return len(covered) == len(graph)


def all_states(n, k):
    return {frozenset(state) for state in itertools.combinations(range(n), k)}


def eternal_kernel(graph, k, banned=frozenset()):
    """Greatest safe family via reverse support dependencies."""

    candidates = {
        state
        for state in all_states(len(graph), k)
        if state not in banned and dominates(graph, state)
    }
    supports = {}
    reverse = {state: [] for state in candidates}
    for state in candidates:
        for attack in set(range(len(graph))) - state:
            obligation = (state, attack)
            answers = {
                frozenset((state - {guard}) | {attack})
                for guard in state
                if attack in graph[guard]
                and frozenset((state - {guard}) | {attack}) in candidates
            }
            supports[obligation] = answers
            for answer in answers:
                reverse[answer].append(obligation)

    live = set(candidates)
    queue = [
        state
        for state in candidates
        if any(not supports[(state, attack)]
               for attack in set(range(len(graph))) - state)
    ]
    queued = set(queue)
    while queue:
        removed = queue.pop()
        if removed not in live:
            continue
        live.remove(removed)
        for source, attack in reverse[removed]:
            if source not in live:
                continue
            answers = supports[(source, attack)]
            answers.discard(removed)
            if not answers and source not in queued:
                queued.add(source)
                queue.append(source)
    return live


def verify_family(graph, family):
    obligations = 0
    for state in family:
        assert dominates(graph, state)
        for attack in set(range(len(graph))) - state:
            obligations += 1
            legal = False
            for guard in state:
                successor = frozenset((state - {guard}) | {attack})
                if attack in graph[guard] and successor in family:
                    legal = True
                    break
            assert legal
    return obligations


def response_lists(graph, family, reference):
    lists = {}
    for attack in set(range(len(graph))) - reference:
        lists[attack] = frozenset(
            guard
            for guard in reference
            if attack in graph[guard]
            and frozenset((reference - {guard}) | {attack}) in family
        )
        assert lists[attack]
    return lists


def direct_colorings(graph, family, reference):
    h = complement(graph)
    lists = response_lists(graph, family, reference)
    outside = sorted(lists, key=lambda x: (len(lists[x]), x))
    coloring = {anchor: anchor for anchor in reference}
    answers = []

    def visit(index):
        if index == len(outside):
            answers.append(dict(coloring))
            return
        vertex = outside[index]
        for color in sorted(lists[vertex]):
            if all(coloring.get(neighbor) != color for neighbor in h[vertex]):
                coloring[vertex] = color
                visit(index + 1)
                del coloring[vertex]

    visit(0)
    return answers


def bipartition(h, vertices):
    side = {}
    components = []
    for root in sorted(vertices):
        if root in side:
            continue
        side[root] = 0
        stack = [root]
        component = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbor in h[vertex] & vertices:
                if neighbor not in side:
                    side[neighbor] = 1 - side[vertex]
                    stack.append(neighbor)
                elif side[neighbor] == side[vertex]:
                    return None
        components.append(sorted(component))
    return side, components


def projection_formula(graph, lists, reference, visible_only=False):
    """Compile and brute-force the component-flip formula independently."""

    h = complement(graph)
    colors = sorted(reference)
    vertex_data = {}
    variables = []
    projections = {}
    for frozen in colors:
        remaining = sorted(reference - {frozen})
        omitted = {x for x, allowed in lists.items() if frozen not in allowed}
        projected = set(remaining) | omitted
        decomposition = bipartition(h, projected)
        if decomposition is None:
            return {"bipartite": False}
        side, components = decomposition
        anchor_index = next(
            index for index, component in enumerate(components)
            if remaining[0] in component
        )
        assert remaining[1] in components[anchor_index]
        if side[remaining[0]]:
            for vertex in components[anchor_index]:
                side[vertex] ^= 1
        for index, component in enumerate(components):
            variable = None
            if index != anchor_index:
                variable = len(variables)
                variables.append((frozen, tuple(component)))
            for vertex in component:
                vertex_data[frozen, vertex] = (
                    side[vertex], variable, tuple(remaining)
                )
        projections[frozen] = components

    units = []
    fixed_failure = False
    for vertex, allowed in lists.items():
        if len(allowed) != 1:
            continue
        demanded = next(iter(allowed))
        for frozen in reference - {demanded}:
            side, variable, remaining = vertex_data[frozen, vertex]
            wanted = side ^ remaining.index(demanded)
            if variable is None:
                fixed_failure |= bool(wanted)
            else:
                units.append((variable, wanted))

    clauses = []
    for left, right in itertools.combinations(sorted(lists), 2):
        if right not in h[left]:
            continue
        if len(lists[left]) == len(lists[right]) == 2:
            omit_left = next(iter(reference - lists[left]))
            omit_right = next(iter(reference - lists[right]))
            if omit_left == omit_right:
                continue
            shared = next(iter(lists[left] & lists[right]))
            literals = []
            for vertex, frozen in ((left, omit_left), (right, omit_right)):
                side, variable, remaining = vertex_data[frozen, vertex]
                collision_value = side ^ remaining.index(shared)
                literals.append((variable, collision_value))
            clauses.append(tuple(literals))

    solutions = []
    for assignment in itertools.product((0, 1), repeat=len(variables)):
        if fixed_failure:
            continue
        if any(assignment[var] != wanted for var, wanted in units):
            continue
        if any(
            all((0 if var is None else assignment[var]) == bad
                for var, bad in clause)
            for clause in clauses
        ):
            continue
        coloring = {}
        for vertex, allowed in lists.items():
            if len(allowed) == 1:
                coloring[vertex] = next(iter(allowed))
            elif len(allowed) == 2:
                frozen = next(iter(reference - allowed))
                side, variable, remaining = vertex_data[frozen, vertex]
                flip = 0 if variable is None else assignment[variable]
                coloring[vertex] = remaining[side ^ flip]
            elif not visible_only:
                continue
        assert all(
            coloring.get(left) != coloring.get(right)
            for left, right in edge_set(h)
            if left in coloring and right in coloring
        )
        solutions.append(coloring)
    return {
        "bipartite": True,
        "variables": len(variables),
        "units": len(units),
        "clauses": len(clauses),
        "solutions": solutions,
        "projections": projections,
    }


def alpha(graph):
    for size in range(len(graph), 0, -1):
        for state in itertools.combinations(range(len(graph)), size):
            if all(right not in graph[left]
                   for left, right in itertools.combinations(state, 2)):
                return size
    raise AssertionError


def gamma(graph):
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state)
               for state in itertools.combinations(range(len(graph)), size)):
            return size
    raise AssertionError


def gamma_infinity(graph):
    for size in range(1, len(graph) + 1):
        if eternal_kernel(graph, size):
            return size
    raise AssertionError


def chromatic_number(graph):
    order = sorted(range(len(graph)), key=lambda u: -len(graph[u]))
    for number in range(1, len(graph) + 1):
        colors = {}

        def visit(index):
            if index == len(order):
                return True
            vertex = order[index]
            used = {colors[v] for v in graph[vertex] if v in colors}
            for color in range(number):
                if color not in used:
                    colors[vertex] = color
                    if visit(index + 1):
                        return True
                    del colors[vertex]
            return False

        if visit(0):
            return number
    raise AssertionError


def parse_states(records):
    return {
        frozenset(int(character) for character in record)
        for record in records.replace(",", " ").split()
    }


FCX = parse_states(
    "012 014 016 024 025 026 045 056 "
    "123 134 136 234 235 236 345 356"
)
FDZ = parse_states(
    "012 123 014 124 134 015 025 135 235 045 145 245 345 "
    "026 236 046 246 346 056 356 456"
)
DUAL_DISPLAYED = parse_states(
    "012 014 015 025 026 027 028 045 046 047 048 056 058 "
    "123 124 127 128 134 135 145 148 157 158 "
    "235 236 237 238 246 247 257 267 268 278 "
    "345 346 347 348 356 358 456 457 468 478 567 568 578"
)
DUAL_BANNED = parse_states("023 013 024 125 126 016")


def coloring_partition(coloring):
    fibers = {}
    for vertex, color in coloring.items():
        fibers.setdefault(color, set()).add(vertex)
    return frozenset(frozenset(fiber) for fiber in fibers.values())


def ridge_audit(graph, family):
    independent = [
        state for state in family
        if all(right not in graph[left]
               for left, right in itertools.combinations(state, 2))
    ]
    ridge_pairs = 0
    covariance_checks = 0
    transported_colorings = 0
    for s, t in itertools.combinations(independent, 2):
        if len(s & t) != len(s) - 1:
            continue
        ridge_pairs += 1
        a = next(iter(s - t))
        b = next(iter(t - s))

        def rho(vertex):
            return b if vertex == a else a if vertex == b else vertex

        ls = response_lists(graph, family, s)
        lt = response_lists(graph, family, t)
        for vertex in set(range(len(graph))) - s:
            covariance_checks += 1
            assert frozenset(rho(color) for color in ls[vertex]) == lt[rho(vertex)]
        t_colorings = direct_colorings(graph, family, t)
        t_records = {
            tuple(sorted(coloring.items())) for coloring in t_colorings
        }
        for coloring in direct_colorings(graph, family, s):
            transported_colorings += 1
            transported = {
                vertex: rho(coloring[rho(vertex)])
                for vertex in range(len(graph))
            }
            assert tuple(sorted(transported.items())) in t_records
            assert coloring_partition(transported) == coloring_partition(coloring)
    return {
        "independent_states": len(independent),
        "ridge_pairs": ridge_pairs,
        "covariance_vertex_checks": covariance_checks,
        "transported_colorings_checked": transported_colorings,
    }


def named_cases():
    records = {}
    definitions = [
        ("FCZbg_greatest", "FCZbg", None, frozenset({0, 4, 6})),
        ("FCXfO_specified_16", "FCXfO", FCX, frozenset({0, 1, 2})),
        ("FDzro_specified_21", "FDzro", FDZ, frozenset({0, 1, 2})),
        ("FDzro_greatest", "FDzro", None, frozenset({0, 1, 2})),
        ("FCpbO_greatest", "FCpbO", None, frozenset({0, 5, 6})),
        ("HDzruf_dual_46", "HDzruf]", DUAL_DISPLAYED, frozenset({0, 1, 2})),
    ]
    for name, g6, specified, reference in definitions:
        graph = graph6(g6)
        family = eternal_kernel(graph, 3) if specified is None else specified
        obligations = verify_family(graph, family)
        lists = response_lists(graph, family, reference)
        formula = projection_formula(
            graph, lists, reference,
            visible_only=any(len(value) == 3 for value in lists.values()),
        )
        direct = direct_colorings(graph, family, reference)
        records[name] = {
            "order": len(graph),
            "family_size": len(family),
            "obligations": obligations,
            "parameters": {
                "gamma": gamma(graph),
                "alpha": alpha(graph),
                "gamma_infinity": gamma_infinity(graph),
                "theta": chromatic_number(complement(graph)),
            },
            "lists": {str(x): sorted(value) for x, value in sorted(lists.items())},
            "full_lists": sorted(x for x, value in lists.items() if len(value) == 3),
            "variables": formula["variables"],
            "units": formula["units"],
            "clauses": formula["clauses"],
            "projection_solutions": len(formula["solutions"]),
            "direct_colorings": len(direct),
            "ridge_audit": ridge_audit(graph, family),
        }

    dual = graph6("HDzruf]")
    expected_h = {
        (0, 1), (0, 2), (1, 2), (3, 4), (4, 5), (5, 6),
        (1, 3), (0, 6), (2, 7), (4, 7), (5, 7), (2, 8), (7, 8),
    }
    assert edge_set(complement(dual)) == expected_h
    dual_kernel = eternal_kernel(dual, 3, DUAL_BANNED)
    assert dual_kernel == DUAL_DISPLAYED
    h = complement(dual)
    assert h[4] & h[5] == {7}
    assert h[2] & h[7] == {8}
    params = records["HDzruf_dual_46"]["parameters"]
    assert params == {
        "gamma": 2, "alpha": 3, "gamma_infinity": 3, "theta": 3
    }
    partition = [{0, 3, 7}, {1, 4, 6, 8}, {2, 5}]
    assert set().union(*partition) == set(range(9))
    assert all(
        all(right in dual[left]
            for left, right in itertools.combinations(part, 2))
        for part in partition
    )
    records["HDzruf_dual_46"]["parameters"] = params
    records["HDzruf_dual_46"]["displayed_equals_banned_kernel"] = True
    records["HDzruf_dual_46"]["literal_w_y_intersections"] = True
    return records


def synthetic_formula_audit():
    """Exhaust all three-outside-vertex no-full abstract list systems."""

    proper_lists = [
        frozenset(choice)
        for size in (1, 2)
        for choice in itertools.combinations(range(3), size)
    ]
    systems = 0
    bipartite_systems = 0
    mismatches = []
    for values in itertools.product(proper_lists, repeat=3):
        lists = {3 + index: value for index, value in enumerate(values)}
        fixed_h = {(0, 1), (0, 2), (1, 2)}
        optional = []
        for vertex, allowed in lists.items():
            optional += [(color, vertex) for color in range(3) if color not in allowed]
        optional += [(3, 4), (3, 5), (4, 5)]
        for mask in range(1 << len(optional)):
            systems += 1
            h_edges = fixed_h | {
                edge for index, edge in enumerate(optional) if mask & (1 << index)
            }
            h = [set() for _ in range(6)]
            for left, right in h_edges:
                h[left].add(right)
                h[right].add(left)
            graph = complement(h)
            formula = projection_formula(graph, lists, frozenset({0, 1, 2}))
            if not formula["bipartite"]:
                continue
            bipartite_systems += 1
            direct = []
            for assignment in itertools.product(*[sorted(lists[x]) for x in (3, 4, 5)]):
                coloring = {0: 0, 1: 1, 2: 2, **dict(zip((3, 4, 5), assignment))}
                if all(coloring[left] != coloring[right] for left, right in h_edges):
                    direct.append(coloring)
            formula_records = {
                tuple(solution[x] for x in (3, 4, 5))
                for solution in formula["solutions"]
            }
            direct_records = {
                tuple(solution[x] for x in (3, 4, 5))
                for solution in direct
            }
            if formula_records != direct_records:
                mismatches.append({
                    "lists": {str(x): sorted(v) for x, v in lists.items()},
                    "h_edges": sorted(h_edges),
                    "formula": sorted(formula_records),
                    "direct": sorted(direct_records),
                })
                if len(mismatches) == 5:
                    return {
                        "systems": systems,
                        "bipartite_systems": bipartite_systems,
                        "mismatches": mismatches,
                    }
    return {
        "systems": systems,
        "bipartite_systems": bipartite_systems,
        "mismatches": mismatches,
    }


def fixed_mixed_core(order):
    graph = [set() for _ in range(order)]
    fixed_edges = {
        (0, 3), (0, 4), (2, 4), (1, 5), (2, 5), (1, 6),
        (3, 5), (3, 6), (4, 6),
    }
    for left, right in fixed_edges:
        graph[left].add(right)
        graph[right].add(left)
    return graph


REQUIRED = parse_states("012 123 124 014 025 015 026")
BANNED = parse_states("023 013 024 125 126 016")


def add_edges(base, edges):
    graph = [set(neighbors) for neighbors in base]
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    return graph


def alpha_at_most_three(graph):
    return not any(
        all(right not in graph[left]
            for left, right in itertools.combinations(state, 2))
        for state in itertools.combinations(range(len(graph)), 4)
    )


def has_dominating_pair(graph):
    return any(
        dominates(graph, pair)
        for pair in itertools.combinations(range(len(graph)), 2)
    )


def exact_realization(graph):
    family = eternal_kernel(graph, 3, BANNED)
    if not REQUIRED <= family:
        return False
    lists = response_lists(graph, family, frozenset({0, 1, 2}))
    expected = {
        3: frozenset({0}), 4: frozenset({0, 2}),
        5: frozenset({1, 2}), 6: frozenset({1}),
    }
    return all(lists[x] == expected[x] for x in expected)


def finite_scans():
    counts8 = {
        "raw_graph_masks": 0,
        "required_states_dominate": 0,
        "required_states_dominate_and_alpha_3": 0,
        "gamma_alpha_3": 0,
        "gamma_alpha_3_and_required_states_dominate": 0,
        "exact_family_realizations": 0,
    }
    unknown8 = [
        (1, 3), (2, 3), (1, 4), (0, 5), (0, 6), (2, 6),
        (0, 7), (1, 7), (2, 7), (3, 7), (6, 7),
    ]
    base8 = fixed_mixed_core(8)
    for mask in range(1 << len(unknown8)):
        graph = add_edges(
            base8,
            [edge for index, edge in enumerate(unknown8) if mask & (1 << index)],
        )
        counts8["raw_graph_masks"] += 1
        required = all(dominates(graph, state) for state in REQUIRED)
        if required:
            counts8["required_states_dominate"] += 1
        a3 = alpha_at_most_three(graph)
        if required and a3:
            counts8["required_states_dominate_and_alpha_3"] += 1
        equality = a3 and not has_dominating_pair(graph)
        if equality:
            counts8["gamma_alpha_3"] += 1
        if equality and required:
            counts8["gamma_alpha_3_and_required_states_dominate"] += 1
            counts8["exact_family_realizations"] += int(exact_realization(graph))

    counts9 = {
        "raw_graph_masks": 1 << 19,
        "masks_after_required_state_neighbor_prefilter": 0,
        "required_states_dominate": 0,
        "required_states_dominate_and_alpha_3": 0,
        "required_states_dominate_and_gamma_alpha_3": 0,
        "exact_family_realizations": 0,
    }
    unknown9 = [
        (1, 3), (2, 3), (1, 4), (0, 5), (0, 6), (2, 6),
        (0, 7), (1, 7), (2, 7), (3, 7), (6, 7),
        (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8),
        (7, 8),
    ]
    base9 = fixed_mixed_core(9)
    for mask in range(1 << len(unknown9)):
        graph = add_edges(
            base9,
            [edge for index, edge in enumerate(unknown9) if mask & (1 << index)],
        )
        new_vertices_prefilter = all(
            graph[new_vertex] & state
            for new_vertex in (7, 8) for state in REQUIRED
        )
        if not new_vertices_prefilter:
            continue
        counts9["masks_after_required_state_neighbor_prefilter"] += 1
        required = all(dominates(graph, state) for state in REQUIRED)
        if not required:
            continue
        counts9["required_states_dominate"] += 1
        if not alpha_at_most_three(graph):
            continue
        counts9["required_states_dominate_and_alpha_3"] += 1
        if has_dominating_pair(graph):
            continue
        counts9["required_states_dominate_and_gamma_alpha_3"] += 1
        counts9["exact_family_realizations"] += int(exact_realization(graph))
    return {"order8": counts8, "order9": counts9}


def main():
    result = {
        "schema": "k3-projection-gluing-hostile-independent-v1",
        "source_hashes": {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (NOTE, PROBE)
        },
        "synthetic_formula_audit": synthetic_formula_audit(),
        "named_cases": named_cases(),
        "finite_scans": finite_scans(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
