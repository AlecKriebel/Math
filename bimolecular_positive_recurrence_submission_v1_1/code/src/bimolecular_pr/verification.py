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

from .episode_bounds import (
    scalar_envelope_branch,
    scalar_envelope_pointwise_increment,
    target_following_path_probability,
)
from .network import Channel, Network, falling_factorial
from .publication_v1_calibrations import (
    absorbing_singleton_stationary,
    rate_degeneration_asymptotic_coefficient,
    rate_degeneration_episode,
    stopped_foster_increment,
    two_state_return_cycle_occupation,
)
from .publication_v1_1_calibrations import (
    ack_marked_target_episode,
    ack_marked_target_log_coefficient,
    ack_unshifted_entropy_drift,
    directed_cycle_return_occupation,
    rate_degeneration_fixed_m_limit,
)
from .state_cycle import (
    finite_accessibility_is_symmetric,
    finite_reachability,
    finite_transition_graph,
    lifted_return_cycle,
)
from .target_augmented import (
    add_weighted_signature,
    direct_exp_increment,
    entropy_rewrite_signature,
    exp_potential_increment,
    expected_increment_signature,
    rational_log_signature,
    source_probabilities,
)
from .top_complex_dichotomy import (
    INVARIANT_CASES,
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
    "src/bimolecular_pr/publication_v1_calibrations.py",
    "src/bimolecular_pr/publication_v1_1_calibrations.py",
    "src/bimolecular_pr/state_cycle.py",
    "src/bimolecular_pr/target_augmented.py",
    "src/bimolecular_pr/top_complex_dichotomy.py",
    "src/bimolecular_pr/verification.py",
    "tests/test_boundary_lattice.py",
    "tests/test_episode.py",
    "tests/test_network.py",
    "tests/test_publication_v1.py",
    "tests/test_publication_v1_1.py",
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
        for p in (Fraction(1, 11), Fraction(2, 3), Fraction(1)):
            increment = scalar_envelope_pointwise_increment(
                q,
                p,
                threshold - 5,
                threshold + 7,
            )
            if increment != 12 * q * p or increment < 0:
                raise AssertionError("scalar envelope is not pointwise nondecreasing")
            count += 1
    return count


def exact_state_cycle_checks() -> dict[str, int]:
    """Exercise the lifted-cycle interface and finite reachability symmetry."""
    zero_cycle = Network(
        ("A",),
        (
            Channel((0,), (1,), Fraction(2), "birth"),
            Channel((1,), (0,), Fraction(3), "death"),
        ),
    )
    multiple_linkages = Network(
        ("A", "B"),
        (
            Channel((1, 0), (0, 1), Fraction(2), "a_to_b_1"),
            Channel((1, 0), (0, 1), Fraction(5), "a_to_b_parallel"),
            Channel((0, 1), (1, 0), Fraction(3), "b_to_a"),
            Channel((2, 0), (1, 1), Fraction(7), "two_a_to_ab"),
            Channel((1, 1), (2, 0), Fraction(11), "ab_to_two_a"),
        ),
    )

    witnesses = 0
    for state in ((0,), (1,), (4,)):
        for channel in zero_cycle.enabled_channels(state):
            witness = lifted_return_cycle(zero_cycle, state, channel)
            if witness.states[0] != state or witness.states[-1] != state:
                raise AssertionError("zero-complex lifted cycle did not close")
            witnesses += 1
    for state in itertools.product(range(4), repeat=2):
        for channel in multiple_linkages.enabled_channels(state):
            witness = lifted_return_cycle(multiple_linkages, state, channel)
            if witness.states[-1] != state:
                raise AssertionError("multiple-linkage lifted cycle did not close")
            witnesses += 1

    parity_cycle = Network(
        ("A", "B"),
        (
            Channel((2, 0), (0, 2), Fraction(2), "forward"),
            Channel((0, 2), (2, 0), Fraction(3), "backward"),
        ),
    )
    shell = {(a, 6 - a) for a in range(7)}
    adjacency = finite_transition_graph(parity_cycle, shell)
    if not finite_accessibility_is_symmetric(adjacency):
        raise AssertionError("finite population accessibility was not symmetric")
    reachability_pairs = 0
    for initial in shell:
        reachable = finite_reachability(adjacency, initial)
        for state in reachable:
            if not adjacency[state] <= reachable:
                raise AssertionError("a finite reachability set was not closed")
        reachability_pairs += len(reachable)

    absorbing = Network(
        ("A",),
        (
            Channel((1,), (2,), Fraction(1), "up"),
            Channel((2,), (1,), Fraction(1), "down"),
        ),
    )
    singleton_graph = finite_transition_graph(absorbing, {(0,)})
    if finite_reachability(singleton_graph, (0,)) != {(0,)}:
        raise AssertionError("absorbing singleton was not its own reachability set")
    return {
        "lifted_edge_witnesses": witnesses,
        "finite_population_states": len(shell) + 1,
        "finite_reachability_pairs": reachability_pairs + 1,
    }


def _ack_network(rates: tuple[Fraction, ...]) -> Network:
    kappa_1, kappa_2, kappa_3, kappa_4, kappa_5 = rates
    return Network(
        ("A", "B", "C"),
        (
            Channel((1, 0, 0), (1, 1, 0), kappa_1, "r1"),
            Channel((1, 1, 0), (1, 0, 1), kappa_2, "r2"),
            Channel((1, 0, 1), (0, 0, 1), kappa_3, "r3"),
            Channel((0, 0, 1), (0, 2, 0), kappa_4, "r4"),
            Channel((0, 2, 0), (1, 0, 0), kappa_5, "r5"),
        ),
    )


def _ack_generic_episode_signature(network: Network, n: int) -> dict[int, Fraction]:
    phases = (
        ((n, 1, 0), (1, 0, 0), network.channels[0]),
        ((n, 2, 0), (1, 1, 0), network.channels[1]),
        ((n, 1, 1), (1, 0, 1), network.channels[2]),
        ((n - 1, 1, 1), (0, 0, 1), None),
    )
    signature: dict[int, Fraction] = {}
    reach_probability = Fraction(1)
    for state, target, designated in phases:
        add_weighted_signature(
            signature,
            expected_increment_signature(network, state, target),
            reach_probability,
        )
        if designated is not None:
            reach_probability *= (
                network.propensity(state, designated) / network.total_rate(state)
            )
    return signature


def _ack_closed_form_signature(
    rates: tuple[Fraction, ...],
    n: int,
) -> dict[int, Fraction]:
    episode = ack_marked_target_episode(n, *rates)
    signature: dict[int, Fraction] = {}
    for value, coefficient in (
        (2, episode.log2_coefficient),
        (n, episode.log_n_coefficient),
        (n - 1, episode.log_n_minus_one_coefficient),
    ):
        add_weighted_signature(
            signature,
            rational_log_signature(Fraction(value)),
            coefficient,
        )
    return signature


def exact_ack_example_checks() -> int:
    """Verify ACK Example 4.1's exact episode against the generic identity."""
    rate_sets = (
        (Fraction(1), Fraction(2), Fraction(3), Fraction(5), Fraction(7)),
        (
            Fraction(2, 3),
            Fraction(5, 4),
            Fraction(7, 6),
            Fraction(11, 5),
            Fraction(13, 7),
        ),
    )
    count = 0
    for rates in rate_sets:
        network = _ack_network(rates)
        for n in range(2, 13):
            if _ack_generic_episode_signature(network, n) != _ack_closed_form_signature(rates, n):
                raise AssertionError("ACK marked-target episode formula failed")
            count += 1
        coefficient = ack_marked_target_log_coefficient(*rates[:3])
        if coefficient >= 0:
            raise AssertionError("ACK episode lacks strict logarithmic restoration")
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
    degeneration = rate_degeneration_episode(
        7,
        Fraction(2, 3),
        Fraction(5, 4),
        Fraction(7, 6),
    )
    degeneration_limit = rate_degeneration_fixed_m_limit(
        7,
        Fraction(2, 3),
        Fraction(5, 4),
    )
    occupation = two_state_return_cycle_occupation(Fraction(2), Fraction(3))
    three_cycle_occupation = directed_cycle_return_occupation(
        (Fraction(2), Fraction(3), Fraction(5))
    )
    ack_drift = ack_unshifted_entropy_drift(11, Fraction(7, 5))
    all_qj_one = classify_top_complexes(
        ((1, 0, 0), (1, 1, 0), (1, 0, 1)),
        (Fraction(1), Fraction(0), Fraction(0)),
        frozenset({0}),
    )
    checks = {
        "absorbing_singleton_stationary_law_is_point_mass": (
            absorbing_singleton_stationary((0, 0)) == {(0, 0): Fraction(1)}
        ),
        "absorbing_zero_state_has_no_enabled_channel": (
            absorbing_network.enabled_channels((0,)) == ()
        ),
        "all_qJ_one_is_the_previously_handled_all_top_case": (
            all_qj_one.case == "all_top_invariant"
            and "K_mass_invariant" not in INVARIANT_CASES
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
        "rate_degeneration_finite_recursion_has_both_log_terms": (
            degeneration.log_m_coefficient > 0
            and degeneration.log_m_minus_one_coefficient < 0
            and degeneration.log_m_coefficient
            == degeneration.phase_a_increment_log_m
            + degeneration.continue_from_a
            * degeneration.phase_ab_increment_log_m
            and degeneration.log_m_minus_one_coefficient
            == degeneration.continue_from_a
            * degeneration.continue_from_ab
            * degeneration.terminal_increment_log_m_minus_one
        ),
        "rate_degeneration_log_coefficient_is_exact": (
            rate_degeneration_asymptotic_coefficient(Fraction(5), Fraction(2))
            == Fraction(-2, 7)
        ),
        "rate_degeneration_fixed_m_limit_is_a_times_one_plus_p": (
            degeneration_limit.limit_log_m_coefficient
            == degeneration_limit.a_log_m_coefficient
            * (1 + degeneration_limit.continue_from_a)
            and degeneration_limit.limit_log_m_coefficient > 0
            and degeneration_limit.limit_log_m_minus_one_coefficient == 0
        ),
        "ack_unshifted_entropy_generator_drift_is_exact": (
            ack_drift.log2_coefficient == Fraction(154, 5)
            and ack_drift.constant == Fraction(-77, 5)
        ),
        "same_displacement_channels_retained": len(same_displacement.channels) == 4,
        "stopped_foster_W_increment_is_nonpositive": (
            stopped_foster_increment(
                Fraction(2),
                (
                    (Fraction(1, 2), Fraction(0)),
                    (Fraction(1, 2), Fraction(2)),
                ),
            )
            <= 0
        ),
        "two_state_return_cycle_occupation_is_stationary": (
            occupation.stationary_0 == Fraction(3, 5)
            and occupation.stationary_1 == Fraction(2, 5)
            and occupation.stationary_0 * 2 == occupation.stationary_1 * 3
        ),
        "three_state_return_cycle_normalization_is_stationary": (
            three_cycle_occupation.expected_cycle_time == Fraction(31, 30)
            and sum(three_cycle_occupation.stationary, Fraction(0)) == 1
            and len(
                {
                    probability * rate
                    for probability, rate in zip(
                        three_cycle_occupation.stationary,
                        (Fraction(2), Fraction(3), Fraction(5)),
                    )
                }
            )
            == 1
        ),
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
        "package_version": "1.1.0",
        "status": "pass",
        "python_required": ">=3.11",
        "classification": {
            "exact_symbolic_or_combinatorial": [
                "falling-factorial residual identities",
                "source-probability entropy identity via rational prime signatures",
                "scalar-envelope branch conditions and pointwise monotonicity",
                "lifted population-state return cycles and finite reachability symmetry",
                "exhaustive certificate-validated three-species top-complex atlas",
                "rate-degeneration target-following recursion and asymptotic coefficient",
                "ACK Example 4.1 unshifted drift and marked-target episode",
                "random-time Foster, regenerative occupation, and absorbing-state calibrations",
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
            "exact_state_cycle_checks": exact_state_cycle_checks(),
            "exact_ack_example_checks": exact_ack_example_checks(),
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
