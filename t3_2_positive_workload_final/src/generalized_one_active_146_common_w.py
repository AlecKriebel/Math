"""Finite partition and frozen inputs for the generalized 146 theorem.

The support table proves only exhaustion.  Analytic truth is represented by
byte-pinned proof inputs and remains false until independent composition
audit.  Pair and global claims remain false.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import two_active_dormant_407_certificate as hard


BASE = {"0", "U", "2U"}
COFACTOR = {"I", "2I", "UI"}
EXPECTED_ROWS_SHA256 = "5ba76aaff2f7ca70dbd61bfd5325ce47c407d36e5e33c3042962e47bfef69eed"
EXPECTED_PAYLOAD_SHA256 = "b368a60cb699e06909b03ed368df85b59a422437454abb030b1814356892db06"

EXACT_COMPLETION_SHA256 = (
    "33dab04fba9d8f70b30f0ac43dffe7e432124867c51f5c647300f9e0bf80e6e4"
)
ORDERED_GREEN_SHA256 = (
    "ea92e6c7a249f75a33d841682be2df620c4d0cab638f982ff40c7e4ca6bf50c2"
)
MIXED_111_SHA256 = (
    "50696e88cc6c195f106331f27cab4af8566a693f983947d486ad1cf9c903692e"
)
SEPARATED_6_SHA256 = (
    "6f63ac4272841d5901e35456ac38ac89c38665e05a2a99f8c4f649fa9bd9ecac"
)


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def rows() -> tuple[dict[str, object], ...]:
    result = []
    for row in hard.generalized_support_templates():
        proper = tuple(row["proper"])
        lower = tuple(row["lower"])
        proper_without_vi = set(proper) - {"VI"}
        exact = (
            len(proper) == 2
            and "VI" in proper
            and len(proper_without_vi & BASE) == 1
        )
        no_history = proper_without_vi <= COFACTOR and set(lower) <= BASE
        separated = proper_without_vi <= BASE and set(lower) <= COFACTOR
        if exact:
            category = "exact_cloud"
        elif no_history:
            category = "no_history"
        elif separated:
            category = "separated"
        else:
            category = "mixed_nonexact"
        result.append(
            {"proper": list(proper), "lower": list(lower), "category": category}
        )
    result.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    return tuple(result)


def certificate() -> dict[str, object]:
    data = rows()
    row_hash = _digest(data)
    categories = Counter(row["category"] for row in data)
    assert len(data) == 146
    assert categories == {
        "exact_cloud": 17,
        "mixed_nonexact": 111,
        "separated": 6,
        "no_history": 12,
    }
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert row_hash == EXPECTED_ROWS_SHA256
    payload = {
        "claim_scope": "146-template partition and frozen local proof inputs",
        "support_templates": len(data),
        "category_histogram": dict(sorted(categories.items())),
        "rows_sha256": row_hash,
        "exact_completion_sha256": EXACT_COMPLETION_SHA256,
        "ordered_green_sha256": ORDERED_GREEN_SHA256,
        "mixed_111_sha256": MIXED_111_SHA256,
        "separated_6_sha256": SEPARATED_6_SHA256,
        "local_input_theorems_independently_audited": True,
        "composition_theorem_independently_audited": False,
        "generalized_146_common_w_certified": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    payload_hash = _digest(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert payload_hash == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), sort_keys=True, indent=2))
