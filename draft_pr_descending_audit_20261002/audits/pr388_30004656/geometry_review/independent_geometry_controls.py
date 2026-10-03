#!/usr/bin/env python3
"""Independent finite controls; supplementary to GEOMETRY_AUDIT.md's proofs.

Python standard library only. Does not import or execute candidate checkers.
All outputs are written beside this script. Fixed RNG seeds ensure replayability.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
import math
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parent
checks = {}


def compositions(total, count):
    for cuts in combinations(range(1, total), count - 1):
        edges = (0,) + cuts + (total,)
        yield tuple(edges[i + 1] - edges[i] for i in range(count))


def circle_exact():
    cases = 0
    flip_counts = {}
    for n in range(2, 8):
        counts = Counter()
        patterns = list(product((-1, 1), repeat=n))
        for ys in patterns:
            marked = [i for i in range(n) if ys[i] != ys[(i + 1) % n]]
            counts[len(marked)] += 1
        for j in range(n + 1):
            expected = 2 * math.comb(n, j) if j % 2 == 0 else 0
            assert counts[j] == expected
        flip_counts[n] = dict(sorted(counts.items()))
        for total in range(n, n + 5):
            for sizes in compositions(total, n):
                angles = [0]
                for size in sizes[:-1]:
                    angles.append(angles[-1] + size)
                for ys in patterns:
                    marked = [i for i in range(n) if ys[i] != ys[(i + 1) % n]]
                    if not marked:
                        continue
                    t = F(min(sizes[i] for i in marked), total)
                    distances = [F(min(abs(angles[i] - angles[j]), total - abs(angles[i] - angles[j])), total)
                                 for i in range(n) for j in range(i + 1, n) if ys[i] != ys[j]]
                    assert min(distances) == t
                    assert 0 < t <= F(1, len(marked)) <= F(1, 2)
                    cases += 1
    # Exhaustive rational simplex lattice control, independent of continuous volumes.
    lattice_cases = 0
    for n in range(2, 7):
        for total in range(n, n + 7):
            comps = list(compositions(total, n))
            for j in range(1, n + 1):
                for threshold in range(total + 1):
                    actual = sum(all(row[i] > threshold for i in range(j)) for row in comps)
                    residual = total - j * threshold
                    expected = math.comb(residual - 1, n - 1) if residual >= n else 0
                    assert actual == expected
                    lattice_cases += 1
    # n=2's closed form has a 1/2 atom at zero and no extra atom at one.
    for u in [1.0, 1.01, 2.0, 10.0, 1e6]:
        direct = 1.0 - math.asin(1.0 / u) / math.pi
        mixture = 0.5 + 0.5 * max(1.0 - 2.0 * math.asin(1.0 / u) / math.pi, 0.0)
        assert abs(direct - mixture) < 1e-14
    return {"deterministic_shortest_arc_cases": cases, "flip_pattern_counts": flip_counts,
            "simplex_lattice_tail_cases": lattice_cases, "n2_CDF_identity": True}


def circle_cdf(n, u):
    if u < 0:
        return 0.0
    if u < 1:
        return 2.0 ** (1 - n)
    t = math.asin(1.0 / u) / math.pi
    return 2.0 ** (1 - n) * (1 + sum(math.comb(n, j) * max(1 - j * t, 0) ** (n - 1)
                                          for j in range(2, n + 1, 2)))


def circle_distribution_control():
    rng = random.Random(38830004656)
    repetitions = 35000
    results = []
    for n in (2, 3, 8):
        thresholds = (0.5, 1.1, 2.0, 5.0, 20.0, 100.0)
        below = [0] * len(thresholds)
        for _ in range(repetitions):
            points = sorted((rng.random(), rng.choice((-1, 1))) for _ in range(n))
            opposite_distances = [min(abs(points[i][0] - points[j][0]), 1 - abs(points[i][0] - points[j][0]))
                                  for i in range(n) for j in range(i + 1, n) if points[i][1] != points[j][1]]
            optimum = 0.0 if not opposite_distances else 1.0 / math.sin(math.pi * min(opposite_distances))
            for a, u in enumerate(thresholds):
                below[a] += optimum <= u
        for a, u in enumerate(thresholds):
            theoretical = circle_cdf(n, u)
            empirical = below[a] / repetitions
            tolerance = 6 * math.sqrt(theoretical * (1 - theoretical) / repetitions) + 0.002
            assert abs(empirical - theoretical) <= tolerance
            results.append({"n": n, "u": u, "CDF_exact": theoretical, "CDF_empirical": empirical,
                            "tolerance": tolerance})
    # Check the specific rooted-vs-origin pitfall independently.
    n = 8
    rooted = [0.0] * n
    origin = [0.0] * n
    for _ in range(repetitions):
        a = sorted([0.0] + [rng.random() for _ in range(n - 1)])
        b = sorted(rng.random() for _ in range(n))
        rootgaps = [a[i + 1] - a[i] for i in range(n - 1)] + [1.0 - a[-1]]
        origingaps = [b[i + 1] - b[i] for i in range(n - 1)] + [1.0 - b[-1] + b[0]]
        rooted = [x + y for x, y in zip(rooted, rootgaps)]
        origin = [x + y for x, y in zip(origin, origingaps)]
    rooted = [x / repetitions for x in rooted]
    origin = [x / repetitions for x in origin]
    assert max(abs(x - 1.0 / n) for x in rooted) < 0.004
    assert abs(origin[-1] - 2.0 / (n + 1)) < 0.004
    assert max(abs(x - 1.0 / (n + 1)) for x in origin[:-1]) < 0.004
    return {"repetitions_per_dimension": repetitions, "CDF_checks": results,
            "rooted_gap_means": rooted, "fixed_origin_gap_means": origin,
            "scope": "Seeded numerical falsification control; not a proof of the random law."}


def state_DP(weights, n):
    """Exact subprobability of no opposite-label collision with outside patch mass."""
    outside = 1 - sum(weights)
    states = {(0,) * len(weights): F(1)}
    for _ in range(n):
        future = {}
        for state, p in states.items():
            future[state] = future.get(state, F(0)) + p * outside
            for j, w in enumerate(weights):
                for sign in (1, -1):
                    if state[j] == -sign:
                        continue
                    new = state if state[j] == sign else state[:j] + (sign,) + state[j + 1:]
                    future[new] = future.get(new, F(0)) + p * w / 2
        states = future
    return sum(states.values())


def birthday_controls():
    exact_cases = 0
    bound_cases = 0
    for M in range(1, 7):
        for n in range(1, 13):
            exact = state_DP([F(1, M)] * M, n)
            inclusion = sum((-1) ** j * math.comb(M, j) * 2 ** (M - j) * F(M - j, 2 * M) ** n
                            for j in range(M + 1))
            assert exact == inclusion
            # M fixed, no-collision probabilities must decrease as n grows.
            if n > 1:
                assert exact <= state_DP([F(1, M)] * M, n - 1)
            exact_cases += 1
    weight_families = [[F(1, 3), F(1, 6)], [F(1, 10), F(1, 7), F(1, 8)],
                      [F(1, 12)] * 6, [F(1, 4)] * 4]
    for weights in weight_families:
        for n in range(1, 13):
            # Here every x=np/4<=1. Verify exact Poisson product versus each proof step.
            assert all(n * p / 4 <= 1 for p in weights)
            poisson_exact = math.prod(2 * math.exp(-n * float(p) / 4) - math.exp(-n * float(p) / 2)
                                      for p in weights)
            sum_squares_bound = math.exp(-n * n * sum(float(p) ** 2 for p in weights) / 64)
            minimum_bound = math.exp(-n * n * len(weights) * float(min(weights)) ** 2 / 64)
            assert poisson_exact <= sum_squares_bound + 1e-15 <= minimum_bound + 2e-15
            fixed_exact = float(state_DP(weights, n))
            assert fixed_exact <= poisson_exact + math.exp(-(math.log(2) - 0.5) * n) + 1e-14
            bound_cases += 1
    round_cases = 0
    # Exact rounded root against ceil inequality; no irrational approximation.
    for s in range(1, 9):
        for a in range(1, 40):
            for b in range(1, 10):
                q = F(a, b)
                if q < 1:
                    continue
                m = math.ceil(q)
                assert q ** s <= m ** s <= 2 ** s * q ** s
                round_cases += 1
    return {"uniform_cell_exact_DP_vs_inclusion_cases": exact_cases,
            "nonuniform_patch_poisson_and_coupling_cases": bound_cases,
            "rounding_cases": round_cases,
            "outside_patch_probability_is_retained": True}


def rank_controls():
    rng = random.Random(3883)
    cases = 0
    for rank in range(1, 9):
        for _ in range(4000):
            u = [rng.uniform(-1, 1) for _ in range(rank)]
            v = [rng.uniform(-1, 1) for _ in range(rank)]
            # Independent radii include boundaries, zero, and nearby vectors.
            radii = [0.0, 0.5, rng.random() / 2]
            ru, rv = rng.choice(radii), rng.choice(radii)
            nu = math.sqrt(sum(t * t for t in u))
            nv = math.sqrt(sum(t * t for t in v))
            u = [ru * t / nu for t in u]
            v = [rv * t / nv for t in v]
            distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(u, v)))
            heightdiff = abs(math.sqrt(1 - ru * ru) - math.sqrt(1 - rv * rv))
            assert heightdiff <= distance / math.sqrt(3) + 1e-14
            liftdistance = math.sqrt(distance * distance + heightdiff * heightdiff)
            assert liftdistance <= 2 / math.sqrt(3) * distance + 1e-14
            cases += 1
    moment_cases = 0
    for d in range(2, 70):
        for m in range(0, 25):
            odd = math.prod(range(1, 2 * m, 2))
            moment = F(d ** m * odd, math.prod(d + 2 * j for j in range(m)))
            assert moment <= odd
            moment_cases += 1
    exact_constants = {
        "error_bad_fraction": F(1, 256) / F(1, 16),
        "projection_bad_fraction_at_rank_threshold": F(32, 512),
        "remaining_good_pair_fraction": F(3, 8) - F(1, 16) - F(1, 16),
        "constant_square": F(9, 8192),
        "small_rank_constant_square": F(1, 64),
        "large_rank_constant_square_times_512": F(9, 8192) * 512,
    }
    assert exact_constants["remaining_good_pair_fraction"] == F(1, 4)
    assert exact_constants["constant_square"] <= exact_constants["small_rank_constant_square"]
    assert exact_constants["large_rank_constant_square_times_512"] == F(9, 16)
    assert -1 + math.log(2) / 2 + math.log(9) / 8 <= -0.25
    assert 4 * F(3, 8) * F(5, 8) == F(15, 16)
    return {"fiber_lift_boundary_and_interior_cases": cases, "exact_moment_cases": moment_cases,
            "counting_and_constant_fractions": {key: str(value) for key, value in exact_constants.items()},
            "net_log_exponent_at_n8d": -1 + math.log(2) / 2 + math.log(9) / 8,
            "rank_d_is_handled_only_by_large_rank_branch": True}


checks["circle_exact"] = circle_exact()
checks["circle_random_law"] = circle_distribution_control()
checks["chart_birthday"] = birthday_controls()
checks["sphere_rank"] = rank_controls()
output = {"created_utc": datetime.now(timezone.utc).isoformat(), "all_controls_passed": True,
          "python_standard_library_only": True,
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "checks": checks,
          "limitations": "Finite and numerical controls support the independent written audit; they do not replace its proofs or certify the whole conjecture."}
(ROOT / "INDEPENDENT_GEOMETRY_CONTROLS.json").write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps({"all_controls_passed": True, "families": list(checks),
                  "output": str(ROOT / "INDEPENDENT_GEOMETRY_CONTROLS.json")}, indent=2))
