#!/usr/bin/env python3
"""Exact verifier for the restrictable four-strand obstruction.

The calculation is independent of any Pauli or Gaussian matrix ansatz.
It constructs H_4 in its permutation basis, derives the unique Markov
trace from cyclicity and the Markov rule, checks the one-dimensional
central idempotents, and verifies the operator-word expansion of the
full mixed-color braid equations.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import permutations

import sympy as sp


Permutation = tuple[int, ...]
Element = dict[Permutation, sp.Expr]
WordPolynomial = dict[tuple[str, ...], int]


def inversion_count(permutation: Permutation) -> int:
    return sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )


def right_simple(permutation: Permutation, index: int) -> Permutation:
    result = list(permutation)
    result[index], result[index + 1] = result[index + 1], result[index]
    return tuple(result)


def left_simple(permutation: Permutation, index: int) -> Permutation:
    return tuple(
        index + 1
        if value == index
        else index
        if value == index + 1
        else value
        for value in permutation
    )


def generator_product(
    permutation: Permutation,
    index: int,
    side: str,
    q_symbol: sp.Expr,
) -> Element:
    adjacent = (
        right_simple(permutation, index)
        if side == "right"
        else left_simple(permutation, index)
    )
    if inversion_count(adjacent) > inversion_count(permutation):
        return {adjacent: sp.Integer(1)}
    return {
        permutation: q_symbol - 1,
        adjacent: q_symbol,
    }


def add_elements(*elements: Element) -> Element:
    result: defaultdict[Permutation, sp.Expr] = defaultdict(
        lambda: sp.Integer(0)
    )
    for element in elements:
        for permutation, coefficient in element.items():
            result[permutation] += coefficient
    return {
        permutation: sp.expand(coefficient)
        for permutation, coefficient in result.items()
        if sp.expand(coefficient) != 0
    }


def scale_element(element: Element, scalar: sp.Expr) -> Element:
    return {
        permutation: sp.expand(scalar * coefficient)
        for permutation, coefficient in element.items()
    }


def multiply_generator_element(
    element: Element,
    index: int,
    side: str,
    q_symbol: sp.Expr,
) -> Element:
    terms = []
    for permutation, coefficient in element.items():
        product = generator_product(permutation, index, side, q_symbol)
        terms.append(scale_element(product, coefficient))
    return add_elements(*terms)


def reduced_word(permutation: Permutation) -> list[int]:
    """Return indices whose right multiplication builds permutation."""

    work = list(range(len(permutation)))
    word: list[int] = []
    for target_position, target_value in enumerate(permutation):
        current_position = work.index(target_value)
        while current_position > target_position:
            index = current_position - 1
            work[index], work[index + 1] = work[index + 1], work[index]
            word.append(index)
            current_position -= 1
    # The swaps above send identity to permutation by left-to-right action.
    return word


def multiply_elements(
    first: Element,
    second: Element,
    q_symbol: sp.Expr,
) -> Element:
    result: Element = {}
    for left_permutation, left_coefficient in first.items():
        for right_permutation, right_coefficient in second.items():
            term: Element = {left_permutation: left_coefficient}
            for index in reduced_word(right_permutation):
                term = multiply_generator_element(
                    term, index, "right", q_symbol
                )
            term = scale_element(term, right_coefficient)
            result = add_elements(result, term)
    return result


def simplify_element_mod_root(element: Element, q_symbol: sp.Symbol) -> Element:
    relation = sp.Poly(q_symbol**2 - q_symbol + 1, q_symbol)
    simplified: Element = {}
    for permutation, coefficient in element.items():
        numerator, denominator = sp.cancel(coefficient).as_numer_denom()
        numerator = sp.rem(sp.Poly(numerator, q_symbol), relation).as_expr()
        denominator = sp.rem(
            sp.Poly(denominator, q_symbol), relation
        ).as_expr()
        value = sp.cancel(numerator / denominator)
        if value != 0:
            simplified[permutation] = value
    return simplified


def construct_idempotents(q_symbol: sp.Symbol) -> tuple[Element, Element]:
    basis = list(permutations(range(4)))
    plus_numerator = {
        permutation: sp.Integer(1) for permutation in basis
    }
    minus_numerator = {
        permutation: (-q_symbol ** -1) ** inversion_count(permutation)
        for permutation in basis
    }
    plus_normalizer = sum(
        q_symbol ** inversion_count(permutation) for permutation in basis
    )
    minus_normalizer = sum(
        q_symbol ** (-inversion_count(permutation)) for permutation in basis
    )
    return (
        scale_element(plus_numerator, 1 / plus_normalizer),
        scale_element(minus_numerator, 1 / minus_normalizer),
    )


def check_idempotents() -> None:
    q_symbol = sp.symbols("q", nonzero=True)
    plus, minus = construct_idempotents(q_symbol)

    for index in range(3):
        for side in ("left", "right"):
            plus_product = multiply_generator_element(
                plus, index, side, q_symbol
            )
            minus_product = multiply_generator_element(
                minus, index, side, q_symbol
            )
            assert all(
                sp.factor(
                    plus_product.get(permutation, 0)
                    - q_symbol * plus.get(permutation, 0)
                )
                == 0
                for permutation in set(plus_product) | set(plus)
            )
            assert all(
                sp.factor(
                    minus_product.get(permutation, 0)
                    + minus.get(permutation, 0)
                )
                == 0
                for permutation in set(minus_product) | set(minus)
            )

    plus_square = multiply_elements(plus, plus, q_symbol)
    minus_square = multiply_elements(minus, minus, q_symbol)
    assert all(
        sp.factor(
            plus_square.get(permutation, 0) - plus.get(permutation, 0)
        )
        == 0
        for permutation in set(plus_square) | set(plus)
    )
    assert all(
        sp.factor(
            minus_square.get(permutation, 0) - minus.get(permutation, 0)
        )
        == 0
        for permutation in set(minus_square) | set(minus)
    )


def markov_trace_basis(
    maximum_strands: int,
    q_symbol: sp.Symbol,
    z_symbol: sp.Symbol,
) -> dict[Permutation, sp.Expr]:
    previous: dict[Permutation, sp.Expr] = {(0,): sp.Integer(1)}

    for strands in range(2, maximum_strands + 1):
        basis = list(permutations(range(strands)))
        positions = {
            permutation: position
            for position, permutation in enumerate(basis)
        }
        variables = sp.symbols(f"t{strands}_0:{len(basis)}")
        equations: list[sp.Expr] = []

        for old_permutation, old_trace in previous.items():
            embedded = tuple(old_permutation) + (strands - 1,)
            equations.append(
                variables[positions[embedded]] - old_trace
            )
            marked = right_simple(embedded, strands - 2)
            equations.append(
                variables[positions[marked]] - z_symbol * old_trace
            )

        for permutation in basis:
            for index in range(strands - 1):
                left = generator_product(
                    permutation, index, "left", q_symbol
                )
                right = generator_product(
                    permutation, index, "right", q_symbol
                )
                equations.append(
                    sum(
                        coefficient * variables[positions[term]]
                        for term, coefficient in left.items()
                    )
                    - sum(
                        coefficient * variables[positions[term]]
                        for term, coefficient in right.items()
                    )
                )

        solution_set = sp.linsolve(equations, variables)
        solutions = list(solution_set)
        assert len(solutions) == 1
        solution = solutions[0]
        allowed_symbols = {q_symbol, z_symbol}
        assert not (
            set().union(*(value.free_symbols for value in solution))
            - allowed_symbols
        )
        previous = {
            permutation: sp.factor(solution[positions[permutation]])
            for permutation in basis
        }

    return previous


def trace_element(
    element: Element,
    basis_trace: dict[Permutation, sp.Expr],
) -> sp.Expr:
    return sp.factor(
        sum(
            coefficient * basis_trace[permutation]
            for permutation, coefficient in element.items()
        )
    )


def reduce_at_sixth_root(expression: sp.Expr, q_symbol: sp.Symbol) -> sp.Expr:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    relation = sp.Poly(q_symbol**2 - q_symbol + 1, q_symbol)
    numerator_remainder = sp.rem(
        sp.Poly(numerator, q_symbol), relation
    ).as_expr()
    denominator_remainder = sp.rem(
        sp.Poly(denominator, q_symbol), relation
    ).as_expr()
    return sp.cancel(numerator_remainder / denominator_remainder)


def check_markov_traces() -> None:
    q_symbol, z_symbol, eta_symbol = sp.symbols(
        "q z eta", nonzero=True
    )
    traces = markov_trace_basis(4, q_symbol, z_symbol)
    plus, minus = construct_idempotents(q_symbol)
    plus_trace = trace_element(plus, traces)
    minus_trace = trace_element(minus, traces)

    denominator = (
        (q_symbol + 1) ** 2
        * (q_symbol**2 + 1)
        * (q_symbol**2 + q_symbol + 1)
    )
    expected_plus = (
        (z_symbol + 1)
        * ((q_symbol + 1) * z_symbol + 1)
        * ((q_symbol**2 + q_symbol + 1) * z_symbol + 1)
        / denominator
    )
    expected_minus = -(
        (z_symbol - q_symbol)
        * ((q_symbol + 1) * z_symbol - q_symbol**2)
        * (
            (q_symbol**2 + q_symbol + 1) * z_symbol
            - q_symbol**3
        )
        / denominator
    )
    assert sp.factor(plus_trace - expected_plus) == 0
    assert sp.factor(minus_trace - expected_minus) == 0

    z_eta = q_symbol - (1 + q_symbol) * eta_symbol
    plus_eta = reduce_at_sixth_root(
        plus_trace.subs(z_symbol, z_eta), q_symbol
    )
    minus_eta = reduce_at_sixth_root(
        minus_trace.subs(z_symbol, z_eta), q_symbol
    )
    expected_plus_eta = (
        (1 - eta_symbol)
        * (2 - 3 * eta_symbol)
        * (1 - 2 * eta_symbol)
        / 2
    )
    expected_minus_eta = (
        eta_symbol
        * (3 * eta_symbol - 1)
        * (2 * eta_symbol - 1)
        / 2
    )
    assert sp.factor(plus_eta - expected_plus_eta) == 0
    assert sp.factor(minus_eta - expected_minus_eta) == 0
    assert sp.gcd(
        sp.Poly(expected_plus_eta, eta_symbol),
        sp.Poly(expected_minus_eta, eta_symbol),
    ).monic() == sp.Poly(
        eta_symbol - sp.Rational(1, 2), eta_symbol
    )

    expected_table = {
        Fraction(0, 1): (Fraction(1, 1), Fraction(0, 1)),
        Fraction(1, 3): (Fraction(1, 9), Fraction(0, 1)),
        Fraction(1, 2): (Fraction(0, 1), Fraction(0, 1)),
        Fraction(2, 3): (Fraction(0, 1), Fraction(1, 9)),
        Fraction(1, 1): (Fraction(0, 1), Fraction(1, 1)),
    }
    for eta, expected in expected_table.items():
        z_value = q_symbol - (1 + q_symbol) * sp.Rational(
            eta.numerator, eta.denominator
        )
        actual = (
            reduce_at_sixth_root(
                plus_trace.subs(z_symbol, z_value), q_symbol
            ),
            reduce_at_sixth_root(
                minus_trace.subs(z_symbol, z_value), q_symbol
            ),
        )
        expected_sympy = tuple(
            sp.Rational(value.numerator, value.denominator)
            for value in expected
        )
        assert actual == expected_sympy


def word_add(*polynomials: WordPolynomial) -> WordPolynomial:
    result: defaultdict[tuple[str, ...], int] = defaultdict(int)
    for polynomial in polynomials:
        for word, coefficient in polynomial.items():
            result[word] += coefficient
    return {
        word: coefficient
        for word, coefficient in result.items()
        if coefficient
    }


def word_scale(
    polynomial: WordPolynomial, coefficient: int
) -> WordPolynomial:
    return {
        word: coefficient * value for word, value in polynomial.items()
    }


def word_multiply(
    first: WordPolynomial, second: WordPolynomial
) -> WordPolynomial:
    result: defaultdict[tuple[str, ...], int] = defaultdict(int)
    for left_word, left_coefficient in first.items():
        for right_word, right_coefficient in second.items():
            result[left_word + right_word] += (
                left_coefficient * right_coefficient
            )
    return dict(result)


def atom(name: str) -> WordPolynomial:
    return {(name,): 1}


def zero() -> WordPolynomial:
    return {}


def block_multiply(
    first: list[list[WordPolynomial]],
    second: list[list[WordPolynomial]],
) -> list[list[WordPolynomial]]:
    size = len(first)
    return [
        [
            word_add(
                *(
                    word_multiply(first[row][middle], second[middle][column])
                    for middle in range(size)
                )
            )
            for column in range(size)
        ]
        for row in range(size)
    ]


def polynomial(*words: tuple[int, tuple[str, ...]]) -> WordPolynomial:
    return {word: coefficient for coefficient, word in words}


def check_mixed_block_equations() -> None:
    names = {
        name: atom(name)
        for name in (
            "D",
            "A",
            "B",
            "C",
            "E",
            "x",
            "y",
            "z",
            "u",
            "F",
        )
    }
    D, A, B, C, E = (names[name] for name in ("D", "A", "B", "C", "E"))
    x, y, z, u, F = (names[name] for name in ("x", "y", "z", "u", "F"))
    O = zero()
    left = [[D, O, O], [O, A, B], [O, C, E]]
    middle = [[x, y, O], [z, u, O], [O, O, F]]
    lml = block_multiply(block_multiply(left, middle), left)
    mlm = block_multiply(block_multiply(middle, left), middle)

    expected_left = [
        [
            polynomial((1, ("D", "x", "D"))),
            polynomial((1, ("D", "y", "A"))),
            polynomial((1, ("D", "y", "B"))),
        ],
        [
            polynomial((1, ("A", "z", "D"))),
            polynomial(
                (1, ("A", "u", "A")),
                (1, ("B", "F", "C")),
            ),
            polynomial(
                (1, ("A", "u", "B")),
                (1, ("B", "F", "E")),
            ),
        ],
        [
            polynomial((1, ("C", "z", "D"))),
            polynomial(
                (1, ("C", "u", "A")),
                (1, ("E", "F", "C")),
            ),
            polynomial(
                (1, ("C", "u", "B")),
                (1, ("E", "F", "E")),
            ),
        ],
    ]
    expected_right = [
        [
            polynomial(
                (1, ("x", "D", "x")),
                (1, ("y", "A", "z")),
            ),
            polynomial(
                (1, ("x", "D", "y")),
                (1, ("y", "A", "u")),
            ),
            polynomial((1, ("y", "B", "F"))),
        ],
        [
            polynomial(
                (1, ("z", "D", "x")),
                (1, ("u", "A", "z")),
            ),
            polynomial(
                (1, ("z", "D", "y")),
                (1, ("u", "A", "u")),
            ),
            polynomial((1, ("u", "B", "F"))),
        ],
        [
            polynomial((1, ("F", "C", "z"))),
            polynomial((1, ("F", "C", "u"))),
            polynomial((1, ("F", "E", "F"))),
        ],
    ]
    assert lml == expected_left
    assert mlm == expected_right


def check_dimension_arithmetic() -> None:
    # Rank choices before the four-strand obstruction.
    diagonal_ranks = (0, 3, 6, 9)
    branches = [
        (rank, 18 - 2 * rank) for rank in diagonal_ranks
    ]
    assert branches == [(0, 18), (3, 12), (6, 6), (9, 0)]

    # A restrictable split in dimension 6 has even summands after the
    # theorem, hence it is 2+4; dimension 2 is known empty.
    even_splits_six = [
        (rank, 6 - rank)
        for rank in range(1, 6)
        if rank % 2 == 0 and (6 - rank) % 2 == 0
    ]
    assert even_splits_six == [(2, 4), (4, 2)]

    # In every proper even split of d=2 mod 4, exactly one summand is
    # again 2 mod 4.
    audited = 0
    for dimension in range(6, 203, 4):
        for rank in range(2, dimension, 2):
            complement = dimension - rank
            assert (
                (rank % 4 == 2) + (complement % 4 == 2)
            ) == 1
            audited += 1
    assert audited > 0


def main() -> None:
    check_idempotents()
    print("four-strand q-symmetrizer and q-antisymmetrizer: exact")

    check_markov_traces()
    print("arbitrary-eta trace factorizations and unique common zero: exact")
    print("Markov trace table at eta=0,1/3,1/2,2/3,1: exact")

    check_mixed_block_equations()
    print("nine arbitrary operator-valued mixed-color equations: exact")

    check_dimension_arithmetic()
    print("restrictable d=6 and d=2 mod 4 descent arithmetic: exact")
    print("PASS")


if __name__ == "__main__":
    main()
