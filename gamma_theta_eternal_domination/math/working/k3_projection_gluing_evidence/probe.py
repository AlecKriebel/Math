#!/usr/bin/env python3
"""Light exact probes for the k=3 frozen-projection gluing attack.

The principal search enumerates all eight-vertex extensions of the displayed
mixed-P4 pattern by the middle-pair domination witness w.  It asks whether
there is an eternal family of triples with the *exact* four response lists at
S after all six forbidden one-swap states are removed.

This is intentionally small: 2^11 labelled graphs and ordinary Python sets.
"""

from __future__ import annotations

import itertools
import json
from collections import deque


def pairs(vertices):
    return itertools.combinations(vertices, 2)


def dominates(state, vertices, edges):
    covered = set(state)
    for u in state:
        for v in vertices:
            if tuple(sorted((u, v))) in edges:
                covered.add(v)
    return covered == set(vertices)


def independence_number(vertices, edges):
    for size in range(len(vertices), 0, -1):
        for subset in itertools.combinations(vertices, size):
            if all(tuple(sorted(edge)) not in edges for edge in pairs(subset)):
                return size
    return 0


def domination_number(vertices, edges):
    for size in range(1, len(vertices) + 1):
        for subset in itertools.combinations(vertices, size):
            if dominates(subset, vertices, edges):
                return size
    raise AssertionError("finite graph has no dominating set")


def chromatic_number_complement(vertices, edges):
    h_neighbors = {
        u: {
            v
            for v in vertices
            if v != u and tuple(sorted((u, v))) not in edges
        }
        for u in vertices
    }
    order = sorted(vertices, key=lambda u: -len(h_neighbors[u]))
    for colors in range(1, len(vertices) + 1):
        assignment = {}

        def visit(index):
            if index == len(order):
                return True
            u = order[index]
            forbidden = {assignment[v] for v in h_neighbors[u] if v in assignment}
            for color in range(colors):
                if color not in forbidden:
                    assignment[u] = color
                    if visit(index + 1):
                        return True
                    del assignment[u]
            return False

        if visit(0):
            return colors
    raise AssertionError("unreachable")


def greatest_family(vertices, edges, forbidden):
    states = {
        frozenset(state)
        for state in itertools.combinations(vertices, 3)
        if frozenset(state) not in forbidden and dominates(state, vertices, edges)
    }
    changed = True
    while changed:
        changed = False
        remove = set()
        for state in states:
            for attack in set(vertices) - set(state):
                if not any(
                    tuple(sorted((guard, attack))) in edges
                    and frozenset((set(state) - {guard}) | {attack}) in states
                    for guard in state
                ):
                    remove.add(state)
                    break
        if remove:
            states -= remove
            changed = True
    return states


def response_lists(reference, vertices, edges, family):
    out = {}
    for x in set(vertices) - set(reference):
        out[x] = sorted(
            u
            for u in reference
            if tuple(sorted((u, x))) in edges
            and frozenset((set(reference) - {u}) | {x}) in family
        )
    return out


def verify_eternal_family(vertices, edges, family):
    obligations = 0
    for state in family:
        if not dominates(state, vertices, edges):
            return False, obligations
        for attack in set(vertices) - set(state):
            obligations += 1
            if not any(
                tuple(sorted((guard, attack))) in edges
                and frozenset((set(state) - {guard}) | {attack}) in family
                for guard in state
            ):
                return False, obligations
    return True, obligations


def complement_edges(vertices, edges):
    return {
        tuple(sorted((u, v)))
        for u, v in pairs(vertices)
        if tuple(sorted((u, v))) not in edges
    }


