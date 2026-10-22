#!/usr/bin/env python3
"""Exact finite algebra controls. Not a knot, essentiality, or cusp certificate."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
from math import isqrt
import hashlib
import json

HERE = Path(__file__).resolve().parent
COUNTS = {}

def require(test, category):
    if not test:
        raise RuntimeError('Control failed: ' + category)
    COUNTS[category] = COUNTS.get(category, 0) + 1

def cap_status(n, P, Q, A0, B):
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError('positive integer intersection required')
    P, Q, A0, B = map(F, (P, Q, A0, B))
    if min(P, Q, A0, B) <= 0:
        raise ValueError('positive cap, area, and target required')
    r = P*P*Q*Q - n*n*A0*A0
    if r < 0:
        return 'inconsistent_inputs'
    d = n*n*B*B - P*P - Q*Q
    if d < 0 or d*d < 4*r:
        return 'inconclusive'
    return 'strict' if d*d > 4*r else 'at_most'

def best_pair(a, p):
    if len(a) != len(p) or len(a) < 2 or min(p) <= 0:
        raise ValueError('valid finite slope/cap list required')
    candidates = [(F(p[i]+p[j], abs(a[i]-a[j])), i, j)
                  for i, j in combinations(range(len(a)), 2) if a[i] != a[j]]
    if not candidates:
        raise ValueError('no feasible meridian combination')
    return min(candidates)

def ceil_sqrt(q):
    q = F(q)
    v = isqrt(q.numerator // q.denominator)
    return v if v*v == q else v+1

def algebra_controls():
    require(cap_status(8,18,18,36,4) == 'strict', 'cap_examples')
    require(cap_status(2,5,5,12,4) == 'at_most', 'cap_examples')
    require(cap_status(2,5,5,12,F(399,100)) == 'inconclusive', 'cap_examples')
    require(cap_status(2,5,5,13,4) == 'inconsistent_inputs', 'cap_examples')
    require(cap_status(1,1,1,1,1) == 'inconclusive', 'cap_examples')
    require(cap_status(8,18,18,1,4) == 'inconclusive', 'cap_examples')
    invalid = [(0,1,1,1,1),(-1,1,1,1,1),(True,1,1,1,1),
               (F(1,2),1,1,1,1),(1,0,1,1,1),(1,1,-1,1,1),
               (1,1,1,0,1),(1,1,1,1,0)]
    for args in invalid:
        try:
            cap_status(*args)
        except ValueError:
            require(True, 'invalid_input_rejection')
        else:
            require(False, 'invalid_input_rejection')

    # Deterministic rational lattice controls, including shear and orientation.
    for m, h, t in product([F(1),F(7,3),F(5)], [F(1,2),F(6,5),F(3)],
                            [F(-4),F(-1,3),F(0),F(9,2)]):
        for a,b in combinations(range(-3,4),2):
            ux, vx = t+a*m, t+b*m
            u2, v2 = ux*ux+h*h, vx*vx+h*h
            dot = ux*vx+h*h
            n, area = abs(a-b), m*h
            require(u2*v2-dot*dot == n*n*area*area, 'gram_identity')
            require((ux-vx)**2 == n*n*m*m, 'difference_identity')
            P, Q = F(ceil_sqrt(u2)), F(ceil_sqrt(v2))
            r = P*P*Q*Q-n*n*area*area
            require(r >= 0, 'cap_discriminant')
            d = n*n*m*m-P*P-Q*Q
            require(d <= 0 or d*d <= 4*r, 'upper_bound_control')
            require(n*n*m*m < (P+Q)**2, 'strict_triangle_control')
            # Any claimed certificate below the actual m is invalid.
            require(cap_status(n,P,Q,area,m-F(1,100)) not in ['strict','at_most'],
                    'no_false_positive_below_actual_length')
            s = cap_status(n,P,Q,area,F(4))
            require(s not in ['strict','at_most'] or m <= 4,
                    'four_certificate_sound_on_controls')
            require(s != 'strict' or m < 4, 'strict_certificate_sound_on_controls')

    for a,p in [((-4,-1,2,5),(3,8,4,9)), ((0,0,2,8),(4,3,6,18)),
                ((-3,0,7,20),(12,6,9,24)), ((1,2,3,4),(6,6,6,6))]:
        B,i,j = best_pair(a,p)
        t = [F(0)]*4
        t[i],t[j] = F(1,a[i]-a[j]), F(-1,a[i]-a[j])
        require(sum(t) == 0 and sum(F(a[k])*t[k] for k in range(4)) == 1,
                'pair_attainment_constraints')
        require(sum(F(p[k])*abs(t[k]) for k in range(4)) == B,
                'pair_attainment_cost')
        for raw in product(range(-2,3),repeat=4):
            moment = sum(a[k]*raw[k] for k in range(4))
            if sum(raw) != 0 or moment == 0:
                continue
            t = [F(v,moment) for v in raw]
            T = sum(max(v,F(0)) for v in t)
            w = {(i,j):max(t[i],F(0))*max(-t[j],F(0))/T
                 for i in range(4) for j in range(4)}
            cost = sum(F(p[k])*abs(t[k]) for k in range(4))
            require(sum(w[i,j]*(a[i]-a[j]) for i,j in w) == 1,
                    'coupling_moment')
            require(sum(w[i,j]*(p[i]+p[j]) for i,j in w) == cost,
                    'coupling_cost')
            require(cost >= B, 'pair_optimality_controls')
        require(best_pair(tuple(x+7 for x in a),p)[0] == B, 'slope_shift_invariance')
        require(best_pair(tuple(-x for x in a),p)[0] == B, 'slope_sign_invariance')

    # Abstract torus only; no knot realization is claimed or encoded.
    m,h,c = F(5),F(6,5),8
    require(m > 4 and m <= 6-F(7,c), 'numerical_model')
    require(c*m+h <= 6*(c-1), 'numerical_model')
    require(h <= 5*c-6 and m*h <= 9*c*(1-F(1,c))**2, 'numerical_model')
    for p,q in product(range(-10,11),repeat=2):
        if p or q:
            require((m*p)**2+(h*q)**2 >= h*h, 'finite_systole_controls')
    for c in range(1,101):
        require((6-F(7,c) <= 4) == (c <= 3), 'crossing_threshold')
    for c,g in product(range(1,101),range(0,31)):
        require((3+F(6*g-6,c) <= 4) == (c >= 6*g-6), 'adequate_threshold')
    for N in range(2,101):
        f = lambda n: F(4)-F(1,N)+F(1,n)
        require(f(N-1)>4 and f(N)==4 and f(N+1)<4, 'limit_quantifier_controls')

    # Falsify explicit corrupted formulas; these are model mutations, not coverage claims.
    def mutated_no_sign(n,P,Q,A,B):
        r=F(P)**2*F(Q)**2-n*n*F(A)**2
        d=n*n*F(B)**2-F(P)**2-F(Q)**2
        return r>=0 and d*d>=4*r
    require(mutated_no_sign(1,1,1,1,1) and
            cap_status(1,1,1,1,1)=='inconclusive','rejected_corruptions')
    # Dropping Q^2 in the bound at R=0 makes orthogonal unit vectors impossible.
    mutated_upper_squared = F(1)  # (P^2+2sqrt(R))/n^2, P=Q=n=A=1.
    actual_difference_squared = F(2)
    require(actual_difference_squared>mutated_upper_squared,'rejected_corruptions')
    # Multiplying the determinant scale by n twice falsely rejects a feasible pair.
    mutated_discriminant=F(5)**4-2**4*F(12)**2
    require(mutated_discriminant<0 and
            cap_status(2,5,5,12,4)=='at_most','rejected_corruptions')
    # Replacing the sum of both caps by their maximum fails the exact LP optimum.
    require(best_pair((0,1),(1,1))[0] > F(max(1,1),1),'rejected_corruptions')
    # Equality in the squared comparison cannot be reported as a strict bound.
    require(cap_status(2,5,5,12,4)=='at_most' and
            F((-4-4)**2,2**2)==F(4)**2,'rejected_corruptions')
    # Convergence alone does not put every finite term below the limiting ceiling.
    require(F(4)-F(1,10)+F(1,9)>4,'rejected_corruptions')

    return {
        'problem_id':2809,
        'status':'PASS',
        'scope':'Exact finite algebra controls only; no knot or universal conjecture certification.',
        'counts':dict(sorted(COUNTS.items())),
        'total_checks':sum(COUNTS.values()),
        'substantive_approaches':5,
        'target_resolved':False,
        'novelty_claim':False
    }

def check_manifest():
    path = HERE/'MANIFEST.json'
    if not path.exists():
        return
    doc = json.loads(path.read_text())
    entries = doc['files']
    actual = {p.name for p in HERE.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
    expected = {x['path'] for x in entries}
    if actual != expected:
        raise RuntimeError('Manifest membership mismatch')
    for e in entries:
        p = HERE/e['path']
        if p.name != e['path']:
            raise RuntimeError('Unsafe manifest path')
        b = p.read_bytes()
        if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:
            raise RuntimeError('Manifest mismatch: '+e['path'])

if __name__ == '__main__':
    check_manifest()
    print(json.dumps(algebra_controls(),indent=2,sort_keys=True))
