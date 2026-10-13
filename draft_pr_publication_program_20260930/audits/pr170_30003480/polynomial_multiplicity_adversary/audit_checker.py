#!/usr/bin/env python3
"""Independent exact checks. Supplementary to DERIVATION.md, not a proof by sampling.

Only Python's standard library is used. Failures use explicit exceptions, so
optimization does not disable checks. No author verifier or results were read.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import ast
import hashlib
import json
import platform
import sys


class AuditFailure(RuntimeError):
    pass


def require(condition, label):
    if not condition:
        raise AuditFailure(label)


class Poly:
    """Sparse exact polynomial in three indeterminates over the rationals."""
    def __init__(self, terms=None):
        self.terms = {e: Q(c) for e, c in (terms or {}).items() if c}

    @staticmethod
    def lift(value):
        return value if isinstance(value, Poly) else Poly({(0, 0, 0): Q(value)})

    def __add__(self, other):
        other = self.lift(other)
        data = dict(self.terms)
        for e, c in other.terms.items():
            data[e] = data.get(e, Q(0)) + c
        return Poly(data)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        data = {}
        for e, a in self.terms.items():
            for f, b in other.terms.items():
                k = tuple(x + y for x, y in zip(e, f))
                data[k] = data.get(k, Q(0)) + a * b
        return Poly(data)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, 'invalid exponent')
        result = Poly.lift(1)
        for _ in range(exponent):
            result = result * self
        return result

    def __eq__(self, other):
        return self.terms == self.lift(other).terms

    def substitute(self, values):
        lifted = [self.lift(v) for v in values]
        powers = [[v ** k for k in range(1 + max((e[i] for e in self.terms), default=0))]
                  for i, v in enumerate(lifted)]
        out = Poly.lift(0)
        for e, c in self.terms.items():
            term = Poly.lift(c)
            for i in range(3):
                term = term * powers[i][e[i]]
            out = out + term
        return out

    def evaluate(self, values):
        return sum((c * values[0] ** e[0] * values[1] ** e[1] * values[2] ** e[2]
                    for e, c in self.terms.items()), Q(0))


t = tuple(Poly({tuple(int(i == j) for i in range(3)): 1}) for j in range(3))
x, b, c = t
L = x - b - c
Lp = x + b + c - 1


def tau(poly, selected=(0,)):
    return poly.substitute([1 - t[i] if i in selected else t[i] for i in range(3)])


def coordinate_form(poly, plane):
    require(plane in ('boundary', 'reflected'), 'unknown plane')
    solution = x + b + c if plane == 'boundary' else x + 1 - b - c
    return poly.substitute([solution, b, c])


def exact_multiplicity(poly, plane):
    transformed = coordinate_form(poly, plane)
    require(bool(transformed.terms), 'zero polynomial has no finite exact multiplicity')
    return min(e[0] for e in transformed.terms)


def residual_restriction_nonzero(poly, plane, claimed):
    transformed = coordinate_form(poly, plane)
    return any(e[0] == claimed and coefficient != 0
               for e, coefficient in transformed.terms.items())


def weights(params):
    a, bb, cc = params
    return (1 - Q(1, 2) * (a + bb + cc),
            Q(1, 2) * (-a + bb + cc),
            Q(1, 2) * (a - bb + cc),
            Q(1, 2) * (a + bb - cc))


def check_weight_identities(ws):
    require(sum(ws) == 1, 'squared amplitudes must sum to one')
    require(ws[2] + ws[3] == t[0], 'mode 1 eigenvalue')
    require(ws[1] + ws[3] == t[1], 'mode 2 eigenvalue')
    require(ws[1] + ws[2] == t[2], 'mode 3 eigenvalue')


def determinant_map(value):
    return value * (1 - value)


def determinant_margins(params):
    ds = tuple(determinant_map(v) for v in params)
    return tuple(sum(ds) - 2 * d for d in ds)


def strict_triangle(params):
    return all(sum(params) - 2 * v > 0 for v in params)


def domain_check(params):
    require(all(0 < v < Q(1, 2) for v in params), 'point is not inside D')
    require(all(v > 0 for v in determinant_margins(params)), 'point is not inside H_3')


def gram_determinants(tensor, n):
    grams = []
    for i in range(n):
        norm0 = norm1 = cross = Q(0)
        for rest in product((0, 1), repeat=n - 1):
            key0 = rest[:i] + (0,) + rest[i:]
            key1 = rest[:i] + (1,) + rest[i:]
            a, bb = tensor.get(key0, Q(0)), tensor.get(key1, Q(0))
            norm0 += a * a
            norm1 += bb * bb
            cross += a * bb
        grams.append((norm0 * norm1 - cross * cross, norm0, norm1, cross))
    return grams


def extend(tensor, unit):
    return {key + (i,): value * component
            for key, value in tensor.items() for i, component in enumerate(unit)}


def norm2(tensor):
    return sum((v * v for v in tensor.values()), Q(0))


def check_extension(tensor, unit):
    old_n = len(next(iter(tensor)))
    enlarged = extend(tensor, unit)
    old_grams = gram_determinants(tensor, old_n)
    new_grams = gram_determinants(enlarged, old_n + 1)
    require(norm2(enlarged) == norm2(tensor), 'unit-factor norm preservation')
    require(new_grams[:-1] == old_grams, 'all previous Gram matrices preserved')
    require(new_grams[-1][0] == 0, 'new unit-vector factor determinant zero')
    return enlarged


def main():
    positive = []
    negative = []

    def record(label, action):
        action()
        positive.append(label)

    def reject(label, action):
        try:
            action()
        except AuditFailure as error:
            negative.append({'mutation': label, 'caught': True, 'reason': str(error)})
        else:
            raise AuditFailure('mutation survived: ' + label)

    record('no assert statements in checker', lambda: require(
        not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(Path(__file__).read_text()))),
        'assert statements could disappear under -O'))
    record('generic real parity support eigenvalue identities', lambda: check_weight_identities(weights(t)))
    count = 0
    for vals in product([Q(k, 8) for k in range(5)], repeat=3):
        feasible = all(sum(vals) >= 2 * v for v in vals)
        ws = weights(vals)
        require((all(v >= 0 for v in ws)) == feasible, 'finite weight feasibility mismatch')
        require(sum(ws) == 1, 'finite weight normalization')
        if feasible:
            require(ws[0] >= Q(1, 4), 'leading parity weight bound')
            count += 1
    positive.append('exact parity-weight grid including zeros and half-eigenvalue endpoints')

    d = tuple(determinant_map(v) for v in t)
    generic = 3 + 2 * d[0] - 5 * d[1] * d[2] + d[0] ** 2 * d[2]
    record('each determinant substitution involution', lambda: require(
        all(tau(generic, (i,)) == generic for i in range(3)), 'invariance failure'))
    record('affine reflection sends boundary equation to negative interior equation', lambda: require(
        tau(L) == -Lp, 'wrong reflected plane'))

    K = Poly.lift(1)
    for bits in product((0, 1), repeat=3):
        K = K * tau(L, tuple(i for i, bit in enumerate(bits) if bit))
    record('full orbit product invariant under all coordinate involutions', lambda: require(
        all(tau(K, (i,)) == K for i in range(3)), 'orbit product invariance'))
    record('exact orbit-product multiplicity is one on both planes', lambda: require(
        exact_multiplicity(K, 'boundary') == exact_multiplicity(K, 'reflected') == 1,
        'exact multiplicities disagree'))
    K2 = K ** 2
    record('squared orbit-product multiplicity is two on both planes', lambda: require(
        exact_multiplicity(K2, 'boundary') == exact_multiplicity(K2, 'reflected') == 2,
        'squared exact multiplicities disagree'))
    record('generic nonzero residual restrictions at exact multiplicity', lambda: require(
        all(residual_restriction_nonzero(K, plane, 1) for plane in ('boundary', 'reflected')),
        'residual restriction vanishes'))

    true_boundary = (b + c, b, c)
    mm = determinant_margins(true_boundary)
    expected = (2 * b * c, 2 * c * (1 - b - c), 2 * b * (1 - b - c))
    record('symbolic true-boundary strict-H margins', lambda: require(mm == expected, 'H boundary identity'))
    reflected = (1 - b - c, b, c)
    record('symbolic reflected-plane strict-H margins', lambda: require(
        determinant_margins(reflected) == (2 * b * c, 2 * reflected[0] * c, 2 * reflected[0] * b),
        'H interior identity'))

    eps = Q(1, 128)
    actual_minus = (Q(1, 4) - eps, Q(1, 8), Q(1, 8))
    actual_plus = (Q(1, 4) + eps, Q(1, 8), Q(1, 8))
    interior_minus = (Q(1, 3) - eps, Q(1, 3), Q(1, 3))
    interior_plus = (Q(1, 3) + eps, Q(1, 3), Q(1, 3))
    for point in (actual_minus, actual_plus, interior_minus, interior_plus):
        domain_check(point)
    require(strict_triangle(actual_minus) and not strict_triangle(actual_plus), 'actual crossing classification')
    require(strict_triangle(interior_minus) and strict_triangle(interior_plus), 'interior crossing classification')
    require((-K).evaluate(actual_minus) > 0 and (-K).evaluate(actual_plus) < 0, 'odd boundary sign witness')
    require((-K).evaluate(interior_minus) * (-K).evaluate(interior_plus) < 0, 'odd interior sign witness')
    require(K2.evaluate(actual_plus) > 0, 'even factor cannot exclude outside point')
    positive.append('both rational local crossings remain strictly in cube and H_3')
    positive.append('odd invariant candidate passes actual crossing and fails interior nonnegativity')
    positive.append('even invariant candidate fails actual crossing exclusion')

    outsider = (Q(5, 16), Q(1, 8), Q(1, 8))
    domain_check(outsider)
    require(not strict_triangle(outsider), 'outside witness triangle violation')
    require(tuple(determinant_map(v) for v in outsider) == (Q(55, 256), Q(28, 256), Q(28, 256)),
            'outside determinant coordinates')
    positive.append('infeasible determinant point strictly inside H_3 excludes zero restrictions')

    tri = -(L * (b - x - c) * (c - x - b))
    for vals in product([Q(k, 8) for k in range(5)], repeat=3):
        require((tri.evaluate(vals) >= 0) == all(sum(vals) >= 2 * v for v in vals),
                'triangle product finite classification')
    require(tau(tri) != tri, 'triangle product incorrectly invariant')
    positive.append('triangle product illustrates why dropping determinant-only invariance changes problem')

    tensor = {(0, 0, 0): Q(4, 5), (0, 1, 1): Q(2, 5),
              (1, 0, 1): Q(2, 5), (1, 1, 0): Q(1, 5)}
    require(norm2(tensor) == 1, 'rational real tensor normalization')
    base_grams = gram_determinants(tensor, 3)
    require([row[0] for row in base_grams] == [Q(4, 25), Q(4, 25), Q(136, 625)],
            'rational tensor determinant values')
    current = tensor
    for _ in range(3):
        current = check_extension(current, (Q(3, 5), Q(4, 5)))
    require(gram_determinants({(0, 0, 0): Q(0)}, 3) == [(0, 0, 0, 0)] * 3, 'zero tensor')
    positive.append('exact rank-one embedding Gram preservation for four through six factors and zero tensor')

    # For d_i=3/16, d_j=7/64: at s=1 the ratio is 1/2;
    # at s=7/8 it is (7-sqrt(21))/6. Their difference is
    # (sqrt(21)-4)/6 > 0, checked by squaring positive numbers.
    require(Q(21) > Q(4) ** 2 and Q(7, 8) ** 2 >= 4 * Q(3, 16), 'ratio witness order')
    positive.append('exact normalization-ratio order at a feasible positive trace')

    reject('replace t(1-t) by t(1+t)', lambda: require(
        tau(x * (1 + x)) == x * (1 + x), 'altered determinant map loses involution'))
    bad_ws = list(weights(t)); bad_ws[1], bad_ws[2] = bad_ws[2], bad_ws[1]
    reject('swap the 011 and 101 weights', lambda: check_weight_identities(bad_ws))
    reject('reflect t1 to -t1 rather than 1-t1', lambda: require(
        L.substitute([-x, b, c]) == -Lp, 'incorrect affine reflection'))
    reject('claim divisibility exponent one is exact for squared orbit product', lambda: require(
        exact_multiplicity(K2, 'boundary') == 1, 'exact exponent is two'))
    reject('assume quotient nonzero on plane after underdividing squared factor', lambda: require(
        residual_restriction_nonzero(K2, 'boundary', 1), 'underdivided residual vanishes on entire plane'))
    reject('allow odd multiplicity on an interior feasible plane', lambda: require(
        (-K).evaluate(interior_minus) >= 0 and (-K).evaluate(interior_plus) >= 0,
        'odd multiplicity gives opposite interior signs'))
    reject('allow even multiplicity to exclude actual outside side', lambda: require(
        K2.evaluate(actual_plus) < 0, 'even multiplicity stays positive outside'))
    reject('change boundary determinant-H margin from +2bc to -2bc', lambda: require(
        mm[0] == -2 * b * c, 'wrong strict-H identity'))
    reject('accept an identically zero polynomial on higher-factor face', lambda: require(
        Poly.lift(0).evaluate(outsider) < 0, 'zero restriction includes infeasible face point'))
    reject('use a nonunit vector in rank-one factor removal', lambda: check_extension(
        tensor, (Q(3, 5), Q(3, 5))))
    reject('reverse the trace-ratio monotonicity', lambda: require(
        Q(21) <= Q(4) ** 2, 'reversed ratio order would require sqrt(21)<=4'))
    reject('let triangle-coordinate polynomial descend without invariance', lambda: require(
        tau(tri) == tri, 'triangle polynomial is not a polynomial in determinant coordinates'))

    data = {
        'status': 'pass',
        'role': 'finite exact supplementary evidence, not the universal proof',
        'python_version': platform.python_version(),
        'optimization_active': not __debug__,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'positive_checks': positive,
        'finite_weight_grid': {'total_points': 125, 'triangle_feasible_points': count},
        'negative_mutations': negative,
        'positive_check_count': len(positive),
        'negative_mutation_count': len(negative),
        'outside_H3_point': ['55/256', '28/256', '28/256'],
        'sampled_higher_factor_counts': [4, 5, 6],
        'universal_claim_proof': 'DERIVATION.md'
    }
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    try:
        main()
    except AuditFailure as error:
        print(json.dumps({'status': 'fail', 'reason': str(error)}, indent=2))
        sys.exit(1)
