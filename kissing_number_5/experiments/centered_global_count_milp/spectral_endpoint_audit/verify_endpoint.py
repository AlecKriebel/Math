#!/usr/bin/env python3
"""Exact audit of the centered quarter-grid rank-five endpoint.

The finite certificate checked here consists of integer edge, triangle, and
row-degree marginals.  It is deliberately not accepted as a labeled matrix
or a spherical code.  The mathematical contradiction for an actual endpoint
uses the separate theorem tau(4)=24; see ``proof.md``.

Only Python's standard library and ``fractions.Fraction`` are used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "endpoint_row_marginal_shadows.json"


class VerificationError(RuntimeError):
    """Raised when an exact certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def feasible_orbits(nodes: list[Q]) -> list[tuple[int, int, int]]:
    """All unordered quarter-grid triangle types on the closed Gram domain."""

    result = []
    for triple in itertools.combinations_with_replacement(
        range(len(nodes)), 3
    ):
        u, v, t = (nodes[index] for index in triple)
        determinant = 1 + 2 * u * v * t - u * u - v * v - t * t
        if determinant >= 0:
            result.append(triple)
    return result


def incident_pair_coefficient(
    triple: tuple[int, int, int], first: int, second: int
) -> int:
    """Contribution of one vertex triple to sum_v d_first(v)d_second(v)."""

    ordered = set(itertools.permutations(triple))
    placements = sum(
        left == first and right == second
        for left, right, _opposite in ordered
    )
    numerator = 6 * placements
    require(
        numerator % len(ordered) == 0,
        "nonintegral incident-pair coefficient",
    )
    return numerator // len(ordered)


def row_second_moments(
    edge_counts: list[int],
    triple_counts: list[int],
    orbits: list[tuple[int, int, int]],
) -> dict[tuple[int, int], int]:
    result = {}
    for first in range(7):
        for second in range(first, 7):
            value = 2 * edge_counts[first] if first == second else 0
            value += sum(
                count
                * incident_pair_coefficient(triple, first, second)
                for triple, count in zip(orbits, triple_counts)
            )
            result[first, second] = value
    return result


def q_square_moment(
    moments: dict[tuple[int, int], int], colors: list[int]
) -> int:
    """Return sum_v (sum_k k^2 d_k(v))^2 from degree moments."""

    total = 0
    for first, color_first in enumerate(colors):
        for second in range(first, len(colors)):
            color_second = colors[second]
            coefficient = color_first**2 * color_second**2
            if first != second:
                coefficient *= 2
            total += coefficient * moments[first, second]
    return total


