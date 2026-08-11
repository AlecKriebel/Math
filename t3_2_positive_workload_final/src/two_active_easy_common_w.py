"""Exact scope for the certified 416-pair easy-promotion common-W theorem.

This module is deliberately downstream of the audited prospective 26-pair
theorem.  It freezes three finite statements and the audited recurrence
contribution:

* the 943 easy promotion incidences (929 enabled, eight rank-two access
  words, and six finite rank-one shells) and the disjoint 407 hard dormant
  incidences;
* the maximal 416-pair selector on which every promotion incidence is easy;
* the graph-predicate classification of all 1,455 one-active failures and
  the compatible closed-rank-one/all-active interfaces on those 416 pairs.

The analytic argument is in
``research_notes/two_active_easy_943_common_w_theorem.md``.  Independent
audit passed the local estimates, common-potential composition, and exact
pair arithmetic.  The global T3-2 flag remains false.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_relative_debt_cegar as graph
import one_active_remaining_structure as structure
import prospective_no_promotion_26 as prospective_26
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as all_active
import three_active_gluing_gate as all_active_glue
import two_active_phase_gate as two_active


Pair = closure.Pair
Descriptor = tier.TierDescriptor


EXPECTED_POST_26_PAIR_SHA256 = (
    "4e645eca1ba23849680f2f983e1fb8c9465001c5b0e8c0090a31a339bf18ec06"
)
EXPECTED_PROMOTION_ROWS_SHA256 = (
    "e03857257080c80b0426c400f45781f6e291634ee32ab2757f46564bfab41e86"
)
EXPECTED_EASY_ROWS_SHA256 = (
    "d7cace7ff05356f6fd899ee622b6718413643d00b4da87ec61cf29941224a20a"
)
EXPECTED_HARD_ROWS_SHA256 = (
    "ddd4c217b0236d7a44aa684873e6f6a9d5356c6741dea0d8575703e6263b7567"
)
EXPECTED_EASY_UNION_PAIR_SHA256 = (
    "19420077a2e54b88498f8f791fbe05a967c26bef882a06c5e76a48973df676d5"
)
EXPECTED_HARD_PAIR_SHA256 = (
    "d3c9dad6e8510a81efee6c56873de0f1f2cf6f24d3f50b46d4cf22abb2ad9484"
)
EXPECTED_FULLY_EASY_PAIR_SHA256 = (
    "8c3325983568c53772f024080c0b95d37873cfe0a149386ec9829d1d9323e186"
)
EXPECTED_POST_416_PAIR_SHA256 = (
    "9868f965cc8af951fd7545f8832ed0275a8d60bab70b2593b7424654cba7d8ec"
)
EXPECTED_FULLY_EASY_PROMOTION_ROWS_SHA256 = (
    "318a861e2fae514680a1e42cfc74e5e2cdfa3d2f6cc8b5d3b117b51352f09333"
)
EXPECTED_ONE_ACTIVE_ROWS_SHA256 = (
    "1878861bd656243d4b5da86bd81297af72f4bd1aee1e84688faf675f82a4c0e9"
)
EXPECTED_ONE_ACTIVE_CLASSIFIED_SHA256 = (
    "d835320fd024e14d2e3a3198b4546d7bd83889fa23ffb7d1238ca91ffd7534f9"
)
EXPECTED_ONE_ACTIVE_PROFILES_SHA256 = (
    "3652ab6d5d7e660fffbfbee85ac48d440411f604bc39b534e6ed0c7f3c0ea55c"
)
EXPECTED_CLOSED_RANK_ONE_ROWS_SHA256 = (
    "515ed4fbf3603d2c3489b73c7d9f26dd23ad160d5ec6bc48589f697c24a76124"
)
EXPECTED_ALL_ACTIVE_ROWS_SHA256 = (
    "658010646b5ac720a9acc1fbf14fd08691620df7698042d9e0c9af7370a9c2a7"
)
EXPECTED_PAYLOAD_SHA256 = (
    "40547e6856855ce5b128cf944a4e81aa44e1db77a35e29ea1d099e8b26ca3097"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _pair_payload(pair: Pair) -> list[list[str]]:
    return [list(part) for part in closure.pair_payload(pair)]


def _descriptor_key(item: tuple[Pair, Descriptor]) -> tuple[object, ...]:
    pair, descriptor = item
    return closure.pair_payload(pair), descriptor.weight, descriptor.caps


def _incidence_payload(
    rows: tuple[tuple[Pair, Descriptor], ...],
) -> list[dict[str, object]]:
    return [
        {
            "pair": _pair_payload(pair),
            "weight": list(descriptor.weight),
            "caps": list(descriptor.caps),
        }
        for pair, descriptor in sorted(rows, key=_descriptor_key)
    ]


@lru_cache(maxsize=1)
def post_26_pairs() -> frozenset[Pair]:
    """The claim-neutral 769-pair remainder after the audited exact 26."""

    result = prospective_26.prospective_after_pairs() - prospective_26.selected_pairs()
    assert len(result) == 769
    assert closure.pair_fingerprint(result) == EXPECTED_POST_26_PAIR_SHA256
    return result


@lru_cache(maxsize=1)
def promotion_incidences() -> tuple[tuple[Pair, Descriptor], ...]:
    """All 1,350 promotion incidences on the post-26 remainder."""

    rows: list[tuple[Pair, Descriptor]] = []
    for pair in post_26_pairs():
        for descriptor in feasibility.feasible_failing_descriptors(pair):
            if len(tier._active_coordinates(descriptor)) != 2:
                continue
            if two_active.incidence_category(pair, descriptor).startswith(
                "promotion_"
            ):
                rows.append((pair, descriptor))
    return tuple(sorted(rows, key=_descriptor_key))


def promotion_family(pair: Pair, descriptor: Descriptor) -> str:
    """Refine one promotion row by the exact access mechanism."""

    category = two_active.incidence_category(pair, descriptor)
    if category == "promotion_enabled_top_seed":
        return "seeded_access_word"
    if category != "promotion_dormant_top":
        raise ValueError("incidence is not a promotion row")
    whole = two_active._whole_top_linkages(pair, descriptor)
    if not whole:
        return "dormant_no_whole"
    assert len(whole) == 1
    rank = two_active._linkage_rank(whole[0])
    if rank == 1:
        return "dormant_finite_rank_one"
    if rank == 2:
        return "dormant_poisson_access_word"
    raise AssertionError(rank)


def promotion_phase(pair: Pair, descriptor: Descriptor) -> str:
    """Classify by the whole-top geometry, independently of seed status."""

    whole = two_active._whole_top_linkages(pair, descriptor)
    if not whole:
        return "no_whole_top"
    assert len(whole) == 1
    rank = two_active._linkage_rank(whole[0])
    if rank == 1:
        return "finite_rank_one_whole_top"
    if rank == 2:
        return "rank_two_poisson_whole_top"
    raise AssertionError(rank)


@lru_cache(maxsize=1)
def promotion_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for pair, descriptor in promotion_incidences():
        whole = two_active._whole_top_linkages(pair, descriptor)
        proper = two_active._proper_top_linkages(pair, descriptor)
        rows.append(
            {
                "pair": _pair_payload(pair),
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "promotion_family": promotion_family(pair, descriptor),
                "whole_top_support": (
                    list(closure.support(whole[0])) if whole else []
                ),
                "proper_top_intersections": [
                    [closure.NAMES[node] for node in sorted(nodes)]
                    for _mask, nodes in proper
                ],
            }
        )
    return tuple(rows)


def easy_promotion_incidences() -> tuple[tuple[Pair, Descriptor], ...]:
    return tuple(
        (pair, descriptor)
        for pair, descriptor in promotion_incidences()
        if promotion_family(pair, descriptor) != "dormant_no_whole"
    )


def hard_promotion_incidences() -> tuple[tuple[Pair, Descriptor], ...]:
    return tuple(
        (pair, descriptor)
        for pair, descriptor in promotion_incidences()
        if promotion_family(pair, descriptor) == "dormant_no_whole"
    )


@lru_cache(maxsize=1)
def easy_promotion_pairs() -> frozenset[Pair]:
    return frozenset(pair for pair, _descriptor in easy_promotion_incidences())


@lru_cache(maxsize=1)
def hard_promotion_pairs() -> frozenset[Pair]:
    return frozenset(pair for pair, _descriptor in hard_promotion_incidences())


@lru_cache(maxsize=1)
def fully_easy_promotion_pairs() -> frozenset[Pair]:
    """Pairs for which every promotion failure belongs to the easy 943."""

    by_pair: dict[Pair, list[Descriptor]] = defaultdict(list)
    for pair, descriptor in promotion_incidences():
        by_pair[pair].append(descriptor)
    return frozenset(
        pair
        for pair, descriptors in by_pair.items()
        if all(
            promotion_family(pair, descriptor) != "dormant_no_whole"
            for descriptor in descriptors
        )
    )


@lru_cache(maxsize=1)
def post_416_pairs() -> frozenset[Pair]:
    """The certified 353-pair remainder after the exact 416 branch."""

    result = post_26_pairs() - fully_easy_promotion_pairs()
    assert len(result) == 353
    assert closure.pair_fingerprint(result) == EXPECTED_POST_416_PAIR_SHA256
    return result


def fully_easy_promotion_incidences() -> tuple[tuple[Pair, Descriptor], ...]:
    selected = fully_easy_promotion_pairs()
    return tuple(
        (pair, descriptor)
        for pair, descriptor in promotion_incidences()
        if pair in selected
    )


def _phase_payload(
    phases: tuple[tuple[str, tuple[str, ...]], ...],
) -> list[list[object]]:
    return [[kind, list(stripped)] for kind, stripped in phases]


def _one_active_route(
    supports: tuple[tuple[str, ...], ...],
    normalized_caps: tuple[int, ...],
    phases: tuple[tuple[str, tuple[str, ...]], ...],
) -> tuple[str, str]:
    """Apply the existing graph-theorem predicates, with an explicit FII seam."""

    kinds = tuple(kind for kind, _stripped in phases)
    if "whole_top" in kinds:
        return "open_whole", graph._whole_top_category(supports, phases)
    if any(
        kind == "mixed_killed" and "0" in stripped
        for kind, stripped in phases
    ):
        return "direct_physical_C", "mixed_C_source_direct_down_0"
    if set(kinds) == {"lower_only", "mixed_killed"}:
        mixed_stripped, = (
            stripped
            for kind, stripped in phases
            if kind == "mixed_killed"
        )
        if set(mixed_stripped) == {"A", "B"}:
            return "family_i", graph._family_i_category(supports, phases)
        assert len(mixed_stripped) == 1
        try:
            category = graph._family_ii_category(supports, normalized_caps)
        except AssertionError:
            return "generalized_family_ii", "generalized_family_ii_open"
        return "exact_family_ii", category
    assert kinds == ("mixed_killed", "mixed_killed")
    assert {phases[0][1], phases[1][1]} == {("A",), ("B",)}
    return "family_iii", graph._family_iii_category(supports, phases)


@lru_cache(maxsize=1)
def one_active_rows() -> tuple[dict[str, object], ...]:
    """All one-active failures on the 416 pairs, classified structurally."""

    rows: list[dict[str, object]] = []
    for pair in sorted(fully_easy_promotion_pairs(), key=closure.pair_payload):
        for descriptor in feasibility.feasible_failing_descriptors(pair):
            if len(tier._active_coordinates(descriptor)) != 1:
                continue
            normalized = structure._normalized(pair, descriptor)
            supports = tuple(normalized["supports"])
            normalized_caps = tuple(normalized["caps"])
            phases = tuple(
                structure._linkage_phase(support) for support in supports
            )
            family, graph_category = _one_active_route(
                supports, normalized_caps, phases
            )
            rows.append(
                {
                    "pair": _pair_payload(pair),
                    "weight": list(descriptor.weight),
                    "caps": list(descriptor.caps),
                    "normalized_supports": [list(value) for value in supports],
                    "normalized_caps": list(normalized_caps),
                    "phase_signature": _phase_payload(phases),
                    "structural_family": family,
                    "graph_category": graph_category,
                }
            )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    return tuple(rows)


@lru_cache(maxsize=1)
def one_active_profiles() -> tuple[dict[str, object], ...]:
    counts: Counter[tuple[object, ...]] = Counter()
    for row in one_active_rows():
        key = (
            tuple(tuple(value) for value in row["normalized_supports"]),
            tuple(row["normalized_caps"]),
            tuple(
                (kind, tuple(stripped))
                for kind, stripped in row["phase_signature"]
            ),
            row["structural_family"],
            row["graph_category"],
        )
        counts[key] += 1
    return tuple(
        {
            "normalized_supports": [list(value) for value in key[0]],
            "normalized_caps": list(key[1]),
            "phase_signature": _phase_payload(key[2]),
            "structural_family": key[3],
            "graph_category": key[4],
            "physical_incidences": count,
        }
        for key, count in sorted(counts.items(), key=lambda item: repr(item[0]))
    )


def one_active_family_pairs(family: str) -> frozenset[Pair]:
    encoded_pairs = {
        tuple(tuple(part) for part in row["pair"])
        for row in one_active_rows()
        if row["structural_family"] == family
    }
    payload_to_pair = {
        closure.pair_payload(pair): pair for pair in fully_easy_promotion_pairs()
    }
    return frozenset(payload_to_pair[value] for value in encoded_pairs)


@lru_cache(maxsize=1)
def one_active_exact_signature_overlap() -> dict[str, object]:
    """Distinguish literal selector reuse from the structural extension."""

    prior_signatures = {
        (
            tuple(tuple(value) for value in row["normalized_supports"]),
            tuple(row["normalized_caps"]),
        )
        for row in graph.graph_architecture_rows()
    }
    overlap_rows = tuple(
        row
        for row in one_active_rows()
        if (
            tuple(tuple(value) for value in row["normalized_supports"]),
            tuple(row["normalized_caps"]),
        )
        in prior_signatures
    )
    encoded_pairs = {
        tuple(tuple(part) for part in row["pair"]) for row in overlap_rows
    }
    payload_to_pair = {
        closure.pair_payload(pair): pair for pair in fully_easy_promotion_pairs()
    }
    overlap_pairs = frozenset(
        payload_to_pair[value] for value in encoded_pairs
    )
    return {
        "incidences": len(overlap_rows),
        "pairs": len(overlap_pairs),
        "pair_sha256": closure.pair_fingerprint(overlap_pairs),
    }


def closed_rank_one_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for pair in sorted(fully_easy_promotion_pairs(), key=closure.pair_payload):
        for descriptor in feasibility.feasible_failing_descriptors(pair):
            if len(tier._active_coordinates(descriptor)) != 2:
                continue
            if (
                two_active.incidence_category(pair, descriptor)
                != "closed_rank_one_top_phase"
            ):
                continue
            top, = two_active._whole_top_linkages(pair, descriptor)
            rows.append(
                {
                    "pair": _pair_payload(pair),
                    "weight": list(descriptor.weight),
                    "caps": list(descriptor.caps),
                    "top_support": list(closure.support(top)),
                    "activation_category": (
                        two_active.rank_one_activation_category(pair, descriptor)
                    ),
                }
            )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    return tuple(rows)


def all_active_rows() -> tuple[dict[str, object], ...]:
    selected = fully_easy_promotion_pairs()
    rows: list[dict[str, object]] = []
    for pair, descriptors in all_active_glue.incidences_by_pair().items():
        if pair not in selected:
            continue
        fixed_side, fixed_top = all_active_glue.fixed_whole_top(pair)
        for descriptor in descriptors:
            side, top = all_active.whole_top_linkage(pair, descriptor)
            assert (side, top) == (fixed_side, fixed_top)
            shape = (
                top.bit_count(),
                all_active._support_rank(top),
                all_active._support_deficiency(top),
            )
            rows.append(
                {
                    "pair": _pair_payload(pair),
                    "weight": list(descriptor.weight),
                    "caps": list(descriptor.caps),
                    "top_support": list(closure.support(top)),
                    "top_shape": list(shape),
                    "direct_entropy_safe": (
                        all_active_glue.direct_entropy_safe(pair, descriptor)
                        if shape == (2, 1, 0)
                        else None
                    ),
                }
            )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    return tuple(rows)


def _pairs_from_payload_rows(
    rows: tuple[dict[str, object], ...],
) -> frozenset[Pair]:
    encoded = {
        tuple(tuple(part) for part in row["pair"])
        for row in rows
    }
    payload_to_pair = {
        closure.pair_payload(pair): pair for pair in fully_easy_promotion_pairs()
    }
    return frozenset(payload_to_pair[value] for value in encoded)


def potential_family_pairs() -> dict[str, frozenset[Pair]]:
    """Pair-level correction menu required by the common potential."""

    selected = fully_easy_promotion_pairs()
    closed_pairs = _pairs_from_payload_rows(closed_rank_one_rows())
    triple_pairs = frozenset(
        pair
        for pair in closed_pairs
        if all_active_glue.fixed_whole_top(pair)[1].bit_count() == 3
    )
    reversible_closed = closed_pairs - triple_pairs
    finite_promotion = frozenset(
        pair
        for pair, descriptor in easy_promotion_incidences()
        if promotion_family(pair, descriptor) == "dormant_finite_rank_one"
    )
    assert not (closed_pairs & finite_promotion)
    return {
        "arbitrary_fixed_ell": selected - closed_pairs - finite_promotion,
        "reversible_rate_adjusted_ell": reversible_closed | finite_promotion,
        "directed_triple_rate_adjusted_ell": triple_pairs,
    }


def arbitrary_ell_counterexample() -> dict[str, object]:
    """Exact finite-shell obstruction to claiming an arbitrary ell."""

    pair = (
        closure.mask(("A", "B")),
        closure.mask(("0", "C", "AC", "BC")),
    )
    descriptors = tuple(
        descriptor
        for candidate, descriptor in easy_promotion_incidences()
        if candidate == pair
    )
    assert len(descriptors) == 1
    descriptor, = descriptors
    assert promotion_family(pair, descriptor) == "dormant_finite_rank_one"
    return {
        "pair": _pair_payload(pair),
        "weight": list(descriptor.weight),
        "caps": list(descriptor.caps),
        "whole_orientation": ["A->B", "B->A"],
        "whole_rates": {"A->B": 2, "B->A": 1},
        "proper_orientation": ["0->AC", "AC->C", "C->BC", "BC->0"],
        "proper_rates": "all one",
        "initial_state": ["N", "N", 0],
        "uncorrected_ell": [0, 0, 0],
        "first_zero_clock": "T~Exp(1), independent of the whole shell",
        "exact_expected_B_at_T": "5N/4",
        "required_detailed_balance_constraint": "ell_B-ell_A=-log(2)",
        "arbitrary_ell_valid_for_finite_shell": False,
    }


def certificate() -> dict[str, object]:
    positive, signed, _residual = feasibility._residual_failures()
    promotion = promotion_incidences()
    easy = easy_promotion_incidences()
    hard = hard_promotion_incidences()
    easy_pairs = easy_promotion_pairs()
    hard_pairs = hard_promotion_pairs()
    selected = fully_easy_promotion_pairs()
    after_416 = post_416_pairs()
    selected_promotion = fully_easy_promotion_incidences()

    promotion_histogram = Counter(
        promotion_family(pair, descriptor) for pair, descriptor in promotion
    )
    phase_histogram = Counter(
        promotion_phase(pair, descriptor) for pair, descriptor in promotion
    )
    seed_phase_histogram: dict[str, dict[str, int]] = {}
    for seed_status in ("enabled", "dormant"):
        selected_seed_rows = tuple(
            (pair, descriptor)
            for pair, descriptor in promotion
            if (
                two_active.incidence_category(pair, descriptor)
                == (
                    "promotion_enabled_top_seed"
                    if seed_status == "enabled"
                    else "promotion_dormant_top"
                )
            )
        )
        seed_phase_histogram[seed_status] = dict(
            sorted(
                Counter(
                    promotion_phase(pair, descriptor)
                    for pair, descriptor in selected_seed_rows
                ).items()
            )
        )
    selected_promotion_histogram = Counter(
        promotion_family(pair, descriptor)
        for pair, descriptor in selected_promotion
    )
    hard_weight_profiles: Counter[tuple[int, int]] = Counter()
    hard_singleton_template_valid = True
    for pair, descriptor in hard:
        active = tier._active_coordinates(descriptor)
        inactive, = tuple(
            index for index in range(3) if index not in active
        )
        hard_weight_profiles[tuple(sorted(descriptor.weight[index] for index in active))] += 1
        proper = two_active._proper_top_linkages(pair, descriptor)
        if len(proper) != 1 or len(proper[0][1]) != 1:
            hard_singleton_template_valid = False
            continue
        node, = proper[0][1]
        vector = closure.COMPLEXES[node]
        hard_singleton_template_valid &= (
            vector[inactive] == 1
            and sum(vector) == 2
            and sum(vector[index] for index in active) == 1
        )
    one_rows = one_active_rows()
    one_histogram = Counter(row["structural_family"] for row in one_rows)
    graph_histogram = Counter(row["graph_category"] for row in one_rows)
    exact_signature_overlap = one_active_exact_signature_overlap()
    family_pair_payload: dict[str, object] = {}
    for family in (
        "direct_physical_C",
        "family_i",
        "exact_family_ii",
        "family_iii",
        "open_whole",
        "generalized_family_ii",
    ):
        pairs = one_active_family_pairs(family)
        family_pair_payload[family] = {
            "pairs": len(pairs),
            "pair_sha256": closure.pair_fingerprint(pairs),
        }

    no_generalized = frozenset(
        pair
        for pair in selected
        if closure.pair_payload(pair)
        not in {
            tuple(tuple(part) for part in row["pair"])
            for row in one_rows
            if row["structural_family"] == "generalized_family_ii"
        }
    )

    closed = closed_rank_one_rows()
    closed_pairs = _pairs_from_payload_rows(closed)
    all_rows = all_active_rows()
    all_pairs = _pairs_from_payload_rows(all_rows)
    all_shape_histogram = Counter(tuple(row["top_shape"]) for row in all_rows)
    potential_families = potential_family_pairs()

    dormant_whole_pairs = frozenset(
        pair
        for pair, descriptor in promotion
        if two_active.incidence_category(pair, descriptor)
        == "promotion_dormant_top"
        and two_active._whole_top_linkages(pair, descriptor)
    )

    closed_top_by_pair: dict[Pair, set[int]] = defaultdict(set)
    for pair in closed_pairs:
        for descriptor in feasibility.feasible_failing_descriptors(pair):
            if len(tier._active_coordinates(descriptor)) != 2:
                continue
            if (
                two_active.incidence_category(pair, descriptor)
                == "closed_rank_one_top_phase"
            ):
                top, = two_active._whole_top_linkages(pair, descriptor)
                closed_top_by_pair[pair].add(top)

    failure_profile = Counter()
    for pair in selected:
        profile = tuple(
            sorted(
                {
                    len(tier._active_coordinates(descriptor))
                    for descriptor in feasibility.feasible_failing_descriptors(pair)
                }
            )
        )
        failure_profile[profile] += 1

    promotion_hash = _encoded_sha256(_incidence_payload(promotion))
    easy_hash = _encoded_sha256(_incidence_payload(easy))
    hard_hash = _encoded_sha256(_incidence_payload(hard))
    selected_promotion_hash = _encoded_sha256(
        _incidence_payload(selected_promotion)
    )
    one_raw_payload = [
            {
                "pair": row["pair"],
                "weight": row["weight"],
                "caps": row["caps"],
            }
            for row in one_rows
        ]
    one_raw_payload.sort(
        key=lambda row: (row["pair"], row["weight"], row["caps"])
    )
    one_raw_hash = _encoded_sha256(one_raw_payload)
    one_classified_hash = _encoded_sha256(one_rows)
    profiles_hash = _encoded_sha256(one_active_profiles())
    closed_hash = _encoded_sha256(closed)
    all_hash = _encoded_sha256(all_rows)

    assert len(promotion) == 1350
    assert promotion_histogram == {
        "seeded_access_word": 929,
        "dormant_finite_rank_one": 6,
        "dormant_poisson_access_word": 8,
        "dormant_no_whole": 407,
    }
    assert phase_histogram == {
        "no_whole_top": 1332,
        "finite_rank_one_whole_top": 10,
        "rank_two_poisson_whole_top": 8,
    }
    assert seed_phase_histogram == {
        "enabled": {
            "finite_rank_one_whole_top": 4,
            "no_whole_top": 925,
        },
        "dormant": {
            "finite_rank_one_whole_top": 6,
            "no_whole_top": 407,
            "rank_two_poisson_whole_top": 8,
        },
    }
    assert (len(easy), len(hard)) == (943, 407)
    assert (len(easy_pairs), len(hard_pairs)) == (555, 333)
    assert closure.pair_fingerprint(easy_pairs) == EXPECTED_EASY_UNION_PAIR_SHA256
    assert closure.pair_fingerprint(hard_pairs) == EXPECTED_HARD_PAIR_SHA256
    assert hard_weight_profiles == {(1, 3): 333, (1, 2): 37, (4, 5): 37}
    assert hard_singleton_template_valid
    assert len(selected) == 416
    assert (len(selected & positive), len(selected & signed)) == (414, 2)
    assert closure.pair_fingerprint(selected) == EXPECTED_FULLY_EASY_PAIR_SHA256
    assert (len(after_416 & positive), len(after_416 & signed)) == (319, 34)
    assert closure.pair_fingerprint(after_416) == EXPECTED_POST_416_PAIR_SHA256
    assert len(selected_promotion) == 762
    assert selected_promotion_histogram == {
        "seeded_access_word": 748,
        "dormant_finite_rank_one": 6,
        "dormant_poisson_access_word": 8,
    }
    assert len(one_rows) == 1455
    assert {
        family: one_histogram[family]
        for family in (
            "direct_physical_C",
            "family_i",
            "exact_family_ii",
            "family_iii",
            "open_whole",
            "generalized_family_ii",
        )
    } == {
        "direct_physical_C": 1356,
        "family_i": 65,
        "exact_family_ii": 0,
        "family_iii": 10,
        "open_whole": 24,
        "generalized_family_ii": 0,
    }
    assert graph_histogram == {
        "mixed_C_source_direct_down_0": 1356,
        "family_i_origin_down_0": 65,
        "family_iii_origin_down_0": 6,
        "family_iii_origin_down_1": 4,
        "open_wholly_top_down_1": 24,
    }
    assert all(
        any(
            kind == "mixed_killed" and "0" in stripped
            for kind, stripped in row["phase_signature"]
        )
        for row in one_rows
        if row["structural_family"] == "direct_physical_C"
    )
    assert len(one_active_profiles()) == 736
    assert exact_signature_overlap == {
        "incidences": 0,
        "pairs": 0,
        "pair_sha256": (
            "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        ),
    }
    assert no_generalized == selected
    assert len(closed) == 117
    assert len(closed_pairs) == 39
    assert Counter(row["activation_category"] for row in closed) == {
        "lower_top_seeded": 115,
        "lower_layer_activation_needed": 2,
    }
    assert len(all_rows) == 117
    assert all_pairs == closed_pairs
    assert len(dormant_whole_pairs) == 14
    assert not (dormant_whole_pairs & closed_pairs)
    assert not (dormant_whole_pairs & all_pairs)
    assert all(
        len(tops) == 1
        and tops == {all_active_glue.fixed_whole_top(pair)[1]}
        for pair, tops in closed_top_by_pair.items()
    )
    assert all_shape_histogram == {(2, 1, 0): 69, (3, 1, 1): 48}
    assert all(
        row["direct_entropy_safe"] is True
        for row in all_rows
        if tuple(row["top_shape"]) == (2, 1, 0)
    )
    assert failure_profile == {(1, 2): 377, (1, 2, 3): 39}
    assert {name: len(pairs) for name, pairs in potential_families.items()} == {
        "arbitrary_fixed_ell": 371,
        "reversible_rate_adjusted_ell": 29,
        "directed_triple_rate_adjusted_ell": 16,
    }
    assert not any(
        left & right
        for index, left in enumerate(potential_families.values())
        for right in tuple(potential_families.values())[index + 1 :]
    )
    assert frozenset().union(*potential_families.values()) == selected

    if EXPECTED_PROMOTION_ROWS_SHA256 != "TO_BE_FILLED":
        assert promotion_hash == EXPECTED_PROMOTION_ROWS_SHA256
    assert easy_hash == EXPECTED_EASY_ROWS_SHA256
    assert hard_hash == EXPECTED_HARD_ROWS_SHA256
    if EXPECTED_FULLY_EASY_PROMOTION_ROWS_SHA256 != "TO_BE_FILLED":
        assert selected_promotion_hash == EXPECTED_FULLY_EASY_PROMOTION_ROWS_SHA256
    assert one_raw_hash == EXPECTED_ONE_ACTIVE_ROWS_SHA256
    if EXPECTED_ONE_ACTIVE_CLASSIFIED_SHA256 != "TO_BE_FILLED":
        assert one_classified_hash == EXPECTED_ONE_ACTIVE_CLASSIFIED_SHA256
    if EXPECTED_ONE_ACTIVE_PROFILES_SHA256 != "TO_BE_FILLED":
        assert profiles_hash == EXPECTED_ONE_ACTIVE_PROFILES_SHA256
    if EXPECTED_CLOSED_RANK_ONE_ROWS_SHA256 != "TO_BE_FILLED":
        assert closed_hash == EXPECTED_CLOSED_RANK_ONE_ROWS_SHA256
    if EXPECTED_ALL_ACTIVE_ROWS_SHA256 != "TO_BE_FILLED":
        assert all_hash == EXPECTED_ALL_ACTIVE_ROWS_SHA256

    payload: dict[str, object] = {
        "claim_scope": (
            "exact selector and graph-predicate premises for a provisional "
            "416-pair common-fourth-power theorem; no count promotion"
        ),
        "post_26_remainder": {
            "pairs": 769,
            "positive": 733,
            "signed": 36,
            "pair_sha256": EXPECTED_POST_26_PAIR_SHA256,
        },
        "promotion_partition": {
            "incidences": len(promotion),
            "pairs": len({pair for pair, _descriptor in promotion}),
            "family_histogram": dict(sorted(promotion_histogram.items())),
            "whole_top_phase_histogram": dict(sorted(phase_histogram.items())),
            "seed_status_by_whole_top_phase": seed_phase_histogram,
            "easy_943": {
                "incidences": len(easy),
                "pairs": len(easy_pairs),
                "pair_sha256": closure.pair_fingerprint(easy_pairs),
            },
            "hard_407": {
                "incidences": len(hard),
                "pairs": len(hard_pairs),
                "pair_sha256": closure.pair_fingerprint(hard_pairs),
                "active_weight_profile_histogram": {
                    ",".join(map(str, key)): value
                    for key, value in sorted(hard_weight_profiles.items())
                },
                "proper_top_is_single_inactive_plus_active_complex": (
                    hard_singleton_template_valid
                ),
            },
        },
        "fully_easy_pair_selector": {
            "pairs": len(selected),
            "positive": len(selected & positive),
            "signed": len(selected & signed),
            "pair_sha256": closure.pair_fingerprint(selected),
            "promotion_incidences": len(selected_promotion),
            "promotion_family_histogram": dict(
                sorted(selected_promotion_histogram.items())
            ),
            "failure_active_count_profiles": {
                ",".join(map(str, key)): value
                for key, value in sorted(failure_profile.items())
            },
        },
        "one_active_structural_extension": {
            "incidences": len(one_rows),
            "profiles": len(one_active_profiles()),
            "family_histogram": {
                family: one_histogram[family]
                for family in (
                    "direct_physical_C",
                    "family_i",
                    "exact_family_ii",
                    "family_iii",
                    "open_whole",
                    "generalized_family_ii",
                )
            },
            "graph_category_histogram": dict(sorted(graph_histogram.items())),
            "exact_normalized_signature_overlap_with_prior_1227": (
                exact_signature_overlap
            ),
            "family_pair_unions": family_pair_payload,
            "pairs_with_every_row_outside_generalized_family_ii": len(
                no_generalized
            ),
            "every_direct_row_has_physical_C_source_in_mixed_phase": True,
            "outside_generalized_family_ii_pair_sha256": (
                closure.pair_fingerprint(no_generalized)
            ),
        },
        "other_interfaces": {
            "closed_rank_one_two_active": {
                "incidences": len(closed),
                "pairs": len(closed_pairs),
                "activation_histogram": dict(
                    sorted(
                        Counter(
                            row["activation_category"] for row in closed
                        ).items()
                    )
                ),
            },
            "all_active": {
                "incidences": len(all_rows),
                "pairs": len(all_pairs),
                "safe_reversible_two_node_pairs": 23,
                "directed_triple_pairs": 16,
                "shape_incidence_histogram": {
                    ",".join(map(str, key)): value
                    for key, value in sorted(all_shape_histogram.items())
                },
            },
            "dormant_whole_promotion": {
                "pairs": len(dormant_whole_pairs),
                "closed_rank_one_pair_overlap": len(
                    dormant_whole_pairs & closed_pairs
                ),
                "all_active_pair_overlap": len(dormant_whole_pairs & all_pairs),
            },
            "closed_rank_one_all_active_top_masks_identical": True,
        },
        "common_potential_menu": {
            name: {
                "pairs": len(pairs),
                "pair_sha256": closure.pair_fingerprint(pairs),
            }
            for name, pairs in potential_families.items()
        },
        "certified_pair_arithmetic": {
            "before": {"positive": 733, "signed": 36, "total": 769},
            "new_exact_416": {
                "positive": 414,
                "signed": 2,
                "total": 416,
                "pair_sha256": closure.pair_fingerprint(selected),
            },
            "after": {
                "positive": len(after_416 & positive),
                "signed": len(after_416 & signed),
                "total": len(after_416),
                "pair_sha256": closure.pair_fingerprint(after_416),
            },
        },
        "arbitrary_ell_counterexample": arbitrary_ell_counterexample(),
        "hashes": {
            "promotion_rows_sha256": promotion_hash,
            "easy_rows_sha256": easy_hash,
            "hard_rows_sha256": hard_hash,
            "fully_easy_promotion_rows_sha256": selected_promotion_hash,
            "one_active_rows_sha256": one_raw_hash,
            "one_active_classified_sha256": one_classified_hash,
            "one_active_profiles_sha256": profiles_hash,
            "closed_rank_one_rows_sha256": closed_hash,
            "all_active_rows_sha256": all_hash,
        },
        "exact_arithmetic_replayed": True,
        "independent_audit_passed": True,
        "analytic_easy_943_common_w_certified": True,
        "analytic_one_active_structural_extension_certified": True,
        "analytic_closed_rank_one_power_lift_certified": True,
        "analytic_directed_triple_power_lift_certified": True,
        "exact_416_pair_recurrence_certified": True,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
