"""Regression tests for the exact common-type five-comb CP tables."""

from __future__ import annotations

import unittest

from check_five_comb_mub_reductions import (
    HOLE_POSITIONS,
    LENGTHS,
    QUARTETS,
)
from search_five_comb_common_type_cp_sat import (
    LAGS,
    PROJECTIVE_REPRESENTATIVES,
    carrier_hole_vector,
    carrier_rows,
    cross_vector,
    reconstruct,
)


Component = tuple[dict[int, int], ...]


def component_autocorrelations(component: Component) -> tuple[int, ...]:
    """Compute positive autocorrelations without using the table helpers."""

    result = [0] * (LAGS + 1)
    for row in component:
        for position, value in row.items():
            for lag in range(1, LAGS + 1):
                result[lag] += value * row.get(position + lag, 0)
    return tuple(result)


def direct_correlations(
    sequences: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    """Independent summed aperiodic autocorrelations."""

    return tuple(
        sum(
            sum(
                sequence[index] * sequence[index + lag]
                for index in range(len(sequence) - lag)
            )
            for sequence in sequences
            if lag < len(sequence)
        )
        for lag in range(LAGS + 1)
    )


def add_components(left: Component, right: Component) -> Component:
    result = []
    for left_row, right_row in zip(left, right, strict=True):
        if set(left_row) & set(right_row):
            raise AssertionError("test components unexpectedly overlap")
        result.append(left_row | right_row)
    return tuple(result)


def one_point_component(row: int, position: int) -> Component:
    result = tuple({} for _ in range(4))
    result[row][position] = 1
    return result


def difference(
    total: tuple[int, ...],
    *parts: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        total[lag] - sum(part[lag] for part in parts)
        for lag in range(LAGS + 1)
    )


class FiveCombCommonTypeTableTests(unittest.TestCase):
    def test_omitted_carrier_self_terms_cancel(self) -> None:
        """AllDifferent makes the unmodeled within-carrier sum identically zero."""

        projective = PROJECTIVE_REPRESENTATIVES[0]
        for quartet in QUARTETS:
            total = [0] * (LAGS + 1)
            for slot, carrier_type in enumerate(range(8)):
                component = carrier_rows(
                    quartet, projective, slot, carrier_type
                )
                self.assertTrue(
                    all(len(row) == 10 for row in component)
                )
                vector = component_autocorrelations(component)
                for lag in range(1, LAGS + 1):
                    total[lag] += vector[lag]
            self.assertEqual(total[1:], [0] * LAGS)

    def test_component_pair_tables_match_direct_expansion(self) -> None:
        """Carrier/carrier and carrier/hole tables count each product once."""

        cases = (
            (0, 0, 0, 1, 0, 7),
            (39, 1, 0, 4, 6, 3),
            (39, 7, 3, 4, 2, 5),
            (47, 3, 2, 7, 7, 1),
        )
        for (
            quartet_index,
            projective_index,
            left_slot,
            right_slot,
            left_type,
            right_type,
        ) in cases:
            quartet = QUARTETS[quartet_index]
            projective = PROJECTIVE_REPRESENTATIVES[projective_index]
            left = carrier_rows(
                quartet, projective, left_slot, left_type
            )
            right = carrier_rows(
                quartet, projective, right_slot, right_type
            )
            direct_cross = difference(
                component_autocorrelations(add_components(left, right)),
                component_autocorrelations(left),
                component_autocorrelations(right),
            )
            self.assertEqual(cross_vector(left, right), direct_cross)

        quartet = QUARTETS[39]
        projective = PROJECTIVE_REPRESENTATIVES[1]
        for slot, carrier_type in ((0, 0), (3, 7), (4, 2), (7, 5)):
            carrier = carrier_rows(
                quartet, projective, slot, carrier_type
            )
            carrier_self = component_autocorrelations(carrier)
            for hole in HOLE_POSITIONS:
                point = one_point_component(*hole)
                if any(
                    set(left_row) & set(right_row)
                    for left_row, right_row in zip(
                        carrier, point, strict=True
                    )
                ):
                    self.fail("a declared hole lies in a carrier support")
                direct_cross = difference(
                    component_autocorrelations(
                        add_components(carrier, point)
                    ),
                    carrier_self,
                    component_autocorrelations(point),
                )
                self.assertEqual(
                    carrier_hole_vector(carrier, hole), direct_cross
                )

    def test_full_decomposition_matches_reconstruction(self) -> None:
        """The complete modeled sum equals direct aperiodic correlation."""

        cases = (
            (
                0,
                0,
                (0, 1, 2, 3, 4, 5, 6, 7),
                (0, 1, 0, 1, 1, 0, 1, 0),
                tuple(index % 2 for index in range(len(HOLE_POSITIONS))),
            ),
            (
                39,
                1,
                (6, 0, 7, 3, 5, 2, 1, 4),
                (0, 0, 1, 1, 0, 1, 0, 1),
                tuple(
                    ((3 * index + 1) % 5) < 2
                    for index in range(len(HOLE_POSITIONS))
                ),
            ),
            (
                47,
                7,
                (7, 6, 5, 4, 3, 2, 1, 0),
                (0, 1, 1, 0, 1, 0, 0, 1),
                tuple(
                    ((5 * index + 2) % 7) < 3
                    for index in range(len(HOLE_POSITIONS))
                ),
            ),
        )
        for (
            quartet_index,
            projective_index,
            types,
            orientations,
            holes,
        ) in cases:
            quartet = QUARTETS[quartet_index]
            projective = PROJECTIVE_REPRESENTATIVES[projective_index]
            components = tuple(
                carrier_rows(
                    quartet, projective, slot, carrier_type
                )
                for slot, carrier_type in enumerate(types)
            )
            modeled = [0] * (LAGS + 1)

            self_terms = [0] * (LAGS + 1)
            for component in components:
                vector = component_autocorrelations(component)
                for lag in range(1, LAGS + 1):
                    self_terms[lag] += vector[lag]
            self.assertEqual(self_terms[1:], [0] * LAGS)

            for left in range(8):
                for right in range(left + 1, 8):
                    multiplier = (
                        -1
                        if orientations[left] ^ orientations[right]
                        else 1
                    )
                    vector = cross_vector(
                        components[left], components[right]
                    )
                    for lag in range(1, LAGS + 1):
                        modeled[lag] += multiplier * vector[lag]

            for slot, component in enumerate(components):
                orientation_sign = -1 if orientations[slot] else 1
                for hole_bit, hole in zip(
                    holes, HOLE_POSITIONS, strict=True
                ):
                    hole_sign = -1 if hole_bit else 1
                    vector = carrier_hole_vector(component, hole)
                    for lag in range(1, LAGS + 1):
                        modeled[lag] += (
                            orientation_sign * hole_sign * vector[lag]
                        )

            for left, (left_row, left_position) in enumerate(HOLE_POSITIONS):
                for right in range(left + 1, len(HOLE_POSITIONS)):
                    right_row, right_position = HOLE_POSITIONS[right]
                    if left_row == right_row:
                        lag = abs(right_position - left_position)
                        modeled[lag] += (
                            -1 if holes[left] ^ holes[right] else 1
                        )

            sequences = reconstruct(
                quartet_index,
                projective_index,
                types,
                orientations,
                holes,
            )
            self.assertEqual(
                tuple(map(len, sequences)),
                LENGTHS,
            )
            direct = direct_correlations(sequences)
            self.assertEqual(tuple(modeled[1:]), direct[1:])


if __name__ == "__main__":
    unittest.main()
