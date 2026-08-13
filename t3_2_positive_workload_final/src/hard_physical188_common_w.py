"""Finite premise composition for the analytic physical hard-188 theorem.

The executable proves only the disjoint 19+169 scope partition and pins the
analytic inputs.  It does not infer a stochastic theorem from finite data.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import hard_exact_pair_macroscopic_entropy_certificate as exact
import hard_nonexact169_corollary_certificate as nonexact
import two_active_dormant_407_certificate as hard


EXPECTED_ROWS_SHA256 = "5295c9952f54069dc4337155aec8391fc09abc2b7e5aaf4b2650cf4036ae2ddc"
EXPECTED_PAYLOAD_SHA256 = "2152dcd4bbe64f08032ec576e126bc8213c3840b642fd15a2e7866a881e4ed0e"

FROZEN_PROOF_SHA256 = {
    "exact19_theorem": "3c18d0ee481e5c351663e4923b97473e871030c86ff37ca674f00688d66a047f",
    "exact19_certificate": "43788cb4a458f6950d9316959393efc7270fbb2ef52bbb2f82bca0b6da848e66",
    "exact19_audit": "754bd752d707348a4098fdd3658fc2449034dcf4e208f13f5853092533f3f6c2",
    "mixed145_theorem": "d53772170088cccbacc7a0911b6a71e05ad6cbe856fbaddf8858769d19805714",
    "mixed145_certificate": "ac9319af8d21f03a67e95458b90d26eb1d04a3274edbcd76b858650d25439e9f",
    "nonexact169_corollary": "734f4cc3b0732b97c361100f2375c5b36a757da8926446c738dfdeef66130645",
    "nonexact169_certificate": "e34038585e738a42fce5a6587e578f28fe8b570c18c376e1394bf8e5791554a4",
    "nonexact169_audit": "938fc5e653c7f19b575ee761b6e87dfc395d80498adf7cf5ee282657baf0be4f",
}


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def rows() -> tuple[dict[str, object], ...]:
    exact_rows = tuple(
        {
            "category": "exact_carrier",
            "ratio": row["ratio"],
            "proper": row["proper"],
            "lower": row["lower"],
        }
        for row in exact.exact_rows()
    )
    nonexact_rows = tuple(
        {
            "category": f"nonexact_{row['category']}",
            "ratio": row["ratio"],
            "proper": row["proper"],
            "lower": row["lower"],
        }
        for row in nonexact.rows()
    )
    result = exact_rows + nonexact_rows
    result = tuple(
        sorted(
            result,
            key=lambda row: json.dumps(
                row, sort_keys=True, separators=(",", ":")
            ),
        )
    )
    keys = {
        (tuple(row["ratio"]), tuple(row["proper"]), tuple(row["lower"]))
        for row in result
    }
    assert len(result) == len(keys) == 188
    canonical = {
        (
            tuple(map(int, row["normalized_ratio"])),
            tuple(row["proper_support"]),
            tuple(row["other_support"]),
        )
        for row in hard.normalized_templates()
    }
    assert keys == canonical
    return result


def certificate() -> dict[str, object]:
    data = rows()
    rows_hash = _digest(data)
    categories = Counter(row["category"] for row in data)
    ratios = Counter(tuple(row["ratio"]) for row in data)
    assert categories == {
        "exact_carrier": 19,
        "nonexact_mixed": 145,
        "nonexact_separated": 8,
        "nonexact_no_history": 16,
    }
    assert ratios == {(1, 2): 17, (1, 3): 154, (4, 5): 17}
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256
    payload = {
        "claim_scope": (
            "finite partition and frozen-input pins for the analytic "
            "physical hard-188 common-W theorem"
        ),
        "normalized_templates": len(data),
        "partition": dict(sorted(categories.items())),
        "ratio_histogram": {
            f"{p}:{q}": count for (p, q), count in sorted(ratios.items())
        },
        "rows_sha256": rows_hash,
        "frozen_proof_sha256": dict(sorted(FROZEN_PROOF_SHA256.items())),
        "physical188_composition_independently_audited": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    payload_hash = _digest(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert payload_hash == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), sort_keys=True, indent=2))
