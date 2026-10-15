"""Independent inspection of stored, complete reproduction enclosures.

This reads recorded balls and immutable archive bytes. It reruns no upstream
calculation and does not purport to certify analytic or topological arguments.
"""
from pathlib import Path
from fractions import Fraction
import datetime
import hashlib
import json
import sys
import zipfile
from flint import arb, ctx

ctx.prec = 256
root = Path(__file__).resolve().parents[2]
receipt_dir = root / "receipts" / sys.argv[1]
archive = root / "publication" / sys.argv[2]
sha = lambda b: hashlib.sha256(b).hexdigest()
receipt = json.loads((receipt_dir / "REPRODUCTION_RECEIPT.json").read_text())
assert receipt["status"] == "PASS_ALL_AUTHORED_COMPUTATIONS"
assert receipt["quick"] is False and receipt["manifest_verified"] is True
assert receipt["python"] == "3.12.14" and receipt["python_flint"] == "0.9.0"
assert receipt["pdf_build_and_text_verified"] is True
with zipfile.ZipFile(archive) as z:
    manifest = json.loads(z.read("PACKAGE_MANIFEST.json"))
    assert receipt["package_identity_sha256"] == manifest["package_identity_sha256"]
    for entry in manifest["files"]:
        b = z.read(entry["path"])
        assert len(b) == entry["bytes"] and sha(b) == entry["sha256"]
    checks = {c["label"]: c for c in receipt["checks"]}
    assert len(checks) == len(receipt["checks"]) == 7
    assert set(checks) == {"fixed_constants", "wreath_orientation", "exact_lattice", "scalar_bounds", "validated_integrals", "secondary_bernstein", "publication_pdf"}
    for name, c in checks.items():
        assert c["returncode"] == 0
        for stream in ("stdout", "stderr"):
            b = (receipt_dir / (name + "." + stream + ".txt")).read_bytes()
            assert sha(b) == c[stream + "_sha256"]
            if stream == "stderr":
                assert b == b""
        if "receipt_sha256" in c:
            assert sha((receipt_dir / (name + ".receipt.json")).read_bytes()) == c["receipt_sha256"]
    load = lambda name: json.loads((receipt_dir / (name + ".receipt.json")).read_text())
    scal = load("scalar_bounds")
    primary = load("validated_integrals")
    secondary = load("secondary_bernstein")
    for r, key, path in [(scal, "source_sha256", "target_b/independent_scalar_checks.py"), (primary, "script_sha256", "target_b/independent_validated_integrals.py"), (secondary, "implementation_sha256", "reproducibility/checks/standalone_arb_bernstein.py")]:
        assert r[key] == sha(z.read(path))
    assert secondary["authored_data_json_sha256"] == sha(z.read("publication/support/data/planar_certificate_tables.json"))
    assert all(r["status"].startswith("pass") for r in (scal, primary, secondary))

# Reconstruct expected geometry from the definition of the interpolation set.
residues = {0, 1, 3, 4, 7, 9}
nodes = [n for n in range(1, 101) if n % 12 in residues]
assert len(nodes) == 51
whole = [0] + nodes
expected = set()
for m in [0] + [n for n in nodes if n <= 40]:
    q = whole.index(m)
    directions = [Fraction(whole[q + 1] - m, 2)]
    if q:
        directions.append(Fraction(whole[q - 1] - m, 2))
    for y in directions:
        for i in (1, 2):
            if i == 1 and (m == 0 or (m == 1 and y < 0)):
                continue
            expected.add((i, m, y))
assert len(expected) == 84
direction = lambda v: Fraction(str(v)).limit_denominator(2)
seen = set()
for r in primary["Bernstein_intervals"]:
    key = (r["i"], r["m"], direction(arb(r["y"]).mid().str(30, radius=False)))
    assert key not in seen
    seen.add(key)
    m = r["m"]
    bound = arb(".74" if m == 0 else ".18" if m == 1 else ".02" if m in (3, 4) else ".009")
    assert arb(r["minimum"]) > bound
