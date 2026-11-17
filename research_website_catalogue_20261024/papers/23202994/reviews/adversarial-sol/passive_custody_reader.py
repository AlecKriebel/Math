"""Passive byte/mode/topology guard for this original-only INITIAL lane.

This file hashes data and inventories filenames. It never imports, parses as
code, evaluates, compiles, or executes scientific source. It never reads
scientific support semantically or performs network operations.
"""
from pathlib import Path
import datetime
import hashlib
import json
import stat
import sys

LANE = Path(__file__).resolve().parent
SOURCE = LANE.parents[1] / "sources"
PROJECT = LANE.parents[3]


def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "md5": hashlib.md5(data).hexdigest(), "mode_octal": oct(stat.S_IMODE(path.lstat().st_mode))}


def inventory(root):
    entries = []
    for path in [root, *sorted(root.rglob("*"))]:
        info = path.lstat()
        relative = "." if path == root else path.relative_to(root).as_posix()
        kind = "directory" if stat.S_ISDIR(info.st_mode) else "file" if stat.S_ISREG(info.st_mode) else "other"
        assert kind != "other", f"Unexpected nonregular node: {path}"
        entry = {"path": relative, "kind": kind, "mode_octal": oct(stat.S_IMODE(info.st_mode)),
                 "hidden_component": any(p.startswith(".") and p not in (".", "..") for p in Path(relative).parts)}
        if kind == "file":
            entry.update({k: v for k, v in pin(path).items() if k != "path"})
        else:
            entry["empty"] = not any(path.iterdir())
        entries.append(entry)
    return entries


def main():
    phase = sys.argv[1]
    assert phase in ("before", "after")
    target = LANE / ("SOURCE_GUARD_" + phase.upper() + ".json")
    assert not target.exists(), "Refusing a guard overwrite"
    adoption = PROJECT / "verification/root-source190191-custody-adoption-20261117.json"
    adoption_pin = pin(adoption)
    assert adoption_pin["sha256"] == "9ab699b60b7ac0a9be04db1211f144ccb6db852b573a71a18aa37bb2a4fa707b"
    entries = inventory(SOURCE)
    assert sum(e["kind"] == "file" for e in entries) == 39
    assert sum(e["kind"] == "directory" for e in entries) == 16
    source_manifest = json.loads((SOURCE / "SOURCE_MANIFEST.json").read_text())
    assert source_manifest["excluded_control_files"] == ["SOURCE_MANIFEST.json", "SOURCE_FINAL.json"]
    assert [e for e in entries if e["path"] not in source_manifest["excluded_control_files"]] == source_manifest["entries"]
    outer = SOURCE / "zenodo-files/paper.pdf"
    assert pin(outer)["bytes"] == 87127
    assert pin(outer)["sha256"] == "b9e7c887787b911b55f012cc640621fedc282dd71e8c57fa01c1f9db49612d9d"
    report = {"UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(), "phase": phase,
              "source_root": str(SOURCE), "files": 39, "child_directories": 15,
              "entries": entries, "adoption_pin": adoption_pin,
              "outer_manuscript_pin": pin(outer), "scientific_source_execution": False,
              "semantic_support_reading": False, "ignore_filters": None}
    if phase == "after":
        before = json.loads((LANE / "SOURCE_GUARD_BEFORE.json").read_text())
        assert before["entries"] == entries, "Source bytes/modes/topology changed"
        report["before_after_exact"] = True
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"phase": phase, "files": 39, "child_directories": 15,
                      "adoption_sha256": adoption_pin["sha256"],
                      "before_after_exact": report.get("before_after_exact"),
                      "original_tex_candidates": [e["path"] for e in entries
                                                  if e["kind"] == "file" and e["path"].endswith(".tex")]}, indent=2))


if __name__ == "__main__":
    main()
