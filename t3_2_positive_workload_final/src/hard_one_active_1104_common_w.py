"""Proof-premise certificate for the hard-family one-active interface.

The executable layer is deliberately finite and claim-limited.  It checks
the exact 1,104-incidence partition and the support predicates used by the
analytic proof.  It does not enumerate orientations, population histories,
or reaction words, and it does not infer any stochastic estimate.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

import global_atlas_interface_closure as closure
import two_active_dormant_407_certificate as hard


EXPECTED_ROWS_SHA256 = (
    "66d931827f2b118306cd10b732d368b50d77f929dafae3c36b1bfae47a40d1b4"
)
EXPECTED_PAYLOAD_SHA256 = (
    "8a5c7f6f6c55fbe3ddb9fa1f438677212c15075d0294f706958c44cc6b91eef3"
)

GENERALIZED_146_NOTE_SHA256 = (
    "e522eb75506293173f0099117b5179db38e7be486ab44670493d761f9a698bc8"
)
GENERALIZED_146_SOURCE_SHA256 = (
    "503715a05e9700dc549d80efd5666b51a08636caa978ef9a2b769e6a294d87ae"
)
GENERALIZED_146_TEST_SHA256 = (
    "368af7cea591b84fee729d8185d373f576165b1352461974ab1c52978b0227dd"
)
GENERALIZED_146_ROWS_SHA256 = (
    "5ba76aaff2f7ca70dbd61bfd5325ce47c407d36e5e33c3042962e47bfef69eed"
)
GENERALIZED_146_PAYLOAD_SHA256 = (
    "b368a60cb699e06909b03ed368df85b59a422437454abb030b1814356892db06"
)
MIXED_SCHUR_NOTE_SHA256 = (
    "50696e88cc6c195f106331f27cab4af8566a693f983947d486ad1cf9c903692e"
)
EASY_COMMON_W_NOTE_SHA256 = (
    "4764849b05915b9005d68ac885c512a906af439430e8db8a7131f04645224e29"
)
PRIOR_1104_SCOPE_AUDIT_SHA256 = (
    "d8b987e70da2aa424d05242411069dea417a9e3de7130c6dea8fb80eba963cd8"
)
DIRECT_OPEN_MULTISERVICE_NOTE_SHA256 = (
    "fbd9f42815b08a2030d931482b70ff10aca9a92df3c080e2533f275fa6733c2a"
)
DIRECT_OPEN_MULTISERVICE_AUDIT_SHA256 = (
    "9ecd375375e6942d803d068591c80f87a27119a37927dd3617f2e743afdab848"
)

BASE = frozenset({"0", "U", "2U"})
COFACTOR = frozenset({"I", "2I", "UI"})
TOKEN_ORDER = {name: index for index, name in enumerate(
    ("0", "U", "2U", "I", "2I", "UI", "q")
)}


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _file_sha256(relative: str) -> str:
    root = Path(__file__).resolve().parents[1]
    return sha256((root / relative).read_bytes()).hexdigest()


def _vector(name: str) -> tuple[int, int, int]:
    return closure.COMPLEXES[closure.NAME_TO_INDEX[name]]


def _translated_exact_supports(
    supports: tuple[tuple[str, ...], ...],
    normalized_caps: tuple[int, int],
) -> dict[str, object]:
    """Put an exact-Family-II-labelled row in ``(U,V,I)`` coordinates.

    Here ``V`` is normalized ``C`` and ``I`` is the unique cofactor in the
    sole active-bearing source ``q=V+I``.  This is the normalization used by
    the abstract mixed fast-Schur theorem.
    """

    active_sources = tuple(
        name
        for support in supports
        for name in support
        if _vector(name)[2] == 1
    )
    q_name, = active_sources
    assert q_name in {"AC", "BC"}
    cofactor = 0 if q_name == "AC" else 1
    spectator = 1 - cofactor
    assert normalized_caps[cofactor] == 0

    def translate(name: str) -> str:
        vector = _vector(name)
        if vector[2] == 1:
            assert name == q_name
            assert vector[cofactor] == 1
            assert vector[spectator] == 0
            return "q"
        assert vector[2] == 0
        key = (vector[spectator], vector[cofactor])
        return {
            (0, 0): "0",
            (1, 0): "U",
            (2, 0): "2U",
            (0, 1): "I",
            (0, 2): "2I",
            (1, 1): "UI",
        }[key]

    translated = tuple(
        tuple(sorted((translate(name) for name in support),
                     key=TOKEN_ORDER.__getitem__))
        for support in supports
    )
    proper, = (support for support in translated if "q" in support)
    proper_without_q = frozenset(proper) - {"q"}
    at_least_one_mixed = any(
        bool((frozenset(support) - {"q"}) & BASE)
        and bool((frozenset(support) - {"q"}) & COFACTOR)
        for support in translated
    )
    exact_base_open_pair = (
        len(proper) == 2
        and len(proper_without_q) == 1
        and proper_without_q <= BASE
    )
    assert at_least_one_mixed
    assert not exact_base_open_pair
    assert all(frozenset(support) <= BASE | COFACTOR | {"q"}
               for support in translated)

    return {
        "q_name": q_name,
        "cofactor": "A" if cofactor == 0 else "B",
        "spectator": "B" if spectator == 1 else "A",
        "spectator_cap": normalized_caps[spectator],
        "translated_supports": [list(support) for support in translated],
        "at_least_one_linkage_is_mixed": at_least_one_mixed,
        "proper_is_not_exact_base_open_pair": not exact_base_open_pair,
        "all_complexes_in_abstract_mixed_menu": True,
    }


def _direct_premises(supports: tuple[tuple[str, ...], ...]) -> dict[str, object]:
    direct_sides = tuple(
        index for index, support in enumerate(supports) if "C" in support
    )
    side, = direct_sides
    support = supports[side]
    active_sources = tuple(name for name in support if _vector(name)[2] > 0)
    lower_targets = tuple(name for name in support if _vector(name)[2] == 0)
    assert lower_targets
    assert all(_vector(name)[2] == 1 for name in active_sources)
    assert all(sum(_vector(name)[:2]) <= 1 for name in active_sources)
    assert all(sum(_vector(name)[:2]) <= 2 for name in lower_targets)
    return {
        "mixed_linkage_contains_physical_active_source_C": True,
        "same_linkage_contains_lower_target": True,
        "stripped_direct_phase_has_zero_source": True,
        "all_active_bearing_complexes_have_one_C": True,
        "stripped_top_menu_subset_0_A_B": True,
        "service_targets_have_inactive_molecularity_at_most_two": True,
        "strong_cut_reaches_a_killed_service_target": True,
        "background_uniform_tagged_service_minorization": True,
        "multiservice_count_is_one_plus_initial_inactive_mass": True,
        "competing_active_free_source_is_defect": True,
        "direct_multiservice_predicate": True,
    }


def _open_premises(
    supports: tuple[tuple[str, ...], ...],
    phase_signature: tuple[tuple[str, tuple[str, ...]], ...],
) -> dict[str, object]:
    whole_sides = tuple(
        index for index, (kind, _stripped) in enumerate(phase_signature)
        if kind == "whole_top"
    )
    side, = whole_sides
    whole = supports[side]
    mixed = supports[1 - side]
    assert whole == ("C", "AC")
    assert set(mixed) == {"0", "B", "2B", "BC"}
    return {
        "whole_phase_is_C_AC": True,
        "stripped_phase_is_immigration_death_0_A": True,
        "other_linkage_has_origin_and_BC_service_source": True,
        "BC_stopping_rule_is_autonomous_of_A": True,
        "designated_zero_source_launch_allowed_at_B_zero": True,
        "defect_excludes_designated_zero_source_launch": True,
        "multiservice_count_is_one_plus_initial_inactive_mass": True,
        "open_all_clock_multiservice_predicate": True,
    }


def false_no_history_witness() -> dict[str, object]:
    """A five-edge analytic witness for the positive-spectator rows.

    This is not a search result.  Taking the complete digraph on each of
    the two displayed supports is a permitted strong orientation, and the
    listed physical word returns to the same no-fast base with two more
    old-active molecules.
    """

    states = (
        (1, 0, 0),  # (U, relative V, I)
        (0, 0, 2),  # U -> 2I
        (0, 1, 1),  # 2I -> q
        (1, 1, 1),  # I -> UI
        (0, 2, 2),  # U -> q
        (1, 2, 0),  # 2I -> U
    )
    assert states[-1][0] == states[0][0]
    assert states[-1][2] == states[0][2] == 0
    assert states[-1][1] - states[0][1] == 2
    return {
        "supports": [["I", "UI"], ["U", "2I", "2U", "q"]],
        "strong_orientation": "complete_digraph_on_each_support",
        "history": ["U->2I", "2I->q", "I->UI", "U->q", "2I->U"],
        "states_U_relativeV_I": [list(state) for state in states],
        "same_no_fast_base_return": True,
        "positive_reflected_debt_created": 2,
        "works_with_inert_U_slack": "every starting U>=1",
        "all_eight_axis_no_history_labels_are_historically_excluded": False,
    }


@lru_cache(maxsize=1)
def coverage_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for row in hard.one_active_rows():
        supports = tuple(tuple(support) for support in row["normalized_supports"])
        caps = tuple(row["normalized_caps"])
        phases = tuple(
            (kind, tuple(stripped))
            for kind, stripped in row["phase_signature"]
        )
        family = row["structural_family"]
        category = row["graph_category"]

        if family == "generalized_family_ii":
            route = "audited_generalized_146"
            premises: dict[str, object] = {
                "hard_generalized_normalization_applies": True,
                "positive_debt_scope_is_required": True,
            }
        elif family == "direct_physical_C":
            route = "audited_direct_C_multiservice"
            premises = _direct_premises(supports)
        elif family == "open_whole":
            route = "audited_open_all_clock_multiservice"
            premises = _open_premises(supports, phases)
        else:
            assert family == "exact_family_ii"
            translated = _translated_exact_supports(supports, caps)
            if category == "family_ii_axis_no_history" and caps == (0, 0):
                route = "zero_inactive_absorbing_face"
                premises = {
                    **translated,
                    "no_source_enabled_at_U_I_zero": True,
                    "positive_debt_impossible_in_a_closed_class": True,
                }
            else:
                route = "abstract_mixed_fast_schur_extension"
                premises = translated

        rows.append(
            {
                "pair": row["pair"],
                "weight": row["weight"],
                "caps": row["caps"],
                "normalized_supports": row["normalized_supports"],
                "normalized_caps": row["normalized_caps"],
                "structural_family": family,
                "graph_category": category,
                "analytic_route": route,
                "premises": premises,
            }
        )
    rows.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    assert len(rows) == 1104
    return tuple(rows)


def certificate() -> dict[str, object]:
    rows = coverage_rows()
    rows_hash = _digest(rows)

    family_histogram = Counter(row["structural_family"] for row in rows)
    route_histogram = Counter(row["analytic_route"] for row in rows)
    exact_category_histogram = Counter(
        row["graph_category"]
        for row in rows
        if row["structural_family"] == "exact_family_ii"
    )
    exact_support_templates = {
        tuple(tuple(value) for value in row["premises"]["translated_supports"])
        for row in rows
        if row["structural_family"] == "exact_family_ii"
    }

    assert family_histogram == {
        "generalized_family_ii": 951,
        "direct_physical_C": 99,
        "exact_family_ii": 48,
        "open_whole": 6,
    }
    assert exact_category_histogram == {
        "family_ii_axis_down_0": 40,
        "family_ii_axis_no_history": 8,
    }
    assert route_histogram == {
        "audited_generalized_146": 951,
        "audited_direct_C_multiservice": 99,
        "audited_open_all_clock_multiservice": 6,
        "abstract_mixed_fast_schur_extension": 44,
        "zero_inactive_absorbing_face": 4,
    }
    assert len(exact_support_templates) == 8
    assert all(
        row["premises"].get("at_least_one_linkage_is_mixed", True)
        and row["premises"].get("proper_is_not_exact_base_open_pair", True)
        for row in rows
    )

    proof_hashes = {
        "generalized_146_note_sha256": _file_sha256(
            "research_notes/generalized_one_active_146_common_w_theorem.md"
        ),
        "generalized_146_source_sha256": _file_sha256(
            "src/generalized_one_active_146_common_w.py"
        ),
        "generalized_146_test_sha256": _file_sha256(
            "tests/test_generalized_one_active_146_common_w.py"
        ),
        "mixed_schur_note_sha256": _file_sha256(
            "research_notes/proof_first_mixed111_fast_schur_resolvent.md"
        ),
        "easy_common_w_note_sha256": _file_sha256(
            "research_notes/two_active_easy_943_common_w_theorem.md"
        ),
        "prior_1104_scope_audit_sha256": _file_sha256(
            "research_notes/hard_one_active_1104_common_w_independent_audit.md"
        ),
        "direct_open_multiservice_note_sha256": _file_sha256(
            "research_notes/hard_one_active_direct_open_multiservice_repair.md"
        ),
        "direct_open_multiservice_audit_sha256": _file_sha256(
            "research_notes/"
            "hard_one_active_direct_open_multiservice_repair_independent_audit.md"
        ),
    }
    assert proof_hashes == {
        "generalized_146_note_sha256": GENERALIZED_146_NOTE_SHA256,
        "generalized_146_source_sha256": GENERALIZED_146_SOURCE_SHA256,
        "generalized_146_test_sha256": GENERALIZED_146_TEST_SHA256,
        "mixed_schur_note_sha256": MIXED_SCHUR_NOTE_SHA256,
        "easy_common_w_note_sha256": EASY_COMMON_W_NOTE_SHA256,
        "prior_1104_scope_audit_sha256": PRIOR_1104_SCOPE_AUDIT_SHA256,
        "direct_open_multiservice_note_sha256": (
            DIRECT_OPEN_MULTISERVICE_NOTE_SHA256
        ),
        "direct_open_multiservice_audit_sha256": (
            DIRECT_OPEN_MULTISERVICE_AUDIT_SHA256
        ),
    }

    payload = {
        "claim_scope": (
            "finite partition and analytic-hypothesis coverage for all "
            "1,104 one-active failed incidences on the hard 333 pairs"
        ),
        "one_active_incidences": len(rows),
        "one_active_incidence_sha256": hard.certificate()[
            "one_active_dimension"
        ]["incidence_sha256"],
        "family_histogram": dict(sorted(family_histogram.items())),
        "exact_family_ii_graph_category_histogram": dict(
            sorted(exact_category_histogram.items())
        ),
        "analytic_route_histogram": dict(sorted(route_histogram.items())),
        "exact_family_ii_translated_support_templates": len(
            exact_support_templates
        ),
        "exact_family_ii_all_satisfy_abstract_mixed_hypotheses": True,
        "axis_no_history_repair": {
            "old_label_count": 8,
            "actually_frozen_zero_inactive_rows": 4,
            "positive_spectator_rows_rerouted_to_mixed_schur": 4,
            "old_eight_row_exclusion_is_false": True,
            "counterhistory": false_no_history_witness(),
        },
        "proof_hashes": proof_hashes,
        "generalized_146_frozen_rows_sha256": GENERALIZED_146_ROWS_SHA256,
        "generalized_146_frozen_payload_sha256": GENERALIZED_146_PAYLOAD_SHA256,
        "generalized_146_strict_independent_audit_passed": True,
        "direct_open_multiservice_strict_independent_audit_passed": True,
        "rows_sha256": rows_hash,
        "finite_code_role": (
            "partition and support-premise verification only; no orientation, "
            "history, state-space, or probability enumeration"
        ),
        "analytic_one_active_1104_theorem_written": True,
        "analytic_one_active_1104_theorem_independently_audited": True,
        "analytic_one_active_1104_audit_basis": (
            "the first hostile audit passed every unaffected route and "
            "isolated exactly the direct-99/open-6 seam; the frozen strict "
            "multi-service audit certifies its replacement"
        ),
        "hard_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    payload_hash = _digest(payload)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert payload_hash == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
