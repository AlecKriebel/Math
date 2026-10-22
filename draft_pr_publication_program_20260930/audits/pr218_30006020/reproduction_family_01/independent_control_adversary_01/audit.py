#!/usr/bin/env python3
"""Independent exact audit; writes only beside this file. No network or git."""
import ast
import contextlib
import datetime
import hashlib
import io
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
SUBJECT = PARENT / 'independent_controls_01.py'
RECEIPT = PARENT / 'INDEPENDENT_CONTROLS_RECEIPT_01.json'
TARGETS = [SUBJECT, RECEIPT,
           PARENT/'exact_public_zip_01/verification/controls/dvv_geometry.py']
before_pins = {str(p.relative_to(PARENT)): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in TARGETS}
source = SUBJECT.read_text()
tree = ast.parse(source)

# Load the subject functions, without the main checker or final write.
functions = ast.Module(body=[n for n in tree.body if isinstance(
    n, (ast.Import, ast.ImportFrom, ast.FunctionDef))], type_ignores=[])
subject = {'__file__': str(SUBJECT), 'COUNTS': Counter()}
exec(compile(functions, str(SUBJECT), 'exec'), subject)


def interval_terms(shape, lo, hi, count_degree):
    """Truncated-power representation of x^(a-1)/(a-1)! on [lo,hi].

    B_j(x-t)=(x-t)_+^j/j!, with coefficient of y^count_degree.
    The identity follows by expanding x=(x-t)+t at each endpoint.
    """
    terms = defaultdict(F)
    m = shape-1
    for knot, sign in ((lo, 1), (hi, -1)):
        for j in range(m+1):
            terms[(knot, j, count_degree)] += sign*knot**(m-j)/factorial(m-j)
    return {k: v for k, v in terms.items() if v}


def convolve(left, right):
    # Direct beta integral: B_j * B_k = B_(j+k+1).
    out = defaultdict(F)
    for (s, j, a), c in left.items():
        for (t, k, b), d in right.items():
            if s+t <= 1:
                out[(s+t, j+k+1, a+b)] += c*d
    return {k: v for k, v in out.items() if v}


def at_one(terms, total):
    result = defaultdict(F)
    for (knot, degree, count_degree), coefficient in terms.items():
        result[count_degree] += (factorial(total-1)*coefficient*
                                 (1-knot)**degree/factorial(degree))
    return dict(result)


@lru_cache(None)
def direct_rectangle(total, shapes, windows):
    """Direct density convolution, without event-level orthant inversion."""
    residual = total-sum(shapes)
    actual_shapes = shapes + ((residual,) if residual else ())
    actual_windows = windows + (((F(0), F(1)),) if residual else ())
    if len(actual_shapes) == 1:
        return F(all(lo <= 1 <= hi for lo, hi in actual_windows))
    factors = [interval_terms(a, lo, hi, 0)
               for a, (lo, hi) in zip(actual_shapes, actual_windows)]
    result = factors[0]
    for factor in factors[1:]:
        result = convolve(result, factor)
    return at_one(result, total).get(0, F(0))


@lru_cache(None)
def direct_count_pgf(shapes, window):
    """Integrate y^number_inside directly, without moments or inversion."""
    lo, hi = window
    if len(shapes) == 1:
        return (F(0), F(1)) if lo <= 1 <= hi else (F(1), F(0))
    factors = []
    for a in shapes:
        terms = defaultdict(F)
        # The three disjoint interval interiors partition the support.
        for lower, upper, degree in ((F(0), lo, 0), (lo, hi, 1), (hi, F(1), 0)):
            for key, value in interval_terms(a, lower, upper, degree).items():
                terms[key] += value
        factors.append({k: v for k, v in terms.items() if v})
    result = factors[0]
    for factor in factors[1:]:
        result = convolve(result, factor)
    values = at_one(result, sum(shapes))
    return tuple(values.get(k, F(0)) for k in range(len(shapes)+1))


checks = Counter()
examples = []


def equal(left, right, family, data=None):
    if left != right:
        raise AssertionError((family, left, right, data))
    checks[family] += 1


# Independent convolution reference anchors, including arbitrary odd shapes.
equal(direct_rectangle(2, (1, 1), ((F(1,4), F(3,4)),)*2), F(1,2),
      'direct_oracle_uniform_anchor')
equal(direct_rectangle(4, (2, 2), ((F(1,4), F(3,4)),)*2), F(11,16),
      'direct_oracle_beta_anchor')

grid = (F(0), F(1,4), F(1,3), F(1,2), F(2,3), F(3,4), F(1))
window_bank = ((F(0), F(1)), (F(0), F(0)), (F(1), F(1)),
               (F(0), F(1,3)), (F(1,3), F(2,3)), (F(2,3), F(1)),
               (F(1,3), F(1,3)), (F(1,2), F(1)))
shape_rows = []
for total in range(1, 9):
    for marks in range(1, min(total, 3)+1):
        for shapes in combinations_with_replacement(range(1, total+1), marks):
            if sum(shapes) > total:
                continue
            shape_rows.append((total, shapes))
            windows_to_check = [(w,)*marks for w in window_bank]
            windows_to_check.extend(tuple(window_bank[(j+3*i) % len(window_bank)]
                                         for i in range(marks)) for j in range(8))
            for windows in windows_to_check:
                expected = direct_rectangle(total, shapes, windows)
                actual = subject['rectangle'](total, shapes, windows)
                equal(actual, expected, 'rectangle_vs_direct_density_convolution',
                      [total, shapes, windows])
            for offset in range(len(grid)):
                thresholds = tuple(grid[(offset+2*i) % len(grid)] for i in range(marks))
                expected = direct_rectangle(total, shapes,
                                            tuple((t, F(1)) for t in thresholds))
                actual = subject['lower_orthant'](total, shapes, thresholds)
                equal(actual, expected, 'survival_vs_direct_density_convolution',
                      [total, shapes, thresholds])

