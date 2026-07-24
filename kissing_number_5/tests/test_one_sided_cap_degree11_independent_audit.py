"""Independent exact adversarial audit of the degree-11 cap certificate.

This file intentionally imports neither degree-10 verifier code nor the
degree-11 verifier.  It reconstructs the rational kernel and Bernstein tree
directly from the degree-11 JSON payload using only the standard library.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "one_sided_cap_degree11_bound.json"
Poly = dict[tuple[int, int, int], Q]


def add(first: Poly, second: Poly) -> Poly:
    answer = dict(first)
    for exponent, value in second.items():
        answer[exponent] = answer.get(exponent, Q(0)) + value
        if answer[exponent] == 0:
            del answer[exponent]
    return answer


def scale(poly: Poly, value: Q) -> Poly:
    return {
        exponent: value * coefficient
        for exponent, coefficient in poly.items()
        if value * coefficient
    }


def multiply(first: Poly, second: Poly) -> Poly:
    answer: Poly = {}
    for (a, b, c), x in first.items():
        for (d, e, f), y in second.items():
            exponent = (a + d, b + e, c + f)
            answer[exponent] = answer.get(exponent, Q(0)) + x * y
    return {exponent: value for exponent, value in answer.items() if value}


def embed(coefficients: tuple[Q, ...], variable: int) -> Poly:
    answer = {}
    for power, value in enumerate(coefficients):
        exponent = [0, 0, 0]
        exponent[variable] = power
        if value:
            answer[tuple(exponent)] = value
    return answer


@lru_cache(maxsize=None)
def zonal(dimension: int, maximum_degree: int) -> tuple[tuple[Q, ...], ...]:
    values: list[list[Q]] = [[Q(1)]]
    if maximum_degree:
        values.append([Q(0), Q(1)])
    for degree in range(2, maximum_degree + 1):
        numerator = [Q(0)] * (len(values[-1]) + 1)
        for index, value in enumerate(values[-1]):
            numerator[index + 1] += (2 * degree + dimension - 4) * value
        for index, value in enumerate(values[-2]):
            numerator[index] -= (degree - 1) * value
        denominator = degree + dimension - 3
        values.append([value / denominator for value in numerator])
    return tuple(tuple(row) for row in values)


def q_polynomials(maximum_degree: int) -> list[Poly]:
    inner_residual = {(0, 0, 1): Q(1), (1, 1, 0): Q(-1)}
    radial_product = {
        (0, 0, 0): Q(1),
        (2, 0, 0): Q(-1),
        (0, 2, 0): Q(-1),
        (2, 2, 0): Q(1),
    }
    values = [{(0, 0, 0): Q(1)}]
    if maximum_degree:
        values.append(inner_residual)
    for degree in range(2, maximum_degree + 1):
        numerator = add(
            scale(
                multiply(inner_residual, values[-1]), Q(2 * degree)
            ),
            scale(
                multiply(radial_product, values[-2]), Q(-(degree - 1))
            ),
        )
        values.append(scale(numerator, Q(1, degree + 1)))
    return values


def gram_blocks(certificate: dict) -> list[list[list[Q]]]:
    blocks = []
    for expected_k, entry in enumerate(certificate["blocks"]):
        assert entry["k"] == expected_k
        size = 12 - expected_k
        assert entry["size"] == size
        denominator = int(entry["factor_denominator"])
        assert denominator > 0
        factor = entry["factor_integer_columns"]
        assert len(factor) == size
        rank = len(factor[0])
        assert rank > 0 and all(len(row) == rank for row in factor)
        blocks.append(
            [
                [
                    sum(
                        (
                            Q(
                                factor[row][column] * factor[col][column],
                                denominator**2,
                            )
                            for column in range(rank)
                        ),
                        Q(0),
                    )
                    for col in range(size)
                ]
                for row in range(size)
            ]
        )
    assert len(blocks) == 12
    return blocks


def construct_polynomial(blocks: list[list[list[Q]]]) -> Poly:
    maximum_degree = 11
    q_values = q_polynomials(maximum_degree)
    answer: Poly = {}
    for k, block in enumerate(blocks):
        size = maximum_degree - k + 1
        basis = zonal(5 + 2 * k, size - 1)
        for row in range(size):
            row_u = embed(basis[row], 0)
            row_v = embed(basis[row], 1)
            diagonal = multiply(multiply(row_u, row_v), q_values[k])
            answer = add(answer, scale(diagonal, block[row][row]))
            for col in range(row + 1, size):
                col_u = embed(basis[col], 0)
                col_v = embed(basis[col], 1)
                symmetric = add(
                    multiply(row_u, col_v), multiply(col_u, row_v)
                )
                answer = add(
                    answer,
                    scale(multiply(symmetric, q_values[k]), block[row][col]),
                )
    return answer


def substitute_t(poly: Poly) -> Poly:
    """Substitute t=-1+3s/2, leaving s in the third exponent."""
    answer: Poly = {}
    for (a, b, c), value in poly.items():
        for power in range(c + 1):
            coefficient = (
                value
                * comb(c, power)
                * ((-1) ** (c - power))
                * Q(3, 2) ** power
            )
            exponent = (a, b, power)
            answer[exponent] = answer.get(exponent, Q(0)) + coefficient
    return {exponent: value for exponent, value in answer.items() if value}


def tensor_bernstein(poly: Poly, degree: int = 11) -> tuple[Q, ...]:
    side = degree + 1
    answer = [Q(0)] * side**3
    ratios = [
        [
            Q(comb(index, power), comb(degree, power))
            if index >= power
            else Q(0)
            for index in range(side)
        ]
        for power in range(side)
    ]
    for (a, b, c), value in poly.items():
        assert max(a, b, c) <= degree
        for i in range(a, side):
            for j in range(b, side):
                prefix = value * ratios[a][i] * ratios[b][j]
                base = (i * side + j) * side
                for k in range(c, side):
                    answer[base + k] += prefix * ratios[c][k]
    return tuple(answer)


def split_line(values: list[Q]) -> tuple[list[Q], list[Q]]:
    levels = [values]
    while len(levels[-1]) > 1:
        old = levels[-1]
        levels.append(
            [(old[index] + old[index + 1]) / 2 for index in range(len(old) - 1)]
        )
    return (
        [level[0] for level in levels],
        [level[-1] for level in reversed(levels)],
    )


def split_tensor(
    values: tuple[Q, ...], axis: int, degree: int = 11
) -> tuple[tuple[Q, ...], tuple[Q, ...]]:
    side = degree + 1
    left = [Q(0)] * len(values)
    right = [Q(0)] * len(values)

    def at(i, j, k):
        return (i * side + j) * side + k

    if axis == 0:
        for j in range(side):
            for k in range(side):
                a, b = split_line([values[at(i, j, k)] for i in range(side)])
                for i in range(side):
                    left[at(i, j, k)], right[at(i, j, k)] = a[i], b[i]
    elif axis == 1:
        for i in range(side):
            for k in range(side):
                a, b = split_line([values[at(i, j, k)] for j in range(side)])
                for j in range(side):
                    left[at(i, j, k)], right[at(i, j, k)] = a[j], b[j]
    else:
        for i in range(side):
            for j in range(side):
                a, b = split_line([values[at(i, j, k)] for k in range(side)])
                for k in range(side):
                    left[at(i, j, k)], right[at(i, j, k)] = a[k], b[k]
    return tuple(left), tuple(right)


def independent_domain_audit(
    margin: tuple[Q, ...], determinant: tuple[Q, ...]
) -> tuple[Counter, str]:
    stack = [(margin, determinant, 0, "")]
    counts = Counter()
    digest = hashlib.sha256()
    while stack:
        h_box, d_box, depth, path = stack.pop()
        if max(d_box) < 0:
            category = "infeasible"
        elif min(h_box) >= 0:
            category = "proved"
        else:
            if depth >= 48:
                raise AssertionError(f"unterminated exact box {path}")
            axis = depth % 3
            h_left, h_right = split_tensor(h_box, axis)
            d_left, d_right = split_tensor(d_box, axis)
            stack.append((h_right, d_right, depth + 1, path + "1"))
            stack.append((h_left, d_left, depth + 1, path + "0"))
            continue
        counts[(category, depth)] += 1
        digest.update(f"{path}:{category}\n".encode())
    return counts, digest.hexdigest()


def diagonal_bernstein(poly: Poly) -> tuple[Q, ...]:
    margin: dict[int, Q] = {0: Q(1647, 50)}
    for (i, j, _), value in poly.items():
        margin[i + j] = margin.get(i + j, Q(0)) - value
    degree = max(margin)
    answer = [Q(0)] * (degree + 1)
    for power, value in margin.items():
        for index in range(power, degree + 1):
            answer[index] += value * Q(
                comb(index, power), comb(degree, power)
            )
    return tuple(answer)


def audit_diagonal(values: tuple[Q, ...]) -> Counter:
    stack = [(values, 0)]
    counts = Counter()
    while stack:
        current, depth = stack.pop()
        if min(current) >= 0:
            counts[depth] += 1
        else:
            if depth >= 48:
                raise AssertionError("diagonal interval did not terminate")
            left, right = split_line(list(current))
            stack.append((tuple(right), depth + 1))
            stack.append((tuple(left), depth + 1))
    return counts


def evaluate(poly: Poly, u: Q, v: Q, t: Q) -> Q:
    powers_u = [Q(1)]
    powers_v = [Q(1)]
    powers_t = [Q(1)]
    for _ in range(11):
        powers_u.append(powers_u[-1] * u)
        powers_v.append(powers_v[-1] * v)
        powers_t.append(powers_t[-1] * t)
    return sum(
        (
            coefficient * powers_u[a] * powers_v[b] * powers_t[c]
            for (a, b, c), coefficient in poly.items()
        ),
        Q(0),
    )


def d5_cap_triples():
    roots = []
    for first in range(5):
        for second in range(first + 1, 5):
            for sign_first in (-1, 1):
                for sign_second in (-1, 1):
                    row = [0] * 5
                    row[first] = sign_first
                    row[second] = sign_second
                    roots.append(tuple(row))
    anchor = roots[-1]

    def dot(first, second):
        return Q(sum(a * b for a, b in zip(first, second)), 2)

    cap = [root for root in roots if dot(anchor, root) >= 0]
    return cap, anchor, dot


class IndependentDegree11CapAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = json.loads(CERTIFICATE.read_text())
        cls.blocks = gram_blocks(cls.certificate)
        cls.polynomial = construct_polynomial(cls.blocks)

    def test_factor_payload_and_objective_arithmetic(self):
        payload = [
            {
                key: block[key]
                for key in (
                    "k",
                    "size",
                    "factor_denominator",
                    "factor_integer_columns",
                )
            }
            for block in self.certificate["blocks"]
        ]
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertEqual(
            digest,
            "723d5521951ce45d236116016a69e7e8e510b8e7ba1f0338f7c1d6fffe507257",
        )
        self.assertEqual(len(self.polynomial), 650)
        self.assertEqual(
            tuple(max(exponent[i] for exponent in self.polynomial) for i in range(3)),
            (11, 11, 11),
        )
        objective = Q(1) + Q(1000, 969) * Q(1647, 50)
        self.assertEqual(objective, Q(11303, 323))
        self.assertEqual(35 - objective, Q(2, 323))

    def test_full_closed_domain_tree_and_diagonal(self):
        off_target = Q(-969, 1000)
        margin = scale(self.polynomial, Q(-1))
        margin[(0, 0, 0)] = margin.get((0, 0, 0), Q(0)) + off_target
        determinant = {
            (0, 0, 0): Q(1),
            (1, 1, 1): Q(2),
            (2, 0, 0): Q(-1),
            (0, 2, 0): Q(-1),
            (0, 0, 2): Q(-1),
        }
        counts, digest = independent_domain_audit(
            tensor_bernstein(substitute_t(margin)),
            tensor_bernstein(substitute_t(determinant)),
        )
        self.assertEqual(sum(counts.values()), 5995)
        self.assertEqual(max(depth for (_, depth) in counts), 31)
        self.assertEqual(
            {
                category: sum(
                    number
                    for (current, _), number in counts.items()
                    if current == category
                )
                for category in ("infeasible", "proved")
            },
            {"infeasible": 2848, "proved": 3147},
        )
        self.assertEqual(
            digest,
            "3ffd08afa66bcd12e52399e392c09fda237f8bab18fc1af9a8090e76f1f81f65",
        )
        diagonal_counts = audit_diagonal(diagonal_bernstein(self.polynomial))
        self.assertEqual(sum(diagonal_counts.values()), 3)
        self.assertEqual(max(diagonal_counts), 2)

    def test_boundaries_former_ridge_and_exact_d5_cap(self):
        off_target = Q(-969, 1000)
        diagonal_target = Q(1647, 50)
        feasible_boundary_points = [
            (Q(0), Q(0), Q(-1)),
            (Q(0), Q(0), Q(1, 2)),
            (Q(1), Q(0), Q(0)),
            (Q(1), Q(1, 2), Q(1, 2)),
            (Q(3, 5), Q(3, 5), Q(-7, 25)),
            (Q(1, 2), Q(1, 2), Q(1, 2)),
            (Q(4791, 65536), Q(5, 64), Q(-113, 128)),
        ]
        for u, v, t in feasible_boundary_points:
            determinant = 1 + 2 * u * v * t - u * u - v * v - t * t
            self.assertGreaterEqual(determinant, 0)
            self.assertLessEqual(t, Q(1, 2))
            self.assertLessEqual(evaluate(self.polynomial, u, v, t), off_target)
            self.assertEqual(
                evaluate(self.polynomial, u, v, t),
                evaluate(self.polynomial, v, u, t),
            )
        for u in (Q(0), Q(1, 64), Q(3, 32), Q(1, 2), Q(1)):
            self.assertLessEqual(
                evaluate(self.polynomial, u, u, Q(1)), diagonal_target
            )

        # Inspect an exact rational grid along the formerly missed u=v ridge.
        for u_numerator, t_numerator in itertools.product(range(0, 9), range(-16, 9)):
            u = Q(u_numerator, 64)
            t = Q(t_numerator, 16)
            determinant = 1 + 2 * u * u * t - 2 * u * u - t * t
            if determinant >= 0 and t <= Q(1, 2):
                self.assertLessEqual(
                    evaluate(self.polynomial, u, u, t), off_target
                )

        cap, anchor, dot = d5_cap_triples()
        self.assertEqual(len(cap), 27)
        total = Q(0)
        cache = {}
        for first in cap:
            u = dot(anchor, first)
            for second in cap:
                v = dot(anchor, second)
                t = dot(first, second)
                key = (u, v, t)
                value = cache.setdefault(
                    key, evaluate(self.polynomial, u, v, t)
                )
                total += value
                if first == second:
                    self.assertLessEqual(value, diagonal_target)
                else:
                    self.assertLessEqual(t, Q(1, 2))
                    self.assertLessEqual(value, off_target)
        # A normalization/sign error in the positive kernels commonly makes
        # this ordered kernel sum negative on the exact D5 cap.
        self.assertGreaterEqual(total, 0)


if __name__ == "__main__":
    unittest.main()
