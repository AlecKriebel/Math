#!/usr/bin/env python3
"""Exact replacement for the Spin17 finite divisibility calculation.
Python >=3.9, standard library only; no network, source files or Maple needed.
All checks use explicit exceptions, so -O and -OO retain every check.
The mathematical interpretation and literature dependencies are in REPORT.md.
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import factorial, prod
import json

ZERO = (0, 0, 0, 0, 0)
ONE = {ZERO: 1}
VARS = [{tuple(int(i == j) for i in range(5)): 1} for j in range(5)]


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def add(*polynomials):
    out = defaultdict(int)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] += coefficient
    return {m: c for m, c in out.items() if c}


def scale(polynomial, scalar):
    return {m: c * scalar for m, c in polynomial.items() if c * scalar}


def multiply(left, right):
    out = defaultdict(int)
    for a, c in left.items():
        for b, d in right.items():
            out[tuple(x + y for x, y in zip(a, b))] += c * d
    return {m: c for m, c in out.items() if c}


def power(polynomial, exponent):
    out = ONE
    for _ in range(exponent):
        out = multiply(out, polynomial)
    return out


def complete_from_elementary(elementary, maximum):
    complete = [ONE]
    for k in range(1, maximum + 1):
        complete.append(add(*(scale(multiply(elementary[j], complete[k-j]),
                                   (-1) ** (j+1))
                              for j in range(1, min(k, len(elementary)-1)+1))))
    return complete


def product_formula(u, q1, q2, q3):
    """Product over eight signs of u +/- y1 +/- y2 +/- y3; qj=e_j(y^2)."""
    return add(power(u, 8), scale(multiply(q1, power(u, 6)), -4),
               multiply(add(scale(power(q1, 2), 6), scale(q2, -8)), power(u, 4)),
               multiply(add(scale(power(q1, 3), -4),
                            scale(multiply(q1, q2), 16), scale(q3, -64)), power(u, 2)),
               power(add(power(q1, 2), scale(q2, -4)), 2))


def symbolic_identities():
    # First verify the eight-factor identity in a free integer polynomial ring.
    u, y1, y2, y3, unused = VARS
    ys = [y1, y2, y3]
    q = [ONE] + [{} for _ in range(3)]
    for y in ys:
        for k in range(3, 0, -1):
            q[k] = add(q[k], multiply(power(y, 2), q[k-1]))
    raw = ONE
    for signs in product((-1, 1), repeat=3):
        raw = multiply(raw, add(u, *(scale(y, s) for y, s in zip(ys, signs))))
    require(raw == product_formula(u, q[1], q[2], q[3]), 'eight-factor identity')

    # Here VARS instead mean elementary Chern classes e1,...,e5.
    elementary = [ONE] + VARS
    squared_elementary = [ONE]
    for k in range(1, 6):
        squared_elementary.append(add(*(
            scale(multiply(elementary[i], elementary[2*k-i]), (-1) ** (i+k))
            for i in range(6) if 0 <= 2*k-i <= 5)))
    hs = complete_from_elementary(squared_elementary, 4)  # h_j(x_1^2,...,x_5^2)
    a = product_formula(VARS[0], scale(hs[1], -1), hs[2], scale(hs[3], -1))
    numerator = add(a, scale(hs[4], -64))
    require(all(c % 128 == 0 for c in numerator.values()), 'a - 64 h4 is a multiple of 128')
    b = {m: c // 128 for m, c in numerator.items()}
    H = complete_from_elementary(elementary, 8)  # ordinary h_j(x_1,...,x_5)
    e1, e2, e3, e4, e5 = VARS
    certificate = add(
        multiply(add(multiply(e1, e3), multiply(power(e1, 2), e2)), H[4]),
        multiply(e3, H[5]), multiply(e2, H[6]), multiply(e1, H[7]), H[8])
    require(all(c % 2 == 0 for c in add(b, scale(certificate, -1)).values()),
            'explicit mod-2 ideal certificate for b')
    changed = add(numerator, ONE)
    require(any(c % 128 for c in changed.values()), 'negative control for normalization')
    return a, b


@lru_cache(None)
def vertical_pieri(partition, k, width):
    out = []
    for rows in combinations(range(len(partition)), k):
        q = tuple(v + (i in rows) for i, v in enumerate(partition))
        if q[0] <= width and all(q[i] >= q[i+1] for i in range(len(q)-1)):
            out.append(q)
    return tuple(out)


def act_elementary(state, k, width=11):
    out = defaultdict(int)
    for partition, coefficient in state.items():
        for q in vertical_pieri(partition, k, width):
            out[q] += coefficient
    return {q: c for q, c in out.items() if c}


def act_monomial(state, monomial, width=11):
    for k, exponent in enumerate(monomial, 1):
        for _ in range(exponent):
            state = act_elementary(state, k, width)
    return state


def act_polynomial(state, polynomial):
    out = defaultdict(int)
    for monomial, coefficient in polynomial.items():
        for partition, d in act_monomial(state, monomial).items():
            out[partition] += coefficient * d
    return {q: c for q, c in out.items() if c}


def integer_schur_pairing(b):
    # s_(4,3,2,1,0)=prod_(i<j)(x_i+x_j), the isotropic zero-locus class.
    state = {(4, 3, 2, 1, 0): 1}
    state = act_monomial(state, (0, 9, 1, 0, 0))  # e2^9 e3
    state_sizes = [len(state)]
    for _ in range(3):
        state = act_polynomial(state, b)
        state_sizes.append(len(state))
    target = (11, 11, 11, 11, 11)
    require(set(state) == {target}, 'top Schur coefficient has the correct degree')
    # Two independent standard type-A controls on the same Pieri implementation.
    determinant_control = act_monomial({ZERO: 1}, (0, 0, 0, 0, 11))
    require(determinant_control == {target: 1}, 'determinant top class control')
    hyperplane_control = act_monomial({ZERO: 1}, (55, 0, 0, 0, 0))
    hook_product = prod((11-j)+(5-i)-1 for i in range(5) for j in range(11))
    require(hyperplane_control == {target: factorial(55)//hook_product},
            'hook-length control for the degree of Gr(5,16)')
    return state[target], state_sizes


def elementary_values(xs):
    es = [1] + [0] * len(xs)
    for x in xs:
        for k in range(len(xs), 0, -1):
            es[k] += x * es[k-1]
    return es


def eight_factor_value(xs, ys):
    u = sum(xs)
    return prod(u + sum(s*y for s, y in zip(signs, ys))
                for signs in product((-1, 1), repeat=3))


def symplectic_pairing(weights, k, numerator):
    """Signed-subset fixed-point formula; xs are roots of T*, ys positive leftovers."""
    total = Fraction()
    count = 0
    for subset in combinations(weights, k):
        ys = [t for t in weights if t not in subset]
        for signs in product((-1, 1), repeat=k):
            xs = [s*t for s, t in zip(signs, subset)]
            denominator = (prod(xs[i]+xs[j] for i in range(k) for j in range(i, k))
                           * prod(x*x-y*y for x in xs for y in ys))
            require(denominator != 0, 'regular symplectic localization weights')
            total += Fraction(numerator(xs, ys), denominator)
            count += 1
    require(total.denominator == 1, 'symplectic pairing is integral')
    return total.numerator, count


def grassmannian_pairing(weights):
    """Ordinary Gr(5,16) evaluation of an independently eliminated polynomial lift."""
    total = Fraction()
    for xs in combinations(weights, 5):
        ys = [t for t in weights if t not in xs]
        es = elementary_values(xs)
        h = [1, 0, 0, 0]
        for x in xs:
            for j in range(1, 4):
                h[j] += x*x*h[j-1]
        u, h1, h2, h3 = es[1], h[1], h[2], h[3]
        a = (u**8 + 4*h1*u**6 + (6*h1*h1-8*h2)*u**4
             + (4*h1**3-16*h1*h2+64*h3)*u*u + (h1*h1-4*h2)**2)
        numerator = (a**3 * es[2]**9 * es[3]
                     * prod(xs[i]+xs[j] for i in range(5) for j in range(i+1, 5)))
        denominator = prod(x-y for x in xs for y in ys)
        total += Fraction(numerator, denominator)
    require(total.denominator == 1, 'ordinary Grassmannian pairing is integral')
    return total.numerator


def v2(n):
    require(n != 0, 'valuation of a nonzero integer')
    return (abs(n) & -abs(n)).bit_length() - 1


def main():
    a, b = symbolic_identities()
    normalized, sizes = integer_schur_pairing(b)
    require(normalized == 6994561955642, 'independently calculated normalized pairing receipt')
    target = normalized * 128**3
    weight_sets = [list(range(1, 9)), [1, 3, 7, 12, 20, 31, 45, 62],
                   [2, 5, 11, 17, 29, 43, 71, 101]]
    cross_checks = []
    def numerator(xs, ys):
        es = elementary_values(xs)
        return eight_factor_value(xs, ys)**3 * es[2]**9 * es[3]
    for weights in weight_sets:
        result, count = symplectic_pairing(weights, 5, numerator)
        require(result == target, 'type-C fixed-point result equals integer Schur calculation')
        require(count == 1792, 'Sp16/P5 Weyl-coset count')
        cross_checks.append({'weights': weights, 'points': count, 'pairing': result})
    require(grassmannian_pairing(tuple(range(1, 17))) == target,
            'ordinary Gr(5,16) rational evaluation matches both other routes')
    require(symplectic_pairing([1, 2, 3], 1, lambda x, y: x[0]**5)[0] == 1,
            'IG(1,6)=P5 control')
    require(symplectic_pairing([1, 2], 2, lambda x, y: sum(x)**3)[0] == 2,
            'IG(2,4)=quadric threefold control')
    require(v2(target) == 22 and normalized % 4 == 2, 'exact valuations')
    require(64-10-9 == 45 and 8*3+2*9+3 == 45, 'root and degree bookkeeping')
    output = {
        'schema': 1, 'checks': 'all passed; no assertions or floating point',
        'variety': 'IG(5,16)=Sp16/P5, standard root numbering',
        'dimension': 45, 'complement': 'c2(T*)^9 c3(T*)',
        'polynomial_normalization_identity': 'a = 128 b + 64 h4(x^2)',
        'mod2_identity': 'b = (e1 e3+e1^2 e2)h4+e3 h5+e2 h6+e1 h7+h8 (mod 2)',
        'b_polynomial': [{'exponents_e1_to_e5': list(m), 'coefficient': c}
                         for m, c in sorted(b.items())],
        'integer_schur_state_sizes': sizes,
        'pairing_b_cubed': normalized, 'pairing_a_cubed': target,
        'pairing_b_cubed_divided_by_2': normalized//2,
        'v2_pairing_a_cubed': v2(target),
        'v2_class_a_cubed': 22,
        'lower_divisibility_reason': 'a=128b; explicit ideal identity implies b^2=0 mod 2 on IG(5,16)',
        'upper_divisibility_reason': 'integral complementary pairing has valuation 22',
        'symplectic_cross_checks': cross_checks,
        'ordinary_grassmannian_cross_check': target,
        'small_geometry_and_hook_length_controls': 'passed',
        'source_author_software_executed': False,
        'printed_maple_schubert_coefficients_used_as_input': False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
