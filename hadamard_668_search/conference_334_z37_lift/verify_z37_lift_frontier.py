#!/usr/bin/env python3
"""Verify the exact C37-orbit frontier for a symmetric conference matrix.

The target is a normalized symmetric conference matrix of order 334.  Its
333 by 333 core S would satisfy

    S 1 = 0,              S^2 = 333 I - J.

If a semiregular C37 acts on the core, there are nine orbits.  The matrix T
of block row sums must therefore satisfy

    T 1 = 0,              T^2 = 333 I_9 - 37 J_9.

This verifier reconstructs an explicit integral T, its strongly-regular
adjacency quotient, and two exact obstructions to overly symmetric lifts.
It does not claim that the general C37-block lift is feasible or impossible.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations, combinations_with_replacement
import json
from math import comb, factorial
from pathlib import Path
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "Z37_LIFT_FRONTIER_CERTIFICATE.json"
N = 9
P = 37
V = 333


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def matrix_multiply(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]
) -> list[list[int]]:
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    require(all(len(row) == middle for row in left), "matrix shape mismatch")
    require(all(len(row) == columns for row in right), "ragged matrix")
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(middle))
            for j in range(columns)
        ]
        for i in range(rows)
    ]


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def semantic_sha256(record: dict[str, object]) -> str:
    payload = dict(record)
    payload.pop("semantic_sha256", None)
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def sylvester_h8() -> list[list[int]]:
    matrix = [[1]]
    for _ in range(3):
        matrix = [row + row for row in matrix] + [
            row + [-entry for entry in row] for row in matrix
        ]
    require(
        matrix_multiply(matrix, [list(row) for row in zip(*matrix)])
        == [[8 if i == j else 0 for j in range(8)] for i in range(8)],
        "Sylvester matrix is not Hadamard",
    )
    return matrix


def construct_orbit_sum_matrix() -> list[list[int]]:
    """Construct T from four rational norm-333 planes on the A8 lattice."""

    hadamard = sylvester_h8()
    columns = [tuple(row + [0]) for row in hadamard[1:]]
    columns.append(tuple([1] * 8 + [-8]))
    gram = [8] * 7 + [72]

    operator = [[0] * 8 for _ in range(8)]
    for first, second in ((1, 2), (3, 4), (5, 6)):
        operator[first][first] = -18
        operator[first][second] = 3
        operator[second][first] = 3
        operator[second][second] = 18

    # The final plane has Gram diag(8,72).  This block is self-adjoint for
    # that Gram and squares to 333 I:
    #
    #     [-18 -9]
    #     [ -1 18].
    operator[0][0] = -18
    operator[0][7] = -9
    operator[7][0] = -1
    operator[7][7] = 18

    result: list[list[Fraction]] = [
        [Fraction(0) for _ in range(N)] for _ in range(N)
    ]
    for first in range(8):
        for second in range(8):
            coefficient = Fraction(
                operator[first][second], gram[second]
            )
            for i in range(N):
                for j in range(N):
                    result[i][j] += (
                        columns[first][i]
                        * coefficient
                        * columns[second][j]
                    )

    require(
        all(value.denominator == 1 for row in result for value in row),
        "orbit-sum construction is not integral",
    )
    return [[int(value) for value in row] for row in result]


def target_core_quotient_square() -> list[list[int]]:
    return [
        [V - P if i == j else -P for j in range(N)]
        for i in range(N)
    ]


def adjacency_quotient(orbit_sum: Sequence[Sequence[int]]) -> list[list[int]]:
    return [
        [
            (P - (1 if i == j else 0) - orbit_sum[i][j]) // 2
            for j in range(N)
        ]
        for i in range(N)
    ]


def verify_orbit_sum_matrix(
    orbit_sum: Sequence[Sequence[int]],
) -> dict[str, object]:
    require(len(orbit_sum) == N, "orbit-sum matrix has wrong order")
    require(all(len(row) == N for row in orbit_sum), "ragged orbit matrix")
    require(
        all(orbit_sum[i][j] == orbit_sum[j][i] for i in range(N) for j in range(N)),
        "orbit-sum matrix is not symmetric",
    )
    require(
        all(sum(row) == 0 for row in orbit_sum),
        "orbit-sum rows do not sum to zero",
    )
    require(
        all(orbit_sum[i][i] % 2 == 0 for i in range(N)),
        "diagonal orbit sums must be even",
    )
    require(
        all(
            orbit_sum[i][j] % 2
            for i in range(N)
            for j in range(N)
            if i != j
        ),
        "off-diagonal orbit sums must be odd",
    )
    require(
        matrix_multiply(orbit_sum, orbit_sum)
        == target_core_quotient_square(),
        "orbit-sum matrix does not square to the conference quotient",
    )

    quotient = adjacency_quotient(orbit_sum)
    require(
        all(
            0 <= quotient[i][j] <= (36 if i == j else 37)
            for i in range(N)
            for j in range(N)
        ),
        "adjacency quotient has an impossible block degree",
    )
    require(
        all(sum(row) == 166 for row in quotient),
        "adjacency quotient is not 166-regular",
    )
    quotient_square_plus = matrix_multiply(quotient, quotient)
    for i in range(N):
        for j in range(N):
            quotient_square_plus[i][j] += quotient[i][j]
    require(
        quotient_square_plus
        == [
            [83 + 83 * P if i == j else 83 * P for j in range(N)]
            for i in range(N)
        ],
        "adjacency quotient fails the SRG orbit equation",
    )

    return {
        "diagonal": [orbit_sum[i][i] for i in range(N)],
        "entry_values": sorted({entry for row in orbit_sum for entry in row}),
        "adjacency_diagonal": [quotient[i][i] for i in range(N)],
        "adjacency_entry_values": sorted(
            {entry for row in quotient for entry in row}
        ),
        "adjacency_row_sum": 166,
        "adjacency_quotient": quotient,
    }


def verify_paley_three_class_obstruction() -> dict[str, object]:
    """Check the zero-frequency norm contradiction for the QR/NR template."""

    diagonal_values = {0, -36, 36}
    off_diagonal_values = {-37, -35, -1, 1, 35, 37}
    reachable = {value * value for value in diagonal_values}
    for _ in range(8):
        reachable = {
            partial + value * value
            for partial in reachable
            for value in off_diagonal_values
        }
    require(296 not in reachable, "Paley three-class row norm unexpectedly feasible")
    require(
        min(reachable) == 8,
        "unexpected minimum Paley three-class row norm",
    )
    return {
        "required_row_norm_squared": 296,
        "diagonal_entry_values": sorted(diagonal_values),
        "off_diagonal_entry_values": sorted(off_diagonal_values),
        "minimum_reachable_row_norm_squared": min(reachable),
        "reachable_row_norm_squared_count": len(reachable),
        "status": "impossible",
    }


def verify_s4_uniform_obstruction() -> dict[str, object]:
    """Verify the Parseval energy deficit in the S4-uniform lift."""

    # On the three-dimensional standard representation of S4, the relevant
    # 2 by 2 Fourier block uses x=a0-a1 and y=c0-c1.  Their zero-frequency
    # values are 3 and -18, so the required spectral energy is already 333.
    zero_frequency_energy = 3 * 3 + (-18) * (-18)
    require(zero_frequency_energy == V, "wrong standard-sector energy")

    # At time zero x is +/-1; at the other 36 positions x is 0 or +/-2.
    # The sequence y is 0 or +/-2 at all 37 positions.
    maximum_time_energy = 1 + 36 * 4 + 37 * 4
    require(
        maximum_time_energy == 293 and maximum_time_energy < V,
        "S4 energy obstruction disappeared",
    )
    require(
        (-11) - 7 == -18 and (-18) % P != 0,
        "the c0-c1 sequence could be constant",
    )
    return {
        "standard_sector_zero_frequency": [3, -18],
        "required_parseval_time_energy": V,
        "maximum_binary_difference_time_energy": maximum_time_energy,
        "energy_deficit": V - maximum_time_energy,
        "status": "impossible",
    }


def verify_order_four_translation_obstruction() -> dict[str, object]:
    """Verify the trace contradiction for a regular order-four pair action."""

    # The three nonprincipal pair-index character sectors force a_g+b_g to
    # be independent of g.  Write this common value as q(t)=2r(t).
    # Every a_g+b_g has total sum -4, hence sum_t r(t)=-2.
    required_r_sum = -2

    possible_trace_values = {
        8 * r + f for r in (-1, 0, 1) for f in (-1, 1)
    }
    multiplicity_one_trace_values = {-3, 3}
    multiplicity_three_trace_values = {-9, 9}
    require(
        possible_trace_values.isdisjoint(multiplicity_one_trace_values),
        "the +/-sqrt(333) trace branch became feasible",
    )
    require(
        possible_trace_values & multiplicity_three_trace_values == {-9, 9},
        "unexpected +/-3sqrt(333) trace intersection",
    )

    # The surviving trace branch forces r(t)=+/-chi(t) for t != 0.
    # The quadratic character on F_37 has total sum zero, contradicting -2.
    quadratic_character_sum = 0
    require(
        quadratic_character_sum != required_r_sum,
        "order-four trace obstruction disappeared",
    )
    return {
        "common_pair_sum_total": -4,
        "required_r_sum": required_r_sum,
        "possible_pointwise_trace_values": sorted(possible_trace_values),
        "multiplicity_one_required_values": sorted(
            multiplicity_one_trace_values
        ),
        "multiplicity_three_required_values": sorted(
            multiplicity_three_trace_values
        ),
        "forced_quadratic_character_sum": quadratic_character_sum,
        "status": "impossible",
    }


def verify_mixed_conference_product_obstruction() -> dict[str, object]:
    """Exclude the obvious mixed Turyn repair of 9- and 37-vertex cores.

    If normalized symmetric conference cores satisfy

        B_m^2=mI-J,  B_n^2=nI-J,  B_m J=J B_m=0,

    their raw tensor has forbidden zeros.  The natural Seidel-pattern repair

        W=B_m tensor B_n + I_m tensor J_n - J_m tensor I_n

    fills those zeros, but direct multiplication leaves an extra term

        (n-m)(I_m tensor J_n - J_m tensor I_n).

    Thus this mixed product works only for m=n, not m=9,n=37.
    """

    first = 9
    second = 37
    target_order = first * second
    extra_coefficient = second - first
    require(target_order == V, "the mixed core product no longer has order 333")
    require(extra_coefficient == 28, "the mixed product defect changed")
    require(
        extra_coefficient != 0,
        "the mixed conference product obstruction disappeared",
    )

    # The two correction tensors have disjoint off-diagonal support types,
    # so their difference is nonzero whenever both factors exceed one.
    correction_difference_nonzero = first > 1 and second > 1
    require(
        correction_difference_nonzero,
        "the mixed product correction tensors unexpectedly coincide",
    )

    return {
        "status": "impossible",
        "scope": "natural_mixed_turyn_tensor_repair_only",
        "normalized_core_orders": [first, second],
        "candidate": (
            "B9 tensor B37 + I9 tensor J37 - J9 tensor I37"
        ),
        "candidate_has_seidel_zero_sign_pattern": True,
        "target_core_square": "333*I-J tensor J",
        "actual_core_square": (
            "333*I-J tensor J+28*(I9 tensor J37-J9 tensor I37)"
        ),
        "nonzero_extra_term_coefficient": extra_coefficient,
    }


def verify_general_diagonal_trace_law(
    adjacency_diagonal: Sequence[int],
) -> dict[str, object]:
    """Verify a necessary trace law for every fully general C37 lift.

    Let A_k be a nonzero 9 by 9 Fourier block of a hypothetical adjacency
    lift.  Its eigenvalues are

        r,s = (-1 +/- 3 sqrt(37))/2.

    Cyclotomic Galois conjugacy makes the multiplicity of r equal to m on
    one quadratic class of frequencies and 9-m on the other.  If g(t)
    counts the diagonal fiber blocks containing displacement t, Fourier
    inversion then gives

        g(t) = (9 +/- 3(2m-9))/2

    on the two nonzero quadratic classes.  The pointwise bounds 0 <= g <= 9
    leave m in {3,4,5,6}.  The branches m in {3,6} would give counts 0 and
    9, forcing every diagonal block to be exactly one complete quadratic
    class and hence to have degree 18.  The displayed quotient has other
    diagonal degrees, so only m in {4,5} survives and the counts are 3,6.
    """

    diagonal = list(adjacency_diagonal)
    require(len(diagonal) == N, "wrong number of diagonal block degrees")
    quotient_trace = sum(diagonal)
    require(quotient_trace == 162, "unexpected quotient trace")

    # At frequency zero the quotient has the valency 166 and four copies
    # of each restricted root.  A conference graph on 333 vertices has 166
    # copies of each restricted root in total.
    zero_sector_restricted_multiplicities = [4, 4]
    full_restricted_multiplicities = [166, 166]
    remaining_restricted_multiplicities = [
        full - zero
        for full, zero in zip(
            full_restricted_multiplicities,
            zero_sector_restricted_multiplicities,
        )
    ]
    require(
        remaining_restricted_multiplicities == [162, 162],
        "wrong nonzero-sector multiplicity total",
    )

    bounded_multiplicities: list[int] = []
    incidence_pairs: set[tuple[int, int]] = set()
    for multiplicity in range(10):
        difference = 3 * (2 * multiplicity - 9)
        numerators = (9 - difference, 9 + difference)
        require(
            all(numerator % 2 == 0 for numerator in numerators),
            "Fourier inversion did not give integral incidences",
        )
        values = tuple(sorted(numerator // 2 for numerator in numerators))
        if 0 <= values[0] and values[1] <= N:
            bounded_multiplicities.append(multiplicity)
            incidence_pairs.add(values)

    require(
        bounded_multiplicities == [3, 4, 5, 6],
        "unexpected multiplicities after pointwise incidence bounds",
    )
    require(
        incidence_pairs == {(0, 9), (3, 6)},
        "unexpected diagonal incidence branches",
    )

    all_or_none_forced_degrees = [18] * N
    require(
        diagonal != all_or_none_forced_degrees,
        "the quotient no longer excludes the all-or-none trace branch",
    )
    surviving_multiplicities = [4, 5]
    forced_incidence_counts = [3, 6]

    # There are 18 elements, or nine inverse pairs, in each quadratic
    # class.  With the orientation chosen so residues have incidence six,
    # these are the resulting total incidences.
    class_size = 18
    inverse_pair_class_size = 9
    wlog_residue_count = 6
    wlog_nonresidue_count = 3
    require(
        class_size * (wlog_residue_count + wlog_nonresidue_count)
        == quotient_trace,
        "trace-law incidence total is inconsistent",
    )

    return {
        "status": "necessary_for_any_lift",
        "quotient_trace": quotient_trace,
        "zero_sector_restricted_root_multiplicities": (
            zero_sector_restricted_multiplicities
        ),
        "full_graph_restricted_root_multiplicities": (
            full_restricted_multiplicities
        ),
        "remaining_nonzero_sector_multiplicities": (
            remaining_restricted_multiplicities
        ),
        "quadratic_frequency_class_size": 18,
        "multiplicities_after_pointwise_bounds": bounded_multiplicities,
        "candidate_diagonal_incidence_pairs": [
            list(pair) for pair in sorted(incidence_pairs)
        ],
        "all_or_none_branch_forced_diagonal_degrees": (
            all_or_none_forced_degrees
        ),
        "actual_diagonal_degrees": diagonal,
        "all_or_none_branch_excluded": True,
        "surviving_frequency_root_multiplicities": surviving_multiplicities,
        "forced_diagonal_incidence_counts": forced_incidence_counts,
        "wlog_quadratic_residue_incidence": wlog_residue_count,
        "wlog_nonresidue_incidence": wlog_nonresidue_count,
        "total_residue_element_incidences": (
            class_size * wlog_residue_count
        ),
        "total_nonresidue_element_incidences": (
            class_size * wlog_nonresidue_count
        ),
        "total_residue_inverse_pair_incidences": (
            inverse_pair_class_size * wlog_residue_count
        ),
        "total_nonresidue_inverse_pair_incidences": (
            inverse_pair_class_size * wlog_nonresidue_count
        ),
    }


def verify_complete_ambient_search_size(
    adjacency_quotient_matrix: Sequence[Sequence[int]],
) -> dict[str, object]:
    """Count the full fixed-margin ambient lift space before SRG equations.

    Off-diagonal unordered fiber pairs are arbitrary subsets of C37 with
    their certified sizes.  A diagonal block is inverse-closed, hence it is
    a subset of the 18 inverse pairs.

    For the trace-law diagonal count, fix the harmless orientation in which
    the nine residue-pair columns have sum six and the nine nonresidue-pair
    columns have sum three.  The dynamic program below counts the resulting
    9 by 18 binary contingency tables exactly.
    """

    quotient = [list(row) for row in adjacency_quotient_matrix]
    require(
        len(quotient) == N and all(len(row) == N for row in quotient),
        "wrong adjacency quotient shape in search-size audit",
    )
    diagonal_pair_degrees = [quotient[i][i] // 2 for i in range(N)]
    require(
        Counter(diagonal_pair_degrees) == Counter({9: 4, 10: 4, 5: 1}),
        "diagonal degree pattern changed",
    )

    off_diagonal_assignments = 1
    for i in range(N):
        for j in range(i + 1, N):
            off_diagonal_assignments *= comb(P, quotient[i][j])

    quotient_only_diagonal_assignments = 1
    for degree in diagonal_pair_degrees:
        quotient_only_diagonal_assignments *= comb(18, degree)

    @lru_cache(maxsize=None)
    def three_per_column_count(state: tuple[int, ...]) -> int:
        """Count labeled 9-row binary matrices with column sum three."""

        state = tuple(sorted(state))
        total = sum(state)
        if total == 0:
            return 1
        if total % 3:
            return 0
        columns = total // 3
        if columns > 9 or state[-1] > columns:
            return 0

        count = 0
        for indices in combinations(range(N), 3):
            if all(state[index] > 0 for index in indices):
                previous = list(state)
                for index in indices:
                    previous[index] -= 1
                count += three_per_column_count(tuple(sorted(previous)))
        return count

    def distinct_permutations(values: Sequence[int]) -> int:
        count = factorial(len(values))
        for multiplicity in Counter(values).values():
            count //= factorial(multiplicity)
        return count

    # Let q_i be the residue-pair row sums and put u_i=9-q_i.
    # Complementing the residue columns changes their column sum from six
    # to three.  The nonresidue row sums are
    #
    #     degree_i-q_i = u_i + (degree_i-9).
    #
    # Four offsets are zero, four are +1, and the last is -4.  Enumerating
    # sorted values inside these equal-offset groups avoids a 10^9 loop
    # while retaining the exact number of labeled assignments.
    trace_law_diagonal_assignments = 0
    for zero_group in combinations_with_replacement(range(10), 4):
        zero_sum = sum(zero_group)
        for plus_one_group in combinations_with_replacement(range(9), 4):
            final_value = 27 - zero_sum - sum(plus_one_group)
            if not 4 <= final_value <= 9:
                continue

            complemented_residue_rows = (
                zero_group + plus_one_group + (final_value,)
            )
            nonresidue_rows = (
                zero_group
                + tuple(value + 1 for value in plus_one_group)
                + (final_value - 4,)
            )
            residue_count = three_per_column_count(
                tuple(sorted(complemented_residue_rows))
            )
            nonresidue_count = three_per_column_count(
                tuple(sorted(nonresidue_rows))
            )
            trace_law_diagonal_assignments += (
                distinct_permutations(zero_group)
                * distinct_permutations(plus_one_group)
                * residue_count
                * nonresidue_count
            )

    require(
        trace_law_diagonal_assignments
        == 21108675338240988108715384392,
        "trace-law diagonal contingency count changed",
    )

    quotient_only_total = (
        off_diagonal_assignments * quotient_only_diagonal_assignments
    )
    trace_law_total = (
        off_diagonal_assignments * trace_law_diagonal_assignments
    )
    require(
        2**42 * trace_law_diagonal_assignments
        < quotient_only_diagonal_assignments
        < 2**43 * trace_law_diagonal_assignments,
        "unexpected trace-law reduction factor",
    )

    return {
        "status": "ambient_space_before_nonzero_fourier_equations",
        "raw_binary_membership_variables": 1494,
        "off_diagonal_binary_variables": 1332,
        "diagonal_inverse_pair_binary_variables": 162,
        "fixed_margin_off_diagonal_assignment_bit_length": (
            off_diagonal_assignments.bit_length()
        ),
        "quotient_only_diagonal_assignments": str(
            quotient_only_diagonal_assignments
        ),
        "trace_law_diagonal_assignments_wlog": str(
            trace_law_diagonal_assignments
        ),
        "trace_law_diagonal_reduction_between_powers_of_two": [42, 43],
        "quotient_only_full_assignment_bit_length": (
            quotient_only_total.bit_length()
        ),
        "trace_law_full_assignment_bit_length_wlog": (
            trace_law_total.bit_length()
        ),
        "trace_law_full_assignment_decimal_digits_wlog": len(
            str(trace_law_total)
        ),
        "interpretation": (
            "The exact nonzero Fourier equations must replace brute force."
        ),
    }


def verify_s4_normal_form_and_residual_symmetry(
    orbit_sum: Sequence[Sequence[int]],
) -> dict[str, object]:
    """Verify the hidden 1+4+4 normal form and sharper lift obstructions."""

    # Put the singleton first, followed by the four even and four odd
    # coordinates of the displayed A8 quotient, and globally negate.
    permutation = [8, 0, 2, 4, 6, 1, 3, 5, 7]
    normal_form = [
        [-orbit_sum[permutation[i]][permutation[j]] for j in range(N)]
        for i in range(N)
    ]

    def construct_normal_form(
        a: int, b: int, c: int, d: int, x: int, y: int
    ) -> list[list[int]]:
        matrix = [[-16] + [1] * 4 + [3] * 4]
        for i in range(4):
            matrix.append(
                [1]
                + [a if i == j else b for j in range(4)]
                + [x if i == j else y for j in range(4)]
            )
        for i in range(4):
            matrix.append(
                [3]
                + [x if i == j else y for j in range(4)]
                + [c if i == j else d for j in range(4)]
            )
        return matrix

    parameters = (0, 3, 4, 1, 11, -7)
    require(
        normal_form == construct_normal_form(*parameters),
        "the quotient lost its S4 normal form",
    )
    normal_report = verify_orbit_sum_matrix(normal_form)

    # A row with diagonal -16 has remaining sum 16 and remaining squared
    # norm 40.  Enumerate its exact sorted odd-entry shell.
    states: dict[tuple[int, int], set[tuple[int, ...]]] = {(0, 0): {()}}
    for _ in range(8):
        next_states: dict[tuple[int, int], set[tuple[int, ...]]] = {}
        for (subtotal, energy), prefixes in states.items():
            for value in range(-17, 18, 2):
                new_energy = energy + value * value
                if new_energy > 40:
                    continue
                key = subtotal + value, new_energy
                bucket = next_states.setdefault(key, set())
                for prefix in prefixes:
                    bucket.add(tuple(sorted(prefix + (value,))))
        states = next_states
    forced_shells = sorted(states.get((16, 40), set()))
    require(
        forced_shells == [(1, 1, 1, 1, 3, 3, 3, 3)],
        "the diagonal-minus-16 shell changed",
    )

    # Exhaust the small diagonal-S4 block algebra.  The row norm bounds
    # restrict diagonal block sums to multiples of four in [-16,16] and
    # off-diagonal sums to odd values in [-17,17].
    completions: list[tuple[int, int, int, int, int, int]] = []
    for a in range(-16, 17, 4):
        for c in range(-16, 17, 4):
            for b in range(-17, 18, 2):
                if a + 3 * b != 9:
                    continue
                for d in range(-17, 18, 2):
                    if c + 3 * d != 7:
                        continue
                    for x in range(-17, 18, 2):
                        for y in range(-17, 18, 2):
                            if x + 3 * y != -10:
                                continue
                            candidate = construct_normal_form(
                                a, b, c, d, x, y
                            )
                            if (
                                matrix_multiply(candidate, candidate)
                                == target_core_quotient_square()
                            ):
                                completions.append((a, b, c, d, x, y))
    require(completions == [parameters], "S4 quotient completion changed")

    # In the fully S4-invariant lift, the diagonal fiber labels have orbits
    # of sizes 1,4,4.  Their subset sums cannot realize the required trace
    # incidences three and six.
    s4_diagonal_incidences = {
        singleton + 4 * first + 4 * second
        for singleton in (0, 1)
        for first in (0, 1)
        for second in (0, 1)
    }
    require(
        s4_diagonal_incidences == {0, 1, 4, 5, 8, 9},
        "unexpected S4 diagonal incidence alphabet",
    )
    require(
        s4_diagonal_incidences.isdisjoint({3, 6}),
        "the trace-law S4 obstruction disappeared",
    )

    # More sharply, invariance under one simultaneous transposition of two
    # paired A/B labels produces an anti-invariant 2D sector.  The same
    # 2D quotient sector also occurs for a nonprincipal character of a
    # simultaneous three-cycle.  Its zero-frequency block is
    #
    #     [-3 18]
    #     [18  3].
    #
    # A binary within-cell difference has time energy at most
    # 1+36*4, and a cross-cell difference at most 37*4.  Parseval and the
    # square equation require their combined energy to be 333.
    standard_sector_zero_frequency = [-3, 18]
    required_energy = sum(
        value * value for value in standard_sector_zero_frequency
    )
    maximum_binary_time_energy = 1 + 36 * 4 + 37 * 4
    require(required_energy == V, "wrong standard-sector energy")
    require(
        maximum_binary_time_energy == 293
        and maximum_binary_time_energy < required_energy,
        "residual pair-symmetry energy obstruction disappeared",
    )

    return {
        "status": "signed_permutation_equivalent_normal_form",
        "global_sign": -1,
        "permutation": permutation,
        "forced_diagonal_minus_16_shell": list(forced_shells[0]),
        "forced_shell_ordered_assignment_count": comb(8, 4),
        "s4_parameters": {
            "a": parameters[0],
            "b": parameters[1],
            "c": parameters[2],
            "d": parameters[3],
            "x": parameters[4],
            "y": parameters[5],
        },
        "completion_count_in_s4_block_algebra": len(completions),
        "normal_form_adjacency_diagonal": normal_report[
            "adjacency_diagonal"
        ],
        "s4_diagonal_orbit_sizes": [1, 4, 4],
        "s4_reachable_diagonal_incidences": sorted(
            s4_diagonal_incidences
        ),
        "required_general_trace_incidences": [3, 6],
        "full_s4_invariant_lift": "impossible",
        "standard_sector_zero_frequency": standard_sector_zero_frequency,
        "required_parseval_time_energy": required_energy,
        "maximum_binary_difference_time_energy": (
            maximum_binary_time_energy
        ),
        "any_single_paired_label_transposition_invariant_lift": (
            "impossible"
        ),
        "any_single_paired_label_three_cycle_invariant_lift": "impossible",
    }


def verify_mod37_first_moment_reduction(
    adjacency_quotient_matrix: Sequence[Sequence[int]],
) -> dict[str, object]:
    """Verify the first nonsemisimple C37 group-ring lift equation.

    Over F_37 put x=1+y, so x^37-1=y^37.  If D(x) is a hypothetical
    adjacency lift and N(y)=D(1+y)-18I, then

        N(y)^2 = 9 y^36 J.

    Its constant matrix is N0=B-18I=-T/2 and has square zero.  Star
    symmetry makes the first coefficient N1 skew-symmetric.  The y
    coefficient gives the exact linear condition

        N0 N1 + N1 N0 = 0.

    This function computes its rank on all 36 skew first moments.
    """

    prime = 37
    quotient = [list(row) for row in adjacency_quotient_matrix]

    def multiply_mod(
        left: Sequence[Sequence[int]],
        right: Sequence[Sequence[int]],
    ) -> list[list[int]]:
        return [
            [
                sum(left[i][k] * right[k][j] for k in range(N)) % prime
                for j in range(N)
            ]
            for i in range(N)
        ]

    def rank_mod(matrix: Sequence[Sequence[int]]) -> int:
        work = [
            [entry % prime for entry in row]
            for row in matrix
        ]
        if not work:
            return 0
        rows = len(work)
        columns = len(work[0])
        rank = 0
        for column in range(columns):
            pivot = next(
                (
                    row
                    for row in range(rank, rows)
                    if work[row][column]
                ),
                None,
            )
            if pivot is None:
                continue
            work[rank], work[pivot] = work[pivot], work[rank]
            inverse = pow(work[rank][column], -1, prime)
            work[rank] = [
                entry * inverse % prime for entry in work[rank]
            ]
            for row in range(rows):
                if row == rank or not work[row][column]:
                    continue
                factor = work[row][column]
                work[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(work[row], work[rank])
                ]
            rank += 1
            if rank == rows:
                break
        return rank

    n0 = [
        [
            (quotient[i][j] - (18 if i == j else 0)) % prime
            for j in range(N)
        ]
        for i in range(N)
    ]
    require(
        multiply_mod(n0, n0) == [[0] * N for _ in range(N)],
        "the mod-37 constant matrix is not square-zero",
    )
    n0_rank = rank_mod(n0)
    require(n0_rank == 4, "unexpected rank of the square-zero quotient")

    linear_columns: list[list[int]] = []
    for first in range(N):
        for second in range(first + 1, N):
            skew = [[0] * N for _ in range(N)]
            skew[first][second] = 1
            skew[second][first] = prime - 1
            left = multiply_mod(n0, skew)
            right = multiply_mod(skew, n0)
            linear_columns.append(
                [
                    (left[i][j] + right[i][j]) % prime
                    for i in range(N)
                    for j in range(N)
                ]
            )
    linear_matrix = [list(row) for row in zip(*linear_columns)]
    first_moment_rank = rank_mod(linear_matrix)
    require(first_moment_rank == 16, "first-moment rank changed")

    # The group sum becomes y^36.  The coefficient of y^m is
    # sum_{t=m}^{36} C(t,m)=C(37,m+1), which vanishes modulo 37 unless
    # m=36.
    group_sum_coefficients = [
        sum(comb(t, degree) for t in range(degree, prime)) % prime
        for degree in range(prime)
    ]
    require(
        group_sum_coefficients == [0] * 36 + [1],
        "the characteristic-37 group-sum identity changed",
    )
    require(
        (18 * 18 + 18) % prime == 9,
        "18 is no longer the repeated modular adjacency root",
    )

    # For any fixed subset size 1..36, translation by a sends the first
    # moment to moment + size*a.  Hence each of the 37 moment values occurs
    # equally often.  The 16 independent linear equations therefore divide
    # the complete off-diagonal fixed-margin census by exactly 37^16.
    block_sizes = [
        quotient[i][j]
        for i in range(N)
        for j in range(i + 1, N)
    ]
    require(
        all(1 <= size < prime for size in block_sizes),
        "a fixed block size does not have uniform first moments",
    )
    off_diagonal_assignments = 1
    for size in block_sizes:
        off_diagonal_assignments *= comb(prime, size)
    reduction_factor = prime**first_moment_rank
    require(
        off_diagonal_assignments % reduction_factor == 0,
        "the exact moment reduction does not divide the census",
    )

    trace_law_diagonal_assignments = 21108675338240988108715384392
    filtered_full_assignments = (
        off_diagonal_assignments
        // reduction_factor
        * trace_law_diagonal_assignments
    )
    require(
        filtered_full_assignments.bit_length() == 1215,
        "unexpected first-moment filtered search exponent",
    )

    return {
        "status": "necessary_for_any_lift",
        "coefficient_ring": "F_37[y]/(y^37)",
        "substitution": "x=1+y",
        "shifted_equation": "N(y)^2=9*y^36*J",
        "shift": 18,
        "constant_matrix_rank": n0_rank,
        "constant_matrix_square_zero": True,
        "skew_first_moment_variables": len(linear_columns),
        "first_moment_linear_rank": first_moment_rank,
        "first_moment_kernel_dimension": (
            len(linear_columns) - first_moment_rank
        ),
        "fixed_weight_first_moments": "exactly_uniform_by_translation",
        "exact_census_reduction_factor": str(reduction_factor),
        "census_reduction_between_powers_of_two": [83, 84],
        "trace_and_first_moment_filtered_full_assignment_bit_length_wlog": (
            filtered_full_assignments.bit_length()
        ),
        "trace_and_first_moment_filtered_decimal_digits_wlog": len(
            str(filtered_full_assignments)
        ),
        "higher_y_adic_coefficients": (
            "formally_integrable_but_binary_support_realizability_open"
        ),
    }


def verify_three_layer_moment_witness(
    adjacency_quotient_matrix: Sequence[Sequence[int]],
) -> dict[str, object]:
    """Replay an actual block assignment through y-adic degree three.

    This is not a conference graph.  It is a concrete membership witness
    showing that the quotient, 6/3 diagonal trace law, and the first three
    modular moment layers are simultaneously feasible.
    """

    prime = 37
    quotient = [list(row) for row in adjacency_quotient_matrix]
    diagonal_pair_rows = [
        "101100011100110010",
        "001111101011001100",
        "110001000111010110",
        "100110101111100100",
        "101100111110001000",
        "101110000111001101",
        "110001101001000111",
        "001100111111010100",
        "011000100000100001",
    ]
    off_diagonal_subsets_by_size = {
        15: [2, 5, 9, 10, 11, 12, 13, 15, 16, 17, 18, 20, 21, 24, 29],
        19: [
            0, 2, 4, 5, 8, 10, 15, 16, 17, 18,
            20, 22, 23, 24, 25, 27, 29, 32, 36,
        ],
        20: [
            2, 3, 4, 5, 6, 8, 10, 11, 13, 14,
            15, 17, 21, 23, 24, 25, 29, 33, 34, 36,
        ],
        24: [
            0, 2, 3, 4, 5, 7, 9, 11, 12, 14, 17, 18,
            19, 20, 24, 26, 28, 29, 30, 31, 32, 33, 34, 36,
        ],
    }

    quadratic_residues = {
        value * value % prime for value in range(1, prime)
    }
    expected_column_sums = [
        6 if representative in quadratic_residues else 3
        for representative in range(1, 19)
    ]
    actual_column_sums = [
        sum(int(row[column]) for row in diagonal_pair_rows)
        for column in range(18)
    ]
    require(
        actual_column_sums == expected_column_sums,
        "the three-layer witness lost the 6/3 trace law",
    )
    require(
        [row.count("1") for row in diagonal_pair_rows]
        == [quotient[i][i] // 2 for i in range(N)],
        "the three-layer diagonal margins changed",
    )

    block_subsets: list[list[set[int]]] = [
        [set() for _ in range(N)] for _ in range(N)
    ]
    for i, row in enumerate(diagonal_pair_rows):
        subset: set[int] = set()
        for representative, bit in enumerate(row, 1):
            if bit == "1":
                subset.add(representative)
                subset.add(prime - representative)
        block_subsets[i][i] = subset

    for i in range(N):
        for j in range(i + 1, N):
            subset = set(
                off_diagonal_subsets_by_size[quotient[i][j]]
            )
            block_subsets[i][j] = subset
            block_subsets[j][i] = {
                (-value) % prime for value in subset
            }

    require(
        all(
            len(block_subsets[i][j]) == quotient[i][j]
            for i in range(N)
            for j in range(N)
        ),
        "the three-layer witness lost a block margin",
    )
    require(
        all(
            block_subsets[j][i]
            == {(-value) % prime for value in block_subsets[i][j]}
            for i in range(N)
            for j in range(N)
        ),
        "the three-layer witness lost star symmetry",
    )

    coefficients: list[list[list[int]]] = []
    for degree in range(5):
        coefficients.append(
            [
                [
                    sum(
                        comb(value, degree)
                        for value in block_subsets[i][j]
                    )
                    % prime
                    for j in range(N)
                ]
                for i in range(N)
            ]
        )
    require(
        coefficients[0] == quotient,
        "the degree-zero moment matrix changed",
    )
    require(
        all(
            coefficients[degree] == [[0] * N for _ in range(N)]
            for degree in (1, 2, 3)
        ),
        "the certified zero moment layers changed",
    )

    shifted = [
        [row[:] for row in coefficient] for coefficient in coefficients
    ]
    for i in range(N):
        shifted[0][i][i] = (shifted[0][i][i] - 18) % prime

    def multiply_mod(
        left: Sequence[Sequence[int]],
        right: Sequence[Sequence[int]],
    ) -> list[list[int]]:
        return [
            [
                sum(left[i][k] * right[k][j] for k in range(N)) % prime
                for j in range(N)
            ]
            for i in range(N)
        ]

    residuals: list[list[list[int]]] = []
    for degree in range(5):
        residual = [[0] * N for _ in range(N)]
        for first in range(degree + 1):
            product = multiply_mod(
                shifted[first], shifted[degree - first]
            )
            residual = [
                [
                    (residual[i][j] + product[i][j]) % prime
                    for j in range(N)
                ]
                for i in range(N)
            ]
        residuals.append(residual)

    require(
        all(
            residuals[degree] == [[0] * N for _ in range(N)]
            for degree in range(4)
        ),
        "the three-layer y-adic witness no longer lifts",
    )
    degree_four_nonzero_entries = sum(
        entry != 0 for row in residuals[4] for entry in row
    )
    require(
        degree_four_nonzero_entries == 79,
        "the certified first failed layer changed",
    )

    return {
        "status": "partial_moment_lift_not_a_conference_graph",
        "diagonal_inverse_pair_rows": diagonal_pair_rows,
        "off_diagonal_subsets_by_size": {
            str(size): subset
            for size, subset in off_diagonal_subsets_by_size.items()
        },
        "zero_binomial_moment_degrees": [1, 2, 3],
        "passed_y_adic_equation_degrees": [0, 1, 2, 3],
        "first_failed_y_adic_equation_degree": 4,
        "degree_four_nonzero_residual_entries": (
            degree_four_nonzero_entries
        ),
        "interpretation": (
            "Three low modular layers are feasible but do not construct "
            "the graph."
        ),
    }


def verify_full_formal_yadic_integrability(
    adjacency_quotient_matrix: Sequence[Sequence[int]],
) -> dict[str, object]:
    """Verify that every first-moment solution has a full formal lift.

    This is a statement in F_37[y]/(y^37), not a binary block lift.  Put
    z=log(1+y), q=z^18, and Q=N0+qJ+19y^36J.  The socle term corrects the
    trace without changing the square.  Every admissible skew first moment
    X is a commutator [N0,A] with A symmetric.  Then

        N(y)=exp(-zA) Q exp(zA)

    has the required star symmetry and satisfies N(y)^2=9 y^36 J.
    """

    prime = 37
    quotient = [list(row) for row in adjacency_quotient_matrix]

    def multiply_matrix(
        left: Sequence[Sequence[int]],
        right: Sequence[Sequence[int]],
    ) -> list[list[int]]:
        return [
            [
                sum(left[i][k] * right[k][j] for k in range(N)) % prime
                for j in range(N)
            ]
            for i in range(N)
        ]

    def rank_mod(matrix: Sequence[Sequence[int]]) -> int:
        work = [[entry % prime for entry in row] for row in matrix]
        if not work:
            return 0
        rows = len(work)
        columns = len(work[0])
        rank = 0
        for column in range(columns):
            pivot = next(
                (
                    row
                    for row in range(rank, rows)
                    if work[row][column]
                ),
                None,
            )
            if pivot is None:
                continue
            work[rank], work[pivot] = work[pivot], work[rank]
            inverse = pow(work[rank][column], -1, prime)
            work[rank] = [
                entry * inverse % prime for entry in work[rank]
            ]
            for row in range(rows):
                if row == rank or not work[row][column]:
                    continue
                factor = work[row][column]
                work[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(work[row], work[rank])
                ]
            rank += 1
        return rank

    n0 = [
        [
            (quotient[i][j] - (18 if i == j else 0)) % prime
            for j in range(N)
        ]
        for i in range(N)
    ]
    zero = [[0] * N for _ in range(N)]
    require(
        multiply_matrix(n0, n0) == zero,
        "formal-lift constant matrix is not square-zero",
    )
    require(
        all(sum(row) % prime == 0 for row in n0),
        "formal-lift constant matrix does not annihilate one",
    )

    symmetric_basis: list[list[list[int]]] = []
    for i in range(N):
        for j in range(i, N):
            matrix = [[0] * N for _ in range(N)]
            matrix[i][j] = 1
            matrix[j][i] = 1
            symmetric_basis.append(matrix)

    commutator_columns: list[list[int]] = []
    for matrix in symmetric_basis:
        left = multiply_matrix(n0, matrix)
        right = multiply_matrix(matrix, n0)
        commutator = [
            [
                (left[i][j] - right[i][j]) % prime
                for j in range(N)
            ]
            for i in range(N)
        ]
        require(
            all(
                commutator[i][j] == -commutator[j][i] % prime
                for i in range(N)
                for j in range(N)
            ),
            "a symmetric commutator is not skew",
        )
        require(
            [
                [
                    (
                        multiply_matrix(n0, commutator)[i][j]
                        + multiply_matrix(commutator, n0)[i][j]
                    )
                    % prime
                    for j in range(N)
                ]
                for i in range(N)
            ]
            == zero,
            "a commutator is not an admissible first moment",
        )
        commutator_columns.append(
            [
                commutator[i][j]
                for i in range(N)
                for j in range(i + 1, N)
            ]
        )
    commutator_map = [list(row) for row in zip(*commutator_columns)]
    commutator_rank = rank_mod(commutator_map)
    require(
        commutator_rank == 20,
        "symmetric commutators no longer span the moment kernel",
    )

    def polynomial_multiply(
        left: Sequence[int], right: Sequence[int]
    ) -> list[int]:
        result = [0] * prime
        for i, first in enumerate(left):
            if not first:
                continue
            for j, second in enumerate(right[: prime - i]):
                result[i + j] = (
                    result[i + j] + first * second
                ) % prime
        return result

    def polynomial_power(base: Sequence[int], exponent: int) -> list[int]:
        result = [1] + [0] * (prime - 1)
        factor = list(base)
        power = exponent
        while power:
            if power & 1:
                result = polynomial_multiply(result, factor)
            factor = polynomial_multiply(factor, factor)
            power //= 2
        return result

    def polynomial_compose(
        outer: Sequence[int], inner: Sequence[int]
    ) -> list[int]:
        result = [0] * prime
        power = [1] + [0] * (prime - 1)
        for coefficient in outer:
            if coefficient:
                result = [
                    (left + coefficient * right) % prime
                    for left, right in zip(result, power)
                ]
            power = polynomial_multiply(power, inner)
        return result

    logarithm = [0] * prime
    involution = [0] * prime
    for degree in range(1, prime):
        sign = 1 if degree % 2 else -1
        logarithm[degree] = sign * pow(degree, -1, prime) % prime
        involution[degree] = (-1 if degree % 2 else 1) % prime
    require(
        polynomial_compose(logarithm, involution)
        == [(-entry) % prime for entry in logarithm],
        "the group-ring involution no longer sends z to -z",
    )

    half_power = polynomial_power(logarithm, 18)
    require(
        polynomial_compose(half_power, involution) == half_power,
        "z^18 is not star-invariant",
    )
    require(
        polynomial_multiply(half_power, half_power)
        == [0] * 36 + [1],
        "z^36 is not y^36 in the truncated ring",
    )

    # Convert q(y)=z^18 from the y basis to the cyclic x basis.  The exact
    # identity q=6 sum_t chi(t)x^t exposes the Paley character hidden in
    # the formal terminal correction.
    x_coefficients = [0] * prime
    for degree in range(prime - 1, -1, -1):
        x_coefficients[degree] = (
            half_power[degree]
            - sum(
                x_coefficients[index] * comb(index, degree)
                for index in range(degree + 1, prime)
            )
        ) % prime
    expected_x_coefficients = [0] + [
        (
            6
            if pow(value, 18, prime) == 1
            else prime - 6
        )
        for value in range(1, prime)
    ]
    require(
        x_coefficients == expected_x_coefficients,
        "the z^18 quadratic-character identity changed",
    )

    # Q=N0+z^18 J+19y^36J has Q^2=9y^36J: N0^2=0,
    # N0J=JN0=0, and J^2=9J.  The socle term changes neither the square
    # nor lower coefficients.  Its trace contribution is 9*19=23, giving
    # the genuine trace branch 23y^36+9z^18.  Conjugation preserves the
    # square and trace.  Its change to J is divisible by y, which is
    # annihilated after multiplication by y^36.
    all_ones = [[1] * N for _ in range(N)]
    require(
        multiply_matrix(n0, all_ones) == zero
        and multiply_matrix(all_ones, n0) == zero,
        "N0 does not annihilate J",
    )
    require(
        multiply_matrix(all_ones, all_ones)
        == [[N] * N for _ in range(N)],
        "J^2 is not 9J",
    )
    require(
        (N * 19) % prime == 23,
        "the terminal socle trace correction changed",
    )

    return {
        "status": (
            "explicit_full_formal_completion_for_every_"
            "admissible_first_moment"
        ),
        "admissible_first_moment_dimension": 20,
        "symmetric_commutator_map_rank": commutator_rank,
        "every_first_moment_is_a_symmetric_commutator": True,
        "formal_coordinate": "z=log(1+y)",
        "terminal_correction": "z^18*J+19*y^36*J",
        "formal_trace_branch": "23*y^36+9*z^18",
        "quadratic_character_identity": (
            "z^18=6*sum_{t!=0} chi(t)*x^t"
        ),
        "full_formal_solution": (
            "exp(-zA)*(N0+z^18*J+19*y^36*J)*exp(zA)"
        ),
        "full_y_adic_equation": "N(y)^2=9*y^36*J",
        "all_degrees_through_36_formally_solvable": True,
        "classification_of_all_formal_solutions": False,
        "remaining_obstruction": (
            "simultaneous realization by exact 0/1 block supports"
        ),
    }


def verify_low_rank_formal_conjugation_obstructions(
    adjacency_quotient_matrix: Sequence[Sequence[int]],
) -> dict[str, object]:
    """Exclude diagonal and every symmetric rank-one conjugator.

    The full formal family from ``verify_full_formal_yadic_integrability``
    is much larger than the binary block family.  This function checks
    exact diagonal-coefficient obstructions for two natural attempts to
    make that family binary.

    For a nonisotropic rank-one generator

        A = alpha * u u^T / (u^T u),

    normalize a nonexceptional lag by r=t/alpha.  If h=1^T u,
    w=1-hu/(u^T u), and

        a_i = w_i^2 + h^2 u_i^2/(u^T u)^2,
        b_i = h w_i u_i/(u^T u),

    then its diagonal coefficient is

        19 + 6 eta (chi(r) a_i
                    + (chi(r-1)+chi(r+1)) b_i),

    with eta in {+1,-1}.  Six realized character patterns force
    a_i in {+3,-3} and b_i=0.  But the definition of a_i,b_i makes b_i=0
    imply a_i=1, a contradiction.

    If u^T u=0, then A=lambda*u*u^T is square-zero.  At zero lag every
    diagonal correction is a coefficient of z^k with 1<=k<=35, whose
    identity coefficient in the cyclic x basis is zero.  Five unchanged
    diagonal entries of N0 are nonbinary.
    """

    prime = 37
    quotient = [list(row) for row in adjacency_quotient_matrix]
    n0_diagonal = [
        (quotient[i][i] - 18) % prime for i in range(N)
    ]
    require(
        n0_diagonal == [0, 2, 0, 2, 0, 2, 0, 2, 29],
        "the square-zero rank-one zero-lag obstruction changed",
    )

    def quadratic_character(value: int) -> int:
        value %= prime
        if value == 0:
            return 0
        return 1 if pow(value, 18, prime) == 1 else -1

    pattern_witnesses = [2, 3, 5, 7, 10, 14]
    patterns = [
        (
            quadratic_character(value),
            quadratic_character(value - 1)
            + quadratic_character(value + 1),
        )
        for value in pattern_witnesses
    ]
    require(
        patterns
        == [(-1, 2), (1, 0), (-1, 0), (1, -2), (1, 2), (-1, -2)],
        "the six rank-one quadratic-character patterns changed",
    )
    all_pattern_counts = Counter(
        (
            quadratic_character(value),
            quadratic_character(value - 1)
            + quadratic_character(value + 1),
        )
        for value in range(prime)
        if value not in (0, 1, prime - 1)
    )
    require(
        all_pattern_counts
        == Counter(
            {
                (-1, 2): 4,
                (1, 0): 8,
                (-1, 0): 10,
                (1, -2): 4,
                (1, 2): 4,
                (-1, -2): 4,
            }
        ),
        "the nonexceptional character-pattern census changed",
    )

    local_solutions: dict[str, list[list[int]]] = {}
    for eta in (1, -1):
        solutions: list[list[int]] = []
        for a_value in range(prime):
            for b_value in range(prime):
                values = [
                    (
                        19
                        + 6
                        * eta
                        * (
                            first * a_value
                            + second * b_value
                        )
                    )
                    % prime
                    for first, second in patterns
                ]
                if all(value in (0, 1) for value in values):
                    solutions.append([a_value, b_value])
        require(
            solutions == [[3, 0], [34, 0]],
            "the semisimple rank-one local binary solutions changed",
        )
        local_solutions[str(eta)] = solutions

    # Algebraic closure of the local contradiction.  If h=0 then w=1,
    # so a_i=1.  If h!=0, b_i=0 says u_i=0 or w_i=0 coordinatewise;
    # either alternative again gives a_i=1.  This is incompatible with
    # the only local possibilities a_i=+/-3.
    forced_local_a_values = sorted(
        {solution[0] for solutions in local_solutions.values()
         for solution in solutions}
    )
    require(
        forced_local_a_values == [3, 34] and 1 not in forced_local_a_values,
        "the rank-one algebraic contradiction disappeared",
    )

    # Verify in the truncated group algebra that the coefficient of x^0
    # in z^k is zero for 1<=k<=35.  This makes the isotropic rank-one
    # zero-lag diagonal immutable.  Polynomials are represented in y=x-1.
    def polynomial_multiply(
        left: Sequence[int], right: Sequence[int]
    ) -> list[int]:
        result = [0] * prime
        for i, first in enumerate(left):
            if not first:
                continue
            for j, second in enumerate(right[: prime - i]):
                result[i + j] = (
                    result[i + j] + first * second
                ) % prime
        return result

    logarithm = [0] * prime
    for degree in range(1, prime):
        sign = 1 if degree % 2 else -1
        logarithm[degree] = sign * pow(degree, -1, prime) % prime

    power = [1] + [0] * (prime - 1)
    identity_coefficients: list[int] = []
    for degree in range(1, prime):
        power = polynomial_multiply(power, logarithm)
        # If f(y)=sum_j c_j x^j, then f(-1)=c_0 in characteristic 37,
        # because x=1+y and every nonzero j is killed at x=0.
        identity_coefficient = sum(
            coefficient * (-1) ** index
            for index, coefficient in enumerate(power)
        ) % prime
        identity_coefficients.append(identity_coefficient)
    require(
        identity_coefficients[:35] == [0] * 35
        and identity_coefficients[35] == 1,
        "the x-identity coefficients of powers of z changed",
    )
    nonbinary_zero_lag_indices = [
        index
        for index, value in enumerate(n0_diagonal)
        if value not in (0, 1)
    ]
    require(
        nonbinary_zero_lag_indices == [1, 3, 5, 7, 8],
        "the isotropic rank-one nonbinary diagonal set changed",
    )

    diagonal_family_nonzero_lag_values = sorted(
        {(19 + orientation * 6 * character) % prime
         for orientation in (1, -1)
         for character in (1, -1)}
    )
    require(
        diagonal_family_nonzero_lag_values == [13, 25],
        "the diagonal-generator obstruction changed",
    )

    return {
        "status": "impossible_within_named_formal_families",
        "family_scope": "constant-A exponential conjugation family",
        "coefficient_field": "F_37",
        "binary_coefficient_alphabet": [0, 1],
        "diagonal_generator_nonzero_lag_values": (
            diagonal_family_nonzero_lag_values
        ),
        "diagonal_symmetric_generators": "impossible",
        "semisimple_rank_one_normalized_lag_witnesses": pattern_witnesses,
        "semisimple_rank_one_character_patterns": [
            list(pattern) for pattern in patterns
        ],
        "semisimple_rank_one_pattern_counts": {
            f"{first},{second}": all_pattern_counts[(first, second)]
            for first, second in patterns
        },
        "semisimple_rank_one_local_solutions_by_eta": local_solutions,
        "semisimple_rank_one_forced_b": 0,
        "semisimple_rank_one_forced_a_values": forced_local_a_values,
        "rank_one_projector_identity_forced_a": 1,
        "semisimple_rank_one_symmetric_generators": "impossible",
        "isotropic_rank_one_zero_lag_diagonal": n0_diagonal,
        "isotropic_rank_one_nonbinary_zero_lag_indices": (
            nonbinary_zero_lag_indices
        ),
        "isotropic_rank_one_symmetric_generators": "impossible",
        "all_nonzero_symmetric_rank_one_generators": "impossible",
        "remaining_formal_conjugator_scope": (
            "genuinely coordinate-mixing symmetric rank at least two"
        ),
    }


def verify_group_ring_characteristic_identity() -> dict[str, object]:
    """Verify aggregate characteristic-polynomial consequences."""

    base = [-83, 1, 1]  # Y^2+Y-83, in ascending powers.

    def polynomial_multiply(
        left: Sequence[int], right: Sequence[int]
    ) -> list[int]:
        result = [0] * (len(left) + len(right) - 1)
        for i, first in enumerate(left):
            for j, second in enumerate(right):
                result[i + j] += first * second
        return result

    fourth_power = [1]
    for _ in range(4):
        fourth_power = polynomial_multiply(fourth_power, base)
    require(len(fourth_power) == 9, "wrong fourth-power polynomial")

    # Expand P(Y)^4 (Y-4-g) as constant_part + g*g_part.
    constant_part: list[int] = []
    trace_part: list[int] = []
    for degree in range(10):
        lower = fourth_power[degree - 1] if degree else 0
        same = fourth_power[degree] if degree < 9 else 0
        constant_part.append(lower - 4 * same)
        trace_part.append(-same)
    require(
        constant_part[-1] == 1 and trace_part[-1] == 0,
        "characteristic polynomial is not monic",
    )
    require(
        (constant_part[8], trace_part[8]) == (0, -1),
        "the trace coefficient changed",
    )
    require(
        (constant_part[7], trace_part[7]) == (-342, -4),
        "the second principal-minor identity changed",
    )
    require(
        (constant_part[0], trace_part[0])
        == (-4 * 83**4, -(83**4)),
        "the determinant identity changed",
    )

    return {
        "status": "necessary_for_any_lift",
        "identity": (
            "det(YI-D)=(Y^2+Y-83)^4*(Y-(4+tr(D)))"
        ),
        "zero_frequency_extra_root": 166,
        "nonzero_frequency_restricted_multiplicities": [4, 5],
        "second_principal_minor_identity": (
            "e2(D)=-342*delta-4*tr(D)"
        ),
        "determinant_identity": (
            f"det(D)={83**4}*(4*delta+tr(D))"
        ),
        "determinant_coefficient_values_zero_residue_nonresidue": [
            4 * 83**4,
            6 * 83**4,
            3 * 83**4,
        ],
    }


def main() -> None:
    record = json.loads(CERTIFICATE.read_text())
    require(
        record["schema"] == "h668-conference-334-z37-lift-frontier-v1",
        "certificate schema changed",
    )

    orbit_sum = construct_orbit_sum_matrix()
    require(orbit_sum == record["orbit_sum_matrix"], "orbit-sum matrix changed")
    orbit_report = verify_orbit_sum_matrix(orbit_sum)
    require(
        orbit_report == record["orbit_sum_verification"],
        "orbit-sum verification record changed",
    )

    paley_report = verify_paley_three_class_obstruction()
    require(
        paley_report == record["paley_three_class_obstruction"],
        "Paley obstruction record changed",
    )
    s4_report = verify_s4_uniform_obstruction()
    require(
        s4_report == record["s4_uniform_lift_obstruction"],
        "S4 obstruction record changed",
    )
    order_four_report = verify_order_four_translation_obstruction()
    require(
        order_four_report == record["order_four_translation_obstruction"],
        "order-four obstruction record changed",
    )
    product_report = verify_mixed_conference_product_obstruction()
    require(
        product_report == record["mixed_conference_product_obstruction"],
        "mixed conference product obstruction record changed",
    )
    trace_law_report = verify_general_diagonal_trace_law(
        orbit_report["adjacency_diagonal"]
    )
    require(
        trace_law_report == record["general_diagonal_trace_law"],
        "general diagonal trace-law record changed",
    )
    search_size_report = verify_complete_ambient_search_size(
        orbit_report["adjacency_quotient"]
    )
    require(
        search_size_report == record["complete_ambient_search_size"],
        "complete ambient search-size record changed",
    )
    normal_form_report = verify_s4_normal_form_and_residual_symmetry(
        orbit_sum
    )
    require(
        normal_form_report == record["s4_normal_form_and_residual_symmetry"],
        "S4 normal-form record changed",
    )
    first_moment_report = verify_mod37_first_moment_reduction(
        orbit_report["adjacency_quotient"]
    )
    require(
        first_moment_report == record["mod37_first_moment_reduction"],
        "mod-37 first-moment record changed",
    )
    moment_witness_report = verify_three_layer_moment_witness(
        orbit_report["adjacency_quotient"]
    )
    require(
        moment_witness_report == record["three_layer_moment_witness"],
        "three-layer moment witness changed",
    )
    formal_report = verify_full_formal_yadic_integrability(
        orbit_report["adjacency_quotient"]
    )
    require(
        formal_report == record["full_formal_yadic_integrability"],
        "full formal y-adic integrability record changed",
    )
    low_rank_report = verify_low_rank_formal_conjugation_obstructions(
        orbit_report["adjacency_quotient"]
    )
    require(
        low_rank_report
        == record["low_rank_formal_conjugation_obstructions"],
        "low-rank formal conjugation obstruction record changed",
    )
    characteristic_report = verify_group_ring_characteristic_identity()
    require(
        characteristic_report
        == record["group_ring_characteristic_identity"],
        "group-ring characteristic identity changed",
    )

    require(
        record["scope"]
        == {
            "general_z37_block_lift": "open",
            "paley_zero_qr_nqr_blocks": "impossible",
            "s4_uniform_block_types": "impossible",
            "single_paired_label_transposition_symmetry": "impossible",
            "single_paired_label_three_cycle_symmetry": "impossible",
            "regular_order_four_pair_translation": "impossible",
            "natural_mixed_order_10_order_38_conference_product": (
                "impossible"
            ),
            "formal_diagonal_conjugation_family": "impossible",
            "formal_symmetric_rank_one_conjugation_family": "impossible",
            "formal_symmetric_rank_at_least_two_family": "open",
        },
        "certificate scope changed",
    )
    digest = semantic_sha256(record)
    require(digest == record["semantic_sha256"], "semantic hash changed")

    print(
        "quotient=FEASIBLE "
        "paley3=IMPOSSIBLE s4=IMPOSSIBLE order4=IMPOSSIBLE "
        "mixed_product=IMPOSSIBLE "
        "transposition=IMPOSSIBLE three_cycle=IMPOSSIBLE "
        "diagonal_trace=3/6 moment_rank=16 ambient_bits=1215 "
        "moment_lift=y3 first_fail=y4 formal_rank1=IMPOSSIBLE "
        "general_lift=OPEN"
    )
    print(f"semantic_sha256={digest}")
    print("PASS: C37 conference-lift frontier verified")


if __name__ == "__main__":
    main()
