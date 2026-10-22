#!/usr/bin/env python3
"""Independent finite controls and bound replay of the frozen authored packet.

Usage: python3 audit_verify.py /path/to/author-packet.zip
No network access, writes, third-party packages, or dynamic imports from the packet.
The packet's known verifier is executed only after the exact ZIP digest is checked.
Finite model checks do not certify a theorem about elliptic dynamics.
"""
import ast
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
import zipfile

EXPECTED_SHA256 = "5286fc55fc2227f1c10cd03742ab4a6e4d5d261a56888c8b736a5ba031a48919"
EXPECTED_BYTES = 22392


def main(path):
    raw = Path(path).read_bytes()
    if len(raw) != EXPECTED_BYTES or hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError("The input is not the frozen packet reviewed by this audit")
    with zipfile.ZipFile(path) as archive:
        contents = {name: archive.read(name) for name in archive.namelist()}
    manifest = json.loads(contents["MANIFEST.json"])
    expected = {item["path"] for item in manifest["files"]}
    if set(contents) != expected | {"MANIFEST.json"}:
        raise AssertionError("Packet inventory mismatch")
    for item in manifest["files"]:
        data = contents[item["path"]]
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise AssertionError("Manifest mismatch: " + item["path"])

    hits = Counter()

    def record(line):
        hits[line] += 1

    class Instrument(ast.NodeTransformer):
        def visit_Assert(self, node):
            call = ast.Expr(ast.Call(ast.Name("_audit_hit", ast.Load()),
                                     [ast.Constant(node.lineno)], []))
            return [ast.copy_location(call, node), node]

    tree = Instrument().visit(ast.parse(contents["verify.py"].decode()))
    ast.fix_missing_locations(tree)
    namespace = {"__name__": "independently_instrumented_verifier", "_audit_hit": record}
    exec(compile(tree, "frozen-verify.py", "exec"), namespace)
    reported = namespace["run"]()
    if reported != json.loads(contents["CONTROL_RESULTS.json"]):
        raise AssertionError("Authored output does not reproduce")
    actual = sum(hits.values())
    if actual != 7580 or sum(hits[n] for n in (18, 19, 20, 22, 23)) != 5600:
        raise AssertionError("Unexpected assertion count")
    corrected = dict(reported)
    corrected["families"] = dict(reported["families"])
    corrected["families"]["exponent_and_moment_identities"] = 5600
    corrected["total_exact_assertions"] = 7580

    checks = Counter()

    def check(family, value):
        checks[family] += 1
        if not value:
            raise AssertionError((family, checks[family]))

    triples = 0
    for q in range(1, 17):
        for p in range(1, 17):
            for j in range(1, 128):
                h = Q(1) + Q(j, 128)
                if h <= Q(2*q, q+1):
                    continue
                triples += 1
                alpha = (q+1)*h - 2*q
                beta = (p+1)*h - p
                a = Q(p+1, p)*h
                family = "expanded_exponent_and_moment_grid"
                check(family, alpha > 0)
                check(family, h-alpha == q*(2-h))
                check(family, beta-h == p*(h-1))
                check(family, beta-alpha == p*(h-1) + q*(2-h))
                check(family, -alpha/q == 2-Q(q+1,q)*h)
                check(family, p*(a-1) == beta)
                check(family, (a>2) == (h>Q(2*p,p+1)))
    for q in range(1, 33):
        check("boundary_controls", (q+1)*Q(2*q,q+1)-2*q == 0)
        check("boundary_controls", (q+1)*2-2*q == 2)
    for p in range(1, 33):
        check("boundary_controls", Q(p+1,p)*Q(2*p,p+1) == 2)
        check("boundary_controls", (p+1)*1-p == 1)

    for c in (Q(1,3), Q(1), Q(2), Q(7,4)):
        for initial in (Q(1,11), Q(2,5), Q(1), Q(5,2)):
            x, derivative = initial, Q(1)
            for n in range(257):
                check("generalized_parabolic_iteration", x == initial/(1+n*c*initial))
                check("generalized_parabolic_iteration", derivative == (1+n*c*initial)**-2)
                derivative /= (1+c*x)**2
                x /= 1+c*x
        for n in range(257):
            lower = Q(1,2)/c
            upper = 1/c
            check("parabolic_interval_geometry", lower/(1+n*c*lower) == 1/(c*(n+2)))
            check("parabolic_interval_geometry", upper/(1+n*c*upper) == 1/(c*(n+1)))
            check("parabolic_interval_geometry", 1/(c*(n+1))-1/(c*(n+2)) == 1/(c*(n+1)*(n+2)))

    seeds = (Q(1,2), Q(2,3), Q(5,4))
    for d in range(1,6):
        for numerator in range(1,13):
            for source_root in seeds:
                for target_root in seeds:
                    for derivative_root in seeds:
                        # rho_source=source_root**d, rho_target=target_root**d,
                        # |f'|=derivative_root**d and h=numerator/d.
                        left = target_root**(-numerator)*(derivative_root*target_root/source_root)**numerator
                        right = derivative_root**numerator*source_root**(-numerator)
                        check("nonintegral_metric_cocycle", left == right)
    check("metric_sign_negative_control", Q(1,3)**2*Q(2,3)**2 != Q(1)**2*Q(1,2)**2)

    for n in range(1,33):
        square = 0
        round_annulus = 0
        for x in range(-2*n,2*n+1):
            for y in range(-2*n,2*n+1):
                square += n <= max(abs(x),abs(y)) < 2*n
                round_annulus += n*n <= x*x+y*y < 4*n*n
        check("direct_lattice_enumeration", square == 12*n*n-4*n)
        check("direct_lattice_enumeration", round_annulus >= 2*n*n)
        check("direct_lattice_enumeration", round_annulus <= 16*n*n)

    for a in range(2,8):
        for k in range(1,257):
            integral = (Q(k)**(1-a)-Q(k+1)**(1-a))/(a-1)
            check("integral_test_cell_bounds", integral <= Q(k)**(-a))
            check("integral_test_cell_bounds", integral >= Q(k+1)**(-a))
        for start in (1,2,5,16,31):
            end = 256
            partial = sum((Q(k)**(-a) for k in range(start,end+1)),Q(0))
            lower = partial + Q(end+1)**(1-a)/(a-1)
            upper = partial + Q(end)**(1-a)/(a-1)
            check("tail_integral_brackets", lower <= upper)
            check("tail_integral_brackets", lower >= Q(start)**(1-a)/(a-1))
            check("tail_integral_brackets", upper <= Q(start)**(-a)+Q(start)**(1-a)/(a-1))

    # A compact full-support exact Hausdorff measure need not have uniform balls.
    # E={0} union [2^-n,2^-n+4^-n/4], n>=1, and mu=12 H^1|E.
    check("exact_measure_nonuniform_ball_example", sum((Q(1,4)**n/4 for n in range(1,101)),Q(0)) + Q(1,4)**101/3 == Q(1,12))
    for n in range(6,129):
        r = Q(1,2)**n
        mass_at_zero = 12*(Q(1,4)**(n+1)/3)
        mass_at_interior = 24*r
        check("exact_measure_nonuniform_ball_example", mass_at_zero == r*r)
        check("exact_measure_nonuniform_ball_example", mass_at_interior/mass_at_zero == 24*2**n)

    # d_n=2^-n alone does not control log_2(D_n/d_n). These are formal sequences,
    # not claimed derivatives of any realized elliptic map.
    for n in range(1,129):
        check("missing_recurrence_rate_countermodel", Q(2**n,4**n+n) <= Q(1,2**n))
    # Pareto exceedance probabilities retain the same convergence type under
    # multiplying the deterministic threshold by any fixed positive constant.
    for kappa in range(1,9):
        for threshold in range(1,33):
            for multiplier in range(1,9):
                check("pareto_exceedance_scaling", Q(multiplier*threshold)**(-kappa) == Q(multiplier)**(-kappa)*Q(threshold)**(-kappa))

    return {
        "frozen_packet_sha256": EXPECTED_SHA256,
        "frozen_packet_bytes": EXPECTED_BYTES,
        "zip_entries": len(contents),
        "manifest_payloads_verified": len(expected),
        "author_output_reproduced": True,
        "author_reported_assertions": reported["total_exact_assertions"],
        "actual_executed_author_assert_statements": actual,
        "author_assert_statement_counts_by_line": dict(sorted(hits.items())),
        "corrected_author_control_results": corrected,
        "independent_exact_checks": sum(checks.values()),
        "independent_families": dict(sorted(checks.items())),
        "expanded_grid_accepted_triples": triples,
        "all_passed": True,
        "scope": "Finite algebraic, sequence, and elementary measure model controls only. No elliptic parameter or exact gauge is constructed. Borel-Cantelli and geometric covering arguments are checked analytically in AUDIT.md, not certified by finite controls."
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(json.dumps(main(sys.argv[1]),indent=2,sort_keys=True))
