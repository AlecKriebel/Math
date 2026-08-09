from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random
import sys

from .episode_bounds import scalar_envelope_branch, target_following_path_probability
from .network import Channel, Network, falling_factorial
from .target_augmented import (
    direct_exp_increment,
    entropy_rewrite_signature,
    exp_potential_increment,
    expected_increment_signature,
    source_probabilities,
)
from .top_complex_dichotomy import (
    TopClassification,
    classify_top_complexes,
    validate_top_classification,
)

SEED = 20260806

# Only these mathematical sources, tests, and release instructions contribute
# to the stable report.  Generated reports, caches, installation metadata, and
# historical transcripts are deliberately outside this closed allowlist.
SOURCE_FILES = (
    "CITATION.cff",
    "LICENSE",
    "README.md",
    "build_backend.py",
    "pyproject.toml",
    "reproduce.sh",
    "src/bimolecular_pr/__init__.py",
    "src/bimolecular_pr/episode_bounds.py",
    "src/bimolecular_pr/network.py",
    "src/bimolecular_pr/target_augmented.py",
    "src/bimolecular_pr/top_complex_dichotomy.py",
    "src/bimolecular_pr/verification.py",
    "tests/test_boundary_lattice.py",
    "tests/test_episode.py",
    "tests/test_network.py",
    "tests/test_top_complex.py",
    "tests/test_verification.py",
)

# These values came from certificate-validated runs and are now fixed.  Every
# subsequent run must reproduce them exactly.
EXPECTED_THREE_SPECIES_ATLAS: dict[str, object] = {
    "complexes": 10,
    "complex_subsets": 1013,
    "normalized_weights": 55,
    "weight_divergent_pairs": 97,
    "cases": 98261,
    "case_counts": {
        "all_top_invariant": 1423,
        "service_availability": 2436,
        "signed_invariant": 288,
        "two_divergent_availability": 86373,
        "unary_top_availability": 7741,
    },
    "sha256": "6bc68fa9ffa0643e3ad4356b02d40839bb8cee28ed0fac026eb6b65881cedf27",
}
EXPECTED_SEEDED_RANDOM_TOP: dict[str, object] = {
    "cases": 5000,
    "case_counts": {
        "all_top_invariant": 87,
        "service_availability": 34,
        "signed_invariant": 21,
        "two_divergent_availability": 4640,
        "unary_top_availability": 218,
    },
    "sha256": "4974d6213318ea627ae4dcec955d9f4d4c192a3c38a96c66504501cff63ea2d1",
}


def canonical(data: object) -> bytes:
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode() + b"\n"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _verification_source_files(root: Path) -> set[str]:
    fixed = {
        "CITATION.cff",
        "LICENSE",
        "README.md",
        "build_backend.py",
        "pyproject.toml",
        "reproduce.sh",
    }
    discovered = fixed.copy()
    for directory in (root / "src", root / "tests"):
        if directory.is_dir():
            discovered.update(
                str(path.relative_to(root))
                for path in directory.rglob("*.py")
                if "__pycache__" not in path.parts
            )
    return discovered


def source_hashes(root: Path) -> dict[str, str]:
    """Hash exactly the closed, explicit verifier source allowlist."""
    expected = set(SOURCE_FILES)
    discovered = _verification_source_files(root)
    missing = sorted(expected - discovered)
    unexpected = sorted(discovered - expected)
    if missing or unexpected:
        raise AssertionError(
            f"source allowlist mismatch; missing={missing}, unexpected={unexpected}"
        )
    return {relative: file_hash(root / relative) for relative in SOURCE_FILES}


def binary_complexes(dimension: int) -> tuple[tuple[int, ...], ...]:
    out = [tuple(0 for _ in range(dimension))]
    for i in range(dimension):
        unary = [0] * dimension
        unary[i] = 1
        out.append(tuple(unary))
        pure_binary = [0] * dimension
        pure_binary[i] = 2
        out.append(tuple(pure_binary))
    for i in range(dimension):
        for j in range(i + 1, dimension):
            mixed = [0] * dimension
            mixed[i] = mixed[j] = 1
            out.append(tuple(mixed))
    return tuple(out)


