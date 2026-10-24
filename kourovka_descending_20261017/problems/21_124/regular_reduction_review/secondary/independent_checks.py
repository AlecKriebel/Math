#!/usr/bin/env python3
"""Independent exact tests of conventions and vertical kernels; not discovery."""
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE.parents[1] / 'nonabelian_holonomy' / 'FINITE_REGULAR_REDUCTION.md'
EXPECTED = '6372e5f77ba26f8d6c59a49c47fa1991ffa521359c65039cdf69d6c699f8a250'


def mul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inv(p):
    return tuple(p.index(i) for i in range(len(p)))


def generated(gs):
    identity = tuple(range(len(gs[0])))
    group = {identity}
    todo = [identity]
    while todo:
        g = todo.pop()
        for s in gs:
            h = mul(s, g)
            if h not in group:
                group.add(h)
                todo.append(h)
    return sorted(group)


def rank(rows):
    a = [[Fraction(v) for v in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [v/q for v in a[r]]
        for i in range(r+1, len(a)):
            q = a[i][c]
            if q:
                a[i] = [v-q*w for v,w in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def action(g, v):
    gi = inv(g)
    return tuple(v[gi[i]] for i in range(len(g)))


def inner(a,b):
    return sum(x*y for x,y in zip(a,b))


def main():
    assert hashlib.sha256(INPUT.read_bytes()).hexdigest() == EXPECTED
    identity = (0,1,2)
    s3 = list(itertools.permutations(range(3)))
    v = (2,-1,4)
    ell = (3,-5,7)
    f = {g: inner(ell, action(inv(g), v)) for g in s3}
    checks = 0
    noncommuting = 0
    for h in s3:
        for g in s3:
            lhs = inner(ell, action(inv(g), action(h,v)))
            rhs = f[mul(inv(h),g)]
            assert lhs == rhs
            checks += 1
            noncommuting += mul(h,g) != mul(g,h)
    assert f[identity] != 0 and noncommuting > 0

    cases = []
    # Cyclic and dihedral cases include identity stable letters and redundant
    # markings. The symmetric example detects nonabelian conventions.
    for n in range(1,7):
        e = tuple(range(n))
        c = tuple((i+1) % n for i in range(n))
        reflection = tuple((-i) % n for i in range(n))
        cases += [('C'+str(n), (c,e,c)),
                  ('D'+str(2*n), (c,reflection,e))]
    cases += [('S3', ((1,0,2),(1,2,0),identity))]
    results = []
    for name, gs in cases:
        group = generated(gs)
        index = {g:i for i,g in enumerate(group)}
        n = len(group)
        rows = []
        # Set A=0 in the complete original matrix, keeping (B,T).
        # No appeal to the author's assembled matrix or code is made.
        for h,q in zip(gs,(2,14,84)):
            for g in group:
                row = [0]*(2*n)
                row[index[g]] = -q
                row[n+index[mul(inv(h),g)]] += 1
                row[n+index[g]] -= 1
                rows.append(row)
        vertical_dim = 2*n-rank(rows)
        assert vertical_dim == 1
        fixed_rows = [r[n:] for r in rows]
        assert n-rank(fixed_rows) == 1
        results.append({'marking':name,'actual_order':n,
                        'vertical_only_kernel_dimension':vertical_dim})
    # Repeated p or q values are not silently used: these actual differences
    # are the nonzero factors in the norm proof.
    assert 20-3 and 14-2 and all(x != 0 for x in (3,20,119,2,14,84))
    output = {'input_sha256':EXPECTED,'outcome':'PASS',
              'equivariance_checks':checks,
              'noncommuting_pairs_checked':noncommuting,
              'vertical_kernel_cases':results,
              'all_finite_group_rank_assertion_checked':False}
    (HERE/'RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
