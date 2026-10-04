#!/usr/bin/env python3
"""Independent standard-library controls; analytic conclusions are in REPORT.md.

No candidate programs or CSV tables are imported. The polynomial certificate
uses a sharp rank-one inverse bound, distinct from the candidate envelope.
"""
from fractions import Fraction as F
from math import tanh, comb
import itertools
import json
import random

counts = {}

def ck(category, condition):
    if not condition:
        raise AssertionError(category)
    counts[category] = counts.get(category, 0) + 1

class Poly:
    """Sparse exact polynomials in beta,m,s,a."""
    def __init__(self, terms):
        self.terms = {k: F(v) for k, v in terms.items() if v}
    def __add__(self, other):
        other = cast(other)
        out = dict(self.terms)
        for k, v in other.terms.items():
            out[k] = out.get(k, F(0)) + v
        return Poly(out)
    __radd__ = __add__
    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})
    def __sub__(self, other):
        return self + (-cast(other))
    def __rsub__(self, other):
        return cast(other) - self
    def __mul__(self, other):
        other = cast(other)
        out = {}
        for k, v in self.terms.items():
            for l, w in other.terms.items():
                exp = tuple(x + y for x, y in zip(k, l))
                out[exp] = out.get(exp, F(0)) + v * w
        return Poly(out)
    __rmul__ = __mul__
    def __pow__(self, n):
        out = cast(1)
        for _ in range(n):
            out = out * self
        return out

def cast(x):
    return x if isinstance(x, Poly) else Poly({(0, 0, 0, 0): F(x)})

variables = [Poly({tuple(int(i == j) for i in range(4)): 1}) for j in range(4)]
beta, m, s, a = variables
C = 1 + F(1, 4) * beta
d = 1 + beta * m
det_numerator = C * (C - 1) * d**2 - (C - 1) - C * beta**2 * (s - m**2)
certificate = beta**2 * ((C * m - F(1, 4))**2 + C * (m - s))
ck('universal_polynomial', not (det_numerator - certificate).terms)
parameter_polynomial = 7 * (2 - a)**3 - 5 * (2 + a) * (4 - 13 * a**2)
positive_form = 172 * (a - F(13, 43))**2 + F(12, 43) + 58 * a**3
ck('universal_polynomial', not (parameter_polynomial - positive_form).terms)
ck('universal_polynomial', F(7, 10) < F(21, 25)**2 < F(24, 25)**2)
ck('universal_polynomial', 16 * F(21, 25) / (1 - F(21, 25)) == 84)
ck('universal_polynomial', 3 + F(25, 24) * 84 == F(181, 2))
ck('universal_polynomial', 1 + F(25, 96) * 84 == F(183, 8))
ck('universal_polynomial', F(181, 2) + F(35, 24) * 84 == 213)

# Exact feasible moment-pair controls and sharpness. These corroborate the
# polynomial proof; they are not an exhaustive empirical proof of it.
for be in (F(0), F(1, 100), F(1, 4), F(1), F(4), F(25)):
    c = 1 + be / 4
    for mu, mix in itertools.product((F(j, 20) for j in range(21)), repeat=2):
        second = (1 - mix) * mu**2 + mix * mu
        den = 1 + be * mu
        numerator = c * (c - 1) * den**2 - (c - 1) - c * be**2 * (second - mu**2)
        ck('feasible_moment', numerator == be**2 * ((c * mu - F(1, 4))**2 + c * (mu - second)))
        ck('feasible_moment', numerator >= 0 and c >= 1 and mu**2 <= second <= mu)
    mu = 1 / (be + 4)
    second = mu
    ck('sharp_rank_one', (c * mu - F(1, 4))**2 + c * (mu - second) == 0)
ck('scope_countercontrol', F(1, 4) * (1 + F(100, 16)) == F(29, 16) > 1)

# Independent exact inverse/Mobius identity without a symbolic package.
def inv(z, r):
    return (2*z-r-1)/(r+4-2*r*z)
def forward(x, r):
    return ((r+4)*x+r+1)/(2*r*x+2)
for r in (F(j, 25) for j in range(-10, 11)):
    for x in (F(j, 24) for j in range(-12, 13)):
        ck('inverse_rectangle', inv(forward(x, r), r) == x)
        derivative = (4-r*r)/(2*(1+r*x)**2)
        ck('inverse_rectangle', 0 < 1/derivative <= F(3, 4))
        ck('inverse_rectangle', 0 <= (1-4*x*x)/(4-r*r) <= F(25, 96))

