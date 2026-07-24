#!/usr/bin/env python3
"""Exact bounded structured phase-family tests on the five h=2 profiles.

This verifier intersects four finite algebraic ansatz families with the
first two lambda-adic placement digits.  Every surviving first-digit point
is enumerated exactly; no timeout or solver status is used.

The phase coordinate is

    u_(X,j,s) in F_3,

where X is the channel, j is the cyclotomic-class index modulo 12, and s is
the row residue modulo 3.  Coordinates occur only at active profile fibers.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys
from typing import Callable, Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SHELL_TWO = SEARCH_ROOT / "shell_two_exact"
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(SHELL_TWO))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

from verify_shell_two_exact_orbits import CANDIDATES  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    direct_first_digits,
    first_digit_equations,
    inconsistency_certificate,
    lambda_digits,
    matrix_rank,
    matrix_rref,
    profiles_from_ids,
    symbolic_first_digits,
)
from verify_lp333_order3_char37_transfer import (  # noqa: E402
    CLASS_OF,
    CLASSES,
)
from verify_lp333_order3_labeled_jet import (  # noqa: E402
    ZERO_A_PLUS,
    ZERO_B_PLUS,
)
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
    quotient_support,
)
from verify_phase_second_digit import (  # noqa: E402
    derive_quadratics,
    direct_second_digits,
    displayed_values,
    second_digit_term_data,
    symbolic_second_digits,
)


MODULUS = 3
EXPECTED_SEMANTIC_SHA256 = (
    "07ca938d874c702290eb5923d30d7e19c80c3947aa9c8d26ef8ace123c572784"
)

Coordinate = tuple[int, int, int]
FeatureFunction = Callable[[Coordinate], tuple[int, ...]]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


@dataclass(frozen=True)
class Family:
    name: str
    description: str
    local_parameter_labels: tuple[str, ...]
    local_features: FeatureFunction
    literature_overlap_control: bool = False

    @property
    def local_dimension(self) -> int:
        return len(self.local_parameter_labels)

    @property
    def parameter_dimension(self) -> int:
        return 2 * self.local_dimension

    @property
    def parameter_labels(self) -> tuple[str, ...]:
        return tuple(
            f"{channel}:{label}"
            for channel in ("A", "B")
            for label in self.local_parameter_labels
        )

    def feature_matrix(
        self,
        coordinates: Sequence[Coordinate],
    ) -> tuple[tuple[int, ...], ...]:
        rows = []
        width = self.parameter_dimension
        for coordinate in coordinates:
            channel, _, _ = coordinate
            local = self.local_features(coordinate)
            if len(local) != self.local_dimension:
                raise AssertionError("feature function returned wrong width")
            row = [0] * width
            offset = channel * self.local_dimension
            row[offset:offset + self.local_dimension] = (
                value % MODULUS for value in local
            )
            rows.append(tuple(row))
        return tuple(rows)


@dataclass(frozen=True)
class MixedFamily:
    """A channel-asymmetric feature family."""

    name: str
    description: str
    channel_parameter_labels: tuple[tuple[str, ...], tuple[str, ...]]
    channel_features: tuple[FeatureFunction, FeatureFunction]
    literature_overlap_control: bool = False

    @property
    def parameter_dimension(self) -> int:
        return sum(len(labels) for labels in self.channel_parameter_labels)

    @property
    def parameter_labels(self) -> tuple[str, ...]:
        return tuple(
            f"{channel}:{label}"
            for channel, labels in zip(
                ("A", "B"), self.channel_parameter_labels
            )
            for label in labels
        )

    def feature_matrix(
        self,
        coordinates: Sequence[Coordinate],
    ) -> tuple[tuple[int, ...], ...]:
        rows = []
        offsets = (0, len(self.channel_parameter_labels[0]))
        for coordinate in coordinates:
            channel, _, _ = coordinate
            local = self.channel_features[channel](coordinate)
            expected = len(self.channel_parameter_labels[channel])
            if len(local) != expected:
                raise AssertionError("mixed feature function returned wrong width")
            row = [0] * self.parameter_dimension
            offset = offsets[channel]
            row[offset:offset + expected] = (
                value % MODULUS for value in local
            )
            rows.append(tuple(row))
        return tuple(rows)


def quadratic_c3_features(coordinate: Coordinate) -> tuple[int, ...]:
    """Total-degree-at-most-two law in (j mod 3,row residue)."""

    _, class_index, residue = coordinate
    x = class_index % 3
    s = residue
    return 1, x, s, x * x, x * s, s * s


def crt4_additive_features(coordinate: Coordinate) -> tuple[int, ...]:
    """An additive C4-class table plus an additive row-residue table."""

    _, class_index, residue = coordinate
    y = class_index % 4
    return (
        1,
        int(y == 1),
        int(y == 2),
        int(y == 3),
        int(residue == 1),
        int(residue == 2),
    )


def antipodal_additive_features(
    coordinate: Coordinate,
) -> tuple[int, ...]:
    """An arbitrary C6 antipodal-class table plus a row-residue table."""

    _, class_index, residue = coordinate
    z = class_index % 6
    return tuple(int(z == value) for value in range(6)) + (
        int(residue == 1),
        int(residue == 2),
    )


def cocyclic_multiaffine_features(
    coordinate: Coordinate,
) -> tuple[int, ...]:
    """A low Fourier/cocyclic law on C6 times the row residue."""

    _, class_index, residue = coordinate
    x = class_index % 3
    parity_character = 1 if class_index % 2 == 0 else -1
    s = residue
    return (
        1,
        x,
        parity_character,
        x * parity_character,
        s,
        x * s,
        parity_character * s,
        x * parity_character * s,
    )


def helical_c4_features(
    twist: int,
) -> FeatureFunction:
    """Return F(j+twist*s mod 4)+G(s) features."""

    def features(coordinate: Coordinate) -> tuple[int, ...]:
        _, class_index, residue = coordinate
        helical_class = (class_index + twist * residue) % 4
        return tuple(
            int(helical_class == value) for value in range(4)
        ) + (
            int(residue == 1),
            int(residue == 2),
        )

    return features


def opposite_sign(class_index: int) -> int:
    """The anti-invariant sign for the opposite-class involution."""

    return 1 if class_index < 6 else -1


def opposite_planar_c3_features(
    coordinate: Coordinate,
) -> tuple[int, ...]:
    """P(x,s)+h_j Q(x,s), with P,Q ternary quadratics."""

    _, class_index, _ = coordinate
    quadratic = quadratic_c3_features(coordinate)
    sign = opposite_sign(class_index)
    return quadratic + tuple(sign * value for value in quadratic)


def opposite_twisted_c6_features(
    coordinate: Coordinate,
) -> tuple[int, ...]:
    """P(x,s)+h_j(F(j mod 6)+G(s))."""

    _, class_index, _ = coordinate
    quadratic = quadratic_c3_features(coordinate)
    antipodal = antipodal_additive_features(coordinate)
    sign = opposite_sign(class_index)
    return quadratic + tuple(sign * value for value in antipodal)


def opposite_helical_c4_features(
    twist: int,
) -> FeatureFunction:
    """Return P(x,s)+h_j(F(j+twist*s mod 4)+G(s))."""

    helix = helical_c4_features(twist)

    def features(coordinate: Coordinate) -> tuple[int, ...]:
        _, class_index, _ = coordinate
        quadratic = quadratic_c3_features(coordinate)
        sign = opposite_sign(class_index)
        return quadratic + tuple(
            sign * value for value in helix(coordinate)
        )

    return features


Q2_LABELS = ("1", "x", "s", "x^2", "x*s", "s^2")
C4_LABELS = (
    "1", "1[y=1]", "1[y=2]", "1[y=3]", "1[s=1]", "1[s=2]"
)
C6_LABELS = (
    "1[z=0]",
    "1[z=1]",
    "1[z=2]",
    "1[z=3]",
    "1[z=4]",
    "1[z=5]",
    "1[s=1]",
    "1[s=2]",
)
COCYCLE_LABELS = ("1", "x", "p", "x*p", "s", "x*s", "p*s", "x*p*s")
HELIX_LABELS = (
    "1[h=0]", "1[h=1]", "1[h=2]", "1[h=3]", "1[s=1]", "1[s=2]"
)


FAMILIES = (
    Family(
        "quadratic_c3",
        (
            "Independent channelwise total-degree <=2 polynomials in "
            "x=j mod 3 and the row residue s."
        ),
        Q2_LABELS,
        quadratic_c3_features,
        True,
    ),
    Family(
        "crt4_additive",
        (
            "Independent channelwise additive tables F(j mod 4)+G(s), "
            "with F(0)=G(0)=0 absorbed into the intercept."
        ),
        C4_LABELS,
        crt4_additive_features,
        True,
    ),
    Family(
        "antipodal_additive",
        (
            "Independent channelwise tables F(j mod 6)+G(s); this is an "
            "antipodal/inversion-periodic cyclotomic placement template."
        ),
        C6_LABELS,
        antipodal_additive_features,
        True,
    ),
    Family(
        "cocyclic_multiaffine",
        (
            "Independent channelwise multiaffine laws in x=j mod 3, "
            "the parity character (-1)^j, and the row residue s."
        ),
        COCYCLE_LABELS,
        cocyclic_multiaffine_features,
        True,
    ),
    Family(
        "opposite_planar_c3_envelope",
        (
            "Independent channelwise laws P_X(x,s)+h_j Q_X(x,s), where "
            "P_X,Q_X have total degree <=2. This contains every ternary "
            "quadratic perfect-nonlinear/balanced-derivative choice for "
            "the opposite component Q_X."
        ),
        Q2_LABELS + tuple(f"h*{label}" for label in Q2_LABELS),
        opposite_planar_c3_features,
    ),
    Family(
        "opposite_twisted_c6",
        (
            "Independent channelwise laws P_X(x,s)+h_j(F_X(j mod 6)"
            "+G_X(s)); the h_j factor deliberately breaks fixed "
            "j -> j+6 multiplier symmetry."
        ),
        Q2_LABELS + tuple(f"h*{label}" for label in C6_LABELS),
        opposite_twisted_c6_features,
    ),
    MixedFamily(
        "opposite_helical_c4",
        (
            "Channel A uses P_A(x,s)+h_j H_A(j+s,s), while channel B "
            "uses P_B(x,s)+h_j H_B(j-s,s). This combines an "
            "opposite-class twist with opposed translation helices."
        ),
        (
            Q2_LABELS + tuple(f"h*{label}" for label in HELIX_LABELS),
            Q2_LABELS + tuple(f"h*{label}" for label in HELIX_LABELS),
        ),
        (
            opposite_helical_c4_features(1),
            opposite_helical_c4_features(-1),
        ),
    ),
)


# These are precisely the minimal proper fixed common-multiplier supergroups
# of <10> identified in arXiv:2607.20765, Table A1.  Since every object in
# this lane already has multiplier 10, invariance under the listed extra
# generator is equivalent to invariance under the corresponding supergroup.
SUPERGROUP_GENERATORS = (
    ("8", 64),
    ("11", 112),
    ("12", 46),
    ("13", 7),
    ("14", 16),
)


def matrix_vector(
    matrix: Sequence[Sequence[int]],
    vector: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        sum(left * right for left, right in zip(row, vector)) % MODULUS
        for row in matrix
    )


def nullspace_basis(
    rows: Sequence[Sequence[int]],
    columns: int,
) -> tuple[tuple[int, ...], ...]:
    if rows and any(len(row) != columns for row in rows):
        raise ValueError("matrix width changed")
    rref, pivots, _ = matrix_rref(rows)
    pivot_set = set(pivots)
    result = []
    for free_column in range(columns):
        if free_column in pivot_set:
            continue
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rref[row][free_column] % MODULUS
        result.append(tuple(vector))
    for vector in result:
        if any(matrix_vector(rows, vector)):
            raise AssertionError("kernel vector failed replay")
    return tuple(result)


def independent_span(
    vectors: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Choose the first rank-increasing vectors in deterministic order."""

    result: list[tuple[int, ...]] = []
    rank = 0
    for vector in vectors:
        normalized = tuple(int(value) % MODULUS for value in vector)
        new_rank = matrix_rank(tuple((*result, normalized)))
        if new_rank > rank:
            result.append(normalized)
            rank = new_rank
    return tuple(result)


