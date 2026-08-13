"""Publication-safe finite certificate for the corrected two-linkage union.

This module performs finite support, tier, affine, and set identities only.
In particular, it does not enumerate reaction orientations, rate vectors,
reaction histories, stochastic trajectories, or population boxes.  Analytic
recurrence claims live in the separately audited theorem files pinned below.

The baseline is reconstructed from the corrected S-tier-superlevel cut, not
from the legacy global-top-D criterion.  The fourteen independently audited
analytic branch selectors must then form an exact disjoint union of that
2,511-pair baseline.
"""

from __future__ import annotations

from functools import cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import all_active_only_recurrence as all_active_only
import critical_one_active_q_trace_certificate as critical
import global_atlas_interface_closure as closure
import global_tier_interface as tier_geometry
import one_active_phase_shape as one_active
import prospective_no_promotion_26 as exact26
import rank_one_no_promotion_branch as rank_one
import rank_two_linear_switch_13 as linear13
import rank_two_mixed_profile_7_stopped_service as stopped7
import rank_two_return_certificate as rank_two
import s_tier_superlevel_interface as corrected_tier
import stoichiometric_gate_feasibility as affine_geometry
import suppressed_promotion_orbit_certificate as suppressed
import two_active_dormant_407_certificate as hard333
import two_active_easy_common_w as easy416
import two_active_promotion_obstruction as promotion


Pair = closure.Pair
PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_ROWS_SHA256 = (
    "9e9c6be443216f3a6d05795fcf0dcf25170ce020371c6bffde25eb316e52ad27"
)
EXPECTED_PAYLOAD_SHA256 = (
    "efd810c7a2ba9b71f9d70d0172d095a5a8ba13079dfbc85d1f6738d758389783"
)


