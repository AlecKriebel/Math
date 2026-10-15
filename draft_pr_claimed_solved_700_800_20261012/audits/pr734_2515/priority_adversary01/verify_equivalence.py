#!/usr/bin/env python3
"""Independent finite computations and recursive action controls; stdlib only.

No source-body inputs or GAP/library identifications are used. Run this file
from any directory; results are written beside it. Permutations are 0-based
image tuples. `after(f,g)` means f after g; `gap` means left-to-right action.
The finite checks support, but do not replace, the induction in report.md.
"""
from itertools import product, permutations
from collections import Counter
from pathlib import Path
import json


def perm(n, *cycles):
    p = list(range(n))
    for c in cycles:
        for x, y in zip(c, c[1:] + c[:1]):
            p[x - 1] = y - 1
    return tuple(p)


def after(f, g):
    return tuple(f[x] for x in g)


def inverse(p):
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return tuple(q)


def gap(*ps):
    q = tuple(range(len(ps[0])))
    for p in ps:
        q = after(p, q)
    return q


def closure(gens, n):
    gens = tuple(sorted(set(gens)))
    e = tuple(range(n))
    seen, pending = {e}, [e]
    while pending:
        x = pending.pop()
        for g in gens:
            y = after(g, x)
            if y not in seen:
                seen.add(y)
                pending.append(y)
    return frozenset(seen)


def orbits(group, n):
    unseen, out = set(range(n)), []
    while unseen:
        x = min(unseen)
        orbit = {g[x] for g in group}
        unseen -= orbit
        out.append(sorted(x + 1 for x in orbit))
    return out


def cycles(p):
    unseen, out = set(range(len(p))), []
    while unseen:
        x = min(unseen)
        c, y = [], x
        while y not in c:
            c.append(y)
            y = p[y]
        unseen -= set(c)
        out.append(c)
    return out


def is_block(c, group):
    c = set(c)
    return all(not (c & {g[x] for x in c}) or c == {g[x] for x in c}
               for g in group)


def cycle_blocks(group):
    return all(is_block(c, group) for g in group for c in cycles(g))


def relabel(p, rho):
    return after(rho, after(p, inverse(rho)))


def subgroup_lattice(group, n):
    e = frozenset({tuple(range(n))})
    seen, pending = {e}, [e]
    while pending:
        h = pending.pop()
        for g in sorted(group - h):
            k = closure(tuple(h) + (g,), n)
            if k not in seen:
                seen.add(k)
                pending.append(k)
    return seen


def parity_group(twisted=True):
    # v=e1*v_1+e2*v_2 is encoded v_1+2*v_2, epsilon is the low bit.
    out = set()
    for f in product(range(2), repeat=4):
        for t in range(4):
            if twisted and sum(f) % 2 != (t & 1):
                continue
            p = tuple(2 * (v ^ t) + (eps ^ f[v ^ t])
                      for v in range(4) for eps in range(2))
            out.add(p)
    return frozenset(out)


def wreath_element(left, right, swap):
    n = len(left)
    # Independent factors act, then the top exchange. This lists all normal forms.
    p = tuple(left) + tuple(n + x for x in right)
    if swap:
        p = tuple((x + n) % (2 * n) for x in p)
    return p


def wreath(group):
    return frozenset(wreath_element(a, b, s)
                     for a in group for b in group for s in (0, 1))


def wreath_generators(gens):
    n = len(gens[0])
    e = tuple(range(n))
    return tuple(wreath_element(g, e, 0) for g in gens) + tuple(
        wreath_element(e, g, 0) for g in gens) + (wreath_element(e, e, 1),)


