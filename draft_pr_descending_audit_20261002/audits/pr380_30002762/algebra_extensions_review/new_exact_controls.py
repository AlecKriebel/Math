#!/usr/bin/env python3
"""Fresh exact group-law controls. No candidate or previous-review imports."""
from fractions import Fraction
from itertools import combinations
import hashlib
import json
import random
from pathlib import Path

HEAD = "9946a67cf8a1f7e3130d2a12de902db05875283a"
RNG = random.Random(38030002762)
COUNT = {}


def check(label, assertion):
    if not assertion:
        raise AssertionError(label)
    COUNT[label] = COUNT.get(label, 0) + 1


def power(g, n, mul, inv, identity):
    if n < 0:
        g, n = inv(g), -n
    ans = identity
    while n:
        if n & 1:
            ans = mul(ans, g)
        g = mul(g, g)
        n >>= 1
    return ans


def comm(g, h, mul, inv):
    return mul(mul(mul(g, h), inv(g)), inv(h))


# A: actual free class-two multiplication, not a derived-group-only model.
class ClassTwo:
    def __init__(self, rank):
        self.rank = rank
        self.pairs = tuple(combinations(range(rank), 2))
        self.identity = ((0,) * rank, (0,) * len(self.pairs))
        self.generators = []
        for i in range(rank):
            v = tuple(int(i == j) for j in range(rank))
            self.generators.append((v, self.identity[1]))

    def mul(self, a, b):
        x, z = a
        y, w = b
        return (tuple(v + u for v, u in zip(x, y)),
                tuple(z[k] + w[k] + x[i] * y[j]
                      for k, (i, j) in enumerate(self.pairs)))

    def inv(self, a):
        x, z = a
        return (tuple(-v for v in x),
                tuple(-z[k] + x[i] * x[j]
                      for k, (i, j) in enumerate(self.pairs)))

    def pow(self, a, n):
        return power(a, n, self.mul, self.inv, self.identity)


N4 = ClassTwo(4)
for _ in range(1400):
    x = tuple(RNG.randrange(-11, 12) for _ in range(4))
    y = tuple(RNG.randrange(-11, 12) for _ in range(4))
    z = tuple(RNG.randrange(-21, 22) for _ in range(6))
    w = tuple(RNG.randrange(-21, 22) for _ in range(6))
    a, b = (x, z), (y, w)
    check("class_two_inverse", N4.mul(a, N4.inv(a)) == N4.identity)
    actual = comm(a, b, N4.mul, N4.inv)
    expected = tuple(x[i] * y[j] - y[i] * x[j] for i, j in N4.pairs)
    check("class_two_actual_commutator", actual == ((0,) * 4, expected))
    pfaff = expected[0] * expected[5] - expected[1] * expected[4] + expected[2] * expected[3]
    check("single_commutator_pfaffian_zero", pfaff == 0)
    result = N4.identity
    for val, (i, j) in zip(z, N4.pairs):
        term = comm(N4.pow(N4.generators[i], val), N4.generators[j], N4.mul, N4.inv)
        result = N4.mul(result, term)
    check("class_two_six_commutator_certificate", result == ((0,) * 4, z))
    check("class_two_bound20_contains_certificate12", 2 * len(N4.pairs) <= 4 * 5)
    n = RNG.randrange(-13, 14)
    check("class_two_signed_power", N4.pow(N4.pow(a, n), -1) == N4.pow(a, -n))
non_single = (1, 0, 0, 0, 0, 1)
check("rank_four_not_single_commutator", non_single[0] * non_single[5] - non_single[1] * non_single[4] + non_single[2] * non_single[3] == 1)


# B: integer Laurent lamps, semidirect the actual infinite dihedral group.
def clean(p):
    return {i: v for i, v in p.items() if v}


def padd(p, q):
    a = dict(p)
    for i, v in q.items():
        a[i] = a.get(i, 0) + v
    return clean(a)


def dact(n, e, p):
    return {n + (-1) ** e * i: v for i, v in p.items()}


DID = ({}, 0, 0)


def dmul(a, b):
    p, n, e = a
    q, m, f = b
    return (padd(p, dact(n, e, q)), n + (-1) ** e * m, (e + f) % 2)


def dinv(a):
    p, n, e = a
    m = -(-1) ** e * n
    return (dact(m, e, {i: -v for i, v in p.items()}), m, e)


def dpow(a, n):
    return power(a, n, dmul, dinv, DID)


T, REFLECT, LAMP = ({}, 1, 0), ({}, 0, 1), ({0: 1}, 0, 0)


