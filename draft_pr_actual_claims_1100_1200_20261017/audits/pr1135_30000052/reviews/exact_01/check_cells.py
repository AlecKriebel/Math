#!/usr/bin/env python3
"""Independent exact vertical-cell integration; standard library only.

No candidate or other review code is imported. Every mathematical expectation
is calculated from the defining integral, not from the advertised fractions.
"""
from fractions import Fraction as Q
from math import comb, factorial
import hashlib
import json
from pathlib import Path
import sys

CHECKS = 0


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    return trim(tuple((p[i] if i < len(p) else Q(0)) +
                      (q[i] if i < len(q) else Q(0))
                      for i in range(max(len(p), len(q)))))


def scale(p, a):
    return trim(tuple(a * b for b in p))


def mul(p, q):
    r = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i+j] += a*b
    return trim(r)


def power(p, m):
    r = (Q(1),)
    for _ in range(m):
        r = mul(r, p)
    return r


def integral(p, left, right):
    return sum((a * (right**(i+1) - left**(i+1)) / (i+1)
                for i, a in enumerate(p)), Q(0))


def evaluate(p, x):
    return sum((a*x**i for i, a in enumerate(p)), Q(0))


def affine(line, z):
    a, b = line
    return a*z+b


def cell_integral(form, degree, left, right, lower, upper):
    """Integrate (a*z+b*delta+c)^degree over the full vertical strip.

    All integrations use elementary antiderivatives; there is no interpolation,
    quadrature, clipping, fitted degree, or numerical approximation.
    """
    a, b, c = form
    if b:
        u = (b*upper[1]+c, a+b*upper[0])
        l = (b*lower[1]+c, a+b*lower[0])
        poly = scale(add(power(u, degree+1), scale(power(l, degree+1), -1)),
                     Q(1, degree+1)/b)
    else:
        width = (upper[1]-lower[1], upper[0]-lower[0])
        poly = mul(power((c, a), degree), width)
    return integral(poly, left, right)


def cuts(n):
    require(isinstance(n, int) and not isinstance(n, bool) and n >= 1,
            'positive integer point count required')
    return sorted({Q(0), Q(1)} |
                  {Q(k, m) for m in range(1, n) for k in range(1, m)})


def floor(x):
    return x.numerator // x.denominator


def make_cells(n, generator_cuts=None):
    grid = cuts(n) if generator_cuts is None else generator_cuts
    require(grid[0] == 0 and grid[-1] == 1 and
            all(a < b for a, b in zip(grid, grid[1:])), 'invalid generator cuts')
    cells = []
    for left, right in zip(grid, grid[1:]):
        mid = (left+right)/2
        # For j>=1, ceil(j*z)-j*z is the only interior wrap threshold.
        boundaries = [(Q(0), Q(0)), (Q(0), Q(1))]
        boundaries += [(Q(-j), Q(floor(j*mid)+1)) for j in range(1, n)]
        boundaries.sort(key=lambda line: affine(line, mid))
        require(len(set(affine(line, mid) for line in boundaries)) == n+1,
                'coincident interior wrap lines: a generator cut is missing')
        for lower, upper in zip(boundaries, boundaries[1:]):
            require(affine(lower, left) <= affine(upper, left) and
                    affine(lower, right) <= affine(upper, right),
                    'wrap lines cross inside a generator interval')
            delta = (affine(lower, mid)+affine(upper, mid))/2
            floors = tuple(floor(j*mid+delta) for j in range(n))
            order = tuple(sorted(range(n), key=lambda j: j*mid+delta-floors[j]))
            cell = {'left': left, 'right': right, 'lower': lower,
                    'upper': upper, 'floors': floors, 'order': order}
            validate_cell(n, cell)
            cells.append(cell)
    require(sum((cell_integral((Q(0), Q(0), Q(1)), 0,
                              c['left'], c['right'], c['lower'], c['upper'])
                 for c in cells), Q(0)) == 1, 'partition area is not one')
    return cells


