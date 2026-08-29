#!/usr/bin/env python3
"""Independent rational-interval replay of the sharpness Krawczyk box.

The two Fourier maps and their Jacobians are rebuilt directly from literal
rooted DAGs.  The certificate supplies only the box, center/scales, pivot
coordinates, row scales, and selected rank columns.  Stored interval
Jacobians, Krawczyk images, physical PASS flags, and rank matrices are ignored.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import sys


sys.set_int_max_str_digits(0)
ORDER3 = (
    "000", "0CC", "0GG", "0TT", "C0C", "CC0", "CGT", "CTG",
    "G0G", "GCT", "GG0", "GTC", "T0T", "TCG", "TGC", "TT0",
)
CHAR = {letter: index for index, letter in enumerate("0CGT")}


if not __debug__:
    raise RuntimeError("run without -O so fail-closed assertions remain active")


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def locate_certificate(package_root):
    for candidate in (
        package_root / "proof_package/sharpness/K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json",
        package_root / "sharpness/K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json",
    ):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("could not locate sharpness certificate beneath --package-root")


def rat(value):
    return Q(str(value))


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError((self.lo, self.hi))

    @staticmethod
    def point(value):
        value = rat(value)
        return Interval(value, value)

    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_interval(other))

    def __rsub__(self, other):
        return as_interval(other) - self

    def __mul__(self, other):
        other = as_interval(other)
        values = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_interval(other)
        if other.lo <= 0 <= other.hi:
            raise ZeroDivisionError(other)
        return self * Interval(min(1/other.lo, 1/other.hi), max(1/other.lo, 1/other.hi))

    def absmax(self):
        return max(abs(self.lo), abs(self.hi))


def as_interval(value):
    return value if isinstance(value, Interval) else Interval.point(value)


def zero_like(values):
    return Interval.point(0) if values and isinstance(values[0], Interval) else Q(0)


def one_like(values):
    return Interval.point(1) if values and isinstance(values[0], Interval) else Q(1)


def multiply(values, identity):
    result = identity
    for value in values:
        result *= value
    return result


def interval_pair(pair):
    return Interval(rat(pair[0]), rat(pair[1]))


def matrix_inverse(matrix):
    size = len(matrix)
    work = [
        [rat(matrix[row][column]) for column in range(size)]
        + [Q(row == column) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot_row = next(row for row in range(column, size) if work[row][column])
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
        pivot = work[column][column]
        work[column] = [value/pivot for value in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [left-factor*right for left, right in zip(work[row], work[column])]
    return [row[size:] for row in work]


def determinant(matrix):
    work = [[rat(value) for value in row] for row in matrix]
    result = Q(1)
    for column in range(len(work)):
        pivot_row = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot_row is None:
            return Q(0)
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            result = -result
        pivot = work[column][column]
        result *= pivot
        for row in range(column + 1, len(work)):
            if work[row][column]:
                factor = work[row][column] / pivot
                for right in range(column + 1, len(work)):
                    work[row][right] -= factor * work[column][right]
    return result


def matrix_multiply(left, right):
    rows, middle, columns = len(left), len(right), len(right[0])
    result = []
    for row in range(rows):
        output_row = []
        for column in range(columns):
            interval = any(
                isinstance(left[row][index], Interval) or isinstance(right[index][column], Interval)
                for index in range(middle)
            )
            seed = Interval.point(0) if interval else Q(0)
            output_row.append(sum(
                (left[row][index] * right[index][column] for index in range(middle)),
                seed,
            ))
        result.append(output_row)
    return result


def matrix_vector(matrix, vector):
    return [row[0] for row in matrix_multiply(matrix, [[value] for value in vector])]


def identity_minus(matrix):
    return [
        [Q(row == column) - matrix[row][column] for column in range(len(matrix))]
        for row in range(len(matrix))
    ]


def interval_inf_norm(matrix):
    return max(sum(as_interval(value).absmax() for value in row) for row in matrix)


class LiteralNetwork:
    def __init__(self, record):
        self.arcs = [tuple(edge) for edge in record["arcs"]]
        self.labels = {node: int(label) for node, label in record["labels"]}
        self.reticulations = list(record["reticulations"])
        self.parent0 = dict(zip(self.reticulations, record["parent0"]))
        self.parents = {
            reticulation: [tail for tail, head in self.arcs if head == reticulation]
            for reticulation in self.reticulations
        }
        assert len(self.arcs) == 10 and len(self.reticulations) == 2
        assert all(
            self.parent0[reticulation] in self.parents[reticulation]
            and len(self.parents[reticulation]) == 2
            for reticulation in self.reticulations
        )
        self.switchings = []
        for choices in product((0, 1), repeat=len(self.reticulations)):
            selected = {}
            for reticulation, choice in zip(self.reticulations, choices):
                other = next(parent for parent in self.parents[reticulation] if parent != self.parent0[reticulation])
                selected[reticulation] = self.parent0[reticulation] if choice else other
            kept = [
                edge for edge in self.arcs
                if edge[1] not in selected or edge[0] == selected[edge[1]]
            ]
            self.switchings.append((choices, kept, self._descendant_masks(kept)))

    def _descendant_masks(self, kept):
        children = {}
        for tail, head in kept:
            children.setdefault(tail, []).append(head)
            children.setdefault(head, [])
        memo = {}

        def visit(node):
            if node in memo:
                return memo[node]
            mask = (1 << self.labels[node]) if node in self.labels else 0
            for child in children.get(node, []):
                mask |= visit(child)
            memo[node] = mask
            return mask

        for tail, head in kept:
            visit(tail)
            visit(head)
        return {edge: memo[edge[1]] for edge in kept}

    @staticmethod
    def sector(mask, chars):
        result = 0
        index = 0
        while mask:
            if mask & 1:
                result ^= chars[index]
            mask >>= 1
            index += 1
        return result

    def value_and_jacobian(self, parameters):
        assert len(parameters) == 32
        one = one_like(parameters)
        zero = zero_like(parameters)
        outputs, jacobian = [], []
        for word in ORDER3[1:]:
            chars = tuple(CHAR[letter] for letter in word)
            value = zero
            row = [zero for _ in range(32)]
            for choices, kept, masks in self.switchings:
                inheritance = [
                    parameters[30+index] if choice else 1-parameters[30+index]
                    for index, choice in enumerate(choices)
                ]
                edge_factors, edge_columns = [], []
                for edge_index, edge in enumerate(self.arcs):
                    if edge not in masks:
                        continue
                    sector = self.sector(masks[edge], chars)
                    if sector:
                        edge_factors.append(parameters[3*edge_index+sector-1])
                        edge_columns.append(3*edge_index+sector-1)
                weight = multiply(inheritance, one)
                edge_product = multiply(edge_factors, one)
                value += weight * edge_product
                for index, column in enumerate(edge_columns):
                    derivative_product = multiply(edge_factors[:index] + edge_factors[index+1:], one)
                    row[column] += weight * derivative_product
                for index, choice in enumerate(choices):
                    other_weights = multiply(inheritance[:index] + inheritance[index+1:], one)
                    row[30+index] += (1 if choice else -1) * other_weights * edge_product
            outputs.append(value)
            jacobian.append(row)
        return outputs, jacobian


def exact_equal_matrix(actual, stored):
    return all(
        actual[row][column] == rat(stored[row][column])
        for row in range(len(actual))
        for column in range(len(actual[row]))
    )


def lower_bound(expression):
    return as_interval(expression).lo


def physical_bounds(parameters):
    categories = {"eigen": [], "transition": [], "ct": [], "inheritance": []}
    for edge in range(10):
        c, g, t = parameters[3*edge:3*edge+3]
        categories["eigen"].extend((
            lower_bound(c), lower_bound(g), lower_bound(t),
            lower_bound(1-c), lower_bound(1-g), lower_bound(1-t),
        ))
        categories["transition"].extend((
            lower_bound((1+c+g+t) * Q(1, 4)),
            lower_bound((1+c-g-t) * Q(1, 4)),
            lower_bound((1-c+g-t) * Q(1, 4)),
            lower_bound((1-c-g+t) * Q(1, 4)),
        ))
        categories["ct"].extend((
            lower_bound(c-g*t), lower_bound(g-c*t), lower_bound(t-c*g),
        ))
    for inheritance in parameters[30:]:
        categories["inheritance"].extend((lower_bound(inheritance), lower_bound(1-inheritance)))
    return {category: min(values) for category, values in categories.items()}


def decimal(value, digits=12):
    value = rat(value)
    with localcontext() as context:
        context.prec = digits + 8
        number = Decimal(value.numerator) / Decimal(value.denominator)
        return f"{number:.{digits}E}"


def exact_summary(value):
    value = rat(value)
    encoded = str(value).encode()
    return {
        "decimal": decimal(value),
        "exact_fraction_sha256": hashlib.sha256(encoded).hexdigest(),
        "numerator_digits": len(str(abs(value.numerator))),
        "denominator_digits": len(str(value.denominator)),
        "sign": -1 if value < 0 else 1 if value > 0 else 0,
    }


def main():
    args = arguments()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    certificate_path = locate_certificate(args.package_root)
    data = json.loads(certificate_path.read_text(encoding="utf-8"))
    parameterization = data["parameterization"]
    box = [interval_pair(pair) for pair in parameterization["direct_parameter_box"]]
    point = [rat(value) for value in parameterization["direct_parameter_point"]]
    center = [rat(value) for value in parameterization["scaled_variable_center"]]
    radius = rat(parameterization["box_radius"])
    pivots = list(parameterization["pivot_global_columns"])
    scales = [
        rat(value)
        for value in parameterization["multiplicative_scales_for_pivots_and_values_for_frozen_parameters"]
    ]
    row_scales = [rat(value) for value in parameterization["row_scales"]]
    assert len(box) == len(point) == len(scales) == 64
    assert len(center) == len(pivots) == len(row_scales) == 15
    assert radius > 0 and len(set(pivots)) == 15 and all(0 <= column < 64 for column in pivots)
    pivot_set = set(pivots)
    assert all(point[column] == scales[column] * center[index] for index, column in enumerate(pivots))
    assert all(
        box[column] == Interval(
            scales[column] * (center[index]-radius),
            scales[column] * (center[index]+radius),
        )
        for index, column in enumerate(pivots)
    )
    assert all(
        point[column] == scales[column]
        and box[column] == Interval(point[column], point[column])
        for column in range(64)
        if column not in pivot_set
    )
    assert all(interval.lo <= value <= interval.hi for interval, value in zip(box, point))

    left = LiteralNetwork(data["primitive_networks"]["W"])
    right = LiteralNetwork(data["primitive_networks"]["Wprime"])
    q_left_point, j_left_point = left.value_and_jacobian(point[:32])
    q_right_point, j_right_point = right.value_and_jacobian(point[32:])
    _, j_left_box = left.value_and_jacobian(box[:32])
    _, j_right_box = right.value_and_jacobian(box[32:])

    residual = [
        row_scales[row] * (q_left_point[row]-q_right_point[row])
        for row in range(15)
    ]
    assert residual == [rat(value) for value in data["equality_system"]["exact_center_residual"]]

    point_jacobian, box_jacobian = [], []
    for row in range(15):
        point_row, box_row = [], []
        for column in pivots:
            if column < 32:
                point_derivative, box_derivative, sign = j_left_point[row][column], j_left_box[row][column], 1
            else:
                point_derivative, box_derivative, sign = j_right_point[row][column-32], j_right_box[row][column-32], -1
            point_row.append(row_scales[row] * sign * scales[column] * point_derivative)
            box_row.append(row_scales[row] * sign * scales[column] * box_derivative)
        point_jacobian.append(point_row)
        box_jacobian.append(box_row)
    assert exact_equal_matrix(point_jacobian, data["equality_system"]["point_jacobian"])
    point_determinant = determinant(point_jacobian)
    assert point_determinant == rat(data["equality_system"]["point_jacobian_determinant"])
    preconditioner = matrix_inverse(point_jacobian)

    error = identity_minus(matrix_multiply(preconditioner, box_jacobian))
    contraction = interval_inf_norm(error)
    correction = [center[index]-value for index, value in enumerate(matrix_vector(preconditioner, residual))]
    delta = [Interval(-radius, radius) for _ in range(15)]
    propagated = matrix_vector(error, delta)
    image = [
        Interval(correction[index]+propagated[index].lo, correction[index]+propagated[index].hi)
        for index in range(15)
    ]
    normalized = max(
        max(abs(image[index].lo-center[index]), abs(image[index].hi-center[index])) / radius
        for index in range(15)
    )
    strict_inclusion = all(
        center[index]-radius < image[index].lo <= image[index].hi < center[index]+radius
        for index in range(15)
    )
    assert strict_inclusion and contraction < 1 and normalized < 1

    rank = {}
    for side, point_matrix, box_matrix in (
        ("W", j_left_point, j_left_box),
        ("Wprime", j_right_point, j_right_box),
    ):
        columns = data["rank_15_minors"][side]["selected_columns"]
        assert len(columns) == len(set(columns)) == 15
        assert all(0 <= column < 32 for column in columns)
        selected_point = [[point_matrix[row][column] for column in columns] for row in range(15)]
        selected_box = [[box_matrix[row][column] for column in columns] for row in range(15)]
        selected_determinant = determinant(selected_point)
        assert selected_determinant == rat(data["rank_15_minors"][side]["point_determinant"])
        inverse = matrix_inverse(selected_point)
        neumann = interval_inf_norm(identity_minus(matrix_multiply(inverse, selected_box)))
        assert neumann < 1
        rank[side] = {
            "selected_columns": columns,
            "point_determinant": exact_summary(selected_determinant),
            "neumann_bound": exact_summary(neumann),
            "rank_15_everywhere_in_box": True,
        }

    physical = {
        "W": {category: exact_summary(value) for category, value in physical_bounds(box[:32]).items()},
        "Wprime": {category: exact_summary(value) for category, value in physical_bounds(box[32:]).items()},
    }
    assert all(record["sign"] > 0 for side in physical.values() for record in side.values())

    result = {
        "literal_maps_match_stored_center_residual": True,
        "literal_maps_match_stored_point_jacobian": True,
        "fresh_point_jacobian_determinant": exact_summary(point_determinant),
        "fresh_max_scaled_center_residual": decimal(max(abs(value) for value in residual)),
        "fresh_krawczyk_strict_self_inclusion": strict_inclusion,
        "fresh_krawczyk_max_normalized_distance": exact_summary(normalized),
        "fresh_preconditioned_interval_jacobian_inf_norm": exact_summary(contraction),
        "uniqueness_scope": "unique zero in the supplied 15-dimensional scaled pivot-coordinate slice box",
        "fresh_rank_certificates": rank,
        "fresh_physical_lower_bounds": physical,
        "independence_boundary": (
            "The literal network polynomials, Jacobians, intervals, Krawczyk image, rank bounds, and physical "
            "margins are rebuilt here.  The rational center, frozen coordinates, pivot scaling, radius, and "
            "selected rank columns remain certificate inputs; uniqueness is not asserted outside that slice."
        ),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (args.output_dir / "krawczyk_box.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
