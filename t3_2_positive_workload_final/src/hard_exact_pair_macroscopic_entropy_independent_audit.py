"""Independent audit certificate for the hard exact-carrier theorem.

This module pins the repaired local theorem and replays only its finite
support premises.  The analytic verdict comes from the accompanying proof
audit, not from enumeration.  No orientation is enumerated, and neither
pair recurrence nor the global T3-2 claim is certified here.
"""

from __future__ import annotations

from hashlib import sha256
import json
from math import ceil, e, log
from pathlib import Path

import hard_exact_pair_macroscopic_entropy_certificate as candidate
import two_active_dormant_407_certificate as hard


EXPECTED_THEOREM_SHA256 = (
    "3c18d0ee481e5c351663e4923b97473e871030c86ff37ca674f00688d66a047f"
)
EXPECTED_CERTIFICATE_SOURCE_SHA256 = (
    "43788cb4a458f6950d9316959393efc7270fbb2ef52bbb2f82bca0b6da848e66"
)
EXPECTED_CERTIFICATE_TEST_SHA256 = (
    "aa963d45f67388902ba2f8ebe40a95288b8deab4b32e3505243a168a24eab1dc"
)
EXPECTED_PRIOR_HOSTILE_AUDIT_SHA256 = (
    "3254ab07684637a98353f19fe20d15cb196c8dd9492930090a5b18136de7a42f"
)
EXPECTED_ROWS_SHA256 = (
    "e931d5277596c5084d89bf63b3963a6fe0ecb202be6549075b47f89c30b0a33b"
)
EXPECTED_UPSTREAM_PAYLOAD_SHA256 = (
    "2a6599b66e6b7db1c7c1701ad65d23410cb33694b75cfc9819ec955267debaf6"
)
EXPECTED_AUDIT_PAYLOAD_SHA256 = (
    "3f7a353473cceeec378bceb7136319e0d2dfca7174e864229aa9c05262565ad7"
)


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _project_file_sha256(relative: str) -> str:
    path = Path(__file__).resolve().parents[1] / relative
    return sha256(path.read_bytes()).hexdigest()


def old_pathwise_counterexample(s: int = 10_000) -> dict[str, object]:
    """Replay a positive clean path that refuted the old pathwise sign.

    On the exceptional shell take u=s, v=floor(s^3/e), ell=0, and make the
    equality birth 0->U+I have limiting selection probability 9/10 before
    the strict U+I->I exit.  The returned entropy increment is exact for
    ``m`` equality births followed by that strict exit.  Its positive value
    proves only that a pathwise sign is false; its probability is positive
    and exponentially small in ``m``.
    """

    if s < 100:
        raise ValueError("s must be at least 100")
    u = s
    v = int(s**3 / e)
    m = ceil(2 * log(s))
    equality_increment = sum(
        log((u + 3 * k + 1) * (u + 3 * k + 2) * (u + 3 * k + 3))
        - log(v - k)
        for k in range(m)
    )
    strict_exit_increment = -log(u + 3 * m)
    total_increment = equality_increment + strict_exit_increment
    assert total_increment > 0
    return {
        "orientation": ["0->UI", "UI->I", "I->2I", "2I->0"],
        "s": s,
        "u": u,
        "v": v,
        "equality_births": m,
        "equality_birth_selection_probability": "9/10 asymptotically",
        "strict_exit_selection_probability": "1/10 asymptotically",
        "exact_total_entropy_increment": total_increment,
        "total_increment_positive": True,
        "lesson": (
            "the clean shell has no pathwise negative sign; control its "
            "positive overshoot in expectation with a killed exponential "
            "Green estimate"
        ),
    }


def _exact_selector_count() -> int:
    count = 0
    for row in hard.normalized_templates():
        proper = set(row["proper_support"])
        if (
            len(proper) == 2
            and "VI" in proper
            and len(proper & {"0", "U", "2U"}) == 1
        ):
            count += 1
    return count


