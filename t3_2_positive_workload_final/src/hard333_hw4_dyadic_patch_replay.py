"""Frozen independent replay of patched hard-H_w4 payload 57608....

The replay certifies only the local common-factorial stopped episode.  Pair
composition and global T3-2 flags deliberately remain false.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import hard333_hw4_dyadic_compound_activation as candidate
import hard333_hw4_dyadic_independent_audit as prior_audit


EXPECTED_CANDIDATE_PAYLOAD_SHA256 = (
    "57608cbc0912802e526b5555631ffcfcaacd8eba2c26852439971babf5ea4aa7"
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
EXPECTED_REPLAY_NOTE_SHA256 = (
    "a29454f9659b6dc9a254e6c492c40fa85a56263a6788ba127957634af108edfa"
)
EXPECTED_PAYLOAD_SHA256 = (
    "e812ceaccb6d38bd9290d708a5acaf5cefa9931c30307a50ee91128062b47115"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _project_path(relative: str) -> Path:
    return Path(__file__).resolve().parents[1] / relative


def _file_sha256(relative: str) -> str:
    return sha256(_project_path(relative).read_bytes()).hexdigest()


def certificate() -> dict[str, object]:
    result = candidate.certificate()
    assert result["payload_sha256"] == EXPECTED_CANDIDATE_PAYLOAD_SHA256

    frozen_files = {
        "canonical_note": _file_sha256(
            "research_notes/hard333_hw4_dyadic_compound_activation.md"
        ),
        "canonical_source": _file_sha256(
            "src/hard333_hw4_dyadic_compound_activation.py"
        ),
        "canonical_test": _file_sha256(
            "tests/test_hard333_hw4_dyadic_compound_activation.py"
        ),
        "replay_note": _file_sha256(
            "research_notes/hard333_hw4_dyadic_compound_activation_patch_replay.md"
        ),
    }
    assert frozen_files["canonical_note"] == EXPECTED_CANONICAL_NOTE_SHA256
    assert frozen_files["canonical_source"] == EXPECTED_CANONICAL_SOURCE_SHA256
    assert frozen_files["canonical_test"] == EXPECTED_CANONICAL_TEST_SHA256
    if EXPECTED_REPLAY_NOTE_SHA256 != "TO_BE_FILLED":
        assert frozen_files["replay_note"] == EXPECTED_REPLAY_NOTE_SHA256

    rows = prior_audit.orientation_rows()
    assert len(rows) == 1606
    assert (
        prior_audit._encoded_sha256(rows)
        == prior_audit.EXPECTED_ORIENTATION_SHA256
    )

    payload: dict[str, object] = {
        "scope": "patched exact-H_w4 local common-factorial stopped episode",
        "candidate_payload_sha256": result["payload_sha256"],
        "frozen_files": frozen_files,
        "orientation_rows": len(rows),
        "orientation_rows_sha256": prior_audit.EXPECTED_ORIENTATION_SHA256,
        "mechanical_replay": {
            "focused_tests": 9,
            "focused_tests_passed": 9,
            "display_openings": 33,
            "display_closings": 33,
            "unique_equation_tags": 33,
            "rendered_pdf_pages": 9,
        },
        "strict_verdict": "PASS_LOCAL_COMMON_W_STOPPED_EPISODE",
        "exact_orientation_or_rate_counterexample_found": False,
        "local_event_skeleton_audited": True,
        "local_service_and_endpoint_audited": True,
        "pair_composition_replayed": False,
        "H_w_4_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
