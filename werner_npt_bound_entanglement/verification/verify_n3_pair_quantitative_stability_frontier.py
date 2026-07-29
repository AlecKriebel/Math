#!/usr/bin/env python3
"""Exact verifier for the rank-one pair-sector stability frontier."""

import itertools

import sympy as sp


WORDS = list(itertools.product(range(3), repeat=3))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
DIMENSION = 27


def swap_replica_word(word, site):
    word = list(word)
    word[site], word[site + 3] = word[site + 3], word[site]
    return tuple(word)


def antisymmetrized(vector, sites):
    """Apply product_{site in sites}(I-F_site) to a sparse vector."""
    out = {}
    for word, coefficient in vector.items():
        for mask in range(1 << len(sites)):
            image = word
            sign = 1
            for bit, site in enumerate(sites):
                if (mask >> bit) & 1:
                    image = swap_replica_word(image, site)
                    sign = -sign
            out[image] = out.get(image, 0) + sign * coefficient
    return {word: value for word, value in out.items() if value}


def variation_replica_vector(x, y, coordinate, left):
    """Sparse xi tensor y or x tensor eta for one coordinate."""
    out = {}
    if left:
        left_word = WORDS[coordinate]
        for right_word, coefficient in y.items():
            out[left_word + right_word] = coefficient
    else:
        right_word = WORDS[coordinate]
        for left_word, coefficient in x.items():
            out[left_word + right_word] = coefficient
    return out


def dot_sparse(left, right):
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(key, 0) for key, value in left.items())


def hessian_times_eight(x, y):
    """Integral matrix 8 H from equation (8) of the note."""
    pair_sites = ((0, 1), (0, 2), (1, 2))
    columns = []
    for left in (True, False):
        for coordinate in range(DIMENSION):
            raw = variation_replica_vector(x, y, coordinate, left)
            pair_images = tuple(
                antisymmetrized(raw, sites) for sites in pair_sites
            )
            triple_image = antisymmetrized(raw, (0, 1, 2))
            columns.append((pair_images, triple_image))

    gram = sp.zeros(2 * DIMENSION)
    for row in range(2 * DIMENSION):
        pair_row, triple_row = columns[row]
        for column in range(row, 2 * DIMENSION):
            pair_column, triple_column = columns[column]
            value = 2 * sum(
                dot_sparse(pair_row[index], pair_column[index])
                for index in range(3)
            )
            value += dot_sparse(triple_row, triple_column)
            gram[row, column] = gram[column, row] = value
    return gram


def check_stability_equivalence():
    d1, d2, epsilon, t = sp.symbols(
        "d1 d2 epsilon t", real=True
    )
    defect = 1 - 3 * (d1**2 - d1 * d2 + d2**2)
    substitution = {1: sp.Rational(9, 4) * (d1**2 + epsilon)}
    # Replace the scalar 1 explicitly rather than using xreplace.
    rewritten = (
        sp.Rational(9, 4) * (d1**2 + epsilon)
        - 3 * (d1**2 - d1 * d2 + d2**2)
    )
    assert sp.factor(
        rewritten
        - sp.Rational(3, 4)
        * (3 * epsilon - (2 * d2 - d1) ** 2)
    ) == 0
    relation = sp.expand(
        ((2 * d2 - d1) ** 2 - 3 * epsilon).subs(
            d2, d1 * (sp.Rational(1, 2) + t)
        )
    ).subs(d1**2, sp.Rational(4, 9) - epsilon)
    threshold = sp.Rational(16) * t**2 / (27 + 36 * t**2)
    assert sp.factor(
        relation.subs(epsilon, threshold)
    ) == 0
    assert defect != 0  # Guard against an accidentally vacuous check.


