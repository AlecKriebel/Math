#!/usr/bin/env python3
"""Fresh guarded deterministic finite controls for the frozen PR445 families.

Mechanisms follow the frozen independent checker and the independently authored
spectral/geometry controls, read as review objects; no frozen code is imported
or executed. All physical finite counts retain boundary and imbalance terms.
Only exact integers/Fractions are used for checks. Historical float diagnostics
are converted from exact rational values to compare their stored JSON numbers.
No finite computation proves the infinite Rudin-Shapiro theorem.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product


class ControlFailure(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ControlFailure(message)


RHO = {'a': 'ab', 'b': 'ac', 'c': 'db', 'd': 'dc'}
C = [(0, 0), (3, 3), (10, 0), (0, 10)]
MEANS = [F(1), F(1), F(1, 2), F(1, 2)]


def substitute(word):
    return ''.join(RHO[letter] for letter in word)


@lru_cache(None)
def rs(n):
    if n == 0:
        return 1
    if n == -1:
        return -1
    q, r = divmod(n, 4)
    return rs(q) * (1 if r < 2 or (q+r) % 2 == 0 else -1)


def substitution_controls(mutant=None):
    rho2 = {c: substitute(substitute(c)) for c in RHO}
    require('ca' in rho2['c'], 'RS legal bilateral seed is missing')
    require(rho2['c'].endswith('c') and rho2['a'].startswith('a'), 'RS seed gluing fails')
    primitive_depth = None
    for depth in range(1, 8):
        images = {c: c for c in RHO}
        for _ in range(depth):
            images = {c: substitute(w) for c, w in images.items()}
        if all(set(w) == set(RHO) for w in images.values()):
            primitive_depth = depth
            break
    require(primitive_depth == 3, 'RS primitivity depth differs')
    for c, d in product(RHO, repeat=2):
        require({(a, b) for a in images[c] for b in images[d]} == set(product(RHO, repeat=2)),
                'Product block primitivity fails')
    word = 'a'
    for _ in range(18):
        word = substitute(word)
    code = 'ac' if mutant == 'rs' else 'ab'
    signs = [1 if c in code else -1 for c in word]
    bits = [(-1) ** ((n & (n >> 1)).bit_count()) for n in range(len(word))]
    require(signs == bits, 'RS one-sided substitution/bit coding differs')
    left, right = 'c', 'a'
    for _ in range(6):
        left, right = substitute(substitute(left)), substitute(substitute(right))
    letters = list(enumerate(left+right, start=-len(left)))
    require([1 if c in 'ab' else -1 for _, c in letters] ==
            [rs(n) for n, _ in letters], 'RS bilateral recursion differs')
    for n, c in letters:
        require(c in ('a', 'd') if n % 2 == 0 else c in ('b', 'c'), 'RS letter parity differs')
    samples = []
    for length in [1024, 4096, 16384, 65536, 262144]:
        values = signs[:length]
        correlations = [F(sum(values[i]*values[i+h] for i in range(length-h)), length)
                        for h in range(1, 65)]
        samples.append({'length': length, 'mean': float(F(sum(values), length)),
                        'max_abs_lag_1_to_64': float(max(map(abs, correlations)))})
    result = {'rho_primitive_depth': primitive_depth, 'rho_vs_bit_formula_sites': len(word),
              'bilateral_source_recursion_sites': len(letters), 'rs_finite_samples': samples,
              'product_block_primitivity_depth': primitive_depth,
              'bilateral_letter_parity_sites': len(letters), 'rho2_images': rho2}
    return signs, result


def marker_controls():
    pairs = [(i, j) for i, c in enumerate(C) for j, d in enumerate(C)
             if tuple((d[k]-c[k]) % 30 for k in [0, 1]) == (3, 3)]
    require(pairs == [(0, 1)], 'Deterministic marker residue differs')
    bad = [(0, 0), (5, 0), (10, 0), (0, 10)]
    bad_pairs = [(i, j) for i, c in enumerate(bad) for j, d in enumerate(bad)
                 if tuple((d[k]-c[k]) % 30 for k in [0, 1]) == (5, 0)]
    require(bad_pairs == [(0, 1), (1, 2)], 'Known bad marker did not expose its extra pair')
    cases = 0
    for xs, ys in product(product((-1, 1), repeat=3), repeat=2):
        pts = {(30*i+C[c][0], 30*j+C[c][1]) for i, j in product(range(3), repeat=2)
               for c in [0, 1]+([2] if xs[i] == 1 else [])+([3] if ys[j] == 1 else [])}
        found = {p for p in pts if (p[0]+3, p[1]+3) in pts}
        require(found == {(30*i, 30*j) for i, j in product(range(3), repeat=2)},
                'Actual local marker membership differs')
        cases += 1
    return {'exhaustive_local_marker_cases': cases,
            'bad_marker_negative_control': 'caught extra pair (1,2)'}


def limit_coefficient(r):
    out = F(0)
    for c, d in product(range(4), repeat=2):
        if all((r[k]-C[d][k]+C[c][k]) % 30 == 0 for k in [0, 1]):
            out += MEANS[c]*MEANS[d]
    if r[0] == 0 and r[1] % 30 == 0:
        out += F(1, 4)
    if r[1] == 0 and r[0] % 30 == 0:
        out += F(1, 4)
    return out


def finite_pairs(r, xs, ys):
    # Independent axis membership sums retain every cell overlap and nonzero mean.
    N = len(xs)
    total = 0
    for c, d in product(range(4), repeat=2):
        rem = [r[k]-C[d][k]+C[c][k] for k in [0, 1]]
        if any(v % 30 for v in rem):
            continue
        m, n = [v // 30 for v in rem]
        I = range(max(0, -m), min(N, N-m))
        J = range(max(0, -n), min(N, N-n))
        xc = sum((c != 2 or xs[i] == 1) and (d != 2 or xs[i+m] == 1) for i in I)
        yc = sum((c != 3 or ys[j] == 1) and (d != 3 or ys[j+n] == 1) for j in J)
        total += xc*yc
    return total


def physical_controls(signs, mutant=None):
    shifts = sorted({(d[0]-c[0]+30*m, d[1]-c[1]+30*n)
                     for c, d in product(C, repeat=2)
                     for m, n in product(range(-1, 2), repeat=2)})
    require(len(shifts) == 117, 'Physical displacement list differs')
    physical = []
    for N in [64, 128, 256]:
        xs, ys = signs[:N], signs[1024:1024+N]
        pts = {(30*i+C[c][0], 30*j+C[c][1]) for i, j in product(range(N), repeat=2)
               for c in [0, 1]+([2] if xs[i] == 1 else [])+([3] if ys[j] == 1 else [])}
        max_error, worst = F(0), None
        for r in shifts:
            actual = sum((p[0]+r[0], p[1]+r[1]) in pts for p in pts)
            if mutant == 'physical_pairs':
                actual += 1
            expected = finite_pairs(r, xs, ys)
            require(actual == expected, f'Physical direct/factored pair count differs: {N}, {r}, {actual}, {expected}')
            error = abs(F(actual, N*N)-limit_coefficient(r))
            if error > max_error:
                max_error, worst = error, r
        physical.append({'side': N, 'point_count': len(pts),
                         'empirical_density': float(F(len(pts), N*N)),
                         'tested_displacements': len(shifts),
                         'max_infinite_limit_error': float(max_error),
                         'worst_displacement_grid30': list(worst) if worst is not None else None})
    # These are finite diagnostics, never asserted equal to their infinite limit.
    N = 256
    require(sum(signs[i]*signs[j] for i, j in product(range(N), repeat=2)) ==
            sum(signs[:N])**2, 'Finite Cartesian product averages differ')
    # A distinct case uses negative indices and x=y at a nonzero phase.
    xs = [rs(i-37) for i in range(32)]
    ys = list(xs)
    phase = (7, -11)
    pts = {(30*i+C[c][0]-phase[0], 30*j+C[c][1]-phase[1])
           for i, j in product(range(32), repeat=2)
           for c in [0, 1]+([2] if xs[i] == 1 else [])+([3] if ys[j] == 1 else [])}
    for r in shifts:
        actual = sum((p[0]+r[0], p[1]+r[1]) in pts for p in pts)
        require(actual == finite_pairs(r, xs, ys), 'Translated identical-sequence pair count differs')
    return {'physical_point_count_controls': physical,
            'additional_equal_sequence_negative_index_phase_pair_checks': len(shifts),
            'total_physical_pair_checks': 4*len(shifts)}


def section_integral(t, mutant=None):
    lo, hi = t.__floor__()-2, t.__ceil__()+3
    cuts = sorted({F(0), F(1)} | {F(z)-t for z in range(lo, hi) if 0 < F(z)-t < 1})
    out = F(0)
    for a, b in zip(cuts, cuts[1:]):
        shift = ((a+b)/2+t).__floor__()
        if shift == 0:
            out += b-a
    return 2*out if mutant == 'subdivision' else out


def flow_controls(mutant=None):
    checks = 0
    for denom in [2, 3, 5, 7, 11, 13]:
        for num in range(-4*denom, 4*denom+1):
            t = F(num, denom)
            require(section_integral(t, mutant) == max(F(0), 1-abs(t)),
                    f'Subdivision/triangle section correlation differs at {t}')
            checks += 1
    require(section_integral(F(0)) == 1 and section_integral(F(-1)) == section_integral(F(1)) == 0,
            'Section norm/endpoints differ')
    return {'exact_flow_section_checks': checks}


def gluing_controls():
    # Physical seam identity with buffered finite windows and legal RS data.
    def points(x, y, phase):
        return {(30*i+C[c][0]-phase[0], 30*j+C[c][1]-phase[1])
                for i, xv in x.items() for j, yv in y.items()
                for c in [0, 1]+([2] if xv == 1 else [])+([3] if yv == 1 else [])}
    def window(pts):
        return {p for p in pts if -180 <= p[0] <= 180 and -180 <= p[1] <= 180}
    x = {i: rs(i) for i in range(-20, 21)}
    y = {i: rs(i+5) for i in range(-20, 21)}
    checks = 0
    for phase in product((0, 1, 10, 27), repeat=2):
        for m, n in product(range(-2, 3), repeat=2):
            sx = {i: x[i+m] for i in range(-15, 16)}
            sy = {j: y[j+n] for j in range(-15, 16)}
            require(window(points(x, y, (phase[0]+30*m, phase[1]+30*n))) ==
                    window(points(sx, sy, phase)), 'Physical suspension representative gluing differs')
            checks += 1
    return {'physical_representative_gluing_checks': checks}


def run_checks(mutant=None):
    require(mutant in [None, 'rs', 'physical_pairs', 'subdivision'], 'Unknown deterministic-control mutant')
    signs, result = substitution_controls(mutant)
    result.update(marker_controls())
    result.update(physical_controls(signs, mutant))
    result.update(flow_controls(mutant))
    result.update(gluing_controls())
    result['scope'] = 'Fresh exact finite deterministic checks; historical diagnostics compared separately; no infinite theorem proved by sampling'
    return result
