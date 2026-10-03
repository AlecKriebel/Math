"""New independent boundary controls; no candidate/reviewer imports.

These finite checks are supplementary controls, never an infinite proof.
"""
import itertools
import json
import math

checks = 0

def check(value):
    global checks
    if not value:
        raise AssertionError('independent boundary control failed')
    checks += 1

def subgroups(elements, operation, identity):
    elements = frozenset(elements)
    def generated(generators):
        found = {identity}
        todo = [identity]
        while todo:
            a = todo.pop()
            for b in generators:
                c = operation(a, b)
                if c not in found:
                    found.add(c)
                    todo.append(c)
        return frozenset(found)
    found = {frozenset({identity})}
    todo = list(found)
    while todo:
        h = todo.pop()
        for g in elements - h:
            j = generated(tuple(h) + (g,))
            if j not in found:
                found.add(j)
                todo.append(j)
    return found

# Exhaustive additive-subgroup enumeration, including skew/nondiagonal
# subgroups, tests the scalar-ideal conclusion beyond coordinate identities.
module_summary = []
for p, e in [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2)]:
    q = p**e
    elements = list(itertools.product(range(q), repeat=2))
    add = lambda a, b: ((a[0]+b[0]) % q, (a[1]+b[1]) % q)
    subs = subgroups(elements, add, (0, 0))
    generators = [lambda v: (v[1], v[0]),
                  lambda v: ((v[0]+v[1]) % q, v[1]),
                  lambda v: (v[0], (v[0]+v[1]) % q)]
    for unit in range(q):
        if math.gcd(unit, q) == 1:
            generators.append(lambda v, u=unit: (u*v[0] % q, v[1]))
    stable = {h for h in subs if all(frozenset(g(x) for x in h) == h
                                    for g in generators)}
    expected = {frozenset((a, b) for a, b in elements
                          if a % (p**k) == b % (p**k) == 0)
                for k in range(e+1)}
    check(stable == expected)
    check(len(stable) == e+1)
    module_summary.append({'p': p, 'e': e, 'additive_subgroups': len(subs),
                           'stable_scalar_subgroups': len(stable)})

# Full multiplication-preserving permutations, not generator-image
# propagation, independently reconstruct all automorphisms of groups <=8.
core_summary = []
for name, elements, operation in [
    ('C2^3', list(itertools.product(range(2), repeat=3)),
     lambda a, b: tuple((x+y) % 2 for x, y in zip(a, b))),
    ('D8', list(itertools.product(range(4), range(2))),
     lambda a, b: ((a[0]+(-1)**a[1]*b[0]) % 4, (a[1]+b[1]) % 2))]:
    identity = elements[0]
    subs = subgroups(elements, operation, identity)
    automorphisms = {}
    for group in subs:
        tail = sorted(group - {identity})
        automorphisms[group] = []
        for perm in itertools.permutations(tail):
            f = dict(zip(tail, perm)); f[identity] = identity
            if all(f[operation(a, b)] == operation(f[a], f[b])
                   for a, b in itertools.product(group, repeat=2)):
                automorphisms[group].append(f)
        check(bool(automorphisms[group]))
    whole = frozenset(elements)
    def core(group, h):
        return frozenset.intersection(*(frozenset(f[x] for x in h)
                                        for f in automorphisms[group]))
    proper = [h for h in subs if h != whole]
    families = 0
    for u, v in itertools.product(proper, repeat=2):
        family = [whole, u, v]
        initial = u & v
        h = initial
        while True:
            old = h
            for group in family:
                h = core(group, h)
                check(h <= old)
            if h == old:
                break
        valid = [k for k in subs if k <= initial and
                 all(core(group, k) == k for group in family)]
        check(h in valid)
        check(all(k <= h for k in valid))
        families += 1
    core_summary.append({'group': name, 'subgroups': len(subs),
                         'whole_automorphisms': len(automorphisms[whole]),
                         'three_group_families': families})