def check_generic_hessians():
    x_product = {(0, 0, 0): 1}
    y_product = {
        (0, 0, 0): 1,
        (1, 0, 0): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
    }
    product_gram = hessian_times_eight(x_product, y_product)
    assert product_gram.rank() == 40
    variable = sp.symbols("lambda")
    product_characteristic = sp.factor(
        product_gram.charpoly(variable).as_expr()
    )
    expected_product = (
        variable**14
        * (variable - 32) ** 3
        * (variable - 8) ** 2
        * (variable**2 - 160 * variable + 4032)
        * (variable**2 - 40 * variable + 192) ** 3
        * (
            variable**3
            - 168 * variable**2
            + 6272 * variable
            - 38400
        )
        * (
            variable**4
            - 200 * variable**3
            + 11520 * variable**2
            - 215552 * variable
            + 942080
        )
        ** 3
        * (
            variable**4
            - 200 * variable**3
            + 12032 * variable**2
            - 264704 * variable
            + 1781760
        )
        ** 3
    )
    assert sp.expand(product_characteristic - expected_product) == 0
    # count_roots counts the distinct endpoint root at zero once; rank
    # above supplies its multiplicity fourteen.
    assert sp.Poly(product_characteristic, variable).count_roots(0, 4) == 1

    x_biseparable = {(0, 0, 0): 1, (0, 1, 1): 2}
    y_biseparable = {
        (0, 0, 0): 1,
        (0, 0, 1): 1,
        (0, 1, 0): 1,
        (0, 1, 1): -2,
    }
    biseparable_gram = hessian_times_eight(
        x_biseparable, y_biseparable
    )
    assert biseparable_gram.rank() == 41
    biseparable_characteristic = sp.factor(
        biseparable_gram.charpoly(variable).as_expr()
    )
    expected_biseparable = (
        variable**13
        * (variable - 232) ** 2
        * (variable - 152) ** 2
        * (variable - 96)
        * (variable**2 - 96 * variable + 1664) ** 5
        * (
            variable**4
            - 480 * variable**3
            + 77952 * variable**2
            - 4938240 * variable
            + 94416896
        )
        ** 4
        * (
            variable**5
            - 480 * variable**4
            + 75456 * variable**3
            - 4900864 * variable**2
            + 129196032 * variable
            - 1132462080
        )
        ** 2
    )
    assert sp.expand(
        biseparable_characteristic - expected_biseparable
    ) == 0
    assert (
        sp.Poly(biseparable_characteristic, variable).count_roots(0, 16)
        == 1
    )


def rank_one_slack(x, y):
    replica = {
        left_word + right_word: left_value * right_value
        for left_word, left_value in x.items()
        for right_word, right_value in y.items()
    }
    value = 0
    for sites in ((0, 1), (0, 2), (1, 2)):
        image = antisymmetrized(replica, sites)
        value += sp.Rational(1, 4) * dot_sparse(image, image)
    triple = antisymmetrized(replica, (0, 1, 2))
    value += sp.Rational(1, 8) * dot_sparse(triple, triple)
    return sp.factor(value)


def check_singular_intersection():
    t = sp.symbols("t", real=True)
    x0 = {(0, 0, 0): 1}
    y0 = {(1, 0, 0): 1}
    intersection_gram = hessian_times_eight(x0, y0)
    assert intersection_gram.rank() == 36

    x_curve = {(0, 0, 0): 1, (1, 0, 1): t}
    y_curve = {(1, 0, 0): 1, (0, 1, 0): t}
    assert rank_one_slack(x_curve, y_curve) == 4 * t**4
    normalized_slack = sp.factor(
        rank_one_slack(x_curve, y_curve) / (1 + t**2) ** 2
    )
    assert normalized_slack == 4 * t**4 / (1 + t**2) ** 2

    # Exact singular values at the sharp intersection.  The nonzero
    # first-site factor has singular value one.  The last-two-site
    # diagonal factor has entries (q_j+q_k)/3.
    p = (sp.Rational(1, 3),) * 3
    q = (
        sp.Rational(2, 3),
        sp.Rational(-1, 3),
        sp.Rational(-1, 3),
    )
    diagonal = sorted(
        (abs((q[j] + q[k]) / 3) for j in range(3) for k in range(3)),
        reverse=True,
    )
    assert diagonal == [
        sp.Rational(4, 9),
        sp.Rational(2, 9),
        sp.Rational(2, 9),
        sp.Rational(2, 9),
        sp.Rational(2, 9),
        sp.Rational(1, 9),
        sp.Rational(1, 9),
        sp.Rational(1, 9),
        sp.Rational(1, 9),
    ]
    assert p == (sp.Rational(1, 3),) * 3


def main():
    check_stability_equivalence()
    check_generic_hessians()
    check_singular_intersection()
    print(
        "verified: sharp stability equivalence, generic Hessian gaps, "
        "and quartic intersection obstruction"
    )


if __name__ == "__main__":
    main()
