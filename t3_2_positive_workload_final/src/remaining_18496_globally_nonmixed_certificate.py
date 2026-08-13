"""Exact support-only bridge from the 18,496 remainder to global nonmixing.

The one-active symbolic theorem defines a pair to be globally nonmixed when
its two linkage supports have the same available/shielded classifier value
in every two-active workload cell, for every choice of the two active
coordinates.  This module replays that literal definition on the exact
18,496-pair remainder.

Only finite support identities are computed.  No orientations, rates,
population states, reaction histories, or stochastic estimates are used.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import outside_mixed_remaining_18496_certificate as remainder


Mask = int
Pair = closure.Pair

# The four primitive representatives, together with active-coordinate
# exchange.  Equality is unchanged by exchange and is listed only once.
WORKLOADS_2D = (
    (1, 1),
    (2, 3),
    (3, 2),
    (1, 2),
    (2, 1),
    (1, 3),
    (3, 1),
)

ACTIVE_PAIRS = ((0, 1), (0, 2), (1, 2))


def _nodes(mask: Mask) -> tuple[int, ...]:
    return tuple(
        node for node in range(len(closure.COMPLEXES)) if mask >> node & 1
    )


def classify_shielded(
    mask: Mask,
    active: tuple[int, int],
    workload: tuple[int, int],
) -> bool:
    """Literal ordered Q/U/C/S available-versus-shielded classifier."""

    nodes = _nodes(mask)
    weight = [0, 0, 0]
    weight[active[0]], weight[active[1]] = workload
    values = {
        node: sum(
            weight[coordinate] * closure.COMPLEXES[node][coordinate]
            for coordinate in range(3)
        )
        for node in nodes
    }
    maximum = max(values.values())
    top = frozenset(node for node in nodes if values[node] == maximum)

    # Flat top.
    if len(top) == len(nodes):
        return True

    # Active quadratic top.
    if any(
        sum(closure.COMPLEXES[node][coordinate] for coordinate in active) >= 2
        for node in top
    ):
        return False

    # One-active-particle-flat obstruction.
    top_active_support = tuple(
        coordinate
        for coordinate in active
        if any(closure.COMPLEXES[node][coordinate] for node in top)
    )
    if all(
        sum(
            closure.COMPLEXES[node][coordinate]
            for coordinate in top_active_support
        )
        == 1
        for node in nodes
    ):
        return True

    # Unary top.
    if any(sum(closure.COMPLEXES[node]) == 1 for node in top):
        return False

    # Shared bounded cofactor.
    (bounded,) = tuple(
        coordinate for coordinate in range(3) if coordinate not in active
    )
    if any(closure.COMPLEXES[node][bounded] for node in top) and any(
        closure.COMPLEXES[node][bounded] for node in set(nodes) - set(top)
    ):
        return False

    # Otherwise shielded.
    return True


@lru_cache(maxsize=None)
def support_signature(mask: Mask) -> tuple[bool, ...]:
    return tuple(
        classify_shielded(mask, active, workload)
        for active in ACTIVE_PAIRS
        for workload in WORKLOADS_2D
    )


def is_globally_nonmixed(pair: Pair) -> bool:
    return support_signature(pair[0]) == support_signature(pair[1])


def pair_payload(pair: Pair) -> tuple[tuple[str, ...], tuple[str, ...]]:
    return closure.pair_payload(pair)


def _digest(payload: object) -> str:
    return sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@lru_cache(maxsize=1)
def certificate() -> dict[str, object]:
    pairs = remainder.remainder_pairs()
    violations = tuple(sorted(
        (pair for pair in pairs if not is_globally_nonmixed(pair)),
        key=pair_payload,
    ))
    manifest = [pair_payload(pair) for pair in sorted(pairs, key=pair_payload)]
    signatures = {
        ",".join(closure.support(mask)): "".join(
            "S" if value else "A" for value in support_signature(mask)
        )
        for mask in sorted({mask for pair in pairs for mask in pair})
    }
    result = {
        "claim_scope": (
            "finite support/workload classifier identity only; no recurrence claim"
        ),
        "active_coordinate_pairs": len(ACTIVE_PAIRS),
        "workload_cells_per_active_pair": len(WORKLOADS_2D),
        "remainder_pairs": len(pairs),
        "globally_nonmixed_pairs": len(pairs) - len(violations),
        "violations": len(violations),
        "pair_manifest_sha256": _digest(manifest),
        "support_signature_sha256": _digest(signatures),
    }
    assert result["remainder_pairs"] == 18_496
    assert result["globally_nonmixed_pairs"] == 18_496
    assert result["violations"] == 0
    return result


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