def lamp_difference_preimage(p):
    assert sum(p.values()) == 0
    if not p:
        return {}
    previous = 0
    ans = {}
    for k in range(min(p), max(p) + 1):
        previous += p.get(k, 0)
        if previous:
            ans[k] = previous
    assert previous == 0
    return ans


def dihedral_lamp_certificate(a):
    p, n, e = a
    zero_lamp = comm((lamp_difference_preimage(p), 0, 0), T, dmul, dinv)
    half, odd = divmod(n, 2)
    translation = comm(dpow(T, half), REFLECT, dmul, dinv)
    if odd:
        translation = dmul(translation, T)
    if e:
        translation = dmul(translation, REFLECT)
    return dmul(zero_lamp, translation), 2 + 2 + odd + e


for _ in range(1600):
    p = clean({k: RNG.randrange(-12, 13) for k in range(-8, 9)})
    p[0] = p.get(0, 0) - sum(p.values())
    p = clean(p)
    a = (p, RNG.randrange(-30, 31), RNG.randrange(2))
    q = clean({k: RNG.randrange(-7, 8) for k in range(-5, 6)})
    b = (q, RNG.randrange(-20, 21), RNG.randrange(2))
    check("dihedral_lamp_inverse", dmul(a, dinv(a)) == DID)
    check("dihedral_lamp_mass_homomorphism", sum(dmul(a, b)[0].values()) == sum(p.values()) + sum(q.values()))
    for n in (-9, -4, -1, 0, 1, 3, 8):
        actual = dpow(a, n)
        cert, norm_upper = dihedral_lamp_certificate(actual)
        check("dihedral_lamp_signed_power_certificate", cert == actual)
        check("dihedral_lamp_uniform_zero_mass_bound6", norm_upper <= 6)
    even = (p, 2 * RNG.randrange(-100, 101), 0)
    cert, upper = dihedral_lamp_certificate(even)
    check("virtually_metabelian_derived_bound4", cert == even and upper == 4)
check("finite_index_intrinsic_vs_ambient_gap", dihedral_lamp_certificate(dpow(T, 102))[1] <= 4 and 102 > 4)
check("bare_dihedral_even_translation_two_letters", comm(dpow(T, 51), REFLECT, dmul, dinv) == dpow(T, 102))
# Nonzero masses are detected by a homomorphism, including signed powers.
for mass in range(-9, 10):
    a = ({0: mass, 3: 4, -6: -4}, 17, 1)
    for n in range(-10, 11):
        check("lamp_mass_signed_linear_detection", sum(dpow(a, n)[0].values()) == n * mass)


# Normal generation without ordinary finite generation: increasing exact slices
# of an infinite direct sum of dyadic rationals, with t acting by doubling.
for dim in range(1, 14):
    identity = ((Fraction(0),) * dim, 0)
    t = (identity[0], 1)

    def rmul(g, h):
        a, n = g
        b, m = h
        return (tuple(x + Fraction(2) ** n * y for x, y in zip(a, b)), n + m)

    def rinv(g):
        a, n = g
        return (tuple(-Fraction(2) ** (-n) * x for x in a), -n)

    for _ in range(140):
        a = tuple(Fraction(RNG.randrange(-40, 41), 2 ** RNG.randrange(8)) for _ in range(dim))
        g = (a, 0)
        check("normally_one_generator_actual_commutator", comm(g, t, rmul, rinv) == (tuple(-x for x in a), 0))
        check("dyadic_semidirect_inverse", rmul(g, rinv(g)) == identity)


# C: free-group words plus a noncommuting integral matrix action.
P = ((1, 2), (0, 1))
U = ((1, 0), (2, 1))
MINUS_P = ((1, -2), (0, 1))
MINUS_U = ((1, 0), (-2, 1))
I2 = ((1, 0), (0, 1))
MATS = {1: P, 2: U, -1: MINUS_P, -2: MINUS_U}


def mmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def mv(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(2)) for i in range(2))


def freduce(word):
    ans = []
    for x in word:
        if ans and ans[-1] == -x:
            ans.pop()
        else:
            ans.append(x)
    return tuple(ans)


def winv(word):
    return tuple(-x for x in reversed(word))


def action(word):
    m = I2
    for x in word:
        m = mmul(m, MATS[x])
    return m


FID = ((0, 0), ())


def fmul(g, h):
    a, q = g
    b, r = h
    mb = mv(action(q), b)
    return (tuple(a[i] + mb[i] for i in range(2)), freduce(q + r))


def finv(g):
    a, q = g
    qi = winv(q)
    return (tuple(-x for x in mv(action(qi), a)), qi)


def fpow(g, n):
    return power(g, n, fmul, finv, FID)


