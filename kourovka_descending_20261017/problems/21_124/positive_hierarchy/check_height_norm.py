#!/usr/bin/env python3
"""Exact row reduction and free-word checks for HEIGHT_NORM_COUNTERMODEL.md."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json


def rref(matrix):
    rows = [[Q(x) for x in row] for row in matrix]
    pivot_row, pivots = 0, []
    for col in range(len(rows[0])):
        pivot = next((i for i in range(pivot_row, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][col]
        rows[pivot_row] = [x / scale for x in rows[pivot_row]]
        for i in range(len(rows)):
            if i != pivot_row and rows[i][col]:
                scale = rows[i][col]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[pivot_row])]
        pivots.append(col)
        pivot_row += 1
    return rows, pivots


def reduce_word(word):
    out = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def power(generator, exponent):
    return (generator if exponent > 0 else -generator,) * abs(exponent)


def substitute(word, images):
    out = []
    for letter in word:
        image = images[abs(letter)]
        out += image if letter > 0 else tuple(-x for x in reversed(image))
    return reduce_word(out)


def main():
    pairs = [(7, 1), (7, -1), (8, 4), (8, -4), (13, 11), (13, -11)]
    metric_rows = [[x*x, 2*x, 1, -y*y, -2*y, -1] for x, y in pairs]
    reduced, pivots = rref(metric_rows)
    assert len(pivots) == 4
    null_basis = [(1, 0, 0, 1, 0, 48), (0, 0, 1, 0, 0, 1)]
    assert all(sum(a*b for a, b in zip(row, v)) == 0 for row in metric_rows for v in null_basis)
    assert all(x*x + 1 == y*y + 49 for x, y in pairs)
    assert len({x for x, _ in pairs}) == 3
    twists = [(7-x, y-1) for x, y in pairs[1:]]
    assert twists == [(0, -2), (-1, 3), (-1, -5), (-6, 10), (-6, -12)]
    forward = {1: (1,), 2: (2,)}
    backward = dict(forward)
    for u, (p, q) in enumerate(twists, 3):
        forward[u] = power(1, p) + (u,) + power(2, q)
        backward[u] = power(1, -p) + (u,) + power(2, -q)
    for i in range(1, 8):
        assert substitute(forward[i], backward) == (i,)
        assert substitute(backward[i], forward) == (i,)
    iterations = 0
    for u, (p, q) in enumerate(twists, 3):
        image = (u,)
        for n in range(101):
            assert image == power(1, n*p) + (u,) + power(2, n*q)
            assert len(image) == n * (abs(p) + abs(q)) + 1
            image = substitute(image, forward)
            iterations += 1
    # Exact projection countermodel for a blocked generic CAT(0) reduction.
    # Product of a four-pronged unit tree and R; diagonal I(s) uses two tree
    # branches. Other two endpoints at height1 project to s=0; their midpoint
    # projects to s=1/2. Compare squared distances, with rational arithmetic.
    endpoint_at_zero = Q(1)**2 + Q(1)**2
    endpoint_at_half = Q(3, 2)**2 + Q(1, 2)**2
    midpoint_at_zero = Q(0)**2 + Q(1)**2
    midpoint_at_half = Q(1, 2)**2 + Q(1, 2)**2
    assert endpoint_at_zero < endpoint_at_half
    assert midpoint_at_half < midpoint_at_zero
    here = Path(__file__).resolve().parent
    receipt = {'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
               'metric_row_rank': len(pivots), 'compatible_forms_dimension': 6-len(pivots),
               'null_basis_A1_C1_D1_A2_C2_D2': null_basis,
               'rref': [[str(x) for x in row] for row in reduced],
               'fiber_rank': 2 + (6-2+1), 'monodromy_iterations': iterations,
               'twists': twists, 'original_graph_only': True,
               'scope': 'CAT(0) free-by-Z test group and failed uniform-height ansatz; no virtual-specialness obstruction',
               'proof_sha256': hashlib.sha256((here/'HEIGHT_NORM_COUNTERMODEL.md').read_bytes()).hexdigest(),
               'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (here/'height_norm_certificate.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
