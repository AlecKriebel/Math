"""Seal this completed audit namespace only; no external or scientific action."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path(__file__).resolve().parent
assert ROOT.name == "thompson-cstar-corrected-fact-sol-20261117"
assert (ROOT / "reader.exit.txt").read_text() == "0\n"
assert json.loads((ROOT / "CUSTODY_AFTER.json").read_text())["before_after_exact"]
final = json.loads((ROOT / "FINAL.json").read_text())
assert final["status"] == "PASS_CORRECTED_PRIVATE_COPY" and final["remaining_issue_count"] == 0
assert final["publication_or_future_action_authority"] is False
TERMINALS = {"FINAL_MANIFEST.json", "FINAL_SEAL.json"}
assert all(not (ROOT / name).exists() for name in TERMINALS)
handles = {name: (ROOT / name).open("xb") for name in sorted(TERMINALS)}
freeze_ns = time.time_ns()
freeze_utc = datetime.datetime.fromtimestamp(freeze_ns / 1_000_000_000, datetime.timezone.utc).isoformat()
objects = [ROOT] + sorted(ROOT.rglob("*"), key=lambda p: p.relative_to(ROOT).as_posix())
for path in objects:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), str(path)
    os.chmod(path, 0o555 if stat.S_ISDIR(mode) else 0o444)
    os.utime(path, ns=(freeze_ns, freeze_ns), follow_symlinks=False)
entries = []
for path in objects:
    rel = "." if path == ROOT else path.relative_to(ROOT).as_posix()
    info = path.lstat()
    entry = {"path": rel, "kind": "directory" if stat.S_ISDIR(info.st_mode) else "file",
             "mode_octal": format(stat.S_IMODE(info.st_mode), "04o"), "mtime_ns": info.st_mtime_ns,
             "hidden_component": any(s.startswith(".") for s in Path(rel).parts if s != ".")}
    if entry["kind"] == "directory":
        entry["empty"] = not any(path.iterdir())
    else:
        data = path.read_bytes()
        entry.update(bytes=len(data), empty=not data)
        if rel in TERMINALS:
            entry["sha256"] = None
            entry["content_hash_exclusion"] = "Already-created terminal pair only; exact object, mode, timestamp, bytes and topology retained"
        else:
            entry["sha256"] = hashlib.sha256(data).hexdigest()
    entries.append(entry)
file_count = sum(e["kind"] == "file" for e in entries)
child_dirs = sum(e["kind"] == "directory" and e["path"] != "." for e in entries)
assert (file_count, child_dirs) == (19, 0)
digest = lambda name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
manifest = {"schema": "finite-whole-owned-corrected-fact-namespace-v1", "scope": str(ROOT),
            "freeze_UTC": freeze_utc, "file_count": file_count, "child_directory_count": child_dirs,
            "root_including_directory_count": child_dirs + 1,
            "terminal_content_hash_exclusions_exact": sorted(TERMINALS), "entries": entries}
seal = {"schema": "finite-corrected-private-copy-fact-seal-v1", "scope": str(ROOT),
        "freeze_UTC": freeze_utc, "status": "PASS_CORRECTED_PRIVATE_COPY_FROZEN_ROOT_ADOPTION_PENDING",
        "completion_percent": 100, "remaining_issue_count": 0, "original_P2_resolved": True,
        "scientific_manuscript_PASS_unchanged": True, "file_count": file_count,
        "child_directory_count": child_dirs, "protected_bounded_inputs_before_after_exact": True,
        "data_reader_attempts": 1, "data_reader_exit": 0, "repair_or_retry_count": 0,
        "scientific_source_producer_helper_execution": 0, "network_Git_W_stage_Sheet_operations": 0,
        "FINAL_sha256": digest("FINAL.json"), "REPORT_sha256": digest("REPORT.md"),
        "manifest_sha256": "0" * 64, "follow_up": None,
        "publication_or_future_action_authority": False, "stop_for_root_adoption": True}
encode = lambda obj: (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()
for _ in range(20):
    manifest_bytes = encode(manifest)
    seal["manifest_sha256"] = hashlib.sha256(manifest_bytes).hexdigest()
    seal_bytes = encode(seal)
    sizes = {"FINAL_MANIFEST.json": len(manifest_bytes), "FINAL_SEAL.json": len(seal_bytes)}
    changed = False
    for entry in entries:
        if entry["path"] in TERMINALS:
            size = sizes[entry["path"]]
            if entry["bytes"] != size or entry["empty"]:
                entry["bytes"], entry["empty"] = size, False
                changed = True
    if not changed:
        break
else:
    raise AssertionError("Terminal byte-count fixed point failed")
for name, data in (("FINAL_MANIFEST.json", manifest_bytes), ("FINAL_SEAL.json", seal_bytes)):
    handles[name].write(data)
    handles[name].flush()
    os.fsync(handles[name].fileno())
    handles[name].close()
    os.utime(ROOT / name, ns=(freeze_ns, freeze_ns), follow_symlinks=False)
actual = [ROOT] + sorted(ROOT.rglob("*"), key=lambda p: p.relative_to(ROOT).as_posix())
assert actual == objects
for path, entry in zip(actual, entries):
    info = path.lstat()
    assert format(stat.S_IMODE(info.st_mode), "04o") == entry["mode_octal"]
    assert info.st_mtime_ns == entry["mtime_ns"]
    if entry["kind"] == "directory":
        assert stat.S_ISDIR(info.st_mode) and (not any(path.iterdir())) == entry["empty"]
    else:
        assert stat.S_ISREG(info.st_mode)
        data = path.read_bytes()
        assert len(data) == entry["bytes"] and (not data) == entry["empty"]
        if entry["sha256"] is not None:
            assert hashlib.sha256(data).hexdigest() == entry["sha256"]
assert digest("FINAL_MANIFEST.json") == seal["manifest_sha256"]
print(json.dumps({"freeze_UTC": freeze_utc, "files": file_count, "child_directories": child_dirs,
                  "status": seal["status"], "external_sha256": {name: digest(name) for name in
                  ("FINAL.json", "REPORT.md", "FINAL_MANIFEST.json", "FINAL_SEAL.json")}}, indent=2))
