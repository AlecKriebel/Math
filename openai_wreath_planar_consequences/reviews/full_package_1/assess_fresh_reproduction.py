"""Independent audit of identity-bound saved replay evidence, not a theorem prover.

All ball inequalities are reparsed at 256 bits. Finite node and interval coverage
is derived from the stated residue class set, rather than trusting receipt counts.
The underlying mathematical algorithms and their applicability are assessed in
FULL_REVIEW.md; this script verifies the fresh evidence they produced.
"""
import datetime
import hashlib
import json
import re
import zipfile
from fractions import Fraction
from pathlib import Path
from flint import arb, ctx

if not __debug__:
    raise RuntimeError("Assertions must remain enabled")
ctx.prec = 256
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RUN = ROOT / "receipts/clean_reproduction_v1"
ZIP = ROOT / "publication/wreath-planar-verification-v1.0.0.zip"
ZIP_HASH = "c542fd82a510d5a07abcc1b968681a45abc0feae1644c420cca9365d08e6e658"
IDENTITY = "eb94a337611a7be11546cccbbb29350e1338021aa1e9c14b6829f109d8c0e272"
PDF_HASH = "e4ffb02321fd0a826395aadb038a10e28995db2fefde21c57a54c8ff9ae7083c"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def load(label):
    return json.loads((RUN / (label + ".receipt.json")).read_text())

def lt(value, bound):
    assert arb(value) < arb(bound), (value, bound)

def gt(value, bound):
    assert arb(value) > arb(bound), (value, bound)

assert digest(ZIP.read_bytes()) == ZIP_HASH
with zipfile.ZipFile(ZIP) as archive:
    names = archive.namelist()
    assert len(names) == 75 and len(set(names)) == 75
    files = {name: archive.read(name) for name in names}
manifest = json.loads(files["PACKAGE_MANIFEST.json"])
assert manifest["package_identity_sha256"] == IDENTITY
inventory = manifest["files"]
assert len(inventory) == 74
for item in inventory:
    assert digest(files[item["path"]]) == item["sha256"]
    assert len(files[item["path"]]) == item["bytes"]

main = json.loads((RUN / "REPRODUCTION_RECEIPT.json").read_text())
assert main["status"] == "PASS_ALL_AUTHORED_COMPUTATIONS"
assert main["package_identity_sha256"] == IDENTITY
assert main["manifest_verified"] and not main["quick"]
assert main["pdf_requested"] and main["pdf_build_and_text_verified"]
assert main["python"] == "3.12.14" and main["python_flint"] == "0.9.0"
assert main["python_patch_matches_recorded"]
assert main["mathematical_input_consistency"] == {
    "status": "PASS_EXACT_INPUT_CONSISTENCY", "checkers_compared": 2}
expected_labels = {"fixed_constants", "wreath_orientation", "exact_lattice",
                   "scalar_bounds", "validated_integrals", "secondary_bernstein",
                   "publication_pdf"}
assert {c["label"] for c in main["checks"]} == expected_labels
assert len(main["checks"]) == 7
saved_output_hashes = {}
for check in main["checks"]:
    label = check["label"]
    assert check["returncode"] == 0 and check["elapsed_seconds"] > 0
    for stream in ("stdout", "stderr"):
        observed = digest((RUN / (label + "." + stream + ".txt")).read_bytes())
        assert observed == check[stream + "_sha256"]
        saved_output_hashes[label + "." + stream] = observed
    assert (RUN / (label + ".stderr.txt")).read_bytes() == b""
    if "receipt_sha256" in check:
        observed = digest((RUN / (label + ".receipt.json")).read_bytes())
        assert observed == check["receipt_sha256"]
        saved_output_hashes[label + ".receipt"] = observed
    if label != "publication_pdf":
        assert "-I" in check["command"] and "-B" in check["command"]
        assert not any(v == "-O" or v == "-OO" for v in check["command"])

fixed = load("fixed_constants")
assert fixed["status"] == "all checks passed"
assert fixed["script_sha256"] == digest(files["target_a/check_fixed_constants.py"])
assert fixed["q"] == 128 and fixed["alphabet_size"] == 16520
for value in fixed["Mf_over_f_representative_rows"].values():
    assert Fraction(value) < Fraction(199, 200)
