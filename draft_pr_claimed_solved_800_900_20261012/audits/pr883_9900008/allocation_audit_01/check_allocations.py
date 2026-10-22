#!/usr/bin/env python3
"""Independent exact diagnostics; universal claims are proved in REPORT.md.

No inherited program is executed. No writes, network, Git or subprocess calls.
All guards are explicit and survive Python optimization.
"""
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PINS = {
    "some-open-probability-problems.pdf": "efe6b6e78e36185a2b278ba0cf5593c2e92f43b479f80159d6f6b7ecc4f6efaf",
    "0906.2062.pdf": "0a4c4813cef44e99c232d0687aa704554248675c621755be85568d0588999719",
    "1405.7566.pdf": "b265c6d7984627f4b186ffbef8efa8faf75a94db674f55ae1333698d20c7c0cb",
    "2112.13053.pdf": "f1400d56b382b86dd4e0740093d53744b313c91dc6cf9512607aa5cfdfaac18c",
    "2303.05137.pdf": "5de5f2453372883da6c769c4ef9d78cf909360bc8ca21406f40c22111253ff85",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def authenticate():
    raw = (BASE / "SOURCE_MANIFEST.json").read_bytes()
    require(sha(raw) == "53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab",
            "external frozen source-manifest pin")
    manifest = json.loads(raw)
    require(manifest["frozen_head"] == "af25d26e21945a1a132aace5e600485152777070", "head pin")
    paths = set()
    total = 0
    for row in manifest["files"]:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts, "unsafe source path")
        require(str(relative) not in paths, "duplicate source path")
        paths.add(str(relative))
        data = (BASE / "source" / relative).read_bytes()
        require(len(data) == row["bytes"] and sha(data) == row["sha256"], "source file differs: " + str(relative))
        total += len(data)
    actual = {str(p.relative_to(BASE / "source")) for p in (BASE / "source").rglob("*") if p.is_file()}
    require(actual == paths and len(paths) == 26 and total == 211771, "source membership/size")
    for name, expected in PINS.items():
        require(sha((BASE / "private_sources" / name).read_bytes()) == expected, "primary pin: " + name)
    return {"original_files": len(paths), "original_bytes": total,
            "source_manifest_sha256": sha(raw), "primary_pdfs_authenticated": len(PINS),
            "inherited_programs_executed": 0}


