#!/usr/bin/env python3
"""Exact trit linearization of the labelled primitive-nine upper lift.

For a fixed normalized residue profile, every nonconstant placement inside
one residue class of the nine rows is encoded by one trit

    u = 1_{q=2} - 1_{q=1}  in F_3,    r = s + 3q.

The encoding is bijective for profile counts one and two.  Moreover,
Lucas' identity

    (1-pi)^(s+3q) = (1-pi)^s (1-pi^3)^q  mod (3, pi^6)

makes jet digits three through five affine-linear in these trits.  The
upper ideal pi^3 R is square-zero, so the full autocorrelation equation is
also affine-linear after digits zero through two are fixed.

The exact arithmetic and certificate replay are dependency-free.  OR-Tools
is imported lazily only by ``build_trit_lift_model``.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from typing import Sequence

from verify_lp333_order3_labeled_jet import (
    CLASS_COUNT,
    JET_LENGTH,
    LABELLED_SURVIVOR_AGGREGATE,
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
    MODULUS,
    P,
    ROWS,
    ZERO_A_PLUS,
    ZERO_B_PLUS,
    actual_word,
    validate_labelled_certificate,
)
from verify_lp333_order3_primitive9_jet import (
    CLASSES,
    group_ring_jet,
    jet_add,
    jet_multiply,
    jet_negate,
    jet_star,
    word_jet,
)
from verify_lp333_order3_quotient import PARTS


Profile = tuple[int, int, int]
Profiles = tuple[tuple[Profile, ...], tuple[Profile, ...]]
Word = tuple[int, ...]
Jet = tuple[int, int, int, int, int, int]
TritCoordinate = tuple[int, int, int]

TRIT_SURVIVOR_MASKS_A = (
    7, 261, 448, 41, 131, 131, 273, 100, 41, 145, 37, 76,
)
TRIT_SURVIVOR_MASKS_B = (
    388, 74, 352, 161, 88, 140, 41, 289, 73, 35, 7, 322,
)

CLASS_OF = {
    value: class_index
    for class_index, part in enumerate(CLASSES)
    for value in part
}


def profile_from_normalized_mask(mask: int) -> Profile:
    if not 0 <= mask < (1 << ROWS) or bin(mask).count("1") != 3:
        raise ValueError("a normalized mask must be a nine-bit triple")
    return tuple(
        sum((mask >> (residue + 3 * quotient)) & 1 for quotient in range(3))
        for residue in range(3)
    )  # type: ignore[return-value]


def normalize_profiles(profiles: Sequence[Sequence[Sequence[int]]]) -> Profiles:
    if len(profiles) != 2 or any(
        len(channel) != CLASS_COUNT for channel in profiles
    ):
        raise ValueError("profiles must have shape 2 by 12 by 3")
    result = tuple(
        tuple(tuple(int(value) for value in profile) for profile in channel)
        for channel in profiles
    )
    if any(
        len(profile) != 3
        or any(not 0 <= value <= 3 for value in profile)
        or sum(profile) != 3
        for channel in result
        for profile in channel
    ):
        raise ValueError("every profile must compose three")
    return result  # type: ignore[return-value]


def profiles_from_masks(
    masks_a: Sequence[int], masks_b: Sequence[int]
) -> Profiles:
    if len(masks_a) != CLASS_COUNT or len(masks_b) != CLASS_COUNT:
        raise ValueError("each channel needs twelve normalized masks")
    return tuple(
        tuple(profile_from_normalized_mask(mask) for mask in channel)
        for channel in (masks_a, masks_b)
    )  # type: ignore[return-value]


PINNED_PROFILES = profiles_from_masks(
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
)


def active_trit_coordinates(profiles: Profiles) -> tuple[TritCoordinate, ...]:
    return tuple(
        (channel, class_index, residue)
        for channel in range(2)
        for class_index in range(CLASS_COUNT)
        for residue, count in enumerate(profiles[channel][class_index])
        if count in (1, 2)
    )


def quotient_support(count: int, trit: int) -> tuple[int, ...]:
    """Return the selected q values for one fixed residue r=s+3q."""

    if trit not in (0, 1, 2):
        raise ValueError("a placement trit must lie in F_3")
    if count == 0:
        return ()
    if count == 3:
        return (0, 1, 2)
    if count == 1:
        return ((0,), (2,), (1,))[trit]
    if count == 2:
        return ((1, 2), (0, 2), (0, 1))[trit]
    raise ValueError("a residue count must lie between zero and three")


def normalized_mask_from_profile_trits(
    profile: Profile, trits: Sequence[int]
) -> int:
    active_residues = tuple(
        residue for residue, count in enumerate(profile) if count in (1, 2)
    )
    if len(trits) != len(active_residues):
        raise ValueError("the number of trits does not match the profile")
    trit_by_residue = dict(zip(active_residues, trits))
    support = []
    for residue, count in enumerate(profile):
        trit = trit_by_residue.get(residue, 0)
        support.extend(
            residue + 3 * quotient
            for quotient in quotient_support(count, trit)
        )
    mask = sum(1 << row for row in support)
    if profile_from_normalized_mask(mask) != profile:
        raise AssertionError("the trit placement changed its residue profile")
    return mask


def class_word_from_profile_trits(
    channel: int,
    class_index: int,
    profile: Profile,
    trits: Sequence[int],
) -> Word:
    mask = normalized_mask_from_profile_trits(profile, trits)
    return actual_word(channel, class_index, mask)


def words_from_profile_trits(
    profiles: Profiles, trits: Sequence[int]
) -> tuple[tuple[Word, ...], tuple[Word, ...]]:
    coordinates = active_trit_coordinates(profiles)
    if len(trits) != len(coordinates):
        raise ValueError("the trit vector has the wrong length")
    values = {
        coordinate: int(trits[index]) % MODULUS
        for index, coordinate in enumerate(coordinates)
    }
    result = []
    for channel in range(2):
        channel_words = []
        for class_index in range(CLASS_COUNT):
            profile = profiles[channel][class_index]
            local_trits = tuple(
                values[(channel, class_index, residue)]
                for residue, count in enumerate(profile)
                if count in (1, 2)
            )
            channel_words.append(
                class_word_from_profile_trits(
                    channel,
                    class_index,
                    profile,
                    local_trits,
                )
            )
        result.append(tuple(channel_words))
    return tuple(result)  # type: ignore[return-value]


def trits_from_masks(
    profiles: Profiles,
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> tuple[int, ...]:
    masks = (masks_a, masks_b)
    if profiles_from_masks(masks_a, masks_b) != profiles:
        raise ValueError("the masks do not have the requested profiles")
    result = []
    for channel, class_index, residue in active_trit_coordinates(profiles):
        mask = masks[channel][class_index]
        selected = tuple(
            quotient
            for quotient in range(3)
            if (mask >> (residue + 3 * quotient)) & 1
        )
        trit = sum(
            1 if quotient == 2 else -1 if quotient == 1 else 0
            for quotient in selected
        ) % MODULUS
        if quotient_support(
            profiles[channel][class_index][residue], trit
        ) != selected:
            raise AssertionError("the oriented moment did not recover the subset")
        result.append(trit)
    return tuple(result)


def residual_coordinates(
    words: Sequence[Sequence[Sequence[int]]],
    degrees: Sequence[int],
) -> tuple[int, ...]:
    if len(words) != 2 or any(len(channel) != CLASS_COUNT for channel in words):
        raise ValueError("words must have shape 2 by 12 by 9")
    products = []
    for channel, zero in enumerate((ZERO_A_PLUS, ZERO_B_PLUS)):
        columns = [zero]
        columns.extend(
            words[channel][CLASS_OF[column]]
            for column in range(1, P)
        )
        products.append(group_ring_jet(columns))
    result = []
    for part in PARTS:
        representative = part[0]
        combined = jet_add(
            products[0][representative],
            products[1][representative],
        )
        target: Jet = (
            167 % MODULUS if representative == 0 else 0,
            0,
            0,
            0,
            0,
            0,
        )
        residual = jet_add(combined, jet_negate(target))
        for column in part:
            check = jet_add(
                jet_add(products[0][column], products[1][column]),
                jet_negate(target),
            )
            if check != residual:
                raise AssertionError("the residual lost class invariance")
        result.extend(residual[degree] for degree in degrees)
    return tuple(result)


def rref_affine_mod3(
    rows: Sequence[Sequence[int]],
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...], bool]:
    if not rows:
        return (), (), True
    width = len(rows[0])
    if width < 1 or any(len(row) != width for row in rows):
        raise ValueError("the affine matrix must be rectangular")
    matrix = [[value % MODULUS for value in row] for row in rows]
    variable_count = width - 1
    pivot_row = 0
    pivot_columns = []
    for column in range(variable_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )
        inverse = pow(matrix[pivot_row][column], -1, MODULUS)
        matrix[pivot_row] = [
            value * inverse % MODULUS for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % MODULUS
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
    consistent = not any(
        not any(row[:-1]) and row[-1] for row in matrix
    )
    independent = tuple(
        tuple(row) for row in matrix if any(row[:-1])
    )
    return independent, tuple(pivot_columns), consistent


@dataclass(frozen=True)
class UpperAffineSystem:
    profiles: Profiles
    coordinates: tuple[TritCoordinate, ...]
    offset: tuple[int, ...]
    columns: tuple[tuple[int, ...], ...]
    rref_rows: tuple[tuple[int, ...], ...]
    pivot_columns: tuple[int, ...]
    consistent: bool

    @property
    def equation_coordinates(self) -> int:
        return len(self.offset)

    @property
    def rank(self) -> int:
        return len(self.pivot_columns)

    @property
    def nullity(self) -> int | None:
        return len(self.coordinates) - self.rank if self.consistent else None

    def accepts(self, trits: Sequence[int]) -> bool:
        if len(trits) != len(self.coordinates):
            raise ValueError("the trit vector has the wrong length")
        return all(
            (
                self.offset[row]
                + sum(
                    self.columns[column][row] * int(trits[column])
                    for column in range(len(self.coordinates))
                )
            )
            % MODULUS
            == 0
            for row in range(self.equation_coordinates)
        )


@lru_cache(maxsize=256)
def _affine_upper_system(profiles: Profiles) -> UpperAffineSystem:
    coordinates = active_trit_coordinates(profiles)
    baseline = (0,) * len(coordinates)
    baseline_words = words_from_profile_trits(profiles, baseline)
    lower = residual_coordinates(baseline_words, (0, 1, 2))
    if any(lower):
        raise ValueError("the fixed profiles fail jet digits zero through two")
    offset = residual_coordinates(baseline_words, (3, 4, 5))
    columns = []
    for variable in range(len(coordinates)):
        assignment = [0] * len(coordinates)
        assignment[variable] = 1
        value = residual_coordinates(
            words_from_profile_trits(profiles, assignment),
            (3, 4, 5),
        )
        column = tuple(
            (value[row] - offset[row]) % MODULUS
            for row in range(len(offset))
        )
        assignment[variable] = 2
        doubled = residual_coordinates(
            words_from_profile_trits(profiles, assignment),
            (3, 4, 5),
        )
        if any(
            (
                doubled[row]
                - offset[row]
                - 2 * column[row]
            )
            % MODULUS
            for row in range(len(offset))
        ):
            raise AssertionError("an upper placement coordinate is nonlinear")
        columns.append(column)
    rows = tuple(
        tuple(columns[column][row] for column in range(len(columns)))
        + ((-offset[row]) % MODULUS,)
        for row in range(len(offset))
    )
    rref_rows, pivots, consistent = rref_affine_mod3(rows)
    return UpperAffineSystem(
        profiles=profiles,
        coordinates=coordinates,
        offset=offset,
        columns=tuple(columns),
        rref_rows=rref_rows,
        pivot_columns=pivots,
        consistent=consistent,
    )


def affine_upper_system(
    profiles: Sequence[Sequence[Sequence[int]]],
) -> UpperAffineSystem:
    return _affine_upper_system(normalize_profiles(profiles))


def verify_local_trit_algebra(profiles: Profiles) -> dict[str, int]:
    """Exhaust the local affine word maps and square-zero products."""

    upper_deltas = []
    local_assignments = 0
    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            profile = profiles[channel][class_index]
            active_count = sum(count in (1, 2) for count in profile)
            baseline = class_word_from_profile_trits(
                channel,
                class_index,
                profile,
                (0,) * active_count,
            )
            baseline_jet = word_jet(baseline)
            local_deltas = []
            for variable in range(active_count):
                one = [0] * active_count
                one[variable] = 1
                two = [0] * active_count
                two[variable] = 2
                one_jet = word_jet(
                    class_word_from_profile_trits(
                        channel, class_index, profile, one
                    )
                )
                two_jet = word_jet(
                    class_word_from_profile_trits(
                        channel, class_index, profile, two
                    )
                )
                delta = tuple(
                    (one_jet[degree] - baseline_jet[degree]) % MODULUS
                    for degree in range(JET_LENGTH)
                )
                double_delta = tuple(
                    (two_jet[degree] - baseline_jet[degree]) % MODULUS
                    for degree in range(JET_LENGTH)
                )
                if any(delta[:3]) or any(
                    (
                        double_delta[degree]
                        - 2 * delta[degree]
                    )
                    % MODULUS
                    for degree in range(JET_LENGTH)
                ):
                    raise AssertionError("a local trit jet is not upper-linear")
                local_deltas.append(delta)
                upper_deltas.append(delta)
            for assignment in product(range(3), repeat=active_count):
                actual = word_jet(
                    class_word_from_profile_trits(
                        channel,
                        class_index,
                        profile,
                        assignment,
                    )
                )
                expected = tuple(
                    (
                        baseline_jet[degree]
                        + sum(
                            assignment[index]
                            * local_deltas[index][degree]
                            for index in range(active_count)
                        )
                    )
                    % MODULUS
                    for degree in range(JET_LENGTH)
                )
                if actual != expected:
                    raise AssertionError("a multi-trit word jet is not affine")
                local_assignments += 1
    square_zero_products = 0
    for left in upper_deltas:
        for right in upper_deltas:
            if any(jet_multiply(left, jet_star(right))):
                raise AssertionError("the upper ideal is not square-zero")
            square_zero_products += 1
    return {
        "upper_deltas": len(upper_deltas),
        "local_assignments": local_assignments,
        "square_zero_products": square_zero_products,
    }


def verify_pinned_trit_linearization() -> dict[str, object]:
    local = verify_local_trit_algebra(PINNED_PROFILES)
    system = affine_upper_system(PINNED_PROFILES)
    pinned_trits = trits_from_masks(
        PINNED_PROFILES,
        LABELLED_SURVIVOR_MASKS_A,
        LABELLED_SURVIVOR_MASKS_B,
    )
    if not system.accepts(pinned_trits):
        raise AssertionError("the pinned survivor fails the affine system")
    trit_survivor = validate_labelled_certificate(
        LABELLED_SURVIVOR_AGGREGATE,
        TRIT_SURVIVOR_MASKS_A,
        TRIT_SURVIVOR_MASKS_B,
    )
    if profiles_from_masks(
        TRIT_SURVIVOR_MASKS_A, TRIT_SURVIVOR_MASKS_B
    ) != PINNED_PROFILES:
        raise AssertionError("the trit survivor changed the fixed profiles")
    return {
        "active_trits": len(system.coordinates),
        "physical_equation_coordinates": system.equation_coordinates,
        "affine_rank": system.rank,
        "affine_nullity": system.nullity,
        "consistent": system.consistent,
        **local,
        "replayed_jet_equations": trit_survivor["jet_equations"],
    }


@dataclass
class TritLiftModel:
    model: object
    trits: tuple[object, ...]
    bits: tuple[tuple[tuple[object, ...], ...], ...]
    signature_variables: tuple[object, ...]
    quotient_variables: tuple[object, ...]
    affine_system: UpperAffineSystem

    def exact_counts(self) -> dict[str, int]:
        proto = self.model.proto
        return {
            "placement_trits": len(self.trits),
            "primary_bits": 2 * CLASS_COUNT * ROWS,
            "signature_variables": len(self.signature_variables),
            "upper_rank": self.affine_system.rank,
            "quotient_variables": len(self.quotient_variables),
            "total_variables": len(proto.variables),
            "total_constraints": len(proto.constraints),
        }


def build_trit_lift_model(
    aggregate: Sequence[int],
    profiles: Sequence[Sequence[Sequence[int]]],
) -> TritLiftModel:
    """Build the exact upper-lift CP model after profiles are fixed."""

    try:
        from ortools.sat.python import cp_model
    except ImportError as error:  # pragma: no cover - optional search layer.
        raise RuntimeError(
            "OR-Tools is required only to build the search model"
        ) from error
    if len(aggregate) != 2 * ROWS:
        raise ValueError("aggregate row word must have 18 coordinates")
    normalized_profiles = normalize_profiles(profiles)
    affine = affine_upper_system(normalized_profiles)
    model = cp_model.CpModel()
    trits = tuple(
        model.new_int_var(0, 2, f"placement_u{index}")
        for index in range(len(affine.coordinates))
    )
    coordinate_index = {
        coordinate: index
        for index, coordinate in enumerate(affine.coordinates)
    }
    bits: list[list[tuple[object, ...]]] = [[], []]
    signatures: list[list[tuple[object, ...]]] = [[], []]
    signature_variables = []
    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            profile = normalized_profiles[channel][class_index]
            local_indices = tuple(
                coordinate_index[(channel, class_index, residue)]
                for residue, count in enumerate(profile)
                if count in (1, 2)
            )
            word_bits = tuple(
                model.new_bool_var(
                    f"tritword_c{channel}_j{class_index}_r{row}"
                )
                for row in range(ROWS)
            )
            signature = tuple(
                model.new_int_var(
                    0,
                    6,
                    f"tritsignature_c{channel}_j{class_index}_a{lag}",
                )
                for lag in range(1, 5)
            )
            table = []
            for local_trits in product(
                range(MODULUS), repeat=len(local_indices)
            ):
                word = class_word_from_profile_trits(
                    channel,
                    class_index,
                    profile,
                    local_trits,
                )
                intersections = tuple(
                    sum(
                        word[row] * word[(row + lag) % ROWS]
                        for row in range(ROWS)
                    )
                    for lag in range(1, 5)
                )
                table.append((*local_trits, *word, *intersections))
            model.add_allowed_assignments(
                (
                    *(trits[index] for index in local_indices),
                    *word_bits,
                    *signature,
                ),
                table,
            )
            bits[channel].append(word_bits)
            signatures[channel].append(signature)
            signature_variables.extend(signature)

    for row in range(ROWS):
        real = aggregate[2 * row]
        imag = aggregate[2 * row + 1]
        if (real - imag) % 2 or (real + imag) % 2:
            raise ValueError("aggregate coordinates have incompatible parity")
        model.add(
            sum(bits[0][class_index][row] for class_index in range(CLASS_COUNT))
            == (12 + real - imag) // 2
        )
        model.add(
            sum(bits[1][class_index][row] for class_index in range(CLASS_COUNT))
            == (12 + real + imag) // 2
        )
    for lag_index in range(4):
        model.add(
            sum(
                signatures[channel][class_index][lag_index]
                for channel in range(2)
                for class_index in range(CLASS_COUNT)
            )
            == 54
        )

    quotient_variables = []
    if not affine.consistent:
        model.add_bool_or(())
    else:
        for equation, row in enumerate(affine.rref_rows):
            quotient = model.new_int_var(
                -100,
                100,
                f"trit_affine_equation_{equation}_quotient",
            )
            model.add(
                sum(
                    row[index] * trits[index]
                    for index in range(len(trits))
                )
                == row[-1] + MODULUS * quotient
            )
            quotient_variables.append(quotient)
    return TritLiftModel(
        model=model,
        trits=trits,
        bits=tuple(
            tuple(tuple(word) for word in channel) for channel in bits
        ),
        signature_variables=tuple(signature_variables),
        quotient_variables=tuple(quotient_variables),
        affine_system=affine,
    )


def normalized_masks_from_solver(
    bundle: TritLiftModel, solver: object
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    result = []
    for channel in range(2):
        masks = []
        for class_index in range(CLASS_COUNT):
            actual_mask = sum(
                int(solver.value(bundle.bits[channel][class_index][row]))
                << row
                for row in range(ROWS)
            )
            high_weight = (
                class_index % 2 == 0
                if channel == 0
                else class_index % 2 == 1
            )
            masks.append(
                actual_mask ^ ((1 << ROWS) - 1)
                if high_weight
                else actual_mask
            )
        result.append(tuple(masks))
    return tuple(result)  # type: ignore[return-value]


def main() -> None:
    result = verify_pinned_trit_linearization()
    print(f"active_placement_trits={result['active_trits']}")
    print(
        "physical_equation_coordinates="
        f"{result['physical_equation_coordinates']}"
    )
    print(f"affine_rank={result['affine_rank']}")
    print(f"affine_nullity={result['affine_nullity']}")
    print(f"local_assignments_checked={result['local_assignments']}")
    print(f"square_zero_products_checked={result['square_zero_products']}")
    print(f"replayed_jet_equations={result['replayed_jet_equations']}")
    print("PASS: exact primitive-nine upper lift linearized over F_3")
    print("STATUS: one profile lift certified; no catalog exclusion asserted")


if __name__ == "__main__":
    main()
