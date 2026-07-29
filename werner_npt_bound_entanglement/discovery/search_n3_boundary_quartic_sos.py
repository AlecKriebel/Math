#!/usr/bin/env python3
"""Discovery-only SOS search for the flat-kernel quartic at C0.

This script needs sympy, numpy, and cvxpy.  It is not part of the exact
verification layer.  Any numerical Gram matrix found here must be
rationally reconstructed and independently checked before it is a result.
"""

from __future__ import annotations

from collections import defaultdict
import importlib.util
import os
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ANALYZER = HERE / "analyze_n3_unshifted_boundary.py"
SPEC = importlib.util.spec_from_file_location("boundary", ANALYZER)
boundary = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(boundary)


def build_quartic():
    hessian = boundary.hessian()
    kernel = boundary.kernel_basis(
        hessian, boundary.connected_components(hessian)
    )
    variables = sp.symbols(f"x0:{len(kernel)}", real=True)

    left = defaultdict(lambda: sp.Integer(0))
    right = defaultdict(lambda: sp.Integer(0))
    for number, direction in enumerate(kernel):
        for coordinate, coefficient in direction.items():
            rational = sp.Rational(coefficient.numerator, coefficient.denominator)
            for key, value in boundary.COORDINATES[coordinate][0].items():
                left[key] += rational * sp.nsimplify(value) * variables[number]
            for key, value in boundary.COORDINATES[coordinate][1].items():
                right[key] += rational * sp.nsimplify(value) * variables[number]

    def gram(frame):
        output = [[0] * 2 for _ in range(2)]
        for (row, a), x in frame.items():
            for (other_row, b), y in frame.items():
                if row == other_row:
                    output[a][b] += sp.conjugate(x) * y
        return [[sp.expand(value) for value in row] for row in output]

    def multiply_right(frame, logical):
        output = defaultdict(lambda: sp.Integer(0))
        for (row, a), value in frame.items():
            for b in range(2):
                output[row, b] += value * logical[a][b]
        return output

    def logical_product(first, second):
        return [
            [
                sp.expand(
                    sum(first[i][k] * second[k][j] for k in range(2))
                )
                for j in range(2)
            ]
            for i in range(2)
        ]

    def series(base_strings, tangent):
        base = defaultdict(lambda: sp.Integer(0))
        base[base_strings[0], 0] = 1
        base[base_strings[1], 1] = 1
        metric = gram(tangent)
        metric_squared = logical_product(metric, metric)
        return (
            base,
            tangent,
            {
                key: -value / 2
                for key, value in multiply_right(base, metric).items()
            },
            {
                key: -value / 2
                for key, value in multiply_right(tangent, metric).items()
            },
            {
                key: sp.Rational(3, 8) * value
                for key, value in multiply_right(base, metric_squared).items()
            },
        )

    def outer(first, second):
        output = defaultdict(lambda: sp.Integer(0))
        for (row, a), x in first.items():
            for (column, b), y in second.items():
                if a == b:
                    output[row, column] += x * sp.conjugate(y)
        return output

    left_series = series(boundary.U0, left)
    right_series = series(boundary.V0, right)
    matrices = []
    for degree in range(5):
        output = defaultdict(lambda: sp.Integer(0))
        for left_degree in range(degree + 1):
            for key, value in outer(
                left_series[left_degree],
                right_series[degree - left_degree],
            ).items():
                output[key] += value
        matrices.append(output)

    def pairing(first, second):
        answer = 0
        for e, x in first.items():
            for f, y in second.items():
                coefficient = boundary.unit_pairing(e, f)
                if coefficient:
                    answer += (
                        sp.conjugate(x)
                        * y
                        * sp.Rational(
                            coefficient.numerator, coefficient.denominator
                        )
                    )
        return answer

    quartic = sp.expand(
        pairing(matrices[2], matrices[2])
        + 2 * sp.re(pairing(matrices[1], matrices[3]))
        + 2 * sp.re(pairing(matrices[0], matrices[4]))
    )
    return variables, sp.Poly(quartic, *variables)


