"""Build only this problem's portable, authored verification package."""
from pathlib import Path
import hashlib, json, shutil, zipfile

HERE = Path(__file__).resolve().parent
D = HERE.parent / "initial_review_20261013"
V = HERE / "verification"
V.mkdir(exist_ok=True)

def copy(source, target):
    out = V / target
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out)

copy(HERE / "outer_pedal_centroid.tex", "paper/outer_pedal_centroid.tex")
copy(D / "candidate_repair_01/PROOF.md", "proof/PROOF.md")
p = V / "proof/PROOF.md"
text = p.read_text()
text = text.replace("Independent review is pending.",
                    "Mathematical and bounded priority audits passed; manuscript review status is recorded separately.")
text = text.replace("## 7. Source credit and remaining review",
                    "## 7. Source credit and audit disposition")
text = text.replace("An independent adversarial audit must decide correctness, full source coverage and the appropriate credited disposition before any PR.",
                    "Independent algebraic and geometric audits accepted the exact theorem and the four-period converse repair. Two bounded priority audits found no earlier covering proof, without certifying historical firstness.")
p.write_text(text)
for name in ["ROOT_MATHEMATICAL_ACCEPTANCE.md", "ROOT_PRIORITY_ACCEPTANCE.md"]:
    copy(D / name, "audits/" + name)
for folder, names in {
    "algebraic_adversary_01": [
        "INDEPENDENT_DERIVATION.md", "AUDIT_REPORT.md",
        "independent_verifier.py", "INDEPENDENT_EVIDENCE.json",
        "independent_winding_certificate.py", "WINDING_CERTIFICATE.json",
        "DOUBLE_PRECISION_FAILURE_HISTORY.md",
        "double_precision_failure_reproducer.py"],
    "geometric_domain_adversary_01": [
        "GEOMETRIC_DOMAIN_REPORT.md", "ALL_REAL_CARTESIAN_PROOF.md",
        "real_cartesian_certificate.py", "CARTESIAN_CERTIFICATE.json",
        "geometric_audit.py", "NUMERICAL_RESULTS.json", "exact_star_audit.py"],
    "priority_billiards_adversary_01": [
        "PRIORITY_AUDIT_REPORT.md", "CIRCLE_FOCUS_INTERMEDIATE_SCOPE.md",
        "EXACT_COMPARISON_CONTROLS.json", "PRIMARY_SOURCE_MANIFEST.json"],
    "priority_recent_adversary_01": [
        "PRIORITY_REPORT.md", "AUDIT_DISPOSITION.json",
        "ZENODO_ORIGINAL_CONTENT_COMPARISON.json"],
}.items():
    for name in names:
        copy(D / folder / name, folder + "/" + name)
original = D / "submitted/unsolved_math_prioritization/attempts/5100017"
copy(original / "verify.py", "author/verify.py")
for name in ["independent_checks.py", "independent_numeric.py"]:
    copy(original / "independent_review" / name, "original_independent/" + name)
for name in ["REPRODUCTION_SUMMARY.json", "RUNTIME_VERSIONS.json",
             "AUTHOR_FLOATING_DIAGNOSTIC_REPRODUCIBILITY_DIFFERENCES.json"]:
    copy(D / "root_reproductions" / name, "reproduction/" + name)
for name in ["README.md", "requirements.txt", "LICENSE", "run_verification.py", "metadata.json"]:
    copy(HERE / name, name)
# Later fresh reviews become additional evidence without changing the proof.
for review in sorted(HERE.glob("review_*/REPORT.md")):
    copy(review, "manuscript_reviews/" + review.parent.name + ".md")
rows = []
for path in sorted(V.rglob("*")):
    if path.is_file() and path.name != "MANIFEST.json" and "__pycache__" not in path.parts:
        data = path.read_bytes()
        rows.append({"path": path.relative_to(V).as_posix(), "bytes": len(data),
                     "sha256": hashlib.sha256(data).hexdigest()})
(V / "MANIFEST.json").write_text(json.dumps({"version": "1.0", "files": rows}, indent=2) + "\n")
target = HERE / "outer-pedal-centroid-verification.zip"
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(V.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            archive.write(path, "outer-pedal-centroid-verification/" + path.relative_to(V).as_posix())
print(json.dumps({"files": len(rows) + 1, "zip_bytes": target.stat().st_size,
                  "zip_sha256": hashlib.sha256(target.read_bytes()).hexdigest()}, indent=2))
