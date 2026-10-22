#!/usr/bin/env python3
"""Independent finite controls: shifted-simplex probabilities and KdV recursion.

No archived mathematical checker is used as this program's oracle.  A frozen
DVV function is loaded only at the final comparison step.  Exact rational
arithmetic is used throughout.  These controls do not establish asymptotics,
the geometric correspondence, novelty, or publication clearance.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product
from collections import Counter
from math import comb, factorial, prod
from pathlib import Path
import ast
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parent
COUNTS = Counter()


def check(ok, family):
    if not ok:
        raise AssertionError(family)
    COUNTS[family] += 1


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for j in range(minimum, total + 1):
        for tail in partitions(total - j, j):
            yield (j,) + tail


# Derive the common-pi-stripped weights without Bernoulli numbers: if
# S(z)=sin(sqrt(z))/sqrt(z), then log H(z)=-log S(z)/2.
# The coefficient identity S'(z)=-2 (log H)'(z) S(z) fixes a_j.
MAX_N = 8
sine = [Q((-1)**j, factorial(2*j + 1)) for j in range(MAX_N + 1)]
weights = [Q(0)]
for n in range(1, MAX_N + 1):
    weights.append((-n*sine[n] - 2*sum(j*weights[j]*sine[n-j]
                                     for j in range(1, n))) / (2*n))
check(weights[1:4] == [Q(1, 12), Q(1, 360), Q(1, 5670)],
      'three_reference_zeta_weights')
h = [Q(1)]
for n in range(1, MAX_N + 1):
    h.append(sum(j*weights[j]*h[n-j] for j in range(1, n+1))/n)


@lru_cache(None)
def lower_orthant(total, shapes, thresholds):
    """P(X_i >= thresholds_i) in an integer-shape Dirichlet law.

    Translate the selected coordinates by their lower bounds and integrate
    each term in the translated simplex.  This formula also handles selection
    of every coordinate (zero residual shape), including one-cylinder atoms.
    It is distinct from the archived rectangle-polynomial integration.
    """
    residue = 1 - sum(thresholds)
    if residue < 0:
        return Q(0)
    value = Q(0)
    for degrees in product(*(range(a) for a in shapes)):
        exponent = total - 1 - sum(degrees)
        coefficient = Q(factorial(total-1), factorial(exponent))
        for threshold, degree in zip(thresholds, degrees):
            coefficient *= threshold**degree / factorial(degree)
        value += coefficient * residue**exponent
    return value


@lru_cache(None)
def rectangle(total, shapes, windows):
    # Inclusion-exclusion of upper-bound failures gives arbitrary rectangles,
    # including those cut by the sum-to-one boundary.  All selected coordinate
    # distributions are continuous except the single-coordinate total atom.
    if len(shapes) == 1 and shapes[0] == total:
        return Q(int(windows[0][0] <= 1 <= windows[0][1]))
    value = Q(0)
    for high in product((0, 1), repeat=len(shapes)):
        thresholds = tuple(w[b] for w, b in zip(windows, high))
        value += (-1)**sum(high) * lower_orthant(total, shapes, thresholds)
    check(0 <= value <= 1, 'shifted_simplex_rectangle_probability_bounds')
    return value


def beta_window(shape, total, lo, hi):
    if shape == total:
        return Q(int(lo <= 1 <= hi))
    def cdf(x):
        return sum(Q(comb(total-1, j))*x**j*(1-x)**(total-1-j)
                   for j in range(shape, total))
    return cdf(hi) - cdf(lo)


# Check every rational-grid marginal against an independent order-statistics
# binomial formula, including windows through the one-cylinder atom.
for total in range(2, 18, 2):
    for shape in range(2, total+1, 2):
        for lo, hi in ((Q(0), Q(1)), (Q(1,4), Q(1,2)),
                       (Q(1,6), Q(2,3)), (Q(1,2), Q(1))):
            check(rectangle(total, (shape,), ((lo, hi),)) ==
                  beta_window(shape, total, lo, hi),
                  'simplex_vs_uniform_order_statistics_marginal')

# Independent exact boundary checks on Dirichlet(2,2): X_2=1-X_1.
check(rectangle(4, (2,2), ((Q(1,4),Q(1,2)),)*2) == 0,
      'singular_sum_one_pair_empty_interior')
check(rectangle(4, (2,2), ((Q(1,4),Q(3,4)),)*2) == Q(11,16),
      'singular_sum_one_pair_reference')
check(rectangle(4, (2,2), ((Q(0),Q(1)),)*2) == 1,
      'all_selected_coordinates_normalization')


area_rows = []
for n in range(1, MAX_N + 1):
    rows = []
    for part in partitions(n):
        counts = Counter(part)
        mass = prod(weights[j]**m / factorial(m) for j,m in counts.items())/h[n]
        rows.append((part, mass))
    check(sum(m for _,m in rows) == 1, 'direct_assembly_probability_normalization')
    for window in ((Q(1,4), Q(1,2)), (Q(1,6), Q(2,3))):
        # Compute every factorial moment by literal subset selection within each
        # finite composition; then reconstruct the entire count distribution.
        factorial_moments = [Q(1)] + [Q(0)]*n
        for part, mass in rows:
            for r in range(1, len(part)+1):
                total_probability = Q(0)
                for selected in combinations(range(len(part)), r):
                    shapes = tuple(sorted(2*part[i] for i in selected))
                    total_probability += rectangle(2*n, shapes, (window,)*r)
                factorial_moments[r] += mass*factorial(r)*total_probability
        count_probabilities = [sum((-1)**(r-k)*factorial_moments[r] /
                                   (factorial(k)*factorial(r-k))
                                   for r in range(k, n+1)) for k in range(n+1)]
        check(sum(count_probabilities) == 1,
              'entire_normalized_count_distribution_mass')
        check(all(p >= 0 for p in count_probabilities),
              'entire_normalized_count_distribution_positivity')
        # A separately formed selected-assembly formula, through order three.
        for r in range(1, min(n,3)+1):
            selected = Q(0)
            for js in product(range(1,n+1), repeat=r):
                removed = sum(js)
                if removed <= n:
                    selected += prod(weights[j] for j in js)*h[n-removed]/h[n] * \
                        rectangle(2*n, tuple(sorted(2*j for j in js)), (window,)*r)
            check(selected == factorial_moments[r],
                  'normalized_joint_selector_identity_orders_1_to_3')
        # Reconstruct the mean and variance from the whole distribution.
        mean = sum(k*p for k,p in enumerate(count_probabilities))
        second = sum(k*k*p for k,p in enumerate(count_probabilities))
        check(mean == factorial_moments[1], 'count_mean_from_entire_distribution')
        check(second == factorial_moments[1] +
              (factorial_moments[2] if n>=2 else 0),
              'count_second_moment_from_entire_distribution')
        area_rows.append({'n':n,'window':[str(x) for x in window],
                          'probabilities':[str(x) for x in count_probabilities],
                          'mean':str(mean),'variance':str(second-mean**2)})


# An independent intersection-number evaluator from the first KdV equation
# plus string and the genus-zero simplex formula.  In the equation below d has
# n entries and dimension is enforced by I:
# (2g+n-1)<tau_0 prod tau_d>_g =
#  (1/12)<tau_0^4 prod tau_d>_(g-1) +
#  (1/2)sum_(h,S)<tau_0^2 prod_(S)tau_d>_h
#                      <tau_0^2 prod_(S^c)tau_d>_(g-h).
# To solve for I(g,ds), increase its largest degree by one and apply string.
# The correction terms have a strictly larger largest degree, and terminate
# at a zero degree (string) or the one-point case.  No DVV factors appear.
def intersection_kdv(g, degrees):
    return _intersection_kdv(g, tuple(sorted(degrees)))


@lru_cache(None)
def _intersection_kdv(g, ds):
    n = len(ds)
    if g < 0 or 2*g-2+n <= 0 or any(d<0 for d in ds) or sum(ds) != 3*g-3+n:
        return Q(0)
    if g == 0:
        return Q(factorial(n-3), prod(factorial(d) for d in ds))
    if ds[0] == 0:
        tail = ds[1:]
        return sum(intersection_kdv(g, tail[:i]+(d-1,)+tail[i+1:])
                   for i,d in enumerate(tail) if d)
    boosted = ds[:-1] + (ds[-1]+1,)
    rhs = intersection_kdv(g-1, (0,0,0,0)+boosted)/12
    for mask in range(1<<n):
        left = tuple(d for i,d in enumerate(boosted) if mask>>i&1)
        right = tuple(d for i,d in enumerate(boosted) if not mask>>i&1)
        for genus in range(g+1):
            rhs += intersection_kdv(genus,(0,0)+left) * \
                   intersection_kdv(g-genus,(0,0)+right)/2
    correction = sum(intersection_kdv(g, ds[:i]+(d-1,)+ds[i+1:-1]+(ds[-1]+1,))
                     for i,d in enumerate(ds[:-1]))
    return rhs/(2*g+n-1) - correction


# Load only the published function definitions/imports, excluding its top-level
# assertions, loops, output writes and claims.  This is a comparator, not an
# input to the KdV evaluator above.
dvv_source = ROOT/'exact_public_zip_01/verification/controls/dvv_geometry.py'
tree = ast.parse(dvv_source.read_text())
definitions = ast.Module(body=[node for node in tree.body if isinstance(
    node, (ast.Import, ast.ImportFrom, ast.FunctionDef))], type_ignores=[])
oracle = {}
exec(compile(definitions, str(dvv_source), 'exec'), oracle)
intersection_dvv = oracle['intersection']


def weak_partitions(total, slots, minimum=0):
    if slots == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, total//slots+1):
        for tail in weak_partitions(total-first,slots-1,first):
            yield (first,)+tail


intersection_rows = []
for g, maximum_marks in ((0,10),(1,8),(2,6),(3,4),(4,3)):
    local = 0
    for marks in range(1, maximum_marks+1):
        if 2*g-2+marks <= 0:
            continue
        for ds in weak_partitions(3*g-3+marks,marks):
            independent = intersection_kdv(g,ds)
            published = intersection_dvv(g,ds)
            check(independent == published, 'independent_KdV_vs_published_DVV')
            check(independent > 0, 'independent_KdV_positive_stable_intersection')
            local += 1
    intersection_rows.append({'g':g,'maximum_marks':maximum_marks,'degree_multisets':local})
for g in range(1,11):
    check(intersection_kdv(g,(3*g-2,)) == Q(1,24**g*factorial(g)),
          'KdV_vs_one_point_closed_form')

receipt = {'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'exact_assertions':sum(COUNTS.values()),'families':dict(sorted(COUNTS.items())),
           'normalized_count_distributions':area_rows,
           'intersection_ranges':intersection_rows,
           'KdV_cache':_intersection_kdv.cache_info()._asdict(),
           'published_DVV_sha256':hashlib.sha256(dvv_source.read_bytes()).hexdigest(),
           'independent_program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'limits':'Finite exact controls only; no proof of the geometric correspondence, uniform high-genus input, asymptotics, novelty, or case completion.'}
(ROOT/'INDEPENDENT_CONTROLS_RECEIPT_01.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
