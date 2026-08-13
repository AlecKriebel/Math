"""Independent, claim-neutral audit of the guard-free H_b12 resolvent.

The audited theorem is only the descriptor-local stopped common-W block.
It does not certify recurrence for the twelve pairs or the global T3-2
claim.  In particular, composition still depends on the common-W 317
theorem.  Every certification flag remains false.
"""

from __future__ import annotations

from hashlib import sha256
import json
from math import ceil, log
from pathlib import Path

import hard333_hb12_global_shell_resolvent as candidate
import hard333_pair_composition as composition


EXPECTED_UPSTREAM_ROWS_SHA256 = (
    "3999b185f5626b0999d72e9c10d3cdf082054f70cd84af8cd43a52aa6f286c7a"
)
EXPECTED_UPSTREAM_PAYLOAD_SHA256 = (
    "f750d01ff8c0ea884df27cf8e4625f6d6ef020f8d335c6086f6c1147c0934417"
)
EXPECTED_AUDIT_PAYLOAD_SHA256 = (
    "4dfbfe2aacf6dfaaf4d3c53c9c30be3b65b0d8e2f62cd31495f3e53ec8d84ed3"
)
EXPECTED_UPSTREAM_NOTE_SHA256 = (
    "8e6988149d6a889582ead592e47c05c3ca9a02f27da6e68182eea9959d55c513"
)
EXPECTED_UPSTREAM_SOURCE_SHA256 = (
    "01c99b0a5cb872be68d0adce6b7ffabd5cd499ded63b5c8d3b2b9df0801ddeaa"
)
EXPECTED_UPSTREAM_TEST_SHA256 = (
    "b6634246517734714cd990bb68a95e036a1a254a425cb383b8467b57217f1f6e"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _project_file_sha256(relative: str) -> str:
    path = Path(__file__).resolve().parents[1] / relative
    return sha256(path.read_bytes()).hexdigest()


def old_guard_counterexample() -> dict[str, object]:
    """Freeze an exact integer sequence defeating a log-largest guard."""

    return {
        "parameter": "integer m tending to infinity",
        "center": {
            "B": "m^2",
            "C": "2^(2*m^3)",
            "A": "m*2^(m^3)",
        },
        "exact_top_balance": "A^2=B*C",
        "exact_tier_order": "2C>AC>{2A,BC}>C>AB>A>2B>B>0",
        "boundary_energy_scale": "Theta(m^2)",
        "log_largest_scale": "Theta(m^3)",
        "conclusion": (
            "a fixed log-largest entropy guard contains B=0 and cannot "
            "support uniform q/q_mode or pathwise boundary avoidance"
        ),
    }


def slow_margin_witness(n: int) -> dict[str, object]:
    """An exact (3,1,5) sequence separating gap and reward scales.

    Put r=ceil(log log n), B=n, A=n^2 r, and C=n^3 r^2.  Then A^2=BC,
    the exact H_b monomial order holds, gap/q is r, but the fixed strong
    cycle AB->A->0->2B->AB has reward and b-L2 scale of order log n.
    Thus gap/(q*g) need not diverge for the same g used in the L2 bound.
    """

    if n < 16:
        raise ValueError("n must be at least 16")
    r = max(2, ceil(log(log(n))))
    a = n * n * r
    b = n
    c = n * n * n * r * r
    monomials = {
        "0": 1,
        "B": b,
        "2B": b * b,
        "A": a,
        "AB": a * b,
        "C": c,
        "2A": a * a,
        "BC": b * c,
        "AC": a * c,
        "2C": c * c,
    }
    assert monomials["2A"] == monomials["BC"]
    blocks = (
        ("2C",),
        ("AC",),
        ("2A", "BC"),
        ("C",),
        ("AB",),
        ("A",),
        ("2B",),
        ("B",),
        ("0",),
    )
    levels = [monomials[block[0]] for block in blocks]
    assert all(left > right for left, right in zip(levels, levels[1:]))
    return {
        "n": n,
        "r": r,
        "A": a,
        "B": b,
        "C": c,
        "A_squared_equals_BC": a * a == b * c,
        "tier_blocks": [list(block) for block in blocks],
        "lower_support": ["0", "A", "2B", "AB"],
        "strong_cycle": ["AB->A", "A->0", "0->2B", "2B->AB"],
        "gap_over_mean_kill_exact_scale": "r",
        "stationary_reward_and_b_L2_scale": "log(n)",
        "same_g_stronger_margin": "r/log(n), which tends to zero",
        "proof_consequence": (
            "do not require gap/(mean_kill*g)->infinity; outside the core "
            "use separate pointwise negativity of the top flux branch and "
            "the lower high-cut branch"
        ),
    }


def certificate() -> dict[str, object]:
    upstream = candidate.certificate()
    assert upstream["hashes"]["rows_sha256"] == EXPECTED_UPSTREAM_ROWS_SHA256
    assert upstream["payload_sha256"] == EXPECTED_UPSTREAM_PAYLOAD_SHA256
    assert composition.EXPECTED_HB_12_SHA256 == upstream["selector"]["pair_sha256"]

    frozen_files = {
        "note_sha256": _project_file_sha256(
            "research_notes/hard333_hb12_global_shell_resolvent.md"
        ),
        "source_sha256": _project_file_sha256(
            "src/hard333_hb12_global_shell_resolvent.py"
        ),
        "test_sha256": _project_file_sha256(
            "tests/test_hard333_hb12_global_shell_resolvent.py"
        ),
    }
    assert frozen_files == {
        "note_sha256": EXPECTED_UPSTREAM_NOTE_SHA256,
        "source_sha256": EXPECTED_UPSTREAM_SOURCE_SHA256,
        "test_sha256": EXPECTED_UPSTREAM_TEST_SHA256,
    }

    upstream_flags = {
        key: value
        for key, value in upstream.items()
        if key.endswith("_certified")
    }
    assert upstream_flags and not any(upstream_flags.values())

    obligations = [
        {
            "id": 1,
            "name": "exact selector and relaxation rows",
            "status": "PASS",
            "evidence": (
                "12 pairs, 16 incidences, gap-minus-kill histogram 12 of 1 "
                "and 4 of 2; rows hash replayed"
            ),
        },
        {
            "id": 2,
            "name": "shifted factorial laws and shell moments",
            "status": "PASS",
            "evidence": (
                "single-source tilts and finite product tilts give fixed "
                "q moments and q-size-biased shell-energy moments"
            ),
        },
        {
            "id": 3,
            "name": "same-state Kac and Dirichlet Green bounds",
            "status": "PASS",
            "evidence": (
                "one-dimensional log-concavity gives a core-point "
                "Dirichlet gap comparable with the shell gap and the "
                "required cycle second/cross moments"
            ),
        },
        {
            "id": 4,
            "name": "exact killed renewal quotient",
            "status": "PASS",
            "evidence": (
                "d=E(1-exp(-H)) and the N/d quotient include a kill in "
                "the initial holding interval; the error is relative "
                "O(mean_kill/gap)=o(1)"
            ),
        },
        {
            "id": 5,
            "name": "full endpoint and duration moments",
            "status": "PASS",
            "evidence": (
                "h_j=sum q_e|Delta_e G|^j controls the actual lower jump "
                "through one p>8; fixed-class cycle constants give "
                "E exp(c*mean_kill*tau)<=C even for arbitrarily slow "
                "subpower refinements"
            ),
        },
        {
            "id": 6,
            "name": "stationary high cut for all orientations",
            "status": "PASS",
            "evidence": (
                "14 unique-high rows and the two tied A/2B and A/2C rows "
                "have a negative first edge out of the actual refined high "
                "set; positive reverse terms are controlled by h*exp(-h)"
            ),
        },
        {
            "id": 7,
            "name": "common fourth power and outside-core split",
            "status": "PASS",
            "evidence": (
                "G=K+sum log(x!)+ell dot x has one shell-independent K, "
                "while c_Q=K-log Z_Q only rewrites -log pi_Q; the common "
                "positive G gives L_Q^2/(G*g)->0.  Inside the "
                "core use the Kac block, while outside it the reversible "
                "top flux and lower high-cut fourth-power drifts are "
                "separately negative.  No false gap/(kill*g) margin is used"
            ),
        },
        {
            "id": 8,
            "name": "lower-dimensional endpoint routing and scope",
            "status": "PASS",
            "evidence": (
                "boundary endpoints use the exact 36+12 two-active and "
                "36+2 one-active common-W menus; recurrence remains "
                "conditional on the common-W 317 composition theorem"
            ),
        },
    ]
    assert [row["id"] for row in obligations] == list(range(1, 9))
    assert {row["status"] for row in obligations} == {"PASS"}

    payload: dict[str, object] = {
        "audit_scope": "descriptor-local guard-free H_b12 common-W stopped block",
        "strict_verdict": "PASS_LOCAL_COMMON_W_STOPPED_BLOCK",
        "upstream": {
            "rows_sha256": EXPECTED_UPSTREAM_ROWS_SHA256,
            "payload_sha256": EXPECTED_UPSTREAM_PAYLOAD_SHA256,
            "frozen_files": frozen_files,
            "focused_tests": "6/6",
            "all_claim_flags_false": True,
        },
        "post_audit_edits": {
            "common_G_grammar": (
                "G_ell=K_ell+sum log(x_i!)+ell dot x is shell-independent; "
                "G_ell=-log pi_Q+c_Q with c_Q=K_ell-log Z_Q"
            ),
            "outside_core_split": (
                "top flux and lower high-cut branches are separately "
                "pointwise negative and absorb only their own remainders"
            ),
            "false_margin_explicitly_withdrawn": (
                "gamma_Q/(mean_kill*g_Q)->infinity is not assumed"
            ),
            "status": "PASS",
        },
        "old_guard_counterexample": old_guard_counterexample(),
        "false_stronger_margin_withdrawn": slow_margin_witness(10**100),
        "obligations": obligations,
        "high_cut_counts": {
            "unique_high_rows": 14,
            "tied_high_rows": 2,
            "total": 16,
        },
        "lower_dimensional_menu": upstream["lower_dimensional_routing"],
        "dependency": {
            "common_W_317_pair_recurrence_certified": False,
            "H_b_12_pair_recurrence_certified": False,
            "global_t3_2_certified": False,
        },
        "certification_edits_made": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_AUDIT_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_AUDIT_PAYLOAD_SHA256
    return {**payload, "audit_payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