orientation = load("wreath_orientation")
assert orientation["status"] == "passed"
assert orientation["nonzero_idempotent_kernel_witness"]
assert not orientation["target_a_group_ring_premise_established"]
lattice = load("exact_lattice")
assert lattice["status"] == "PASS_EXACT_FINITE_CONTROLS"
assert lattice["script_sha256"] == digest(files["bridges/triangle/check_exact_lattice.py"])
assert lattice["triangle_lower_bound"] == "4/3"
assert lattice["fourier_phase"] == "exp(-2*pi*i*<x,xi>)"

data = json.loads(files["publication/support/data/planar_certificate_tables.json"])
nodes = [n for n in range(1, 101) if n % 12 in {0, 1, 3, 4, 7, 9}]
assert len(nodes) == 51
assert nodes == [row[0] for row in data["tables"]["coefficients"]["rows"]]
all_nodes = [0] + nodes
expected_intervals = {}
for m in all_nodes:
    if m > 40:
        break
    p = all_nodes.index(m)
    offsets = [Fraction(all_nodes[p + 1] - m, 2)]
    if p > 0:
        offsets.append(Fraction(all_nodes[p - 1] - m, 2))
    for i in (1, 2):
        for y in offsets:
            if i == 1 and (m == 0 or (m == 1 and y < 0)):
                continue
            expected_intervals[(i, m, y)] = 0 if m == 0 else 1 if i == 1 and m == 1 else 2
assert len(expected_intervals) == 84

def interval_key(i, m, y_string):
    y_ball = arb(y_string)
    candidates = [key for key in expected_intervals if key[0] == i and key[1] == m
                  and y_ball.contains(arb(key[2].numerator) / key[2].denominator)]
    assert len(candidates) == 1, (i, m, y_string)
    # A ball that admitted both signs or another relevant offset fails above.
    return candidates[0]

adaptive = load("validated_integrals")
assert adaptive["status"] == "pass" and adaptive["full_finite_gates"] == "pass"
assert adaptive["precision_bits"] == 160
assert adaptive["script_sha256"] == digest(files["target_b/independent_validated_integrals.py"])
assert adaptive["coverage"] == {"finite_nodes": 51, "matrix_signs": 2,
    "residual_pairs": 102, "half_gap_intervals": 84, "Bernstein_inequalities": 2436}
assert {v["eta"] for v in adaptive["cross_certificates"]} == {1, -1}
assert len(adaptive["cross_certificates"]) == 2
for cross in adaptive["cross_certificates"]:
    for field, threshold in [("defect", ".001"), ("WU", "3.54"),
                             ("inverse_upper", "32"), ("cross_upper", "3.7")]:
        lt(cross[field], threshold)
lt(adaptive["low_exterior_norm"], ".09")
residual_keys = []
for row in adaptive["residuals"]:
    residual_keys.append((row["i"], row["m"]))
    lt(row["c"], "1e-9")
    lt(row["d"], "1e-9")
assert len(residual_keys) == 102 and len(set(residual_keys)) == 102
assert set(residual_keys) == {(i, n) for i in (1, 2) for n in nodes}
adaptive_keys = []
for row in adaptive["Bernstein_intervals"]:
    key = interval_key(row["i"], row["m"], row["y"])
    adaptive_keys.append(key)
    m = row["m"]
    threshold = ".74" if m == 0 else ".18" if m == 1 else ".02" if m in (3, 4) else ".009"
    gt(row["minimum"], threshold)
    assert arb(row["threshold"]).contains(arb(threshold))
assert len(adaptive_keys) == len(set(adaptive_keys)) == 84
assert set(adaptive_keys) == set(expected_intervals)

def stronger_bound(i, m):
    if m == 0:
        return ".762"
    groups = [(1, ".314", ".191"), (4, ".028", ".024"),
              (9, ".114", ".112"), (16, ".0105", ".0094"),
              (21, ".123", ".113"), (28, ".0111", ".0113"),
              (33, ".121", ".126"), (40, ".0107", ".0115")]
    for top, first, second in groups:
        if m <= top:
            return first if i == 1 else second
    raise ValueError(m)

secondary = load("secondary_bernstein")
assert secondary["status"] == "pass_all_finite_bernstein_grouped_claims"
assert secondary["implementation_sha256"] == digest(files["reproducibility/checks/standalone_arb_bernstein.py"])
assert secondary["authored_data_json_sha256"] == digest(files["publication/support/data/planar_certificate_tables.json"])
assert secondary["coefficient_table_upstream_sha256"] == data["files_sha256"]["coefficients.tsv"]
secondary_keys = []
count = 0
for row in secondary["checks"]:
    i, m = row["function_index"], row["center"]
    key = interval_key(i, m, row["y"])
    secondary_keys.append(key)
    assert row["order"] == expected_intervals[key]
    assert len(row["all_29_bernstein_enclosures"]) == 29
    bound = stronger_bound(i, m)
    assert arb(row["claimed_group_lower"]).contains(arb(bound))
    for coefficient in row["all_29_bernstein_enclosures"]:
        gt(coefficient, bound)
        count += 1
