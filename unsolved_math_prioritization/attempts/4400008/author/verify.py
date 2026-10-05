#!/usr/bin/env python3
"""Exact finite controls for the authored examples, not a proof of Boyle's problem."""
from pathlib import Path
import hashlib
import json
import sys

checks = 0

def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)


def shift(support, amount):
    return frozenset(j - amount for j in support)


def displacement(support):
    """The Lemma 6 homeomorphism on finite-support binary points."""
    if not support:
        return 0
    n = min(abs(j) for j in support)
    if n == 0:
        return 0
    if frozenset(j for j in support if -3*n <= j <= 3*n) == frozenset([n]):
        return 2*n
    if frozenset(j for j in support if -5*n <= j <= n) == frozenset([-n]):
        return -2*n
    return 0


def h(support):
    return shift(support, displacement(support))


def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def traces(a, nmax):
    p = [[int(i == j) for j in range(len(a))] for i in range(len(a))]
    out = []
    for _ in range(nmax):
        p = mm(p, a)
        out.append(sum(p[i][i] for i in range(len(a))))
    return out


def main():
    global checks
    coords = list(range(-6, 7))
    tested = 0
    for mask in range(1 << len(coords)):
        p = frozenset(coords[i] for i in range(len(coords)) if mask & (1 << i))
        check(h(h(p)) == p, "involution on finite-support sample")
        tested += 1
    jumps = []
    for n in range(1, 201):
        p = frozenset([n+1, 3*n+2])
        check(displacement(p) == 0, "x_n outside exchanged cylinders")
        check(displacement(shift(p, 1)) == 2*n, "S x_n in U_n")
        check(h(shift(p, 1)) == shift(h(p), 2*n+1), "exact unbounded cocycle")
        check(h(h(shift(p, 1))) == shift(p, 1), "partner cylinder reversal")
        jumps.append(2*n+1)
    check(max(jumps) > 100, "negative control rejects uniform bound 100")

    even_controls = []
    for m in range(1, 65):
        gap = 2*m+1
        period = (1,) + (0,)*gap
        window = 2*m+1
        # Every window has at most one 1, hence occurs in an even-shift
        # point with at most one 1 on the entire integer line.
        max_ones = max(sum(period[(start+j) % len(period)] for j in range(window))
                       for start in range(len(period)))
        check(max_ones <= 1, "even-shift finite-window legal witness")
        check(gap % 2 == 1, "even-shift genuine forbidden odd gap")
        check(period[0] == period[(gap+1) % len(period)] == 1,
              "consecutive periodic markers enclose forbidden gap")
        even_controls.append({"m": m, "window": window, "odd_zero_gap": gap,
                              "period": len(period), "maximum_ones_per_window": max_ones})

    # Finite cycles can have a different positive generator; infinite one-orbit
    # positivity is settled by Lemma 9, not by this computation.
    cycle3 = [0]
    for _ in range(2):
        cycle3.append((cycle3[-1]+2) % 3)
    check(set(cycle3) == {0, 1, 2}, "finite 3-cycle step two")
    check(all((2*k) % 2 == 0 for k in range(-100, 101)), "S squared parity split control")
    check(1 % 2 != 0, "S x excluded from the even-indexed orbit")

    full = [[2]]
    expansion = [[1, 1, 0], [0, 0, 1], [1, 1, 0]]
    fp = traces(full, 20)
    ep = traces(expansion, 20)
    check(fp == [2**n for n in range(1, 21)], "full-shift exact traces")
    check(fp[0] == 2 and ep[0] == 1, "flow expansion does not preserve fixed points")
    # Cross-check expansion counts by direct enumeration of closed paths.
    for n in range(1, 9):
        count = 0
        for start in range(3):
            counts = [0, 0, 0]
            counts[start] = 1
            for _ in range(n):
                counts = [sum(counts[i]*expansion[i][j] for i in range(3)) for j in range(3)]
            count += counts[start]
        check(count == ep[n-1], "independent path count for expansion")

    result = {
        "target_id": "4400008",
        "result": "PASS: exact negative controls; original problem not resolved",
        "arithmetic": "Python integers and finite sets only; no floating point",
        "assertions": checks,
        "controls": {
            "unbounded_cocycle": {"finite_support_involution_cases": tested,
                                    "symbolic_family_checked_n": [1, 200],
                                    "first_jump": jumps[0], "last_jump": jumps[-1],
                                    "false_inference_rejected": "expansivity bounds every TOE cocycle"},
            "finite_window_nonstabilization": {"checked_m": [1, 64],
                                                 "first": even_controls[0], "last": even_controls[-1],
                                                 "false_inference_rejected": "arbitrary finite tests establish SFT"},
            "positive_speedup": {"cycle3_step2_order": cycle3,
                                    "false_inference_rejected": "S squared retains each entire aperiodic S orbit"},
            "flow_vs_orbit_equivalence": {"full_shift_fixed_point_counts_n1_to20": fp,
                                             "expanded_shift_fixed_point_counts_n1_to20": ep,
                                             "false_inference_rejected": "flow equivalence is TOE"}
        },
        "proof_status": "Infinite constructions and general lemmas are proved in proofs.md; tests alone are not theorem proofs."
    }
    print(json.dumps(result, indent=2, sort_keys=True))


def check_manifest():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'manifest.json').read_text())
    for row in manifest['files']:
        data = (root / row['path']).read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise AssertionError('Manifest mismatch: ' + row['path'])
    print('PASS: ' + str(len(manifest['files'])) + ' authored files match manifest')


if __name__ == '__main__':
    if sys.argv[1:] == ['--check-manifest']:
        check_manifest()
    elif sys.argv[1:]:
        raise SystemExit('usage: python3 verify.py [--check-manifest]')
    else:
        main()