def exact_identity_checks() -> int:
    """Check the factorial increment identity over sources, targets, outcomes."""
    count = 0
    complexes = binary_complexes(2)
    for state in itertools.product(range(5), repeat=2):
        enabled = [y for y in complexes if falling_factorial(state, y) > 0]
        for carried_target in enabled:
            for source in enabled:
                for outcome in complexes:
                    channel = Channel(source, outcome, Fraction(1), "identity-check")
                    direct = direct_exp_increment(state, carried_target, channel)
                    ratio = exp_potential_increment(state, carried_target, source)
                    if direct != ratio:
                        raise AssertionError("residual factorial identity failed")
                    count += 1
    return count


def _entropy_networks() -> tuple[Network, ...]:
    complexes = binary_complexes(2)
    cycle_channels = []
    for index, source in enumerate(complexes):
        target = complexes[(index + 1) % len(complexes)]
        cycle_channels.append(
            Channel(
                source,
                target,
                Fraction(index + 2, (index % 3) + 1),
                f"cycle-{index}",
            )
        )
    # A genuine parallel channel ensures bar-kappa aggregation is tested.
    cycle_channels.append(
        Channel(complexes[0], complexes[1], Fraction(5, 7), "parallel-zero")
    )
    canonical_cycle = Network(
        ("A", "B"),
        (
            Channel((0, 0), (1, 1), Fraction(2, 3), "trigger"),
            Channel((1, 1), (0, 1), Fraction(5, 4), "drain"),
            Channel((0, 1), (0, 0), Fraction(7, 5), "reset"),
        ),
    )
    return Network(("A", "B"), tuple(cycle_channels)), canonical_cycle


def exact_entropy_checks() -> int:
    """Compare both sides of the entropy rewrite as exact log signatures."""
    count = 0
    for network in _entropy_networks():
        for state in itertools.product(range(5), repeat=2):
            for target in source_probabilities(network, state):
                left = expected_increment_signature(network, state, target)
                right = entropy_rewrite_signature(network, state, target)
                if left != right:
                    raise AssertionError(
                        f"entropy identity failed at state={state}, target={target}"
                    )
                count += 1
    return count


def exact_scalar_checks() -> int:
    count = 0
    for q in [Fraction(1, 7), Fraction(1, 2), Fraction(1), Fraction(3, 2)]:
        threshold = -Fraction(1, 1) / q
        trial_values = [
            threshold - 3,
            threshold - Fraction(1, 2),
            threshold,
            threshold + Fraction(1, 2),
            Fraction(0),
            Fraction(4),
        ]
        for value in trial_values:
            branch = scalar_envelope_branch(q, value)
            if value >= threshold:
                if branch.branch != "endpoint" or branch.maximizer != 1:
                    raise AssertionError("incorrect endpoint scalar-envelope branch")
            elif branch.branch != "interior" or not 0 < branch.maximizer < 1:
                raise AssertionError("incorrect interior scalar-envelope branch")
            count += 1
    return count


