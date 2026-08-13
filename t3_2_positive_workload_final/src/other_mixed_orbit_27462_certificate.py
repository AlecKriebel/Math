"""Finite seed partition for the already completed 27,462-pair mixed orbit.

The exact 5,169 inherited shielded/available seeds contain 110 seeds whose
only early label was an active-coordinate invariant.  This certificate
removes precisely those 110 seeds and partitions the other 5,059 among
standalone recurrence branches.  It then closes those eligible seeds under
species permutations and linkage reversal.  Only finite support, tier, and
set identities are certified; no stochastic conclusion is computed here.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

import active_invariant_orbit_gap_432_certificate as orbit_gap
import corrected_t3_2_two_linkage_union as residual_union
import global_atlas_interface_closure as closure
import s_tier_superlevel_interface as corrected_tier


Pair = closure.Pair

EXPECTED_DEPENDENCY_SHA256 = {
    "active_invariant_orbit_gap_432_certificate.py": (
        "31fa24a20e18546e9c623d3aaf6d3b845c1708d5782f86333c02417fa366cd53"
    ),
    "corrected_t3_2_two_linkage_union.py": (
        "501d96c4cea2de33ed34db2c31702d3104e8ed80c1abb8cf15e895c56201593f"
    ),
    "global_atlas_interface_closure.py": (
        "293a63711f6da152edd72615d27fad5bbb859aa33a4b7eb150673b27ae3cb5bd"
    ),
    "s_tier_superlevel_interface.py": (
        "1a4e27fcf40af76cac6281f8830b7644bf086b3c05d97a963ce9f5bac736ad57"
    ),
}

EXPECTED_ELIGIBLE_SEED_SHA256 = (
    "c45f67990ff841e1ba7b7d5d8a2795539f495f2434d68135ad3b2483d2fda44f"
)
EXPECTED_STRICT_SEED_SHA256 = (
    "e760b14784236fe097aec28fa775553bcda4516fcc81e858b478a70eefd0bd6a"
)
EXPECTED_DZ_SEED_SHA256 = (
    "4e79e97328e35796ba4ff903708f1ccc341db564bd89463ccb47e1fa349a8fc1"
)
EXPECTED_PHYSICAL_SEAM_SEED_SHA256 = (
    "7a8d67d09a4d76923df5c36879f53bbaf301f2f666e6282a8e36f729aa48f2b1"
)
EXPECTED_TIER_PASS_SEED_SHA256 = (
    "9d70b04459dc110a1f7451d63c36e7e21d874eca3afec284268cac8cba942ba7"
)
EXPECTED_RESIDUAL_SEED_SHA256 = (
    "0c57f530eb44a688520cc1706f830afa18063f4d08d24e5006f47a5666edd0b3"
)
EXPECTED_OTHER_ORBIT_SHA256 = (
    "1bf337cf143c6eb4cee5088827bb9e9b9cec704f01a1b1f57bde6aed856d2812"
)
EXPECTED_BRANCH_MANIFEST_SHA256 = (
    "22f10cf6ea09a7b36650df174a866fd15470c770b3da6079728cfe5301f61c76"
)


def _digest(payload: object) -> str:
    return sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def dependency_sha256() -> dict[str, str]:
    source_directory = Path(__file__).resolve().parent
    return {
        filename: sha256((source_directory / filename).read_bytes()).hexdigest()
        for filename in EXPECTED_DEPENDENCY_SHA256
    }


@lru_cache(maxsize=1)
def eligible_seed_pairs() -> frozenset[Pair]:
    return orbit_gap.inherited_seed_pairs() - orbit_gap.active_invariant_seed_pairs()


@lru_cache(maxsize=1)
def strict_invariant_seed_pairs() -> frozenset[Pair]:
    return frozenset(
        pair
        for pair in eligible_seed_pairs()
        if closure.branch(pair) == "finite_strict_invariant"
    )


@lru_cache(maxsize=1)
def deficiency_zero_seed_pairs() -> frozenset[Pair]:
    return frozenset(
        pair
        for pair in eligible_seed_pairs()
        if closure.branch(pair) == "full_deficiency_zero"
    )


@lru_cache(maxsize=1)
def physical_seam_seed_pairs() -> frozenset[Pair]:
    seam_branches = {
        "exact_seven_support_seam",
        "exact_signed_service_seam",
        "exact_residual_pair",
    }
    return frozenset(
        pair
        for pair in eligible_seed_pairs()
        if closure.branch(pair) in seam_branches
    )


@lru_cache(maxsize=1)
def tier_pass_seed_pairs() -> frozenset[Pair]:
    positive_passed, _positive_failed = corrected_tier.tier_split(
        closure.POSITIVE_SHIELDED_MASKS
    )
    signed_passed, _signed_failed = corrected_tier.tier_split(
        closure.SIGNED_SHIELDED_MASKS
    )
    return positive_passed | signed_passed


@lru_cache(maxsize=1)
def residual_seed_pairs() -> frozenset[Pair]:
    _positive, _signed, residual = residual_union.corrected_baseline()
    return residual


@lru_cache(maxsize=1)
def seed_branches() -> dict[str, frozenset[Pair]]:
    return {
        "strict_positive_invariant": strict_invariant_seed_pairs(),
        "deficiency_zero": deficiency_zero_seed_pairs(),
        "literal_physical_seams": physical_seam_seed_pairs(),
        "corrected_tier_pass": tier_pass_seed_pairs(),
        "audited_residual_union": residual_seed_pairs(),
    }


def branch_manifest() -> list[dict[str, object]]:
    return [
        {
            "branch": name,
            "pairs": len(pairs),
            "sha256": closure.pair_fingerprint(pairs),
        }
        for name, pairs in seed_branches().items()
    ]


@lru_cache(maxsize=1)
def certificate() -> dict[str, object]:
    dependencies = dependency_sha256()
    seeds = orbit_gap.inherited_seed_pairs()
    active = orbit_gap.active_invariant_seed_pairs()
    eligible = eligible_seed_pairs()
    selected = seed_branches()
    branch_sets = tuple(selected.values())
    seed_union = frozenset().union(*branch_sets)
    orbit = orbit_gap.pair_orbit(eligible)

    assert dependencies == EXPECTED_DEPENDENCY_SHA256
    residual_union.verify_exact_dependencies()
    assert len(seeds) == 5_169
    assert len(active) == 110
    assert len(eligible) == 5_059
    assert not active & eligible
    assert active | eligible == seeds

    expected_counts = {
        "strict_positive_invariant": 187,
        "deficiency_zero": 974,
        "literal_physical_seams": 9,
        "corrected_tier_pass": 1_378,
        "audited_residual_union": 2_511,
    }
    assert {name: len(pairs) for name, pairs in selected.items()} == expected_counts
    for index, first in enumerate(branch_sets):
        for second in branch_sets[index + 1 :]:
            assert not first & second
    assert seed_union == eligible
    assert len(orbit) == 27_462
    assert orbit == orbit_gap.other_seed_orbit()

    fingerprints = {
        "eligible": closure.pair_fingerprint(eligible),
        "strict": closure.pair_fingerprint(selected["strict_positive_invariant"]),
        "dz": closure.pair_fingerprint(selected["deficiency_zero"]),
        "seams": closure.pair_fingerprint(selected["literal_physical_seams"]),
        "tier": closure.pair_fingerprint(selected["corrected_tier_pass"]),
        "residual": closure.pair_fingerprint(selected["audited_residual_union"]),
        "orbit": closure.pair_fingerprint(orbit),
    }
    expected_fingerprints = {
        "eligible": EXPECTED_ELIGIBLE_SEED_SHA256,
        "strict": EXPECTED_STRICT_SEED_SHA256,
        "dz": EXPECTED_DZ_SEED_SHA256,
        "seams": EXPECTED_PHYSICAL_SEAM_SEED_SHA256,
        "tier": EXPECTED_TIER_PASS_SEED_SHA256,
        "residual": EXPECTED_RESIDUAL_SEED_SHA256,
        "orbit": EXPECTED_OTHER_ORBIT_SHA256,
    }
    assert fingerprints == expected_fingerprints

    manifest = branch_manifest()
    assert _digest(manifest) == EXPECTED_BRANCH_MANIFEST_SHA256
    return {
        "claim_scope": (
            "finite support, corrected-tier, seed-partition, and symmetry-orbit "
            "identities only; no stochastic recurrence claim"
        ),
        "recurrence_claim": False,
        "orientation_rate_population_or_history_enumeration": False,
        "dependency_sha256": dependencies,
        "inherited_seed_pairs": len(seeds),
        "excluded_active_invariant_seeds": len(active),
        "eligible_seed_pairs": len(eligible),
        "eligible_seed_sha256": fingerprints["eligible"],
        "branch_manifest": manifest,
        "branch_manifest_sha256": _digest(manifest),
        "eligible_seed_partition_exact": seed_union == eligible,
        "other_mixed_orbit_pairs": len(orbit),
        "other_mixed_orbit_sha256": fingerprints["orbit"],
    }


def main() -> None:
    print(json.dumps(certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
