"""Finite-field discovery of low-degree Fourier invariants.

The output is not itself a certificate.  Candidate relations must be lifted to
Q and substituted symbolically into the exact parameterizations.
"""

from __future__ import annotations

import argparse
import random
from itertools import combinations_with_replacement

import sympy as sp
from flint import nmod_mat

from fourier_models import source_parameterization, target_parameterization


def unique_coordinate_representatives(coordinates):
    representatives = []
    seen = set()
    for assignment, expression in coordinates.items():
        key = sp.srepr(sp.expand(expression))
        if key not in seen:
            seen.add(key)
            representatives.append(assignment)
    return representatives


def compiled_polynomials(expressions, parameters):
    result = []
    for expression in expressions:
        terms = []
        for monomial, coefficient in sp.Poly(sp.expand(expression), *parameters).terms():
            coefficient = int(coefficient)
            terms.append((monomial, coefficient))
        result.append(terms)
    return result


def evaluate_compiled(polynomials, values, prime):
    powers = []
    for value in values:
        powers.append((1, value % prime, value * value % prime))
    outputs = []
    for polynomial in polynomials:
        total = 0
        for monomial, coefficient in polynomial:
            term = coefficient % prime
            for index, exponent in enumerate(monomial):
                if exponent:
                    if exponent < len(powers[index]):
                        term = term * powers[index][exponent] % prime
                    else:
                        term = term * pow(values[index], exponent, prime) % prime
            total = (total + term) % prime
        outputs.append(total)
    return outputs


def feature_index(count, degree):
    if degree != 2:
        raise NotImplementedError("currently degree 2 only")
    return list(combinations_with_replacement(range(count), 2))


def feature_values(coordinates, features, prime):
    return [coordinates[i] * coordinates[j] % prime for i, j in features]


def random_row(compiled, parameter_count, features, prime, rng):
    values = [rng.randrange(1, prime) for _ in range(parameter_count)]
    coordinates = evaluate_compiled(compiled, values, prime)
    return feature_values(coordinates, features, prime)


def centered(value, prime):
    value = int(value)
    return value if value <= prime // 2 else value - prime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=("K2P", "K3P"))
    parser.add_argument("--samples", type=int, default=700)
    parser.add_argument("--prime", type=int, default=65521)
    parser.add_argument("--seed", type=int, default=20260801)
    parser.add_argument("--show", type=int, default=20)
    args = parser.parse_args()

    source, source_parameters = source_parameterization(args.model, "")
    target, target_parameters = target_parameterization(args.model, "")
    representatives = unique_coordinate_representatives(source)
    source_compiled = compiled_polynomials(
        [source[g] for g in representatives], source_parameters
    )
    target_compiled = compiled_polynomials(
        [target[g] for g in representatives], target_parameters
    )
    features = feature_index(len(representatives), 2)
    rng = random.Random(args.seed)

    source_rows = [
        random_row(
            source_compiled, len(source_parameters), features, args.prime, rng
        )
        for _ in range(args.samples)
    ]
    matrix = nmod_mat(source_rows, args.prime)
    rank = matrix.rank()
    nullspace, nullity = matrix.nullspace()
    print(
        "model", args.model,
        "coordinates", len(representatives),
        "features", len(features),
        "samples", args.samples,
        "rank", rank,
        "nullity", nullity,
    )

    target_rows = [
        random_row(
            target_compiled, len(target_parameters), features, args.prime, rng
        )
        for _ in range(4)
    ]
    candidates = []
    for column in range(nullity):
        coefficients = [int(nullspace[row, column]) for row in range(len(features))]
        values = [
            sum(c * x for c, x in zip(coefficients, target_row)) % args.prime
            for target_row in target_rows
        ]
        if any(values):
            support = [(i, centered(c, args.prime)) for i, c in enumerate(coefficients) if c]
            height = max(abs(c) for _, c in support)
            candidates.append((len(support), height, values, support))

    candidates.sort(key=lambda item: (item[0], item[1]))
    print("distinguishing_nullspace_basis_vectors", len(candidates))
    for support_size, height, values, support in candidates[: args.show]:
        print("candidate", "support", support_size, "height", height, "target", values)
        for index, coefficient in support:
            i, j = features[index]
            print(" ", coefficient, representatives[i], representatives[j])


if __name__ == "__main__":
    main()

