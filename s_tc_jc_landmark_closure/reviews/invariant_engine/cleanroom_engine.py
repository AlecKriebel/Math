#!/usr/bin/env python3
"""Independent exact algebra for the JC invariant-engine audit.

This module deliberately imports nothing from ``primary`` or from any
historical Fourier implementation.  The only project data accepted by the
driver are inert integer coefficient templates and descriptors.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, permutations, product
import hashlib
import math
from typing import Iterable, Sequence


Poly = dict[tuple[int, ...], int]
Descriptor = tuple[int, tuple[tuple[int, ...], ...]]
Invariant = tuple[tuple[tuple[int, ...], int], ...]


def poly_add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    answer = dict(left)
    for exponent, coefficient in right.items():
        value = answer.get(exponent, 0) + scale * coefficient
        if value:
            answer[exponent] = value
        else:
            answer.pop(exponent, None)
    return answer


def poly_mul(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return {}
    answer: dict[tuple[int, ...], int] = defaultdict(int)
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exponent, right_exponent))
            answer[exponent] += left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def poly_constant(value: int, variables: int) -> Poly:
    return {} if not value else {(0,) * variables: int(value)}


def poly_primitive(poly: Poly) -> tuple[tuple[tuple[int, ...], int], ...]:
    """Primitive representative with sign normalized by its first monomial."""
    if not poly:
        return ()
    content = 0
    for coefficient in poly.values():
        content = math.gcd(content, abs(coefficient))
    reduced = {exponent: coefficient // content for exponent, coefficient in poly.items()}
    first = min(reduced)
    if reduced[first] < 0:
        reduced = {exponent: -coefficient for exponent, coefficient in reduced.items()}
    return tuple(sorted(reduced.items()))


def exact_polynomial_hash(poly: Poly) -> str:
    return hashlib.sha256(repr(tuple(sorted(poly.items()))).encode()).hexdigest()


def primitive_polynomial_hash(poly: Poly) -> str:
    return hashlib.sha256(repr(poly_primitive(poly)).encode()).hexdigest()


def evaluate(poly: Poly, values: Sequence[Fraction]) -> Fraction:
    total = Fraction(0)
    for exponent, coefficient in poly.items():
        term = Fraction(coefficient)
        for value, power in zip(values, exponent):
            term *= value**power
        total += term
    return total


def evaluate_mod(poly: Poly, values: Sequence[int], prime: int) -> int:
    total = 0
    for exponent, coefficient in poly.items():
        term = coefficient % prime
        for value, power in zip(values, exponent):
            term = term * pow(value, power, prime) % prime
        total = (total + term) % prime
    return total


def nonzero_colour_maps() -> tuple[tuple[int, int, int, int], ...]:
    return tuple((0, *permutation) for permutation in permutations((1, 2, 3)))


def colour_canonical(row: Sequence[int]) -> tuple[int, ...]:
    return min(
        tuple(mapping[value] for value in row)
        for mapping in nonzero_colour_maps()
    )


def jc_representatives() -> tuple[tuple[int, int, int, int], ...]:
    """Derive the 15 zero-sum JC character orbits from G=(Z/2)^2."""
    representatives = {
        colour_canonical(row)
        for row in product(range(4), repeat=4)
        if row[0] ^ row[1] ^ row[2] ^ row[3] == 0
    }
    answer = tuple(sorted(representatives))
    if len(answer) != 15 or answer[0] != (0, 0, 0, 0):
        raise AssertionError(answer)
    return answer


def canonicalize_rows(reticulations: int, rows: Iterable[Sequence[int]]) -> Descriptor:
    """Quotient duplicate edge rows and reticulation labels/choice flips."""
    rows = tuple(sorted(set(tuple(row) for row in rows if any(row))))
    if not reticulations:
        return 0, rows
    displays = tuple(product((0, 1), repeat=reticulations))
    display_index = {bits: index for index, bits in enumerate(displays)}
    candidates: list[Descriptor] = []
    for permutation in permutations(range(reticulations)):
        for flips in product((0, 1), repeat=reticulations):
            moved_rows = []
            for signature in rows:
                moved = [0] * len(displays)
                for old_index, old_bits in enumerate(displays):
                    new_bits = tuple(
                        old_bits[permutation[new_index]] ^ flips[new_index]
                        for new_index in range(reticulations)
                    )
                    moved[display_index[new_bits]] = signature[old_index]
                moved_rows.append(tuple(moved))
            candidates.append((reticulations, tuple(sorted(set(moved_rows)))))
    return min(candidates)


def restrict_raw_descriptor(
    reticulations: int,
    rows: Iterable[Sequence[int]],
    ordered_positions: Sequence[int],
) -> Descriptor:
    moved_rows = []
    for row in rows:
        moved_signature = []
        for mask in row:
            new_mask = 0
            for new_position, old_position in enumerate(ordered_positions):
                if mask & (1 << old_position):
                    new_mask |= 1 << new_position
            moved_signature.append(new_mask)
        moved_rows.append(tuple(moved_signature))
    return canonicalize_rows(reticulations, moved_rows)


def all_ordered_quartet_deck_from_raw(
    total_ports: int,
    reticulations: int,
    rows: Iterable[Sequence[int]],
) -> dict[tuple[int, int, int, int], Descriptor]:
    return {
        ordered: restrict_raw_descriptor(reticulations, rows, ordered)
        for ordered in permutations(range(total_ports), 4)
    }


def coordinate_polynomials(descriptor: Descriptor) -> tuple[Poly, ...]:
    """Displayed-tree JC Fourier mixture, expanded over Z exactly."""
    reticulations, signatures = descriptor
    displays = tuple(product((0, 1), repeat=reticulations))
    variable_count = len(signatures) + reticulations
    answer: list[Poly] = []
    for assignment in jc_representatives():
        coordinate: Poly = {}
        for display_index, choices in enumerate(displays):
            exponent = [0] * variable_count
            for edge_index, signature in enumerate(signatures):
                state = 0
                mask = signature[display_index]
                for port, character in enumerate(assignment):
                    if mask & (1 << port):
                        state ^= character
                if state:
                    exponent[edge_index] = 1
            term: Poly = {tuple(exponent): 1}
            for reticulation, choice in enumerate(choices):
                variable = len(signatures) + reticulation
                linear = [0] * variable_count
                linear[variable] = 1
                factor = (
                    {tuple(linear): 1}
                    if choice == 0
                    else {(0,) * variable_count: 1, tuple(linear): -1}
                )
                term = poly_mul(term, factor)
            coordinate = poly_add(coordinate, term)
        answer.append(coordinate)
    return tuple(answer)


def coordinate_values_mod(
    descriptor: Descriptor,
    seed: int,
    prime: int = 2_147_483_647,
) -> tuple[int, ...]:
    reticulations, signatures = descriptor
    variable_count = len(signatures) + reticulations
    values = []
    for index in range(variable_count):
        value = (seed + 37 * index + 11) % prime
        values.append(2 if value in (0, 1) else value)
    return tuple(
        evaluate_mod(poly, values, prime)
        for poly in coordinate_polynomials(descriptor)
    )


def invariant_value_mod(
    coordinates: Sequence[int],
    invariant: Sequence[tuple[Sequence[int], int]],
    prime: int = 2_147_483_647,
) -> int:
    total = 0
    for monomial, coefficient in invariant:
        term = int(coefficient) % prime
        for coordinate in monomial:
            term = term * coordinates[coordinate] % prime
        total = (total + term) % prime
    return total


def pullbacks_shared(descriptor: Descriptor, invariants: Sequence[Invariant]) -> tuple[Poly, ...]:
    coordinates = coordinate_polynomials(descriptor)
    variable_count = len(descriptor[1]) + descriptor[0]
    products: dict[tuple[int, ...], Poly] = {(): poly_constant(1, variable_count)}

    def coordinate_product(indices: tuple[int, ...]) -> Poly:
        if indices not in products:
            products[indices] = poly_mul(
                coordinate_product(indices[:-1]), coordinates[indices[-1]]
            )
        return products[indices]

    answers = []
    for invariant in invariants:
        answer: Poly = {}
        for monomial, coefficient in invariant:
            answer = poly_add(answer, coordinate_product(tuple(monomial)), coefficient)
        answers.append(answer)
    return tuple(answers)


def normalize_invariant(terms: Iterable[tuple[Sequence[int], int]]) -> Invariant:
    combined: dict[tuple[int, ...], int] = defaultdict(int)
    for indices, coefficient in terms:
        combined[tuple(sorted(int(index) for index in indices))] += int(coefficient)
    answer = tuple(sorted((indices, coefficient) for indices, coefficient in combined.items() if coefficient))
    if answer and answer[0][1] < 0:
        answer = tuple((indices, -coefficient) for indices, coefficient in answer)
    return answer


def invariant_orbit(templates: Iterable[Sequence[tuple[Sequence[int], int]]]) -> tuple[Invariant, ...]:
    representatives = jc_representatives()
    representative_index = {row: index for index, row in enumerate(representatives)}
    orbit: set[Invariant] = set()
    for template in templates:
        for leaf_permutation in permutations(range(4)):
            moved_terms = []
            for monomial, coefficient in template:
                moved_monomial = []
                for coordinate in monomial:
                    assignment = representatives[int(coordinate)]
                    transported = tuple(assignment[leaf_permutation[position]] for position in range(4))
                    moved_monomial.append(representative_index[colour_canonical(transported)])
                moved_terms.append((moved_monomial, int(coefficient)))
            orbit.add(normalize_invariant(moved_terms))
    return tuple(sorted(orbit))


def arm_multidegrees(invariant: Invariant) -> set[tuple[int, int, int, int]]:
    representatives = jc_representatives()
    return {
        tuple(
            sum(representatives[index][port] != 0 for index in monomial)
            for port in range(4)
        )
        for monomial, _coefficient in invariant
    }


def trinet_F_template() -> Invariant:
    representatives = jc_representatives()
    index = {row: representatives.index(row) for row in (
        (1, 1, 0, 0),
        (1, 0, 1, 0),
        (0, 1, 1, 0),
        (1, 2, 3, 0),
    )}
    return normalize_invariant((
        ((index[(1, 1, 0, 0)], index[(1, 0, 1, 0)], index[(0, 1, 1, 0)]), 1),
        ((index[(1, 2, 3, 0)], index[(1, 2, 3, 0)]), -1),
    ))


def exhaustive_small_descriptors() -> tuple[Descriptor, ...]:
    """A finite descriptor universe defined independently of project graphs.

    It contains all reticulation-free descriptors with at most two distinct
    nonzero four-port masks, every one-row one-reticulation descriptor over
    all four-port masks, and every one-row two-reticulation descriptor whose
    displayed masks lie in {0,1,2,3}.
    """
    descriptors: set[Descriptor] = {(0, ())}
    masks = tuple(range(1, 16))
    for size in (1, 2):
        for chosen in combinations(masks, size):
            descriptors.add(canonicalize_rows(0, ((mask,) for mask in chosen)))
    for row in product(range(16), repeat=2):
        if any(row):
            descriptors.add(canonicalize_rows(1, (row,)))
    for row in product(range(4), repeat=4):
        if any(row):
            descriptors.add(canonicalize_rows(2, (row,)))
    return tuple(sorted(descriptors))


def to_sympy(poly: Poly):
    import sympy as sp

    variable_count = len(next(iter(poly))) if poly else 0
    symbols = sp.symbols(f"q0:{variable_count}")
    expression = sp.Integer(0)
    for exponents, coefficient in poly.items():
        term = sp.Integer(coefficient)
        for symbol, exponent in zip(symbols, exponents):
            term *= symbol**exponent
        expression += term
    return symbols, sp.expand(expression)


def bernstein_coefficients(expression, symbols, elevation: int):
    """Exact tensor-product Bernstein coefficients at native+elevation degree."""
    import sympy as sp

    polynomial = sp.Poly(expression, *symbols, domain=sp.QQ)
    all_degrees = tuple(int(value) for value in polynomial.degree_list())
    used = tuple(index for index, degree in enumerate(all_degrees) if degree)
    if not used:
        return used, (), (Fraction(polynomial.LC()),)
    native = tuple(all_degrees[index] for index in used)
    degrees = tuple(degree + elevation for degree in native)
    power_coefficients = {
        tuple(exponents[index] for index in used): Fraction(coefficient)
        for exponents, coefficient in polynomial.terms()
    }
    coefficients = []
    for bernstein_index in product(*(range(degree + 1) for degree in degrees)):
        value = Fraction(0)
        for powers, coefficient in power_coefficients.items():
            if all(power <= index for power, index in zip(powers, bernstein_index)):
                ratio = Fraction(1)
                for index, power, degree in zip(bernstein_index, powers, degrees):
                    ratio *= Fraction(math.comb(index, power), math.comb(degree, power))
                value += coefficient * ratio
        coefficients.append(value)
    return used, degrees, tuple(coefficients)


def bernstein_proof(expression, symbols, max_elevation: int = 3) -> dict:
    """Return the first exact Bernstein orthant proof, if one exists."""
    for elevation in range(max_elevation + 1):
        used, degrees, coefficients = bernstein_coefficients(expression, symbols, elevation)
        if all(value >= 0 for value in coefficients) and any(value > 0 for value in coefficients):
            return {
                "certified": True,
                "sign": 1,
                "used_variables": used,
                "degrees": degrees,
                "elevation": elevation,
                "coefficient_count": len(coefficients),
                "minimum": str(min(coefficients)),
                "maximum": str(max(coefficients)),
            }
        if all(value <= 0 for value in coefficients) and any(value < 0 for value in coefficients):
            return {
                "certified": True,
                "sign": -1,
                "used_variables": used,
                "degrees": degrees,
                "elevation": elevation,
                "coefficient_count": len(coefficients),
                "minimum": str(min(coefficients)),
                "maximum": str(max(coefficients)),
            }
        if not used:
            return {"certified": False}
    return {"certified": False}


def factor_bernstein_strict_sign(poly: Poly, max_elevation: int = 3) -> dict:
    """Independent factor-and-Bernstein proof with product replay."""
    import sympy as sp

    if not poly:
        return {"certified": False, "reason": "zero polynomial"}
    symbols, expression = to_sympy(poly)
    constant, factors = sp.factor_list(expression, *symbols)
    rebuilt = sp.Integer(constant)
    rows = []
    sign = 1 if constant > 0 else -1
    for factor, multiplicity in factors:
        rebuilt *= factor**multiplicity
        proof = bernstein_proof(factor, symbols, max_elevation)
        rows.append({
            "factor": str(sp.expand(factor)),
            "multiplicity": int(multiplicity),
            "proof": proof,
        })
        if not proof["certified"]:
            return {
                "certified": False,
                "factor_product_exact": sp.expand(rebuilt - expression) == 0,
                "factors": rows,
            }
        if multiplicity % 2:
            sign *= int(proof["sign"])
    if sp.expand(rebuilt - expression) != 0:
        raise AssertionError("factorization did not multiply back")
    return {
        "certified": True,
        "strict_sign": sign,
        "domain": "open_unit_cube",
        "factors": rows,
    }
