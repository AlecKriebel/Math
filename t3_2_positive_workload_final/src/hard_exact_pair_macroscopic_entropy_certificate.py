"""Finite premises for the proof-first macroscopic exact-pair theorem.

This module freezes support identities only.  It does not infer a stochastic
theorem from finite enumeration and keeps every certification flag false.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import two_active_dormant_407_certificate as hard


EXPECTED_ROWS_SHA256 = (
    "e931d5277596c5084d89bf63b3963a6fe0ecb202be6549075b47f89c30b0a33b"
)
EXPECTED_PAYLOAD_SHA256 = (
    "2a6599b66e6b7db1c7c1701ad65d23410cb33694b75cfc9819ec955267debaf6"
)


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _complex(name: str) -> tuple[int, int]:
    return {
        "0": (0, 0),
        "U": (1, 0),
        "2U": (2, 0),
        "I": (0, 1),
        "2I": (0, 2),
        "UI": (1, 1),
    }[name]


def exact_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for row in hard.normalized_templates():
        p, q = map(int, row["normalized_ratio"])
        proper = tuple(row["proper_support"])
        lower = tuple(row["other_support"])
        if len(proper) != 2 or "VI" not in proper:
            continue
        base, = tuple(name for name in proper if name != "VI")
        if base not in {"0", "U", "2U"}:
            continue
        a = {"0": 0, "U": 1, "2U": 2}[base]
        phi = {
            name: p * (c + a * b) - q * b
            for name in lower
            for c, b in (_complex(name),)
        }
        maximum = max(phi.values())
        maximizers = tuple(sorted(name for name, value in phi.items() if value == maximum))
        rows.append(
            {
                "ratio": [p, q],
                "a": a,
                "proper": list(proper),
                "lower": list(lower),
                "phi": dict(sorted(phi.items())),
                "maximizers": list(maximizers),
                "maximizer_set_proper": len(maximizers) < len(lower),
                "maximum_phi": maximum,
                "primitive_interruption_gap": q - p * max(
                    _complex(name)[0] for name in lower
                ),
            }
        )
    rows.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    return tuple(rows)


def certificate() -> dict[str, object]:
    rows = exact_rows()
    row_hash = _digest(rows)
    ratio_histogram = Counter(tuple(row["ratio"]) for row in rows)
    maximizer_histogram = Counter(tuple(row["maximizers"]) for row in rows)
    assert len(rows) == 19
    assert ratio_histogram == {(1, 2): 1, (1, 3): 17, (4, 5): 1}
    assert maximizer_histogram == {
        ("U",): 8,
        ("2U",): 10,
        ("0", "UI"): 1,
    }
    assert all(row["maximizer_set_proper"] for row in rows)
    assert min(row["maximum_phi"] for row in rows) >= 0
    assert min(row["primitive_interruption_gap"] for row in rows) >= 1
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert row_hash == EXPECTED_ROWS_SHA256
    payload = {
        "claim_scope": "support premises only; no analytic or pair promotion",
        "exact_normalized_ratio_support_rows": len(rows),
        "ratio_histogram": {f"{p}:{q}": count for (p, q), count in sorted(ratio_histogram.items())},
        "maximizer_histogram": {"|".join(key): value for key, value in sorted(maximizer_histogram.items())},
        "every_maximizer_set_proper": True,
        "minimum_maximum_phi": min(row["maximum_phi"] for row in rows),
        "minimum_primitive_interruption_gap": min(
            row["primitive_interruption_gap"] for row in rows
        ),
        "rows_sha256": row_hash,
        "analytic_theorem_certified": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    payload_hash = _digest(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert payload_hash == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), sort_keys=True, indent=2))
