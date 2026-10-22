"""Exact controls for two unrestricted SU(3) partial theorems.

The finite checks supplement the all-weight proofs in TURN_4.md; they are not
a positivity classification beyond the precise theorem hypotheses.
"""
from fractions import Fraction as F
from itertools import permutations
from collections import Counter
import hashlib
import json

checks = Counter()


def ck(value, label):
    assert value, label
    checks[label] += 1


def add(a, b, scalar=1):
    c = dict(a)
    for key, value in b.items():
        c[key] = c.get(key, 0) + scalar * value
    return {key: value for key, value in c.items() if value}


def mul(a, b):
    c = {}
    for (i, j), v in a.items():
        for (k, l), w in b.items():
            c[i + k, j + l] = c.get((i + k, j + l), 0) + v * w
    return {key: value for key, value in c.items() if value}


def power(a, n):
    out = {(0, 0): 1}
    for _ in range(n):
        out = mul(out, a)
    return out


def swap(a):
    return {(j, i): c for (i, j), c in a.items()}


def shift(a, x, y):
    return {(i + x, j + y): c for (i, j), c in a.items()}


def character_table(bound):
    cs = {(0, 0): {(0, 0): 1}}
    for n in range(1, bound + 1):
        for a in range(n, 0, -1):
            b = n - a
            cs[a, b] = add(add(shift(cs[a - 1, b], 1, 0),
                                 cs.get((a - 2, b + 1), {}), -1),
                           cs.get((a - 1, b - 1), {}), -1)
        cs[0, n] = swap(cs[n, 0])
    return cs


def substitute(p, upowers, vpowers):
    out = {}
    for (a, b), c in p.items():
        out = add(out, mul(upowers[a], vpowers[b]), c)
    return out


def alt(exps):
    eig = [(1, 0), (0, 1), (-1, -1)]
    out = {}
    for perm in permutations(range(3)):
        inversions = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3))
        e = tuple(sum(exps[i] * eig[perm[i]][j] for i in range(3)) for j in range(2))
        out[e] = out.get(e, 0) + (-1) ** inversions
    return {e: c for e, c in out.items() if c}


def decompose(poly, cs):
    out = {}
    while poly:
        key = max(poly, key=lambda e: (sum(e), e))
        c = poly[key]
        out[key] = out.get(key, 0) + c
        poly = add(poly, cs[key], -c)
    return {e: c for e, c in out.items() if c}


BOUND = 10
cs = character_table(2 * BOUND)
u = {(1, 0): 1, (0, 1): 1, (-1, -1): 1}
v = {(-i, -j): c for (i, j), c in u.items()}
upowers = [power(u, n) for n in range(2 * BOUND + 1)]
vpowers = [power(v, n) for n in range(2 * BOUND + 1)]
den = alt((2, 1, 0))
for (a, b), ch in cs.items():
    ck(ch.get((a, b)) == 1, 'triangular_character_leading_term')
    ck(all(i + j < a + b for i, j in ch if (i, j) != (a, b)), 'triangular_lower_terms')
    ck(swap(ch) == cs[b, a], 'conjugation_formula')
    if a + b <= BOUND:
        torus = substitute(ch, upowers, vpowers)
        ck(mul(den, torus) == alt((a + b + 2, b + 1, 0)), 'independent_weyl_formula')
        ck(sum(torus.values()) == (a + 1) * (b + 1) * (a + b + 2) // 2, 'dimension_formula')

diagonal_records = []
for a in range(BOUND + 1):
    for b in range(BOUND + 1 - a):
        n = a + b
        dec = decompose(mul(cs[a, b], cs[b, a]), cs)
        ck(all(c >= 0 for c in dec.values()), 'ordinary_tensor_product_nonnegative')
        ck(dec.get((n, n)) == 1, 'highest_diagonal_multiplicity_one')
        ck(dec.get((0, 0)) == 1, 'haar_mean_one')
        for k in range(n + 1):
            expected = min(a, b, k, n - k) + 1
            count = max(0, min(a, k) - max(0, k - b) + 1)
            ck(dec.get((k, k), 0) == expected, 'diagonal_tensor_multiplicity')
            ck(count == expected, 'tableau_parameter_count')
            diagonal_records.append([a, b, k, expected])
        for k in range(1, n // 2 + 1):
            difference = dec.get((k, k), 0) - dec.get((k - 1, k - 1), 0)
            ck(difference == int(min(a, b) >= k), 'threshold_moment_identity')

# Exact Laurent identity underlying the self-dual negative witnesses.
# Set z=s^2, so trace(diag(1,z,z^-1))=1+s^2+s^-2.
trace = {(0, 0): 1, (2, 0): 1, (-2, 0): 1}
tp = [power(trace, n) for n in range(2 * BOUND + 1)]
denline = mul(power({(1, 0): 1, (-1, 0): -1}, 2), {(2, 0): 1, (-2, 0): -1})
for a in range(BOUND + 1):
    n = a + 1
    chline = substitute(cs[a, a], tp, tp)
    num = mul(power({(n, 0): 1, (-n, 0): -1}, 2), {(2 * n, 0): 1, (-2 * n, 0): -1})
    ck(mul(chline, denline) == num, 'self_dual_principal_laurent_identity')
    ck((a + 1) ** 3 == (a + 1) * (a + 1) * (2 * a + 2) // 2, 'self_dual_dimension_cube')

at_three_halves = sum(F(c) * F(3, 2) ** (i + j) for (i, j), c in cs[2, 2].items())
ck(at_three_halves == F(-27, 16), 'a_equals_two_negative_witness')
ck(F(-27, 16) < -1, 'strict_negative_affine_value')
ck(cs[1, 1] == {(1, 1): 1, (0, 0): -1}, 'adjoint_square_identity')

print(json.dumps({
    'status': 'PASS_EXACT_ALGEBRA_CONTROLS',
    'completed_substantive_author_turns': 4,
    'original_status': 'unresolved',
    'assertions': sum(checks.values()),
    'counts': dict(sorted(checks.items())),
    'tensor_products_checked': (BOUND + 1) * (BOUND + 2) // 2,
    'tensor_product_weight_bound': BOUND,
    'self_dual_laurent_identities_checked': BOUND + 1,
    'diagonal_record_sha256': hashlib.sha256(json.dumps(diagonal_records, separators=(',', ':')).encode()).hexdigest(),
    'scope': 'Controls for the all-weight affine-single-irrep and integral-convex-square theorems of TURN_4.md. The universal statements are proved there; no finite support cutoff is asserted for arbitrary S-characters.',
}, indent=2, sort_keys=True))
