"""Verify all public packet bytes, including immutable author and review bindings."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
counts = {}
for name in ["TURN_1_MANIFEST.json", "TURN_2_MANIFEST.json", "TURN_3_MANIFEST.json",
             "TURN_4_MANIFEST.json", "TURN_5_MANIFEST.json", "FREEZE_MANIFEST.json",
             "REVIEW_MANIFEST.json", "PUBLICATION_MANIFEST.json"]:
    manifest = json.loads((root / name).read_text())
    for item in manifest["files"]:
        data = (root / item["path"]).read_bytes()
        assert len(data) == item["bytes"], (name, item["path"], "bytes")
        assert hashlib.sha256(data).hexdigest() == item["sha256"], (name, item["path"], "sha256")
    counts[name] = len(manifest["files"])
assert (root / "FREEZE_MANIFEST.json").read_bytes() == (root / "TURN_5_MANIFEST.json").read_bytes()
status = json.loads((root / "REVIEWED_STATUS.json").read_text())
assert status["original_target_resolved"] is False and status["turns_used"] == 5
assert status["status"] == "unsolved" and status["review_verdict"] == "PASS_SCOPED_PARTIALS_ORIGINAL_UNSOLVED"
for key, name in [("author_freeze_sha256", "FREEZE_MANIFEST.json"),
                  ("review_sha256", "REVIEW.md"),
                  ("review_manifest_sha256", "REVIEW_MANIFEST.json")]:
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == status[key]
assert not any(f.suffix in {".pdf", ".sqlite", ".db"} for f in root.rglob("*"))
print(json.dumps({"verified_overlapping_manifest_counts": counts,
                  "original_target_resolved": False, "turns_used": 5}, indent=2, sort_keys=True))
