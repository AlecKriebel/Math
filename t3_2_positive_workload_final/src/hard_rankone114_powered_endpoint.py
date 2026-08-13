"""Finite premises for the analytic powered rank-one hard-114 corollary."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import hard333_pair_composition as composition
import two_active_dormant_407_certificate as hard
import two_active_phase_gate as phase


EXPECTED_ROWS_SHA256 = "5478bf16e158420669fd1fe07a7f763de25e8c5a25452a43abff65e6aa86d54a"
EXPECTED_PAYLOAD_SHA256 = "2b9280cb7ef663d57c249d27d60d2081fb7cf194a3de0ae95b517e5f785efdcf"


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def rows() -> tuple[dict[str, object], ...]:
    correction = {
        tuple(tuple(part) for part in row["pair"]): row[
            "pair_fixed_correction_family"
        ]
        for row in composition.common_rows()
    }
    result: list[dict[str, object]] = []
    for pair, descriptor, category in phase.incidences():
        if pair not in hard.selected_pairs() or category != "closed_rank_one_top_phase":
            continue
        if pair in composition.hb_switch_pairs():
            correction_family = "reversible_top_adjusted_ell"
        else:
            key = tuple(tuple(part) for part in closure.pair_payload(pair))
            correction_family = correction[key]
        top, = phase._whole_top_linkages(pair, descriptor)
        result.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "top": list(closure.support(top)),
                "activation": phase.rank_one_activation_category(pair, descriptor),
                "correction_family": correction_family,
            }
        )
    result.sort(key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")))
    return tuple(result)


def certificate() -> dict[str, object]:
    data = rows()
    rows_hash = _digest(data)
    activation = Counter(row["activation"] for row in data)
    corrections = Counter(row["correction_family"] for row in data)
    pairs = {
        tuple(tuple(part) for part in row["pair"])
        for row in data
    }
    assert len(data) == 114
    assert len(pairs) == 38
    assert activation == {
        "lower_top_seeded": 110,
        "top_phase_activates": 2,
        "lower_layer_activation_needed": 2,
    }
    assert corrections == {
        "reversible_top_adjusted_ell": 90,
        "directed_triple_adjusted_ell": 24,
    }
    hw_payloads = {
        tuple(tuple(part) for part in closure.pair_payload(pair))
        for pair in composition.hw_switch_pairs()
    }
    assert not any(
        tuple(tuple(part) for part in row["pair"]) in hw_payloads
        for row in data
    )
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256
    payload = {
        "claim_scope": "finite premises for the analytic powered rank-one hard-114 theorem",
        "incidences": len(data),
        "pairs": len(pairs),
        "activation_histogram": dict(sorted(activation.items())),
        "correction_histogram": dict(sorted(corrections.items())),
        "rows_sha256": rows_hash,
        "positive_overshoot_input_independently_audited": True,
        "rankone114_composition_independently_audited": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    payload_hash = _digest(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert payload_hash == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), sort_keys=True, indent=2))