def matrix_product(a, b):
    return [[sum(x*y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]

def matrix_power(a, n):
    result = [[int(i == j) for j in range(len(a))] for i in range(len(a))]
    while n:
        if n & 1:
            result = matrix_product(result, a)
        a = matrix_product(a, a); n //= 2
    return result

def determinant(a):
    a = [row[:] for row in a]
    sign = 1; previous = 1
    for k in range(len(a)-1):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]; sign *= -1
        value = a[k][k]
        for i in range(k+1, len(a)):
            for j in range(k+1, len(a)):
                numerator = value*a[i][j] - a[i][k]*a[k][j]
                check(numerator % previous == 0)
                a[i][j] = numerator // previous
        previous = value
    return sign*a[-1][-1]

# Integral augmentation-lattice determinant/norm controls use basis matrices
# and repeated squaring, rather than author recurrence or prior binomial sums.
valuation_summary = []
for p in [2, 3, 5, 7, 11, 17, 23]:
    n = p-1
    cols = []
    for j in range(1, p):
        vector = [0]*p; vector[j] = 1; vector[0] = -1
        shifted_minus = [vector[(i-1) % p] - vector[i] for i in range(p)]
        cols.append(shifted_minus[1:])
    t = [list(row) for row in zip(*cols)]
    check(determinant(t) == (-1)**n*p)
    power = matrix_power(t, n)
    check(all(x % p == 0 for row in power for x in row))
    b = [[x // p for x in row] for row in power]
    check(abs(determinant(b)) == 1)
    for a in [0, 1, 2, 3, 7, 11]:
        for remainder in [0, max(0, n-1)]:
            k = a*n+remainder+1
            result = matrix_power(t, k-1)
            # T e0 has augmentation coordinates (1,0,...,0).
            coordinates = [row[0] for row in result]
            ambient = [-sum(coordinates)] + coordinates
            def valuation(x):
                if not x:
                    return math.inf
                count = 0
                while x % p == 0:
                    x //= p; count += 1
                return count
            check(min(valuation(x) for x in ambient) == a)
            for e in [1, 2, 7, 11]:
                check(all(x % (p**e) == 0 for x in ambient) == (a >= e))
    valuation_summary.append({'p': p, 'augmentation_rank': n,
                              'determinant_abs': p, 'unit_B': True})

# Prime-power Heisenberg quotients deliberately expose extra finite centers.
# Z(U mod p^e) is larger than the image of the actual p-adic Z(U).
heisenberg_summary = []
for p, e in [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (5, 1)]:
    q = p**e
    elements = list(itertools.product(range(q), repeat=3))
    def mul(a, b):
        return ((a[0]+b[0]) % q, (a[1]+b[1]) % q,
                (a[2]+b[2]+a[0]*b[1]) % q)
    def theta(a):
        return (a[1], a[0], (a[0]*a[1]-a[2]) % q)
    u = [a for a in elements if a[0] % p == 0]
    center = {a for a in u if all(mul(a, b) == mul(b, a) for b in u)}
    predicted = {(0, b, c) for b in range(q) for c in range(q)
                 if p*b % q == 0}
    genuine_center_image = {(0, 0, c) for c in range(q)}
    check(center == predicted)
    check(genuine_center_image < center)
    for a in elements:
        check(theta(theta(a)) == a)
        for b in elements:
            check(theta(mul(a, b)) == mul(theta(a), theta(b)))
    heisenberg_summary.append({'p': p, 'e': e, 'quotient_order': q**3,
                              'finite_U_center_order': len(center),
                              'p_adic_center_image_order': q})

# Nonabelian lamp multiplication: conjugation moves noncommuting elements to
# commuting distinct factors; all nonidentity lamps still separate, at p=2.
wreath_summary = []
for q, top in [(4, 2), (4, 4), (3, 3)]:
    lamp = list(itertools.product(range(q), repeat=3))
    zero = (0, 0, 0)
    def lm(a, b):
        return ((a[0]+b[0]) % q, (a[1]+b[1]) % q,
                (a[2]+b[2]+a[0]*b[1]) % q)
    def shift(a, index):
        return tuple(a[(i-index) % top] for i in range(top))
    def wreath(a, b):
        shifted = shift(b[0], a[1])
        return tuple(lm(x, y) for x, y in zip(a[0], shifted)), (a[1]+b[1]) % top
    blank = tuple([zero]*top)
    s = (blank, 1); inverse_s = (blank, top-1)
    for a in lamp:
        original = ((a,) + tuple([zero]*(top-1)), 0)
        moved = wreath(wreath(s, original), inverse_s)
        check(moved[0] == shift(original[0], 1))
        check((moved != original) == (a != zero))
        for b in lamp:
            displaced = (tuple([zero])+(b,)+tuple([zero]*(top-2)), 0)
            check(wreath(original, displaced) == wreath(displaced, original))
    wreath_summary.append({'Heisenberg_lamp_modulus': q,
                           'lamp_order': q**3, 'cyclic_top_order': top})

print(json.dumps({'result': 'PASS', 'assertions': checks,
                  'module_enumerations': module_summary,
                  'three_family_core_controls': core_summary,
                  'augmentation_matrix_controls': valuation_summary,
                  'finite_extra_center_controls': heisenberg_summary,
                  'nonabelian_wreath_controls': wreath_summary,
                  'scope': 'New exact finite boundary controls only; no author imports; no infinite solution claim'},
                 indent=2, sort_keys=True))