# Re-execute the submitted main program without its one output write.  The
# original __file__ is retained solely for its frozen comparator read and pins.
replay_tree = ast.parse(source)
removed = [n for n in replay_tree.body if isinstance(n, ast.Expr)
           and isinstance(n.value, ast.Call)
           and isinstance(n.value.func, ast.Attribute)
           and n.value.func.attr == 'write_text']
assert len(removed) == 1
replay_tree.body = [n for n in replay_tree.body if n not in removed]
replay = {'__file__': str(SUBJECT)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(replay_tree, str(SUBJECT), 'exec'), replay)
submitted = json.loads(RECEIPT.read_text())
reproduced = replay['receipt']
for key in submitted:
    if key != 'utc':
        equal(reproduced[key], submitted[key], 'receipt_exact_replay_except_timestamp', key)
(HERE/'REPRODUCED_RECEIPT.json').write_text(json.dumps(reproduced, indent=2)+'\n')

# Direct count laws for every submitted assembly n and window.  The assembly
# weights are the explicitly declared input model, not a geometric assertion.
count_rows = []
for row in submitted['normalized_count_distributions']:
    n = row['n']
    window = tuple(F(x) for x in row['window'])
    result = [F(0)]*(n+1)
    for part in subject['partitions'](n):
        multiplicities = Counter(part)
        mass = F(1)
        for j, m in multiplicities.items():
            mass *= replay['weights'][j]**m/factorial(m)
        mass /= replay['h'][n]
        conditional = direct_count_pgf(tuple(2*j for j in part), window)
        equal(sum(conditional), F(1), 'direct_count_conditional_mass')
        equal(all(p >= 0 for p in conditional), True, 'direct_count_conditional_positivity')
        for k, p in enumerate(conditional):
            result[k] += mass*p
    equal(result, list(map(F, row['probabilities'])),
          'submitted_entire_count_law_vs_direct_pgf', [n, window])
    count_rows.append({'n': n, 'window': list(map(str, window)),
                       'probabilities': list(map(str, result))})

# Independently exercise first-KdV recursion with a well-founded rank on every
# nonzero-domain call, including calls served from cache.
rank_edges = Counter()
active = []
raw_kdv = subject['_intersection_kdv'].__wrapped__
memo_kdv = lru_cache(None)(raw_kdv)


def valid_state(g, ds):
    return (g >= 0 and 2*g-2+len(ds) > 0 and all(d >= 0 for d in ds)
            and sum(ds) == 3*g-3+len(ds))


def rank(g, ds):
    return (g, len(ds), sum(ds)-max(ds))


def traced_kdv(g, ds):
    valid = valid_state(g, ds)
    if active and valid:
        parent_g, parent_ds = active[-1]
        if valid_state(parent_g, parent_ds):
            assert rank(g, ds) < rank(parent_g, parent_ds), (g, ds, active[-1])
            family = ('genus' if g < parent_g else
                      'marks' if len(ds) < len(parent_ds) else 'largest_degree')
            rank_edges[family] += 1
    assert (g, ds) not in active, ('cycle', active, g, ds)
    active.append((g, ds))
    try:
        return memo_kdv(g, ds)
    finally:
        active.pop()


subject['_intersection_kdv'] = traced_kdv
intersection = subject['intersection_kdv']
for g, marks_max in ((0, 10), (1, 9), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3)):
    for marks in range(1, marks_max+1):
        if 2*g-2+marks <= 0:
            continue
        for ds in subject['weak_partitions'](3*g-3+marks, marks):
            actual = intersection(g, ds)
            equal(actual > 0, True, 'extended_kdv_positive_stable_values')
            # Dilaton is absent from the submitted KdV evaluator.
            equal(intersection(g, (1,)+ds), (2*g-2+marks)*actual,
                  'independent_dilaton_consistency')
for g in range(1, 13):
    equal(intersection(g, (3*g-2,)), F(1, 24**g*factorial(g)),
          'extended_one_point_formula')

# Explicit unsupported-input counterexample.  This is outside all submitted
# tests, but prevents calling the helper an unrestricted-threshold API.
negative = subject['lower_orthant'](3, (2,), (F(-1,2),))
equal(negative, F(3,4), 'negative_threshold_counterexample_reproduced')
examples.append({'function': 'lower_orthant', 'arguments': ['3', '(2,)', '(-1/2,)'],
                 'returned': str(negative), 'actual_probability': '1',
                 'interpretation': 'Missing input-domain validation; negative thresholds unsupported.'})

after_pins = {str(p.relative_to(PARENT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in TARGETS}
equal(after_pins, before_pins, 'audited_inputs_unchanged')
report = {
    'status': 'PASS_ON_DECLARED_DOMAIN_WITH_SCOPE_LIMITS',
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'subject_pins': before_pins,
    'checks': dict(sorted(checks.items())),
    'shape_parameter_families': len(shape_rows),
    'maximum_total_shape': 8,
    'maximum_selected_components': 3,
    'direct_count_distributions': count_rows,
    'kdv_valid_recursive_edge_rank_checks': dict(sorted(rank_edges.items())),
    'kdv_states': memo_kdv.cache_info()._asdict(),
    'domain_counterexamples': examples,
    'limits': 'Finite exact verification under stated Dirichlet/assembly/KdV identities. No geometric correspondence, high-genus estimate, asymptotics, novelty, or case completion certified.'
}
(HERE/'AUDIT_RECEIPT.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k: report[k] for k in ('status', 'checks', 'shape_parameter_families',
                                         'kdv_valid_recursive_edge_rank_checks', 'kdv_states')}, indent=2))
