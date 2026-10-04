#!/usr/bin/env python3
"""Independent exact controls for the integer endpoint construction.

This does not import the author's verifier. Uniform positivity, completeness
and the all-r claim are checked in the written review, not by samples.
"""
from collections import Counter
from itertools import product
import json
import sympy as s

x, y = s.symbols('x y', real=True)
rho, eps, K, beta = s.symbols('rho eps K beta', positive=True)
t = s.symbols('t', nonnegative=True)
counts = Counter()
def check(ok, name):
    assert bool(ok), name
    counts[name] += 1
def zero(expr):
    return s.simplify(s.expand(expr)) == 0
def lap(expr):
    return s.diff(expr, x, 2) + s.diff(expr, y, 2)

# Explicit scalar bounds used in the nonlinear error absorption:
# exp(-t)(1+t) <= 1 and exp(-t)(1+t)^2 <= 4/e.
p = s.exp(-t)*(1+t)
q = s.exp(-t)*(1+t)**2
check(zero(s.diff(p, t)+t*s.exp(-t)), 'uniform_scalar_bound_certificate')
check(zero(s.diff(q, t)-(1-t)*(1+t)*s.exp(-t)), 'uniform_scalar_bound_certificate')
check(p.subs(t, 0) == 1, 'uniform_scalar_bound_certificate')
check(q.subs(t, 1) == 4/s.E, 'uniform_scalar_bound_certificate')

# The critical first variation has both signs and scale eps/s.
Q = x*x+y*y
S2 = Q+rho*rho
H = x*(s.log(S2)+Q/(2*S2))  # Re(partial_z(z^2 log(s)))
profile = 4*x*(Q*Q+3*Q*rho*rho+3*rho**4)/S2**3
check(zero(lap(H)-profile), 'critical_laplacian_profile')
check(zero(profile.subs({x:rho, y:0})-s.Rational(7, 2)/rho), 'critical_laplacian_profile')
check(zero(profile.subs({x:-rho, y:0})+s.Rational(7, 2)/rho), 'critical_laplacian_profile')
check(zero(3*S2**2-(Q*Q+3*Q*rho*rho+3*rho**4)
           -(2*Q*Q+3*Q*rho*rho)), 'uniform_profile_bound_certificate')
# Together with |x|<=s, the polynomial certificate proves |s*profile|<=12.
for X, Y in product(range(-3, 4), repeat=2):
    for r in (s.Rational(1, 8), s.Rational(1, 64)):
        value = profile.subs({x:r*X, y:r*Y, rho:r})
        rad2 = r*r*(1+X*X+Y*Y)
        check(rad2*value**2 <= 144, 'scaled_profile_diagnostic')

# An exact chart made from two nonlinear shears, not the author's single shear.
a, b = s.Rational(1, 3), -s.Rational(1, 5)
F = s.Matrix([x+a*y*y, y+b*(x+a*y*y)**2])
G = s.Matrix([x-a*(y-b*x*x)**2, y-b*x*x])
subF = {x:F[0], y:F[1]}
check(all(zero(e) for e in G.subs(subF, simultaneous=True)-s.Matrix([x,y])),
      'double_shear_inverse')
J = F.jacobian([x,y])
Ji = J.inv()
check(zero(J.det()-1), 'double_shear_orientation')
inverse_derivative = G.jacobian([x,y]).subs(subF, simultaneous=True)
for e in inverse_derivative-Ji:
    check(zero(e), 'inverse_derivative')
A = Ji*Ji.T
A_from_inverse = inverse_derivative*inverse_derivative.T
for e in A_from_inverse-A:
    check(zero(e), 'principal_laplacian_coefficient')
actual_drift = s.Matrix([lap(G[i]).subs(subF, simultaneous=True) for i in range(2)])
hessian_traces = s.Matrix([
    sum(A[i,j]*s.diff(F[k], [x,y][i], [x,y][j]) for i in range(2) for j in range(2))
    for k in range(2)])
predicted_drift = -Ji*hessian_traces
for e in actual_drift-predicted_drift:
    check(zero(e), 'inverse_laplacian_drift')
check(any(not zero(e) for e in actual_drift), 'dropping_drift_fails')
wrong_A = Ji.T*Ji
check(any(e.subs({x:1,y:1}) != 0 for e in A-wrong_A),
      'transposing_principal_coefficient_fails')

# Actual critical map jets at zero. The cubic jet vanishes; the quadratic
# perturbation is holomorphic, so its trace and the drift at zero vanish.
L = s.log(S2)/2
f = s.Matrix([x+eps*(x*x-y*y)*L, y+2*eps*x*y*L])
at_zero = {x:0,y:0}
check(f.subs(at_zero) == s.zeros(2,1), 'normalization_at_origin')
check(f.jacobian([x,y]).subs(at_zero) == s.eye(2), 'normalization_at_origin')
for k in range(2):
    check(zero(lap(f[k]).subs(at_zero)), 'critical_drift_at_origin')
    for j in range(4):
        check(zero(s.diff(f[k], x,j,y,3-j).subs(at_zero)), 'critical_cubic_jet')

# h's exact two-jet follows from f_z=1+2 eps log(rho) z+O(|z|^3).
c = 2*eps*s.log(rho)
h_two_jet = c*x-c*c*(x*x-y*y)/2
check(lap(h_two_jet) == 0, 'log_jacobian_harmonic_two_jet')
bg = beta*s.log(1+Q)
correction = K*eps*s.sqrt(S2)
check(zero(lap(bg+correction).subs(at_zero)-(4*beta+2*K*eps/rho)),
      'positive_corrected_laplacian_at_origin')
check(s.diff(correction,x).subs(at_zero) == 0 and
      s.diff(correction,y).subs(at_zero) == 0,
      'correction_preserves_critical_gradient')
check(s.diff(h_two_jet,x).subs(at_zero).subs(eps,-1/s.log(rho)) == -2,
      'critical_nonconvergent_factor_gradient')

print(json.dumps({
    'status':'PASS','exact_assertions':sum(counts.values()),
    'categories':dict(counts),'sympy_version':s.__version__,
    'limits':[
        'First-variation samples are diagnostic and do not prove nonlinear positivity',
        'The uniform all-n correction estimate is assessed in the written review',
        'No historical-priority or human-peer-review certificate'
    ]
},indent=2))