assert count == 2436
assert len(secondary_keys) == len(set(secondary_keys)) == 84
assert set(secondary_keys) == set(expected_intervals)

scalar = load("scalar_bounds")
assert scalar["status"] == "pass" and scalar["precision_bits"] == 192
assert scalar["source_sha256"] == digest(files["target_b/independent_scalar_checks.py"])
assert set(scalar["row_tail_envelopes"]) == {"0", "4", "16", "100"}
for cut, upper in [("0", "28"), ("4", ".28"), ("16", ".015"), ("100", "5e-10")]:
    lt(scalar["row_tail_envelopes"][cut], upper)
for field, upper in [("atom_tail", "3.2e-8"), ("exact_list_error", ".00003"),
                     ("finite_inverse_bound", "90"), ("tail_second_derivative_bound", ".006"),
                     ("quadrature_error_bound", "1e-22")]:
    lt(scalar[field], upper)
for field, count_expected, upper in [("coefficient_norms", 2, "2.29"),
    ("coefficient_tail_norms", 2, ".00002"), ("Taylor_remainder_bounds", 5, ".001")]:
    assert len(scalar[field]) == count_expected
    for value in scalar[field]:
        lt(value, upper)
assert len(scalar["rational_part_lower_bounds"]) == 2
for value, lower in zip(scalar["rational_part_lower_bounds"], (".012", ".016")):
    gt(value, lower)
assert len(scalar["quotient_perturbation_bounds"]) == 4
for value, upper in zip(scalar["quotient_perturbation_bounds"], (".004", ".011", ".011", ".002")):
    lt(value, upper)
assert len(scalar["midpoint_barriers"]) == 6
for value in scalar["midpoint_barriers"]:
    gt(value, ".68")

pdf = next(c for c in main["checks"] if c["label"] == "publication_pdf")
assert pdf["packaged_pdf_sha256"] == PDF_HASH
assert digest(files["publication/preprint.pdf"]) == PDF_HASH
assert digest((RUN / "pdf/preprint.pdf").read_bytes()) == pdf["rebuilt_pdf_sha256"]
assert pdf["normalized_all_page_text_matches"]
original_text = (RUN / "publication_original_text.txt").read_text()
rebuilt_text = (RUN / "publication_rebuilt_text.txt").read_text()
normalize = lambda value: re.sub(r"\s+", " ", value).strip()
assert normalize(original_text) == normalize(rebuilt_text)
assert original_text.count("\f") == 8 and rebuilt_text.count("\f") == 8

receipt = {
    "schema": "independent-fresh-reproduction-assessment-v1",
    "assessed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASS_FRESH_IDENTITY_COVERAGE_AND_FULL_BALL_THRESHOLDS",
    "zip_sha256": ZIP_HASH,
    "package_identity_sha256": IDENTITY,
    "reproduction_receipt_sha256": digest((RUN / "REPRODUCTION_RECEIPT.json").read_bytes()),
    "assessor_sha256": digest(Path(__file__).read_bytes()),
    "independently_verified_saved_output_hashes": saved_output_hashes,
    "all_exact_frozen_payload_hashes_verified": 74,
    "finite_node_pairs_verified": 102,
    "half_gap_intervals_verified": 84,
    "secondary_full_ball_inequalities_verified": count,
    "scalar_thresholds_rechecked": True,
    "adaptive_matrix_and_residual_thresholds_rechecked": True,
    "pdf_page_text_equality_independently_rechecked": True,
    "pdf_pages": 8,
    "fresh_rebuilt_pdf_sha256": pdf["rebuilt_pdf_sha256"],
    "packaged_pdf_sha256": PDF_HASH,
    "scope": "Saved fresh arithmetic evidence, exact package/file identity and all-page PDF text. Written mathematical proof and original source algorithms assessed separately in FULL_REVIEW.md. PDF images assessed separately. No formal-proof or exhaustive-priority claim."
}
(OUT / "fresh_reproduction_assessment.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({k: v for k, v in receipt.items() if k != "independently_verified_saved_output_hashes"}, indent=2))
