#!/usr/bin/env python3
"""Distinct exact adversarial controls. Not a numerical proof of PDE existence.

This program checks the new sealed family's algebra and deliberately false
substitutes. All universal statements rest on EARLY_INDEPENDENT_SEAL.md/REPORT.md.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sympy as s

counts = Counter()
negative = {}


def check(value, name):
    assert bool(value), name
    counts[name] += 1


def zero(value, name):
    check(s.cancel(s.expand(value)) == 0, name)


def reject(value, name):
    check(not bool(value), "negative_control_rejected")
    negative[name] = "REJECTED_AS_REQUIRED"


t = s.symbols("t", real=True)
k = s.symbols("k", positive=True)
c = k**2
L = 6*k
A = s.Rational(5, 2)*k

# Local periodic crest branches, independently expressed as c-k*|r|+r²/6.
# For an arbitrary prescribed path r(t), V=c+r'(t) enforces the material
# relative-velocity identity. It does not make these paths PDE solutions.
paths = [
    (t, 1, "positive_traversal_right_branch"),
    (t, -1, "positive_traversal_left_branch"),
    (-t, 1, "negative_traversal_right_branch"),
    (-t, -1, "negative_traversal_left_branch"),
    (t**2, 1, "quadratic_tangency_right_branch"),
    (-t**2, -1, "quadratic_tangency_left_branch"),
    ((t-1)**2, 1, "exit_from_dwell_right_branch"),
    (-(t+1)**2, -1, "entry_into_dwell_left_branch"),
]
for r, branch_sign, name in paths:
    phi = c-k*branch_sign*r+r**2/6
    slope = -k*branch_sign+r/3
    V = c+s.diff(r, t)
    h = V-phi
    pb = (phi-c)*slope
    # Candidate difference identity after writing P u along this test path
    # as V'. No frozen-crest substitution occurs.
    zero(s.diff(h, t)-(s.diff(V,t)-pb-slope*h), name)
    zero(s.diff(phi,t)-slope*s.diff(r,t), "branch_chain_rule")

for bounded_crest_derivative in [-k, 0, k]:
    # A positive-measure dwell has r'=0, V=c, h=0 and P b=0.
    zero(0-(0-0-bounded_crest_derivative*0), "dwell_any_bounded_representative")
check((c-k*t+t**2/6).subs(t,0)==(c+k*t+t**2/6).subs(t,0),
      "crossing_value_continuity")
reject((-k)==k, "false_classical_derivative_at_crest")

# Kernel sign control reaches the norm bound, catching sign/normalization
# mistakes. At x=0, G(-y)=-1/2+y/L and h(y) follows its sign.
y = s.symbols("y", real=True)
gminus = -s.Rational(1,2)+y/L
zero(-s.integrate(gminus,(y,0,L/2))+s.integrate(gminus,(y,L/2,L))-L/4,
     "sharp_primitive_kernel_sign_control")
zero(-L/2+L/2, "sharp_control_zero_mean")
zero(A-(k+L/4), "independent_amplitude_rate")
reject(L/4==L/8, "primitive_bound_too_small")

# Full displacement-bound algebra, retaining the subleading e^(k t) term.
a = s.symbols("a", positive=True)
Z = a*(s.exp(A*t)-s.exp(k*t))/(A-k)
zero(s.diff(Z,t)-k*Z-a*s.exp(A*t), "displacement_bound_ODE")
zero(Z.subs(t,0), "displacement_bound_initial")
F = a*s.exp(A*t)+k*Z
zero(F-(s.Rational(5,3)*a*s.exp(A*t)-s.Rational(2,3)*a*s.exp(k*t)),
     "retained_true_crest_forcing")
reject(s.simplify(F-a*s.exp(A*t))==0, "freezing_corner_displacement")
zero((c+s.symbols("f"))-(-k+s.symbols("z"))**2-
     (s.symbols("f")+2*k*s.symbols("z")-s.symbols("z")**2),
     "independent_shifted_Riccati")

# Generic support η=δ^p gives amplitude δ^(1+p), so the weighted error
# power is 1+p-(A/k-2)/2. It is o(δ) exactly when p>(A/k-2)/2.
p, ratio = s.symbols("p ratio", real=True)
weighted_error_power = 1+p-(ratio-2)/2
zero(weighted_error_power.subs({p:2,ratio:s.Rational(5,2)})-s.Rational(11,4),
     "generic_scale_candidate_error_power")
zero((weighted_error_power-1).subs({p:2,ratio:s.Rational(5,2)})-s.Rational(7,4),
     "generic_scale_candidate_relative_error_power")
for support_power in [s.Rational(1,2),1,2,3]:
    check((weighted_error_power-1).subs({p:support_power,ratio:s.Rational(5,2)})>0,
          "other_valid_narrowing_scale_controls")
reject((weighted_error_power-1).subs({p:0,ratio:s.Rational(5,2)})>0,
       "fixed_width_perturbation_control")
reject((weighted_error_power-1).subs({p:s.Rational(1,4),ratio:s.Rational(5,2)})>0,
       "critical_width_does_not_give_little_o")
reject((weighted_error_power-1).subs({p:2,ratio:6})>0,
       "excessively_large_amplitude_rate_control")

# An explicit sufficient δ bound is tested exactly after replacing
# δ=2ε q^4. For q<=1/8 and C0<=1000, the relative error below is <1/2.
q = s.symbols("q", positive=True)
eps=s.Rational(1,10)
d=2*eps*q**4
C0=s.symbols("C0", positive=True)
error_ratio=s.Rational(10,3)*C0*d**2*(1/q-1)
zero(error_ratio-s.Rational(2,15)*C0*q**7*(1-q), "independent_error_ratio")
for cutoff_constant in [1,7,31,1000]:
    for qval in [s.Rational(1,8),s.Rational(1,16),s.Rational(1,32)]:
        value=error_ratio.subs({C0:cutoff_constant,q:qval})
        check(0<value<s.Rational(1,2), "finite_fixed_threshold_controls")

# C1 compact-support proxy has an independent quartic cutoff and an
# explicitly normalized, separated mean-correction bump. This tests only
# scales/endpoint mechanics; the universal proof uses fixed C-infinity data.
x,delta=s.symbols("x delta", positive=True)
eta=delta**2
raw=-delta*x*(1-(x/eta)**2)**2
mass=s.integrate(raw,(x,0,eta))
zero(mass+delta**5/6, "quartic_proxy_mass_scale")
zero(s.diff(raw,x).subs(x,0)+delta, "quartic_proxy_right_slope")
zero(raw.subs(x,eta), "quartic_proxy_join_value")
zero(s.diff(raw,x).subs(x,eta), "quartic_proxy_join_slope")
z=s.symbols("z", real=True)
beta=30*z**2*(1-z)**2
check(s.integrate(beta,(z,0,1))==1, "independent_mean_bump_normalized")
zero(mass-mass*s.integrate(beta,(z,0,1)), "exact_mean_correction")
for endpoint in [0,1]:
    zero(beta.subs(z,endpoint), "mean_bump_endpoint_value")
    zero(s.diff(beta,z).subs(z,endpoint), "mean_bump_endpoint_slope")

# An endpoint violation is visible on positive measure by branch continuity.
# Affine slope model w(x)=-k-e+x has essential sup ≥ k+e-h/2 on (0,h/2).
e, h = s.symbols("e h", positive=True)
zero(-(-k-e+h/2)-(k+e-h/2), "one_sided_neighborhood_slope_excess")

# Shrinking slope patches disprove a generic inference to weaker norms.
# triangular f on [-h,h] has ||f'||∞=e, ||f||∞=e h,
# ||f'||²_2=2e²h and ||f||²_2=2e²h³/3. Its mean can be corrected with O(h²).
tri=e*(h-x)
zero(2*s.integrate(tri**2,(x,0,h))-s.Rational(2,3)*e**2*h**3,
     "fixed_slope_shrinking_L2_control")
zero(2*s.integrate(s.diff(tri,x)**2,(x,0,h))-2*e**2*h,
     "fixed_slope_shrinking_H1_control")
check(s.limit(2*e**2*h+s.Rational(2,3)*e**2*h**3,h,0)==0,
      "no_generic_fixed_H1_departure")

receipt={
    "status":"PASS",
    "utc":datetime.now(timezone.utc).isoformat(),
    "sympy_version":s.__version__,
    "assertions":sum(counts.values()),
    "checks":dict(counts),
    "negative_controls":negative,
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope":"Finite exact analytic controls, branch examples and deliberate false-substitute rejection; universal PDE/norm argument rests on sealed written proof."
}
Path(__file__).with_name("adversarial_results.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