def fiber_bits(
    channel: int,
    class_index: int,
    count: int,
    trit: int,
) -> tuple[int, ...]:
    """Return the three actual bits in one fixed row residue."""

    normalized_support = set(quotient_support(count, trit))
    high_weight = (
        class_index % 2 == 0
        if channel == 0
        else class_index % 2 == 1
    )
    normalized = tuple(
        int(quotient in normalized_support) for quotient in range(3)
    )
    return tuple(1 - bit for bit in normalized) if high_weight else normalized


def multiplier_constraints(
    profiles: Sequence[Sequence[Sequence[int]]],
    multiplier: int,
) -> tuple[tuple[int, ...], ...]:
    """Return exact affine trit constraints for fixed multiplier symmetry.

    Each row has form ``coefficients + (right_hand_side,)``.  A literal
    all-zero coefficient row with right-hand side one records an immediate
    fixed-profile or fixed-zero-column contradiction.
    """

    if multiplier % 3 != 1:
        raise ValueError("the structured lane only uses the mod-3 kernel")
    coordinates = active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    variable_count = len(coordinates)
    row_multiplier = multiplier % 9
    column_multiplier = multiplier % 37

    # The canonical zero column is part of the labelled slice and must be
    # fixed too.
    for zero in (ZERO_A_PLUS, ZERO_B_PLUS):
        if any(
            int(zero[row])
            != int(zero[(row_multiplier * row) % 9])
            for row in range(9)
        ):
            return ((0,) * variable_count + (1,),)

    rows: list[tuple[int, ...]] = []
    for channel in range(2):
        for class_index in range(12):
            representative = CLASSES[class_index][0]
            destination_class = CLASS_OF[
                column_multiplier * representative % 37
            ]
            for residue in range(3):
                source_count = int(
                    profiles[channel][class_index][residue]
                )
                destination_count = int(
                    profiles[channel][destination_class][residue]
                )
                source_active = source_count in (1, 2)
                destination_active = destination_count in (1, 2)
                source_values = range(3) if source_active else (0,)
                destination_values = (
                    range(3) if destination_active else (0,)
                )
                allowed = []
                for source_trit in source_values:
                    source = fiber_bits(
                        channel,
                        class_index,
                        source_count,
                        source_trit,
                    )
                    transported = [0] * 3
                    for quotient, bit in enumerate(source):
                        row = residue + 3 * quotient
                        destination_row = row_multiplier * row % 9
                        if destination_row % 3 != residue:
                            raise AssertionError(
                                "a mod-3-kernel multiplier moved a residue"
                            )
                        destination_quotient = (
                            destination_row - residue
                        ) // 3
                        transported[destination_quotient] = bit
                    for destination_trit in destination_values:
                        destination = fiber_bits(
                            channel,
                            destination_class,
                            destination_count,
                            destination_trit,
                        )
                        if tuple(transported) == destination:
                            allowed.append((source_trit, destination_trit))

                if not allowed:
                    return ((0,) * variable_count + (1,),)
                source_coordinate = (
                    channel, class_index, residue
                )
                destination_coordinate = (
                    channel, destination_class, residue
                )
                if source_active and destination_active:
                    mapping = {
                        source: destination for source, destination in allowed
                    }
                    if len(mapping) != 3 or len(set(mapping.values())) != 3:
                        raise AssertionError(
                            "multiplier action is not a trit bijection"
                        )
                    beta = mapping[0] % MODULUS
                    alpha = (mapping[1] - beta) % MODULUS
                    if alpha == 0 or mapping[2] % MODULUS != (
                        2 * alpha + beta
                    ) % MODULUS:
                        raise AssertionError(
                            "multiplier trit action is not affine"
                        )
                    row = [0] * variable_count
                    row[coordinate_index[destination_coordinate]] += 1
                    row[coordinate_index[source_coordinate]] -= alpha
                    normalized = tuple(
                        value % MODULUS for value in row
                    ) + (beta,)
                    if any(normalized[:-1]) or normalized[-1]:
                        rows.append(normalized)
                elif source_active:
                    possible = sorted({source for source, _ in allowed})
                    if len(possible) == 3:
                        continue
                    if len(possible) != 1:
                        raise AssertionError(
                            "non-affine unary source restriction"
                        )
                    row = [0] * variable_count
                    row[coordinate_index[source_coordinate]] = 1
                    rows.append(tuple(row) + (possible[0],))
                elif destination_active:
                    possible = sorted(
                        {destination for _, destination in allowed}
                    )
                    if len(possible) == 3:
                        continue
                    if len(possible) != 1:
                        raise AssertionError(
                            "non-affine unary destination restriction"
                        )
                    row = [0] * variable_count
                    row[coordinate_index[destination_coordinate]] = 1
                    rows.append(tuple(row) + (possible[0],))
                # Fixed-to-fixed compatibility was already established by
                # the nonempty ``allowed`` table.

    # Multiplier 10 generates the base symmetry and must impose no new
    # placement restriction on every profile in this lane.
    if multiplier == 10 and matrix_rank(tuple(row[:-1] for row in rows)):
        raise AssertionError("base multiplier unexpectedly restricted trits")
    return tuple(rows)


