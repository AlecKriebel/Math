"""Read-only integrity checks. Never writes files or reruns mathematical loops."""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    require(path.is_file() and not path.is_symlink(), "Missing or linked file: " + str(path))
    return json.loads(path.read_text())


def inventory(base, entries):
    expected = set()
    for entry in entries:
        relative = Path(entry["path"])
        require(not relative.is_absolute() and ".." not in relative.parts, "Unsafe inventory path")
        name = relative.as_posix()
        require(name not in expected, "Duplicate inventory path: " + name)
        expected.add(name)
        path = base / relative
        require(path.is_file() and not path.is_symlink(), "Missing or linked artifact: " + name)
        require(path.stat().st_size == entry["bytes"], "Byte count mismatch: " + name)
        require(digest(path) == entry["sha256"], "Hash mismatch: " + name)
    return expected


def actual_inventory(base):
    result = set()
    for path in base.rglob("*"):
        require(not path.is_symlink(), "Symlinks are not accepted in the namespace")
        if path.is_file():
            result.add(path.relative_to(base).as_posix())
    return result


ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--mode", choices=("full", "public-only"), required=True)
ap.add_argument("--root", type=Path, help="Full review root or directory containing public artifacts")
args = ap.parse_args()
default_root = Path(__file__).resolve().parent.parent if args.mode == "full" else Path(__file__).resolve().parent
root = args.root.resolve() if args.root else default_root
public = root / "public" if (root / "public").is_dir() else root
pm_path = public / "PUBLIC_MANIFEST.json"
pc_path = public / "PUBLIC_CLOSURE.json"
pm = load(pm_path)
pc = load(pc_path)
require(pc["status"] == "CLOSED_READ_ONLY_NO_FURTHER_WRITES", "Public closure status mismatch")
require(digest(pm_path) == pc["public_manifest_sha256"], "Public manifest binding failed")
public_expected = inventory(public, pm["public_artifacts"])
require(actual_inventory(public) == public_expected | {pm_path.name, pc_path.name}, "Public actual inventory mismatch")
require(digest(public / "WORD_OVERLAP_CHECKS.json") == pm["own_control_expected_stdout_sha256"], "Expected control stdout binding failed")
require(load(public / "WORD_OVERLAP_CHECKS.json")["status"] == "PASS", "Control receipt status mismatch")
limitations = [
    "Public-only mode cannot inspect the source-first exposure gate or raw source excerpts/renders.",
    "Public-only mode cannot inspect submitted author/portable native streams, commands, or pre-execution input pins.",
    "Public-only mode cannot inspect frozen candidate copies or private provenance; it checks public bytes against the public closure.",
    "Neither mode reruns mathematical loops or certifies proof correctness, priority, human peer review, or local Git binding.",
    "Neither mode independently reproduces the unavailable historical five-private-source integrity mode.",
    "The whole official PDF is cached outside this package; full mode checks the preserved source excerpt/render inventory, not that external PDF.",
]
result = {"status": "PASS", "mode": args.mode, "public_artifact_count": len(public_expected),
          "public_manifest_sha256": digest(pm_path), "public_closure_sha256": digest(pc_path),
          "read_only_program": True, "mathematical_loops_rerun": False, "limitations": limitations}
