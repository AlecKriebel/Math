import datetime
import hashlib
import json
import os
from pathlib import Path

A = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
EXPECTED_CANDIDATE = "0a15d03ab92cbd13f17042a4708f75c3d592f4884810c7ffadc6a5f34f1cb6c4"
HEAD = "5cc1602c05d79502defb07cec7027963149494d2"
MANIFESTS = [
    ("classical_priority_mechanism_20261004/MANIFEST.json", "cb51fa96a929117ce050c156f554cafa715e3b77e05a9442c10d669000addc27"),
    ("classical_priority_mechanism_20261004/adversarial_review/SELF_MANIFEST.json", "55198a6d113284e27f308de8b12c3e4a52c17ba2042aa9c91e935de89e105f7d"),
    ("current_priority_sources_20261004/FINAL_MANIFEST.json", "bc85e4d7d734b4cdcdf7b85a34134d24e90fc99c63799d1b1ca8738f7035990a"),
]

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def verify(path, expected):
    actual = pin(path)
    if actual["bytes"] != expected["bytes"] or actual["sha256"] != expected["sha256"]:
        raise ValueError("Artifact mismatch: " + str(path))
    return actual

candidate = A / "original_source_authentication_20261004/original/unsolved_math_prioritization/attempts/2305051/CANDIDATE.md"
sources = [pin(Path(__file__).resolve()), pin(candidate)]
for name, digest in MANIFESTS:
    item = pin(A / name)
    if item["sha256"] != digest:
        raise ValueError("Manifest pin mismatch: " + name)
    sources.append(item)
if sources[1]["sha256"] != EXPECTED_CANDIDATE:
    raise ValueError("Candidate changed")
pre = {"UTC": utc(), "pid": os.getpid(), "immutable_head": HEAD, "sources_prelaunch": sources}
(OUT / "SOURCE_PRELAUNCH.json").write_text(json.dumps(pre, indent=2) + "\n")

verified_manifests = []
for name, digest in MANIFESTS:
    path = A / name
    manifest = json.loads(path.read_text())
    domain = manifest["files"]
    entries = domain if isinstance(domain, list) else [
        dict(value, path=key) for key, value in domain.items()
    ]
    seen = set()
    for entry in entries:
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Unsafe artifact path")
        if str(relative) in seen:
            raise ValueError("Duplicate artifact path")
        seen.add(str(relative))
        full = path.parent / relative
        if full.is_symlink() or not full.is_file():
            raise ValueError("Nonregular artifact")
        verify(full, entry)
    verified_manifests.append({"path": str(path), "sha256": digest, "verified_members": len(entries)})

classical = A / "classical_priority_mechanism_20261004"
classical_rows = []
for path in sorted((classical / "execution").glob("*/record.json")):
    rec = json.loads(path.read_text())
    row = {"path": str(path), "subprocess_pid": rec.get("subprocess_pid"), "exit_code": rec.get("exit_code")}
    if "stdout_sha256" in rec and "stderr_sha256" in rec:
        for label in ["stdout", "stderr"]:
            verify(path.parent / label, {"bytes": rec[label + "_bytes"], "sha256": rec[label + "_sha256"]})
        row["streams_verified"] = True
    else:
        row["streams_verified"] = False
        row["limitation"] = "This record has no flat stream hash pair; no stream verification inferred."
    classical_rows.append(row)

current = A / "current_priority_sources_20261004"
current_rows = []
for line in (current / "process_receipts.jsonl").read_text().splitlines():
    rec = json.loads(line)
    if not isinstance(rec.get("pid"), int) or not isinstance(rec.get("argv"), list):
        raise ValueError("Missing actual current-family process identity")
    for label in ["stdout", "stderr"]:
        entry = rec[label]
        verify(Path(entry["path"]), entry)
    current_rows.append({key: rec[key] for key in ["label", "pid", "exit_code", "started_utc", "finished_utc"]})

private = json.loads((current / "PRIVATE_CACHE_INVENTORY.json").read_text())
private_files = private["all_private_files"]
for entry in private_files:
    verify(Path(entry["path"]), entry)
for name, digest in MANIFESTS:
    if pin(A / name)["sha256"] != digest:
        raise ValueError("Manifest changed during readback")
if pin(candidate)["sha256"] != EXPECTED_CANDIDATE:
    raise ValueError("Candidate changed during readback")

result = {
    "schema": "PR65-root-new-priority-custody-readback/v1",
    "UTC": utc(),
    "pid": os.getpid(),
    "immutable_head": HEAD,
    "candidate_unchanged": True,
    "manifests": verified_manifests,
    "classical_execution_records": classical_rows,
    "current_family_processes": current_rows,
    "current_family_streams_verified": 2 * len(current_rows),
    "private_cache_files_verified": len(private_files),
    "scope": "Byte custody of completed new priority artifacts and actual records; not a proof of literature completeness, novelty, source reading, or a fresh mathematical test run.",
    "priority_clearance": False,
    "PR65_publication_or_merge": False,
    "result": "PASS",
}
(OUT / "READBACK.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({key: result[key] for key in ["UTC", "pid", "candidate_unchanged", "manifests", "current_family_streams_verified", "private_cache_files_verified", "result"]}))
