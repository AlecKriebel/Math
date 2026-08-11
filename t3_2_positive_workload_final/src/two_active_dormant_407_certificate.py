"""Exact selector and proof-premise audit for the unified hard interface.

The analytic candidate theorem is written in
``research_notes/two_active_dormant_407_resolvent_theorem.md``.  This
module does not infer recurrence from finite enumeration.  It freezes the
exact 407 dormant two-active incidence set, normalizes its three species as

``U`` = lower-weight active species,
``V`` = higher-weight active species, and
``I`` = inactive species,

and verifies the support alternatives used by the arbitrary-orientation
cut proof.  It also freezes all 1,104 one-active failures on the same 333
pairs and the exact 951-to-317 generalized-Family-II promotion map.  The
map is a support identity, not a finite-state recurrence inference.
Independent audit found that the candidate's uniform unweighted Green bound
is false for unbounded spectator starts. The exact finite selector remains
valid, but the analytic theorem requires a start-weighted repair. Pair-level
and global certification remain false.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_relative_debt_cegar as one_active_graph
import one_active_remaining_structure as one_active_structure
import prospective_no_promotion_26 as prospective
import stoichiometric_gate_feasibility as feasibility
import two_active_phase_gate as phase


Pair = closure.Pair
Descriptor = tier.TierDescriptor


EXPECTED_INCIDENCE_SHA256 = (
    "ddd4c217b0236d7a44aa684873e6f6a9d5356c6741dea0d8575703e6263b7567"
)
EXPECTED_PAIR_SHA256 = (
    "d3c9dad6e8510a81efee6c56873de0f1f2cf6f24d3f50b46d4cf22abb2ad9484"
)
EXPECTED_NORMALIZED_ROW_SHA256 = (
    "dc15a6144dc604ef2e44e3b2da148281ce9a4f7dfc48f65818781cbf25373d04"
)
EXPECTED_NORMALIZED_TEMPLATE_SHA256 = (
    "fc0f8e9ced3824c5a6f8172e1f74775c61f1d001042a66c443ca8bae38611bcc"
)
EXPECTED_EXCEPTIONAL_PAIR_SHA256 = (
    "7fcbd17c5571534a7e1bd50d218cfc56389c73a136c2fe0a73d3478ac2cf14fb"
)
EXPECTED_ONE_ACTIVE_INCIDENCE_SHA256 = (
    "a594c1f98a890ef17c255d90e765d655d45721c8dcf036be99651ea362a301fb"
)
EXPECTED_ONE_ACTIVE_CLASSIFIED_SHA256 = (
    "ada26d0a37444e135bcab62dc97d9df116f0dec9c06f6bfd63c3244294b6dd0e"
)
EXPECTED_ONE_ACTIVE_PROFILE_SHA256 = (
    "7b467db2167ac27b0420d6a1c8bba914fea0ff2379494a8f78bfd8fe1341584b"
)
EXPECTED_GENERALIZED_ONE_ACTIVE_INCIDENCE_SHA256 = (
    "8af9ed6aa8ba1661bacfe1390778b5677ee8d67cf1a606e042e5329e6ee86496"
)
EXPECTED_GENERALIZED_PAIR_SHA256 = (
    "0c8291a398cc981002c2164b643fbf75e1d107252beb9133fc3b4ad3af229c4a"
)
EXPECTED_GENERALIZED_NORMALIZED_ROW_SHA256 = (
    "725b014b571202c2970b333f865eee0762e83ce7a6d797d94f11f8f176536771"
)
EXPECTED_GENERALIZED_SUPPORT_TEMPLATE_SHA256 = (
    "c2af132164aa2159478594a60378261d4d3956bbea1a61453b283995d27d2715"
)
EXPECTED_GENERALIZED_SUPPORT_CAP_TEMPLATE_SHA256 = (
    "e16ecfc8c8f6300e21c5b58bfa813590c0c044eb5ced2eed85b1c3ff02e0cd49"
)
EXPECTED_PROMOTION_MAP_SHA256 = (
    "2b34a3c828fa55a93a5595555f7dd5160e7a676338245bd0611809f399b4296f"
)
EXPECTED_PROMOTION_TARGET_INCIDENCE_SHA256 = (
    "61be985100426fa5720254e5f95bb6ebce020b6f9198260a7e42596c41d047f4"
)
EXPECTED_PROMOTION_TARGET_NORMALIZED_ROW_SHA256 = (
    "4fa439da6e1094cebfecf5d4042dc4cf5cd74a9ecaad7b7e01b8aa05c3568f59"
)
EXPECTED_PROMOTION_TARGET_TEMPLATE_SHA256 = (
    "e0c71987e5aa74d9268796ff3f27bbaa8bdaad0ce0abca7c08af496afc46271f"
)
EXPECTED_HARD_ONLY_PAIR_SHA256 = (
    "3a552bf80f494f991e46ec3516d2a5c65a9de427f7d1a256eb2d918c12406879"
)


NORMALIZED_VECTORS = {
    (0, 0, 0): "0",
    (1, 0, 0): "U",
    (0, 1, 0): "V",
    (0, 0, 1): "I",
    (2, 0, 0): "2U",
    (0, 2, 0): "2V",
    (0, 0, 2): "2I",
    (1, 1, 0): "UV",
    (1, 0, 1): "UI",
    (0, 1, 1): "VI",
}
NORMALIZED_ORDER = tuple(NORMALIZED_VECTORS.values())
NORMALIZED_INDEX = {
    name: index for index, name in enumerate(NORMALIZED_ORDER)
}
U_DEGREE = {"0": 0, "U": 1, "2U": 2}

LOWER_UNIVERSES = {
    (1, 2): frozenset(("0", "U", "I", "2I", "UI")),
    (1, 3): frozenset(("0", "U", "I", "2U", "2I", "UI")),
    (4, 5): frozenset(("0", "U", "I", "2I", "UI")),
}

EXCEPTIONAL_LOWER_SUPPORTS = frozenset(
    {
        ("0", "U", "I", "2I"),
        ("0", "U", "I", "UI"),
        ("0", "U", "2I", "UI"),
        ("0", "I", "2I", "UI"),
        ("U", "I", "2I", "UI"),
        ("0", "U", "I", "2I", "UI"),
    }
)


def current_remainder_769() -> frozenset[Pair]:
    """The claim-neutral remainder after the certified 26-pair branch."""

    result = prospective.prospective_after_pairs() - prospective.selected_pairs()
    assert len(result) == 769
    return result


def incidences() -> tuple[tuple[Pair, Descriptor], ...]:
    """Return the exact dormant/no-wholly-top rows on the 769 remainder."""

    remainder = current_remainder_769()
    result = tuple(
        (pair, descriptor)
        for pair, descriptor, category in phase.incidences()
        if pair in remainder
        and category == "promotion_dormant_top"
        and not phase._whole_top_linkages(pair, descriptor)
    )
    assert len(result) == 407
    return result


def selected_pairs() -> frozenset[Pair]:
    return frozenset(pair for pair, _descriptor in incidences())


def _normalization_order(descriptor: Descriptor) -> tuple[int, int, int]:
    inactive, = tuple(
        coordinate
        for coordinate, value in enumerate(descriptor.weight)
        if value == 0
    )
    active = tuple(
        sorted(
            (
                coordinate
                for coordinate, value in enumerate(descriptor.weight)
                if value > 0
            ),
            key=lambda coordinate: descriptor.weight[coordinate],
        )
    )
    if len(active) != 2:
        raise AssertionError("row is not two-active")
    lower, higher = active
    if descriptor.weight[lower] >= descriptor.weight[higher]:
        raise AssertionError("active weights do not have a strict order")
    return lower, higher, inactive


def _normalized_name(node: int, order: tuple[int, int, int]) -> str:
    vector = tuple(closure.COMPLEXES[node][coordinate] for coordinate in order)
    return NORMALIZED_VECTORS[vector]


def _normalized_support(
    mask: int,
    order: tuple[int, int, int],
) -> tuple[str, ...]:
    return tuple(
        sorted(
            (_normalized_name(node, order) for node in tier._nodes(mask)),
            key=NORMALIZED_INDEX.__getitem__,
        )
    )


def normalized_rows() -> tuple[dict[str, object], ...]:
    result: list[dict[str, object]] = []
    for pair, descriptor in incidences():
        order = _normalization_order(descriptor)
        lower, higher, _inactive = order
        proper_rows = phase._proper_top_linkages(pair, descriptor)
        if len(proper_rows) != 1:
            raise AssertionError("row does not have one proper-top linkage")
        proper_mask, top_nodes = proper_rows[0]
        other_mask = pair[1] if pair[0] == proper_mask else pair[0]
        proper = _normalized_support(proper_mask, order)
        other = _normalized_support(other_mask, order)
        top = tuple(
            sorted(
                (_normalized_name(node, order) for node in top_nodes),
                key=NORMALIZED_INDEX.__getitem__,
            )
        )
        result.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "normalized_ratio": [
                    descriptor.weight[lower],
                    descriptor.weight[higher],
                ],
                "proper_side": 0 if pair[0] == proper_mask else 1,
                "proper_support": list(proper),
                "other_support": list(other),
                "proper_top_intersection": list(top),
            }
        )
    result.sort(
        key=lambda row: json.dumps(
            row, sort_keys=True, separators=(",", ":")
        )
    )
    return tuple(result)


def normalized_templates() -> tuple[dict[str, object], ...]:
    templates = {
        (
            tuple(row["normalized_ratio"]),
            tuple(row["proper_support"]),
            tuple(row["other_support"]),
        )
        for row in normalized_rows()
    }
    return tuple(
        {
            "normalized_ratio": list(ratio),
            "proper_support": list(proper),
            "other_support": list(other),
        }
        for ratio, proper, other in sorted(templates, key=repr)
    )


def _encoded_sha256(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()
    return sha256(encoded).hexdigest()


def _normalized_row_fingerprint_payload(
    rows: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    """Canonical compact schema used by the announced row fingerprint."""

    payload = tuple(
        {
            "pair": row["pair"],
            "weight": row["weight"],
            "caps": row["caps"],
            "ratio": row["normalized_ratio"],
            "proper": sorted(row["proper_support"]),
            "lower": sorted(row["other_support"]),
            "proper_side": row["proper_side"],
        }
        for row in rows
    )
    return tuple(
        sorted(
            payload,
            key=lambda row: json.dumps(
                row, sort_keys=True, separators=(",", ":")
            ),
        )
    )


def _normalized_template_fingerprint_payload(
    rows: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    """Canonical compact schema used by the announced template hash."""

    templates = {
        (
            tuple(row["normalized_ratio"]),
            tuple(sorted(row["proper_support"])),
            tuple(sorted(row["other_support"])),
        )
        for row in rows
    }
    return tuple(
        {
            "ratio": list(ratio),
            "proper": list(proper),
            "lower": list(other),
        }
        for ratio, proper, other in sorted(templates, key=repr)
    )


def _template_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        tuple(row["normalized_ratio"]),
        tuple(row["proper_support"]),
        tuple(row["other_support"]),
    )


def _base_maximum(row: dict[str, object]) -> str:
    network = set(row["proper_support"]) | set(row["other_support"])
    enabled = network & set(U_DEGREE)
    if not enabled:
        raise AssertionError("no enabled source on the I=0 face")
    maximum_degree = max(U_DEGREE[name] for name in enabled)
    maximum = tuple(
        name for name in enabled if U_DEGREE[name] == maximum_degree
    )
    if len(maximum) != 1:
        raise AssertionError("base maximum is not unique")
    return maximum[0]


def _resistance_class(row: dict[str, object]) -> int:
    ratio = tuple(row["normalized_ratio"])
    proper = tuple(row["proper_support"])
    other = tuple(row["other_support"])
    maximum = _base_maximum(row)
    exceptional = proper == ("2U", "VI")
    if not exceptional:
        return 0
    if ratio != (1, 3) or maximum != "2U":
        raise AssertionError("unexpected two-node neutral exception")
    return 1 if "U" in other else 2


def _descriptor_key(
    item: tuple[Pair, Descriptor],
) -> tuple[object, ...]:
    pair, descriptor = item
    return closure.pair_payload(pair), descriptor.weight, descriptor.caps


def _pair_payload(pair: Pair) -> list[list[str]]:
    return [list(part) for part in closure.pair_payload(pair)]


def _phase_payload(
    phases: tuple[tuple[str, tuple[str, ...]], ...],
) -> list[list[object]]:
    return [[kind, list(stripped)] for kind, stripped in phases]


def _one_active_route(
    supports: tuple[tuple[str, ...], ...],
    normalized_caps: tuple[int, ...],
    phases: tuple[tuple[str, tuple[str, ...]], ...],
) -> tuple[str, str]:
    """Apply the existing exact predicates and expose the generalized seam."""

    kinds = tuple(kind for kind, _stripped in phases)
    if "whole_top" in kinds:
        return "open_whole", one_active_graph._whole_top_category(
            supports, phases
        )
    if any("0" in stripped for _kind, stripped in phases):
        return "direct_physical_C", "mixed_C_source_direct_down_0"
    if set(kinds) == {"lower_only", "mixed_killed"}:
        mixed_stripped, = (
            stripped
            for kind, stripped in phases
            if kind == "mixed_killed"
        )
        if set(mixed_stripped) == {"A", "B"}:
            return "family_i", one_active_graph._family_i_category(
                supports, phases
            )
        assert len(mixed_stripped) == 1
        try:
            category = one_active_graph._family_ii_category(
                supports, normalized_caps
            )
        except AssertionError:
            return "generalized_family_ii", "generalized_family_ii_open"
        return "exact_family_ii", category
    assert kinds == ("mixed_killed", "mixed_killed")
    assert {phases[0][1], phases[1][1]} == {("A",), ("B",)}
    return "family_iii", one_active_graph._family_iii_category(
        supports, phases
    )


@lru_cache(maxsize=1)
def one_active_incidences() -> tuple[tuple[Pair, Descriptor], ...]:
    """All one-active failures on the exact 333 hard-pair union."""

    rows = tuple(
        (pair, descriptor)
        for pair in selected_pairs()
        for descriptor in feasibility.feasible_failing_descriptors(pair)
        if len(tier._active_coordinates(descriptor)) == 1
    )
    result = tuple(sorted(rows, key=_descriptor_key))
    assert len(result) == 1104
    return result


@lru_cache(maxsize=1)
def one_active_rows() -> tuple[dict[str, object], ...]:
    """Classify all 1,104 one-active failures without analytic promotion."""

    rows: list[dict[str, object]] = []
    for pair, descriptor in one_active_incidences():
        normalized = one_active_structure._normalized(pair, descriptor)
        supports = tuple(normalized["supports"])
        normalized_caps = tuple(normalized["caps"])
        phases = tuple(
            one_active_structure._linkage_phase(support)
            for support in supports
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
    rows.sort(
        key=lambda row: json.dumps(
            row, sort_keys=True, separators=(",", ":")
        )
    )
    return tuple(rows)


@lru_cache(maxsize=1)
def one_active_profiles() -> tuple[dict[str, object], ...]:
    """Freeze the 527 exact ordered normalized profiles and multiplicities."""

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


def _generalized_one_active_incidence(
    pair: Pair, descriptor: Descriptor
) -> bool:
    normalized = one_active_structure._normalized(pair, descriptor)
    supports = tuple(normalized["supports"])
    normalized_caps = tuple(normalized["caps"])
    phases = tuple(
        one_active_structure._linkage_phase(support) for support in supports
    )
    family, _category = _one_active_route(
        supports, normalized_caps, phases
    )
    return family == "generalized_family_ii"


@lru_cache(maxsize=1)
def generalized_one_active_incidences(
) -> tuple[tuple[Pair, Descriptor], ...]:
    result = tuple(
        item for item in one_active_incidences()
        if _generalized_one_active_incidence(*item)
    )
    assert len(result) == 951
    return result


@lru_cache(maxsize=1)
def _descriptor_lookup() -> dict[tuple[tuple[int, ...], tuple[int, ...]], Descriptor]:
    return {
        (descriptor.weight, descriptor.caps): descriptor
        for descriptor in tier.tier_descriptors()
    }


def _one_active_normalization(
    pair: Pair, descriptor: Descriptor
) -> tuple[dict[str, object], Descriptor]:
    """Normalize as U=spectator, V=old active, I=top cofactor."""

    normalized = one_active_structure._normalized(pair, descriptor)
    supports = tuple(normalized["supports"])
    normalized_caps = tuple(normalized["caps"])
    old_for_new = tuple(normalized["old_for_new"])
    phases = tuple(
        one_active_structure._linkage_phase(support) for support in supports
    )
    family, _category = _one_active_route(
        supports, normalized_caps, phases
    )
    if family != "generalized_family_ii":
        raise ValueError("incidence is not generalized Family II")

    stripped, = (
        stripped
        for kind, stripped in phases
        if kind == "mixed_killed"
    )
    assert stripped in (("A",), ("B",))
    cofactor = 0 if stripped == ("A",) else 1
    spectator = 1 - cofactor
    assert normalized_caps[cofactor] == 0

    # Coordinates in the one-active normalization are A,B,C.  Reorder them
    # as U=spectator, V=C, I=cofactor, exactly the dormant-row convention.
    order = (spectator, 2, cofactor)

    def canonical_support(support: tuple[str, ...]) -> tuple[str, ...]:
        names = []
        for name in support:
            vector = closure.COMPLEXES[closure.NAME_TO_INDEX[name]]
            names.append(
                NORMALIZED_VECTORS[tuple(vector[index] for index in order)]
            )
        return tuple(sorted(names, key=NORMALIZED_INDEX.__getitem__))

    proper_support, = (
        canonical_support(supports[index])
        for index, (kind, _stripped) in enumerate(phases)
        if kind == "mixed_killed"
    )
    lower_support, = (
        canonical_support(supports[index])
        for index, (kind, _stripped) in enumerate(phases)
        if kind == "lower_only"
    )
    assert "VI" in proper_support
    assert "V" not in set(proper_support) | set(lower_support)

    # The moving spectator boundary has relative exponent one against the
    # old active exponent three; the cofactor remains exactly zero.  Map this
    # normalized (1,3,0) descriptor back to physical coordinates.
    normalized_weight = [0, 0, 3]
    normalized_weight[spectator] = 1
    normalized_target_caps = [2, 2, 2]
    normalized_target_caps[cofactor] = 0
    target_weight = [0, 0, 0]
    target_caps = [0, 0, 0]
    for new_coordinate, old_coordinate in enumerate(old_for_new):
        target_weight[old_coordinate] = normalized_weight[new_coordinate]
        target_caps[old_coordinate] = normalized_target_caps[new_coordinate]
    target = _descriptor_lookup()[(tuple(target_weight), tuple(target_caps))]

    row = {
        "pair": _pair_payload(pair),
        "weight": list(descriptor.weight),
        "caps": list(descriptor.caps),
        "spectator_cap": normalized_caps[spectator],
        "proper": list(proper_support),
        "lower": list(lower_support),
    }
    return row, target


@lru_cache(maxsize=1)
def generalized_normalized_rows() -> tuple[dict[str, object], ...]:
    rows = [
        _one_active_normalization(pair, descriptor)[0]
        for pair, descriptor in generalized_one_active_incidences()
    ]
    rows.sort(
        key=lambda row: json.dumps(
            row, sort_keys=True, separators=(",", ":")
        )
    )
    return tuple(rows)


@lru_cache(maxsize=1)
def generalized_support_templates() -> tuple[dict[str, object], ...]:
    supports = {
        (tuple(row["proper"]), tuple(row["lower"]))
        for row in generalized_normalized_rows()
    }
    return tuple(
        {"proper": list(proper), "lower": list(lower)}
        for proper, lower in sorted(supports, key=repr)
    )


@lru_cache(maxsize=1)
def generalized_support_cap_templates() -> tuple[dict[str, object], ...]:
    supports = {
        (
            tuple(row["proper"]),
            tuple(row["lower"]),
            row["spectator_cap"],
        )
        for row in generalized_normalized_rows()
    }
    return tuple(
        {
            "proper": list(proper),
            "lower": list(lower),
            "spectator_cap": cap,
        }
        for proper, lower, cap in sorted(supports, key=repr)
    )


@lru_cache(maxsize=1)
def promotion_targets() -> tuple[tuple[Pair, Descriptor], ...]:
    targets = {
        (pair, _one_active_normalization(pair, descriptor)[1])
        for pair, descriptor in generalized_one_active_incidences()
    }
    return tuple(sorted(targets, key=_descriptor_key))


@lru_cache(maxsize=1)
def promotion_map_payload() -> tuple[dict[str, object], ...]:
    rows = []
    for pair, descriptor in generalized_one_active_incidences():
        _normalized, target = _one_active_normalization(pair, descriptor)
        rows.append(
            {
                "pair": _pair_payload(pair),
                "one_weight": list(descriptor.weight),
                "one_caps": list(descriptor.caps),
                "two_weight": list(target.weight),
                "two_caps": list(target.caps),
            }
        )
    rows.sort(
        key=lambda row: json.dumps(
            row, sort_keys=True, separators=(",", ":")
        )
    )
    return tuple(rows)


def one_active_family_pairs(family: str) -> frozenset[Pair]:
    result = set()
    for pair, descriptor in one_active_incidences():
        normalized = one_active_structure._normalized(pair, descriptor)
        supports = tuple(normalized["supports"])
        normalized_caps = tuple(normalized["caps"])
        phases = tuple(
            one_active_structure._linkage_phase(support)
            for support in supports
        )
        row_family, _category = _one_active_route(
            supports, normalized_caps, phases
        )
        if row_family == family:
            result.add(pair)
    return frozenset(result)


def certificate() -> dict[str, object]:
    rows = normalized_rows()
    templates = normalized_templates()
    pairs = selected_pairs()
    positive, signed, _residual = feasibility._residual_failures()

    incidence_digest = feasibility._incidence_fingerprint(incidences())
    row_digest = _encoded_sha256(_normalized_row_fingerprint_payload(rows))
    template_digest = _encoded_sha256(
        _normalized_template_fingerprint_payload(rows)
    )
    assert incidence_digest == EXPECTED_INCIDENCE_SHA256
    assert closure.pair_fingerprint(pairs) == EXPECTED_PAIR_SHA256
    assert row_digest == EXPECTED_NORMALIZED_ROW_SHA256
    assert template_digest == EXPECTED_NORMALIZED_TEMPLATE_SHA256

    ratio_histogram = Counter(tuple(row["normalized_ratio"]) for row in rows)
    template_ratio_histogram = Counter(
        tuple(row["normalized_ratio"]) for row in templates
    )
    multiplicities = Counter(Counter(_template_key(row) for row in rows).values())
    resistance_histogram = Counter(_resistance_class(row) for row in rows)
    template_resistance_histogram = Counter(
        _resistance_class(row) for row in templates
    )
    maximum_histogram = Counter(_base_maximum(row) for row in rows)

    assert ratio_histogram == {(1, 2): 37, (1, 3): 333, (4, 5): 37}
    assert template_ratio_histogram == {(1, 2): 17, (1, 3): 154, (4, 5): 17}
    assert multiplicities == {1: 17, 2: 147, 4: 24}
    assert resistance_histogram == {0: 395, 1: 10, 2: 2}
    assert template_resistance_histogram == {0: 182, 1: 5, 2: 1}
    assert maximum_histogram == {"U": 111, "2U": 296}

    support_templates_by_ratio = {
        ratio: frozenset(
            (
                tuple(row["proper_support"]),
                tuple(row["other_support"]),
            )
            for row in templates
            if tuple(row["normalized_ratio"]) == ratio
        )
        for ratio in ((1, 2), (1, 3), (4, 5))
    }
    assert support_templates_by_ratio[(1, 2)] == support_templates_by_ratio[(4, 5)]
    assert len(set().union(*support_templates_by_ratio.values())) == 154

    exceptional_rows = tuple(
        row for row in rows if tuple(row["proper_support"]) == ("2U", "VI")
    )
    exceptional_pairs = frozenset(
        pair
        for pair, descriptor in incidences()
        if (
            normalized := next(
                item
                for item in rows
                if item["pair"]
                == [list(part) for part in closure.pair_payload(pair)]
                and item["weight"] == list(descriptor.weight)
                and item["caps"] == list(descriptor.caps)
            )
        )["proper_support"]
        == ["2U", "VI"]
    )
    assert len(exceptional_rows) == 12
    assert {
        tuple(row["other_support"]) for row in exceptional_rows
    } == EXCEPTIONAL_LOWER_SUPPORTS
    assert len(exceptional_pairs) == 12
    assert closure.pair_fingerprint(exceptional_pairs) == EXPECTED_EXCEPTIONAL_PAIR_SHA256

    # Freeze the complete one-active dimension on the same 333 pairs.  The
    # generalized Family-II rows are the only graph-theorem seam not already
    # covered by the established one-active predicates.
    one_rows = one_active_rows()
    one_profiles = one_active_profiles()
    one_incidence_digest = feasibility._incidence_fingerprint(
        one_active_incidences()
    )
    one_classified_digest = _encoded_sha256(one_rows)
    one_profile_digest = _encoded_sha256(one_profiles)
    assert one_incidence_digest == EXPECTED_ONE_ACTIVE_INCIDENCE_SHA256
    assert one_classified_digest == EXPECTED_ONE_ACTIVE_CLASSIFIED_SHA256
    assert one_profile_digest == EXPECTED_ONE_ACTIVE_PROFILE_SHA256
    assert len(one_rows) == 1104
    assert len(one_profiles) == 527

    one_family_histogram = Counter(
        row["structural_family"] for row in one_rows
    )
    one_graph_histogram = Counter(row["graph_category"] for row in one_rows)
    assert one_family_histogram == {
        "generalized_family_ii": 951,
        "direct_physical_C": 99,
        "exact_family_ii": 48,
        "open_whole": 6,
    }
    assert one_graph_histogram == {
        "generalized_family_ii_open": 951,
        "mixed_C_source_direct_down_0": 99,
        "family_ii_axis_down_0": 40,
        "family_ii_axis_no_history": 8,
        "open_wholly_top_down_1": 6,
    }

    generalized_incidences = generalized_one_active_incidences()
    generalized_pairs = frozenset(pair for pair, _ in generalized_incidences)
    generalized_rows = generalized_normalized_rows()
    support_templates = generalized_support_templates()
    support_cap_templates = generalized_support_cap_templates()
    assert feasibility._incidence_fingerprint(generalized_incidences) == (
        EXPECTED_GENERALIZED_ONE_ACTIVE_INCIDENCE_SHA256
    )
    assert closure.pair_fingerprint(generalized_pairs) == (
        EXPECTED_GENERALIZED_PAIR_SHA256
    )
    assert _encoded_sha256(generalized_rows) == (
        EXPECTED_GENERALIZED_NORMALIZED_ROW_SHA256
    )
    assert _encoded_sha256(support_templates) == (
        EXPECTED_GENERALIZED_SUPPORT_TEMPLATE_SHA256
    )
    assert _encoded_sha256(support_cap_templates) == (
        EXPECTED_GENERALIZED_SUPPORT_CAP_TEMPLATE_SHA256
    )
    assert len(generalized_incidences) == 951
    assert len(generalized_pairs) == 317
    assert len(support_templates) == 146
    assert len(support_cap_templates) == 438
    assert Counter(row["spectator_cap"] for row in generalized_rows) == {
        0: 317,
        1: 317,
        2: 317,
    }

    targets = promotion_targets()
    target_set = frozenset(targets)
    hard_incidence_set = frozenset(incidences())
    assert target_set <= hard_incidence_set
    assert len(targets) == 317
    assert feasibility._incidence_fingerprint(targets) == (
        EXPECTED_PROMOTION_TARGET_INCIDENCE_SHA256
    )
    assert _encoded_sha256(promotion_map_payload()) == (
        EXPECTED_PROMOTION_MAP_SHA256
    )
    target_multiplicity = Counter(
        (pair, _one_active_normalization(pair, descriptor)[1])
        for pair, descriptor in generalized_incidences
    )
    assert Counter(target_multiplicity.values()) == {3: 317}

    hard_row_lookup = {
        (
            tuple(tuple(part) for part in row["pair"]),
            tuple(row["weight"]),
            tuple(row["caps"]),
        ): row
        for row in rows
    }
    target_rows = tuple(
        hard_row_lookup[
            (
                tuple(tuple(part) for part in closure.pair_payload(pair)),
                descriptor.weight,
                descriptor.caps,
            )
        ]
        for pair, descriptor in targets
    )
    target_rows = tuple(
        sorted(
            target_rows,
            key=lambda row: json.dumps(
                row, sort_keys=True, separators=(",", ":")
            ),
        )
    )
    target_template_payload = _normalized_template_fingerprint_payload(
        target_rows
    )
    assert _encoded_sha256(_normalized_row_fingerprint_payload(target_rows)) == (
        EXPECTED_PROMOTION_TARGET_NORMALIZED_ROW_SHA256
    )
    assert len(target_template_payload) == 146
    assert _encoded_sha256(target_template_payload) == (
        EXPECTED_PROMOTION_TARGET_TEMPLATE_SHA256
    )
    target_resistance_histogram = Counter(
        _resistance_class(row) for row in target_rows
    )
    assert target_resistance_histogram == {0: 305, 1: 10, 2: 2}

    # The one-active normalization has exactly the target hard support.  This
    # is an incidence-level identity, not an analytic handoff assertion.
    for pair, descriptor in generalized_incidences:
        generalized_row, target = _one_active_normalization(pair, descriptor)
        hard_row = hard_row_lookup[
            (
                tuple(tuple(part) for part in closure.pair_payload(pair)),
                target.weight,
                target.caps,
            )
        ]
        assert generalized_row["proper"] == hard_row["proper_support"]
        assert generalized_row["lower"] == hard_row["other_support"]
        assert hard_row["normalized_ratio"] == [1, 3]

    exact_family_ii_pairs = one_active_family_pairs("exact_family_ii")
    hard_only_pairs = pairs - generalized_pairs
    assert exact_family_ii_pairs == hard_only_pairs
    assert len(hard_only_pairs) == 16
    assert closure.pair_fingerprint(hard_only_pairs) == (
        EXPECTED_HARD_ONLY_PAIR_SHA256
    )
    assert generalized_pairs | exact_family_ii_pairs == pairs

    # Premises of the arbitrary-orientation cut proof.  Below the unique
    # top VI, lower source order is exactly U-degree.  If the unique base
    # maximum lies in the other linkage, each of its outgoing edges
    # descends.  If it lies in the proper linkage, the only possible
    # zero-service SCC is {maximum, VI}; it is a proper subset unless the
    # row is one of the twelve exact one-dimensional birth--death exceptions.
    for row in rows:
        ratio = tuple(row["normalized_ratio"])
        proper = set(row["proper_support"])
        other = set(row["other_support"])
        lower_universe = LOWER_UNIVERSES[ratio]
        assert proper & other == set()
        assert set(row["proper_top_intersection"]) == {"VI"}
        assert "VI" in proper
        assert proper - {"VI"} <= lower_universe
        assert other <= lower_universe
        assert len(proper) >= 2 and len(other) >= 2
        maximum = _base_maximum(row)
        maximum_degree = U_DEGREE[maximum]
        if maximum in other:
            assert all(
                name not in U_DEGREE
                or U_DEGREE[name] < maximum_degree
                for name in other - {maximum}
            )
        else:
            assert maximum in proper
            assert all(
                name == "VI"
                or name not in U_DEGREE
                or U_DEGREE[name] < maximum_degree
                for name in proper - {maximum}
            )
            if proper == {maximum, "VI"}:
                assert ratio == (1, 3)
                assert maximum == "2U"

    return {
        "claim_scope": (
            "exact 407-row selector, complete 333-pair one-active "
            "classification, normalized support exhaustion, 951-to-317 "
            "promotion map, and proof premises; the analytic candidate "
            "failed audit at its uniform unweighted spectator Green bound"
        ),
        "authoritative_parent_remainder": {
            "pairs": len(current_remainder_769()),
            "pair_sha256": closure.pair_fingerprint(current_remainder_769()),
        },
        "selected_incidences": {
            "total": len(rows),
            "positive": sum(pair in positive for pair, _ in incidences()),
            "signed": sum(pair in signed for pair, _ in incidences()),
            "sha256": incidence_digest,
        },
        "selected_pairs": {
            "total": len(pairs),
            "positive": len(pairs & positive),
            "signed": len(pairs & signed),
            "sha256": closure.pair_fingerprint(pairs),
        },
        "normalization": {
            "inactive_species": "I",
            "lower_weight_active_species": "U",
            "higher_weight_active_species": "V",
            "proper_top_intersection": ["VI"],
            "ratio_histogram": {
                f"{first}:{second}": count
                for (first, second), count in sorted(ratio_histogram.items())
            },
            "lower_universes": {
                f"{first}:{second}": sorted(
                    LOWER_UNIVERSES[(first, second)],
                    key=NORMALIZED_INDEX.__getitem__,
                )
                for first, second in sorted(LOWER_UNIVERSES)
            },
            "row_sha256": row_digest,
        },
        "normalized_templates": {
            "total": len(templates),
            "ratio_histogram": {
                f"{first}:{second}": count
                for (first, second), count in sorted(
                    template_ratio_histogram.items()
                )
            },
            "support_templates_ignoring_ratio": 154,
            "ratio_1_2_equals_ratio_4_5_support_menu": True,
            "physical_multiplicity_histogram": dict(sorted(multiplicities.items())),
            "sha256": template_digest,
        },
        "base_maximum_histogram": dict(sorted(maximum_histogram.items())),
        "candidate_resistance_partition": {
            "incidences": dict(sorted(resistance_histogram.items())),
            "templates": dict(sorted(template_resistance_histogram.items())),
            "maximum_down_resistance": 2,
            "claimed_upward_gap_in_candidate_note": 1,
        },
        "exceptional_birth_death_comparison_block": {
            "normalized_ratio": [1, 3],
            "proper_support": ["2U", "VI"],
            "incidences": len(exceptional_rows),
            "pairs": len(exceptional_pairs),
            "positive_pairs": len(exceptional_pairs & positive),
            "signed_pairs": len(exceptional_pairs & signed),
            "other_supports": [
                list(support) for support in sorted(EXCEPTIONAL_LOWER_SUPPORTS)
            ],
            "pair_sha256": closure.pair_fingerprint(exceptional_pairs),
        },
        "one_active_dimension": {
            "incidences": len(one_rows),
            "pairs": len(pairs),
            "incidence_sha256": one_incidence_digest,
            "classified_sha256": one_classified_digest,
            "profiles": len(one_profiles),
            "profile_sha256": one_profile_digest,
            "family_histogram": dict(sorted(one_family_histogram.items())),
            "graph_category_histogram": dict(
                sorted(one_graph_histogram.items())
            ),
        },
        "generalized_family_ii": {
            "incidences": len(generalized_incidences),
            "pairs": len(generalized_pairs),
            "incidence_sha256": feasibility._incidence_fingerprint(
                generalized_incidences
            ),
            "pair_sha256": closure.pair_fingerprint(generalized_pairs),
            "normalization": {
                "U": "inactive spectator promoted at the moving boundary",
                "V": "old active species",
                "I": "unique top cofactor, fixed at zero before promotion",
                "proper_top_intersection": ["VI"],
                "spectator_cap_histogram": {
                    str(cap): count
                    for cap, count in sorted(
                        Counter(
                            row["spectator_cap"]
                            for row in generalized_rows
                        ).items()
                    )
                },
                "row_sha256": _encoded_sha256(generalized_rows),
            },
            "support_templates": {
                "total": len(support_templates),
                "sha256": _encoded_sha256(support_templates),
            },
            "support_cap_templates": {
                "total": len(support_cap_templates),
                "sha256": _encoded_sha256(support_cap_templates),
            },
        },
        "one_to_two_active_promotion_handoff": {
            "mapped_source_incidences": len(generalized_incidences),
            "distinct_target_incidences": len(targets),
            "distinct_target_pairs": len(
                frozenset(pair for pair, _descriptor in targets)
            ),
            "source_multiplicity_per_target": 3,
            "map_sha256": _encoded_sha256(promotion_map_payload()),
            "target_incidence_sha256": feasibility._incidence_fingerprint(
                targets
            ),
            "target_normalized_row_sha256": _encoded_sha256(
                _normalized_row_fingerprint_payload(target_rows)
            ),
            "target_templates": len(target_template_payload),
            "target_template_sha256": _encoded_sha256(
                target_template_payload
            ),
            "target_resistance_histogram": dict(
                sorted(target_resistance_histogram.items())
            ),
            "all_targets_are_exact_hard_1_to_3_rows": True,
            "normalized_supports_identical_at_handoff": True,
            "boundary_entry_jump_charged_analytically_in_note": True,
        },
        "hard_pair_one_active_partition": {
            "generalized_family_ii_pairs": len(generalized_pairs),
            "exact_family_ii_hard_only_pairs": len(hard_only_pairs),
            "exact_family_ii_hard_only_pair_sha256": (
                closure.pair_fingerprint(hard_only_pairs)
            ),
            "union_is_all_333_hard_pairs": True,
        },
        "arbitrary_orientation_graph_theorem_candidate_written": True,
        "aggregate_resolvent_theorem_candidate_written": True,
        "generalized_one_active_resolvent_theorem_candidate_written": True,
        "independent_analytic_audit_status": (
            "fail_as_written_start_weighted_green_repair_open"
        ),
        "uniform_unweighted_unbounded_spectator_green_bound_withdrawn": True,
        "analytic_theorem_independently_audited": False,
        "pair_level_recurrence_certified": False,
        "global_t3_2_certified": False,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
