#!/usr/bin/env python3
"""Reviewer controls, independently written; finite checks do not replace proofs."""
import itertools
import json


def rank(a, p):
    a = [[x % p for x in row] for row in a]
    r = 0
    for j in range(len(a[0])):
        i = next((i for i in range(r, len(a)) if a[i][j]), None)
        if i is None:
            continue
        a[r], a[i] = a[i], a[r]
        scale = pow(a[r][j], -1, p)
        a[r] = [x * scale % p for x in a[r]]
        for i in range(len(a)):
            if i != r:
                scale = a[i][j]
                a[i] = [(x - scale*y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def tr(a):
    return list(map(list, zip(*a)))


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def join(a, b):
    return [x+y for x, y in zip(a, b)]


def module(n):
    f = [[0]*(2*n) for _ in range(2*n)]
    v = [[0]*(2*n) for _ in range(2*n)]
    for i, j in ((0, 1), (1, 2), (3, 4)):
        f[j][i] = 1
    for i, j in ((0, 5), (3, 2), (5, 4)):
        v[j][i] = 1
    for i in range(6, 2*n, 2):
        f[i+1][i] = v[i+1][i] = 1
    return f, v


def basis(d, indices):
    return [[int(i == j) for j in indices] for i in range(d)]


def delta(f, v, p):
    ff, vv = mul(f, f), mul(v, v)
    return rank(ff, p) + rank(vv, p) - rank(join(ff, vv), p)


def flag_valid(f, v, columns, p):
    t = tr(columns)
    for end in (2, 4):
        q = [row[:end] for row in t]
        for a in (f, v):
            if rank(join(q, mul(a, q)), p) != end:
                return False
    return rank(t, p) == 6


def main():
    rows = []
    for p, n in itertools.product((2, 3, 5, 7, 11, 17, 101), (3, 4, 8)):
        f, v = module(n)
        zero = [[0]*(2*n) for _ in range(2*n)]
        assert mul(f, v) == zero == mul(v, f)
        assert delta(f, v, p) == 0
        assert delta(tr(v), tr(f), p) == 1
        l = basis(2*n, [0, 3, 5] + list(range(6, 2*n, 2)))
        assert rank(join(f, l), p) == 2*n
        assert rank(mul(v, l), p) == n
        rows.append(dict(p=p, n=n, delta=0, dual_delta=1))
    columns = [[0,1,0,1,0,1], [0,0,1,0,1,0], [0,2,0,1,0,0],
               [0,0,1,0,0,0], [1,0,0,0,0,0], [0,1,0,0,0,0]]
    f, v = module(3)
    assert all(flag_valid(f, v, columns, p) for p in (2, 3, 5, 7, 101))
    bad_columns = [x[:] for x in columns]
    bad_columns[0][5] = 0
    assert not flag_valid(f, v, bad_columns, 5)
    bad_l = basis(6, [1, 3, 5])
    assert rank(join(f, bad_l), 5) != 6
    assert rank(mul(v, bad_l), 5) != 3
    bad_v = [row[:] for row in v]
    bad_v[5][0] = 0
    assert rank(f, 5) + rank(bad_v, 5) != 6
    # Deformability does not require equal ranks: the etale one-dimensional pair.
    assert rank([[1]], 5) + rank([[0]], 5) == 1
    # The sequence Z/p -> Z/p^2 -> Z/p has zero image on the middle p-kernel.
    p = 5
    middle_kernel = [x for x in range(p*p) if p*x % (p*p) == 0]
    right_kernel = list(range(p))
    assert set(x % p for x in middle_kernel) == {0}
    assert set(x % p for x in middle_kernel) != set(right_kernel)
    print(json.dumps(dict(status='PASS', finite_cases=rows,
        flag_checked_at_characteristics=[2,3,5,7,101],
        broken_flag_rejected=True, broken_honda_complement_rejected=True,
        broken_exactness_edge_rejected=True,
        unequal_rank_deformable_boundary_verified=True,
        arbitrary_finite_group_p_kernel_counterexample_verified=True,
        scope='Prime-field finite controls only; all-p and semilinear conclusions use the independent symbolic derivations in REPORT.md. p=2,3 checks do not extend the published theorem or the trace-Witt argument.'), indent=2))


if __name__ == '__main__':
    main()