def certificate() -> dict[str, object]:
    frozen_files = {
        "theorem_sha256": _project_file_sha256(
            "research_notes/proof_first_hard_exact_pair_macroscopic_entropy.md"
        ),
        "certificate_source_sha256": _project_file_sha256(
            "src/hard_exact_pair_macroscopic_entropy_certificate.py"
        ),
        "certificate_test_sha256": _project_file_sha256(
            "tests/test_hard_exact_pair_macroscopic_entropy_certificate.py"
        ),
        "prior_hostile_audit_sha256": _project_file_sha256(
            "research_notes/hard_exact_pair_macroscopic_entropy_hostile_audit.md"
        ),
    }
    assert frozen_files == {
        "theorem_sha256": EXPECTED_THEOREM_SHA256,
        "certificate_source_sha256": EXPECTED_CERTIFICATE_SOURCE_SHA256,
        "certificate_test_sha256": EXPECTED_CERTIFICATE_TEST_SHA256,
        "prior_hostile_audit_sha256": EXPECTED_PRIOR_HOSTILE_AUDIT_SHA256,
    }

    upstream = candidate.certificate()
    assert upstream["rows_sha256"] == EXPECTED_ROWS_SHA256
    assert upstream["payload_sha256"] == EXPECTED_UPSTREAM_PAYLOAD_SHA256
    upstream_flags = {
        key: value for key, value in upstream.items() if key.endswith("_certified")
    }
    assert upstream_flags and not any(upstream_flags.values())

    rows = candidate.exact_rows()
    assert len(hard.normalized_templates()) == 188
    assert _exact_selector_count() == 19
    assert len(rows) == 19
    assert all(
        set(row["lower"]) <= {"0", "U", "2U", "I", "2I", "UI"}
        for row in rows
    )
    assert min(
        row["ratio"][1] - row["ratio"][0] * row["a"] for row in rows
    ) >= 1
    assert min(row["primitive_interruption_gap"] for row in rows) >= 1
    assert all(row["maximizer_set_proper"] for row in rows)
    assert min(row["maximum_phi"] for row in rows) >= 0
    nonsingleton = [row for row in rows if len(row["maximizers"]) > 1]
    assert len(nonsingleton) == 1
    exceptional = nonsingleton[0]
    assert exceptional == {
        "ratio": [1, 3],
        "a": 2,
        "proper": ["2U", "VI"],
        "lower": ["0", "I", "2I", "UI"],
        "phi": {"0": 0, "2I": -2, "I": -1, "UI": 0},
        "maximizers": ["0", "UI"],
        "maximizer_set_proper": True,
        "maximum_phi": 0,
        "primitive_interruption_gap": 2,
    }

    obligations = [
        {
            "id": 1,
            "name": "exact carrier averaging and source exponent",
            "status": "PASS",
            "evidence": (
                "falling-factorial cancellation gives (2.2), and the "
                "successive carrier ratio is O(s^(pa-q)/(j+1))"
            ),
        },
        {
            "id": 2,
            "name": "sourcewise dirty estimate and shifted cleanup",
            "status": "PASS",
            "evidence": (
                "ordered reversibility gives relative error "
                "s^(-min(q-pa,q-pc*)+o(1)); the (4,5) row uses c*=1"
            ),
        },
        {
            "id": 3,
            "name": "hazard exponent equals entropy gradient",
            "status": "PASS",
            "evidence": (
                "the clean endpoint identity gives Delta G="
                "(phi(target)-phi(source))*log(s)+o(log(s))"
            ),
        },
        {
            "id": 4,
            "name": "exceptional killed equality shell",
            "status": "PASS",
            "evidence": (
                "B+R0>0, D+R1>0, and R0+R1>0 follow from strong "
                "connectivity; uphill moves have exponential rate penalty"
            ),
        },
        {
            "id": 5,
            "name": "positive overshoot and logarithmic cap",
            "status": "PASS",
            "evidence": (
                "the killed exponential Foster bound gives integrable "
                "positive overshoot and cap probability s^(-M), while a "
                "strict exit loses at least log(s)+o(log(s))"
            ),
        },
        {
            "id": 6,
            "name": "carrier boundary, endpoints, and physical duration",
            "status": "PASS",
            "evidence": (
                "carrier ratios pay the logarithmic boundary "
                "superpolynomially; compound proper excursions and the "
                "time-marked shell Green recursion have fixed s^o(1) moments"
            ),
        },
        {
            "id": 7,
            "name": "common fourth-power lift and claim boundary",
            "status": "PASS",
            "evidence": (
                "E Delta G<=-c log(s) and fixed Delta G moments make the "
                "linear term in the exact fourth-power expansion dominant"
            ),
        },
    ]
    assert [row["id"] for row in obligations] == list(range(1, 8))
    assert {row["status"] for row in obligations} == {"PASS"}

    payload: dict[str, object] = {
        "audit_scope": "local macroscopic hard exact-carrier stopped theorem",
        "strict_verdict": "PASS_LOCAL_ANALYTIC_THEOREM",
        "frozen_files": frozen_files,
        "finite_replay": {
            "physical_normalized_templates": 188,
            "exact_templates": 19,
            "rows_sha256": upstream["rows_sha256"],
            "minimum_carrier_gap_q_minus_pa": min(
                row["ratio"][1] - row["ratio"][0] * row["a"] for row in rows
            ),
            "minimum_interruption_gap_q_minus_pcmax": min(
                row["primitive_interruption_gap"] for row in rows
            ),
            "unique_nonsingleton_maximizer": exceptional,
        },
        "prior_pathwise_counterexample": old_pathwise_counterexample(),
        "repair": {
            "pathwise_shell_sign_used": False,
            "killed_positive_overshoot_used": True,
            "strong_connectivity_rate_conditions": [
                "B+R0>0",
                "D+R1>0",
                "R0+R1>0",
            ],
        },
        "obligations": obligations,
        "upstream_claim_flags": upstream_flags,
        "dependency": {
            "pair_recurrence_certified": False,
            "global_t3_2_certified": False,
        },
        "certification_edits_made": False,
    }
    digest = _digest(payload)
    if EXPECTED_AUDIT_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_AUDIT_PAYLOAD_SHA256
    return {**payload, "audit_payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
