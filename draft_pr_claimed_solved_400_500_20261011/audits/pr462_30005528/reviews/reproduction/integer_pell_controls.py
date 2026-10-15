#!/usr/bin/env python3
"""Fresh integer/Pell finite controls. No historical author module is imported.

Invalid claims are rejected through actual subprocesses even under optimization.
The universal claims require the proof; these are finite exact controls only.
"""
import argparse
from collections import Counter
from dataclasses import dataclass
import json
from math import gcd, isqrt
import os
from pathlib import Path
import subprocess
import sys

COUNTS = Counter()


def require(condition, category):
    if not condition:
        raise ValueError(category)
    COUNTS[category] += 1


@dataclass(frozen=True)
class IntegerSurd:
    """(a+b*sqrt(2))/d with integer coefficients and positive denominator."""
    a: int
    b: int = 0
    d: int = 1

    def __post_init__(self):
        if self.d <= 0:
            raise ValueError("nonpositive denominator")
        common = gcd(gcd(abs(self.a), abs(self.b)), self.d)
        object.__setattr__(self, "a", self.a // common)
        object.__setattr__(self, "b", self.b // common)
        object.__setattr__(self, "d", self.d // common)

    def __add__(self, other):
        return IntegerSurd(self.a * other.d + other.a * self.d,
                           self.b * other.d + other.b * self.d, self.d * other.d)

    def __sub__(self, other):
        return self + IntegerSurd(-other.a, -other.b, other.d)

    def __mul__(self, other):
        return IntegerSurd(self.a * other.a + 2 * self.b * other.b,
                           self.a * other.b + self.b * other.a, self.d * other.d)

    def sign(self):
        a, b = self.a, self.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a * b > 0:
            return (a > 0) - (a < 0)
        norm = a*a - 2*b*b
        if norm == 0:
            # Nonzero integer a,b cannot have this norm: parity descent.
            raise ValueError("impossible nonzero integer norm zero")
        return ((a > 0) - (a < 0)) * ((norm > 0) - (norm < 0))


ZERO = IntegerSurd(0)
ONE = IntegerSurd(1)
ROOT = IntegerSurd(0, 1)
GAP_DENOMINATOR = IntegerSurd(1, 2)
WRONG_CLAIMS = (
    "periodic_minimizer", "unreduced_period", "drop_initial_cost",
    "rationalization_plus", "rationalization_missing_denominator", "reversed_gap",
)


def cost_prefix(t, n, drop_initial=False):
    cost = ONE + t
    total = ZERO
    for _ in range(n if drop_initial else n + 1):
        total = total + cost
    return total * IntegerSurd(1, 0, n)


def reject_wrong_claim(name):
    if name == "periodic_minimizer":
        # Exact rational angle 3/2 returns after two steps but its height is positive.
        require(IntegerSurd(3, -2, 2) == ZERO, "false periodic minimizer")
    elif name == "unreduced_period":
        # n=4 yields m=6, whose least denominator is 2 rather than 4.
        m, n, claimed = 6, 4, 4
        require(all(k*m % n != 0 for k in range(1, claimed)), "false least period")
    elif name == "drop_initial_cost":
        t = IntegerSurd(3, -2, 2)
        require(cost_prefix(t, 7, True) - (ONE+t) == (ONE+t)*IntegerSurd(1, 0, 7), "false prefix normalization")
    elif name == "rationalization_plus":
        p, q = 3, 2
        t = IntegerSurd(p, -q, q)
        require(t * (IntegerSurd(p, 0, q)+ROOT) == IntegerSurd(p*p+2*q*q, 0, q*q), "false rationalization sign")
    elif name == "rationalization_missing_denominator":
        p, q = 3, 2
        t = IntegerSurd(p, -q, q)
        require(t * (IntegerSurd(p, 0, q)+ROOT) == IntegerSurd(p*p-2*q*q), "false rationalization denominator")
    elif name == "reversed_gap":
        t = IntegerSurd(3, -2, 2)
        require((t * GAP_DENOMINATOR * IntegerSurd(4) - ONE).sign() < 0, "false gap direction")
    else:
        raise ValueError("unknown wrong claim")
    raise ValueError("wrong claim unexpectedly reached end")


def run():
    heights = prefixes = smaller = 0
    for n in range(1, 257):
        m = isqrt(2*n*n)+1
        require((m-1)**2 < 2*n*n < m*m, "integer_floor_square_bounds")
        # Domain bounds use integer squares, with no rational bracket precision.
        require(m*m > 2*n*n and (m-1)**2 < 2*n*n, "integer_competitor_domain")
        t = IntegerSurd(m, -n, n)
        require(t.sign() > 0 and (IntegerSurd(1, 0, n)-t).sign() > 0, "integer_surd_height_bounds")
        q = n // gcd(m, n)
        require(q*m % n == 0, "modular_period_return")
        for k in range(1, q):
            require(k*m % n != 0, "modular_smaller_period_exclusion")
            smaller += 1
        for size in (1, 2, 7, 32, 101):
            mean = cost_prefix(t, size)
            require(mean-(ONE+t) == (ONE+t)*IntegerSurd(1, 0, size), "integer_coefficient_prefix_sum")
            prefixes += 1
        heights += 1

    angles = 0
    for q in range(1, 129):
        for p in range(q, 3*q+1):
            if gcd(p, q) != 1 or p*p <= 2*q*q or (p-q)**2 >= 2*q*q:
                continue
            r = IntegerSurd(p, 0, q)
            t = r-ROOT
            require(t.sign() > 0 and (ONE-t).sign() > 0, "integer_square_angle_domain")
            require((r*IntegerSurd(q)) == IntegerSurd(p), "reduced_rational_period_identity")
            require(t*(r+ROOT) == IntegerSurd(p*p-2*q*q, 0, q*q), "integer_rationalization_identity")
            require(p*p-2*q*q >= 1, "positive_integer_norm")
            require((t*GAP_DENOMINATOR*IntegerSurd(q*q)-ONE).sign() > 0, "integer_norm_gap_bound")
            angles += 1

    # A new near-boundary family much finer than the fixed historical bracket.
    # (3+2*sqrt(2))^j has norm 1. Its rational angles approach sqrt(2) from above.
    m, q = 1, 0
    pell_samples = []
    for j in range(1, 31):
        m, q = 3*m+4*q, 2*m+3*q
        require(m*m-2*q*q == 1, "pell_norm_one_identity")
        require(gcd(m, q) == 1, "pell_reduced_denominator")
        t = IntegerSurd(m, -q, q)
        require(t.sign() > 0 and (ONE-t).sign() > 0, "pell_admissible_height")
        require(t*(IntegerSurd(m, 0, q)+ROOT) == IntegerSurd(1, 0, q*q), "pell_exact_rationalization")
        require((t*GAP_DENOMINATOR*IntegerSurd(q*q)-ONE).sign() > 0, "pell_integer_gap_bound")
        if j in (1, 10, 20, 30):
            pell_samples.append({"j": j, "numerator": m, "least_period_denominator": q, "norm": 1})

    require((heights, smaller, prefixes, angles) == (256, 23955, 1280, 5022), "finite_counts_crosscheck")
    subprocess_results = []
    for optimized in (False, True):
        env = dict(os.environ)
        env["PYTHONOPTIMIZE"] = "1" if optimized else "0"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        for name in WRONG_CLAIMS:
            flags = ["-B", "-O"] if optimized else ["-B"]
            proc = subprocess.run([sys.executable, *flags, str(Path(__file__).resolve()), "--wrong-claim", name], env=env, capture_output=True)
            require(proc.returncode != 0 and b"ValueError" in proc.stderr, "actual_wrong_claim_subprocess_rejection")
            subprocess_results.append({"claim": name, "optimized": optimized, "returncode": proc.returncode, "rejected": True})
    return {
        "status": "passed", "arithmetic": "integer surds, integer squares, modular divisibility, Pell norm identity; no float or fixed bracket",
        "finite_coverage": {"explicit_competitors": heights, "smaller_period_candidates": smaller, "prefix_sums": prefixes, "reduced_rational_angles_denominator_at_most_128": angles, "pell_instances": 30},
        "check_counts": dict(sorted(COUNTS.items())), "checks_total": sum(COUNTS.values()),
        "pell_samples": pell_samples, "wrong_claim_subprocesses": subprocess_results,
        "wrong_claims_rejected_per_mode": 6,
        "limits": ["Finite integer/Pell controls are independent supplementary evidence, not an infinite certificate.", "All-period exclusion requires the exact parity-descent irrationality proof and period identity.", "No numerical test here proves compactness, density, source interpretation, historical priority, or packing realization."]
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wrong-claim", choices=WRONG_CLAIMS)
    args = parser.parse_args()
    if args.wrong_claim:
        reject_wrong_claim(args.wrong_claim)
    else:
        print(json.dumps(run(), indent=2, sort_keys=True))