def main() -> None:
    import cvxpy as cp

    variables, polynomial = build_quartic()
    terms = dict(polynomial.terms())
    print("quartic terms", len(terms))
    adjacency = [set() for _ in variables]
    for exponent in terms:
        support = [index for index, power in enumerate(exponent) if power]
        for first in support:
            adjacency[first].update(support)
    components = []
    seen = set()
    for start in range(len(variables)):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        component = []
        while stack:
            current = stack.pop()
            component.append(current)
            for other in adjacency[current]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        components.append(component)
    print("variable component sizes", sorted(map(len, components), reverse=True))
    # Retain only quadratic monomials that divide a nonzero quartic term.
    monomials = set()
    for exponent in terms:
        support = []
        for index, power in enumerate(exponent):
            support.extend([index] * power)
        for chosen in __import__("itertools").combinations(range(4), 2):
            quadratic = [0] * len(variables)
            quadratic[support[chosen[0]]] += 1
            quadratic[support[chosen[1]]] += 1
            monomials.add(tuple(quadratic))
    monomials = sorted(monomials)
    print("quadratic monomials", len(monomials))

    term_adjacency = [set() for _ in monomials]
    for first in range(len(monomials)):
        for second in range(first, len(monomials)):
            exponent = tuple(
                a + b for a, b in zip(monomials[first], monomials[second])
            )
            if exponent in terms:
                term_adjacency[first].add(second)
                term_adjacency[second].add(first)
    term_components = []
    seen = set()
    for start in range(len(monomials)):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        component = []
        while stack:
            current = stack.pop()
            component.append(current)
            for other in term_adjacency[current]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        term_components.append(component)
    print(
        "term-sparsity component sizes",
        sorted(map(len, term_components), reverse=True)[:100],
    )
    if os.environ.get("N3_QUARTIC_ANALYZE_ONLY"):
        return

    component_of = {}
    local_index = {}
    for component_number, component in enumerate(term_components):
        for position, monomial_number in enumerate(component):
            component_of[monomial_number] = component_number
            local_index[monomial_number] = position

    by_exponent = defaultdict(list)
    for first in range(len(monomials)):
        component_number = component_of[first]
        for second in term_components[component_number]:
            if second < first:
                continue
            exponent = tuple(
                a + b for a, b in zip(monomials[first], monomials[second])
            )
            by_exponent[exponent].append(
                (
                    component_number,
                    local_index[first],
                    local_index[second],
                )
            )
    print("quartic constraints", len(by_exponent))

    grams = [
        cp.Variable((len(component), len(component)), symmetric=True)
        for component in term_components
    ]
    constraints = [gram >> 0 for gram in grams]
    for exponent, pairs in by_exponent.items():
        expression = 0
        for component_number, first, second in pairs:
            expression += (1 if first == second else 2) * grams[
                component_number
            ][first, second]
        coefficient = float(terms.get(exponent, 0))
        constraints.append(expression == coefficient)

    problem = cp.Problem(
        cp.Minimize(sum(cp.trace(gram) for gram in grams)), constraints
    )
    problem.solve(
        solver=cp.CLARABEL,
        tol_gap_abs=1e-9,
        tol_feas=1e-9,
        max_iter=500,
        verbose=True,
    )
    print("status", problem.status, "trace", problem.value)
    if all(gram.value is not None for gram in grams):
        eigenvalues = [np.linalg.eigvalsh(gram.value) for gram in grams]
        print(
            "smallest block eigenvalues",
            sorted(float(values[0]) for values in eigenvalues)[:30],
        )
        np.savez(
            "/tmp/n3_boundary_quartic_grams.npz",
            **{
                f"block_{index}": gram.value
                for index, gram in enumerate(grams)
            },
        )
        np.save(
            "/tmp/n3_boundary_quartic_monomials.npy",
            np.asarray(monomials, dtype=np.int8),
        )


if __name__ == "__main__":
    main()
