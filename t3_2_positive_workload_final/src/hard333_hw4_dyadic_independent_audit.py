"""Scoped executable replay for the hard-H_w dyadic independent audit.

This module freezes the exact four-node orientation obligations and strict
local-PASS/global-false verdict for patched candidate payload 57608....
Pair-recurrence and global flags remain false pending their separate gates.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import hard333_hw4_dyadic_compound_activation as candidate


AUDITED_CANDIDATE_PAYLOAD_SHA256 = (
    "57608cbc0912802e526b5555631ffcfcaacd8eba2c26852439971babf5ea4aa7"
)
EXPECTED_NOTE_SHA256 = (
    "f47d64f754abf0cc26456483207e97eeefe131e5dea0ca8840d6910d650ccdc0"
)
EXPECTED_ORIENTATION_SHA256 = (
    "3a0309d65c77d14f0227dee231c21d44cf7412f341dca3cef02e9f1949ac44b4"
)
EXPECTED_PAYLOAD_SHA256 = (
    "3526e78c9b5f99f21cab819468df6753694f161f34d089e0dd5bde2a29e8a3ef"
)
EXPECTED_CANONICAL_NOTE_SHA256 = (
    "df392304c5c0b5476584175c4601fd2e3d7f80e41154ae03c7ab1bd9de54b518"
)
EXPECTED_CANONICAL_SOURCE_SHA256 = (
    "bbe1bd66769c14c88930bb28a3402abba980b6d0422ce2201c83c1ea28be6a8f"
)
EXPECTED_CANONICAL_TEST_SHA256 = (
    "cf273a011d38b26f455b6490ba52d43dfde2962e34a749094f2cea0ba59ebb54"
)

PURE = 1       # 2C in the canonical resistance-two relabeling: abstract 2P
CARRIER = 3    # XY in the canonical resistance-two relabeling: abstract XU
HIGH = frozenset((0, 2))


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def note_sha256() -> str:
    path = (
        Path(__file__).resolve().parents[1]
        / "research_notes"
        / "hard333_hw4_dyadic_compound_activation_independent_audit.md"
    )
    return sha256(path.read_bytes()).hexdigest()


def _project_sha256(relative: str) -> str:
    path = Path(__file__).resolve().parents[1] / relative
    return sha256(path.read_bytes()).hexdigest()


def orientation_rows() -> tuple[dict[str, object], ...]:
    arc_bit = {arc: bit for bit, arc in enumerate(candidate.ARCS)}

    def has(mask: int, source: int, target: int) -> bool:
        return bool(mask & (1 << arc_bit[(source, target)]))

    rows: list[dict[str, object]] = []
    for mask, left_distance, right_distance in candidate.strong_cut_profile():
        direct_pure = any(has(mask, PURE, target) for target in HIGH)
        direct_carrier = any(has(mask, CARRIER, target) for target in HIGH)
        pure_to_carrier = has(mask, PURE, CARRIER)
        carrier_to_pure = has(mask, CARRIER, PURE)

        # These are the exact graph-theoretic premises of the two pathwise
        # source-balance inequalities.  Strong connectivity excludes two
        # nondirect minimum nodes and forces the zero escape from either
        # individual nondirect node.
        assert direct_pure or direct_carrier
        assert direct_pure or pure_to_carrier
        assert direct_carrier or carrier_to_pure

        rows.append(
            {
                "mask": mask,
                "minimum_cut_distances": [left_distance, right_distance],
                "direct_pure": direct_pure,
                "direct_carrier": direct_carrier,
                "pure_to_carrier_zero": pure_to_carrier,
                "carrier_to_pure_zero": carrier_to_pure,
            }
        )

    result = tuple(rows)
    assert len(result) == 1606
    return result


def orientation_histogram() -> dict[str, int]:
    counts = Counter(
        (
            row["direct_pure"],
            row["direct_carrier"],
            row["pure_to_carrier_zero"],
            row["carrier_to_pure_zero"],
        )
        for row in orientation_rows()
    )
    return {
        f"dP={int(d_pure)},dB={int(d_carrier)},"
        f"PtoB={int(pure_to_carrier)},BtoP={int(carrier_to_pure)}": count
        for (
            d_pure,
            d_carrier,
            pure_to_carrier,
            carrier_to_pure,
        ), count in sorted(counts.items())
    }


def certificate() -> dict[str, object]:
    # Do not call ``candidate.certificate()`` here: the canonical author may
    # be applying the replacement while this frozen audit remains runnable.
    # The audited byte target is recorded above, while the immutable finite
    # orientation enumerator is replayed directly below.
    rows = orientation_rows()
    rows_hash = _encoded_sha256(rows)
    note_hash = note_sha256()
    if EXPECTED_ORIENTATION_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ORIENTATION_SHA256
    if EXPECTED_NOTE_SHA256 != "TO_BE_FILLED":
        assert note_hash == EXPECTED_NOTE_SHA256

    canonical_files = {
        "note_sha256": _project_sha256(
            "research_notes/hard333_hw4_dyadic_compound_activation.md"
        ),
        "source_sha256": _project_sha256(
            "src/hard333_hw4_dyadic_compound_activation.py"
        ),
        "test_sha256": _project_sha256(
            "tests/test_hard333_hw4_dyadic_compound_activation.py"
        ),
    }
    assert canonical_files == {
        "note_sha256": EXPECTED_CANONICAL_NOTE_SHA256,
        "source_sha256": EXPECTED_CANONICAL_SOURCE_SHA256,
        "test_sha256": EXPECTED_CANONICAL_TEST_SHA256,
    }

    payload: dict[str, object] = {
        "scope": "independent event-skeleton audit of the exact hard H_w four",
        "audited_candidate_payload_sha256": AUDITED_CANDIDATE_PAYLOAD_SHA256,
        "audit_note_sha256": note_hash,
        "canonical_files": canonical_files,
        "strong_digraphs": len(rows),
        "orientation_rows_sha256": rows_hash,
        "orientation_histogram": orientation_histogram(),
        "abstract_support": ["2P", "XU", "PU", "2U"],
        "height_coordinate": "R=P+2U",
        "heights": {"2P": 2, "XU": 2, "PU": 3, "2U": 4},
        "source_balance_obligations": {
            "carrier_nondirect": (
                "m_B<=U_0+2*m_A+2*e; "
                "m_A>=(m_A+m_B-2*r-2*e)/3"
            ),
            "pure_nondirect": (
                "2*m_A<=P_0+2*m_B+2*e; "
                "m_B>=(m_A+m_B-r-e)/2"
            ),
            "direct_branching": (
                "conditional cut probability at a direct source is a fixed "
                "positive rate ratio"
            ),
        },
        "propensity_obligations": {
            "minimum": "P*(P-1)+X*U >= c*r^2",
            "high": "U*R",
            "exceptional_ratio": "C*(epsilon+1/r)",
            "jump_bound": "every bad R decrement is at most 2",
        },
        "strict_verdict": "PASS_LOCAL_COMMON_W_STOPPED_EPISODE",
        "reason": (
            "the patched candidate contains the independently replayed "
            "event-skeleton, service, and common-endpoint proof"
        ),
        "exact_counterexample_found": False,
        "event_skeleton_replacement_audited": True,
        "local_service_and_endpoint_audited": True,
        "canonical_replacement_present": True,
        "dyadic_activation_certified": False,
        "H_w_4_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