def validate_cell(n, cell):
    require(sorted(cell['order']) == list(range(n)), 'invalid permutation')
    for z in (cell['left'], cell['right']):
        for d in (affine(cell['lower'], z), affine(cell['upper'], z)):
            values = tuple(j*z+d-cell['floors'][j] for j in range(n))
            require(all(0 <= t <= 1 for t in values), 'invalid modular floor on cell')
            sorted_values = [values[j] for j in cell['order']]
            require(all(a <= b for a, b in zip(sorted_values, sorted_values[1:])),
                    'point order changes inside the cell')


def moment(n, p, cells=None, count_denominator=None):
    require(isinstance(p, int) and not isinstance(p, bool) and p >= 2 and p % 2 == 0,
            'this polynomial integral requires a positive even exponent')
    cells = make_cells(n) if cells is None else cells
    norm = n if count_denominator is None else count_denominator
    total = Q(0)
    records = []
    for cell in cells:
        # Each form is a*z+b*delta+c; include the fixed endpoints 0 and 1.
        forms = [(Q(0), Q(0), Q(0))]
        forms += [(Q(j), Q(1), Q(-cell['floors'][j])) for j in cell['order']]
        forms += [(Q(0), Q(0), Q(1))]
        value = Q(0)
        for k in range(n+1):
            low, high = forms[k], forms[k+1]
            low = (low[0], low[1], low[2]-Q(k, norm))
            high = (high[0], high[1], high[2]-Q(k, norm))
            value += (cell_integral(high, p+1, cell['left'], cell['right'],
                                    cell['lower'], cell['upper']) -
                      cell_integral(low, p+1, cell['left'], cell['right'],
                                    cell['lower'], cell['upper'])) / (p+1)
        require(value >= 0, 'negative even discrepancy integral')
        total += value
        records.append({**cell, 'area': cell_integral((Q(0), Q(0), Q(1)), 0,
                         cell['left'], cell['right'], cell['lower'], cell['upper']),
                        'integral': value})
    return total, records


def iid_moment(n, p):
    # Directly integrate the entire binomial law. Beta integral arguments are
    # nonnegative integers and are evaluated as exact factorial quotients.
    value = Q(0)
    for k in range(n+1):
        for a in range(p+1):
            coefficient = comb(n, k)*comb(p, a)*Q(k, n)**(p-a)*(-1)**a
            value += coefficient*Q(factorial(k+a)*factorial(n-k),
                                   factorial(n+a+1))
    return value


def fixed_points_moment(points, p):
    require(p % 2 == 0, 'even p required')
    points = sorted(points)
    n = len(points)
    full = [Q(0)] + points + [Q(1)]
    return sum((((full[k+1]-Q(k, n))**(p+1) -
                 (full[k]-Q(k, n))**(p+1))/(p+1)
                for k in range(n+1)), Q(0))


def partition_witnesses(n, cells):
    tested = 0
    for den in (11, 13, 17):
        for iz in range(1, den):
            z = Q(iz, den)
            for idelta in range(1, den):
                delta = Q(idelta, den)
                if any((j*z+delta).denominator == 1 for j in range(n)):
                    continue
                hits = [c for c in cells if c['left'] < z < c['right'] and
                        affine(c['lower'], z) < delta < affine(c['upper'], z)]
                require(len(hits) == 1, 'interior witness has nonunique cell')
                c = hits[0]
                actual_floors = tuple(floor(j*z+delta) for j in range(n))
                require(actual_floors == c['floors'], 'witness floor mismatch')
                actual_order = tuple(sorted(range(n), key=lambda j:
                                     j*z+delta-actual_floors[j]))
                require(actual_order == c['order'], 'witness order mismatch')
                tested += 1
    return tested