def point_satisfies_constraints(
    point: Sequence[int],
    constraints: Sequence[Sequence[int]],
) -> bool:
    return all(
        sum(
            row[index] * int(point[index])
            for index in range(len(point))
        )
        % MODULUS
        == row[-1] % MODULUS
        for row in constraints
    )


def affine_intersection_count(
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
    constraint_sets: Sequence[Sequence[Sequence[int]]],
) -> int:
    """Count an affine family intersected with several affine constraints."""

    variable_count = len(basis)
    restricted = []
    for constraints in constraint_sets:
        for row in constraints:
            coefficients = tuple(
                sum(
                    row[index] * basis[column][index]
                    for index in range(len(origin))
                )
                % MODULUS
                for column in range(variable_count)
            )
            right_hand_side = (
                row[-1]
                - sum(
                    row[index] * origin[index]
                    for index in range(len(origin))
                )
            ) % MODULUS
            restricted.append(coefficients + (right_hand_side,))
    if not restricted:
        return MODULUS ** variable_count
    coefficient_rank = matrix_rank(
        tuple(row[:-1] for row in restricted)
    )
    augmented_rank = matrix_rank(tuple(restricted))
    return (
        MODULUS ** (variable_count - coefficient_rank)
        if coefficient_rank == augmented_rank
        else 0
    )


