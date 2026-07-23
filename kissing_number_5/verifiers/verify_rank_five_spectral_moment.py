#!/usr/bin/env python3
"""Exact checks for proofs/rank_five_spectral_moment.md.

Only Python's standard library is used.  All mathematical quantities are
computed with Fraction; floating-point arithmetic is absent.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
from typing import Optional


Q = Fraction
ROOT = Path(__file__).resolve().parents[1]


def parse_q(value: str | int) -> Q:
    return Q(value)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def power_sums(values: list[Q], maximum_degree: int = 6) -> dict[int, Q]:
    return {
        degree: sum(value**degree for value in values)
        for degree in range(1, maximum_degree + 1)
    }


def newton_e6_numerator(power: dict[int, Q]) -> Q:
    """Return 720 e_6 from power sums p_1,...,p_6."""
    p = power
    return (
        p[1] ** 6
        - 15 * p[1] ** 4 * p[2]
        + 40 * p[1] ** 3 * p[3]
        + 45 * p[1] ** 2 * p[2] ** 2
        - 90 * p[1] ** 2 * p[4]
        - 120 * p[1] * p[2] * p[3]
        + 144 * p[1] * p[5]
        - 15 * p[2] ** 3
        + 90 * p[2] * p[4]
        + 40 * p[3] ** 2
        - 120 * p[6]
    )


def elementary_six(values: list[Q]) -> Q:
    return sum(
        _product(subset)
        for subset in itertools.combinations(values, 6)
    )


def _product(values: tuple[Q, ...]) -> Q:
    result = Q(1)
    for value in values:
        result *= value
    return result


def spectral_quantities(
    eigenvalues: list[Q], rank_bound: int = 5
) -> tuple[Q, Q, Q, Q, Q, Q]:
    assert len(eigenvalues) <= rank_bound
    padded = eigenvalues + [Q(0)] * (rank_bound - len(eigenvalues))
    p1 = sum(padded)
    p2 = sum(value**2 for value in padded)
    p3 = sum(value**3 for value in padded)
    variance = p2 - p1**2 / rank_bound
    centered_third = (
        p3 - p1**3 / rank_bound**2
        - 3 * p1 * variance / rank_bound
    )
    squared_margin = 20 * centered_third**2 - 9 * variance**3
    return p1, p2, p3, variance, centered_third, squared_margin


def centered_moments(
    eigenvalues: list[Q], rank_bound: int = 5
) -> dict[int, Q]:
    """Power sums after centering a spectrum padded to rank_bound."""
    assert len(eigenvalues) <= rank_bound
    padded = eigenvalues + [Q(0)] * (rank_bound - len(eigenvalues))
    mean = sum(padded) / rank_bound
    return {
        degree: sum((value - mean) ** degree for value in padded)
        for degree in range(1, 7)
    }


def verify_centered_rank_five_moments(eigenvalues: list[Q]) -> None:
    """Check the exact quartic and sixth-moment inequalities."""
    centered = centered_moments(eigenvalues)
    assert centered[1] == 0
    variance = centered[2]
    third = centered[3]
    fourth = centered[4]
    sixth = centered[6]
    assert 30 * fourth >= 7 * variance**2
    assert 20 * fourth <= 13 * variance**2
    assert 5 * variance * fourth >= 5 * third**2 + variance**3
    assert (
        sixth
        == -variance**3 / 8
        + 3 * variance * fourth / 4
        + third**2 / 3
    )
    # This is the determinant of the moment Gram matrix for 1,z,z^3.
    assert (
        5 * variance * sixth
        - 5 * fourth**2
        - variance * third**2
        >= 0
    )


def matmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [
        [
            sum(a[i][h] * b[h][j] for h in range(len(b)))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def matrix_trace_power(matrix: list[list[Q]], degree: int) -> Q:
    power = [
        [Q(i == j) for j in range(len(matrix))]
        for i in range(len(matrix))
    ]
    for _ in range(degree):
        power = matmul(power, matrix)
    return sum(power[i][i] for i in range(len(matrix)))


def verify_four_cycle_expansion() -> dict[str, Q]:
    """Check the p4 partition formula on the exact 10-point cross polytope."""
    dimension = 5
    vectors: list[tuple[int, ...]] = []
    for coordinate in range(dimension):
        for sign in (-1, 1):
            vector = [0] * dimension
            vector[coordinate] = sign
            vectors.append(tuple(vector))
    size = len(vectors)
    gram = [
        [
            Q(sum(x * y for x, y in zip(a, b)))
            for b in vectors
        ]
        for a in vectors
    ]

    # The measures are normalized by 1/N, exactly as in the proof.
    pair_square = sum(
        gram[i][j] ** 2
        for i in range(size)
        for j in range(size)
        if i != j
    ) / size
    pair_fourth = sum(
        gram[i][j] ** 4
        for i in range(size)
        for j in range(size)
        if i != j
    ) / size
    triple_cycle = sum(
        gram[i][j] * gram[i][k] * gram[j][k]
        for i in range(size)
        for j in range(size)
        for k in range(size)
        if len({i, j, k}) == 3
    ) / size
    opposite_repeat = sum(
        gram[i][j] ** 2 * gram[i][k] ** 2
        for i in range(size)
        for j in range(size)
        for k in range(size)
        if len({i, j, k}) == 3
    ) / size
    distinct_four_cycle = sum(
        gram[i][j] * gram[j][k] * gram[k][ell] * gram[ell][i]
        for i in range(size)
        for j in range(size)
        for k in range(size)
        for ell in range(size)
        if len({i, j, k, ell}) == 4
    ) / size
    disjoint_matching = sum(
        gram[i][j] ** 2 * gram[k][ell] ** 2
        for i in range(size)
        for j in range(size)
        for k in range(size)
        for ell in range(size)
        if len({i, j, k, ell}) == 4
    ) / size

    determinant_integral = Q(0)
    for i in range(size):
        for j in range(size):
            for k in range(size):
                for ell in range(size):
                    if len({i, j, k, ell}) != 4:
                        continue
                    a = gram[i][j]
                    b = gram[i][k]
                    c = gram[i][ell]
                    d = gram[j][k]
                    e = gram[j][ell]
                    f = gram[k][ell]
                    determinant = (
                        1
                        - (a**2 + b**2 + c**2 + d**2 + e**2 + f**2)
                        + 2 * (a * b * d + a * c * e + b * c * f + d * e * f)
                        + (a**2 * f**2 + b**2 * e**2 + c**2 * d**2)
                        - 2 * (a * d * f * c + a * e * f * b + b * d * e * c)
                    )
                    assert 0 <= determinant <= 1
                    determinant_integral += determinant
    determinant_integral /= size

    mass = Q((size - 1) * (size - 2) * (size - 3))
    lift = Q((size - 2) * (size - 3))
    assert disjoint_matching == (
        size * pair_square**2
        - 4 * opposite_repeat
        - 2 * pair_fourth
    )
    assert determinant_integral == (
        mass
        - 6 * lift * pair_square
        + 8 * (size - 3) * triple_cycle
        + 3 * disjoint_matching
        - 6 * distinct_four_cycle
    )
    expanded = size * (
        1
        + 6 * pair_square
        + pair_fourth
        + 4 * triple_cycle
        + 2 * opposite_repeat
        + distinct_four_cycle
    )
    direct = matrix_trace_power(gram, 4)
    assert expanded == direct
    # The frame spectrum of the cross polytope is 2 with multiplicity five.
    assert direct == 5 * 2**4
    return {
        "pair_square": pair_square,
        "pair_fourth": pair_fourth,
        "triple_cycle": triple_cycle,
        "opposite_repeat": opposite_repeat,
        "distinct_four_cycle": distinct_four_cycle,
        "disjoint_matching": disjoint_matching,
        "determinant_integral": determinant_integral,
        "p4": direct,
    }


def verify_weighted_residual_pseudo(
    expected: dict[str, str]
) -> dict[str, Q]:
    """Apply the rank-five cut to the exact integral triple pseudo-incidence."""
    data = json.loads(
        (ROOT / "certificates" / "local_hybrid_pseudodistribution.json")
        .read_text()
    )
    assert data["size"] == 41
    nodes = [
        Q(atom["t_numerator"], atom["t_denominator"])
        for atom in data["atoms"]
    ]
    ordered_counts = [atom["ordered_count"] for atom in data["atoms"]]
    triple_counts = {
        (0, 0, 4): 275,
        (0, 1, 4): 30,
        (0, 2, 4): 508,
        (0, 3, 4): 2227,
        (1, 1, 4): 3,
        (1, 3, 4): 81,
        (2, 2, 2): 7,
        (2, 2, 3): 2066,
        (2, 2, 4): 224,
        (3, 3, 3): 227,
        (3, 3, 4): 3313,
        (3, 4, 4): 1033,
        (4, 4, 4): 666,
    }
    cardinality = Q(41)
    pair_square = sum(
        Q(count, 41) * node**2
        for count, node in zip(ordered_counts, nodes)
    )
    triple_cycle = sum(
        Q(6 * count, 41) * nodes[i] * nodes[j] * nodes[k]
        for (i, j, k), count in triple_counts.items()
    )
    p2 = cardinality * (1 + pair_square)
    p3 = cardinality * (1 + 3 * pair_square + triple_cycle)
    variance = p2 - cardinality**2 / 5
    centered_third = (
        p3 - cardinality**3 / 25
        - 3 * cardinality * variance / 5
    )
    violation = 20 * centered_third**2 - 9 * variance**3
    actual = {
        "pair_square_moment_A": pair_square,
        "triple_cycle_moment_T": triple_cycle,
        "gram_trace_p2": p2,
        "gram_trace_p3": p3,
        "spectral_variance_V": variance,
        "centered_third_moment_D": centered_third,
        "rank_five_squared_violation": violation,
    }
    assert actual == {key: parse_q(value) for key, value in expected.items()}
    assert centered_third > 0
    assert violation > 0
    return actual


def verify(certificate_path: Optional[Path] = None) -> dict[str, object]:
    if certificate_path is None:
        certificate_path = (
            ROOT / "certificates" / "rank_five_spectral_moment_certificate.json"
        )
    certificate = json.loads(certificate_path.read_text())
    assert certificate["schema"] == "rank-five-spectral-moment-barrier-v1"
    assert certificate["dimension"] == 5
    assert certificate["cardinality"] == 41
    assert parse_q(
        certificate["centered_quartic_lower_coefficient"]
    ) == Q(7, 30)
    assert parse_q(
        certificate["centered_quartic_upper_coefficient"]
    ) == Q(13, 20)

    pseudo_path = (
        ROOT / "certificates" / certificate["source_pseudodistribution"]
    )
    assert file_sha256(pseudo_path) == certificate["source_sha256"]
    pseudo = json.loads(pseudo_path.read_text())
    assert pseudo["cardinality"] == 41
    grid = [parse_q(value) for value in pseudo["grid"]]
    alpha = [parse_q(value) for value in pseudo["alpha"]]
    triples = [tuple(map(int, triple)) for triple in pseudo["triples"]]
    nu = [parse_q(value) for value in pseudo["nu"]]
    assert sum(alpha) == 40
    assert sum(nu) == 40 * 39

    pair_square_moment = sum(
        weight * q**2 for weight, q in zip(alpha, grid)
    )
    triple_cycle_moment = sum(
        weight * grid[i] * grid[j] * grid[k]
        for weight, (i, j, k) in zip(nu, triples)
    )
    assert pair_square_moment == parse_q(
        certificate["pair_square_moment_A"]
    )
    assert triple_cycle_moment == parse_q(
        certificate["triple_cycle_moment_T"]
    )

    cardinality = Q(41)
    p2 = cardinality * (1 + pair_square_moment)
    p3 = cardinality * (
        1 + 3 * pair_square_moment + triple_cycle_moment
    )
    variance = p2 - cardinality**2 / 5
    centered_third = (
        p3 - cardinality**3 / 25 - 3 * cardinality * variance / 5
    )
    violation = 20 * centered_third**2 - 9 * variance**3

    assert p2 == parse_q(certificate["gram_trace_p2"])
    assert p3 == parse_q(certificate["gram_trace_p3"])
    assert variance == parse_q(certificate["spectral_variance_V"])
    assert centered_third == parse_q(
        certificate["centered_third_moment_D"]
    )
    assert centered_third > 0
    assert violation == parse_q(
        certificate["rank_five_squared_violation"]
    )
    assert violation > 0

    delta = pair_square_moment - Q(36, 5)
    excess = (
        triple_cycle_moment - Q(1116, 25) - Q(108, 5) * delta
    )
    normalized_violation = 20 * excess**2 - 369 * delta**3
    assert delta == parse_q(certificate["normalized_delta"])
    assert excess == parse_q(certificate["normalized_excess_E"])
    assert excess > 0
    assert normalized_violation == parse_q(
        certificate["normalized_squared_violation"]
    )
    assert normalized_violation > 0

    # D5 is a tight frame: its five nonzero Gram eigenvalues are all 8.
    d5_spectrum = [
        parse_q(value) for value in certificate["d5_expected_spectrum"]
    ]
    d5 = spectral_quantities(d5_spectrum)
    assert d5[:5] == (Q(40), Q(320), Q(2560), Q(0), Q(0))
    assert d5[5] == 0
    assert newton_e6_numerator(power_sums(d5_spectrum)) == 0
    verify_centered_rank_five_moments(d5_spectrum)

    # The exact 11-code ±e_i plus (1,...,1)/sqrt(5) has frame spectrum
    # 3,2,2,2,2.  The pair bound is exact because 1/sqrt(5)<1/2 iff 4<5.
    assert 4 < 5
    sharp_spectrum = [
        parse_q(value)
        for value in certificate["sharp_small_code_frame_spectrum"]
    ]
    sharp = spectral_quantities(sharp_spectrum)
    assert sharp[:5] == (
        Q(11), Q(25), Q(59), Q(4, 5), Q(12, 25)
    )
    assert sharp[5] == 0
    assert newton_e6_numerator(power_sums(sharp_spectrum)) == 0
    verify_centered_rank_five_moments(sharp_spectrum)

    # Independently check Newton's formula on a genuine six-eigenvalue list,
    # where neither side vanishes.
    six_values = [Q(1), Q(2), Q(3), Q(4), Q(5), Q(6)]
    lhs = newton_e6_numerator(power_sums(six_values))
    rhs = 720 * elementary_six(six_values)
    assert lhs == rhs == 720 * 720

    # Adversarial exact tests include rank-deficient spectra, repeated
    # eigenvalues, a zero eigenvalue, and strongly skewed positive spectra.
    rational_spectra = [
        [Q(1)],
        [Q(1), Q(2)],
        [Q(0), Q(1), Q(2), Q(3), Q(4)],
        [Q(1, 7), Q(2, 5), Q(3, 2), Q(11, 3), Q(19, 4)],
        [Q(9), Q(31, 4), Q(31, 4), Q(31, 4), Q(31, 4)],
    ]
    for spectrum in rational_spectra:
        verify_centered_rank_five_moments(spectrum)
        assert newton_e6_numerator(power_sums(spectrum)) == 0

    four_cycle = verify_four_cycle_expansion()
    weighted_residual = verify_weighted_residual_pseudo(
        certificate["weighted_residual_pseudo"]
    )

    return {
        "status": "PASS",
        "pair_square_moment_A": str(pair_square_moment),
        "triple_cycle_moment_T": str(triple_cycle_moment),
        "spectral_variance_V": str(variance),
        "centered_third_moment_D": str(centered_third),
        "rank_five_squared_violation": str(violation),
        "normalized_squared_violation": str(normalized_violation),
        "d5_equality": True,
        "sharp_small_code_equality": True,
        "centered_quartic_bounds_checked": True,
        "centered_sixth_identity_checked": True,
        "cross_polytope_p4": str(four_cycle["p4"]),
        "weighted_residual_rank_violation": str(
            weighted_residual["rank_five_squared_violation"]
        ),
        "newton_e6_identity_checked": True,
        "conclusion": (
            "stored all-harmonic pseudo-measure violates a necessary "
            "rank-five spectral moment inequality"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
