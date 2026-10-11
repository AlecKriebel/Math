#!/usr/bin/env python3
"""Independent exact controls. No author imports; bounded evidence, not proof."""
from pathlib import Path
from itertools import product, permutations, combinations
from math import comb, gcd
from functools import reduce
import hashlib
import json
import datetime

HERE = Path(__file__).resolve().parent
assertions = 0


def check(condition):
    global assertions
    assert condition
    assertions += 1


def vp(n, p):
    if not n:
        return None
    n = abs(n)
    result = 0
    while n % p == 0:
        n //= p
        result += 1
    return result


def cyclic_coefficients(m, k):
    """Expand the binomial directly, then reduce exponents modulo m."""
    return [sum((-1) ** (k - a) * comb(k, a)
                for a in range(j, k + 1, m)) for j in range(m)]


def lattice_controls():
    records = []
    for p, e in [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2)]:
        q = p ** e
        points = list(product(range(q), repeat=2))
        # Any subgroup of this two-generator abelian p-group has <=2 generators.
        subgroups = {frozenset(((a*x[0]+b*y[0]) % q,
                               (a*x[1]+b*y[1]) % q)
                              for a, b in product(range(q), repeat=2))
                     for x, y in combinations(points, 2)}
        subgroups.add(frozenset({(0, 0)}))
        matrices = [m for m in product(range(q), repeat=4)
                    if gcd(m[0]*m[3]-m[1]*m[2], q) == 1]
        invariant = []
        for subgroup in subgroups:
            is_invariant = all(
                frozenset(((a*x+b*y) % q, (c*x+d*y) % q)
                          for x, y in subgroup) == subgroup
                for a, b, c, d in matrices)
            if is_invariant:
                invariant.append(subgroup)
        expected = {frozenset((x, y) for x, y in points
                              if x % (p**a) == 0 and y % (p**a) == 0)
                    for a in range(e + 1)}
        check(set(invariant) == expected)
        # Permutation invariance is insufficient: the sum-zero-mod-p subgroup.
        weak = frozenset((x, y) for x, y in points if (x+y) % p == 0)
        check(frozenset((y, x) for x, y in weak) == weak)
        check(weak not in expected)
        # A single transvection actually breaks this weaker invariance.
        check(frozenset(((x+y) % q, y) for x, y in weak) != weak)
        records.append({'p': p, 'e': e, 'subgroups': len(subgroups),
                        'full_GL2_matrices': len(matrices),
                        'invariant_subgroups': len(invariant)})
    return records


