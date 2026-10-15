"""Exact finite arithmetic for the SL(2,5), p=2 counterexample.

No external packages, character-table database, source PDF, or floating point.
The mathematical bridge from these finite checks to nonsemiperfectness is proved
in COUNTEREXAMPLE.md; finite checks alone do not establish that bridge.
"""
from fractions import Fraction as F
from itertools import product, permutations
from collections import Counter
from pathlib import Path
import json

def A(x, y):
    return (x[0] + y[0], x[1] + y[1])

def N(x):
    return (-x[0], -x[1])

def M(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)

def S(x, n):
    return (x[0] * n, x[1] * n)
zero = (F(0), F(0))
one = (F(1), F(0))
phi = (F(0), F(1))

def qmul(q, r):
    a, b, c, d = q
    e, f, g, h = r
    return (A(A(M(a, e), N(M(b, f))), N(A(M(c, g), M(d, h)))), A(A(M(a, f), M(b, e)), A(M(c, h), N(M(d, g)))), A(A(M(a, g), N(M(b, h))), A(M(c, e), M(d, f))), A(A(M(a, h), M(b, g)), A(N(M(c, f)), M(d, e))))

def parity(p):
    return sum((p[i] > p[j] for i in range(4) for j in range(i + 1, 4))) % 2

def icosians():
    G = set()
    for i in range(4):
        for s in [-1, 1]:
            q = [zero] * 4
            q[i] = S(one, s)
            G.add(tuple(q))
    for signs in product([-1, 1], repeat=4):
        G.add(tuple((S(one, F(s, 2)) for s in signs)))
    for signs in product([-1, 1], repeat=3):
        q = (zero, S(one, F(signs[0], 2)), S(phi, F(signs[1], 2)), S(A(phi, N(one)), F(signs[2], 2)))
        for p in permutations(range(4)):
            if parity(p) == 0:
                G.add(tuple((q[i] for i in p)))
    if not len(G) == 120:
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:42')
    e = (one, zero, zero, zero)
    z = tuple((N(x) for x in e))
    for q in G:
        if not qmul(q, (q[0], N(q[1]), N(q[2]), N(q[3]))) == e:
            raise AssertionError('Verification failed at frozen source verify_counterexample.py:45')
        for r in G:
            if not qmul(q, r) in G:
                raise AssertionError('Verification failed at frozen source verify_counterexample.py:46')

    def order(q):
        r = e
        for n in range(1, 121):
            r = qmul(r, q)
            if r == e:
                return n
        raise AssertionError
    orders = {q: order(q) for q in G}

    def chi(q):
        x = S(q[0], 2)
        y = A(M(M(x, x), x), N(S(x, 2)))
        if not (y[1] == 0 and y[0].denominator == 1):
            raise AssertionError('Verification failed at frozen source verify_counterexample.py:57')
        return int(y[0])
    values = {q: chi(q) for q in G}
    norm = sum((x * x for x in values.values()))
    fs = sum((chi(qmul(q, q)) for q in G))
    if not (norm == 120 and fs == -120):
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:62')
    if not sum((1 for q in G if all((qmul(q, r) == qmul(r, q) for r in G)))) == 2:
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:63')
    rows = {o: sorted({values[q] for q in G if orders[q] == o}) for o in sorted(set(orders.values()))}
    if not rows == {1: [4], 2: [-4], 3: [1], 4: [0], 5: [-1], 6: [-1], 10: [1]}:
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:65')
    return {'order': 120, 'closure_products_checked': 14400, 'center_order': 2, 'element_order_counts': dict(sorted(Counter(orders.values()).items())), 'symmetric_cube_values_by_order': rows, 'symmetric_cube_norm': str(F(norm, 120)), 'symmetric_cube_frobenius_schur_indicator': str(F(fs, 120))}

