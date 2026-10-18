#!/usr/bin/env python3
"""Independent, standard-library-only audit of one sufficient Spin17 pairing.

No Maple, source-author package, or printed Schubert coefficients are used.
Method 1 is exact torus localization on IG(5,16).
Method 2 is integer Pieri multiplication in Gr(5,16).
See COMPUTATION_NOTES.md for geometric assumptions and the interpretation.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import comb, prod
import json


def require(condition, message):
    """Validation stays active under normal, -O and -OO Python execution."""
    if not condition:
        raise ArithmeticError(message)


def v2(value):
    if not value:
        return None
    value = abs(value)
    return (value & -value).bit_length() - 1


def elementary(roots):
    values = [1] + [0] * len(roots)
    for root in roots:
        for j in range(len(roots), 0, -1):
            values[j] += root * values[j - 1]
    return values


def fixed_points(weights, m):
    """All coordinate isotropic m-planes; return roots and tangent Euler classes."""
    n = len(weights)
    for indices in combinations(range(n), m):
        ys = [weights[i] for i in range(n) if i not in indices]
        for signs in product((-1, 1), repeat=m):
            xs = [weights[i] * sign for i, sign in zip(indices, signs)]
            # T_IG = Hom(S,S^perp/S) + Sym^2(S^dual).
            sym = prod(-x - y for i, x in enumerate(xs) for y in xs[i:])
            cross = prod(sign * y - x for x in xs for y in ys for sign in (-1, 1))
            euler = sym * cross
            require(euler, 'Nonzero tangent denominator')
            # Independent tangent derivation: IG is cut out by wedge^2 S^dual in Gr.
            all_weights = list(weights) + [-w for w in weights]
            outside = [w for w in all_weights if w not in xs]
            ambient = prod(y - x for x in xs for y in outside)
            normal = prod(-x - y for i, x in enumerate(xs) for y in xs[i + 1:])
            require(normal and Fraction(ambient, normal) == euler, 'Ambient/normal tangent identity')
            # The odd-orthogonal tangent replaces diagonal -2*x by -x.
            odd_euler = cross * prod(-x for x in xs)
            odd_euler *= prod(-x - y for i, x in enumerate(xs) for y in xs[i + 1:])
            require(euler == 2**m * odd_euler, 'Symplectic/odd-orthogonal tangent ratio')
            a = prod(sum(xs) + sum(s*y for s, y in zip(ss, ys))
                     for ss in product((-1, 1), repeat=n-m))
            yield xs, ys, elementary(xs), euler, odd_euler, a


def localize(weights, m, numerator, odd=False):
    return sum((Fraction(numerator(xs, ys, e, a), odd_euler if odd else euler)
                for xs, ys, e, euler, odd_euler, a in fixed_points(weights, m)), Fraction())


# Polynomials in e1,...,e5: exponent tuple -> exact rational coefficient.
M = 5
ONE = {(0,)*M: Fraction(1)}


def var(i):
    return {tuple(int(j == i-1) for j in range(M)): Fraction(1)}


def add(*polys):
    out = defaultdict(Fraction)
    for poly in polys:
        for powers, coefficient in poly.items():
            out[powers] += coefficient
    return {k: v for k, v in out.items() if v}


def scale(poly, coefficient):
    return {k: v*coefficient for k, v in poly.items() if v*coefficient}


def multiply(left, right):
    out = defaultdict(Fraction)
    for powers, coefficient in left.items():
        for powers2, coefficient2 in right.items():
            out[tuple(a+b for a, b in zip(powers, powers2))] += coefficient*coefficient2
    return {k: v for k, v in out.items() if v}


def power(poly, exponent):
    out = ONE
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def ordinary_a():
    # Newton identities, then h_j(x_1^2,...,x_5^2), j<=3.
    ps = {}
    for k in range(1, 7):
        terms = [scale(multiply(var(i), ps[k-i]), (-1)**(i-1))
                 for i in range(1, min(k-1, M)+1)]
        if k <= M:
            terms.append(scale(var(k), (-1)**(k-1)*k))
        ps[k] = add(*terms)
    h1 = ps[2]
    h2 = scale(add(power(ps[2], 2), ps[4]), Fraction(1, 2))
    h3 = scale(add(power(ps[2], 3), scale(multiply(ps[2], ps[4]), 3),
                   scale(ps[6], 2)), Fraction(1, 6))
    x = var(1)
    a = add(power(x, 8), scale(multiply(h1, power(x, 6)), 4),
            multiply(add(scale(power(h1, 2), 6), scale(h2, -8)), power(x, 4)),
            multiply(add(scale(power(h1, 3), 4), scale(multiply(h1, h2), -16),
                         scale(h3, 64)), power(x, 2)),
            power(add(power(h1, 2), scale(h2, -4)), 2))
    require(all(v.denominator == 1 for v in a.values()), 'Integral ordinary-a coefficients')
    require(all(sum((i+1)*e for i, e in enumerate(k)) == 8 for k in a), 'Homogeneous degree8 ordinary-a polynomial')
    return {k: int(v) for k, v in a.items()}


def vertical_strips(shape, k):
    for rows in combinations(range(M), k):
        result = tuple(v + int(i in rows) for i, v in enumerate(shape))
        if result[0] <= 11 and all(result[i] >= result[i+1] for i in range(M-1)):
            yield result


def times_elementary(ring, k):
    out = defaultdict(int)
    for shape, coefficient in ring.items():
        for result in vertical_strips(shape, k):
            out[result] += coefficient
    return dict(out)


def times_polynomial(ring, poly):
    out = defaultdict(int)
    for exponents, coefficient in poly.items():
        term = ring
        for k, exponent in enumerate(exponents, 1):
            for _ in range(exponent):
                term = times_elementary(term, k)
        for shape, c in term.items():
            out[shape] += coefficient*c
    return {k: v for k, v in out.items() if v}


def pieri_pairing(a, with_normal=True):
    # prod_(i<j)(x_i+x_j) = s_(4,3,2,1,0), the normal Euler class.
    ring = {(4,3,2,1,0) if with_normal else (0,)*5: 1}
    for _ in range(9):
        ring = times_elementary(ring, 2)
    ring = times_elementary(ring, 3)
    for _ in range(3):
        ring = times_polynomial(ring, a)
    # Total degree 55 is odd: T roots versus T^dual roots change sign.
    return -ring.get((11,)*5, 0)


def main():
    a_poly = ordinary_a()
    target = lambda xs, ys, e, a: a**3 * e[2]**9 * e[3]
    weight_sets = [(1,2,3,4,5,6,7,8), (1,3,5,7,11,13,17,19), (2,4,6,8,10,12,14,16)]
    localization = [localize(ws, 5, target) for ws in weight_sets]
    require(all(x.denominator == 1 for x in localization), 'Integral localization results')
    integer = localization[0].numerator
    require(all(x == integer for x in localization), 'Weight-independence of localization')
    pieri = pieri_pairing(a_poly)
    require(integer == pieri == -14668659594398531584, 'Agreement of localization and integer Pieri')
    require(v2(integer) == 22 and integer // 2**22 == -3497280977821, 'Pairing valuation and odd quotient')
    # A rational integral class ztilde has a=2^8*ztilde.
    odd_degree = localize(weight_sets[0], 5,
                          lambda xs, ys, e, a: Fraction(target(xs, ys, e, a), 2**24), odd=True)
    require(odd_degree == Fraction(integer, 2**19) == -27978247822568, 'Odd-orthogonal rational zero-cycle degree')
    require(odd_degree.denominator == 1 and v2(odd_degree.numerator) == 3, 'Odd-orthogonal zero-cycle degree valuation')

    controls = []
    for n, m, expected in [(1,1,1), (3,1,1), (2,2,2), (3,2,14), (3,3,16)]:
        dim = m*(2*n-m) - m*(m-1)//2
        actual = localize(tuple(range(1,n+1)), m,
                          lambda xs, ys, e, a: (-e[1])**dim)
        require(actual == expected, 'Small Grassmannian degree control')
        controls.append({'n':n, 'm':m, 'plucker_degree':expected, 'actual':actual.numerator})
    below = localize(weight_sets[0], 5, lambda xs, ys, e, a: a**3*e[2]**8*e[3])
    require(below == 0, 'Below-dimension vanishing')
    no_normal = pieri_pairing(a_poly, with_normal=False)
    require(no_normal == 0 and no_normal != integer, 'Normal-Euler omission mutant rejected')
    # Execute a wrong-denominator variant that omits 2 in each of five long roots.
    mutant_value = sum((Fraction(target(xs, ys, e, a), euler//2**5)
                        for xs, ys, e, euler, odd_euler, a in fixed_points(weight_sets[0],5)), Fraction())
    require(mutant_value.denominator == 1, 'Integral long-root omission mutant')
    mutant_long_roots = mutant_value.numerator
    require(mutant_long_roots == integer*2**5, 'Long-root omission multiplies by32')
    require(mutant_long_roots != pieri and v2(mutant_long_roots) == 27, 'Long-root omission mutant rejected')
    # The point count is binomial(8,5)*2^5; all tangent rank checks hold in fixed_points.
    require(sum(1 for _ in fixed_points(weight_sets[0],5)) == comb(8,5)*2**5 == 1792, 'Fixed-point count')

    print(json.dumps({
        'schema':1, 'arithmetic':'exact integers and fractions, standard Python only',
        'source_author_software_executed':False, 'methods':['torus localization','Grassmannian vertical Pieri'],
        'fixed_point_count':1792, 'ig_dimension':45,
        'pairing_class':'a^3*c2(T)^9*c3(T)',
        'localization_weight_sets':[list(ws) for ws in weight_sets],
        'pairing_values':[x.numerator for x in localization], 'pieri_value':pieri,
        'pairing_v2':22, 'odd_quotient_after_2_power_22':integer//2**22,
        'class_conclusion':'v2(a^3)<=22; nondivisibility by 2^23; no class-level exact valuation claimed',
        'odd_orthogonal_rational_zero_cycle_degree':odd_degree.numerator,
        'odd_orthogonal_zero_cycle_degree_v2':3,
        'sufficient_index_conclusion':'generic Spin17 OG5 index divides 8, conditional on published rationality input',
        'ordinary_a_in_e1_to_e5':[{'exponents':list(k),'coefficient':v} for k,v in sorted(a_poly.items())],
        'controls':controls, 'below_dimension_integral':below.numerator,
        'mutants':[
            {'name':'omit normal Euler class in ambient Grassmannian','value':no_normal,'rejected':True},
            {'name':'omit factor2 in long tangent roots','value':mutant_long_roots,'v2':27,'rejected':True}],
        'limits':['No full printed Schubert expansion reproduced','No proof-assistant certificate',
                  'Standard localization and Grassmannian Chow/Pieri theorems remain inputs',
                  'Published Prop3.4 rationality and Spin/parabolic identification remain inputs']
    },indent=2))


if __name__ == '__main__':
    main()
