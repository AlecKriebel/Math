#!/usr/bin/env python3
"""Independent finite algebra certificates. Standard library; no source imports.

A vector is a parity set of (basis_name,U_exponent,V_exponent) terms.
Maps act directly on vectors, rather than through the packet's matrix routines.
The fixtures are formal complexes; no test recognizes knot realizability.
"""
import argparse
import itertools
import json

NAMES = ('a', 'b', 'c', 'd', 'x')
MUTANTS = ('quotient_character', 'full_square', 'repair_without_a_x',
           'naive_tensor', 'tensor_missing_bc', 'tensor_projection',
           'surgery_additive', 'hkl_parity', 'rank_reversed',
           'rank_without_torsion', 'grading')


def demand(condition, tag):
    if not condition:
        raise ValueError(tag)


def vec(*terms):
    result = set()
    for term in terms:
        if isinstance(term, str):
            term = (term, 0, 0)
        result.symmetric_difference_update({term})
    return frozenset(result)


def plus(*vectors):
    result = set()
    for value in vectors:
        result.symmetric_difference_update(value)
    return frozenset(result)


def apply(mapping, vector, skew=False):
    terms = []
    for name, u, v in vector:
        if skew:
            u, v = v, u
        terms.extend((target, u+a, v+b) for target, a, b in mapping[name])
    return vec(*terms)


def compose(left, right, skew=False):
    return {name: apply(left, value, skew) for name, value in right.items()}


def identity(names):
    return {name: vec(name) for name in names}


def mapplus(*maps):
    return {name: plus(*(mapping[name] for mapping in maps)) for name in maps[0]}


def derivative(mapping, variable):
    return {name: vec(*((target, u-(variable == 0), v-(variable == 1))
                       for target, u, v in terms
                       if (u if variable == 0 else v) % 2))
            for name, terms in mapping.items()}


def truncate(mapping, horizontal=False):
    return {name: frozenset(term for term in terms
                           if term[2] == 0 and (horizontal or term[1] == 0))
            for name, terms in mapping.items()}


def long_box(n, lam, mu):
    differential = {'a': vec(('b', n, 0), ('c', 0, n)),
                    'b': vec(('d', 0, n)), 'c': vec(('d', n, 0)),
                    'd': vec(), 'x': vec()}
    involution = {'a': vec('a', *(['x'] if lam else [])),
                  'b': vec('c'), 'c': vec('b'), 'd': vec('d'),
                  'x': vec('x', *((('d', n-1, n-1),) if mu else ())) }
    grades = dict(zip(NAMES, ((0, 0), (2*n-1, -1), (-1, 2*n-1),
                              (2*n-2, 2*n-2), (0, 0))))
    return differential, involution, grades


def grade_check(mapping, grades, differential=False, skew=False):
    for name, terms in mapping.items():
        g = grades[name]
        expected = (g[0]-1, g[1]-1) if differential else (g[::-1] if skew else g)
        for target, u, v in terms:
            demand((grades[target][0]-2*u, grades[target][1]-2*v) == expected,
                   'bigrading')


def local_directions(differential, involution, grades, tower='x'):
    eligible = [name for name in differential if grades[name] == (0, 0)]
    demand(all(g[1] != 0 or g[0] == 0 for g in grades.values()),
           'constant-map-completeness')
    inclusions, projections = [], []
    for bits in itertools.product((0, 1), repeat=len(eligible)):
        support = {name for name, bit in zip(eligible, bits) if bit}
        if tower not in support:
            continue
        value = vec(*support)
        if not apply(differential, value) and apply(involution, value) == value:
            inclusions.append(sorted(support))
        projection = {name: vec('1') if name in support else vec() for name in differential}
        if all(not apply(projection, differential[name]) and
               apply(projection, involution[name]) == projection[name]
               for name in differential):
            projections.append(sorted(support))
    return bool(inclusions), bool(projections)


def tensor(left, right):
    return {x+y: vec(*((a+b, u+s, v+t) for a, u, v in left[x]
                       for b, s, t in right[y])) for x in left for y in right}


def in_span(columns, target):
    pivots = {}
    for value in columns:
        while value:
            lead = value.bit_length()-1
            if lead not in pivots:
                pivots[lead] = value
                break
            value ^= pivots[lead]
    while target:
        lead = target.bit_length()-1
        if lead not in pivots:
            return False
        target ^= pivots[lead]
    return True


def membership(involution, torsion_cycles, tower):
    names = list(involution)
    def mask(value):
        return sum(1 << names.index(name) for name, u, v in value)
    columns = [1 << names.index(name) for name in torsion_cycles]
    columns += [mask(plus(vec(name), involution[name])) for name in names]
    return in_span(columns, 1 << names.index(tower))


