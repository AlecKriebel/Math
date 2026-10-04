#!/usr/bin/env python3
"""Exact finite audit controls, not a verifier for an entire-function theorem.

Run with a sibling submission directory, or pass --submission PATH.
Only reads the frozen submission. Writes no files; output is JSON on stdout.
"""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys

EXPECTED_MANIFEST = "b2075d407c7c8549feb69e16fa6ca33dad6d65a57873291da59dda37ce7f0653"
EXPECTED_RESULT = "073340a7e505d58912b40e4bca9f4d18fead1362346d336bb7ccffa176d5b3c7"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", type=Path,
                        default=Path(__file__).resolve().parent.parent / "submission")
    submission = parser.parse_args().submission
    checks = 0

    def check(statement):
        nonlocal checks
        assert statement
        checks += 1

    check(digest(submission / "MANIFEST.json") == EXPECTED_MANIFEST)
    check(digest(submission / "RESULT.md") == EXPECTED_RESULT)
    manifest = json.loads((submission / "MANIFEST.json").read_text())
    for name, record in manifest["files"].items():
        check(digest(submission / name) == record["sha256"])
        check((submission / name).stat().st_size == record["bytes"])
    for line in (submission / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        check(digest(submission / name.strip()) == expected)
    replay = json.loads(subprocess.check_output(
        [sys.executable, str(submission / "verify_controls.py")], text=True))
    check(replay == json.loads((submission / "control_results.json").read_text()))
    check(replay["checks"] == 8233)
    check(replay["target_resolution"] is False)
    integrity_checks = checks

    # Independent exhaustive small permutation control: local branch generators
    # may connect sheets jointly, although none is individually transitive.
    permutation_cases = 0
    for n in range(2, 8):
        edges = [(j, j + 1) for j in range(n - 1)]
        for mask in itertools.product((False, True), repeat=n - 1):
            seen = set()
            components = 0
            for seed in range(n):
                if seed in seen:
                    continue
                components += 1
                stack = [seed]
                seen.add(seed)
                while stack:
                    x = stack.pop()
                    for include, (u, v) in zip(mask, edges):
                        if include and x in (u, v):
                            y = v if x == u else u
                            if y not in seen:
                                seen.add(y)
                                stack.append(y)
            check(components == n - sum(mask))
            check((components == 1) == all(mask))
            permutation_cases += 1

    # A genuine analytic delayed-capture example, with exact rational constants.
    # P(z)=z^2+3/16, a=1/4, B=B(a,1/32).
    # The analytic proofs of connectivity claims are in AUDIT.md, not inferred
    # from these scalar assertions or from samples of the complex plane.
    a, c, r = F(1, 4), F(3, 16), F(1, 32)
    p = lambda z: z*z+c
    check(p(a) == a)
    check(2*a == F(1, 2))
    check(2*a+r < 1)  # |P(a+h)-a| <= (2a+r)|h| on closure B
    check(abs(c-a) > r)  # critical value outside B; W_1 has two components
    check(p(-a) == a)
    check(p(a) == a)
    check(abs(p(p(F(0)))-a) < r)
    check(p(c) == F(57, 256))
    check(a-p(c) == F(7, 256) < r)
    # For real x in [-a,a], P(x) in [c,a] and P^2(x) in [P(c),a].
    check(c < a)
    check(a-r < p(c) <= a < a+r)
    orbit = [F(0)]
    for _ in range(10):
        orbit.append(p(orbit[-1]))
    for j in range(1, len(orbit)):
        check(orbit[j-1] < orbit[j] < a)
        check((abs(orbit[j]-a) < r) == (j >= 2))
    stage_counts = []
    for m in range(1, 11):
        # Critical value P^k(0) of P^m has multiplicity 2^(m-k).
        inside_ramification = sum(2**(m-k) for k in range(1, m+1)
                                   if abs(orbit[k]-a) < r)
        components = 2**m - inside_ramification
        check(inside_ramification == 2**(m-1)-1)
        check(components == 2**(m-1)+1)
        check(components > 1)
        stage_counts.append({"m": m, "degree": 2**m,
                             "ramification_inside": inside_ramification,
                             "components_by_disc_Riemann_Hurwitz": components})

    # Fixed-point qualifier mutation: P(z)=z^2-1 exchanges 0 and -1.
    q = lambda z: z*z-1
    check(q(0) == -1)
    check(q(-1) == 0)
    check(0 != -1)
    check((2*0)*(2*(-1)) == 0)

    # Singleton-enlargement mutation: exp(z^2)^-1(B(0,e^-1)) equals
    # {(x,y): y^2-x^2>1}, two components, while exp(z^2)^-1({0}) is empty.
    # Check discriminating rational cross-sections only; analytic set identity
    # and the two-component argument are supplied separately.
    cross_sections = []
    for x in range(-5, 6):
        y = abs(x)+2
        check(y*y-x*x > 1)
        check((-y)*(-y)-x*x > 1)
        check(0*0-x*x <= 1)
        cross_sections.append({"x": x, "upper_y": y, "lower_y": -y})

    return {
        "status": "passed",
        "frozen_manifest_sha256": EXPECTED_MANIFEST,
        "frozen_result_sha256": EXPECTED_RESULT,
        "integrity_and_replay_checks": integrity_checks,
        "replayed_original_checks": replay["checks"],
        "new_finite_assertions": checks-integrity_checks,
        "total_audit_assertions": checks,
        "permutation_cases": permutation_cases,
        "delayed_capture": {"polynomial": "z^2+3/16", "a": str(a),
                            "radius": str(r), "critical_value": str(c),
                            "second_critical_image": str(p(c)),
                            "stage_counts": stage_counts},
        "singleton_control_cross_sections": cross_sections,
        "limitations": "Finite exact arithmetic, graph, provenance and replay controls only. Connectivity conclusions require the analytic proofs in AUDIT.md. No resolution of either unrestricted source question.",
        "target_resolution": False
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
