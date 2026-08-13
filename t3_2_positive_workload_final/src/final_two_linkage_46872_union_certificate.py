"""Exact support-set union for the final two-linkage theorem.

The universe consists of ordered pairs of disjoint nontrivial supports in
the ten three-species binary complexes.  This certificate proves only a
finite set identity.  It does not enumerate orientations, rate vectors,
population states, stochastic histories, or communicating classes, and it
makes no recurrence claim.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

import active_invariant_orbit_gap_432_certificate as orbit_gap
import all_active_residual_levelset_336_certificate as levelset
import global_atlas_interface_closure as closure
import outside_mixed_remaining_18496_certificate as remainder


Pair = closure.Pair

EXPECTED_DEPENDENCY_SHA256 = {
    "active_invariant_orbit_gap_432_certificate.py": (
        "31fa24a20e18546e9c623d3aaf6d3b845c1708d5782f86333c02417fa366cd53"
    ),
    "all_active_residual_levelset_336_certificate.py": (
        "4149b682d1222bd3327548b0eb95921f7aae20663816b345b48285239c12f93d"
    ),
    "global_atlas_interface_closure.py": (
        "293a63711f6da152edd72615d27fad5bbb859aa33a4b7eb150673b27ae3cb5bd"
    ),
    "outside_mixed_remaining_18496_certificate.py": (
        "314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63"
    ),
}

EXPECTED_UNIVERSE_SHA256 = (
    "00446e17dca5ce6b75e86cdc755b5660d7c94b68fa4f3e6f028efa40d02c6c60"
)
EXPECTED_OTHER_MIXED_ORBIT_SHA256 = (
    "1bf337cf143c6eb4cee5088827bb9e9b9cec704f01a1b1f57bde6aed856d2812"
)
EXPECTED_ACTIVE_ORBIT_GAP_SHA256 = orbit_gap.EXPECTED_GAP_PAIR_SHA256
EXPECTED_STRICT_INVARIANT_SHA256 = (
    "d1fc7112f8a08605ef4dc33b664bce47c765e5c49b7496433e53a22bb62a087c"
)
EXPECTED_LEVELSET_SHA256 = (
    "ea3d7b08d39c6f9cc4c5a15c9924a624a5ccb4a6a356724ecddea96aa18869ea"
)
EXPECTED_REMAINDER_SHA256 = remainder.EXPECTED_REMAINDER_PAIR_SHA256
EXPECTED_BRANCH_MANIFEST_SHA256 = (
    "bd6ae54bff3aed8fc4fedb9255fe0b7377a28dc67404d6a5bea41c6aa4ac1bba"
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
def all_pairs() -> frozenset[Pair]:
    return levelset.all_ordered_disjoint_pairs()


@lru_cache(maxsize=1)
def other_mixed_orbit_pairs() -> frozenset[Pair]:
    """Orbit of inherited seed pairs not routed by active-only invariance."""

    return orbit_gap.other_seed_orbit()


@lru_cache(maxsize=1)
def active_orbit_gap_pairs() -> frozenset[Pair]:
    return orbit_gap.exclusive_orbit_gap_pairs()


@lru_cache(maxsize=1)
def strict_invariant_pairs() -> frozenset[Pair]:
    """Outside-mixed pairs removed by a strictly positive invariant."""

    return (
        levelset.outside_mixed_atlas()
        - levelset.after_strictly_positive_invariant_branch()
    )


@lru_cache(maxsize=1)
def levelset_336_pairs() -> frozenset[Pair]:
    return remainder.levelset_pairs()


@lru_cache(maxsize=1)
def outside_mixed_remainder_pairs() -> frozenset[Pair]:
    return remainder.remainder_pairs()


@lru_cache(maxsize=1)
def branches() -> dict[str, frozenset[Pair]]:
    return {
        "other_mixed_orbit": other_mixed_orbit_pairs(),
        "active_orbit_gap": active_orbit_gap_pairs(),
        "strict_positive_invariant": strict_invariant_pairs(),
        "levelset_residual": levelset_336_pairs(),
        "outside_mixed_remainder": outside_mixed_remainder_pairs(),
    }


def branch_manifest() -> list[dict[str, object]]:
    return [
        {
            "branch": name,
            "pairs": len(pairs),
            "sha256": closure.pair_fingerprint(pairs),
        }
        for name, pairs in branches().items()
    ]


@lru_cache(maxsize=1)
def certificate() -> dict[str, object]:
    dependencies = dependency_sha256()
    universe = all_pairs()
    selected = branches()
    branch_sets = tuple(selected.values())
    mixed = levelset.mixed_atlas_orbit()
    outside = levelset.outside_mixed_atlas()
    union = frozenset().union(*branch_sets)

    assert dependencies == EXPECTED_DEPENDENCY_SHA256
    assert len(universe) == 46_872
    assert closure.pair_fingerprint(universe) == EXPECTED_UNIVERSE_SHA256
    assert len(mixed) == 27_894
    assert len(outside) == 18_978
    assert mixed | outside == universe
    assert not mixed & outside

    expected_counts = {
        "other_mixed_orbit": 27_462,
        "active_orbit_gap": 432,
        "strict_positive_invariant": 146,
        "levelset_residual": 336,
        "outside_mixed_remainder": 18_496,
    }
    assert {name: len(pairs) for name, pairs in selected.items()} == expected_counts
    assert closure.pair_fingerprint(selected["other_mixed_orbit"]) == (
        EXPECTED_OTHER_MIXED_ORBIT_SHA256
    )
    assert closure.pair_fingerprint(selected["active_orbit_gap"]) == (
        EXPECTED_ACTIVE_ORBIT_GAP_SHA256
    )
    assert closure.pair_fingerprint(selected["strict_positive_invariant"]) == (
        EXPECTED_STRICT_INVARIANT_SHA256
    )
    assert closure.pair_fingerprint(selected["levelset_residual"]) == (
        EXPECTED_LEVELSET_SHA256
    )
    assert closure.pair_fingerprint(selected["outside_mixed_remainder"]) == (
        EXPECTED_REMAINDER_SHA256
    )

    for index, first in enumerate(branch_sets):
        for second in branch_sets[index + 1 :]:
            assert not first & second
    assert union == universe

    assert (
        selected["other_mixed_orbit"] | selected["active_orbit_gap"]
        == mixed
    )
    assert (
        selected["strict_positive_invariant"]
        | selected["levelset_residual"]
        | selected["outside_mixed_remainder"]
        == outside
    )
    assert remainder.no_failure_pairs() | remainder.failed_pairs() == (
        selected["outside_mixed_remainder"]
    )
    assert not remainder.no_failure_pairs() & remainder.failed_pairs()

    manifest = branch_manifest()
    assert _digest(manifest) == EXPECTED_BRANCH_MANIFEST_SHA256
    return {
        "claim_scope": (
            "finite ordered-support set identity only; no orientation, rate, "
            "population, history, class, or recurrence claim"
        ),
        "recurrence_claim": False,
        "orientation_rate_population_or_history_enumeration": False,
        "dependency_sha256": dependencies,
        "ordered_disjoint_support_pairs": len(universe),
        "universe_sha256": closure.pair_fingerprint(universe),
        "mixed_orbit_pairs": len(mixed),
        "outside_mixed_pairs": len(outside),
        "branch_manifest": manifest,
        "branch_manifest_sha256": _digest(manifest),
        "outside_mixed_remainder_split": {
            "no_failure": len(remainder.no_failure_pairs()),
            "failure": len(remainder.failed_pairs()),
            "no_failure_sha256": closure.pair_fingerprint(
                remainder.no_failure_pairs()
            ),
            "failure_sha256": closure.pair_fingerprint(remainder.failed_pairs()),
        },
        "pairwise_disjoint": True,
        "union_equals_universe": True,
    }


def main() -> None:
    print(json.dumps(certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
