#!/usr/bin/env python3
"""Independent reference replay for the dense-shell C++ benchmark.

The C++ kernel diagonalizes each restricted quadratic pencil.  This checker
does something intentionally different: for one real h=1 support and one
real h=0 support, it enumerates every point in the affine kernel, tabulates
the six quadratic outputs, and applies the 729-entry Fourier transform
directly.  Every exact Eisenstein character sum is compared with C++.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import pathlib
import subprocess
import tempfile
from collections import defaultdict


FIELD = 3
PRIME = 37
CLASS_COUNT = 12
QUARTETS = 6
AMBIENT = 24
CHARACTERS = 729
ROOTS = ((1, 0), (0, 1), (-1, -1))

# Filled after the independent brute-force replay was first completed.
EXPECTED_REFERENCE_SHA256 = (
    "58ca5a703683faf2072a5268af97ed826"
    "2d92b91ce60f92b6fc4500f319b70fe"
)


def mod3(value: int) -> int:
    return value % FIELD


def ambient_index(quartet: int, local: int) -> int:
    return (
        quartet,
        quartet + 6,
        quartet + 12,
        quartet + 18,
    )[local]


def geometry() -> tuple[tuple[tuple[int, ...], ...], ...]:
    subgroup = (1, 26, 10)
    classes = []
    class_of = [-1] * PRIME
    power = 1
    for class_index in range(CLASS_COUNT):
        part = tuple(power * member % PRIME for member in subgroup)
        classes.append(part)
        for value in part:
            if class_of[value] != -1:
                raise AssertionError("cyclotomic classes overlap")
            class_of[value] = class_index
        power = power * 2 % PRIME

    result = []
    for lag_class in range(QUARTETS):
        transition = [[0] * CLASS_COUNT for _ in range(CLASS_COUNT)]
        lag = classes[lag_class][0]
        for source in range(1, PRIME):
            target = (source + lag) % PRIME
            if target:
                transition[class_of[source]][class_of[target]] += 1
        polar = [[0] * AMBIENT for _ in range(AMBIENT)]
        for channel in range(2):
            offset = channel * CLASS_COUNT
            for left in range(CLASS_COUNT):
                for right in range(CLASS_COUNT):
                    polar[offset + left][offset + right] = (
                        transition[left][right]
                        + transition[right][left]
                    ) % FIELD
        result.append(tuple(tuple(row) for row in polar))
    summed = tuple(
        tuple(
            sum(result[lag][left][right] for lag in range(QUARTETS))
            % FIELD
            for right in range(AMBIENT)
        )
        for left in range(AMBIENT)
    )
    expected = tuple(
        tuple(2 if left == right else 0 for right in range(AMBIENT))
        for left in range(AMBIENT)
    )
    if summed != expected:
        raise AssertionError("the Python universal pencil is not 2I")
    return tuple(result)


POLAR = geometry()


def local_histograms() -> tuple[tuple[int, ...], tuple[int, ...]]:
    equation = (-1, 1, 1, -1)
    supports = [0] * 5
    signed = [0] * 5
    for mask in range(16):
        active = tuple(index for index in range(4) if mask & (1 << index))
        legal = 0
        for signs in itertools.product((1, -1), repeat=len(active)):
            if sum(
                equation[position] * sign
                for position, sign in zip(active, signs, strict=True)
            ) % FIELD == 0:
                legal += 1
        if legal:
            supports[len(active)] += 1
        signed[len(active)] += legal
    return tuple(supports), tuple(signed)


def polynomial_count(
    local: tuple[int, ...],
) -> dict[tuple[int, int], int]:
    state = {(0, 0): 1}
    for _quartet in range(QUARTETS):
        update: defaultdict[tuple[int, int], int] = defaultdict(int)
        for (medium, nonempty), count in state.items():
            for occupancy, multiplicity in enumerate(local):
                if multiplicity:
                    update[
                        medium + occupancy,
                        nonempty + (occupancy != 0),
                    ] += count * multiplicity
        state = dict(update)
    return state


def constraint_rows(mask: int) -> tuple[tuple[int, ...], ...]:
    positions = tuple(
        index for index in range(AMBIENT) if mask & (1 << index)
    )
    rows = []
    for quartet in range(QUARTETS):
        local_positions = {
            ambient_index(quartet, local) for local in range(4)
        }
        row = tuple(
            int(position in local_positions) for position in positions
        )
        if any(row):
            rows.append(row)
    rows.append(tuple(int(position < CLASS_COUNT) for position in positions))
    return tuple(rows)


def rref_nullspace(
    rows: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    work = [list(row) for row in rows]
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    pivots = []
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        if work[rank][column] == 2:
            work[rank] = [2 * value % FIELD for value in work[rank]]
        for row in range(row_count):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % FIELD
                for left, right in zip(work[row], work[rank], strict=True)
            ]
        pivots.append(column)
        rank += 1
        if rank == row_count:
            break
    if rank != row_count:
        raise AssertionError("reference constraint rows are dependent")
    pivot_set = set(pivots)
    basis = []
    for free in range(column_count):
        if free in pivot_set:
            continue
        vector = [0] * column_count
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -work[row][free] % FIELD
        basis.append(tuple(vector))
    return tuple(basis)


def parse_key_values(line: str) -> dict[str, str]:
    return dict(field.split("=", 1) for field in line.split()[1:])


def build_cpp(source: pathlib.Path, output: pathlib.Path) -> None:
    subprocess.run(
        (
            "clang++",
            "-O3",
            "-DNDEBUG",
            "-std=c++20",
            "-mcpu=apple-m1",
            str(source),
            "-o",
            str(output),
        ),
        check=True,
    )


def read_cpp_reference(binary: pathlib.Path) -> tuple[str, list[dict]]:
    process = subprocess.run(
        (str(binary), "--emit-reference"),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    fixtures: dict[int, dict] = {}
    for line in process.stdout.splitlines():
        if line.startswith("REFERENCE_META "):
            fields = parse_key_values(line)
            shell = int(fields["shell"])
            fixtures[shell] = {
                "shell": shell,
                "mask": int(fields["mask"]),
                "r": int(fields["r"]),
                "d": int(fields["d"]),
                "rho": int(fields["rho"]),
                "nu": int(fields["nu"]),
                "x0": tuple(map(int, fields["x0"])),
                "target": tuple(map(int, fields["target"])),
                "rhs": tuple(map(int, fields["rhs"])),
                "sign_code": int(fields["sign_code"]),
                "high_position": int(fields["high_position"]),
                "values": [None] * CHARACTERS,
            }
        elif line.startswith("REFERENCE_VALUE "):
            fields = parse_key_values(line)
            shell = int(fields["shell"])
            fixtures[shell]["values"][int(fields["code"])] = (
                int(fields["a"]),
                int(fields["b"]),
            )
    if set(fixtures) != {15, 18}:
        raise AssertionError("C++ did not emit both dense-shell fixtures")
    for fixture in fixtures.values():
        if any(value is None for value in fixture["values"]):
            raise AssertionError("a C++ reference character is missing")
    required_counts = (
        "h1_unsigned_supports=510384",
        "h0_unsigned_supports=107476",
        "h1_signed_skeletons=59743488",
        "h0_signed_skeletons=47730304",
    )
    if any(item not in process.stdout for item in required_counts):
        raise AssertionError("the C++ global census output changed")
    return process.stdout, [fixtures[15], fixtures[18]]


def restricted_forms(
    mask: int,
    x0_ambient: tuple[int, ...],
) -> tuple[
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
    tuple[int, ...],
]:
    positions = tuple(
        index for index in range(AMBIENT) if mask & (1 << index)
    )
    rows = constraint_rows(mask)
    basis_compact = rref_nullspace(rows)
    basis_ambient = tuple(
        tuple(
            basis[positions.index(ambient)] if ambient in positions else 0
            for ambient in range(AMBIENT)
        )
        for basis in basis_compact
    )

    constants = []
    linears = []
    restricted = []
    for lag in range(QUARTETS):
        matrix_times_x0 = tuple(
            sum(
                POLAR[lag][left][right] * x0_ambient[right]
                for right in range(AMBIENT)
            )
            % FIELD
            for left in range(AMBIENT)
        )
        constants.append(
            2
            * sum(
                x0_ambient[left]
                * POLAR[lag][left][right]
                * x0_ambient[right]
                for left in range(AMBIENT)
                for right in range(AMBIENT)
            )
            % FIELD
        )
        linears.append(
            tuple(
                sum(
                    vector[ambient] * matrix_times_x0[ambient]
                    for ambient in range(AMBIENT)
                )
                % FIELD
                for vector in basis_ambient
            )
        )
        restricted.append(
            tuple(
                tuple(
                    sum(
                        basis_ambient[left][ambient_left]
                        * POLAR[lag][ambient_left][ambient_right]
                        * basis_ambient[right][ambient_right]
                        for ambient_left in range(AMBIENT)
                        for ambient_right in range(AMBIENT)
                    )
                    % FIELD
                    for right in range(len(basis_ambient))
                )
                for left in range(len(basis_ambient))
            )
        )
    rhs = tuple(
        sum(
            row[column] * x0_ambient[position]
            for column, position in enumerate(positions)
        )
        % FIELD
        for row in rows
    )
    return (
        tuple(constants),
        tuple(linears),
        tuple(restricted),
        rhs,
    )


def brute_force_character_sums(fixture: dict) -> tuple[tuple[int, int], ...]:
    constants, linears, restricted, rhs = restricted_forms(
        fixture["mask"], fixture["x0"]
    )
    if rhs != fixture["rhs"]:
        raise AssertionError("the independently computed affine RHS changed")
    dimension = fixture["d"]
    if len(linears[0]) != dimension:
        raise AssertionError("the independently computed dimension changed")

    # Convert each symmetric matrix to its explicit quadratic coefficients:
    # q(y)=constant+linear*y+2*y^T B*y.
    terms = []
    for lag in range(QUARTETS):
        lag_terms = []
        for left in range(dimension):
            diagonal = 2 * restricted[lag][left][left] % FIELD
            if diagonal:
                lag_terms.append((left, left, diagonal))
            for right in range(left + 1, dimension):
                # The two off-diagonal entries contribute
                # 4*B_lr=B_lr modulo 3.
                coefficient = restricted[lag][left][right] % FIELD
                if coefficient:
                    lag_terms.append((left, right, coefficient))
        terms.append(tuple(lag_terms))

    histogram = [0] * CHARACTERS
    powers = (1, 3, 9, 27, 81, 243)
    for point in itertools.product(range(FIELD), repeat=dimension):
        output_code = 0
        for lag in range(QUARTETS):
            value = constants[lag] - fixture["target"][lag]
            value += sum(
                linears[lag][index] * point[index]
                for index in range(dimension)
            )
            value += sum(
                coefficient
                * point[left]
                * (point[left] if left == right else point[right])
                for left, right, coefficient in terms[lag]
            )
            output_code += (value % FIELD) * powers[lag]
        histogram[output_code] += 1
    if sum(histogram) != FIELD**dimension:
        raise AssertionError("quadratic histogram lost affine points")

    outputs = tuple(
        tuple((code // (FIELD**index)) % FIELD for index in range(QUARTETS))
        for code in range(CHARACTERS)
    )
    values = []
    for coefficient in outputs:
        real = 0
        omega = 0
        for output, multiplicity in zip(outputs, histogram, strict=True):
            if not multiplicity:
                continue
            exponent = sum(
                left * right
                for left, right in zip(coefficient, output, strict=True)
            ) % FIELD
            root = ROOTS[exponent]
            real += multiplicity * root[0]
            omega += multiplicity * root[1]
        values.append((real, omega))
    return tuple(values)


def reference_hash(fixtures: list[dict]) -> str:
    payload = [
        {
            "shell": fixture["shell"],
            "mask": fixture["mask"],
            "d": fixture["d"],
            "x0": fixture["x0"],
            "target": fixture["target"],
            "rhs": fixture["rhs"],
            "values": fixture["values"],
        }
        for fixture in fixtures
    ]
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    supports, signed = local_histograms()
    if supports != (1, 0, 6, 4, 1):
        raise AssertionError("Python local support histogram changed")
    if signed != (1, 0, 12, 8, 6):
        raise AssertionError("Python local signed histogram changed")
    support_counts = polynomial_count(supports)
    signed_counts = polynomial_count(signed)
    if support_counts[15, 4] + support_counts[15, 5] + support_counts[15, 6] != 510_384:
        raise AssertionError("Python h=1 support count changed")
    if support_counts[18, 5] + support_counts[18, 6] != 107_476:
        raise AssertionError("Python h=0 support count changed")
    if signed_counts[15, 4] != 103_680:
        raise AssertionError("Python h=1,r=4 signed count changed")
    if signed_counts[15, 5] != 12_085_248:
        raise AssertionError("Python h=1,r=5 signed count changed")
    if signed_counts[15, 6] != 47_554_560:
        raise AssertionError("Python h=1,r=6 signed count changed")
    if signed_counts[18, 5] != 1_296_000:
        raise AssertionError("Python h=0,r=5 signed count changed")
    if signed_counts[18, 6] != 46_434_304:
        raise AssertionError("Python h=0,r=6 signed count changed")

    here = pathlib.Path(__file__).resolve().parent
    source = here / "benchmark_dense_shell_characters.cpp"
    with tempfile.TemporaryDirectory(prefix="h668-dense-benchmark-") as temp:
        binary = pathlib.Path(temp) / "benchmark"
        build_cpp(source, binary)
        _stdout, fixtures = read_cpp_reference(binary)

    for fixture in fixtures:
        expected = brute_force_character_sums(fixture)
        actual = tuple(fixture["values"])
        if actual != expected:
            mismatch = next(
                index
                for index, (left, right) in enumerate(
                    zip(actual, expected, strict=True)
                )
                if left != right
            )
            raise AssertionError(
                f"shell {fixture['shell']} character {mismatch}: "
                f"C++={actual[mismatch]}, brute_force={expected[mismatch]}"
            )

    digest = reference_hash(fixtures)
    print(f"reference_sha256={digest}")
    if digest != EXPECTED_REFERENCE_SHA256:
        raise AssertionError(
            "the exact reference checksum is not pinned or changed: "
            f"expected {EXPECTED_REFERENCE_SHA256}, obtained {digest}"
        )
    print(
        "PASS: local counts, two affine-cube enumerations, and all "
        "1,458 exact character sums agree"
    )


if __name__ == "__main__":
    main()
