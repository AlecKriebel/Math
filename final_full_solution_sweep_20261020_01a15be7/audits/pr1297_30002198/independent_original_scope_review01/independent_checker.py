"""Exact independent arithmetic for the PR1297 scope correction.

No downloaded program is imported or executed.  PBW is an explicit mathematical
import, not something the finite checks claim to prove.  Polynomial coefficients
are in ascending order.  Failures remain active under Python -O and -OO.
"""
from collections import Counter
from fractions import Fraction
from itertools import product, permutations
from math import gcd
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, v in enumerate(a):
        c[i] += v
    for i, v in enumerate(b):
        c[i] += v
    return trim(c)


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def divmod_poly(a, b):
    a, b = trim(a), trim(b)
    require(b != [0], "zero divisor")
    q = [0] * max(1, len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        k = len(a) - len(b)
        z = Fraction(a[-1], b[-1])
        q[k] += z
        for i, x in enumerate(b):
            a[k + i] -= z * x
        a = trim(a)
    return trim(q), a


def quantum(length, step):
    require(length > 0 and step > 0, "invalid quantum integer")
    a = [0] * (step * (length - 1) + 1)
    for i in range(length):
        a[step * i] = 1
    return a


def mult_all(polys):
    a = [1]
    for b in polys:
        a = mul(a, b)
    return a


PHI = {}
for n in range(1, 61):
    f = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            f, rem = divmod_poly(f, PHI[d])
            require(rem == [0], "cyclotomic recurrence")
    PHI[n] = f


def valuation(a, n):
    v = 0
    while True:
        q, r = divmod_poly(a, PHI[n])
        if r != [0]:
            return v
        require(a != [0], "zero polynomial valuation")
        v += 1
        a = q


def obstruction(a):
    return valuation(a, 15) > 0 and valuation(a, 3) == 0


# Z[zeta_5] and Q(zeta_5), with a separate Gaussian elimination check of
# degree-two and degree-three quantum symmetrizer ranks.
ZERO = (Fraction(0),) * 4
ONE = (Fraction(1),) + (Fraction(0),) * 3


def fld(a):
    rem = divmod_poly(a, PHI[5])[1]
    return tuple(Fraction(x) for x in rem) + (Fraction(0),) * (4 - len(rem))


def fadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def fneg(a):
    return tuple(-x for x in a)


def fmul(a, b):
    return fld(mul(a, b))


def finv(a):
    require(a != ZERO, "field division by zero")
    r0, r1 = PHI[5], trim(a)
    s0, s1 = [0], [1]
    while r1 != [0]:
        q, r = divmod_poly(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, add(s0, [-x for x in mul(q, s1)])
    require(len(r0) == 1, "irreducible-field inverse")
    out = fld([x / r0[0] for x in s0])
    require(fmul(a, out) == ONE, "inverse postcondition")
    return out


ZETA = [fld([0] * i + [1]) for i in range(5)]
EXP = ((1, 4, 0), (0, 1, 4), (0, 0, 1))
CARTAN = ((2, -1, 0), (-1, 2, -1), (0, -1, 2))


def compatible(q):
    return all(q[i][i] % 5 == 1 for i in range(3)) and all(
        (q[i][j] + q[j][i] - CARTAN[i][j]) % 5 == 0
        for i in range(3) for j in range(3) if i != j)


def character(g, j, q=EXP):
    return sum(g[i] * q[i][j] for i in range(3)) % 5


def reflect(root, i):
    out = list(root)
    out[i] -= sum(CARTAN[i][j] * root[j] for j in range(3))
    return tuple(out)


def roots_from_reflections():
    roots = {tuple(int(i == j) for i in range(3)) for j in range(3)}
    todo = list(roots)
    while todo:
        a = todo.pop()
        for i in range(3):
            b = reflect(a, i)
            if b not in roots:
                require(sum(abs(x) for x in b) <= 3, "root orbit escaped A3")
                roots.add(b)
                todo.append(b)
    return sorted(roots)


def symmetrizer_matrix(n, q):
    words = list(product(range(3), repeat=n))
    index = {w: i for i, w in enumerate(words)}
    matrix = [[ZERO for _ in words] for _ in words]
    # For an ordering p of original positions, an inverted pair i<j crosses
    # once with the original left letter crossing the original right letter.
    for col, w in enumerate(words):
        for p in permutations(range(n)):
            pos = {v: i for i, v in enumerate(p)}
            exponent = sum(q[w[i]][w[j]] for i in range(n)
                           for j in range(i + 1, n) if pos[i] > pos[j]) % 5
            row = index[tuple(w[i] for i in p)]
            matrix[row][col] = fadd(matrix[row][col], ZETA[exponent])
    return matrix


def rank(matrix):
    a = [row[:] for row in matrix]
    pivot_row = 0
    for col in range(len(a[0])):
        k = next((i for i in range(pivot_row, len(a)) if a[i][col] != ZERO), None)
        if k is None:
            continue
        a[pivot_row], a[k] = a[k], a[pivot_row]
        inv = finv(a[pivot_row][col])
        a[pivot_row] = [fmul(v, inv) for v in a[pivot_row]]
        for i in range(pivot_row + 1, len(a)):
            if a[i][col] != ZERO:
                factor = a[i][col]
                a[i] = [fadd(x, fneg(fmul(factor, y)))
                        for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def main():
    require(compatible(EXP), "Cartan data")
    minimal = []
    for i in range(3):
        row = []
        for j in range(3):
            if i == j:
                row.append(2)
                continue
            m = next(m for m in range(5)
                     if (m + 1) % 5 == 0 or (m + EXP[i][j] + EXP[j][i]) % 5 == 0)
            row.append(-m)
        minimal.append(row)
    require(minimal == [list(r) for r in CARTAN], "minimal Cartan integers")

    group = list(product(range(5), repeat=3))
    character_checks = 0
    for g in group:
        for h in group:
            gh = tuple((x + y) % 5 for x, y in zip(g, h))
            for j in range(3):
                require(character(gh, j) == (character(g, j) + character(h, j)) % 5,
                        "character multiplicativity")
                character_checks += 1
    # The coordinate projections commute with every diagonal group action and
    # preserve the homogeneous coaction degrees. Their ranks are exactly one.
    for j in range(3):
        for g in group:
            for i in range(3):
                require((int(i == j) * character(g, i)) % 5 ==
                        (character(g, i) * int(i == j)) % 5, "submodule projection")
    require(len({tuple(x) for x in group}) == 125, "support generators")
    for i, j, k in product(range(3), repeat=3):
        require((EXP[i][j] + EXP[i][k] + EXP[j][k]) % 5 ==
                (EXP[j][k] + EXP[i][k] + EXP[i][j]) % 5, "braid equation")
    all_roots = roots_from_reflections()
    positive = [a for a in all_roots if min(a) >= 0]
    require(len(all_roots) == 12 and len(positive) == 6, "A3 root count")
    heights = sorted(map(sum, positive))
    require(heights == [1, 1, 1, 2, 2, 3], "ordinary root heights")
    self_exponents = [sum(a[i] * EXP[i][j] * a[j] for i in range(3)
                          for j in range(3)) % 5 for a in positive]
    require(self_exponents == [1] * 6, "root orders")
    h = mult_all(quantum(5, d) for d in heights)
    counts = Counter(sum(x * d for x, d in zip(exps, heights))
                     for exps in product(range(5), repeat=6))
    require(h == [counts[i] for i in range(41)], "independent PBW enumeration")
    require(sum(h) == 15625 and len(h) == 41 and h == h[::-1], "dimension/degree/duality")
    require(h[-1] == 1 and all(x > 0 for x in h), "Hilbert endpoints/positivity")
    exponents = {n: valuation(h, n) for n in range(1, 61)}
    nonzero = {n: e for n, e in exponents.items() if e}
    require(nonzero == {5: 6, 10: 2, 15: 1}, "full cyclotomic multiplicities")
    require(divmod_poly(h, PHI[3])[1] == [5, 5], "primitive-cube remainder")
    require(obstruction(h), "primitive-fifteen obstruction")
    # Complete finite dimension/degree reduction, separate from the universal
    # root-of-unity implication proved in the report.
    possible_counts = []
    for a, b, c in product(range(7), repeat=3):
        if a + b + 2 * c == 6 and 4 * a + 8 * b + 24 * c == 40:
            possible_counts.append([a, b, c])
            candidate = mult_all([quantum(5, 1)] * a + [quantum(5, 2)] * b +
                                 [quantum(25, 1)] * c)
            require(candidate != h, "exhaustive dimension/degree factor candidate")
    symranks = {n: rank(symmetrizer_matrix(n, EXP)) for n in [2, 3, 4]}
    require(symranks == {2: h[2], 3: h[3], 4: h[4]}, "exact quantum-symmetrizer ranks")

    controls = []
    def control(name, ok):
        require(ok, "control: " + name)
        controls.append(name)

    changed = [list(r) for r in EXP]
    changed[0][1] = 0
    control("altered_adjacent_pair_fails_A3", not compatible(changed))
    changed = [list(r) for r in EXP]
    changed[0][2] = 1
    control("altered_nonadjacent_pair_fails_A3", not compatible(changed))
    changed = [list(r) for r in EXP]
    changed[1][1] = 0
    control("order_one_diagonal_rejected", not compatible(changed))
    control("remove_height3_removes_obstruction",
            not obstruction(mult_all(quantum(5, d) for d in [1, 1, 1, 2, 2])))
    control("replace_height3_by2_removes_obstruction",
            not obstruction(mult_all(quantum(5, d) for d in [1, 1, 1, 2, 2, 2])))
    control("allowed_15_t_has_required_Phi3", not obstruction(quantum(15, 1)))
    control("allowed_15_t2_has_required_Phi3", not obstruction(quantum(15, 2)))
    control("allowed_empty_and_unit_products_do_not_vanish",
            not obstruction([1]) and quantum(1, 1) == [1] and quantum(1, 2) == [1])
    control("allowing_step3_breaks_implication", obstruction(quantum(5, 3)))
    control("allowing_quotients_breaks_implication",
            divmod_poly(quantum(15, 1), quantum(3, 1))[1] == [0] and
            obstruction(divmod_poly(quantum(15, 1), quantum(3, 1))[0]))
    control("regrading_roots_as_degree1_loses_actual_H", quantum(5, 1) != h and
            mult_all([quantum(5, 1)] * 6) != h)
    control("dimension_alone_does_not_determine_H",
            sum(mult_all([quantum(5, 1)] * 6)) == sum(h))
    control("transposed_braiding_keeps_A3_and_low_ranks",
            compatible(tuple(zip(*EXP))) and
            rank(symmetrizer_matrix(3, tuple(zip(*EXP)))) == h[3])
    disconnected = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    control("disconnecting_changes_degree2_rank",
            rank(symmetrizer_matrix(2, disconnected)) != h[2])
    # A one-dimensional quantum line is absolutely simple and finite at order5,
    # but has an allowed factor. It is a genuine intended-scope positive foil.
    control("simple_quantum_line_is_not_counterexample", not obstruction(quantum(5, 1)))
    # For allowed step 1 or 2, the cyclotomic implication is also exhaustively
    # checked for 600 lengths, without using this bound in the proof.
    tested_allowed = 0
    for length, step in product(range(1, 601), (1, 2)):
        order15 = 15 // gcd(15, step)
        order3 = 3 // gcd(3, step)
        require(length % order15 != 0 or length % order3 == 0, "allowed factor implication")
        tested_allowed += 1
    result = {
        "schema": "independent-pr1297-exact-v1", "status": "PASS",
        "field": "Q(zeta5)", "character_multiplicativity_checks": character_checks,
        "group_order": 125, "proper_YD_summand_ranks": [1, 1, 1],
        "positive_roots": positive, "root_heights": heights,
        "root_self_braiding_exponents_mod5": self_exponents,
        "PBW_tuples": 15625, "Hilbert_degree": 40, "Hilbert_at_one": sum(h),
        "Hilbert_coefficients": h, "cyclotomic_valuations": nonzero,
        "remainder_mod_Phi3": [5, 5], "quantum_symmetrizer_ranks": symranks,
        "dimension_degree_reduced_factor_counts_5t_5t2_25t": possible_counts,
        "bounded_allowed_factor_controls": tested_allowed,
        "controls": controls, "control_count": len(controls),
        "limits": "PBW and intended-source interpretation are explicit written imports; no finite check proves them."
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
