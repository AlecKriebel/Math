#!/usr/bin/env python3
"""Exact finite diagnostics for the contact-pencil proof; not a proof of ET/Gray."""
from pathlib import Path
from fractions import Fraction
import hashlib
import itertools
import json
import sympy as sy

checks = {}

def ck(name, value):
    if not bool(value):
        raise AssertionError(name)
    checks[name] = "PASS"

def tidy(form):
    return {I: sy.expand(c) for I, c in form.items() if sy.expand(c) != 0}

def plus(*forms):
    out = {}
    for form in forms:
        for I, c in form.items():
            out[I] = out.get(I, 0) + c
    return tidy(out)

def scale(c, form):
    return tidy({I: c * v for I, v in form.items()})

def wedge(a, b):
    out = {}
    for I, c in a.items():
        for J, d in b.items():
            if set(I) & set(J):
                continue
            sign = (-1) ** sum(i > j for i in I for j in J)
            K = tuple(sorted(I + J))
            out[K] = out.get(K, 0) + sign * c * d
    return tidy(out)

basis = [{(i,): sy.Integer(1)} for i in range(3)]
alpha, omega, gamma = basis
one = {(): sy.Integer(1)}
vol = {(0, 1, 2): sy.Integer(1)}
da = wedge(alpha, omega)
dw = wedge(alpha, gamma)
dg = wedge(omega, gamma)
d_basis = [da, dw, dg]

def d_const(form):
    """CE derivative with coefficients constant on the manifold."""
    out = {}
    for I, c in form.items():
        for j, i in enumerate(I):
            left, right = one, one
            for k in I[:j]:
                left = wedge(left, basis[k])
            for k in I[j+1:]:
                right = wedge(right, basis[k])
            out = plus(out, scale(c * (-1) ** j,
                                 wedge(wedge(left, d_basis[i]), right)))
    return out

for i, j, k in itertools.product(range(3), repeat=3):
    ck(f"exterior_associativity_{i}{j}{k}",
       wedge(wedge(basis[i], basis[j]), basis[k]) ==
       wedge(basis[i], wedge(basis[j], basis[k])))
for i in range(3):
    ck(f"CE_d_squared_{i}", d_const(d_const(basis[i])) == {})

s, t, h, p, q, r = sy.symbols("s t h p q r")
beta = plus(omega, scale(s, alpha))
dbeta = plus(dw, scale(s, da))
ck("source_sign_d_alpha", d_const(alpha) == wedge(alpha, omega))
ck("integrability", wedge(alpha, da) == {})
ck("d_squared_forces_alpha_domega", wedge(alpha, dw) == {})
ck("contact_nonzero", wedge(omega, dw) == scale(-1, vol))
ck("global_constant_pencil",
   wedge(beta, dbeta) == wedge(omega, dw))
ck("same_alpha_connection_equation", wedge(alpha, beta) == da)
ck("foliation_limit_pencil",
   wedge(plus(alpha, scale(t, omega)), plus(da, scale(t, dw))) ==
   scale(t*t, wedge(omega, dw)))
dh = plus(scale(p, alpha), scale(q, omega), scale(r, gamma))
variable = plus(omega, scale(h, alpha))
dvariable = plus(dw, wedge(dh, alpha), scale(h, da))
ck("variable_shift_has_error",
   plus(wedge(variable, dvariable), scale(-1, wedge(omega, dw))) ==
   wedge(wedge(omega, dh), alpha))
ck("variable_shift_can_destroy_contact",
   tidy({I: c.subs(r, 1) for I, c in wedge(variable, dvariable).items()}) == {})

# Every permutation of a coframe and both orientations: the equation is tensorial.
for perm in itertools.permutations(range(3)):
    for sign in (-1, 1):
        a, w, g = basis[perm[0]], scale(sign, basis[perm[1]]), basis[perm[2]]
        aa, ww = wedge(a, w), wedge(a, g)
        bb = plus(w, scale(s, a))
        ck(f"coframe_pencil_{perm}_{sign}",
           wedge(bb, plus(ww, scale(s, aa))) == wedge(w, ww))

# Arbitrary common nonconstant rescaling multiplies contact volume by its square.
E = sy.symbols("E", nonzero=True)
df = plus(scale(p, alpha), scale(q, omega), scale(r, gamma))
scaled = scale(E, beta)
dscaled = scale(E, plus(wedge(df, beta), dbeta))
ck("common_rescaling_volume", wedge(scaled, dscaled) ==
   scale(E**2, wedge(omega, dw)))

