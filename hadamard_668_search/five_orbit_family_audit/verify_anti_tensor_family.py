#!/usr/bin/env python3
"""Exact anti-tensor placement-family audit on all five shell-two orbits.

The family is

    u_X(j,s) = P_X(j mod 3,s) + h_j F_X(j mod 6) G_X(s),

where P_X has total degree at most two over F_3, h_j is +1 on classes
0,...,5 and -1 on classes 6,...,11, F_X is arbitrary, and G_X runs
projectively over the nonconstant nonzero functions F_3 -> F_3.

For fixed projective row directions (G_A,G_B), this is a linear feature
family.  There are exactly 12^2=144 charts.  We solve the first placement
digit on every chart, deduplicate their affine images, and evaluate the
complete union in the exact second placement digit.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SHELL_TWO = SEARCH_ROOT / "shell_two_exact"
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
STRUCTURED = SEARCH_ROOT / "structured_phase_families"
sys.path.insert(0, str(SHELL_TWO))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(STRUCTURED))
sys.path.insert(0, str(SEARCH_ROOT))

try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised by portable fallback
    np = None

import verify_f27_submodule_families as f27  # noqa: E402
import verify_structured_phase_families as structured  # noqa: E402
from verify_shell_two_exact_orbits import CANDIDATES  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    direct_first_digits,
    first_digit_equations,
    profiles_from_ids,
    symbolic_first_digits,
)
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
)
from verify_phase_second_digit import (  # noqa: E402
    direct_second_digits,
    second_digit_term_data,
    symbolic_second_digits,
)


MODULUS = 3
TRIT_COUNT = 54
EXPECTED_SEMANTIC_SHA256 = (
    "39de8bf9d6e60ee078e7710daa81d3546e519589a769bbd2c5579693c6203bef"
)

Vector = tuple[int, ...]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def packed_hash(points: Sequence[bytes]) -> str:
    if any(len(point) != TRIT_COUNT for point in points):
        raise AssertionError("packed trit record changed width")
    return sha256(b"".join(points)).hexdigest()


def canonical_projective(vector: Sequence[int]) -> Vector:
    """Normalize a nonzero ternary vector by its first nonzero entry."""

    for value in vector:
        if value % MODULUS:
            inverse = 1 if value % MODULUS == 1 else 2
            return tuple(inverse * int(entry) % MODULUS for entry in vector)
    raise ValueError("zero vector has no projective normalization")


def nonconstant_row_directions() -> tuple[Vector, ...]:
    directions = {
        canonical_projective(vector)
        for vector in product(range(MODULUS), repeat=3)
        if any(vector)
    }
    result = tuple(sorted(
        vector for vector in directions if len(set(vector)) > 1
    ))
    if len(directions) != 13 or len(result) != 12:
        raise AssertionError("P^2(F_3) row-direction census changed")
    return result


def anti_tensor_features(row_direction: Sequence[int]):
    """Return the twelve local features P(x,s)+h F(z)G(s)."""

    if tuple(row_direction) not in nonconstant_row_directions():
        raise ValueError("row direction is not a canonical nonconstant line")

    def features(coordinate: tuple[int, int, int]) -> Vector:
        _, class_index, residue = coordinate
        quadratic = structured.quadratic_c3_features(coordinate)
        opposite = structured.opposite_sign(class_index)
        class_residue = class_index % 6
        tensor = tuple(
            opposite
            * int(row_direction[residue])
            * int(class_residue == value)
            for value in range(6)
        )
        return quadratic + tensor

    return features


def chart(
    direction_a: Sequence[int],
    direction_b: Sequence[int],
) -> structured.MixedFamily:
    labels = (
        "1", "x", "s", "x^2", "x*s", "s^2",
        "h*G(s)*1[z=0]",
        "h*G(s)*1[z=1]",
        "h*G(s)*1[z=2]",
        "h*G(s)*1[z=3]",
        "h*G(s)*1[z=4]",
        "h*G(s)*1[z=5]",
    )
    return structured.MixedFamily(
        "opposite_rank_one_anti_tensor",
        (
            "Channelwise quadratic background plus a nonconstant "
            "rank-one opposite-class x row-residue tensor."
        ),
        (labels, labels),
        (
            anti_tensor_features(direction_a),
            anti_tensor_features(direction_b),
        ),
    )


def encoded_affine_points(
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> Iterable[bytes]:
    """Yield every affine point as a fixed-width byte record."""

    if np is None:
        for point in structured.affine_points(origin, basis):
            yield bytes(point)
        return

    dimension = len(basis)
    if dimension == 0:
        yield bytes(origin)
        return
    coefficients = np.indices(
        (MODULUS,) * dimension,
        dtype=np.int8,
    ).reshape(dimension, -1).T
    points = (
        coefficients @ np.asarray(basis, dtype=np.int8)
        + np.asarray(origin, dtype=np.int8)
    ) % MODULUS
    for point in points:
        yield point.tobytes()


def vectorized_second_digits(
    term_data: Sequence[tuple[Sequence[object], int]],
    points: Sequence[bytes],
) -> tuple[tuple[int, ...], ...]:
    """Evaluate all second digits, using NumPy when it is available."""

    if np is None:
        return tuple(
            symbolic_second_digits(term_data, tuple(point))
            for point in points
        )

    matrix = np.frombuffer(
        b"".join(points), dtype=np.uint8
    ).reshape(-1, TRIT_COUNT)
    result = np.empty((len(points), len(term_data)), dtype=np.int8)
    for row_index, (terms, constant_at_zero) in enumerate(term_data):
        values = np.full(
            len(points), 2 * (constant_at_zero // 3), dtype=np.int32
        )
        for term in terms:
            exponent = np.full(
                len(points), term.constant, dtype=np.int16
            )
            for variable, coefficient in term.coefficients:
                exponent += coefficient * matrix[:, variable]
            exponent %= MODULUS
            values += term.sign * (
                2 * exponent * exponent + exponent
            )
        result[:, row_index] = values % MODULUS
    return tuple(tuple(int(value) for value in row) for row in result)


def named_feature_sets(
    coordinates: Sequence[tuple[int, int, int]],
    equations: Sequence[object],
) -> tuple[dict[str, set[bytes]], set[bytes]]:
    """Reconstruct the seven previously certified linear-feature sets."""

    per_family: dict[str, set[bytes]] = {}
    union: set[bytes] = set()
    for family in structured.FAMILIES:
        features = family.feature_matrix(coordinates)
        restricted = structured.compose_first_digit(equations, features)
        origin, basis, _ = structured.affine_image(restricted, features)
        points: set[bytes] = set()
        if origin is not None and basis is not None:
            points.update(encoded_affine_points(origin, basis))
        per_family[family.name] = points
        union.update(points)
    return per_family, union


def f27_placements(
    profiles: Sequence[Sequence[Sequence[int]]],
    submodules: Sequence[dict[str, object]],
) -> set[bytes]:
    """Reconstruct the complete prior F_27-minimal-submodule union."""

    coordinates = active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    equation_rows = augmented_system(first_digit_equations(profiles))

    channel_bases: dict[tuple[int, int], tuple[Vector, ...]] = {}
    for submodule_index, record in enumerate(submodules):
        submodule = record["basis"]
        if not isinstance(submodule, tuple):
            raise AssertionError("F27 basis representation changed")
        for channel in range(2):
            embedded = []
            for residue in range(3):
                embedded.extend(f27.slice_intersection_basis(
                    profiles,
                    coordinate_index,
                    channel,
                    residue,
                    submodule,
                ))
            channel_bases[(submodule_index, channel)] = (
                structured.independent_span(embedded)
            )

    placements: set[bytes] = set()
    for submodule_a in range(len(submodules)):
        for submodule_b in range(len(submodules)):
            basis = structured.independent_span(
                channel_bases[(submodule_a, 0)]
                + channel_bases[(submodule_b, 1)]
            )
            restricted = f27.compose_first_digit(equation_rows, basis)
            affine = f27.affine_trit_space(restricted, basis)
            if affine is not None:
                placements.update(encoded_affine_points(*affine))
    return placements


def supergroup_memberships(
    profiles: Sequence[Sequence[Sequence[int]]],
    points: Sequence[bytes],
) -> tuple[dict[str, set[bytes]], set[bytes]]:
    """Return exact fixed-point sets for the five proper supergroups."""

    per_group: dict[str, set[bytes]] = {}
    union: set[bytes] = set()
    for identifier, generator in structured.SUPERGROUP_GENERATORS:
        constraints = structured.multiplier_constraints(
            profiles, generator
        )
        fixed = {
            point for point in points
            if structured.point_satisfies_constraints(
                tuple(point), constraints
            )
        }
        per_group[identifier] = fixed
        union.update(fixed)
    return per_group, union


def audit_profile(
    candidate: Sequence[object],
    row_directions: Sequence[Vector],
    submodules: Sequence[dict[str, object]],
) -> dict[str, object]:
    label, partition, target, identifiers_a, identifiers_b = candidate
    profiles = profiles_from_ids(identifiers_a, identifiers_b)
    coordinates = active_trit_coordinates(profiles)
    if len(coordinates) != TRIT_COUNT:
        raise AssertionError("shell-two placement dimension changed")
    equations = first_digit_equations(profiles)

    placements: set[bytes] = set()
    dimension_histogram: Counter[int] = Counter()
    inconsistent_charts = 0
    affine_point_incidences = 0
    chart_records = []
    for direction_a in row_directions:
        for direction_b in row_directions:
            family = chart(direction_a, direction_b)
            features = family.feature_matrix(coordinates)
            restricted = structured.compose_first_digit(
                equations, features
            )
            coefficient_rank = structured.matrix_rank(
                tuple(row[:-1] for row in restricted)
            )
            augmented_rank = structured.matrix_rank(restricted)
            origin, basis, _ = structured.affine_image(
                restricted, features
            )
            if origin is None or basis is None:
                if coefficient_rank == augmented_rank:
                    raise AssertionError("consistent chart lost affine image")
                inconsistent_charts += 1
                chart_records.append((
                    tuple(direction_a),
                    tuple(direction_b),
                    coefficient_rank,
                    augmented_rank,
                    None,
                ))
                continue
            if coefficient_rank != augmented_rank:
                raise AssertionError("inconsistent chart acquired an image")
            dimension = len(basis)
            dimension_histogram[dimension] += 1
            incidence = MODULUS ** dimension
            affine_point_incidences += incidence
            chart_points = tuple(encoded_affine_points(origin, basis))
            if len(chart_points) != incidence:
                raise AssertionError("affine chart enumeration changed")
            placements.update(chart_points)
            chart_records.append((
                tuple(direction_a),
                tuple(direction_b),
                coefficient_rank,
                augmented_rank,
                dimension,
            ))

    ordered = tuple(sorted(placements))
    if not ordered:
        raise AssertionError("anti-tensor family unexpectedly empty")
    residuals = vectorized_second_digits(
        second_digit_term_data(profiles), ordered
    )
    zero_rows = tuple(
        sum(value == 0 for value in residual) for residual in residuals
    )
    histogram = Counter(zero_rows)
    maximum_zero_rows = max(zero_rows)
    nearest_index = zero_rows.index(maximum_zero_rows)
    nearest = tuple(ordered[nearest_index])
    nearest_residual = residuals[nearest_index]
    second_digit_survivors = tuple(
        tuple(ordered[index])
        for index, count in enumerate(zero_rows)
        if count == 20
    )

    # Detached exact-Eisenstein checks validate both accelerated evaluators.
    replay_indices = sorted({
        0, len(ordered) // 2, len(ordered) - 1, nearest_index
    })
    for index in replay_indices:
        point = tuple(ordered[index])
        if symbolic_first_digits(equations, point) != (0,) * 20:
            raise AssertionError("affine union point failed digit one")
        if direct_first_digits(profiles, point) != (0,) * 20:
            raise AssertionError("union point failed direct digit-one replay")
        if symbolic_second_digits(
            second_digit_term_data(profiles), point
        ) != residuals[index]:
            raise AssertionError("accelerated second digit disagrees")
        if direct_second_digits(profiles, point) != residuals[index]:
            raise AssertionError("direct second digit disagrees")

    prior_by_name, prior_feature_union = named_feature_sets(
        coordinates, equations
    )
    f27_points = f27_placements(profiles, submodules)
    prior_union = prior_feature_union | f27_points
    fixed_by_group, fixed_union = supergroup_memberships(
        profiles, ordered
    )
    genuinely_new = placements - prior_union
    proper_supergroup_free = placements - fixed_union
    new_and_supergroup_free = genuinely_new - fixed_union

    if second_digit_survivors:
        raise AssertionError(
            "certificate schema assumes the measured digit-two exclusion"
        )
    if genuinely_new != new_and_supergroup_free:
        raise AssertionError(
            "a genuinely new anti-tensor point gained a known supergroup"
        )

    return {
        "profile": label,
        "partition": partition,
        "target": target,
        "active_trits": len(coordinates),
        "charts": len(row_directions) ** 2,
        "consistent_charts": (
            len(row_directions) ** 2 - inconsistent_charts
        ),
        "inconsistent_charts": inconsistent_charts,
        "solution_dimension_histogram": {
            str(key): dimension_histogram[key]
            for key in sorted(dimension_histogram)
        },
        "affine_point_incidences": affine_point_incidences,
        "distinct_first_digit_placements": len(placements),
        "first_digit_union_packed_sha256": packed_hash(ordered),
        "chart_records_sha256": compact_hash(chart_records),
        "prior_named_family_intersections": {
            name: len(placements & family_points)
            for name, family_points in prior_by_name.items()
        },
        "prior_named_family_union_intersection": len(
            placements & prior_feature_union
        ),
        "prior_f27_intersection": len(placements & f27_points),
        "prior_complete_union_intersection": len(
            placements & prior_union
        ),
        "genuinely_new_first_digit_placements": len(genuinely_new),
        "proper_supergroup_fixed_counts": {
            identifier: len(fixed_by_group[identifier])
            for identifier, _ in structured.SUPERGROUP_GENERATORS
        },
        "proper_supergroup_free_placements": len(
            proper_supergroup_free
        ),
        "new_and_proper_supergroup_free": len(
            new_and_supergroup_free
        ),
        "second_digit_zero_row_histogram": {
            str(key): histogram[key] for key in sorted(histogram)
        },
        "maximum_second_digit_zero_rows": maximum_zero_rows,
        "nearest_trits": nearest,
        "nearest_trit_sha256": compact_hash(nearest),
        "nearest_second_digit_residual": nearest_residual,
        "second_digit_survivors": len(second_digit_survivors),
        "direct_replay_points_checked": len(replay_indices),
    }


def build_certificate() -> dict[str, object]:
    row_directions = nonconstant_row_directions()
    submodules = f27.minimal_submodules()
    audits = tuple(
        audit_profile(candidate, row_directions, submodules)
        for candidate in CANDIDATES
    )
    return {
        "schema": "lp333-shell-two-opposite-rank-one-anti-tensor-v1",
        "scope": (
            "Exact profile-conditioned placement-digit audit on the five "
            "certified shell-two profiles. It is not a placement witness, "
            "an LP(333), or an H(668)."
        ),
        "family": (
            "u_X(j,s)=P_X(j mod 3,s)+h_j F_X(j mod 6)G_X(s), "
            "deg(P_X)<=2, F_X arbitrary, and G_X a nonconstant "
            "projective row function."
        ),
        "projective_row_directions": row_directions,
        "projective_row_direction_sha256": compact_hash(row_directions),
        "charts_per_profile": len(row_directions) ** 2,
        "audits": audits,
        "totals": {
            "profiles": len(audits),
            "charts": sum(int(audit["charts"]) for audit in audits),
            "consistent_charts": sum(
                int(audit["consistent_charts"]) for audit in audits
            ),
            "affine_point_incidences": sum(
                int(audit["affine_point_incidences"])
                for audit in audits
            ),
            "distinct_first_digit_placements": sum(
                int(audit["distinct_first_digit_placements"])
                for audit in audits
            ),
            "genuinely_new_first_digit_placements": sum(
                int(audit["genuinely_new_first_digit_placements"])
                for audit in audits
            ),
            "new_and_proper_supergroup_free": sum(
                int(audit["new_and_proper_supergroup_free"])
                for audit in audits
            ),
            "second_digit_survivors": sum(
                int(audit["second_digit_survivors"])
                for audit in audits
            ),
        },
        "finish_line": (
            "The complete 144-chart family has zero remaining unchecked "
            "points through placement digit two."
        ),
        "claim_boundary": {
            "profile_level": (
                "The five input profiles are the previously certified "
                "exact profile-zero orbit representatives."
            ),
            "digit_level": (
                "Every point in this family that passes placement digit "
                "one has been checked at placement digit two."
            ),
            "placement": (
                "No member passes digit two; no primitive-nine placement "
                "is constructed or excluded outside this family."
            ),
            "lp333": "No Legendre pair of length 333 is claimed.",
            "h668": "No Hadamard matrix of order 668 is claimed.",
        },
    }


def compact_certificate(certificate: dict[str, object]) -> dict[str, object]:
    """Retain the theorem's pinned census without storing 517,109 points."""

    audits = certificate["audits"]
    if not isinstance(audits, tuple):
        raise AssertionError("generated audit representation changed")
    return {
        "schema": "lp333-shell-two-opposite-rank-one-anti-tensor-compact-v1",
        "full_semantic_sha256": compact_hash(certificate),
        "projective_row_direction_sha256": (
            certificate["projective_row_direction_sha256"]
        ),
        "totals": certificate["totals"],
        "profiles": tuple({
            "profile": audit["profile"],
            "consistent_charts": audit["consistent_charts"],
            "inconsistent_charts": audit["inconsistent_charts"],
            "solution_dimension_histogram": (
                audit["solution_dimension_histogram"]
            ),
            "affine_point_incidences": audit["affine_point_incidences"],
            "distinct_first_digit_placements": (
                audit["distinct_first_digit_placements"]
            ),
            "first_digit_union_packed_sha256": (
                audit["first_digit_union_packed_sha256"]
            ),
            "chart_records_sha256": audit["chart_records_sha256"],
            "prior_complete_union_intersection": (
                audit["prior_complete_union_intersection"]
            ),
            "genuinely_new_first_digit_placements": (
                audit["genuinely_new_first_digit_placements"]
            ),
            "proper_supergroup_fixed_counts": (
                audit["proper_supergroup_fixed_counts"]
            ),
            "second_digit_zero_row_histogram": (
                audit["second_digit_zero_row_histogram"]
            ),
            "maximum_second_digit_zero_rows": (
                audit["maximum_second_digit_zero_rows"]
            ),
            "nearest_trit_sha256": audit["nearest_trit_sha256"],
            "nearest_second_digit_residual": (
                audit["nearest_second_digit_residual"]
            ),
            "second_digit_survivors": audit["second_digit_survivors"],
        } for audit in audits),
        "claim_boundary": certificate["claim_boundary"],
    }


def main() -> None:
    certificate = build_certificate()
    semantic_hash = compact_hash(certificate)
    stored_path = HERE / "anti_tensor_family_certificate.json"
    stored = json.loads(stored_path.read_text())
    generated_compact = compact_certificate(certificate)
    if compact_hash(stored) != compact_hash(generated_compact):
        raise AssertionError("stored anti-tensor certificate changed")
    if semantic_hash != EXPECTED_SEMANTIC_SHA256:
        raise AssertionError("anti-tensor semantic hash changed")
    print(
        "PASS anti-tensor family audit "
        f"hash={semantic_hash} "
        f"first={certificate['totals']['distinct_first_digit_placements']} "
        f"new={certificate['totals']['genuinely_new_first_digit_placements']} "
        f"digit2={certificate['totals']['second_digit_survivors']}"
    )
    for audit in certificate["audits"]:
        print(
            f"{audit['profile']}: "
            f"charts={audit['consistent_charts']}/{audit['charts']} "
            f"first={audit['distinct_first_digit_placements']} "
            f"new={audit['genuinely_new_first_digit_placements']} "
            f"best={audit['maximum_second_digit_zero_rows']}/20 "
            f"digit2={audit['second_digit_survivors']}"
        )


if __name__ == "__main__":
    main()
