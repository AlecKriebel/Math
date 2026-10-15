"""Validate the exact confirmed-license package; no publication or Git writes."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "publication/upload-kit/source-and-verification.zip"
OLD = ROOT / "reviews/versions/final_candidate_v2/publication/upload-kit/source-and-verification.zip"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(args, cwd):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=120)
    if p.returncode:
        raise RuntimeError(p.stdout + p.stderr)
    return p.stdout


def main():
    with zipfile.ZipFile(ZIP) as z, zipfile.ZipFile(OLD) as old:
        assert z.testzip() is None
        names = z.namelist()
        assert len(names) == len(set(names)) == 41
        assert set(names) == set(old.namelist())
        for name in names:
            path = PurePosixPath(name)
            assert not path.is_absolute() and ".." not in path.parts
            assert (z.getinfo(name).external_attr >> 16) & 0o170000 == 0o100000
        manifest = json.loads(z.read("SOURCE_MANIFEST.json"))
        assert manifest["license_id"] == "cc-by-4.0"
        assert manifest["human_license_decision_confirmed"] is True
        assert len(manifest["files"]) == 40
        for entry in manifest["files"]:
            data = z.read(entry["path"])
            assert len(data) == entry["bytes"] and digest(data) == entry["sha256"]
        versions = json.loads(z.read("SOURCE_VERSIONS.json"))
        assert versions["own_license"] == {"id": "cc-by-4.0", "human_decision_confirmed": True}
        assert "confirmed by the human user" in z.read("LICENSES.md").decode()
        assert z.read("zenodo-deposit.json") == (ROOT / "zenodo-deposit.json").read_bytes()
        assert z.read("manuscript/main.tex") == (ROOT / "manuscript/main.tex").read_bytes()
        changed = sorted(n for n in names if z.read(n) != old.read(n))
        assert changed == ["LICENSES.md", "SOURCE_MANIFEST.json", "SOURCE_VERSIONS.json", "publication/README.md"], changed
        scratch = Path(tempfile.mkdtemp(prefix="licensed-final-reproduction-", dir=ROOT / "tmp"))
        z.extractall(scratch)

    (scratch / "output/pdf").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "output/pdf/paper.pdf", scratch / "output/pdf/paper.pdf")

    # All proof, code, upstream, and publication metadata bytes are unchanged.
    # Rebuild the exact selected-license archive from the clean extracted tree.
    run(["python3", "publication/build_upload_kit.py", "--root", str(scratch),
         "--license", "cc-by-4.0", "--license-confirmed"], scratch)
    assert (scratch / "publication/upload-kit/source-and-verification.zip").read_bytes() == ZIP.read_bytes()
    expected_results = {rel: (scratch / rel).read_bytes() for rel in
                        ("research/cohomology_adversary_checks.json", "research/draft_whole_review_1_checks.json")}
    scripts = ("research/cohomology_adversary_checks.py", "research/draft_whole_review_1_checks.py",
               "research/revised_checkpoint_review_symbolic_central_homotopy/original_symbolic_check.py")
    replay = []
    for script in scripts:
        output = run(["python3", script], scratch)
        replay.append({"script": script, "exit_code": 0, "stdout": output})
    for rel, expected in expected_results.items():
        assert (scratch / rel).read_bytes() == expected, rel

    run(["python3", "reproducibility/build_paper.py", "--root", str(scratch), "--render",
         "--receipt", str(scratch / "receipts/paper_build.json")], scratch)
    rebuilt = scratch / "output/pdf/paper.pdf"
    text = run(["pdftotext", "-layout", str(rebuilt), "-"], scratch)
    original_text = run(["pdftotext", "-layout", str(ROOT / "output/pdf/paper.pdf"), "-"], ROOT)
    assert text == original_text
    build = json.loads((scratch / "receipts/paper_build.json").read_text())
    reference = ROOT / "tmp/clean-publication-build-ivj44om4"
    raster = []
    for i, rel in enumerate(build["rendered_pages"], 1):
        fresh = (scratch / rel).read_bytes()
        assert fresh == (reference / f"page-{i}.png").read_bytes()
        raster.append({"page": i, "sha256": digest(fresh), "exact_png_equality": True})
    assert len(raster) == 7
    receipt = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Confirmed-license exact-package construction, clean build and finite replay; not a proof or publication clearance",
        "archive_sha256": digest(ZIP.read_bytes()), "archive_bytes": ZIP.stat().st_size,
        "archive_member_count": 41, "all40manifest_entries_verified": True,
        "changed_members_from_reviewed_v2": changed,
        "proof_code_upstream_and_metadata_members_unchanged": True,
        "license_id": "cc-by-4.0", "human_license_decision_confirmed": True,
        "deterministic_archive_rebuild_exact": True,
        "clean_extraction": str(scratch.relative_to(ROOT)),
        "clean_build": build, "layout_text_exact_equality": True,
        "rendered_pages": raster, "finite_replays": replay,
        "original_pdf_sha256": digest((ROOT / "output/pdf/paper.pdf").read_bytes()),
        "formal_build_reproduced": False, "publication_or_tracker_action_performed": False,
    }
    (ROOT / "receipts/confirmed_license_package_revalidation_20261007.json").write_text(
        json.dumps(receipt, indent=2) + "\n")
    tests = {key: receipt[key] for key in ("utc", "scope", "archive_sha256", "archive_member_count",
             "license_id", "human_license_decision_confirmed", "deterministic_archive_rebuild_exact",
             "layout_text_exact_equality", "proof_code_upstream_and_metadata_members_unchanged",
             "changed_members_from_reviewed_v2", "formal_build_reproduced", "publication_or_tracker_action_performed")}
    (ROOT / "publication/upload-kit/preparation_tests.json").write_text(json.dumps(tests, indent=2) + "\n")
    print(json.dumps(tests, indent=2))


if __name__ == "__main__":
    main()
