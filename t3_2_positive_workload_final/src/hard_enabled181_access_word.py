"""Finite scope certificate for the analytic hard enabled-181 corollary."""

from __future__ import annotations

from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import two_active_dormant_407_certificate as hard
import two_active_easy_common_w as easy
import two_active_phase_gate as phase


EXPECTED_ROWS_SHA256 = "5e8c7399b0635d616fba850ea1c6aeccfe6e9ebcad8501c6895b8e2eb7dcd0f6"
EXPECTED_PAYLOAD_SHA256 = "500469227922b21d38ce135e2af00fe37446773f04e26e5208e97e6a723d442b"


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def rows() -> tuple[dict[str, object], ...]:
    hard_rows = tuple(
        (pair, descriptor)
        for pair, descriptor, category in phase.incidences()
        if pair in hard.selected_pairs()
        and category == "promotion_enabled_top_seed"
    )
    seeded_929 = {
        (pair, descriptor)
        for pair, descriptor in easy.promotion_incidences()
        if easy.promotion_family(pair, descriptor) == "seeded_access_word"
    }
    assert set(hard_rows) <= seeded_929
    result = tuple(
        sorted(
            (
                {
                    "pair": [list(part) for part in closure.pair_payload(pair)],
                    "weight": list(descriptor.weight),
                    "caps": list(descriptor.caps),
                    "audited_seeded_929_member": True,
                }
                for pair, descriptor in hard_rows
            ),
            key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")),
        )
    )
    assert len(result) == 181
    return result


def certificate() -> dict[str, object]:
    data = rows()
    rows_hash = _digest(data)
    pairs = {tuple(tuple(part) for part in row["pair"]) for row in data}
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256
    payload = {
        "claim_scope": "finite subset identity for the analytic hard enabled-181 access-word corollary",
        "incidences": len(data),
        "pairs": len(pairs),
        "all_rows_are_members_of_audited_seeded_929": True,
        "arbitrary_fixed_ell": True,
        "rows_sha256": rows_hash,
        "enabled181_corollary_independently_audited": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    payload_hash = _digest(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert payload_hash == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), sort_keys=True, indent=2))
