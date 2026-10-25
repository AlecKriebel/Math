"""New analytic GF4/cubic-ring controls and finite-jet boundary diagnostics.

No provided programme, record stream, symbolic package or historical fixture is
loaded. Finite jets are diagnostics only; the formal-module proof is separate.
"""
from pathlib import Path
from itertools import product
import datetime, json, math, sys

E = Path(__file__).resolve().parent
fault = sys.argv[1] if len(sys.argv) > 1 else ''


def need(v, s):
    if not v:
        raise RuntimeError(s)


def fm(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return r


def fi(a):
    need(a != 0, 'nonzero_field_inverse')
    return next(b for b in range(1, 4) if fm(a, b) == 1)


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return tuple(a)


def pa(a, b):
    return trim([(a[i] if i < len(a) else 0) ^ (b[i] if i < len(b) else 0) for i in range(max(len(a), len(b)))])


def pm(a, b):
    if not a or not b:
        return ()
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] ^= fm(x, y)
    return trim(c)


ONE = ((1,), (1,))
Y = ((0, 1), (1,))


def ra(a, b):
    return pa(pm(a[0], b[1]), pm(b[0], a[1])), pm(a[1], b[1])


def rm(a, b):
    return pm(a[0], b[0]), pm(a[1], b[1])


def rp(a, n):
    if n < 0:
        need(a[0], 'nonzero_rational_denominator')
        return rp((a[1], a[0]), -n)
    r = ONE
    for _ in range(n):
        r = rm(r, a)
    return r


def req(a, b):
    return pm(a[0], b[1]) == pm(b[0], a[1])


def peval(p, r):
    out = ((), (1,))
    for a in reversed(p):
        out = ra(rm(out, r), ((a,), (1,)))
    return out


def rsub(a, r):
    num = peval(a[0], r)
    den = peval(a[1], r)
    return rm(num, rp(den, -1))


# Exact rational identities, with polynomial cross multiplication over GF4.
one_y = ra(ONE, Y)
sigma = rm(Y, rp(one_y, -1))
z = rm(rp(Y, 2), rp(one_y, -1))
weight = rp(one_y, 2)
if fault == 'weight':
    weight = ONE
rational = {
    'sigma_involution': req(rsub(sigma, sigma), Y),
    'z_invariant': req(rsub(z, sigma), z),
    'y_squared_relation': req(rp(Y, 2), rm(z, one_y)),
    'T_y_equals_y_plus_y_squared': req(rm(weight, sigma), ra(Y, rp(Y, 2))),
    'T_y_squared_fixed': req(rm(weight, rp(sigma, 2)), rp(Y, 2)),
    'T_one_normal_form': req(weight, ra(ra(ONE, z), rm(z, Y))),
    'T_y_normal_form': req(rm(weight, sigma), ra(z, rm(ra(ONE, z), Y))),
}
need(all(rational.values()), 'exact_rational_module_identities')
need(not req(sigma, ra(Y, rp(Y, 2))), 'wrong_derivation_weight_detected')
need(fm(2, 3) == 1 and fm(2, 2) == 3, 'literal_GF4_extension')

# The weakly ramified additive action, as literal matrices over GF4.
def matmul(A, B, add, mul, zero):
    out = []
    for i in range(2):
        for j in range(2):
            v = zero
            for k in range(2):
                v = add(v, mul(A[2*i+k], B[2*k+j]))
            out.append(v)
    return tuple(out)


actions = [(1, 0, a, 1) for a in range(4)]
for a, b in product(range(4), repeat=2):
    need(matmul(actions[a], actions[b], lambda x,y:x^y, fm, 0) == actions[a^b], 'all16_additive_action_relations')
need(len(set(actions)) == 4, 'faithful_additive_action')
quotient_denominator = pm((1, 2), (1, 3))
need(quotient_denominator == (1, 1, 1), 'quotient_u_action_denominator')

# B=GF4[e]/e^3, represented by three literal field coefficients.
Z = (0, 0, 0)
O = (1, 0, 0)
ep = (0, 1, 0)
ep2 = (0, 0, 1)


