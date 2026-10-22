#!/usr/bin/env python3
"""Exact finite controls for Attempt 4. No search for an infinite counterexample."""
import json
from pathlib import Path


def valuation(a, p, n):
    a %= p ** n
    if a == 0:
        return n
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    return v


def check(p, n):
    modulus = p ** n
    units = [u for u in range(modulus) if u % p]
    group = [(b, u) for u in units for b in range(modulus)]

    def mul(x, y):
        b, u = x
        c, v = y
        return ((b + u * c) % modulus, (u * v) % modulus)

    def inv(x):
        b, u = x
        v = pow(u, -1, modulus)
        return ((-v * b) % modulus, v)

    identity = (0, 1)
    for x in group:
        assert mul(x, inv(x)) == identity == mul(inv(x), x)
    remaining = set(group)
    classes = []
    translation_sizes = {}
    for x in group:
        if x not in remaining:
            continue
        orbit = {mul(mul(g, x), inv(g)) for g in group}
        # Independently evaluate the explicit affine conjugation formula.
        formula_orbit = {
            ((v * x[0] + (1 - x[1]) * a) % modulus, x[1])
            for a, v in group
        }
        assert orbit == formula_orbit
        assert orbit <= remaining
        assert {y[1] for y in orbit} == {x[1]}
        remaining -= orbit
        classes.append(orbit)
        if x[1] == 1:
            k = valuation(x[0], p, n)
            assert {valuation(b, p, n) for b, _ in orbit} == {k}
            expected_size = 1 if k == n else (p - 1) * p ** (n-k-1)
            assert len(orbit) == expected_size
            translation_sizes[str(k)] = len(orbit)
    assert not remaining
    fixed_multiplier_counts = {
        u: sum(next(iter(orbit))[1] == u for orbit in classes) for u in units
    }
    for u, count in fixed_multiplier_counts.items():
        assert count == valuation(1-u, p, n) + 1
    predicted_total = len(units) + (modulus - 1) // (p - 1)
    assert len(classes) == predicted_total
    assert len(translation_sizes) == n + 1
    assert sum(translation_sizes.values()) == modulus
    return {
        "p": p,
        "n": n,
        "group_order": len(group),
        "conjugacy_classes": len(classes),
        "predicted_conjugacy_classes": predicted_total,
        "translation_classes_including_identity": n + 1,
        "translation_class_sizes_by_valuation": translation_sizes,
        "distinct_multiplier_images": len(units),
        "all_assertions_passed": True,
    }


def run():
    cases = [(2, n) for n in range(1, 6)]
    cases += [(3, n) for n in range(1, 4)]
    cases += [(5, n) for n in range(1, 3)]
    return {
        "scope": "Ten finite affine groups; exact enumeration, not an infinite-group certificate",
        "cases": [check(p, n) for p, n in cases],
    }


if __name__ == "__main__":
    result = run()
    target = Path(__file__).with_name("affine_results.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
