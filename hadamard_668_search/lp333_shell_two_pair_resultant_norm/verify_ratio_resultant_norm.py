#!/usr/bin/env python3
"""Verify the pair-resultant norm consequence of the primitive ratio torus.

For primitive units write R_r=W_B,r/W_A,r.  The three paired norm equations
give

    R_(r+3) = -R_r^(-p^9),  r=0,1,2.

For each paired factor, W_X,r W_X,r+3 has a norm from F_(p^12) to
F_(p^3).  The two channels have the same three pair norms.  This script
checks the exponent arithmetic, the exact character decomposition of
F_(p^3)^*, and several independent field fixtures in the repository's
pinned model.  Equality of the total six-factor resultant norms is only
the product of these three stronger equalities.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
if str(SEARCH_ROOT) not in sys.path:
    sys.path.insert(0, str(SEARCH_ROOT))

import verify_lp333_order3_prime167_split as split  # noqa: E402


P = 167
E_DEGREE = 12
BASE_DEGREE = 3
E_SIZE = P**E_DEGREE
BASE_SIZE = P**BASE_DEGREE
NORM_EXPONENT = (E_SIZE - 1) // (BASE_SIZE - 1)
CHARACTER_ORDERS = (2, 83, 28057)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def product(values: list[split.L] | tuple[split.L, ...]) -> split.L:
    result = split.L_ONE
    for value in values:
        result = split.l_multiply(result, value)
    return result


def norm_to_p3(value: split.L) -> split.L:
    result = split.l_power(value, NORM_EXPONENT)
    if split.l_power(result, P**BASE_DEGREE) != result:
        raise AssertionError("the relative norm left F_(167^3)")
    return result


def nonzero_fixture(seed: int) -> split.L:
    value = split.field_fixture(seed)
    if value == split.L_ZERO:
        raise AssertionError("a deterministic field fixture vanished")
    if split.l_power(value, E_SIZE) != value:
        raise AssertionError("a deterministic fixture left E")
    return value


def ratio_partners(first: tuple[split.L, ...]) -> tuple[split.L, ...]:
    if len(first) != 3:
        raise ValueError("expected three free ratio coordinates")
    return tuple(
        split.l_power(
            split.l_neg(split.l_inverse(value)),
            P**9,
        )
        for value in first
    )


def primitive_residual(
    wa: tuple[split.L, ...], wb: tuple[split.L, ...], index: int
) -> split.L:
    return split.l_add(
        split.l_multiply(wa[index], split.l_power(wa[index + 3], P**3)),
        split.l_multiply(wb[index], split.l_power(wb[index + 3], P**3)),
    )


def verify() -> dict[str, object]:
    group_order = BASE_SIZE - 1
    if group_order != 4_657_462:
        raise AssertionError("the F_(167^3) unit-group order changed")
    if group_order != 2 * 83 * 28057:
        raise AssertionError("the character factorization changed")
    if not all(is_prime(value) for value in CHARACTER_ORDERS):
        raise AssertionError("the three character orders are not prime")
    if len(set(CHARACTER_ORDERS)) != len(CHARACTER_ORDERS):
        raise AssertionError("the character factors are not distinct")

    # Direct exponent proof.  The minus sign has norm one because the
    # extension degree is four, and (1-p^9) times the norm exponent is zero
    # modulo p^12-1.
    if NORM_EXPONENT != 1 + P**3 + P**6 + P**9:
        raise AssertionError("the relative norm exponent changed")
    if NORM_EXPONENT % 2:
        raise AssertionError("the norm of -1 is no longer one")
    if ((1 - P**9) * NORM_EXPONENT) % (E_SIZE - 1):
        raise AssertionError("the Hilbert-90 exponent no longer has norm one")

    fixtures = []
    for fixture_index in range(4):
        wa = tuple(
            nonzero_fixture(500 + 20 * fixture_index + index)
            for index in range(6)
        )
        first_ratios = tuple(
            nonzero_fixture(700 + 20 * fixture_index + index)
            for index in range(3)
        )
        ratios = first_ratios + ratio_partners(first_ratios)
        wb = tuple(
            split.l_multiply(left, ratio)
            for left, ratio in zip(wa, ratios)
        )
        if any(
            primitive_residual(wa, wb, index) != split.L_ZERO
            for index in range(3)
        ):
            raise AssertionError("a ratio-torus fixture missed the norm cone")

        pair_products_a = tuple(
            split.l_multiply(wa[index], wa[index + 3])
            for index in range(3)
        )
        pair_products_b = tuple(
            split.l_multiply(wb[index], wb[index + 3])
            for index in range(3)
        )
        pair_norms_a = tuple(norm_to_p3(value) for value in pair_products_a)
        pair_norms_b = tuple(norm_to_p3(value) for value in pair_products_b)
        if pair_norms_a != pair_norms_b:
            raise AssertionError("the pair-resultant norms disagree")

        pa = product(list(pair_products_a))
        pb = product(list(pair_products_b))
        nua = norm_to_p3(pa)
        nub = norm_to_p3(pb)
        if nua != nub or nua != product(list(pair_norms_a)):
            raise AssertionError("the total resultant norm corollary failed")

        ratio_product = product(ratios)
        s = product(first_ratios)
        expected_ratio_product = split.l_neg(
            split.l_multiply(
                s,
                split.l_inverse(split.l_power(s, P**9)),
            )
        )
        if ratio_product != expected_ratio_product:
            raise AssertionError("the six-ratio product formula failed")
        if norm_to_p3(ratio_product) != split.L_ONE:
            raise AssertionError("the ratio product left the norm-one torus")

        character_checks = []
        for order in CHARACTER_ORDERS:
            pair_character_hashes = []
            for index in range(3):
                # chi_d(Norm(Pair)) = Pair^((p^12-1)/d).
                character_a = split.l_power(
                    pair_products_a[index], (E_SIZE - 1) // order
                )
                character_b = split.l_power(
                    pair_products_b[index], (E_SIZE - 1) // order
                )
                norm_character_a = split.l_power(
                    pair_norms_a[index], group_order // order
                )
                norm_character_b = split.l_power(
                    pair_norms_b[index], group_order // order
                )
                if (
                    character_a != character_b
                    or character_a != norm_character_a
                    or character_b != norm_character_b
                    or split.l_power(character_a, order) != split.L_ONE
                ):
                    raise AssertionError(
                        "a pair character projection identity failed"
                    )
                pair_character_hashes.append(compact_hash(character_a))
            character_checks.append(
                {
                    "order": order,
                    "pair_value_sha256": pair_character_hashes,
                }
            )

        fixtures.append(
            {
                "fixture": fixture_index,
                "pa_sha256": compact_hash(pa),
                "pb_sha256": compact_hash(pb),
                "common_norm_sha256": compact_hash(nua),
                "common_pair_norm_sha256": [
                    compact_hash(value) for value in pair_norms_a
                ],
                "ratio_product_sha256": compact_hash(ratio_product),
                "characters": character_checks,
            }
        )

    # Show the equality is not an identity on arbitrary unit pairs.
    left = product(tuple(nonzero_fixture(900 + index) for index in range(6)))
    right = product(tuple(nonzero_fixture(950 + index) for index in range(6)))
    if norm_to_p3(left) == norm_to_p3(right):
        raise AssertionError("the negative-control norms accidentally agree")

    result = {
        "schema": "h668-ratio-resultant-norm-v1",
        "prime": P,
        "primitive_field_degree": E_DEGREE,
        "resultant_norm_base_degree": BASE_DEGREE,
        "resultant_norm_group_order": group_order,
        "pair_norm_key_space": group_order**3,
        "character_orders": list(CHARACTER_ORDERS),
        "character_order_product": 2 * 83 * 28057,
        "ratio_product_formula": "-S^(1-p^9)",
        "norm_exponent": NORM_EXPONENT,
        "norm_exponent_identity": "1+p^3+p^6+p^9",
        "ratio_norm_is_one": True,
        "channel_pair_resultant_norms_equal": True,
        "channel_total_resultant_norms_equal": True,
        "negative_control_norms_differ": True,
        "fixtures": fixtures,
    }
    result["semantic_sha256"] = compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
