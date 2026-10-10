#!/usr/bin/env python3
"""Recalculate arithmetic specializations and verify the frozen packet.

This is not a formal proof checker. The geometric existence, smoothness,
irreducibility and tangent-map results remain cited literature dependencies.
"""
import argparse
import hashlib
import json
from itertools import combinations
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def arithmetic_and_metadata_checks():
    status = read("STATUS.json")
    checks = []

    def check(name, actual, expected):
        if actual != expected:
            raise AssertionError((name, actual, expected))
        checks.append({"name": name, "actual": actual, "expected": expected,
                       "passed": True})

    cd = status["codimension_one_example"]
    n, a, d = (cd[k] for k in ("n", "a", "d"))
    check("CD dimension and parameter range", n >= 3 and d >= 1 and 0 <= a <= d, True)
    check("CD Fano inequalities", a <= n - 1 and d - a <= n - 1, True)
    check("CD nonisomorphism parameter range", 2 <= a <= d - 2, True)
    degree = comb(d, a)
    check("CD VMRT degree specialization", degree, cd["vmrt_degree"])
    pa = (degree - 1) * (degree - 2) // 2
    check("CD plane curve arithmetic genus", pa, cd["vmrt_arithmetic_genus"])
    numerator = comb(d, a) * (a * (d - a) - 2)
    check("CD genus formula integrality", numerator % 2, 0)
    genus = 1 + numerator // 2
    check("CD relative Hilbert curve genus formula", genus, cd["normalization_genus"])
    check("CD normalization defect", pa - genus, cd["normalization_defect_length"])
    check("CD codimension-one family dimension", n - 2, 1)

    # Independent arithmetic consistency of the genus formula in this example:
    # a simple branch transposition of four sheets acts as two transpositions
    # on the six 2-subsets. A generic projection of a smooth quartic has
    # 2*g(A)-2+2*d = 12 simple branch points. The geometric assertions in this
    # sentence are inputs, not established by this finite computation.
    subsets = list(combinations(range(d), a))
    transposition = {0: 1, 1: 0, **{i: i for i in range(2, d)}}
    moved = sum(tuple(sorted(transposition[i] for i in s)) != s for s in subsets)
    check("CD induced transposition ramification contribution", moved // 2, 2)
    quartic_genus = (d - 1) * (d - 2) // 2
    branch_count = 2 * quartic_genus - 2 + 2 * d
    check("CD projection branch-count arithmetic", branch_count, 12)
    rh_numerator = -2 * degree + branch_count * (moved // 2)
    check("CD Riemann-Hurwitz consistency", 1 + rh_numerator // 2, genus)

    hk = status["degree_minimal_example"]
    n, d = hk["n"], hk["d"]
    check("HK odd degree and nonimmersion range", d >= 3 and d % 2 == 1 and n >= 2 * d, True)
    check("HK irreducibility range", n > d, True)
    weights = [1] * n + [2, d]
    hypersurface_degree = 2 * d
    check("HK dimension from weights", len(weights) - 2, n)
    check("HK index from adjunction", sum(weights) - hypersurface_degree, hk["index"])
    check("HK normalized family dimension", n - d, hk["normalized_family_dimension"])
    check("HK VMRT codimension", (n - 1) - (n - d), hk["vmrt_codimension"])
    check("HK numerical minimal anticanonical degree", hk["index"] * hk["family_degree_wrt_ample_generator"], 5)

    check("Credited prior result disposition", status["disposition"], "credited_prior_result")
    check("No authored research turns", status["turns_completed"], 0)
    chronology = read("CHRONOLOGY.json")
    check("Chronology has no mathematical turns", any(e["mathematical_turn"] for e in chronology["events"]), False)
    check("No new result claimed", status["new_mathematical_result_claimed"], False)
    sources = read("SOURCE_METADATA.json")["sources"]
    check("Four full-text primary sources recorded", sorted(s["id"] for s in sources), ["CD2015", "HK2015", "HM2004", "OWR2011"])
    for source in sources:
        valid = (source["bytes"] > 0 and len(source["sha256"]) == 64
                 and all(c in "0123456789abcdef" for c in source["sha256"])
                 and source["retrieved_url"].startswith("https://")
                 and all(1 <= p <= source["page_count"] for p in source["inspected_pdf_pages_one_based"])
                 and source["included_in_packet"] is False)
        check(source["id"] + " metadata validity", valid, True)

    return {"passed": True, "check_count": len(checks), "checks": checks,
            "limitations": "Checks establish arithmetic consistency and metadata validity; published geometric theorems and human hypothesis verification are dependencies."}


def verify_frozen_manifest():
    manifest = read("FROZEN_MANIFEST.json")
    if any(p.is_dir() for p in ROOT.iterdir()):
        raise AssertionError("Frozen packet must contain only the declared top-level files")
    observed = {p.name for p in ROOT.iterdir() if p.is_file() and p.name != "FROZEN_MANIFEST.json"}
    declared = set(manifest["files"])
    if observed != declared:
        raise AssertionError({"extra_files": sorted(observed - declared),
                              "missing_files": sorted(declared - observed)})
    for name, expected in manifest["files"].items():
        if Path(name).name != name:
            raise AssertionError("Nonlocal path in frozen manifest")
        data = (ROOT / name).read_bytes()
        actual = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        if actual != expected:
            raise AssertionError((name, actual, expected))
    return {"passed": True, "verified_file_count": len(declared),
            "manifest_sha256": hashlib.sha256((ROOT / "FROZEN_MANIFEST.json").read_bytes()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true",
                        help="Before freezing only: write the deterministic arithmetic/metadata result.")
    args = parser.parse_args()
    result = arithmetic_and_metadata_checks()
    if args.write_results:
        if (ROOT / "FROZEN_MANIFEST.json").exists():
            raise RuntimeError("Refusing to alter a frozen packet")
        (ROOT / "CHECK_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"passed": result["passed"], "check_count": result["check_count"]}))
    else:
        stored = read("CHECK_RESULTS.json")
        if stored != result:
            raise AssertionError("Stored arithmetic/metadata output disagrees with recalculation")
        print(json.dumps({"arithmetic_and_metadata": result,
                          "frozen_integrity": verify_frozen_manifest()}, indent=2))
