#!/usr/bin/env python3
"""Independent exact controls; infinite/metric/normal claims still require proofs.

No projection solver, finite sampling of a conjecture, network, or input mutation.
"""
import json
from collections import Counter
import sympy as s

counts = Counter()
def check(value, name):
    assert bool(value), name
    counts[name] += 1
def equal(actual, expected, name):
    check(s.simplify(actual - expected) == 0, name)

t, c = s.symbols("t c", positive=True)
z = s.symbols("z")
x, y, u, v, X, U, V = s.symbols("x y u v X U V", real=True)
I = s.I
p = z*z + t*t*z + t*t + I*t**3
equal(s.expand((z+I*t)*(z+t*t-I*t)), p, "factorization")
equal(p.subs(z, -I*t), 0, "active_root")
equal(p.subs(z, -t*t+I*t), 0, "strict_other_root")

# Centering leaves each root's real part invariant.
shift = s.expand((z-I*y/2)**2 + (x+I*y)*(z-I*y/2) + u+I*v)
equal(shift, z*z+x*z+u+y*y/4+I*(v-x*y/2), "centered_chart")
equal((X*X+4*U)**2 - ((X*X-4*U)**2+16*V*V),
      16*(X*X*U-V*V), "stability_squaring_identity")
phi = v-x*y/2-x*s.sqrt(u+y*y/4)
pt = {x:t*t, y:0, u:t*t, v:t**3}
n = s.Matrix([-t, -t*t/2, -t/2, 1])
for j, coordinate in enumerate([x, y, u, v]):
    equal(s.diff(phi, coordinate).subs(pt), n[j], "chart_gradient")
equal(phi.subs(pt), 0, "upper_constraint_active")
equal((v-x*y/2+x*s.sqrt(u+y*y/4)).subs(pt), 2*t**3,
      "lower_constraint_strict")

# Independently solve the implicit derivative, including every real direction.
lam = -I*t
D = 2*lam+t*t
gamma = 2/(t*(t*t+4))
directions = [lam, I*lam, 1, I]
expected = [-2/(t*t+4), -t/(t*t+4), -1/(t*t+4),
            2/(t*(t*t+4))]
for j, derivative in enumerate([-q/D for q in directions]):
    equal(s.re(derivative), expected[j], "implicit_monic_gradient")
    equal(expected[j], gamma*n[j], "gradient_normal_scaling")
N = s.Matrix([t**3/2, -t*t, *n])
for j, direction in enumerate([lam*lam, I*lam*lam]+directions):
    equal(s.re(-direction/D), gamma*N[j], "implicit_full_gradient")

# A scale family, with the original sqrt(2) case as a specialization.
delta = s.Matrix([(c*c-1)*t*t, 0, (c*c-1)*t*t, (c**3-1)*t**3])
equal(n.dot(delta), (c-1)**2*(c+s.Rational(1,2))*t**3,
      "general_scale_support_factored")
equal(delta.dot(delta), 2*(c*c-1)**2*t**4+(c**3-1)**2*t**6,
      "general_scale_distance")
original_delta = delta.subs(c,s.sqrt(2))
coef = 2*s.sqrt(2)-s.Rational(5,2)
check(coef>0, "sqrt2_positive_support")
equal(n.dot(original_delta), coef*t**3, "original_support")
equal(s.limit(t*n.dot(original_delta)/original_delta.dot(original_delta),
              t,0,dir="+"),coef/2, "original_exact_rate")

# Simpler base-point comparisons furnish direct failures of proximal normality.
w = s.Matrix([t*t, 0, t*t, t**3])
n0 = s.Matrix([0,0,0,1])
equal(n.dot(-w), t**3/2, "normal_to_base_support")
equal(n0.dot(w), t**3, "base_normal_support")
equal(w.dot(w), 2*t**4+t**6, "base_distance")
equal(s.limit(t*n.dot(-w)/w.dot(w),t,0,dir="+"),s.Rational(1,4),
      "normal_to_base_exact_rate")
equal(s.limit(t*n0.dot(w)/w.dot(w),t,0,dir="+"),s.Rational(1,2),
      "base_normal_exact_rate")

epin = s.Matrix([*n, -1/gamma])
epifull = s.Matrix([*N, -1/gamma])
for nn, ambient, target_index in [(n,4,3),(N,6,5),(epin,5,3),(epifull,7,5)]:
    for j in range(ambient):
        equal(s.limit(nn[j],t,0,dir="+"),int(j==target_index),
              "bounded_normal_limit")
check(s.limit(gamma,t,0,dir="+")==s.oo, "gradient_diverges")
equal(epin.dot(s.Matrix([*original_delta,0])),coef*t**3,
      "epigraph_support")
equal(epifull.dot(s.Matrix([0,0,*original_delta,0])),coef*t**3,
      "full_epigraph_support")

# General symmetric G: support is invariant as a covector, while distance's
# leading coefficient is e^T G e. Its strict positivity is the SPD hypothesis,
# proved analytically in the report, rather than inferred from finite matrices.
for dimension, e_indices, f_index in [(4,[0,2],3),(6,[2,4],5),
                                      (5,[0,2],3),(7,[2,4],5)]:
    entries = {}
    G = s.zeros(dimension)
    for j in range(dimension):
        for k in range(j,dimension):
            entries[j,k] = s.symbols(f"g{dimension}_{j}_{k}",real=True)
            G[j,k] = G[k,j] = entries[j,k]
    e = s.Matrix([int(j in e_indices) for j in range(dimension)])
    f = s.Matrix([int(j==f_index) for j in range(dimension)])
    displacement = t*t*e+t**3*f
    distance = (displacement.T*G*displacement)[0]
    equal(distance/t**4,(e.T*G*e)[0]+2*t*(e.T*G*f)[0]+t*t*(f.T*G*f)[0],
          "arbitrary_metric_distance_polynomial")
    equal(s.limit(distance/t**4,t,0,dir="+"),(e.T*G*e)[0],
          "arbitrary_metric_leading_coefficient")

# Exact boundary cases reinforce which sign conventions the analytic chart uses.
cases = [(0,0,0,True),(0,1,0,True),(0,-1,0,False),(0,1,1,False),
         (1,0,0,True),(1,1,1,True),(1,1,-1,True),(1,1,2,False),
         (-1,1,0,False),(2,1,2,True),(2,1,-2,True)]
for xx,uu,vv,stable in cases:
    root_real_magnitude = s.sqrt((s.sqrt((xx*xx-4*uu)**2+16*vv*vv)+xx*xx-4*uu)/2)
    alpha = (-xx+root_real_magnitude)/2
    check(bool(alpha<=0)==stable,"exact_chart_boundary_cases")
    chart = xx>=0 and uu>=0 and vv*vv<=xx*xx*uu
    check(chart==stable,"closed_chart_boundary_cases")

print(json.dumps({"status":"PASS", "exact_assertions":sum(counts.values()),
                  "counts":dict(sorted(counts.items())),
                  "floating_diagnostics":0,
                  "scope":"Exact symbolic identities and finite boundary controls; global proximal-normal, closedness, universal SPD, and projection implications are proved separately."},
                 indent=2,sort_keys=True))
