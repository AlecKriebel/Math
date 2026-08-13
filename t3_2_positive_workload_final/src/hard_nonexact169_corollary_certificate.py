"""Finite scope premises for the nonexact-169 proof corollary."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import two_active_dormant_407_certificate as hard


BASE_DEGREE = {"0": 0, "U": 1, "2U": 2}
BASE_COMPLEX = {degree: name for name, degree in BASE_DEGREE.items()}
COFACTOR = {"I", "2I", "UI"}
EXPECTED_ROWS_SHA256 = "2834f714f8ae4c2d8216cc391546d633bc553e32fbdc565ab9e3bddab2ed20f3"
EXPECTED_PAYLOAD_SHA256 = "2784c8e65edbe7675cc9c45eda61dfbbfbb8657b286b013c6326c9cea8736417"


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
        proper_set, lower_set = set(proper), set(lower)
        assert "VI" in proper_set
        assert proper_set | lower_set <= set(BASE_DEGREE) | COFACTOR | {"VI"}
        exact = (
            len(proper) == 2
            and len((proper_set - {"VI"}) & set(BASE_DEGREE)) == 1
        )
        if exact:
            continue
        proper_without_vi = proper_set - {"VI"}
        no_history = proper_without_vi <= COFACTOR and lower_set <= set(BASE_DEGREE)
        separated = proper_without_vi <= set(BASE_DEGREE) and lower_set <= COFACTOR
        category = "no_history" if no_history else "separated" if separated else "mixed"
        degree = max(
            BASE_DEGREE[name]
            for name in proper_set | lower_set
            if name in BASE_DEGREE
        )
        linkage_with_maximum = (
            proper_set
            if BASE_COMPLEX[degree] in proper_set
            else lower_set
        )
        assert BASE_COMPLEX[degree] in linkage_with_maximum
        assert len(linkage_with_maximum) >= 2
        if "VI" in linkage_with_maximum:
            assert linkage_with_maximum != {"VI", BASE_COMPLEX[degree]}
        result.append(
            {
                "ratio": [p, q],
                "proper": list(proper),
                "lower": list(lower),
                "category": category,
                "maximum_base_degree": degree,
                "fast_gap": q - p * degree,
            }
        )
    result.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    return tuple(result)


def certificate() -> dict[str, object]:
    data = rows()
    row_hash = _digest(data)
    categories = Counter(row["category"] for row in data)
    ratios = Counter(tuple(row["ratio"]) for row in data)
    gaps = Counter(row["fast_gap"] for row in data)
    assert len(data) == 169
    assert categories == {"mixed": 145, "separated": 8, "no_history": 16}
    assert ratios == {(1, 2): 16, (1, 3): 137, (4, 5): 16}
    assert gaps == {1: 153, 2: 16}
    assert min(row["fast_gap"] for row in data) >= 1
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert row_hash == EXPECTED_ROWS_SHA256
    payload = {
        "claim_scope": "finite premises for analytic 145-to-169 corollary",
        "nonexact_rows": len(data),
        "category_histogram": dict(sorted(categories.items())),
        "ratio_histogram": {
            f"{p}:{q}": count for (p, q), count in sorted(ratios.items())
        },
        "fast_gap_histogram": dict(sorted(gaps.items())),
        "minimum_fast_gap": min(row["fast_gap"] for row in data),
        "rows_sha256": row_hash,
        "corollary_independently_audited": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    payload_hash = _digest(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert payload_hash == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), sort_keys=True, indent=2))
