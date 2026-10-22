#!/usr/bin/env python3
"""Read-only authentication of the 26 immutable originals; optional own-folder receipt.

No assessment bodies are printed. Run without arguments for a read-only check.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import stat
import subprocess

HEAD = "b356dec5cb01e5f536b9cfeece56ad08844c03cb"
RECORD_SHA256 = "610351fbb778f78ce53cda03ea715f38615abb5710690987c214f8093bda13ae"


def authenticate(stage: str) -> dict:
    work = Path(__file__).resolve().parent
    audit = work.parents[1]
    project = audit.parents[1]
    repo = Path(subprocess.check_output(
        ["git", "-C", str(project), "rev-parse", "--show-toplevel"], text=True
    ).strip())
    record_path = audit / "ORIGINAL_FILE_RECORDS.json"
    record_bytes = record_path.read_bytes()
    record_sha = hashlib.sha256(record_bytes).hexdigest()
    if record_sha != RECORD_SHA256:
        raise RuntimeError("Whole records file digest mismatch")
    record = json.loads(record_bytes)
    if record["head"] != HEAD or len(record["files"]) != 26:
        raise RuntimeError("Record head/file-count mismatch")
    files = {}
    problems = []
    total = 0
    for relative, expected in sorted(record["files"].items()):
        rel = Path(relative)
        if rel.is_absolute() or ".." in rel.parts:
            raise RuntimeError("Unsafe original path")
        path = audit / "original" / rel
        data = path.read_bytes()
        total += len(data)
        tree = subprocess.check_output(
            ["git", "-C", str(repo), "ls-tree", HEAD, "--", relative], text=True
        ).strip()
        mode, kind, rest = tree.split(" ", 2)
        blob, tree_path = rest.split("\t", 1)
        git_data = subprocess.check_output(
            ["git", "-C", str(repo), "show", f"{HEAD}:{relative}"]
        )
        actual = {
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "disk_mode": format(stat.S_IMODE(path.lstat().st_mode), "04o"),
            "git_mode": mode,
            "git_blob": blob,
            "git_bytes": len(git_data),
            "git_sha256": hashlib.sha256(git_data).hexdigest(),
            "disk_git_identical": data == git_data,
        }
        actual["all_match"] = (
            kind == "blob" and tree_path == relative
            and all(actual[key] == expected[key] for key in
                    ("bytes", "sha256", "disk_mode", "git_mode", "git_blob"))
            and actual["disk_git_identical"]
        )
        files[relative] = actual
        if not actual["all_match"]:
            problems.append(relative)
    actual_paths = {
        str(p.relative_to(audit / "original"))
        for p in (audit / "original").rglob("*") if p.is_file()
    }
    extras = sorted(actual_paths - set(record["files"]))
    missing = sorted(set(record["files"]) - actual_paths)
    result = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "head": HEAD,
        "records_path": str(record_path),
        "records_bytes": len(record_bytes),
        "records_sha256": record_sha,
        "external_records_sha256": RECORD_SHA256,
        "file_count": len(files),
        "total_disk_bytes": total,
        "exact_original_file_set": not extras and not missing,
        "extra_files": extras,
        "missing_files": missing,
        "all_match": not problems and not extras and not missing and total == 147731,
        "problems": problems,
        "files": files,
    }
    if not result["all_match"]:
        raise RuntimeError("Original authentication failed")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", default="read_only_check")
    parser.add_argument("--receipt", help="Optional JSON basename within this family folder")
    args = parser.parse_args()
    result = authenticate(args.stage)
    if args.receipt:
        name = Path(args.receipt)
        if name.name != args.receipt or name.suffix != ".json":
            raise SystemExit("Receipt must be one JSON basename")
        (Path(__file__).resolve().parent / name).write_text(
            json.dumps(result, indent=2) + "\n"
        )
    summary_keys = ("utc", "stage", "head", "records_sha256", "file_count",
                    "total_disk_bytes", "exact_original_file_set", "all_match")
    print(json.dumps({key: result[key] for key in summary_keys}, indent=2))


if __name__ == "__main__":
    main()
