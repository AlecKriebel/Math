"""Read-only verification of the explicit authored-file manifest."""

from hashlib import sha256
import json
from pathlib import Path


root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_text())
names = [item["path"] for item in manifest["authored_files"]]
if len(names) != len(set(names)) or "MANIFEST.json" in names:
    raise SystemExit("Manifest membership error")
for item in manifest["authored_files"]:
    path = root / item["path"]
    if path.resolve().parent != root or path.name.startswith("_local"):
        raise SystemExit("Non-authored or external member")
    data = path.read_bytes()
    if len(data) != item["bytes"] or sha256(data).hexdigest() != item["sha256"]:
        raise SystemExit(f"Integrity mismatch: {item['path']}")
checks = json.loads((root / "CHECKS.json").read_text())
if not checks["all_pass"]:
    raise SystemExit("Recorded checks did not all pass")
print(f"PASS: {len(names)} explicit authored files; self and raw evidence excluded")
