#!/usr/bin/env python3
"""Exact polynomial-vector-field rank upper certificates.

This is the small, self-contained rank-upper engine used by the theta2
five-port closure.  For edge-sector parameters ``x_i`` and inheritance
parameters ``l_j`` it searches the polynomial vector fields

    V(x_i) = x_i A_i(l),
    V(l_j) = l_j(1-l_j) C_j(l without l_j),

with multilinear A and C.  Coefficientwise expansion of ``J_f V = 0`` is an
integer linear system.  Exact evaluation of its kernel at an interior
rational point certifies the generic fibre dimension and hence a rank upper
bound.  No sampled Jacobian is used for the upper bound.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import gcd


def _lcm(a: int, b: int) -> int:
    return abs(a // gcd(a, b) * b) if a and b else 0


def ansatz_layout(desc):
    evars = 2 * desc.edge_class_count
    r = desc.retic_count
    labels = []
    for i in range(evars):
        for mask in range(1 << r):
            labels.append(("edge", i, mask))
    for j in range(r):
        for mask in range(1 << r):
            if not (mask >> j) & 1:
                labels.append(("lambda", j, mask))
    return tuple(labels)


def coefficient_system(desc, output_sparse_polynomials):
    labels = ansatz_layout(desc)
    column = {label: index for index, label in enumerate(labels)}
    evars = 2 * desc.edge_class_count
    r = desc.retic_count
    constraints = defaultdict(lambda: defaultdict(int))
    for output_index, polynomial in enumerate(output_sparse_polynomials(desc)):
        for exponent, coefficient in polynomial.items():
            exponent = tuple(exponent)
            for i in range(evars):
                power = exponent[i]
                if not power:
                    continue
                for mask in range(1 << r):
                    out_exp = list(exponent)
                    for j in range(r):
                        if (mask >> j) & 1:
                            out_exp[evars + j] += 1
                    constraints[(output_index, tuple(out_exp))][
                        column[("edge", i, mask)]
                    ] += coefficient * power
            for j in range(r):
                position = evars + j
                power = exponent[position]
                if not power:
                    continue
                for mask in range(1 << r):
                    if (mask >> j) & 1:
                        continue
                    base = list(exponent)
                    for q in range(r):
                        if (mask >> q) & 1:
                            base[evars + q] += 1
                    constraints[(output_index, tuple(base))][
                        column[("lambda", j, mask)]
                    ] += coefficient * power
                    raised = list(base)
                    raised[position] += 1
                    constraints[(output_index, tuple(raised))][
                        column[("lambda", j, mask)]
                    ] -= coefficient * power
    rows = []
    row_labels = []
    for key in sorted(constraints):
        sparse = constraints[key]
        row = [sparse.get(i, 0) for i in range(len(labels))]
        if any(row):
            row_labels.append(key)
            rows.append(row)
    return tuple(labels), tuple(row_labels), rows


def evaluation_rows(desc, labels, edge_pairs, lambdas):
    evars = 2 * desc.edge_class_count
    parameter_count = evars + desc.retic_count
    xs = tuple(value for pair in edge_pairs for value in pair)
    rows = []
    for parameter in range(parameter_count):
        values = []
        for kind, index, mask in labels:
            monomial = Fraction(1)
            for j, inheritance in enumerate(lambdas):
                if (mask >> j) & 1:
                    monomial *= inheritance
            value = Fraction(0)
            if kind == "edge" and parameter == index:
                value = xs[index] * monomial
            elif kind == "lambda" and parameter == evars + index:
                inheritance = lambdas[index]
                value = inheritance * (1 - inheritance) * monomial
            values.append(value)
        denominator = 1
        for value in values:
            denominator = _lcm(denominator, value.denominator)
        rows.append([int(value * denominator) for value in values])
    return rows


def exact_integer_rank(rows):
    if not rows:
        return 0
    from sympy import ZZ
    from sympy.polys.matrices import DomainMatrix

    return int(DomainMatrix.from_list(rows, ZZ).rank())


def upper_certificate(desc, output_sparse_polynomials, default_exact_point):
    labels, row_labels, system = coefficient_system(
        desc, output_sparse_polynomials
    )
    edge_pairs, lambdas = default_exact_point(desc)
    evaluation = evaluation_rows(desc, labels, edge_pairs, lambdas)
    rank_system = exact_integer_rank(system)
    rank_stacked = exact_integer_rank(system + evaluation)
    independent_kernel_fields = rank_stacked - rank_system
    parameter_count = 2 * desc.edge_class_count + desc.retic_count
    return {
        "parameter_count": parameter_count,
        "unknown_coefficient_count": len(labels),
        "coefficient_equation_count": len(system),
        "coefficient_system_rank": rank_system,
        "stacked_system_rank": rank_stacked,
        "independent_kernel_fields": independent_kernel_fields,
        "certified_rank_upper": parameter_count - independent_kernel_fields,
        "row_label_count": len(row_labels),
    }
