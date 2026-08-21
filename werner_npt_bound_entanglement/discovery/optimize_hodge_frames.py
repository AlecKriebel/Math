#!/usr/bin/env python3
"""Discovery optimizer for local Hodge frames.

For a rank-two code U=(u,v), define the three 3^4 tensors

    A_k = u^T B_k u,  B_k = u^T B_k v,  C_k = v^T B_k v,

where B_k=L_{k1} tensor ... tensor L_{k4}.  A local physical unitary
acts on each Hodge label by a unitary 3-by-3 matrix (up to one irrelevant
phase).  This file therefore optimizes

    sum_k |A_k C_k-B_k^2|

using only the three 81-entry tensors.  It contains:

* exact construction of the balanced graph-code tensors in floating point;
* extraction from a saved 81-by-2 frame;
* analytic Euclidean and Riemannian gradients for one local U(3);
* Armijo ascent with QR retraction;
* multistart cyclic coordinate ascent over U(3)^4;
* a finite-difference gradient self-test.

All optimization output is discovery evidence, not an exact certificate.
"""

from __future__ import annotations

import argparse
import cmath
import math
import random
from typing import Iterable


ComplexVector = list[complex]
Matrix = list[list[complex]]
HodgeTensors = tuple[ComplexVector, ComplexVector, ComplexVector]

WORDS = [
    (a, b, c, d)
    for a in range(3)
    for b in range(3)
    for c in range(3)
    for d in range(3)
]
INDEX = {word: index for index, word in enumerate(WORDS)}


def epsilon(k: int, a: int, b: int) -> int:
    if len({k, a, b}) < 3:
        return 0
    permutation = (k, a, b)
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions & 1 else 1


def hodge_maps() -> list[list[tuple[int, int]]]:
    maps: list[list[tuple[int, int]]] = []
    for labels in WORDS:
        local_map: list[tuple[int, int]] = []
        for word in WORDS:
            output = [0] * 4
            coefficient = 1
            for site in range(4):
                found = False
                for value in range(3):
                    sign = epsilon(labels[site], value, word[site])
                    if sign:
                        output[site] = value
                        coefficient *= sign
                        found = True
                        break
                if not found:
                    coefficient = 0
                    break
            local_map.append(
                (INDEX[tuple(output)] if coefficient else 0, coefficient)
            )
        maps.append(local_map)
    return maps


HODGE_MAPS = hodge_maps()


def graph_frame() -> tuple[ComplexVector, ComplexVector]:
    zeta = cmath.exp(2j * math.pi / 3)
    adjacency = (
        (0, 2, 2, 1),
        (2, 0, 2, 1),
        (2, 2, 0, 1),
        (1, 1, 1, 0),
    )
    syndrome = (2, 2, 2, 1)
    u: ComplexVector = []
    v: ComplexVector = []
    for word in WORDS:
        phase = sum(
            adjacency[i][j] * word[i] * word[j]
            for i in range(4)
            for j in range(i + 1, 4)
        ) % 3
        shift = sum(
            syndrome[i] * word[i] for i in range(4)
        ) % 3
        u.append(zeta**phase / 9)
        v.append(zeta ** ((phase + shift) % 3) / 9)
    return u, v


def load_frame(path: str) -> tuple[ComplexVector, ComplexVector]:
    u = [0j] * 81
    v = [0j] * 81
    with open(path, encoding="utf-8") as stream:
        for line in stream:
            index, ur, ui, vr, vi = line.split()
            i = int(index)
            u[i] = complex(float(ur), float(ui))
            v[i] = complex(float(vr), float(vi))
    return u, v


def extract_tensors(
    u: ComplexVector, v: ComplexVector
) -> HodgeTensors:
    tensor_a: ComplexVector = []
    tensor_b: ComplexVector = []
    tensor_c: ComplexVector = []
    for local_map in HODGE_MAPS:
        au = [0j] * 81
        av = [0j] * 81
        for source, (target, coefficient) in enumerate(local_map):
            if coefficient:
                au[target] = coefficient * u[source]
                av[target] = coefficient * v[source]
        tensor_a.append(sum(u[i] * au[i] for i in range(81)))
        tensor_b.append(sum(u[i] * av[i] for i in range(81)))
        tensor_c.append(sum(v[i] * av[i] for i in range(81)))
    return tensor_a, tensor_b, tensor_c


