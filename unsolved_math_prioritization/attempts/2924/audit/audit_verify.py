#!/usr/bin/env python3
"""Replay the frozen packet and test independent finite algebraic controls.

Usage: python3 audit_verify.py ../public
The output is a consistency audit, not a proof of any homotopy-group claim.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import subprocess
import sys


def require(value, message):
    if not value:
        raise RuntimeError(message)


root = Path(sys.argv[1] if len(sys.argv) > 1 else "../public")
expected_manifest = "b17e146dff9c3f63a2e3445d5fe1bac763ac3216029fca7dfbc23801e74c6e05"
manifest_bytes = (root / "SHA256SUMS").read_bytes()
require(sha256(manifest_bytes).hexdigest() == expected_manifest, "Frozen manifest changed")
manifest_checks = {}
for line in manifest_bytes.decode().splitlines():
    expected, filename = line.split("  ", 1)
    require(Path(filename).name == filename, "Unexpected manifest path")
    actual = sha256((root / filename).read_bytes()).hexdigest()
    require(actual == expected, "Frozen file changed: " + filename)
    manifest_checks[filename] = actual
require(set(p.name for p in root.iterdir()) == set(manifest_checks) | {"SHA256SUMS"},
        "Unexpected frozen packet inventory")

replay = subprocess.run([sys.executable, str(root / "verify.py")],
                        check=True, capture_output=True).stdout
require(replay == (root / "verification.json").read_bytes(), "Replay differs")
recorded = json.loads(replay)
require(recorded["total_assertions"] == 104647, "Unexpected replay count")
require(sum(recorded["checks_by_name"].values()) == 104647, "Count does not sum")

counts = {}


def check(label, condition):
    require(condition, label)
    counts[label] = counts.get(label, 0) + 1


def norm(x):
    return max(abs(u) for u in x)


def mul(xs):
    ans = F(1)
    for x in xs:
        ans *= x
    return ans


def compressed(x, a, t):
    """Closed displacement formula, without calling the packet's functions."""
    if not t or norm(x) >= t:
        return x
    return (x[0] + a * t * mul(1 - abs(u) / t for u in x),) + x[1:]


def compressed_inverse(y, a, t):
    if not t or norm(y) >= t:
        return y
    c = a * mul(1 - abs(u) / t for u in y[1:])
    numerator = y[0] - t * c
    denominator = 1 + c if y[0] <= t * c else 1 - c
    return (numerator / denominator,) + y[1:]


def shrink(mapper, x, t):
    if not t or norm(x) >= t:
        return x
    return tuple(t * y for y in mapper(tuple(u / t for u in x)))


grid = [F(-1), F(-1, 3), F(0), F(2, 5), F(1)]
parameters = [F(-4, 5), F(2, 7), F(5, 6)]
times = [F(0), F(1, 7), F(2, 3), F(1)]
for a, point in product(parameters, product(grid, repeat=4)):
    for t in times:
        y = compressed(point, a, t)
        check("independent_cube_preservation", norm(y) <= 1)
        check("independent_left_inverse", compressed_inverse(y, a, t) == point)
        check("independent_right_inverse", compressed(compressed_inverse(point, a, t), a, t) == point)
        check("independent_special_bound", norm(tuple(v - u for u, v in zip(point, y))) <= abs(a) * t)
        check("independent_general_bound", norm(tuple(v - u for u, v in zip(point, y))) <= 2 * t)
        check("independent_dilation_formula", shrink(lambda x: compressed(x, a, F(1)), point, t) == y)
        if norm(point) >= t:
            check("independent_support", y == point)
        for s in times:
            check("independent_semigroup", shrink(lambda x: compressed(x, a, t), point, s) == compressed(point, a, s * t))

# Deliberately false alternatives must be rejected. These are finite witnesses,
# not tests of the infinite-dimensional topology.
zero = (F(0),) * 4
a = F(1, 3)
t = F(1, 2)
check("negative_wrong_inverse_sign", compressed_inverse(compressed(zero, a, t), -a, t) != zero)
check("negative_no_scale_amplitude", compressed(zero, a, t) != compressed(zero, a, F(1)))
check("negative_time_zero_equals_original", compressed(zero, a, F(0)) != compressed(zero, a, F(1)))
check("negative_product_moves_boundary_cap", compressed(zero, a, F(1)) != zero)
check("negative_dimension_four_strict_inequality", not (F(2) < min(F(4 - 2), F(4, 2))))
check("positive_dimension_five_strict_inequality", F(2) < min(F(5 - 2), F(5, 2)))

# Post-run integrity check catches accidental writes during replay.
for filename, expected in manifest_checks.items():
    require(sha256((root / filename).read_bytes()).hexdigest() == expected,
            "File changed during audit: " + filename)
require(sha256((root / "SHA256SUMS").read_bytes()).hexdigest() == expected_manifest,
        "Manifest changed during audit")

print(json.dumps({
    "result": "pass",
    "problem_id": 2924,
    "problem_code": "KP-4.48",
    "frozen_manifest_sha256": expected_manifest,
    "frozen_authored_file_count_including_manifest": 9,
    "manifest_entries_verified": len(manifest_checks),
    "packet_replay": {"byte_identical": True, "total_assertions": 104647},
    "independent_grid": [str(x) for x in grid],
    "independent_parameters": [str(x) for x in parameters],
    "independent_times": [str(x) for x in times],
    "independent_checks_by_name": counts,
    "independent_total_checks": sum(counts.values()),
    "frozen_packet_preserved": True,
    "scope": "Finite exact arithmetic and integrity controls only; no computation of the unknown homotopy groups or proof of the general contractibility question."
}, indent=2, sort_keys=True))
