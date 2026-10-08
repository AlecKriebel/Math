#!/usr/bin/env python3
"""Independent half-edge cube and exact field homology for positive 2-braids.

This implementation does not import the candidate verifier.  It uses a graph
on four half-edges per crossing, graph traversal rather than union-find, and
Fraction/bitset row elimination.  SymPy is used only for rational nullspaces
when directly computing the connecting map, never to supply knot data.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
import sympy as sp


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank_q(rows, cols):
    basis = {}
    for original in rows:
        row = [Fraction(x) for x in original]
        for pivot in sorted(basis):
            if row[pivot]:
                coefficient = row[pivot]
                row = [x - coefficient*y for x, y in zip(row, basis[pivot])]
        pivot = next((j for j in range(cols) if row[j]), None)
        if pivot is not None:
            coefficient = row[pivot]
            basis[pivot] = [x/coefficient for x in row]
    return len(basis)


def rank_f2(rows, cols):
    basis = {}
    for row in rows:
        v = sum((int(x) & 1) << j for j, x in enumerate(row))
        while v:
            p = v.bit_length()-1
            if p in basis:
                v ^= basis[p]
            else:
                basis[p] = v
                break
    return len(basis)


def smoothing_components(n, state):
    graph = {v: set() for v in range(4*n)}

    def edge(a, b):
        graph[a].add(b)
        graph[b].add(a)

    for k in range(n):
        # Half-edges are input-left, input-right, output-left, output-right.
        edge(4*k+2, 4*((k+1) % n))
        edge(4*k+3, 4*((k+1) % n)+1)
        if (state >> k) & 1:
            edge(4*k, 4*k+1)
            edge(4*k+2, 4*k+3)
        else:
            edge(4*k, 4*k+2)
            edge(4*k+1, 4*k+3)
    remaining = set(graph)
    components = []
    while remaining:
        stack, component = [min(remaining)], set()
        while stack:
            v = stack.pop()
            if v in component:
                continue
            component.add(v)
            stack.extend(graph[v]-component)
        remaining -= component
        components.append(frozenset(component))
    return tuple(components)


def cube(n):
    components = {s: smoothing_components(n, s) for s in range(1 << n)}
    basis = defaultdict(list)
    grading, marked = {}, {}
    for state, circles in components.items():
        for labels in product((0, 1), repeat=len(circles)):
            generator = (state, labels)
            i = state.bit_count()
            q = n+i+len(circles)-2*sum(labels)
            basis[i, q].append(generator)
            grading[generator] = i, q
            marked[generator] = labels[next(j for j, c in enumerate(circles) if 0 in c)]
    indices = {degree: {g: j for j, g in enumerate(gs)} for degree, gs in basis.items()}
    matrices = {}
    for (i, q), generators in basis.items():
        rows = [[0]*len(generators) for _ in basis.get((i+1, q), [])]
        for col, (state, labels) in enumerate(generators):
            old = components[state]
            label_by_circle = dict(zip(old, labels))
            for crossing in range(n):
                if (state >> crossing) & 1:
                    continue
                target = state | (1 << crossing)
                new = components[target]
                common = set(old) & set(new)
                changed_old = [c for c in old if c not in common]
                changed_new = [c for c in new if c not in common]
                output_labels = []
                if len(changed_old) == 2 and len(changed_new) == 1:
                    power = sum(label_by_circle[c] for c in changed_old)
                    if power <= 1:
                        output_labels.append({changed_new[0]: power})
                elif len(changed_old) == 1 and len(changed_new) == 2:
                    power = label_by_circle[changed_old[0]]
                    for a, b in ([(1, 1)] if power else [(0, 1), (1, 0)]):
                        output_labels.append(dict(zip(changed_new, (a, b))))
                else:
                    raise RuntimeError('Edge must be exactly one merge or split')
                sign = -1 if (state & ((1 << crossing)-1)).bit_count() % 2 else 1
                for changes in output_labels:
                    all_labels = {c: label_by_circle[c] for c in common}
                    all_labels.update(changes)
                    target_generator = target, tuple(all_labels[c] for c in new)
                    check(grading[target_generator] == (i+1, q), 'Wrong differential grading')
                    row = indices[i+1, q][target_generator]
                    rows[row][col] += sign
        matrices[i, q] = rows
    for (i, q), rows in matrices.items():
        following = matrices.get((i+1, q), [])
        for row in following:
            for col in range(len(basis[i, q])):
                check(sum(row[k]*rows[k][col] for k in range(len(rows))) == 0,
                      'Integer differential did not square to zero')

    def submatrix(degree, source_kind=None, target_kind=None):
        i, q = degree
        source = [j for j, g in enumerate(basis.get(degree, []))
                  if source_kind is None or marked[g] == source_kind]
        target = [j for j, g in enumerate(basis.get((i+1, q), []))
                  if target_kind is None or marked[g] == target_kind]
        original = matrices.get(degree, [])
        return [[original[a][b] for b in source] for a in target], len(source)

    def homology(kind):
        ranks, counts = {}, {}
        for degree, generators in basis.items():
            rows, count = submatrix(degree, kind, kind)
            counts[degree] = count
            ranks[degree] = rank_q(rows, count), rank_f2(rows, count)
        result = {}
        for (i, q), count in sorted(counts.items()):
            outgoing, incoming = ranks[i, q], ranks.get((i-1, q), (0, 0))
            rq, r2 = [count-outgoing[j]-incoming[j] for j in (0, 1)]
            check(rq >= 0 and r2 >= 0, 'Negative homology dimension')
            if rq or r2:
                result[f'{i},{q + int(kind == 1)}'] = {'Q': rq, 'F2': r2}
        return {'Q': sum(x['Q'] for x in result.values()),
                'F2': sum(x['F2'] for x in result.values()), 'bigraded': result}

    # A direct connecting-map computation, independent of any dimension identity.
    connecting_ranks = {}
    for (i, q), generators in sorted(basis.items()):
        d0, source_count = submatrix((i, q), 0, 0)
        cross, _ = submatrix((i, q), 0, 1)
        sub_d, boundary_count = submatrix((i, q), 1, 1)
        target_count = sum(marked[g] == 1 for g in basis.get((i+1, q), []))
        if not source_count or not target_count:
            continue
        quotient_matrix = sp.Matrix(len(d0), source_count, sum(d0, []))
        null_basis = quotient_matrix.nullspace()
        cycles = sp.Matrix.hstack(*null_basis) if null_basis else sp.zeros(source_count, 0)
        cross_matrix = sp.Matrix(target_count, source_count, sum(cross, []))
        images = cross_matrix*cycles
        boundaries = sp.Matrix(target_count, boundary_count, sum(sub_d, []))
        combined = boundaries.row_join(images)
        value = rank_q(combined.tolist(), combined.cols)-rank_q(boundaries.tolist(), boundaries.cols)
        if value:
            connecting_ranks[f'{i},{q-1}->{i+1},{q+1}'] = value
    return {'unreduced': homology(None), 'reduced': homology(1),
            'direct_connecting_rank': sum(connecting_ranks.values()),
            'direct_connecting_bigradings': connecting_ranks,
            'integer_d_squared_zero': True,
            'smoothing_states': len(components),
            'unreduced_chain_generators': sum(map(len, basis.values()))}


def main():
    result = {'implementation': 'Independent half-edge graph, Fraction and bitset elimination',
              'knots': {f'T(2,{n})': cube(n) for n in (1, 3, 5)}}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
