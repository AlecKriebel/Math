#!/usr/bin/env python3
"""Exact verifier for the rational degree-10 one-sided cap-SDP bound.

The candidate matrix blocks are reconstructed from rational Gram factors.
The script then tries to prove, with Fraction arithmetic, that

    F(u,v,t) <= off_target

whenever 0<=u,v<=1, -1<=t<=1/2, and
1+2uvt-u^2-v^2-t^2>=0, and that F(u,u,1)<=diag_target.

Only the Python standard library is used.  The floating-point discovery
metadata in the certificate is ignored.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import json
from math import comb
from pathlib import Path


Exponent = tuple[int, int, int]
Polynomial = dict[Exponent, Q]
ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_PATH = ROOT / "certificates" / "one_sided_cap_degree10_bound.json"


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, Q(0)) + coefficient
        if answer[exponent] == 0:
            del answer[exponent]
    return answer


def poly_scale(poly: Polynomial, scalar: Q) -> Polynomial:
    if scalar == 0:
        return {}
    return {
        exponent: coefficient * scalar
        for exponent, coefficient in poly.items()
        if coefficient * scalar
    }


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for (i, j, k), first in left.items():
        for (a, b, c), second in right.items():
            exponent = i + a, j + b, k + c
            answer[exponent] = answer.get(exponent, Q(0)) + first * second
    return {exponent: value for exponent, value in answer.items() if value}


def embed_univariate(
    coefficients: list[Q], variable: int
) -> Polynomial:
    answer = {}
    for degree, coefficient in enumerate(coefficients):
        exponent = [0, 0, 0]
        exponent[variable] = degree
        if coefficient:
            answer[tuple(exponent)] = coefficient
    return answer


@lru_cache(maxsize=None)
def gegenbauer(dimension: int, degree: int) -> tuple[tuple[Q, ...], ...]:
    values: list[list[Q]] = [[Q(1)]]
    if degree == 0:
        return tuple(tuple(row) for row in values)
    values.append([Q(0), Q(1)])
    for k in range(2, degree + 1):
        shifted = [Q(0)] + values[k - 1]
        numerator = [Q(0)] * max(len(shifted), len(values[k - 2]))
        for index, value in enumerate(shifted):
            numerator[index] += (2 * k + dimension - 4) * value
        for index, value in enumerate(values[k - 2]):
            numerator[index] -= (k - 1) * value
        denominator = k + dimension - 3
        values.append([value / denominator for value in numerator])
    return tuple(tuple(row) for row in values)


def q_polynomials(degree: int) -> list[Polynomial]:
    delta = {(0, 0, 1): Q(1), (1, 1, 0): Q(-1)}
    radial = {
        (0, 0, 0): Q(1),
        (2, 0, 0): Q(-1),
        (0, 2, 0): Q(-1),
        (2, 2, 0): Q(1),
    }
    answer = [{(0, 0, 0): Q(1)}]
    if degree:
        answer.append(delta)
    for k in range(2, degree + 1):
        numerator = poly_add(
            poly_scale(poly_multiply(delta, answer[-1]), Q(2 * k)),
            poly_scale(poly_multiply(radial, answer[-2]), Q(-(k - 1))),
        )
        answer.append(poly_scale(numerator, Q(1, k + 1)))
    return answer


def load_blocks(path: str) -> list[list[list[Q]]]:
    data = json.loads(Path(path).read_text())
    blocks = []
    for expected_k, entry in enumerate(data["blocks"]):
        assert entry["k"] == expected_k
        denominator = int(entry["factor_denominator"])
        factor = entry["factor_integer_columns"]
        size = int(entry["size"])
        assert len(factor) == size
        rank = len(factor[0]) if size else 0
        assert all(len(row) == rank for row in factor)
        block = [
            [
                sum(
                    (Q(factor[i][column] * factor[j][column],
                       denominator * denominator)
                     for column in range(rank)),
                    Q(0),
                )
                for j in range(size)
            ]
            for i in range(size)
        ]
        blocks.append(block)
    return blocks


def factor_payload_digest(certificate: dict) -> str:
    payload = [
        {
            key: entry[key]
            for key in (
                "k",
                "size",
                "factor_denominator",
                "factor_integer_columns",
            )
        }
        for entry in certificate["blocks"]
    ]
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def cap_polynomial(blocks: list[list[list[Q]]]) -> Polynomial:
    degree = len(blocks) - 1
    q_values = q_polynomials(degree)
    answer: Polynomial = {}
    for k, block in enumerate(blocks):
        size = degree - k + 1
        assert len(block) == size
        basis = gegenbauer(5 + 2 * k, size - 1)
        for i in range(size):
            pi_u = embed_univariate(list(basis[i]), 0)
            pi_v = embed_univariate(list(basis[i]), 1)
            diagonal = poly_multiply(poly_multiply(pi_u, pi_v), q_values[k])
            answer = poly_add(answer, poly_scale(diagonal, block[i][i]))
            for j in range(i + 1, size):
                pj_u = embed_univariate(list(basis[j]), 0)
                pj_v = embed_univariate(list(basis[j]), 1)
                symmetric = poly_add(
                    poly_multiply(pi_u, pj_v),
                    poly_multiply(pj_u, pi_v),
                )
                term = poly_multiply(symmetric, q_values[k])
                answer = poly_add(answer, poly_scale(term, block[i][j]))
    return answer


def substitute_t_to_unit(poly: Polynomial) -> Polynomial:
    """Substitute t=-1+(3/2)s, retaining s as the third variable."""

    answer: Polynomial = {}
    for (i, j, k), coefficient in poly.items():
        for r in range(k + 1):
            value = coefficient * comb(k, r) * Q((-1) ** (k - r))
            value *= Q(3, 2) ** r
            exponent = i, j, r
            answer[exponent] = answer.get(exponent, Q(0)) + value
    return {exponent: value for exponent, value in answer.items() if value}


def power_to_bernstein(poly: Polynomial, degree: int) -> tuple[Q, ...]:
    side = degree + 1
    answer = [Q(0)] * (side**3)
    ratios = [
        [
            Q(comb(index, power), comb(degree, power))
            if index >= power else Q(0)
            for index in range(side)
        ]
        for power in range(side)
    ]
    for (a, b, c), coefficient in poly.items():
        assert a <= degree and b <= degree and c <= degree
        for i in range(a, side):
            first = coefficient * ratios[a][i]
            for j in range(b, side):
                second = first * ratios[b][j]
                base = (i * side + j) * side
                for k in range(c, side):
                    answer[base + k] += second * ratios[c][k]
    return tuple(answer)


def split_line(values: list[Q]) -> tuple[list[Q], list[Q]]:
    levels = [values]
    while len(levels[-1]) > 1:
        previous = levels[-1]
        levels.append(
            [(previous[index] + previous[index + 1]) / 2
             for index in range(len(previous) - 1)]
        )
    left = [level[0] for level in levels]
    right = [level[-1] for level in reversed(levels)]
    return left, right


def split_tensor(
    coefficients: tuple[Q, ...], degree: int, axis: int
) -> tuple[tuple[Q, ...], tuple[Q, ...]]:
    side = degree + 1
    left = [Q(0)] * len(coefficients)
    right = [Q(0)] * len(coefficients)

    def index(i: int, j: int, k: int) -> int:
        return (i * side + j) * side + k

    if axis == 0:
        for j in range(side):
            for k in range(side):
                line = [coefficients[index(i, j, k)] for i in range(side)]
                a, b = split_line(line)
                for i in range(side):
                    left[index(i, j, k)] = a[i]
                    right[index(i, j, k)] = b[i]
    elif axis == 1:
        for i in range(side):
            for k in range(side):
                line = [coefficients[index(i, j, k)] for j in range(side)]
                a, b = split_line(line)
                for j in range(side):
                    left[index(i, j, k)] = a[j]
                    right[index(i, j, k)] = b[j]
    else:
        for i in range(side):
            for j in range(side):
                line = [coefficients[index(i, j, k)] for k in range(side)]
                a, b = split_line(line)
                for k in range(side):
                    left[index(i, j, k)] = a[k]
                    right[index(i, j,k)] = b[k]
    return tuple(left), tuple(right)


def diagonal_polynomial(poly: Polynomial) -> dict[int, Q]:
    answer: dict[int, Q] = {}
    for (i, j, k), coefficient in poly.items():
        degree = i + j
        answer[degree] = answer.get(degree, Q(0)) + coefficient
        # t=1, so k does not change the monomial.
    return {degree: value for degree, value in answer.items() if value}


def univariate_power_to_bernstein(
    coefficients: dict[int, Q], degree: int
) -> tuple[Q, ...]:
    answer = [Q(0)] * (degree + 1)
    for power, value in coefficients.items():
        for index in range(power, degree + 1):
            answer[index] += value * Q(
                comb(index, power), comb(degree, power)
            )
    return tuple(answer)


def split_univariate(values: tuple[Q, ...]) -> tuple[tuple[Q, ...], tuple[Q, ...]]:
    left, right = split_line(list(values))
    return tuple(left), tuple(right)


def audit_univariate(values: tuple[Q, ...], max_depth: int) -> Counter:
    stack = [(values, 0)]
    counts: Counter = Counter()
    while stack:
        coefficients, depth = stack.pop()
        if min(coefficients) >= 0:
            counts[("proved", depth)] += 1
            continue
        if depth >= max_depth:
            raise RuntimeError(
                f"univariate audit failed at depth {depth}: "
                f"lower={min(coefficients)} upper={max(coefficients)}"
            )
        left, right = split_univariate(coefficients)
        stack.append((right, depth + 1))
        stack.append((left, depth + 1))
    return counts


def audit_domain(
    h_values: tuple[Q, ...],
    determinant_values: tuple[Q, ...],
    degree: int,
    max_depth: int,
    max_nodes: int,
    verbose: bool = False,
) -> tuple[Counter, str]:
    stack = [(h_values, determinant_values, 0, "")]
    counts: Counter = Counter()
    digest = hashlib.sha256()
    nodes = 0
    while stack:
        h_box, determinant_box, depth, path = stack.pop()
        nodes += 1
        if verbose and nodes % 1000 == 0:
            print(
                f"nodes={nodes} stack={len(stack)} depth={depth} "
                f"h_lower~{float(min(h_box)):.6g} "
                f"det_upper~{float(max(determinant_box)):.6g}",
                flush=True,
            )
        if nodes > max_nodes:
            raise RuntimeError(f"node limit {max_nodes} exhausted")
        if max(determinant_box) < 0:
            category = "infeasible"
        elif min(h_box) >= 0:
            category = "proved"
        else:
            if depth >= max_depth:
                raise RuntimeError(
                    f"domain audit failed path={path} depth={depth} "
                    f"h=[{min(h_box)},{max(h_box)}] "
                    f"det=[{min(determinant_box)},{max(determinant_box)}]"
                )
            axis = depth % 3
            h_left, h_right = split_tensor(h_box, degree, axis)
            d_left, d_right = split_tensor(determinant_box, degree, axis)
            stack.append((h_right, d_right, depth + 1, path + "1"))
            stack.append((h_left, d_left, depth + 1, path + "0"))
            continue
        counts[(category, depth)] += 1
        digest.update(f"{path}:{category}\n".encode())
    return counts, digest.hexdigest()


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    assert certificate["status"] == "COMPUTATIONALLY CERTIFIED"
    assert certificate["harmonic_degree"] == 10
    assert factor_payload_digest(certificate) == certificate[
        "factor_payload_sha256"
    ]
    assert certificate["factor_payload_sha256"] == (
        "d2c2bf6959c0d5be7c3ee182d4ddc8ae891c5e6df2d74632fb631623bc3585cc"
    )
    manifest = certificate["bernstein_tree_manifest"]
    assert manifest["leaf_digest_sha256"] == (
        "c4de17e5b741b824ed0b45d2af74a3927165db13c2ee717d8461efc78a028743"
    )
    assert manifest["total_leaves"] == 2483
    assert manifest["maximum_leaf_depth"] == 26
    off_target = Q(certificate["off_diagonal_upper_target"])
    diag_target = Q(certificate["diagonal_upper_target"])
    assert off_target == Q(-19, 20)
    assert diag_target == 33

    blocks = load_blocks(str(CERTIFICATE_PATH))
    degree = len(blocks) - 1
    polynomial = cap_polynomial(blocks)
    max_multidegree = tuple(
        max(exponent[index] for exponent in polynomial)
        for index in range(3)
    )
    assert degree == 10
    assert len(polynomial) == 506
    assert max_multidegree == (10, 10, 10)

    diagonal_margin = {
        0: diag_target
    }
    for power, coefficient in diagonal_polynomial(polynomial).items():
        diagonal_margin[power] = diagonal_margin.get(power, Q(0)) - coefficient
    diag_degree = max(diagonal_margin)
    diag_bernstein = univariate_power_to_bernstein(
        diagonal_margin, diag_degree
    )
    diag_counts = audit_univariate(diag_bernstein, 36)
    assert sum(diag_counts.values()) == 3

    h_polynomial = poly_scale(polynomial, Q(-1))
    h_polynomial[(0, 0, 0)] = (
        h_polynomial.get((0, 0, 0), Q(0)) + off_target
    )
    # h = off_target - F; h>=0 is the certified off-diagonal bound.
    h_unit = substitute_t_to_unit(h_polynomial)
    h_bernstein = power_to_bernstein(h_unit, degree)

    determinant = {
        (0, 0, 0): Q(1),
        (1, 1, 1): Q(2),
        (2, 0, 0): Q(-1),
        (0, 2, 0): Q(-1),
        (0, 0, 2): Q(-1),
    }
    determinant_unit = substitute_t_to_unit(determinant)
    determinant_bernstein = power_to_bernstein(determinant_unit, degree)
    counts, digest = audit_domain(
        h_bernstein,
        determinant_bernstein,
        degree,
        36,
        1_000_000,
    )
    total_leaves = sum(counts.values())
    maximum_leaf_depth = max(depth for (_, depth) in counts)
    category_counts = {
        category: sum(
            number
            for (current_category, _), number in counts.items()
            if current_category == category
        )
        for category in ("infeasible", "proved")
    }
    assert total_leaves == manifest["total_leaves"] == 2483
    assert maximum_leaf_depth == manifest["maximum_leaf_depth"] == 26
    assert category_counts == manifest["terminal_category_counts"]
    assert category_counts == {"infeasible": 1090, "proved": 1393}
    assert digest == manifest["leaf_digest_sha256"]

    # Scaling F by 20/19 converts the off-diagonal upper bound -19/20
    # into the standard cap-dual normalization -1.  Its diagonal bound is
    # 660/19, and the resulting objective is 679/19<36.
    scale = -Q(1) / off_target
    objective = Q(1) + scale * diag_target
    assert scale == Q(20, 19)
    assert objective == Q(certificate["resulting_real_objective"]) == Q(679, 19)
    assert objective < 36
    assert certificate["resulting_integer_bound"] == 35

    return {
        "status": "PASS",
        "harmonic_degree": degree,
        "power_terms": len(polynomial),
        "max_multidegree": max_multidegree,
        "diagonal_bernstein_leaves": sum(diag_counts.values()),
        "domain_bernstein_leaves": total_leaves,
        "maximum_leaf_depth": maximum_leaf_depth,
        "terminal_category_counts": category_counts,
        "leaf_digest_sha256": digest,
        "dual_objective": objective,
        "one_sided_kissing_upper_bound": 35,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
