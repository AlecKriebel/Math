"""Independent finite replay for the proof-first hard-333 audit.

The mathematical audit is recorded in
``research_notes/hard333_final_composition_independent_audit.md``.  This
module deliberately checks only frozen bytes, descriptor routing, analytic
premises, and literal correction-mask compatibility.  It does not infer a
stochastic estimate from a finite search.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import hard333_final_descriptor_coverage as candidate
import hard_one_active_1104_common_w as one_active
import hard_physical188_common_w as physical188
import prospective_no_promotion_26 as atlas
import three_active_flat_phase as flat
import three_active_gluing_gate as all_active
import two_active_dormant_407_certificate as dormant
import two_active_phase_gate as two_active


TARGET_HASHES = {
    "theorem": "ddcc1f054febae9f08bb4d78bd66569ff4eebdd367b5cb4479b9029c960ecf84",
    "source": "de618c831152352f0898cdb6cd6a0bfc286e73c6b15d28c507ad4fd8ecde9049",
    "test": "fb1becfc2183ec691d711375459ef75bc824668a6b348ad4530cd6d11bb09e0a",
}

TARGET_PATHS = {
    "theorem": "research_notes/hard333_common_w_fixed_class_theorem.md",
    "source": "src/hard333_final_descriptor_coverage.py",
    "test": "tests/test_hard333_final_descriptor_coverage.py",
}

# These are the audited local proof inputs actually replayed by the hostile
# composition audit.  Pinning them prevents a later edit from silently
# inheriting this verdict.
DEPENDENCY_HASHES = {
    "research_notes/hard_one_active_1104_common_w_theorem.md":
        "d2d2eff482190abb78ae7d5b0a83440881931ff8387f35435d2066fb8b20bca8",
    "src/hard_one_active_1104_common_w.py":
        "03f61eb180792201cf5bbdcbd1ac85b198cd02bcddb85e7e46771d9fdd4c47cc",
    "tests/test_hard_one_active_1104_common_w.py":
        "29856f4c64c30bb376527389e4c90d06e79c4bd5647aff511c19428df1d141db",
    "research_notes/hard_one_active_direct_open_multiservice_repair.md":
        "fbd9f42815b08a2030d931482b70ff10aca9a92df3c080e2533f275fa6733c2a",
    "research_notes/hard_one_active_direct_open_multiservice_repair_independent_audit.md":
        "9ecd375375e6942d803d068591c80f87a27119a37927dd3617f2e743afdab848",
    "research_notes/proof_first_hard_physical188_common_w_theorem.md":
        "fc9f1b9039fe1cf416c2d346799465c4a16c0c84e5cde85b6d1168d1355d89f4",
    "research_notes/proof_first_hard_physical188_common_w_independent_audit.md":
        "6c4442b557e61fc526c63fd49497843c93575fa5aa545e135e52496cfc3ab526",
    "src/hard_physical188_common_w.py":
        "9be690af29127013613d6d5f3d482943f51248d37da9d4af21c2b44cda1c0b65",
    "tests/test_hard_physical188_common_w.py":
        "39f71e131532303015544de75023bc58b34803edf1c19891e964c69cacb727ac",
    "research_notes/proof_first_hard_enabled181_access_word.md":
        "9be70e2b6c9ce5c4762bf3130246f1ea660bea73f41aa7abdd997853cc0a6b04",
    "research_notes/proof_first_hard_enabled181_access_word_independent_audit.md":
        "4028c026a7d01c1e0930bdbdaa75216a79402078999d6450c283a77eb2a04883",
    "src/hard_enabled181_access_word.py":
        "7a4397e01c36767474d1040e7937a992f1caa551192e936872e7ed6057243582",
    "tests/test_hard_enabled181_access_word.py":
        "33a8a9337a131bf67b9f562134cec2c418b2ab15b9f5b39381fab5c0ba4260de",
    "research_notes/proof_first_hard_rankone114_powered_endpoint.md":
        "8802e901d501494bbdbc2e33acf5a0b0df44d12218acdd9ad5ed72c0abfb4a33",
    "research_notes/proof_first_hard_rankone114_powered_endpoint_independent_audit.md":
        "43c85f9ac7595fa6b704f82aefadad6a3fe49853f6f6ce0795306070f868a6e4",
    "src/hard_rankone114_powered_endpoint.py":
        "725ab17abb7295b3a0e2feb79b1d4d4d43336d31d9d614fc40a8314f81a60974",
    "tests/test_hard_rankone114_powered_endpoint.py":
        "a5822e09cf18f3f62d4b5e938ea50faa1000d90b6bc6714e3a6ea8d652b39136",
    "research_notes/prospective_26_candidate_pair_theorem.md":
        "c78e53f11aeb981b415a90a486583b409608ef2256b73b9e063db48ac8d4fc88",
    "src/prospective_26_candidate_theorem.py":
        "45e42904072bb1cd451a98fdfd2750c0bb8ed442e028a9a1198193f1b91abff5",
    "tests/test_prospective_26_candidate_theorem.py":
        "d770f7c723b9748cf2f25cd455bf6a630dfd5eeea8bff287ca72d3739b8ee896",
    "research_notes/two_active_easy_943_common_w_theorem.md":
        "4764849b05915b9005d68ac885c512a906af439430e8db8a7131f04645224e29",
    "research_notes/two_active_easy_416_independent_audit.md":
        "c07f9d9d79574d1c590b03d552de574882c141c84f35fdf452508689e46743f6",
    "research_notes/hard333_hb12_global_shell_resolvent.md":
        "8e6988149d6a889582ead592e47c05c3ca9a02f27da6e68182eea9959d55c513",
    "research_notes/hard333_hb12_global_shell_resolvent_independent_audit.md":
        "6c3b62d6b19b89a8b0881885fb8a93c35dce3e13ffb4d8b1264342d76e111b3e",
    "src/hard333_hb12_global_shell_resolvent.py":
        "01c99b0a5cb872be68d0adce6b7ffabd5cd499ded63b5c8d3b2b9df0801ddeaa",
    "tests/test_hard333_hb12_global_shell_resolvent.py":
        "b6634246517734714cd990bb68a95e036a1a254a425cb383b8467b57217f1f6e",
    "research_notes/hard333_hw4_dyadic_compound_activation.md":
        "df392304c5c0b5476584175c4601fd2e3d7f80e41154ae03c7ab1bd9de54b518",
    "research_notes/hard333_hw4_dyadic_compound_activation_patch_replay.md":
        "a29454f9659b6dc9a254e6c492c40fa85a56263a6788ba127957634af108edfa",
    "src/hard333_hw4_dyadic_compound_activation.py":
        "bbe1bd66769c14c88930bb28a3402abba980b6d0422ce2201c83c1ea28be6a8f",
    "tests/test_hard333_hw4_dyadic_compound_activation.py":
        "cf273a011d38b26f455b6490ba52d43dfde2962e34a749094f2cea0ba59ebb54",
    "research_notes/proof_first_hard_family_fixed_class_composition.md":
        "43b311cf898cf8fef5c075e173327df5a3b4b72db67d742b88e48ad85a2f411a",
}


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def _file_hash(relative: str) -> str:
    return sha256((_root() / relative).read_bytes()).hexdigest()


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _pair_from_payload(payload: object) -> closure.Pair:
    return tuple(closure.mask(part) for part in payload)  # type: ignore[arg-type]


def _pair_payload(pair: closure.Pair) -> tuple[tuple[str, ...], ...]:
    return closure.pair_payload(pair)


def _key(
    pair: closure.Pair, descriptor: tier.Descriptor
) -> tuple[tuple[tuple[str, ...], ...], tuple[int, ...], tuple[int, ...]]:
    return (
        _pair_payload(pair),
        tuple(descriptor.weight),
        tuple(descriptor.caps),
    )


def _payload_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        tuple(tuple(part) for part in row["pair"]),
        tuple(row["weight"]),
        tuple(row["caps"]),
    )


def _three_active_route(
    pair: closure.Pair, descriptor: tier.Descriptor
) -> tuple[str, tuple[str, ...], str]:
    _side, top = flat.whole_top_linkage(pair, descriptor)
    support = tuple(closure.support(top))
    rank = flat._support_rank(top)
    if rank == 2:
        return "H_w4_dyadic_activation_return", support, "arbitrary_fixed_ell"
    if top.bit_count() == 3:
        assert rank == 1
        return (
            "directed_triple_powered_generator",
            support,
            "directed_triple_adjusted_ell",
        )
    assert rank == 1 and top.bit_count() == 2
    route = (
        "safe_reversible_powered_generator"
        if all_active.direct_entropy_safe(pair, descriptor)
        else "H_b12_guard_free_shell_resolvent"
    )
    return route, support, "reversible_top_adjusted_ell"


def independent_rows() -> tuple[dict[str, object], ...]:
    """Rebuild the finite routing from the lower-level certified tables."""

    one_by_key = {_payload_key(row): row for row in one_active.coverage_rows()}
    assert len(one_by_key) == 1104
    selected = frozenset(_pair_from_payload(key[0]) for key in one_by_key)
    assert len(selected) == 333

    two_by_key: dict[tuple[object, ...], str] = {}
    two_route = {
        "promotion_dormant_top": "physical188_macroscopic_carrier",
        "promotion_enabled_top_seed": "enabled181_access_word",
        "closed_rank_one_top_phase": "rankone114_powered_endpoint",
    }
    for pair, descriptor, category in two_active.incidences():
        if pair not in selected:
            continue
        key = _key(pair, descriptor)
        assert key not in two_by_key
        two_by_key[key] = two_route[category]
    assert len(two_by_key) == 702

    rows: list[dict[str, object]] = []
    for pair in sorted(selected, key=_pair_payload):
        for descriptor in atlas.failures(pair):
            key = _key(pair, descriptor)
            active = len(tier._active_coordinates(descriptor))
            row: dict[str, object] = {
                "pair": [list(part) for part in _pair_payload(pair)],
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "active_coordinates": active,
            }
            if active == 1:
                row["analytic_route"] = one_by_key[key]["analytic_route"]
            elif active == 2:
                row["analytic_route"] = two_by_key[key]
            else:
                assert active == 3
                route, support, _correction = _three_active_route(pair, descriptor)
                row["analytic_route"] = route
                row["top_support"] = list(support)
            rows.append(row)
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")))
    assert len(rows) == 1960
    assert len({_payload_key(row) for row in rows}) == 1960
    return tuple(rows)


def _mask_and_correction_replay(
    rows: tuple[dict[str, object], ...]
) -> dict[str, object]:
    selected = frozenset(_pair_from_payload(row["pair"]) for row in rows)
    rank_masks: dict[tuple[tuple[str, ...], ...], set[tuple[str, ...]]] = defaultdict(set)
    all_masks: dict[tuple[tuple[str, ...], ...], set[tuple[str, ...]]] = defaultdict(set)
    evidence: dict[tuple[tuple[str, ...], ...], set[str]] = defaultdict(set)

    for pair, descriptor, category in two_active.incidences():
        if pair not in selected or category != "closed_rank_one_top_phase":
            continue
        top, = two_active._whole_top_linkages(pair, descriptor)
        support = tuple(closure.support(top))
        payload = _pair_payload(pair)
        rank_masks[payload].add(support)
        evidence[payload].add(
            "directed_triple_adjusted_ell"
            if len(support) == 3
            else "reversible_top_adjusted_ell"
        )

    for pair in selected:
        for descriptor in atlas.failures(pair):
            if len(tier._active_coordinates(descriptor)) != 3:
                continue
            _route, support, correction = _three_active_route(pair, descriptor)
            payload = _pair_payload(pair)
            all_masks[payload].add(support)
            evidence[payload].add(correction)

    assert len(rank_masks) == 38
    assert len(all_masks) == 46
    assert set(rank_masks) <= set(all_masks)
    assert all(len(masks) == 1 for masks in rank_masks.values())
    assert all(len(masks) == 1 for masks in all_masks.values())
    assert all(rank_masks[pair] == all_masks[pair] for pair in rank_masks)
    assert all(len(values) == 1 for values in evidence.values())

    relevant_pairs = set(evidence)
    pair_correction = {
        _pair_payload(pair): next(
            iter(evidence.get(_pair_payload(pair), set())), "arbitrary_fixed_ell"
        )
        for pair in selected
    }
    correction_histogram = Counter(pair_correction.values())
    assert correction_histogram == {
        "arbitrary_fixed_ell": 291,
        "reversible_top_adjusted_ell": 34,
        "directed_triple_adjusted_ell": 8,
    }

    hb_pairs = {
        tuple(tuple(part) for part in row["pair"])
        for row in rows
        if row["analytic_route"] == "H_b12_guard_free_shell_resolvent"
    }
    hw_pairs = {
        tuple(tuple(part) for part in row["pair"])
        for row in rows
        if row["analytic_route"] == "H_w4_dyadic_activation_return"
    }
    assert (len(hb_pairs), len(hw_pairs)) == (12, 4)
    assert hb_pairs <= set(rank_masks)
    assert not (hw_pairs & set(rank_masks))

    return {
        "rankone_pairs": len(rank_masks),
        "rankone_pairs_with_one_mask": sum(len(value) == 1 for value in rank_masks.values()),
        "all_active_pairs": len(all_masks),
        "all_active_pairs_with_one_mask": sum(len(value) == 1 for value in all_masks.values()),
        "rankone_all_active_overlap_pairs": len(set(rank_masks) & set(all_masks)),
        "overlap_pairs_with_identical_mask": sum(
            rank_masks[pair] == all_masks[pair] for pair in rank_masks
        ),
        "correction_relevant_pairs": len(relevant_pairs),
        "correction_relevant_pairs_with_one_literal_mask": sum(
            len(all_masks.get(pair, set()) | rank_masks.get(pair, set())) == 1
            for pair in relevant_pairs
        ),
        "H_b_pairs": len(hb_pairs),
        "H_w_pairs": len(hw_pairs),
        "H_w_pairs_without_rankone_mask": sum(pair not in rank_masks for pair in hw_pairs),
        "pair_correction_histogram": dict(sorted(correction_histogram.items())),
    }


def certificate() -> dict[str, object]:
    target_actual = {name: _file_hash(path) for name, path in TARGET_PATHS.items()}
    assert target_actual == TARGET_HASHES
    dependency_actual = {path: _file_hash(path) for path in DEPENDENCY_HASHES}
    assert dependency_actual == DEPENDENCY_HASHES

    independent = independent_rows()
    frozen = candidate.failure_rows()
    assert independent == frozen
    frozen_certificate = candidate.certificate()
    assert frozen_certificate["pair_rows_sha256"] == candidate.EXPECTED_PAIR_ROWS_SHA256
    assert frozen_certificate["failure_rows_sha256"] == candidate.EXPECTED_FAILURE_ROWS_SHA256
    assert frozen_certificate["payload_sha256"] == candidate.EXPECTED_PAYLOAD_SHA256

    active_histogram = Counter(row["active_coordinates"] for row in independent)
    route_histogram = Counter(row["analytic_route"] for row in independent)
    assert active_histogram == {1: 1104, 2: 702, 3: 154}
    assert route_histogram == {
        "audited_generalized_146": 951,
        "audited_direct_C_multiservice": 99,
        "abstract_mixed_fast_schur_extension": 44,
        "zero_inactive_absorbing_face": 4,
        "audited_open_all_clock_multiservice": 6,
        "physical188_macroscopic_carrier": 407,
        "enabled181_access_word": 181,
        "rankone114_powered_endpoint": 114,
        "safe_reversible_powered_generator": 110,
        "directed_triple_powered_generator": 24,
        "H_b12_guard_free_shell_resolvent": 16,
        "H_w4_dyadic_activation_return": 4,
    }

    physical_replay = {
        (
            tuple(map(int, row["normalized_ratio"])),
            tuple(row["proper_support"]),
            tuple(row["other_support"]),
        )
        for row in dormant.normalized_templates()
    }
    audited_physical = {
        (tuple(row["ratio"]), tuple(row["proper"]), tuple(row["lower"]))
        for row in physical188.rows()
    }
    assert physical_replay == audited_physical
    assert len(audited_physical) == 188

    masks = _mask_and_correction_replay(independent)
    assert frozen_certificate["hard333_composition_independently_audited"] is False
    assert frozen_certificate["hard333_pair_recurrence_certified"] is False
    assert frozen_certificate["global_t3_2_certified"] is False

    payload: dict[str, object] = {
        "claim_scope": (
            "independent proof-first composition audit of the frozen hard-333 "
            "fixed-class theorem; finite replay is premise/exhaustion only"
        ),
        "target_hashes": target_actual,
        "dependency_hashes": dependency_actual,
        "pairs": 333,
        "failed_incidences": 1960,
        "active_count_histogram": {
            str(key): value for key, value in sorted(active_histogram.items())
        },
        "analytic_route_histogram": dict(sorted(route_histogram.items())),
        "independent_failure_rows_sha256": _digest(independent),
        "candidate_failure_rows_sha256": frozen_certificate["failure_rows_sha256"],
        "physical_dormant_normalized_templates": len(audited_physical),
        "literal_correction_mask_replay": masks,
        "proof_obligations": {
            "one_literal_common_W_per_pair": True,
            "reflected_debt_eligibility": True,
            "multiservice_D1_internal_DK_terminal": True,
            "actual_endpoint_and_physical_time_moments_q_gt_8": True,
            "active2_and_active3_handoffs": True,
            "passing_descriptor_generator_descent": True,
            "properness": True,
            "nonexplosion": True,
            "random_time_foster_gluing": True,
            "finite_mean_return_implies_positive_recurrence": True,
        },
        "audit_verdict": "STRICT PASS",
        "hard333_fixed_class_theorem_independently_audited": True,
        "hard333_pair_recurrence_theorem_established": True,
        "candidate_flags_were_not_modified": True,
        "global_t3_2_certified": False,
    }
    return {**payload, "payload_sha256": _digest(payload)}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
