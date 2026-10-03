#!/usr/bin/env python3
"""Exact, dependency-free finite-rooted-model certificate checker.

A core vertex i has spoke color spokes[i]. Off-diagonal edges[i][j]
is its core-edge color. The infinite tail and background have color 0.
All colors must be integers in range(c), and every color 1,...,c-1
must occur on a core edge or spoke. Diagonal entries are ignored.

This is an exhaustive checker of an explicitly supplied candidate, not
an exhaustive search over all candidates or a proof of Erickson's conjecture.
"""
import argparse
import hashlib
import itertools
import json
import sys


def validate(model):
    c, m = model['c'], model['m']
    if type(c) is not int or type(m) is not int or not 1 <= m <= c:
        raise ValueError('Require integers 1 <= m <= c.')
    spokes, edges = model['spokes'], model['edges']
    n = len(spokes)
    if len(edges) != n or any(len(row) != n for row in edges):
        raise ValueError('edges must be an n by n matrix.')
    used = {0}
    for i in range(n):
        if type(spokes[i]) is not int or not 0 <= spokes[i] < c:
            raise ValueError('Spoke label out of range.')
        used.add(spokes[i])
        for j in range(i):
            if edges[i][j] != edges[j][i]:
                raise ValueError('Core-edge matrix must be symmetric.')
            if any(type(label) is not int or not 0 <= label < c
                   for label in (edges[i][j], edges[j][i])):
                raise ValueError('Edge label out of range.')
            used.add(edges[i][j])
    if used != set(range(c)):
        raise ValueError(f'Not surjective: unused colors {sorted(set(range(c))-used)}.')
    return c, m, spokes, edges


def palette(vertices, spokes, edges):
    colors = {0}
    colors.update(spokes[i] for i in vertices)
    colors.update(edges[i][j] for i, j in itertools.combinations(vertices, 2))
    return colors


def verify(model, full_spectrum=False):
    c, m, spokes, edges = validate(model)
    n = len(spokes)
    # Any m-color witness can be reduced to at most 2(m-1) vertices.
    maximum = n if full_spectrum else min(n, 2 * (m - 1))
    witnesses = {}
    checked = 0
    for size in range(maximum + 1):
        for vertices in itertools.combinations(range(n), size):
            colors = palette(vertices, spokes, edges)
            checked += 1
            witnesses.setdefault(len(colors), {'vertices': list(vertices), 'colors': sorted(colors)})
    minimal_losses = []
    for i in range(n):
        after = palette(tuple(j for j in range(n) if j != i), spokes, edges)
        minimal_losses.append(sorted(set(range(c)) - after))
    canonical = json.dumps(model, sort_keys=True, separators=(',', ':')).encode()
    return {
        'c': c, 'm': m, 'core_vertices': n,
        'is_counterexample': m not in witnesses,
        'target_check_complete': True,
        'subset_size_limit': maximum,
        'subsets_checked': checked,
        'full_spectrum_checked': maximum == n,
        'observed_spectrum': sorted(witnesses),
        'spectrum_witnesses': {str(k): witnesses[k] for k in sorted(witnesses)},
        'vertex_deletion_lost_colors': minimal_losses,
        'vertex_minimal_for_full_palette': all(minimal_losses),
        'input_sha256': hashlib.sha256(canonical).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input_json')
    parser.add_argument('--full-spectrum', action='store_true')
    args = parser.parse_args()
    try:
        with open(args.input_json) as f:
            result = verify(json.load(f), args.full_spectrum)
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(json.dumps({'valid_input': False, 'error': str(error)}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['is_counterexample'] else 1


if __name__ == '__main__':
    sys.exit(main())