def objective(tensors: HodgeTensors, smoothing: float = 0.0) -> float:
    tensor_a, tensor_b, tensor_c = tensors
    return sum(
        math.sqrt(abs(a * c - b * b) ** 2 + smoothing * smoothing)
        for a, b, c in zip(tensor_a, tensor_b, tensor_c)
    )


def identity() -> Matrix:
    return [[complex(i == j) for j in range(3)] for i in range(3)]


def conjugate_transpose(matrix: Matrix) -> Matrix:
    return [
        [matrix[j][i].conjugate() for j in range(3)]
        for i in range(3)
    ]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(3))
            for j in range(3)
        ]
        for i in range(3)
    ]


def matrix_add(
    left: Matrix, right: Matrix, scale: float = 1.0
) -> Matrix:
    return [
        [left[i][j] + scale * right[i][j] for j in range(3)]
        for i in range(3)
    ]


def matrix_norm_squared(matrix: Matrix) -> float:
    return sum(abs(value) ** 2 for row in matrix for value in row)


def qr_retract(matrix: Matrix) -> Matrix:
    """Orthonormalize columns by modified Gram--Schmidt."""
    columns: list[ComplexVector] = []
    for column_index in range(3):
        column = [matrix[row][column_index] for row in range(3)]
        for old in columns:
            overlap = sum(
                old[i].conjugate() * column[i] for i in range(3)
            )
            column = [
                column[i] - overlap * old[i] for i in range(3)
            ]
        length = math.sqrt(sum(abs(value) ** 2 for value in column))
        if length < 1e-14:
            raise ArithmeticError("rank-deficient QR retraction")
        columns.append([value / length for value in column])
    return [
        [columns[column][row] for column in range(3)]
        for row in range(3)
    ]


def haar_unitary(rng: random.Random) -> Matrix:
    return qr_retract([
        [
            complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0))
            for _ in range(3)
        ]
        for _ in range(3)
    ])


def apply_mode(
    tensor: ComplexVector, matrix: Matrix, site: int
) -> ComplexVector:
    output = [0j] * 81
    for output_index, output_word in enumerate(WORDS):
        value = 0j
        for source_label in range(3):
            source_word = list(output_word)
            source_word[site] = source_label
            value += (
                matrix[output_word[site]][source_label]
                * tensor[INDEX[tuple(source_word)]]
            )
        output[output_index] = value
    return output


def transform(
    tensors: HodgeTensors, matrix: Matrix, site: int
) -> HodgeTensors:
    return tuple(
        apply_mode(tensor, matrix, site) for tensor in tensors
    )  # type: ignore[return-value]


def value_and_euclidean_gradient(
    tensors: HodgeTensors,
    matrix: Matrix,
    site: int,
    smoothing: float = 1e-12,
) -> tuple[float, Matrix]:
    """Objective and real-Euclidean gradient in the matrix variable."""
    transformed = transform(tensors, matrix, site)
    tensor_a, tensor_b, tensor_c = transformed
    gradient = [[0j] * 3 for _ in range(3)]
    value = 0.0
    for output_index, output_word in enumerate(WORDS):
        row = output_word[site]
        a = tensor_a[output_index]
        b = tensor_b[output_index]
        c = tensor_c[output_index]
        determinant = a * c - b * b
        modulus = math.sqrt(
            abs(determinant) ** 2 + smoothing * smoothing
        )
        value += modulus
        coefficient = determinant.conjugate() / modulus
        for source_label in range(3):
            source_word = list(output_word)
            source_word[site] = source_label
            source_index = INDEX[tuple(source_word)]
            differential_coefficient = coefficient * (
                c * tensors[0][source_index]
                + a * tensors[2][source_index]
                - 2 * b * tensors[1][source_index]
            )
            # df=Re sum(conj(G_ij) dH_ij).
            gradient[row][source_label] += (
                differential_coefficient.conjugate()
            )
    return value, gradient


def tangent_gradient(matrix: Matrix, euclidean: Matrix) -> Matrix:
    product = matrix_multiply(conjugate_transpose(matrix), euclidean)
    hermitian = [
        [
            (product[i][j] + product[j][i].conjugate()) / 2
            for j in range(3)
        ]
        for i in range(3)
    ]
    normal = matrix_multiply(matrix, hermitian)
    return matrix_add(euclidean, normal, scale=-1.0)