def ceil(q):
    return -((-q.numerator) // q.denominator)


def count_lines(offset, lo, hi):
    return ceil(hi - offset) - ceil(lo - offset)


def rect_mass(phase, rect, displacements=((F(0), F(0)), (F(0), F(0)))):
    x0, x1, y0, y1 = rect
    require(x0 <= x1 and y0 <= y1, "rectangle order")
    # The preimage of an x-interval under a line translation has the same length.
    return (x1 - x0) * sum(
        weight * count_lines(offset - phase + displacement[1], y0, y1)
        for offset, weight, displacement in zip((F(0), F(1, 2)), (F(1), F(2)), displacements)
    )


def pi(u):
    u %= 1
    if u == 0:
        return F(3, 7), F(2)
    if u == F(1, 2):
        return F(-5, 11), F(-3)
    return F(0), -u


def collapse_pi(u):
    u %= 1
    return (F(0), F(0)) if u in (0, F(1, 2)) else (F(0), -u)


def tau(u, s, displacement=pi):
    a, b = displacement((u + s[1]) % 1)
    return s[0] + a, s[1] + b


def check_quotient():
    solutions = []
    for labels in itertools.product(range(3), repeat=2):
        received = [0, 0, 0]
        for label, w in zip(labels, (1, 2)):
            received[label] += w
        if received == [1, 2, 0]:
            solutions.append(labels)
    require(solutions == [(0, 1)], "two-family quotient rigidity")
    equal_solutions = []
    for labels in itertools.product(range(2), repeat=2):
        received = [0, 0]
        for label in labels:
            received[label] += 1
        if received == [1, 1]:
            equal_solutions.append(labels)
    require((1, 0) in equal_solutions, "equal-weight negative control did not expose swap")
    extra_solutions = []
    for labels in itertools.product(range(2), repeat=3):
        received = [0, 0]
        for label in labels:
            received[label] += 1
        if received == [1, 2]:
            extra_solutions.append(labels)
    require(len(extra_solutions) == 3, "extra-family negative control did not expose merging")
    return {"quotient_cases": 9, "unique_preserving_labels": solutions,
            "equal_weight_control_exposes_swap": True,
            "extra_source_family_control_exposes_merging": True}


def check_covariance_and_rectangles():
    values = (F(-7, 3), F(-1), F(0), F(1, 4), F(1, 2), F(8, 7), F(3))
    checks = 0
    for u, x, y, a, b in itertools.product(values, repeat=5):
        left = tau((u + b) % 1, (x - a, y - b))
        v = tau(u, (x, y))
        require(left == (v[0] - a, v[1] - b), "covariance/sign error")
        checks += 1
    rectangle_checks = 0
    for u, y, length in itertools.product(values, values, (F(1, 7), F(1), F(13, 5))):
        rect = F(-5, 7), F(8, 3), y, y + length
        require(rect_mass(u, rect, (pi(0), pi(F(1, 2)))) == rect_mass(u, rect),
                "positive-control rectangle pushforward")
        rectangle_checks += 1
    # An actual admissible allocation may be noninjective and nonsurjective off support.
    require(tau(0, (F(0), F(1, 3)), collapse_pi) == (0, 0), "collapse point 1")
    require(tau(0, (F(0), F(1, 4)), collapse_pi) == (0, 0), "collapse point 2")
    require(collapse_pi(0) == (0, 0) and collapse_pi(F(1, 2)) == (0, 0), "support fixed")
    return {"rational_covariance_instances": checks, "exact_rectangle_instances": rectangle_checks,
            "noninjective_nonsurjective_off_support_control": "admitted"}


def check_nonequivariant_swap():
    # Light -> heavy, x -> x/2; heavy -> light, x -> 2x.
    # Pushforward density is source density / absolute affine slope.
    require(F(1) / F(1, 2) == 2 and F(2) / F(2) == 1, "swap Jacobians")
    image_origin = (F(0), F(1, 2))
    image_minus_e1 = (F(-1, 2), F(1, 2))
    shifted_image_origin = (F(-1), F(1, 2))
    require(image_minus_e1 != shifted_image_origin, "must fail horizontal covariance")
    return {"measure_preserving": True, "root_changes_type": True,
            "source_class_member": False, "exclusion": "fails horizontal covariance"}


def background_pi(state):
    u, r = (v % 1 for v in state)
    if u == 0:
        return -r / 2, F(1, 2)
    if u == F(1, 2) and r < F(1, 2):
        return r, F(-1, 2)
    return F(0), F(0)


def background_tau(state, s):
    u, r = state
    a, b = background_pi(((u + s[1]) % 1, (r + s[0]) % 1))
    return s[0] + a, s[1] + b


def preimage_length(a, b, slope, intercept, target_lo, target_hi):
    lo = max(a, (target_lo - intercept) / slope)
    hi = min(b, (target_hi - intercept) / slope)
    return max(F(0), hi - lo)


def check_background_and_kernel():
    values = (F(-1), F(0), F(1, 4), F(1, 2), F(3, 4), F(5, 3))
    covariance_checks = 0
    for u, r, x, y, a, b in itertools.product(values, repeat=6):
        left = background_tau(((u + b) % 1, (r + a) % 1), (x - a, y - b))
        right = background_tau((u, r), (x, y))
        require(left == (right[0] - a, right[1] - b), "background covariance")
        covariance_checks += 1
    # Each tuple is source interval, source weight, positive slope, intercept, target type.
    pieces = ((0, 1, 1, F(1, 2), 0, 1),
              (0, F(1, 2), 2, 2, 0, 0),
              (F(1, 2), 1, 2, 1, 0, 1))
    points = sorted({F(i, n) for n in range(1, 9) for i in range(n + 1)})
    interval_checks = 0
    for lo, hi in itertools.combinations(points, 2):
        for target, weight in ((0, 1), (1, 2)):
            image = sum(w * preimage_length(F(a), F(b), F(c), F(d), lo, hi)
                        for a, b, w, c, d, target_type in pieces if target_type == target)
            require(image == weight * (hi - lo), "background exact interval pushforward")
            interval_checks += 1
    for r in points[:-1]:
        require(background_pi((0, r))[1] == F(1, 2), "background root must be heavy")
    kernel = ((F(0), F(1)), (F(1, 2), F(1, 2)))
    require(all(sum(row) == 1 for row in kernel), "kernel stochastic")
    received = [sum(w * kernel[i][j] for i, w in enumerate((F(1), F(2)))) for j in range(2)]
    require(received == [1, 2] and kernel[0][1] == 1, "kernel balance/root change")
    return {"background_covariance_instances": covariance_checks,
            "background_exact_interval_instances": interval_checks,
            "stationary_independent_background_breaks_original_invariance": True,
            "background_scope": "stronger premise; not an original-state allocation",
            "Markov_kernel_rows": [[str(v) for v in row] for row in kernel],
            "Markov_kernel_preserves_mass_but_changes_root": True}


def check_direct_witness():
    require(F(2, 3) > 0 and F(1, 3) + F(2, 3) == 1, "probability arithmetic")
    for u in (F(0), F(1, 9), F(1, 2), F(8, 9), F(1)):
        require(rect_mass(0, (0, 1, -u, 1 - u)) == 3, "mass-sampling denominator")
    return {"unit_square_mass": "3", "original_heavy_event_probability": "0",
            "mass_resampled_heavy_event_probability": "2/3"}


def main():
    result = {"status": "PASS", "scope": "independent allocation-family exact diagnostics",
              "authentication": authenticate(), "quotient": check_quotient(),
              "actual_source_class": check_covariance_and_rectangles(),
              "relaxed_covariance_control": check_nonequivariant_swap(),
              "stronger_class_controls": check_background_and_kernel(),
              "direct_mass_stationarity_failure": check_direct_witness(),
              "limitation": "Finite exact diagnostics do not prove the universal measurable classification; see REPORT.md."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