# Exact boundary correction in a fixed tubular chart, including moving graphs.
x, y, z, eps = sy.symbols("x y z eps")
coords = (x, y, z)
H = x*x + y*z + z
B = x*y + z*z + 1
C = x*z + y*y + 2
eta = (H, B, C)
U = x*x + eps*x
V = x*x*x - eps*x*x
subs = {y: U, z: V}
qgraph = sy.expand(sum(eta[i].subs(subs, simultaneous=True) *
                      [1, sy.diff(U, x), sy.diff(V, x)][i]
                      for i in range(3)))
chi = (1-(y-U)**2-(z-V)**2)**2
corrected = (H-qgraph*chi, B, C)
pullback = sy.expand(sum(corrected[i].subs(subs, simultaneous=True) *
                        [1, sy.diff(U, x), sy.diff(V, x)][i]
                        for i in range(3)))
ck("moving_boundary_exactly_legendrian", pullback == 0)
ck("moving_boundary_tangential_derivative_zero", sy.diff(pullback, x) == 0)
ck("moving_cutoff_value_one", sy.expand(chi.subs(subs, simultaneous=True)) == 1)
ck("graph_boundary_error_derivative_chain_rule",
   sy.expand(sy.diff(qgraph, x) -
     sum((sy.diff(eta[i], x) + sy.diff(eta[i], y)*sy.diff(U, x) +
          sy.diff(eta[i], z)*sy.diff(V, x)).subs(subs, simultaneous=True) *
         [1, sy.diff(U, x), sy.diff(V, x)][i]
         + eta[i].subs(subs, simultaneous=True) *
         [0, sy.diff(U, x, 2), sy.diff(V, x, 2)][i] for i in range(3))) == 0)

# Local model theta = dz + y dx: the correction is C1-small and leaves
# boundary transversality open. This is a chart diagnostic, not a global OT disk.
noise = (x*x + y + z, x+y*z, 1+x*z)
perturbed = (y+eps*noise[0], eps*noise[1], 1+eps*noise[2])
qb = perturbed[0].subs({y: 0, z: 0})
cb = (1-y*y-z*z)**2
fixed = (sy.expand(perturbed[0]-qb*cb), perturbed[1], perturbed[2])
ck("fixed_boundary_legendrian", fixed[0].subs({y: 0, z: 0}) == 0)
for i in range(3):
    difference = sy.expand(fixed[i] - [y, 0, 1][i])
    ck(f"correction_value_small_{i}", difference.subs(eps, 0) == 0)
    for j, coord in enumerate(coords):
        ck(f"correction_derivative_small_{i}{j}",
           sy.diff(difference, coord).subs(eps, 0) == 0)

def curl_form(a):
    return (sy.diff(a[2], y)-sy.diff(a[1], z),
            sy.diff(a[0], z)-sy.diff(a[2], x),
            sy.diff(a[1], x)-sy.diff(a[0], y))

contact = sy.expand(sum(a*b for a,b in zip(fixed, curl_form(fixed))))
ck("contact_model_limit_nonzero", contact.subs(eps, 0) == -1)
ck("boundary_transversality_limit",
   sy.expand((fixed[1]+fixed[2]).subs({y: 0, z: 0, eps: 0})) == 1)

# Rational controls for the uniform finite-interval error bound.
for i, (bound, lower) in enumerate(itertools.product(
        (Fraction(1, 10), Fraction(1), Fraction(10), Fraction(1000)),
        (Fraction(1, 1000), Fraction(1), Fraction(100), Fraction(100000)))):
    delta = min(Fraction(1), lower/(8*(bound+1)))
    ck(f"uniform_contact_margin_{i}",
       2*bound*delta+delta*delta < lower/2)

root = Path(__file__).resolve().parent
receipt = {
    "problem_id": 10300055,
    "status": "PASS",
    "assertions": len(checks),
    "sympy_version": sy.__version__,
    "candidate_sha256": hashlib.sha256((root/"CANDIDATE.md").read_bytes()).hexdigest(),
    "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope": "Finite exact differential-form and smoothing diagnostics only; "
             "not verification of the imported Eliashberg-Thurston or Gray theorems.",
    "checks": checks
}
print(json.dumps(receipt, indent=2, sort_keys=True))
