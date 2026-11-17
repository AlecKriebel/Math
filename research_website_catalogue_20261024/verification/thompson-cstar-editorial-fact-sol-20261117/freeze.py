"""Finite administrative seal of this audit's owned namespace only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path(__file__).resolve().parent
assert ROOT.name == "thompson-cstar-editorial-fact-sol-20261117"
assert (ROOT / "reader.exit.txt").read_text() == "0\n"
assert json.loads((ROOT / "CUSTODY_AFTER.json").read_text())["before_after_exact"]
final = json.loads((ROOT / "FINAL.json").read_text())
assert final["status"] == "COPY_CORRECTION_REQUIRED"
assert final["full_copy_PASS"] is False and len(final["issues"]) == 1
TERMINALS = {"FINAL_MANIFEST.json", "FINAL_SEAL.json"}
assert all(not (ROOT / name).exists() for name in TERMINALS)
handles = {name: (ROOT / name).open("xb") for name in sorted(TERMINALS)}
freeze_ns = time.time_ns()
freeze_utc = datetime.datetime.fromtimestamp(
    freeze_ns / 1_000_000_000, datetime.timezone.utc
).isoformat()
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
    entry = {
        "path": rel,
        "kind": "directory" if stat.S_ISDIR(info.st_mode) else "file",
        "mode_octal": format(stat.S_IMODE(info.st_mode), "04o"),
        "mtime_ns": info.st_mtime_ns,
        "hidden_component": any(part.startswith(".") for part in Path(rel).parts if part != "."),
    }
    if entry["kind"] == "directory":
        entry["empty"] = not any(path.iterdir())
    else:
        data = path.read_bytes()
        entry["bytes"] = len(data)
        entry["empty"] = not data
        if rel in TERMINALS:
            entry["sha256"] = None
            entry["content_hash_exclusion"] = "Already-created terminal pair only; exact object, mode, timestamp, byte count and topology retained"
        else:
            entry["sha256"] = hashlib.sha256(data).hexdigest()
    entries.append(entry)

file_count = sum(e["kind"] == "file" for e in entries)
child_dir_count = sum(e["kind"] == "directory" and e["path"] != "." for e in entries)
assert file_count == 14 and child_dir_count == 0
manifest = {
    "schema": "finite-whole-owned-audit-namespace-v1",
    "scope": str(ROOT),
    "freeze_UTC": freeze_utc,
    "file_count": file_count,
    "child_directory_count": child_dir_count,
    "root_including_directory_count": child_dir_count + 1,
    "terminal_content_hash_exclusions_exact": sorted(TERMINALS),
    "entries": entries,
}
digest = lambda name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
seal = {
    "schema": "finite-private-factual-audit-seal-v1",
    "freeze_UTC": freeze_utc,
    "scope": str(ROOT),
    "status": "COPY_CORRECTION_REQUIRED_FROZEN_ROOT_ADOPTION_PENDING",
    "completion_percent": 100,
    "issue_count": 1,
    "full_copy_PASS": False,
    "scientific_manuscript_PASS_unchanged": True,
    "file_count": file_count,
    "child_directory_count": child_dir_count,
    "source55_14_writer27_1_root_inputs_before_after_exact": True,
    "data_reader_attempts": 1,
    "data_reader_exit": 0,
    "scientific_source_producer_helper_execution": 0,
    "network_Git_W_stage_Sheet_operations": 0,
    "FINAL_sha256": digest("FINAL.json"),
    "FACT_REPORT_sha256": digest("FACT_REPORT.md"),
    "manifest_sha256": "0" * 64,
    "follow_up": None,
    "publication_or_future_action_authority": False,
    "stop_for_root_adoption": True,
}
encode = lambda obj: (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()
for _ in range(20):
    manifest_bytes = encode(manifest)
    seal["manifest_sha256"] = hashlib.sha256(manifest_bytes).hexdigest()
    seal_bytes = encode(seal)
    expected_sizes = {"FINAL_MANIFEST.json": len(manifest_bytes), "FINAL_SEAL.json": len(seal_bytes)}
    changed = False
    for entry in entries:
        if entry["path"] in TERMINALS:
            size = expected_sizes[entry["path"]]
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

actual_objects = [ROOT] + sorted(ROOT.rglob("*"), key=lambda p: p.relative_to(ROOT).as_posix())
assert len(actual_objects) == len(objects)
assert [str(p) for p in actual_objects] == [str(p) for p in objects]
for path, entry in zip(actual_objects, entries):
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
print(json.dumps({
    "freeze_UTC": freeze_utc,
    "files": file_count,
    "child_directories": child_dir_count,
    "status": seal["status"],
    "external_sha256": {name: digest(name) for name in (
        "FINAL.json", "FACT_REPORT.md", "FINAL_MANIFEST.json", "FINAL_SEAL.json"
    )},
}, indent=2))
