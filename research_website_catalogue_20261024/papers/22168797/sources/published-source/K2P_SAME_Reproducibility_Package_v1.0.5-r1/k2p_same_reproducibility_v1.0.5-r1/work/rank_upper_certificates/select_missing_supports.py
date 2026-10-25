#!/usr/bin/env python3
"""Select exact-point edge-kernel supports outside the base syzygy span."""

from __future__ import annotations

import json
import pickle
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix

from k2p_atlas_core import (
    default_exact_point,
    descriptor_jacobian,
    output_sparse_polynomials,
)
from syzygy_upper import coefficient_system


WORK = Path(__file__).resolve().parent


def q(value):
    value = Fraction(value)
    return sp.Rational(value.numerator, value.denominator)


def base_evaluated_vectors(desc):
    labels, _, system = coefficient_system(desc, output_sparse_polynomials)
    coefficient_kernel = DomainMatrix.from_list(system, ZZ).nullspace().to_Matrix()
    edge_pairs, lambdas = default_exact_point(desc)
    xs = tuple(value for pair in edge_pairs for value in pair)
    evars = len(xs)
    rows = []
    for parameter in range(evars + len(lambdas)):
        row = []
        for kind, index, mask in labels:
            lambda_monomial = sp.S.One
            for j, lam in enumerate(lambdas):
                if (mask >> j) & 1:
                    lambda_monomial *= q(lam)
            value = sp.S.Zero
            if kind == "edge" and parameter == index:
                value = q(xs[index]) * lambda_monomial
            elif kind == "lambda" and parameter == evars + index:
                lam = q(lambdas[index])
                value = lam * (1 - lam) * lambda_monomial
            row.append(value)
        rows.append(row)
    return sp.Matrix(rows) * coefficient_kernel.T


def main():
    with (WORK / "exception_orbit_representatives.pkl").open("rb") as handle:
        representatives = pickle.load(handle)
    data = json.loads((WORK / "exception_orbits.json").read_text())
    if len(representatives) != len(data["orbits"]):
        raise AssertionError("representative/ledger mismatch")

    for desc, row in zip(representatives, data["orbits"]):
        base = base_evaluated_vectors(desc)
        base_rank = base.rank()
        evars = 2 * desc.edge_class_count
        lambdas = desc.retic_count
        edge_kernel = sp.Matrix(
            [jacobian_row[:evars] for jacobian_row in descriptor_jacobian(desc)]
        ).nullspace()
        span = base
        chosen = []
        for vector in edge_kernel:
            padded = sp.Matrix.vstack(vector, sp.zeros(lambdas, 1))
            enlarged = sp.Matrix.hstack(span, padded)
            if enlarged.rank() > span.rank():
                support = tuple(i for i, value in enumerate(vector) if value)
                chosen.append(support)
                span = enlarged
        required = (2 * desc.edge_class_count + desc.retic_count) - row["lower_rank"]
        if span.rank() != required:
            raise AssertionError(
                (row["orbit_index"], base_rank, chosen, span.rank(), required)
            )
        row["base_evaluated_field_rank"] = base_rank
        row["selected_missing_edge_supports"] = [list(support) for support in chosen]
        row["combined_evaluated_field_rank"] = span.rank()
        print(
            f"orbit {row['orbit_index']}: base={base_rank} add={chosen} total={span.rank()}",
            flush=True,
        )
    (WORK / "exception_orbits.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