def arf_rank_bit(involution, torsion_cycles, tower, certified_torsion):
    if not certified_torsion:
        return None
    return int(membership(involution, torsion_cycles, tower))


def staircase_v0(power):
    # Exhaustive chain enumeration, separate from the packet's Gaussian solver.
    basis = list(itertools.product('pqr', repeat=power))
    filt = {'p': (0, 1), 'q': (1, 0), 'r': (1, 1)}
    for k in (0, 1, 2):
        allowed = []
        for basis_word in basis:
            maslov = basis_word.count('r')
            if maslov % 2:
                continue
            exponent = k + maslov//2
            i = sum(filt[name][0] for name in basis_word)-exponent
            j = sum(filt[name][1] for name in basis_word)-exponent
            if i <= 0 and j <= 0:
                allowed.append((basis_word, exponent))
        for flags in itertools.product((0, 1), repeat=len(allowed)):
            boundary = set()
            augmentation = 0
            for flag, (word, exponent) in zip(flags, allowed):
                if not flag:
                    continue
                if 'r' not in word:
                    augmentation ^= 1
                for position, name in enumerate(word):
                    if name == 'r':
                        for replacement in 'pq':
                            term = (word[:position]+(replacement,)+word[position+1:], exponent)
                            boundary.symmetric_difference_update({term})
            if not boundary and augmentation:
                return k
    raise ValueError('staircase-search-bound')