def main():
    qa = perm(8, (1, 4, 5, 8), (2, 3), (6, 7))
    qb = perm(8, (1, 3), (2, 8), (4, 6), (5, 7))
    pa = perm(8, (1, 3, 2, 4), (5, 7), (6, 8))
    pb = perm(8, (1, 5), (2, 6), (3, 7), (4, 8))
    pz = perm(8, (3, 4), (5, 6))
    q = closure((qa, qb), 8)
    p = parity_group()
    assert len(q) == len(p) == 32
    assert closure((pa, pb), 8) == p
    assert orbits(q, 8) == [list(range(1, 9))]

    r = gap(qa, qa)
    s = gap(inverse(qa), inverse(qb), qa, qb)
    t = gap(inverse(qa), s, qa)
    assert r == perm(8, (1, 5), (4, 8))
    assert s == perm(8, (2, 6), (4, 8))
    assert t == perm(8, (1, 5), (3, 7))
    f = closure((r, s, t), 8)
    assert len(f) == 8
    assert all(after(a, b) == after(b, a) for a in f for b in f)
    assert all(relabel(h, g) in f for h in f for g in q)
    lattice = subgroup_lattice(q, 8)
    proper = lattice - {q}
    maximal = [h for h in proper if not any(h < k < q for k in lattice)]
    assert len(maximal) == 3
    assert all(len(orbits(h, 8)) > 1 for h in proper)
    assert set.intersection(*(set(h) for h in maximal)) == set(f)
    explicit_max = [closure(tuple(f) + (g,), 8) for g in (qa, qb, gap(qb, qa))]
    assert set(explicit_max) == set(maximal)

    u = gap(qb, qa)
    v = gap(qb, inverse(qa), qb, qa)
    assert u == perm(8, (1, 2), (3, 4, 7, 8), (5, 6))
    assert v == perm(8, (2, 6), (4, 8))
    assert {0, 1} in [set(c) for c in cycles(u)]
    assert {v[0], v[1]} == {0, 5}
    assert not is_block({0, 1}, q)
    assert not cycle_blocks(q)
    assert not is_block({0, 4}, p)
    assert {pz[0], pz[4]} == {0, 5}

    # Choose a concrete conjugacy without assuming the generator pairs match.
    rho = next(h for h in permutations(range(8))
               if {relabel(g, h) for g in q} == set(p))
    # Some relabellings conjugate groups but not the displayed generator pairs.
    generator_images = [relabel(g, rho) for g in (qa, qb)]
    assert closure(generator_images, 8) == p
    assert {relabel(g, rho) for g in q} == set(p)

    # Auxiliary primary-source finite attributions (consulted after our own result).
    # Hulpke's 2002 supplement adds a redundant generator t to qa and qb.
    assert closure((perm(8, (1, 5), (3, 7)), qa, qb), 8) == q
    # Xia-Zheng p=2,m=2,b_R=(1,0): theta eta(1)=delta_0.
    # Their first generator evaluates the base function at the INPUT v.
    xia_first = tuple(2*(v ^ 1)+(eps ^ (v == 0))
                      for v in range(4) for eps in range(2))
    xia_second = tuple(2*(v ^ 2)+eps
                       for v in range(4) for eps in range(2))
    assert xia_first == inverse(pa) and xia_second == pb
    assert closure((xia_first, xia_second), 8) == p
    # Images of X1, X2, X1*X2 span exactly the even functions (dimension3).
    ring_ideal_images = [(1, 1, 0, 0), (1, 0, 1, 0), (1, 1, 1, 1)]
    even_functions = {tuple(sum(c[i]*ring_ideal_images[i][v]
                               for i in range(3)) % 2 for v in range(4))
                      for c in product(range(2), repeat=3)}
    assert len(even_functions) == 8
    assert even_functions == {f for f in product(range(2), repeat=4)
                              if sum(f) % 2 == 0}

    wq, wp = wreath(q), wreath(p)
    rho1 = tuple(rho) + tuple(8 + x for x in rho)
    assert len(wq) == len(wp) == 2048
    assert {relabel(g, rho1) for g in wq} == set(wp)
    bottom = set(range(8))
    q_local = {tuple(g[i] for i in range(8)) for g in wq
               if {g[i] for i in bottom} == bottom}
    assert q_local == set(q)
    assert all(is_block(bottom, {g}) for g in wq)

    # At higher stages verify recursive generators; the general equality is inductive.
    qgens, pgens = (qa, qb), tuple(generator_images)
    stage_checks = []
    for n in range(7):
        npoints = 8 * 2**n
        rn = tuple(8*j + rho[x] for j in range(2**n) for x in range(8))
        assert {relabel(g, rn) for g in qgens} == set(pgens)
        fibres = [set(range(8*j, 8*j+8)) for j in range(2**n)]
        for g in qgens:
            for b in fibres:
                image = {g[x] for x in b}
                assert image in fibres
                j, k = min(b)//8, min(image)//8
                assert tuple(g[8*j+x]-8*k for x in range(8)) in q
        # The stage map appends high bit 0, so it commutes with first-factor inclusion.
        if n:
            assert rn[:npoints//2] == previous_rn
        previous_rn = rn
        stage_checks.append({'stage': n, 'points': npoints,
                             'order_exponent_base_2': 6*2**n-1,
                             'generators_checked': len(qgens), 'passed': True})
        qgens, pgens = wreath_generators(qgens), wreath_generators(pgens)

    # Negative controls: the untwisted action contains the regular C2^3.
    full = parity_group(twisted=False)
    flip = perm(8, (1, 2), (3, 4), (5, 6), (7, 8))
    e1 = perm(8, (1, 3), (2, 4), (5, 7), (6, 8))
    reg = closure((flip, e1, pb), 8)
    assert len(full) == 64 and reg <= full and len(reg) == 8
    assert orbits(reg, 8) == [list(range(1, 9))] and cycle_blocks(reg)
    # The identity translate has full rather than partial intersection.
    assert {0, 1} == {tuple(range(8))[x] for x in {0, 1}}
    # Diagonal embeddings replicate support at each level: they cannot substitute.
    diag = qa
    diagonal_supports = []
    for n in range(5):
        diagonal_supports.append(sum(i != x for i, x in enumerate(diag)))
        diag = wreath_element(diag, diag, 0)
    assert diagonal_supports == [8, 16, 32, 64, 128]

    result = {
        'verdict': 'finite checks pass; complete inductive equivalence in report.md',
        'prior_local_order': len(q), 'candidate_local_order': len(p),
        'subgroup_count': len(lattice),
        'subgroup_order_counts': dict(sorted(Counter(map(len, lattice)).items())),
        'proper_transitive_subgroups': 0,
        'maximal_orbits': [orbits(h, 8) for h in explicit_max],
        'frattini_order': len(f),
        'prior_witness': {'cycle': [1, 2], 'translated_cycle': [1, 6]},
        'candidate_witness': {'cycle': [1, 5], 'translated_cycle': [1, 6]},
        'rho_prior_to_candidate_one_based': [x+1 for x in rho],
        'prior_generator_images_one_based': [[x+1 for x in g] for g in generator_images],
        'first_wreath_order': len(wq), 'first_wreath_full_equality': True,
        'first_wreath_local_action_equal_Q': True,
        'auxiliary_finite_attributions': {
            'hulpke_2002_three_generators_generate_Q': True,
            'xia_zheng_first_generator_equals_candidate_a_inverse': True,
            'xia_zheng_second_generator_equals_candidate_b': True,
            'xia_zheng_generated_group_equals_P': True,
            'xia_zheng_kernel_ideal_maps_to_even_base_dimension': 3,
        },
        'stage_generator_checks': stage_checks,
        'controls': {'untwisted_regular_subgroup_cycle_blocks': True,
                     'identity_is_not_crossing_witness': True,
                     'diagonal_support_growth': diagonal_supports},
    }
    out = Path(__file__).with_name('equivalence_results.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
