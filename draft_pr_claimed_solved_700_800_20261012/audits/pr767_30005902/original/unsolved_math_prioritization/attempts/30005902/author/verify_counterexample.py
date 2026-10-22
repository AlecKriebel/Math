#!/usr/bin/env python3
"""Exact F_3 verification of the 27-dimensional Hopf cohomology example.
Standard library only. This finite certificate supplements PROOF.md.
"""
from itertools import product
from collections import Counter
import json

P = 3
BASIS = tuple(product(range(P), repeat=3))
ONE = (0, 0, 0)
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
COUNTS = Counter()

def require(test, category):
    COUNTS[category] += 1
    if not test:
        raise AssertionError(category)

def clean(a):
    return {m: c % P for m, c in a.items() if c % P}

def add(*args):
    r = {}
    for a in args:
        for m, c in a.items():
            r[m] = r.get(m, 0) + c
    return clean(r)

def scale(a, c):
    return clean({m: c*v for m, v in a.items()})

def mono(m):
    return {m: 1}

def mul(a, b):
    r = {}
    for m, c in a.items():
        for n, d in b.items():
            q = tuple(i+j for i, j in zip(m, n))
            if all(i < P for i in q):
                r[q] = r.get(q, 0) + c*d
    return clean(r)

def power(a, n):
    unit = (0,)*len(next(iter(a))) if a else ONE
    r = mono(unit)
    for _ in range(n):
        r = mul(r, a)
    return r

def eps(a):
    return a.get(ONE, 0)

def delta_generators(cross=True):
    return (
        add(mono(X+ONE), mono(ONE+X)),
        add(mono(Y+ONE), mono(ONE+Y)),
        add(mono(Z+ONE), mono(ONE+Z), mono(X+Y) if cross else {}),
    )

def algebra_map(generators):
    d = {}
    unit = (0,)*len(next(iter(generators[0])))
    for m in BASIS:
        v = mono(unit)
        for generator, n in zip(generators, m):
            for _ in range(n):
                v = mul(v, generator)
        d[m] = v
    def apply(a):
        return add(*(scale(d[m], c) for m, c in a.items()))
    return apply

DELTA = algebra_map(delta_generators())
S = algebra_map((scale(mono(X), -1), scale(mono(Y), -1), add(scale(mono(Z), -1), mono((1, 1, 0)))))

def coeff(m, a):
    return a.get(m, 0)

def lift(m, a, delta=DELTA):
    """R_f=(f tensor id)Delta, f the coefficient-of-m functional."""
    return clean({}) if not a else add(*(
        scale(mono(t[3:]), c) for t, c in delta(a).items() if t[:3] == m
    ))

def derivative(a, i):
    out = {}
    for m, c in a.items():
        if m[i]:
            n = list(m)
            n[i] -= 1
            out[tuple(n)] = out.get(tuple(n), 0) + c*m[i]
    return clean(out)

