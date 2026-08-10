"""Exact classification of affine-feasible all-active tier failures.

This module is a finite support/descriptor certificate only.  It identifies
the whole linkage contained in the global top D-tier, computes its internal
rank and deficiency, and records the remaining full-network geometry.  It
does not assert recurrence of any residual network.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
import json
from typing import Iterable

import exact_shielded_seam as seam
import global_atlas_interface_closure as closure
import global_tier_interface as tier
import stoichiometric_gate_feasibility as feasibility


Pair = closure.Pair
Mask = int


def _support_rank(mask: Mask) -> int:
    nodes = tuple(sorted(tier._nodes(mask)))
    anchor = closure.COMPLEXES[nodes[0]]
    rows = tuple(
        tuple(
            closure.COMPLEXES[node][coordinate] - anchor[coordinate]
            for coordinate in range(3)
        )
        for node in nodes[1:]
    )
    return len(seam._rref(rows))


def _support_deficiency(mask: Mask) -> int:
    return mask.bit_count() - 1 - _support_rank(mask)


def _all_active(descriptor: tier.TierDescriptor) -> bool:
    return all(descriptor.weight)


@lru_cache(maxsize=1)
def feasible_all_active_incidences() -> tuple[tuple[Pair, tier.TierDescriptor], ...]:
    """Every post-tier failed incidence feasible in an affine class."""

    positive = tier.tier_split(closure.POSITIVE_SHIELDED_MASKS)[1]
    signed = tier.tier_split(closure.SIGNED_SHIELDED_MASKS)[1]
    incidences = [
        (pair, descriptor)
        for pair in positive | signed
        for descriptor in tier.tier_descriptors()
        if _all_active(descriptor)
        and not tier.universal_orientation_tier_condition(pair, descriptor)
        and feasibility.descriptor_feasible(pair, descriptor)
    ]
    incidences.sort(
        key=lambda item: (
            closure.pair_payload(item[0]),
            item[1].weight,
            item[1].caps,
        )
    )
    return tuple(incidences)


def whole_top_linkage(pair: Pair, descriptor: tier.TierDescriptor) -> tuple[int, Mask]:
    """Return the unique linkage lying wholly in the global top D-tier."""

    top_d, top_s = tier.tier_sets(pair, descriptor)
    assert top_d == top_s  # all three coordinates are active
    whole: list[tuple[int, Mask]] = []
    for side, mask in enumerate(pair):
        nodes = tier._nodes(mask)
        intersection = nodes & top_d
        # A universal-orientation failure is flat: no nonempty proper top
        # subset can occur in either linkage when top_D equals top_S.
        assert not intersection or intersection == nodes
        if intersection == nodes:
            whole.append((side, mask))
    assert len(whole) == 1
    return whole[0]


def _permuted_mask(mask: Mask, permutation: tuple[int, int, int]) -> Mask:
    vector_to_index = {
        vector: index for index, vector in enumerate(closure.COMPLEXES)
    }
    result = 0
    for node in tier._nodes(mask):
        vector = closure.COMPLEXES[node]
        permuted = tuple(vector[permutation[index]] for index in range(3))
        result |= 1 << vector_to_index[permuted]
    return result


def support_orbit_key(mask: Mask) -> Mask:
    return min(
        _permuted_mask(mask, permutation)
        for permutation in permutations(range(3))
    )


def _incidence_fingerprint(
    incidences: Iterable[tuple[Pair, tier.TierDescriptor]],
) -> str:
    payload = [
        {
            "pair": closure.pair_payload(pair),
            "weight": list(descriptor.weight),
            "caps": list(descriptor.caps),
            "top": list(closure.support(whole_top_linkage(pair, descriptor)[1])),
        }
        for pair, descriptor in incidences
    ]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def _minimum_incidence_payload(
    incidences: list[tuple[Pair, tier.TierDescriptor]],
) -> dict[str, object]:
    pair, descriptor = min(
        incidences,
        key=lambda item: (
            item[0][0].bit_count() + item[0][1].bit_count(),
            closure.pair_payload(item[0]),
            item[1].weight,
        ),
    )
    side, top = whole_top_linkage(pair, descriptor)
    return {
        "pair": [list(part) for part in closure.pair_payload(pair)],
        "weight": list(descriptor.weight),
        "top_side": "shielded" if side == 0 else "available",
        "top_support": list(closure.support(top)),
    }


def certificate() -> dict[str, object]:
    incidences = feasible_all_active_incidences()
    positive_pairs = tier.tier_split(closure.POSITIVE_SHIELDED_MASKS)[1]
    signed_pairs = tier.tier_split(closure.SIGNED_SHIELDED_MASKS)[1]

    by_shape: dict[tuple[int, int, int], list[tuple[Pair, tier.TierDescriptor]]] = defaultdict(list)
    by_support: dict[Mask, list[tuple[Pair, tier.TierDescriptor]]] = defaultdict(list)
    full_deficiency = Counter()
    full_rank = Counter()
    side_histogram = Counter()
    descriptor_histogram = Counter()
    pairs: set[Pair] = set()

    for pair, descriptor in incidences:
        side, top = whole_top_linkage(pair, descriptor)
        rank = _support_rank(top)
        deficiency = _support_deficiency(top)
        shape = rank, deficiency, top.bit_count()
        by_shape[shape].append((pair, descriptor))
        by_support[top].append((pair, descriptor))
        full_rank[len(closure.full_rows(*pair))] += 1
        full_deficiency[closure.full_deficiency(*pair)] += 1
        side_histogram[side] += 1
        descriptor_histogram[descriptor.weight] += 1
        pairs.add(pair)

        values = {
            sum(
                descriptor.weight[coordinate]
                * closure.COMPLEXES[node][coordinate]
                for coordinate in range(3)
            )
            for node in tier._nodes(top)
        }
        assert len(values) == 1
        assert min(descriptor.weight) > 0

    expected_shapes = {
        (1, 0, 2): 966,
        (1, 1, 3): 279,
        (2, 1, 4): 17,
        (2, 2, 5): 6,
        (2, 3, 6): 1,
    }
    assert {shape: len(items) for shape, items in by_shape.items()} == expected_shapes
    assert full_rank == Counter({3: len(incidences)})

    exceptional_nonquadratic = tuple(
        sorted(
            (
                top
                for top in by_support
                if _support_rank(top) == 2
                and not all(
                    sum(closure.COMPLEXES[node]) == 2
                    for node in tier._nodes(top)
                )
            ),
            key=closure.support,
        )
    )
    assert tuple(map(closure.support, exceptional_nonquadratic)) == (
        ("A", "2B", "2C", "BC"),
        ("B", "2A", "2C", "AC"),
    )

    support_rows = []
    for top, items in sorted(
        by_support.items(),
        key=lambda item: (
            item[0].bit_count(),
            closure.support(item[0]),
        ),
    ):
        support_rows.append(
            {
                "support": list(closure.support(top)),
                "rank": _support_rank(top),
                "deficiency": _support_deficiency(top),
                "molecularity_two_only": all(
                    sum(closure.COMPLEXES[node]) == 2
                    for node in tier._nodes(top)
                ),
                "incidences": len(items),
                "distinct_pairs": len({pair for pair, _ in items}),
                "full_deficiency_histogram": {
                    str(value): count
                    for value, count in sorted(
                        Counter(
                            closure.full_deficiency(*pair) for pair, _ in items
                        ).items()
                    )
                },
            }
        )

    payload: dict[str, object] = {
        "claim_scope": (
            "exact support geometry of affine-feasible all-active failures; "
            "no recurrence claim"
        ),
        "incidences": len(incidences),
        "distinct_pairs": len(pairs),
        "positive_incidences": sum(pair in positive_pairs for pair, _ in incidences),
        "positive_pairs": len(pairs & positive_pairs),
        "signed_incidences": sum(pair in signed_pairs for pair, _ in incidences),
        "signed_pairs": len(pairs & signed_pairs),
        "distinct_descriptor_weights": len(descriptor_histogram),
        "unique_whole_top_supports": len(by_support),
        "whole_top_support_orbits_under_S3": len(
            {support_orbit_key(top) for top in by_support}
        ),
        "top_side_histogram": {
            "shielded": side_histogram[0],
            "available": side_histogram[1],
        },
        "full_rank_histogram": {
            str(value): count for value, count in sorted(full_rank.items())
        },
        "full_deficiency_histogram": {
            str(value): count
            for value, count in sorted(full_deficiency.items())
        },
        "analytic_shapes": [
            {
                "top_rank": rank,
                "top_deficiency": deficiency,
                "top_support_size": size,
                "incidences": len(by_shape[(rank, deficiency, size)]),
                "unique_top_supports": len(
                    {
                        whole_top_linkage(pair, descriptor)[1]
                        for pair, descriptor in by_shape[(rank, deficiency, size)]
                    }
                ),
                "minimum_incidence": _minimum_incidence_payload(
                    by_shape[(rank, deficiency, size)]
                ),
            }
            for rank, deficiency, size in sorted(by_shape)
        ],
        "exceptional_nonquadratic_rank_two_supports": [
            list(closure.support(mask)) for mask in exceptional_nonquadratic
        ],
        "top_supports": support_rows,
        "incidence_sha256": _incidence_fingerprint(incidences),
    }
    digest = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = sha256(digest).hexdigest()
    return payload


def self_test() -> None:
    result = certificate()
    assert result["incidences"] == 1269
    assert result["distinct_pairs"] == 403
    assert result["positive_incidences"] == 1263
    assert result["positive_pairs"] == 401
    assert result["signed_incidences"] == 6
    assert result["signed_pairs"] == 2
    assert result["distinct_descriptor_weights"] == 39
    assert result["unique_whole_top_supports"] == 35
    assert result["whole_top_support_orbits_under_S3"] == 15
    assert result["top_side_histogram"] == {"shielded": 1233, "available": 36}
    assert result["full_rank_histogram"] == {"3": 1269}


if __name__ == "__main__":
    self_test()
    print(json.dumps(certificate(), indent=2, sort_keys=True))
