#!/usr/bin/env python3
"""Own finite combinatorial controls, stdout only; no native/source access."""
import json


ORDER = ['a', 'b', 'c', 'd', 'cd', 'bd', 'ac']
EDGES = {'cd': ('c', 'd'), 'bd': ('b', 'd'), 'ac': ('a', 'c')}


def directed(matching):
    arrows = {x: [] for x in ORDER}
    for edge, endpoints in EDGES.items():
        for vertex in endpoints:
            if (vertex, edge) in matching:
                arrows[vertex].append(edge)
            else:
                arrows[edge].append(vertex)
    return arrows


def paths(graph, start, end, prefix=()):
    assert start not in prefix
    route = prefix + (start,)
    if start == end:
        return [list(route)]
    found = []
    for target in graph[start]:
        found.extend(paths(graph, target, end, route))
    return found


def rank_table():
    partitions = []
    blocks = []
    for simplex in ORDER:
        if simplex in EDGES:
            u, v = EDGES[simplex]
            touched = [b for b in blocks if u in b or v in b]
            assert len(touched) == 2
            merged = set().union(*touched)
            blocks = [b for b in blocks if b not in touched] + [merged]
        else:
            blocks.append({simplex})
        partitions.append([set(b) for b in blocks])
    bars = [(1, 8), (2, 7), (3, 6), (4, 5)]
    rows = []
    for i in range(1, 8):
        born = set(ORDER[:min(i, 4)])
        row = []
        for j in range(i, 8):
            rank = sum(bool(b & born) for b in partitions[j-1])
            from_bars = sum(b <= i and j < d for b, d in bars)
            assert rank == from_bars
            row.append(rank)
        rows.append(row)
    return rows


def main():
    signed_boundaries = {'cd': [0, 0, -1, 1], 'bd': [0, -1, 0, 1], 'ac': [-1, 0, 1, 0]}
    u4 = signed_boundaries['cd']
    u3 = [x-y for x, y in zip(signed_boundaries['bd'], u4)]
    u2 = [x-y for x, y in zip(signed_boundaries['ac'], u3)]
    assert [u2, u3, u4] == [[-1, 1, 0, 0], [0, -1, 1, 0], [0, 0, -1, 1]]
    integral_pairing = [('d', 'cd'), ('c', 'bd'), ('b', 'ac')]
    matching = {(v, e) for v, e in integral_pairing if v in EDGES[e]}
    assert matching == {('d', 'cd')}
    fixed = directed(matching)
    potential = {'ac': 6, 'bd': 5, 'd': 4, 'cd': 3, 'c': 2, 'b': 1, 'a': 0}
    assert all(potential[u] > potential[v] for u in fixed for v in fixed[u])
    assert paths(fixed, 'ac', 'b') == []
    assert paths(fixed, 'bd', 'c') == [['bd', 'd', 'cd', 'c']]
    assert paths(fixed, 'ac', 'a') == [['ac', 'a']]
    assert paths(fixed, 'ac', 'c') == [['ac', 'c']]
    updated = directed({('d', 'bd'), ('c', 'cd')})
    updated_potential = {'ac': 6, 'c': 5, 'cd': 4, 'd': 3, 'bd': 2, 'b': 1, 'a': 0}
    assert all(updated_potential[u] > updated_potential[v] for u in updated for v in updated[u])
    assert paths(updated, 'ac', 'b') == [['ac', 'c', 'cd', 'd', 'bd', 'b']]
    rows = rank_table()
    expected = [[1,1,1,1,1,1,1], [2,2,2,2,2,1], [3,3,3,2,1], [4,3,2,1], [3,2,1], [2,1], [1]]
    assert rows == expected
    print(json.dumps({'kind': 'own exact integer/set controls; universal all-field basis proof in accompanying text',
                      'native_executions': 0, 'signed_boundary_basis': [u2,u3,u4],
                      'pairing': integral_pairing, 'fixed_graph': fixed, 'fixed_ac_to_b_paths': paths(fixed,'ac','b'),
                      'earlier_bd_to_c_paths': paths(fixed,'bd','c'), 'updated_graph': updated,
                      'updated_ac_to_b_paths': paths(updated,'ac','b'),
                      'rank_invariant_triangular_rows': rows, 'all_assertions_passed': True}, indent=2))


if __name__ == '__main__':
    main()