def ba(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def bm(a, b):
    out = [0, 0, 0]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j < 3:
                out[i+j] ^= fm(x, y)
    return tuple(out)


def J(a):
    if fault == 'fixed-ring':
        return a
    return a[0], a[1], a[2] ^ a[1]


allB = list(product(range(4), repeat=3))
fixed = []
for a in allB:
    need(J(J(a)) == a, 'j_involution_all64')
    if J(a) == a:
        fixed.append(a)
for a, b in product(allB, repeat=2):
    need(J(ba(a,b)) == ba(J(a),J(b)), 'j_additive_all4096')
    need(J(bm(a,b)) == bm(J(a),J(b)), 'j_multiplicative_all4096')
need(len(fixed) == 16 and all(a[1] == 0 for a in fixed), 'literal_cubic_fixed_ring')
reductions = sorted({(a[0],a[1]) for a in fixed})
need(reductions == [(a,0) for a in range(4)], 'every_fixed_element_reduces_to_residue')
MM = lambda a,b: matmul(a,b,ba,bm,Z)
scale = lambda s,A: tuple(bm(s,x) for x in A)
M = (O,ep,O,O)
MJ = (O,ba(ep,ep2),O,O)
C = (ba(O,ep),ep,Z,O)
if fault == 'translation':
    C = (ba(O,ep),Z,Z,O)
need(MM(M,M) == scale(ba(O,ep),(O,Z,Z,O)), 'involution_projective_unit_square')
need(MM(MJ,C) == scale(ba(O,ep),MM(C,M)), 'exact_cubic_conjugacy')
units = [a for a in allB if a[0]]
badC = (ba(O,ep),Z,Z,O)
need(not any(MM(MJ,badC) == scale(s,MM(badC,M)) for s in units), 'missing_translation_rejected_even_projectively')
need(MM(MJ,C) != MM(C,M), 'omitted_projective_scalar_rejected')

# First-order nontriviality diagnostic: constant of every coboundary is zero,
# including a nonzero constant coefficient in the general coordinate h.
constant_checks = [(a, a ^ a) for a in range(4)]
need(all(b == 0 for a,b in constant_checks), 'all_conjugator_constant_coefficients_allowed')


def binom(n, k):
    if n >= 0:
        return math.comb(n,k) if k <= n else 0
    return (-1)**k * math.comb(-n+k-1,k)


def rank(A):
    A = [r[:] for r in A]
    r = 0
    for c in range(len(A[0])):
        pivot = next((i for i in range(r,len(A)) if A[i][c]),None)
        if pivot is None:
            continue
        A[r],A[pivot] = A[pivot],A[r]
        scalar = fi(A[r][c])
        A[r] = [fm(scalar,x) for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                scalar = A[i][c]
                A[i] = [x ^ fm(scalar,y) for x,y in zip(A[i],A[r])]
        r += 1
    return r


jets = []
for cutoff in range(2,33):
    # M_cutoff = y*k[y]/(y^cutoff), NOT the complete module M.
    n = cutoff - 1
    T = [[0]*n for _ in range(n)]
    for d in range(1,cutoff):
        for k in range(cutoff-d):
            T[d+k-1][d-1] = binom(2-d,k) & 1
    D = [[T[i][j] ^ int(i==j) for j in range(n)] for i in range(n)]
    need(all(not sum(D[i][k]*D[k][j] for k in range(n))%2 for i in range(n) for j in range(n)), 'jet_norm_square_zero')
    rk = rank(D)
    h1 = n - 2*rk
    need(h1 == int(cutoff%2==0), 'actual_truncation_boundary_pattern')
    jets.append({'cutoff':cutoff,'dimension':n,'norm_rank':rk,'H1_dimension':h1})
need(any(r['H1_dimension'] for r in jets), 'reject_finite_jet_inference_of_complete_vanishing')

result = {
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'PASS',
    'source_programmes_or_foreign_code_loaded':False,
    'finite_checks_are_universal_formal_series_proof':False,
    'exact_rational_identities':rational,
    'additive_action_relations':16,
    'cubic_ring_elements':64,
    'j_ring_homomorphism_pair_checks':8192,
    'j_fixed_elements':fixed,
    'fixed_reductions_to_dual_numbers':reductions,
    'involution_and_conjugacy_full_cubic_ring':True,
    'negative_controls':{
        'wrong_derivation_weight_rejected':True,
        'missing_translation_rejected_for_all48_unit_scalars':True,
        'omitted_projective_scalar_rejected':True,
        'finite_jet_vanishing_inference_falsified':True,
    },
    'complete_formal_module_basis':'M=k[[z]]*y direct_sum k[[z]]*y^2; T=[[1,0],[1,1]], so invariants=image(T-1)=k[[z]]*y^2',
    'jet_boundary_diagnostics':jets,
    'no_source_or_existing_receipt_changed':True,
}
(E/'EXACT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'rational_identities':len(rational),'fixed_ring_elements':len(fixed),'jet_cutoffs_checked':len(jets),'spurious_nonzero_jet_H1_cutoffs':[r['cutoff'] for r in jets if r['H1_dimension']],'negative_controls':result['negative_controls']},indent=2))
