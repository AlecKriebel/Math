#!/usr/bin/env python3
"""Exact characteristic-zero checks. Requires Python 3 and SymPy 1.14.

The finite search concerns labelled coefficient supports, not isomorphism classes.
No network or source files are used.
"""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import sympy as s


def end_basis(dims, arrows, matrices):
    offsets = list(itertools.accumulate([0] + [d*d for d in dims]))
    nv = offsets[-1]
    rows = []
    for (u, v), a in zip(arrows, matrices):
        for i in range(dims[v]):
            for j in range(dims[u]):
                row = [0] * nv
                for k in range(dims[v]):
                    row[offsets[v] + i*dims[v] + k] += a[k, j]
                for k in range(dims[u]):
                    row[offsets[u] + k*dims[u] + j] -= a[i, k]
                rows.append(row)
    equations = s.Matrix(rows) if rows else s.zeros(0, nv)
    basis = equations.nullspace()
    blocks = [[s.Matrix(d, d, b[offsets[i]:offsets[i+1]])
               for i, d in enumerate(dims)] for b in basis]
    assert all(all(f[v]*a == a*f[u] for (u,v),a in zip(arrows,matrices))
               for f in blocks)
    return basis, blocks


def algebra_data(dims, arrows, matrices):
    basis, blocks = end_basis(dims, arrows, matrices)
    h = len(basis)
    bmat = s.Matrix.hstack(*basis)
    pivot_rows = list(bmat.T.rref()[1])
    inv = bmat[pivot_rows, :].inv()
    regular = []
    for left in blocks:
        columns = []
        for right in blocks:
            product = s.Matrix([x for a,b in zip(left,right) for x in a*b])
            coords = inv * product[pivot_rows, :]
            assert bmat * coords == product
            columns.append(coords)
        regular.append(s.Matrix.hstack(*columns))
    trace_form = s.Matrix(h, h, lambda i,j: s.trace(regular[i]*regular[j]))
    rank = trace_form.rank()
    return {'endomorphism_dimension': h, 'regular_trace_rank': rank,
            'indecomposable_over_C': rank == 1}


def slots_for(dims, arrows):
    return [(a, i, j) for a,(u,v) in enumerate(arrows)
            for i in range(dims[v]) for j in range(dims[u])]


def tree_support(dims, arrows, support):
    offsets = list(itertools.accumulate([0] + list(dims)))
    n = offsets[-1]
    if len(support) != n-1:
        return False
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for a,i,j in support:
        u,v = arrows[a]
        x,y = find(offsets[u]+j),find(offsets[v]+i)
        if x == y:
            return False
        parent[x] = y
    return len({find(x) for x in range(n)}) == 1


def matrices_for(dims, arrows, support):
    mats = [s.zeros(dims[v],dims[u]) for u,v in arrows]
    for a,i,j in support:
        mats[a][i,j] = 1
    return mats


def support_for(matrices):
    return tuple((a,i,j) for a,m in enumerate(matrices)
                 for i in range(m.rows) for j in range(m.cols) if m[i,j] != 0)


def enumerate_trees(dims, arrows, quotient=False):
    slots = slots_for(dims, arrows)
    total = 0
    types = Counter()
    counts = Counter()
    witnesses = {}
    cache = {}
    permutations = list(itertools.product(*[list(itertools.permutations(range(d)))
                                            for d in dims])) if quotient else []
    for support in itertools.combinations(slots, sum(dims)-1):
        if not tree_support(dims, arrows, support):
            continue
        total += 1
        key = support
        if quotient:
            key = min(tuple(sorted((a,p[arrows[a][1]][i],p[arrows[a][0]][j])
                                   for a,i,j in support)) for p in permutations)
        if key not in cache:
            cache[key] = algebra_data(dims, arrows, matrices_for(dims,arrows,key))
        result = cache[key]
        label = '%d,%d' % (result['endomorphism_dimension'],result['regular_trace_rank'])
        types[label] += 1
        counts[str(result['indecomposable_over_C'])] += 1
        if result['indecomposable_over_C']:
            witnesses.setdefault(label,[list(m) for m in matrices_for(dims,arrows,key)])
    return {'dimensions':dims, 'arrows':arrows, 'labelled_tree_supports':total,
            'algebra_cases_evaluated':len(cache),
            'basis_permutation_quotient_used':quotient,
            'endomorphism_dimension_trace_rank_histogram':dict(sorted(types.items())),
            'indecomposable_counts':dict(counts), 'witnesses':witnesses}


