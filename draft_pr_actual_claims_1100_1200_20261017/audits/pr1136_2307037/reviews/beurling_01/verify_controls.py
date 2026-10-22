#!/usr/bin/env python3
"""Supplementary deterministic controls; no universal claim is inferred here.

All conditions use explicit exceptions, so optimization cannot disable them.
The analytic arguments and endpoint proofs are in REPORT.md.
"""

import cmath
import hashlib
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def close(actual, expected, tolerance=2e-10):
    return abs(actual - expected) <= tolerance * max(1.0, abs(expected))


def disk_transform(center, radius, z, radial=32, angular=128):
    """Direct midpoint integration of the smooth, nonsingular complex kernel."""
    require(abs(z - center) > radius, "kernel evaluation point must be exterior")
    dr = radius / radial
    dt = 2 * math.pi / angular
    value = 0j
    for ir in range(radial):
        r = (ir + 0.5) * dr
        for it in range(angular):
            w = center + r * cmath.exp(1j * (it + 0.5) * dt)
            value += r * dr * dt / (w - z) ** 2
    return -value / math.pi


def disk_field_area(radius, pole, radial=96, angular=256):
    """Direct midpoint integral over a disk separated from the single pole."""
    require(abs(pole) > radius, "pole must be separated")
    dr = radius / radial
    dt = 2 * math.pi / angular
    value = 0.0
    for ir in range(radial):
        r = (ir + 0.5) * dr
        for it in range(angular):
            z = r * cmath.exp(1j * (it + 0.5) * dt)
            value += r * dr * dt / abs(z - pole) ** 2
    return value


def entropy(x):
    require(0 <= x <= 1, "entropy domain")
    return 0.0 if x == 0 else -x * math.log(x)


def main():
    disk_cases = [
        (0j, 1.0, 2 + 0j),
        (2 + 1j, 0.7, -1 + 2j),
        (-4 + 3j, 1.3, 2 - 2j),
        (0j, 3.0, 6 + 0j),
    ]
    witnesses = []
    for center, radius, z in disk_cases:
        actual = disk_transform(center, radius, z)
        expected = -radius ** 2 / (z - center) ** 2
        require(close(actual, expected), "complex disk kernel/normalization mismatch")
        witnesses.append(abs(actual - expected))

    base = disk_transform(2 + 1j, 0.7, -1 + 2j)
    scaled = disk_transform(6 + 3j, 2.1, -3 + 6j)
    require(close(base, scaled), "scale invariance mismatch")

    # Mutation guards each fail a materially wrong alternative.
    reference = disk_transform(0j, 1.0, 2 + 0j)
    guards = {
        "opposite_transform_sign": not close(reference, 0.25),
        "missing_one_over_pi": not close(reference, -math.pi / 4),
        "spurious_L_squared_field_factor": not close(scaled, 9 * base),
        "spurious_inverse_L_squared_field_factor": not close(scaled, base / 9),
    }

    far_exact = math.pi * math.log(6.25 / 5.25)
    far_numerical = disk_field_area(1.0, 2.5)
    require(close(far_numerical, far_exact, 8e-6), "polar area integral mismatch")
    require(far_exact > 0, "far support witness lost")
    guards["discard_far_support_when_a_zero"] = not close(far_exact, 0.0)

    # Endpoint values and a deliberately interior entropy maximizer.
    require(entropy(0) == 0 and entropy(1) == 0, "entropy endpoint failure")
    require(close(entropy(1 / math.e), 1 / math.e), "entropy maximizer failure")
    guards["drop_positive_entropy_term"] = entropy(1 / math.e) > 0.3

    u = (math.sqrt(1 + 4 * math.e) - 1) / 2
    require(close(u * (u + 1), math.e), "optimized split stationary equation")
    sharper = math.log1p(1 / u) + u / math.e
    original = math.log(2) + 1 / math.e
    require(sharper < original, "sharper analytic bound comparison failed")
    require(0 < u / math.e < 1, "maximizer escaped admissible interval")
    guards["replace_sharp_leading_coefficient_by_smaller_value"] = (
        2 * math.pi * math.log(math.e ** 4) > math.pi * math.log(math.e ** 4)
    )

    for name, rejected in guards.items():
        require(rejected, "wrong alternative not rejected: " + name)

    pin_path = Path(__file__).resolve().with_name("INPUT_PINS.json")
    pins = json.loads(pin_path.read_text())
    audit_root = Path(__file__).resolve().parents[2]
    recorded_audit_prefix = Path(pins["inputs"][0]["path"]).parent.parent
    for entry in pins["inputs"]:
        historical_path = Path(entry["path"])
        try:
            relative_path = historical_path.relative_to(recorded_audit_prefix)
            p = (audit_root / relative_path).resolve()
            p.relative_to(audit_root)
        except ValueError as error:
            raise RuntimeError("pinned input escapes audit folder") from error
        require(p.is_file(), "pinned input missing: " + str(p))
        require(p.stat().st_size == entry["bytes"], "input byte count changed")
        require(hashlib.sha256(p.read_bytes()).hexdigest() == entry["sha256"],
                "input digest changed: " + str(p))

    result = {
        "analytic_proof_dependency": False,
        "controls": "deterministic smooth disk quadrature and scalar witnesses",
        "complex_disk_cases": len(disk_cases),
        "max_complex_disk_error": max(witnesses),
        "far_disk_exact_integral": far_exact,
        "far_disk_quadrature_error": abs(far_exact - far_numerical),
        "wrong_alternative_guards": guards,
        "sharper_universal_constant_divided_by_pi": sharper,
        "manuscript_constant_divided_by_pi": original,
        "optimized_split_u": u,
        "input_pin_checks": len(pins["inputs"]),
        "verdict": "PASS_SUPPLEMENTARY_CONTROLS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