def verify_shadow(
    shadow: dict[str, object],
    edge_counts: list[int],
    colors: list[int],
    orbits: list[tuple[int, int, int]],
) -> dict[str, object]:
    triple_counts = shadow["triple_counts"]
    require(
        isinstance(triple_counts, list)
        and len(triple_counts) == len(orbits),
        "wrong triple-count vector length",
    )
    require(
        all(isinstance(value, int) and value >= 0 for value in triple_counts),
        "triple counts must be nonnegative integers",
    )
    require(sum(triple_counts) == 10660, "wrong total number of triples")

    for index in range(7):
        incidence = sum(
            count * triple.count(index)
            for triple, count in zip(orbits, triple_counts)
        )
        require(
            incidence == 39 * edge_counts[index],
            f"wrong edge-triple incidence for color {colors[index]}",
        )

    triangle_product_sum = sum(
        count
        * colors[triple[0]]
        * colors[triple[1]]
        * colors[triple[2]]
        for triple, count in zip(orbits, triple_counts)
    )
    require(
        triangle_product_sum == 19534,
        "shadow does not lie at the forced cubic endpoint",
    )

    records = shadow["row_type_counts"]
    require(isinstance(records, list), "row_type_counts must be a list")
    total_rows = 0
    first_moments = [0] * 7
    second_moments = {
        (first, second): 0
        for first in range(7)
        for second in range(first, 7)
    }
    z_square_counts: Counter[Q] = Counter()
    seen_degrees: set[tuple[int, ...]] = set()

    for record in records:
        degree = tuple(record["degree"])
        count = record["count"]
        z_square = Q(record["z_square"])
        require(
            len(degree) == 7
            and all(isinstance(value, int) and value >= 0 for value in degree),
            "invalid row degree",
        )
        require(degree not in seen_degrees, "duplicate row type")
        seen_degrees.add(degree)
        require(
            isinstance(count, int) and count > 0,
            "row multiplicity must be a positive integer",
        )
        require(sum(degree) == 40, "row degree does not sum to 40")
        require(
            sum(color * value for color, value in zip(colors, degree)) == -4,
            "row degree violates centering",
        )
        require(sum(degree[:4]) >= 7, "row violates robust negative depth")
        require(sum(degree[5:]) >= 6, "row violates robust positive depth")
        require(degree[6] <= 15, "row violates contact-degree bound")
        require(degree[1] <= 5, "row violates the -3/4-neighbour bound")
        if degree[0]:
            require(
                degree[1] == 0
                and degree[2] == degree[6]
                and degree[3] == degree[5],
                "antipodal row symmetry is missing",
            )

        q_value = sum(
            color * color * value for color, value in zip(colors, degree)
        )
        require(
            Q(q_value) == 116 - 4 * z_square,
            "row energy does not match its z-square",
        )
        require(
            q_value % 2 == 0,
            "centered integer row has odd square energy",
        )

        total_rows += count
        z_square_counts[z_square] += count
        for index, value in enumerate(degree):
            first_moments[index] += count * value
        for first in range(7):
            for second in range(first, 7):
                second_moments[first, second] += (
                    count * degree[first] * degree[second]
                )

    require(total_rows == 41, "wrong number of row copies")
    require(
        first_moments == [2 * value for value in edge_counts],
        "row first moments do not match edge counts",
    )
    target_second = row_second_moments(
        edge_counts, triple_counts, orbits
    )
    require(
        second_moments == target_second,
        "row second moments do not match triangle counts",
    )

    stored_z_counts = {
        Q(key): value for key, value in shadow["z_square_counts"].items()
    }
    require(
        dict(z_square_counts) == stored_z_counts,
        "stored z-square counts do not match row copies",
    )
    require(
        sum(square * count for square, count in z_square_counts.items())
        == 8,
        "z-square mass is not 8",
    )

    case = shadow["case"]
    if case == "rational_square_class":
        require(
            stored_z_counts == {Q(0): 33, Q(1): 8},
            "wrong rational-square-class distribution",
        )
        require(
            shadow["sign_counts_for_centering"] == {"+1": 4, "-1": 4},
            "wrong rational-class sign counts",
        )
    elif case == "twice_rational_square_class":
        require(
            stored_z_counts == {Q(0): 25, Q(1, 2): 16},
            "wrong twice-rational-square-class distribution",
        )
        require(
            shadow["sign_counts_for_centering"]
            == {"+1/sqrt(2)": 8, "-1/sqrt(2)": 8},
            "wrong twice-rational-class sign counts",
        )
    else:
        raise VerificationError(f"unknown endpoint case {case!r}")

    product_y = 3636864 - 2160 * 2362 + 75 * triangle_product_sum
    require(product_y == -6, "wrong cubic endpoint Y")
    return {
        "case": case,
        "active_row_types": len(records),
        "active_triangle_types": sum(value > 0 for value in triple_counts),
        "row_q_square_moment": q_square_moment(
            second_moments, colors
        ),
        "zero_height_count": stored_z_counts[Q(0)],
    }


def allowable_z_square_distributions() -> set[tuple[tuple[Q, int], ...]]:
    """Enumerate the square-class and row-parity alternatives.

    The matrix identity gives z_i^2 in
    {0,1/4,1/2,3/4,1}; rational pair products force all nonzero
    squares into one rational square class.  Centered integer rows force
    4*z_i^2 to be even.
    """

    square_classes = (
        (Q(1, 4), Q(1)),
        (Q(1, 2),),
        (Q(3, 4),),
    )
    outcomes: set[tuple[tuple[Q, int], ...]] = set()
    for square_class in square_classes:
        allowed = [
            square
            for square in square_class
            if int(4 * square) % 2 == 0
        ]
        if len(allowed) != 1:
            continue
        square = allowed[0]
        count = Q(8) / square
        if count.denominator != 1 or not 0 <= count <= 41:
            continue
        nonzero = int(count)
        outcomes.add(((Q(0), 41 - nonzero), (square, nonzero)))
    return outcomes


