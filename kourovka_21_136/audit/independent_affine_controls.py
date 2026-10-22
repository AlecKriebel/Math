#!/usr/bin/env python3
"""Independent permutation-action audit; never writes into the frozen release."""
from pathlib import Path
import hashlib
import json
import math
import runpy


def run():
    root = Path(__file__).resolve().parent.parent / "frozen_original"
    manifest = json.loads((root / "MANIFEST.json").read_text())
    actual = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}
    expected = {item["path"] for item in manifest["files"]} | {"MANIFEST.json"}
    assert actual == expected
    for item in manifest["files"]:
        data = (root / item["path"]).read_bytes()
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
    original = runpy.run_path(str(root / "checks/affine_controls.py"))["run"]()
    assert original == json.loads((root / "checks/affine_results.json").read_text())
    rows = []
    cases = [(2, n) for n in range(1, 6)]
    cases += [(3, n) for n in range(1, 4)]
    cases += [(5, n) for n in range(1, 3)]
    for p, n in cases:
        modulus = p ** n
        units = [u for u in range(modulus) if math.gcd(u, modulus) == 1]
        permutations = {
            tuple((b + u * i) % modulus for i in range(modulus)): (b, u)
            for u in units for b in range(modulus)
        }
        group = list(permutations)
        assert len(group) == modulus * len(units)

        def compose(f, g):
            return tuple(f[g[i]] for i in range(modulus))

        def valuation(a):
            a %= modulus
            if a == 0:
                return n
            return next(j for j in range(n) if a % p ** (j + 1))

        inverses = {}
        for g in group:
            inverse = [0] * modulus
            for i, j in enumerate(g):
                inverse[j] = i
            inverses[g] = tuple(inverse)
        remaining = set(group)
        classes = []
        while remaining:
            x = min(remaining)
            orbit = {compose(compose(g, x), inverses[g]) for g in group}
            assert orbit <= remaining
            remaining -= orbit
            classes.append(orbit)
        by_multiplier = {u: 0 for u in units}
        translation_sizes = {}
        for orbit in classes:
            pairs = {permutations[x] for x in orbit}
            multipliers = {x[1] for x in pairs}
            assert len(multipliers) == 1
            u = next(iter(multipliers))
            by_multiplier[u] += 1
            b = next(iter(pairs))[0]
            if u == 1:
                k = valuation(b)
                assert {valuation(t) for t, _ in pairs} == {k}
                translation_sizes[str(k)] = len(pairs)
            assert pairs == {
                ((v * b + (1 - u) * a) % modulus, u)
                for a in range(modulus) for v in units
            }
        assert all(by_multiplier[u] == 1 + valuation(1 - u) for u in units)
        expected_row = next(
            row for row in original["cases"] if (row["p"], row["n"]) == (p, n)
        )
        assert len(classes) == expected_row["conjugacy_classes"]
        assert len(classes) == len(units) + (modulus - 1) // (p - 1)
        assert translation_sizes == expected_row["translation_class_sizes_by_valuation"]
        commuting_pairs = sum(
            compose(g, h) == compose(h, g) for g in group for h in group
        )
        assert commuting_pairs == len(classes) * len(group)
        rows.append({
            "p": p, "n": n, "order": len(group), "classes": len(classes),
            "commuting_ordered_pairs": commuting_pairs,
            "translation_class_sizes_by_valuation": translation_sizes,
            "all_assertions_passed": True,
        })
    return {
        "manifest_sha256": hashlib.sha256((root / "MANIFEST.json").read_bytes()).hexdigest(),
        "release_file_count": len(actual),
        "manifest_all_entries_passed": True,
        "author_non_mutating_replay_matches_frozen_json": True,
        "method": "Actual permutations; independently enumerated conjugacy and all commuting pairs",
        "cases": rows,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