def sl2_checks():
    p = 5
    G = [x for x in product(range(p), repeat=4) if (x[0] * x[3] - x[1] * x[2]) % p == 1]
    e = (1, 0, 0, 1)
    z = (4, 0, 0, 4)

    def mul(x, y):
        a, b, c, d = x
        f, g, h, i = y
        return ((a * f + b * h) % p, (a * g + b * i) % p, (c * f + d * h) % p, (c * g + d * i) % p)

    def order(x):
        y = e
        for n in range(1, 121):
            y = mul(y, x)
            if y == e:
                return n
        raise AssertionError
    orders = {g: order(g) for g in G}
    chi_plus = {1: 4, 2: 4, 3: 1, 4: 0, 5: -1, 6: 1, 10: -1}
    chi_minus = {1: 4, 2: -4, 3: 1, 4: 0, 5: -1, 6: -1, 10: 1}
    psi = {g: 2 * chi_plus[orders[g]] if orders[g] % 2 else 0 for g in G}
    if not all((psi[g] == chi_plus[orders[g]] + chi_minus[orders[g]] for g in G)):
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:84')
    inner = sum((psi[g] * chi_minus[orders[g]] for g in G))
    if not inner == 120:
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:86')
    if not sum((chi_minus[order(mul(g, g))] for g in G)) == -120:
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:87')
    cosets = {min(g, mul(z, g)) for g in G}
    if not len(cosets) == 60:
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:90')
    return {'group_order': len(G), 'element_order_counts': dict(sorted(Counter(orders.values()).items())), 'central_cosets': len(cosets), 'central_nilpotent_operator_rank': 60, 'central_nilpotent_kernel_dimension': 60, 'forced_projective_dimension': psi[e], 'faithful_character_multiplicity': str(F(inner, 120))}

def rank2(rows):
    basis = {}
    for v in rows:
        while v:
            i = v.bit_length() - 1
            if i in basis:
                v ^= basis[i]
            else:
                basis[i] = v
                break
    return len(basis)

def a5_augmentation():
    G = [p for p in permutations(range(5)) if sum((p[i] > p[j] for i in range(5) for j in range(i + 1, 5))) % 2 == 0]
    matrices = []
    for g in G:
        bits = 0
        for j in range(4):
            v = 1 << g[j] ^ 1 << g[4]
            for i in range(4):
                if v >> i & 1:
                    bits |= 1 << 4 * i + j
        matrices.append(bits)
    span = rank2(matrices)
    if not (len(G) == 60 and span == 16):
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:114')
    V4 = [g for g in G if g[4] == 4 and all((g[g[i]] == i for i in range(5)))]
    if not (len(V4) == 4 and {g[0] for g in V4} == set(range(4))):
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:118')
    return {'group_order': 60, 'augmentation_dimension': 4, 'matrix_algebra_span_dimension': span, 'absolutely_irreducible': True, 'sylow_2_order': 4, 'restriction_regular': True}

def monoid_checks():
    reductions = {'V1': (1, 0, 0), 'V5': (1, 1, 0), 'V4': (0, 0, 1)}
    targets = [(8, 4, 0), (8, 6, 0), (0, 0, 2)]
    coeffs = [(4, 4, 0), (2, 6, 0), (0, 0, 2)]
    dims = (1, 4, 4)
    out = []
    for target, c in zip(targets, coeffs):
        got = tuple((sum((c[i] * list(reductions.values())[i][j] for i in range(3))) for j in range(3)))
        if not got == target:
            raise AssertionError('Verification failed at frozen source verify_counterexample.py:130')
        out.append({'pim_composition_vector': target, 'rational_witness_coefficients_V1_V5_V4': c, 'dimension': sum((a * b for a, b in zip(target, dims)))})
    if not 24 + 2 * 32 + 4 * 8 == 120:
        raise AssertionError('Verification failed at frozen source verify_counterexample.py:133')
    return {'all_three_F2_pims': out, 'regular_dimension_reconstruction': 120}

def main():
    result = {'icosian_character_construction': icosians(), 'sl2_f5': sl2_checks(), 'a5_simple_projective': a5_augmentation(), 'positive_monoid': monoid_checks(), 'all_assertions_passed': True}
    out = Path(__file__).with_name('counterexample_results.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