def independent_k2_check():
    """Second exact test for 2x2 pencils, independent of the trace form."""
    dims, arrows = [2,2], [(0,1),(0,1)]
    histogram = Counter()
    for support in itertools.combinations(slots_for(dims,arrows), 3):
        if not tree_support(dims,arrows,support):
            continue
        a,b = matrices_for(dims,arrows,support)
        for t in (0,1,2):
            p = a + t*b
            if p.det() != 0:
                c = p.inv()*b
                break
        else:
            raise AssertionError('No invertible pencil at 0,1,2')
        scalar = c == c[0,0]*s.eye(2)
        disc = s.trace(c)**2-4*c.det()
        indecomp = not scalar and disc == 0
        expected_end_dim = 4 if scalar else 2
        direct = algebra_data(dims,arrows,[a,b])
        assert direct['endomorphism_dimension'] == expected_end_dim
        assert direct['indecomposable_over_C'] == indecomp
        histogram[str(indecomp)] += 1
    assert histogram == {'False':24,'True':8}
    return dict(histogram)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--extended-control', action='store_true')
    args = parser.parse_args()
    k2_arrows = [(0,1),(0,1)]
    i2,j2 = s.eye(2),s.Matrix([[0,1],[0,0]])
    connected_decomposable = [s.Matrix([[1,1],[1,0]]),s.zeros(2)]
    controls = {
      'kronecker_local':algebra_data([2,2],k2_arrows,[i2,j2]),
      'connected_tree_but_decomposable':algebra_data([2,2],k2_arrows,connected_decomposable),
      'degeneration_t0':algebra_data([2,2],k2_arrows,[i2,s.zeros(2)]),
      'degeneration_t1':algebra_data([2,2],k2_arrows,[i2,j2]),
      'degeneration_t2':algebra_data([2,2],k2_arrows,[i2,2*j2]),
      'one_vertex_simple':algebra_data([1],[],[]),
      'one_vertex_double':algebra_data([2],[],[]),
      'D4_tree':algebra_data([2,1,1,1],[(1,0),(2,0),(3,0)],
                           [s.Matrix([1,0]),s.Matrix([0,1]),s.Matrix([1,1])]),
      'A2_nonroot':algebra_data([2,1],[(0,1)],[s.Matrix([[1,1]])]),
    }
    assert tree_support([2,2],k2_arrows,support_for(connected_decomposable))
    assert tree_support([2,2],k2_arrows,support_for([i2,j2]))
    assert controls['kronecker_local'] == {'endomorphism_dimension':2,'regular_trace_rank':1,'indecomposable_over_C':True}
    assert controls['connected_tree_but_decomposable']['regular_trace_rank'] == 4
    assert controls['D4_tree']['endomorphism_dimension'] == 1
    assert controls['one_vertex_simple']['indecomposable_over_C']
    assert controls['one_vertex_double']['regular_trace_rank'] == 4
    assert not controls['A2_nonroot']['indecomposable_over_C']
    result = {'field':'C; exact rational matrices', 'sympy_version':s.__version__,
              'controls':controls, 'independent_K2_pencil_test':independent_k2_check(), 'enumerations':{
        'K2_2_2': enumerate_trees([2,2],k2_arrows),
        'D4_2_1_1_1':enumerate_trees([2,1,1,1],[(1,0),(2,0),(3,0)]),
        'A2_2_1_nonroot':enumerate_trees([2,1],[(0,1)])}}
    assert result['enumerations']['K2_2_2']['labelled_tree_supports'] == 32
    assert result['enumerations']['D4_2_1_1_1']['labelled_tree_supports'] == 12
    if args.extended_control:
        result['enumerations']['affine_D4_3_2_2_1_1'] = enumerate_trees(
             [3,2,2,1,1],[(1,0),(2,0),(3,0),(4,0)],quotient=True)
    text = json.dumps(result,indent=2,default=int)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