def rank_mod_p(rows):
    a = [[v % P for v in row] for row in rows]
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][col], -1, P)
        a[r] = [(v*inv) % P for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                c = a[i][col]
                a[i] = [(u-c*v) % P for u, v in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r

def run():
    require(len(BASIS) == 27, 'dimension')
    for g in delta_generators():
        require(not power(g, 3), 'relations_preserved_by_delta')
    for g in (S(mono(X)), S(mono(Y)), S(mono(Z))):
        require(not power(g, 3), 'relations_preserved_by_antipode')
    for m in BASIS:
        a = mono(m)
        d = DELTA(a)
        left, right = {}, {}
        for t, c in d.items():
            for u, b in DELTA(mono(t[:3])).items():
                left = add(left, scale(mono(u+t[3:]), c*b))
            for u, b in DELTA(mono(t[3:])).items():
                right = add(right, scale(mono(t[:3]+u), c*b))
        require(left == right, 'coassociativity_all_basis')
        lc = add(*(scale(mono(t[3:]), c) for t, c in d.items() if t[:3] == ONE))
        rc = add(*(scale(mono(t[:3]), c) for t, c in d.items() if t[3:] == ONE))
        require(lc == a and rc == a, 'counit_all_basis')
        la = add(*(scale(mul(S(mono(t[:3])), mono(t[3:])), c) for t, c in d.items()))
        ra = add(*(scale(mul(mono(t[:3]), S(mono(t[3:]))), c) for t, c in d.items()))
        require(la == scale(mono(ONE), eps(a)) and ra == la, 'antipode_both_sides_all_basis')
        require(S(S(a)) == a, 'bijective_antipode_all_basis')
        require(lift(X, a) == add(derivative(a, 0), mul(mono(Y), derivative(a, 2))), 'R_x_formula_all_basis')
        require(lift(Y, a) == derivative(a, 1), 'R_y_formula_all_basis')
        require(lift(Z, a) == derivative(a, 2), 'R_z_formula_all_basis')
        commutator = add(lift(X, lift(Y, a)), scale(lift(Y, lift(X, a)), -1))
        require(commutator == scale(lift(Z, a), -1), 'hochschild_commutator_all_basis')
        require(eps(commutator) == (-coeff(Z, a)) % P, 'scalar_bracket_all_basis')
        # Every scalar 0-coboundary is a -> epsilon(a)c-c epsilon(a)=0.
        for c in range(P):
            require((eps(a)*c-c*eps(a)) % P == 0, 'all_degree_one_boundaries_zero')
    d1rows = []
    for m, n in product(BASIS, repeat=2):
        a, b = mono(m), mono(n)
        ab = mul(a, b)
        require(mul(a,b) == mul(b,a), 'commutativity_all_basis_pairs')
        require(DELTA(ab) == mul(DELTA(a), DELTA(b)), 'bialgebra_all_basis_pairs')
        require(eps(ab) == eps(a)*eps(b) % P, 'epsilon_multiplicative_all_basis_pairs')
        for t in (X, Y, Z):
            require((eps(a)*coeff(t,b)-coeff(t,ab)+coeff(t,a)*eps(b)) % P == 0, 'three_scalar_one_cocycles_all_pairs')
            require(lift(t,ab) == add(mul(lift(t,a),b),mul(a,lift(t,b))), 'three_Hochschild_one_cocycles_all_pairs')
        d1rows.append([(eps(a)*(n==t)-(ab.get(t,0))+(m==t)*eps(b)) % P for t in BASIS])
    for m,n,t in product(BASIS,repeat=3):
        a,b,c=mono(m),mono(n),mono(t)
        require(mul(mul(a,b),c)==mul(a,mul(b,c)), 'associativity_all_basis_triples')
    d1rank = rank_mod_p(d1rows)
    require(d1rank == 24, 'scalar_d1_rank')
    require(27-d1rank == 3, 'H1_dimension')
    noncocommutativity = add(DELTA(mono(Z)),scale({t[3:]+t[:3]:c for t,c in DELTA(mono(Z)).items()},-1))
    require(noncocommutativity == add(mono(X+Y),scale(mono(Y+X),-1)), 'noncocommutativity_witness')
    require(bool(noncocommutativity), 'noncocommutativity_nonzero')
    bracket_z = eps(add(lift(X,lift(Y,mono(Z))),scale(lift(Y,lift(X,mono(Z))),-1)))
    require(bracket_z == 2, 'nonboundary_pairing_z')
    # Deliberate false alternatives: they must not satisfy the asserted witness.
    badS = algebra_map((scale(mono(X),-1),scale(mono(Y),-1),scale(mono(Z),-1)))
    bad_antipode = add(*(scale(mul(badS(mono(t[:3])),mono(t[3:])),c) for t,c in DELTA(mono(Z)).items()))
    require(bool(bad_antipode), 'negative_control_omit_antipode_xy')
    cocomm = algebra_map(delta_generators(False))
    bad_bracket = add(lift(X,lift(Y,mono(Z),cocomm),cocomm),scale(lift(Y,lift(X,mono(Z),cocomm),cocomm),-1))
    require(not bad_bracket, 'negative_control_remove_coproduct_cross_term')
    require(bracket_z != 0, 'negative_control_false_zero_bracket')
    require(bracket_z != 1, 'negative_control_wrong_orientation_sign')
    return {
        'status':'PASS', 'field':'F_3', 'dimension':27,
        'cohomology':'Ext_H^*(k,k)', 'degree_one_bracket':'[f_x,f_y]=-f_z',
        'witness_value_on_z':bracket_z, 'scalar_d1_rank':d1rank,
        'scalar_d0_rank':0, 'H1_dimension':3,
        'assertions':sum(COUNTS.values()), 'checks_by_category':dict(sorted(COUNTS.items())),
        'scope':'Finite-dimensional counterexample to the unrestricted-field statement; not the finite-dimensional characteristic-zero variant.',
        'limits':'Exact finite arithmetic certificate plus written proof; not formal proof-assistant verification or peer review.'
    }

if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
