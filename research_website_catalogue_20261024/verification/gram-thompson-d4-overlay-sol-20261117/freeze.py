"""Seal the finite owned overlay packet, retaining intended overlay file modes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path(__file__).resolve().parent
assert ROOT.name == "gram-thompson-d4-overlay-sol-20261117"
assert (ROOT / "builder.exit.txt").read_text() == "0\n"
assert json.loads((ROOT / "FIXED_INPUTS_AFTER.json").read_text())["before_after_exact"]
assert json.loads((ROOT / "WEBSITE_AFTER.json").read_text())["before_after_exact"]
final = json.loads((ROOT / "FINAL.json").read_text())
assert final["status"] == "PRIVATE_OVERLAY_PREPARED_PENDING_INDEPENDENT_AUDIT"
assert final["publication_or_future_active_mode_authority"] is False
targets = json.loads((ROOT / "TARGETS.json").read_text())["changes"]
for target in targets:
    path = ROOT / "overlay" / target["path"]
    assert len(path.read_bytes()) == target["bytes"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == target["SHA256"]
    assert oct(stat.S_IMODE(path.stat().st_mode)) == target["mode"]
TERMINALS = {"MANIFEST.json", "SEAL.json"}
assert all(not (ROOT / name).exists() for name in TERMINALS)
handles = {name: (ROOT / name).open("xb") for name in sorted(TERMINALS)}
freeze_ns = time.time_ns()
freeze_utc = datetime.datetime.fromtimestamp(freeze_ns / 1_000_000_000, datetime.timezone.utc).isoformat()
for name in TERMINALS:
    os.chmod(ROOT / name, 0o644)
    os.utime(ROOT / name, ns=(freeze_ns, freeze_ns))
objects = [ROOT] + sorted(ROOT.rglob("*"), key=lambda p: p.relative_to(ROOT).as_posix())
entries = []
for path in objects:
    rel = "." if path == ROOT else path.relative_to(ROOT).as_posix()
    info = path.lstat()
    assert stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode), str(path)
    entry = {"path": rel, "mode": oct(stat.S_IMODE(info.st_mode)), "mtime_ns": info.st_mtime_ns,
             "hidden": any(x.startswith(".") for x in Path(rel).parts if x != ".")}
    if stat.S_ISDIR(info.st_mode):
        entry.update(kind="directory", empty=not any(path.iterdir()))
    else:
        data = path.read_bytes()
        entry.update(kind="file", bytes=len(data), empty=not data)
        if rel in TERMINALS:
            entry["content_hash_exclusion"] = "Already-created exact terminal pair only; complete object/mode/mtime/bytes/topology retained"
        else:
            entry["SHA256"] = hashlib.sha256(data).hexdigest()
    entries.append(entry)
files = sum(e["kind"] == "file" for e in entries)
dirs = sum(e["kind"] == "directory" for e in entries) - 1
assert (files, dirs) == (41, 6), (files, dirs)
digest = lambda name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
manifest = {"schema": "finite-owned-private-overlay-namespace-v1", "scope": str(ROOT), "freeze_UTC": freeze_utc,
            "file_count": files, "child_directory_count": dirs, "root_including_directory_count": dirs + 1,
            "logical_freeze_individual_modes_retained": True,
            "terminal_content_hash_exclusions_exact": sorted(TERMINALS), "entries": entries}
seal = {"schema": "finite-private-three-paper-overlay-seal-v1", "scope": str(ROOT), "freeze_UTC": freeze_utc,
        "status": "PRIVATE_OVERLAY_FROZEN_PENDING_INDEPENDENT_ACTUAL_AUDIT_ROOT_ADOPTION", "completion_percent": 100,
        "file_count": files, "child_directory_count": dirs, "physical_overlay_files": 15,
        "target_A_M": [13, 2], "projected_public_files_childdirs_articles_XMLURLs": [816, 390, 136, 137],
        "all_bounded_guards_and_complete_old_aggregate_preservation_exact": True,
        "builder_attempts": 1, "builder_exit": 0, "repair_or_retry_count": 0,
        "whole_public_or_W_copies": 0, "native_scientific_source_oldhelper_execution": 0,
        "W_mutation_Git_network_Sheet_server_install_deploy_operations": 0,
        "FINAL_SHA256": digest("FINAL.json"), "REPORT_SHA256": digest("REPORT.md"),
        "TARGETS_SHA256": digest("TARGETS.json"), "manifest_SHA256": "0" * 64,
        "page_publication_date": None, "AA": None, "redirect": None, "follow_up": None,
        "publication_or_future_active_mode_authority": False, "stop": True}
encode = lambda value: (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()
for _ in range(20):
    manifest_bytes = encode(manifest)
    seal["manifest_SHA256"] = hashlib.sha256(manifest_bytes).hexdigest()
    seal_bytes = encode(seal)
    sizes = {"MANIFEST.json": len(manifest_bytes), "SEAL.json": len(seal_bytes)}
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
for name, data in (("MANIFEST.json", manifest_bytes), ("SEAL.json", seal_bytes)):
    handles[name].write(data)
    handles[name].flush()
    os.fsync(handles[name].fileno())
    handles[name].close()
    os.utime(ROOT / name, ns=(freeze_ns, freeze_ns))
actual = [ROOT] + sorted(ROOT.rglob("*"), key=lambda p: p.relative_to(ROOT).as_posix())
assert actual == objects
for path, entry in zip(actual, entries):
    info = path.lstat()
    assert oct(stat.S_IMODE(info.st_mode)) == entry["mode"] and info.st_mtime_ns == entry["mtime_ns"]
    if entry["kind"] == "directory":
        assert stat.S_ISDIR(info.st_mode) and (not any(path.iterdir())) == entry["empty"]
    else:
        assert stat.S_ISREG(info.st_mode)
        data = path.read_bytes()
        assert len(data) == entry["bytes"] and (not data) == entry["empty"]
        if "SHA256" in entry:
            assert hashlib.sha256(data).hexdigest() == entry["SHA256"]
assert digest("MANIFEST.json") == seal["manifest_SHA256"]
print(json.dumps({"freeze_UTC": freeze_utc, "files": files, "child_directories": dirs,
                  "status": seal["status"], "external_SHA256": {name: digest(name) for name in
                  ("FINAL.json", "REPORT.md", "TARGETS.json", "MANIFEST.json", "SEAL.json")}}, indent=2))
