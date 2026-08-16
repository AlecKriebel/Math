"""Search multihomogeneous low-degree invariants over a finite field.

Pendant-edge scaling gives one grading component for every leaf and every
nonzero character class.  Splitting the monomial search by this grading makes
cubic and quartic invariant discovery tractable.  Reported modular candidates
remain conjectural until exact symbolic substitution succeeds.
"""

from __future__ import annotations

import argparse
import random
from collections import defaultdict
from itertools import combinations_with_replacement

from flint import nmod_mat

from fourier_models import source_parameterization, target_parameterization
from search_low_degree_invariants import (
    centered,
    compiled_polynomials,
    evaluate_compiled,
    unique_coordinate_representatives,
)


def character_class(model: str, character: int) -> int | None:
    if character == 0:
        return None
    if model == "K2P":
        return 0 if character == 1 else 1
    if model == "K3P":
        return character - 1
    raise ValueError(model)


def coordinate_degree(model: str, assignment):
    classes = 2 if model == "K2P" else 3
    degree = [0] * (4 * classes)
    for leaf, character in enumerate(assignment):
        cls = character_class(model, character)
        if cls is not None:
            degree[leaf * classes + cls] += 1
    return tuple(degree)


def monomial_degree(coordinate_degrees, monomial):
    return tuple(
        sum(coordinate_degrees[index][component] for index in monomial)
        for component in range(len(coordinate_degrees[0]))
    )


def monomial_value(row, monomial, prime):
    value = 1
    for index in monomial:
        value = value * row[index] % prime
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=("K2P", "K3P"))
    parser.add_argument("degree", type=int)
    parser.add_argument("--prime", type=int, default=65521)
    parser.add_argument("--seed", type=int, default=20260801)
    parser.add_argument("--show", type=int, default=30)
    args = parser.parse_args()

    source, source_parameters = source_parameterization(args.model, "")
    target, target_parameters = target_parameterization(args.model, "")
    representatives = unique_coordinate_representatives(source)
    coordinate_degrees = [coordinate_degree(args.model, g) for g in representatives]
    source_compiled = compiled_polynomials(
        [source[g] for g in representatives], source_parameters
    )
    target_compiled = compiled_polynomials(
        [target[g] for g in representatives], target_parameters
    )

    buckets = defaultdict(list)
    for monomial in combinations_with_replacement(range(len(representatives)), args.degree):
        buckets[monomial_degree(coordinate_degrees, monomial)].append(monomial)
    maximum = max(map(len, buckets.values()))
    print(
        "model", args.model,
        "degree", args.degree,
        "coordinates", len(representatives),
        "monomials", sum(map(len, buckets.values())),
        "multidegrees", len(buckets),
        "max_bucket", maximum,
    )

    rng = random.Random(args.seed)
    sample_count = maximum + 12
    source_rows = []
    target_rows = []
    for _ in range(sample_count):
        values = [rng.randrange(1, args.prime) for _ in source_parameters]
        source_rows.append(evaluate_compiled(source_compiled, values, args.prime))
        values = [rng.randrange(1, args.prime) for _ in target_parameters]
        target_rows.append(evaluate_compiled(target_compiled, values, args.prime))

    candidates = []
    total_source_nullity = 0
    distinguishing_multidegrees = 0
    for multidegree, monomials in buckets.items():
        if len(monomials) == 1:
            continue
        source_matrix = nmod_mat(
            [
                [monomial_value(row, monomial, args.prime) for monomial in monomials]
                for row in source_rows[: len(monomials) + 4]
            ],
            args.prime,
        )
        nullspace, nullity = source_matrix.nullspace()
        total_source_nullity += nullity
        if not nullity:
            continue
        found_here = False
        for column in range(nullity):
            coefficients = [int(nullspace[row, column]) for row in range(len(monomials))]
            target_values = []
            for row in target_rows:
                value = sum(
                    coefficient * monomial_value(row, monomial, args.prime)
                    for coefficient, monomial in zip(coefficients, monomials)
                ) % args.prime
                target_values.append(value)
            if any(target_values):
                found_here = True
                support = [
                    (monomial, centered(coefficient, args.prime))
                    for monomial, coefficient in zip(monomials, coefficients)
                    if coefficient
                ]
                height = max(abs(coefficient) for _, coefficient in support)
                candidates.append(
                    (
                        len(support),
                        height,
                        multidegree,
                        target_values[:4],
                        support,
                    )
                )
        distinguishing_multidegrees += int(found_here)

    candidates.sort(key=lambda item: (item[0], item[1]))
    print(
        "total_source_nullity", total_source_nullity,
        "distinguishing_multidegrees", distinguishing_multidegrees,
        "distinguishing_basis_vectors", len(candidates),
    )
    for support_size, height, multidegree, values, support in candidates[: args.show]:
        print(
            "candidate",
            "support", support_size,
            "height", height,
            "multidegree", multidegree,
            "target", values,
        )
        for monomial, coefficient in support:
            print(" ", coefficient, tuple(representatives[index] for index in monomial))


if __name__ == "__main__":
    main()

