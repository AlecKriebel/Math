#!/usr/bin/env python3
"""Numerically search for effective-quartic zero components.

Discovery only.  The exact 300 quadratic zero equations are minimized on
the unit sphere, while the distance to the known 37-dimensional
factorized tangent component is monitored.  A penalty continuation can
force the search away from that component.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "analyze_n3_boundary_effective_zero_variety.py"
SPEC = importlib.util.spec_from_file_location("zero_analysis", SOURCE)
zero_analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(zero_analysis)


def main():
    dimension, _, _, equations = zero_analysis.reconstruct()
    matrices = np.zeros((len(equations), dimension, dimension))
    for number, equation in enumerate(equations):
        for (first, second), coefficient in equation.items():
            value = float(coefficient)
            if first == second:
                matrices[number, first, second] += value
            else:
                matrices[number, first, second] += value / 2
                matrices[number, second, first] += value / 2

    factorized = zero_analysis.factorized_zero_tangent()
    factorized_matrix = np.column_stack(
        [
            np.asarray(
                [float(direction.get(index, 0)) for index in range(dimension)]
            )
            for direction in factorized
        ]
    )
    factorized_q, _ = np.linalg.qr(factorized_matrix)
    transverse_projector = (
        np.eye(dimension) - factorized_q @ factorized_q.T
    )

    def normalized(raw):
        norm = np.linalg.norm(raw)
        return raw / norm, norm

    def residual_data(x):
        residuals = np.einsum("i,aij,j->a", x, matrices, x)
        gradients = 2 * np.einsum("aij,j->ai", matrices, x)
        return residuals, gradients

    penalty = float(os.environ.get("N3_ZERO_TRANSVERSE_REWARD", "0"))

    def objective(raw):
        x, norm = normalized(raw)
        residuals, gradients = residual_data(x)
        residual_value = float(np.dot(residuals, residuals))
        ambient_gradient = 2 * residuals @ gradients
        transverse = transverse_projector @ x
        value = residual_value - penalty * float(
            np.dot(transverse, transverse)
        )
        ambient_gradient -= 2 * penalty * transverse
        tangent_gradient = (
            ambient_gradient
            - float(np.dot(ambient_gradient, x)) * x
        ) / norm
        return value, tangent_gradient

    starts = int(os.environ.get("N3_ZERO_STARTS", "100"))
    seed = int(os.environ.get("N3_ZERO_SEED", "20260729"))
    rng = np.random.default_rng(seed)
    records = []
    for start in range(starts):
        initial = rng.normal(size=dimension)
        result = minimize(
            objective,
            initial,
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": 5000, "ftol": 1e-15, "gtol": 1e-12},
        )
        x, _ = normalized(result.x)
        residuals, _ = residual_data(x)
        residual_norm = float(np.linalg.norm(residuals))
        transverse_norm = float(
            np.linalg.norm(transverse_projector @ x)
        )
        records.append((residual_norm, transverse_norm, x))
        if start < 20 or residual_norm < 1e-8 and transverse_norm > 1e-5:
            print(
                "start",
                start,
                "residual",
                f"{residual_norm:.4e}",
                "transverse",
                f"{transverse_norm:.8f}",
                "objective",
                f"{result.fun:.8e}",
                "success",
                result.success,
                flush=True,
            )
    records.sort(key=lambda record: record[0])
    print("best residual/transverse pairs")
    for residual, transverse, _ in records[:20]:
        print(f"{residual:.6e}", f"{transverse:.9f}")
    best_outside = max(
        (
            record
            for record in records
            if record[0] < 1e-8
        ),
        key=lambda record: record[1],
        default=None,
    )
    if best_outside:
        residual, transverse, x = best_outside
        print("best zero-like transverse", residual, transverse)
        print(
            "coordinates",
            [(index, float(value)) for index, value in enumerate(x) if abs(value) > 1e-6],
        )
        factor_pairs = zero_analysis.factored_linear_forms(equations, dimension)
        classification_cache = {}

        def classify_linear_component(point):
            selected = []
            for pair in factor_pairs:
                if pair is None:
                    continue
                values = [
                    abs(sum(float(a) * b for a, b in zip(row, point)))
                    for row in pair
                ]
                minimum = min(values)
                if minimum < 1e-5:
                    selected.append(pair[values.index(minimum)])
                if max(values) < 1e-5:
                    selected.extend(pair)

            normalized = {}
            for row in selected:
                pivot = next((value for value in row if value), None)
                if pivot is None:
                    continue
                row = tuple(value / pivot for value in row)
                normalized[row] = row
            import sympy as sp
            exact_rows = list(normalized)
            matrix = sp.Matrix(exact_rows)
            reduced, _ = matrix.rref()
            nonzero_rows = tuple(
                tuple(row)
                for row in reduced.tolist()
                if any(row)
            )
            if nonzero_rows in classification_cache:
                return classification_cache[nonzero_rows]
            nullspace = matrix.nullspace()
            directions = [
                {
                    index: zero_analysis.Fraction(value)
                    for index, value in enumerate(vector)
                    if value
                }
                for vector in nullspace
            ]
            exact_component = False
            if directions:
                try:
                    zero_analysis.verify_linear_zero_subspace(
                        equations, directions
                    )
                    exact_component = True
                except AssertionError:
                    pass
            result = (
                len(exact_rows),
                matrix.rank(),
                directions,
                exact_component,
                nonzero_rows,
            )
            classification_cache[nonzero_rows] = result
            return result

        (
            selected_count,
            rank,
            directions,
            exact_component,
            nonzero_rows,
        ) = classify_linear_component(x)
        print(
            "selected vanishing linear factors",
            selected_count,
            "rank",
            rank,
            "nullity",
            len(directions),
            "exact zero component",
            exact_component,
        )
        if exact_component:
            print("exact linear equations")
            for row in nonzero_rows:
                print(
                    [
                        (index, str(value))
                        for index, value in enumerate(row)
                        if value
                    ]
                )

        components = {}
        unclassified = []
        for residual, transverse, point in records:
            if residual >= 1e-7:
                continue
            classification = classify_linear_component(point)
            signature = classification[-1]
            if classification[-2]:
                components.setdefault(signature, []).append(
                    (residual, transverse)
                )
            else:
                unclassified.append((residual, transverse))
        print(
            "distinct exact linear components reached",
            len(components),
            "unclassified zero-like endpoints",
            len(unclassified),
        )
        for number, (signature, members) in enumerate(components.items()):
            print(
                "component",
                number,
                "rank",
                len(signature),
                "hits",
                len(members),
                "max transverse",
                max(value[1] for value in members),
            )
            print(
                " equations",
                [
                    [
                        (index, str(value))
                        for index, value in enumerate(row)
                        if value
                    ]
                    for row in signature
                ],
            )


if __name__ == "__main__":
    main()
