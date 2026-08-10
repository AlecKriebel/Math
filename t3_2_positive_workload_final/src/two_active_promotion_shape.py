"""Exact fast-phase split inside the two-active promotion incidences.

This is a support/tier certificate only.  It separates promotion incidences
with no wholly-top linkage from the fifty incidences having one, and freezes
the six possible whole-top supports.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import two_active_phase_gate as phase


EXPECTED_ROWS_SHA256 = (
    "3e3616f8099b93ccd860db2e3320cd90300c8adf896f12127cae1a32f7d7bfe5"
)


def rows() -> tuple[dict[str, object], ...]:
    result = []
    for pair, descriptor, category in phase.incidences():
        if not category.startswith("promotion_"):
            continue
        whole = phase._whole_top_linkages(pair, descriptor)
        result.append(
            {
                "pair": closure.pair_payload(pair),
                "weight": descriptor.weight,
                "caps": descriptor.caps,
                "category": category,
                "whole_top": tuple(closure.support(mask) for mask in whole),
            }
        )
    return tuple(result)


def _row_hash(items: tuple[dict[str, object], ...]) -> str:
    encoded = json.dumps(items, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def _pair_key(row: dict[str, object]) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(part) for part in row["pair"])


def certificate() -> dict[str, object]:
    items = rows()
    no_phase = tuple(row for row in items if not row["whole_top"])
    with_phase = tuple(row for row in items if row["whole_top"])
    support_histogram = Counter(
        ",".join(row["whole_top"][0]) for row in with_phase
    )
    finite_supports = {"A,B", "A,BC", "B,2A", "B,AC"}
    open_poisson_supports = {"A,B,AC", "A,B,BC"}
    assert set(support_histogram) == finite_supports | open_poisson_supports
    finite_rows = tuple(
        row
        for row in with_phase
        if ",".join(row["whole_top"][0]) in finite_supports
    )
    poisson_rows = tuple(
        row
        for row in with_phase
        if ",".join(row["whole_top"][0]) in open_poisson_supports
    )
    fingerprint = _row_hash(items)
    assert fingerprint == EXPECTED_ROWS_SHA256
    assert all(row["caps"].count(0) == 1 for row in items)
    return {
        "claim_scope": "finite support/tier split only; no recurrence claim",
        "promotion_incidences": len(items),
        "promotion_pairs": len({_pair_key(row) for row in items}),
        "no_wholly_top_incidences": len(no_phase),
        "no_wholly_top_pairs": len({_pair_key(row) for row in no_phase}),
        "wholly_top_incidences": len(with_phase),
        "wholly_top_pairs": len({_pair_key(row) for row in with_phase}),
        "pair_overlap_between_modes": len(
            {_pair_key(row) for row in no_phase}
            & {_pair_key(row) for row in with_phase}
        ),
        "finite_shell_incidences": len(finite_rows),
        "poisson_phase_incidences": len(poisson_rows),
        "whole_top_support_histogram": dict(sorted(support_histogram.items())),
        "rows_sha256": fingerprint,
        "analytic_theorem_certified": False,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
