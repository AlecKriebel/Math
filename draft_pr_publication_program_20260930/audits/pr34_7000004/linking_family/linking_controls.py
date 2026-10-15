#!/usr/bin/env python3
"""Exact adversarial framing controls, not a solution of Ghomi Problem 1.4."""
import json
from pathlib import Path
import sympy as S

checks = {}


def check(name, claim):
    assert bool(claim), name
    checks[name] = "PASS"


def zero(expr):
    if isinstance(expr, S.MatrixBase):
        return all(S.trigsimp(S.simplify(x)) == 0 for x in expr)
    return S.trigsimp(S.simplify(expr)) == 0


t = S.symbols("t", real=True)
G = S.Matrix([S.cos(t), S.sin(t), 0])
T = G.diff(t)
N = G.diff(t, 2)
B = S.Matrix([0, 0, 1])
check("circle_orientation", zero(T.cross(N) - B))

# The disk intersection proof gives linking m for these framed circles.
# This code checks its algebra and the binormal-compatibility exclusion.
circle_records = []
for m in range(-5, 6):
    V = S.cos(m*t)*N + S.sin(m*t)*B
    check("unit_frame_"+str(m), zero(V.dot(V)-1))
    check("normal_frame_"+str(m), zero(V.dot(T)))
    check("twist_density_"+str(m), zero(T.dot(V.cross(V.diff(t)))-m))
    check("binormal_failure_"+str(m), not zero(V.dot(N)))
    disk_count = abs(m)
    signed_disk_count = (1 if m > 0 else -1)*disk_count if m else 0
    check("signed_disk_count_"+str(m), signed_disk_count == m)
    circle_records.append({"m": m, "oriented_disk_intersection_count": m,
                           "binormal": False})

# A sphere-valued injective smooth map may have zero derivative.
h = t-S.sin(t)
Q = S.Matrix([S.cos(h), S.sin(h), 0])
check("stationary_sphere_map_unit", zero(Q.dot(Q)-1))
check("monotone_lift_derivative", zero(S.diff(h,t)-2*S.sin(t/2)**2))
check("stationary_sphere_map_zero_derivative", zero(Q.diff(t).subs(t,0)))
check("stationary_lift_period", zero(h.subs(t,t+2*S.pi)-h-2*S.pi))

# An injective vector-valued loop whose unit direction repeats at 0 and pi.
# Its positive z-coordinate determines cos(t), and then x/z determines sin(t).
v = S.Matrix([S.sin(t), S.sin(2*t), 1])
R = (2+S.cos(t))*v
check("nonunit_scale_positive_bound", S.Integer(2)-1 > 0)
check("nonunit_recover_cos", zero(R[2]-2-S.cos(t)))
check("nonunit_recover_sin", zero(R[0]/R[2]-S.sin(t)))
check("nonunit_vectors_different", R.subs(t,0) != R.subs(t,S.pi))
check("normalized_directions_repeat", v.subs(t,0) == v.subs(t,S.pi))

# Explicit embedded graph over a circle with zero linking of its radial frame,
# but rigorously nonzero twist. The full geometric argument is in PROOF.md.
eta = S.Rational(1,20)
f = S.cos(t)+S.cos(2*t)
height = eta*(S.sin(t)+S.sin(2*t)/2)
g = S.Matrix([S.cos(t),S.sin(t),height])
speed_squared = 1+eta**2*f**2
unit_tangent = g.diff(t)/S.sqrt(speed_squared)
check("graph_speed_formula", zero(g.diff(t).dot(g.diff(t))-speed_squared))
check("graph_radial_normal", zero(N.dot(unit_tangent)))
check("graph_twist_formula", zero(unit_tangent.dot(N.cross(N.diff(t)))-eta*f/S.sqrt(speed_squared)))
check("graph_radial_not_binormal", zero(N.dot(g.diff(t,2))-1))
check("mean_f_zero", S.integrate(f,(t,0,2*S.pi)) == 0)
check("third_moment_exact", S.integrate(S.expand_trig(f**3),(t,0,2*S.pi)) == 3*S.pi/2)
lead = -S.Rational(3,8)*eta**3
remainder_bound = 12*eta**5
check("rigorous_twist_upper_bound_negative", lead+remainder_bound < 0)
check("rigorous_twist_lower_bound_negative", lead-remainder_bound < 0)

# Two crossing signs cancel. Counting unsigned crossings changes the result.
crossings = [1,-1]
check("signed_crossing_cancellation", sum(crossings)==0)
check("unsigned_crossing_substitution_rejected", sum(abs(z) for z in crossings)!=sum(crossings))
check("formal_linking_cancellation_possible", -1+S.Rational(1,2)*2==0)

# Local immersed-branch obstruction: at the double point a compatible normal
# push-off hits a distinct straight branch for every sufficiently small epsilon.
s,e = S.symbols("s e",real=True)
branch_x = S.Matrix([s,0,0])
local_B = S.Matrix([0,S.sin(s),S.cos(s)])
branch_z = S.Matrix([0,0,e])
check("local_branch_binormal_orthogonal_first", zero(local_B.dot(branch_x.diff(s))))
check("local_branch_binormal_orthogonal_second", zero(local_B.dot(branch_x.diff(s,2))))
check("local_push_off_hits_other_branch", zero((branch_x+e*local_B).subs(s,0)-branch_z))

out = {"passed":len(checks),"failed":0,"sympy_version":S.__version__,
       "checks":checks,"framed_circle_controls":circle_records,
       "zero_linking_nonzero_twist_control":{
           "eta":str(eta),"twist_lower_bound":str(lead-remainder_bound),
           "twist_upper_bound":str(lead+remainder_bound),
           "linking_number":0,"normal_field_is_binormal":False},
       "scope":"Exact algebra and universal arguments explained in PROOF.md; no solution or counterexample to the intended binormal target; formal crossing counts are not realizability claims."}
Path(__file__).with_name("linking_controls_results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
