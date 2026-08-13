"""Finite premises for the proof-first macroscopic mixed-145 theorem.

This module checks support identities only.  It does not infer a stochastic
theorem and deliberately leaves every analytic, pair, and global flag false.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import two_active_dormant_407_certificate as hard


BASE_DEGREE = {"0": 0, "U": 1, "2U": 2}
COFACTOR = {"I", "2I", "UI"}
EXPECTED_ROWS_SHA256 = "03cca5fd5e16beb42c6c21f4b4e12fb4f2f1b214bc152a63ddd89f8b2386de7e"
EXPECTED_PAYLOAD_SHA256 = "cd7c70f4fab34bbc1664e9cc54fa711bb5387c042f2a76465c854a947e73c52b"


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def rows() -> tuple[dict[str, object], ...]:
    result = []
    for row in hard.normalized_templates():
        p, q = map(int, row["normalized_ratio"])
        proper = tuple(row["proper_support"])
        lower = tuple(row["other_support"])
        proper_without_vi = set(proper) - {"VI"}
        all_complexes = set(proper) | set(lower)
        assert "VI" in set(proper)
        assert all_complexes <= set(BASE_DEGREE) | COFACTOR | {"VI"}
        exact = (
            len(proper) == 2
            and "VI" in proper
            and len(set(proper) & set(BASE_DEGREE)) == 1
        )
        no_history = (
            proper_without_vi <= COFACTOR
            and set(lower) <= set(BASE_DEGREE)
        )
        separated = (
            proper_without_vi <= set(BASE_DEGREE)
            and set(lower) <= COFACTOR
        )
        mixed = not no_history and not separated
        if exact or not mixed:
            continue
        actual_mixed = any(
            (support & set(BASE_DEGREE)) and (support & COFACTOR)
            for support in (set(proper) - {"VI"}, set(lower))
        )
        assert actual_mixed
        degree = max(
            BASE_DEGREE[name]
            for name in set(proper) | set(lower)
            if name in BASE_DEGREE
        )
        result.append(
            {
                "ratio": [p, q],
                "proper": list(proper),
                "lower": list(lower),
                "maximum_base_degree": degree,
                "fast_gap": q - p * degree,
                "proper_not_exact_base_vi_pair": True,
                "mixed_after_deleting_vi": actual_mixed,
            }
        )
    result.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    return tuple(result)


def certificate() -> dict[str, object]:
    data = rows()
    row_hash = _digest(data)
    ratios = Counter(tuple(row["ratio"]) for row in data)
    degrees = Counter(row["maximum_base_degree"] for row in data)
    gaps = Counter(row["fast_gap"] for row in data)
    assert len(data) == 145
    assert ratios == {(1, 2): 13, (1, 3): 119, (4, 5): 13}
    assert degrees == {1: 39, 2: 106}
    assert gaps == {1: 132, 2: 13}
    assert min(row["fast_gap"] for row in data) >= 1
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert row_hash == EXPECTED_ROWS_SHA256
    payload = {
        "claim_scope": "support premises only; no stochastic inference",
        "normalized_ratio_support_rows": len(data),
        "ratio_histogram": {
            f"{p}:{q}": count for (p, q), count in sorted(ratios.items())
        },
        "maximum_base_degree_histogram": dict(sorted(degrees.items())),
        "fast_gap_histogram": dict(sorted(gaps.items())),
        "minimum_fast_gap": min(row["fast_gap"] for row in data),
        "every_proper_support_is_nonexact": True,
        "every_row_is_mixed": True,
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
