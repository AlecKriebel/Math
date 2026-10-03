#!/usr/bin/env python3
"""Independent arithmetic/scope audit; not a proof of quasiconformal estimates.

Python standard library only. No network, file mutation, or symbolic assumptions
about transcendental functions. The 915 count refers to parameter cases, not
individual assertions. Optional author replay runs only hash-verified code.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


EXPECTED_COUNTS = {
    "ball_area_rearrangement": 50,
    "class_count_rearrangement": 200,
    "cover_ratio_rearrangement": 15,
    "finite_subgroup_threshold": 50,
    "tube_count_rearrangement": 600,
}
MANIFEST_SHA256 = "a0551bf9c2e75444178fcb771606180216b5a096b33f793ac364fb169f2d33ee"


def check(condition, message):
    # Unlike assert, this verification remains active under python -O.
    if not condition:
        raise RuntimeError(message)


def exact_controls():
    counts = dict.fromkeys(EXPECTED_COUNTS, 0)
    ts = (F(101, 100), F(3, 2), F(2), F(5))
    ks = (F(101, 100), F(6, 5), F(2))
    for genus in range(2, 52):
        # Normalize areas by 2*pi; A(S)/(2*pi)=2g-2.
        area = F(2 * genus - 2)
        boundary = area + 1
        for delta in (F(-1, 4), F(0), F(1, 4)):
            c = boundary + delta
            check((c - 1 <= area) == (c <= 2 * genus - 1), "ball threshold")
        counts["ball_area_rearrangement"] += 1

        # Derive the finite-subgroup threshold from surface area / Hurwitz.
        threshold = 1 + area / (84 * (genus - 1))
        check(threshold == F(43, 42), "finite subgroup constant")
        for c in (threshold - F(1, 840), threshold, threshold + F(1, 840)):
            check((84 * (genus - 1) * (c - 1) >= area) == (c >= F(43, 42)),
                  "finite subgroup inequality direction")
        counts["finite_subgroup_threshold"] += 1

        for t in ts:
            # Factorized rational parametrization, independently from author.
            ball = (t - 1) ** 2 / (2 * t)
            sinh = (t * t - 1) / (2 * t)
            cosh = (t * t + 1) / (2 * t)
            check(cosh * cosh - sinh * sinh == 1, "hyperbolic identity")
            check(ball == cosh - 1 and ball > 0 and sinh > 0, "positive areas")
            class_threshold = F(4 * (genus - 1)) * t / ((t - 1) ** 2)
            for n in (class_threshold / 2, class_threshold, class_threshold * 2):
                check((n * ball >= area) == (n >= class_threshold), "class threshold")
            counts["class_count_rearrangement"] += 1

            for k in ks:
                ell = F(7, 3)
                # Normalize m by pi: u=m/pi, so u*(K*ell)*sinh >= 2g-2.
                u0 = F(4 * (genus - 1)) * t / (k * ell * (t*t - 1))
                for u in (u0 / 2, u0, u0 * 2):
                    check((u * k * ell * sinh >= area) == (u >= u0), "tube threshold")
                counts["tube_count_rearrangement"] += 1

    for ell in map(F, (1, 3, 10, 100, 1000)):
        for diameter in (F(1), F(7, 3), F(10)):
            for offset in (F(0), diameter, 2*diameter):
                d = ell + offset
                check(1 <= d / ell <= 1 + 2 * diameter / ell, "cover interval")
                check((d - ell) / ell == d / ell - 1, "cover normalization")
            check((ell + 2*diameter) / ell - 1 == 2*diameter / ell, "cover endpoint")
            counts["cover_ratio_rearrangement"] += 1
    check(counts == EXPECTED_COUNTS, "parameter-case count")

    # Mutations are falsified by explicit rational witnesses, not silently accepted.
    rejected = {
        "ball_cosh_boundary_2g_instead_of_2g_minus_1": F(4)-1 > 2,
        "Hurwitz_threshold_85_over_84": 84*(F(85,84)-1) < 2,
        "class_bound_missing_factor_2": F(1,2)*2 < 2,
        "tube_bound_missing_factor_2": F(1)*1*1*1 < 2,
        "regular_cover_additive_D_instead_of_2D": 1+2*F(1) > 1+F(1),
    }
    check(all(rejected.values()), "mutation controls")

    # A genus-two handle supports a_1,b_1 with integral intersection one.
    J = ((0,1,0,0),(-1,0,0,0),(0,0,0,1),(0,0,-1,0))
    a, b = (1,0,0,0), (0,1,0,0)
    intersection = sum(a[i]*J[i][j]*b[j] for i in range(4) for j in range(4))
    check(intersection == 1, "positive genus odd-intersection witness")
    check(all(J[i][j] == -J[j][i] for i in range(4) for j in range(4)), "skew form")
    return {"checks": counts, "total_cases": sum(counts.values()),
            "arithmetic": "exact fractions", "negative_controls_rejected": rejected,
            "topological_algebra_control": {"genus": 2, "a1_intersection_b1": intersection},
            "scope": "finite algebra tests; geometry and topology are justified in AUDIT.md"}


def constant_diagnostic():
    # Numerical diagnostic only. AGM computes the complete elliptic integral.
    def agm(a, b):
        for _ in range(40):
            a, b = (a+b)/2, math.sqrt(a*b)
        return a
    def elliptic_k(parameter):
        return math.pi / (2*agm(1, math.sqrt(1-parameter)))
    diameter = math.acosh(1/(math.tan(math.pi/3)*math.tan(math.pi/7)))
    r = math.exp(-diameter)
    mu = math.pi/2 * elliptic_k(1-r*r) / elliptic_k(r*r)
    constant = 1/math.tanh(math.pi**2/(4*mu))**2
    check(abs(constant - 1.3613826121756994) < 1e-12, "strong constant numerical check")
    return {"method": "binary floating point with AGM; not certified interval arithmetic",
            "orbifold_diameter": diameter, "strong_homogeneity_infimum": constant,
            "applies_to_ordinary_homogeneity": False}


def inspect_author(directory, replay):
    manifest_path = directory / "FROZEN_AUTHOR_MANIFEST.json"
    raw = manifest_path.read_bytes()
    check(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256, "frozen manifest hash")
    manifest = json.loads(raw)
    check(manifest["problem_id"] == 30000330 and manifest["rank"] == 497,
          "problem identity")
    verified = []
    for entry in manifest["files"]:
        name = entry["path"]
        check(Path(name).name == name, "manifest filename must be basename")
        data = (directory / name).read_bytes()
        check(len(data) == entry["bytes"], "frozen byte count: " + name)
        check(hashlib.sha256(data).hexdigest() == entry["sha256"], "frozen hash: " + name)
        verified.append(name)
    check(len(verified) == 6, "frozen file count")
    result = {"manifest_sha256": MANIFEST_SHA256, "files_verified": verified,
              "author_script_replayed": False}
    if replay:
        output = json.loads(subprocess.check_output(
            [sys.executable, str(directory / "verify_bounds.py")], text=True))
        check(output == json.loads((directory / "exact_results.json").read_text()),
              "author output must equal recorded result")
        check(output["checks"] == EXPECTED_COUNTS and output["total_checks"] == 915,
              "author output count")
        result["author_script_replayed"] = True
        result["author_recorded_output_matches"] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-dir", type=Path, help="optional frozen public directory")
    parser.add_argument("--replay-author", action="store_true",
                        help="replay only after successful frozen hash verification")
    args = parser.parse_args()
    check(not args.replay_author or args.author_dir is not None, "replay needs author directory")
    result = {"result": "PASS_PARTIAL_RESEARCH", "problem_id": 30000330,
              "independent_controls": exact_controls(), "numerical_diagnostic": constant_diagnostic()}
    if args.author_dir is not None:
        result["freeze_verification"] = inspect_author(args.author_dir, args.replay_author)
    result["universal_gap_verified"] = False
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
