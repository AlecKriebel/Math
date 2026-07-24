#!/usr/bin/env python3
"""Exact exhaustive verifier for the 3/4 covering lemma.

All 46,512 candidate bases are solved over ``fractions.Fraction``.  The
program uses explicit exceptions instead of ``assert`` and has no input from
a numerical optimizer.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
import sys


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def constraints(sigma, tau):
    require(sigma in (-1, 1) and tau in (-1, 1), "invalid sign case")
    answer = []

    def add(coefficients, bound, name):
        require(len(coefficients) == 5, "constraint coefficient shape")
        answer.append(
            (tuple(Fraction(x) for x in coefficients), Fraction(bound), name)
        )

    for index, name in enumerate(("a", "b", "c", "U", "V")):
        row = [0] * 5
        row[index] = -1
        add(row, 0, name + ">=0")

    add((1, 0, 0, 0, tau), 1, "S14+")
    add((0, 1, 0, -sigma, 0), 1, "S23-")
    add((0, 0, 1, sigma, 0), 1, "S25+")
    add((0, 1, 0, 0, -tau), 1, "S34-")
    add((1, 0, 1, 0, 0), 1, "S15")

    three_halves = Fraction(3, 2)
    add((1, 0, 0, 1, 0), three_halves, "V12")
    add((1, 1, 0, 0, 0), three_halves, "V13")
    add((1, 0, 0, 0, -tau), three_halves, "V14")
    add((0, 1, 0, sigma, 0), three_halves, "V23")
    add((0, 0, 0, 1, 1), three_halves, "V24")
    add((0, 0, 1, -sigma, 0), three_halves, "V25")
    add((0, 1, 0, 0, tau), three_halves, "V34")
    add((0, 1, 1, 0, 0), three_halves, "V35")
    add((0, 0, 1, 0, 1), three_halves, "V45")
    require(len(answer) == 19, "wrong constraint count")
    return tuple(answer)


def solve_basis(rows, bounds):
    work = [
        [Fraction(value) for value in row] + [Fraction(bound)]
        for row, bound in zip(rows, bounds)
    ]
    dimension = 5
    for column in range(dimension):
        pivot = next(
            (row for row in range(column, dimension) if work[row][column]),
            None,
        )
        if pivot is None:
            return None
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        for j in range(column, dimension + 1):
            work[column][j] /= scale
        for row in range(dimension):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            for j in range(column, dimension + 1):
                work[row][j] -= scale * work[column][j]
    return tuple(work[row][dimension] for row in range(dimension))


def feasible(point, system):
    return all(
        sum(coefficient * value for coefficient, value in zip(row, point))
        <= bound
        for row, bound, _ in system
    )


def enumerate_vertices(sigma, tau):
    system = constraints(sigma, tau)
    vertices = set()
    feasible_bases = 0
    for indices in combinations(range(len(system)), 5):
        point = solve_basis(
            [system[index][0] for index in indices],
            [system[index][1] for index in indices],
        )
        if point is None or not feasible(point, system):
            continue
        feasible_bases += 1
        vertices.add(point)
    require(vertices, "sign-case polytope has no enumerated vertices")
    norms = Counter(sum(value * value for value in point) for point in vertices)
    return vertices, feasible_bases, norms


def verify():
    expected = {
        (-1, -1): (46, 184, Fraction(29, 16)),
        (-1, 1): (46, 176, Fraction(29, 16)),
        (1, -1): (46, 176, Fraction(29, 16)),
        (1, 1): (60, 200, Fraction(2, 1)),
    }
    cases = {}
    equality_points = set()
    for signs, (vertex_count, basis_count, maximum) in expected.items():
        vertices, feasible_bases, norms = enumerate_vertices(*signs)
        require(len(vertices) == vertex_count, "vertex count mismatch")
        require(feasible_bases == basis_count, "feasible-basis count mismatch")
        require(max(norms) == maximum, "maximum squared norm mismatch")
        for point in vertices:
            if sum(value * value for value in point) == 2:
                equality_points.add((signs, point))
        cases["%d,%d" % signs] = {
            "vertices": len(vertices),
            "feasible_bases": feasible_bases,
            "maximum_squared_norm": str(max(norms)),
            "norm_distribution": {
                str(key): value
                for key, value in sorted(norms.items(), key=lambda item: item[0])
            },
        }

    expected_equality = (
        (1, 1),
        (
            Fraction(1, 2),
            Fraction(1, 1),
            Fraction(1, 2),
            Fraction(1, 2),
            Fraction(1, 2),
        ),
    )
    require(equality_points == {expected_equality}, "equality case mismatch")
    return {
        "status": "COMPUTATIONALLY_CERTIFIED_EXACT_RATIONAL_ENUMERATION",
        "candidate_bases_checked": 4 * 11628,
        "cases": cases,
        "covering_inner_product": "3/4",
        "scaled_equality_magnitude": ["1/2", "1", "1/2", "1/2", "1/2"],
    }


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    require(not arguments, "usage: verify_covering_lemma.py")
    print(json.dumps(verify(), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print("VERIFICATION FAILED: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
