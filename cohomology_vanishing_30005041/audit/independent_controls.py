#!/usr/bin/env python3
"""Portable, exact adversarial controls. Standard library; no author imports.

Run: python3 independent_controls.py [--author PATH]
The optional path enables frozen-byte checks. This program only reads that path.
Mathematical checks alone run without the author packet or source PDFs.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

COUNTS = Counter()
def check(condition, category):
    if not condition:
        raise AssertionError(category)
    COUNTS[category] += 1

def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def multiply(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]

def apply(a, x):
    return [sum((u*v for u, v in zip(row, x)), F(0)) for row in a]

def rank(a):
    # Independent exact Gaussian elimination, not the geometric-series formula.
    a = [[F(x) for x in row] for row in a]
    if not a:
        return 0
    pivot = 0
    for col in range(len(a[0])):
        selected = next((j for j in range(pivot, len(a)) if a[j][col]), None)
        if selected is None:
            continue
        a[pivot], a[selected] = a[selected], a[pivot]
        divisor = a[pivot][col]
        a[pivot] = [x/divisor for x in a[pivot]]
        for j in range(len(a)):
            if j != pivot and a[j][col]:
                factor = a[j][col]
                a[j] = [x-factor*y for x, y in zip(a[j], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot

def inverse(a):
    n = len(a)
    z = [list(map(F, row)) + eye for row, eye in zip(a, ident(n))]
    for c in range(n):
        selected = next(j for j in range(c, n) if z[j][c])
        z[c], z[selected] = z[selected], z[c]
        d = z[c][c]
        z[c] = [x/d for x in z[c]]
        for j in range(n):
            if j != c:
                d = z[j][c]
                z[j] = [x-d*y for x, y in zip(z[j], z[c])]
    return [row[n:] for row in z]

def cycles(perm):
    remaining = set(range(len(perm)))
    result = []
    while remaining:
        first = min(remaining)
        cyc, j = [], first
        while j in remaining:
            cyc.append(j)
            remaining.remove(j)
            j = perm[j]
        result.append(cyc)
    return result

def signed_matrix(perm, signs):
    n = len(perm)
    return [[F(signs[i] if j == perm[i] else 0) for j in range(n)]
            for i in range(n)]

def difference(u):
    return [[F(i == j)-u[i][j] for j in range(len(u))]
            for i in range(len(u))]

def exact_root(n, degree):
    if n < 2:
        return n
    lo, hi = 0, 1 << ((n.bit_length()+degree-1)//degree)
    while lo+1 < hi:
        mid = (lo+hi)//2
        if mid**degree <= n:
            lo = mid
        else:
            hi = mid
    if hi**degree == n:
        return hi
    if lo**degree == n:
        return lo
    raise ValueError('Expected an exact rational root')

def rational_power(x, p):
    x, p = F(x), F(p)
    if x < 0:
        raise ValueError('Use absolute values for fractional powers')
    return F(exact_root(x.numerator, p.denominator),
             exact_root(x.denominator, p.denominator))**p.numerator

def norm_power(v, p, masses=None):
    masses = masses or [F(1)]*len(v)
    return sum((m*rational_power(abs(x), p) for m, x in zip(masses, v)), F(0))

# 1. Full arbitrary permutations, multiple orbits, and all sign assignments.
# This checks rank/cokernel directly rather than testing the author's inverse.
finite_models = 0
for n in range(0, 7):
    for perm in permutations(range(n)):
        cyc = cycles(perm)
        for signs in product((-1, 1), repeat=n):
            positive_cycles = 0
            for c in cyc:
                sign = 1
                for i in c:
                    sign *= signs[i]
                positive_cycles += sign == 1
            d = difference(signed_matrix(perm, signs))
            check(n-rank(d) == positive_cycles, 'signed_permutation_cokernel_dimension')
            finite_models += 1

# 2. Invert negative cycles by independent elimination; inspect exact entries.
for n in range(1, 18):
    perm = [(i-1) % n for i in range(n)]
    signs = [-1] + [1]*(n-1)
    u = signed_matrix(perm, signs)
    d = difference(u)
    inv = inverse(d)
    check(multiply(d, inv) == ident(n), 'negative_cycle_inverse_left')
    check(multiply(inv, d) == ident(n), 'negative_cycle_inverse_right')
    check(all(abs(x) == F(1, 2) for row in inv for x in row),
          'negative_cycle_inverse_entry_magnitudes')
    # For 0<p<=1 the exact quasi-operator norm is n^(1/p)/2:
    # the upper estimate follows by subadditivity, and every basis column attains it.
    for p in (F(1, 3), F(1, 2), F(2, 3), F(1)):
        e = [F(2 if i == 0 else 0) for i in range(n)]
        y = apply(inv, e)
        # The input is 2 e_0, so the exact output pth power is n.
        # This realizes ||inverse||^p = n/2^p, including p<1.
        check(norm_power(y, p) == n, 'quasinorm_basis_extremizer_structure')

# 3. Exact nonsingular weighted models and density intertwiners for p below 1.
exponents = (F(1,3), F(1,2), F(2,3), F(1), F(3,2), F(2), F(3), F(6))
for perm in ((1,0), (1,2,0), (1,0,3,4,2)):
    n = len(perm)
    bases = [F(i+2) for i in range(n)]
    masses = [b**6 for b in bases]
    signs = [(-1)**i for i in range(n)]
    u = signed_matrix(perm, signs)
    ps = {}
    for p in exponents:
        roots = [rational_power(m, 1/p) for m in masses]
        pp = [[u[i][j]*roots[j]/roots[i] for j in range(n)] for i in range(n)]
        ps[p] = pp
        normalised = [[roots[i]*pp[i][j]/roots[j] for j in range(n)] for i in range(n)]
        check(normalised == u, 'weighted_atomic_normalization_rational_p')
        check(n-rank(difference(pp)) == n-rank(difference(u)),
              'weighted_atomic_cohomology_invariance')
    for p, q in ((p,q) for p in exponents for q in exponents if p < q):
        t, r = 1/p-1/q, 1/(1/p-1/q)
        a = [rational_power(m, -t) for m in masses]
        # Diagonal equality A P_q = P_p A, evaluated entrywise.
        check(all(a[i]*ps[q][i][j] == ps[p][i][j]*a[j]
                  for i in range(n) for j in range(n)),
              'positive_density_intertwiner_rational_pq')
        w = [rational_power(x, r) for x in a]
        check([w[i]*masses[i] for i in range(n)] == [F(1)]*n,
              'finite_invariant_density_rational_pq')
        f = [rational_power(m, -1/q) for m in masses]
        check(norm_power(f, q, masses) == n and
              norm_power([ai*fi for ai,fi in zip(a,f)], p, masses) == n,
              'multiplier_holder_equality_witness')
    # Identity inclusion is not equivariant at distinct exponents on this model.
    check(ps[F(1)] != ps[F(2)], 'raw_inclusion_nonintertwining_negative_control')

# 4. Signed-power bound at rational powers not covered by the author's controls.
values = (F(-5), F(-3), F(-2), F(-1), F(-1,2), F(-1,3), F(0),
          F(1,3), F(1,2), F(1), F(2), F(3), F(5))
for numerator, denominator in ((2,3),(2,5),(3,5),(3,4),(4,7),(5,7),(1,7)):
    for u,v in product(values, repeat=2):
        x = (-1 if u < 0 else 1)*abs(u)**denominator
        y = (-1 if v < 0 else 1)*abs(v)**denominator
        mx = (-1 if u < 0 else 1)*abs(u)**numerator
        my = (-1 if v < 0 else 1)*abs(v)**numerator
        check(abs(mx-my)**denominator <=
              2**(denominator-numerator)*abs(x-y)**numerator,
              'signed_power_rational_holder_bound')

# 5. Independent exact gluing controls, including p<1 and noninteger p>1.
# Let p=A/B, n_k=2^(A*k), u_k=2^(-B*k) on its cycle.
# Then ||u_k||_p^p=1 and ||(I-U)u_k||_p^p=2^p/n_k.
# We divide the second quantity by 2^p so every stored calculation is rational.
for p in exponents:
    A, B = p.numerator, p.denominator
    for K in (1,2,3,5,8,13,21):
        primitive = F(0)
        normalized_defect = F(0)
        for k in range(1,K+1):
            n, amplitude = 2**(A*k), F(1,2**(B*k))
            primitive += n*rational_power(amplitude,p)
            normalized_defect += rational_power(amplitude,p)
        expected = (1-F(1,2**(A*K)))/F(2**A-1)
        check(primitive == K, 'gluing_primitive_divergence_rational_p')
        check(normalized_defect == expected, 'gluing_defect_geometric_sum_rational_p')
        # Exact tail after K, divided by 2^p, tends to zero.
        tail = F(1,2**(A*K)*(2**A-1))
        check(normalized_defect+tail == F(1,2**A-1),
              'coboundary_closure_tail_rational_p')

# 6. Formal/measurable exact sequence in finite-dimensional algebraic models.
# V embeds in W as its first d coordinates; U_W preserves V.
# A quotient-invariant coset maps via delta to V; its kernel modulo V is the
# image of W-invariants. Dimension computations independently verify exactness.
for a in (-1,1):
    for b in (-1,1):
        for c in (-2,-1,0,1,2):
            uw = [[F(a),F(c)],[F(0),F(b)]]
            dv = [[F(a-1)]]
            dw = [[uw[i][j]-F(i==j) for j in range(2)] for i in range(2)]
            # H1(V)->H1(W): rank of image([V]) minus rank(delta W).
            image_rank = rank([dw[0]+[F(1)],dw[1]+[F(0)]])-rank(dw)
            h1v = 1-rank(dv)
            kernel = h1v-image_rank
            q_inv = 1 if b == 1 else 0
            w_inv = 2-rank(dw)
            v_inv = 1-rank(dv)
            rhs = q_inv-(w_inv-v_inv)
            check(kernel == rhs, 'formal_measurable_exact_sequence_dimension')

# The topological quotient W/V must not be silently used: V=Lp is dense in
# L0 by finite-support truncation; the quotient is not generally Hausdorff.
# The exact algebraic model above asserts no Hausdorff quotient property.

EXPECTED = {
 'ATTEMPTS.md':'bd764263ce2c166b8c0e2710408f3e07ddae50d10cb63fbaa1eb38aa3d2d00cf',
 'README.md':'c33902f6849c1f4e91260354ea91f4f0156f59a72fb9096790bcd3382d0c072a',
 'SOURCES.md':'9579e5d73979c5702375ef8ac86bed29ae437c84d996e87abe09d990de340408',
 'checks/exact_controls.json':'8b929ad57ff18171f0b302af29493843a176cf23d11846477817ea73c4c5de59',
 'checks/exact_controls.py':'4bf3f5c8c312aa82113a747d5bc04170981bc710bf85c8697f3e856e99b6e6bf'
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--author', type=Path)
args = parser.parse_args()
integrity = 'not requested'
if args.author is not None:
    manifest = args.author/'FROZEN_MANIFEST.json'
    check(sha256(manifest.read_bytes()).hexdigest() ==
          '8945c0b8686a4bb95bd6ba74a30ea04b609d4dd7d9ca3946434c5147d7a2264c',
          'frozen_manifest_identity')
    data = json.loads(manifest.read_text())
    check(data['files'] == EXPECTED, 'frozen_manifest_file_map')
    for rel, expected in EXPECTED.items():
        check(sha256((args.author/rel).read_bytes()).hexdigest() == expected,
              'frozen_file_sha256')
    check({str(p.relative_to(args.author)) for p in args.author.rglob('*') if p.is_file()}
          == set(EXPECTED)|{'FROZEN_MANIFEST.json'}, 'frozen_exact_file_inventory')
    integrity = 'PASS'
print(json.dumps({
    'status':'PASS',
    'audit_scope':'Scoped partial propositions only; original fixed-family interval question remains unsolved.',
    'arbitrary_signed_permutation_models':finite_models,
    'exact_assertion_cases':sum(COUNTS.values()),
    'checks':dict(sorted(COUNTS.items())),
    'frozen_integrity':integrity,
    'dependencies':'Python 3 standard library only',
    'limitations':'Finite exact controls are regression witnesses, not proofs of infinite-dimensional assertions. See independent_audit.md.'
},indent=2))