def verify(mutant=None):
    # Additive reduction: a countermodel, additivity, 2G annihilation, kernel identity.
    group = list(itertools.product((0, 1), repeat=2))
    a = lambda element: element[0]
    b = lambda element: element[0] ^ element[1]
    difference = lambda element: a(element) ^ b(element)
    for x, y in itertools.product(group, repeat=2):
        xy = tuple(u ^ v for u, v in zip(x, y))
        demand(difference(xy) == (difference(x) ^ difference(y)), 'character-additivity')
        demand(b((x[0] ^ a(x), x[1])) == difference(x), 'kernel-reduction')
    claimed_residual_witness = 0 if mutant == 'quotient_character' else 1
    demand(difference((0, 1)) == claimed_residual_witness, 'nonzero-residual-character')
    demand(a((1, 0)) == b((1, 0)) == 1, 'figure-eight-normalization')
    demand(all((n*n) % 8 == 1 for n in range(-99, 100, 2)), 'odd-square-residues')

    tested_n = list(range(1, 18)) + [31, 32, 101]
    records = []
    unit = identity(NAMES)
    null = {name: vec() for name in NAMES}
    for n in tested_n:
        for lam, mu in itertools.product((0, 1), repeat=2):
            d, j, grades = long_box(n, lam, mu)
            if mutant == 'grading' and (n, lam, mu) == (3, 1, 1):
                grades['x'] = (2, 0)
            grade_check(d, grades, differential=True)
            grade_check(j, grades, skew=True)
            demand(compose(d, d) == null, 'differential-square')
            demand(compose(d, j) == compose(j, d, skew=True), 'skew-chain-map')
            phi, psi = derivative(d, 0), derivative(d, 1)
            square = compose(j, j, skew=True)
            phipsi = compose(phi, psi)
            expected_term = vec(('d', n-1, n-1)) if n % 2 else vec()
            demand(phipsi['a'] == expected_term and
                   all(not phipsi[name] for name in NAMES if name != 'a'),
                   'formal-derivative-product')
            expected = (lam*mu == n % 2)
            if mutant == 'full_square' and (n, lam, mu) == (3, 0, 0):
                expected = True
            demand((square == mapplus(unit, phipsi)) == expected, 'full-square-relation')
            if n % 2:
                demand(n-1 < n and n-1 >= 0, 'ideal-obstruction-exponents')
            hd, hj = truncate(d, horizontal=True), truncate(j)
            hp = truncate(derivative(hd, 0))
            companion = compose(hj, compose(hp, hj))
            horizontal_valid = (compose(hj, hj) == mapplus(unit, compose(hp, companion)))
            demand(horizontal_valid == (n > 1 or lam*mu == 1), 'horizontal-square')
            if horizontal_valid:
                demand(compose(hp, companion) == compose(companion, hp), 'horizontal-commutation')
                lift = null if n > 1 else truncate(psi, horizontal=True)
                demand(truncate(lift) == companion, 'companion-hat-lift')
                demand(compose(hd, lift) == compose(lift, hd), 'companion-chain-lift')
                directions = local_directions(hd, hj, grades)
                expect = (True, lam == 0) if n > 1 else (False, False)
                demand(directions == expect, 'all-graded-local-maps')
            euler = {}
            for u, v in grades.values():
                demand((u-v) % 2 == 0, 'integral-Alexander-grading')
                degree = (u-v)//2
                euler[degree] = euler.get(degree, 0) + (-1 if u % 2 else 1)
            demand(euler == {0: 3, n: -1, -n: -1}, 'Euler-polynomial')
            records.append([n, lam, mu, expected, horizontal_valid])
    repaired_lam = 0 if mutant == 'repair_without_a_x' else 1
    d, j, _ = long_box(3, repaired_lam, 1)
    demand(compose(j, j, skew=True) == mapplus(unit, compose(derivative(d, 0), derivative(d, 1))),
           'odd-box-repair')

    d, j, grades = long_box(1, 1, 1)
    d, j = truncate(d, horizontal=True), truncate(j)
    phi = truncate(derivative(d, 0))
    dt = mapplus(tensor(d, unit), tensor(unit, d))
    naive = tensor(j, j)
    correction = tensor(compose(phi, j), compose(j, phi))
    jt = naive if mutant == 'naive_tensor' else mapplus(naive, correction)
    support = ['ad', 'bc', 'cb', 'da', 'xx']
    gsupport = [name for name in support if name != 'bc'] if mutant == 'tensor_missing_bc' else support
    fsupport = [name for name in support if name != 'cb'] if mutant == 'tensor_projection' else support
    g = vec(*gsupport)
    f = {name: vec('1') if name in fsupport else vec() for name in dt}
    tensor_grades = {x+y: tuple(u+v for u, v in zip(grades[x], grades[y])) for x in NAMES for y in NAMES}
    demand(all(tensor_grades[name] == (0, 0) for name in set(gsupport+fsupport)), 'tensor-grading')
    demand(not apply(dt, g), 'literal-tensor-inclusion-chain')
    demand(apply(jt, g) == g, 'literal-tensor-inclusion-equivariance')
    demand(all(not apply(f, image) for image in dt.values()), 'literal-tensor-projection-chain')
    demand(all(apply(f, image) == f[name] for name, image in jt.items()), 'literal-tensor-projection-equivariance')
    demand('xx' in gsupport and 'xx' in fsupport, 'tensor-localized-tower')
    demand(plus(apply(naive, vec(*support)), vec(*support)) == vec('dd'), 'naive-tensor-defect')

    v0 = [staircase_v0(power) for power in (1, 2)]
    claimed = [1, 2] if mutant == 'surgery_additive' else [1, 1]
    demand(v0 == claimed, 'trefoil-V0-nonadditivity')
    demand(-2*v0[1] != -4*v0[0], 'surgery-d-nonadditivity')
    for n in range(-128, 129):
        determinant = abs((-2*n)*(2*n)-1)
        demand(determinant == 4*n*n+1, 'branched-cover-determinant')
        bit = n % 2
        if mutant == 'hkl_parity':
            bit ^= 1
        demand((determinant % 8 in (3, 5)) == bool(bit), 'HKL-Arf-parity')

    oi = {'x': vec('x')}
    oi_bit = arf_rank_bit(oi, [], 'x', True)
    ei_bit = arf_rank_bit(j, ['b', 'd'], 'x', True)
    demand((oi_bit, ei_bit) == ((1, 0) if mutant == 'rank_reversed' else (0, 1)), 'torsion-rank-direction')
    ld, lj, _ = long_box(3, 1, 1)
    lj = truncate(lj)
    demand(membership(lj, ['b', 'd'], 'x'), 'nontorsion-membership-control')
    unsafe = mutant == 'rank_without_torsion'
    demand(arf_rank_bit(lj, ['b', 'd'], 'x', unsafe) is None, 'torsion-hypothesis-required')
    # The missing Z term is detectable even when x is not itself in W.
    zi = {'x': vec('x'), 'z': vec('z'), 'y': vec('y', 'x', 'z')}
    demand(not membership(zi, [], 'x') and membership(zi, ['z'], 'x'), 'Z-plus-W-required')
    return {'result': 'PASS', 'long_box_cases': records,
            'literal_tensor_support': support, 'naive_tensor_inclusion_defect': 'dd',
            'trefoil_V0': v0, 'surgery_d_values': [-2, -4],
            'determinant_checks': 257, 'torsion_rank_bits_O_E': [oi_bit, ei_bit],
            'nontorsion_rank_classification': None,
            'scope': 'Independent finite algebra certificates; no realizability or target-equality oracle.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant', choices=MUTANTS)
    args = parser.parse_args()
    print(json.dumps(verify(args.mutant), indent=2, sort_keys=True))