ANALYTIC_DEPENDENCY_MANIFEST: dict[str, dict[str, str]] = {
    "affine_stoichiometric_151": {
        "theorem_path": "research_notes/s_tier_superlevel_cut_and_affine151_corrected.md",
        "theorem_sha256": "d91f369d34cadfb28ddb872df8fb9f6d17799ec207da29933037f55ae95f0407",
        "audit_path": "research_notes/proof_first_exact_byte_audit_affine151_and_two_linkage.md",
        "audit_sha256": "62378e56b43ce205b7d3f36fe6829dc361800c991a6f1a86d3b654292f7dd354",
        "status": "analytic dependencies independently audited",
    },
    "rank_two_14": {
        "theorem_path": "research_notes/rank_two_global_return_all14.md",
        "theorem_sha256": "821478a8c4410a371f99fa9df02e18ab5dbcc7c24aafa78f7d0db20cb6ab0bbe",
        "audit_path": "research_notes/proof_first_three_two_linkage_pair_theorems_consolidated_exact_byte_audit.md",
        "audit_sha256": "13f328883635ae832570620f3fabde0081af0358a0a5c69bcd316236f633df02",
        "status": "analytic dependencies independently audited",
    },
    "all_active_only_51": {
        "theorem_path": "research_notes/all_active_only_reversible_top.md",
        "theorem_sha256": "3f8c3662ed55d13133ef67f5e4e75e7ef9057075fa6e755faf33420e71ea0a26",
        "audit_path": "research_notes/proof_first_three_two_linkage_pair_theorems_consolidated_exact_byte_audit.md",
        "audit_sha256": "13f328883635ae832570620f3fabde0081af0358a0a5c69bcd316236f633df02",
        "status": "analytic dependencies independently audited",
    },
    "rank_one_no_promotion_141": {
        "theorem_path": "research_notes/rank_one_no_promotion_pair_branch.md",
        "theorem_sha256": "adc325b740dd18bfa4cc9ee53c2a3632f3660df589369a14cc4d9c3ce16992c1",
        "audit_path": "research_notes/proof_first_141_92_15_26_current_exact_byte_audit.md",
        "audit_sha256": "d68293a3d47f8f708b604467e90fdd1801f3b3ed583d07fb53e7b9e64b987239",
        "status": "analytic dependencies independently audited",
    },
    "post_rank_one_one_active_92": {
        "theorem_path": "research_notes/post_rank_one_one_active_repair.md",
        "theorem_sha256": "b4944d0bed95f92978a0eaf08336744813804ca7ddd6af0c4cd84005361c6113",
        "audit_path": "research_notes/proof_first_141_92_15_26_current_exact_byte_audit.md",
        "audit_sha256": "d68293a3d47f8f708b604467e90fdd1801f3b3ed583d07fb53e7b9e64b987239",
        "status": "analytic dependencies independently audited",
    },
    "two_active_promotion_36": {
        "theorem_path": "research_notes/two_active_promotion_36_pair_theorem.md",
        "theorem_sha256": "2f52d0ed580c70916fbe75f13e8ea09d77af53940bdf21048b43423830620f97",
        "audit_path": "research_notes/proof_first_three_two_linkage_pair_theorems_consolidated_exact_byte_audit.md",
        "audit_sha256": "13f328883635ae832570620f3fabde0081af0358a0a5c69bcd316236f633df02",
        "status": "analytic dependencies independently audited",
    },
    "suppressed_promotion_4": {
        "theorem_path": "research_notes/suppressed_promotion_orbit_full_proof.md",
        "theorem_sha256": "edbe0c4affe9735fb7cb650f9e0e3d653c75e7b37df5b5c8c8b838f43565a518",
        "audit_path": "research_notes/suppressed_promotion_orbit_independent_audit.md",
        "audit_sha256": "4ff20ae0ba6443d14a25f4bed3337e5cacc880b0e42044d717a5644ce2b7b509",
        "status": "analytic dependencies independently audited",
    },
    "critical_one_active_15": {
        "theorem_path": "research_notes/critical_one_active_q_trace.md",
        "theorem_sha256": "01a7827e96874171bc0f96be4fd05edb2a7ce607398be312b1378e762f62ea82",
        "audit_path": "research_notes/proof_first_141_92_15_26_current_exact_byte_audit.md",
        "audit_sha256": "d68293a3d47f8f708b604467e90fdd1801f3b3ed583d07fb53e7b9e64b987239",
        "status": "analytic dependencies independently audited",
    },
    "universal_one_active_net_1212": {
        "theorem_path": "research_notes/one_active_fourth_power_pair_composition.md",
        "theorem_sha256": "0ab1cff97dee0594db9981db451a9f26799a6f2cdd5cf5d00a19f03e12c6ea9c",
        "audit_path": "research_notes/one_active_fourth_power_pair_composition_current_independent_audit.md",
        "audit_sha256": "119918037899e9af543f321d3d019006abcbcf947b34c51b0af611c74b017db7",
        "status": "analytic dependencies independently audited",
    },
    "exact_common_w_26": {
        "theorem_path": "research_notes/prospective_26_candidate_pair_theorem.md",
        "theorem_sha256": "c78e53f11aeb981b415a90a486583b409608ef2256b73b9e063db48ac8d4fc88",
        "audit_path": "research_notes/proof_first_141_92_15_26_current_exact_byte_audit.md",
        "audit_sha256": "d68293a3d47f8f708b604467e90fdd1801f3b3ed583d07fb53e7b9e64b987239",
        "status": "analytic dependencies independently audited",
    },
    "easy_common_w_416": {
        "theorem_path": "research_notes/two_active_easy_943_common_w_theorem.md",
        "theorem_sha256": "4764849b05915b9005d68ac885c512a906af439430e8db8a7131f04645224e29",
        "audit_path": "research_notes/two_active_easy_416_independent_audit.md",
        "audit_sha256": "c07f9d9d79574d1c590b03d552de574882c141c84f35fdf452508689e46743f6",
        "status": "analytic dependencies independently audited",
    },
    "rank_two_scalar_13": {
        "theorem_path": "research_notes/rank_two_linear_switch_13_common_scalar.md",
        "theorem_sha256": "0be8e4e0bb28fa2086c434ee459b7d2f2ab061c67f9d45d2ecdb6a059a764478",
        "audit_path": "research_notes/rank_two_linear_switch_13_independent_audit.md",
        "audit_sha256": "4946686c9c19703216662fa00044b6c80e0673e294ef1beb7ee0725233de9bd4",
        "status": "analytic dependencies independently audited",
    },
    "rank_two_stopped_7": {
        "theorem_path": "research_notes/rank_two_mixed_profile_7_stopped_service_theorem.md",
        "theorem_sha256": "e8045791f98334d706e058adab0f838f4bf902a71b08bc1b24a4f3493474355b",
        "audit_path": "research_notes/rank_two_mixed_profile_7_stopped_service_current_exact_byte_audit.md",
        "audit_sha256": "658250797d819a961c8889435f1df795021c0d15d97eb90143f9bdabdbfdef98",
        "status": "analytic dependencies independently audited",
    },
    "hard_common_w_333": {
        "theorem_path": "research_notes/hard333_common_w_fixed_class_theorem.md",
        "theorem_sha256": "ddcc1f054febae9f08bb4d78bd66569ff4eebdd367b5cb4479b9029c960ecf84",
        "audit_path": "research_notes/hard333_final_composition_independent_audit.md",
        "audit_sha256": "8bba33d321e7812a22b2422ca06c33d0abe2e4736c68e9c11be037d8a8819fd6",
        "status": "analytic dependencies independently audited",
    },
}


