#!/usr/bin/env python3
"""Exact checks for the complete one-sided 4+2 color-block reduction.

Part I verifies the 64-block master formula for the cubic residual against
an independently assembled dense operator over the rationals.

Part II inserts the exact published-d4 two-site leakage limitation model
and checks all projection-block, marginal, and leakage identities in the
notation of the new reduction.
"""

from __future__ import annotations

from itertools import product

import sympy as sp

from verify_one_sided_square_invariance import (
    embed_d4_and_rectangle_mix,
)


Color = int
Pair = tuple[Color, Color]
Triple = tuple[Color, Color, Color]


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def color_indices(local_dimensions: tuple[int, int], colors: tuple[int, ...]) -> list[int]:
    """Lexicographic basis indices with each site restricted to one color."""
    d = sum(local_dimensions)
    local_ranges = (
        range(local_dimensions[0]),
        range(local_dimensions[0], d),
    )
    indices: list[int] = []
    for local in product(*(local_ranges[color] for color in colors)):
        index = 0
        for coordinate in local:
            index = d * index + coordinate
        indices.append(index)
    return indices


def extract_block(
    matrix: sp.Matrix,
    local_dimensions: tuple[int, int],
    output_colors: tuple[int, ...],
    input_colors: tuple[int, ...],
) -> sp.Matrix:
    rows = color_indices(local_dimensions, output_colors)
    columns = color_indices(local_dimensions, input_colors)
    return matrix.extract(rows, columns)


def deterministic_pair_operator(
    local_dimensions: tuple[int, int],
) -> sp.Matrix:
    """A rational operator reducing WW, with otherwise arbitrary blocks."""
    d = sum(local_dimensions)
    operator = sp.zeros(d**2)
    ww = color_indices(local_dimensions, (0, 0))
    complement = [
        index
        for colors in ((0, 1), (1, 0), (1, 1))
        for index in color_indices(local_dimensions, colors)
    ]
    q_block = sp.Matrix(
        len(ww),
        len(ww),
        lambda row, column: 2 + 3 * row - 5 * column,
    )
    k_block = sp.Matrix(
        len(complement),
        len(complement),
        lambda row, column: 7 - 2 * row + 4 * column,
    )
    for row_local, row in enumerate(ww):
        for column_local, column in enumerate(ww):
            operator[row, column] = q_block[row_local, column_local]
    for row_local, row in enumerate(complement):
        for column_local, column in enumerate(complement):
            operator[row, column] = k_block[row_local, column_local]
    return operator


def pair_blocks(
    operator: sp.Matrix,
    local_dimensions: tuple[int, int],
) -> dict[tuple[Pair, Pair], sp.Matrix]:
    pairs = tuple(product((0, 1), repeat=2))
    return {
        (output, input_colors): extract_block(
            operator, local_dimensions, output, input_colors
        )
        for output in pairs
        for input_colors in pairs
    }


def cubic_block_formula(
    blocks: dict[tuple[Pair, Pair], sp.Matrix],
    local_dimensions: tuple[int, int],
    output: Triple,
    input_colors: Triple,
) -> sp.Matrix:
    """The complete output/input color block of ABA-BAB-(A-B)/3."""
    a, b, c = output
    i, j, k = input_colors
    dimensions = local_dimensions
    result = sp.zeros(
        dimensions[a] * dimensions[b] * dimensions[c],
        dimensions[i] * dimensions[j] * dimensions[k],
    )

    for x, y, z in product((0, 1), repeat=3):
        result += (
            tensor(blocks[((a, b), (x, z))], sp.eye(dimensions[c]))
            * tensor(sp.eye(dimensions[x]), blocks[((z, c), (y, k))])
            * tensor(blocks[((x, y), (i, j))], sp.eye(dimensions[k]))
        )

    for x, y, t in product((0, 1), repeat=3):
        result -= (
            tensor(sp.eye(dimensions[a]), blocks[((b, c), (t, y))])
            * tensor(blocks[((a, t), (i, x))], sp.eye(dimensions[y]))
            * tensor(sp.eye(dimensions[i]), blocks[((x, y), (j, k))])
        )

    if c == k:
        result -= sp.Rational(1, 3) * tensor(
            blocks[((a, b), (i, j))], sp.eye(dimensions[k])
        )
    if a == i:
        result += sp.Rational(1, 3) * tensor(
            sp.eye(dimensions[i]), blocks[((b, c), (j, k))]
        )
    return result


