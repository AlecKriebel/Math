#!/usr/bin/env python3
"""Build this problem's publication package from explicit original files."""
if not __debug__:
    raise SystemExit("Run without Python optimization; checks use assertions.")
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publication"
KIT = PUB / "kit"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sources = {
        "paper.pdf": ROOT / "preprint/main.pdf",
        "main.tex": ROOT / "preprint/main.tex",
        "README.md": PUB / "README.md",
        "LICENSE.txt": PUB / "LICENSE.txt",
        "source_manifest.json": ROOT / "source_manifest.json",
        "algebra_sources.json": ROOT / "nil_embeddings/sources/SOURCE_MANIFEST.json",
        "absolute_extension_sources.json": ROOT / "nil_embeddings/sources/ABSOLUTE_EXTENSION_SOURCE_MANIFEST.json",
        "absolute_review_sources.json": ROOT / "absolute_fresh_adversary/SOURCE_MANIFEST.json",
        "verification/run_all.py": PUB / "run_all.py",
        "verification/lib/tree_sections.py": ROOT / "tree_targets/adversary/check_construction.py",
        "verification/lib/finite_levels.py": ROOT / "tree_targets/verify_finite_levels.py",
        "verification/lib/noncommutative.py": ROOT / "nil_embeddings/adversarial_review/noncommutative_check/check.py",
        "verification/lib/wreath_augmentation.py": ROOT / "nil_embeddings/adversarial_review/check_wreath_augmentation.py",
        "verification/lib/fresh_independent.py": ROOT / "combined_fresh_review/independent_checks.py",
        "verification/review2_stress.py": ROOT / "verification/review2_stress.py",
        "verification/review2_stress.json": ROOT / "verification/review2_stress.json",
        "audits/target_review.md": ROOT / "tree_targets/adversary/adversarial_audit.md",
        "audits/algebra_review.md": ROOT / "nil_embeddings/adversarial_review/AUDIT.md",
        "audits/noncommutative_review.md": ROOT / "nil_embeddings/adversarial_review/noncommutative_check/REPORT.md",
        "audits/combined_review.md": ROOT / "combined_fresh_review/REVIEW.md",
        "audits/absolute_nil_review.md": ROOT / "absolute_fresh_adversary/AUDIT.md",
        "audits/fresh_scope_review.md": ROOT / "fresh_scope_adversary/SCOPE_AUDIT.md",
        "audits/exact_source_contract.md": ROOT / "PROBLEM.md",
        "audits/extended_priority.md": ROOT / "priority_deep/originality_verdict.md",
        "audits/priority_scope_addendum.md": ROOT / "priority_deep/priority_scope_addendum_20261024.md",
    }
    for report in sorted((ROOT / "reviews").glob("final_package*.md")):
        sources["audits/" + report.name] = report
    if KIT.exists():
        shutil.rmtree(KIT)  # Only this script's disposable generated directory.
    KIT.mkdir()
    for name, source in sources.items():
        destination = KIT / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    runner = runpy.run_path(str(KIT / "verification/run_all.py"))
    results = runner["evaluate"]()
    # Compare to independent original checkpoint outputs, not just a regenerated baseline.
    assert results["construction_family"] == json.loads((ROOT / "tree_targets/finite_level_results.json").read_text())
    fresh = json.loads((ROOT / "combined_fresh_review/independent_results.json").read_text())
    assert results["fresh_tree"] == fresh["tree"]
    assert results["fresh_algebra"] == fresh["algebra"]
    original_wreath = json.loads((ROOT / "nil_embeddings/adversarial_review/wreath_augmentation_results.json").read_text())
    assert results["wreath_augmentation"] == original_wreath["UT3_examples"]
    baseline = PUB / "expected_results.json"
    if baseline.exists():
        assert results == json.loads(baseline.read_text()), "Publication baseline changed"
    else:
        baseline.write_text(json.dumps(results, indent=2) + "\n")
    shutil.copyfile(baseline, KIT / "verification/expected_results.json")
    # Running canonical main checks the baseline and creates its latest result.
    runner["main"]()
    manifest = {"version": "1.0.0", "files": [
        {"path": str(p.relative_to(KIT)), "bytes": p.stat().st_size, "sha256": sha(p)}
        for p in sorted(KIT.rglob("*")) if p.is_file()
    ], "scope": "All package files except this manifest; no third-party paper bodies."}
    (KIT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    archive = PUB / "source-and-verification.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(KIT.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo("kourovka-21-131/" + str(path.relative_to(KIT)),
                                       date_time=(2026, 10, 24, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info, path.read_bytes())
    shutil.copyfile(KIT / "paper.pdf", PUB / "paper.pdf")
    receipt = {"utc": datetime.now(timezone.utc).isoformat(), "paper_sha256": sha(PUB / "paper.pdf"),
               "tex_sha256": sha(KIT / "main.tex"), "archive_sha256": sha(archive),
               "archive_bytes": archive.stat().st_size,
               "package_files_including_manifest": len(manifest["files"]) + 1}
    (PUB / "package_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