FINITE_DEPENDENCY_MANIFEST: dict[str, str] = {
    "src/all_active_only_recurrence.py": "c25c18fc85f37a54e02028f4ac8afd389f60c56bad3aa5a40f8b875b99c2eed1",
    "src/critical_one_active_q_trace_certificate.py": "23a30baa3ff9b67a0ee174fd1183f846a607c046bc0201b07e3787ba8833d505",
    "src/global_atlas_interface_closure.py": "293a63711f6da152edd72615d27fad5bbb859aa33a4b7eb150673b27ae3cb5bd",
    "src/global_tier_interface.py": "b8feae08c2eecf21b6e4e387eeaa6f5b15f32d862fca5324d4523c38872494ab",
    "src/one_active_phase_shape.py": "781c1e6b5106cc6785ec6902d932fb319ef2078fb40b4e4f983fdc6f7bc45be4",
    "src/prospective_no_promotion_26.py": "7c0c3b4b3640438816bf7c091de479dae3ea536ffde8511239f34b48b3cc9203",
    "src/rank_one_no_promotion_branch.py": "8775d572485532131de7616f28a92fb9cb551e48fe5f4ed9f71323eed1cefb41",
    "src/rank_two_linear_switch_13.py": "caf223210e695142eea560c5ddb45bbb604759f5f13be4c645686d6478bb3af6",
    "src/rank_two_mixed_profile_7_stopped_service.py": "2130fe04800e26911d470bdb20e2703f9c12834ef3c7d4bacd9ab96fc28f1fc5",
    "src/rank_two_return_certificate.py": "b2a96061516ad3348e7dc997121d2acb989488077a3f03495e58c09ad5890363",
    "src/s_tier_superlevel_interface.py": "1a4e27fcf40af76cac6281f8830b7644bf086b3c05d97a963ce9f5bac736ad57",
    "src/stoichiometric_gate_feasibility.py": "4602e7d31af02c26cc9785ed056c876e3e571e428ad974e861e4940b9edba9a1",
    "src/suppressed_promotion_orbit_certificate.py": "ae9befb765638a3455d2c382d4bd303db29bc9cbba9ec9febb542210640bf7ea",
    "src/two_active_dormant_407_certificate.py": "098969ceeef5589a5a17f000901f43f168583015ac435de8c025add5c412e6a2",
    "src/two_active_easy_common_w.py": "c03e25156ec3718bcf954560a92926b898083fce660018314a7373613ccd4b73",
    "src/two_active_promotion_obstruction.py": "952f28d4900ccadaf535a08fcb995488828ef8e274c12b4043009a9904de948a",
    "tests/test_s_tier_superlevel_interface.py": "4d9f960d89a361a27d9dadbd765297783755b9ec09c60f32301229447f51af40",
}