def decode_graph6(record):
    data = record.encode("ascii")
    if not data or not 63 <= data[0] <= 125:
        raise ValueError("only short graph6 records are supported")
    order = data[0] - 63
    bits = []
    for byte in data[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = set()
    position = 0
    for high in range(1, order):
        for low in range(high):
            if bits[position]:
                edges.add((low, high))
            position += 1
    return tuple(range(order)), edges


def is_bipartite(subset, h_edges):
    neighbors = {u: set() for u in subset}
    for u, v in h_edges:
        if u in neighbors and v in neighbors:
            neighbors[u].add(v)
            neighbors[v].add(u)
    parity = {}
    components = []
    for root in subset:
        if root in parity:
            continue
        parity[root] = 0
        component = []
        queue = deque([root])
        while queue:
            u = queue.popleft()
            component.append(u)
            for v in neighbors[u]:
                if v not in parity:
                    parity[v] = parity[u] ^ 1
                    queue.append(v)
                elif parity[v] == parity[u]:
                    return False, {}, []
        components.append(sorted(component))
    return True, parity, components


def analyze_projection_gluing(graph6, family, reference):
    vertices, edges = decode_graph6(graph6)
    reference = frozenset(reference)
    colors = sorted(reference)
    lists = response_lists(reference, vertices, edges, family)
    family_valid, attack_obligations = verify_eternal_family(
        vertices, edges, family
    )
    h_edges = complement_edges(vertices, edges)
    projections = {}
    component_data = {}
    variables = []
    for frozen in colors:
        remaining = sorted(reference - {frozen})
        omitted = {
            x
            for x in set(vertices) - set(reference)
            if frozen not in lists[x]
        }
        projected = set(remaining) | omitted
        ok, parity, components = is_bipartite(projected, h_edges)
        assert ok
        anchor_component = next(
            index
            for index, component in enumerate(components)
            if remaining[0] in component
        )
        assert remaining[1] in components[anchor_component]
        if parity[remaining[0]] != 0:
            for x in components[anchor_component]:
                parity[x] ^= 1
        assert parity[remaining[0]] == 0
        assert parity[remaining[1]] == 1
        for index, component in enumerate(components):
            variable = None
            if index != anchor_component:
                variable = len(variables)
                variables.append(
                    {
                        "id": variable,
                        "frozen": frozen,
                        "component": component,
                    }
                )
            for x in component:
                component_data[(frozen, x)] = {
                    "component_index": index,
                    "variable": variable,
                    "parity": parity[x],
                    "remaining": remaining,
                }
        projections[str(frozen)] = {
            "vertices": sorted(projected),
            "components": components,
            "anchor_component": anchor_component,
            "parity": {str(x): parity[x] for x in sorted(projected)},
        }

    units = []
    internal_contradictions = []
    for x, response in lists.items():
        if len(response) != 1:
            continue
        demanded = response[0]
        for frozen in sorted(reference - {demanded}):
            data = component_data[(frozen, x)]
            target_index = data["remaining"].index(demanded)
            required_flip = data["parity"] ^ target_index
            if data["variable"] is None:
                if required_flip:
                    internal_contradictions.append(
                        {
                            "vertex": x,
                            "frozen": frozen,
                            "demanded_color": demanded,
                            "reason": "anchor component has the opposite parity",
                        }
                    )
            else:
                units.append(
                    {
                        "variable": data["variable"],
                        "value": required_flip,
                        "vertex": x,
                        "frozen": frozen,
                        "demanded_color": demanded,
                    }
                )

    def two_list_choice(x, assignment):
        response = lists[x]
        assert len(response) == 2
        frozen = next(iter(reference - set(response)))
        data = component_data[(frozen, x)]
        flip = (
            False
            if data["variable"] is None
            else assignment[data["variable"]]
        )
        return data["remaining"][data["parity"] ^ int(flip)]

    cross_clauses = []
    outside = sorted(set(vertices) - set(reference))
    for x, y in itertools.combinations(outside, 2):
        if tuple(sorted((x, y))) not in h_edges:
            continue
        if len(lists[x]) == len(lists[y]) == 2:
            omitted_x = next(iter(reference - set(lists[x])))
            omitted_y = next(iter(reference - set(lists[y])))
            if omitted_x != omitted_y:
                shared = next(iter(set(lists[x]) & set(lists[y])))
                cross_clauses.append(
                    {
                        "edge": [x, y],
                        "shared_color": shared,
                        "x": x,
                        "y": y,
                    }
                )

    solutions = []
    for bits in itertools.product((False, True), repeat=len(variables)):
        if internal_contradictions:
            continue
        if any(bits[unit["variable"]] != bool(unit["value"]) for unit in units):
            continue
        visible_coloring = {}
        for x in outside:
            if len(lists[x]) == 1:
                visible_coloring[x] = lists[x][0]
            elif len(lists[x]) == 2:
                visible_coloring[x] = two_list_choice(x, bits)
        if any(
            visible_coloring[clause["x"]]
            == visible_coloring[clause["y"]]
            == clause["shared_color"]
            for clause in cross_clauses
        ):
            continue
        assert all(
            visible_coloring.get(x) != visible_coloring.get(y)
            for x, y in h_edges
            if x in visible_coloring and y in visible_coloring
        )
        solutions.append(
            {
                "orientation": [int(bit) for bit in bits],
                "visible_coloring": {
                    str(x): visible_coloring[x] for x in sorted(visible_coloring)
                },
            }
        )

    direct_colorings = []
    list_order = sorted(outside, key=lambda x: (len(lists[x]), x))

    def extend_coloring(index, coloring):
        if index == len(list_order):
            direct_colorings.append({str(x): coloring[x] for x in sorted(coloring)})
            return
        x = list_order[index]
        h_neighbors = {
            y
            for y in coloring
            if tuple(sorted((x, y))) in h_edges
        }
        for color in lists[x]:
            if color not in {coloring[y] for y in h_neighbors}:
                coloring[x] = color
                extend_coloring(index + 1, coloring)
                del coloring[x]

    extend_coloring(0, {})
    return {
        "graph6": graph6,
        "reference": sorted(reference),
        "family_size": len(family),
        "family_valid": family_valid,
        "attack_obligations_checked": attack_obligations,
        "lists": {str(x): lists[x] for x in sorted(lists)},
        "full_list_vertices": [
            x for x in outside if len(lists[x]) == len(reference)
        ],
        "projections": projections,
        "orientation_variables": variables,
        "singleton_unit_constraints": units,
        "projection_internal_contradictions": internal_contradictions,
        "cross_projection_clauses": cross_clauses,
        "projection_gluing_solution_count": len(solutions),
        "projection_gluing_solutions": solutions[:10],
        "direct_global_list_coloring_count": len(direct_colorings),
        "direct_global_list_colorings": direct_colorings[:10],
    }


def named_stress_tests():
    cases = []

    vertices, edges = decode_graph6("FCZbg")
    fcz_family_masks = bit_greatest_family(len(vertices), edges, set())
    fcz_family = {
        frozenset(u for u in vertices if mask & (1 << u))
        for mask in fcz_family_masks
    }
    cases.append(
        (
            "FCZbg greatest family",
            analyze_projection_gluing("FCZbg", fcz_family, {0, 4, 6}),
        )
    )

    # Exact full-closure countermodel for the dual deficient-pair extension
    # of the mixed P4.  It deliberately fails gamma=3.
    dual_vertices, dual_edges = decode_graph6("HDzruf]")
    dual_forbidden = {
        frozenset(state)
        for state in (
            (0, 2, 3),
            (0, 1, 3),
            (0, 2, 4),
            (1, 2, 5),
            (1, 2, 6),
            (0, 1, 6),
        )
    }
    dual_family = greatest_family(
        dual_vertices, dual_edges, dual_forbidden
    )
    dual_analysis = analyze_projection_gluing(
        "HDzruf]", dual_family, {0, 1, 2}
    )
    dual_analysis["parameters"] = {
        "gamma": domination_number(dual_vertices, dual_edges),
        "alpha": independence_number(dual_vertices, dual_edges),
        "gamma_infinity": 3,
        "theta": chromatic_number_complement(dual_vertices, dual_edges),
    }
    dual_analysis["role"] = (
        "full-closure W/Y countermodel; fails only the target gamma=3 "
        "among the displayed parameter equalities"
    )
    cases.append(("HDzruf] dual deficient-pair family", dual_analysis))

    fcx_family = {
        frozenset(state)
        for state in (
            (0, 1, 2),
            (0, 1, 4),
            (0, 1, 6),
            (0, 2, 4),
            (0, 2, 5),
            (0, 2, 6),
            (0, 4, 5),
            (0, 5, 6),
            (1, 2, 3),
            (1, 3, 4),
            (1, 3, 6),
            (2, 3, 4),
            (2, 3, 5),
            (2, 3, 6),
            (3, 4, 5),
            (3, 5, 6),
        )
    }
    cases.append(
        (
            "FCXfO specified 16-state family",
            analyze_projection_gluing("FCXfO", fcx_family, {0, 1, 2}),
        )
    )

    fdz_family = {
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
    }
    cases.append(
        (
            "FDzro specified 21-state family",
            analyze_projection_gluing("FDzro", fdz_family, {0, 1, 2}),
        )
    )
    vertices, edges = decode_graph6("FDzro")
    fdz_greatest_masks = bit_greatest_family(len(vertices), edges, set())
    fdz_greatest = {
        frozenset(u for u in vertices if mask & (1 << u))
        for mask in fdz_greatest_masks
    }
    cases.append(
        (
            "FDzro greatest family",
            analyze_projection_gluing("FDzro", fdz_greatest, {0, 1, 2}),
        )
    )

    vertices, edges = decode_graph6("FCpbO")
    fcp_family_masks = bit_greatest_family(len(vertices), edges, set())
    fcp_family = {
        frozenset(u for u in vertices if mask & (1 << u))
        for mask in fcp_family_masks
    }
    cases.append(
        (
            "FCpbO greatest family",
            analyze_projection_gluing("FCpbO", fcp_family, {0, 5, 6}),
        )
    )
    return {name: data for name, data in cases}


def enumerate_mixed_p4_witness_extensions():
    vertices = tuple(range(8))
    s = frozenset({0, 1, 2})
    required = {
        s,
        frozenset({1, 2, 3}),
        frozenset({1, 2, 4}),
        frozenset({0, 1, 4}),
        frozenset({0, 2, 5}),
        frozenset({0, 1, 5}),
        frozenset({0, 2, 6}),
    }
    forbidden = {
        frozenset({0, 2, 3}),
        frozenset({0, 1, 3}),
        frozenset({0, 2, 4}),
        frozenset({1, 2, 5}),
        frozenset({1, 2, 6}),
        frozenset({0, 1, 6}),
    }

    fixed_edges = {
        (0, 3),
        (0, 4),
        (2, 4),
        (1, 5),
        (2, 5),
        (1, 6),
        (3, 5),
        (3, 6),
        (4, 6),
    }
    fixed_nonedges = {
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
        (4, 5),
        (5, 6),
        (4, 7),
        (5, 7),
    }
    unknown = [
        (1, 3),
        (2, 3),
        (1, 4),
        (0, 5),
        (0, 6),
        (2, 6),
        (0, 7),
        (1, 7),
        (2, 7),
        (3, 7),
        (6, 7),
    ]
    assert fixed_edges.isdisjoint(fixed_nonedges)
    assert len(fixed_edges | fixed_nonedges | set(unknown)) == 28

    counts = {
        "graphs": 0,
        "required_states_dominate_without_parameters": 0,
        "required_states_dominate_and_alpha_3": 0,
        "gamma_alpha_3": 0,
        "required_states_dominate": 0,
        "exact_family_realizations": 0,
    }
    witnesses = []
    for mask in range(1 << len(unknown)):
        counts["graphs"] += 1
        edges = set(fixed_edges)
        edges.update(unknown[i] for i in range(len(unknown)) if mask & (1 << i))
        required_dominate = all(dominates(state, vertices, edges) for state in required)
        if required_dominate:
            counts["required_states_dominate_without_parameters"] += 1
        alpha = independence_number(vertices, edges)
        if required_dominate and alpha == 3:
            counts["required_states_dominate_and_alpha_3"] += 1
        if alpha != 3:
            continue
        if domination_number(vertices, edges) != 3:
            continue
        counts["gamma_alpha_3"] += 1
        if not required_dominate:
            continue
        counts["required_states_dominate"] += 1
        family = greatest_family(vertices, edges, forbidden)
        if not required <= family:
            continue
        lists = response_lists(s, vertices, edges, family)
        expected = {3: [0], 4: [0, 2], 5: [1, 2], 6: [1]}
        if any(lists[x] != expected[x] for x in expected):
            continue
        counts["exact_family_realizations"] += 1
        h_edges = complement_edges(vertices, edges)
        projections = {}
        for frozen in sorted(s):
            omission = [x for x in vertices if x not in s and frozen not in lists[x]]
            projected = sorted((set(s) - {frozen}) | set(omission))
            ok, parity, components = is_bipartite(projected, h_edges)
            projections[str(frozen)] = {
                "vertices": projected,
                "bipartite": ok,
                "parity": {str(x): parity[x] for x in projected} if ok else {},
                "components": components,
            }
        witnesses.append(
            {
                "mask": mask,
                "edges": sorted([list(edge) for edge in edges]),
                "family_size": len(family),
                "family": sorted([sorted(state) for state in family]),
                "lists": {str(k): v for k, v in lists.items()},
                "theta": chromatic_number_complement(vertices, edges),
                "projections": projections,
            }
        )
    return counts, witnesses


def bit_adjacency(order, edges):
    adjacency = [1 << u for u in range(order)]
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return adjacency


def bit_dominates(state_mask, adjacency, full_mask):
    covered = 0
    while state_mask:
        low = state_mask & -state_mask
        covered |= adjacency[low.bit_length() - 1]
        state_mask -= low
    return covered == full_mask


def bit_alpha_at_most_three(order, edges):
    edge_set = set(edges)
    return not any(
        all(tuple(sorted(edge)) not in edge_set for edge in pairs(subset))
        for subset in itertools.combinations(range(order), 4)
    )


def bit_greatest_family(order, edges, forbidden):
    full_mask = (1 << order) - 1
    adjacency = bit_adjacency(order, edges)
    states = {
        sum(1 << u for u in state)
        for state in itertools.combinations(range(order), 3)
        if frozenset(state) not in forbidden
        and bit_dominates(sum(1 << u for u in state), adjacency, full_mask)
    }
    changed = True
    while changed:
        changed = False
        remove = set()
        for state in states:
            attacks = full_mask ^ state
            while attacks:
                attack_bit = attacks & -attacks
                attack = attack_bit.bit_length() - 1
                guards = state
                legal = False
                while guards:
                    guard_bit = guards & -guards
                    guard = guard_bit.bit_length() - 1
                    if adjacency[guard] & attack_bit:
                        successor = (state ^ guard_bit) | attack_bit
                        if successor in states:
                            legal = True
                            break
                    guards -= guard_bit
                if not legal:
                    remove.add(state)
                    break
                attacks -= attack_bit
        if remove:
            states -= remove
            changed = True
    return states


def enumerate_order_nine_extensions():
    """Add one arbitrary extra vertex beyond the designated witness w."""

    order = 9
    vertices = tuple(range(order))
    full_mask = (1 << order) - 1
    s = frozenset({0, 1, 2})
    required = {
        s,
        frozenset({1, 2, 3}),
        frozenset({1, 2, 4}),
        frozenset({0, 1, 4}),
        frozenset({0, 2, 5}),
        frozenset({0, 1, 5}),
        frozenset({0, 2, 6}),
    }
    required_masks = [sum(1 << u for u in state) for state in required]
    forbidden = {
        frozenset({0, 2, 3}),
        frozenset({0, 1, 3}),
        frozenset({0, 2, 4}),
        frozenset({1, 2, 5}),
        frozenset({1, 2, 6}),
        frozenset({0, 1, 6}),
    }
    fixed_edges = {
        (0, 3),
        (0, 4),
        (2, 4),
        (1, 5),
        (2, 5),
        (1, 6),
        (3, 5),
        (3, 6),
        (4, 6),
    }
    base_unknown = [(1, 3), (2, 3), (1, 4), (0, 5), (0, 6), (2, 6)]
    witness_choices = []
    for mask in range(1 << 5):
        neighbors = {
            v for i, v in enumerate((0, 1, 2, 3, 6)) if mask & (1 << i)
        }
        if all(neighbors & set(state) for state in required):
            witness_choices.append(neighbors)
    extra_choices = []
    for mask in range(1 << 7):
        neighbors = {v for v in range(7) if mask & (1 << v)}
        if all(neighbors & set(state) for state in required):
            extra_choices.append(neighbors)

    counts = {
        "graphs_after_required_state_neighbor_prefilter": 0,
        "required_states_dominate": 0,
        "alpha_3": 0,
        "gamma_alpha_3": 0,
        "exact_family_realizations": 0,
    }
    witnesses = []
    for base_mask in range(1 << len(base_unknown)):
        base_edges = set(fixed_edges)
        base_edges.update(
            base_unknown[i]
            for i in range(len(base_unknown))
            if base_mask & (1 << i)
        )
        for w_neighbors in witness_choices:
            with_w = set(base_edges)
            with_w.update(tuple(sorted((7, v))) for v in w_neighbors)
            # The designated witness is missed by x1 and x2.
            for z_neighbors in extra_choices:
                with_z = set(with_w)
                with_z.update(tuple(sorted((8, v))) for v in z_neighbors)
                for wz in (False, True):
                    counts["graphs_after_required_state_neighbor_prefilter"] += 1
                    edges = set(with_z)
                    if wz:
                        edges.add((7, 8))
                    adjacency = bit_adjacency(order, edges)
                    if not all(
                        bit_dominates(state, adjacency, full_mask)
                        for state in required_masks
                    ):
                        continue
                    counts["required_states_dominate"] += 1
                    if not bit_alpha_at_most_three(order, edges):
                        continue
                    counts["alpha_3"] += 1
                    if any(
                        bit_dominates((1 << u) | (1 << v), adjacency, full_mask)
                        for u, v in pairs(vertices)
                    ):
                        continue
                    counts["gamma_alpha_3"] += 1
                    family_masks = bit_greatest_family(order, edges, forbidden)
                    if not all(mask in family_masks for mask in required_masks):
                        continue
                    family = {
                        frozenset(
                            u for u in vertices if state_mask & (1 << u)
                        )
                        for state_mask in family_masks
                    }
                    lists = response_lists(s, vertices, edges, family)
                    expected = {
                        3: [0],
                        4: [0, 2],
                        5: [1, 2],
                        6: [1],
                    }
                    if any(lists[x] != expected[x] for x in expected):
                        continue
                    counts["exact_family_realizations"] += 1
                    if len(witnesses) < 10:
                        witnesses.append(
                            {
                                "base_mask": base_mask,
                                "w_neighbors": sorted(w_neighbors),
                                "z_neighbors": sorted(z_neighbors),
                                "wz": wz,
                                "edges": sorted([list(edge) for edge in edges]),
                                "family_size": len(family),
                                "family": sorted(
                                    [sorted(state) for state in family]
                                ),
                                "lists": {str(k): v for k, v in lists.items()},
                                "theta": chromatic_number_complement(
                                    vertices, edges
                                ),
                            }
                        )
    return counts, witnesses


def main():
    counts8, witnesses8 = enumerate_mixed_p4_witness_extensions()
    counts9, witnesses9 = enumerate_order_nine_extensions()
    stress_tests = named_stress_tests()
    print(
        json.dumps(
            {
                "schema": "k3-projection-gluing-probe-v1",
                "order8": {
                    "search": "all 2^11 mixed-P4 witness extensions",
                    "counts": counts8,
                    "witnesses": witnesses8,
                },
                "order9": {
                    "search": (
                        "all labelled extensions by one designated middle-pair "
                        "witness and one arbitrary extra vertex after exact "
                        "required-state neighbor prefiltering"
                    ),
                    "counts": counts9,
                    "witnesses": witnesses9,
                },
                "named_stress_tests": stress_tests,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