Q1, Q2 = ((0, 0), (1,)), ((0, 0), (2,))


def pi(g):
    return (tuple(v % 2 for v in g[0]), g[1])


def hmul(g, h):
    return (tuple((g[0][i] + h[0][i]) % 2 for i in range(2)), freduce(g[1] + h[1]))


def four_letter_certificate(v):
    assert all(x % 2 == 0 for x in v)
    a = ((0, -v[0] // 2), ())
    b = ((-v[1] // 2, 0), ())
    return fmul(comm(a, Q1, fmul, finv), comm(b, Q2, fmul, finv))


def brooks_raw(word):
    return sum(int((a, b) == (1, 2)) - int((a, b) == (-2, -1)) for a, b in zip(word, word[1:]))


def brooks_homogeneous(word):
    core = list(word)
    while len(core) >= 2 and core[0] == -core[-1]:
        core = core[1:-1]
    if len(core) < 2:
        return 0
    return sum(int((core[i], core[(i + 1) % len(core)]) == (1, 2))
               - int((core[i], core[(i + 1) % len(core)]) == (-2, -1))
               for i in range(len(core)))


check("split_action_is_noncommutative", mmul(P, U) != mmul(U, P))
max_defect = 0
for _ in range(4000):
    q = freduce(tuple(RNG.choice((-2, -1, 1, 2)) for _ in range(RNG.randrange(20))))
    r = freduce(tuple(RNG.choice((-2, -1, 1, 2)) for _ in range(RNG.randrange(20))))
    a = tuple(RNG.randrange(-80, 81) for _ in range(2))
    b = tuple(RNG.randrange(-80, 81) for _ in range(2))
    g, h = (a, q), (b, r)
    check("split_exact_inverse", fmul(g, finv(g)) == FID)
    check("split_projection_is_homomorphism", pi(fmul(g, h)) == hmul(pi(g), pi(h)))
    check("noncommuting_action_all_congruence_identity", all((action(q)[i][j] - I2[i][j]) % 2 == 0 for i in range(2) for j in range(2)))
    v = tuple(2 * RNG.randrange(-1000, 1001) for _ in range(2))
    check("split_kernel_four_letter_certificate", four_letter_certificate(v) == (v, ()))
    qa = mv(action(q), a)
    v = tuple(qa[i] - a[i] for i in range(2))
    check("arbitrary_word_coboundary_grouped_into_two", four_letter_certificate(v) == (v, ()))
    d = abs(brooks_homogeneous(fmul(g, h)[1]) - brooks_homogeneous(q) - brooks_homogeneous(r))
    max_defect = max(max_defect, d)
    check("ordinary_quasimorphism_global_defect12_control", d <= 12)
    check("homogeneous_vs_raw_distance3_control", abs(brooks_homogeneous(q) - brooks_raw(q)) <= 3)
    n = RNG.randrange(-8, 9)
    check("ordinary_quasimorphism_pullback_signed_homogeneity", brooks_homogeneous(fpow(g, n)[1]) == n * brooks_homogeneous(q))
qcomm = (1, 2, -1, -2)
check("ordinary_nonhomomorphism_detection", brooks_homogeneous(qcomm) == 1 and sum(qcomm.count(i) - qcomm.count(-i) for i in (1, 2)) == 0)
for v in ((0, 0), (2, 6), (-100, 42)):
    g = (v, qcomm)
    for n in range(-12, 13):
        check("same_domain_quasimorphism_detects_kernel_perturbations", brooks_homogeneous(fpow(g, n)[1]) == n)


# D: nonsplit extension has a cocycle; central coordinate is not additive.
H3 = ClassTwo(2)
x, y = H3.generators
check("nonsplit_central_coordinate_not_homomorphism", H3.mul(x, y)[1][0] == 1 and x[1][0] + y[1][0] == 0)
for n in range(-100, 101):
    check("heisenberg_central_infinite_bounded_powers", comm(H3.pow(x, n), y, H3.mul, H3.inv) == ((0, 0), (n,)))


result = {
    "pass": True,
    "head": HEAD,
    "seed": 38030002762,
    "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "total_exact_assertions": sum(COUNT.values()),
    "assertions_by_family": COUNT,
    "observed_brooks_homogeneous_defect_max": max_defect,
    "universal_vs_empirical": "The universal arguments are in INDEPENDENT_RECONSTRUCTION.md; finite controls check exact group laws and reject invalid boundary assumptions, not universal theorem proofs.",
    "independence": "Written and sealed before TURN/FINAL/old/sibling/root verdict reads; no candidate imports; RNG fixed; rational and integer arithmetic only.",
}
print(json.dumps(result, indent=2, sort_keys=True))
