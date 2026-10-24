#!/usr/bin/env python3
"""Exact finite controls for an independent topological reduction audit.

The general topological assertions are proved in AUDIT.md. These controls
falsify a tempting tuple-witness lifting shortcut and check value-image
surjectivity on a concrete nontrivial inverse sequence.
"""
from datetime import datetime, timezone
import json
from pathlib import Path

checks = []
for n in range(1, 9):
    modulus = 2 ** n
    values = {2 * x % modulus for x in range(modulus)}
    next_values = {2 * x % (2 * modulus) for x in range(2 * modulus)}
    assert {y % modulus for y in next_values} == values
    assert len(values) == 2 ** (n - 1)
    checks.append({"stage": n, "modulus": modulus,
                   "square_value_count": len(values),
                   "next_value_projection_surjective": True})

roots_C2 = {x for x in range(2) if 2 * x % 2 == 0}
roots_C4 = {x for x in range(4) if 2 * x % 4 == 0}
projected_roots = {x % 2 for x in roots_C4}
assert roots_C2 == {0, 1}
assert roots_C4 == {0, 2}
assert projected_roots == {0}
assert projected_roots != roots_C2

# Thin-branch inverse sets: Y_n={0,...,n}; n+1 projects to zero.
# At finite depth d, coherent prefixes are all-zero or determined by one
# first positive label k, after which that label stays fixed.
thin_checks = []
prefixes = [(0,), (1,)]
for n in range(1, 12):
    extended = []
    for prefix in prefixes:
        for label in range(n + 2):
            projected = label if label <= n else 0
            if projected == prefix[-1]:
                extended.append(prefix + (label,))
    prefixes = extended
    assert len(prefixes) == n + 2
    for prefix in prefixes:
        nz = [i for i, x in enumerate(prefix) if x]
        if nz:
            k = prefix[nz[0]]
            assert all(x == 0 for x in prefix[:nz[0]])
            assert all(x == k for x in prefix[nz[0]:])
    thin_checks.append({"depth": n + 1, "coherent_prefix_count": len(prefixes)})

result = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "result": "PASS",
    "cyclic_square_inverse_sequence": checks,
    "non_surjective_witness_fiber_control": {
        "word": "x^2", "quotient": "C4 -> C2", "target": "identity",
        "roots_C2": sorted(roots_C2), "roots_C4": sorted(roots_C4),
        "projected_roots": sorted(projected_roots),
        "witness_1_in_C2_has_no_root_lift_for_target_0_in_C4": True
    },
    "thin_branch_finite_controls": thin_checks,
    "scope": "Finite controls only; general topology is proved separately."
}
Path(__file__).with_name("independent_control_results.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(json.dumps({"result": "PASS", "cyclic_stages": len(checks),
                  "thin_prefix_depths": len(thin_checks),
                  "non_surjective_witness_fiber": True}))
