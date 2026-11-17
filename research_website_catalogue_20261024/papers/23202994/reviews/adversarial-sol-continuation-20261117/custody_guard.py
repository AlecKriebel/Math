"""Passive exact source/old-INITIAL before/after guard; no scientific execution."""
from pathlib import Path
import datetime
import hashlib
import json
import stat
import sys

LANE = Path(__file__).resolve().parent
RECORD = LANE.parents[1]
ROOTS = {"SOURCE": RECORD / "sources", "OLD_INITIAL": RECORD / "reviews/adversarial-sol"}


def pin(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "mode": oct(stat.S_IMODE(path.lstat().st_mode))}


def snapshot(root):
    entries = []
    for path in [root, *sorted(root.rglob("*"))]:
        info = path.lstat()
        relative = "." if path == root else path.relative_to(root).as_posix()
        kind = "directory" if stat.S_ISDIR(info.st_mode) else "file" if stat.S_ISREG(info.st_mode) else "other"
        assert kind != "other"
        row = {"path": relative, "kind": kind, "mode": oct(stat.S_IMODE(info.st_mode)),
               "hidden": any(p.startswith(".") and p not in (".", "..") for p in Path(relative).parts)}
        if kind == "file":
            row.update(pin(path))
        else:
            row["empty"] = not any(path.iterdir())
        entries.append(row)
    return entries


phase = sys.argv[1]
assert phase in ("BEFORE", "AFTER")
report = {"UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(), "phase": phase, "roots": []}
for label, root in ROOTS.items():
    entries = snapshot(root)
    files = sum(e["kind"] == "file" for e in entries)
    dirs = sum(e["kind"] == "directory" for e in entries) - 1
    assert (files, dirs) == ((39, 15) if label == "SOURCE" else (20, 0))
    if label == "OLD_INITIAL":
        assert pin(root / "INITIAL_MANIFEST.json")["sha256"] == "f22ab1433b4bb4b78735502e9fd6a56d08d1fe79f59c83a59f6d123bccb90e60"
        assert pin(root / "INITIAL_SEAL.json")["sha256"] == "47614abc642716071ad5a2c00b6ced5e76d85df23c69cf459485c7d89745a0fc"
        assert entries[0]["mode"] == "0o555"
        assert all(e["mode"] == "0o444" for e in entries if e["kind"] == "file")
    row = {"label": label, "root": str(root), "files": files, "child_directories": dirs, "entries": entries}
    if phase == "AFTER":
        old = json.loads((LANE / "GUARDS_BEFORE.json").read_text())
        assert entries == next(e["entries"] for e in old["roots"] if e["label"] == label)
        row["before_after_exact"] = True
    report["roots"].append(row)
target = LANE / ("GUARDS_" + phase + ".json")
assert not target.exists()
target.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"phase": phase, "counts": [{k: r[k] for k in ("label", "files", "child_directories")} for r in report["roots"]]}, indent=2))
