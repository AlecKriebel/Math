"""Exact pointwise additive-scalar obstruction for the mixed rank-two seven.

At a zero-cap one-active axis all top reactions and the lower death are
disabled.  The sole lower birth has zero uncorrected factorial increment
and increases total workload by one.  Thus no scalar ``W + phi(H)`` with
eventually increasing ``phi`` can have negative pointwise drift there.

This is not a recurrence obstruction; it isolates why a stopped episode or
state-dependent corrector is necessary.  Every claim flag remains false.
"""

from __future__ import annotations

from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import rank_two_mixed_profile_7 as branch


EXPECTED_ROWS_SHA256 = (
    "d45f7b10a144060b84c2153b30c17e0e97e63fadf8cb05a0e236ab06096dd77b"
)
EXPECTED_PAYLOAD_SHA256 = (
    "627a994b83581237f03257ac51c94fe01f501904a6e3414818a259f807f972ef"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def dormant_axis_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for pair in sorted(branch.selected_pairs(), key=closure.pair_payload):
        zero_rows = tuple(
            row
            for row in branch.one_active_rows()
            if row["pair"]
            == [list(part) for part in closure.pair_payload(pair)]
            and row["normalized_caps"] == [0, 0]
        )
        assert zero_rows
        for row in zero_rows:
            top = row["normalized_supports"][1]
            assert all(name not in {"0", "C", "2C"} for name in top)
            assert all("A" in name or "B" in name for name in top)
            rows.append(
                {
                    "pair": row["pair"],
                    "physical_active_species": row[
                        "physical_active_species"
                    ],
                    "normalized_axis_state": [0, 0, "n"],
                    "normalized_top_support": top,
                    "enabled_reactions": ["0->A"],
                    "delta_uncorrected_factorial": 0,
                    "delta_W": 0,
                    "delta_H": 1,
                    "generator_on_W_plus_phi_H": (
                        "kappa_0A*(phi(n+1)-phi(n))"
                    ),
                }
            )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    assert len({json.dumps(row["pair"]) for row in rows}) == 7
    return tuple(rows)


def certificate() -> dict[str, object]:
    rows = dormant_axis_rows()
    rows_hash = _encoded_sha256(rows)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256

    payload: dict[str, object] = {
        "claim_scope": (
            "exact obstruction to pointwise additive scalarization only"
        ),
        "selector": {
            "pairs": 7,
            "pair_sha256": closure.pair_fingerprint(
                branch.selected_pairs()
            ),
            "zero_cap_axis_rows": len(rows),
        },
        "obstruction": {
            "scalar_class": "V=W+phi(H)",
            "hypothesis_on_phi": (
                "phi(n+1)>phi(n) for all sufficiently large n"
            ),
            "axis_generator": (
                "L V=kappa_0A*(phi(n+1)-phi(n))>0"
            ),
            "orientation_and_rate_scope": (
                "every strong top orientation and every positive rate vector"
            ),
            "consequence": (
                "a stopped activation/service episode or a state-dependent "
                "corrector is necessary"
            ),
        },
        "rows": list(rows),
        "hashes": {"rows_sha256": rows_hash},
        "recurrence_obstruction_claimed": False,
        "candidate_7_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