def supergroup_census(
    profiles: Sequence[Sequence[Sequence[int]]],
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> tuple[dict[str, int], int]:
    """Count all five minimal proper supergroups and their union."""

    constraints_by_id = {
        identifier: multiplier_constraints(profiles, generator)
        for identifier, generator in SUPERGROUP_GENERATORS
    }
    counts = {
        identifier: affine_intersection_count(
            origin, basis, (constraints,)
        )
        for identifier, constraints in constraints_by_id.items()
    }
    union_count = 0
    identifiers = tuple(constraints_by_id)
    for size in range(1, len(identifiers) + 1):
        sign = 1 if size % 2 else -1
        for subset in combinations(identifiers, size):
            union_count += sign * affine_intersection_count(
                origin,
                basis,
                tuple(constraints_by_id[identifier] for identifier in subset),
            )
    total = MODULUS ** len(basis)
    if not 0 <= union_count <= total:
        raise AssertionError("supergroup inclusion-exclusion failed")
    return counts, total - union_count


def compose_first_digit(
    equations: Sequence[object],
    features: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    rows = augmented_system(equations)
    parameter_count = len(features[0])
    return tuple(
        tuple(
            sum(row[coordinate] * features[coordinate][parameter] for coordinate in range(len(features)))
            % MODULUS
            for parameter in range(parameter_count)
        )
        + (row[-1] % MODULUS,)
        for row in rows
    )


def affine_image(
    restricted_rows: Sequence[Sequence[int]],
    features: Sequence[Sequence[int]],
) -> tuple[
    tuple[int, ...] | None,
    tuple[tuple[int, ...], ...] | None,
    tuple[tuple[int, ...], ...],
]:
    """Return an origin and independent basis for distinct trit placements."""

    parameter_count = len(features[0])
    origin_parameters = canonical_solution(restricted_rows, parameter_count)
    coefficient_rows = tuple(row[:-1] for row in restricted_rows)
    parameter_kernel = nullspace_basis(coefficient_rows, parameter_count)
    if origin_parameters is None:
        return None, None, parameter_kernel
    origin = matrix_vector(features, origin_parameters)
    image_vectors = tuple(
        matrix_vector(features, vector) for vector in parameter_kernel
    )
    return origin, independent_span(image_vectors), parameter_kernel


def affine_points(
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
):
    for coefficients in product(range(MODULUS), repeat=len(basis)):
        yield tuple(
            (
                origin[index]
                + sum(
                    coefficients[column] * basis[column][index]
                    for column in range(len(basis))
                )
            )
            % MODULUS
            for index in range(len(origin))
        )


def lift_affine_coordinates(
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
    coefficients: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        (
            origin[index]
            + sum(
                coefficients[column] * basis[column][index]
                for column in range(len(basis))
            )
        )
        % MODULUS
        for index in range(len(origin))
    )


def evaluate_restricted_quadratics(
    constants: Sequence[int],
    linears: Sequence[Sequence[int]],
    polars: Sequence[Sequence[Sequence[int]]],
    point: Sequence[int],
) -> tuple[int, ...]:
    """Evaluate ``c+l.x+(1/2)x^T Bx`` with sparse exact arithmetic."""

    result = []
    for equation in range(len(constants)):
        value = int(constants[equation])
        linear = linears[equation]
        polar = polars[equation]
        for left, left_value in enumerate(point):
            if not left_value:
                continue
            value += int(linear[left]) * left_value
            value += (
                2
                * int(polar[left][left])
                * left_value
                * left_value
            )
            for right in range(left + 1, len(point)):
                if point[right]:
                    value += (
                        int(polar[left][right])
                        * left_value
                        * int(point[right])
                    )
        result.append(value % MODULUS)
    return tuple(result)


def audit_family_on_profile(
    family: Family,
    candidate: Sequence[object],
) -> dict[str, object]:
    label, partition, target, identifiers_a, identifiers_b = candidate
    profiles = profiles_from_ids(identifiers_a, identifiers_b)
    coordinates = active_trit_coordinates(profiles)
    if len(coordinates) != 54:
        raise AssertionError("shell-two placement dimension changed")
    equations = first_digit_equations(profiles)
    features = family.feature_matrix(coordinates)
    parameter_count = family.parameter_dimension
    feature_rank = matrix_rank(features)
    restricted = compose_first_digit(equations, features)
    coefficient_rank = matrix_rank(tuple(row[:-1] for row in restricted))
    augmented_rank = matrix_rank(restricted)
    consistent = coefficient_rank == augmented_rank
    origin, image_basis, parameter_kernel = affine_image(
        restricted, features
    )

    result: dict[str, object] = {
        "profile": label,
        "partition": partition,
        "target": target,
        "active_trits": len(coordinates),
        "parameters": parameter_count,
        "feature_rank": feature_rank,
        "distinct_family_placements": MODULUS ** feature_rank,
        "first_digit_coefficient_rank": coefficient_rank,
        "first_digit_augmented_rank": augmented_rank,
        "first_digit_consistent": consistent,
        "first_digit_parameter_solutions": (
            MODULUS ** (parameter_count - coefficient_rank)
            if consistent
            else 0
        ),
    }
    if not consistent:
        if origin is not None or image_basis is not None:
            raise AssertionError("inconsistent family acquired an origin")
        certificate = inconsistency_certificate(
            restricted, parameter_count
        )
        if certificate is None:
            raise AssertionError("missing first-digit contradiction")
        combined = tuple(
            sum(
                certificate[row] * restricted[row][column]
                for row in range(len(restricted))
            )
            % MODULUS
            for column in range(parameter_count + 1)
        )
        if combined != (0,) * parameter_count + (1,):
            raise AssertionError("first-digit contradiction failed replay")
        result.update({
            "first_digit_distinct_placements": 0,
            "parameter_kernel_dimension": len(parameter_kernel),
            "first_digit_image_dimension": None,
            "inconsistency_multipliers": certificate,
            "inconsistency_sha256": compact_hash(certificate),
            "second_digit_survivors": 0,
            "second_digit_zero_row_histogram": {},
            "maximum_second_digit_zero_rows": None,
            "nearest_trits": None,
            "nearest_trit_sha256": None,
            "nearest_second_digit_residual": None,
            "direct_replay_checked": False,
            "second_digit_witness_records": (),
            "exact_phase_survivors": 0,
            "minimal_supergroup_fixed_counts": {
                identifier: 0
                for identifier, _ in SUPERGROUP_GENERATORS
            },
            "proper_supergroup_free_placements": 0,
            "proper_supergroup_free_witness_sha256": None,
        })
        return result

    if origin is None or image_basis is None:
        raise AssertionError("consistent family lost its affine image")
    image_dimension = len(image_basis)
    first_digit_count = MODULUS ** image_dimension
    result.update({
        "first_digit_distinct_placements": first_digit_count,
        "parameter_kernel_dimension": len(parameter_kernel),
        "first_digit_image_dimension": image_dimension,
        "inconsistency_multipliers": None,
        "inconsistency_sha256": None,
    })
    supergroup_counts, supergroup_free_count = supergroup_census(
        profiles, origin, image_basis
    )
    result.update({
        "minimal_supergroup_fixed_counts": supergroup_counts,
        "proper_supergroup_free_placements": supergroup_free_count,
    })

    term_data = second_digit_term_data(profiles)
    restricted_quadratics = derive_quadratics(
        term_data, origin, image_basis
    )
    histogram: dict[int, int] = {}
    second_digit_survivors: list[tuple[int, ...]] = []
    nearest: tuple[int, ...] | None = None
    nearest_residual: tuple[int, ...] | None = None
    supergroup_free_witness: tuple[int, ...] | None = None
    supergroup_constraints = tuple(
        multiplier_constraints(profiles, generator)
        for _, generator in SUPERGROUP_GENERATORS
    )
    maximum_zero_rows = -1
    enumerated = 0
    for affine_coordinates in product(
        range(MODULUS), repeat=image_dimension
    ):
        residual = evaluate_restricted_quadratics(
            *restricted_quadratics, affine_coordinates
        )
        zero_rows = sum(value == 0 for value in residual)
        histogram[zero_rows] = histogram.get(zero_rows, 0) + 1
        enumerated += 1
        trits = None
        if zero_rows > maximum_zero_rows:
            trits = lift_affine_coordinates(
                origin, image_basis, affine_coordinates
            )
            maximum_zero_rows = zero_rows
            nearest = trits
            nearest_residual = residual
        if zero_rows == len(equations):
            if trits is None:
                trits = lift_affine_coordinates(
                    origin, image_basis, affine_coordinates
                )
            second_digit_survivors.append(trits)
        if (
            supergroup_free_witness is None
            and supergroup_free_count
        ):
            if trits is None:
                trits = lift_affine_coordinates(
                    origin, image_basis, affine_coordinates
                )
            if not any(
                point_satisfies_constraints(trits, constraints)
                for constraints in supergroup_constraints
            ):
                supergroup_free_witness = trits
    if enumerated != first_digit_count or sum(histogram.values()) != enumerated:
        raise AssertionError("family enumeration count changed")
    if nearest is None or nearest_residual is None:
        raise AssertionError("nonempty affine family lost its nearest point")
    if (supergroup_free_witness is None) != (supergroup_free_count == 0):
        raise AssertionError("supergroup-free witness census disagrees")

    # Detached exact-Eisenstein replay of the canonical nearest point.
    if direct_first_digits(profiles, nearest) != (0,) * len(equations):
        raise AssertionError("nearest point failed direct first-digit replay")
    if direct_second_digits(profiles, nearest) != nearest_residual:
        raise AssertionError("nearest point failed direct second-digit replay")

    # No present family reaches this branch, but any future second-digit hit
    # is retained explicitly rather than silently promoted to an exact lift.
    exact_phase_survivors = []
    second_digit_witness_records = []
    for trits in second_digit_survivors:
        direct = direct_second_digits(profiles, trits)
        if direct != (0,) * len(equations):
            raise AssertionError("symbolic second-digit hit failed replay")
        exact_values = displayed_values(profiles, trits)
        digit_records = tuple(
            lambda_digits(value, 6) for value in exact_values
        )
        exact_phase = all(value == (0, 0) for value in exact_values)
        if exact_phase:
            exact_phase_survivors.append(trits)
        second_digit_witness_records.append({
            "trits": trits,
            "trit_sha256": compact_hash(trits),
            "lambda_digit_3": tuple(
                digits[3] for digits in digit_records
            ),
            "lambda_digit_4": tuple(
                digits[4] for digits in digit_records
            ),
            "lambda_digit_5": tuple(
                digits[5] for digits in digit_records
            ),
            "exact_phase_equations_zero": exact_phase,
        })

    result.update({
        "second_digit_survivors": len(second_digit_survivors),
        "second_digit_zero_row_histogram": {
            str(key): histogram[key] for key in sorted(histogram)
        },
        "maximum_second_digit_zero_rows": maximum_zero_rows,
        "nearest_trits": nearest,
        "nearest_trit_sha256": compact_hash(nearest),
        "nearest_second_digit_residual": nearest_residual,
        "proper_supergroup_free_witness_sha256": (
            None
            if supergroup_free_witness is None
            else compact_hash(supergroup_free_witness)
        ),
        "direct_replay_checked": True,
        "second_digit_witness_records": tuple(
            second_digit_witness_records
        ),
        "exact_phase_survivors": len(exact_phase_survivors),
    })
    return result


def build_certificate() -> dict[str, object]:
    family_records = []
    for family in FAMILIES:
        audits = tuple(
            audit_family_on_profile(family, candidate)
            for candidate in CANDIDATES
        )
        family_records.append({
            "name": family.name,
            "description": family.description,
            "parameter_labels": family.parameter_labels,
            "literature_overlap_control": (
                family.literature_overlap_control
            ),
            "audits": audits,
            "profiles_first_digit_excluded": sum(
                not audit["first_digit_consistent"] for audit in audits
            ),
            "profiles_second_digit_excluded": sum(
                audit["first_digit_consistent"]
                and audit["second_digit_survivors"] == 0
                for audit in audits
            ),
            "total_first_digit_distinct_placements": sum(
                int(audit["first_digit_distinct_placements"])
                for audit in audits
            ),
            "total_second_digit_survivors": sum(
                int(audit["second_digit_survivors"]) for audit in audits
            ),
            "total_proper_supergroup_free_placements": sum(
                int(audit["proper_supergroup_free_placements"])
                for audit in audits
            ),
        })
    return {
        "schema": "lp333-shell-two-structured-phase-families-v1",
        "scope": (
            "Four bounded phase ansatz families on all five exact h=2 "
            "profile orbits. Exhaustive first/second lambda-digit audit; "
            "no LP(333) or H(668) claim."
        ),
        "field": "F_3",
        "profiles": len(CANDIDATES),
        "families": tuple(family_records),
    }


def main() -> None:
    certificate = build_certificate()
    semantic_sha256 = compact_hash(certificate)
    if (
        EXPECTED_SEMANTIC_SHA256
        and semantic_sha256 != EXPECTED_SEMANTIC_SHA256
    ):
        raise AssertionError("structured-family semantic certificate changed")
    for family in certificate["families"]:
        print(
            f"{family['name']}: "
            f"first_digit_points="
            f"{family['total_first_digit_distinct_placements']} "
            f"supergroup_free="
            f"{family['total_proper_supergroup_free_placements']} "
            f"second_digit_survivors={family['total_second_digit_survivors']}"
        )
        for audit in family["audits"]:
            print(
                f"  {audit['profile']}: "
                f"ranks={audit['first_digit_coefficient_rank']}/"
                f"{audit['first_digit_augmented_rank']} "
                f"first={audit['first_digit_distinct_placements']} "
                f"free={audit['proper_supergroup_free_placements']} "
                f"second={audit['second_digit_survivors']} "
                f"best={audit['maximum_second_digit_zero_rows']}"
            )
    print(f"semantic_sha256={semantic_sha256}")


if __name__ == "__main__":
    main()