def _fraction_record(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def _certificate_record(certificate: TopClassification) -> object:
    if certificate.case in {
        "two_divergent_availability",
        "unary_top_availability",
    }:
        source, terminal = certificate.witness
        return {"source": list(source), "terminal": list(terminal)}
    if certificate.case == "service_availability":
        source, terminal, service = certificate.witness
        return {
            "source": list(source),
            "terminal": list(terminal),
            "service": service,
        }
    if certificate.case == "K_mass_invariant":
        return {"indices": sorted(certificate.witness)}
    return {"vector": [_fraction_record(Fraction(v)) for v in certificate.witness]}


def _finite_weight_atlas() -> tuple[tuple[Fraction, ...], ...]:
    weights: set[tuple[Fraction, ...]] = set()
    for total in range(1, 7):
        for first in range(total + 1):
            for second in range(total - first + 1):
                third = total - first - second
                weights.add(
                    (
                        Fraction(first, total),
                        Fraction(second, total),
                        Fraction(third, total),
                    )
                )
    return tuple(sorted(weights))


def _divergent_supersets(weight: tuple[Fraction, ...]) -> tuple[frozenset[int], ...]:
    support = frozenset(i for i, value in enumerate(weight) if value > 0)
    zero_indices = tuple(i for i, value in enumerate(weight) if value == 0)
    out = []
    for mask in range(1 << len(zero_indices)):
        slower_tiers = {
            index for bit, index in enumerate(zero_indices) if mask & (1 << bit)
        }
        out.append(frozenset(set(support) | slower_tiers))
    return tuple(out)


def _compute_three_species_atlas() -> dict[str, object]:
    """Exhaust every nontrivial 3-species subset over a rational weight atlas."""
    complexes = binary_complexes(3)
    weights = _finite_weight_atlas()
    counts: Counter[str] = Counter()
    digest = hashlib.sha256()
    cases = 0

    for size in range(2, len(complexes) + 1):
        for subset in itertools.combinations(complexes, size):
            for weight in weights:
                for divergent in _divergent_supersets(weight):
                    result = classify_top_complexes(subset, weight, divergent)
                    validate_top_classification(subset, weight, divergent, result)
                    record = {
                        "complexes": [list(y) for y in subset],
                        "weight": [_fraction_record(value) for value in weight],
                        "divergent": sorted(divergent),
                        "case": result.case,
                        "top": [list(y) for y in result.top],
                        "certificate": _certificate_record(result),
                    }
                    digest.update(canonical(record))
                    counts[result.case] += 1
                    cases += 1

    return {
        "complexes": len(complexes),
        "complex_subsets": sum(
            1 for size in range(2, len(complexes) + 1)
            for _ in itertools.combinations(complexes, size)
        ),
        "normalized_weights": len(weights),
        "weight_divergent_pairs": sum(
            len(_divergent_supersets(weight)) for weight in weights
        ),
        "cases": cases,
        "case_counts": dict(sorted(counts.items())),
        "sha256": digest.hexdigest(),
    }


def deterministic_top_atlas() -> dict[str, object]:
    result = _compute_three_species_atlas()
    if result != EXPECTED_THREE_SPECIES_ATLAS:
        raise AssertionError(
            "three-species atlas differs from the fixed validated result: "
            f"{result!r}"
        )
    return result


def _compute_seeded_random_top() -> dict[str, object]:
    rng = random.Random(SEED)
    complexes = binary_complexes(4)
    digest = hashlib.sha256()
    counts: Counter[str] = Counter()
    cases = 5000
    for _ in range(cases):
        size = rng.randint(2, min(8, len(complexes)))
        subset = tuple(sorted(rng.sample(complexes, size)))
        raw = [rng.randint(0, 7) for _ in range(4)]
        if sum(raw) == 0:
            raw[rng.randrange(4)] = 1
        total = sum(raw)
        weight = tuple(Fraction(value, total) for value in raw)
        divergent = frozenset(
            i for i in range(4) if rng.random() < 0.6 or weight[i] > 0
        )
        result = classify_top_complexes(subset, weight, divergent)
        validate_top_classification(subset, weight, divergent, result)
        record = {
            "complexes": [list(y) for y in subset],
            "weight": [_fraction_record(value) for value in weight],
            "divergent": sorted(divergent),
            "case": result.case,
            "top": [list(y) for y in result.top],
            "certificate": _certificate_record(result),
        }
        digest.update(canonical(record))
        counts[result.case] += 1
    return {
        "cases": cases,
        "case_counts": dict(sorted(counts.items())),
        "sha256": digest.hexdigest(),
    }


def seeded_random_top() -> dict[str, object]:
    result = _compute_seeded_random_top()
    if result != EXPECTED_SEEDED_RANDOM_TOP:
        raise AssertionError(
            "seeded four-species stress test differs from its fixed result: "
            f"{result!r}"
        )
    return result


def calibrations() -> dict[str, bool]:
    zero = (0, 0)
    a = (1, 0)
    b = (0, 1)
    ab = (1, 1)
    canonical_network = Network(
        ("A", "B"),
        (
            Channel(zero, ab, Fraction(1), "trigger"),
            Channel(ab, b, Fraction(2), "drain"),
            Channel(b, zero, Fraction(3), "reset"),
        ),
    )
    parallel = Network(
        ("A",),
        (
            Channel((0,), (1,), Fraction(2), "p1"),
            Channel((0,), (1,), Fraction(3), "p2"),
            Channel((2,), (1,), Fraction(1), "down"),
        ),
    ).combined_parallel()
    same_displacement = Network(
        ("A", "B"),
        (
            Channel((1, 0), (0, 1), Fraction(1), "one"),
            Channel((2, 0), (1, 1), Fraction(1), "two"),
            Channel((0, 1), (1, 0), Fraction(1), "back1"),
            Channel((1, 1), (2, 0), Fraction(1), "back2"),
        ),
    ).combined_parallel()
    equal_molecularity = Network(
        ("A", "B"),
        (
            Channel(a, b, Fraction(2), "forward"),
            Channel(b, a, Fraction(3), "backward"),
        ),
    )
    equal_probabilities = source_probabilities(equal_molecularity, (3, 3))
    finite_class = {(1, 0), (0, 1)}
    finite_class_closed = all(
        equal_molecularity.successor(state, channel) in finite_class
        for state in finite_class
        for channel in equal_molecularity.enabled_channels(state)
    )
    absorbing_network = Network(
        ("A",),
        (
            Channel((1,), (2,), Fraction(1), "birth"),
            Channel((2,), (1,), Fraction(1), "death"),
        ),
    )
    target_following_zero = all(
        direct_exp_increment(channel.source, channel.source, channel) == 1
        for channel in canonical_network.channels
    )
    checks = {
        "absorbing_zero_state_has_no_enabled_channel": (
            absorbing_network.enabled_channels((0,)) == ()
        ),
        "canonical_cycle_binary": canonical_network.is_binary,
        "canonical_cycle_strongly_connected": canonical_network.strongly_connected(),
        "canonical_cycle_target_following_increments_zero": target_following_zero,
        "equal_molecularity_source_probabilities": (
            equal_probabilities == {a: Fraction(2, 5), b: Fraction(3, 5)}
        ),
        "finite_molecularity_one_class_closed": finite_class_closed,
        "parallel_combination_rate": any(
            channel.source == (0,)
            and channel.target == (1,)
            and channel.rate == 5
            for channel in parallel.channels
        ),
        "same_displacement_channels_retained": len(same_displacement.channels) == 4,
        "zero_complex_falling_factorial_is_one": falling_factorial((0, 0), zero) == 1,
        "zero_length_path_probability_is_one": target_following_path_probability([]) == 1,
    }
    return checks


def build_report(root: Path) -> dict[str, object]:
    checks = calibrations()
    if not all(checks.values()):
        failed = sorted(name for name, passed in checks.items() if not passed)
        raise AssertionError(f"calibration failure: {failed}")
    return {
        "schema_version": 2,
        "package_version": "0.3.0",
        "status": "pass",
        "python_required": ">=3.11",
        "classification": {
            "exact_symbolic_or_combinatorial": [
                "falling-factorial residual identities",
                "source-probability entropy identity via rational prime signatures",
                "scalar-envelope branch conditions",
                "exhaustive certificate-validated three-species top-complex atlas",
                "boundary, finite-class, channel, and target-following calibrations",
            ],
            "floating_numerical_calibrations": [],
            "seeded_stress_tests_not_used_as_proof": [
                "certificate-validated random four-species top-complex classifications"
            ],
        },
        "fixed_random_seeds": {"random_four_species": SEED},
        "stable_checks": {
            "exact_factorial_checks": exact_identity_checks(),
            "exact_entropy_signature_checks": exact_entropy_checks(),
            "exact_scalar_branch_checks": exact_scalar_checks(),
            "three_species_top_atlas": deterministic_top_atlas(),
            "seeded_random_top": seeded_random_top(),
            "calibrations": checks,
        },
        "source_sha256": source_hashes(root),
    }


def build_provenance(stable_report: Path) -> dict[str, object]:
    """Return environment metadata kept outside the deterministic report."""
    return {
        "schema_version": 1,
        "stable_report_sha256": file_hash(stable_report),
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provenance-output", type=Path)
    args = parser.parse_args()

    report = build_report(args.root.resolve())
    args.output.write_bytes(canonical(report))
    if args.provenance_output is not None:
        args.provenance_output.write_bytes(canonical(build_provenance(args.output)))
    print(
        json.dumps(
            {
                "python": ".".join(map(str, sys.version_info[:3])),
                "sha256": file_hash(args.output),
                "status": "pass",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
