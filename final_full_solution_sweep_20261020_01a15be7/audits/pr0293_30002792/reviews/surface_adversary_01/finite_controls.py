"""Finite sanity checks for the explicit inseparable-conductor model.

These controls are not a proof of Lemmas A/B. The algebraic derivation in
EXPLICIT_CONTROLS.md is the proof of the stated model properties.
Uses only Python's standard library.
"""
from datetime import datetime, timezone
import json
from pathlib import Path

PRIMES = [2, 3, 5, 7, 11, 13]

# Sparse multivariable polynomials: monomial exponent tuples -> residue.
def clean(poly, p):
    return {m: c % p for m, c in poly.items() if c % p}

def derivative(poly, var, p):
    out = {}
    for mon, coeff in poly.items():
        if mon[var]:
            new = list(mon)
            new[var] -= 1
            new = tuple(new)
            out[new] = out.get(new, 0) + coeff * mon[var]
    return clean(out, p)

def evaluate(poly, point, p):
    result = 0
    for mon, coeff in poly.items():
        term = coeff
        for value, exponent in zip(point, mon):
            term *= pow(value, exponent, p)
        result += term
    return result % p

def in_monomial_ring(a, b, p):
    # k[x, xt, t^p] subset k[x,t]. For t-exponent b, spend r=b%p
    # copies of xt and the remaining exponent on t^p, then pad with x.
    return a >= b % p

rows = []
for p in PRIMES:
    Q = {(p, 1, 0, 0): 1, (0, 0, p, 1): -1}
    deriv = [derivative(Q, i, p) for i in range(4)]
    expected = [{}, {(p, 0, 0, 0): 1}, {}, {(0, 0, p, 0): p-1}]
    assert deriv == expected

    # On x3=1, use x0=x, x2=xt, x1=t^p. Every checked pair
    # maps into Q=0. This is a finite control for a polynomial identity.
    parametrization_checks = 0
    for x in range(p):
        for t in range(p):
            assert evaluate(Q, (x, pow(t, p, p), x*t % p, 1), p) == 0
            parametrization_checks += 1

    # Check conductor condition on a finite monomial box. The proof that
    # this box suffices for the claimed threshold uses residue cycling.
    conductor_checks = 0
    for a in range(2*p+1):
        for b in range(3*p+1):
            sampled_conductor = all(in_monomial_ring(a, b+j, p) for j in range(3*p+1))
            assert sampled_conductor == (a >= p-1)
            conductor_checks += 1

    # Pullback of the good plane: x(1+t)+t^p. Its x coefficient 1+t
    # and constant t^p are coprime since t^p at t=-1 is nonzero.
    assert pow(p-1, p, p) != 0
    # At x=t=0 the curve meets x=0 with order p and is smooth since
    # its x derivative is 1. Its t derivative is x in characteristic p.
    curve = {(1,0):1, (1,1):1, (0,p):1}
    assert evaluate(derivative(curve, 0, p), (0,0), p) == 1
    assert evaluate(derivative(curve, 1, p), (0,0), p) == 0
    rows.append({
        'characteristic': p,
        'surface_degree': p+1,
        'adjoint_polynomial_degree': p-1,
        'jacobian_identity': True,
        'parametrization_point_checks': parametrization_checks,
        'conductor_monomial_checks': conductor_checks,
        'conductor_x_threshold': p-1,
        'integral_good_plane_gcd_control': True,
        'good_pullback_smooth_at_conductor': True,
    })

# Control the warning that an arbitrary plane section can fail.
# In p=2, x(1+t)+t^2+1=(t+1)(x+t+1).
p=2
lhs={(1,0):1,(1,1):1,(0,2):1,(0,0):1}
rhs={}
for mon1,c1 in {(0,1):1,(0,0):1}.items():
    for mon2,c2 in {(1,0):1,(0,1):1,(0,0):1}.items():
        mon=tuple(a+b for a,b in zip(mon1,mon2))
        rhs[mon]=rhs.get(mon,0)+c1*c2
assert clean(lhs,p)==clean(rhs,p)

result={
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'status':'all finite controls passed',
    'purpose':'Explicit model checks only; not universal validation of Lemmas A/B.',
    'models':rows,
    'special_bad_plane_reducibility_char2':True,
}
Path(__file__).with_name('FINITE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