def _digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def _file_digest(relative_path: str) -> str:
    return sha256((PROJECT_ROOT / relative_path).read_bytes()).hexdigest()


def verify_exact_dependencies() -> None:
    """Reject any silent edit to a pinned finite or analytic dependency."""

    for branch, entry in ANALYTIC_DEPENDENCY_MANIFEST.items():
        for kind in ("theorem", "audit"):
            path = entry[f"{kind}_path"]
            expected = entry[f"{kind}_sha256"]
            actual = _file_digest(path)
            if actual != expected:
                raise AssertionError(
                    f"{branch} {kind} bytes changed: {actual} != {expected}"
                )
    for path, expected in FINITE_DEPENDENCY_MANIFEST.items():
        actual = _file_digest(path)
        if actual != expected:
            raise AssertionError(
                f"finite dependency bytes changed for {path}: "
                f"{actual} != {expected}"
            )


@cache
def corrected_baseline() -> tuple[frozenset[Pair], frozenset[Pair], frozenset[Pair]]:
    """Reconstruct the 2,511 residual pairs from the corrected cut."""

    _positive_passed, positive = corrected_tier.tier_split(
        closure.POSITIVE_SHIELDED_MASKS
    )
    _signed_passed, signed = corrected_tier.tier_split(
        closure.SIGNED_SHIELDED_MASKS
    )
    if positive & signed:
        raise AssertionError("the positive and signed residual strata overlap")
    residual = positive | signed
    if (len(positive), len(signed), len(residual)) != (2312, 199, 2511):
        raise AssertionError("the corrected residual cardinalities changed")
    return positive, signed, residual


@cache
def corrected_affine_branch() -> frozenset[Pair]:
    """Pairs with no affine-feasible failure under the corrected cut."""

    _positive, _signed, residual = corrected_baseline()
    descriptors = tier_geometry.tier_descriptors()
    return frozenset(
        pair
        for pair in residual
        if not any(
            not corrected_tier.universal_strong_orientation_condition(
                pair, descriptor
            )
            and affine_geometry.descriptor_feasible(pair, descriptor)
            for descriptor in descriptors
        )
    )


@cache
def disjoint_branches() -> dict[str, frozenset[Pair]]:
    """Return the fourteen analytic scopes as finite support-pair sets."""

    early = {
        "affine_stoichiometric_151": corrected_affine_branch(),
        "rank_two_14": frozenset(
            pair for pair, _descriptor in rank_two._rank_two_rows()
        ),
        "all_active_only_51": all_active_only.selected_pairs(),
        "rank_one_no_promotion_141": rank_one.candidate_pair_level_pairs(),
        "post_rank_one_one_active_92": rank_one.one_active_obstruction_pairs(),
        "two_active_promotion_36": promotion.pair_level_selector(),
        "suppressed_promotion_4": suppressed.selected_pairs(),
        "critical_one_active_15": critical.selected_pairs(),
    }
    early_union = frozenset().union(*early.values())
    universal = frozenset(one_active.candidate_pairs()) - early_union
    branches = {
        **early,
        "universal_one_active_net_1212": universal,
        "exact_common_w_26": exact26.selected_pairs(),
        "easy_common_w_416": easy416.fully_easy_promotion_pairs(),
        "rank_two_scalar_13": linear13.selected_pairs(),
        "rank_two_stopped_7": stopped7.branch.selected_pairs(),
        "hard_common_w_333": hard333.selected_pairs(),
    }
    if set(branches) != set(ANALYTIC_DEPENDENCY_MANIFEST):
        raise AssertionError("branch and analytic manifests differ")
    names = tuple(sorted(branches))
    overlaps = {
        f"{left}|{right}": branches[left] & branches[right]
        for left, right in combinations(names, 2)
    }
    if any(overlaps.values()):
        raise AssertionError("the fourteen branches are not pairwise disjoint")
    return branches