def optimize_one_site(
    tensors: HodgeTensors,
    site: int,
    initial: Matrix,
    iterations: int = 300,
    initial_step: float = 0.25,
) -> tuple[float, Matrix]:
    matrix = initial
    value, _ = value_and_euclidean_gradient(tensors, matrix, site)
    step = initial_step
    for _ in range(iterations):
        current, euclidean = value_and_euclidean_gradient(
            tensors, matrix, site
        )
        gradient = tangent_gradient(matrix, euclidean)
        gradient_squared = matrix_norm_squared(gradient)
        if gradient_squared < 1e-22:
            break
        accepted = False
        trial_step = step
        for _ in range(30):
            candidate = qr_retract(
                matrix_add(matrix, gradient, scale=trial_step)
            )
            candidate_value, _ = value_and_euclidean_gradient(
                tensors, candidate, site
            )
            if candidate_value >= (
                current + 1e-5 * trial_step * gradient_squared
            ):
                matrix = candidate
                value = candidate_value
                step = min(initial_step, 1.3 * trial_step)
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            break
    return value, matrix


def best_one_site(
    tensors: HodgeTensors,
    site: int,
    rng: random.Random,
    starts: int,
    iterations: int,
) -> tuple[float, Matrix]:
    candidates = [identity()] + [
        haar_unitary(rng) for _ in range(max(0, starts - 1))
    ]
    best_value = -1.0
    best_matrix = identity()
    for candidate in candidates:
        value, matrix = optimize_one_site(
            tensors, site, candidate, iterations=iterations
        )
        if value > best_value:
            best_value = value
            best_matrix = matrix
    return best_value, best_matrix


def coordinate_ascent(
    tensors: HodgeTensors,
    rng: random.Random,
    sweeps: int,
    starts: int,
    iterations: int,
) -> tuple[float, HodgeTensors, list[Matrix]]:
    current = tensors
    accumulated = [identity() for _ in range(4)]
    for sweep in range(sweeps):
        previous = objective(current)
        for site in range(4):
            _, matrix = best_one_site(
                current, site, rng, starts, iterations
            )
            current = transform(current, matrix, site)
            accumulated[site] = matrix_multiply(
                matrix, accumulated[site]
            )
        value = objective(current)
        print(f"sweep {sweep}: C={value:.17g}")
        if value - previous < 1e-12:
            break
    return objective(current), current, accumulated


def finite_difference_test(
    tensors: HodgeTensors, rng: random.Random
) -> None:
    site = rng.randrange(4)
    matrix = haar_unitary(rng)
    direction = [
        [
            complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0))
            for _ in range(3)
        ]
        for _ in range(3)
    ]
    _, gradient = value_and_euclidean_gradient(
        tensors, matrix, site, smoothing=1e-8
    )
    predicted = sum(
        (gradient[i][j].conjugate() * direction[i][j]).real
        for i in range(3)
        for j in range(3)
    )
    epsilon_value = 1e-7
    plus, _ = value_and_euclidean_gradient(
        tensors,
        matrix_add(matrix, direction, scale=epsilon_value),
        site,
        smoothing=1e-8,
    )
    minus, _ = value_and_euclidean_gradient(
        tensors,
        matrix_add(matrix, direction, scale=-epsilon_value),
        site,
        smoothing=1e-8,
    )
    observed = (plus - minus) / (2 * epsilon_value)
    error = abs(predicted - observed)
    scale_value = max(1.0, abs(predicted), abs(observed))
    if error > 2e-6 * scale_value:
        raise AssertionError(
            f"gradient failure: predicted={predicted}, "
            f"observed={observed}, error={error}"
        )
    print(
        "finite-difference gradient check:",
        f"predicted={predicted:.12g}",
        f"observed={observed:.12g}",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frame", help="saved 81-by-2 frame")
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--sweeps", type=int, default=8)
    parser.add_argument("--starts", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=250)
    parser.add_argument(
        "--scramble",
        action="store_true",
        help="apply independent Haar frames before optimization",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    frame = load_frame(args.frame) if args.frame else graph_frame()
    tensors = extract_tensors(*frame)
    print(f"initial C={objective(tensors):.17g}")
    finite_difference_test(tensors, rng)
    if args.scramble:
        for site in range(4):
            tensors = transform(tensors, haar_unitary(rng), site)
        print(f"scrambled C={objective(tensors):.17g}")
    for site in range(4):
        value, _ = best_one_site(
            tensors, site, rng, args.starts, args.iterations
        )
        print(f"best one-site {site}: C={value:.17g}")
    value, _, _ = coordinate_ascent(
        tensors, rng, args.sweeps, args.starts, args.iterations
    )
    print(f"coordinate optimum C={value:.17g}")


if __name__ == "__main__":
    main()
