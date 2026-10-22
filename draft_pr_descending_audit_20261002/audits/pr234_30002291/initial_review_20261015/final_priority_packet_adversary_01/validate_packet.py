"""Read-only parent packet validation; all replay writes stay in this folder."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess

OWN = Path(__file__).resolve().parent
BASE = OWN.parent
PACKET = BASE / "corrected_packet"
SUBMITTED = BASE / "submitted/unsolved_math_prioritization/attempts/30002291"
PYTHON = Path("/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_entries(root, data, field="files"):
    entries = data[field]
    if isinstance(entries, dict):
        entries = [{"path": p, "sha256": h} for p, h in entries.items()]
    for row in entries:
        p = root / row["path"]
        assert sha(p) == row["sha256"], str(p)
        if "bytes" in row:
            assert p.stat().st_size == row["bytes"], str(p)
    return len(entries)


def main():
    manifest_path = BASE / "PROPOSED_CURRENT_PACKET_MANIFEST.json"
    assert sha(manifest_path) == "b67b9f3d2b7709bcf324ef0ea65d2a370cb56bbabc9c7550fd582d49585be006"
    manifest = json.loads(manifest_path.read_text())
    assert verify_entries(PACKET, manifest) == 31
    actual = {str(p.relative_to(PACKET)) for p in PACKET.rglob("*") if p.is_file()}
    assert actual == {r["path"] for r in manifest["files"]}
    archive = PACKET / "original_submission"
    originals = sorted(p for p in SUBMITTED.rglob("*") if p.is_file())
    assert len(originals) == 17
    assert {str(p.relative_to(SUBMITTED)) for p in originals} == {
        str(p.relative_to(archive)) for p in archive.rglob("*") if p.is_file()
    }
    for p in originals:
        assert p.read_bytes() == (archive / p.relative_to(SUBMITTED)).read_bytes()
    old = (SUBMITTED / "PROOF.md").read_bytes()
    new = (PACKET / "PROOF.md").read_bytes()
    marker_start = b"## 2. Driver and kernel assumptions"
    marker_end = b"## 8. Disposition and limitations"
    old_core = old[old.index(marker_start):old.index(marker_end)]
    new_core = new[new.index(marker_start):new.index(marker_end)]
    assert old_core == new_core
    complete_sections_sha = hashlib.sha256(new_core).hexdigest()
    # The proposer defines its core digest after the Section 2 heading.
    # Verify the heading too, then reproduce that documented extraction.
    core_sha = hashlib.sha256(new_core[len(marker_start):]).hexdigest()
    assert core_sha == manifest["core_sha256"] == "c801125f4f2c68b10fc129a112d58e59c4ea413648f2707098c7b9c5ea1a86a8"
    current_frozen = json.loads((PACKET / "FROZEN_MANIFEST.json").read_text())
    current_publication = json.loads((PACKET / "PUBLICATION_MANIFEST.json").read_text())
    assert verify_entries(PACKET, current_frozen) == 29
    assert verify_entries(PACKET, current_publication) == 30
    assert verify_entries(archive, json.loads((archive / "FROZEN_MANIFEST.json").read_text())) == 9
    assert verify_entries(archive / "independent_review", json.loads((archive / "independent_review/REVIEW_MANIFEST.json").read_text())) == 6

    native_path = BASE / "PROPOSED_NATIVE_CHANGES.json"
    native = json.loads(native_path.read_text())
    assert native["packet_manifest_sha256"] == sha(manifest_path)
    assert native["original_head"] == manifest["original_head"] == "34e4dfaeda693b5349b4ef5eec458962781b4bb3"
    old_fields = native["old_row"].split("|")
    new_fields = native["new_row"].split("|")
    assert len(old_fields) == len(new_fields)
    changed_columns = [i for i, (a, b) in enumerate(zip(old_fields, new_fields)) if a != b]
    assert changed_columns == [8, 11]
    assert old_fields[8].strip() == "claimed_solved"
    assert new_fields[8].strip() == "already_solved"
    assert new_fields[9].strip() == "1/5"
    assert "novelty unresolved" in new_fields[11]
    assert "no full-class anticipation established" in new_fields[11]
    assert native["native_application_cleared"] is False
    assert native["merge_close_comment_paper_deposit_tracker"] is False

    lane_manifests = [
        ("priority_general_volterra_01/AUTHORED_MANIFEST.json", "files"),
        ("priority_classical_coverage_01/AUTHORED_MANIFEST.json", "files"),
        ("priority_boundary_class_01/SAFE_ARTIFACT_MANIFEST.json", "safe_authored_artifacts"),
        ("priority_history_citations_01/SAFE_AUTHORED_MANIFEST.json", "files"),
        ("priority_novelty_scope_challenge_01/AUTHORED_MANIFEST.json", "safe_authored_artifacts"),
    ]
    lane_receipts = []
    for rel, field in lane_manifests:
        path = BASE / rel
        count = verify_entries(path.parent, json.loads(path.read_text()), field)
        lane_receipts.append({"manifest": rel, "sha256": sha(path), "verified_safe_entries": count})
    assert sum(r["verified_safe_entries"] for r in lane_receipts) == 57

    replay_root = OWN / "replays"
    replay_root.mkdir(exist_ok=True)
    cases = [
        ("archived_author", archive / "checks/verify_exact.py", archive / "checks/EXACT_CHECKS.json", None),
        ("archived_independent", archive / "independent_review/independent_checks.py", archive / "independent_review/INDEPENDENT_CHECKS.json", None),
        ("classical_scope", BASE / "priority_classical_coverage_01/scope_checks.py", BASE / "priority_classical_coverage_01/SCOPE_CHECK_RECEIPT.json", "utc"),
        ("boundary_scope", BASE / "priority_boundary_class_01/check_scope_separators.py", BASE / "priority_boundary_class_01/SCOPE_CHECKS.json", "created_utc"),
        ("general_scope", BASE / "priority_general_volterra_01/scope_checks.py", BASE / "priority_general_volterra_01/SCOPE_CHECKS.json", None),
    ]
    runs = []
    for label, source, expected, time_key in cases:
        out = replay_root / label
        out.mkdir(exist_ok=True)
        copied = out / source.name
        shutil.copyfile(source, copied)
        assert copied.read_bytes() == source.read_bytes()
        proc = subprocess.run([str(PYTHON), "-I", "-B", str(copied)], cwd=out, capture_output=True, timeout=45)
        (out / "stdout.json").write_bytes(proc.stdout)
        (out / "stderr.txt").write_bytes(proc.stderr)
        assert proc.returncode == 0 and proc.stderr == b"", (label, proc.stderr)
        old_data = json.loads(expected.read_text())
        if label == "boundary_scope":
            new_data = json.loads((out / "SCOPE_CHECKS.json").read_text())
        else:
            new_data = json.loads(proc.stdout)
        if time_key:
            old_data.pop(time_key)
            new_data.pop(time_key)
        assert new_data == old_data, label
        runs.append({"case": label, "source_sha256": sha(source), "returncode": proc.returncode,
                     "receipt_equal_ignoring_timestamp_only": True,
                     "stdout_byte_identical": proc.stdout == expected.read_bytes(),
                     "exact_assertions": new_data.get("exact_assertions"),
                     "limitation": "Finite identity and scope controls only; not a stochastic proof or novelty certificate"})
    assert verify_entries(PACKET, manifest) == 31
    runtime = subprocess.run([str(PYTHON), "-I", "-B", "-c", "import sys,sympy; print(sys.version); print(sympy.__version__)"], capture_output=True, check=True)
    receipt = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "PASS_PACKET_STRUCTURE_AND_REPLAY",
        "proposed_packet_manifest_sha256": sha(manifest_path),
        "proposed_native_changes_sha256": sha(native_path),
        "verified_current_files": 31,
        "archived_originals_byte_identical": 17,
        "core_sections_2_through_7_byte_identical": True,
        "core_sha256": core_sha,
        "complete_sections_including_section_2_heading_sha256": complete_sections_sha,
        "current_frozen_pins": 29,
        "current_publication_pins": 30,
        "historical_author_pins": 9,
        "historical_review_pins": 6,
        "catalog_changed_columns": changed_columns,
        "author_turn": "1/5",
        "lane_manifests": lane_receipts,
        "actual_replays": runs,
        "runtime": str(PYTHON),
        "runtime_version": runtime.stdout.decode().strip(),
        "parent_files_unchanged_by_replay": True,
        "git_index_ref_provider_mutation": False,
        "note": "Semantic disposition is reviewed separately; this script does not certify global novelty or historic firstness."
    }
    (OWN / "PACKET_CHECK_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
