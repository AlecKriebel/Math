#!/usr/bin/env python3
"""Exact finite controls for the 2305073 partial-results packet.

These tests check formulas and finite construction invariants, not the full
analytic theorems. Only the Python standard library is required.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


ROOT = Path(__file__).resolve().parent
PAYLOAD = {
    "README.md", "PARTIAL_RESULTS.md", "APPROACH_LOG.md",
    "SOURCE_VERIFICATION.json", "verify_controls.py", "CONTROL_RESULTS.json",
}
COUNTS = Counter()


def check(group, condition):
    if not condition:
        raise AssertionError(group)
    COUNTS[group] += 1


def spike_controls():
    # alpha=1/m makes all original lengths, masses, and powers rational.
    for m in range(2, 17):
        q = F(1, 2**m)
        for n in range(1, 41):
            length = q**n
            height = F(2**n)
            mass = F(1, 2**n)
            tail = length / (1-q)
            next_tail = length*q/(1-q)
            check("spike_scaling", length == mass**m)
            check("spike_pairing", height*mass == 1)
            check("rearrangement_cell", tail-next_tail == length)
            check("atomic_rearrangement_bound", height**m*tail == 1/(1-q))
            check("integrable_spike_ratio", 2*q < 1)
            check("separated_geometry", length < F(1, 2))
        for N in range(1, 41):
            check("finite_spike_mass", sum((F(1, 2**n) for n in range(1, N+1)), F()) == 1-F(1, 2**N))
            check("finite_spike_pairing", sum((F(2**n)*F(1, 2**n) for n in range(1, N+1)), F()) == N)
    # At alpha=1/2, C_alpha=2 sqrt(2)<3 and 2^alpha<2.
    check("coarse_uniform_spike_bound", F(8) < 9)
    check("coarse_uniform_spike_bound", F(2) < 4)
    check("coarse_uniform_spike_bound", 3+2 == 5)
    # Exact rational samples of the geometric distance estimates. The proof
    # covers every real t; this sample does not establish that universal claim.
    intervals = [(F(3*n), F(3*n)+F(1, 4**n)) for n in range(1, 21)]
    def distance(t, interval):
        a, b = interval
        return max(a-t, F(), t-b)
    for j in range(-16, 520):
        t = F(j, 8)
        nearby = [n for n in range(1, 21) if abs(t-3*n) < 1]
        check("neighborhood_uniqueness", len(nearby) <= 1)
        if nearby:
            n = nearby[0]
            check("far_interval_distance", all(distance(t, I) > 1 for k, I in enumerate(intervals, 1) if k != n))
        else:
            check("outside_neighborhood_distance", all(distance(t, I) >= F(1, 2) for I in intervals))


def cantor_controls():
    # Finite construction geometry at r=1/3. The proof establishes the
    # corresponding infinite measure by its consistent cylinder masses.
    intervals = [(F(), F(1), "")]
    for depth in range(10):
        expected_length = F(1, 3**depth)
        for a, b, bits in intervals:
            check("cantor_length", b-a == expected_length)
            check("cantor_coding", len(bits) == depth)
        for left, right in zip(intervals, intervals[1:]):
            check("cantor_minimum_gap", right[0]-left[1] >= expected_length)
        check("cantor_total_mass", len(intervals)*F(1, 2**depth) == 1)
        check("cantor_total_length", sum((b-a for a, b, _ in intervals), F()) == F(2, 3)**depth)
        for n in range(1, depth+1):
            prefix = "0"*(n-1)+"1"
            count = sum(bits.startswith(prefix) for _, _, bits in intervals)
            check("cantor_first_right_mass", count*F(1, 2**depth) == F(1, 2**n))
        intervals = [(a, a+(b-a)/3, bits+"0") for a, b, bits in intervals] + [(b-(b-a)/3, b, bits+"1") for a, b, bits in intervals]
        intervals.sort()
    for N in range(1, 101):
        check("cantor_obstacle_pairing", sum((F(2**n)*F(1, 2**n) for n in range(1, N+1)), F()) == N)
    # sqrt(3)<7/4 and sqrt(3)/2<7/8, proved by positive squares.
    check("cantor_geometric_convergence", F(3) < 4)
    check("cantor_rational_upper_bound", F(3) < F(7, 4)**2)
    check("cantor_rational_upper_bound", F(3, 4) < F(7, 8)**2)
    K = 2 + 2*F(1, 3)/(1-2*F(1, 3))
    check("cantor_cover_constant", K == 4)
    check("cantor_potential_bound_57", 1+K*F(7, 4)/(1-F(7, 8)) == 57)


def interval_atom_controls():
    # At alpha=1/2, choose L=2u^2, so the atomic mass b sqrt(L/2)=bu.
    for u in [F(1, 8), F(1, 3), F(1), F(7, 2), F(10)]:
        for b in [F(1, 9), F(1, 2), F(1), F(5), F(31, 4)]:
            L = 2*u*u
            atom_mass = b*u
            for j in range(-16, 17):
                distance = abs(F(j, 16))*L/2
                # At distance zero a positive atom gives infinity. At other
                # distances, the squared inequality is equivalent to
                # atom_mass/sqrt(distance) >= b.
                check("interval_atom_positive_mass", atom_mass > 0)
                if distance:
                    check("interval_atom_lower_bound", atom_mass**2 >= b*b*distance)
                else:
                    check("interval_atom_center", distance == 0)
            check("interval_atom_endpoint_equality", atom_mass**2 == b*b*L/2)
    for N in range(1, 81):
        epsilon = F(1, 2**N)
        weights = [epsilon*F(1, 2**j) for j in range(1, N+1)]
        check("countable_atomic_positive_weights", all(w > 0 for w in weights))
        check("countable_atomic_mass_budget", sum(weights, F()) < epsilon)
    # For alpha=1/2, C_alpha<3. L=(4M+1)^2 forces sqrt(L)>3M.
    for M in [F(n, d) for d in range(1, 12) for n in range(0, 51)]:
        root_L = 4*M+1
        check("constant_obstacle_large_interval", root_L > 3*M)


def scope_controls():
    metadata = json.loads((ROOT/"SOURCE_VERIFICATION.json").read_text())
    required = {
        "problem_id": "2305073",
        "problem_number": "AMR-022-5073",
        "kernel": "abs(x-t)**(-alpha)",
        "kernel_normalization": "1",
        "parameter_range": "0 < alpha < 1",
        "target_domination": "pointwise",
        "measure_class": "finite positive Borel measures on R",
        "original_problem_status_in_this_packet": "unresolved",
        "approaches_completed": 5,
        "complete_pointwise_characterization_claimed": False,
        "novelty_claimed": False,
        "remote_writes_by_author": 0,
        "fresh_independent_audit_complete": False,
    }
    for key, value in required.items():
        check("scope_metadata", metadata.get(key) == value)
    check("primary_pdf_identity", metadata["primary_source"]["local_pdf_sha256"] == "8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0")
    check("primary_pdf_identity", metadata["primary_source"]["local_pdf_bytes"] == 1706228)


def check_manifest():
    manifest_path = ROOT/"AUTHOR_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema") != "function-theory-2305073-authored-packet/v1":
        raise AssertionError("manifest schema")
    if set(manifest.get("files", {})) != PAYLOAD:
        raise AssertionError("manifest payload set")
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}
    if actual != PAYLOAD | {"AUTHOR_MANIFEST.json"}:
        raise AssertionError("unexpected or missing file")
    for name in sorted(PAYLOAD):
        path = ROOT/name
        if path.is_symlink():
            raise AssertionError("symlink in packet")
        content = path.read_bytes()
        row = manifest["files"][name]
        if row != {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}:
            raise AssertionError("manifest mismatch: "+name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-manifest", action="store_true")
    args = parser.parse_args()
    if args.check_manifest:
        check_manifest()
    spike_controls()
    cantor_controls()
    interval_atom_controls()
    scope_controls()
    result = {
        "schema": "function-theory-2305073-exact-controls/v1",
        "result": "PASS",
        "arithmetic": "Python standard-library Fraction; no floating point",
        "counts": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "scope": "Finite formula, construction, geometry, and metadata controls only; not an analytic proof or an independent audit.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
