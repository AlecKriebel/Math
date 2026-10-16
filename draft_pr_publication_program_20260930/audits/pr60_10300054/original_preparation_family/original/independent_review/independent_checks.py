#!/usr/bin/env python3
"""Independent exact gauge and small-divisor controls.

No imports from the submitted checker. No foliation counterexample is asserted.
"""
from collections import Counter
from fractions import Fraction
from math import factorial
import json
import sympy as s

counts = Counter()
def check(ok, label):
    assert bool(ok), label
    counts[label] += 1

x, y, z = s.symbols('x y z', real=True)
variables = (x, y, z)
def gradient(f):
    return s.Matrix([s.diff(f, v) for v in variables])
def curl(v):
    return s.Matrix([s.diff(v[2], y)-s.diff(v[1], z),
                     s.diff(v[0], z)-s.diff(v[2], x),
                     s.diff(v[1], x)-s.diff(v[0], y)])
def divergence(v):
    return sum(s.diff(v[i], variables[i]) for i in range(3))
def zero(e):
    return s.simplify(s.expand(e)) == 0

# Non-coordinate foliated charts: the defining normal has three variable
# components, and the z derivative of F is 1, so it never vanishes.
examples = [
    (z+x*y, x, x+y*y, y*z, x*z+y),
    (z+x*x*y, y, y+z*z, x*y, z+x*x),
    (z+x*y*y, z, z+x*x, x+y*z, y+x*z),
]
for F, H, k, f, h in examples:
    check(s.diff(F,z) == 1, 'defining_submersion')
    alpha = s.exp(H)*gradient(F)
    omega = -gradient(H)+k*alpha
    alpha_f = s.exp(f)*alpha
    omega_f = omega-gradient(f)
    auxiliary = omega_f+h*alpha_f
    for e in curl(alpha)-alpha.cross(omega):
        check(zero(e), 'integrable_noncoordinate_chart')
    for e in curl(alpha_f)-alpha_f.cross(auxiliary):
        check(zero(e), 'full_rescaled_auxiliary_equation')
    Y, X = curl(omega), curl(alpha_f)
    old_density = omega.dot(Y)
    new_density = auxiliary.dot(curl(auxiliary))
    check(zero(new_density-old_density+Y.dot(gradient(f))-X.dot(gradient(h))),
          'full_gauge_density')
    check(zero(divergence(X)) and zero(divergence(Y)), 'both_fields_preserve_volume')
    check(zero(alpha.dot(Y)) and zero(alpha_f.dot(X)), 'both_fields_are_tangent')
    # Constant auxiliary changes have no density effect, despite changing the form.
    constant_shift = omega_f+7*alpha_f
    check(zero(constant_shift.dot(curl(constant_shift))-omega_f.dot(curl(omega_f))),
          'constant_auxiliary_invariance')

# Exact transport corrections for periodic modes, including both signs.
for k in (-3, -2, -1, 1, 2, 3):
    for mean in (-1, 0, 1):
        g = mean+s.cos(k*x)
        h = -s.sin(k*x)/k
        check(zero(g+s.diff(h,x)-mean), 'periodic_transport_mode')
check(1+2*s.cos(s.pi) == -1, 'negative_invariant_orbit_control')
check(s.integrate(1+2*s.cos(y), (y,0,2*s.pi))/(2*s.pi) == 1,
      'positive_volume_average_control')

# Exact finite Liouville approximants. No decimal or floating-point arithmetic.
last_q = 0
for n in range(2, 6):
    q = 10**factorial(n)
    a_n = sum((Fraction(1,10**factorial(j)) for j in range(1,n+1)), Fraction())
    p = q*a_n
    check(p.denominator == 1, 'integer_frequency')
    check(q > last_q and 0 < p < q, 'distinct_frequency_and_size')
    last_q = q
    a_later = a_n+Fraction(1,10**factorial(n+1))+Fraction(1,10**factorial(n+2))
    delta = q*a_later-p
    leading = Fraction(1,q**n)
    check(leading < delta < Fraction(10,9)*leading, 'finite_tail_geometric_bound')
    coefficient = Fraction(1, 10**(n*factorial(n)//2))
    check(coefficient*coefficient == Fraction(1,q**n), 'exact_amplitude')
    forced_fourier = coefficient/(2*delta)
    lower = Fraction(10**(n*factorial(n)//2),4)
    check(forced_fourier >= lower, 'forced_fourier_blowup_control')
    check(factorial(n+1)-factorial(n) == n*factorial(n), 'leading_tail_exponent')

# Every derivative order has a summable tail: finite exponent controls of the
# all-m argument in the report, without constructing huge factorial powers.
for m in range(11):
    for n in range(2*m+2,2*m+8):
        check(Fraction(n,2)-m >= 1, 'smooth_tail_exponent')
        check(factorial(n) >= n, 'geometric_summability_majorant')

print(json.dumps({
    'status':'PASS','exact_assertions':sum(counts.values()),
    'categories':dict(counts),'sympy_version':s.__version__,
    'scope':'Finite exact diagnostics of the smooth gauge and abstract transport arguments; no source-manifold realization or resolution.'
},indent=2))