def adverse_checks():
    caught = []
    def reject(name, callback):
        try:
            callback()
        except (ValueError, ZeroDivisionError, TypeError):
            caught.append(name)
            return
        raise ValueError('adverse case was not rejected: '+name)
    reject('zero_point_count', lambda: cuts(0))
    reject('odd_power_without_absolute_value', lambda: moment(3, 3))
    reject('missing_generator_cut', lambda: make_cells(3, [Q(0), Q(1)]))
    good = make_cells(3)
    bad_floor = dict(good[0], floors=tuple(t+1 for t in good[0]['floors']))
    reject('corrupted_modular_floor', lambda: validate_cell(3, bad_floor))
    bad_order = dict(good[0], order=tuple(reversed(good[0]['order'])))
    reject('reversed_interior_order', lambda: validate_cell(3, bad_order))
    bad_perm = dict(good[0], order=(0, 0, 2))
    reject('duplicated_point_index', lambda: validate_cell(3, bad_perm))
    correct, records = moment(3, 4, good)
    truncated = sum((r['integral'] for r in records[:-1]), Q(0))
    require(truncated != correct, 'missing positive cell not detected')
    caught.append('deleted_positive_cell_detected')
    unnormalized, _ = moment(3, 4, good, count_denominator=1)
    require(unnormalized != correct, 'normalization mutation not detected')
    caught.append('removed_count_normalization_detected')
    require(correct != iid_moment(3, 4), 'triple iid substitution not detected')
    caught.append('pairwise_to_joint_independence_substitution_detected')
    constant_generator = Q(1, 15)  # Derived also by n=1 uniform shift, below.
    require(constant_generator != correct, 'fixed zero generator confusion')
    caught.append('zero_generator_replaces_generator_average_detected')
    require(Q(2, 105*2) < iid_moment(3, 4), 'n=3 tail lower bound misused')
    caught.append('n3_empty_tail_bound_insufficient_detected')
    one, _ = moment(1, 4)
    require(one == constant_generator, 'zero generator/uniform point control')
    return caught


def run():
    root = Path(__file__).resolve().parents[2]/'inputs'
    pins = {p.name: {'bytes': len(p.read_bytes()),
                    'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(root.iterdir()) if p.is_file()}
    expected_pins = json.loads((Path(__file__).parent/'INPUT_PINS.json').read_text())
    require(pins == expected_pins, 'frozen input inventory or digest mismatch')
    values = []
    all_records = {}
    for n in range(1, 8):
        cells = make_cells(n)
        witnesses = partition_witnesses(n, cells)
        for p in (2, 4, 6, 8):
            lattice, records = moment(n, p, cells)
            iid = iid_moment(n, p)
            if p == 2:
                require(lattice == Q(1, 6*n) == iid, 'second moment control')
            if n <= 2:
                require(lattice == iid, 'one/two-point complete-law control')
            if p == 4:
                require(iid == Q(3*n-1, 30*n**3), 'iid fourth moment formula')
            values.append({'n': n, 'p': p, 'cells': len(cells),
                           'witnesses': witnesses, 'lattice': lattice, 'iid': iid,
                           'difference': lattice-iid})
            if n in (3, 4) and p == 4:
                all_records[str(n)] = records
    main = next(r for r in values if r['n'] == 3 and r['p'] == 4)
    supplementary = next(r for r in values if r['n'] == 4 and r['p'] == 4)
    require(main['lattice'] > main['iid'], 'claimed counterexample is not strict')
    require(supplementary['lattice'] > Q(2, 315) > supplementary['iid'],
            'second counterexample lower bound control')
    # Dimensional checks evaluate the analytically proved all-(n,d) expression.
    dimension_controls = [{'n': n, 'd': d,
                           'second_moment': (Q(1, 2)**d-Q(1, 3)**d)/n}
                          for n in range(1, 8) for d in range(1, 8)]
    # Coincident indexed points are retained. This test does not delete samples.
    require(fixed_points_moment([Q(1, 3)]*3, 4) ==
            fixed_points_moment([Q(1, 3)], 4), 'collision multiplicity control')
    adverse = adverse_checks()
    return {'method': 'complete affine wrap strips with direct antiderivatives',
            'input_pins': pins, 'moments': values, 'cells': all_records,
            'dimension_formula_evaluations': dimension_controls,
            'adverse_controls': adverse, 'requirements': CHECKS,
            'strict_counterexample_ratio': main['lattice']/main['iid']}


if __name__ == '__main__':
    result = run()
    if sys.argv[1:] == ['--negative-guard']:
        require(False, 'deliberate negative guard remains active under optimization')
    elif sys.argv[1:]:
        raise ValueError('unknown command-line arguments')
    print(json.dumps(result, indent=2, default=str, sort_keys=True))
