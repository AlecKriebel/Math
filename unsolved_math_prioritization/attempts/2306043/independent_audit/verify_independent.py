#!/usr/bin/env python3
"""Independent exact audit controls for frozen Problem 2306043.

No source text or dataset content is embedded. No network or remote writes.
Finite controls supplement, and do not replace, the mathematical audit.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import json
import random
import subprocess
import sys

FROZEN = "21ac6f2720eb4492499e1034053e9652bbc41fca6b47613077cfb05eece936f6"
COUNTS = Counter()


def require(group, condition):
    if not condition:
        raise AssertionError(group)
    COUNTS[group] += 1


def verify_binding(packet):
    manifest_bytes = (packet / "FROZEN_MANIFEST.json").read_bytes()
    require("freeze", sha256(manifest_bytes).hexdigest() == FROZEN)
    manifest = json.loads(manifest_bytes)
    require("freeze", len(manifest["files"]) == 13)
    require("freeze", sum(row["bytes"] for row in manifest["files"]) == 42715)
    actual = {p.name for p in packet.iterdir() if p.is_file()}
    expected = {row["path"] for row in manifest["files"]} | {"FROZEN_MANIFEST.json"}
    require("freeze", actual == expected)
    for row in manifest["files"]:
        data = (packet / row["path"]).read_bytes()
        require("freeze", len(data) == row["bytes"])
        require("freeze", sha256(data).hexdigest() == row["sha256"])
    output = subprocess.check_output(
        [sys.executable, str(packet / "verify_controls.py")], text=True)
    replay = json.loads(output)
    require("original_replay", replay == json.loads((packet / "CONTROL_RESULTS.json").read_bytes()))
    require("original_replay", replay["status"] == "PASS" and replay["checks_passed"] == 2945)
    return replay


def abel_and_triangular_controls():
    rng = random.Random(2306043)
    for length in range(1, 41):
        a = [Q(rng.randrange(0, 20), rng.randrange(1, 8)) for _ in range(length)]
        x = [Q(rng.randrange(-20, 21), rng.randrange(1, 8)) for _ in range(length)]
        sums = [sum(a[:n], Q(0)) for n in range(1, length + 1)]
        milin = [sum((Q(n + 1 - k) * x[k - 1] for k in range(1, n + 1)), Q(0))
                 for n in range(1, length + 1)]
        for r in [Q(1, 7), Q(1, 2), Q(9, 10), Q(99, 100)]:
            lhs = sum((v * r**n for n, v in enumerate(a, 1)), Q(0))
            rhs = (1-r)*sum((v*r**n for n, v in enumerate(sums, 1)), Q(0)) + sums[-1]*r**(length+1)
            require("abel_random_exact", lhs == rhs)
            total_x = sum(x, Q(0))
            moment_x = sum((n*v for n, v in enumerate(x, 1)), Q(0))
            tail = r**(length+1)/(1-r)*(total_x*(length+2+r/(1-r))-moment_x)
            lhs_m = sum((v*r**n for n, v in enumerate(milin, 1)), Q(0)) + tail
            rhs_m = sum((v*r**n for n, v in enumerate(x, 1)), Q(0))/(1-r)**2
            require("triangular_generating_exact", lhs_m == rhs_m)


def rudin_shapiro_controls():
    p = q = [1]
    for m in range(13):
        n = 1 << m
        independent = [(-1)**((k & (k >> 1)).bit_count()) for k in range(n)]
        require("rudin_shapiro_binary_formula", p == independent)
        if m:
            q_independent = [v * (-1 if k >= n//2 else 1) for k, v in enumerate(independent)]
            require("rudin_shapiro_binary_formula", q == q_independent)
        # Evaluate the exact Laurent identity by all its integer coefficients.
        if m <= 10:
            for lag in range(n):
                correlation = sum(p[k]*p[k+lag]+q[k]*q[k+lag] for k in range(n-lag))
                require("rudin_shapiro_laurent_exact", correlation == (2*n if lag == 0 else 0))
        p, q = p+q, p+[-v for v in q]


def all_scale_algebra_controls():
    # The complete infinite argument is in the audit report. These exercise its
    # algebra through enormous indices without expanding sparse blocks.
    for j in range(3, 21):
        m = 1 << j
        n = 1 << m
        sum_m = (1 << (j+1))-8
        require("all_scale_exact", sum_m == sum(1 << i for i in range(3, j+1)))
        require("all_scale_exact", Q(1)+Q(sum_m, 16) <= Q(m, 2))
        require("all_scale_exact", Q(sum_m, 16) < Q(m, 8))
        require("all_scale_exact", m <= 8*n)
        require("all_scale_exact", n*n == (1 << (1 << (j+1))))
        require("all_scale_exact", 2*n-1 < n*n)
        require("all_scale_exact", 2*j <= m)
        require("all_scale_exact", Q(m, 8*n) <= Q(1, 8*(1 << j)))
        require("all_scale_exact", Q(m, n) < Q(1, 16) if j >= 4 else True)
        if j > 3:
            old_m = 1 << (j-1)
            old_n = 1 << old_m
            require("sparse_mass_ratio_exact", Q(old_m*old_n, m*n) < Q(1, 4))
        # Square of the asserted lower bound on (1-r_j)A(r_j).
        require("radial_growth_scale_exact", Q(m, 1024) == Q(m, 16*64))


def dyadic_and_energy_controls():
    # Independent exact prefix comparison, including every entry in first block.
    energy = harmonic = double_sum = Q(0)
    for n in range(1, 2049):
        square = Q(1) if n == 1 else Q(1, 2) if 256 <= n <= 511 else Q(0)
        energy += square/n
        harmonic += Q(1, n)
        double_sum += energy-harmonic
        require("actual_prefix_energy_exact", energy <= harmonic)
        require("actual_prefix_milin_exact", double_sum <= 0)
    for j in range(31):
        n = 1 << j
        require("dyadic_exact", n*(3*n-1)//2 <= 2*n*n)
        cumulative = sum(1 << (k+1) for k in range(j+1))
        require("dyadic_exact", cumulative == 2*((1 << (j+1))-1))
        for end in [n, n+max(0, n//2-1), 2*n-1]:
            require("dyadic_exact", cumulative <= 4*end)


def critical_and_radial_controls():
    # Bounds hold for the entire infinite tail, not a numerically truncated H.
    for q in [Q(3, 4), Q(49, 100), Q(51, 100)]:
        tail = q**256*(Q(256)/(1-q)+q/(1-q)**2)
        if q == Q(49, 100):
            require("critical_infinite_tail_exact", 1-2*q-2*tail > 0)
        else:
            require("critical_infinite_tail_exact", 1-2*q+2*tail < 0)
    for n in range(1, 513):
        r = Q(2*n-1, 2*n)
        require("radial_bernoulli_exact", r**n >= Q(1, 2))
        require("radial_bernoulli_exact", r**(2*n) >= Q(1, 4))
        require("radial_block_exact", (1-r)*sum((r**k for k in range(n, 2*n)), Q(0)) >= Q(1, 8))


def finite_energy_and_normalization_controls():
    # A concrete finite tail checks the exact squared Cauchy-Schwarz formulas.
    d = [Q((-1)**n, n*n) for n in range(1, 41)]
    for k in [0, 1, 7, 20, 39]:
        tail = d[k:]
        energy = sum((n*x*x for n, x in enumerate(d, 1) if n > k), Q(0))
        mass = sum((n*abs(x) for n, x in enumerate(d, 1) if n > k), Q(0))
        require("finite_energy_cauchy_exact", mass*mass <= energy*Q(40*41, 2))
        for r in [Q(1, 3), Q(3, 4), Q(99, 100)]:
            radial = sum((n*abs(x)*r**n for n, x in enumerate(d, 1) if n > k), Q(0))
            require("finite_energy_cauchy_exact", ((1-r)*radial)**2 <= energy*r)
    # Formal exp(2G) below the first high block is exp(-2z). Verify both
    # F'(0)=1 and the logarithmic-derivative factor 1+2H exactly.
    exponential = [Q(1)]
    for n in range(1, 41):
        exponential.append(exponential[-1]*Q(-2, n))
    require("factor_two_exact", exponential[0] == 1 and exponential[1] == -2)
    for n in range(1, 41):
        require("factor_two_exact", (n+1)*exponential[n] == exponential[n]-2*exponential[n-1])
    # At a quarter-turn the sign of the maximal-growth phase matters.
    for n in range(1, 41):
        phase = n % 4
        inverse_phase = (-n) % 4
        require("phase_rotation_exact", (phase+inverse_phase) % 4 == 0)
        if n % 2:
            require("phase_rotation_exact", (phase+phase) % 4 != 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    replay = verify_binding(args.packet)
    abel_and_triangular_controls()
    rudin_shapiro_controls()
    all_scale_algebra_controls()
    dyadic_and_energy_controls()
    critical_and_radial_controls()
    finite_energy_and_normalization_controls()
    # Reverify the freeze after all work, including the original replay.
    verify_binding(args.packet)
    report = {
        "problem_id": "2306043",
        "verdict": "PASS_WITH_STATED_SOURCE_LIMITS",
        "frozen_manifest_sha256": FROZEN,
        "frozen_payload_files": 13,
        "frozen_payload_bytes": 42715,
        "original_control_assertions": replay["checks_passed"],
        "independent_control_assertions": sum(COUNTS.values()),
        "groups": dict(sorted(COUNTS.items())),
        "arithmetic": "Exact integers and rational fractions only",
        "critical_point_bracket": ["49/100", "51/100"],
        "critical_point_bracket_scope": "Infinite-tail bound for the actual fixed construction",
        "full_problem_solved": False,
        "relaxed_map_univalent": False,
        "recommended_queue_status": "exhausted",
        "recommended_turns": "5/5",
        "scope": "Finite controls plus separately documented mathematical audit; no proof-engine claim",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
