"""Finite coverage premises for the proof-first hard-333 theorem.

The stochastic estimates are proved in the pinned analytic notes.  This
module has the deliberately narrower job of checking that every failed
descriptor on the final 333 support pairs is assigned once to one of those
lemmas and that one correction vector is compatible across each pair.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import hard_one_active_1104_common_w as one_active1104
import hard_physical188_common_w as physical188
import prospective_no_promotion_26 as atlas
import three_active_flat_phase as flat
import three_active_gluing_gate as all_active
import two_active_dormant_407_certificate as hard
import two_active_phase_gate as two_active


EXPECTED_PAIR_ROWS_SHA256 = (
    "a1765765a7bc7f9eafd2f9ca0744f082a61a83ad7df9f8efc01a3f38aaa9de08"
)
EXPECTED_FAILURE_ROWS_SHA256 = (
    "b96325940e9d4178e9ef3dcd7f221fcd0e758b2f1c30b4904e2b3b0fc3fb7ca9"
)
EXPECTED_PAYLOAD_SHA256 = (
    "9537f53f0aa3af10ac612b01da85081a3bd44b0382f689149da5f5917e353cc1"
)

ONE_ACTIVE_1104_NOTE_SHA256 = (
    "d2d2eff482190abb78ae7d5b0a83440881931ff8387f35435d2066fb8b20bca8"
)
ONE_ACTIVE_1104_SOURCE_SHA256 = (
    "03f61eb180792201cf5bbdcbd1ac85b198cd02bcddb85e7e46771d9fdd4c47cc"
)
ONE_ACTIVE_1104_TEST_SHA256 = (
    "29856f4c64c30bb376527389e4c90d06e79c4bd5647aff511c19428df1d141db"
)
ONE_ACTIVE_1104_ROWS_SHA256 = (
    "66d931827f2b118306cd10b732d368b50d77f929dafae3c36b1bfae47a40d1b4"
)
ONE_ACTIVE_1104_PAYLOAD_SHA256 = (
    "8a5c7f6f6c55fbe3ddb9fa1f438677212c15075d0294f706958c44cc6b91eef3"
)


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _file_sha256(relative: str) -> str:
    root = Path(__file__).resolve().parents[1]
    return sha256((root / relative).read_bytes()).hexdigest()


def _pair_payload(pair: closure.Pair) -> list[list[str]]:
    return [list(part) for part in closure.pair_payload(pair)]


def _descriptor_key(
    pair: closure.Pair, descriptor: tier.Descriptor
) -> tuple[tuple[tuple[str, ...], tuple[str, ...]], tuple[int, ...], tuple[int, ...]]:
    return (
        closure.pair_payload(pair),
        tuple(descriptor.weight),
        tuple(descriptor.caps),
    )


def _payload_descriptor_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        tuple(tuple(part) for part in row["pair"]),
        tuple(row["weight"]),
        tuple(row["caps"]),
    )


def pair_rows(
    failures: tuple[dict[str, object], ...] | None = None,
    rankone_rows: tuple[dict[str, object], ...] | None = None,
) -> tuple[dict[str, object], ...]:
    """Recover the pair correction directly from its audited local rows."""

    if failures is None:
        failures = failure_rows()
    if rankone_rows is None:
        selected = frozenset(
            tuple(closure.mask(part) for part in row["pair"])
            for row in failures
        )
        rankone_rows = _rankone_premise_rows(selected)

    pair_payloads = {
        tuple(tuple(part) for part in row["pair"])
        for row in failures
    }
    assert len(pair_payloads) == 333
    hb_payloads = {
        tuple(tuple(part) for part in row["pair"])
        for row in failures
        if row["analytic_route"] == "H_b12_guard_free_shell_resolvent"
    }
    hw_payloads = {
        tuple(tuple(part) for part in row["pair"])
        for row in failures
        if row["analytic_route"] == "H_w4_dyadic_activation_return"
    }
    assert (len(hb_payloads), len(hw_payloads)) == (12, 4)
    assert not (hb_payloads & hw_payloads)

    correction_evidence: dict[
        tuple[tuple[str, ...], ...], set[str]
    ] = {pair: set() for pair in pair_payloads}
    for row in rankone_rows:
        pair = tuple(tuple(part) for part in row["pair"])
        correction_evidence[pair].add(str(row["correction_family"]))

    all_active_correction = {
        "safe_reversible_powered_generator": "reversible_top_adjusted_ell",
        "directed_triple_powered_generator": "directed_triple_adjusted_ell",
        "H_b12_guard_free_shell_resolvent": "reversible_top_adjusted_ell",
        "H_w4_dyadic_activation_return": "arbitrary_fixed_ell",
    }
    for row in failures:
        if row["active_coordinates"] != 3:
            continue
        pair = tuple(tuple(part) for part in row["pair"])
        correction_evidence[pair].add(
            all_active_correction[str(row["analytic_route"])]
        )

    rows: list[dict[str, object]] = []
    for key in sorted(pair_payloads):
        evidence = correction_evidence[key]
        assert len(evidence) <= 1
        correction = next(iter(evidence), "arbitrary_fixed_ell")
        if key in hb_payloads:
            assert correction == "reversible_top_adjusted_ell"
            correction = "reversible_top_adjusted_ell"
            switch = "H_b_guard_free_shell"
        elif key in hw_payloads:
            assert correction == "arbitrary_fixed_ell"
            correction = "arbitrary_fixed_ell"
            switch = "H_w_dyadic_activation_return"
        else:
            switch = "ordinary_common_factorial"
        rows.append(
            {
                "pair": [list(part) for part in key],
                "pair_fixed_correction_family": correction,
                "all_active_switch": switch,
            }
        )

    assert len(rows) == 333
    assert len({tuple(tuple(p) for p in row["pair"]) for row in rows}) == 333
    return tuple(rows)


def _one_active_routes() -> dict[tuple[object, ...], str]:
    result = {
        _payload_descriptor_key(row): str(row["analytic_route"])
        for row in one_active1104.coverage_rows()
    }
    assert len(result) == 1104
    return result


def _two_active_routes(
    selected: frozenset[closure.Pair],
) -> dict[tuple[object, ...], str]:
    result: dict[tuple[object, ...], str] = {}
    for pair, descriptor, category in two_active.incidences():
        if pair not in selected:
            continue
        key = _descriptor_key(pair, descriptor)
        if category == "promotion_dormant_top":
            route = "physical188_macroscopic_carrier"
        elif category == "promotion_enabled_top_seed":
            route = "enabled181_access_word"
        else:
            assert category == "closed_rank_one_top_phase"
            route = "rankone114_powered_endpoint"
        assert key not in result
        result[key] = route
    assert len(result) == 702
    return result


def _rankone_premise_rows(
    selected: frozenset[closure.Pair],
) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for pair, descriptor, category in two_active.incidences():
        if pair not in selected or category != "closed_rank_one_top_phase":
            continue
        top, = two_active._whole_top_linkages(pair, descriptor)
        support = tuple(closure.support(top))
        assert len(support) in (2, 3)
        correction = (
            "directed_triple_adjusted_ell"
            if len(support) == 3
            else "reversible_top_adjusted_ell"
        )
        rows.append(
            {
                "pair": _pair_payload(pair),
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "top": list(support),
                "correction_family": correction,
            }
        )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")))
    assert len(rows) == 114
    assert Counter(row["correction_family"] for row in rows) == {
        "reversible_top_adjusted_ell": 90,
        "directed_triple_adjusted_ell": 24,
    }
    return tuple(rows)


def _all_active_route(
    pair: closure.Pair, descriptor: tier.Descriptor
) -> str:
    _side, top = flat.whole_top_linkage(pair, descriptor)
    rank = flat._support_rank(top)
    if rank == 2:
        return "H_w4_dyadic_activation_return"
    if top.bit_count() == 3:
        assert rank == 1
        return "directed_triple_powered_generator"
    assert rank == 1 and top.bit_count() == 2
    if all_active.direct_entropy_safe(pair, descriptor):
        return "safe_reversible_powered_generator"
    return "H_b12_guard_free_shell_resolvent"


def failure_rows() -> tuple[dict[str, object], ...]:
    one = _one_active_routes()
    selected = frozenset(
        tuple(closure.mask(part) for part in key[0])
        for key in one
    )
    assert len(selected) == 333
    assert closure.pair_fingerprint(selected) == hard.EXPECTED_PAIR_SHA256
    two = _two_active_routes(selected)
    rows: list[dict[str, object]] = []
    for pair in sorted(selected, key=closure.pair_payload):
        for descriptor in atlas.failures(pair):
            key = _descriptor_key(pair, descriptor)
            active = len(tier._active_coordinates(descriptor))
            if active == 1:
                route = one[key]
            elif active == 2:
                route = two[key]
            else:
                assert active == 3
                route = _all_active_route(pair, descriptor)
            row = {
                "pair": _pair_payload(pair),
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "active_coordinates": active,
                "analytic_route": route,
            }
            if active == 3:
                _side, top = flat.whole_top_linkage(pair, descriptor)
                row["top_support"] = list(closure.support(top))
            rows.append(row)
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")))
    assert len(rows) == 1960
    assert len({_payload_descriptor_key(row) for row in rows}) == 1960
    return tuple(rows)


def _switch_mask_compatibility(
    failures: tuple[dict[str, object], ...],
    rankone_rows: tuple[dict[str, object], ...],
) -> dict[str, int | bool]:
    """Check the support identity on the sixteen pair-level switches."""

    hb_payloads = {
        tuple(tuple(part) for part in row["pair"])
        for row in failures
        if row["analytic_route"] == "H_b12_guard_free_shell_resolvent"
    }
    hw_payloads = {
        tuple(tuple(part) for part in row["pair"])
        for row in failures
        if row["analytic_route"] == "H_w4_dyadic_activation_return"
    }
    switch_payloads = hb_payloads | hw_payloads
    assert (len(hb_payloads), len(hw_payloads)) == (12, 4)

    all_active_masks: dict[tuple[tuple[str, ...], ...], set[tuple[str, ...]]] = {}
    for row in failures:
        if row["analytic_route"] not in {
            "H_b12_guard_free_shell_resolvent",
            "H_w4_dyadic_activation_return",
        }:
            continue
        pair = tuple(tuple(part) for part in row["pair"])
        all_active_masks.setdefault(pair, set()).add(tuple(row["top_support"]))

    rankone_masks: dict[tuple[tuple[str, ...], ...], set[tuple[str, ...]]] = {}
    for row in rankone_rows:
        pair = tuple(tuple(part) for part in row["pair"])
        rankone_masks.setdefault(pair, set()).add(tuple(row["top"]))

    assert len(switch_payloads) == 16
    assert all(pair in all_active_masks for pair in switch_payloads)
    assert all(len(all_active_masks[pair]) == 1 for pair in switch_payloads)

    rankone_overlap = switch_payloads & set(rankone_masks)
    assert rankone_overlap == hb_payloads
    assert all(len(rankone_masks[pair]) == 1 for pair in rankone_overlap)
    assert all(
        rankone_masks[pair] == all_active_masks[pair]
        for pair in rankone_overlap
    )
    assert not (hw_payloads & set(rankone_masks))

    return {
        "switch_pairs": len(switch_payloads),
        "switch_pairs_with_one_all_active_mask": sum(
            len(all_active_masks[pair]) == 1 for pair in switch_payloads
        ),
        "rankone_overlap_pairs": len(rankone_overlap),
        "rankone_overlap_pairs_with_one_identical_mask": sum(
            len(rankone_masks[pair]) == 1
            and rankone_masks[pair] == all_active_masks[pair]
            for pair in rankone_overlap
        ),
        "H_w_pairs_with_no_rankone_mask": sum(
            pair not in rankone_masks for pair in hw_payloads
        ),
        "all_switch_mask_assertions_passed": True,
    }


def _correction_compatibility(
    pairs: tuple[dict[str, object], ...],
    failures: tuple[dict[str, object], ...],
    rankone_rows: tuple[dict[str, object], ...],
) -> dict[str, int | bool]:
    """Compare pair-fixed corrections on every rank-one/all-active row."""

    pair_correction = {
        tuple(tuple(part) for part in row["pair"]): row[
            "pair_fixed_correction_family"
        ]
        for row in pairs
    }

    rankone_mismatches = [
        row
        for row in rankone_rows
        if pair_correction[tuple(tuple(part) for part in row["pair"])]
        != row["correction_family"]
    ]
    assert len(rankone_rows) == 114
    assert not rankone_mismatches

    expected_all_active_correction = {
        "safe_reversible_powered_generator": "reversible_top_adjusted_ell",
        "directed_triple_powered_generator": "directed_triple_adjusted_ell",
        "H_b12_guard_free_shell_resolvent": "reversible_top_adjusted_ell",
        "H_w4_dyadic_activation_return": "arbitrary_fixed_ell",
    }
    all_active_rows = [row for row in failures if row["active_coordinates"] == 3]
    all_active_mismatches = [
        row
        for row in all_active_rows
        if pair_correction[tuple(tuple(part) for part in row["pair"])]
        != expected_all_active_correction[row["analytic_route"]]
    ]
    assert len(all_active_rows) == 154
    assert not all_active_mismatches

    return {
        "rankone_rows_checked": len(rankone_rows),
        "rankone_correction_mismatches": len(rankone_mismatches),
        "all_active_rows_checked": len(all_active_rows),
        "all_active_correction_mismatches": len(all_active_mismatches),
        "all_114_plus_154_corrections_match_pair_fixed_choice": True,
    }


def certificate() -> dict[str, object]:
    failures = failure_rows()
    selected = frozenset(
        tuple(closure.mask(part) for part in row["pair"])
        for row in failures
    )
    rankone_rows = _rankone_premise_rows(selected)
    pairs = pair_rows(failures, rankone_rows)
    pair_hash = _digest(pairs)
    failure_hash = _digest(failures)
    active_histogram = Counter(row["active_coordinates"] for row in failures)
    route_histogram = Counter(row["analytic_route"] for row in failures)
    correction_histogram = Counter(
        row["pair_fixed_correction_family"] for row in pairs
    )
    switch_masks = _switch_mask_compatibility(failures, rankone_rows)
    correction_compatibility = _correction_compatibility(
        pairs, failures, rankone_rows
    )

    one_active_certificate = one_active1104.certificate()
    assert one_active_certificate["rows_sha256"] == ONE_ACTIVE_1104_ROWS_SHA256
    assert (
        one_active_certificate["payload_sha256"]
        == ONE_ACTIVE_1104_PAYLOAD_SHA256
    )
    assert one_active_certificate[
        "analytic_one_active_1104_theorem_independently_audited"
    ]
    one_active_proof_hashes = {
        "theorem_sha256": _file_sha256(
            "research_notes/hard_one_active_1104_common_w_theorem.md"
        ),
        "source_sha256": _file_sha256(
            "src/hard_one_active_1104_common_w.py"
        ),
        "test_sha256": _file_sha256(
            "tests/test_hard_one_active_1104_common_w.py"
        ),
    }
    assert one_active_proof_hashes == {
        "theorem_sha256": ONE_ACTIVE_1104_NOTE_SHA256,
        "source_sha256": ONE_ACTIVE_1104_SOURCE_SHA256,
        "test_sha256": ONE_ACTIVE_1104_TEST_SHA256,
    }

    assert active_histogram == {1: 1104, 2: 702, 3: 154}
    assert route_histogram == {
        "audited_generalized_146": 951,
        "audited_direct_C_multiservice": 99,
        "audited_open_all_clock_multiservice": 6,
        "abstract_mixed_fast_schur_extension": 44,
        "zero_inactive_absorbing_face": 4,
        "physical188_macroscopic_carrier": 407,
        "enabled181_access_word": 181,
        "rankone114_powered_endpoint": 114,
        "safe_reversible_powered_generator": 110,
        "directed_triple_powered_generator": 24,
        "H_b12_guard_free_shell_resolvent": 16,
        "H_w4_dyadic_activation_return": 4,
    }
    assert correction_histogram == {
        "arbitrary_fixed_ell": 291,
        "reversible_top_adjusted_ell": 34,
        "directed_triple_adjusted_ell": 8,
    }
    assert len(physical188.rows()) == 188
    assert {
        (
            tuple(map(int, row["normalized_ratio"])),
            tuple(row["proper_support"]),
            tuple(row["other_support"]),
        )
        for row in hard.normalized_templates()
    } == {
        (tuple(row["ratio"]), tuple(row["proper"]), tuple(row["lower"]))
        for row in physical188.rows()
    }

    payload = {
        "claim_scope": (
            "finite descriptor exhaustion and one-correction compatibility "
            "for the proof-first hard-333 theorem"
        ),
        "pairs": len(pairs),
        "pair_sha256": closure.pair_fingerprint(
            frozenset(
                tuple(closure.mask(part) for part in row["pair"])
                for row in pairs
            )
        ),
        "pair_rows_sha256": pair_hash,
        "failed_incidences": len(failures),
        "failure_rows_sha256": failure_hash,
        "active_count_histogram": {
            str(key): value for key, value in sorted(active_histogram.items())
        },
        "analytic_route_histogram": dict(sorted(route_histogram.items())),
        "pair_correction_histogram": dict(sorted(correction_histogram.items())),
        "audited_one_active_1104_input": {
            "proof_hashes": one_active_proof_hashes,
            "rows_sha256": one_active_certificate["rows_sha256"],
            "payload_sha256": one_active_certificate["payload_sha256"],
            "strict_scope_audit_passed": True,
        },
        "switch_mask_compatibility": switch_masks,
        "correction_compatibility": correction_compatibility,
        "physical_dormant_normalized_templates": 188,
        "finite_code_role": (
            "descriptor and premise coverage only; no stochastic, orientation, "
            "reaction-history, or population-box proof"
        ),
        "hard333_composition_independently_audited": False,
        "hard333_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    payload_hash = _digest(payload)
    if EXPECTED_PAIR_ROWS_SHA256 != "TO_BE_FILLED":
        assert pair_hash == EXPECTED_PAIR_ROWS_SHA256
    if EXPECTED_FAILURE_ROWS_SHA256 != "TO_BE_FILLED":
        assert failure_hash == EXPECTED_FAILURE_ROWS_SHA256
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert payload_hash == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
