"""Finite support checks for the rank-one carrier theorem.

The executable certifies incidence counts and support geometry and records
the independently audited local corrected-factorial endpoint theorem.  Its
local flag is deliberately separate from pair-level recurrence and global
T3-2 certification.
"""

from __future__ import annotations

from hashlib import sha256
import json
from collections import Counter

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import two_active_phase_gate as phase


def _lower_data(pair, descriptor):
    top = phase._whole_top_linkages(pair, descriptor)[0]
    lower = pair[1] if pair[0] == top else pair[0]
    nodes = tier._nodes(lower)
    orders = {
        node: sum(
            descriptor.weight[i] * tier.COMPLEXES[node][i]
            for i in range(3)
        )
        for node in nodes
    }
    maximum = max(orders.values())
    maximal = frozenset(node for node, value in orders.items() if value == maximum)
    return top, lower, nodes, maximum, maximal


def certificate() -> dict[str, object]:
    rows = tuple(
        (pair, descriptor)
        for pair, descriptor, category in phase.incidences()
        if category == "closed_rank_one_top_phase"
    )
    categories = {
        name: tuple(
            (pair, descriptor)
            for pair, descriptor in rows
            if phase.rank_one_activation_category(pair, descriptor) == name
        )
        for name in (
            "lower_top_seeded",
            "top_phase_activates",
            "lower_layer_activation_needed",
            "zero_boundary_phase_only",
        )
    }

    all_maximal_proper = True
    all_maximum_one = True
    for pair, descriptor in rows:
        _, _, nodes, maximum, maximal = _lower_data(pair, descriptor)
        all_maximal_proper &= bool(maximal) and maximal != nodes
        all_maximum_one &= maximum == 1

    allowed_dormant = {
        tier.NAMES.index(name) for name in ("0", "C", "2C", "AC", "BC")
    }
    dormant_payload = []
    for pair, descriptor in categories["lower_layer_activation_needed"]:
        _, lower, nodes, maximum, maximal = _lower_data(pair, descriptor)
        inactive = tuple(i for i, value in enumerate(descriptor.weight) if value == 0)
        assert inactive == (2,)
        assert descriptor.caps[2] == 0
        assert nodes <= allowed_dormant
        assert tier.NAMES.index("0") in nodes
        assert bool(nodes & {tier.NAMES.index("C"), tier.NAMES.index("2C")})
        assert bool(nodes & {tier.NAMES.index("AC"), tier.NAMES.index("BC")})
        assert maximal <= {tier.NAMES.index("AC"), tier.NAMES.index("BC")}
        enabled = frozenset(
            node for node in nodes if tier._enabled(node, descriptor.caps)
        )
        assert enabled == {tier.NAMES.index("0")}
        dormant_payload.append(
            {
                "pair": closure.pair_payload(pair),
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "lower": list(closure.support(lower)),
                "maximal": [tier.NAMES[node] for node in sorted(maximal)],
            }
        )

    dormant_payload.sort(
        key=lambda row: (
            row["pair"], row["weight"], row["caps"], row["lower"], row["maximal"]
        )
    )
    dormant_hash = sha256(
        json.dumps(dormant_payload, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()

    dormant_top_histogram = Counter()
    for pair, descriptor in categories["lower_layer_activation_needed"]:
        top = phase._whole_top_linkages(pair, descriptor)[0]
        dormant_top_histogram[
            ",".join(tier.NAMES[node] for node in sorted(tier._nodes(top)))
        ] += 1

    top_activation_geometry = True
    for pair, descriptor in categories["top_phase_activates"]:
        top, _, lower_nodes, _, _ = _lower_data(pair, descriptor)
        enabled_top = tuple(
            node
            for node in tier._nodes(top)
            if tier._enabled(node, descriptor.caps)
        )
        enabled_lower = tuple(
            node
            for node in lower_nodes
            if tier._enabled(node, descriptor.caps)
        )
        top_activation_geometry &= (
            len(enabled_top) == 1
            and sum(tier.COMPLEXES[enabled_top[0]]) == 2
            and all(
                sum(
                    descriptor.weight[i] * tier.COMPLEXES[node][i]
                    for i in range(3)
                )
                == 0
                for node in enabled_lower
            )
        )

    return {
        "rank_one_incidences": len(rows),
        "seeded_incidences": len(categories["lower_top_seeded"]),
        "top_activation_incidences": len(categories["top_phase_activates"]),
        "lower_activation_incidences": len(
            categories["lower_layer_activation_needed"]
        ),
        "finite_zero_boundary_incidences": len(
            categories["zero_boundary_phase_only"]
        ),
        "multichannel_direct_coverage": (
            len(categories["lower_top_seeded"])
            + len(categories["top_phase_activates"])
        ),
        "candidate_activation_coverage": len(
            categories["lower_layer_activation_needed"]
        ),
        "all_maximal_lower_tiers_proper": all_maximal_proper,
        "all_maximal_lower_weights_one": all_maximum_one,
        "lower_activation_top_support_histogram": dict(
            sorted(dormant_top_histogram.items())
        ),
        "top_activation_has_quadratic_top_source_and_only_weight_zero_lower_competitors": (
            top_activation_geometry
        ),
        "dormant_geometry_sha256": dormant_hash,
        "corrected_factorial_local_endpoint_certified": True,
        "pair_level_recurrence_certified": False,
        "global_t3_2_certified": False,
        "analytic_theorem_certified": False,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