# Full interval pushforward masses for flat and nonflat cumulative maps.
# On a source cell with density h, CDF image length is h/cell_count.
# Intersect each image with a target interval, pull it back, and compute its
# source mass; zero cells contribute zero, with no division by zero.
cumulative_cases = 0
for raw in itertools.product((0, 1, 4), repeat=4):
    total = sum(raw)
    if not total:
        continue
    heights = [F(4*v, total) for v in raw]
    ends = [F(0)]
    for h in heights:
        ends.append(ends[-1] + h/4)
    for left, right in itertools.combinations((F(j, 17) for j in range(18)), 2):
        mass = F(0)
        for i, h in enumerate(heights):
            length = max(F(0), min(right, ends[i+1]) - max(left, ends[i]))
            mass += h * (length/h) if h else F(0)
        ck('cdf_interval_mass', mass == right-left)
    cumulative_cases += 1

# Scalar nonlinear inverse on unequal, correlated samples. Randomness is
# deterministic. This float experiment is labeled numerical corroboration.
rng = random.Random(35930001370)
def solve_v(z, weights, amp, slope):
    lo, hi = -amp, amp
    for _ in range(90):
        r = (lo+hi)/2
        field = sum(w*inv(v, r) for w, v in zip(weights, z))
        residual = r - amp*tanh(slope*field/amp)
        if residual > 0:
            hi = r
        else:
            lo = r
    r = (lo+hi)/2
    values = [inv(v, r) for v in z]
    field = sum(w*v for w, v in zip(weights, values))
    return values, r, r - amp*tanh(slope*field/amp)

worst_ratio_squared = 0.0
max_residual = 0.0
numerical_cases = 0
for amp, slope in itertools.product((0.4, 0.001, 1e-9), (6.000001, 16.0)):
    for trial in range(120):
        labels = [i % 2 for i in range(31)]
        weights = [rng.random()+0.01 for _ in labels]
        norm = sum(weights)
        weights = [w/norm for w in weights]
        # Labels are deterministic and heavily correlated with the next
        # variable in every third case, rather than independent.
        z = [rng.uniform(-0.5, 0.5) + label for label in labels]
        zp = [(-0.49 if label else 0.49) + label if trial % 3 == 0
              else rng.uniform(-0.5, 0.5) + label for label in labels]
        x, r, residual = solve_v(z, weights, amp, slope)
        xp, rp, residualp = solve_v(zp, weights, amp, slope)
        denominator = sum(w*(v-vp)**2 for w,v,vp in zip(weights,z,zp))
        ratio = sum(w*(v-vp)**2 for w,v,vp in zip(weights,x,xp))/denominator
        worst_ratio_squared = max(worst_ratio_squared, ratio)
        max_residual = max(max_residual, abs(residual), abs(residualp))
        ck('numerical_feedback', max(abs(residual), abs(residualp)) < 1e-12)
        ck('numerical_feedback', ratio <= 0.7 + 1e-12)
        ck('numerical_feedback', all(-0.5-1e-14 <= v <= 0.5+1e-14 for v in x+xp))
        numerical_cases += 1

# Independent zero-mass/zero-field polynomial counterexample to invariance
# of the source proof's proposed ker(phi), using only rational integration.
def integrate(poly):
    return sum(c * ((F(1,2)**(i+1))-((-F(1,2))**(i+1))) / (i+1)
               for i,c in enumerate(poly))
def double(poly):
    out = [F(0)] * len(poly)
    for i,c in enumerate(poly):
        for j in range(i+1):
            out[j] += c * comb(i,j) * F(1,2)**j * ((-F(1,4))**(i-j) + F(1,4)**(i-j))/2
    return out
poly = [F(0), -F(3,20), F(0), F(1)]
ck('linear_counterexample', integrate(poly) == integrate([F(0)]+poly) == 0)
ck('linear_counterexample', integrate([F(0)]+double(poly)) == F(1,320))

print(json.dumps({
    'status': 'PASS',
    'categories': counts,
    'exact_assertions': sum(v for k,v in counts.items() if k != 'numerical_feedback'),
    'numerical_assertions': counts['numerical_feedback'],
    'universal_inverse_norm_squared_bound': '7/10',
    'chosen_rational_contraction': '21/25',
    'parameter_sum_coefficient': '84',
    'log_distortion_coefficient': '213',
    'cumulative_density_cases': cumulative_cases,
    'numerical_cases': numerical_cases,
    'maximum_numerical_ratio_squared': worst_ratio_squared,
    'maximum_numerical_feedback_residual': max_residual,
    'scope': 'Exact polynomial and finite controls plus labeled numerical corroboration; all-density/topological conclusions require the analytic report.'
}, indent=2, sort_keys=True))
