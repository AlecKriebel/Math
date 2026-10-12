#!/usr/bin/env python3
"""Reproduce the small cyclic-group checks in binary_root_route.md.

Group elements are additive exponents modulo Q. These are exhaustive finite
falsification checks, not an implementation of finite-field root extraction or
a proof of the unrestricted claim. Only the Python standard library is used.
Run: python3 -B agent_notes/binary_root_checks.py > agent_notes/binary_root_checks.json
"""

from datetime import datetime, timezone
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
import platform


def check():
    # This is the executable check preserved verbatim in the research note.
    isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n**0.5)+1))
    branches = cases = 0
    for Q in range(1, 161):
        for D in range(1, Q+1):
            if Q % D:
                continue
            for ell in range(2, D+1):
                if D % ell or not isprime(ell):
                    continue
                for a in range(0, Q, D):
                    roots = [x for x in range(Q) if (ell*x-a) % Q == 0]
                    assert roots and all(x % (D//ell) == 0 for x in roots)
                    branches += len(roots)
    for Q in range(1, 81):
        for r in range(1, 201):
            g = gcd(r, Q)
            M = Q//g
            for a in range(Q):
                if a % g:
                    continue
                if M == 1:
                    x = 0
                else:
                    c = (a*pow(r//g, -1, M)) % Q
                    D = g
                    ell = 2
                    while D > 1:
                        if D % ell:
                            ell += 1
                            continue
                        roots = [v for v in range(Q) if (ell*v-c) % Q == 0]
                        assert roots
                        c = roots[-1]
                        D //= ell
                        assert c % D == 0
                    x = c
                assert (r*x-a) % Q == 0
                cases += 1
    assert (branches, cases) == (37856, 473806)
    # F_3*, represented as the cyclic additive group of order2: the first
    # square root of identity0 may be1, and that element has no square root.
    naive_roots = [x for x in range(2) if (2*x-1) % 2 == 0]
    assert naive_roots == []
    return {
        "status": "passed",
        "all_choice_root_branches": branches,
        "complete_largest_choice_cases": cases,
        "invariant_scope": {"Q_max": 160, "D": "every divisor of Q",
                            "ell": "every prime divisor of D",
                            "a": "every D-th power", "roots": "all"},
        "complete_scope": {"Q_max": 80, "r_max": 200,
                           "a": "every solvable group element",
                           "root_choice": "largest additive exponent"},
        "naive_counterexample": {"Q": 2, "r": 4, "a_exponent": 0,
                                  "first_square_root_exponent": 1,
                                  "next_square_roots": naive_roots},
        "limitation": "Finite cyclic-group checks; unbounded claim requires the proof.",
    }


if __name__ == "__main__":
    result = check()
    result.update({"timestamp_utc": datetime.now(timezone.utc).isoformat(),
                   "python_version": platform.python_version(),
                   "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest()})
    print(json.dumps(result, indent=2, sort_keys=True))
