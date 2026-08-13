"""Exact scope overlap of the old candidate-1227 theorem with the 6,654.

This is a finite support/orbit/descriptor identity only.  It checks direct
support membership, S3/linkage-reversal orbit membership, and exact
normalized one-active support templates.  It does not enumerate directed
orientations, rates, populations, histories, or communicating classes, and
it makes no recurrence claim.

The final diagnostic applies the old finite category router syntactically to
the new one-active rows.  A successful syntactic route is explicitly not a
theorem transfer: the old analytic theorem was proved on its exact selector.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

import active_invariant_orbit_gap_432_certificate as orbit
import one_active_phase_shape as candidate
import one_active_relative_debt_cegar as graph
import one_active_remaining_structure as structure
import outside_mixed_remaining_18496_certificate as remainder


EXPECTED_DEPENDENCY_SHA256 = {
    "active_invariant_orbit_gap_432_certificate.py": (
        "31fa24a20e18546e9c623d3aaf6d3b845c1708d5782f86333c02417fa366cd53"
    ),
    "one_active_phase_shape.py": (
        "781c1e6b5106cc6785ec6902d932fb319ef2078fb40b4e4f983fdc6f7bc45be4"
    ),
    "one_active_relative_debt_cegar.py": (
        "32d2313f428663c09a3d14e658f4c72a6ccbcaeb99c2b0cbf92dcce3c8b843ba"
    ),
    "one_active_remaining_structure.py": (
        "ce1ff5e872cf4b93e085d56743b90c660eabf01f80491310c55955f2ca107e24"
    ),
    "outside_mixed_remaining_18496_certificate.py": (
        "314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63"
    ),
}

EXPECTED_CANDIDATE_ORBIT_SHA256 = (
    "7bfe8bc085e29d864fb26da7a6f81906feed5cae03458fafb9190ce584bb4410"
)
EXPECTED_PAYLOAD_SHA256 = (
    "4163d9adefa525663a75afc797774e3028e38cee2aa7b04d82343eb80b8daf2b"
)


def dependency_sha256() -> dict[str, str]:
    directory = Path(__file__).resolve().parent
    return {
        name: sha256((directory / name).read_bytes()).hexdigest()
        for name in EXPECTED_DEPENDENCY_SHA256
    }


def _route_old_category(pair, descriptor) -> str:
    """Run the literal old finite router, without promoting its conclusion."""

    normalized = structure._normalized(pair, descriptor)
    supports = tuple(normalized["supports"])
    caps = tuple(normalized["caps"])
    phases = tuple(structure._linkage_phase(support) for support in supports)
    kinds = tuple(kind for kind, _stripped in phases)
    if "whole_top" in kinds:
        return graph._whole_top_category(supports, phases)
    if any("0" in stripped for _kind, stripped in phases):
        return "mixed_C_source_direct_down_0"
    if set(kinds) == {"lower_only", "mixed_killed"}:
        mixed_stripped, = (
            stripped
            for kind, stripped in phases
            if kind == "mixed_killed"
        )
        if set(mixed_stripped) == {"A", "B"}:
            return graph._family_i_category(supports, phases)
        assert len(mixed_stripped) == 1
        return graph._family_ii_category(supports, caps)
    assert kinds == ("mixed_killed", "mixed_killed")
    assert {phases[0][1], phases[1][1]} == {("A",), ("B",)}
    return graph._family_iii_category(supports, phases)


def _digest(payload: object) -> str:
    return sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def certificate() -> dict[str, object]:
    dependencies = dependency_sha256()
    old_pairs = frozenset(candidate.candidate_pairs())
    old_orbit = orbit.pair_orbit(old_pairs)
    failed = remainder.failed_pairs()
    entire_remainder = remainder.remainder_pairs()

    old_support_types = set()
    old_cap_types = set()
    for pair, descriptor in candidate.candidate_incidences():
        normalized = structure._normalized(pair, descriptor)
        supports = tuple(normalized["supports"])
        old_support_types.add(supports)
        old_cap_types.add((supports, tuple(normalized["caps"])))

    new_support_types = set()
    new_cap_types = set()
    profile_sets = defaultdict(set)
    syntactic_categories: Counter[str] = Counter()
    syntactic_failures = 0
    syntactic_by_pair = defaultdict(list)
    one_active_rows = 0
    witness = None

    for pair, descriptor in remainder.feasible_corrected_cut_failures():
        profile = remainder.failure_profile(pair, descriptor)
        profile_sets[pair].add(profile)
        if descriptor.active_mask.bit_count() != 1:
            continue
        one_active_rows += 1
        normalized = structure._normalized(pair, descriptor)
        supports = tuple(normalized["supports"])
        caps = tuple(normalized["caps"])
        new_support_types.add(supports)
        new_cap_types.add((supports, caps))
        try:
            category = _route_old_category(pair, descriptor)
            syntactic_categories[f"{profile}|{category}"] += 1
            syntactic_by_pair[pair].append(True)
        except AssertionError:
            syntactic_failures += 1
            syntactic_by_pair[pair].append(False)
            if witness is None:
                witness = {
                    "pair": remainder.closure.pair_payload(pair),
                    "weight": descriptor.weight,
                    "caps": descriptor.caps,
                    "profile": profile,
                    "normalized_supports": supports,
                    "normalized_caps": caps,
                }

    aa_pairs = {pair for pair, profiles in profile_sets.items() if "AA" in profiles}
    one_active_only_pairs = set(profile_sets) - aa_pairs
    all_rows_route = {
        pair
        for pair in one_active_only_pairs
        if syntactic_by_pair[pair] and all(syntactic_by_pair[pair])
    }

    payload = {
        "claim_scope": (
            "finite support/orbit/descriptor comparison only; syntactic old-"
            "router success is not an analytic theorem transfer"
        ),
        "dependency_sha256": dependencies,
        "candidate_1227_pairs": len(old_pairs),
        "candidate_1227_sha256": remainder.closure.pair_fingerprint(old_pairs),
        "candidate_s3_reversal_orbit_pairs": len(old_orbit),
        "candidate_s3_reversal_orbit_sha256": (
            remainder.closure.pair_fingerprint(old_orbit)
        ),
        "failed_remainder_pairs": len(failed),
        "failed_remainder_sha256": remainder.closure.pair_fingerprint(failed),
        "direct_candidate_overlap": len(old_pairs & failed),
        "s3_reversal_orbit_overlap": len(old_orbit & failed),
        "candidate_overlap_with_entire_18496": len(old_pairs & entire_remainder),
        "candidate_orbit_overlap_with_entire_18496": (
            len(old_orbit & entire_remainder)
        ),
        "new_failure_one_active_rows": one_active_rows,
        "new_pairs_with_aa_failure": len(aa_pairs),
        "new_pairs_with_only_one_active_failures": len(one_active_only_pairs),
        "old_normalized_support_types": len(old_support_types),
        "new_normalized_support_types": len(new_support_types),
        "normalized_support_type_overlap": (
            len(old_support_types & new_support_types)
        ),
        "old_normalized_support_cap_types": len(old_cap_types),
        "new_normalized_support_cap_types": len(new_cap_types),
        "normalized_support_cap_type_overlap": len(old_cap_types & new_cap_types),
        "old_router_syntactic_success_rows": sum(syntactic_categories.values()),
        "old_router_syntactic_failure_rows": syntactic_failures,
        "one_active_only_pairs_all_rows_route_syntactically": len(all_rows_route),
        "one_active_only_pairs_with_router_failure": (
            len(one_active_only_pairs - all_rows_route)
        ),
        "syntactic_category_histogram": dict(sorted(syntactic_categories.items())),
        "first_router_failure_witness": witness,
        "orientation_rate_population_or_history_enumeration": False,
        "recurrence_claim": False,
    }

    assert dependencies == EXPECTED_DEPENDENCY_SHA256
    assert len(old_pairs) == 1_227
    assert remainder.closure.pair_fingerprint(old_pairs) == candidate.closure.pair_fingerprint(old_pairs)
    assert len(old_orbit) == 6_546
    assert remainder.closure.pair_fingerprint(old_orbit) == EXPECTED_CANDIDATE_ORBIT_SHA256
    assert len(failed) == 6_654
    assert not old_pairs & failed
    assert not old_orbit & failed
    assert not old_pairs & entire_remainder
    assert not old_orbit & entire_remainder
    assert one_active_rows == 18_822
    assert len(aa_pairs) == 1_596
    assert len(one_active_only_pairs) == 5_058
    assert (len(old_support_types), len(new_support_types)) == (727, 1_275)
    assert not old_support_types & new_support_types
    assert (len(old_cap_types), len(new_cap_types)) == (1_599, 3_163)
    assert not old_cap_types & new_cap_types
    assert sum(syntactic_categories.values()) == 16_986
    assert syntactic_failures == 1_836
    assert len(all_rows_route) == 4_662
    assert len(one_active_only_pairs - all_rows_route) == 396
    assert witness == {
        "pair": (("0", "2A", "2B"), ("A", "AB", "AC")),
        "weight": (0, 0, 1),
        "caps": (0, 0, 2),
        "profile": "B/F0",
        "normalized_supports": (("0", "2A", "2B"), ("A", "AB", "AC")),
        "normalized_caps": (0, 0),
    }
    digest = _digest(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


def main() -> None:
    print(json.dumps(certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
