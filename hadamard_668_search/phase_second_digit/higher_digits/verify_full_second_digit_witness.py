#!/usr/bin/env python3
"""Dependency-free exact replay of the full second-digit witness."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SECOND_DIGIT = HERE.parent
SEARCH_ROOT = SECOND_DIGIT.parent
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_integral9 import expand_columns  # noqa: E402


CERTIFICATE = HERE / "full_second_digit_witness.json"
SUPERGROUP_GENERATORS = (64, 112, 46, 7, 16)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def fixed_by_multiplier(columns, multiplier: int) -> bool:
    """Test the labelled CRT array under multiplication modulo 333."""

    return all(
        int(word[row])
        == int(
            channel[
                multiplier * column_index % 37
            ][multiplier * row % 9]
        )
        for channel in columns
        for column_index, word in enumerate(channel)
        for row in range(9)
    )


def eisenstein_norm(value: tuple[int, int]) -> int:
    first, second_value = map(int, value)
    return (
        first * first
        - first * second_value
        + second_value * second_value
    )


def lambda_valuation(value: tuple[int, int]) -> int | None:
    """Return the exact lambda valuation, or None for zero."""

    if value == (0, 0):
        return None
    first, second_value = map(int, value)
    valuation = 0
    while (first + second_value) % 3 == 0:
        numerator_first = 2 * first - second_value
        numerator_second = first + second_value
        if numerator_first % 3 or numerator_second % 3:
            raise AssertionError("lambda division lost integrality")
        first = numerator_first // 3
        second_value = numerator_second // 3
        valuation += 1
    return valuation


def audit_exactness_cutoff() -> dict[str, int]:
    """Mechanically audit the sharp displayed-coefficient cutoff."""

    # Every nonzero displayed residual is a sum of at most 135 unit roots.
    # The exceptional E0-origin residual is identically zero.
    norm_bound = 135**2
    coordinate_bound = 2 * 135
    maximum = -1
    witnesses = 0
    checked = 0
    for first in range(-coordinate_bound, coordinate_bound + 1):
        for second_value in range(-coordinate_bound, coordinate_bound + 1):
            value = (first, second_value)
            norm = eisenstein_norm(value)
            if value == (0, 0) or norm > norm_bound:
                continue
            checked += 1
            valuation = lambda_valuation(value)
            assert valuation is not None
            if valuation > maximum:
                maximum = valuation
                witnesses = 1
            elif valuation == maximum:
                witnesses += 1
    if maximum != 8:
        raise AssertionError("the norm-bounded maximum valuation changed")
    if not 3**8 <= norm_bound < 3**9:
        raise AssertionError("the nine-digit norm cutoff changed")
    return {
        "norm_bound": norm_bound,
        "nonzero_values_checked": checked,
        "maximum_lambda_valuation": maximum,
        "maximal_valuation_witnesses": witnesses,
        "digits_sufficient_for_exact_zero": 9,
    }


def audit() -> dict[str, object]:
    stored = json.loads(CERTIFICATE.read_text())
    candidate_index = int(stored["candidate_index"])
    candidate = second.CANDIDATES[candidate_index]
    if (
        stored["label"] != candidate[0]
        or tuple(stored["partition"]) != candidate[1]
        or tuple(stored["target"]) != candidate[2]
        or tuple(stored["profile_ids_a"]) != candidate[3]
        or tuple(stored["profile_ids_b"]) != candidate[4]
    ):
        raise AssertionError("the fixed profile metadata changed")
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    equations = second.first_digit_equations(profiles)
    origin, basis = second.affine_parameterization(equations, 54)
    affine = tuple(map(int, stored["affine_coordinates"]))
    placement = tuple(map(int, stored["placement_trits"]))
    if second.lift_affine_point(origin, basis, affine) != placement:
        raise AssertionError("the affine witness no longer lifts")
    if compact_hash(affine) != stored["affine_coordinates_sha256"]:
        raise AssertionError("the affine-coordinate hash changed")
    if compact_hash(placement) != stored["placement_trits_sha256"]:
        raise AssertionError("the placement hash changed")

    if second.symbolic_first_digits(equations, placement) != (0,) * 20:
        raise AssertionError("the witness left the first digit")
    term_data = second.second_digit_term_data(profiles)
    if second.symbolic_second_digits(term_data, placement) != (0,) * 20:
        raise AssertionError("the symbolic second digit failed")
    if second.direct_second_digits(profiles, placement) != (0,) * 20:
        raise AssertionError("the direct second digit failed")

    values = second.displayed_values(profiles, placement)
    digits = tuple(second.lambda_digits(value, 10) for value in values)
    if values != tuple(map(tuple, stored["displayed_exact_values"])):
        raise AssertionError("the exact displayed coefficients changed")
    if digits != tuple(map(tuple, stored["lambda_digits_through_9"])):
        raise AssertionError("the lambda-digit replay changed")
    if compact_hash(values) != stored["displayed_values_sha256"]:
        raise AssertionError("the displayed-value hash changed")
    if compact_hash(digits) != stored["lambda_digits_sha256"]:
        raise AssertionError("the displayed-digit hash changed")
    if any(any(row[index] for index in range(3)) for row in digits):
        raise AssertionError("the certified three-digit prefix changed")
    digit_three_nonzero = sum(row[3] != 0 for row in digits)
    if digit_three_nonzero != stored["digit_3_nonzero_rows"]:
        raise AssertionError("the next-digit residual count changed")

    masks_a, masks_b = second.masks_from_trits(profiles, placement)
    columns = expand_columns(masks_a, masks_b)
    base_fixed = fixed_by_multiplier(columns, 10)
    proper_fixed = tuple(
        fixed_by_multiplier(columns, generator)
        for generator in SUPERGROUP_GENERATORS
    )
    if not base_fixed or any(proper_fixed):
        raise AssertionError("the multiplier stabilizer audit changed")

    # The origin E0 coefficient is structurally zero.  Every other displayed
    # coefficient is a signed sum of at most 135 unit roots, giving a strict
    # modulus bound below 167 for every placement in all five profiles.
    maximum_term_bound = 0
    for profile_candidate in second.CANDIDATES:
        local_profiles = second.profiles_from_ids(
            profile_candidate[3], profile_candidate[4]
        )
        entries = second.phase_entries(local_profiles)
        for row_index, (component, lag) in enumerate(
            second.displayed_specifications()
        ):
            terms, target = second.coefficient_terms(
                entries, component, lag
            )
            if row_index == 0:
                if not (
                    component == "E0"
                    and lag == 0
                    and len(terms) == target == 167
                    and all(
                        term.sign == 1
                        and not term.coefficients
                        and term.constant == 0
                        for term in terms
                    )
                ):
                    raise AssertionError("the structural origin row changed")
                continue
            maximum_term_bound = max(maximum_term_bound, len(terms))
    if maximum_term_bound != 135:
        raise AssertionError("the displayed coefficient bound changed")

    return {
        "schema": stored["schema"],
        "label": stored["label"],
        "zero_digit_prefix": stored["zero_digit_prefix"],
        "digit_3_nonzero_rows": digit_three_nonzero,
        "placement_trits_sha256": stored["placement_trits_sha256"],
        "proper_supergroup_fixed": proper_fixed,
        "maximum_nonorigin_unit_terms": maximum_term_bound,
        "exactness_cutoff": audit_exactness_cutoff(),
    }


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2))
    print(f"semantic_sha256={compact_hash(result)}")


if __name__ == "__main__":
    main()