if args.mode == "full":
    require(public == root / "public", "Full mode requires the full review root")
    private_path = root / "PRIVATE_MANIFEST.json"
    seal_path = root / "SEALED_NAMESPACE.json"
    private = load(private_path)
    seal = load(seal_path)
    require(seal["status"] == pc["status"], "Full closure status mismatch")
    require(digest(private_path) == seal["private_manifest_sha256"] == pc["private_manifest_sha256"], "Private manifest binding failed")
    require(digest(pm_path) == seal["public_manifest_sha256"], "Full/public manifest binding failed")
    require(digest(pc_path) == seal["public_closure_sha256"], "Full/public closure binding failed")
    private_expected = inventory(root, private["private_artifacts"])
    whole_expected = private_expected | {private_path.name, seal_path.name}
    whole_expected |= {"public/" + name for name in public_expected | {pm_path.name, pc_path.name}}
    require(actual_inventory(root) == whole_expected, "Full actual inventory mismatch")
    writable = [name for name in whole_expected if (root / name).stat().st_mode & 0o222]
    require(not writable, "Closed full namespace has writable files: " + repr(writable))
    pins = load(root / "private_reproducibility/preexecution_pins.json")
    require(digest(root / "check_word_overlap.py") == pins["own_control_sha256"], "Own pre-execution code pin failed")
    require(digest(public / "check_word_overlap.py") == pins["own_control_sha256"], "Published/executed control code differs")
    require(digest(root / "run_reproducibility.py") == pins["runner_sha256"], "Runner pre-execution code pin failed")
    frozen = root / "private/candidate_snapshot"
    for entry in pins["verified_snapshot_files"]:
        path = frozen / entry["path"]
        require(path.is_file() and digest(path) == entry["sha256"], "Frozen pre-execution input pin failed: " + entry["path"])
    require(pins["frozen_head"] == pm["frozen_head"] and pins["frozen_base"] == pm["frozen_base"], "Frozen commit label mismatch")
    rows = load(root / "private_reproducibility/reproduction_results.json")
    require(len(rows) == 3, "Expected three recorded complete native runs")
    require(datetime.fromisoformat(pins["utc"]) <= min(datetime.fromisoformat(row["started_utc"]) for row in rows), "Code pins were not recorded before native runs")
    for row in rows:
        name = row["name"]
        recorded = load(root / "private_reproducibility" / (name + ".metadata.json"))
        require(recorded == row, "Native metadata/result mismatch: " + name)
        require(datetime.fromisoformat(row["started_utc"]) <= datetime.fromisoformat(row["finished_utc"]), "Native run timestamps reversed: " + name)
        require(row["exit_code"] == 0 and row["stderr_bytes"] == 0, "Native run status failed: " + name)
        for stream in ("stdout", "stderr"):
            path = root / "private_reproducibility" / (name + "." + stream)
            require(path.stat().st_size == row[stream + "_bytes"], "Complete native stream size mismatch: " + name)
            require(digest(path) == row[stream + "_sha256"], "Complete native stream hash mismatch: " + name)
        if name == "submitted_author":
            receipt = frozen / "problems/30001552_antimorphic_periods/TURN_1_CHECKS.json"
        elif name == "submitted_public_portable":
            receipt = frozen / "problems/30001552_antimorphic_periods/review/PORTABLE_CHECKS.json"
        else:
            require(name == "own_direct_word", "Unknown native run")
            receipt = public / "WORD_OVERLAP_CHECKS.json"
        require((root / "private_reproducibility" / (name + ".stdout")).read_bytes() == receipt.read_bytes(), "Whole native stdout/receipt mismatch: " + name)
    runner_rows = [json.loads(line) for line in (root / "runner_native_stdout.txt").read_text().splitlines()]
    require(runner_rows == rows, "Whole runner stdout mismatch")
    require((root / "runner_native_stderr.txt").read_bytes() == b"", "Runner stderr is nonempty")
    gate = load(root / "source_first/gate_20261004T003506Z.json")
    require(digest(root / "source_first" / gate["baseline_file"]) == gate["baseline_sha256"], "Source-first baseline binding failed")
    require(digest(root / "source_first/official_pages_25_28.txt") == gate["source_extracted_text_sha256"], "Source extraction binding failed")
    result.update({"private_artifact_count": len(private_expected), "native_stream_count": 8,
                   "preexecution_snapshot_input_count": len(pins["verified_snapshot_files"]),
                   "own_preexecution_code_pin": pins["own_control_sha256"],
                   "runner_preexecution_code_pin": pins["runner_sha256"],
                   "closure_sha256": digest(seal_path), "private_manifest_sha256": digest(private_path)})
print(json.dumps(result, indent=2))
