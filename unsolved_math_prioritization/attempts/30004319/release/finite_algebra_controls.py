#!/usr/bin/env python3
"""Exhaustive labelled F2-algebra controls. These are not A2-group constructions.

The 4096 tables exhaust unital bilinear products on the fixed basis (1,e,f).
Strong inverses use Wiedemann Definition 5.1.12, not just ab=ba=1.
All loops are finite; no external package, random sampling, or group solver.
"""
import itertools
import json
import hashlib
from collections import Counter


def table(products):
    basis = [[1, 2, 4], [2, products[0], products[1]],
             [4, products[2], products[3]]]
    return [[xor(basis[i][j] for i in range(3) for j in range(3)
                 if a >> i & 1 and b >> j & 1) for b in range(8)]
            for a in range(8)]


def xor(xs):
    out = 0
    for x in xs:
        out ^= x
    return out


def associator(m, a, b, c):
    return m[m[a][b]][c] ^ m[a][m[b][c]]


def strong_inverse(m, a, b):
    return all(m[a][m[b][z]] == z == m[b][m[a][z]] and
               m[m[z][a]][b] == z == m[m[z][b]][a] for z in range(8))


def moufang_at(m, a):
    # a(y(az))=(a(ya))z; ((za)y)a=z((ay)a); (ay)(za)=(a(yz))a.
    return all(m[a][m[y][m[a][z]]] == m[m[a][m[y][a]]][z] and
               m[m[m[z][a]][y]][a] == m[z][m[m[a][y]][a]] and
               m[m[a][y]][m[z][a]] == m[m[a][m[y][z]]][a]
               for y in range(8) for z in range(8))


def details(products):
    m = table(products)
    units = [a for a in range(8) if any(strong_inverse(m, a, b)
                                      for b in range(8))]
    left_bad = next(((a, b, associator(m, a, a, b))
                     for a in range(8) for b in range(8)
                     if associator(m, a, a, b)), None)
    right_bad = next(((a, b, associator(m, b, a, a))
                      for a in range(8) for b in range(8)
                      if associator(m, b, a, a)), None)
    alternative = left_bad is None and right_bad is None
    associative = all(associator(m, a, b, c) == 0
                      for a in (1, 2, 4) for b in (1, 2, 4)
                      for c in (1, 2, 4))
    passes = all(moufang_at(m, a) for a in units)
    # The unit-shift sufficient condition only includes integer multiples of 1.
    shift_covers = all(a in units or (a ^ 1) in units for a in range(8))
    return dict(products=list(products), units=units, associative=associative,
                alternative=alternative, unit_moufang=passes,
                integer_shift_covers=shift_covers,
                left_witness=left_bad, right_witness=right_bad)


def opposite_root_obstruction(m):
    """Necessary: ab=ca=0 => (bc)(at)=(ta)(bc)=a((bc)t)=(t(bc))a=0."""
    for a,b,c in itertools.product(range(8),repeat=3):
        if m[a][b] or m[c][a]:
            continue
        d = m[b][c]
        for t in range(8):
            values = [m[d][m[a][t]], m[m[t][a]][d],
                      m[a][m[d][t]], m[m[t][d]][a]]
            if any(values):
                return dict(a=a,b=b,c=c,t=t,values=values)
    return None


def main():
    counts = Counter()
    survivor_histogram = Counter()
    first = None
    survivors = []
    final_survivors = []
    for products in itertools.product(range(8), repeat=4):
        d = details(products)
        counts['total'] += 1
        for key in ['associative', 'alternative', 'unit_moufang',
                    'integer_shift_covers']:
            counts[key] += int(d[key])
        assert not d['associative'] or d['alternative']
        assert not d['alternative'] or d['unit_moufang']
        assert not (d['unit_moufang'] and d['integer_shift_covers']) or d['alternative']
        if d['alternative']:
            assert opposite_root_obstruction(table(products)) is None
        if d['unit_moufang'] and not d['alternative']:
            counts['nonalternative_survivors'] += 1
            survivor_histogram[len(d['units'])] += 1
            survivors.append(list(products))
            if first is None:
                first = d
            if opposite_root_obstruction(table(products)) is None:
                final_survivors.append(list(products))
    counts['nonalternative_after_both_filters'] = len(final_survivors)
    counts['nonalternative_rejected_by_opposite_root'] = len(survivors)-len(final_survivors)
    assert counts['total'] == 4096
    # Concrete independent positive-root-group control over the first survivor.
    m = table(first['products'])
    mul = lambda p,q: (p[0]^q[0], p[1]^q[1], p[2]^q[2]^m[p[0]][q[1]])
    inv = lambda p: (p[0], p[1], p[2]^m[p[0]][p[1]])
    identity = (0,0,0)
    elements = list(itertools.product(range(8),repeat=3))
    assert all(mul(p,inv(p)) == identity == mul(inv(p),p) for p in elements)
    # Full cocycle identity exhausts all nontrivial coordinates in associativity.
    cocycle_count = 0
    for a,b,c,d in itertools.product(range(8), repeat=4):
        assert m[a][b] ^ m[a ^ c][d] == m[c][d] ^ m[a][b ^ d]
        cocycle_count += 1
    # x12(a) x23(b) = x23(b) x12(a) x13(ab), exhaustively.
    for a,b in itertools.product(range(8),repeat=2):
        x,y,z = (a,0,0), (0,b,0), (0,0,m[a][b])
        assert mul(x,y) == mul(mul(y,x),z)
    print(json.dumps(dict(
        domain='All 4096 labelled unital bilinear F2 algebra tables on (1,e,f)',
        bit_encoding={'1':1,'e':2,'f':4},
        products_order=['e*e','e*f','f*e','f*f'],
        counts=dict(counts),
        nonalternative_survivor_unit_counts=dict(sorted(survivor_histogram.items())),
        first_nonalternative_survivor=first,
        first_survivor_opposite_root_rejection=opposite_root_obstruction(m),
        first_after_both_filters=details(final_survivors[0]),
        simple_commutative_survivor=details((0,1,1,0)),
        positive_group={'order':512,'two_sided_inverse_checks':512,
                        'exhaustive_cocycle_checks':cocycle_count,
                        'commutator_checks':64},
        limits=['labelled tables, not isomorphism classes',
                'only dimension 3 over F2',
                'strong-unit Moufang is necessary, not sufficient',
                'no full A2-graded group or counterexample constructed',
                'the opposite-root filter is also only a necessary condition',
                'no universal-group root injectivity or nondegeneracy tested'],
        unit_moufang_nonalternative_tables_sha256=hashlib.sha256(
            json.dumps(survivors,separators=(',',':')).encode()).hexdigest(),
        survivor_tables_after_both_filters=final_survivors),indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
