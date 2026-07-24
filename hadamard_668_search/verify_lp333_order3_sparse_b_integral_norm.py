#!/usr/bin/env python3
"""Verify the finite certificate around the integral sparse-B obstruction.

The number-field computations themselves are replayed, with an unconditional
``bnfcertify`` call, by
``verify_lp333_order3_sparse_b_integral_norm.gp``.  This dependency-free
companion verifies the exact allocation arithmetic, unit-norm parity
deduction, raw-word census, and a compact SHA-256 certificate over the pinned
GP outputs.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
import json

from verify_lp333_order3_sparse_b_norm import (
    NORM_TYPES,
    all_sparse_words,
    field_orbit,
    lift_safe_orbit,
    orbit_partition,
    verify as verify_upstream_census,
)


CLASS_MODULUS = 12
TARGETS = ((5, 1, 0, 0), (4, -1, 0, 0))
UNIT_RANK = 11
EXPECTED_CERTIFICATE_SHA256 = (
    "ee3c525efe9b6f9c86c11960ba493159cc33c906a945c297c8676304cb934706"
)


CASES = (
    {
        "separation": 1,
        "z": (-1, -2),
        "m_factors": (
            (11, 1, 2),
            (5227, 1, 1),
            (145753, 1, 1),
            (808368911783227, 1, 1),
        ),
        "split_class_pairs": ((5, 7), (11, 1), (10, 2)),
        "inert_fixed_classes": (0,),
        "allocation_classes": (2, 4, 4, 6, 6, 8, 8, 10),
        "principal_allocations": 0,
        "field_orbit_size": 24,
        "obstruction": "nonprincipal",
    },
    {
        "separation": 3,
        "z": (-2, -1),
        "m_factors": (
            (7, 3, 1),
            (219819964650290982168469, 1, 1),
        ),
        "split_class_pairs": ((9, 3), (7, 5)),
        "inert_fixed_classes": (),
        "allocation_classes": (2, 4, 8, 10),
        "principal_allocations": 0,
        "field_orbit_size": 24,
        "obstruction": "nonprincipal",
    },
    {
        "separation": 6,
        "z": (-2, -1),
        "m_factors": (
            (10111, 1, 1),
            (6708007752409580171263, 1, 1),
        ),
        "split_class_pairs": ((0, 0), (0, 0)),
        "inert_fixed_classes": (),
        "allocation_classes": (0, 0, 0, 0),
        "principal_allocations": 4,
        "field_orbit_size": 24,
        "obstruction": "unit_norm_parity",
    },
    {
        "separation": 6,
        "z": (-1, -2),
        "m_factors": (
            (60691617632525224495033153, 1, 1),
        ),
        "split_class_pairs": ((2, 10),),
        "inert_fixed_classes": (),
        "allocation_classes": (2, 10),
        "principal_allocations": 0,
        "field_orbit_size": 12,
        "obstruction": "nonprincipal",
    },
)

HASSE_UNIT_NORM_FREE_VECTOR = (2, 0, -1, 0, 1, 1, 1, 1, -1, 1, 1)
HASSE_UNIT_NORM_PARITY = tuple(
    value % 2 for value in HASSE_UNIT_NORM_FREE_VECTOR
)
EPSILON_FREE_VECTOR = (0, 1, 0, 1, 2, 0, -1, -1, 0, -1, 0)
EPSILON_UNIT_COORDINATES = (*EPSILON_FREE_VECTOR, 1)
EPSILON_PARITY = tuple(value % 2 for value in EPSILON_FREE_VECTOR)
UNIT_NORM_SQUARE_CLASSES = (
    (0,) * UNIT_RANK,
    HASSE_UNIT_NORM_PARITY,
)
CLASS_ORDER_RESIDUE_PRIMES = (1777, 2221, 2887, 3109)
CLASS_ORDER_RESIDUE_RANKS = ((2, 96, 12, 13), (3, 96, 12, 13))


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def allocation_classes(case: dict[str, object]) -> tuple[int, ...]:
    pairs = tuple(case["split_class_pairs"])
    fixed = sum(case["inert_fixed_classes"]) % CLASS_MODULUS
    return tuple(
        sorted(
            (
                fixed
                + sum(
                    int(pair[choice])
                    for pair, choice in zip(pairs, choices)
                )
            )
            % CLASS_MODULUS
            for choices in product((0, 1), repeat=len(pairs))
        )
    )


def verify() -> dict[str, object]:
    upstream = verify_upstream_census()
    if int(upstream["raw_words"]) != 396:
        raise AssertionError("the upstream sparse-B census changed")
    if int(upstream["obstructed_raw_words"]) != 312:
        raise AssertionError("the upstream inert-prime obstruction changed")
    if int(upstream["surviving_raw_words"]) != 84:
        raise AssertionError("the upstream residual census changed")
    if len(upstream["lift_safe_orbit_sizes"]) != 34:
        raise AssertionError("the upstream lift-safe orbit census changed")
    if int(upstream["surviving_lift_safe_orbits"]) != 8:
        raise AssertionError("the upstream residual orbit census changed")
    expected_survivors = tuple(
        (int(case["separation"]), tuple(case["z"])) for case in CASES
    )
    upstream_survivors = tuple(
        (norm_type.separation, norm_type.value)
        for norm_type in NORM_TYPES
        if norm_type.status == "relative_norm"
    )
    if upstream_survivors != expected_survivors:
        raise AssertionError(
            "the integral cases are not the exact upstream survivors"
        )
    surviving_words = frozenset().union(
        *(
            field_orbit(norm_type.representative)
            for norm_type in NORM_TYPES
            if norm_type.status == "relative_norm"
        )
    )
    surviving_safe_orbits = tuple(
        orbit
        for orbit in orbit_partition(all_sparse_words(), lift_safe_orbit)
        if orbit <= surviving_words
    )
    if len(surviving_words) != 84 or len(surviving_safe_orbits) != 8:
        raise AssertionError(
            "the four integral cases lost their exact orbit coverage"
        )

    for case in CASES:
        pairs = tuple(case["split_class_pairs"])
        if any(
            (int(left) + int(right)) % CLASS_MODULUS
            for left, right in pairs
        ):
            raise AssertionError("a displayed split-prime pair is not inverse")
        observed_classes = allocation_classes(case)
        if observed_classes != tuple(case["allocation_classes"]):
            raise AssertionError("an integral-allocation class list changed")
        principal_count = observed_classes.count(0)
        if principal_count != int(case["principal_allocations"]):
            raise AssertionError("a principal-allocation count changed")
        expected_kind = (
            "nonprincipal"
            if principal_count == 0
            else "unit_norm_parity"
        )
        if case["obstruction"] != expected_kind:
            raise AssertionError("an obstruction label changed")

    if len(EPSILON_FREE_VECTOR) != UNIT_RANK:
        raise AssertionError("the epsilon vector has the wrong unit rank")
    if HASSE_UNIT_NORM_PARITY != (
        0,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    ):
        raise AssertionError("the Hasse-unit norm parity changed")
    if EPSILON_PARITY != (0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0):
        raise AssertionError("the pinned epsilon parity changed")
    if EPSILON_PARITY in UNIT_NORM_SQUARE_CLASSES:
        raise AssertionError("the principal row became a unit norm")
    if CLASS_ORDER_RESIDUE_RANKS != (
        (2, 96, 12, 13),
        (3, 96, 12, 13),
    ):
        raise AssertionError("the class-order residue ranks changed")

    newly_excluded = sum(int(case["field_orbit_size"]) for case in CASES)
    if newly_excluded != 84:
        raise AssertionError("the four residual field orbits no longer total 84")
    previous_inert_obstruction = int(upstream["obstructed_raw_words"])
    total_sparse_words = previous_inert_obstruction + newly_excluded
    if total_sparse_words != 396:
        raise AssertionError("the sparse-B census no longer closes")

    certificate = {
        "field": {
            "degree_M": 12,
            "degree_L": 24,
            "class_group": (12,),
            "class_number_M": 1,
            "class_number_L": 12,
            "unit_rank": UNIT_RANK,
            "roots_of_unity": 6,
            "odd_character_L0_product": 4096,
            "hasse_unit_index": 2,
            "maximal_orders_certified": True,
        },
        "targets": TARGETS,
        "cases": CASES,
        "class_order_residue_primes": CLASS_ORDER_RESIDUE_PRIMES,
        "class_order_residue_ranks": CLASS_ORDER_RESIDUE_RANKS,
        "class_generator_norm": 3_861_691,
        "class_generator_order": 12,
        "hasse_unit_norm_free_vector": HASSE_UNIT_NORM_FREE_VECTOR,
        "hasse_unit_norm_parity": HASSE_UNIT_NORM_PARITY,
        "unit_norm_square_classes": UNIT_NORM_SQUARE_CLASSES,
        "epsilon_free_vector": EPSILON_FREE_VECTOR,
        "epsilon_unit_coordinates": EPSILON_UNIT_COORDINATES,
        "epsilon_parity": EPSILON_PARITY,
        "previous_inert_obstruction": previous_inert_obstruction,
        "new_integral_obstruction": newly_excluded,
        "total_sparse_words": total_sparse_words,
        "total_lift_safe_orbits": 34,
        "energy_six_sector_closed": True,
    }
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_CERTIFICATE_SHA256
    ):
        raise AssertionError(
            "the integral sparse-B certificate changed: "
            f"{certificate_hash} != {EXPECTED_CERTIFICATE_SHA256}"
        )
    return {**certificate, "certificate_sha256": certificate_hash}


def main() -> None:
    result = verify()
    print(f"certified_class_group=C_{result['field']['class_group'][0]}")
    print(f"certified_unit_rank={result['field']['unit_rank']}")
    print(
        "principal_allocation_counts="
        f"{tuple(case['principal_allocations'] for case in CASES)}"
    )
    print(f"class_order_residue_ranks={CLASS_ORDER_RESIDUE_RANKS}")
    print(f"Hasse_unit_norm_parity={HASSE_UNIT_NORM_PARITY}")
    print(f"principal_row_epsilon_coordinates={EPSILON_UNIT_COORDINATES}")
    print(f"principal_row_unit_parity={EPSILON_PARITY}")
    print(f"newly_excluded_field_norm_words={result['new_integral_obstruction']}")
    print(f"total_excluded_sparse_B_words={result['total_sparse_words']}")
    print("energy_six_sector_closed=true")
    print(f"certificate_sha256={result['certificate_sha256']}")


if __name__ == "__main__":
    main()
