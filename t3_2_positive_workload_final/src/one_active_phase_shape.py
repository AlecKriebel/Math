"""Exact shape of the countable phase in the candidate one-active branch.

This is a finite support/tier certificate.  It does not assert recurrence.
It identifies every linkage that is wholly contained in the active-degree-one
menu along a pair whose affine-feasible failures are all one-active.
"""

from __future__ import annotations

from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import stoichiometric_gate_feasibility as feasibility


Pair = closure.Pair

EXPECTED_ROWS_SHA256 = (
    "5086c198fab678cba7e8ce8d10d6621887456f9f7caa8a188e5d68a214c52854"
)


def candidate_pairs() -> tuple[Pair, ...]:
    """Pairs whose nonempty affine-feasible failure set is all one-active."""

    positive, signed, _ = feasibility._residual_failures()
    result = []
    for pair in positive | signed:
        failures = feasibility.feasible_failing_descriptors(pair)
        if failures and all(
            len(tier._active_coordinates(descriptor)) == 1
            for descriptor in failures
        ):
            result.append(pair)
    return tuple(sorted(result, key=closure.pair_payload))


def candidate_incidences():
    """All affine-feasible failed descriptors on the candidate pairs."""

    return tuple(
        (pair, descriptor)
        for pair in candidate_pairs()
        for descriptor in feasibility.feasible_failing_descriptors(pair)
    )


def _stripped_support(
    mask: int,
    active_coordinate: int,
) -> tuple[tuple[int, int, int], ...] | None:
    """Strip the active molecule if a linkage lies wholly in the top menu."""

    nodes = tuple(sorted(tier._nodes(mask)))
    if not all(
        closure.COMPLEXES[node][active_coordinate] == 1 for node in nodes
    ):
        return None
    stripped = []
    for node in nodes:
        vector = list(closure.COMPLEXES[node])
        vector[active_coordinate] -= 1
        stripped.append(tuple(vector))
    return tuple(sorted(stripped))


def wholly_top_rows() -> tuple[dict[str, object], ...]:
    """Every wholly top linkage in the candidate incidence table."""

    rows = []
    for pair, descriptor in candidate_incidences():
        active, = tier._active_coordinates(descriptor)
        for side, mask in enumerate(pair):
            stripped = _stripped_support(mask, active)
            if stripped is None:
                continue
            rows.append(
                {
                    "pair": closure.pair_payload(pair),
                    "weight": descriptor.weight,
                    "caps": descriptor.caps,
                    "active_coordinate": active,
                    "side": side,
                    "top_support": closure.support(mask),
                    "stripped_support": stripped,
                }
            )
    return tuple(
        sorted(
            rows,
            key=lambda row: (
                row["pair"],
                row["weight"],
                row["caps"],
                row["side"],
            ),
        )
    )


def _is_open_pair(row: dict[str, object]) -> bool:
    support = row["stripped_support"]
    assert isinstance(support, tuple)
    if len(support) != 2 or (0, 0, 0) not in support:
        return False
    nonzero, = (vector for vector in support if vector != (0, 0, 0))
    return sum(nonzero) == 1


def _fingerprint(rows: tuple[dict[str, object], ...]) -> str:
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def certificate() -> dict[str, object]:
    pairs = candidate_pairs()
    incidences = candidate_incidences()
    rows = wholly_top_rows()
    open_rows = tuple(row for row in rows if _is_open_pair(row))

    # There is no conservative pair {U,V}, open triple {0,U,V}, or any
    # larger wholly top phase left in this affine-filtered branch.
    assert rows == open_rows
    assert len({(row["pair"], row["weight"], row["caps"]) for row in rows}) == len(rows)

    return {
        "claim_scope": (
            "finite affine/tier support classification only; the analytic "
            "countable-phase service theorem remains a separate obligation"
        ),
        "candidate_pairs": len(pairs),
        "candidate_incidences": len(incidences),
        "wholly_top_incidences": len(rows),
        "wholly_top_pairs": len({row["pair"] for row in rows}),
        "only_wholly_top_shape": "one-dimensional open pair {0,U}",
        "rows_sha256": _fingerprint(rows),
        "rows": rows,
        "analytic_theorem_certified": False,
    }


def main() -> None:
    result = certificate()
    assert result["candidate_pairs"] == 1227
    assert result["candidate_incidences"] == 3297
    assert result["wholly_top_incidences"] == 222
    assert result["wholly_top_pairs"] == 74
    assert result["rows_sha256"] == EXPECTED_ROWS_SHA256
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
