"""Scoped certificate for the audited prospective 26-pair theorem.

The analytic arguments live in
``research_notes/prospective_26_candidate_pair_theorem.md``.  This file
freezes the exact selector rows and checks the structural premises used
there.  The independent audit passed the two analytic extensions and their
pair-level composition.  The global T3-2 flag remains false.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import factorial
import json
import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_remaining_structure as structure
import one_active_prospective_composition as prospective
import prospective_no_promotion_26 as selector
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as all_active
import three_active_gluing_gate as gluing


Pair = closure.Pair
Descriptor = tier.TierDescriptor

EXPECTED_ONE_ROWS_SHA256 = (
    "091dc59dc83b6445d36135a2d6b1e6c1bfb9565db88328fc1725c39f78bbc7e4"
)
EXPECTED_NORMALIZED_PROFILES_SHA256 = (
    "36b6eb1c1beadc939681fc7515e2adf3dfb9e16d116da4b8d2bd73ac77aabe12"
)
EXPECTED_ALL_ACTIVE_ROWS_SHA256 = (
    "55669e3dc9b3fbb7ee84895ea158b3b596d339265cde1a23189bdf312a314bea"
)
EXPECTED_PAIR_TOPS_SHA256 = (
    "d1de16c1c45eaab3bce35a17db75bd947a8398a049722f100d96dd227b7e21d5"
)
EXPECTED_AFTER_769_SHA256 = (
    "4e645eca1ba23849680f2f983e1fb8c9465001c5b0e8c0090a31a339bf18ec06"
)
EXPECTED_PAYLOAD_SHA256 = (
    "a1f528caffb63729d889e792ce8831b899865e70c1564b2a0a33d46f295a39da"
)


def _encoded_sha256(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()
    return sha256(encoded).hexdigest()


def _phase_payload(
    phases: tuple[tuple[str, tuple[str, ...]], ...],
) -> list[list[object]]:
    return [[kind, list(stripped)] for kind, stripped in phases]


def one_active_rows() -> tuple[dict[str, object], ...]:
    """The exact 30 rows, including the normalized proof data."""

    rows: list[dict[str, object]] = []
    for pair, descriptor in selector._incidence_rows(1):
        normalized = structure._normalized(pair, descriptor)
        supports = tuple(normalized["supports"])
        caps = tuple(normalized["caps"])
        phases = tuple(
            structure._linkage_phase(support) for support in supports
        )
        category = selector.one_active_graph_category(pair, descriptor)
        active_coordinate, = tier._active_coordinates(descriptor)
        lower_supports = tuple(
            tuple(
                name
                for name in support
                if name not in structure.TOP_MENU
            )
            for support in supports
        )
        direct_sides = tuple(
            side
            for side, (kind, stripped) in enumerate(phases)
            if kind == "mixed_killed" and "0" in stripped
        )
        rows.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "active_species": "ABC"[active_coordinate],
                "normalized_supports": [list(item) for item in supports],
                "normalized_caps": list(caps),
                "phase_signature": _phase_payload(phases),
                "lower_supports": [list(item) for item in lower_supports],
                "direct_active_source_linkage_sides": list(direct_sides),
                "graph_category": category,
            }
        )

    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    return tuple(rows)


def normalized_profiles() -> tuple[dict[str, object], ...]:
    """Aggregate the 30 physical rows into their 15 exact support profiles."""

    counts: Counter[tuple[object, ...]] = Counter()
    for row in one_active_rows():
        key = (
            tuple(tuple(item) for item in row["normalized_supports"]),
            tuple(row["normalized_caps"]),
            tuple(
                (kind, tuple(stripped))
                for kind, stripped in row["phase_signature"]
            ),
            row["graph_category"],
        )
        counts[key] += 1
    return tuple(
        {
            "normalized_supports": [list(item) for item in key[0]],
            "normalized_caps": list(key[1]),
            "phase_signature": _phase_payload(key[2]),
            "graph_category": key[3],
            "physical_incidences": count,
        }
        for key, count in sorted(counts.items(), key=lambda item: repr(item[0]))
    )


def _changed_coordinates(top: int) -> tuple[int, ...]:
    first, second = sorted(tier._nodes(top))
    y = closure.COMPLEXES[first]
    z = closure.COMPLEXES[second]
    return tuple(index for index in range(3) if y[index] != z[index])


def all_active_rows() -> tuple[dict[str, object], ...]:
    """The exact 94 rows and their curvature-cofactor witnesses."""

    rows: list[dict[str, object]] = []
    for pair, descriptor in selector._incidence_rows(3):
        side, top = all_active.whole_top_linkage(pair, descriptor)
        lower = pair[1 - side]
        levels = {
            node: rank
            for rank, block in enumerate(descriptor.partition)
            for node in block
        }
        lower_rank = min(levels[node] for node in tier._nodes(lower))
        cofactors = gluing.curvature_cofactors(pair, descriptor)
        cofactor_rows = tuple(
            {
                "complex": closure.NAMES[node],
                "tier_rank": levels[node],
                "at_or_below_lower_maximum": levels[node] >= lower_rank,
            }
            for node in cofactors
        )
        rows.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "top_side": side,
                "top_support": list(closure.support(top)),
                "lower_support": list(closure.support(lower)),
                "changed_species": [
                    "ABC"[index] for index in _changed_coordinates(top)
                ],
                "lower_maximal_tier_rank": lower_rank,
                "curvature_cofactors": list(cofactor_rows),
                "direct_entropy_safe": gluing.direct_entropy_safe(
                    pair, descriptor
                ),
            }
        )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    return tuple(rows)


def pair_tops() -> tuple[dict[str, object], ...]:
    """Check that the same two-node top is used by every cone of a pair."""

    result: list[dict[str, object]] = []
    for pair in sorted(selector.selected_pairs(), key=closure.pair_payload):
        descriptors = tuple(
            descriptor
            for candidate, descriptor in selector._incidence_rows(3)
            if candidate == pair
        )
        tops = {
            all_active.whole_top_linkage(pair, descriptor)
            for descriptor in descriptors
        }
        assert len(tops) == 1
        side, top = next(iter(tops))
        first, second = sorted(tier._nodes(top))
        y = closure.COMPLEXES[first]
        z = closure.COMPLEXES[second]
        result.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "all_active_failed_cones": len(descriptors),
                "top_side": side,
                "top_support": list(closure.support(top)),
                "canonical_top_reaction_vector": [
                    z[index] - y[index] for index in range(3)
                ],
                "rate_adjustment_constraint": (
                    "ell_dot_(z-y)=-log(kappa_yz/kappa_zy)"
                ),
            }
        )
    return tuple(result)


def _falling(value: int, degree: int) -> int:
    if degree < 0 or value < degree:
        raise ValueError("falling factorial requires value >= degree >= 0")
    return factorial(value) // factorial(value - degree)


def _factorial_ratio(
    state: tuple[int, int, int], jump: tuple[int, int, int]
) -> Fraction:
    result = Fraction(1)
    for value, delta in zip(state, jump):
        endpoint = value + delta
        if endpoint < 0:
            raise ValueError("jump leaves the population lattice")
        result *= Fraction(factorial(endpoint), factorial(value))
    return result


def discrete_endpoint_identity_samples() -> tuple[dict[str, object], ...]:
    """Exact integer checks behind the discrete detailed-balance formula.

    For ``d=z-y``, the identity checked is

        prod_i (x_i+d_i)!/x_i! = falling(x+d,z)/falling(x,y).

    Multiplying by ``kappa_zy/kappa_yz`` gives
    ``exp(F_ell(x+d)-F_ell(x))`` when
    ``ell.d=-log(kappa_yz/kappa_zy)``.
    """

    samples: list[dict[str, object]] = []
    for names in (("2A", "BC"), ("AC", "BC")):
        y = closure.COMPLEXES[closure.NAME_TO_INDEX[names[0]]]
        z = closure.COMPLEXES[closure.NAME_TO_INDEX[names[1]]]
        jump = tuple(z[index] - y[index] for index in range(3))
        for state in ((7, 8, 9), (11, 13, 17)):
            endpoint = tuple(
                state[index] + jump[index] for index in range(3)
            )
            lhs = _factorial_ratio(state, jump)
            numerator = 1
            denominator = 1
            for index in range(3):
                numerator *= _falling(endpoint[index], z[index])
                denominator *= _falling(state[index], y[index])
            rhs = Fraction(numerator, denominator)
            assert lhs == rhs
            samples.append(
                {
                    "top_support": list(names),
                    "state": list(state),
                    "jump": list(jump),
                    "ratio": f"{lhs.numerator}/{lhs.denominator}",
                    "identity_holds": True,
                }
            )
    return tuple(samples)


def prospective_pair_arithmetic() -> dict[str, object]:
    """Freeze disjointness inside the claim-neutral prospective 795."""

    positive, signed, _residual = feasibility._residual_failures()
    parent = selector.prospective_after_pairs()
    selected = selector.selected_pairs()
    after = parent - selected
    prior = frozenset().union(*prospective.certified_branch_sets().values())

    assert selected <= parent
    assert not (parent & prior)
    assert not (selected & prior)
    assert (len(parent & positive), len(parent & signed), len(parent)) == (
        759,
        36,
        795,
    )
    assert (
        len(selected & positive),
        len(selected & signed),
        len(selected),
    ) == (26, 0, 26)
    assert (len(after & positive), len(after & signed), len(after)) == (
        733,
        36,
        769,
    )
    assert closure.pair_fingerprint(after) == EXPECTED_AFTER_769_SHA256
    return {
        "authoritative_prospective_parent": {
            "positive": 759,
            "signed": 36,
            "total": 795,
            "pair_sha256": closure.pair_fingerprint(parent),
        },
        "selected_candidate": {
            "positive": 26,
            "signed": 0,
            "total": 26,
            "pair_sha256": closure.pair_fingerprint(selected),
            "subset_of_parent": True,
            "prior_certified_overlap": 0,
        },
        "claim_neutral_remainder_after_candidate": {
            "positive": 733,
            "signed": 36,
            "total": 769,
            "pair_sha256": closure.pair_fingerprint(after),
        },
    }


def certificate() -> dict[str, object]:
    one_rows = one_active_rows()
    profiles = normalized_profiles()
    all_rows = all_active_rows()
    tops = pair_tops()

    category_histogram = Counter(row["graph_category"] for row in one_rows)
    assert category_histogram == {
        "mixed_C_source_direct_down_0": 20,
        "family_iii_origin_down_0": 8,
        "family_iii_origin_no_history": 2,
    }
    assert len(one_rows) == 30 and len(profiles) == 15
    assert all(row["normalized_caps"] == [0, 0] for row in one_rows)
    assert all(
        [phase[0] for phase in row["phase_signature"]]
        == ["mixed_killed", "mixed_killed"]
        for row in one_rows
    )

    direct = tuple(
        row
        for row in one_rows
        if row["graph_category"] == "mixed_C_source_direct_down_0"
    )
    family_down = tuple(
        row
        for row in one_rows
        if row["graph_category"] == "family_iii_origin_down_0"
    )
    family_no_history = tuple(
        row
        for row in one_rows
        if row["graph_category"] == "family_iii_origin_no_history"
    )
    assert all(row["direct_active_source_linkage_sides"] for row in direct)
    assert all(
        not row["direct_active_source_linkage_sides"]
        for row in family_down + family_no_history
    )
    assert all(
        {tuple(phase[1]) for phase in row["phase_signature"]}
        == {("A",), ("B",)}
        for row in family_down + family_no_history
    )
    assert all(
        any(
            "0" in lower and len(lower) > 1
            for lower in row["lower_supports"]
        )
        for row in family_down
    )
    assert all(
        all("0" not in lower for lower in row["lower_supports"])
        for row in family_no_history
    )

    assert len(all_rows) == 94 and len(tops) == 26
    assert Counter(
        ",".join(row["top_support"]) for row in all_rows
    ) == {"2A,BC": 40, "AC,BC": 54}
    assert all(row["direct_entropy_safe"] for row in all_rows)
    assert all(
        cofactor["at_or_below_lower_maximum"]
        for row in all_rows
        for cofactor in row["curvature_cofactors"]
    )
    assert all(len(row["top_support"]) == 2 for row in tops)

    hashes = {
        "one_active_rows_sha256": _encoded_sha256(one_rows),
        "normalized_profiles_sha256": _encoded_sha256(profiles),
        "all_active_rows_sha256": _encoded_sha256(all_rows),
        "pair_tops_sha256": _encoded_sha256(tops),
    }
    expected = {
        "one_active_rows_sha256": EXPECTED_ONE_ROWS_SHA256,
        "normalized_profiles_sha256": EXPECTED_NORMALIZED_PROFILES_SHA256,
        "all_active_rows_sha256": EXPECTED_ALL_ACTIVE_ROWS_SHA256,
        "pair_tops_sha256": EXPECTED_PAIR_TOPS_SHA256,
    }
    for name, digest in expected.items():
        assert hashes[name] == digest

    payload: dict[str, object] = {
        "claim_scope": (
            "finite support/premise certificate plus independently audited "
            "analytic and pair-level recurrence theorem"
        ),
        "selector": {
            "pairs": len(selector.selected_pairs()),
            "pair_sha256": closure.pair_fingerprint(
                selector.selected_pairs()
            ),
            "one_active_incidences": len(one_rows),
            "two_active_incidences": 0,
            "all_active_incidences": len(all_rows),
        },
        "prospective_pair_arithmetic": prospective_pair_arithmetic(),
        "one_active_scope_extension": {
            "normalized_profiles": len(profiles),
            "category_histogram": dict(sorted(category_histogram.items())),
            "all_normalized_caps_are_origin": True,
            "all_rows_are_two_mixed_linkages": True,
            "direct_rows_have_physical_active_source": True,
            "family_iii_down_rows_have_nontrivial_zero_lower_support": True,
            "family_iii_no_history_rows_have_no_zero_complex": True,
        },
        "all_active_powered_lift_premises": {
            "fixed_two_node_top_for_each_pair": True,
            "top_support_incidence_histogram": {
                "2A,BC": 40,
                "AC,BC": 54,
            },
            "all_curvature_cofactors_at_or_below_lower_maximum": True,
            "common_rate_adjustment_equation": (
                "ell_dot_(z-y)=-log(kappa_yz/kappa_zy)"
            ),
            "discrete_endpoint_identity_samples": (
                discrete_endpoint_identity_samples()
            ),
        },
        "hashes": hashes,
        "independent_audit_verdict": "PASS",
        "analytic_one_active_scope_extension_certified": True,
        "analytic_powered_all_active_lift_certified": True,
        "candidate_26_pair_recurrence_certified": True,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    assert digest == EXPECTED_PAYLOAD_SHA256, (
        digest,
        EXPECTED_PAYLOAD_SHA256,
    )
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
