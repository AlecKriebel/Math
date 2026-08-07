from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

from .episode_bounds import scalar_envelope_branch
from .network import Channel, Network, falling_factorial
from .target_augmented import direct_exp_increment, exp_potential_increment
from .top_complex_dichotomy import classify_top_complexes

SEED = 20260806


def canonical(data: object) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode() + b"\n"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes(root: Path) -> dict[str, str]:
    excluded = {"verification_report.json"}
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name in excluded or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.name.startswith(".verification_run_") or ".egg-info" in "".join(path.parts):
            continue
        result[str(path.relative_to(root))] = file_hash(path)
    return result


def binary_complexes(d: int) -> tuple[tuple[int, ...], ...]:
    out = [tuple(0 for _ in range(d))]
    for i in range(d):
        v = [0] * d; v[i] = 1; out.append(tuple(v))
        v = [0] * d; v[i] = 2; out.append(tuple(v))
    for i in range(d):
        for j in range(i + 1, d):
            v = [0] * d; v[i] = v[j] = 1; out.append(tuple(v))
    return tuple(out)


def exact_identity_checks() -> int:
    count = 0
    complexes = binary_complexes(2)
    for x in itertools.product(range(5), repeat=2):
        enabled = [y for y in complexes if falling_factorial(x, y) > 0]
        for t in enabled:
            for s in enabled:
                ch = Channel(s, t, Fraction(1), "check")
                if direct_exp_increment(x, t, ch) != exp_potential_increment(x, t, s):
                    raise AssertionError("residual factorial identity failed")
                count += 1
    return count


def exact_scalar_checks() -> int:
    count = 0
    for q in [Fraction(1, 7), Fraction(1, 2), Fraction(1), Fraction(3, 2)]:
        threshold = -Fraction(1, 1) / q
        for M in [threshold - 3, threshold - Fraction(1, 2), threshold, threshold + Fraction(1, 2), Fraction(0), Fraction(4)]:
            branch = scalar_envelope_branch(q, M)
            if M >= threshold:
                assert branch.branch == "endpoint" and branch.maximizer == 1
            else:
                assert branch.branch == "interior" and 0 < branch.maximizer < 1
            count += 1
    return count


def deterministic_top_atlas() -> tuple[int, str]:
    complexes = binary_complexes(3)
    weights = [
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(1, 2), Fraction(1, 2), Fraction(0)),
        (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)),
        (Fraction(2, 3), Fraction(0), Fraction(1, 3)),
    ]
    lines: list[str] = []
    count = 0
    # Exhaustive subsets of sizes 2--5, enough to attack every finite case type.
    for size in range(2, 6):
        for subset in itertools.combinations(complexes, size):
            for w in weights:
                divergent = frozenset(i for i, wi in enumerate(w) if wi > 0)
                result = classify_top_complexes(subset, w, divergent)
                lines.append(f"{subset}|{w}|{result.case}|{result.witness}")
                count += 1
    digest = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    return count, digest


def seeded_random_top() -> tuple[int, str]:
    rng = random.Random(SEED)
    complexes = binary_complexes(4)
    lines: list[str] = []
    for _ in range(5000):
        size = rng.randint(2, min(8, len(complexes)))
        subset = tuple(sorted(rng.sample(complexes, size)))
        raw = [rng.randint(0, 7) for _ in range(4)]
        if sum(raw) == 0:
            raw[rng.randrange(4)] = 1
        total = sum(raw)
        w = tuple(Fraction(a, total) for a in raw)
        divergent = frozenset(i for i in range(4) if rng.random() < 0.6 or w[i] > 0)
        divergent |= frozenset(i for i, wi in enumerate(w) if wi > 0)
        result = classify_top_complexes(subset, w, divergent)
        lines.append(f"{subset}|{w}|{sorted(divergent)}|{result.case}")
    return len(lines), hashlib.sha256("\n".join(lines).encode()).hexdigest()


def calibrations() -> dict[str, bool]:
    zero = (0, 0); a = (1, 0); b = (0, 1); ab = (1, 1)
    canonical_net = Network(("A", "B"), (
        Channel(zero, ab, Fraction(1), "trigger"),
        Channel(ab, b, Fraction(2), "drain"),
        Channel(b, zero, Fraction(3), "reset"),
    ))
    parallel = Network(("A",), (
        Channel((0,), (1,), Fraction(2), "p1"),
        Channel((0,), (1,), Fraction(3), "p2"),
        Channel((2,), (1,), Fraction(1), "down"),
    )).combined_parallel()
    same_displacement = Network(("A", "B"), (
        Channel((1,0), (0,1), Fraction(1), "one"),
        Channel((2,0), (1,1), Fraction(1), "two"),
        Channel((0,1), (1,0), Fraction(1), "back1"),
        Channel((1,1), (2,0), Fraction(1), "back2"),
    )).combined_parallel()
    return {
        "canonical_binary": canonical_net.is_binary,
        "canonical_strongly_connected": canonical_net.strongly_connected(),
        "equal_molecularity_binary": Network(("A","B"), (Channel(a,b,Fraction(1)), Channel(b,a,Fraction(1)))).is_binary,
        "parallel_combination_rate": any(c.source == (0,) and c.target == (1,) and c.rate == 5 for c in parallel.channels),
        "same_displacement_channels_retained": len(same_displacement.channels) == 4,
    }


def build_report(root: Path) -> dict[str, object]:
    atlas_count, atlas_hash = deterministic_top_atlas()
    random_count, random_hash = seeded_random_top()
    checks = calibrations()
    if not all(checks.values()):
        raise AssertionError("calibration failure")
    return {
        "schema_version": 1,
        "package_version": "0.2.0",
        "status": "pass",
        "python_required": ">=3.11",
        "tested_python": ".".join(map(str, sys.version_info[:3])),
        "classification": {
            "exact_symbolic_or_combinatorial": [
                "falling-factorial residual identities",
                "scalar-envelope branch conditions",
                "deterministic top-complex atlas",
                "channel-combination calibrations",
            ],
            "floating_numerical_calibrations": [],
            "seeded_stress_tests_not_used_as_proof": ["random four-species top-complex classifications"],
        },
        "fixed_random_seeds": {"random_four_species": SEED},
        "stable_checks": {
            "exact_factorial_checks": exact_identity_checks(),
            "exact_scalar_branch_checks": exact_scalar_checks(),
            "deterministic_top_atlas_cases": atlas_count,
            "deterministic_top_atlas_sha256": atlas_hash,
            "seeded_random_top_cases": random_count,
            "seeded_random_top_sha256": random_hash,
            "calibrations": checks,
        },
        "source_sha256": source_hashes(root),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(args.root.resolve())
    args.output.write_bytes(canonical(report))
    print(json.dumps({"status": "pass", "sha256": file_hash(args.output)}, sort_keys=True))


if __name__ == "__main__":
    main()
