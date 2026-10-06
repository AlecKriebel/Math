#!/usr/bin/env python3
"""Self-excluding manifest of this family's first-party audit artifacts only."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
EXCLUDED = "FIRST_PARTY_MANIFEST.json"
records = []
for path in sorted(HERE.iterdir()):
    if not path.is_file() or path.name == EXCLUDED:
        continue
    raw = path.read_bytes()
    records.append({"path": path.name, "bytes": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest()})
early = next(x for x in records if x["path"] == "EARLY_INDEPENDENT_RECONSTRUCTION.md")
assert early["sha256"] == "3b44e662a84376d5f9fb989476d8813c70e486eb602116123e64ad40536dcaf7"
frozen = json.loads((HERE.parent / "snapshot_manifest.json").read_text())
for original in frozen["files"]:
    raw = (HERE.parent / "source_snapshot" / original["path"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == original["sha256"]
    assert len(raw) == original["bytes"]
repo = HERE.parents[3]
branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=repo, text=True).strip()
assert branch == "main", branch
ignored = subprocess.run(["git", "check-ignore", str(HERE / "tmp")], cwd=repo,
                         capture_output=True, text=True)
assert ignored.returncode == 0
data = {"utc": datetime.now(timezone.utc).isoformat(), "scope": "First-party potential-family artifacts only",
        "self_excluded": EXCLUDED, "excluded_trees": ["tmp/"],
        "foreign_downloads_renderings_and_replays_only_in_ignored_tmp": True,
        "main_branch_confirmed": True, "frozen_original17_unchanged_at_close": True,
        "artifacts": records}
(HERE / EXCLUDED).write_text(json.dumps(data, indent=2) + "\n")
print("Manifested %d first-party artifacts; sealed reconstruction and frozen original17 unchanged; main confirmed." % len(records))