@cache
def rows() -> tuple[dict[str, object], ...]:
    """Canonical ownership row for each corrected residual pair."""

    positive, _signed, residual = corrected_baseline()
    branches = disjoint_branches()
    owner: dict[Pair, str] = {}
    for name, branch in branches.items():
        for pair in branch:
            if pair in owner:
                raise AssertionError("duplicate pair ownership")
            owner[pair] = name
    if frozenset(owner) != residual:
        raise AssertionError("the branch union is not the corrected residual")
    return tuple(
        {
            "pair": [list(part) for part in closure.pair_payload(pair)],
            "stratum": "positive" if pair in positive else "signed",
            "analytic_branch": owner[pair],
        }
        for pair in sorted(residual, key=closure.pair_payload)
    )


@cache
def certificate() -> dict[str, object]:
    """Return and verify the frozen finite-union payload."""

    verify_exact_dependencies()
    positive, signed, residual = corrected_baseline()
    branches = disjoint_branches()
    canonical_rows = rows()
    rows_hash = _digest(canonical_rows)
    if rows_hash != EXPECTED_ROWS_SHA256:
        raise AssertionError(f"ownership rows changed: {rows_hash}")

    branch_payload = {
        name: {
            "pairs": len(branch),
            "positive": len(branch & positive),
            "signed": len(branch & signed),
            "pair_sha256": closure.pair_fingerprint(branch),
            "analytic_dependency": ANALYTIC_DEPENDENCY_MANIFEST[name],
        }
        for name, branch in sorted(branches.items())
    }
    union = frozenset().union(*branches.values())
    payload: dict[str, object] = {
        "schema": "corrected-t3-2-two-linkage-finite-union-v1",
        "claim_scope": (
            "finite support, corrected S-tier-superlevel, affine, and set "
            "identities only; no stochastic, orientation, or history proof"
        ),
        "corrected_interface": {
            "criterion": "S-tier-superlevel cut",
            "positive_residual_pairs": len(positive),
            "positive_residual_sha256": closure.pair_fingerprint(positive),
            "signed_residual_pairs": len(signed),
            "signed_residual_sha256": closure.pair_fingerprint(signed),
            "total_residual_pairs": len(residual),
            "total_residual_sha256": closure.pair_fingerprint(residual),
            "certificate_sha256": "77c7ce0d2325379acfed7b13a44f9577454279275918ee14f968e313b488a7e0",
        },
        "baseline": {
            "pairs": len(residual),
            "positive": len(positive),
            "signed": len(signed),
            "pair_sha256": closure.pair_fingerprint(residual),
        },
        "branches": branch_payload,
        "branch_count": len(branches),
        "pairwise_disjoint": True,
        "union_equals_corrected_baseline": union == residual,
        "remaining_pairs": len(residual - union),
        "rows_sha256": rows_hash,
        "finite_code_role": "finite identities only; no analytic proof",
        "analytic_dependency_status": (
            "analytic dependencies independently audited"
        ),
        "global_claim_status": (
            "not asserted by this finite certificate"
        ),
        "finite_dependency_manifest": FINITE_DEPENDENCY_MANIFEST,
    }
    payload_hash = _digest(payload)
    if payload_hash != EXPECTED_PAYLOAD_SHA256:
        raise AssertionError(f"certificate payload changed: {payload_hash}")
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
