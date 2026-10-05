#!/usr/bin/env python3
"""Exact auxiliary controls and immutable-package verification; no theorem prover."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def compute_checks():
    def swap(n):
        return 1 if n == 0 else 0 if n == 1 else n

    pair_count = 0
    ratios = []
    for a, b in combinations(range(-20, 21), 2):
        assert swap(swap(a)) == a and swap(swap(b)) == b
        ratio = Fraction(abs(swap(a) - swap(b)), abs(a - b))
        assert Fraction(1, 2) <= ratio <= 2
        ratios.append(ratio)
        pair_count += 1
    assert (swap(-1), swap(0), swap(1)) == (-1, 1, 0)
    assert min(ratios) == Fraction(1, 2) and max(ratios) == 2

    counting_cases = 0
    for M in range(101):
        n = M + 1
        targets = (2 * n + 1) ** 2
        possible_preimages = (2 * ((n + M) // 2) + 1) ** 2
        upper_bound = (n + M + 1) ** 2
        assert possible_preimages <= upper_bound < targets
        counting_cases += 1

    translation_points = []
    for m in range(-4, 5):
        for n in range(-4, 5):
            d = (Fraction(m) + Fraction(1, 2), Fraction(n))
            a_d = (d[0] - Fraction(1, 2), d[1])
            assert a_d == (m, n)
            assert (a_d[0] + Fraction(1, 2), a_d[1]) == d
            translation_points.append((d, a_d))
    isometry_pairs = 0
    for (d1, z1), (d2, z2) in combinations(translation_points, 2):
        assert sum((x - y) ** 2 for x, y in zip(d1, d2)) == sum(
            (x - y) ** 2 for x, y in zip(z1, z2)
        )
        isometry_pairs += 1
    assert (-Fraction(1, 2)).denominator != 1  # 0 is not in Z²+(1/2,0).
    assert 1 % 2 != 0  # (1,0) is not in 2Z².

    # Arithmetic only: substitute the displayed upper bounds into DK Thm. 1.3.
    base_exponent = 84 + 39 * 52 + 200 * 54 + 41 * 30
    alpha_exponent = 15 * 52 + 77 * 54 + 16 * 30
    assert (base_exponent, alpha_exponent) == (14142, 5418)
    assert base_exponent <= 20000 and alpha_exponent <= 6000

    sources = json.loads((ROOT / "SOURCE_VERIFICATION.json").read_text())
    primary = next(s for s in sources["sources"] if s["id"] == "DK2026-published")
    assert primary["sha256"] == "4ba7e9055487079a3aa760bcd4a20953c44b4898f784e8103e3035919209af85"
    assert primary["bytes"] == 617569 and primary["pages"] == 34
    assert primary["public_status"] == "published"
    assert sources["resolution"]["classification"] == "already_solved"
    assert sources["resolution"]["campaign_approaches_used"] == 1
    assert sources["resolution"]["original_solution_credit"] == 0

    return {
        "adjacent_swap_pairs": pair_count,
        "adjacent_swap_min_distance_ratio": str(min(ratios)),
        "adjacent_swap_max_distance_ratio": str(max(ratios)),
        "bounded_displacement_counting_cases": counting_cases,
        "translation_inverse_points": len(translation_points),
        "translation_isometry_pairs": isometry_pairs,
        "published_bound_arithmetic": {
            "base_10_exponent_from_substitution": base_exponent,
            "alpha_exponent_from_substitution": alpha_exponent,
            "stated_base_10_exponent": 20000,
            "stated_alpha_exponent": 6000,
        },
        "source_metadata_consistency": "PASS",
        "limitations": "Exact auxiliary checks only; no computational proof of the published extension theorem or universal conclusions.",
    }


def verify_manifest():
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    records = manifest["files"]
    expected = {record["name"] for record in records}
    actual = {p.name for p in ROOT.iterdir() if p.is_file()}
    assert actual == expected | {"MANIFEST.json"}, (actual, expected)
    assert not any(p.is_dir() for p in ROOT.iterdir()), "Unexpected subdirectory"
    for record in records:
        p = ROOT / record["name"]
        assert p.parent == ROOT and not p.is_symlink()
        data = p.read_bytes()
        assert len(data) == record["bytes"], record["name"]
        assert hashlib.sha256(data).hexdigest() == record["sha256"], record["name"]
    return len(records)


if __name__ == "__main__":
    checks = compute_checks()
    assert checks == json.loads((ROOT / "CHECKS.json").read_text())
    count = verify_manifest()
    print(json.dumps({"checks": checks, "manifest_payload_files": count, "result": "PASS"}, indent=2, sort_keys=True))
