"""Reproduce every finite control and verify recovered checkpoint provenance."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
summary = {"turns": {}, "checkpoint_entries": 0, "local_sources": 0}
for i in range(1, 6):
    run = subprocess.run([sys.executable, str(root / f"verify_turn{i}.py")],
                         cwd=root, check=True, capture_output=True, text=True)
    actual = json.loads(run.stdout)
    expected = json.loads((root / f"TURN_{i}_CHECKS.json").read_text())
    assert actual == expected, f"turn {i} output differs"
    summary["turns"][str(i)] = actual["assertions"]
manifest = json.loads((root / "TURN_4_MANIFEST.json").read_text())
for item in manifest["files"]:
    data = (root / item["path"]).read_bytes()
    assert len(data) == item["bytes"], item["path"]
    assert hashlib.sha256(data).hexdigest() == item["sha256"], item["path"]
    summary["checkpoint_entries"] += 1
source_manifest = root / "sources" / "RECOVERY_MANIFEST.json"
if source_manifest.exists():
    for item in json.loads(source_manifest.read_text()):
        data = (root / "sources" / item["file"]).read_bytes()
        assert item["matches_checkpoint"], item["file"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"], item["file"]
        summary["local_sources"] += 1
else:
    summary["source_note"] = "Local primary PDFs absent; source URLs and expected hashes remain in the source manifests."
summary["assertions"] = sum(summary["turns"].values())
print(json.dumps(summary, indent=2, sort_keys=True))