def table_groups():
    # C8, elementary abelian C2^3, and Q8: none occur in author core controls.
    cyclic = [[(a+b) % 8 for b in range(8)] for a in range(8)]
    elementary = [[a ^ b for b in range(8)] for a in range(8)]
    # Q8 = { +/-1, +/-i, +/-j, +/-k }; index = 2*basis + sign.
    products = [[(0, 0), (1, 0), (2, 0), (3, 0)],
                [(1, 0), (0, 1), (3, 0), (2, 1)],
                [(2, 0), (3, 1), (0, 1), (1, 0)],
                [(3, 0), (2, 0), (1, 1), (0, 1)]]
    quaternion = []
    for a in range(8):
        row = []
        for b in range(8):
            c, sign = products[a//2][b//2]
            row.append(2*c + (sign ^ (a % 2) ^ (b % 2)))
        quaternion.append(row)
    return [('C8', cyclic), ('C2^3', elementary), ('Q8', quaternion)]


def finite_core_controls():
    records = []
    for name, table in table_groups():
        universe = frozenset(range(8))
        check(all(table[0][x] == x == table[x][0] for x in universe))
        check(all(table[table[x][y]][z] == table[x][table[y][z]]
                  for x, y, z in product(universe, repeat=3)))
        # Inspect all subsets, not a generator-growth subgroup enumeration.
        subgroups = []
        for mask in range(1 << 7):
            subset = frozenset({0} | {i+1 for i in range(7) if mask >> i & 1})
            if all(table[x][y] in subset for x, y in product(subset, repeat=2)):
                subgroups.append(subset)
        autos = {}
        for subgroup in subgroups:
            ordered = sorted(subgroup)
            found = []
            # Inspect every identity-fixing permutation directly.
            for tail in permutations(ordered[1:]):
                f = dict(zip(ordered, (0,) + tail))
                if all(f[table[x][y]] == table[f[x]][f[y]]
                       for x, y in product(subgroup, repeat=2)):
                    found.append(f)
            autos[subgroup] = found
            check(bool(found))

        def characteristic(ambient, subgroup):
            return all(frozenset(f[x] for x in subgroup) == subgroup
                       for f in autos[ambient])

        def core(ambient, subgroup):
            image = set(subgroup)
            for f in autos[ambient]:
                image.intersection_update(f[x] for x in subgroup)
            return frozenset(image)

        proper = [u for u in subgroups if u != universe]
        families = [(universe, u) for u in proper]
        families += [(universe, u, v) for u, v in combinations(proper, 2)]
        nonzero = zero = max_rounds = 0
        for family in families:
            start = frozenset.intersection(*family)
            admissible = [k for k in subgroups if k <= start and
                          all(characteristic(u, k) for u in family)]
            # Product of all common characteristic subgroups is the maximal one.
            maximal = max(admissible, key=len)
            check(all(k <= maximal for k in admissible))
            for order in permutations(family):
                current = start
                rounds = 0
                while True:
                    following = current
                    for u in order:
                        following = core(u, following)
                        check(following <= current)
                    rounds += 1
                    if following == current:
                        break
                    current = following
                    check(rounds <= 8)
                check(current == maximal)
                max_rounds = max(max_rounds, rounds)
            if len(maximal) > 1:
                nonzero += 1
            else:
                zero += 1
        # Omitting an operator can leave a falsely accepted characteristic subgroup.
        if name == 'C2^3':
            plane = frozenset({0, 1, 2, 3})
            check(core(plane, plane) == plane)
            check(not characteristic(universe, plane))
            check(core(universe, plane) == frozenset({0}))
        if name == 'Q8':
            line = frozenset({0, 1, 2, 3})
            check(core(line, core(universe, line)) == frozenset({0, 1}))
        records.append({'group': name, 'subgroups': len(subgroups),
                        'full_automorphisms': len(autos[universe]),
                        'families': len(families), 'zero_core_families': zero,
                        'nonzero_core_families': nonzero,
                        'max_rounds_to_stable_core': max_rounds})
    return records


def invert(word):
    return [-x for x in reversed(word)]


def schreier_exponents(word, p):
    state = 0
    exponents = [0] * (p + 1)
    for letter in word:
        if abs(letter) == 2:
            exponents[1+state] += 1 if letter > 0 else -1
        elif letter == 1:
            if state == p-1:
                exponents[0] += 1
            state = (state + 1) % p
        elif letter == -1:
            if state == 0:
                exponents[0] -= 1
            state = (state - 1) % p
        else:
            raise AssertionError('unexpected free letter')
    check(state == 0)
    return exponents


def commutator_controls():
    primes = [2, 3, 5, 7, 11, 17, 19, 23, 29, 31]
    for p in primes:
        for k in range(1, 221):
            coefficients = cyclic_coefficients(p, k)
            divisor = reduce(gcd, coefficients)
            check(divisor != 0)
            check(sum(coefficients) == 0)
            check(vp(divisor, p) == (k-1)//(p-1))
            for e in range(1, 9):
                check((divisor % p**e == 0) == (k >= e*(p-1)+1))
        for e in range(1, 9):
            before = e*(p-1)  # k=n-1 just before the first invisible word.
            after = before+1
            check(any(c % p**e for c in cyclic_coefficients(p, before)))
            check(all(c % p**e == 0 for c in cyclic_coefficients(p, after)))
    actual_words = []
    for p in [2, 3, 5, 7]:
        word = [2]
        for n in range(1, 10):
            exponents = schreier_exponents(word, p)
            check(exponents[0] == 0)
            check(exponents[1:] == cyclic_coefficients(p, n-1))
            actual_words.append({'p': p, 'n': n, 'word_length': len(word),
                                 'exponents': exponents})
            word = [1] + word + [-1] + invert(word)
        check(schreier_exponents([1]*p + [2] + [-1]*p, p)[1:] ==
              cyclic_coefficients(p, 0))
    # The prime-cycle assumption cannot be dropped in this valuation formula.
    composite = cyclic_coefficients(4, 6)
    check(vp(reduce(gcd, composite), 2) == 2)
    check(vp(reduce(gcd, composite), 2) != (6-1)//(4-1))
    return {'primes': primes, 'max_power': 220,
            'actual_word_receipts': actual_words,
            'negative_composite_cycle': {'m': 4, 'prime': 2, 'k': 6,
                                         'coefficients': composite,
                                         'valuation': 2,
                                         'false_extended_formula': 1}}


def frozen_check():
    parent = HERE.parent
    manifest = json.loads((parent/'snapshot_manifest.json').read_text())
    check(manifest['head'] == 'fd4a71f2f7e08ece5f0d34d9d0df3fb6f460d8bf')
    check(len(manifest['files']) == 45)
    for item in manifest['files']:
        data = (parent/'snapshot'/item['path']).read_bytes()
        check(len(data) == item['bytes'])
        check(hashlib.sha256(data).hexdigest() == item['sha256'])
    return {'head': manifest['head'], 'paths': len(manifest['files']),
            'snapshot_manifest_sha256': hashlib.sha256(
                (parent/'snapshot_manifest.json').read_bytes()).hexdigest(),
            'all_hashes_match': True}


if __name__ == '__main__':
    output = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'scope': 'Independent bounded controls and negative cases. Infinite proofs are in REVIEW.md.',
              'frozen': frozen_check(),
              'lattices': lattice_controls(),
              'finite_cores': finite_core_controls(),
              'commutators': commutator_controls()}
    output['assertions'] = assertions
    print(json.dumps(output, indent=2, sort_keys=True))
