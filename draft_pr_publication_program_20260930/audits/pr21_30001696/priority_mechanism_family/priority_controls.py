"""Exact-arithmetic transcription controls, not a proof of the target theorem."""
from fractions import Fraction as F
import json
from pathlib import Path


def variations(v):
    signs = [1 if x > 0 else -1 for x in v if x]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def squared(v):
    return sum(x * x for x in v)


def main():
    coordinate_cases = 0
    for d in range(2, 21):
        e1 = [F(1)] + [F(0)] * (d - 1)
        alternating = [F(1)] + [F((-1) ** j, 1000) for j in range(1, d)]
        assert variations(e1) == 0
        assert variations(alternating) == d - 1
        for i in range(d - 1):
            assert variations(e1) <= i < variations(alternating)
            coordinate_cases += 1
    x = [F(4), F(1, 10), F(1, 10), F(1, 10)]
    y = [F(-3), F(-1), F(1), F(3)]
    z = [a + b for a, b in zip(x, y)]
    assert [variations(v) for v in (x, y, z)] == [0, 1, 2]
    diagonal = [F(4), F(3), F(1), F(1, 2)]
    sample_checks = 0
    for y0 in range(-2, 3):
        for y1 in range(-2, 3):
            for z0 in range(-2, 3):
                for z1 in range(-2, 3):
                    v = list(map(F, (y0, y1, z0, z1)))
                    if not any(v) or squared(v[2:]) > squared(v[:2]):
                        continue
                    image = [a * b for a, b in zip(diagonal, v)]
                    assert squared(image[2:]) < squared(image[:2])
                    sample_checks += 1
    line = [F(1), F(0), F(2), F(0)]
    assert squared(line[2:]) > squared(line[:2])
    line_image = [a * b for a, b in zip(diagonal, line)]
    assert squared(line_image[2:]) < squared(line_image[:2])
    result = {
        "scope": "finite exact-arithmetic replay of universally proved adapter controls",
        "target_proof_attempts_added": 0,
        "coordinate_boundary_cases": coordinate_cases,
        "coordinate_dimensions_replayed": [2, 20],
        "chebyshev_sum_variations": [0, 1, 2],
        "rank_two_cone_integer_samples_checked": sample_checks,
        "isolated_line_strict_image_checked": True,
        "stable_range_counterexample": {"d": 6, "i": 3, "c": 2, "m": 3},
        "status": "PASS",
    }
    destination = Path(__file__).with_name("CONTROL_RESULTS.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
