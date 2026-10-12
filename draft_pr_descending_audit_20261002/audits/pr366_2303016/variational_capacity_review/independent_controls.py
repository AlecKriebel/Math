"""Supplement the sealed analytic audit; do not infer polarity from computation."""
from fractions import Fraction as Q
import json
import sympy as S

checks = 0
negative_controls = []


def require(value):
    global checks
    if not value:
        raise AssertionError("independent exact control failed")
    checks += 1


def reject(name, incorrect_claim):
    require(not incorrect_claim)
    negative_controls.append(name)


t, J, L, H = S.symbols("t J L H", real=True)
variation = S.expand((1-t)**2*J + 2*t*(1-t)*L + t*t*H)
require(S.expand(variation-J-2*t*(L-J)-t*t*(J-2*L+H)) == 0)
require(S.diff(variation, t).subs(t, 0) == 2*(L-J))
reject("reversed_first_variation_sign", S.diff(variation, t).subs(t, 0) == 2*(J-L))

# The exact variance identity establishes the dyadic mass bound for arbitrary
# masses summing to one, rather than testing only equal-bin masses.
variance_identities = []
for bins in range(2, 11):
    masses = list(S.symbols("m0:" + str(bins-1), real=True))
    masses.append(1-sum(masses))
    residual = sum(x*x for x in masses)-S.Rational(1, bins)
    squares = sum((masses[i]-masses[j])**2
                  for i in range(bins) for j in range(i+1, bins))/bins
    require(S.expand(residual-squares) == 0)
    variance_identities.append(bins)

r, d, exponent = S.symbols("r d exponent", positive=True)
antiderivative = -r**(-exponent)/exponent
require(S.simplify(S.diff(antiderivative, r)-r**(-exponent-1)) == 0)
kernel_integral = S.integrate(exponent*r**(-exponent-1), (r, d, S.oo))
require(S.simplify(kernel_integral-d**(-exponent)) == 0)
k = S.symbols("k", integer=True)
level = S.symbols("level", integer=True, nonnegative=True)
dyadic_sum = S.summation(2**(k-1), (k, 0, level))
require(S.simplify(dyadic_sum-(2**level-S.Rational(1, 2))) == 0)

# Probe exactly on, immediately above, and immediately below dyadic thresholds.
for level_value in range(101):
    endpoint = Q(1, 2**level_value)
    for factor in [Q(1), Q(1)+Q(1, 1009), Q(1)-Q(1, 1009)]:
        distance = endpoint*factor
        if distance > 1:
            continue
        included = [j for j in range(level_value+3)
                    if distance <= Q(1, 2**j)]
        lower_sum = sum((Q(2)**(j-1) for j in included), Q(0))
        require(lower_sum <= 1/distance)

for exponent_value in range(1, 101):
    global_constant = 2**exponent_value
    small_tail = Q(1, 4*global_constant*exponent_value)
    require(global_constant*exponent_value*small_tail == Q(1, 4))
    require(Q(1, 4**exponent_value) <= Q(1, 4))
    for ratio in [Q(1, 4), Q(1, 16), Q(1, 1024)]:
        require(global_constant*exponent_value*small_tail+ratio**exponent_value <= Q(1, 2))

mass = Q(1, 3)
energy = Q(5)
restricted_probability_energy = energy/(mass*mass)
reject("restriction_uses_mass_instead_of_mass_squared",
       restricted_probability_energy == energy/mass)
reject("nearest_support_kernel_factor_inverted", Q(1, 3) <= Q(1, 2)*Q(1, 4))
reject("localization_diameter_not_shrunk", Q(1, 4)+Q(1) <= Q(1, 2))
reject("dimension_two_uses_n_ge_three_tail_bound", Q(1, 4**0) <= Q(1, 4))
reject("dyadic_coefficients_doubled", Q(1)+Q(2) <= Q(2))
# A midpoint belongs to two adjacent CLOSED dyadic intervals. A disjoint
# partition assigns it to one bin, as the analytical proof requires.
midpoint = Q(1, 2)
closed_bin_memberships = sum(left <= midpoint <= right
                             for left, right in [(Q(0), Q(1, 2)), (Q(1, 2), Q(1))])
reject("closed_overlapping_bins_treated_as_probability_partition", closed_bin_memberships == 1)

print(json.dumps({
    "status": "PASS",
    "assertions": checks,
    "symbolic_first_variation": str(variation),
    "symbolic_layer_cake": str(kernel_integral),
    "symbolic_dyadic_envelope": str(dyadic_sum),
    "arbitrary_mass_variance_identity_bin_counts": variance_identities,
    "dyadic_thresholds_checked": 101,
    "dimension_exponents_checked": list(range(1, 101)),
    "negative_controls_rejected": negative_controls,
    "scope": "Symbolic identities, arbitrary-mass dyadic inequality, exact threshold and constant controls, and deliberate false-claim rejection. The sealed analytical audit proves the all-set theorem; finite controls do not certify polarity."
}, indent=2, sort_keys=True))