def verify_all_cubic_color_blocks() -> None:
    local_dimensions = (2, 1)
    d = sum(local_dimensions)
    pair_operator = deterministic_pair_operator(local_dimensions)
    first = tensor(pair_operator, sp.eye(d))
    second = tensor(sp.eye(d), pair_operator)
    dense_residual = (
        first * second * first
        - second * first * second
        - sp.Rational(1, 3) * (first - second)
    )
    blocks = pair_blocks(pair_operator, local_dimensions)

    checked = 0
    for output in product((0, 1), repeat=3):
        for input_colors in product((0, 1), repeat=3):
            expected = extract_block(
                dense_residual,
                local_dimensions,
                output,
                input_colors,
            )
            obtained = cubic_block_formula(
                blocks, local_dimensions, output, input_colors
            )
            assert obtained == expected
            checked += 1
    assert checked == 64


def partial_trace_rectangular(
    block: sp.Matrix,
    output_dimensions: Pair,
    input_dimensions: Pair,
    traced_leg: int,
) -> sp.Matrix:
    """Partial trace of a rectangular two-leg map when traced sizes agree."""
    if output_dimensions[traced_leg] != input_dimensions[traced_leg]:
        raise ValueError("traced output/input dimensions differ")
    keep = 1 - traced_leg
    result = sp.zeros(output_dimensions[keep], input_dimensions[keep])
    traced_dimension = output_dimensions[traced_leg]
    for output_keep in range(output_dimensions[keep]):
        for input_keep in range(input_dimensions[keep]):
            for traced in range(traced_dimension):
                if traced_leg == 0:
                    output_index = traced * output_dimensions[1] + output_keep
                    input_index = traced * input_dimensions[1] + input_keep
                else:
                    output_index = (
                        output_keep * output_dimensions[1] + traced
                    )
                    input_index = input_keep * input_dimensions[1] + traced
                result[output_keep, input_keep] += block[
                    output_index, input_index
                ]
    return result


def hs_norm_squared(matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(matrix.conjugate().T * matrix))


def verify_projection_and_marginal_blocks() -> None:
    projection, _ = embed_d4_and_rectangle_mix()
    local_dimensions = (4, 2)
    blocks = pair_blocks(projection, local_dimensions)

    cell_a = (0, 1)
    cell_b = (1, 0)
    cell_d = (1, 1)
    a = blocks[(cell_a, cell_a)]
    b = blocks[(cell_b, cell_b)]
    d_block = blocks[(cell_d, cell_d)]
    z = blocks[(cell_a, cell_b)]
    x = blocks[(cell_a, cell_d)]
    y = blocks[(cell_b, cell_d)]

    assert a.conjugate().T == a
    assert b.conjugate().T == b
    assert d_block.conjugate().T == d_block
    assert blocks[(cell_b, cell_a)] == z.conjugate().T
    assert blocks[(cell_d, cell_a)] == x.conjugate().T
    assert blocks[(cell_d, cell_b)] == y.conjugate().T

    assert a**2 + z * z.conjugate().T + x * x.conjugate().T == a
    assert b**2 + z.conjugate().T * z + y * y.conjugate().T == b
    assert (
        d_block**2
        + x.conjugate().T * x
        + y.conjugate().T * y
        == d_block
    )
    assert a * z + z * b + x * y.conjugate().T == z
    assert a * x + z * y + x * d_block == x
    assert z.conjugate().T * x + b * y + y * d_block == y

    assert partial_trace_rectangular(a, (4, 2), (4, 2), 1) == sp.eye(4)
    assert partial_trace_rectangular(b, (2, 4), (2, 4), 0) == sp.eye(4)
    assert (
        partial_trace_rectangular(a, (4, 2), (4, 2), 0)
        + partial_trace_rectangular(d_block, (2, 2), (2, 2), 0)
        == 3 * sp.eye(2)
    )
    assert (
        partial_trace_rectangular(b, (2, 4), (2, 4), 1)
        + partial_trace_rectangular(d_block, (2, 2), (2, 2), 1)
        == 3 * sp.eye(2)
    )
    assert partial_trace_rectangular(x, (4, 2), (2, 2), 1) == sp.zeros(4, 2)
    assert partial_trace_rectangular(y, (2, 4), (2, 2), 0) == sp.zeros(4, 2)

    assert sp.trace(a) == 4
    assert sp.trace(b) == 4
    assert sp.trace(d_block) == 2
    delta = sp.simplify(
        sp.trace(d_block - d_block**2)
    )
    assert delta == hs_norm_squared(x) + hs_norm_squared(y)
    assert delta == sp.Rational(1, 2)
    assert not (x == sp.zeros(*x.shape) and y == sp.zeros(*y.shape))


def main() -> None:
    verify_all_cubic_color_blocks()
    print("PASS all 64 exact cubic color-block equations")
    verify_projection_and_marginal_blocks()
    print("PASS complete complement projection-block equations")
    print("PASS complete scalar-partial-trace block equations")
    print("PASS exact leakage identity delta=||X||^2+||Y||^2=1/2")
    print("All one-sided fixed-H4 color-block checks passed exactly.")


if __name__ == "__main__":
    main()
