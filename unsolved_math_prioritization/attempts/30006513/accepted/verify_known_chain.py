#!/usr/bin/env python3
"""Finite sanity checks of the published F_2 incidence-submodule chain.

This audits TheoretiCS 2024, Theorem 4.16. It is not a proof of the
infinite theorem, nor a search for the finite-relational homogeneous case.
No dependencies, network, source bodies, or repository operations.
"""
import itertools
import json
from pathlib import Path


def subspaces(d):
    levels = [{frozenset([0])}]
    for n in range(d):
        nxt = set()
        for u in levels[-1]:
            for v in range(1 << d):
                if v not in u:
                    nxt.add(u | frozenset(x ^ v for x in u))
        levels.append(nxt)
    return levels


def bits(s):
    return sum(1 << x for x in s)


def basis(rows):
    b = {}
    for x in rows:
        while x:
            j = x.bit_length() - 1
            if j in b:
                x ^= b[j]
            else:
                b[j] = x
                break
    return b


def contains(b, x):
    while x:
        j = x.bit_length() - 1
        if j not in b:
            return False
        x ^= b[j]
    return True


def min_weight(b):
    words = [0]
    for row in b.values():
        words += [x ^ row for x in words]
    return min(x.bit_count() for x in words if x)


def generators(d):
    gs = []
    for i in range(d - 1):
        def swap(x, i=i):
            return x ^ ((1 << i) | (1 << (i + 1))) if ((x >> i) ^ (x >> (i + 1))) & 1 else x
        gs.append(swap)
    if d >= 2:
        gs.append(lambda x: x ^ (((x >> 1) & 1) << 0))
    return gs


def run():
    results = []
    for d in range(1, 5):
        ls = subspaces(d)
        previous = None
        for n in range(1, d + 1):
            rows = [bits(u) for u in ls[n]]
            b = basis(rows)
            aff = {bits({x ^ v for x in u}) for u in ls[n] for v in range(1 << d)}
            ab = basis(aff)
            pb = basis([x >> 1 for x in rows])
            assert min_weight(b) == 1 << n
            assert min_weight(ab) == 1 << n
            assert len(pb) == len(b)
            assert min_weight(pb) == (1 << n) - 1
            assert all(row.bit_count() % 2 == 0 for row in b.values())
            for g in generators(d):
                assert all(contains(b, bits(g(x) for x in u)) for u in ls[n])
            if previous is not None:
                assert all(contains(previous, row) for row in rows)
                assert len(b) < len(previous)
            if n >= 2:
                for u in ls[n]:
                    total = 0
                    for h in ls[n-1]:
                        if h <= u:
                            total ^= bits(h)
                    assert total == bits(u)
            results.append(dict(ambient_dimension=d,subspace_dimension=n,
                generators=len(rows),rank=len(b),minimum_weight=min_weight(b),
                affine_rank=len(ab),affine_minimum_weight=min_weight(ab),
                projective_rank=len(pb),projective_minimum_weight=min_weight(pb)))
            previous = b
    # A ternary-addition partial isomorphism that cannot be extended linearly.
    domain = [0,1,2,4,7]
    image = [0,1,2,4,8]
    mapping = dict(zip(domain,image))
    assert all((x ^ y == z) == (mapping[x] ^ mapping[y] == mapping[z])
               for x,y,z in itertools.product(domain,repeat=3))
    assert (1 ^ 2 ^ 4 ^ 7) == 0 and (1 ^ 2 ^ 4 ^ 8) != 0
    return dict(status='PASS',theorem='Published TheoretiCS 2024 Theorem 4.16',
                scope='Finite sanity checks only; the authored audit gives the infinite proof.',
                zero_new_substantive_proof_search_turns=True,
                finite_tests=results,nonhomogeneity_ternary_partial_isomorphism='PASS')


if __name__ == '__main__':
    result = run()
    destination = Path(__file__).with_name('CHECK_RESULTS.json')
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result,indent=2))
