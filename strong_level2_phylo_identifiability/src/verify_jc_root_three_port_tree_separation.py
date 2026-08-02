#!/usr/bin/env python3
"""Exact Bernstein certificates separating root trees from three-port blobs."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path

import sympy as sp

from generic_fourier_network import reticulation_vertices
from verify_jc_root_three_port_saturation import (
    enumerate_unlabelled,
    exact_generic_rank,
)


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_root_three_port_tree_separation.json"


def remove_positive_boundary_factors(polynomial, variables):
    polynomial = sp.Poly(polynomial, *variables, domain=sp.QQ)
    factors = []
    while True:
        changed = False
        for variable in variables:
            at_zero = sp.Poly(
                polynomial.as_expr().subs(variable, 0),
                *variables,
                domain=sp.QQ,
            )
            at_one = sp.Poly(
                polynomial.as_expr().subs(variable, 1),
                *variables,
                domain=sp.QQ,
            )
            if at_zero.is_zero:
                polynomial, remainder = sp.div(
                    polynomial,
                    sp.Poly(variable, *variables, domain=sp.QQ),
                )
                assert remainder.is_zero
                factors.append((str(variable), 0))
                changed = True
                break
            if at_one.is_zero:
                polynomial, remainder = sp.div(
                    polynomial,
                    sp.Poly(1 - variable, *variables, domain=sp.QQ),
                )
                assert remainder.is_zero
                factors.append((str(variable), 1))
                changed = True
                break
        if not changed:
            return polynomial, tuple(factors)


def natural_bernstein_coefficients(polynomial):
    variables = polynomial.gens
    degrees = tuple(polynomial.degree(variable) for variable in variables)
    power_terms = polynomial.terms()
    coefficients = []
    for bernstein_index in product(*(range(degree + 1) for degree in degrees)):
        coefficient = sp.Rational(0)
        for power_index, power_coefficient in power_terms:
            if not all(
                power <= bernstein
                for power, bernstein in zip(power_index, bernstein_index)
            ):
                continue
            term = power_coefficient
            for power, bernstein, degree in zip(
                power_index, bernstein_index, degrees
            ):
                term *= sp.Rational(
                    comb(bernstein, power), comb(degree, power)
                )
            coefficient += term
        coefficients.append(coefficient)
    return degrees, tuple(coefficients)


def topology_certificate(record):
    network = record["network"]
    edge_count = len(network["edges"])
    reticulation_count = len(reticulation_vertices(network["vertices"]))
    parameters = sp.symbols(f"g0:{edge_count + reticulation_count}")
    _rank, _rows, _columns, _determinant, coordinates = exact_generic_rank(
        network
    )
    r12, r13, r23, triple = coordinates
    separator = sp.factor(r12 * r13 * r23 - triple**2)

    if record["kind"] == "tree":
        assert separator == 0
        return {"kind": "tree", "separator_pullback": "0"}

    leaf_set = set(network["leaves"])
    pendant_indices = tuple(
        index
        for index, (_tail, head) in enumerate(network["edges"])
        if head in leaf_set
    )
    assert len(pendant_indices) == 3
    expanded = sp.Poly(sp.expand(separator), *parameters, domain=sp.QQ)
    minimum_pendant_exponents = tuple(
        min(monomial[index] for monomial, _coefficient in expanded.terms())
        for index in pendant_indices
    )
    assert minimum_pendant_exponents == (2, 2, 2)
    pendant_factor = sp.prod(parameters[index] ** 2 for index in pendant_indices)
    reduced = sp.factor(separator / pendant_factor)
    assert not any(reduced.has(parameters[index]) for index in pendant_indices)

    variables = tuple(
        parameter
        for index, parameter in enumerate(parameters)
        if index not in pendant_indices
    )
    residual, boundary_factors = remove_positive_boundary_factors(
        reduced, variables
    )
    degrees, coefficients = natural_bernstein_coefficients(residual)
    negative = sum(1 for coefficient in coefficients if coefficient < 0)
    zero = sum(1 for coefficient in coefficients if coefficient == 0)
    positive = sum(1 for coefficient in coefficients if coefficient > 0)
    assert negative == 0 and positive > 0
    assert min(coefficients) in (0, 1)
    assert max(coefficients) == 1

    digest = sha256(
        "|".join(str(coefficient) for coefficient in coefficients).encode()
    ).hexdigest()
    return {
        "kind": record["kind"],
        "core_index": record.get("core_index"),
        "subdivision_counts": list(record.get("counts", ())),
        "pendant_factor_exponents": list(minimum_pendant_exponents),
        "positive_open_cube_boundary_factors": [
            {"variable": variable, "boundary": boundary}
            for variable, boundary in boundary_factors
        ],
        "residual_power_terms": len(residual.terms()),
        "natural_bernstein_multidegree": list(degrees),
        "bernstein_coefficient_count": len(coefficients),
        "bernstein_negative": negative,
        "bernstein_zero": zero,
        "bernstein_positive": positive,
        "bernstein_minimum": str(min(coefficients)),
        "bernstein_maximum": str(max(coefficients)),
        "bernstein_sha256": digest,
        "separator_sign_on_complete_open_cube": "strictly positive",
    }


def generate_certificate():
    records = enumerate_unlabelled()
    certificates = [topology_certificate(record) for record in records]
    assert sum(record["kind"] == "tree" for record in certificates) == 1
    reticulate = [record for record in certificates if record["kind"] != "tree"]
    assert len(reticulate) == 7
    assert all(record["bernstein_negative"] == 0 for record in reticulate)
    assert all(record["bernstein_positive"] > 0 for record in reticulate)
    return {
        "status": {
            "ordinary_tree_vs_reticulate_open_interiors": "PROVED DISJOINT",
            "ordinary_tree_one_sided_containment": "PROVED ABSENT",
            "reticulate_one_sided_containment_in_tree": "PROVED ABSENT",
            "complete_three_port_root_bowtie_and_containment_classification": "PROVED",
        },
        "separator": "F=r12*r13*r23-u123^2",
        "tree_pullback": "F=0 identically",
        "reticulate_pullback": (
            "F is a positive pendant monomial times positive x or (1-x) "
            "boundary factors times a residual having only nonnegative "
            "natural Bernstein coefficients and at least one positive coefficient"
        ),
        "strictness_argument": (
            "every Bernstein basis function is strictly positive on the "
            "open unit cube, as is every removed factor"
        ),
        "topologies": certificates,
        "conclusion": (
            "the dimension-three ordinary-tree class and the dimension-four "
            "R3 reticulate class have disjoint complete open stochastic "
            "interiors, so neither one-sided generic containment occurs"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(json.dumps(generate_certificate(), sort_keys=True))
    if args.write_certificate:
        CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    else:
        assert certificate == json.loads(CERTIFICATE.read_text())
    print(
        json.dumps(
            {
                "status": certificate["status"],
                "separator": certificate["separator"],
                "reticulate_bernstein_counts": [
                    {
                        "kind": record["kind"],
                        "negative": record["bernstein_negative"],
                        "zero": record["bernstein_zero"],
                        "positive": record["bernstein_positive"],
                    }
                    for record in certificate["topologies"]
                    if record["kind"] != "tree"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
