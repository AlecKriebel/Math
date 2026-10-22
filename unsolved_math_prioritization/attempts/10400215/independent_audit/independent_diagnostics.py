"""Independent exact controls. These are finite algebra checks, not topology certificates."""
from fractions import Fraction
from itertools import product
import json

Q = Fraction
counts = {}
def require(label, condition):
    if not condition:
        raise RuntimeError('Independent check failed: ' + label)
    counts[label] = counts.get(label, 0) + 1

# Include the empty JSJ hyperbolic list and arbitrary zero-norm entries.
for r in range(0, 6):
    for terms in product((Q(0), Q(1,7), Q(2,3), Q(5,2)), repeat=r):
        total = sum(terms, Q(0))
        maximum = max(terms, default=Q(0))
        squares = sum((g*g for g in terms), Q(0))
        deficit = sum((g*(maximum-g) for g in terms), Q(0))
        require('sum_square_deficit_identity', maximum*total-squares == deficit >= 0)
        require('quadratic_refinement', squares <= maximum*total <= total*total)
        if not total:
            require('empty_and_zero_piece_lists', squares == maximum == 0)
            continue
        ratios = tuple(Q((i+1)**2, i+3) for i in range(r))
        weighted = sum((g*z for g,z in zip(terms,ratios)), Q(0))
        high = max(ratios)
        require('weighted_deficit_identity', high*total-weighted == sum((g*(high-z) for g,z in zip(terms,ratios)), Q(0)))
        require('selected_piece_ratio_bound', weighted/total <= high)

# The polynomial has exactly the sign of the integer-rounding criterion.
# t = (L/(2*pi))^2; no approximation to pi or fractional powers is used.
for n in range(1, 6001):
    t = Q(3*n,2)
    polynomial = n*n*(t-1)**3-(n-1)**2*t**3
    require('independent_cubic_clear_denominators', polynomial == Q(n*n*(9*n-8),8))
    require('strict_integer_rounding_margin', polynomial > 0)
    require('valid_hyperbolic_slope_domain', t > 1)
    normalized_lower_square = n*n*((t-1)/t)**3
    require('only_integer_n_can_remain', (n-1)**2 < normalized_lower_square < n*n)
    require('improvement_over_old_cutoff', t < 2*n)
    for multiplier in (Q(1),Q(7,6),Q(5,2)):
        u=t*multiplier
        require('longer_slopes_preserve_strict_margin', n*n*(u-1)**3 > (n-1)**2*u**3)

# Explicit small-n controls for the full admissible integer range.
for n in range(1,21):
    t=Q(3*n,2)
    allowed=[s for s in range(n+1) if s*s >= n*n*((t-1)/t)**3]
    require('small_n_integer_enumeration', allowed == [n])
# An endpoint with zero margin does not justify strict integer rounding.
require('n1_exact_endpoint_is_excluded', Q(1-1)**3 == Q(0))
for d in range(2,201):
    t=Q(d+1,d)
    require('n1_every_strictly_long_slope', (t-1)**3 > 0)

# Coefficient alpha < 3/2 fails eventually in this particular rounding test.
for denominator in range(2,51):
    alpha=Q(3,2)-Q(1,denominator)
    n=10000*denominator
    t=alpha*n
    require('smaller_asymptotic_coefficient_fails', n*n*(t-1)**3 < (n-1)**2*t**3)

for numerator in range(1,18):
    for denominator in range(1,18):
        sqrtC=Q(numerator,denominator)
        C=sqrtC**2
        for offset in (Q(0),Q(1,9),Q(7,3)):
            G=1/sqrtC+offset
            A=Q(numerator+2,13)
            D=Q(denominator+3,11)
            require('norm_gap_squared', C*G*G >= 1)
            require('affine_absorption_varied_rationals', A*G+D <= (A+D*sqrtC)*G)
        for factor in (Q(1,7),Q(2,3),Q(99,100)):
            G=factor/sqrtC
            require('subgap_precludes_positive_integral_shadow', C*G*G < 1)

for m in range(1,6001):
    G=Q(m); s=m*m; quantum=Q(m)
    require('quantum_upper_bounds_do_not_control_shadow', quantum<=s and quantum<=G and G<=s<=G*G)
    require('unbounded_numerical_ratio_formula', s/G==m)

out={'schema':1,'status':'pass','total_checks':sum(counts.values()),'checks':counts,
     'scope':'Exact finite algebra and small-integer controls only; no manifold realization, topology certificate, novelty assessment, or full-conjecture proof.'}
print(json.dumps(out,sort_keys=True,indent=2))
