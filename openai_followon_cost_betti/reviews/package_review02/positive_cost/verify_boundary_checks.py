#!/usr/bin/env python3
"""Exact arithmetic and the stated J/conjugate intersection boundary check.

Run with Python 3; this uses only its standard library. It does not write files.
The intersection calculation constructs the explicit already-folded core graph
from the displayed generators b_i and w, then explores the fibre component.
"""

import json


def core_graph():
    graph = {v: {} for v in range(199)}

    def edge(source, target, generator):
        positive = (generator, 1)
        negative = (generator, -1)
        assert positive not in graph[source]
        assert negative not in graph[target]
        graph[source][positive] = target
        graph[target][negative] = source

    for i in range(99):
        edge(2 * i, 2 * i + 1, "a")
    edge(198, 0, "a")
    for i in range(1, 100):
        edge(0, 0, f"b_{i}")
        edge(2 * i - 1, 2 * i, f"b_{i}")
    return graph


def intersection_component(graph):
    initial = (0, 1)
    seen = {initial}
    pending = [initial]
    edges = set()
    while pending:
        source = pending.pop()
        left, right = source
        for generator, sign in graph[left].keys() & graph[right].keys():
            target = (graph[left][generator, sign], graph[right][generator, sign])
            # Canonical orientation of the labelled geometric edge.
            edge = (generator, source, target) if sign == 1 else (generator, target, source)
            edges.add(edge)
            if target not in seen:
                seen.add(target)
                pending.append(target)
    return seen, edges


def main():
    lhs = 2 * 3**97 * 96**4
    rhs = 2**183
    assert lhs < rhs
    assert 2**61 > 200
    graph = core_graph()
    core_edge_count = sum(len(outgoing) for outgoing in graph.values()) // 2
    assert core_edge_count == 298
    vertices, edges = intersection_component(graph)
    expected = {(1, 3), (0, 2), (0, 1), (198, 0), (197, 0), (196, 198)}
    assert vertices == expected
    assert len(edges) == 5
    assert len(edges) - len(vertices) + 1 == 0
    print(json.dumps({
        "constant_certificate": {
            "2_times_3_pow_97_times_96_pow_4": str(lhs),
            "2_pow_183": str(rhs),
            "lhs_strictly_less_than_rhs": lhs < rhs,
            "2_pow_61": str(2**61),
            "eta_denominator": str(100 * 2**61),
        },
        "core_graph": {"vertices": len(graph), "edges": core_edge_count},
        "fibre_component_at_0_1": {
            "vertices": sorted(vertices),
            "positive_labelled_edges": sorted(edges),
            "edge_count": len(edges),
            "fundamental_group_rank": len(edges) - len(vertices) + 1,
            "connected_by_construction": True,
        },
    }, indent=2))


if __name__ == "__main__":
    main()