def verify(
    certificate_path: Path = CERTIFICATE,
    source_path: Path | None = None,
) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    require(
        certificate["schema"]
        == "kissing5.centered_quarter_spectral_endpoint_row_marginal_shadows.v1",
        "wrong certificate schema",
    )
    require(
        certificate["status"]
        == "EXACT INTEGER MARGINAL SHADOWS; NOT MATRICES OR SPHERICAL CODES",
        "unsafe certificate status",
    )
    require(certificate["dimension"] == 5, "wrong dimension")
    require(certificate["cardinality"] == 41, "wrong cardinality")
    require(
        certificate["grid_numerators"] == list(range(-4, 3))
        and certificate["grid_denominator"] == 4,
        "wrong quarter grid",
    )

    colors = certificate["grid_numerators"]
    nodes = [Q(color, 4) for color in colors]
    orbits = feasible_orbits(nodes)
    require(len(orbits) == 51, "wrong feasible triangle-orbit count")

    edge_counts = certificate["edge_counts"]
    require(
        len(edge_counts) == 7
        and all(isinstance(value, int) and value >= 0 for value in edge_counts),
        "invalid edge counts",
    )
    require(sum(edge_counts) == 820, "wrong edge-count total")
    require(
        sum(color * count for color, count in zip(colors, edge_counts))
        == -82,
        "edge counts violate global centering",
    )
    edge_square_sum = sum(
        color * color * count
        for color, count in zip(colors, edge_counts)
    )
    require(edge_square_sum == 2362, "wrong edge-square sum Q")

    x_value = 5 * edge_square_sum - 11808
    require(x_value == 2, "wrong X=40V")
    residue = (3636864 - 2160 * edge_square_sum) % 75
    possible_y = [
        value
        for value in range(-6, 7)
        if 2 * value * value <= 9 * x_value**3
        and value % 75 == residue
    ]
    require(
        possible_y == [-6],
        "spectral inequality and cubic integrality do not force Y=-6",
    )
    y_value = possible_y[0]
    v_value = Q(x_value, 40)
    d_value = Q(y_value, 800)
    require(
        20 * d_value**2 == 9 * v_value**3,
        "endpoint does not saturate the five-eigenvalue skew inequality",
    )

    endpoint = certificate["endpoint"]
    require(endpoint["edge_square_sum_Q"] == 2362, "stored Q mismatch")
    require(endpoint["X_equals_40V"] == 2, "stored X mismatch")
    require(endpoint["forced_Y_equals_800D"] == -6, "stored Y mismatch")
    require(
        endpoint["triangle_product_sum_P"] == 19534,
        "stored P mismatch",
    )
    spectrum = [Q(value) for value in endpoint["spectrum"]]
    require(
        spectrum == [Q(8)] + [Q(33, 4)] * 4,
        "wrong equality spectrum",
    )
    require(sum(spectrum) == 41, "spectrum has wrong trace")
    require(
        sum(value * value for value in spectrum)
        == Q(1345, 4),
        "spectrum has wrong second trace",
    )
    require(
        sum(value**3 for value in spectrum) == Q(44129, 16),
        "spectrum has wrong third trace",
    )

    outcomes = allowable_z_square_distributions()
    expected_outcomes = {
        ((Q(0), 33), (Q(1), 8)),
        ((Q(0), 25), (Q(1, 2), 16)),
    }
    require(outcomes == expected_outcomes, "wrong z-square alternatives")
    require(
        all(dict(outcome)[Q(0)] > 24 for outcome in outcomes),
        "an endpoint alternative lacks the tau(4) contradiction",
    )

    if source_path is None:
        source_path = (
            certificate_path.parent / certificate["source_result"]
        ).resolve()
    source_bytes = source_path.read_bytes()
    require(
        hashlib.sha256(source_bytes).hexdigest()
        == certificate["source_result_sha256"],
        "source discovery result hash mismatch",
    )
    source = json.loads(source_bytes)
    require(
        source["final_edge_counts"] == edge_counts,
        "source edge counts differ",
    )
    source_triples = source["final_triple_counts"]
    require(
        len(source_triples) == len(orbits),
        "source triple vector has wrong length",
    )
    source_product = sum(
        count
        * colors[triple[0]]
        * colors[triple[1]]
        * colors[triple[2]]
        for triple, count in zip(orbits, source_triples)
    )
    require(source_product == 19534, "source triple product mismatch")
    source_y = 3636864 - 2160 * edge_square_sum + 75 * source_product
    require(source_y == -6, "source is not at the cubic endpoint")
    source_moments = row_second_moments(
        edge_counts, source_triples, orbits
    )
    source_q2 = q_square_moment(source_moments, colors)
    require(
        source_q2 == 555192,
        "unexpected source row-q second moment",
    )
    source_active_q2 = 0
    for record in source["iterations"][0]["active_degree_types"]:
        degree = record["degree"]
        q_value = sum(
            color * color * value for color, value in zip(colors, degree)
        )
        source_active_q2 += record["count"] * q_value**2
    require(
        source_active_q2 == source_q2,
        "source active row types do not match its triple moments",
    )
    require(
        source_q2 not in {544400, 544336},
        "source row types accidentally satisfy an endpoint z alternative",
    )

    shadows = [
        verify_shadow(shadow, edge_counts, colors, orbits)
        for shadow in certificate["shadows"]
    ]
    require(len(shadows) == 2, "expected two marginal shadows")
    require(
        {record["case"] for record in shadows}
        == {"rational_square_class", "twice_rational_square_class"},
        "missing endpoint shadow case",
    )
    require(
        {record["row_q_square_moment"] for record in shadows}
        == {544400, 544336},
        "wrong endpoint row-energy second moments",
    )

    return {
        "status": "verified exact endpoint audit",
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "edge_square_sum_Q": edge_square_sum,
        "X_equals_40V": x_value,
        "Y_equals_800D": y_value,
        "spectrum": [str(value) for value in spectrum],
        "source_row_q_square_moment": source_q2,
        "marginal_shadows": shadows,
        "geometric_obstruction": (
            "each z-square alternative has at least 25 zero-height points; "
            "tau(4)=24 rules out an actual Gram realization"
        ),
    }


def main() -> None:
    try:
        result = verify()
    except (KeyError, TypeError, ValueError, VerificationError) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