assert seen == expected
assert {(r["i"], r["m"]) for r in primary["residuals"]} == {(i, m) for i in (1, 2) for m in nodes}
assert len(primary["residuals"]) == 102
for r in primary["residuals"]:
    assert arb(r["c"]) < arb("1e-9") and arb(r["d"]) < arb("1e-9")
assert set(primary["W_checks"]) == {"1", "-1"}
for c in primary["W_checks"].values():
    defect, norm = arb(c["defect"]), arb(c["norm_W"])
    assert defect < arb(".001") and norm / (1 - defect) < 32
assert {r["eta"] for r in primary["cross_certificates"]} == {1, -1}
for c in primary["cross_certificates"]:
    assert arb(c["WU"]) / (1 - arb(c["defect"])) < arb("3.7")
    assert arb(c["inverse_upper"]) < 32 and arb(c["cross_upper"]) < arb("3.7")
assert arb(primary["low_exterior_norm"]) < arb(".09")
assert primary["coverage"] == {"finite_nodes": 51, "matrix_signs": 2, "residual_pairs": 102, "half_gap_intervals": 84, "Bernstein_inequalities": 2436}

# Stronger lower thresholds are transcribed from the original Appendix table.
groups = [(0, 0, (None, ".762")), (1, 1, (".314", ".191")), (3, 4, (".028", ".024")), (7, 9, (".114", ".112")), (12, 16, (".0105", ".0094")), (19, 21, (".123", ".113")), (24, 28, (".0111", ".0113")), (31, 33, (".121", ".126")), (36, 40, (".0107", ".0115"))]
seen = set()
count = 0
for r in secondary["checks"]:
    i, m = r["function_index"], r["center"]
    key = (i, m, direction(arb(r["y"]).mid().str(30, radius=False)))
    assert key not in seen
    seen.add(key)
    bound = next(arb(g[i - 1]) for lo, hi, g in groups if lo <= m <= hi)
    balls = r["all_29_bernstein_enclosures"]
    assert len(balls) == 29
    for b in balls:
        assert arb(b) > bound
        count += 1
assert seen == expected and count == 2436
for key, bound in {"0": "28", "4": ".28", "16": ".015", "100": "5e-10"}.items():
    assert arb(scal["row_tail_envelopes"][key]) < arb(bound)
for key, bound in {"atom_tail": "3.2e-8", "exact_list_error": ".00003", "finite_inverse_bound": "90", "tail_second_derivative_bound": ".006", "quadrature_error_bound": "1e-22"}.items():
    assert arb(scal[key]) < arb(bound)
for v in scal["coefficient_norms"]:
    assert arb(v) < arb("2.29")
for v in scal["coefficient_tail_norms"]:
    assert arb(v) < arb(".00002")
for v, lower in zip(scal["rational_part_lower_bounds"], (".012", ".016")):
    assert arb(v) > arb(lower) and arb(v) - arb(".00003") / arb("1.5") > arb(".011")
for v, bound in zip(scal["quotient_perturbation_bounds"], (".004", ".011", ".011", ".002")):
    assert arb(v) < arb(bound)
assert len(scal["Taylor_remainder_bounds"]) == 5
assert len(scal["midpoint_barriers"]) == 6
assert all(arb(v) < arb(".001") for v in scal["Taylor_remainder_bounds"])
assert all(arb(v) > arb(".68") for v in scal["midpoint_barriers"])
result = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "PASS_INDEPENDENT_STORED_ENCLOSURE_ASSESSMENT", "archive_sha256": sha(archive.read_bytes()), "package_identity_sha256": receipt["package_identity_sha256"], "receipt_sha256": sha((receipt_dir / "REPRODUCTION_RECEIPT.json").read_bytes()), "started_utc": receipt["started_utc"], "finished_utc": receipt["finished_utc"], "checks": 7, "residual_pairs": 102, "half_gap_intervals": 84, "secondary_bernstein_enclosures": count, "script_sha256": sha(Path(__file__).read_bytes()), "limit": "Inspection of retained interval evidence and coverage, not a new quadrature run or formal proof"}
(Path(__file__).parent / (sys.argv[1] + "_assessment.json")).write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
