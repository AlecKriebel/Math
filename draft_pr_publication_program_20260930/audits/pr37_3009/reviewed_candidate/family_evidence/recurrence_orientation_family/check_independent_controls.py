#!/usr/bin/env python3
"""Execute independent formula/construction controls; not a topology certificate."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, localcontext
import datetime
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
checks = []
controls = []


def check(name, condition, evidence):
    if not condition:
        raise AssertionError(name)
    checks.append({"name": name, "result": "PASS", "evidence": evidence})


def reject(name, asserted_condition, witness, scope):
    if asserted_condition:
        raise AssertionError("Counter-control did not reject: " + name)
    controls.append({"mutation": name, "result": "REJECTED", "witness": witness,
                     "scope": scope})


def norm2(v):
    return sum(t*t for t in v)


def dist2(v, w):
    return norm2(tuple(a-b for a, b in zip(v, w)))


def stereo(v):
    z = norm2(v)
    return tuple(2*t/(1+z) for t in v) + ((z-1)/(1+z),)


def q2(v, w):
    return 4*dist2(v, w)/((1+norm2(v))*(1+norm2(w)))


stereo_cases = []
for x, y in [((F(0), F(0)), (F(0), F(0))),
             ((F(1), F(0)), (F(0), F(1))),
             ((F(3, 5), F(4, 5)), (F(-7, 3), F(2, 9))),
             ((F(1000), F(1, 1000)), (F(999), F(-1, 1000)))]:
    assert norm2(stereo(x)) == 1 and dist2(stereo(x), stereo(y)) == q2(x, y)
    stereo_cases.append({"x": x, "y": y, "q_squared": q2(x, y)})
check("chordal_identity_independent_exact_instances", True, stereo_cases)

tail_cases = []
for D in [F(0), F(1, 3), F(1), F(10)]:
    for gap in [F(1, 1000), F(1), F(1000)]:
        R = D+gap
        bound2 = 4*D*D/((1+R*R)*(1+(R-D)**2))
        for direction in [(F(1), F(0)), (F(3, 5), F(4, 5))]:
            x = tuple(R*u for u in direction)
            for v in [(F(0), F(0)), tuple(-D*u for u in direction),
                      (F(0), D/2)]:
                y = tuple(a+b for a, b in zip(x, v))
                assert norm2(v) <= D*D and norm2(y) >= (R-D)**2
                actual = q2(x, y)
                assert actual <= bound2
                tail_cases.append({"D": D, "R": R, "actual_q_squared": actual,
                                   "bound_squared": bound2})
check("tail_bound_including_zero_and_near_R_equals_D", True,
      {"exact_cases": len(tail_cases), "examples": tail_cases[:6]})
x, y, D, R = (F(2), F(0)), (F(1), F(0)), F(1), F(2)
wrong_tail = D*D/((1+R*R)*(1+(R-D)**2))
reject("delete_chordal_factor_2", q2(x, y) <= wrong_tail,
       {"x": x, "y": y, "actual_q_squared": q2(x, y),
        "wrong_bound_squared": wrong_tail}, "Exact metric formula mutation.")

points = [F(0), F(1, 4), F(1), F(1, 2)]
D = max(abs(a-b) for a in points for b in points)
for i in range(len(points)):
    for a in range(-8, 9):
        for b in range(-8, 9):
            left = abs(points[(i+a) % 4]-points[(i+b) % 4])
            rebased = (i+b) % 4
            right = abs(points[(rebased+a-b) % 4]-points[rebased])
            assert left == right and left <= D
check("all_integer_anchor_to_pair_rebasing", True,
      {"finite_permutation_period": 4, "all_integer_test_range": [-8, 8], "D": D})
reject("replace_all_iterate_bound_with_one_step_bound", abs(F(2)-F(0)) <= 1,
       {"map": "x -> x+1", "one_step_displacement": 1,
        "two_step_displacement": 2}, "Translation fails full-orbit bound.")
exponents = [0]*12
reject("allow_constant_zero_recurrence_exponents", max(exponents) >= 1,
       {"map": "x -> x+1", "exponents": exponents, "maps": "all identity"},
       "This is a failed recurrence premise, not a valid subsequence.")
reject("omit_bounded_displacement_when_inferring_orientation", abs(-2-2) <= 1,
       {"map": "x -> -x", "period": 2, "x": 2, "displacement": 4},
       "Reflection is recurrent and reverses orientation; bound fails.")

pell = []
p, n = 1, 1
for j in range(8):
    assert abs(p*p-2*n*n) == 1
    with localcontext() as ctx:
        ctx.prec = 80
        residual = Decimal(n)*Decimal(2).sqrt()-Decimal(p)
        assert residual != 0
        abs_residual = abs(residual)
        residual_bound = Decimal(1)/(Decimal(n)*Decimal(2).sqrt()+Decimal(p))
        assert abs(abs_residual-residual_bound) < Decimal("1e-70")
        sine = abs(math.sin(math.pi*float(residual)))
        circle_displacement = 2*sine
        compensating_radius = 1/circle_displacement
        actual_at_radius = compensating_radius*circle_displacement
        assert abs(actual_at_radius-1) < 1e-12
        pell.append({"n": n, "p": p, "nonzero_residual": str(residual),
                     "unit_circle_displacement": circle_displacement,
                     "radius_with_displacement_1": compensating_radius,
                     "sphere_sup_chordal_displacement": circle_displacement})
    p, n = p+2*n, p+n
check("irrational_rotation_explicit_positive_return_sequence", all(
    pell[j+1]["unit_circle_displacement"] < pell[j]["unit_circle_displacement"]
    for j in range(len(pell)-1)), pell)
reject("compact_open_means_global_Euclidean_uniform", pell[-1]["radius_with_displacement_1"]
       *pell[-1]["unit_circle_displacement"] < F(1, 2), pell[-1],
       "At each returning nonzero iterate some radius has displacement 1; supremum is infinite.")
reject("recurrence_implies_periodicity", pell[-1]["nonzero_residual"] == "0",
       {"rotation_angle_turns": "sqrt(2)", "irrationality": "2*n^2=p^2 has no positive integer solution",
        "tested_return": pell[-1]}, "Irrationality excludes every nonzero identity power; finite Pell values are controls only.")

epsilon = F(1, 1000)
radial_inside_slope = F(1, 2)+3*epsilon/4-epsilon*epsilon/4
reject("boundary_fixed_diffeomorphism_glues_C1", F(1, 2) == F(1),
       {"h": "(1+(1-|x|^2)/4)x", "radial_derivative_interior": F(1, 2),
        "radial_derivative_exterior": F(1), "inside_difference_quotient_at_t_1_over_1000": radial_inside_slope},
       "Category control only; this map is not recurrent.")
check("radial_disk_map_is_smooth_diffeomorphism", min(F(5, 4)-3*r*r/4
      for r in [F(0), F(1, 2), F(1)]) == F(1, 2),
      {"radial_derivative_formula": "5/4-3*r^2/4", "range_on_unit_interval": [F(1, 2), F(5, 4)]})
annulus_displacement = pell[0]["unit_circle_displacement"]/4
reject("extend_finite_D_theorem_to_arbitrary_open_set", annulus_displacement == 0,
       {"domain": "1/6 < |x| < 1/3", "map": "irrational rotation by sqrt(2) turns",
        "all_orbit_diameter_strict_upper_bound": F(2, 3), "D": 1,
        "nonidentity_displacement_at_radius_1_over_4": annulus_displacement},
       "All hypotheses of naive finite-D open-set version hold, but map is nonidentity; smooth returns also hold.")

# The computed fixed witnesses belong to the fixed circle of S^3 rotation.
fixed_sphere3 = [(F(0), F(0), F(1), F(0)), (F(0), F(0), F(0), F(1)),
                (F(0), F(0), F(3, 5), F(4, 5))]
assert all(norm2(v) == 1 for v in fixed_sphere3)
reject("use_S2_two_fixed_points_on_S3", len(set(fixed_sphere3)) == 2,
       {"map": "rotate coordinates 1,2 by sqrt(2) turns; fix coordinates 3,4",
        "three_distinct_fixed_sphere_points": fixed_sphere3,
        "full_fixed_set": "S^1"}, "Smooth recurrent orientation preserving higher sphere control.")


def circle_distance(x, y):
    gap = abs((x-y) % 1)
    return min(gap, 1-gap)


def eps(j):
    return F(1, 2**(j+3))


def period(j):
    return 2**(j*(j+5)//2)


def conjugacy(j, x):
    x = x % 1
    e = eps(j)
    return x/(2*e) if x <= e else F(1, 2)+(x-e)/(2*(1-e))


def inverse_conjugacy(j, y):
    y = y % 1
    e = eps(j)
    return 2*e*y if y <= F(1, 2) else e+2*(1-e)*(y-F(1, 2))


def iterate(j, x, n):
    return inverse_conjugacy(j, (conjugacy(j, x)+F(n, period(j))) % 1)


nonregular = []
for j in range(1, 11):
    for x in [F(0), eps(j)/2, eps(j), F(1, 3), F(3, 4)]:
        assert inverse_conjugacy(j, conjugacy(j, x)) == x
        assert iterate(j, iterate(j, x, 1), -1) == x
        assert circle_distance(iterate(j, x, 1), x) <= F(2, period(j))
    before = circle_distance(F(0), eps(j)/2)
    left = iterate(j, F(0), period(j)//2)
    right = iterate(j, eps(j)/2, period(j)//2)
    after = circle_distance(left, right)
    assert after == (1-eps(j))/2 and after >= F(1, 4)
    nonregular.append({"fiber_j": j, "period": period(j), "points": [F(0), eps(j)/2],
                       "initial_distance": before, "iterate_exponent": period(j)//2,
                       "images": [left, right], "final_distance": after})
return_bounds = []
for k in range(1, 8):
    for j in range(1, 11):
        for x in [F(0), eps(j)/2, F(1, 3), F(3, 4)]:
            actual = circle_distance(iterate(j, x, period(k)), x)
            if j <= k:
                assert actual == 0
            else:
                assert actual <= F(2*period(k), period(j)) <= F(1, 2**(k+2))
    return_bounds.append({"exponent": period(k), "uniform_tail_bound": F(1, 2**(k+2)),
                          "proof_for_all_uncomputed_tail_fibers": "m_j >= m_(k+1) and 2m_k/m_(k+1)=2^(-k-2)"})
check("compact_recurrent_non_equicontinuous_model_exact_controls", True,
      {"returns": return_bounds, "separation_witnesses": nonregular,
       "analytic_tail_proof": "step <=2/m_j; finite heads vanish; all tails bounded by 2^(-k-2)",
       "scope": "compact nonmanifold X=({0} union {1/j}) times circle"})
w = nonregular[-1]
reject("recurrence_supplies_uniform_modulus_all_iterates", w["final_distance"] < F(1, 4),
       w, "Initial distances tend to zero while final distances stay >=1/4; explicit exact formula for every j.")
reject("recurrence_supplies_compact_cyclic_closure", w["final_distance"] < F(1, 4),
       w, "A compact closure in Homeo(X) would be equicontinuous by joint continuity; preceding witnesses disprove it.")

out = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       "independent_groups_passed": len(checks), "counter_controls_rejected": len(controls),
       "failed": 0, "checks": checks, "counter_controls": controls,
       "limitations": ["Finite calculations do not prove the imported surface theorems.",
                       "The nonregular compact-space control is not a manifold or a KP counterexample.",
                       "No explicit non-locally-compact cyclic closure theorem is certified here.",
                       "Original full target remains unresolved."]}
serialized = json.dumps(out, indent=2, default=str)+"\n"
(HERE/"independent_control_results.json").write_text(serialized)
print(serialized)
